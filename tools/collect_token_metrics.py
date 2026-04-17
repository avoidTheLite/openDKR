#!/usr/bin/env python3
"""
Collect routing token metrics from routing trace data.

Input trace format (JSON):
{
  "run_id": "...",
  "timestamp": "...",
  "repo_sha": "...",
  "runner": "...",
  "model": "...",
  "executions": [
    {
      "domain_id": "...",
      "route_id": "...",
      "selected_target": "...",
      "adjudication_used": false,
      "confidence_score": 0.9,
      "latency_ms": 123,
      "prompt_tokens": 100,          # optional
      "completion_tokens": 20,       # optional
      "context_files": [
        "domains/example/knowledge/PRODUCT_CONTEXT.md"
      ]
    }
  ]
}
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import shutil
from pathlib import Path
from statistics import quantiles
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def estimate_tokens(char_count: int) -> int:
    # Stable cross-run estimate. Replace with provider counts when available.
    return int(math.ceil(char_count / 4.0))


def parse_budget_markdown(path: Path) -> dict[str, float]:
    budgets: dict[str, float] = {}
    key_val_re = re.compile(r"-\s+`([^`]+)`:\s+([0-9]+(?:\.[0-9]+)?)")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = key_val_re.match(line.strip())
        if m:
            budgets[m.group(1)] = float(m.group(2))
    return budgets


def p95(values: list[int]) -> int:
    if not values:
        return 0
    if len(values) == 1:
        return values[0]
    # inclusive keeps stable behavior for smaller sets
    return int(quantiles(values, n=100, method="inclusive")[94])


def collect_metrics(repo_root: Path, trace: dict[str, Any], budgets: dict[str, float]) -> dict[str, Any]:
    executions = trace.get("executions", [])
    file_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    route_token_totals: dict[str, int] = {}
    route_samples: dict[str, list[int]] = {}
    budget_violations: list[dict[str, Any]] = []
    split_recommendations: list[dict[str, Any]] = []

    for exec_row in executions:
        route_id = exec_row.get("route_id", "unknown-route")
        context_files = exec_row.get("context_files", [])
        context_total = 0
        per_file_rows: list[dict[str, Any]] = []

        for rel_path in context_files:
            file_path = (repo_root / rel_path).resolve()
            if not file_path.exists():
                continue
            if file_path.suffix.lower() != ".md":
                continue

            content = file_path.read_text(encoding="utf-8")
            char_count = len(content)
            token_est = estimate_tokens(char_count)
            context_total += token_est
            per_file_rows.append(
                {
                    "file_path": rel_path,
                    "file_type": "markdown",
                    "raw_char_count": char_count,
                    "estimated_tokens": token_est,
                    "included_by": "route_required_context",
                }
            )

        prompt_tokens = exec_row.get("prompt_tokens")
        completion_tokens = exec_row.get("completion_tokens")
        provider_total = None
        token_source = "estimated"

        if isinstance(prompt_tokens, int) and isinstance(completion_tokens, int):
            provider_total = prompt_tokens + completion_tokens
            token_source = "provider_reported"

        total_tokens = provider_total if provider_total is not None else context_total

        for row in per_file_rows:
            if context_total > 0:
                row["percent_of_route_context"] = round(row["estimated_tokens"] / context_total, 4)
            else:
                row["percent_of_route_context"] = 0.0
            row["route_id"] = route_id
            row["domain_id"] = exec_row.get("domain_id")
            file_rows.append(row)

            share = row["percent_of_route_context"]
            if share >= budgets.get("single_file_share_block", 0.60):
                budget_violations.append(
                    {
                        "severity": "blocking",
                        "type": "single_file_share_block",
                        "route_id": route_id,
                        "file_path": row["file_path"],
                        "value": share,
                    }
                )
            elif share >= budgets.get("single_file_share_warn", 0.40):
                budget_violations.append(
                    {
                        "severity": "warning",
                        "type": "single_file_share_warn",
                        "route_id": route_id,
                        "file_path": row["file_path"],
                        "value": share,
                    }
                )

        if total_tokens >= budgets.get("hard_budget_tokens", 9000):
            budget_violations.append(
                {
                    "severity": "blocking",
                    "type": "route_hard_budget",
                    "route_id": route_id,
                    "value": total_tokens,
                }
            )
        elif total_tokens >= budgets.get("soft_budget_tokens", 6000):
            budget_violations.append(
                {
                    "severity": "warning",
                    "type": "route_soft_budget",
                    "route_id": route_id,
                    "value": total_tokens,
                }
            )

        route_rows.append(
            {
                "domain_id": exec_row.get("domain_id"),
                "route_id": route_id,
                "selected_target": exec_row.get("selected_target"),
                "adjudication_used": bool(exec_row.get("adjudication_used", False)),
                "confidence_score": exec_row.get("confidence_score"),
                "latency_ms": exec_row.get("latency_ms"),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "token_source": token_source,
            }
        )
        route_token_totals[route_id] = route_token_totals.get(route_id, 0) + total_tokens
        route_samples.setdefault(route_id, []).append(total_tokens)

    route_token_p95 = {route_id: p95(samples) for route_id, samples in route_samples.items()}

    flow_token_summary = []
    for row in route_rows:
        flow_token_summary.append(
            {
                "flow_id": row.get("route_id"),
                "domain_id": row.get("domain_id"),
                "route_id": row.get("route_id"),
                "selected_target": row.get("selected_target"),
                "adjudication_used": row.get("adjudication_used"),
                "token_source": row.get("token_source"),
                "total_tokens": row.get("total_tokens"),
            }
        )

    top_context_files_by_tokens = sorted(
        file_rows, key=lambda row: row.get("estimated_tokens", 0), reverse=True
    )[:10]

    for row in top_context_files_by_tokens:
        if row.get("percent_of_route_context", 0) >= budgets.get("single_file_share_warn", 0.40):
            split_recommendations.append(
                {
                    "route_id": row.get("route_id"),
                    "file_path": row.get("file_path"),
                    "reason": "single_file_context_share_high",
                    "recommendation": "Split or summarize this markdown file and narrow required_context.",
                }
            )

    summary = {
        "route_token_totals": route_token_totals,
        "route_token_p95": route_token_p95,
        "top_context_files_by_tokens": top_context_files_by_tokens,
        "flow_count": len(flow_token_summary),
        "flow_token_total": sum(item.get("total_tokens", 0) or 0 for item in flow_token_summary),
    }

    return {
        "run": {
            "run_id": trace.get("run_id") or f"run-{dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "timestamp": trace.get("timestamp") or dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "repo_sha": trace.get("repo_sha"),
            "runner": trace.get("runner", "unknown"),
            "model": trace.get("model"),
            "token_source": "mixed",
        },
        "summary": summary,
        "route_executions": route_rows,
        "flow_token_summary": flow_token_summary,
        "file_token_breakdown": file_rows,
        "budget_violations": budget_violations,
        "split_recommendations": split_recommendations,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect routing token metrics from route traces.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument(
        "--trace-file",
        default="validation/reports/route-trace-latest.json",
        help="Input route trace JSON file.",
    )
    parser.add_argument(
        "--budget-file",
        default="validation/metrics/TOKEN_BUDGETS.md",
        help="Budget markdown file with backticked keys.",
    )
    parser.add_argument(
        "--latest-output",
        default="validation/reports/token-usage-latest.json",
        help="Latest output JSON path.",
    )
    parser.add_argument(
        "--history-dir",
        default="validation/reports/token-usage-history",
        help="History output directory.",
    )
    parser.add_argument(
        "--archive-dir",
        default="validation/reports/archive",
        help="Directory where previous latest report files are archived.",
    )
    parser.add_argument(
        "--flow-summary-output",
        default="validation/reports/flow-token-summary-latest.json",
        help="Compact flow summary output JSON path.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    trace_path = (repo_root / args.trace_file).resolve()
    budget_path = (repo_root / args.budget_file).resolve()
    latest_output_path = (repo_root / args.latest_output).resolve()
    flow_summary_output_path = (repo_root / args.flow_summary_output).resolve()
    history_dir = (repo_root / args.history_dir).resolve()
    archive_dir = (repo_root / args.archive_dir).resolve()
    history_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    trace = load_json(trace_path)
    budgets = parse_budget_markdown(budget_path)
    report = collect_metrics(repo_root, trace, budgets)

    timestamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    latest_output_path.parent.mkdir(parents=True, exist_ok=True)

    # Archive previous latest snapshot before overwriting it.
    if latest_output_path.exists():
        archived_name = f"{timestamp}-{latest_output_path.name}"
        archived_path = archive_dir / archived_name
        shutil.move(str(latest_output_path), str(archived_path))
        print(f"Archived previous latest report: {archived_path}")

    if flow_summary_output_path.exists():
        archived_flow_name = f"{timestamp}-{flow_summary_output_path.name}"
        archived_flow_path = archive_dir / archived_flow_name
        shutil.move(str(flow_summary_output_path), str(archived_flow_path))
        print(f"Archived previous flow summary: {archived_flow_path}")

    latest_output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    flow_summary_output_path.parent.mkdir(parents=True, exist_ok=True)
    compact_flow_summary = {
        "run": report.get("run", {}),
        "flow_token_summary": report.get("flow_token_summary", []),
    }
    flow_summary_output_path.write_text(json.dumps(compact_flow_summary, indent=2) + "\n", encoding="utf-8")

    history_path = history_dir / f"{timestamp}-token-usage.json"
    history_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote latest report: {latest_output_path}")
    print(f"Wrote flow summary report: {flow_summary_output_path}")
    print(f"Wrote history report: {history_path}")


if __name__ == "__main__":
    main()
