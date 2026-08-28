"""
AI prompt-building logic — ported from the validated lesson-planner engine
(`index.html` lines 1436-1731 and 2122-2251 as of 2026-08-14): stageTimings,
buildScriptPrompt, sheetsCommonContext, sheetSpec, buildSingleSheetPrompt,
exerciseTypeSpec, buildExerciseTypeSheetPrompt, buildExtensionPrompt,
splitSheetContent, stripLeadingMd.

One adaptation from the source engine: the engine picks a single fixed
"Keep Talking" activity per class from its own 65-row ACTIVITIES table
(`state.activityId`). THE TEACHKIT's existing product model has no
equivalent single-activity picker — it captures a teacher's preferred
`activity_types` (Games/Pair work/Songs/etc.) at onboarding instead. Rather
than porting the whole ACTIVITIES table (a separate warm-up-library concern
from the curriculum/prompt-quality porting this module is about),
`build_script_prompt` takes `activity_types: List[str]` and asks the model
to choose a suitable activity from that list for the production stage.
Everything else here is a faithful, same-intent port — the prose-not-
dialogue style rules, the Form+Function grammar instruction, and the
6-word vocab cap with pronunciation are carried over verbatim.
"""
import re
from typing import List, Optional, Tuple


def stage_timings(total_minutes: int) -> dict:
    def round5(n: float) -> int:
        return max(5, round(n / 5) * 5)

    return {
        "warmup": round5(total_minutes * 0.15),
        "presentation": round5(total_minutes * 0.20),
        "practice": round5(total_minutes * 0.30),
        "production": round5(total_minutes * 0.25),
        "wrapup": round5(total_minutes * 0.10),
    }


def build_script_prompt(
    level: dict,
    week: int,
    curriculum: dict,
    skills: List[str],
    duration: int,
    student_count: int,
    activity_types: List[str],
    extension_activity: bool = True,
) -> str:
    t = stage_timings(duration)
    is_adult_track = level["cycle"] in ("Adultes", "Business")
    audience_note = (
        'This is an adult learner (a working professional) — no mime, no TPR, no "stand up" or '
        "physical gesture instructions anywhere. Verbal and conversational techniques only."
        if is_adult_track
        else "Gesture/TPR is fine where it helps young learners, especially for younger levels."
    )
    max_words = 6

    grammar_line = f"\nGrammar target: {curriculum['grammar']}" if curriculum.get("grammar") else ""
    vocab_line = f"\nVocabulary focus: {curriculum['vocab']}" if curriculum.get("vocab") else ""
    extension_line = (
        " Include one line in the controlled-practice stage on what fast finishers (stronger students) should do next."
        if extension_activity
        else ""
    )
    activity_types_str = ", ".join(activity_types) if activity_types else "Games, Pair work, Group work, Songs, Role-play"

    return f"""You are an experienced EFL teacher writing your OWN lesson plan for a class you are about to teach — the kind of practical, no-nonsense document a real teacher writes for themselves, not a formal training script.

STYLE — the most important instruction. Write like a real teacher's own lesson notes:
- NO "Teacher: ... / Students: ..." turn-by-turn dialogue transcript
- Describe what to do in plain instructions; put the exact words to say in quotes only where the
  wording genuinely matters (e.g. Say: "What's this? It's a dog." Class repeats 3 times.)
- Short, practical, scannable — bullet points and short lines, not essays
- No tables, no boxes
- Total length: about 1 page for school levels, up to 1.5 pages for adults — trim detail, never
  trim the content a teacher actually needs mid-class

LESSON CONTEXT
--------------
Level: {level['label']} · CEFR: {level['cefr']} · {level['cycle']} · Ages: {level['ages']}
Duration: {duration} min · Week {week} of 32 · {curriculum['block']} ({curriculum['date_range']})
Class size: {student_count} students · Skills: {', '.join(skills)}
Preferred activity types for the production stage: {activity_types_str} — choose one that fits this week's topic.
{audience_note}

THIS WEEK'S CURRICULUM (mandatory — teach this, not a different topic)
--------------------------------------------------------------------------
Topic: {curriculum['theme']}{grammar_line}{vocab_line}

WRITE THE LESSON PLAN WITH THESE SECTIONS, IN THIS ORDER (use a markdown heading, e.g. "## Grammar point", for each one so they're visually distinct)
------------------------------------------------------------------------------------------------------------------------------------------------------
1. Title — the curriculum topic above, not the activity name
2. Lesson aim — 2-3 short bullet points: what students will be able to do by the end
3. Grammar point — for each form: the FORM (how it's built) and the FUNCTION (what it's used for/what it
   means), 2-5 short lines total (e.g. "should + base verb — Form: modal + verb, no 'to'. Function: giving advice
   or saying what's the right thing to do.")
4. Key vocabulary — max {max_words} words/phrases for the whole class. For EACH one give, on its own line:
   the word, its part of speech (noun/verb/adjective/adverb/phrase etc.), a simple pronunciation guide in
   slashes (e.g. /bʊk/ — plain respelling is fine, not full IPA, if that's clearer for a French speaker), and
   a short simple-English meaning. Format: word (part of speech) /pronunciation/ — meaning. One line per word,
   no table.
5. Lesson stages — 5 short numbered stages covering the full {duration} minutes: warm-up ({t['warmup']} min),
   presentation ({t['presentation']} min), controlled practice ({t['practice']} min, this is where the printed
   activity sheet(s) get used — mention it, don't re-describe the sheet), free production ({t['production']} min,
   using an activity type from the list above; one line on group sizing for {student_count} students), wrap-up ({t['wrapup']} min,
   consolidation + homework if appropriate for this level). For each stage: a few short lines of what to do,
   mixing plain instructions with the odd exact quote where wording matters.{extension_line}
6. Common mistakes to watch for — 3-5 short lines, typical errors for a {level['cefr']} French speaker at this point,
   each with the correction (e.g. "You should to sleep. → You should sleep.")
7. Teacher reminders — 2-4 short bullet points of practical advice (e.g. "Keep instructions short.",
   "Correct fast and recycle the correction.", "Don't let writing replace speaking.")

Do not write an "objectives essay", a vocabulary table, a curriculum-alignment appendix, a lesson-summary
table, or a formal Teacher:/Students: transcript. Grammar and vocabulary must be strictly {level['cefr']}-appropriate
and must match the curriculum above — do not overestimate or underestimate the level."""


