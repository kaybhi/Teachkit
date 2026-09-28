"""
Sheet plan — one job per sheet. Ported from the local lesson engine
(index.html "SHEET PLAN", 2026-09-26).

Sheets used to be generated in parallel with no knowledge of each other, so a
pack came out as ~10 near-identical drills (same verbs, same characters, same
"usually ... but today" frame). Now one quick planning call runs first and
gives EVERY sheet its own job, language facet, setting, characters and
vocabulary slice, and tells each sheet what the others cover. If the planning
call fails or returns junk, a deterministic fallback plan is used, so lesson
generation never breaks.

Everything here is pure (no network) except that server.py makes the one AI
call with the prompt from build_sheet_plan_prompt().
"""
import json
from typing import Dict, List, Optional

SHEET_ROLES: Dict[str, str] = {
    "A": "PERSONALISE — a communicative speaking task (see the speaking format below)",
    "B": "RECOGNISE — listening for meaning, students react rather than write",
    "C": "READ FOR MEANING — a short text with comprehension questions",
    "D": "PRODUCE — students write their own sentences",
    "gapfill": "PRODUCE FORMS — complete sentences with the right form",
    "matching": "LINK MEANINGS — connect words, phrases or translations",
    "spotmistake": "NOTICE ERRORS — find and correct typical mistakes",
    "multiplechoice": "CHOOSE — recognise the right form among tempting distractors",
    "truefalse": "CHECK UNDERSTANDING — judge statements about the rule and about a situation",
    "wordorder": "BUILD SENTENCES — put jumbled words in order",
    "guidedwriting": "WRITE — a short guided paragraph with sentence starters",
    "pictureqa": "DESCRIBE — answer questions about a scene described in words",
}

SHEET_LABELS: Dict[str, str] = {
    "A": "Speaking", "B": "Listening", "C": "Reading", "D": "Writing",
    "gapfill": "Gap Fill", "matching": "Matching", "spotmistake": "Spot the Mistake",
    "multiplechoice": "Multiple Choice", "truefalse": "True or False",
    "wordorder": "Word Order", "guidedwriting": "Guided Writing", "pictureqa": "Picture-Based Questions",
}

SCHOOL_SETTINGS = ["at the bus stop", "in the school canteen", "at the park", "on the phone with a friend",
                   "at a birthday party", "in a shop", "at the sports centre", "at home on a Saturday"]
SCHOOL_NAMES = ["Maya", "Leo", "Tom", "Lily", "Sam", "Zoe", "Omar", "Nina", "Jack", "Emma", "Ali", "Chloé",
                "Ben", "Sara", "Hugo", "Inès", "Noah", "Jade", "Ravi", "Lucie"]
ADULT_SETTINGS = ["at the office", "in a café", "at the train station", "on a video call", "at a hotel",
                  "in a supermarket", "at the gym", "at a family dinner"]
ADULT_NAMES = ["Marc", "Sophie", "Ahmed", "Julia", "Paul", "Elena", "Karim", "Anna", "Luc", "Maria", "Tom",
               "Nadia", "David", "Léa", "Omar", "Clara"]

_MULTI = "NO table, no columns — plain numbered lists."

