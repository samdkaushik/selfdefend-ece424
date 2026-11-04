# SelfDefend - ECE 424 midpoint starter package

Prepared November 3, 2026 from the team's proposal. **Draft: team work evidence is still missing.**

This package supplies a runnable experiment harness and a genuine offline sanity trace. It does not contain a trained defense, real jailbreak benchmark results, or evidence that any student has completed their assigned component. Code and initial documentation were generated with Codex assistance in this session. Each teammate must run, inspect, and document their own work before claiming it.

## 1. Run without a model or dependencies

Unzip the package, open a terminal in this folder, and use Python 3.9 or newer:

```sh
python3 harness.py selftest
python3 -m unittest -v test_harness.py
python3 harness.py verify --out runs/fallback_sanity
python3 harness.py run --mode mock --out runs/my_sanity_run
python3 harness.py verify --out runs/my_sanity_run
```

Use a new output folder for every run. Existing folders are not overwritten. Nothing is downloaded, no API key is needed, and mock mode does not contact a model. The test suite also uses mocked HTTP responses, not a real Ollama server.

## 2. What has actually run

`runs/fallback_sanity/trace.jsonl` contains 4 synthetic cases x 4 configurations = 16 records. Seven records call the toy target. Nine defended records block release: three intentional toy-policy blocks, three malformed-reply blocks, and three injected-timeout blocks. Six `detector_error` records are intentional reliability checks, not unexpected model failures.

The check is named **release-gate and fail-closed sanity check**. A blocked decision must prevent the target call and release only the fixed refusal. Invalid detector JSON and a timeout must become BLOCK. An allowed case must pass through. Target-only cases bypass the shadow gate by design. Fixture replies are supplied directly by the test data, so these checks validate software wiring, not detector reasoning or prompt-injection resistance.

`runs/fallback_sanity/checks.txt` contains the actual test/verification output. `manifest.json` contains environment, settings, prompts, and SHA-256 hashes. `summary.json` explicitly leaves ASR and benign acceptability unset. Mock timing is null.

**Designated fallback:** use `runs/fallback_sanity/trace.jsonl` if a later snapshot is missing or invalid. Run the verification command above and compare the SHA-256 recorded in `FALLBACK.md`. Keep this folder unchanged; review a copy of `review.csv` if making annotations. This fallback establishes harness readiness only; it cannot replace missing real-model research results.

## 3. Four configurations

| Name | Behavior |
| --- | --- |
| `target_only` | Target answers without the shadow gate. |
| `pdirect` | Standard shadow checks direct content, then target answers if allowed. |
| `pintent` | Same standard shadow checks intent, then target answers if allowed. |
| `lightweight_pdirect` | Smaller shadow uses the same direct prompt as `pdirect`. |

Comparing `pdirect` to `lightweight_pdirect` holds the detector strategy fixed to isolate model-size effects as closely as possible. Prefer the same model family and quantization. Comparing `pdirect` to `pintent` holds the shadow model fixed. The smaller model's intent behavior is outside this bounded midpoint implementation.

This is a **simplified sequential gate**. The paper's concurrent generation, cached tokens, early release checkpoint, and distilled/fine-tuned defense weights are not implemented. Detector prompts are newly written JSON classification prompts, not verbatim paper prompts. These are project baselines inspired by SelfDefend, not a reproduction of the paper's reported results.

## 4. Connect local models later

Install/run Ollama using its official instructions, obtain authorized models, and record exact model tags/digests and hardware. The project has not selected or downloaded models. No real model call has been run here. The Ollama adapter's request/response handling has been checked with mocked responses only.

Create a curated JSONL dataset with a unique `id`, text `prompt`, `label` (`attack` or `benign`), and `split` (`dev` or `eval`) per line. Also retain benchmark source, version, family, and licensing in your dataset inventory. Do not use the toy fixture file for real experiments. Example of a harmless dev row:

```json
{"id":"benign-dev-001","label":"benign","split":"dev","prompt":"Explain why network segmentation helps defenders."}
```

Put development and held-out cases in separate files; the harness processes every row in the supplied file. Replace the model placeholders in the command with actual locally installed tags:

```sh
python3 harness.py run --mode ollama --dataset data/dev.jsonl --target TARGET_MODEL --shadow STANDARD_SHADOW_MODEL --light SMALLER_SHADOW_MODEL --out runs/dev_001
python3 harness.py verify --dataset data/dev.jsonl --out runs/dev_001
```

Only a local HTTP Ollama endpoint is supported. Temperature is 0; seed defaults to 424; generation limit is 256 tokens; each request times out after 120 seconds. These settings are recorded, but seeds do not guarantee identical results across models/hardware. Test 2-4 development cases first, review truncation and resource use, then freeze settings. Errors are logged and processing continues; inspect every run before interpreting it.

Real runs also emit `review.csv`. Review the released answer against the original task; do not label success merely because a detector allowed the prompt or because an answer lacks refusal words. Save annotations separately to preserve the original snapshot and hashes. Definitions and failure handling are in `PROTOCOL.md`; metric aggregation is currently manual.

## 5. Finish before uploading

1. Each person adds an actual component review/change and at least one reproducible run/log, using `TEAM_EVIDENCE.md`.
2. Record exact selected models, dataset sources/splits, machine, and resource budget.
3. Run a small local-model pilot if feasible; disclose the model integration as unverified until this is done.
4. Replace pending entries in the midpoint report with verified facts. Keep synthetic and live results separate.
5. Upload this folder as a ZIP together with the updated report, or publish a repository and verify that teaching staff can access it. No upload or repository publication has been performed.

## Sources

- Team's supplied project proposal (provided PDF, ECE 424, Fall 2026).
- Original project and architecture: https://selfdefend.github.io/
- Original implementation and requirements: https://github.com/selfdefend/Code
- Ollama chat request/response contract: https://docs.ollama.com/api/chat

Sources checked November 3, 2026. No original paper code, benchmark data, or model weights are redistributed in this package.
