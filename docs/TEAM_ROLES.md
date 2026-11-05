# Team roles

| Member | Component | Experiments / report responsibilities |
| --- | --- | --- |
| Samarth Kaushik | Target-only baseline and harness | Attack/benign baseline; sanity and failure logging; threat model, instructions, baseline review |
| Sharon Melendez | Direct-content shadow (Pdirect) | Direct defense decisions and latency; architecture and direct-results section |
| Yasmin Shahlamedina | Intent shadow and smaller-shadow comparison | Intent comparison; standard-direct versus smaller-direct; bounded contribution and comparative analysis |

Read [CONTRIBUTING.md](../CONTRIBUTING.md) before editing. Use component folders to reduce overlapping edits. Integration changes to `harness.py` and shared prompts should be agreed in a pull request.

Current evidence: Samarth's recorded baseline includes four real-model development
cases. The Pdirect v2.1 implementation and a fresh 48-case paired comparison
are available in its [handoff](../defenses/pdirect/HANDOFF.md); prior detector misses,
remaining false positives, and pending human adjudication are documented. Yasmin's [pilot evidence](../submission/midpoint/evidence/yasmin/README.md) is
available in PR #2; repo-native Pintent/lightweight code and shared-input comparisons
remain pending. Planned ownership must not be presented
as completed work.

All members contribute their own dated evidence and review the combined midpoint report. Samarth assembles the final package; Sharon checks the architecture/sanity explanation; Yasmin checks the contribution plan and experimental protocol. These assembly tasks do not replace individual technical work.
