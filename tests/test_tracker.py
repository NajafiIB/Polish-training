import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tracker


class TrackerTests(unittest.TestCase):
    def test_generate_next_prompt_contains_focus(self):
        text = tracker.generate_next_prompt()
        self.assertIn("Continue Polish B1 training", text)
        self.assertIn("mój/moja/moje", text)

    def test_generate_drill_contains_known_error(self):
        text = tracker.generate_drill()
        self.assertIn("w średnie miasto", text)
        self.assertIn("w średnim mieście", text)

    def test_add_session_updates_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state_path = tmp_path / "learning_state.json"
            error_path = tmp_path / "error_log.csv"
            sentence_path = tmp_path / "sentence_bank.md"
            history_path = tmp_path / "session_history.md"
            drill_path = tmp_path / "daily_drill.md"
            prompt_path = tmp_path / "next_session_prompt.md"
            state_path.write_text(json.dumps({
                "current_level": "A2+",
                "learner_profile": {"name": "Test", "main_goal": "B1"},
                "covered_topics": [],
                "weaknesses": {},
                "known_sentences": [],
                "next_session_focus": []
            }), encoding="utf-8")
            sentence_path.write_text("# Sentence Bank\n", encoding="utf-8")
            history_path.write_text("# Session History\n", encoding="utf-8")
            session = tmp_path / "session.json"
            session.write_text(json.dumps({
                "date": "2026-04-26",
                "session_title": "Test session",
                "topics": ["city"],
                "errors": [{
                    "wrong": "mój miasto",
                    "correct": "moje miasto",
                    "category": "agreement",
                    "rule": "miasto is neuter",
                    "severity": 5,
                    "repeat": True
                }],
                "new_sentences": ["Moje miasto jest wygodne do życia."],
                "level_estimate": "B1-",
                "next_focus": ["agreement"],
                "notes": "Test note"
            }), encoding="utf-8")

            with patch.object(tracker, "STATE_PATH", state_path), \
                 patch.object(tracker, "ERROR_LOG_PATH", error_path), \
                 patch.object(tracker, "SENTENCE_BANK_PATH", sentence_path), \
                 patch.object(tracker, "SESSION_HISTORY_PATH", history_path), \
                 patch.object(tracker, "DAILY_DRILL_PATH", drill_path), \
                 patch.object(tracker, "NEXT_PROMPT_PATH", prompt_path):
                tracker.add_session(session)
                state = json.loads(state_path.read_text(encoding="utf-8"))
                self.assertEqual(state["current_level"], "B1-")
                self.assertIn("city", state["covered_topics"])
                self.assertIn("Moje miasto", sentence_path.read_text(encoding="utf-8"))
                self.assertIn("mój miasto", error_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
