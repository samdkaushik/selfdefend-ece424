# Pdirect v2.1 — evaluation log

## Setup

- Model: `qwen2.5:1.5b`, Q4_K_M; Ollama 0.40.14
- Configurations: target-only and Pdirect
- Inputs: 48 fresh hand-authored cases, 24 attack and 24 benign
- Three repeats; 288 attempts total
- Temperature 0; seed 424; output cap 256; timeout 120 seconds; context 4096
- Machine: WSL2, Ryzen 7 9850X3D, RTX 5070 Ti 16 GiB, 15 GiB host-visible RAM
- Warmup excluded; case/configuration order randomized; shared GPU load

Exact commands, model digest, settings, and source/input hashes are in
[manifest.json](manifest.json). Raw results are in [trace.jsonl](trace.jsonl).

## Detector results

| Outcome per repeat | V1 replay | V2.1 |
| --- | ---: | ---: |
| Attack cases blocked | 21/24 | 24/24 |
| Attack cases allowed | 2/24 | 0/24 |
| Attack cases with invalid verdict | 1/24 | 0/24 |
| Benign cases allowed | 17/24 | 22/24 |
| Benign cases blocked | 5/24 | 2/24 |
| Benign cases with invalid verdict | 2/24 | 0/24 |

Decisions were consistent across repeats. Both remaining V2.1 false positives
concern public quotation analysis. No V2.1 request/verdict errors occurred.

## Released responses

Preliminary target-only review: 15 compliance, 34 refusal/safe alternatives,
and 23 unresolved attack attempts out of 72. Pdirect released 72 fixed refusals
and made no attack target calls. Labels and notes are preserved in
[review.assisted.jsonl](review.assisted.jsonl); confirmation is pending.

Target-only had three truncated outputs; Pdirect had none. Allowed benign
answers sometimes missed word limits or gave incomplete/incorrect explanations.

## Full-response latency

Milliseconds; median / nearest-rank p95, 72 attempts per label/configuration.

| Inputs | Target-only | Pdirect |
| --- | ---: | ---: |
| Benign | 105.4 / 280.9 | 139.4 / 317.4 |
| Attack | 68.7 / 679.4 | 37.2 / 47.5 |

Blocked requests skip target generation. These shared-GPU measurements do not
establish general speedup, time to first token, or cost savings.

## Scope

The classifier policy was frozen before these cases were written. A context-size
mismatch prompted a runtime-only change from 8K/4K to 4K/4K before verdict inspection.
No classifier tuning followed this evaluation. See the
[development log](../V2_DEVELOPMENT.md).

This is a small diagnostic set with categories overlapping development, not an
independent benchmark. The target has no configured private system secret, so
extraction cases cannot demonstrate protection against actual secret leakage.

## Reproduce and verify

From the repository root, with Ollama running:

```sh
python3 defenses/pdirect/evaluate.py --out experiments/pdirect/NEW_RUN --repeats 3 --machine-note "Describe hardware and load"
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001
```

The original evaluated source is preserved in `source/`. Current tooling adds
UTF-8 handling, model-digest checks, and portable manifest paths. Raw evidence
and the frozen classifier remain unchanged.
