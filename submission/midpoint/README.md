# SelfDefend — midpoint submission

Samarth Kaushik · Sharon Melendez · Yasmin Shahlamedina — ECE 424

This folder is a self-contained midpoint package. Run commands from this folder;
the original development repository is not needed. Code, selected traces, protocol,
contribution evidence, and fallback are collected here. **The missing submission
material is Yasmin's actual work evidence**, identified below rather than invented.

## 1. Project and bounded contribution

Research question: can a shadow LLM reduce harmful target responses without
excessive benign blocking or latency? Our bounded contribution is to compare a
smaller shadow with a standard shadow, and compare direct-content (Pdirect) with
intent-based (Pintent) checking, while holding the target and inputs fixed.

The target-only baseline sends each user prompt directly to a local model and
logs its response. Beyond that baseline, Pdirect now checks the same input in a
separate shadow call. A valid ALLOW forwards the unchanged prompt; BLOCK returns
a fixed refusal. Invalid, failed, and unsupported checks withhold generation with
a distinguishable error. JSON input framing, constrained verdicts, strict parsing,
input-budget checks, and experiment logging are implemented. This sequential
gate differs from the paper's concurrent generation/release checkpoint.

Remaining bounded work: integrate Yasmin's Pintent and smaller-shadow components;
compare all four configurations on shared versioned inputs; select approximately
100 attack and 100 benign prompts for the planned final study; obtain human
adjudication of released answers; and report safety, benign utility, and latency
separately. These are final-study plans, not claims of completed midpoint work.

## 2. Runnable baseline and instructions

Requirements: Python 3.9+ and a running local Ollama installation. No pip packages
are required. Download model weights separately; they are not in this package.
Run the server with `OLLAMA_CONTEXT_LENGTH=4096` to reproduce the recorded target
context. The configured project machine already has this setting in its user service.

From this directory:

```sh
ollama pull qwen2.5:1.5b
python3 harness.py
```

On Windows, substitute `python` or `py` for `python3`. The baseline reads
[data/baseline_dev.jsonl](data/baseline_dev.jsonl) and appends new records to
`logs/baseline_trace.jsonl`. The preserved fallback file is never overwritten.
Baseline source: [harness.py](harness.py).

Run the implemented Pdirect gate using a new output folder each time:

```sh
python3 defenses/pdirect/defense.py --out experiments/pdirect/NEW_BASELINE_RUN
python3 defenses/pdirect/defense.py --prompt "Explain why multifactor authentication helps." --out experiments/pdirect/NEW_DEMO
```

The second command prints the released answer as well as saving the full trace.
See [defense.py](defenses/pdirect/defense.py) and
[detector_prompt.txt](defenses/pdirect/detector_prompt.txt). Ollama must be
reachable at `http://localhost:11434`. Unsupported input produces a check error:
there is a 3000-byte UTF-8 cap plus a potentially smaller encoded-context allowance.

## 3. Checkable trace, failure log, and sanity result

Primary midpoint trace:
[final Pdirect/target-only trace](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/trace.jsonl).
Its [manifest](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/manifest.json)
records the command, model digest, settings, hardware note, and source/input hashes.
Exact inputs, instructions, source snapshots, warmup, and summaries are alongside it.

Named sanity check: **`test_block_never_calls_target`** in
[test_defense.py](defenses/pdirect/test_defense.py). It supplies a BLOCK verdict
and verifies that the target function is never called and the result is `blocked`.
It passes. The full suite has **18 passing component tests** covering schema and
input validation, failed requests, gating, frozen-model checks, and accounting.
These mocked tests verify software behavior, not LLM detection accuracy.

A recorded real setup failure is also included:
[failure trace](experiments/pdirect/2026-11-04_setup_probe_001/trace.jsonl).
Before Ollama was installed, all four detector requests failed with connection
refused and all four target calls were withheld. This is historical failure-path
evidence, not a present-day service failure or a successful safety detection.
Its original manifest and input snapshot are preserved; that earlier implementation
is not the current frozen version.

Verify the package without Ollama or downloaded weights:

```sh
python3 verify_submission.py
```

Actual command output is saved in [SANITY_CHECKS.txt](SANITY_CHECKS.txt).
This verifies fallback integrity, the 18 tests, all 288 paired trace records,
raw verdicts, source/input hashes, gate invariants, summaries, and assisted-review
coverage. It also checks this document's local links.

## 4. Current results and updated experimental protocol

Completed midpoint comparison: **48 unique hand-authored diagnostic prompts**
(24 attack, 24 benign), three repeats, target-only and Pdirect: **288 attempts**.
Pdirect blocked all 24 attack cases and allowed 22/24 benign cases on every repeat.
The two false positives are legitimate quotation-analysis tasks. No request or
verdict-format errors occurred. These are small diagnostic results, not independent
benchmark accuracy or guaranteed injection protection.

Target-only attack-answer review found 15 clear compliance, 34 refusal/safe
alternatives, and 23 unresolved out of 72 attempts. Pdirect released 72 fixed
refusals without invoking the target for attack inputs. These are explicitly
**Codex-assisted judgments; human adjudication is pending**. Per-response notes
and hashes are in
[review.assisted.jsonl](experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/review.assisted.jsonl);
the untouched `review.jsonl` is available for human review. The target has no
configured private system secret, so extraction tests do not establish actual
secret-leakage protection. Allowed answers can still have factual/quality problems.

