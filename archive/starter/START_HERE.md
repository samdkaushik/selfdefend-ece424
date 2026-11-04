# SelfDefend team handoff - read this first

Updated November 3, 2026. This is a collaboration starter, not a completed midpoint submission.

## Proposed shared setup

- Local/free model runner: Ollama (Mac or Windows).
- Target: `qwen2.5:1.5b` (Qwen2.5 1.5B Instruct).
- Standard shadow: `qwen2.5:1.5b`, called separately with detector instructions.
- Smaller shadow: `qwen2.5:0.5b`.
- Model calls: temperature 0; seed 424; max 256 generated tokens; 120-second request timeout.
- Use matching model digests, prompts, and settings across teammates. Log hardware; perform timing comparisons on the same computer.
- These are initial choices; document differences from the original SelfDefend paper and any later revisions.

## Who does what

| Member | Responsibility | Evidence to contribute |
| --- | --- | --- |
| Samarth | Target-only baseline; threat model; run instructions | Attack/benign baseline responses, reviewed outcomes, commands, settings, errors, timings |
| Sharon | Pdirect shadow; architecture and direct results | Detector prompt/change, allowed/blocked examples, direct-defense run and timing log |
| Yasmin | Pintent and smaller-shadow comparison; contribution plan | Intent run, controlled standard-direct vs smaller-direct comparison, model details and observations |

Everyone should review their component, record their actual changes/runs, and complete TEAM_EVIDENCE.md. The shared code was generated with Codex assistance; the commented copy is a learning guide for writing your own implementation. Do not claim planned experiments as completed work.

## What's in this ZIP

- `harness.py`: runnable four-configuration harness with teaching comments.
- `snapshots/initial/harness.py`: exact original source used for the supplied fallback trace.
- `test_harness.py`: software tests using fixtures and mocked HTTP responses.
- `data/sanity.jsonl`: synthetic software checks, not LLM evaluation data.
- `data/pilot_dev.jsonl`: four newly authored development prompts (two benign, two attack). Not a published benchmark or held-out set.
- `data/dataset_inventory.csv`: provenance template to complete for the eventual benchmark.
- `runs/fallback_sanity/`: completed offline trace, manifest, review template, summary, and check output.
- `runs/setup_checks/`: actual assisted setup failure and isolated CPU readiness probe, with limitations explained.
- `README.md`, `PROTOCOL.md`, `FALLBACK.md`, `TEAM_EVIDENCE.md`, `EXPERIMENT_LOG.md`: detailed instructions and initial planning records.
- The obsolete initial PDF report has been removed.
- `sources/Original_Project_Proposal.pdf`: original team proposal.

This START_HERE file is the latest status. Earlier planning documents/report describe the initial snapshot: model selection now has proposed Qwen tags, and setup checks have occurred, but real attack evaluation and per-member work evidence remain pending.

## Step 1: run the offline software check

Install Python 3.9+ if needed, unzip the folder, and open a terminal in `SelfDefend_Team`.

Mac/Linux:

```sh
python3 harness.py selftest
python3 -m unittest -v test_harness.py
python3 snapshots/initial/harness.py verify --out runs/fallback_sanity
```

Windows PowerShell:

```powershell
python harness.py selftest
python -m unittest -v test_harness.py
python snapshots/initial/harness.py verify --out runs/fallback_sanity
```

On Windows, `py` may be used instead of `python` if that is how Python was installed.

Expected: passing software tests and 16 verified synthetic trace records. To generate your own synthetic run, use `python3 harness.py run --mode mock --out runs/YOUR_NAME_sanity_001` (use `python` on Windows). Use a new folder for every run.

## Step 2: prepare local models

Install Ollama from https://ollama.com/download and keep the application running. Then:

```sh
ollama pull qwen2.5:1.5b
ollama pull qwen2.5:0.5b
ollama run qwen2.5:1.5b
```

Try a harmless greeting. Exit the interactive chat with `/bye`. Record any setup failure instead of treating it as a model refusal. Samarth's assisted setup encountered a graphics backend failure, so a complete Ollama harness run is still pending. A separate CPU readiness probe succeeded; the current harness does not directly support that alternate server API.

Windows requirements: https://docs.ollama.com/windows
Model details: https://ollama.com/library/qwen2.5:1.5b and https://ollama.com/library/qwen2.5:0.5b

## Step 3: run the tiny real-model development pilot

Only proceed after the local Ollama greeting works. From this folder (one line):

```sh
python3 harness.py run --mode ollama --dataset data/pilot_dev.jsonl --target qwen2.5:1.5b --shadow qwen2.5:1.5b --light qwen2.5:0.5b --out runs/YOUR_NAME_pilot_001
```

Use `python` instead of `python3` on Windows. Then verify with:

```sh
python3 harness.py verify --dataset data/pilot_dev.jsonl --out runs/YOUR_NAME_pilot_001
```

The current harness runs ALL FOUR configurations. Samarth's baseline rows are the ones labeled `target_only`; Sharon's are `pdirect`; Yasmin's are `pintent` and `lightweight_pdirect`. The suggested `--config target_only` extension from the chat has NOT been implemented in these files; it is a coding exercise for Samarth's working copy. No `--config` flag currently exists.

Review a COPY of review.csv: judge actual released responses, not ALLOW decisions. Keep attack success, benign usefulness, timeouts, and other errors distinct. The harness does not automatically calculate research ASR. Four dev cases are a setup pilot, not evidence of final robustness.

## Step 4: finish the midpoint evidence together

Each member adds their own dated code/review/run evidence. Record exact model digests/version, hardware, dataset provenance, settings, and remaining tasks. Update the contribution plan and protocol as needed. Keep held-out prompts separate from development.

Designated fallback: `runs/fallback_sanity/trace.jsonl`, with its matching original source/data/manifest. This fallback proves software control flow only. Preserve that snapshot; new code versions and experiments need new run folders and matching source copies.

## Sharing and repository notes

Share this ZIP or upload its contents to the team repository. Invite all members and ensure teaching staff can access the final submission. Keep models/runtime binaries, secrets, and Python cache files out of GitHub. Download model weights separately on each computer. No paid API is required for this setup.
