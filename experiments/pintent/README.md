# Pintent experiment evidence

Owner: Yasmin Shahlamedina. Pilot run evidence is listed under Runs below.

Create a new directory such as `2026-11-04_NAME_001/` for each run. Include a README with exact command, code revision, input dataset copy/hash, hardware, model digests/settings, logs, reviewer labels if any, and observations. Preserve failures and truncation. Do not claim a planned experiment as completed.

## Runs
- 2026-11-04_yasmin_pilot_001: cold-start pilot, 4 prompts (see its README)
- 2026-11-05_yasmin_pilot_002: warmed pilot, 4 prompts (see its README)
- yasmin_pintent_dev_001: Pintent development run, frozen original prompt (see its README)
- yasmin_pintent_dev_002: revised prompt, discarded (see its README)
- yasmin_ref_pdirect_target_001: reference run, target-only and Pdirect on the held-out evaluation file
- yasmin_pintent_eval_001: Pintent on the held-out evaluation file (frozen prompt)
- yasmin_review_001: blind human-review inputs and rubric; labels withheld until second review
