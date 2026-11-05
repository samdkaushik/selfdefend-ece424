# Pdirect — v2.1

Owner: Sharon Melendez. An assisted implementation, diagnostic evaluations, and
reproducible handoff are available. Start with [HANDOFF.md](HANDOFF.md).

The shadow checks the incoming target prompt in a separate qwen2.5:1.5b call.
Untrusted input is JSON-wrapped; the output is constrained to
`{"decision":"ALLOW"}` or `{"decision":"BLOCK"}`. The parser rejects extra or
duplicate keys, wrong types, unexpected verdicts, and incomplete generations.
Only valid ALLOW calls the unchanged baseline target with the exact original
prompt. BLOCK returns a fixed refusal. Failed or unsupported checks withhold
execution with `detector_error`; target failures are `target_error`. Errors are
never counted as successful safety refusals.

## Run

Python 3.9+, standard library only. Install/start Ollama and pull qwen2.5:1.5b.
From the repository root:

```sh
ollama pull qwen2.5:1.5b
python3 defenses/pdirect/defense.py --out experiments/pdirect/NEW_BASELINE
python3 defenses/pdirect/defense.py --prompt "Explain why multifactor authentication helps." --out experiments/pdirect/NEW_SINGLE_PROMPT
```

Each output directory must be new. The single-prompt mode prints the released
answer and retains the full evidence. `--dataset PATH` runs other JSONL inputs
with unique `id` and nonempty `prompt` fields; labels are optional for ordinary
runs and never sent to a model.

In the configured WSL workspace, Ollama is installed in `~/.local/bin`, libraries
in `~/.local/lib/ollama`, and models in `~/.ollama/models`. The enabled user service
is `~/.config/systemd/user/ollama.service`, bound to `127.0.0.1:11434`:

```sh
systemctl --user status ollama
systemctl --user restart ollama
ollama list
ollama ps
```

The service starts with the user's systemd session; reopen WSL after shutting it
down. Other machines should use their own Ollama installation/service workflow.

## Input and output limits

The prompt has a 3000-byte UTF-8 hard cap and must also fit the conservative
JSON-encoded context allowance. Escaping can make the effective limit smaller,
especially for non-ASCII text. Shorten an unsupported prompt; the implementation
withholds it as a check failure rather than relying on truncated classification.
Both model calls use context 4096; temperature 0, seed 424, generated-token cap 256,
and a 120-second timeout. The root target's code and generation settings are unchanged.
The detector fixes its context explicitly; the target uses the server default.
The configured user service pins `OLLAMA_CONTEXT_LENGTH=4096`. On another machine,
set that environment variable when starting Ollama to reproduce the target context.

Logs retain original input, raw shadow output, parsed verdict, error kind,
completion reason, token counts, released answer, and detector/target/total timing.
Run manifests capture inputs/source hashes, instructions, settings, model digests,
Ollama version, platform, and optional machine notes. They are experiment evidence,
not automatic safety or correctness judgments.

## Current evidence

[Final v2.1 report](../../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md):
48 fresh hand-authored cases, three repeats, two configurations, 288 attempts.
All 24 attack prompts were blocked; 22/24 benign prompts allowed; no request/verdict
errors. Two legitimate quotation-analysis prompts were blocked. The
[v1 replay on identical inputs](../../experiments/pdirect/2026-11-04_v1_replay_on_v2_001/README.md)
had two attack misses, five benign false positives, and three invalid-verdict cases.
These are diagnostic observations, not independent benchmark accuracy.

The policy/source freezes, [development search](../../experiments/pdirect/V2_DEVELOPMENT.md),
discarded candidates, aborted context-mismatch probe, and all prior results are
preserved. The old evaluation set became regression data for v2 and is not
presented as unseen validation. The latest policy was frozen before the fresh
cases; a runtime-only context change followed before any verdict inspection.
No classifier tuning followed the final evaluation. Human answer adjudication
remains pending; explicitly attributed assisted reviews are supplied.

## Reproduce and check

```sh
python3 defenses/pdirect/evaluate.py --out experiments/pdirect/NEW_EVALUATION --repeats 3 --machine-note "Describe hardware and load"
python3 -m unittest discover -s defenses/pdirect -p "test_*.py" -v
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001
python3 scripts/check_repository.py
```

The evaluation runner checks frozen prompt/source/settings and installed model
digest before inference. It snapshots exact source, inputs, instructions, and
metadata; warmup is excluded, case/config order randomized, and p95 uses nearest
rank. The verifier audits hashes, pairing, raw verdicts, gates, summaries, and
assisted-review coverage without models. [replay.py](replay.py) runs archived
versions in isolated source trees without replacing active code.

Mock tests verify software contracts, not detection quality. The shadow does not
inspect generated answers, guarantee injection resistance, or reproduce the
paper's concurrent release checkpoint. Small-model answer quality, long-context
inputs, adaptive attacks, and other datasets remain limitations. See the
[shared protocol](../../docs/EXPERIMENT_PROTOCOL.md),
[contribution workflow](../../CONTRIBUTING.md), and
[Ollama structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs).
