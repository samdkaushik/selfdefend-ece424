# Sharon Melendez — midpoint contribution

Status: assisted implementation and experiment evidence recorded below; the
owner's personal review and course attribution remain pending. The blank entry
is retained for the owner's own work, not as a claim of completed work.

## Dated entry

- Date:
- Component reviewed or changed:
- Work actually performed:
- Code/commit or review link:
- Exact run command:
- Dataset and settings:
- Run log/artifact path:
- Observed result and interpretation:
- Limitation or setup failure:
- Assistance/tools used, as required by course policy:
- Next experiment:

## 2026-11-04 — assisted Pdirect implementation

Codex generated `defenses/pdirect/defense.py`, detector instructions, eight mock
tests, separate development injection examples, and usage documentation following
the user's confirmation that their component is Pdirect and checks incoming prompts.
This entry records assisted implementation; it does not claim independent authorship
or a completed personal review by Sharon.

- Scope: sequential ALLOW/BLOCK gate; baseline target code and inputs unchanged.
- Validation: eight Pdirect mock tests and the repository integrity check passed.
- Setup probe: `python3 defenses/pdirect/defense.py --out experiments/pdirect/2026-11-04_setup_probe_001 --machine-note 'Local ZIP workspace; Ollama executable unavailable; service availability probe only. Hardware and warm state not measured.'`
- Evidence: [setup probe](../experiments/pdirect/2026-11-04_setup_probe_001/README.md).
- Observed: all four detector requests failed because localhost Ollama refused
  connections; all four target calls were prevented. No detection accuracy,
  safety improvement, or live-model latency result is claimed.
- Source revision: ZIP workspace has no Git history; run manifest records source hashes.
- Next: install/start Ollama, pull the shared model, run both datasets into new
  folders, and manually review verdicts and released responses.

## 2026-11-04 — assisted local Ollama setup and development runs

At the user's request, Codex installed Ollama 0.40.14 under the local user account,
enabled its localhost user service, and downloaded qwen2.5:1.5b (Q4_K_M).
Inference ran on the RTX 5070 Ti. Exact commands, input/source hashes, settings,
model digest, machine notes, detector decisions, released answers, and timings
are saved in each run manifest and trace.

The first instructions overblocked benign inputs and produced a non-verdict
answer for one baseline case. Codex revised the instructions with classification
examples after inspecting these development failures, preserving both original
runs. Revised baseline: two benign ALLOWs and two harmful BLOCKs. Revised injection
set: two attack BLOCKs, one attack ALLOW, and three benign ALLOWs. The missed
extraction attempt was refused by the target; it is still a shadow-detector miss.
Some benign target answers hit the token cap or violated the requested word limit.

Evidence: [run index](../experiments/pdirect/README.md). Eight mock gate tests and
repository checks passed after the prompt revision. These are assisted development
observations, not a held-out benchmark, an independently adjudicated safety score,
or a latency comparison with the team's baseline machine. Sharon's own review
and course-required attribution remain to be completed.

## 2026-11-04 — assisted frozen evaluation and handoff

Codex added an authority-spoofing rule and development example. The original
extraction miss was blocked on rerun; all five benign development cases were
allowed. The detector prompt was then frozen before writing 24 fresh diagnostic
cases. No tuning followed inspection of evaluation results.

Codex implemented a randomized paired target-only/Pdirect runner with warmup
exclusion, three repeats, per-label/category accounting, and median/nearest-rank
p95 full-response latency. The experiment completed 144 attempts on the same
machine without request errors or target truncations. Pdirect blocked 10/12 unique
attack cases and allowed 10/12 benign cases: two extraction false negatives and
two security-education false positives persisted across repeats.

