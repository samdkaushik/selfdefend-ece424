# Shared data

`baseline_dev.jsonl` is the active four-case development dataset. Each line contains a unique `id`, `label` (`benign` or `attack`), and `prompt`. Samarth's current harness reads this file from the repository root.

Use the exact same inputs/settings for baseline and defense comparisons. Current IDs: benign-exercise-001, benign-dogs-001, attack-scam-003, attack-credential-004. The November 4 preserved trace records exercise under its old ID benign-001; compare the exact prompt and consult the baseline fallback note.

These prompts were created/revised during guided development, not drawn from a validated benchmark. No held-out evaluation set is provided. Preserve an input copy/version with each future run. Assign a new ID to changed wording, and document mappings if renaming an unchanged prompt.

`sanity.jsonl` belongs to the original synthetic software checks. Keep it byte-for-byte unchanged. `archive/` contains older unused pilot/prompts/provenance templates; they are not the active dataset.