# Sheets are generated as separate, small, parallel API calls (one per sheet
# type) rather than one big combined call — mirrors the source engine's
# reasoning: a single combined call asking for 3-4 full sheets is slow and
# more likely to hit a timeout, so callers should fire these concurrently
# (e.g. via asyncio.gather) rather than sequentially.

def sheets_common_context(level: dict, curriculum: dict, student_count: int, activity_types: List[str]) -> str:
    activity_types_str = ", ".join(activity_types) if activity_types else "Games, Pair work, Group work"
    grammar_part = f" · Grammar: {curriculum['grammar']}" if curriculum.get("grammar") else ""
    vocab_part = f" · Vocabulary: {curriculum['vocab']}" if curriculum.get("vocab") else ""
    return f"""Level: {level['label']} · CEFR: {level['cefr']} · Ages: {level['ages']}
Class size: {student_count} students
Preferred activity types: {activity_types_str}
Curriculum topic: {curriculum['theme']}{grammar_part}{vocab_part}"""


def sheet_spec(letter: str, level: dict, student_count: int) -> str:
    small_class = student_count <= 6
    if letter == "A":
        pair_note = (
            f", for a small class of {student_count} students (pair or small-group discussion — the same partner throughout, or swap once or twice)"
            if small_class
            else ""
        )
        return f"""SHEET A — SPEAKING
A plain numbered list of exactly 10 discussion prompts/questions based on this week's topic{pair_note}.
NO table, no columns, no grid — just a numbered list.
A worked example for item 1 is optional — only include one if it genuinely helps
clarify the task; otherwise just start with item 1 as a normal blank item.
No answer key — it's communicative."""
    if letter == "B":
        return """SHEET B — LISTENING TASK
A plain numbered list, exactly 10 questions — tick the correct answer OR fill in the
missing word. NO table, no columns. If you split this into more than one part/format
(e.g. Part A true/false, Part B gap-fill), each part still needs its own full 10 items —
do not divide 10 items between parts; every part gets 10.
A worked example for item 1 is optional — only include one if it genuinely helps
clarify the task.
Must be completable from what the teacher will say during the lesson. This sheet must be
self-contained — the teacher should not need to flip back to the full lesson script to
run it. In the teacher notes section, include a clearly labelled "TEACHER'S LISTENING
SCRIPT": the exact sentences to read aloud, in question order, word-for-word, plus a
one-line instruction on pacing (e.g. read each sentence twice, at natural but slightly
slow speed, pause between sentences)."""
    if letter == "C":
        max_words = 80 if level["band"] <= 1 else (120 if level["band"] <= 3 else 180)
        return f"""SHEET C — READING + COMPREHENSION
A short graded text (max {max_words} words), then a plain numbered list of exactly 10
comprehension questions. NO table, no columns. At least one question requiring a
full sentence answer. A worked example for question 1 is optional."""
    return """SHEET D — WRITING TASK
A plain numbered list of exactly 10 gap-fill or sentence-correction items (or, for guided
writing, a template with sentence starters). NO table, no columns.
A worked example for item 1 is optional — only include one if it genuinely helps
clarify the task."""