SPEAKING_FORMATS: Dict[str, dict] = {
    "mimeguess": {
        "adult_ok": False, "young_ok": True, "mid_ok": True,
        "pick": "students mime an action, the partner guesses with a question — ideal for present continuous, actions, can/can't",
        "spec": """SHEET A — SPEAKING: MIME & GUESS CARDS
Ten numbered cards. Each card names ONE action or scene to mime silently (the student never says the words), e.g. "Mime: you are eating a hot soup." The partner guesses by asking a question with this week's target structure — write the sentence starter in brackets on each card — and the mimer answers with a short answer.
At the top, a 2-line "Say it like this" model exchange (one question, one short answer).
All 10 actions must be different; no two cards share a verb. Finish with a one-line scoring rule (1 point for each correct guess).""",
    },
    "infogap": {
        "adult_ok": True, "young_ok": False, "mid_ok": True,
        "pick": "each partner has half the information and asks questions to complete the picture — ideal for questions, present/past facts, descriptions",
        "spec": """SHEET A — SPEAKING: PARTNER INFORMATION GAP
Two labelled halves on the same page: "STUDENT A" and "STUDENT B". Each half is a plain numbered list of 8 short facts about the SAME situation (e.g. what four people are doing, a weekly timetable, four people's plans) where 4 pieces of information are MISSING in each half, shown as ______ . The missing pieces in A are given in B and the other way round.
Students ask each other questions using this week's target structure (write one model question at the top) and write the answers in their gaps, WITHOUT looking at their partner's half.""",
    },
    "findsomeone": {
        "adult_ok": True, "young_ok": True, "mid_ok": True,
        "pick": "a mingling task: students ask the class and write names — ideal for habits, likes, past experiences, plans",
        "spec": """SHEET A — SPEAKING: FIND SOMEONE WHO…
Ten numbered prompts of the form "Find someone who ..." written so that asking the question needs this week's target structure. One model question at the top. Students stand up, ask classmates and write one classmate's name beside each prompt, and can ask a follow-up "Why?" or "What...?".
Leave a blank ______ after each prompt for the name.""",
    },
    "dicegame": {
        "adult_ok": True, "young_ok": True, "mid_ok": True,
        "pick": "roll a die, read the matching prompt, answer in a full sentence — ideal for revision of several facets",
        "spec": """SHEET A — SPEAKING: DICE & QUESTION GAME
Six categories numbered 1 to 6 (the number on the die). Each category has 3 short prompts, 18 in all, and each category practises a DIFFERENT facet of this week's target language. A student rolls the die (or picks a number 1-6), reads one prompt from that category to their partner, and the partner answers in a full sentence. A correct use of the target structure earns 1 point.""",
    },
    "roleplay": {
        "adult_ok": True, "young_ok": False, "mid_ok": True,
        "pick": "two short realistic conversations with role cards — ideal for questions, polite requests, past events, plans",
        "spec": """SHEET A — SPEAKING: ROLE-PLAY CARDS
Two situations. For each: "Role A" and "Role B" cards, each with the situation in 2 short lines and 4 things to ask or say, plus 3 useful phrases. Students swap roles for the second situation. Situations must use this week's target structure naturally.""",
    },
}


def _is_adult(level: dict) -> bool:
    return level.get("cycle") in ("Adultes", "Business")


def allowed_speaking_formats(level: dict) -> List[str]:
    adult = _is_adult(level)
    young = level.get("band", 2) <= 1
    out = []
    for key, f in SPEAKING_FORMATS.items():
        ok = f["adult_ok"] if adult else (f["young_ok"] if young else f["mid_ok"])
        if ok:
            out.append(key)
    return out


def speaking_format_spec(plan: Optional[dict], student_count: int) -> Optional[str]:
    """Spec text for Sheet A in the format the plan chose, or None (caller
    falls back to the classic 10-prompt discussion sheet)."""
    fmt = SPEAKING_FORMATS.get((plan or {}).get("speaking_format"))
    if not fmt:
        return None
    small = (
        f"\nThis is a small class of {student_count} students — design it for pairs or a small group."
        if student_count <= 6 else ""
    )
    return (
        f"{fmt['spec']}{small}\nBase it on this week's topic.\n"
        "After a dashed line add a short \"TEACHER NOTES\" section (3-5 lines: how to run it, timing). "
        "No answer key — it's communicative.\n" + _MULTI
    )


