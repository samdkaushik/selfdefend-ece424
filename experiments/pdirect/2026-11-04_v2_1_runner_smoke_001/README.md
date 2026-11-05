# Final current-runner smoke test

Two reused cases, one repeat, four measured target-only/Pdirect records. This is a software/runtime confirmation, not additional fresh evaluation evidence. The current runner successfully verified the installed frozen model digest, warmed the model, wrote UTF-8 records including Spanish text, saved source snapshots, and completed paired measurement.

The local user service now explicitly pins OLLAMA_CONTEXT_LENGTH=4096, matching the default observed in the final evaluation. Exact command, model/settings metadata, warmup, raw inputs/trace, source hashes/copies, and unresolved review template are retained. The offline evidence verifier audits this run as well.
