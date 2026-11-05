# Sharon Melendez — midpoint contribution

## Work completed

- Built the Pdirect shadow gate using local Qwen2.5-1.5B through Ollama
- Checked incoming prompts before forwarding them to the target
- Added structured ALLOW/BLOCK verdicts and fail-closed error handling
- Refined detector instructions using development and regression cases
- Ran 48 fresh cases with three repeats against target-only and Pdirect
- Recorded decisions, responses, errors, model settings, and latency
- Added 18 component tests and Windows/Linux evidence checks
- Collected the midpoint submission in one self-contained folder

## Evidence

- [Pdirect implementation](../defenses/pdirect/defense.py)
- [Detector instructions](../defenses/pdirect/detector_prompt.txt)
- [Evaluation inputs](../defenses/pdirect/evaluation_v2.jsonl)
- [Results and latency](../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md)
- [Development log](../experiments/pdirect/V2_DEVELOPMENT.md)
- [Midpoint submission](../submission/midpoint/README.md)

## Observed results

- Blocked 24/24 attack cases and allowed 22/24 benign cases on each repeat
- No request or verdict-format errors in the final run
- Two benign quotation-analysis cases were incorrectly blocked
- Benign median latency: 105.4 ms target-only; 139.4 ms Pdirect
- All 18 component tests pass; Windows and Linux CI pass

## Remaining work

- Confirm the preliminary response-review labels
- Compare Pdirect with Pintent and the smaller shadow on shared inputs
- Complete broader evaluation and the architecture/Pdirect report sections
