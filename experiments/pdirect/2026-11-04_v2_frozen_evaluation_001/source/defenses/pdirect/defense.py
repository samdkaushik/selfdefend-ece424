"""Sequential direct-content shadow gate; standard library only."""

import argparse
import hashlib
import json
import platform
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import harness  # Reuse the unchanged target model, settings, and request code.

PROMPT_PATH = Path(__file__).with_name("detector_prompt.txt")
SHADOW_MODEL = "qwen2.5:1.5b"
SETTINGS = {"temperature": 0, "seed": 424, "num_predict": 256}
DETECTOR_SETTINGS = dict(SETTINGS, num_ctx=8192)
MAX_PROMPT_BYTES = 3000
VERDICT_SCHEMA = {
    "type": "object",
    "properties": {"decision": {"type": "string", "enum": ["ALLOW", "BLOCK"]}},
    "required": ["decision"], "additionalProperties": False,
}
REFUSAL = "I can't help with that request."
UNAVAILABLE = "This request could not be checked safely. Please try again later."
REQUEST_ERRORS = (urllib.error.URLError, TimeoutError, OSError,
                  ValueError, KeyError, TypeError)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_verdict(raw):
    if not isinstance(raw, str):
        raise ValueError("Detector content must be text")
    value = json.loads(raw, object_pairs_hook=unique_object)
    if not isinstance(value, dict) or set(value) != {"decision"}:
        raise ValueError("Expected exactly one decision field")
    if not isinstance(value["decision"], str) or value["decision"] not in ("ALLOW", "BLOCK"):
        raise ValueError("Expected decision ALLOW or BLOCK")
    return value["decision"]


def detector_payload(prompt, model):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a nonempty string")
    if len(prompt.encode("utf-8")) > MAX_PROMPT_BYTES:
        raise ValueError(f"Prompt exceeds the {MAX_PROMPT_BYTES}-byte input limit")
    messages = [
        {"role": "system", "content": PROMPT_PATH.read_text(encoding="utf-8")},
        {"role": "user", "content": json.dumps({"request": prompt})},
    ]
    # Conservative byte-based allowance for content, chat-template overhead,
    # and generated output. Reject rather than rely on silent context truncation.
    content_bytes = sum(len(m["content"].encode("utf-8")) for m in messages)
    reserved = 256 + 32 * len(messages) + DETECTOR_SETTINGS["num_predict"]
    if content_bytes + reserved > DETECTOR_SETTINGS["num_ctx"]:
        raise ValueError("Encoded request exceeds the detector context budget")
    return {"model": model, "messages": messages, "stream": False,
            "format": VERDICT_SCHEMA, "options": DETECTOR_SETTINGS}


