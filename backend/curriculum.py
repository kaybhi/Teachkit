"""
Syllabus assembly — builds the 32-week lesson list a teacher sees before
enrichment. Curriculum content itself (theme/grammar/vocab per week) now
comes from curriculum_data.py/curriculum_lookup.py (a full port of the
validated lesson-planner engine, covering School/Adult/Business tracks),
replacing the old single-level, hardcoded `WEEKS` template.

`build_ppp_activities`/`build_materials` are unchanged from the original
shell — they generate lightweight, zero-AI-call placeholder content so the
dashboard has *something* to show before a teacher runs `/enrich` on a
given week (which replaces this with the real, validated prose script +
sheets from prompt_builders.py).
"""
from curriculum_data import LEVELS_BY_ID
from curriculum_lookup import get_curriculum_for_week


def build_ppp_activities(theme: str, grammar: str, vocab: list, priorities: list, activity_types: list) -> dict:
    """
    Build a PPP (Presentation-Practice-Production) activity plan
    tailored to the teacher's priority skills and preferred activity types.
    """
    top_skill = priorities[0] if priorities else "Speaking"
    # Filter/rank activity types
    at = activity_types if activity_types else ["Games", "Pair work", "Group work", "Songs", "Role-play"]

    presentation = {
        "phase": "Presentation",
        "duration_min": 15,
        "activities": [
            {
                "title": f"Warm-up: '{theme}' brainstorm",
                "description": f"Elicit prior knowledge on '{theme}'. Show flashcards / images. Introduce key vocabulary: {', '.join(vocab[:5])}.",
                "type": "Flashcards / Whole class",
                "skill": "Listening",
            },
            {
                "title": f"Grammar spotlight: {grammar}",
                "description": f"Present the target grammar ({grammar}) with 3-4 clear examples on the board. Use gestures and mini-dialogues.",
                "type": "Teacher-led",
                "skill": "Listening",
            },
        ],
    }

    practice = {
        "phase": "Practice",
        "duration_min": 20,
        "activities": [
            {
                "title": f"Controlled drill: {grammar}",
                "description": f"Students complete a gap-fill worksheet on {grammar}. Correct in pairs, then whole class.",
                "type": at[1] if len(at) > 1 else "Pair work",
                "skill": "Writing",
            },
            {
                "title": f"Vocabulary game with '{theme}' words",
                "description": f"Play a fun game (Pictionary / Memory / Kahoot!) with the day's vocabulary: {', '.join(vocab[5:10]) if len(vocab) > 5 else ', '.join(vocab)}.",
                "type": at[0] if at else "Games",
                "skill": "Reading",
            },
        ],
    }

    production = {
        "phase": "Production",
        "duration_min": 20,
        "activities": [
            {
                "title": f"Free {top_skill.lower()} task",
                "description": f"Students use the target grammar ({grammar}) and vocabulary in a communicative task related to '{theme}'. Circulate and provide feedback.",
                "type": at[2] if len(at) > 2 else "Group work",
                "skill": top_skill,
            },
            {
                "title": "Wrap-up & self-assessment",
                "description": "Students share one new thing they learned. Quick thumbs-up self-check on lesson objectives.",
                "type": "Whole class",
                "skill": "Speaking",
            },
        ],
    }

    return {
        "presentation": presentation,
        "practice": practice,
        "production": production,
    }


def build_materials(week_data: dict) -> list:
    """Build a detailed materials list for a given week."""
    return [
        f"Flashcards: {week_data['theme']} ({len(week_data['vocabulary'])} cards)",
        f"Worksheet: {week_data['grammar']} (1 page, printable A4)",
        "Whiteboard + markers",
        "Projector / IWB for images and short videos",
        f"Audio track: pronunciation of '{week_data['theme']}' vocabulary (MP3)",
        "Student notebooks + coloured pens",
        "Timer (for game rounds)",
        f"Optional: short authentic video (2-3 min) on '{week_data['theme']}'",
    ]


def _vocab_string_to_list(vocab) -> list:
    """Curriculum vocab is a single resolved string (e.g. "hello, goodbye,
    my name is") or None for undetailed levels — build_ppp_activities/
    build_materials expect a list, so split on commas."""
    if not vocab:
        return []
    return [v.strip() for v in vocab.split(",") if v.strip()]


def _placeholder_objectives(theme: str, grammar) -> list:
    """The old CM2-only WEEKS template had a hand-written `objectives` list
    per week; the ported curriculum data doesn't carry that field, so
    generate a generic placeholder — real objectives come from `/enrich`'s
    AI-generated teacher script, which has an actual "Lesson aim" section."""
    objectives = [f"Understand and use vocabulary related to {theme}"]
    if grammar:
        objectives.append(f"Apply the target grammar: {grammar}")
    objectives.append("Practise the lesson's target language across speaking, listening, reading and writing")
    return objectives


def generate_full_syllabus(
    class_type: str, level_id: str, priorities: list, activity_types: list
) -> list:
    """Generate the complete 32-week syllabus for the given class type/level,
    personalised with the teacher's priorities and activity types. Covers
    School (CM1/CM2/6ème/...), Adult, and Business tracks via
    curriculum_lookup.get_curriculum_for_week — unlike the old CM2-only
    template this replaces."""
    level = LEVELS_BY_ID.get(level_id)
    if not level:
        raise ValueError(f"Unknown level_id: {level_id}")

    lessons = []
    for week in range(1, 33):
        c = get_curriculum_for_week(level, week)
        vocab_list = _vocab_string_to_list(c["vocab"])
        ppp = build_ppp_activities(c["theme"], c["grammar"] or "this week's target language", vocab_list, priorities, activity_types)
        week_data = {"theme": c["theme"], "grammar": c["grammar"] or "this week's target language", "vocabulary": vocab_list}
        lessons.append({
            "week": week,
            "title": c["theme"],
            "theme": c["theme"],
            "cefr_level": level["cefr"],
            "grammar": c["grammar"],
            "vocabulary": vocab_list,
            "objectives": _placeholder_objectives(c["theme"], c["grammar"]),
            "materials": build_materials(week_data),
            "ppp": ppp,
            "notes": "",
            "class_type": class_type,
            "special_topic_key": None,
            "pack": None,
            "pack_generated_at": None,
        })
    return lessons
