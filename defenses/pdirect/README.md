# Pdirect

Owner: Sharon Melendez. Status: implementation and midpoint results available.

The shadow checks the incoming prompt using a separate `qwen2.5:1.5b` call.
Only a valid ALLOW forwards the original prompt to the target. BLOCK returns a
refusal. Invalid verdicts, failed requests, and oversized inputs withhold the
target call and are logged as errors.

## Run

Python 3.9+ and Ollama; no pip dependencies. Keep Ollama running with
`OLLAMA_CONTEXT_LENGTH=4096`. From the repository root:

```sh
ollama pull qwen2.5:1.5b
python3 defenses/pdirect/defense.py --out experiments/pdirect/NEW_RUN
```

Use a new output folder each time. To check one prompt:

```sh
python3 defenses/pdirect/defense.py --prompt "Explain why multifactor authentication helps." --out experiments/pdirect/NEW_DEMO
```

## Settings and logs

- Target/shadow: `qwen2.5:1.5b`; context 4096
- Temperature 0; seed 424; output cap 256; request timeout 120 seconds
- Input cap: 3000 UTF-8 bytes, with a potentially tighter encoded-context limit
- Logs: original prompt, raw verdict, decision, response, errors, and timings
- Manifests: exact inputs, source hashes, model digest, settings, and machine notes

## Results

The final 48-case comparison used three repeats and two configurations, for
288 attempts. Pdirect blocked 24/24 attack cases and allowed 22/24 benign cases
on each repeat. Two quotation-analysis cases were false positives. This small
hand-authored set does not establish general injection resistance.

See the [result log](../../experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001/README.md)
and [midpoint submission](../../submission/midpoint/README.md).

## Checks

```sh
python3 -m unittest discover -s defenses/pdirect -p "test_*.py" -v
python3 defenses/pdirect/verify_evaluation.py experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001
```

All 18 component tests pass. Tests verify gating and logging; the saved experiment
measures model behavior. Response-review labels still need confirmation.
