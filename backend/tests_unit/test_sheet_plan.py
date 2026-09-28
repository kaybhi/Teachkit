"""
Unit tests for sheet_plan.py — the "one job per sheet" planner that stops a
lesson pack from being ten near-identical drills (real 5ème Week 6 pack: the
same 4 verbs ~119 times, the same 4 characters and the same "usually ... but
today" frame on every sheet). Plain unittest, see test_curriculum_lookup.py.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from curriculum_data import LEVELS_BY_ID  # noqa: E402
from prompt_builders import build_exercise_type_sheet_prompt, build_single_sheet_prompt  # noqa: E402
from sheet_plan import (  # noqa: E402
    allowed_speaking_formats,
    fallback_sheet_plan,
    parse_sheet_plan,
    sheet_plan_block,
    speaking_format_spec,
)

IDS = ["A", "B", "gapfill", "spotmistake", "wordorder"]
CURRICULUM = {
    "theme": "What's happening now — questions, negatives & contrast",
    "grammar": "Are you...? He isn't sleeping.",
    "vocab": "today, usually, but, wear, wait, run, smile",
    "block": "Block 1", "date_range": "x",
}
LEVEL = LEVELS_BY_ID["5e"]


class FallbackPlanTests(unittest.TestCase):
    def test_every_sheet_gets_its_own_setting_and_characters(self):
        plan = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)
        settings = [plan["sheets"][i]["setting"] for i in IDS]
        self.assertEqual(len(set(settings)), len(IDS))
        names = [n for i in IDS for n in plan["sheets"][i]["characters"]]
        self.assertEqual(len(names), len(set(names)), "a name is shared by two sheets")

    def test_vocab_slices_differ_and_none_uses_every_word(self):
        plan = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)
        slices = [tuple(plan["sheets"][i]["vocab"]) for i in IDS]
        self.assertGreater(len(set(slices)), 1)
        for sl in slices:
            self.assertLess(len(sl), 7)

    def test_different_weeks_give_different_cast(self):
        a = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=5)
        b = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)
        self.assertNotEqual(a["sheets"]["A"]["characters"], b["sheets"]["A"]["characters"])


class SpeakingFormatTests(unittest.TestCase):
    def test_adults_never_get_mime(self):
        self.assertNotIn("mimeguess", allowed_speaking_formats(LEVELS_BY_ID["biz-b1"]))

    def test_young_learners_only_get_simple_formats(self):
        fmts = allowed_speaking_formats(LEVELS_BY_ID["cm1"])
        self.assertEqual(set(fmts), {"mimeguess", "findsomeone", "dicegame"})

    def test_sheet_a_spec_uses_the_planned_format(self):
        spec = speaking_format_spec({"speaking_format": "infogap"}, student_count=4)
        self.assertIn("STUDENT A", spec)
        self.assertIn("small class of 4", spec)
        self.assertIsNone(speaking_format_spec({"speaking_format": "nonsense"}, 4))


class ParsePlanTests(unittest.TestCase):
    def setUp(self):
        self.fallback = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)

    def test_garbage_reply_falls_back_completely(self):
        self.assertEqual(parse_sheet_plan("sorry, no json", IDS, self.fallback, LEVEL), self.fallback)

    def test_good_reply_is_used_and_missing_fields_keep_fallback(self):
        raw = "Here you go:\n" + json.dumps({
            "speakingFormat": "dicegame",
            "sheets": {"A": {"facet": "questions", "setting": "at the zoo", "characters": ["Ines", "Ravi"], "vocab": ["run"]}},
        })
        plan = parse_sheet_plan(raw, IDS, self.fallback, LEVEL)
        self.assertEqual(plan["speaking_format"], "dicegame")
        self.assertEqual(plan["sheets"]["A"]["setting"], "at the zoo")
        self.assertEqual(plan["sheets"]["B"], self.fallback["sheets"]["B"])

    def test_format_not_allowed_for_level_is_rejected(self):
        raw = json.dumps({"speakingFormat": "roleplay", "sheets": {}})
        plan = parse_sheet_plan(raw, IDS, fallback_sheet_plan(IDS, LEVELS_BY_ID["cm1"], CURRICULUM, 6), LEVELS_BY_ID["cm1"])
        self.assertIn(plan["speaking_format"], allowed_speaking_formats(LEVELS_BY_ID["cm1"]))


class PromptWiringTests(unittest.TestCase):
    def test_plan_block_lists_the_other_sheets_settings(self):
        plan = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)
        block = sheet_plan_block(plan, "gapfill")
        self.assertIn("SHEET PLAN — MANDATORY", block)
        self.assertIn(plan["sheets"]["gapfill"]["setting"], block)
        self.assertIn(plan["sheets"]["B"]["setting"], block)  # listed under "do NOT reuse"

    def test_sheet_prompts_carry_the_plan(self):
        plan = fallback_sheet_plan(IDS, LEVEL, CURRICULUM, week=6)
        p1 = build_single_sheet_prompt("B", LEVEL, CURRICULUM, 4, ["Games"], "x", plan)
        p2 = build_exercise_type_sheet_prompt("gapfill", LEVEL, CURRICULUM, 4, ["Games"], "x", plan)
        p3 = build_single_sheet_prompt("A", LEVEL, CURRICULUM, 4, ["Games"], "x", plan)
        self.assertIn("SHEET PLAN — MANDATORY", p1)
        self.assertIn("SHEET PLAN — MANDATORY", p2)
        self.assertIn(plan["speaking_format"].upper()[:4], p3.upper())

    def test_no_plan_means_old_behaviour(self):
        p = build_single_sheet_prompt("B", LEVEL, CURRICULUM, 4, ["Games"], "x")
        self.assertNotIn("SHEET PLAN", p)


if __name__ == "__main__":
    unittest.main()
