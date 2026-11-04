# Designated fallback snapshot

Use `runs/fallback_sanity/trace.jsonl` if a later snapshot is absent or fails verification.

Trace SHA-256:

```
34e5401c44274d75ce647579e2c300171d159e07d328c2630dcb0f934efaa5dd
```

Created UTC: 2026-11-03T17:13:24.442610+00:00

From the package folder:

```sh
python3 snapshots/initial/harness.py verify --out runs/fallback_sanity
```

The accompanying manifest verifies the harness, dataset, trace, summary, and original review template hashes. Integrity checks detect mismatches; they are not a digital signature proving authorship. Keep this snapshot unchanged and save new runs separately.

The fallback is a synthetic control-flow trace: 4 cases x 4 configurations = 16 records. It establishes gate/error behavior only. It is not a real-model ASR result, benign accuracy estimate, or model latency measurement. Check output is saved in `runs/fallback_sanity/checks.txt`.
