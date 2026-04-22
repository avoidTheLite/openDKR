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
            "target_type": "domain_doc",
            "target_ref": "domains/example/knowledge/WORKAROUNDS.md",
      "adjudication_used": false,
            "confidence_floor": 0.85,
      "confidence_score": 0.9,
      "latency_ms": 123,
      "prompt_tokens": 100,          # optional
      "completion_tokens": 20,       # optional
            "intent_pattern_terms": [      # optional routing-sync validation inputs
                "known",
                "issue"
            ],
            "known_domain_terms": [
                "known",
                "issue",
                "workaround"
            ],
            "registered_targets": [
                "domains/support/interfaces/OUTBOUND.md"
            ],
            "allowed_confidence_floors": [
                0.6,
                0.85
            ],
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


def evaluate_routing_sync(repo_root: Path, exec_row: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    route_id = exec_row.get("route_id", "unknown-route")
    domain_id = exec_row.get("domain_id")

    for rel_path in exec_row.get("context_files", []):
        if not isinstance(rel_path, str):
            continue
        if not Path(rel_path).suffix.lower() == ".md":
            continue
        if not (repo_root / rel_path).exists():
            violations.append(
                {
                    "route_id": route_id,
                    "domain_id": domain_id,
                    "severity": "blocking",
                    "violation_type": "required_context_integrity",
                    "stale_field": "required_context",
                    "expected_value": "existing markdown file",
                    "actual_value": rel_path,
                }
            )

    intent_terms = [term for term in exec_row.get("intent_pattern_terms", []) if isinstance(term, str)]
    known_terms = {term for term in exec_row.get("known_domain_terms", []) if isinstance(term, str)}
    stale_terms = [term for term in intent_terms if term not in known_terms]
    if intent_terms and known_terms and stale_terms:
        violations.append(
            {
                "route_id": route_id,
                "domain_id": domain_id,
                "severity": "warning",
                "violation_type": "intent_pattern_entity_alignment",
                "stale_field": "intent_pattern",
                "expected_value": sorted(known_terms),
                "actual_value": stale_terms,
            }
        )

    target_type = exec_row.get("target_type")
    if target_type == "cross_domain":
        registered_targets = [target for target in exec_row.get("registered_targets", []) if isinstance(target, str)]
        target_ref = exec_row.get("target_ref") or exec_row.get("selected_target")
        if registered_targets and isinstance(target_ref, str) and target_ref not in registered_targets:
            violations.append(
                {
                    "route_id": route_id,
                    "domain_id": domain_id,
                    "severity": "blocking",
                    "violation_type": "cross_domain_target_existence",
                    "stale_field": "target_ref",
                    "expected_value": registered_targets,
                    "actual_value": target_ref,
                }
            )

    confidence_floor = exec_row.get("confidence_floor")
    allowed_floors = [floor for floor in exec_row.get("allowed_confidence_floors", []) if isinstance(floor, (int, float))]
    if isinstance(confidence_floor, (int, float)) and allowed_floors:
        rounded_floor = round(float(confidence_floor), 2)
        normalized_allowed = [round(float(floor), 2) for floor in allowed_floors]
        if rounded_floor not in normalized_allowed:
            violations.append(
                {
                    "route_id": route_id,
                    "domain_id": domain_id,
                    "severity": "warning",
                    "violation_type": "confidence_floor_band_alignment",
                    "stale_field": "confidence_floor",
                    "expected_value": normalized_allowed,
                    "actual_value": rounded_floor,
                }
            )

    return violations


def validate_assertions(trace: dict[str, Any], report: dict[str, Any]) -> list[str]:
    assertions = trace.get("assertions", {})
    if not isinstance(assertions, dict):
        return ["assertions must be an object when present"]

    failures: list[str] = []
    flow_rows = report.get("flow_token_summary", [])
    routing_sync_violations = report.get("routing_sync_violations", [])
    budget_violations = report.get("budget_violations", [])
    top_context_files = report.get("summary", {}).get("top_context_files_by_tokens", [])

    if "flow_count" in assertions:
        expected = assertions.get("flow_count")
        actual = len(flow_rows)
        if actual != expected:
            failures.append(f"flow_count expected {expected}, got {actual}")

    if "adjudication_used" in assertions:
        expected = assertions.get("adjudication_used")
        actual = [row.get("adjudication_used") for row in flow_rows]
        if actual != expected:
            failures.append(f"adjudication_used expected {expected}, got {actual}")

    if "routing_sync_violation_types" in assertions:
        expected = sorted(assertions.get("routing_sync_violation_types", []))
        actual = sorted(
            violation.get("violation_type")
            for violation in routing_sync_violations
            if isinstance(violation.get("violation_type"), str)
        )
        if actual != expected:
            failures.append(f"routing_sync_violation_types expected {expected}, got {actual}")

    if "routing_sync_violation_severities" in assertions:
        expected = sorted(assertions.get("routing_sync_violation_severities", []))
        actual = sorted(
            violation.get("severity")
            for violation in routing_sync_violations
            if isinstance(violation.get("severity"), str)
        )
        if actual != expected:
            failures.append(f"routing_sync_violation_severities expected {expected}, got {actual}")

    if "budget_violation_types_contains" in assertions:
        expected = assertions.get("budget_violation_types_contains", [])
        actual = {
            violation.get("type")
            for violation in budget_violations
            if isinstance(violation.get("type"), str)
        }
        missing = [value for value in expected if value not in actual]
        if missing:
            failures.append(f"budget_violation_types_contains missing {missing} from {sorted(actual)}")

    if "top_context_files_contains" in assertions:
        expected = assertions.get("top_context_files_contains", [])
        actual = {
            row.get("file_path")
            for row in top_context_files
            if isinstance(row.get("file_path"), str)
        }
        missing = [value for value in expected if value not in actual]
        if missing:
            failures.append(f"top_context_files_contains missing {missing} from {sorted(actual)}")

    if "token_sources" in assertions:
        expected = assertions.get("token_sources")
        actual = [row.get("token_source") for row in flow_rows]
        if actual != expected:
            failures.append(f"token_sources expected {expected}, got {actual}")

    if "selected_targets" in assertions:
        expected = assertions.get("selected_targets")
        actual = [row.get("selected_target") for row in flow_rows]
        if actual != expected:
            failures.append(f"selected_targets expected {expected}, got {actual}")

    return failures


def collect_metrics(repo_root: Path, trace: dict[str, Any], budgets: dict[str, float]) -> dict[str, Any]:
    executions = trace.get("executions", [])
    file_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    route_token_totals: dict[str, int] = {}
    route_samples: dict[str, list[int]] = {}
    budget_violations: list[dict[str, Any]] = []
    split_recommendations: list[dict[str, Any]] = []
    routing_sync_violations: list[dict[str, Any]] = []

    for exec_row in executions:
        route_id = exec_row.get("route_id", "unknown-route")
        context_files = exec_row.get("context_files", [])
        context_total = 0
        per_file_rows: list[dict[str, Any]] = []

        for violation in evaluate_routing_sync(repo_root, exec_row):
            actual_value = violation.get("actual_value")
            if violation.get("violation_type") == "required_context_integrity" and isinstance(actual_value, str):
                actual_path = (repo_root / actual_value).resolve()
                if actual_path.exists():
                    continue
            routing_sync_violations.append(violation)

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
        "routing_sync_violations": routing_sync_violations,
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
    assertion_failures = validate_assertions(trace, report)

    if assertion_failures:
        for failure in assertion_failures:
            print(f"ASSERTION FAILED: {failure}")
        raise SystemExit(1)

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
