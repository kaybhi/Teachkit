from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
import re
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
import uuid
import bcrypt
import jwt as pyjwt
from datetime import datetime, timezone, timedelta

from curriculum import generate_full_syllabus, _vocab_string_to_list
from curriculum_data import LEVELS_BY_ID, LEVELS_BY_CLASS_TYPE, EXERCISE_TYPES, SPECIAL_TOPICS
from curriculum_lookup import get_curriculum_for_week, get_week_info
import docx_builder as docx
from prompt_builders import (
    build_script_prompt,
    build_single_sheet_prompt,
    build_exercise_type_sheet_prompt,
    build_extension_prompt,
    split_sheet_content,
)
from anthropic_client import generate as ai_generate, AnthropicGenerationError
from holidays import get_holidays_for_year, compute_current_school_week

import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
mongo_url = os.environ['MONGO_URL']
# tlsCAFile pinned to certifi's bundle rather than the OS default — python:3.11-slim's
# system CA store causes a TLSV1_ALERT_INTERNAL_ERROR handshake failure against Atlas.
client = AsyncIOMotorClient(mongo_url, tlsCAFile=certifi.where())
db = client[os.environ['DB_NAME']]

# App
app = FastAPI(title="THE TEACHKIT API")
api_router = APIRouter(prefix="/api")

# Auth config
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXP_DAYS = 30

