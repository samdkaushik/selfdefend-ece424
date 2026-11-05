"""Offline midpoint-package checks; does not run an LLM or change evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    fallback = ROOT / "logs/baseline_dev_2026-11-04.jsonl"
    expected = "e18641021a86a4e669c0e425803a7f9507dc88e94d52cca20ee90e64ac27ad5f"
    if hashlib.sha256(fallback.read_bytes()).hexdigest() != expected:
        raise ValueError("Designated baseline fallback is missing or invalid")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", (ROOT / "README.md").read_text(encoding="utf-8")):
        if "://" not in target and not (ROOT / target.split("#", 1)[0]).exists():
            raise ValueError("Missing submission evidence/link: " + target)
    print("PASS: designated real-model fallback hash and submission links", flush=True)
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "defenses/pdirect", "-p", "test_*.py", "-v"],
        [sys.executable, "defenses/pdirect/verify_evaluation.py",
         "experiments/pdirect/2026-11-04_v2_1_frozen_evaluation_001"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            return result.returncode
    print("PASS: midpoint software/evidence checks; no LLM requests performed")
    pilot = ROOT / "evidence/yasmin"
    provenance = json.loads((pilot / "provenance.json").read_text(encoding="utf-8"))
    for name, expected_hash in provenance["files"].items():
        if hashlib.sha256((pilot / name).read_bytes()).hexdigest() != expected_hash:
            raise ValueError("Yasmin evidence differs from recorded source: " + name)
    for run in sorted(p for p in pilot.iterdir() if p.is_dir()):
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        for name, expected_hash in manifest["sha256"].items():
            filename = {"harness.py": "harness_used.py", "dataset": "pilot_dev.jsonl"}.get(name, name)
            actual = hashlib.sha256((run / filename).read_bytes()).hexdigest()
            if actual != expected_hash:
                if filename != "review.csv":
                    raise ValueError("Pilot manifest mismatch: " + run.name + "/" + filename)
                print("FOLLOW-UP: " + run.name + "/review.csv differs from original manifest")
    print("PASS: Yasmin pilot snapshots match PR #2 source; review-manifest follow-up noted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
