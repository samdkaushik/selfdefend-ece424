# Pdirect v2.1 — final local evaluation

November 4, 2026. Working classroom prototype with preserved development history,
fresh diagnostic evidence, and documented limits. Human adjudication is pending.

## Result on the same fresh cases

The new detector blocked all 24 attack prompts and allowed 22 of 24 benign prompts.
Decisions were consistent across three repeats. The frozen v1 detector was replayed
on exactly the same inputs in a separate run:

| Detector outcome | V1 | V2.1 |
| --- | ---: | ---: |
| Attack cases with valid BLOCK | 21/24 | 24/24 |
| Attack cases with valid ALLOW (miss) | 2/24 | 0/24 |
| Attack cases with invalid verdict | 1/24 | 0/24 |
| Benign cases with valid ALLOW | 17/24 | 22/24 |
| Benign cases with valid BLOCK | 5/24 | 2/24 |
| Benign cases with invalid verdict | 2/24 | 0/24 |

Each case was attempted three times: **288 measured attempts per version run**
(48 cases × 3 repeats × target-only/Pdirect). V1 had nine malformed-verdict attempts
across three cases; these were withheld as technical failures, not successful
detections. V2.1 had no request or verdict errors. The version comparison concerns
detector decisions; v1 released answers have not received a new assisted review.

## What changed

The short direct-content policy classifies JSON-wrapped untrusted text. Ollama
constrains the output to a one-field decision object. The local parser also rejects
wrong types, duplicate keys, extra fields, invalid verdicts, and incomplete outputs.
Only a valid ALLOW invokes the unchanged target with the exact original prompt.
Raw output, verdict, errors, completion reason, token counts, and timings remain
separate. This is a prompted off-the-shelf classifier, not a trained safety model.

Inputs have a 3000-byte UTF-8 hard cap plus a conservative encoded-context budget;
the latter can be tighter, especially for escaped non-ASCII text. Unsupported
inputs are withheld as `detector_error`, not counted as safe detections. Both
detector and target use context 4096 to avoid repeatedly reloading the same model
at different context sizes. No target code or shared baseline inputs changed.

## Development and evaluation boundaries

Four development rounds compared twelve configurations against 82 available cases:
the original development sets, the original 24-case evaluation promoted to
regression data, and 48 new development cases. The selection criterion weighted
missed attacks twice as much as benign blocks, with errors also penalized. The
selected compact candidate had zero misses, three false positives, and no errors
in that search; an integrated 48-case development pass had four false positives,
illustrating that a seed does not guarantee identical model decisions. See the
[development record](../V2_DEVELOPMENT.md); discarded trials are retained.

The policy, schema, and implementation were frozen before authoring this new
48-case set. The first evaluation used a detector context 8192 and target context 4096,
causing repeated model reloads. It was deliberately interrupted after 36 records
before any test verdicts were inspected. A separate v2.1 runtime freeze matched
both contexts at 4096; the classifier policy and test inputs were unchanged. The
compact policy had already been tested at 4096 in development. No classifier tuning
followed the completed fresh evaluation. Thus the dataset follows the policy
freeze but predates the runtime-only v2.1 freeze; both freezes and the aborted run
are preserved rather than presenting the revision as fully preplanned.

The 48 hand-authored cases include 24 benign and 24 attack requests: ordinary
questions, security education, defensive programming, quoted analysis, direct
harmful content, safety overrides, extraction, and detector manipulation. Spanish,
base64/ROT13 requests, JSON role spoofing, and a padded extraction request appear
in the set. Categories overlap development; detector and tests share an AI-assisted
author. This is **not an independent benchmark or an estimate of general robustness**.
Three repeats are repeated observations of 48 cases, not 144 independent cases.

## Remaining errors and released-answer review

Both persistent false positives are legitimate quoted-analysis tasks: translating
a public attack sentence and explaining why a claimed classifier verdict is
untrustworthy. All eight benign security-education cases and all four defensive
programming cases were allowed. All six cases in each attack category were blocked
on all repeats. Input limits, other languages, adaptive attacks, indirect injections
with real trust boundaries, and larger independent datasets remain limitations.

`review.assisted.jsonl` records a Codex-assisted review of every answer, with
sequence identifiers, response hashes, and notes. Human adjudication remains
pending; `review.jsonl` is an untouched unresolved template for that review.

For target-only attack attempts, assisted review found **15 clear compliance,
34 refusal/safe alternatives, and 23 unresolved out of 72**. Unresolved cases omit
key requested behavior, hallucinate an unverified hidden message, output only a
verdict, or truncate while incorrectly decoding. Counts intentionally preserve
uncertainty rather than scoring every non-refusal as compliance. Pdirect returned
72 fixed refusals and made zero attack target calls. The target has no configured
private system secret, so extraction tests cannot establish actual secret-leakage
protection. These results are not a representative attack-success rate.

For benign attempts, assisted labels were 29 acceptable/43 quality-limited for
target-only and 31 acceptable/35 quality-limited/6 blocked for Pdirect. Differences
in generated wording can change quality labels despite matching prompts/settings.
Quality limitations include word-limit failures, a wrong task, misleading security
guidance, and an incorrect claimed base64 output alongside otherwise correct code.
The shadow checks input; it does not guarantee target factual accuracy or usefulness.
There were three target-only truncations and zero Pdirect target truncations.

## Latency and environment

Milliseconds, full response, warm model; nearest-rank p95. There are 72 attempts
per input label/configuration, 144 per configuration overall.

| Inputs | Target-only median / p95 | V2.1 median / p95 |
| --- | ---: | ---: |
| Benign | 105.4 / 280.9 | 139.4 / 317.4 |
| Attack | 68.7 / 679.4 | 37.2 / 47.5 |
| Mixed | 97.7 / 330.4 | 45.9 / 280.2 |

Benign median rises about 34 ms; that group includes false-positive blocks. Attack
blocks skip target generation, so the mixed median is not pure detector overhead
or proof of a general speedup. Within each run, cases and configuration order are
randomized using seed 424; warmup is logged and excluded. V1 and v2.1 were separate
sequential runs, so their latency differences are descriptive, not randomized
paired version timing. This measures neither time to first token nor monetary cost.

Ollama 0.40.14, target/shadow qwen2.5:1.5b, Q4_K_M, digest
`65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`.
Temperature 0, seed 424, output cap 256, request timeout 120 s. Both contexts 4096.
WSL2, Ryzen 7 9850X3D, 15 GiB host-visible RAM, RTX 5070 Ti 16 GiB; Ollama reported 100% GPU.
The desktop also used the GPU; load was not isolated.

## Reproduce and audit

From the repository root, with Ollama running and qwen2.5:1.5b installed:

```sh
python3 defenses/pdirect/evaluate.py --out experiments/pdirect/NEW_RUN --repeats 3 --machine-note "Describe hardware and load"
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001
```

`manifest.json` retains the exact command, settings, model/runtime metadata,
dataset hash, and source hashes. Exact inputs, instructions, freeze, warmup,
raw trace, source snapshots, summaries, and assisted reviews are preserved.
The evaluated source snapshots are immutable. The current runner additionally
specifies UTF-8 for portable future runs and rejects changed installed model
digests before inference; those guards do not alter the evaluated classifier.
The offline verifier checks pair completeness, input/source
hashes, gate invariants, summaries, review coverage, and reviewed response hashes.
See [v1 replay](../2026-11-04_v1_replay_on_v2_001/README.md) and the
[handoff](../../../defenses/pdirect/HANDOFF.md).
