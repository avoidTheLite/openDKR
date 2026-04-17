#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CASE_DIR="${REPO_ROOT}/validation/test-cases"
RESULT_ROOT="${REPO_ROOT}/validation/reports/test-case-results"

mkdir -p "${RESULT_ROOT}"

for case_file in "${CASE_DIR}"/*.json; do
  case_name="$(basename "${case_file}" .json)"
  case_out_dir="${RESULT_ROOT}/${case_name}"
  case_history_dir="${case_out_dir}/history"
  case_archive_dir="${case_out_dir}/archive"
  mkdir -p "${case_history_dir}" "${case_archive_dir}"

  echo "Running token metrics for test case: ${case_name}"
  python3 "${REPO_ROOT}/tools/collect_token_metrics.py" \
    --repo-root "${REPO_ROOT}" \
    --trace-file "validation/test-cases/${case_name}.json" \
    --budget-file "validation/metrics/TOKEN_BUDGETS.md" \
    --latest-output "validation/reports/test-case-results/${case_name}/token-usage-latest.json" \
    --flow-summary-output "validation/reports/test-case-results/${case_name}/flow-token-summary-latest.json" \
    --history-dir "validation/reports/test-case-results/${case_name}/history" \
    --archive-dir "validation/reports/test-case-results/${case_name}/archive"
done

echo "All test cases completed. Results in ${RESULT_ROOT}"
