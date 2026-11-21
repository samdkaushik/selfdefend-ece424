# Smaller direct shadow

Owner: Yasmin Shahlamedina. Status: pilot evidence and a Nov 21 same-input evaluation run contributed; human-review results pending the second reviewer.

Compares qwen2.5:0.5b (a8b0c5157701) with the standard-direct qwen2.5:1.5b (65ec06548149), keeping the direct prompt
and target fixed. Harness configuration name: lightweight_pdirect. Same harness copy, command and hardware as
defenses/pintent/README.md. No separate detector code is needed here: the Nov 21 run uses defenses/pdirect/defense.py unchanged with --model qwen2.5:0.5b.

## Run evidence
experiments/lightweight/2026-11-04_yasmin_pilot_001/ and experiments/lightweight/2026-11-05_yasmin_pilot_002/ (identical copies of the same two runs), and experiments/lightweight/2026-11-21_yasmin_lightweight_eval_001/ (Nov 21, 48 cases on defenses/pdirect/evaluation_v2.jsonl).

## Observations
lightweight_pdirect blocked 2/2 attacks and 0/2 benign prompts in both runs. pdirect (1.5B) also blocked all four, so this
pilot cannot show whether the smaller model retains most of the standard shadow's behavior. The detector's stated reasons
sometimes contradicted its own BLOCK decision (for example pilot-benign-001 and pilot-attack-002 in run 002).
A 34.9 s lightweight call in run 001 was a cold start; run 002 was after warm-up. Timings are from one machine only.

## Nov 21 same-input run
experiments/lightweight/2026-11-21_yasmin_lightweight_eval_001/: qwen2.5:0.5b with the unchanged Pdirect prompt on defenses/pdirect/evaluation_v2.jsonl (24 attack, 24 benign); target qwen2.5:1.5b; same settings and hardware as the Pintent run. All 48 detector verdicts were valid BLOCK with no errors, so no response reached the target. A detector that blocks every prompt also blocks every benign one, so its attack numbers alone say nothing about quality. Human-review results and metrics are pending the second reviewer; no retained-benefit claim is made yet.

## Assistance
Assistance/tools used (course policy): Claude (AI assistant) helped run and interpret the Lightweight evaluation (this folder has no code of its own) and helped suggest a label and justification for most review items. I ran all commands on my own machine, read the outputs, entered every label myself using my own judgement on Claude's suggestions, and decided what to keep or change. Labels are not independent of Claude's suggestions; independence is only from the second human reviewer.
