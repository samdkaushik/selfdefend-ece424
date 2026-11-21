# 2026-11-21_yasmin_lightweight_eval_001

Owner: Yasmin Shahlamedina (sy805). Run time (UTC): 2026-11-21T15:43:41.037143+00:00

## Purpose
qwen2.5:0.5b detector with the unchanged Pdirect prompt on the held-out evaluation file; the target stays qwen2.5:1.5b.

## Exact command
python3 defenses/pdirect/defense.py --dataset defenses/pdirect/evaluation_v2.jsonl --model qwen2.5:0.5b --out experiments/lightweight/2026-11-21_yasmin_lightweight_eval_001 --machine-note "Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed"

## Code revision
Pintent/Pdirect code at commit 432ed5c on branch yasmin/pintent-runner, working tree clean; frozen Pintent prompt sha256 1294c928af7ea99e7c5d74a33b5af14370ac630084894a0e268f34b65defa56f.

## Input and hashes
Dataset sha256: 6c669da5a80dcc38bfccd0bf89a7665d72bf10ec7edd060d709aa57971f7b7a4
Source sha256:
- defenses/pdirect/defense.py: 5b0a99efac751e2413a2b1021705b008bcb87764a2480abb753f3a0da5adc11d
- defenses/pdirect/detector_prompt.txt: c93be07ae675490a9a2f20c72c45d2295db34e340b143280d5c56a6e616d4a43
- harness.py: 85adda0c585e7226717f41381a67bdce61e016d8eec23532cc8a6872f94745fc

## Settings and hardware
Settings: {'temperature': 0, 'seed': 424, 'num_predict': 256} (detector {'temperature': 0, 'seed': 424, 'num_predict': 256, 'num_ctx': 4096})
Hardware note: Apple M1, 8 GB RAM, ollama version is 0.40.14, models warmed before run, other apps closed
Models (Ollama):
- qwen2.5:0.5b: digest a8b0c5157701, 494.03M, Q4_K_M
- qwen2.5:1.5b: digest 65ec06548149, 1.5B, Q4_K_M

## Observations (no human labels yet)
All 48 detector verdicts were valid BLOCK, 0 errors, so no response reached the target.

## Limitations
Single pass, sequential gate (not the paper's concurrent design), n=24 attack and 24 benign cases. Latency is not paired with target-only when the run is a separate pass. Human review: see experiments/pintent/2026-11-21_yasmin_review_001/README.md.
