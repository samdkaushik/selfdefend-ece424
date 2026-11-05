# Pdirect handoff

## Current work

Pdirect checks the target prompt before generation. ALLOW calls the target;
BLOCK or a failed check withholds it. The target-only harness is unchanged.

## Start here

- [Run instructions](README.md)
- [Contribution note](../../contributions/sharon.md)
- [Results and latency](../../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md)
- [Consolidated midpoint submission](../../submission/midpoint/README.md)

## Check

```sh
python3 -m unittest discover -s defenses/pdirect -p "test_*.py" -v
python3 scripts/check_repository.py
python3 submission/midpoint/verify_submission.py
```

## Remaining work

Confirm preliminary answer labels, integrate the other defense comparisons,
and run a broader evaluation. Yasmin's work evidence is still pending.
Changes are on `sharon/pdirect-midpoint` for review in PR #1.
