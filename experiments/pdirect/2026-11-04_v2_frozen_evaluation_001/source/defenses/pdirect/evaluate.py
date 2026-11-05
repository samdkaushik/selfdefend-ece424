"""Frozen-prompt, paired same-machine development evaluation."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import sys
import time

import defense

HERE = Path(__file__).resolve().parent


def target_only(prompt):
    started = time.perf_counter()
    record = {"config": "target_only", "prompt": prompt, "target_called": True,
              "response": None, "error": None, "target_details": None,
              "target_elapsed_ms": None, "status": "target_error"}
    try:
        answer, elapsed, details = defense.harness.query_target(prompt)
        if not isinstance(answer, str):
            raise ValueError("Target response must be text")
        record.update(status="ok", response=answer,
                      target_elapsed_ms=elapsed, target_details=details)
    except defense.REQUEST_ERRORS as error:
        record["error"] = f"{type(error).__name__}: {error}"
    record["elapsed_ms"] = (time.perf_counter() - started) * 1000
    return record


def latency(records):
    values = sorted(r["elapsed_ms"] for r in records)
    if not values:
        return {"n": 0, "median_ms": None, "p95_ms": None}
    return {"n": len(values), "median_ms": statistics.median(values),
            "p95_ms": values[math.ceil(.95 * len(values)) - 1]}


def summarize(records):
    result = {}
    for config in ("target_only", "pdirect"):
        subset = [r for r in records if r["config"] == config]
        result[config] = {
            "attempts": len(subset), "unique_cases": len({r["case_id"] for r in subset}),
            "statuses": dict(Counter(r["status"] for r in subset)),
            "target_truncations": sum((r["target_details"] or {}).get("done_reason") == "length" for r in subset),
            "latency_all_attempts": latency(subset),
            "latency_without_errors": latency([r for r in subset if r["status"] in ("ok", "blocked")]),
            "by_label": {label: latency([r for r in subset if r["label"] == label]) for label in ("benign", "attack")},
        }
        if config == "pdirect":
            groups = {}
            for category in sorted({r["category"] for r in subset}):
                rows = [r for r in subset if r["category"] == category]
                groups[category] = {
                    "attempts": len(rows), "unique_cases": len({r["case_id"] for r in rows}),
                    "valid_allow": sum(r["detector"]["status"] == "ok" and r["detector"]["decision"] == "ALLOW" for r in rows),
                    "valid_block": sum(r["detector"]["status"] == "ok" and r["detector"]["decision"] == "BLOCK" for r in rows),
                    "detector_errors": sum(r["detector"]["status"] != "ok" for r in rows),
                }
            result[config]["detector_by_category"] = groups
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=HERE / "evaluation_v2.jsonl")
    parser.add_argument("--freeze", type=Path, default=HERE / "evaluation_freeze_v2.json")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--machine-note", required=True)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    freeze = json.loads(args.freeze.read_text())
    if hashlib.sha256(defense.PROMPT_PATH.read_bytes()).hexdigest() != freeze["prompt_sha256"]:
        parser.error("Detector prompt differs from the frozen version")
    if freeze.get("detector_source_sha256") != hashlib.sha256((HERE / "defense.py").read_bytes()).hexdigest():
        parser.error("Detector implementation differs from the frozen version")
    if freeze.get("detector_settings") != defense.DETECTOR_SETTINGS:
        parser.error("Detector settings differ from the frozen version")
    data = args.dataset.read_bytes()
    cases = defense.read_cases(data)
    if any(c.get("label") not in ("benign", "attack") or not isinstance(c.get("category"), str) for c in cases):
        parser.error("Evaluation cases require a label and category")
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "inputs.jsonl").write_bytes(data)
    (args.out / "detector_prompt.txt").write_bytes(defense.PROMPT_PATH.read_bytes())
    (args.out / "evaluation_freeze.json").write_bytes(args.freeze.read_bytes())
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable] + sys.argv, "repeats": args.repeats,
        "order_seed": 424, "machine_note": args.machine_note,
        "dataset_sha256": hashlib.sha256(data).hexdigest(),
        "source_sha256": {str(p.relative_to(defense.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (Path(__file__), HERE / "defense.py", defense.ROOT / "harness.py", defense.PROMPT_PATH)},
        "runtime": defense.runtime_metadata(), "settings": defense.SETTINGS,
        "detector_settings": defense.DETECTOR_SETTINGS, "max_prompt_bytes": defense.MAX_PROMPT_BYTES,
        "verdict_schema": defense.VERDICT_SCHEMA,
        "shadow_model": defense.SHADOW_MODEL, "target_model": defense.harness.TARGET_MODEL,
        "timeout_seconds": 120,
        "design": "Warmup excluded; shuffled cases each repeat and randomized config order within each case pair. Shared model resident; sequential requests. Full-response latency, nearest-rank p95. Repeats are not independent prompts.",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for name in manifest["source_sha256"]:
        saved = args.out / "source" / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes((defense.ROOT / name).read_bytes())
    warmup = {"detector": defense.detect("What is two plus two?"),
              "target": target_only("Answer briefly: what is two plus two?")}
    (args.out / "warmup.json").write_text(json.dumps(warmup, indent=2) + "\n")
    if warmup["detector"]["status"] != "ok" or warmup["target"]["status"] != "ok":
        print("Warmup failed; inspect warmup.json", file=sys.stderr)
        return 1
    rng = random.Random(424)
    records = []
    with (args.out / "trace.jsonl").open("x") as trace:
        for repeat in range(1, args.repeats + 1):
            ordered = list(cases)
            rng.shuffle(ordered)
            for case in ordered:
                configs = ["target_only", "pdirect"]
                rng.shuffle(configs)
                for config in configs:
                    r = target_only(case["prompt"]) if config == "target_only" else defense.defend(case["prompt"])
                    r.update(case_id=case["id"], label=case["label"], category=case["category"],
                             repeat=repeat, sequence=len(records) + 1,
                             timestamp_utc=datetime.now(timezone.utc).isoformat())
                    records.append(r)
                    trace.write(json.dumps(r, ensure_ascii=False) + "\n")
                    trace.flush()
                print(f"repeat {repeat}: {case['id']}", flush=True)
    summary = summarize(records)
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    # A review sheet deliberately starts unresolved; transport never judges safety.
    with (args.out / "review.jsonl").open("x") as review:
        for r in records:
            review.write(json.dumps({"sequence": r["sequence"], "case_id": r["case_id"],
                                    "config": r["config"], "repeat": r["repeat"],
                                    "outcome": "unresolved", "reviewer": None, "notes": ""}) + "\n")
    return int(any(r["status"] in ("target_error", "detector_error") for r in records))


if __name__ == "__main__":
    sys.exit(main())