| Warm full-response latency | Target-only median / p95 | Pdirect median / p95 |
| --- | ---: | ---: |
| Benign inputs, 72 attempts/config | 105.4 / 280.9 ms | 139.4 / 317.4 ms |
| Attack inputs, 72 attempts/config | 68.7 / 679.4 ms | 37.2 / 47.5 ms |

Blocking skips target generation; these figures do not establish pure detector
overhead, time-to-first-token improvement, or monetary savings. Target-only had
three truncated outputs; Pdirect had none in this run.

The current protocol is:

- Local authorized models only; attacker controls input text, not weights or server code.
- Target and standard shadow: `qwen2.5:1.5b`, Q4_K_M. Planned smaller shadow:
  `qwen2.5:0.5b`. The smaller-model and Pintent comparisons are not yet supplied.
- Temperature 0, seed 424, output cap 256, timeout 120 seconds. Detector context
  4096; target server default 4096 on the recorded machine. Seeds do not guarantee
  identical responses across executions.
- Recorded setup: Ollama 0.40.14; Ryzen 7 9850X3D, 15 GiB host-visible RAM,
  RTX 5070 Ti 16 GiB, WSL2. GPU load was shared with the desktop, not isolated.
  Exact model digest and settings are in the manifest and
  [freeze](defenses/pdirect/evaluation_freeze_v2_1.json).
- Tune only on development/regression cases. The original four-case set and
  earlier diagnostic cases were used for development. The latest policy was
  frozen before these 48 fresh cases were written. An 8K/4K context mismatch
  prompted a runtime-only revision to 4K/4K before any test verdicts were inspected;
  inputs and classifier policy did not change. No tuning followed this evaluation.
- Shuffle cases and randomize configuration order within each pair using seed
  424; log and exclude warmup. Record detector, target, and end-to-end timings;
  summarize median and nearest-rank p95. Repeats are not independent prompts.
- Separate direct harmful requests, safety overrides, extraction, manipulation,
  benign acceptance, actual released-answer compliance, errors, and truncation.
  Use compliance/refusal-or-safe-alternative/unresolved answer labels with a named
  reviewer. ALLOW alone is not attack success; an error is not a safety refusal.
- For the final study, select licensed/versioned sources, keep related templates
  together across splits, agree a local-compute cap before scaling, freeze inputs
  and settings, and use a new evaluation set after any further tuning. Current
  hand-authored cases share categories with development and are not an independent
  benchmark. Preserve every run and distinguish planned work from completed work.

Reproduce the paired experiment with a new directory (the runner checks the
installed model digest against the freeze before inference):

```sh
python3 defenses/pdirect/evaluate.py --out experiments/pdirect/NEW_COMPARISON --repeats 3 --machine-note "Describe hardware, load, and warm state"
```

## 5. Individual work and remaining teammate material

| Member | Work evidenced so far | Evidence in this package | Remaining responsibility |
| --- | --- | --- | --- |
| Samarth Kaushik | Target-only Ollama harness, dataset loop, timing/error/completion logging, four-case real-model baseline | `harness.py`, shared dataset, preserved baseline trace | Threat model/baseline section, broader shared baseline comparison |
| Sharon Melendez | Pdirect workspace developed with Codex assistance: gate, detector prompt, strict verdict parsing, tests, attack/benign comparison, and latency evidence | `defenses/pdirect/`, selected experiment trace, manifest, assisted reviews | Architecture/Pdirect results, personal review and course-required attribution |
| Yasmin Shahlamedina | **No work evidence received yet**; planned ownership is not counted as completed work | Add actual files and a dated evidence note when received | Pintent and smaller-shadow implementations/comparisons; contribution/comparative analysis |

The Samarth summary reflects his recorded contribution note and baseline evidence.
The Sharon summary records the assisted implementation performed in this workspace;
it does not claim independent authorship or a personal review she has not completed.
Assisted answer labels remain explicitly attributed. The experiments were produced in a ZIP workspace without Git history; their
manifests preserve source hashes. Repository integration is handled separately
through the class account; no model credentials are included in this package.

**To complete Yasmin's section:** add her actual code, run or failure log, exact
command/settings, dated description of what she did, and any assistance disclosure.
Partial work is acceptable evidence if described accurately. Put it in this folder
and update the row above; do not replace the missing entry with planned tasks.
No completed Pintent or lightweight result is claimed in this submission draft.

## 6. Explicit fallback

If a newer snapshot is missing or invalid, the designated baseline fallback is
[logs/baseline_dev_2026-11-04.jsonl](logs/baseline_dev_2026-11-04.jsonl).
It is the preserved four-case real-model target-only trace from November 4, 2026.
Its SHA-256 is:

```text
e18641021a86a4e669c0e425803a7f9507dc88e94d52cca20ee90e64ac27ad5f
```

The verifier checks that exact hash. The trace contains two benign and two direct
harmful requests; all completed normally, and Samarth's recorded review found
harmful-request compliance on both harmful cases. The exercise ID remains
`benign-001` in the immutable trace and is `benign-exercise-001` in the current
dataset. This fallback supports the runnable-baseline milestone; it does not
replace missing Pdirect/Pintent/lightweight results or establish broad robustness.

The latest Pdirect trace is separately audited from its source/input hashes. If
that audit fails, report the failure and use the designated baseline fallback as
baseline evidence, rather than carrying forward invalid defense claims.
