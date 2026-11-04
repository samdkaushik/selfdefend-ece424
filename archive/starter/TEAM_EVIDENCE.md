# Individual work evidence - required before submission

The proposal identifies intended responsibilities. It does not prove completed work. The user reported starting from the proposal on November 3, 2026. No individual commits, student-run logs, or component reviews have been supplied. Initial package creation and checks were performed with Codex assistance in this session and cannot be attributed to any member as completed independent work.

| Member | Planned ownership from proposal | Planned experiments | Actual evidence supplied |
| --- | --- | --- | --- |
| Samarth Kaushik (sdk143) | Target and baseline harness; threat model/baseline sections | Target-only ASR; benign prompt test | Pending |
| Sharon Melendez (skm204) | Pdirect defense; architecture/Pdirect results | Direct defense test; latency test | Pending |
| Yasmin Shahlamedina (sy805) | Pintent and lightweight defense; comparative analysis | Intent comparison; model-size stress test | Pending |

## Minimum useful evidence to add now

Samarth: run and inspect the harness; verify the target-only path; add actual commands/output and a short explanation of the trace. If a local model is available, run a benign target pilot and record model/hardware details. Record any changes personally made.

Sharon: inspect the direct classifier prompt and release gate; reproduce the block/malformed/timeout checks; document findings and any actual change. A real direct-detector/latency pilot can follow when the models are selected. Synthetic checks should remain labeled synthetic.

Yasmin: review the intent prompt and controlled smaller-direct comparison; document selected candidate models with parameter counts/quantization and rationale; run an actual intent/smaller-model pilot when available. A documented design review is work evidence, but not an executed model experiment.

## Per-member entry template

Copy this once per person and replace all pending fields with facts:

```
Member / date:
Work actually performed:
Component/files reviewed or changed:
Commit or accessible artifact path:
Exact run command (if applicable):
Run folder and trace hash:
Observed result and interpretation:
Limitations / unresolved issue:
Assistance/tools used:
Next experiment:
```

Commit history is helpful but not the only acceptable evidence. A named, dated review note, reproducible command with output, and a specific component change are also checkable. Never backdate work or claim the planned experiments are completed. Confirm teaching staff can access any external links before upload.
