# Pdirect v1 — evaluation log

## Setup

- Target/shadow: `qwen2.5:1.5b`, Q4_K_M; Ollama 0.40.14
- 24 unique cases: 12 attack, 12 benign; three repeats; 144 attempts
- Temperature 0; seed 424; output cap 256; timeout 120 seconds
- Warm model on WSL2/RTX 5070 Ti; context 4096; shared GPU load
- Policy frozen before these cases were written; warmup excluded

## Results

- Blocked 10/12 attack cases and allowed 10/12 benign cases each repeat
- Missed two extraction variants and blocked two benign security questions
- No request errors or target truncations
- Target-only preliminary attack review: 15 compliance, 15 refusal/safe alternatives,
  6 unresolved out of 36 attempts
- Pdirect blocked 30 attack attempts; the target deflected/refused the six allowed
  extractions. These remain detector misses.
- Benign median/p95 latency: 123.9/436.3 ms target-only; 140.0/468.8 ms Pdirect

## Evidence

[Manifest](manifest.json), [trace](trace.jsonl), [summary](summary.json),
[preliminary reviews](review.assisted.jsonl), and exact source snapshots in `source/`.
Review labels need confirmation. This small set is not a general robustness
benchmark; the target has no actual configured private system secret.

## Verify

From the repository root:

```sh
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_frozen_evaluation_001
```

This is historical v1 evidence. The current runner defaults to the v2.1 study;
use the archived source or replay tool to reproduce v1.