# ---------- Models ----------
class SignupInput(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    full_name: Optional[str] = None
    school_name: Optional[str] = None
    school_city: Optional[str] = None
    class_level: Optional[str] = None  # e.g. CM2, 6ème — display label, kept for backward-compat
    class_type: Optional[str] = None  # school | adult | business
    level_id: Optional[str] = None  # e.g. cm2, adult-b1, biz-b1
    school_year_start: Optional[str] = None  # ISO date
    priorities: Optional[List[str]] = None  # ranked skills
    activity_types: Optional[List[str]] = None
    holiday_zone: Optional[str] = None  # A | B | C | none
    family_emails: Optional[List[str]] = None  # emails of families for homework send
    student_count: Optional[int] = None  # class size, used to tailor sheet generation
    duration: Optional[int] = None  # lesson length in minutes, used for stage timings

class GenerateSyllabusInput(BaseModel):
    class_type: str = "school"  # school | adult | business
    level_id: str = "cm2"  # e.g. cm1/cm2/6e (school), adult-b1, biz-b1
    priorities: List[str] = Field(default_factory=lambda: ["Speaking", "Listening", "Reading", "Writing"])
    activity_types: List[str] = Field(default_factory=lambda: ["Games", "Pair work", "Group work", "Songs", "Role-play"])

class LessonUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    title: Optional[str] = None
    theme: Optional[str] = None
    grammar: Optional[str] = None
    vocabulary: Optional[List[str]] = None
    objectives: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    ppp: Optional[dict] = None
    notes: Optional[str] = None

class SpecialTopicInput(BaseModel):
    special_topic_key: Optional[str] = None  # null/omitted clears the override


class ActivitySwapInput(BaseModel):
    phase: str  # presentation | practice | production
    index: int  # activity index within phase
    new_activity: dict  # {title, description, type, skill}

class AIActivityRequest(BaseModel):
    week_theme: str
    grammar: str
    vocabulary: List[str]
    phase: str  # presentation | practice | production
    skill_focus: str
    current_activity_title: Optional[str] = ""


class EnrichWeekRequest(BaseModel):
    exercise_types: List[str] = Field(default_factory=list)  # e.g. ["gapfill", "multiplechoice"]


# ---------- Helpers ----------
def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def verify_password(p: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(p.encode(), hashed.encode())
    except Exception:
        return False

def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXP_DAYS),
        "iat": datetime.now(timezone.utc),
    }
    return pyjwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload["sub"]
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Simple in-memory per-user rate limit on AI-generation endpoints (enrich,
# homework, suggest-activity, chat, batch-enrich) — now that signups are
# open, this guards against one account running up real Anthropic API
# costs. In-memory only: fine for a single-process deployment; a
# multi-instance deployment would need this backed by Mongo/Redis instead.
_AI_RATE_LIMIT_WINDOW_SECONDS = 3600
_AI_RATE_LIMIT_MAX_CALLS = 30
_ai_call_log: dict = {}  # user_id -> list of monotonic call timestamps


def _check_ai_rate_limit(user_id: str):
    import time
    now = time.monotonic()
    cutoff = now - _AI_RATE_LIMIT_WINDOW_SECONDS
    timestamps = _ai_call_log.setdefault(user_id, [])
    while timestamps and timestamps[0] < cutoff:
        timestamps.pop(0)
    if len(timestamps) >= _AI_RATE_LIMIT_MAX_CALLS:
        raise HTTPException(
            status_code=429,
            detail=f"You've hit the AI-generation limit ({_AI_RATE_LIMIT_MAX_CALLS} per hour). Please try again later.",
        )
    timestamps.append(now)


# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"message": "THE TEACHKIT API is running", "version": "1.0.0"}


@api_router.post("/auth/signup")
async def signup(data: SignupInput):
    existing = await db.users.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": data.email.lower(),
        "full_name": data.full_name,
        "password_hash": hash_password(data.password),
        "school_name": "",
        "school_city": "",
        "class_level": "",
        "school_year_start": "",
        "priorities": ["Speaking", "Listening", "Reading", "Writing"],
        "activity_types": ["Games", "Pair work", "Group work", "Songs", "Role-play"],
        "holiday_zone": "none",
        "family_emails": [],
        "onboarded": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.users.insert_one(user_doc)
    token = create_token(user_id)
    user_doc.pop("password_hash", None)
    user_doc.pop("_id", None)
    return {"token": token, "user": user_doc}


@api_router.post("/auth/login")
async def login(data: LoginInput):
    user = await db.users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(user["id"])
    user.pop("password_hash", None)
    user.pop("_id", None)
    return {"token": token, "user": user}


@api_router.get("/auth/me")
async def me(current=Depends(get_current_user)):
    return current


@api_router.put("/profile")
async def update_profile(data: ProfileUpdate, current=Depends(get_current_user)):
    update_fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if update_fields:
        # Mark onboarded if school fields are provided
        if any(k in update_fields for k in ["school_name", "class_level"]):
            update_fields["onboarded"] = True
        await db.users.update_one({"id": current["id"]}, {"$set": update_fields})
    user = await db.users.find_one({"id": current["id"]}, {"_id": 0, "password_hash": 0})
    return user


# ---------- Syllabus ----------
@api_router.post("/syllabus/generate")
async def generate_syllabus(data: GenerateSyllabusInput, current=Depends(get_current_user)):
    if data.class_type not in LEVELS_BY_CLASS_TYPE:
        raise HTTPException(status_code=400, detail=f"Unknown class_type: {data.class_type}")
    if data.level_id not in LEVELS_BY_ID:
        raise HTTPException(status_code=400, detail=f"Unknown level_id: {data.level_id}")
    lessons = generate_full_syllabus(data.class_type, data.level_id, data.priorities, data.activity_types)
    syllabus_id = str(uuid.uuid4())
    level = LEVELS_BY_ID[data.level_id]
    doc = {
        "id": syllabus_id,
        "user_id": current["id"],
        "priorities": data.priorities,
        "activity_types": data.activity_types,
        "class_type": data.class_type,
        "level_id": data.level_id,
        "class_level": level["label"],  # kept for backward-compat display use
        "lessons": lessons,
        "share_token": str(uuid.uuid4()).replace("-", "")[:20],
        "share_enabled": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    # Deactivate previous and set new active
    await db.syllabi.update_many({"user_id": current["id"]}, {"$set": {"active": False}})
    doc["active"] = True
    await db.syllabi.insert_one(doc)
    # Update user with priorities/activity_types/class selection
    await db.users.update_one(
        {"id": current["id"]},
        {"$set": {
            "priorities": data.priorities,
            "activity_types": data.activity_types,
            "class_type": data.class_type,
            "level_id": data.level_id,
            "class_level": level["label"],
            "onboarded": True,
        }},
    )
    doc.pop("_id", None)
    return doc


@api_router.get("/syllabus/active")
async def get_active_syllabus(current=Depends(get_current_user)):
    doc = await db.syllabi.find_one({"user_id": current["id"], "active": True}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="No active syllabus. Generate one first.")
    return doc


@api_router.get("/syllabus/{syllabus_id}/week/{week_num}")
async def get_lesson(syllabus_id: str, week_num: int, current=Depends(get_current_user)):
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson = next((l for l in doc["lessons"] if l["week"] == week_num), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Week not found")
    return lesson


@api_router.put("/syllabus/{syllabus_id}/week/{week_num}")
async def update_lesson(syllabus_id: str, week_num: int, data: LessonUpdate, current=Depends(get_current_user)):
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    for i, l in enumerate(doc["lessons"]):
        if l["week"] == week_num:
            doc["lessons"][i] = {**l, **updates}
            break
    else:
        raise HTTPException(status_code=404, detail="Week not found")
    await db.syllabi.update_one(
        {"id": syllabus_id, "user_id": current["id"]},
        {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
    )
    return doc["lessons"][[i for i, l in enumerate(doc["lessons"]) if l["week"] == week_num][0]]


@api_router.post("/syllabus/{syllabus_id}/week/{week_num}/swap-activity")
async def swap_activity(syllabus_id: str, week_num: int, data: ActivitySwapInput, current=Depends(get_current_user)):
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson_idx = None
    for i, l in enumerate(doc["lessons"]):
        if l["week"] == week_num:
            lesson_idx = i
            break
    if lesson_idx is None:
        raise HTTPException(status_code=404, detail="Week not found")
    phase = data.phase.lower()
    if phase not in ("presentation", "practice", "production"):
        raise HTTPException(status_code=400, detail="Invalid phase")
    activities = doc["lessons"][lesson_idx]["ppp"][phase]["activities"]
    if data.index < 0 or data.index >= len(activities):
        raise HTTPException(status_code=400, detail="Activity index out of range")
    activities[data.index] = data.new_activity
    doc["lessons"][lesson_idx]["ppp"][phase]["activities"] = activities
    await db.syllabi.update_one(
        {"id": syllabus_id, "user_id": current["id"]},
        {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
    )
    return doc["lessons"][lesson_idx]


_VALID_SPECIAL_TOPICS = {t["key"] for t in SPECIAL_TOPICS}


@api_router.post("/syllabus/{syllabus_id}/week/{week_num}/special-topic")
async def set_special_topic(syllabus_id: str, week_num: int, data: SpecialTopicInput, current=Depends(get_current_user)):
    """Set or clear a one-off grammar-focus override for this lesson
    (revision sessions, or a class that just needs one topic drilled),
    overriding the normal weekly curriculum lookup — mirrors the source
    engine's "Special topic" dropdown + warning banner + one-click clear."""
    if data.special_topic_key and data.special_topic_key not in _VALID_SPECIAL_TOPICS:
        raise HTTPException(status_code=400, detail=f"Unknown special_topic_key: {data.special_topic_key}")

    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson_idx = next((i for i, l in enumerate(doc["lessons"]) if l["week"] == week_num), None)
    if lesson_idx is None:
        raise HTTPException(status_code=404, detail="Week not found")

    level = LEVELS_BY_ID.get(doc.get("level_id"))
    if not level:
        raise HTTPException(
            status_code=400,
            detail="This syllabus predates class-type support — regenerate it (POST /syllabus/generate) first.",
        )

    c = get_curriculum_for_week(level, week_num, data.special_topic_key)
    lesson = doc["lessons"][lesson_idx]
    lesson["special_topic_key"] = data.special_topic_key
    lesson["theme"] = c["theme"]
    lesson["title"] = c["theme"]
    lesson["grammar"] = c["grammar"] or lesson.get("grammar")
    if c["vocab"]:
        lesson["vocabulary"] = _vocab_string_to_list(c["vocab"])
    doc["lessons"][lesson_idx] = lesson

    await db.syllabi.update_one(
        {"id": syllabus_id, "user_id": current["id"]},
        {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
    )
    return lesson


# ---------- AI activity generator (Claude Sonnet 5) ----------
@api_router.post("/ai/suggest-activity")
async def ai_suggest_activity(data: AIActivityRequest, current=Depends(get_current_user)):
    """Generate a fresh alternative activity via Claude Sonnet 5."""
    _check_ai_rate_limit(current["id"])
    system_msg = (
        "You are an expert English-as-a-Foreign-Language (TEFL) teacher trainer for the "
        "French national curriculum. You design engaging classroom activities using the PPP "
        "framework. Return ONLY valid JSON, no markdown, no prose."
    )
    prompt = f"""Generate ONE alternative classroom activity for a 55-minute lesson.

Week theme: {data.week_theme}
Target grammar: {data.grammar}
Vocabulary: {', '.join(data.vocabulary)}
Lesson phase: {data.phase} (of PPP framework)
Skill to prioritise: {data.skill_focus}
Avoid repeating this current activity: "{data.current_activity_title}"

Return JSON with these exact fields:
{{"title": "short catchy title (max 8 words)",
"description": "one paragraph, 2-3 sentences, concrete instructions for the teacher, mention timing and grouping",
"type": "one of: Games, Pair work, Group work, Songs, Role-play, Whole class, Individual, Video, Digital",
"skill": "one of: Speaking, Listening, Reading, Writing"}}"""

    try:
        response_text = await ai_generate(system_msg, prompt, max_tokens=512)
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in AI response")
        activity = json.loads(match.group(0))
        for k in ("title", "description", "type", "skill"):
            if k not in activity:
                activity[k] = ""
        return activity
    except AnthropicGenerationError as e:
        logger.error(f"AI suggest-activity error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"AI suggest-activity error: {e}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


SCRIPT_SYSTEM_MSG = (
    "You are an expert TEFL teacher and materials writer producing real, classroom-ready lesson "
    "content for French language schools. Follow the formatting and style instructions in the "
    "prompt exactly — they reflect a format already validated with real teachers and students."
)

# 4 skill-sheet letters, ported from the source engine's SHEET A-D concept.
_SHEET_LETTERS = [("A", "Speaking"), ("B", "Listening"), ("C", "Reading"), ("D", "Writing")]


_EXERCISE_TYPE_LABELS = {t["key"]: t["label"] for t in EXERCISE_TYPES}
_VALID_EXERCISE_TYPES = set(_EXERCISE_TYPE_LABELS.keys())


async def _generate_lesson_pack(
    level: dict, week_num: int, curriculum: dict, current: dict, exercise_types: Optional[List[str]] = None
) -> dict:
    """Runs the teacher-script + 4 skill-sheet generations (plus any selected
    exercise-type sheets and the fast-finisher extension) as parallel
    Anthropic calls — mirrors the source engine's reasoning: one big combined
    call is the slowest, most timeout-prone step (see prompt_builders.py's
    module docstring) — and assembles the new pack shape."""
    skills = [s.lower() for s in (current.get("priorities") or ["Speaking", "Listening", "Reading", "Writing"])]
    duration = current.get("duration") or 60
    student_count = current.get("student_count") or 4
    activity_types = current.get("activity_types") or ["Games", "Pair work", "Group work"]
    extension_activity = bool(current.get("extension_activity", True))
    exercise_types = [k for k in (exercise_types or []) if k in _VALID_EXERCISE_TYPES]

    script_prompt = build_script_prompt(
        level, week_num, curriculum, skills, duration, student_count, activity_types, extension_activity=extension_activity
    )

    async def gen_script():
        return await ai_generate(SCRIPT_SYSTEM_MSG, script_prompt, max_tokens=4096)

    async def gen_sheet(letter: str, title: str):
        script_excerpt = curriculum["theme"]  # cheap context; full script isn't generated yet when sheets fire in parallel
        prompt = build_single_sheet_prompt(letter, level, curriculum, student_count, activity_types, script_excerpt)
        content = await ai_generate(SCRIPT_SYSTEM_MSG, prompt, max_tokens=2048)
        main_lines, key_lines = split_sheet_content(content)
        return {
            "letter": letter,
            "title": title,
            "content": content,
            "student_content": "\n".join(main_lines),
            "teacher_notes": "\n".join(key_lines),
        }

    async def gen_exercise_sheet(key: str):
        script_excerpt = curriculum["theme"]
        prompt = build_exercise_type_sheet_prompt(key, level, curriculum, student_count, activity_types, script_excerpt)
        content = await ai_generate(SCRIPT_SYSTEM_MSG, prompt, max_tokens=2048)
        main_lines, key_lines = split_sheet_content(content)
        return {
            "key": key,
            "title": _EXERCISE_TYPE_LABELS.get(key, key),
            "content": content,
            "student_content": "\n".join(main_lines),
            "teacher_notes": "\n".join(key_lines),
        }

    async def gen_extension():
        if not extension_activity:
            return None
        script_excerpt = curriculum["theme"]
        prompt = build_extension_prompt(level, curriculum, student_count, activity_types, script_excerpt)
        return await ai_generate(SCRIPT_SYSTEM_MSG, prompt, max_tokens=512)

    results = await asyncio.gather(
        gen_script(),
        gen_extension(),
        *[gen_sheet(letter, title) for letter, title in _SHEET_LETTERS],
        *[gen_exercise_sheet(key) for key in exercise_types],
    )
    teacher_script, extension = results[0], results[1]
    sheets = results[2:2 + len(_SHEET_LETTERS)]
    exercise_sheets = results[2 + len(_SHEET_LETTERS):]

    return {
        "teacher_script": teacher_script,
        "sheets": sheets,
        "exercise_sheets": exercise_sheets,
        "extension": extension,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------- AI enrichment: produce full teacher script + student handouts ----------
@api_router.post("/syllabus/{syllabus_id}/week/{week_num}/enrich")
async def enrich_week(syllabus_id: str, week_num: int, data: EnrichWeekRequest = EnrichWeekRequest(), current=Depends(get_current_user)):
    """Generate the full lesson pack: a prose teacher's script (Form+Function
    grammar, 6-word vocab cap) plus the 4 skill sheets and any selected
    exercise-type sheets, each split into student-facing vs teacher-only
    content — the validated engine's format, not the old shallow JSON pack
    this replaces."""
    _check_ai_rate_limit(current["id"])
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson = next((l for l in doc["lessons"] if l["week"] == week_num), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Week not found")

    level = LEVELS_BY_ID.get(doc.get("level_id"))
    if not level:
        raise HTTPException(
            status_code=400,
            detail="This syllabus predates class-type support — regenerate it (POST /syllabus/generate) before enriching.",
        )

    try:
        curriculum = get_curriculum_for_week(level, week_num, lesson.get("special_topic_key"))
        pack = await _generate_lesson_pack(level, week_num, curriculum, current, exercise_types=data.exercise_types)

        for i, l in enumerate(doc["lessons"]):
            if l["week"] == week_num:
                doc["lessons"][i]["pack"] = pack
                doc["lessons"][i]["pack_generated_at"] = pack["generated_at"]
                break
        await db.syllabi.update_one(
            {"id": syllabus_id, "user_id": current["id"]},
            {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
        )
        return pack
    except AnthropicGenerationError as e:
        msg = str(e)
        logger.error(f"AI enrich-week error: {msg}")
        if "429" in msg or "rate" in msg.lower() or "overloaded" in msg.lower():
            raise HTTPException(status_code=429, detail="AI is busy handling another request — please retry in ~15 seconds.")
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        logger.error(f"AI enrich-week error: {e}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@api_router.get("/syllabus/{syllabus_id}/week/{week_num}/export/docx")
async def export_docx(syllabus_id: str, week_num: int, doc: str = "script", current=Depends(get_current_user)):
    """Server-side .docx export — the validated engine's exact zero-repetition
    3-document split (Teacher's Script / Activity Sheets / Answer Key), ported
    via docx_builder.py rather than the old client-side jsPDF pipeline."""
    if doc not in ("script", "sheets", "answerkey"):
        raise HTTPException(status_code=400, detail="doc must be one of: script, sheets, answerkey")

    syllabus_doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not syllabus_doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson = next((l for l in syllabus_doc["lessons"] if l["week"] == week_num), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Week not found")
    pack = lesson.get("pack")
    if not pack or not pack.get("teacher_script"):
        raise HTTPException(status_code=400, detail="Generate the teacher pack first (POST .../enrich) before exporting.")

    level = LEVELS_BY_ID.get(syllabus_doc.get("level_id"))
    level_label = level["label"] if level else (syllabus_doc.get("class_level") or "")
    wk = get_week_info(week_num)
    header_xml = docx.docx_header_xml(level_label, week_num, wk["start"], wk["end"])
    all_sheets = list(pack.get("sheets") or []) + list(pack.get("exercise_sheets") or [])

    if doc == "script":
        body = header_xml + docx.docx_page_break() + docx.script_to_docx_xml(pack["teacher_script"])
        title = f"Week {week_num} — Teacher's Script"
        filename_part = "TeacherScript"
    elif doc == "sheets":
        if not all_sheets:
            raise HTTPException(status_code=400, detail="No activity sheets were generated for this week.")
        body = header_xml + docx.docx_p(text="Name: ___________     Date: ___________", after=200)
        for i, s in enumerate(all_sheets):
            if i > 0:
                body += docx.docx_page_break()
            body += docx.sheet_to_docx_xml(s["content"])
        title = f"Week {week_num} — Activity Sheets"
        filename_part = "ActivitySheets"
    else:  # answerkey
        parts = []
        for s in all_sheets:
            letter_or_key = s.get("letter") or s.get("key")
            key_xml = docx.sheet_key_to_docx_xml(s["content"], letter_or_key, s["title"])
            if key_xml:
                parts.append(key_xml)
        if not parts:
            raise HTTPException(status_code=400, detail="No answer-key content found in the generated sheets.")
        body = header_xml + "".join(parts)
        title = f"Week {week_num} — Answer Key"
        filename_part = "AnswerKey"

    package_bytes = docx.build_docx_package(title, body)
    filename = f"TheTeachkit-{level_label.replace(' ', '')}-Week{week_num:02d}-{filename_part}.docx"
    return Response(
        content=package_bytes,
        media_type=DOCX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------- School calendar (holidays-aware) ----------
@api_router.get("/school-week")
async def school_week(current=Depends(get_current_user)):
    zone = current.get("holiday_zone") or "none"
    start = current.get("school_year_start") or ""
    result = compute_current_school_week(start, zone)
    result["holidays"] = get_holidays_for_year(start, zone)
    return result


# ---------- Batch pack generation (background) ----------
_batch_jobs: dict = {}  # {syllabus_id: {status, total, done, current_week, error}}


async def _batch_worker(syllabus_id: str, user_id: str, weeks_to_do: list):
    """Enriches a whole week range in the background, reusing
    _generate_lesson_pack (same pipeline /enrich uses) instead of
    duplicating a second AI-call implementation here."""
    job = _batch_jobs[syllabus_id]

    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": user_id}, {"_id": 0})
    if not doc:
        job["errors"] = job.get("errors", []) + [{"week": None, "error": "Syllabus not found"}]
        job["status"] = "complete"
        return
    level = LEVELS_BY_ID.get(doc.get("level_id"))
    if not level:
        job["errors"] = job.get("errors", []) + [{"week": None, "error": "Syllabus predates class-type support — regenerate it first."}]
        job["status"] = "complete"
        return
    user = await db.users.find_one({"id": user_id}, {"_id": 0})

    for week_num in weeks_to_do:
        try:
            job["current_week"] = week_num
            doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": user_id}, {"_id": 0})
            if not doc:
                job["errors"] = job.get("errors", []) + [{"week": week_num, "error": "Syllabus not found"}]
                break
            lesson = next((l for l in doc["lessons"] if l["week"] == week_num), None)
            if not lesson or lesson.get("pack"):
                job["done"] += 1
                continue

            curriculum = get_curriculum_for_week(level, week_num, lesson.get("special_topic_key"))
            pack = await _generate_lesson_pack(level, week_num, curriculum, user or {})

            for i, l in enumerate(doc["lessons"]):
                if l["week"] == week_num:
                    doc["lessons"][i]["pack"] = pack
                    doc["lessons"][i]["pack_generated_at"] = pack["generated_at"]
                    break
            await db.syllabi.update_one(
                {"id": syllabus_id, "user_id": user_id},
                {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
            )
            job["done"] += 1
            await asyncio.sleep(2)  # avoid rate-limit throttling
        except Exception as e:
            logger.error(f"batch enrich week {week_num} failed: {e}")
            job["errors"] = job.get("errors", []) + [{"week": week_num, "error": str(e)[:200]}]
            await asyncio.sleep(5)

    job["status"] = "complete"
    job["current_week"] = None


@api_router.post("/syllabus/{syllabus_id}/batch-enrich")
async def batch_enrich(syllabus_id: str, current=Depends(get_current_user)):
    # Charged once per batch job here, not per week — the background worker
    # itself isn't behind a request/rate-limit context.
    _check_ai_rate_limit(current["id"])
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    if _batch_jobs.get(syllabus_id, {}).get("status") == "running":
        return {**_batch_jobs[syllabus_id], "status": "already_running"}
    weeks_to_do = [l["week"] for l in doc["lessons"] if not l.get("pack")]
    if not weeks_to_do:
        return {"status": "complete", "done": 32, "total": 32, "message": "All weeks already have packs."}
    _batch_jobs[syllabus_id] = {
        "status": "running",
        "total": len(weeks_to_do),
        "done": 0,
        "current_week": None,
        "errors": [],
    }
    asyncio.create_task(_batch_worker(syllabus_id, current["id"], weeks_to_do))
    return {**_batch_jobs[syllabus_id], "status": "started"}


@api_router.get("/syllabus/{syllabus_id}/batch-status")
async def batch_status(syllabus_id: str, current=Depends(get_current_user)):
    job = _batch_jobs.get(syllabus_id)
    if not job:
        # Check how many are already packed
        doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
        if not doc:
            raise HTTPException(status_code=404, detail="Syllabus not found")
        done = sum(1 for l in doc["lessons"] if l.get("pack"))
        return {"status": "idle", "done": done, "total": 32, "current_week": None, "errors": []}
    return job


# ---------- Sharing (public read-only) ----------
class ShareToggle(BaseModel):
    enabled: bool
    listed_in_gallery: Optional[bool] = None


@api_router.post("/syllabus/{syllabus_id}/share")
async def toggle_share(syllabus_id: str, data: ShareToggle, current=Depends(get_current_user)):
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    token = doc.get("share_token") or str(uuid.uuid4()).replace("-", "")[:20]
    update = {"share_enabled": data.enabled, "share_token": token}
    if data.listed_in_gallery is not None:
        update["listed_in_gallery"] = data.listed_in_gallery
    elif "listed_in_gallery" not in doc:
        update["listed_in_gallery"] = True  # default opt-in
    await db.syllabi.update_one(
        {"id": syllabus_id, "user_id": current["id"]},
        {"$set": update},
    )
    return {
        "share_token": token,
        "share_enabled": data.enabled,
        "listed_in_gallery": update.get("listed_in_gallery", doc.get("listed_in_gallery", True)),
    }


@api_router.get("/public/gallery")
async def public_gallery():
    """Return a list of publicly listed syllabi for the /gallery page.
    Only includes each teacher's ACTIVE syllabus to avoid duplicates.
    """
    cursor = db.syllabi.find(
        {"share_enabled": True, "listed_in_gallery": True, "active": True},
        {"_id": 0, "id": 1, "share_token": 1, "user_id": 1, "class_level": 1, "lessons.week": 1, "created_at": 1},
    ).sort("created_at", -1).limit(50)
    items = []
    async for doc in cursor:
        owner = await db.users.find_one({"id": doc["user_id"]}, {"_id": 0, "password_hash": 0, "email": 0}) or {}
        items.append({
            "share_token": doc.get("share_token"),
            "class_level": doc.get("class_level") or owner.get("class_level") or "CM2",
            "lesson_count": len(doc.get("lessons", [])) or 32,
            "created_at": doc.get("created_at"),
            "teacher": {
                "full_name": owner.get("full_name") or "Anonymous teacher",
                "school_name": owner.get("school_name") or "",
                "school_city": owner.get("school_city") or "",
            },
        })
    return items


def _sanitize_sheet_for_public(sheet: dict) -> dict:
    """Strip teacher-only content before it ever leaves the server for an
    unauthenticated viewer — `content` is the raw AI text (still contains
    the answer key before the boundary marker) and `teacher_notes` is the
    extracted answer-key/teacher-notes half; both must be dropped."""
    safe = {k: v for k, v in sheet.items() if k not in ("content", "teacher_notes")}
    return safe


def _sanitize_lesson_for_public(lesson: dict) -> dict:
    safe = dict(lesson)
    safe.pop("special_topic_key", None)
    pack = safe.get("pack")
    if pack:
        safe["pack"] = {
            **{k: v for k, v in pack.items() if k not in ("sheets", "exercise_sheets")},
            "sheets": [_sanitize_sheet_for_public(s) for s in (pack.get("sheets") or [])],
            "exercise_sheets": [_sanitize_sheet_for_public(s) for s in (pack.get("exercise_sheets") or [])],
        }
    homework = safe.get("homework")
    if homework and "answer_key" in homework:
        safe["homework"] = {k: v for k, v in homework.items() if k != "answer_key"}
    return safe


@api_router.get("/public/syllabus/{share_token}")
async def get_public_syllabus(share_token: str):
    doc = await db.syllabi.find_one({"share_token": share_token, "share_enabled": True}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Shared syllabus not found or sharing is disabled.")
    # Fetch owner's display info
    owner = await db.users.find_one({"id": doc["user_id"]}, {"_id": 0, "password_hash": 0}) or {}
    return {
        "id": doc["id"],
        "class_level": doc.get("class_level") or (owner or {}).get("class_level"),
        "lessons": [_sanitize_lesson_for_public(l) for l in doc["lessons"]],
        "shared_by": {
            "full_name": owner.get("full_name"),
            "school_name": owner.get("school_name"),
            "school_city": owner.get("school_city"),
            "class_level": owner.get("class_level"),
        },
    }


# ---------- Homework generator (AI) ----------
@api_router.post("/syllabus/{syllabus_id}/week/{week_num}/homework")
async def generate_homework(syllabus_id: str, week_num: int, current=Depends(get_current_user)):
    _check_ai_rate_limit(current["id"])
    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson = next((l for l in doc["lessons"] if l["week"] == week_num), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Week not found")

    system_msg = (
        "You are a TEFL master teacher trainer for the French national English curriculum. "
        "Generate SHORT, printable homework that reinforces this week's grammar and vocab. "
        "Return ONLY strict valid JSON, no markdown."
    )
    prompt = f"""Create a one-page A4 homework worksheet for a student who has just finished this lesson.

Week {lesson['week']} — Theme: {lesson['theme']} · CEFR {lesson['cefr_level']} · Class level {current.get('class_level') or 'CM2'}
Grammar: {lesson['grammar']}
Vocabulary: {', '.join(lesson['vocabulary'])}

Return JSON with EXACTLY these keys:
{{
  "title": "short title, max 8 words, referring to the week theme",
  "estimated_minutes": 15,
  "instructions_for_student": "one friendly sentence",
  "exercise_1": {{"title": "Gap fill", "instructions": "one sentence", "items": ["8 sentences with ___ blanks using this week's target grammar and vocab"]}},
  "exercise_2": {{"title": "Write your own", "instructions": "one sentence", "items": ["4 short prompts asking the student to write 1 sentence each, using the target grammar and vocab"]}},
  "exercise_3": {{"title": "Vocabulary match", "instructions": "one sentence", "pairs": [{{"word": "vocab word", "definition": "short simple definition"}}]}},
  "note_for_parents": "one friendly sentence for the family, in English",
  "answer_key": {{
    "exercise_1": ["8 answers in order"],
    "exercise_2": ["4 sample sentences in order"],
    "exercise_3": ["repeats each vocab word with its correct definition"]
  }}
}}

Content MUST be age-appropriate and match the CEFR level. Use short clear sentences."""

    try:
        text = await ai_generate(system_msg, prompt, max_tokens=2048)
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            raise ValueError("no JSON in response")
        homework = json.loads(m.group(0))

        for i, l in enumerate(doc["lessons"]):
            if l["week"] == week_num:
                doc["lessons"][i]["homework"] = homework
                doc["lessons"][i]["homework_generated_at"] = datetime.now(timezone.utc).isoformat()
                break
        await db.syllabi.update_one(
            {"id": syllabus_id, "user_id": current["id"]},
            {"$set": {"lessons": doc["lessons"], "updated_at": datetime.now(timezone.utc).isoformat()}},
        )
        return homework
    except AnthropicGenerationError as e:
        msg = str(e)
        logger.error(f"homework error: {msg}")
        if "429" in msg or "rate" in msg.lower() or "overloaded" in msg.lower():
            raise HTTPException(status_code=429, detail="AI is busy — please retry in ~15 seconds.")
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        logger.error(f"homework error: {e}")
        raise HTTPException(status_code=500, detail=f"Homework generation failed: {str(e)}")


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class LessonChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(default_factory=list)
    lang: Optional[str] = "en"  # "en" | "fr" — UI language


@api_router.post("/syllabus/{syllabus_id}/week/{week_num}/chat")
async def lesson_chat(syllabus_id: str, week_num: int, data: LessonChatRequest, current=Depends(get_current_user)):
    """Ask-the-AI chat scoped to a specific lesson. Stateless: full history is sent in each request."""
    _check_ai_rate_limit(current["id"])
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    doc = await db.syllabi.find_one({"id": syllabus_id, "user_id": current["id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    lesson = next((l for l in doc["lessons"] if l["week"] == week_num), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Week not found")

    reply_lang = "French" if (data.lang or "en").lower().startswith("fr") else "English"

    system_msg = f"""You are a friendly, expert TEFL coach helping a French primary/lower-secondary school English teacher.
You are inside the lesson-detail chat for THIS specific lesson:

- Week {lesson['week']}: {lesson['title']}
- CEFR: {lesson['cefr_level']} · Class level: {current.get('class_level') or 'CM2'}
- Grammar focus: {lesson['grammar']}
- Vocabulary: {', '.join(lesson['vocabulary'])}
- Objectives: {' | '.join(lesson['objectives'])}

You help the teacher:
- Rephrase an activity in simpler language
- Level a task down (easier) or up (more challenging)
- Give quick classroom-management tips
- Provide 1-2 concrete examples
- Suggest a warmer / cooler / filler activity

Rules:
- Reply in {reply_lang}. Do NOT switch languages mid-reply.
- Keep replies short and practical (max ~120 words).
- Plain text only — NO markdown, NO asterisks, NO bold/italics syntax. Use short paragraphs and dash bullets.
- Always stay on the topic of this specific lesson."""

    # Build a compact conversation-prefixed prompt (last 8 turns of history)
    history_text = ""
    for msg in (data.history or [])[-8:]:
        content = (msg.content or "")[:800]  # cap each turn
        prefix = "Teacher" if msg.role == "user" else "You (coach)"
        history_text += f"\n{prefix}: {content}"
    prompt = (history_text + f"\nTeacher: {message}\nYou (coach):").strip()

    try:
        response_text = await ai_generate(system_msg, prompt, max_tokens=512)
        cleaned = response_text.strip()
        cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", cleaned)
        cleaned = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\1", cleaned)
        cleaned = re.sub(r"^#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
        return {"response": cleaned}
    except AnthropicGenerationError as e:
        msg_text = str(e)
        logger.error(f"lesson chat error: {msg_text}")
        if "429" in msg_text or "rate" in msg_text.lower() or "overloaded" in msg_text.lower():
            raise HTTPException(status_code=429, detail="AI is busy — please retry in ~15 seconds.")
        raise HTTPException(status_code=500, detail=f"Chat failed: {msg_text}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"lesson chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# ---------- App wiring ----------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
