# Smaller direct shadow

Owner: Yasmin Shahlamedina. Status: pilot evidence contributed; repo-native implementation pending.

Compares qwen2.5:0.5b (a8b0c5157701) with the standard-direct qwen2.5:1.5b (65ec06548149), keeping the direct prompt
and target fixed. Harness configuration name: lightweight_pdirect. Same harness copy, command and hardware as
defenses/pintent/README.md. No detector code has been written in this folder yet.

## Run evidence
experiments/lightweight/2026-11-04_yasmin_pilot_001/ and experiments/lightweight/2026-11-05_yasmin_pilot_002/ (identical copies of the same two runs).

## Observations
lightweight_pdirect blocked 2/2 attacks and 0/2 benign prompts in both runs. pdirect (1.5B) also blocked all four, so this
pilot cannot show whether the smaller model retains most of the standard shadow's behavior. The detector's stated reasons
sometimes contradicted its own BLOCK decision (for example pilot-benign-001 and pilot-attack-002 in run 002).
A 34.9 s lightweight call in run 001 was a cold start; run 002 was after warm-up. Timings are from one machine only.