def _adult_note(level: dict) -> str:
    is_adult_track = level["cycle"] in ("Adultes", "Business")
    return (
        '\nThis is an adult learner, not a child — no mime, no TPR, no "stand up" or physical gesture instructions anywhere on this sheet.\n'
        if is_adult_track
        else ""
    )


def build_single_sheet_prompt(
    letter: str, level: dict, curriculum: dict, student_count: int, activity_types: List[str], script_excerpt: str
) -> str:
    return f"""You are an expert EFL materials writer for French schools. Generate ONE printable student activity sheet.

LESSON CONTEXT
--------------
{sheets_common_context(level, curriculum, student_count, activity_types)}

Teacher's script excerpt (for context):
{script_excerpt}

TASK
----
{sheet_spec(letter, level, student_count)}
{_adult_note(level)}
FORMAT RULES:
- Start with: Name: ___________ Date: ___________
- Include a clear title
- One short plain instruction line per exercise (e.g. "Complete with the correct
  tense.") — not a separate boxed "Instructions:" section
- NO markdown tables anywhere (no | pipe syntax, no columns/grids) — even for a
  matching exercise, use a plain numbered list instead (e.g. "1. set up a business
  — write the letter of the definition that matches: ___")
- A worked example is optional, not required — only include one where it genuinely
  clarifies the task; don't force one onto every exercise
- Each exercise/section on this sheet needs a full 10 items of its own. If the sheet
  has only one exercise, that's 10 items total. If it's split into multiple named
  parts or formats, every part gets its own 10 — never divide one shared count of 10
  across several parts
- Instructions in simple English appropriate for {level['cefr']} level
- Write every blank as plain underscores, e.g. ______________ — do NOT escape
  underscores with a backslash and do not use any markdown escape characters
  (no \\_, \\*, \\[, \\] etc.)
- Keep formatting plain: minimal markdown, no unnecessary column headers or labels
  ("your answer", "teacher writes" etc.) — the student already knows it's their own sheet
- Everything above this point is STUDENT-FACING — do not put any teacher-only text,
  setup instructions, or notes anywhere in it
- After a dashed line at the very end, add a staff-only section — labelled
  "ANSWER KEY — Do not distribute" if there are correct answers, otherwise just
  "TEACHER NOTES" for a speaking sheet — ending with a short note on exactly how
  to run this sheet in class (what to say, timing, pacing). This section will be
  stripped out before the sheet is given to students, so put ALL teacher-facing
  content here and nowhere else
- Output ONLY this one sheet's content — no other commentary, no ===SHEET X=== markers"""


# Each checked "Worksheet exercise type" box gets its own full standalone
# page — a grammar/vocab practice sheet in that specific format, independent
# of whichever skill sheets (A-D) also exist.
def exercise_type_spec(key: str) -> str:
    specs = {
        "gapfill": """GAP FILL PRACTICE
A plain numbered list of exactly 10 gap-fill sentences using this week's grammar/vocabulary
target. One blank per sentence, plain underscores (e.g. ______________). NO table, no columns.""",
        "matching": """MATCHING PRACTICE
A plain numbered list of exactly 10 items to match — NOT a table. For each numbered item give
the word/phrase and a blank for the matching letter (e.g. "1. set up a business — write the
letter of the definition that matches: ___"), then a lettered list of the 10 definitions/
translations/pairs below the numbered items.""",
        "spotmistake": """SPOT THE MISTAKE
A plain numbered list of exactly 10 sentences, each containing one grammar or vocabulary
mistake tied to this week's target. Leave a blank line under each sentence for the student to
write the corrected version.""",
        "multiplechoice": """MULTIPLE CHOICE PRACTICE
A plain numbered list of exactly 10 multiple-choice questions testing this week's grammar/
vocabulary target. EVERY single item, with no exceptions, must have exactly 3 lettered options
(a/b/c) directly under it. Do not let any item become a plain fill-in-the-blank with no options
— if a question is about a blank in a sentence, still give it 3 lettered answer choices for that
blank, the same as every other item on this sheet.""",
        "truefalse": """TRUE OR FALSE PRACTICE
A plain numbered list of exactly 10 true/false statements about this week's grammar/
vocabulary/topic. Students circle True or False for each.""",
        "wordorder": """WORD ORDER PRACTICE
A plain numbered list of exactly 10 items, each a scrambled/jumbled sentence (words given out
of order) built from this week's grammar target, for students to reorder into a correct
sentence on the line below.""",
        "guidedwriting": """GUIDED WRITING PRACTICE
A plain numbered list of exactly 10 sentence starters or prompts (e.g. "I usually... / My
company..."), each requiring the student to complete it in writing using this week's grammar/
vocabulary target.""",
        "pictureqa": """PICTURE-BASED QUESTIONS
A plain numbered list of exactly 10 questions built around a scene the teacher will show or
describe. Start with one line briefly describing the scene/image (for the teacher to sketch on
the board, project, or describe aloud), then the 10 questions about it using this week's
grammar/vocabulary target.""",
    }
    return specs.get(key, "")


