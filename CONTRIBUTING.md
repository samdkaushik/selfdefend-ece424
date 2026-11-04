# Contributing

## One-time setup

Accept the collaborator invitation and clone the private repository:

```sh
git clone https://github.com/samdkaushik/selfdefend-ece424.git
cd selfdefend-ece424
```

Open this folder in VS Code. Work from the repository root when running scripts. Python 3.9+ is required; the current baseline has no pip dependencies.

## Choose your workspace

- Samarth: `harness.py`, `docs/baseline/`, baseline inputs/logs; note in `contributions/samarth.md`.
- Sharon: `defenses/pdirect/`, `experiments/pdirect/`; note in `contributions/sharon.md`.
- Yasmin: `defenses/pintent/`, `defenses/lightweight/`, corresponding experiment folders; note in `contributions/yasmin.md`.

Read your component README. Empty workspaces indicate pending work, not implemented defenses. Coordinate shared dataset or generation-setting changes with the team.

## Make a branch and contribute

Example for Sharon; substitute your own name and component:

```sh
git switch main
git pull --ff-only origin main
git switch -c sharon/pdirect
```

Make your changes. Run the checks from the main README, inspect `git diff`, and stage your specific files:

```sh
git status --short
git add defenses/pdirect experiments/pdirect contributions/sharon.md
git commit -m "Add Pdirect experiment and evidence"
git push -u origin sharon/pdirect
```

Open the repository on GitHub and select **Compare & pull request**. Explain what changed, the exact command you ran, the result, and limitations. Ask a teammate to review before merging; this is a team convention, not an enforced branch rule. Start another branch from updated main for the next task. Do not force-push over teammates' changes.

## Evidence and experiment files

Save each defense run under `experiments/COMPONENT/YYYY-MM-DD_NAME_RUN/`. Include commands, prompts or dataset hash, exact model tags/digests, settings, machine, decisions/released responses, timings, errors, and a short interpretation. Document setup failures honestly. Do not put hand-authored expectations in place of an actual run.

Keep the shared target and input wording fixed for comparison. Separate request errors, truncation, detector decisions, harmful-request compliance, and benign usefulness. Compare latency on the same machine. Copy the working dataset into each new run folder to preserve the actual input version.

Keep `logs/baseline_dev_2026-11-04.jsonl`, `runs/fallback_sanity/`, and `snapshots/initial/harness.py` unchanged. Use new folders/files for new results. Archived tests use the archived source; current code should have its own meaningful checks as the team develops it.

Record actual changes, reviews, run evidence, and assistance in your own contribution note as required by the course. Keep model files, credentials, .env files, runtime downloads, and Python caches out of Git. Commit small evidence files so teaching staff can inspect them.
