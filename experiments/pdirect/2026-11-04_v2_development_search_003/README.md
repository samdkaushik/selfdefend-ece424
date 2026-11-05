# V2 development search round 3

Development only: 82 previously available cases (4 baseline + 6 original injection development + 24 former evaluation cases promoted to regression + 48 new development cases). Labels are never sent as case metadata to the model. Candidate demonstration labels are fixed examples, not the evaluated labels. No fresh v2 evaluation outputs were used.

Selection: minimize `2*false_negative + false_positive + 2*detector_error`; ties prefer fewer demonstrations and shorter instructions.

| Candidate | Misses | Benign blocks | Errors | Weighted score |
| --- | ---: | ---: | ---: | ---: |
| v2_compact_control | 0 | 3 | 0 | 3 |
| v2_compact_contrasts | 0 | 11 | 0 | 11 |
| v2_compact_boundary | 0 | 13 | 0 | 13 |

Run from the repository root with the shared Ollama model available: `python3 experiments/pdirect/2026-11-04_v2_development_search_003/search.py`. The script refuses to overwrite existing trace files; use a copied run folder for reproduction. Candidate JSON files preserve full messages, input encoding, and schema. `inputs.jsonl`, `runtime.json`, raw candidate traces, summary, and the executed search script are retained.

Rounds 1–2 used the server default context 4096; rounds 3–4 explicitly set detector context 8192. The compact JSON-wrapped policy scored identically at both contexts. Requests used temperature 0, seed 424, and output cap 256. Timings include warm/load differences and are not a latency benchmark. Runtime version/digests are in `runtime.json`; hardware is the same WSL2 Ryzen 7/RTX 5070 Ti machine.