def fallback_sheet_plan(ids: List[str], level: dict, curriculum: dict, week: int) -> dict:
    adult = _is_adult(level)
    settings = ADULT_SETTINGS if adult else SCHOOL_SETTINGS
    names = ADULT_NAMES if adult else SCHOOL_NAMES
    vocab = curriculum.get("vocab") or ""
    words = [w.strip() for w in vocab.split(",") if w.strip()]
    size = max(3, -(-len(words) * 6 // 10))  # ceil(0.6 * n)
    formats = allowed_speaking_formats(level)
    plan = {"speaking_format": formats[week % len(formats)], "sheets": {}}
    grammar = curriculum.get("grammar")
    for i, sid in enumerate(ids):
        slice_ = [words[(i * 2 + k) % len(words)] for k in range(min(size, len(words)))] if words else []
        base = (week * 3 + i * 2) % len(names)
        plan["sheets"][sid] = {
            "facet": (f"the week's grammar target ({grammar}) — a different part of it from the other sheets"
                      if grammar else "this week's language"),
            "setting": settings[(week + i) % len(settings)],
            "characters": [names[base], names[(base + 1) % len(names)]],
            "vocab": slice_,
        }
    return plan


def build_sheet_plan_prompt(ids: List[str], level: dict, common_context: str, script_excerpt: str) -> str:
    formats = allowed_speaking_formats(level)
    jobs = "\n".join(f"{sid}: {SHEET_LABELS.get(sid, sid)} — {SHEET_ROLES.get(sid, '')}" for sid in ids)
    format_text = ""
    if "A" in ids:
        options = "; ".join(f"{k} ({SPEAKING_FORMATS[k]['pick']})" for k in formats)
        format_text = f"\n- \"speakingFormat\": pick the ONE that best practises this week's grammar from: {options}."
    return f"""You are planning a pack of {len(ids)} practice sheets for ONE lesson so that the sheets feel genuinely DIFFERENT from each other — different job, different scenario, different characters — instead of {len(ids)} copies of the same drill.

LESSON CONTEXT
--------------
{common_context}

Teacher's script excerpt:
{script_excerpt}

SHEETS TO PLAN (id: sheet — its job)
{jobs}

Return ONLY valid JSON (no markdown fences, no commentary) in exactly this shape:
{{"speakingFormat":"<format id or empty>","sheets":{{"<id>":{{"facet":"...","setting":"...","characters":["Name1","Name2"],"vocab":["word","word"]}}}}}}

RULES
- Split the week's grammar target into 3-5 facets (for example statements, questions, negatives, short answers, contrast) and give each sheet 1-2 of them. Different sheets get different facets or combinations, and every facet is practised by at least two sheets.
- Every sheet gets a DIFFERENT everyday setting and DIFFERENT characters: exactly 2 first names each, no name used by two sheets, and none of {", ".join(SCHOOL_NAMES[:4])} unless nothing else fits.
- Every sheet gets 4-6 of the lesson's vocabulary words as its main words. Different sheets get different subsets; every lesson word appears on at least two sheets; no sheet uses them all. Only use words from the lesson vocabulary.
- Stay strictly within the grammar limits and vocabulary cap of this level.{format_text}
- Keep every value short (a few words)."""


def parse_sheet_plan(raw: str, ids: List[str], fallback: dict, level: dict) -> dict:
    """Merge the model's JSON over the fallback plan field by field; anything
    missing or malformed keeps the fallback value. Never raises."""
    try:
        start, end = raw.index("{"), raw.rindex("}")
        parsed = json.loads(raw[start:end + 1])
        if not isinstance(parsed, dict):
            return fallback
    except (ValueError, TypeError):
        return fallback
    formats = allowed_speaking_formats(level)
    chosen = parsed.get("speakingFormat")
    plan = {"speaking_format": chosen if chosen in formats else fallback["speaking_format"], "sheets": {}}
    raw_sheets = parsed.get("sheets") if isinstance(parsed.get("sheets"), dict) else {}
    for sid in ids:
        p = raw_sheets.get(sid) if isinstance(raw_sheets.get(sid), dict) else {}
        f = fallback["sheets"][sid]
        chars = p.get("characters")
        vocab = p.get("vocab")
        plan["sheets"][sid] = {
            "facet": p["facet"].strip() if isinstance(p.get("facet"), str) and p["facet"].strip() else f["facet"],
            "setting": p["setting"].strip() if isinstance(p.get("setting"), str) and p["setting"].strip() else f["setting"],
            "characters": [str(c) for c in chars[:3]] if isinstance(chars, list) and chars else f["characters"],
            "vocab": [str(v) for v in vocab[:8]] if isinstance(vocab, list) and vocab else f["vocab"],
        }
    return plan


def sheet_plan_block(plan: Optional[dict], sid: str) -> str:
    if not plan or sid not in plan.get("sheets", {}):
        return ""
    mine = plan["sheets"][sid]
    others = "\n".join(
        f"- {SHEET_LABELS.get(k, k)}: {v['setting']} ({' & '.join(v['characters'])})"
        for k, v in plan["sheets"].items() if k != sid
    )
    words = ", ".join(mine["vocab"]) if mine["vocab"] else "the lesson vocabulary"
    return f"""

SHEET PLAN — MANDATORY. This pack has {len(plan['sheets'])} sheets and each one has a DIFFERENT job, so students never meet the same page twice.
YOUR JOB: {SHEET_ROLES.get(sid, '')}
Language facet to practise: {mine['facet']}
Setting for every item: {mine['setting']} — use no other scenario
Characters: {', '.join(mine['characters'])} — use only these names
Main words for this sheet: {words} (use other lesson words only sparingly)
The OTHER sheets already use these settings and characters — do NOT reuse them:
{others or '(none)'}
Do not build every item on the same sentence frame — vary the structures inside your facet."""
