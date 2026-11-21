# 2026-11-21_yasmin_pintent_dev_001

Owner: Yasmin Shahlamedina (sy805). Run time (UTC): 2026-11-21T15:19:24.525937+00:00

## Purpose
Pintent development run with the frozen original detector prompt. Development data only.

## Exact command
python3 defenses/pintent/defense.py --dataset defenses/pdirect/development_v2.jsonl --out experiments/pintent/2026-11-21_yasmin_pintent_dev_001 --machine-note "Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed"

## Code revision
Pintent/Pdirect code as of commit 432ed5c (since squashed into b64c02e and merged as df4182c; the code files are unchanged, see the source hashes in manifest.json), working tree clean; frozen Pintent prompt sha256 1294c928af7ea99e7c5d74a33b5af14370ac630084894a0e268f34b65defa56f.

## Input and hashes
Dataset sha256: c56eb1777b04075217220cf0f151d6c534989523385a46b8fd56469545e72120
Source sha256:
- defenses/pintent/defense.py: 37639d24abf02b7adc6ba6a5c1e59d500795610e3e5cfb66a6d402b9e41ca638
- defenses/pintent/detector_prompt.txt: 1294c928af7ea99e7c5d74a33b5af14370ac630084894a0e268f34b65defa56f
- harness.py: 85adda0c585e7226717f41381a67bdce61e016d8eec23532cc8a6872f94745fc
- defenses/pdirect/defense.py: 5b0a99efac751e2413a2b1021705b008bcb87764a2480abb753f3a0da5adc11d

## Settings and hardware
Settings: {'temperature': 0, 'seed': 424, 'num_predict': 256} (detector {'temperature': 0, 'seed': 424, 'num_predict': 256, 'num_ctx': 4096})
Hardware note: Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed
Models (Ollama):
- qwen2.5:0.5b: digest a8b0c5157701, 494.03M, Q4_K_M
- qwen2.5:1.5b: digest 65ec06548149, 1.5B, Q4_K_M

## Observations (no human labels yet)
Chosen as the frozen prompt by a rule stated before running: fewer misclassified development cases (attacks allowed plus benign blocked) wins, ties keep the original. Run 001 had 4, run 002 had 5. Attack: 22/24 blocked; benign: 22/24 allowed; 0 detector or target errors.

## Limitations
Single pass, sequential gate (not the paper's concurrent design), n=24 attack and 24 benign cases. Latency is not paired with target-only when the run is a separate pass. Human review: see experiments/pintent/2026-11-21_yasmin_review_001/README.md.
