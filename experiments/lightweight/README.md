# Smaller direct shadow experiment evidence

Owner: Yasmin Shahlamedina. Pilot runs and one Nov 21 evaluation run are contributed. Review labels and metrics are
provisional until the second reviewer finishes; no retained-benefit claim is made here.

Create a new directory such as `2026-11-04_NAME_001/` for each run. Include a README with exact command, code revision, input dataset copy/hash, hardware, model digests/settings, logs, reviewer labels if any, and observations. Preserve failures and truncation. Do not claim a planned experiment as completed.

## Runs
- 2026-11-04_yasmin_pilot_001: cold-start pilot, 4 prompts (see its README)
- 2026-11-05_yasmin_pilot_002: warmed pilot, 4 prompts (see its README)
- yasmin_lightweight_eval_001: qwen2.5:0.5b detector with the unchanged Pdirect prompt
  (defenses/pdirect/defense.py --model qwen2.5:0.5b) on defenses/pdirect/evaluation_v2.jsonl, 48 cases. All 48 detector
  verdicts were valid BLOCK with no errors, so no response reached the target. Hashes, settings and hardware are in its
  manifest.json. Same-input reference runs: experiments/pintent/yasmin_ref_pdirect_target_001 (target-only
  and Pdirect) and experiments/pintent/yasmin_pintent_eval_001.