def build_exercise_type_sheet_prompt(
    key: str, level: dict, curriculum: dict, student_count: int, activity_types: List[str], script_excerpt: str
) -> str:
    return f"""You are an expert EFL materials writer for French schools. Generate ONE printable student activity sheet — a standalone grammar/vocabulary practice page in the exact format the teacher requested below.

LESSON CONTEXT
--------------
{sheets_common_context(level, curriculum, student_count, activity_types)}

Teacher's script excerpt (for context):
{script_excerpt}

TASK
----
{exercise_type_spec(key)}
{_adult_note(level)}
FORMAT RULES:
- Start with: Name: ___________ Date: ___________
- Include a clear title
- One short plain instruction line at the top (e.g. "Complete with the correct tense.")
- NO markdown tables anywhere (no | pipe syntax, no columns/grids) — use a plain numbered list
- Exactly 10 items — not fewer, not more
- A worked example for item 1 is optional — only include one where it genuinely clarifies the task
- Instructions in simple English appropriate for {level['cefr']} level
- Write every blank as plain underscores, e.g. ______________ — do NOT escape underscores with
  a backslash and do not use any markdown escape characters (no \\_, \\*, \\[, \\] etc.)
- Everything above this point is STUDENT-FACING — do not put any teacher-only text, setup
  instructions, or notes anywhere in it
- After a dashed line at the very end, add a staff-only section labelled "ANSWER KEY — Do not
  distribute" with the correct answers. This section will be stripped out before the sheet is
  given to students, so put ALL teacher-facing content here and nowhere else
- Output ONLY this one sheet's content — no other commentary, no ===SHEET X=== markers"""


def build_extension_prompt(level: dict, curriculum: dict, student_count: int, activity_types: List[str], script_excerpt: str) -> str:
    return f"""You are an expert EFL materials writer for French schools. Write ONE short extension task for students who finish the main activity early (fast finishers / stronger students).

LESSON CONTEXT
--------------
{sheets_common_context(level, curriculum, student_count, activity_types)}

Teacher's script excerpt (for context):
{script_excerpt}

TASK
----
Write 2-4 lines: a slightly harder stretch task using the same grammar and vocabulary as
this lesson (e.g. one extra sentence to write, a follow-up question for a partner, or a
small bonus challenge). Start with the line "⭐ For early finishers:". If it has a single
correct answer, add one line for the answer at the end — otherwise leave it open, like a
speaking task. No Name/Date header, no title, plain underscores for any blanks, no markdown
escaping. Output ONLY these few lines, nothing else."""


def strip_leading_md(line: str) -> str:
    line = re.sub(r"^#{1,6}\s*", "", line)
    line = re.sub(r"^>\s?", "", line)
    line = re.sub(r"^[-*]\s+(?=\S)", "", line)
    return line.strip()


_ANSWER_KEY_RE = re.compile(r"answer\s*key|teacher\s*notes", re.IGNORECASE)


def split_sheet_content(content: str) -> Tuple[List[str], List[str]]:
    """Regex-based boundary split enforcing the zero-repetition rule between
    student-facing sheet content and staff-only answer-key/teacher-notes
    content within a single AI response. Same boundary marker as the
    source engine: the first line matching /answer\\s*key|teacher\\s*notes/i
    (after stripping markdown and ** bold markers)."""
    lines = [line.strip() for line in re.split(r"\r?\n", content)]
    key_idx = -1
    for i, line in enumerate(lines):
        clean = strip_leading_md(line).replace("**", "").strip()
        if _ANSWER_KEY_RE.search(clean):
            key_idx = i
            break
    if key_idx == -1:
        return lines, []
    return lines[:key_idx], lines[key_idx:]


def strip_leading_name_date_line(lines: List[str]) -> List[str]:
    """Each sheet's own generated content leads with its own "Name: ___
    Date: ___" line — repetitive when several sheets are combined into one
    document that shows it once at the top instead. Strips that leading
    line if present."""
    idx = next((i for i, line in enumerate(lines) if len(line) > 0), -1)
    if idx != -1 and re.match(r"^name\s*:.*date\s*:", lines[idx], re.IGNORECASE):
        return lines[:idx] + lines[idx + 1:]
    return lines
