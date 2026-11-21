"""Pintent: sequential intent-first shadow gate; standard library only.

Same gate, shadow model, settings and policy text as defenses/pdirect, except the
detector first states the request's underlying intent and then decides from it.
Copied from the Pdirect structure on purpose so Pdirect's frozen files are untouched."""

import argparse
import hashlib
import importlib.util
import json
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
DETECTOR_SETTINGS = dict(SETTINGS, num_ctx=4096)
MAX_PROMPT_BYTES = 3000
VERDICT_SCHEMA = {
    "type": "object",
    "properties": {"intent": {"type": "string"},
                   "decision": {"type": "string", "enum": ["ALLOW", "BLOCK"]}},
    "required": ["intent", "decision"], "additionalProperties": False,
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
    """Return (decision, intent) or raise ValueError."""
    if not isinstance(raw, str):
        raise ValueError("Detector content must be text")
    value = json.loads(raw, object_pairs_hook=unique_object)
    if not isinstance(value, dict) or set(value) != {"intent", "decision"}:
        raise ValueError("Expected exactly the fields intent and decision")
    if not isinstance(value["intent"], str) or not value["intent"].strip():
        raise ValueError("Intent must be a nonempty string")
    if not isinstance(value["decision"], str) or value["decision"] not in ("ALLOW", "BLOCK"):
        raise ValueError("Expected decision ALLOW or BLOCK")
    return value["decision"], value["intent"].strip()


def detector_payload(prompt, model):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a nonempty string")
    if len(prompt.encode("utf-8")) > MAX_PROMPT_BYTES:
        raise ValueError(f"Prompt exceeds the {MAX_PROMPT_BYTES}-byte input limit")
    messages = [
        {"role": "system", "content": PROMPT_PATH.read_text(encoding="utf-8")},
        {"role": "user", "content": json.dumps({"request": prompt})},
    ]
    # Byte-based allowance for content, chat-template overhead and generated output.
    # Reject rather than rely on silent context truncation.
    content_bytes = sum(len(m["content"].encode("utf-8")) for m in messages)
    reserved = 256 + 32 * len(messages) + DETECTOR_SETTINGS["num_predict"]
    if content_bytes + reserved > DETECTOR_SETTINGS["num_ctx"]:
        raise ValueError("Encoded request exceeds the detector context budget")
    return {"model": model, "messages": messages, "stream": False,
            "format": VERDICT_SCHEMA, "options": DETECTOR_SETTINGS}


def detect(prompt, model=SHADOW_MODEL):
    """Inspect only the prompt, never its dataset label. Fail closed on errors."""
    started = time.perf_counter()
    result = {"decision": "BLOCK", "status": "error", "intent": None,
              "raw_response": None, "elapsed_ms": None, "model": model,
              "error": None, "done_reason": None, "output_tokens": None,
              "prompt_tokens": None, "input_limit_bytes": MAX_PROMPT_BYTES,
              "error_kind": None}
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
        decision, intent = parse_verdict(result["raw_response"])
        result.update(decision=decision, intent=intent, status="ok")
    except REQUEST_ERRORS as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["error_kind"] = stage
    result["elapsed_ms"] = (time.perf_counter() - started) * 1000
    return result


def defend(prompt, model=SHADOW_MODEL):
    """Only a valid ALLOW can invoke the baseline target."""
    started = time.perf_counter()
    detector = detect(prompt, model)
    record = {"prompt": prompt, "config": "pintent", "detector": detector,
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


def _load_pdirect():
    """Load Sharon's Pdirect module to reuse its case reader and runtime metadata."""
    path = ROOT / "defenses" / "pdirect" / "defense.py"
    spec = importlib.util.spec_from_file_location("pdirect_defense", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    """Check one prompt (prints only) or run a dataset and save a complete run directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--dataset", type=Path)
    inputs.add_argument("--prompt", help="Check one prompt; saves a trace only with --out")
    parser.add_argument("--out", type=Path, help="New run directory; never overwritten")
    parser.add_argument("--model", default=SHADOW_MODEL)
    parser.add_argument("--machine-note", default="Not supplied")
    args = parser.parse_args()
    if args.out is None:
        if args.dataset is not None:
            parser.error("--out is required with --dataset")
        print(json.dumps(detect(args.prompt, args.model), indent=2, ensure_ascii=False))
        return 0
    pdirect = _load_pdirect()
    if args.prompt is not None:
        data = (json.dumps({"id": "interactive-001", "prompt": args.prompt}) + "\n").encode("utf-8")
    else:
        data = args.dataset.read_bytes()
    cases = pdirect.read_cases(data)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "inputs.jsonl").write_bytes(data)
    (args.out / "detector_prompt.txt").write_bytes(PROMPT_PATH.read_bytes())
    sources = (Path(__file__).resolve(), PROMPT_PATH.resolve(), ROOT / "harness.py",
               ROOT / "defenses" / "pdirect" / "defense.py")
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable] + sys.argv,
        "config": "pintent",
        "dataset_sha256": hashlib.sha256(data).hexdigest(),
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
        "shadow_model": args.model, "target_model": harness.TARGET_MODEL,
        "settings": SETTINGS, "timeout_seconds": 120,
        "detector_settings": DETECTOR_SETTINGS, "verdict_schema": VERDICT_SCHEMA,
        "max_prompt_bytes": MAX_PROMPT_BYTES,
        "reused_from_pdirect": ["read_cases", "runtime_metadata"],
        "machine_note": args.machine_note, "runtime": pdirect.runtime_metadata(),
        "limitations": "Sequential gate; statuses are not safety or usefulness scores.",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    counts = {}
    with (args.out / "trace.jsonl").open("x", encoding="utf-8") as output:
        for case in cases:
            record = defend(case["prompt"], args.model)
            record.update(case_id=case["id"], label=case.get("label"),
                          category=case.get("category"),
                          timestamp_utc=datetime.now(timezone.utc).isoformat())
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            output.flush()
            counts[record["status"]] = counts.get(record["status"], 0) + 1
            print(f"{case['id']}: {record['status']} ({record['detector']['decision']})")
    (args.out / "summary.json").write_text(json.dumps(counts, indent=2) + "\n", encoding="utf-8")
    return 1 if counts.get("detector_error") or counts.get("target_error") else 0


if __name__ == "__main__":
    sys.exit(main())
