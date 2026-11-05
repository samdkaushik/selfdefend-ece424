# Yasmin Shahlamedina — midpoint contribution

Status: pilot evidence prepared; implementation and second-reviewer labels pending.

## Dated entry

- Date: November 5, 2026
- Component reviewed or changed: PROMPTS["intent"] and the lightweight_pdirect path in the team-zip harness (no code changes). Harness copy: harness_used.py, sha256 cf44f514fa79a0ac2ee7cefb4aa9b054fd3cec9e3c3daa8f5aa164baebd05ad8
- Work actually performed: ran the offline checks (selftest, unit tests, fallback verify), all passed on my Mac; installed Ollama 0.40.14 and pulled qwen2.5:1.5b and qwen2.5:0.5b; ran the 4-prompt pilot twice (run 001 cold, run 002 warmed), both passed harness verify; labeled all 16 rows in each run's review.csv (reviewer sy805); prepared the runs, labels and READMEs under experiments/ and defenses/ on branch yasmin/pintent for a pull request. Not done yet: repo-native detector code in defenses/pintent/, second-reviewer labels, 20+20 or held-out runs.
- Code/commit or review link: pull request https://github.com/samdkaushik/selfdefend-ece424/pull/2
- Exact run command: python3 harness.py run --mode ollama --dataset data/pilot_dev.jsonl --target qwen2.5:1.5b --shadow qwen2.5:1.5b --light qwen2.5:0.5b --out runs/yasmin_pilot_00N (N = 1 or 2; run from my local copy of the team-zip folder)
- Dataset and settings: data/pilot_dev.jsonl, sha256 6651e0ceafa535d20b96a192616668e95ecc5f2e42fd64a3c911558a544c3d78 (4 prompts: 2 attack, 2 benign); qwen2.5:1.5b (65ec06548149) target and standard shadow, qwen2.5:0.5b (a8b0c5157701) smaller shadow; seed 424; Apple M1, 8 GB, Ollama 0.40.14
- Run log/artifact path: experiments/pintent/ and experiments/lightweight/ (2026-11-04_yasmin_pilot_001, trace sha256 0e448786246558eac76525cc464f75b5873f78d6cfd316247ff2a851a7b2f8a4; 2026-11-05_yasmin_pilot_002, trace sha256 8b546df7d079d69939b644733a3c9e22765616c407c13ec0e79e237b8a344c0f)
- Observed result and interpretation: pintent blocked 2/2 attacks and allowed 1/2 benign; lightweight_pdirect blocked 2/2 attacks and 0/2 benign; decisions identical across both runs. pdirect also blocked all four, so the pilot cannot show whether the smaller shadow retains most of the standard shadow's behavior. Setup evidence only. Details in defenses/pintent/README.md and defenses/lightweight/README.md.
- Limitation or setup failure: four prompts; inputs differ from the experiments/pdirect runs so no comparison is claimed; sequential gate, not the paper's concurrent design; one reviewer so far; run 001 had a 34.9 s cold-start detector call.
- Assistance/tools used, as required by course policy: the harness and starter docs were generated with AI assistance; Claude guided my setup and helped me interpret outputs. I ran the commands and labeled the rows myself.
- Next experiment: 20+20 dev set on the same inputs as Pdirect; compare pintent and lightweight_pdirect against pdirect, reporting detector errors separately.
