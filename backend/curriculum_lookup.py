"""
Curriculum resolution logic — ported 1:1 from the validated lesson-planner
engine (`index.html`, lines 988-1138 as of 2026-08-14): curriculumTierKey,
getWeekInfo, weekOffsetInBlock, resolveWeekVocab, getCurriculumForWeek,
specialTopicTier.

`state.specialTopic` (a JS global) becomes an explicit `special_topic_key`
parameter here — everything else is a faithful, same-shape port.
"""
from typing import Optional, TypedDict

from curriculum_data import (
    ADULT_GENERAL_CURRICULUM,
    BUSINESS_CURRICULUM,
    CM2_CURRICULUM,
    MASTER_CURRICULUM,
    SPECIAL_TOPICS,
)


class CurriculumResult(TypedDict):
    block: str
    date_range: str
    theme: Optional[str]
    grammar: Optional[str]
    vocab: Optional[str]
    detailed: bool
    source: str


def curriculum_tier_key(level: dict) -> str:
    if level["cycle"] in ("Adultes", "Business"):
        return "adultes"
    if level["cycle"] in ("Cycle 2", "Cycle 3"):
        return "primaires"
    return "college"


def get_week_info(week: int) -> dict:
    for row in MASTER_CURRICULUM:
        if row["week"] == week:
            return row
    return MASTER_CURRICULUM[0]


def week_offset_in_block(week: int) -> int:
    """0-indexed position of `week` among the weeks sharing its block, e.g.
    week 9 is index 1 within block 2 (weeks 8-14) — used to pick that
    week's entry out of a per-week vocab array."""
    wk = get_week_info(week)
    weeks_in_block = sorted(
        row["week"] for row in MASTER_CURRICULUM if row["block"] == wk["block"]
    )
    try:
        return weeks_in_block.index(week)
    except ValueError:
        return 0


def resolve_week_vocab(vocab, week: int) -> Optional[str]:
    """A curriculum row's `vocab` field is either a plain string (CM2's
    weekly plan, already one row per week) or a list of per-week strings
    (the adult/business block-level tables) — resolve to this week's
    string either way."""
    if not isinstance(vocab, list):
        return vocab
    if not vocab:
        return None
    idx = min(week_offset_in_block(week), len(vocab) - 1)
    return vocab[idx]


def special_topic_tier(level: dict) -> str:
    """Maps a level's band (0-4, same scale used everywhere else) to one
    of a special topic's three complexity tiers."""
    band = level["band"]
    if band <= 1:
        return "young"
    if band <= 3:
        return "mid"
    return "advanced"


def get_curriculum_for_week(
    level: dict, week: int, special_topic_key: Optional[str] = None
) -> CurriculumResult:
    wk = get_week_info(week)

    if special_topic_key:
        topic = next((t for t in SPECIAL_TOPICS if t["key"] == special_topic_key), None)
        if topic:
            tier = topic["tiers"][special_topic_tier(level)]
            return {
                "block": "Special topic",
                "date_range": f"{wk['start']} – {wk['end']}",
                "theme": topic["theme"],
                "grammar": tier["grammar"],
                "vocab": tier["vocab"],
                "detailed": True,
                "source": f"special topic override (not this week's curriculum) — {level['cefr']}-level content",
            }

    detailed = None
    source = "school-wide curriculum map (block-level topic)"

    if level["id"] == "cm2":
        detailed = next((r for r in CM2_CURRICULUM if r["week"] == week), None)
        if detailed:
            source = "CM2 weekly curriculum plan"
    elif level["cycle"] == "Adultes":
        detailed = next(
            (r for r in ADULT_GENERAL_CURRICULUM if r["block"] == wk["block"] and r["level"] == level["id"]),
            None,
        )
        if detailed:
            source = "adult general English curriculum"
    elif level["cycle"] == "Business":
        detailed = next(
            (r for r in BUSINESS_CURRICULUM if r["block"] == wk["block"] and r["level"] == level["id"]),
            None,
        )
        if detailed:
            source = "business English curriculum"

    return {
        "block": wk["name"],
        "date_range": f"{wk['start']} – {wk['end']}",
        "theme": detailed["theme"] if detailed else wk[curriculum_tier_key(level)],
        "grammar": detailed["grammar"] if detailed else None,
        "vocab": resolve_week_vocab(detailed["vocab"], week) if detailed else None,
        "detailed": bool(detailed),
        "source": source,
    }
