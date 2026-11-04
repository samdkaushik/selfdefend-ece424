"""Harness contract checks; uses a mocked HTTP response, never a real model."""
import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import harness as h


def settings(**kwargs):
    values = dict(mode="mock", target=None, shadow=None, light=None,
                  endpoint="http://127.0.0.1:11434", seed=424,
                  dataset=str(h.ROOT / "data/sanity.jsonl"), out="unused", command="run")
    values.update(kwargs)
    return argparse.Namespace(**values)


class HarnessTests(unittest.TestCase):
    def test_parser(self):
        h.selftest()

    def test_matrix_gating_and_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = settings(out=str(Path(tmp) / "run"))
            h.run(args)
            h.verify(args)
            path = Path(args.out) / "trace.jsonl"
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(rows), 16)
            self.assertEqual(sum(r["status"] == "detector_error" for r in rows), 6)
            self.assertEqual(sum(r["target_called"] for r in rows), 7)
            path.write_text(path.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "Hash mismatch"):
                h.verify(args)

    def test_ollama_request_response_contract(self):
        response = {"done": True, "model": "test-model", "message": {"content": '{"decision":"ALLOW"}'}}
        with patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as call:
            content, elapsed, metadata = h.ollama("http://127.0.0.1:11434", "test-model", [], 424, True)
            body = json.loads(call.call_args.args[0].data)
            self.assertFalse(body["stream"])
            self.assertEqual(body["format"], "json")
            self.assertEqual(body["options"]["seed"], 424)
            self.assertEqual(h.parse_decision(content), "ALLOW")
            self.assertGreaterEqual(elapsed, 0)
            self.assertEqual(metadata["model"], "test-model")
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b'{"done":false}')):
            with self.assertRaisesRegex(ValueError, "Incomplete"):
                h.ollama("http://127.0.0.1:11434", "test", [], 424)

    def test_live_target_failure_not_scored_as_success(self):
        case = {"id": "x", "label": "benign", "split": "dev", "prompt": "Hello"}
        with patch("harness.ollama", side_effect=TimeoutError("injected target timeout")):
            result = h.execute(case, "target_only", settings(mode="ollama", target="test"))
        self.assertEqual(result["status"], "target_error")
        self.assertIsNone(result["released_response"])

    def test_live_detector_failure_blocks_target(self):
        case = {"id": "x", "label": "benign", "split": "dev", "prompt": "Hello"}
        with patch("harness.ollama", side_effect=TimeoutError("injected detector timeout")) as call:
            result = h.execute(case, "pdirect", settings(mode="ollama", target="test", shadow="test-shadow"))
        self.assertEqual(call.call_count, 1)
        self.assertFalse(result["target_called"])
        self.assertEqual(result["decision"], "BLOCK")

    def test_input_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            dataset = Path(tmp) / "cases.jsonl"
            c = {"id": "x", "label": "attack", "split": "dev", "prompt": "unique"}
            dataset.write_text(json.dumps(c) + "\n" + json.dumps(c) + "\n")
            with self.assertRaisesRegex(ValueError, "unique"):
                h.load_cases(dataset)
            dataset.write_text(json.dumps(c) + "\n")
            with self.assertRaisesRegex(ValueError, "local HTTP"):
                h.run(settings(mode="ollama", dataset=str(dataset), endpoint="https://example.com"))
            with self.assertRaisesRegex(ValueError, "distinct"):
                h.run(settings(mode="ollama", dataset=str(dataset), target="a", shadow="b", light="b"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
