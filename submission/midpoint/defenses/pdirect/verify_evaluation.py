"""Audit saved evaluation evidence without contacting a model."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import defense
import evaluate


def verify(folder):
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    source_hashes = {name.replace("\\", "/"): digest
                     for name, digest in manifest["source_sha256"].items()}
    if len(source_hashes) != len(manifest["source_sha256"]):
        raise ValueError("Ambiguous normalized source paths")
    data = (folder / "inputs.jsonl").read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest["dataset_sha256"]:
        raise ValueError("Dataset hash mismatch")
    cases = {c["id"]: c for c in defense.read_cases(data)}
    frozen = json.loads((folder / "evaluation_freeze.json").read_text(encoding="utf-8"))
    prompt_hash = hashlib.sha256((folder / "detector_prompt.txt").read_bytes()).hexdigest()
    if prompt_hash != frozen["prompt_sha256"]:
        raise ValueError("Saved prompt differs from freeze")
    if prompt_hash != source_hashes["defenses/pdirect/detector_prompt.txt"]:
        raise ValueError("Manifest prompt hash mismatch")
    if frozen.get("detector_source_sha256"):
        if frozen["detector_source_sha256"] != source_hashes["defenses/pdirect/defense.py"]:
            raise ValueError("Detector source differs from frozen implementation")
        if frozen["detector_settings"] != manifest.get("detector_settings"):
            raise ValueError("Detector settings differ from freeze")
        catalog = manifest["runtime"].get("models", {})
        models = catalog.get("models", []) if isinstance(catalog, dict) else []
        matching = [m for m in models if isinstance(m, dict) and m.get("name") == frozen["model"]]
        if len(matching) != 1 or matching[0].get("digest") != frozen.get("model_digest"):
            raise ValueError("Recorded model digest differs from freeze")
    for name, expected in source_hashes.items():
        saved = folder / "source" / name
        if hashlib.sha256(saved.read_bytes()).hexdigest() != expected:
            raise ValueError("Source hash mismatch: " + name)
    records = [json.loads(line) for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    expected = Counter((case, config, repeat)
                       for case in cases for config in ("target_only", "pdirect")
                       for repeat in range(1, manifest["repeats"] + 1))
    actual = Counter((r["case_id"], r["config"], r["repeat"]) for r in records)
    if actual != expected:
        raise ValueError("Missing, duplicate, or unexpected paired records")
    for sequence, r in enumerate(records, 1):
        case = cases[r["case_id"]]
        if r["sequence"] != sequence or any(r[k] != case[k] for k in ("prompt", "label", "category")):
            raise ValueError("Record metadata/input mismatch")
        if r["config"] == "pdirect":
            detector = r["detector"]
            if detector["status"] == "ok":
                raw = detector["raw_response"]
                verdict = defense.parse_verdict(raw) if frozen.get("version", "").startswith("pdirect-v2") else raw.strip()
                if verdict != detector["decision"] or detector["done_reason"] != "stop":
                    raise ValueError("Detector verdict/completion differs from raw output")
            allowed = detector["status"] == "ok" and detector["decision"] == "ALLOW"
            if r["target_called"] != allowed:
                raise ValueError("Target gate invariant failed")
            if not allowed and r["status"] not in ("blocked", "detector_error"):
                raise ValueError("Invalid withheld status")
    saved_summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    if evaluate.summarize(records) != saved_summary:
        raise ValueError("Summary does not match raw trace")
    review_path = folder / "review.assisted.jsonl"
    if review_path.exists():
        reviews = [json.loads(line) for line in review_path.read_text(encoding="utf-8").splitlines()]
        if Counter(r["sequence"] for r in reviews) != Counter(r["sequence"] for r in records):
            raise ValueError("Review does not cover every record exactly once")
        by_sequence = {r["sequence"]: r for r in records}
        for review in reviews:
            record = by_sequence[review["sequence"]]
            if any(review[k] != record[k] for k in ("case_id", "config", "repeat")):
                raise ValueError("Review metadata mismatch")
            digest = hashlib.sha256((record["response"] or "").encode()).hexdigest()
            if review["response_sha256"] != digest:
                raise ValueError("Review response hash mismatch")
        counts = {config: dict(Counter(r["outcome"] for r in reviews if r["config"] == config))
                  for config in ("target_only", "pdirect")}
        if counts != json.loads((folder / "review_summary.json").read_text(encoding="utf-8")):
            raise ValueError("Review summary mismatch")
    print(f"PASS: {len(cases)} cases, {len(records)} paired records; hashes, inputs, gate, and summary verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    verify(parser.parse_args().run)
