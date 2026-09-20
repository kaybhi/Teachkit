"""
Unit tests for curriculum_lookup.py — pins the vocab-rotation-within-block
behavior (the bug fixed in the source engine on 2026-08-14: vocab must
change every week even when grammar spans a whole block) and the
block-boundary edge cases.

Deliberately plain `unittest`, run directly with `python3 -m unittest`, not
pytest — `backend/tests/conftest.py` is Emergent's live-integration-test
harness (requires a running backend + REACT_APP_BACKEND_URL) and raises at
import time if that's missing, so it must not be collected for these pure
logic tests.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from curriculum_data import ALL_LEVELS, LEVELS_BY_ID  # noqa: E402
from curriculum_lookup import (  # noqa: E402
    get_curriculum_for_week,
    get_week_info,
    resolve_week_vocab,
    special_topic_tier,
    week_offset_in_block,
)


class WeekOffsetInBlockTests(unittest.TestCase):
    def test_block2_offsets(self):
        # Block 2 = weeks 8-14 (7 weeks) — week 9 is index 1.
        self.assertEqual(week_offset_in_block(8), 0)
        self.assertEqual(week_offset_in_block(9), 1)
        self.assertEqual(week_offset_in_block(14), 6)

    def test_block_boundary_resets(self):
        # Week 7 is the last week of block 1 (offset 6); week 8 starts
        # block 2 fresh at offset 0 — the just-fixed bug was vocab NOT
        # resetting/rotating across this exact boundary.
        self.assertEqual(week_offset_in_block(7), 6)
        self.assertEqual(week_offset_in_block(8), 0)

    def test_unknown_week_falls_back_to_zero(self):
        self.assertEqual(week_offset_in_block(999), 0)


class ResolveWeekVocabTests(unittest.TestCase):
    def test_flat_string_passthrough(self):
        self.assertEqual(resolve_week_vocab("greetings, family", 1), "greetings, family")

    def test_array_rotates_per_week(self):
        vocab = ["a", "b", "c", "d", "e", "f", "g"]
        self.assertEqual(resolve_week_vocab(vocab, 8), "a")
        self.assertEqual(resolve_week_vocab(vocab, 9), "b")
        self.assertEqual(resolve_week_vocab(vocab, 14), "g")

    def test_array_shorter_than_block_clamps_to_last(self):
        # Block 3 is 5 weeks (15-19) but a vocab array might have fewer
        # entries — resolveWeekVocab clamps rather than indexing out of range.
        vocab = ["a", "b", "c"]
        self.assertEqual(resolve_week_vocab(vocab, 19), "c")

    def test_empty_array_returns_none(self):
        self.assertIsNone(resolve_week_vocab([], 8))


class GetCurriculumForWeekTests(unittest.TestCase):
    def test_business_b1_block2_vocab_rotates_grammar_stays_constant(self):
        """The exact case the user reported: 'the grammar target can be the
        same for 4 weeks but the vocab needs to change in every class. atm
        the vocab words remain the same for 4 weeks.'"""
        level = LEVELS_BY_ID["biz-b1"]
        results = [get_curriculum_for_week(level, wk) for wk in range(8, 15)]

        themes = {r["theme"] for r in results}
        grammars = {r["grammar"] for r in results}
        self.assertEqual(themes, {"Arranging meetings & simple emails"})
        self.assertEqual(grammars, {"Future forms for arrangements (will/going to), polite requests"})

        vocabs = [r["vocab"] for r in results]
        self.assertEqual(len(vocabs), len(set(vocabs)), f"vocab did not rotate: {vocabs}")
        self.assertEqual(vocabs[0], "set up (a meeting), schedule, arrange")
        self.assertEqual(vocabs[-1], "meeting logistics: agenda, minutes, attendees")

    def test_adult_b1_block2_vocab_rotates(self):
        level = LEVELS_BY_ID["adult-b1"]
        results = [get_curriculum_for_week(level, wk) for wk in range(8, 15)]
        vocabs = [r["vocab"] for r in results]
        self.assertEqual(len(vocabs), len(set(vocabs)))
        self.assertEqual(vocabs[0], "housing: rent, mortgage, flat, apartment")

    def test_block_boundary_week7_to_8_switches_content(self):
        level = LEVELS_BY_ID["biz-b1"]
        wk7 = get_curriculum_for_week(level, 7)
        wk8 = get_curriculum_for_week(level, 8)
        self.assertNotEqual(wk7["theme"], wk8["theme"])
        self.assertEqual(wk7["theme"], "Introducing yourself & your company")
        self.assertEqual(wk8["theme"], "Arranging meetings & simple emails")

    def test_cm2_uses_flat_per_week_vocab_unaffected_by_rotation_fix(self):
        level = LEVELS_BY_ID["cm2"]
        r1 = get_curriculum_for_week(level, 1)
        self.assertEqual(r1["vocab"], "greetings, family, numbers 1-100")
        self.assertTrue(r1["detailed"])
        self.assertEqual(r1["source"], "CM2 weekly curriculum plan")

    def test_school_level_without_own_detailed_plan_uses_band_curriculum(self):
        # CM1 has no CM2-style per-week plan of its own, but (as of the
        # 2026-09-18 fix) resolves to its band's real weekly curriculum
        # instead of the old flat block-level string that repeated the same
        # topic for a whole 5-7 week block.
        level = LEVELS_BY_ID["cm1"]
        result = get_curriculum_for_week(level, 1)
        self.assertTrue(result["detailed"])
        self.assertEqual(result["source"], "weekly curriculum plan (band 1)")
        self.assertIsNotNone(result["vocab"])
        self.assertIsNotNone(result["grammar"])
        self.assertEqual(result["theme"], "All about me")

    def test_school_band_topic_changes_within_2_weeks(self):
        # The rule that motivated this fix: a real 5ème class was stuck on
        # one theme for 7 straight weeks. No topic may now span more than 2.
        level = LEVELS_BY_ID["5e"]
        themes = [get_curriculum_for_week(level, wk)["theme"] for wk in range(1, 9)]
        self.assertEqual(themes[0], themes[1])
        self.assertNotEqual(themes[1], themes[2])
        self.assertEqual(themes[2], themes[3])
        self.assertNotEqual(themes[3], themes[4])

    def test_college_tier_now_differs_by_band_not_just_shared_string(self):
        # 6e (band 2) and a band-3/4 level must no longer share identical
        # theme text the way the old flat "college" block string did.
        sixieme = get_curriculum_for_week(LEVELS_BY_ID["6e"], 1)
        troisieme = get_curriculum_for_week(LEVELS_BY_ID["3e"], 1)
        self.assertNotEqual(sixieme["theme"], troisieme["theme"])

    def test_cm2_plan_unaffected_by_band_curriculum_fix(self):
        level = LEVELS_BY_ID["cm2"]
        result = get_curriculum_for_week(level, 1)
        self.assertEqual(result["source"], "CM2 weekly curriculum plan")
        self.assertEqual(result["theme"], "Greetings + family + numbers")

    def test_special_topic_override(self):
        level = LEVELS_BY_ID["biz-b1"]
        normal = get_curriculum_for_week(level, 8)
        override = get_curriculum_for_week(level, 8, special_topic_key="modals")
        self.assertEqual(override["block"], "Special topic")
        self.assertEqual(override["theme"], "Modal Verbs")
        self.assertTrue(override["detailed"])
        self.assertNotEqual(normal["theme"], override["theme"])


class SpecialTopicTierTests(unittest.TestCase):
    def test_band_to_tier_mapping(self):
        self.assertEqual(special_topic_tier({"band": 0}), "young")
        self.assertEqual(special_topic_tier({"band": 1}), "young")
        self.assertEqual(special_topic_tier({"band": 2}), "mid")
        self.assertEqual(special_topic_tier({"band": 3}), "mid")
        self.assertEqual(special_topic_tier({"band": 4}), "advanced")


class DataIntegrityTests(unittest.TestCase):
    def test_all_levels_resolve_curriculum_for_week_1_without_error(self):
        for level in ALL_LEVELS:
            result = get_curriculum_for_week(level, 1)
            self.assertIn("theme", result)

    def test_master_curriculum_covers_32_weeks(self):
        weeks = {row["week"] for row in get_week_info.__globals__["MASTER_CURRICULUM"]}
        self.assertEqual(weeks, set(range(1, 33)))


if __name__ == "__main__":
    unittest.main()