def detect(prompt, model=SHADOW_MODEL):
    """Inspect only the prompt, never its dataset label. Fail closed on errors."""
    started = time.perf_counter()
    result = {"decision": "BLOCK", "status": "error", "raw_response": None,
              "elapsed_ms": None, "model": model, "error": None,
              "done_reason": None, "output_tokens": None, "prompt_tokens": None,
              "input_limit_bytes": MAX_PROMPT_BYTES, "error_kind": None}
    stage = "input"
    try:
        payload = detector_payload(prompt, model)
        stage = "transport"
        request = urllib.request.Request(
            harness.OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.load(response)
        stage = "invalid_output"
        result["raw_response"] = body["message"]["content"]
        result["done_reason"] = body.get("done_reason")
        result["output_tokens"] = body.get("eval_count")
        result["prompt_tokens"] = body.get("prompt_eval_count")
        if body.get("done") is not True or body.get("done_reason") != "stop":
            raise ValueError("Detector did not complete normally")
        verdict = parse_verdict(result["raw_response"])
        result.update(decision=verdict, status="ok")
    except REQUEST_ERRORS as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["error_kind"] = stage
    result["elapsed_ms"] = (time.perf_counter() - started) * 1000
    return result


def defend(prompt, model=SHADOW_MODEL):
    """Only a valid ALLOW can invoke the baseline target."""
    started = time.perf_counter()
    detector = detect(prompt, model)
    if detector["status"] == "ok" and detector["decision"] not in ("ALLOW", "BLOCK"):
        detector.update(status="error", decision="BLOCK", error="Invalid detector decision",
                        error_kind="invalid_output")
    record = {"prompt": prompt, "config": "pdirect", "detector": detector,
              "target_model": harness.TARGET_MODEL, "target_called": False,
              "target_elapsed_ms": None, "target_details": None,
              "response": None, "status": "detector_error", "error": detector["error"]}
    if detector["status"] != "ok":
        record["response"] = UNAVAILABLE
    elif detector["decision"] == "BLOCK":
        record.update(status="blocked", response=REFUSAL)
    else:
        record["target_called"] = True
        target_started = time.perf_counter()
        try:
            answer, elapsed, details = harness.query_target(prompt)
            if not isinstance(answer, str):
                raise ValueError("Target response must be text")
            record.update(status="ok", response=answer,
                          target_elapsed_ms=elapsed, target_details=details)
        except REQUEST_ERRORS as error:
            record.update(status="target_error", error=f"{type(error).__name__}: {error}")
        finally:
            if record["target_elapsed_ms"] is None:
                record["target_elapsed_ms"] = (time.perf_counter() - target_started) * 1000
    record["elapsed_ms"] = (time.perf_counter() - started) * 1000
    return record


def read_cases(data):
    cases = [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
    ids = set()
    if not cases:
        raise ValueError("Dataset must not be empty")
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            raise ValueError("Case IDs must be unique nonempty strings")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("Each case needs a nonempty prompt")
        case["prompt"].encode("utf-8")
        ids.add(case_id)
    return cases


def runtime_metadata():
    """Capture installed model digests and Ollama version without downloading."""
    metadata = {"platform": platform.platform(), "python": platform.python_version(),
                "machine": platform.machine(), "processor": platform.processor()}
    base = harness.OLLAMA_URL.rsplit("/api/", 1)[0]
    for name, endpoint in (("ollama_version", "/api/version"), ("models", "/api/tags")):
        try:
            with urllib.request.urlopen(base + endpoint, timeout=5) as response:
                metadata[name] = json.load(response)
        except REQUEST_ERRORS as error:
            metadata[name] = {"error": f"{type(error).__name__}: {error}"}
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--dataset", type=Path)
    inputs.add_argument("--prompt", help="Check one prompt and save its complete trace")
    parser.add_argument("--out", type=Path, required=True, help="New run directory; never overwritten")
    parser.add_argument("--model", default=SHADOW_MODEL)
    parser.add_argument("--machine-note", default="Not supplied")
    args = parser.parse_args()
    if args.prompt is not None:
        data = (json.dumps({"id": "interactive-001", "prompt": args.prompt}) + "\n").encode("utf-8")
    else:
        data = (args.dataset or ROOT / "data/baseline_dev.jsonl").read_bytes()
    cases = read_cases(data)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "inputs.jsonl").write_bytes(data)
    (args.out / "detector_prompt.txt").write_bytes(PROMPT_PATH.read_bytes())
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable] + sys.argv,
        "dataset_sha256": hashlib.sha256(data).hexdigest(),
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (Path(__file__), PROMPT_PATH, ROOT / "harness.py")},
        "shadow_model": args.model, "target_model": harness.TARGET_MODEL,
        "settings": SETTINGS, "timeout_seconds": 120,
        "detector_settings": DETECTOR_SETTINGS, "verdict_schema": VERDICT_SCHEMA,
        "max_prompt_bytes": MAX_PROMPT_BYTES,
        "machine_note": args.machine_note, "runtime": runtime_metadata(),
        "limitations": "Sequential gate; statuses are not safety or usefulness scores.",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    counts = {}
    with (args.out / "trace.jsonl").open("x", encoding="utf-8") as output:
        for case in cases:
            record = defend(case["prompt"], args.model)
            record.update(case_id=case["id"], label=case.get("label"),
                          timestamp_utc=datetime.now(timezone.utc).isoformat())
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            output.flush()
            counts[record["status"]] = counts.get(record["status"], 0) + 1
            print(f"{case['id']}: {record['status']} ({record['detector']['decision']})")
            if args.prompt is not None:
                print(record["response"] or record["error"])
    (args.out / "summary.json").write_text(json.dumps(counts, indent=2) + "\n", encoding="utf-8")
    return 1 if counts.get("detector_error") or counts.get("target_error") else 0


if __name__ == "__main__":
    sys.exit(main())
