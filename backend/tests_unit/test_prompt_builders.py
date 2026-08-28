"""
Unit tests for prompt_builders.py — focused on split_sheet_content (the
zero-repetition boundary split) since that's the safety-critical, easy-to-
silently-break piece: a regression here means Teacher's Script / Answer Key
/ Activity Sheets content leaks across documents, which is the exact
"notice that the answer key and teacher's script have no repitition"
requirement the user gave directly.

Plain unittest — see test_curriculum_lookup.py for why (avoids colliding
with backend/tests/conftest.py, which is Emergent's live-integration
harness and raises at import time without a running backend).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompt_builders import (  # noqa: E402
    build_script_prompt,
    exercise_type_spec,
    split_sheet_content,
    strip_leading_name_date_line,
)


class SplitSheetContentTests(unittest.TestCase):
    def test_splits_on_answer_key_marker(self):
        content = (
            "Name: ___________ Date: ___________\n"
            "SHEET A — SPEAKING\n"
            "1. What do you do?\n"
            "2. Where do you work?\n"
            "----------\n"
            "ANSWER KEY — Do not distribute\n"
            "1. Open answer\n"
            "2. Open answer\n"
        )
        main_lines, key_lines = split_sheet_content(content)
        main_text = "\n".join(main_lines)
        key_text = "\n".join(key_lines)
        self.assertIn("SHEET A", main_text)
        self.assertNotIn("Open answer", main_text)
        self.assertIn("ANSWER KEY", key_text)
        self.assertIn("Open answer", key_text)

    def test_splits_on_teacher_notes_marker_for_speaking_sheets(self):
        content = "Name: ___ Date: ___\n1. Talk about your day.\n---\nTEACHER NOTES\nRun as pair work, 10 min.\n"
        main_lines, key_lines = split_sheet_content(content)
        self.assertNotIn("pair work", "\n".join(main_lines))
        self.assertIn("pair work", "\n".join(key_lines))

    def test_marker_inside_markdown_heading_is_still_detected(self):
        content = "1. Item one\n## Answer Key\n1. Answer\n"
        main_lines, key_lines = split_sheet_content(content)
        self.assertEqual(main_lines, ["1. Item one"])
        self.assertIn("Answer Key", "\n".join(key_lines))

    def test_no_marker_means_everything_is_main(self):
        # Matches JS `content.split(/\r?\n/)` semantics exactly: a trailing
        # newline produces a trailing empty string, not just the 2 content lines.
        content = "1. Item one\n2. Item two\n"
        main_lines, key_lines = split_sheet_content(content)
        self.assertEqual(main_lines, ["1. Item one", "2. Item two", ""])
        self.assertEqual(key_lines, [])


class StripLeadingNameDateLineTests(unittest.TestCase):
    def test_strips_when_present(self):
        lines = ["Name: ___________ Date: ___________", "Title", "1. Item"]
        result = strip_leading_name_date_line(lines)
        self.assertEqual(result, ["Title", "1. Item"])

    def test_leaves_untouched_when_absent(self):
        lines = ["Title", "1. Item"]
        self.assertEqual(strip_leading_name_date_line(lines), lines)


class ExerciseTypeSpecTests(unittest.TestCase):
    def test_multiplechoice_forbids_optionless_items(self):
        # Pins the teacher-reported bug fix: every MC item must require
        # exactly 3 lettered options, no bare fill-in-the-blank items.
        spec = exercise_type_spec("multiplechoice")
        self.assertIn("EVERY single item", spec)
        self.assertIn("3 lettered options", spec)
        self.assertIn("Do not let any item become a plain fill-in-the-blank", spec)

    def test_all_eight_types_have_specs(self):
        for key in [
            "gapfill", "matching", "spotmistake", "multiplechoice",
            "truefalse", "wordorder", "guidedwriting", "pictureqa",
        ]:
            self.assertTrue(exercise_type_spec(key), f"missing spec for {key}")

    def test_unknown_type_returns_empty(self):
        self.assertEqual(exercise_type_spec("nonsense"), "")


class BuildScriptPromptTests(unittest.TestCase):
    def test_contains_form_function_and_six_word_vocab_cap(self):
        level = {"label": "B1", "cefr": "B1", "cycle": "Business", "ages": "18+", "band": 3}
        curriculum = {
            "block": "Block 2", "date_range": "x", "theme": "Arranging meetings",
            "grammar": "Future forms", "vocab": "set up (a meeting), schedule",
        }
        prompt = build_script_prompt(
            level, 8, curriculum, ["speaking", "listening"], 60, 4,
            activity_types=["Role-play"], extension_activity=True,
        )
        self.assertIn("FORM", prompt)
        self.assertIn("FUNCTION", prompt)
        self.assertIn("max 6 words", prompt)
        self.assertIn("no mime, no TPR", prompt)  # adult track note
        self.assertIn('NO "Teacher: ...', prompt)  # prohibits dialogue-transcript style

    def test_school_level_gets_tpr_allowance_not_adult_note(self):
        level = {"label": "CM1", "cefr": "A1", "cycle": "Cycle 3", "ages": "9-10", "band": 1}
        curriculum = {"block": "Block 1", "date_range": "x", "theme": "Colours", "grammar": None, "vocab": None}
        prompt = build_script_prompt(level, 1, curriculum, ["speaking"], 60, 6, activity_types=["Games"])
        self.assertIn("Gesture/TPR is fine", prompt)


if __name__ == "__main__":
    unittest.main()
