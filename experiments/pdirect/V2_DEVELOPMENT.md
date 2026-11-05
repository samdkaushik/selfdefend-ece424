# V2 development decisions

Four rounds tested twelve candidate configurations on 82 development/regression cases each (984 detector calls). These are reused tuning observations, not unseen evaluation accuracy.

| Round | Candidate | Misses | Benign blocks | Errors | Score |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | v1_reference | 2 | 3 | 2 | 11 |
| 1 | v2_schema_policy | 0 | 5 | 0 | 5 |
| 1 | v2_schema_examples | 4 | 2 | 0 | 10 |
| 2 | v2_policy_clarified | 0 | 3 | 0 | 3 |
| 2 | v2_policy_compact | 0 | 3 | 0 | 3 |
| 2 | v2_action_summary | 0 | 5 | 0 | 5 |
| 3 | v2_compact_control | 0 | 3 | 0 | 3 |
| 3 | v2_compact_contrasts | 0 | 11 | 0 | 11 |
| 3 | v2_compact_boundary | 0 | 13 | 0 | 13 |
| 4 | v2_compact_raw | 4 | 17 | 0 | 25 |
| 4 | v2_compact_delimited | 1 | 6 | 0 | 8 |
| 4 | v2_compact_five_examples | 8 | 1 | 0 | 17 |

Selected the compact schema-constrained classifier with JSON-wrapped user input. It caught every development attack, with three benign blocks and no malformed verdicts. More examples, longer boundary instructions, raw input, and delimited input generally performed worse; all trials remain available.

The policy and source were frozen before authoring the new 48-case dataset. An 8K-detector/4K-target context mismatch caused repeated model reloads; the first evaluation was stopped after 36 records before any verdict inspection. A runtime-only v2.1 freeze matched both contexts at 4096 and retained conservative byte-budget rejection. The policy/schema and evaluation cases were not changed in response to test outcomes. The compact policy had already been tested at 4096 in development. No further classifier changes followed the completed evaluation.

The integrated 48-case development confirmation is in `2026-11-04_v2_integrated_dev_001`. The v1 prompt/freezes, original frozen study, discarded candidates, and aborted probe are preserved. Results do not guarantee robustness against adaptive attacks, long contexts, or other datasets.
