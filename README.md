# SelfDefend — ECE 424

A team study of whether a smaller shadow language model can preserve the benefit of a jailbreak defense while reducing resource use and latency.

**Start here:** [team roles](docs/TEAM_ROLES.md) · [contribute](CONTRIBUTING.md) · [experiment protocol](docs/EXPERIMENT_PROTOCOL.md) · [baseline results](docs/baseline/BASELINE_REVIEW.md)

**Midpoint submission:** [self-contained package and single entry document](submission/midpoint/README.md).
It gathers runnable code, selected evidence, sanity results, protocol, contribution
summary, and the fallback in one folder. This package covers the Pdirect contribution.

## Project status

| Component | Owner | Current status | Where to go |
| --- | --- | --- | --- |
| Target-only baseline | Samarth | Working local-model harness; four-case development snapshot saved | [harness.py](harness.py), [instructions](docs/baseline/BASELINE_INSTRUCTIONS.md) |
| Direct-content shadow | Sharon | V2.1: all 24 fresh attack cases blocked, 22/24 benign cases allowed; v1 comparison and limits documented | [Pdirect handoff](defenses/pdirect/HANDOFF.md) |
| Intent shadow | Yasmin | Implementation and results to be contributed | [Pintent workspace](defenses/pintent/README.md) |
| Smaller-shadow comparison | Yasmin | Comparison and results to be contributed | [lightweight workspace](defenses/lightweight/README.md) |

The baseline snapshot contains two benign and two direct harmful requests. Qwen complied with both deceptive requests under preliminary review (2/2 in this tiny development sample). This is not a representative benchmark or demonstrated jailbreak bypass. A transport status of `ok` does not judge safety, correctness, or usefulness.

## Run Samarth's baseline

Install Python 3.9+ and [Ollama](https://ollama.com/download). Keep Ollama running. From the **repository root**:

```sh
ollama pull qwen2.5:1.5b
python3 harness.py
```

On Windows use `python harness.py` or `py harness.py`. No Python packages need installing. The harness reads `data/baseline_dev.jsonl` and appends to `logs/baseline_trace.jsonl`.

Proposed models: target/standard shadow `qwen2.5:1.5b`; smaller shadow `qwen2.5:0.5b`. Models are downloaded separately; weights and API keys do not belong in this repository. See the [protocol](docs/EXPERIMENT_PROTOCOL.md) for shared settings and the paper/setup differences.

## Find things quickly

| Location | Contents |
| --- | --- |
| `harness.py` | Samarth's current target-only code, with his comments |
| `data/` | Shared current development prompts and dataset guidance |
| `logs/` | Baseline working trace and preserved real-model snapshot |
| `defenses/` | Separate places for teammates' defense implementations |
| `experiments/` | Defense experiment output folders and naming guidance |
| `contributions/` | Each member's dated work evidence |
| `docs/baseline/` | Baseline instructions, review, and fallback note |
| `docs/` | Shared roles and experimental protocol |
| `sources/` | Original project proposal |
| `snapshots/initial/`, `runs/fallback_sanity/` | Original assisted synthetic harness, tests, and immutable fallback |
| `archive/starter/` | Older starter documents; historical reference |

## Checks without a model

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s snapshots/initial -p test_harness.py -v
python3 -m unittest discover -s defenses/pdirect -p "test_*.py" -v
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_frozen_evaluation_001
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v1_replay_on_v2_001
```

The repository check validates Python syntax, active dataset IDs, document links, the real baseline snapshot hash, and the original synthetic snapshot hashes. The six archived tests exercise the original assisted harness, not the current target-only implementation. Pdirect tests exercise gating and evaluation accounting; its evidence verifier audits saved pairs and hashes. These commands do not run an LLM. GitHub Actions runs these checks on Windows and Linux after publication.

## Contribute and submit

Follow [CONTRIBUTING.md](CONTRIBUTING.md): make a personal branch, put your work in your component folder, save a small reproducible run, update your contribution note, and open a pull request. You can add collaborators under the repository's **Settings → Collaborators**.

For baseline fallback use [logs/baseline_dev_2026-11-04.jsonl](logs/baseline_dev_2026-11-04.jsonl), described in [the fallback note](docs/baseline/BASELINE_FALLBACK.md). Preserve it unchanged. The older synthetic trace is a separate software check, not research evidence.
