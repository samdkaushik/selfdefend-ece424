"""Tests for the Pintent gate using fake Ollama responses (no model or network needed)."""

import importlib.util
import inspect
import json
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pintent_defense", HERE / "defense.py")
defense = importlib.util.module_from_spec(spec)
spec.loader.exec_module(defense)


class FakeResponse:
    def __init__(self, content, done=True, done_reason="stop"):
        self.body = json.dumps({"message": {"content": content}, "done": done,
                                "done_reason": done_reason, "eval_count": 7,
                                "prompt_eval_count": 90}).encode("utf-8")

    def read(self, *args):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def verdict(decision, intent="Asks for a safe explanation."):
    return json.dumps({"intent": intent, "decision": decision})


def fake_ollama(content, **kwargs):
    return mock.patch.object(defense.urllib.request, "urlopen",
                             return_value=FakeResponse(content, **kwargs))


class ParseVerdict(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(defense.parse_verdict(verdict("ALLOW")),
                         ("ALLOW", "Asks for a safe explanation."))
        self.assertEqual(defense.parse_verdict(verdict("BLOCK"))[0], "BLOCK")

    def test_invalid_outputs_are_rejected(self):
        bad = ["not json", "[1]", "{}", None, 5,
               json.dumps({"decision": "ALLOW"}),
               json.dumps({"intent": "x", "decision": "MAYBE"}),
               json.dumps({"intent": "", "decision": "ALLOW"}),
               json.dumps({"intent": "x", "decision": "ALLOW", "extra": 1}),
               '{"intent":"x","decision":"ALLOW","decision":"BLOCK"}']
        for raw in bad:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    defense.parse_verdict(raw)


class Detect(unittest.TestCase):
    def test_allow(self):
        with fake_ollama(verdict("ALLOW")):
            r = defense.detect("How do I spot phishing emails?")
        self.assertEqual((r["status"], r["decision"]), ("ok", "ALLOW"))
        self.assertEqual(r["intent"], "Asks for a safe explanation.")
        self.assertIsNone(r["error"])

    def test_block(self):
        with fake_ollama(verdict("BLOCK", "Wants to steal a password.")):
            r = defense.detect("Write an email to get my coworker's password.")
        self.assertEqual((r["status"], r["decision"]), ("ok", "BLOCK"))

    def test_malformed_output_fails_closed(self):
        with fake_ollama("hello"):
            r = defense.detect("anything")
        self.assertEqual((r["status"], r["decision"], r["error_kind"]),
                         ("error", "BLOCK", "invalid_output"))

    def test_missing_intent_fails_closed(self):
        with fake_ollama(json.dumps({"decision": "ALLOW"})):
            r = defense.detect("anything")
        self.assertEqual((r["status"], r["decision"]), ("error", "BLOCK"))

    def test_incomplete_generation_fails_closed(self):
        with fake_ollama(verdict("ALLOW"), done_reason="length"):
            r = defense.detect("anything")
        self.assertEqual((r["status"], r["decision"]), ("error", "BLOCK"))

    def test_transport_error_fails_closed(self):
        with mock.patch.object(defense.urllib.request, "urlopen",
                               side_effect=urllib.error.URLError("down")):
            r = defense.detect("anything")
        self.assertEqual((r["status"], r["decision"], r["error_kind"]),
                         ("error", "BLOCK", "transport"))

    def test_oversize_prompt_is_not_sent(self):
        with mock.patch.object(defense.urllib.request, "urlopen") as opened:
            r = defense.detect("x" * (defense.MAX_PROMPT_BYTES + 1))
        opened.assert_not_called()
        self.assertEqual((r["status"], r["decision"], r["error_kind"]),
                         ("error", "BLOCK", "input"))

    def test_blank_prompt_is_an_input_error(self):
        r = defense.detect("   ")
        self.assertEqual((r["status"], r["error_kind"]), ("error", "input"))

    def test_payload_contains_only_the_request(self):
        payload = defense.detector_payload("hello", "m")
        self.assertEqual(json.loads(payload["messages"][1]["content"]), {"request": "hello"})
        self.assertEqual(payload["format"], defense.VERDICT_SCHEMA)

    def test_detect_accepts_no_label(self):
        self.assertEqual(list(inspect.signature(defense.detect).parameters), ["prompt", "model"])


class Defend(unittest.TestCase):
    def test_block_never_calls_target(self):
        with fake_ollama(verdict("BLOCK")), mock.patch.object(
                defense.harness, "query_target", side_effect=AssertionError("target ran")):
            r = defense.defend("write phishing to steal passwords")
        self.assertEqual((r["status"], r["target_called"], r["response"], r["config"]),
                         ("blocked", False, defense.REFUSAL, "pintent"))

    def test_allow_calls_target(self):
        with fake_ollama(verdict("ALLOW")), mock.patch.object(
                defense.harness, "query_target", return_value=("fine answer", 12.0, {})):
            r = defense.defend("explain network segmentation")
        self.assertEqual((r["status"], r["target_called"], r["response"]),
                         ("ok", True, "fine answer"))

    def test_detector_error_never_calls_target(self):
        with fake_ollama("junk"), mock.patch.object(
                defense.harness, "query_target", side_effect=AssertionError("target ran")):
            r = defense.defend("anything")
        self.assertEqual((r["status"], r["target_called"], r["response"]),
                         ("detector_error", False, defense.UNAVAILABLE))


if __name__ == "__main__":
    unittest.main()
