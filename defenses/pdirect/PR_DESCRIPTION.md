# Add Pdirect v2.1 gate and reproducible diagnostic evaluation

Incoming prompts previously reached the target without a shadow check. Add a
separate qwen2.5:1.5b classifier using JSON-framed untrusted input, constrained
verdict output, and strict parsing. Only a valid completed ALLOW calls the unchanged
baseline target with the original prompt. Malformed, failed, and oversized checks
withhold generation with distinguishable errors. Single-prompt and dataset CLIs
save reproducible evidence. The evaluation runner enforces frozen source/settings
and installed model digest; archived versions replay in isolated source trees.

A fresh 48-case diagnostic set, three repeats, and target-only/Pdirect pairing
completed 288 attempts. V2.1 blocked 24/24 attack cases and allowed 22/24 benign
cases with no verdict/request errors. Frozen v1 replay on identical inputs had
two attack misses, five benign false positives, and three invalid-verdict cases.
Both remaining v2.1 errors concern legitimate quotation analysis. This small,
AI-assisted study is not an independent benchmark or a production-security claim.

Validation: 18 component tests, six archived tests, repository integrity checks,
and offline audits of the original evaluation, final evaluation, and v1 replay.
CI is configured to run these without models. Per-answer assisted reviews retain
response hashes, uncertainty, and pending human adjudication. Exact sources,
settings, model metadata, warmup, inputs, raw traces, and discarded development
trials are preserved, including an explicitly aborted context-mismatch probe.

See [handoff](HANDOFF.md), [final report](../../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md),
and [assistance record](../../contributions/sharon.md). Inputs have a raw 3000-byte
cap plus a tighter encoded-context allowance. The target has no configured secret,
so extraction trials cannot establish actual leakage protection. No GitHub
publication has occurred; owner review and course attribution remain pending.
