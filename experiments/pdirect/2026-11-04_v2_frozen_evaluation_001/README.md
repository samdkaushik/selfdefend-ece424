# Aborted v2 context-mismatch performance probe

The run was deliberately interrupted after observing repeated Ollama model reloads caused by detector context 8192 versus target context 4096. It is incomplete and is not scored as a completed evaluation.

36 complete records were written before interruption; manifests, source snapshots, inputs, warmup, and partial trace are preserved. No verdicts were inspected before the runtime revision. The final v2.1 policy is identical; both contexts use 4096, with conservative encoded-input budget checks. The evaluation set was written after the policy freeze and before this runtime-only revision.

Do not treat missing records or the interruption as model safety results. See the final v2.1 comparison for complete evidence.
