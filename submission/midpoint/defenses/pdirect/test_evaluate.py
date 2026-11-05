"""Checks that experimental accounting cannot hide failed requests."""
import unittest
from contextlib import redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import evaluate
import verify_evaluation


class EvaluationTests(unittest.TestCase):
    def test_runner_saves_reproducible_pairs_sources_and_warmup(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            dataset = folder / "data.jsonl"
            dataset.write_text(json.dumps({"id": "b", "prompt": "Hello", "label": "benign", "category": "ordinary"}) + "\n")
            output = folder / "run"
            target = {"config": "target_only", "status": "ok", "target_called": True,
                      "response": "Hello", "error": None, "target_details": {}, "elapsed_ms": 1}
            guarded = dict(target, config="pdirect", detector={"status": "ok", "decision": "ALLOW",
                           "raw_response": '{"decision":"ALLOW"}', "done_reason": "stop"})
            argv = ["evaluate.py", "--dataset", str(dataset), "--out", str(output), "--repeats", "2", "--machine-note", "Mock test"]
            freeze = json.loads((evaluate.HERE / "evaluation_freeze_v2_1.json").read_text(encoding="utf-8"))
            metadata = {"models": {"models": [{"name": freeze["model"], "digest": freeze["model_digest"]}]}}
            with patch.object(evaluate.sys, "argv", argv), \
                 patch.object(evaluate.defense, "runtime_metadata", return_value=metadata), \
                 patch.object(evaluate.defense, "detect", return_value={"status": "ok"}), \
                 patch.object(evaluate, "target_only", side_effect=lambda prompt: dict(target, prompt=prompt)), \
                 patch.object(evaluate.defense, "defend", side_effect=lambda prompt: dict(guarded, prompt=prompt)):
                self.assertEqual(evaluate.main(), 0)
            records = [json.loads(line) for line in (output / "trace.jsonl").read_text().splitlines()]
            self.assertEqual(len(records), 4)  # Warmup is separate from measured pairs.
            manifest = json.loads((output / "manifest.json").read_text())
            for name, digest in manifest["source_sha256"].items():
                self.assertEqual(hashlib.sha256((output / "source" / name).read_bytes()).hexdigest(), digest)
            verify_evaluation.verify(output)
            # A duplicated/missing pair must not pass an evidence audit.
            records[-1] = records[0]
            (output / "trace.jsonl").write_text(''.join(json.dumps(r) + '\n' for r in records))
            with self.assertRaisesRegex(ValueError, "paired records"):
                verify_evaluation.verify(output)

    def test_changed_model_digest_is_rejected_before_inference(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            argv = ["evaluate.py", "--out", str(output), "--machine-note", "Mock test"]
            metadata = {"models": {"models": [{"name": evaluate.defense.SHADOW_MODEL, "digest": "different"}]}}
            with patch.object(evaluate.sys, "argv", argv), \
                 patch.object(evaluate.defense, "runtime_metadata", return_value=metadata), \
                 patch.object(evaluate.defense, "detect") as detect, \
                 patch.object(evaluate, "target_only") as target, \
                 redirect_stderr(io.StringIO()), \
                 self.assertRaises(SystemExit) as error:
                evaluate.main()
            self.assertEqual(error.exception.code, 2)
            self.assertFalse(output.exists())
            detect.assert_not_called()
            target.assert_not_called()

    def test_errors_remain_in_attempts_but_not_success_latency(self):
        base = {"config": "pdirect", "case_id": "attack-1", "label": "attack",
                "category": "instruction_extraction", "target_details": None}
        records = [dict(base, status="blocked", elapsed_ms=10,
                        detector={"status": "ok", "decision": "BLOCK"}),
                   dict(base, status="detector_error", elapsed_ms=1000,
                        detector={"status": "error", "decision": "BLOCK"}),
                   dict(base, status="ok", elapsed_ms=100,
                        detector={"status": "ok", "decision": "ALLOW"})]
        result = evaluate.summarize(records)["pdirect"]
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(result["unique_cases"], 1)
        self.assertEqual(result["latency_all_attempts"]["p95_ms"], 1000)
        self.assertEqual(result["latency_without_errors"]["n"], 2)
        group = result["detector_by_category"]["instruction_extraction"]
        self.assertEqual(group["valid_block"], 1)
        self.assertEqual(group["valid_allow"], 1)
        self.assertEqual(group["detector_errors"], 1)

    def test_target_truncation_is_preserved_and_empty_groups_are_null(self):
        record = {"config": "target_only", "case_id": "benign-1", "label": "benign",
                  "status": "ok", "elapsed_ms": 20,
                  "target_details": {"done_reason": "length"}}
        result = evaluate.summarize([record])
        self.assertEqual(result["target_only"]["target_truncations"], 1)
        self.assertEqual(result["target_only"]["by_label"]["attack"]["n"], 0)
        self.assertIsNone(result["pdirect"]["latency_all_attempts"]["median_ms"])

    def test_nearest_rank_p95_does_not_interpolate_unobserved_latency(self):
        result = evaluate.latency([{"elapsed_ms": n} for n in range(1, 21)])
        self.assertEqual(result, {"n": 20, "median_ms": 10.5, "p95_ms": 19})


if __name__ == "__main__":
    unittest.main()
