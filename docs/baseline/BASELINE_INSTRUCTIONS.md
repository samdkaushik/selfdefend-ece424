# Running the target-only baseline

## Purpose
This harness sends development prompts directly to Qwen without a shadow
defense. It saves responses, timings, completion details, and errors

## Requirements
- Python 3.9 or newer
- Ollama installed and running
- The qwen2.5:1.5b model downloaded

## Setup
Download the target model:

ollama pull qwen2.5:1.5b

Open a terminal in the project folder. Keep Ollama running

## Run
On Mac:

python3 harness.py

On Windows:

python harness.py

The harness reads every case in data/baseline_dev.jsonl.

## Settings
- Target: qwen2.5:1.5b
- Configuration: target_only
- Temperature: 0
- Seed: 424
- Maximum generated tokens: 256
- Request timeout: 120 seconds

## Output
Results are appended to logs/baseline_trace.jsonl
Each nonblank line is one JSON result

A status of "ok" means the request completed. Review the response separately
for usefulness, harmful-request compliance, and truncation

A completion reason of "length" indicates that generation reached its limit

## Checks performed during development
1. Sent a harmless prompt and confirmed that a response was saved
2. Temporarily changed the endpoint to localhost:1
3. Confirmed that the failed connection produced an error record
4. Restored the endpoint to localhost:11434

The connection-failure check showed that failed requests were preserved
in the trace. It did not test model safety.

## Baseline snapshot
logs/baseline_dev_2026-11-04.jsonl contains the preserved four-case run:
two benign cases and two direct harmful requests

The exercise case is recorded as benign-001 in that snapshot
Its dataset ID was subsequently changed to benign-exercise-001
The snapshot, however, remains unchanged

## Limitations
These are preliminary development cases. The run does not establish
general jailbreak resistance or representative latency. The two direct harmful
requests showed preliminary compliance in this small development sample.
