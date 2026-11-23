# yasmin_pintent_dev_002

Owner: Yasmin Shahlamedina (sy805). Run time (UTC): 2026-11-21T15:28:58.032666+00:00

## Purpose
Pintent development run with a revised detector prompt.

## Exact command
python3 defenses/pintent/defense.py --dataset defenses/pdirect/development_v2.jsonl --out experiments/pintent/yasmin_pintent_dev_002 --machine-note "Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed"

## Code revision
Code as of commit 432ed5c (since squashed into b64c02e and merged as df4182c) with an UNCOMMITTED revised detector prompt; the exact prompt used is saved here as detector_prompt.txt and hashed in manifest.json.

## Input and hashes
Dataset sha256: c56eb1777b04075217220cf0f151d6c534989523385a46b8fd56469545e72120
Source sha256:
- defenses/pintent/defense.py: 37639d24abf02b7adc6ba6a5c1e59d500795610e3e5cfb66a6d402b9e41ca638
- defenses/pintent/detector_prompt.txt: 837ab815495038b5a156be96e0a6ae124ac9e1e4c677c6bd31f53e6f169c94c1
- harness.py: 85adda0c585e7226717f41381a67bdce61e016d8eec23532cc8a6872f94745fc
- defenses/pdirect/defense.py: 5b0a99efac751e2413a2b1021705b008bcb87764a2480abb753f3a0da5adc11d

## Settings and hardware
Settings: {'temperature': 0, 'seed': 424, 'num_predict': 256} (detector {'temperature': 0, 'seed': 424, 'num_predict': 256, 'num_ctx': 4096})
Hardware note: Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed
Models (Ollama):
- qwen2.5:0.5b: digest a8b0c5157701, 494.03M, Q4_K_M
- qwen2.5:1.5b: digest 65ec06548149, 1.5B, Q4_K_M

## Observations (no human labels yet)
Discarded, kept for the record. Attack: 22/24 blocked; benign: 21/24 allowed. The revised prompt was not used for any evaluation run.

## Limitations
Single pass, sequential gate (not the paper's concurrent design), n=24 attack and 24 benign cases. Latency is not paired with target-only when the run is a separate pass. Human review: see experiments/pintent/yasmin_review_001/README.md.
