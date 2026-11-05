"""Replay an archived evaluated version in isolation, without replacing active code."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True, help="Run containing source snapshots")
    parser.add_argument("--dataset", type=Path, help="Defaults to the archived inputs")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--machine-note", required=True)
    args = parser.parse_args()
    original = args.run.resolve()
    output = args.out.resolve()
    if output.exists():
        parser.error("Output directory already exists")
    manifest = json.loads((original / "manifest.json").read_text(encoding="utf-8"))
    dataset = (args.dataset or original / "inputs.jsonl").resolve()
    with tempfile.TemporaryDirectory(prefix="pdirect-replay-") as temporary:
        stage = Path(temporary)
        for name, expected in manifest["source_sha256"].items():
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("Invalid archived source path")
            data = (original / "source" / relative).read_bytes()
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("Archived source hash mismatch: " + name)
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        component = stage / "defenses/pdirect"
        for name in ("evaluation_freeze.json", "evaluation_freeze_v2.json", "evaluation_freeze_v2_1.json"):
            (component / name).write_bytes((original / "evaluation_freeze.json").read_bytes())
        command = [sys.executable, str(component / "evaluate.py"), "--dataset", str(dataset),
                   "--out", str(output), "--repeats", str(args.repeats),
                   "--machine-note", args.machine_note]
        result = subprocess.run(command, cwd=stage, capture_output=True, text=True, encoding="utf-8")
        if output.exists():
            (output / "replay_stdout.txt").write_text(result.stdout, encoding="utf-8")
            (output / "replay_stderr.txt").write_text(result.stderr, encoding="utf-8")
            (output / "replay_provenance.json").write_text(json.dumps({
                "source_run": str(original),
                "source_manifest_sha256": hashlib.sha256((original / "manifest.json").read_bytes()).hexdigest(),
                "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "exit_code": result.returncode,
                "note": "Archived implementation and instructions replayed in an isolated temporary source tree.",
            }, indent=2) + "\n", encoding="utf-8")
            # Early v1 runners did not automatically preserve source copies.
            for name in manifest["source_sha256"]:
                destination = output / "source" / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    destination.write_bytes((stage / name).read_bytes())
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
