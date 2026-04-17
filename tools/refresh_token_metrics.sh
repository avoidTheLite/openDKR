#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TRACE_FILE="${TRACE_FILE:-validation/reports/route-trace-latest.json}"
BUDGET_FILE="${BUDGET_FILE:-validation/metrics/TOKEN_BUDGETS.md}"
LATEST_OUTPUT="${LATEST_OUTPUT:-validation/reports/token-usage-latest.json}"
FLOW_SUMMARY_OUTPUT="${FLOW_SUMMARY_OUTPUT:-validation/reports/flow-token-summary-latest.json}"
HISTORY_DIR="${HISTORY_DIR:-validation/reports/token-usage-history}"
ARCHIVE_DIR="${ARCHIVE_DIR:-validation/reports/archive}"

python3 "${REPO_ROOT}/tools/collect_token_metrics.py" \
  --repo-root "${REPO_ROOT}" \
  --trace-file "${TRACE_FILE}" \
  --budget-file "${BUDGET_FILE}" \
  --latest-output "${LATEST_OUTPUT}" \
  --flow-summary-output "${FLOW_SUMMARY_OUTPUT}" \
  --history-dir "${HISTORY_DIR}" \
  --archive-dir "${ARCHIVE_DIR}"