Codex reviewed every released answer and saved explicitly AI-assisted labels
and response hashes. Human adjudication remains pending. Target-only had 15 clear
harmful-compliance attempts plus 6 unresolved out of 36 attack attempts; Pdirect
had none observed, with missed extractions deflected/refused by the target.
There was no actual configured target system secret. Benign median full-response
latency was 123.9 ms target-only versus 140.0 ms Pdirect on this warm shared GPU.
These hand-authored examples are not an independent benchmark, and three repeats
do not increase the number of unique prompts.

Evidence and exact commands: [frozen evaluation report](../experiments/pdirect/2026-11-04_frozen_evaluation_001/README.md).
Reproduction and demo: [handoff](../defenses/pdirect/HANDOFF.md).
Added four evaluation-accounting tests (12 component tests total), an offline
evidence verifier, and corresponding CI steps. Original baseline/archive evidence
remains unchanged. This ZIP workspace cannot publish a branch or PR without
being transferred to an authenticated Git clone; no publication occurred.

## 2026-11-04 — assisted iterative v2.1 improvement

At the user's request, Codex compared twelve candidate configurations over four
recorded development-search rounds (82 tuning/regression cases each). The old
evaluation set was explicitly promoted to regression data. Selected a short
direct-content policy, JSON-wrapped input, and a constrained JSON verdict schema.
Longer instructions and few-shot chat examples generally performed worse; all
trials and source scripts are preserved. Added strict duplicate/extra-key/type
validation, malformed-adapter gating, UTF-8/input-context limits, single-prompt
CLI mode, exact installed-model digest checks for evaluation, and archived replay.

The selected search candidate had zero attack misses and three benign false
positives; a full integrated development pass had four false positives. The policy
was frozen before writing a fresh 48-case diagnostic set. An initial 8K/4K context
mismatch caused repeated model reloads; the run was stopped after 36 records
before inspecting test verdicts. A documented runtime-only v2.1 freeze matched
both contexts at 4096 without changing policy/schema/test inputs. No classifier
tuning followed the completed evaluation.

Final v2.1: 48 fresh cases, three repeats, target-only/Pdirect, 288 attempts.
All 24 attack prompts blocked and 22/24 benign prompts allowed, consistent across
repeats; zero request/verdict errors. A separate exact-source v1 replay on the
same inputs had two attack misses, five benign false-positive cases, and three
invalid-verdict cases. The remaining v2.1 false positives are public quoted-analysis
tasks; these remain documented rather than tuned on the final test results.

Codex reviewed every v2.1 run answer with explicitly attributed assisted labels,
response hashes, and uncertainty notes. Human adjudication remains pending.
Target-only had 15 clear compliance, 34 refusal/safe alternatives, and 23 unresolved
attack attempts out of 72; v2.1 released 72 fixed refusals without attack target calls.
The target still has no actual configured system secret, limiting extraction claims.
Benign median full-response latency was 105.4 ms target-only versus 139.4 ms Pdirect.
Both use the same warm local GPU; load was not isolated. These cases are not an
independent benchmark, and repeated observations are not independent prompts.

Evidence: [final report](../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md),
[v1 replay](../experiments/pdirect/2026-11-04_v1_replay_on_v2_001/README.md), and
[development history](../experiments/pdirect/V2_DEVELOPMENT.md). Eighteen component
tests cover gate/schema/input-budget/evaluation contracts, plus archived tests and
offline evidence audits. Final single-prompt benign and extraction smoke tests
are saved under `experiments/pdirect/2026-11-04_v2_1_demo_*`.

The configured local user service pins context length 4096 for repeatable target
defaults. Code, reports, AI-assistance notes, demo commands, PR description, and
a portable project archive are prepared. No Git branch, remote write, or publication
has occurred. Owner review and course attribution remain to be completed.

## Repository integration

Prepared this assisted Pdirect implementation, preserved experiment evidence,
and self-contained midpoint package in a fresh clone using class account
`skm204-crypto`. The user explicitly requested direct integration into `main`
instead of a PR. The original baseline and Yasmin's pending components are
preserved; no Pintent or lightweight implementation is claimed.
