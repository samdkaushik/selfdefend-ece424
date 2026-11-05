# Frozen v1 replay on the fresh v2 set

The exact original evaluated v1 detector and runner were loaded from verified
source snapshots into a temporary source tree. The active v2.1 implementation
was not replaced. Original instructions and settings were retained. Same fresh
48-case inputs, three repeats, target-only/Pdirect pairing: 288 records.

V1 blocked 21/24 attack cases, missed 2/24, and produced an invalid verdict on 1/24.
It allowed 17/24 benign cases, blocked 5/24, and produced invalid verdicts on 2/24.
These decisions were consistent across repeats: nine protocol-error attempts,
all withheld without target calls. The process exited 1 as designed for errors.
Released answers from this replay have not been reviewed.

From the repository root:

```sh
python3 defenses/pdirect/replay.py --run experiments/pdirect/2026-11-04_frozen_evaluation_001 --dataset defenses/pdirect/evaluation_v2.jsonl --out experiments/pdirect/NEW_V1_REPLAY --repeats 3 --machine-note "Describe hardware and load"
```

Exact actual command/runtime/settings are in the manifest and replay provenance;
source snapshots, frozen prompt, inputs, raw trace, unresolved review template,
summary, stdout, and stderr are preserved. Hardware is the same WSL2 Ryzen 7/
RTX 5070 Ti machine with a warm model and both contexts 4096. This run followed the
v2.1 run sequentially; version timing is not a randomized paired comparison.
See the [final comparison](../2026-11-04_v2_1_frozen_evaluation_001/README.md).
