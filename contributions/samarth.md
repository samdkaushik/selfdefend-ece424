# Samarth Kaushik — midpoint contribution

## Work completed
- Built and ran a target-only Python harness through guided development
- Connected the harness to local Qwen2.5-1.5B through Ollama
- Added dataset loading and a loop to process multiple prompts
- Logged responses, timings, timestamps, settings, errors, completion
  reasons, and output-token counts
- Verified successful-request logging and deliberate connection-failure
  logging
- Investigated a truncated benign response and revised its prompt
- Ran two benign and two direct harmful development cases
- Preserved the four-case baseline snapshot and calculated its SHA-256

## Evidence
- harness.py
- data/baseline_dev.jsonl
- logs/baseline_trace.jsonl
- logs/baseline_dev_2026-11-04.jsonl
- docs/baseline/BASELINE_REVIEW.md
- docs/baseline/BASELINE_INSTRUCTIONS.md
- docs/baseline/BASELINE_FALLBACK.md

## Remaining work
- Confirm the preliminary response-review labels.
- Share the exact baseline inputs and settings with the team.
- Compare the baseline with teammates' shadow defenses.
- Complete broader evaluation and the baseline report section.