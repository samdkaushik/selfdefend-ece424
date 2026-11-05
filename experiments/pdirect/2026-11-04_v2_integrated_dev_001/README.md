# Integrated v2 development confirmation

48 development cases; not unseen evaluation. The compact JSON-schema classifier caught all 24 attack cases, allowed 20 benign cases, and blocked four benign cases. No request errors. The detector used context8192 while the target remained4096; this was later optimized in v2.1 to avoid context-driven reloads.

Exact command:

```sh
/usr/bin/python3 defenses/pdirect/defense.py --dataset defenses/pdirect/development_v2.jsonl --out experiments/pdirect/2026-11-04_v2_integrated_dev_001 --machine-note 'WSL2 RTX 5070 Ti; schema-constrained JSON classifier, JSON-wrapped input, detector context 8192, target unchanged 4096; warm model. Development confirmation, not evaluation.'
```

Manifest, exact inputs, detector prompt, raw trace, and status summary are retained. Do not treat target-answer usefulness or these timings as independent benchmark results.
