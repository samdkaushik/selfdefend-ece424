# SelfDefend — Pdirect midpoint submission

Sharon Melendez — ECE 424

This folder contains the runnable code, selected evidence, protocol, contribution
summary, and fallback for the Pdirect contribution. Run commands from this
directory. Other team contributions are maintained in their own submissions.

## Baseline and running instructions

The target-only baseline sends prompts to local Qwen and logs responses, timing,
settings, errors, and completion details. Pdirect adds a separate shadow check:
ALLOW forwards the original prompt; BLOCK or an invalid/failed check withholds it.

Requirements: Python 3.9+, Ollama running locally, and `qwen2.5:1.5b`.
No pip dependencies. Start Ollama with `OLLAMA_CONTEXT_LENGTH=4096`.
On Windows, use `python` or `py` instead of `python3`.

```sh
ollama pull qwen2.5:1.5b
python3 harness.py
python3 defenses/pdirect/defense.py --out experiments/pdirect/NEW_RUN
```

The baseline reads [baseline_dev.jsonl](data/baseline_dev.jsonl) and appends to
`logs/baseline_trace.jsonl`. Use a new output folder for each defense run.
The preserved fallback is never overwritten.

## Trace and sanity checks

- [Recorded target-only/Pdirect trace](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/trace.jsonl)
- [Command, source/input hashes, model digest, and settings](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/manifest.json)
- [Recorded connection-failure trace](experiments/pdirect/2026-11-04_setup_probe_001/trace.jsonl)
- [Sanity-check output](SANITY_CHECKS.txt)

Named check: **`test_block_never_calls_target`** verifies that a BLOCK verdict
prevents the target call. It passed, along with all 18 component tests.
The earlier connection-failure probe recorded four failed detector requests and
zero target calls. Those failures are not counted as successful safety detections.

Verify code, trace/source hashes, pairing, review coverage, links, and fallback
without running a model:

```sh
python3 verify_submission.py
```

## Results so far

48 fresh hand-authored cases, 24 attack and 24 benign, were repeated three times
with target-only and Pdirect: 288 attempts. Pdirect blocked 24/24 attack cases
and allowed 22/24 benign cases on each repeat. Two quotation-analysis cases were
false positives; no request/verdict errors occurred.

Preliminary target-only attack review: 15 compliance, 34 refusal/safe alternatives,
and 23 unresolved out of 72 attempts. Pdirect released 72 fixed refusals without
calling the target for attacks. Response-review labels still need confirmation.
[Review notes](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/review.assisted.jsonl)
and raw responses are preserved.

Benign median/p95 full-response latency was 105.4/280.9 ms target-only and
139.4/317.4 ms Pdirect. Target-only had three truncated outputs; Pdirect had none.
This small diagnostic set does not establish general robustness. The target has
no private system secret, so extraction tests do not demonstrate actual leakage
protection. Allowed target answers can still have quality problems.

## Updated experimental protocol

- Local authorized models only. Attacker controls prompt text, not weights/server code.
- Target and standard shadow: `qwen2.5:1.5b`, Q4_K_M; planned smaller shadow:
  `qwen2.5:0.5b`.
- Temperature 0; seed 424; output cap 256; timeout 120 seconds; context 4096.
- Recorded machine: Ollama 0.40.14, WSL2, Ryzen 7 9850X3D, RTX 5070 Ti 16 GiB,
  15 GiB host-visible RAM. Warm model, shared GPU load.
- Tune on development/regression cases; keep fresh evaluation outputs separate.
  The policy was frozen before the latest 48 cases. A context mismatch prompted
  a runtime-only change before verdict inspection; no classifier tuning followed
  the final evaluation. Details are in the [freeze](defenses/pdirect/evaluation_freeze_v2_1.json).
- Randomize cases and configuration order, exclude warmup, record separate detector,
  target, and total latency; report median and nearest-rank p95. Repeats are not
  independent prompts.
- Separate direct harmful requests, overrides, extraction, manipulation, benign
  acceptance, released-answer compliance, errors, and truncation. ALLOW alone is
  not attack success. Retain unresolved review labels.
- Preserve exact inputs, sources, model/settings metadata, raw outputs, and logs.
  Select versioned/licensed sources and keep related templates in the same split
  before the broader final study. Agree a compute cap before scaling.

## Bounded contribution and next experiments

Beyond the target-only baseline, compare direct-content versus intent detection
and standard versus smaller shadows while holding target and inputs fixed.
Pdirect implementation, attack/benign tests, and latency measurements are complete
for this midpoint. This package reports Pdirect only; other configurations are
covered by their own contributions.

Next: integrate those components, confirm response labels, and compare all four
configurations on approximately 100 attack and 100 benign prompts. The current
sequential gate is a simplified setup, not the paper's concurrent release checkpoint.

## Contribution evidence

Sharon Melendez: Pdirect gate, detector instructions, structured verdicts,
error handling, tests, attack/benign evaluation, latency measurements, and the
midpoint package. Evidence is in [defense.py](defenses/pdirect/defense.py),
[detector_prompt.txt](defenses/pdirect/detector_prompt.txt), and the recorded
comparison linked above. Remaining work is broader evaluation, response-label
confirmation, and the architecture/Pdirect results sections.

The target-only [harness](harness.py) and preserved baseline trace are Samarth's
existing baseline, included to make this contribution runnable and checkable.

## Designated fallback

If a later snapshot is missing or invalid, use
[logs/baseline_dev_2026-11-04.jsonl](logs/baseline_dev_2026-11-04.jsonl).
This is the preserved four-case real-model baseline. All four requests completed;
Samarth's recorded review found compliance on both harmful requests.
The exercise ID is `benign-001` in the snapshot and `benign-exercise-001` in the
current dataset. Keep the snapshot unchanged.

SHA-256, checked by `verify_submission.py`:

```text
e18641021a86a4e669c0e425803a7f9507dc88e94d52cca20ee90e64ac27ad5f
```

The fallback supports the baseline milestone; it does not replace missing defense
results. Report an invalid defense trace rather than retaining its result claims.
