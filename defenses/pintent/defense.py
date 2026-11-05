"""Pintent: sequential intent-first shadow gate; standard library only.

Same gate, shadow model, settings and policy text as defenses/pdirect, except the
detector first states the request's underlying intent and then decides from it.
Copied from the Pdirect structure on purpose so Pdirect's frozen files are untouched."""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
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


def main():
    """Quick live look at one detector verdict. Prints only; saves no trace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default=SHADOW_MODEL)
    args = parser.parse_args()
    print(json.dumps(detect(args.prompt, args.model), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
