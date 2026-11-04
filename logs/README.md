# Baseline evidence

- `baseline_trace.jsonl`: Samarth's append-only working log; includes earlier prompts, revisions, deliberate connection-failure checks, and multiple runs. Do not treat every row as a distinct evaluation case.
- `baseline_dev_2026-11-04.jsonl`: preserved four-case real-model development snapshot. SHA-256: `e18641021a86a4e669c0e425803a7f9507dc88e94d52cca20ee90e64ac27ad5f`.

Do not change historical IDs, responses, or settings in the snapshot. Exercise appears as benign-001 there and benign-exercise-001 in the current dataset. See `docs/baseline/` for review, instructions, and fallback details. Store new defense runs under `experiments/`.
