# Pdirect setup probe — 2026-11-04

This is a failed local-service setup probe, not an LLM evaluation. No model ran.
All four baseline inputs received `detector_error` with connection refused;
`target_called` is false for every record. The process exited 1 as intended.
Error fallback messages are technical failures, not model safety refusals.

From the repository root, the exact command was:

```sh
python3 defenses/pdirect/defense.py --out experiments/pdirect/2026-11-04_setup_probe_001 --machine-note 'Local ZIP workspace; Ollama executable unavailable; service availability probe only. Hardware and warm state not measured.'
```

See `inputs.jsonl`, `detector_prompt.txt`, `manifest.json`, `trace.jsonl`, and
`summary.json` in this folder. The manifest records input/source hashes,
generation settings, platform, and failed version/model metadata requests.
No model digest, quantization, cold/warm state, or GPU measurements are available.
The ZIP checkout has no commit revision. Timings measure failed connections only.

`checks.txt` records a separate actual mocked test run and repository checks.
Its eight Pdirect tests exercise software contracts; the six archived tests
exercise the preserved starter harness. Neither demonstrates model quality.
