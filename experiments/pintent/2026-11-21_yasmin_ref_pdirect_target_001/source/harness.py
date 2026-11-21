import json
import time
import urllib.request
import urllib.error
import socket
from pathlib import Path
from datetime import datetime, timezone

OLLAMA_URL = "http://localhost:11434/api/chat"
TARGET_MODEL = "qwen2.5:1.5b"


#The requests that are being sent to Ollama are explained here
def query_target(prompt):
    payload = {
        "model": TARGET_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0,
            "seed": 424,
            "num_predict": 256
        }
    }

    #Convert python to json bytes
    data = json.dumps(payload).encode("utf-8")

    #Create a request object with the url and data
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    #Starts measuring the response time
    start = time.perf_counter()

    #Send the request and read Ollama's JSON response
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    #Converts the elapsed time from seconds to milliseconds
    elapsed_ms = (time.perf_counter() - start) * 1000

    #Collects the model's answer and completion details
    answer = result["message"]["content"]

    details = {
        "done_reason": result.get("done_reason"),
        "output_tokens": result.get("eval_count")
    }

    #Return the answer, elapsed time, and completion details
    return answer, elapsed_ms, details


#Reads each test case from the dataset file
def load_cases(file_path):
    cases = []

    #Opens the file and reads it one line at a time
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            #Skips empty lines
            if not line.strip():
                continue

            #Converts each JSON line into a python dictionary
            case = json.loads(line)
            cases.append(case)

    return cases


#Calls function when the file is run
if __name__ == "__main__":
    #Loads the test cases from the dataset
    cases = load_cases("data/baseline_dev.jsonl")

    print(f"Loaded {len(cases)} test cases")

    #Create the logs folder if it does not already exist
    Path("logs").mkdir(exist_ok=True)

    #Runs each test case from the dataset
    for case in cases:
        test_prompt = case["prompt"]

        #Collects details from the test before sending the request
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "case_id": case["id"],
            "label": case["label"],
            "model": TARGET_MODEL,
            "prompt": test_prompt,
            "config": "target_only",

            #These values get updated after the request
            "response": None,
            "elapsed_ms": None,
            "status": "pending",
            "error": None,
            "done_reason": None,
            "output_tokens": None,

            #Records the settings used for the model
            "settings": {
                "temperature": 0,
                "seed": 424,
                "num_predict": 256
            }
        }

        #Tracks how long the attempt takes even if it fails
        attempt_start = time.perf_counter()

        try:
            #Sends the prompt to the target model
            answer, elapsed_ms, details = query_target(test_prompt)

            #Records the response if the request works
            record["response"] = answer
            record["elapsed_ms"] = elapsed_ms
            record["status"] = "ok"

            #Records whether the model finished or reached its token limit
            record["done_reason"] = details["done_reason"]
            record["output_tokens"] = details["output_tokens"]

            print("\nCase:", case["id"])
            print("Prompt:", test_prompt)
            print("Response:", answer)
            print(f"Response time: {elapsed_ms:.2f} ms")
            print("Completion reason:", details["done_reason"])
            print("Output tokens:", details["output_tokens"])

        except (
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
            json.JSONDecodeError,
            KeyError,
            TypeError
        ) as error:
            #Records the error instead of losing the test result
            record["status"] = "error"
            record["error"] = f"{type(error).__name__}: {error}"

            #Records how long the failed attempt took
            record["elapsed_ms"] = (
                time.perf_counter() - attempt_start
            ) * 1000

            print("\nCase:", case["id"])
            print("Request failed:", record["error"])

        #Append one JSON record per line (preserves earlier JSON lines)
        with open(
            "logs/baseline_trace.jsonl",
            "a",
            encoding="utf-8"
        ) as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\nResults saved to logs/baseline_trace.jsonl")