# Pdirect experiment evidence

## Current result: v2.1

The [final report](2026-11-04_v2_1_frozen_evaluation_001/README.md) compares 48 fresh
cases, three repeats, and target-only/Pdirect: 288 attempts. V2.1 blocked 24/24
attack cases and allowed 22/24 benign cases, with no errors. The
[archived v1 replay on identical inputs](2026-11-04_v1_replay_on_v2_001/README.md)
had two attack misses, five benign false positives, and three invalid-verdict cases.
Both remaining v2.1 errors concern legitimate quotation analysis.

See [development selection](V2_DEVELOPMENT.md), the four development-search folders,
and the [aborted context-mismatch probe](2026-11-04_v2_frozen_evaluation_001/README.md).
The latter is incomplete and is not scored as an evaluation. All prior evidence
below is historical; no independent benchmark or human adjudication is claimed.

## Earlier v1 evidence

Owner: Sharon Melendez. A setup probe, six assisted development runs, and a
frozen 24-case paired comparison are available. The final instructions fix the
original development miss but still miss two fresh extraction variants and block
two benign security questions. Independent benchmarking and human adjudication
are pending.

- [Frozen evaluation report, raw evidence, and reviews](2026-11-04_frozen_evaluation_001/README.md)
- [Final baseline development run](2026-11-04_baseline_live_003/README.md)
- [Final injection development run](2026-11-04_injection_live_003/README.md)

- [Setup failure probe](2026-11-04_setup_probe_001/README.md)
- [Original baseline run](2026-11-04_baseline_live_001/README.md)
- [Original injection run](2026-11-04_injection_live_001/README.md)
- [Revised baseline run](2026-11-04_baseline_live_002/README.md)
- [Revised injection run](2026-11-04_injection_live_002/README.md)

Create a new directory such as `2026-11-04_NAME_001/` for each run. Include a README with exact command, code revision, input dataset copy/hash, hardware, model digests/settings, logs, reviewer labels if any, and observations. Preserve failures and truncation. Do not claim a planned experiment as completed.
