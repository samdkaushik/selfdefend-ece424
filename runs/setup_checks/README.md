# Assisted setup checks - not an attack evaluation

These raw responses were recorded by Codex during the November 3 setup session.

- `ollama_failed_probe.json`: Ollama 0.40.14 returned a backend initialization error on Samarth's Mac when attempting a simple readiness prompt. This is a runtime failure, not a model refusal or successful defense.
- `cpu_ready_probe.json`: the llama-server binary included with that Ollama release returned "Ready." to a readiness prompt using the downloaded 1.5B GGUF. It ran on CPU with `--device none --no-kv-offload --no-op-offload`, context 2048 and 4 threads. This was an isolated connectivity probe through a different API, not a completed harness experiment.

The servers were stopped when the user requested step-by-step guidance. No real four-configuration pilot or target-only attack evaluation has been completed in this shared package. These checks do not establish any student's independent contribution.
