# Experiment log - November 3, 2026

## M0 - release-gate and fail-closed sanity check

- Operator: Codex-assisted execution in this session; not attributed as completed work by any team member.
- Actual run command: `python3 outputs/selfdefend_midpoint/harness.py run --mode mock --out outputs/selfdefend_midpoint/runs/fallback_sanity` (from the chat workspace).
- Dataset: `data/sanity.jsonl`; four explicitly synthetic fixtures.
- Configurations: target_only, pdirect, pintent, lightweight_pdirect.
- Seed: 424. No model server, downloads, GPU, external API, or credentials used.
- Results: 16 records; 7 toy target calls; 9 defended blocks; 6 injected detector errors; 0 target errors. All expected outcomes verified.
- Interpretation: allowed prompts pass through; blocked, malformed, and timed-out detector cases prevent target release. This says nothing about an LLM's ability to detect harmful intent.
- Timing/ASR/benign usefulness: not measured; summary values are null.
- Fallback trace SHA-256: `34e5401c44274d75ce647579e2c300171d159e07d328c2630dcb0f934efaa5dd`.
- Exact timestamp and environment: `runs/fallback_sanity/manifest.json`.

## M1 - software contract and corruption checks

- Actual commands and complete output: `runs/fallback_sanity/checks.txt`.
- Six unit tests passed, including eight parser cases; full fixture matrix; an altered-trace hash rejection; malformed/incomplete Ollama responses; target timeout logging; detector timeout blocking; duplicate-ID and endpoint/model validation.
- Ollama adapter tests use mocked HTTP replies; no live integration was verified.

## L0 - real-model pilot (pending)

- Models/digests/hardware: not selected.
- Dataset source/version/license and dev/eval manifests: pending.
- Next action: team installs/selects authorized local models, records model details and runtime budget, runs 2-4 development cases, and reviews the resulting trace before scaling up.
- Team work evidence: pending for all three members; see TEAM_EVIDENCE.md.
