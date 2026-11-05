# Yasmin — midpoint pilot evidence

Source: [PR #2](https://github.com/samdkaushik/selfdefend-ece424/pull/2), commit
`ce707a6`. Files are copied unchanged; the PR remains separate and unmerged.
See [contribution.md](contribution.md) and [provenance.json](provenance.json).

## Work completed

- Set up Ollama 0.40.14 and both Qwen model sizes on an Apple M1, 8 GB
- Ran two four-prompt pilots: one cold, one warmed
- Each run contains target-only, Pdirect, Pintent, and lightweight-direct rows
- Labeled the 16 records in each run as reviewer sy805

## Evidence

- [First run](2026-11-04_yasmin_pilot_001/README.md)
- [Second run](2026-11-05_yasmin_pilot_002/README.md)
- Each folder includes the exact harness, inputs, manifest, trace, summary, and review CSV

## Results and remaining work

Pintent blocked 2/2 attacks and allowed 1/2 benign prompts. Lightweight-direct
blocked 2/2 attacks and allowed 0/2 benign prompts. Decisions matched across runs.
These are setup pilots, not comparable to Sharon's different inputs and hardware.
The same runs were filed under both components in PR #2; they are counted once here.

Harness, input, trace, and summary hashes match both original manifests.
Both `review.csv` hashes differ from their manifest entries; see
[manifest_audit.json](manifest_audit.json). Original files are preserved and the
package verifier reports this mismatch. Manifest review hashes need refreshing
before claiming complete integrity verification of the labeled runs.

Repo-native Pintent/lightweight detectors, second-reviewer labels, and a larger
shared-input evaluation remain pending.
