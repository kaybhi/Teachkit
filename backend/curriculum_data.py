"""
Curriculum reference data — ported 1:1 from the validated lesson-planner
engine (`index.html`, lines 442-1130 as of 2026-08-14). This file is pure
data; see curriculum_lookup.py for the logic that resolves it per week.

Do not hand-edit values here without also checking the source engine —
this is meant to stay a faithful port, not a fork.
"""

SCHOOL_LEVELS = [
    {"id": "cp", "label": "CP", "cycle": "Cycle 2", "ages": "6-7", "cefr": "Pré-A1", "band": 0, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "ce1", "label": "CE1", "cycle": "Cycle 2", "ages": "7-8", "cefr": "Pré-A1", "band": 0, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "ce2", "label": "CE2", "cycle": "Cycle 2", "ages": "8-9", "cefr": "Pré-A1", "band": 0, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "cm1", "label": "CM1", "cycle": "Cycle 3", "ages": "9-10", "cefr": "A1", "band": 1, "lessons_per_week": 2, "duration": "60 min"},
    {"id": "cm2", "label": "CM2", "cycle": "Cycle 3", "ages": "10-11", "cefr": "A1+", "band": 1, "lessons_per_week": 2, "duration": "60 min"},
    {"id": "6e", "label": "6ème", "cycle": "Collège", "ages": "11-12", "cefr": "A1/A2", "band": 2, "lessons_per_week": 2, "duration": "60 min"},
    {"id": "5e", "label": "5ème", "cycle": "Collège", "ages": "12-13", "cefr": "A2", "band": 2, "lessons_per_week": 2, "duration": "60 min"},
    {"id": "4e", "label": "4ème", "cycle": "Collège", "ages": "13-14", "cefr": "A2+", "band": 2, "lessons_per_week": 3, "duration": "60 min"},
    {"id": "3e", "label": "3ème", "cycle": "Collège", "ages": "14-15", "cefr": "B1", "band": 3, "lessons_per_week": 3, "duration": "60 min"},
    {"id": "2nde", "label": "2nde", "cycle": "Lycée", "ages": "15-16", "cefr": "B1+", "band": 3, "lessons_per_week": 3, "duration": "60 min"},
    {"id": "1ere", "label": "1ère", "cycle": "Lycée", "ages": "16-17", "cefr": "B2", "band": 4, "lessons_per_week": 4, "duration": "60 min"},
    {"id": "term", "label": "Terminale", "cycle": "Lycée", "ages": "17-18", "cefr": "B2+", "band": 4, "lessons_per_week": 4, "duration": "60 min"},
]

ADULT_LEVELS = [
    {"id": "adult-a1", "label": "A1", "cycle": "Adultes", "ages": "18+", "cefr": "A1", "band": 2, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "adult-a2", "label": "A2", "cycle": "Adultes", "ages": "18+", "cefr": "A2", "band": 3, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "adult-b1", "label": "B1", "cycle": "Adultes", "ages": "18+", "cefr": "B1", "band": 3, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "adult-b2", "label": "B2", "cycle": "Adultes", "ages": "18+", "cefr": "B2", "band": 4, "lessons_per_week": 1, "duration": "60 min"},
]

BUSINESS_LEVELS = [
    {"id": "biz-b1", "label": "B1", "cycle": "Business", "ages": "18+", "cefr": "B1", "band": 3, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "biz-b2", "label": "B2", "cycle": "Business", "ages": "18+", "cefr": "B2", "band": 4, "lessons_per_week": 1, "duration": "60 min"},
    {"id": "biz-c1", "label": "C1", "cycle": "Business", "ages": "18+", "cefr": "C1", "band": 4, "lessons_per_week": 1, "duration": "60 min"},
]

LEVELS_BY_CLASS_TYPE = {
    "school": SCHOOL_LEVELS,
    "adult": ADULT_LEVELS,
    "business": BUSINESS_LEVELS,
}

ALL_LEVELS = SCHOOL_LEVELS + ADULT_LEVELS + BUSINESS_LEVELS
LEVELS_BY_ID = {lv["id"]: lv for lv in ALL_LEVELS}

CURRICULUM_BLOCKS = {
    1: {
        "name": "Block 1 (Sept - Oct): Foundation",
        "maternelles": "Greetings, Colors, Numbers 1-10, Classroom Objects",
        "primaires": "Alphabet, Spelling, To Be / To Have, Daily Routines (Present Simple)",
        "college": "Present Simple vs Continuous, Adverbs of Frequency, Be/Have Traps",
        "adultes": "Socializing (Jobs/Family), Survival Travel English (Airports, Hotels)",
    },
    2: {
        "name": "Block 2 (Nov - Dec): Expansion",
        "maternelles": "Body Parts, Clothing, Halloween/Christmas Vocab",
        "primaires": "Telling Time, School Subjects, Likes/Dislikes, Festive Vocab",
        "college": "Past Simple (Regular & Irregular), Storytelling, Fixing 'J'ai'",
        "adultes": "Daily Routines, Ordering Food, Past Experiences (Past Simple)",
    },
    3: {
        "name": "Block 3 (Jan - Feb): Deep Dive",
        "maternelles": "Animals (Farm/Wild), Basic Action Verbs (Run, Jump)",
        "primaires": "Describing People/Places, Present Continuous (What are you doing?)",
        "college": "Asking Questions (Do/Does/Did/Wh-), Modal Verbs (Can/Must/Should)",
        "adultes": "Dealing with Problems/Complaints, Making Plans/Arrangements",
    },
    4: {
        "name": "Block 4 (Mar - Apr): Fluency",
        "maternelles": "Food/Fruit, Family Members, Emotions (Happy/Sad)",
        "primaires": "Comparatives/Superlatives, Giving Directions, City Vocab",
        "college": "The Future (Going to vs Will), Debate Formatting (Comparatives)",
        "adultes": "Expressing Opinions, Agree/Disagree, Workplace Comms (Emails)",
    },
    5: {
        "name": "Block 5 (May - Jun): Consolidation",
        "maternelles": "Weather, Summer Vocab, Final Performance Rehearsal",
        "primaires": "Intro to Past Simple (Regular), End of Year Projects",
        "college": "Present Perfect (Experience vs Finished Time), 1st Conditional, Exam Prep",
        "adultes": "Advanced Storytelling (Present Perfect), Conditionals, Open Debates",
    },
}

_MASTER_CURRICULUM_ROWS = [
    {"week": 1, "block": 1, "start": "31 Aug 2026", "end": "05 Sep 2026"},
    {"week": 2, "block": 1, "start": "07 Sep 2026", "end": "12 Sep 2026"},
    {"week": 3, "block": 1, "start": "14 Sep 2026", "end": "19 Sep 2026"},
    {"week": 4, "block": 1, "start": "21 Sep 2026", "end": "26 Sep 2026"},
    {"week": 5, "block": 1, "start": "28 Sep 2026", "end": "03 Oct 2026"},
    {"week": 6, "block": 1, "start": "05 Oct 2026", "end": "10 Oct 2026"},
    {"week": 7, "block": 1, "start": "12 Oct 2026", "end": "17 Oct 2026"},
    {"week": 8, "block": 2, "start": "02 Nov 2026", "end": "07 Nov 2026"},
    {"week": 9, "block": 2, "start": "09 Nov 2026", "end": "14 Nov 2026"},
    {"week": 10, "block": 2, "start": "16 Nov 2026", "end": "21 Nov 2026"},
    {"week": 11, "block": 2, "start": "23 Nov 2026", "end": "28 Nov 2026"},
    {"week": 12, "block": 2, "start": "30 Nov 2026", "end": "05 Dec 2026"},
    {"week": 13, "block": 2, "start": "07 Dec 2026", "end": "12 Dec 2026"},
    {"week": 14, "block": 2, "start": "14 Dec 2026", "end": "19 Dec 2026"},
    {"week": 15, "block": 3, "start": "04 Jan 2027", "end": "09 Jan 2027"},
    {"week": 16, "block": 3, "start": "11 Jan 2027", "end": "16 Jan 2027"},
    {"week": 17, "block": 3, "start": "18 Jan 2027", "end": "23 Jan 2027"},
    {"week": 18, "block": 3, "start": "25 Jan 2027", "end": "30 Jan 2027"},
    {"week": 19, "block": 3, "start": "01 Feb 2027", "end": "06 Feb 2027"},
    {"week": 20, "block": 4, "start": "22 Feb 2027", "end": "27 Feb 2027"},
    {"week": 21, "block": 4, "start": "01 Mar 2027", "end": "06 Mar 2027"},
    {"week": 22, "block": 4, "start": "08 Mar 2027", "end": "13 Mar 2027"},
    {"week": 23, "block": 4, "start": "15 Mar 2027", "end": "20 Mar 2027"},
    {"week": 24, "block": 4, "start": "22 Mar 2027", "end": "27 Mar 2027"},
    {"week": 25, "block": 4, "start": "29 Mar 2027", "end": "03 Apr 2027"},
    {"week": 26, "block": 5, "start": "19 Apr 2027", "end": "24 Apr 2027"},
    {"week": 27, "block": 5, "start": "26 Apr 2027", "end": "01 May 2027"},
    {"week": 28, "block": 5, "start": "03 May 2027", "end": "08 May 2027"},
    {"week": 29, "block": 5, "start": "10 May 2027", "end": "15 May 2027"},
    {"week": 30, "block": 5, "start": "17 May 2027", "end": "22 May 2027"},
    {"week": 31, "block": 5, "start": "24 May 2027", "end": "29 May 2027"},
    {"week": 32, "block": 5, "start": "31 May 2027", "end": "05 Jun 2027"},
]

# Port of `.map(r => Object.assign({}, r, CURRICULUM_BLOCKS[r.block]))` —
# each week row merged with its block's descriptive fields.
MASTER_CURRICULUM = [
    {**row, **CURRICULUM_BLOCKS[row["block"]]} for row in _MASTER_CURRICULUM_ROWS
]

# CM2 has a detailed week-by-week PPP (Presentation/Practice/Production) plan.
# Other levels fall back to the tier-level Master Curriculum Map topic above.
CM2_CURRICULUM = [
    {"week": 1, "period": "P1", "theme": "Greetings + family + numbers", "vocab": "greetings, family, numbers 1-100", "grammar": "be: am/is/are + short answers", "class_type": "Vocabulary Focus"},
    {"week": 2, "period": "P1", "theme": "Colours + classroom objects", "vocab": "colours, school objects", "grammar": "have got / has got: I've got...", "class_type": "Grammar Focus"},
    {"week": 3, "period": "P1", "theme": "Clothes + animals", "vocab": "clothing, animals", "grammar": "This/that + plurals: These are my shoes.", "class_type": "Grammar Focus"},
    {"week": 4, "period": "P1", "theme": "Prepositions + simple questions", "vocab": "position words", "grammar": "Where is...? It's + preposition", "class_type": "Grammar Focus"},
    {"week": 5, "period": "P1", "theme": "Review + A1 core accuracy", "vocab": "P1 all content", "grammar": "Review Q&A dialogue: family + objects", "class_type": "Review"},
    {"week": 6, "period": "P1", "theme": "Assessment P1", "vocab": "P1 content", "grammar": "Short oral + written activity: describe your school bag", "class_type": "Assessment"},
    {"week": 7, "period": "P2", "theme": "House + furniture", "vocab": "rooms, furniture words", "grammar": "There is / There are: There's a sofa in the living room.", "class_type": "Grammar Focus"},
    {"week": 8, "period": "P2", "theme": "Food + drinks", "vocab": "food, drink words", "grammar": "Present simple: I like / I don't like + food", "class_type": "Grammar Focus"},
    {"week": 9, "period": "P2", "theme": "Daily actions", "vocab": "wake up, eat, go to school, play, sleep", "grammar": "WH questions: What do you eat for breakfast?", "class_type": "Grammar Focus"},
    {"week": 10, "period": "P2", "theme": "Toys + hobbies descriptions", "vocab": "toys, hobbies", "grammar": "have got + WH questions combined", "class_type": "Grammar Focus"},
    {"week": 11, "period": "P2", "theme": "Short paragraph reading + production", "vocab": "P2 vocabulary", "grammar": "Read + produce short description of home/routine", "class_type": "Grammar Focus"},
    {"week": 12, "period": "P2", "theme": "Review P2", "vocab": "P2 content", "grammar": "Checkpoint: written + oral short description", "class_type": "Review"},
    {"week": 13, "period": "P3", "theme": "Extended animals + nature", "vocab": "wild animals, nature words", "grammar": "Present continuous: The elephant is eating grass.", "class_type": "Grammar Focus"},
    {"week": 14, "period": "P3", "theme": "Town + places", "vocab": "town, places vocabulary", "grammar": "can / can't: You can see lions at the zoo.", "class_type": "Grammar Focus"},
    {"week": 15, "period": "P3", "theme": "Clothes + actions in context", "vocab": "clothes + action verbs", "grammar": "Present continuous + clothes: She's wearing a coat and running.", "class_type": "Grammar Focus"},
    {"week": 16, "period": "P3", "theme": "Prepositions of place review", "vocab": "position words", "grammar": "Describe an image using prepositions", "class_type": "Grammar Focus"},
    {"week": 17, "period": "P3", "theme": "Completion + reading tasks", "vocab": "P3 vocabulary", "grammar": "Short reading + fill-in activity", "class_type": "Grammar Focus"},
    {"week": 18, "period": "P3", "theme": "Review P3", "vocab": "P3 content", "grammar": "Oral + written checkpoint", "class_type": "Review"},
    {"week": 19, "period": "P4", "theme": "Transport + leisure", "vocab": "transport, leisure words", "grammar": "Present simple vs continuous: contrast and use", "class_type": "Grammar Focus"},
    {"week": 20, "period": "P4", "theme": "Time + daily routine", "vocab": "time expressions, routine verbs", "grammar": "WH questions with time: What time do you...?", "class_type": "Grammar Focus"},
    {"week": 21, "period": "P4", "theme": "Using and / but / because", "vocab": "P4 content vocabulary", "grammar": "Connectors: I like football but I don't like swimming.", "class_type": "Grammar Focus"},
    {"week": 22, "period": "P4", "theme": "Complex questions", "vocab": "extended vocabulary", "grammar": "Question formation: Where do you go? What do you do?", "class_type": "Grammar Focus"},
    {"week": 23, "period": "P4", "theme": "Short paragraph writing", "vocab": "P4 vocabulary", "grammar": "Write 4-5 sentences about daily routine + transport", "class_type": "Grammar Focus"},
    {"week": 24, "period": "P4", "theme": "Possessives (optional extension)", "vocab": "possessive adjectives: my, your, his, her", "grammar": "His dog is big. Her book is red.", "class_type": "Grammar Focus"},
    {"week": 25, "period": "P4", "theme": "Review P4 + assessment", "vocab": "P4 content", "grammar": "Oral dialogue + written sentences checkpoint", "class_type": "Assessment"},
    {"week": 26, "period": "P5", "theme": "Daily situations review", "vocab": "revision A1 all", "grammar": "like + -ing: I like reading. She likes swimming.", "class_type": "Grammar Focus"},
    {"week": 27, "period": "P5", "theme": "Possessives revision", "vocab": "possessives + pronouns", "grammar": "Possessive short answers: It's mine / It's his.", "class_type": "Grammar Focus"},
    {"week": 28, "period": "P5", "theme": "Full A1 oral task practice", "vocab": "all CM2 content", "grammar": "Speak about yourself: family, home, food, hobbies", "class_type": "Grammar Focus"},
    {"week": 29, "period": "P5", "theme": "Full A1 written task practice", "vocab": "all CM2 content", "grammar": "Write a short self-description (5-6 sentences)", "class_type": "Grammar Focus"},
    {"week": 30, "period": "P5", "theme": "Full review P1-P3", "vocab": "CM2 P1-P3", "grammar": "Mixed games + written review", "class_type": "Review"},
    {"week": 31, "period": "P5", "theme": "Full review P4-P5", "vocab": "CM2 P4-P5", "grammar": "Oral task + written task simulation", "class_type": "Review"},
    {"week": 32, "period": "P5", "theme": "End of year assessment", "vocab": "all CM2 content", "grammar": "A1 oral task + short written task", "class_type": "Assessment"},
]

# ============================================================
# SCHOOL WEEKLY CURRICULA — one per band-group, ported from the local
# lesson-planner engine (index.html, 2026-09-18) after a real 5ème class
# was found stuck on "Present Simple vs Continuous, Adverbs of Frequency,
# Be/Have Traps" for 7 straight weeks — every school level except CM2 had
# only a flat block-level theme string, handed to every week (and every
# grade sharing that tier) unchanged. Real teacher rule: a topic runs for
# at most 2 classes before moving on.
#
# build_weekly_curriculum() raises immediately if any topic exceeds 2 weeks
# or the total doesn't sum to 32 — a hard structural guarantee, not a
# convention that can silently drift the way the old flat strings did.
# ============================================================
def build_weekly_curriculum(topics: list) -> list:
    """16 topics, each with an "a" week and a "b" week -> 32 week-rows. The two
    weeks of a topic must differ in focus, vocab AND grammar (two identical
    classes back to back is a bug — real 5ème weeks 5 and 6 came out as the
    same lesson). Each row carries a part_note telling the generator what the
    other week covers, so examples don't repeat."""
    rows = []
    week = 1
    for t in topics:
        a, b = t.get("a"), t.get("b")
        if not a or not b:
            raise ValueError(f'Curriculum topic "{t["theme"]}" needs both an "a" and a "b" week')
        if a["focus"] == b["focus"] or a["vocab"] == b["vocab"] or a["grammar"] == b["grammar"]:
            raise ValueError(f'Curriculum topic "{t["theme"]}": its two weeks must differ in focus, vocab AND grammar')
        for i, p in enumerate((a, b)):
            if i == 0:
                part_note = (
                    f'This is week 1 of 2 on "{t["theme"]}". This week\'s focus: {a["focus"]}. '
                    f'Next week covers {b["focus"]}, so do NOT teach or test that yet.'
                )
            else:
                part_note = (
                    f'This is week 2 of 2 on "{t["theme"]}". LAST WEEK covered: {a["focus"]} ({a["vocab"]}). '
                    f'This week is DIFFERENT: {b["focus"]}. Do NOT reuse last week\'s vocabulary, example sentences, '
                    f'characters, verbs or sentence stems — build on it with new content.'
                )
            rows.append({
                "week": week,
                "topic": t["theme"],
                "theme": f'{t["theme"]} — {p["focus"]}',
                "vocab": p["vocab"],
                "grammar": p["grammar"],
                "class_type": t["class_type"],
                "part_note": part_note,
            })
            week += 1
    if week - 1 != 32:
        raise ValueError(f"Weekly curriculum sums to {week - 1} weeks, expected 32")
    return rows


# Band 0 — CP/CE1/CE2 (ages 6-9). Grammar allowed is almost nothing (to be,
# basic noun phrases, colours, numbers 1-20) — the year is mostly vocabulary
# expansion inside that one tiny frame ("It's a...", "This is my..."), which
# is exactly how real early-years EFL works.
BAND0_CURRICULUM = build_weekly_curriculum([
    {
        "theme": "Hello & introductions", "class_type": "Vocabulary Focus",
        "a": {"focus": "greetings", "vocab": "hello, hi, goodbye, bye, yes, no", "grammar": "Hello! Goodbye! Yes. No."},
        "b": {"focus": "names", "vocab": "name, boy, girl, friend, teacher, I'm", "grammar": "My name is... What's your name? I'm..."},
    },
    {
        "theme": "Colours", "class_type": "Vocabulary Focus",
        "a": {"focus": "primary colours", "vocab": "red, blue, yellow, green, black, white", "grammar": "It's + colour: It's red."},
        "b": {"focus": "more colours", "vocab": "pink, orange, purple, brown, grey, colour", "grammar": "What colour is it? It's pink."},
    },
    {
        "theme": "Numbers 1-10", "class_type": "Vocabulary Focus",
        "a": {"focus": "one to five", "vocab": "one, two, three, four, five, count", "grammar": "Counting: one, two, three..."},
        "b": {"focus": "six to ten", "vocab": "six, seven, eight, nine, ten, how many", "grammar": "How many? Six! Counting objects."},
    },
    {
        "theme": "Classroom objects", "class_type": "Vocabulary Focus",
        "a": {"focus": "things on my desk", "vocab": "pen, book, bag, chair, table, pencil", "grammar": "It's a...: It's a pen."},
        "b": {"focus": "things in the room", "vocab": "rubber, ruler, desk, board, door, window", "grammar": "What is it? It's a ruler."},
    },
    {
        "theme": "Family", "class_type": "Vocabulary Focus",
        "a": {"focus": "close family", "vocab": "mum, dad, sister, brother, baby, family", "grammar": "This is my...: This is my mum."},
        "b": {"focus": "the wider family", "vocab": "grandma, grandpa, aunt, uncle, friend, me", "grammar": "Who is it? This is my grandma."},
    },
    {
        "theme": "Pets & animals", "class_type": "Vocabulary Focus",
        "a": {"focus": "pets", "vocab": "cat, dog, bird, fish, rabbit, hamster", "grammar": "It's a...: It's a cat."},
        "b": {"focus": "big and small", "vocab": "big, small, mouse, horse, snake, parrot", "grammar": "It's a big/small...: It's a big horse."},
    },
    {
        "theme": "Body parts", "class_type": "Vocabulary Focus",
        "a": {"focus": "head and hands", "vocab": "head, hand, foot, eye, ear, nose", "grammar": "It's my...: It's my hand."},
        "b": {"focus": "the whole body", "vocab": "arm, leg, mouth, hair, face, finger", "grammar": "This is my...: This is my arm."},
    },
    {
        "theme": "Fruit & food", "class_type": "Vocabulary Focus",
        "a": {"focus": "fruit", "vocab": "apple, banana, orange, pear, grapes, strawberry", "grammar": "It's a/an...: It's an apple."},
        "b": {"focus": "food and drink", "vocab": "bread, milk, egg, water, cheese, cake", "grammar": "It's a cake. It's milk."},
    },
    {
        "theme": "Toys", "class_type": "Vocabulary Focus",
        "a": {"focus": "classic toys", "vocab": "ball, doll, kite, car, teddy bear, blocks", "grammar": "It's a...: It's a ball."},
        "b": {"focus": "my toys", "vocab": "robot, train, puzzle, bike, drum, game", "grammar": "It's my...: It's my robot."},
    },
    {
        "theme": "Clothes", "class_type": "Vocabulary Focus",
        "a": {"focus": "one item", "vocab": "hat, shoes, coat, dress, t-shirt, socks", "grammar": "It's a hat."},
        "b": {"focus": "two items", "vocab": "skirt, trousers, jumper, jeans, scarf, gloves", "grammar": "They are trousers. They are jeans."},
    },
    {
        "theme": "Weather", "class_type": "Vocabulary Focus",
        "a": {"focus": "everyday weather", "vocab": "sunny, rainy, cold, hot, windy, cloudy", "grammar": "It's + weather word: It's sunny."},
        "b": {"focus": "more weather", "vocab": "snowy, foggy, stormy, warm, cool, rainbow", "grammar": "It's snowy. It's a rainbow!"},
    },
    {
        "theme": "Shapes", "class_type": "Vocabulary Focus",
        "a": {"focus": "shapes", "vocab": "circle, square, triangle, star, heart, box", "grammar": "It's a...: It's a circle."},
        "b": {"focus": "colour + shape", "vocab": "red star, blue heart, green triangle, yellow circle, black square, white box", "grammar": "It's a red star. (colour + shape)"},
    },
    {
        "theme": "Numbers 11-20", "class_type": "Vocabulary Focus",
        "a": {"focus": "eleven to fifteen", "vocab": "eleven, twelve, thirteen, fourteen, fifteen, count", "grammar": "Counting 11-15."},
        "b": {"focus": "sixteen to twenty", "vocab": "sixteen, seventeen, eighteen, nineteen, twenty, how many", "grammar": "How many? Counting 16-20."},
    },
    {
        "theme": "Farm animals", "class_type": "Vocabulary Focus",
        "a": {"focus": "one animal", "vocab": "cow, sheep, horse, goat, donkey, farm", "grammar": "It's a...: It's a cow."},
        "b": {"focus": "two or more animals", "vocab": "duck, pig, hen, chick, turkey, goose", "grammar": "They are ducks. They are pigs."},
    },
    {
        "theme": "Transport", "class_type": "Vocabulary Focus",
        "a": {"focus": "everyday transport", "vocab": "car, bus, train, bike, plane, boat", "grammar": "It's a...: It's a car."},
        "b": {"focus": "big and small vehicles", "vocab": "taxi, tram, lorry, ship, helicopter, scooter", "grammar": "It's a big red bus. (size + colour + noun)"},
    },
    {
        "theme": "Review & end-of-year show", "class_type": "Review",
        "a": {"focus": "colours, numbers, classroom", "vocab": "review: colours, numbers 1-20, classroom objects", "grammar": "Review: It's a.../What colour is it?"},
        "b": {"focus": "family, animals, food", "vocab": "review: family, animals, food, toys, clothes", "grammar": "Review: This is my.../They are.../My name is..."},
    },
])

# Band 1 — CM1 (ages 9-10, the year before CM2). Present Simple, have got,
# can/can't, Do/Does questions. Deliberately distinct progression from CM2
# (CM2 already has its own detailed year, one grade ahead).
CM1_CURRICULUM = build_weekly_curriculum([
    {
        "theme": "All about me", "class_type": "Vocabulary Focus",
        "a": {"focus": "greetings & names", "vocab": "name, hello, nice to meet you, I am, my, your", "grammar": "I am... / My name is... / Nice to meet you."},
        "b": {"focus": "age & home", "vocab": "how old, nine, ten, eleven, France, live", "grammar": "How old are you? I am nine. I live in France."},
    },
    {
        "theme": "Family", "class_type": "Grammar Focus",
        "a": {"focus": "I have got", "vocab": "mum, dad, brother, sister, grandma, grandpa", "grammar": "Have got: I've got a brother."},
        "b": {"focus": "he/she has got", "vocab": "cousin, aunt, uncle, baby, big, small", "grammar": "He's got / She's got: She's got two cousins."},
    },
    {
        "theme": "School subjects", "class_type": "Grammar Focus",
        "a": {"focus": "saying what I like", "vocab": "maths, English, art, sport, music, break", "grammar": "I like maths. I don't like art."},
        "b": {"focus": "asking what you like", "vocab": "science, French, history, lunch, teacher, favourite", "grammar": "Do you like...? Yes, I do. / No, I don't."},
    },
    {
        "theme": "Age & counting", "class_type": "Grammar Focus",
        "a": {"focus": "my age & birthday", "vocab": "birthday, old, young, numbers to 20, month, today", "grammar": "How old are you? I am nine. My birthday is in May."},
        "b": {"focus": "other people's ages", "vocab": "twenty, thirty, forty, fifty, sixty, hundred", "grammar": "He is / She is + number: My mum is forty."},
    },
    {
        "theme": "Pets & animals", "class_type": "Grammar Focus",
        "a": {"focus": "describing my pet", "vocab": "dog, cat, rabbit, fish, hamster, bird", "grammar": "I've got a dog. It's big. It's brown."},
        "b": {"focus": "asking about pets", "vocab": "pet, name, black, white, brown, what", "grammar": "Have you got a pet? Yes, I have. / No, I haven't."},
    },
    {
        "theme": "Daily routine", "class_type": "Grammar Focus",
        "a": {"focus": "my day (I)", "vocab": "wake up, get up, wash, eat breakfast, go to school, come home", "grammar": "Present Simple I: I wake up at seven."},
        "b": {"focus": "his/her day (he/she)", "vocab": "play, do homework, eat dinner, watch TV, go to bed, sleep", "grammar": "Present Simple he/she: She wakes up at 7. He goes to bed."},
    },
    {
        "theme": "Food & likes", "class_type": "Grammar Focus",
        "a": {"focus": "likes & dislikes", "vocab": "pizza, chocolate, vegetables, fruit, cheese, ice cream", "grammar": "I like pizza. I don't like fish."},
        "b": {"focus": "asking & answering", "vocab": "chicken, rice, pasta, soup, juice, milk", "grammar": "Do you like...? Does he like...? Yes, he does. / No, he doesn't."},
    },
    {
        "theme": "Sports & abilities", "class_type": "Grammar Focus",
        "a": {"focus": "I can / I can't", "vocab": "swim, run, jump, ride a bike, play football, dance", "grammar": "Can/can't: I can swim. I can't fly."},
        "b": {"focus": "asking about abilities", "vocab": "sing, draw, climb, skate, cook, play the guitar", "grammar": "Can you...? Yes, I can. / No, I can't. He can run."},
    },
    {
        "theme": "My house", "class_type": "Grammar Focus",
        "a": {"focus": "rooms", "vocab": "bedroom, kitchen, bathroom, garden, living room, big", "grammar": "My house has got a garden. It's big."},
        "b": {"focus": "things in my room", "vocab": "bed, table, sofa, TV, lamp, window", "grammar": "I've got a big bed. My bedroom has got a lamp."},
    },
    {
        "theme": "Hobbies", "class_type": "Grammar Focus",
        "a": {"focus": "what I do", "vocab": "draw, read, dance, play games, watch TV, listen to music", "grammar": "Present Simple: I play football on Saturdays."},
        "b": {"focus": "what he/she does", "vocab": "football, tennis, guitar, piano, chess, cards", "grammar": "Present Simple -s: He plays tennis. She reads. Do you play...?"},
    },
    {
        "theme": "Clothes & weather", "class_type": "Grammar Focus",
        "a": {"focus": "clothes", "vocab": "coat, hat, boots, scarf, jumper, gloves", "grammar": "I wear a coat. She wears boots."},
        "b": {"focus": "weather & clothes", "vocab": "cold, hot, rainy, sunny, snowy, windy", "grammar": "It's rainy. I wear boots when it's rainy."},
    },
    {
        "theme": "Jobs", "class_type": "Grammar Focus",
        "a": {"focus": "who they are", "vocab": "teacher, doctor, farmer, nurse, driver, cook", "grammar": "My dad is a teacher. She is a doctor."},
        "b": {"focus": "where they work", "vocab": "school, hospital, farm, shop, restaurant, office", "grammar": "He works in a school. Where does she work?"},
    },
    {
        "theme": "Time & schedule", "class_type": "Grammar Focus",
        "a": {"focus": "telling the time", "vocab": "o'clock, half past, morning, afternoon, evening, night", "grammar": "What time is it? It's seven o'clock."},
        "b": {"focus": "when I do things", "vocab": "wake up, lunch, dinner, school, bed, at", "grammar": "What time do you wake up? I wake up at seven."},
    },
    {
        "theme": "Animal abilities", "class_type": "Grammar Focus",
        "a": {"focus": "what animals can do", "vocab": "fly, swim, climb, run, jump, walk", "grammar": "Can/can't: Birds can fly. Fish can't walk."},
        "b": {"focus": "asking about animals", "vocab": "monkey, snake, bird, fish, elephant, kangaroo", "grammar": "Can a monkey climb? Yes, it can. / No, it can't."},
    },
    {
        "theme": "Free time", "class_type": "Review",
        "a": {"focus": "my weekend", "vocab": "weekend, friends, park, games, fun, Saturday", "grammar": "Present Simple review, mixed persons: I play. She goes."},
        "b": {"focus": "asking about the weekend", "vocab": "Sunday, visit, cinema, family, play, do", "grammar": "What do you do at the weekend? Do you...? Does he...?"},
    },
    {
        "theme": "Year review", "class_type": "Review",
        "a": {"focus": "review part 1", "vocab": "review: family, pets, school, food, my house", "grammar": "Review: I am, I've got, Do you like...?"},
        "b": {"focus": "review part 2", "vocab": "review: sports, routines, hobbies, jobs, time", "grammar": "Review: can/can't, Present Simple, What time...?"},
    },
])

# Band 2 — 6e/5e/4e (ages 11-14, all share this band's grammar ceiling).
# Present Simple+Continuous, simple past, comparatives, going to, must/should.
# FORBIDDEN for this band: Conditional 2/3, past continuous, passive,
# relative clauses — so "going to" and "must/should" are as far as this
# group goes on future/obligation; the old flat block string that later
# pushed Present Perfect + Conditional 1 onto this group (band-3 content)
# is not carried over here.
BAND2_CURRICULUM = build_weekly_curriculum([
    {
        "theme": "Introductions & routines", "class_type": "Review",
        "a": {"focus": "introducing yourself", "vocab": "introduce yourself, hobbies, school, family, favourite", "grammar": "Present Simple review: I am... I like... I go to school by bus."},
        "b": {"focus": "asking about others", "vocab": "interview, ask, answer, live, come from, partner", "grammar": "Present Simple questions: Where do you live? What do you like?"},
    },
    {
        "theme": "Daily routines + frequency", "class_type": "Grammar Focus",
        "a": {"focus": "adverbs of frequency", "vocab": "always, usually, often, sometimes, never, routine", "grammar": "Adverbs before the verb: I always eat breakfast."},
        "b": {"focus": "how often?", "vocab": "every day, once a week, twice a month, on Mondays, weekend, how often", "grammar": "How often do you...? I go swimming twice a week."},
    },
    {
        "theme": "What's happening now", "class_type": "Grammar Focus",
        "a": {"focus": "statements", "vocab": "right now, at the moment, look, listen, eat, drink", "grammar": "Present Continuous statements: She is eating. They are listening."},
        "b": {"focus": "questions, negatives & contrast", "vocab": "today, usually, but, wear, wait, run, smile", "grammar": "Are you...? Yes, I am. He isn't sleeping. I usually walk, but today I'm taking the bus."},
    },
    {
        "theme": "Be/have & personal info", "class_type": "Grammar Focus",
        "a": {"focus": "feelings with be", "vocab": "hungry, cold, tired, thirsty, hot, afraid", "grammar": "Be for feelings: I am hungry (not I have hungry)."},
        "b": {"focus": "age & have got", "vocab": "years old, old, right, wrong, have got, brother", "grammar": "I am twelve (not I have twelve years). I've got a brother."},
    },
    {
        "theme": "Yesterday (regular verbs)", "class_type": "Grammar Focus",
        "a": {"focus": "affirmative", "vocab": "watched, played, walked, cooked, yesterday, last night", "grammar": "Past Simple regular verbs: I watched TV yesterday."},
        "b": {"focus": "negatives & questions", "vocab": "cleaned, listened, helped, visited, ago, did", "grammar": "I didn't watch TV. Did you play? Yes, I did. / No, I didn't."},
    },
    {
        "theme": "Yesterday (irregular verbs)", "class_type": "Grammar Focus",
        "a": {"focus": "go, see, eat, have, come, do", "vocab": "went, saw, ate, had, came, did", "grammar": "Past Simple irregular: I went to the park. She saw a film."},
        "b": {"focus": "make, take, get, give + questions", "vocab": "made, took, got, gave, didn't, did", "grammar": "Did you see...? I didn't eat. He made a cake."},
    },
    {
        "theme": "School rules", "class_type": "Grammar Focus",
        "a": {"focus": "must", "vocab": "must, uniform, homework, listen, be on time, rule", "grammar": "Must for obligation: You must wear a uniform."},
        "b": {"focus": "mustn't", "vocab": "mustn't, phone, run, shout, cheat, late", "grammar": "Mustn't for prohibition: You mustn't use your phone in class."},
    },
    {
        "theme": "Comparing things", "class_type": "Grammar Focus",
        "a": {"focus": "short adjectives", "vocab": "bigger, smaller, taller, faster, older, than", "grammar": "Comparatives: Tom is taller than Ben."},
        "b": {"focus": "long adjectives", "vocab": "more interesting, more expensive, more difficult, more beautiful, better, worse", "grammar": "More + adjective: Maths is more difficult than art."},
    },
    {
        "theme": "Future plans", "class_type": "Grammar Focus",
        "a": {"focus": "statements", "vocab": "going to, weekend, holiday, plan, tomorrow, visit", "grammar": "Going to for future plans: I'm going to visit my cousins. I'm not going to..."},
        "b": {"focus": "questions & answers", "vocab": "next week, tonight, travel, invite, buy, invitation", "grammar": "Are you going to...? Yes, I am. What are you going to do?"},
    },
    {
        "theme": "Hobbies & free time", "class_type": "Review",
        "a": {"focus": "habits (Present Simple)", "vocab": "review of hobby vocabulary, club, team, practise, often, weekend", "grammar": "Present Simple: What do you do in your free time?"},
        "b": {"focus": "now vs habits", "vocab": "at the moment, today, usually, but, join, watch", "grammar": "Present Simple vs Continuous contrast: I usually play, but now I am reading."},
    },
    {
        "theme": "Health & advice", "class_type": "Grammar Focus",
        "a": {"focus": "should / shouldn't", "vocab": "should, shouldn't, healthy, sleep, drink water, exercise", "grammar": "Should/shouldn't for advice: You should drink water."},
        "b": {"focus": "symptoms & advice", "vocab": "headache, stomachache, cold, doctor, medicine, rest", "grammar": "What's the matter? I've got a headache. You should see a doctor."},
    },
    {
        "theme": "Past experiences", "class_type": "Grammar Focus",
        "a": {"focus": "telling", "vocab": "trip, holiday, last year, ago, last summer, visited", "grammar": "Past Simple regular + irregular mixed: Last summer I went to Spain."},
        "b": {"focus": "asking", "vocab": "where, who, what, when, how, with", "grammar": "Where did you go? What did you do? Who did you see?"},
    },
    {
        "theme": "Weekend plans extension", "class_type": "Grammar Focus",
        "a": {"focus": "invitations", "vocab": "invite, party, cinema, picnic, join, let's", "grammar": "Would you like to come? Let's go! I'm going to..."},
        "b": {"focus": "reasons & times", "vocab": "tonight, next Saturday, because, so, after school, plan", "grammar": "Going to + because: I'm going to stay home because I'm tired."},
    },
    {
        "theme": "Rules & the environment", "class_type": "Grammar Focus",
        "a": {"focus": "must / mustn't", "vocab": "recycle, waste, plastic, save water, protect, mustn't", "grammar": "We must recycle. We mustn't waste water."},
        "b": {"focus": "should for suggestions", "vocab": "turn off, bin, energy, plant trees, pollution, planet", "grammar": "We should turn off the lights. What should we do?"},
    },
    {
        "theme": "Storytelling", "class_type": "Review",
        "a": {"focus": "sequence words", "vocab": "first, then, after that, finally, once upon a time, suddenly", "grammar": "Past Simple with sequence words: First he opened the door. Then he..."},
        "b": {"focus": "was/were & description", "vocab": "was, were, sunny, happy, afraid, dark", "grammar": "Past Simple of be: It was a dark night. They were afraid."},
    },
    {
        "theme": "End of year review", "class_type": "Review",
        "a": {"focus": "oral checkpoint", "vocab": "review of the year's topics, speaking, partner, ask, answer", "grammar": "Mixed review — oral: present, past, going to."},
        "b": {"focus": "written checkpoint", "vocab": "review of the year's topics, write, sentence, correct, test", "grammar": "Mixed review — written: must/should, comparatives, questions."},
    },
])

# Band 3 — 3e/2nde (ages 14-16). All past tenses, Conditional 1 & 2, passive,
# relative clauses. FORBIDDEN: Conditional 3, complex reported speech,
# subjunctive — simple reported speech (basic backshift) is fine here.
BAND3_CURRICULUM = build_weekly_curriculum([
    {
        "theme": "Settling in — past review", "class_type": "Review",
        "a": {"focus": "regular verbs & time expressions", "vocab": "last summer, ago, yesterday, in 2020, visited, decided, stayed", "grammar": "Past Simple review — narrating last summer."},
        "b": {"focus": "irregular verbs & questions", "vocab": "went, met, bought, wrote, took, did you, where, who", "grammar": "Past Simple questions and irregular verbs: Where did you go? Who did you meet?"},
    },
    {
        "theme": "In the middle of it", "class_type": "Grammar Focus",
        "a": {"focus": "Past Continuous", "vocab": "was/were + -ing, at eight o'clock, all evening, watching, cooking, waiting", "grammar": "Past Continuous: I was watching TV at eight."},
        "b": {"focus": "Past Simple vs Continuous", "vocab": "when, while, interrupted, suddenly, rang, arrived", "grammar": "I was walking when I saw an accident. While she was cooking, the phone rang."},
    },
    {
        "theme": "Life experiences", "class_type": "Grammar Focus",
        "a": {"focus": "ever / never", "vocab": "have been, have never, ever, tried, seen, eaten", "grammar": "Present Perfect for experience: Have you ever been to London?"},
        "b": {"focus": "already / yet / just, for / since", "vocab": "already, yet, just, for, since, been vs gone", "grammar": "I've just finished. She hasn't called yet. I've lived here since 2019."},
    },
    {
        "theme": "Real possibilities", "class_type": "Grammar Focus",
        "a": {"focus": "Conditional 1 statements", "vocab": "if, will, possible, decision, weather, plan", "grammar": "Conditional 1: If it rains, I will stay home."},
        "b": {"focus": "questions, unless & when", "vocab": "unless, when, what will you do, promise, warn, probably", "grammar": "What will you do if...? Unless you hurry, you will be late."},
    },
    {
        "theme": "Imagining things", "class_type": "Grammar Focus",
        "a": {"focus": "Conditional 2 statements", "vocab": "if, would, imagine, hypothetical, rich, famous", "grammar": "Conditional 2: If I were rich, I would travel."},
        "b": {"focus": "questions & advice", "vocab": "if I were you, advice, what would you do, choice, dream, wish", "grammar": "What would you do if...? If I were you, I would..."},
    },
    {
        "theme": "What was done", "class_type": "Grammar Focus",
        "a": {"focus": "passive statements", "vocab": "was built, was invented, is spoken, is made, was painted, by", "grammar": "Passive voice: The window was broken. English is spoken here."},
        "b": {"focus": "passive questions & agent", "vocab": "who was it written by, when was it invented, discovered, designed, founded, by", "grammar": "Was it built by...? When was it invented?"},
    },
    {
        "theme": "Describing people & things", "class_type": "Grammar Focus",
        "a": {"focus": "who / which", "vocab": "who, which, neighbour, colleague, thing, person", "grammar": "Relative clauses: The man who lives next door is a doctor."},
        "b": {"focus": "that / where / whose", "vocab": "that, where, whose, place, city, owner", "grammar": "The town where I grew up... The girl whose bag is red..."},
    },
    {
        "theme": "Telling a story", "class_type": "Grammar Focus",
        "a": {"focus": "setting the scene", "vocab": "one day, at first, meanwhile, in the end, suddenly, afterwards", "grammar": "Past Simple + Past Continuous in narrative with linkers."},
        "b": {"focus": "earlier events", "vocab": "had already, before, by the time, after, realised, discovered", "grammar": "Past Perfect: When I arrived, the film had started."},
    },
    {
        "theme": "Opinions & debate", "class_type": "Review",
        "a": {"focus": "giving opinions", "vocab": "in my opinion, I think, agree, disagree, reason, because", "grammar": "Opinions supported with Conditional 1: If we do this, it will help."},
        "b": {"focus": "counter-arguments", "vocab": "however, on the other hand, although, in contrast, point, argument", "grammar": "Conditional 2 in argument: If schools were free, more people would study."},
    },
    {
        "theme": "Global issues", "class_type": "Grammar Focus",
        "a": {"focus": "problems (passive)", "vocab": "environment, pollution, is caused by, was destroyed, threatened, waste", "grammar": "Passive in context: Forests are being cut down. Rivers are polluted."},
        "b": {"focus": "solutions (relative clauses)", "vocab": "solution, protect, people who, companies that, a plan which, recycle", "grammar": "Relative clauses in context: People who recycle help the planet."},
    },
    {
        "theme": "Reporting what people say", "class_type": "Grammar Focus",
        "a": {"focus": "reported statements", "vocab": "said, told, that, reported, admitted, explained", "grammar": "Simple reported speech: She said she was tired."},
        "b": {"focus": "say vs tell, requests", "vocab": "told me to, asked me to, say, tell, ordered, warned", "grammar": "She told me to sit down. He said that he was busy."},
    },
    {
        "theme": "News & media", "class_type": "Grammar Focus",
        "a": {"focus": "headlines", "vocab": "headline, announced, confirmed, rescued, arrested, elected", "grammar": "Passive in headlines: Three people were rescued."},
        "b": {"focus": "news reports", "vocab": "report, witness, according to, reporter, incident, police", "grammar": "News report: Past Simple + Past Continuous + passive together."},
    },
    {
        "theme": "Ambitions & the future", "class_type": "Grammar Focus",
        "a": {"focus": "what I want", "vocab": "hope, dream, would like to, career, want to, plan to", "grammar": "I would like to be... I hope to study..."},
        "b": {"focus": "imagined futures", "vocab": "if I became, would earn, would live, abroad, success, salary", "grammar": "Conditional 2: If I became a doctor, I would help people."},
    },
    {
        "theme": "Culture & travel", "class_type": "Grammar Focus",
        "a": {"focus": "describing places", "vocab": "monument, tradition, festival, region, which, where", "grammar": "Relative clauses: Paris is a city which attracts millions of tourists."},
        "b": {"focus": "travel stories", "vocab": "journey, abroad, sightseeing, souvenir, have visited, was amazed", "grammar": "Present Perfect experiences + Past Simple details: I have been to Rome. I visited the Colosseum."},
    },
    {
        "theme": "Mixed review", "class_type": "Review",
        "a": {"focus": "past tenses review", "vocab": "review of the year's topics, narrative, timeline, memory, event", "grammar": "Mixed past tenses: Simple, Continuous, Perfect."},
        "b": {"focus": "conditionals & passive review", "vocab": "review of the year's topics, if, would, will, made, built", "grammar": "Conditionals 1 & 2 + passive review."},
    },
    {
        "theme": "Exam preparation", "class_type": "Assessment",
        "a": {"focus": "mock oral", "vocab": "review of the year's topics, describe, opinion, question, picture", "grammar": "Full mock exam — oral."},
        "b": {"focus": "mock written", "vocab": "review of the year's topics, essay, email, paragraph, correct", "grammar": "Full mock exam — written."},
    },
])

# Band 4 — 1ère/Terminale (ages 16-18). Full grammar range, no vocab limit.
BAND4_CURRICULUM = build_weekly_curriculum([
    {
        "theme": "Settling in — advanced review", "class_type": "Review",
        "a": {"focus": "self-presentation", "vocab": "background, goals, strengths, ambitions, personality, interests", "grammar": "Mixed tense review, advanced self-presentation."},
        "b": {"focus": "accuracy check", "vocab": "error, common mistakes, register, collocation, fluency, nuance", "grammar": "Error correction across all tenses."},
    },
    {
        "theme": "Regrets", "class_type": "Grammar Focus",
        "a": {"focus": "Conditional 3", "vocab": "regret, missed opportunity, consequence, mistake, if only, would have", "grammar": "Conditional 3: If I had studied, I would have passed."},
        "b": {"focus": "wish / if only", "vocab": "wish, if only, I should have, blame, apologise, forgive", "grammar": "I wish I had... If only I had... I should have..."},
    },
    {
        "theme": "Reporting in detail", "class_type": "Grammar Focus",
        "a": {"focus": "reported statements & questions", "vocab": "claimed, denied, announced, enquired, backshift, according to", "grammar": "Complex reported speech with backshift."},
        "b": {"focus": "reporting verbs", "vocab": "suggested, insisted, accused, promised, refused, warned", "grammar": "Reporting verbs + patterns: She accused him of lying. He refused to help."},
    },
    {
        "theme": "Formal suggestions", "class_type": "Grammar Focus",
        "a": {"focus": "the subjunctive", "vocab": "essential, vital, recommend, insist, demand, proposal", "grammar": "Subjunctive: It is essential that he be on time."},
        "b": {"focus": "formal register", "vocab": "furthermore, nevertheless, hereby, request, kindly, regarding", "grammar": "Formal register: I would be grateful if you could..."},
    },
    {
        "theme": "Debate & persuasion", "class_type": "Grammar Focus",
        "a": {"focus": "building an argument", "vocab": "claim, evidence, counter-argument, persuade, rebuttal, conclusion", "grammar": "Advanced connectors and mixed structures in argument."},
        "b": {"focus": "responding & rebutting", "vocab": "concede, dismiss, undermine, valid, flawed, nevertheless", "grammar": "Concession and contrast: Admittedly..., that said..."},
    },
    {
        "theme": "Media literacy", "class_type": "Grammar Focus",
        "a": {"focus": "analysing the news", "vocab": "bias, source, headline, propaganda, credible, fake news", "grammar": "Passive + reported speech in news analysis."},
        "b": {"focus": "writing a critique", "vocab": "objective, subjective, imply, reliability, editorial, sponsored", "grammar": "Hedging and evaluative language: It appears that... The article suggests..."},
    },
    {
        "theme": "Culture & literature", "class_type": "Grammar Focus",
        "a": {"focus": "analysing a text", "vocab": "theme, narrator, symbolism, plot, character, setting", "grammar": "Relative clauses + nuanced vocabulary for literary analysis."},
        "b": {"focus": "comparing texts", "vocab": "whereas, resemble, contrast, adaptation, genre, author", "grammar": "Comparison structures: While A..., B... / not only... but also..."},
    },
    {
        "theme": "Global issues & solutions", "class_type": "Grammar Focus",
        "a": {"focus": "problems & causes", "vocab": "climate change, inequality, poverty, migration, emissions, policy", "grammar": "Conditional 2 & 3 mixed: If we had acted sooner, we would not be facing..."},
        "b": {"focus": "proposing solutions", "vocab": "implement, legislation, sustainable, invest, renewable, awareness", "grammar": "Proposals: We ought to..., It is high time that we..."},
    },
    {
        "theme": "University & career", "class_type": "Grammar Focus",
        "a": {"focus": "university life", "vocab": "degree, lecture, application, scholarship, campus, specialise", "grammar": "Formal register, subjunctive practice."},
        "b": {"focus": "job applications", "vocab": "CV, cover letter, qualification, experience, candidate, interview", "grammar": "Formal writing: I am writing to apply for... I have experience in..."},
    },
    {
        "theme": "Ethics & society", "class_type": "Grammar Focus",
        "a": {"focus": "moral dilemmas", "vocab": "dilemma, right and wrong, justice, responsibility, consequence, principle", "grammar": "Abstract discussion with advanced connectors."},
        "b": {"focus": "social change", "vocab": "equality, discrimination, rights, tolerance, reform, movement", "grammar": "Expressing degrees of certainty: It could / must / can't be that..."},
    },
    {
        "theme": "Science & technology", "class_type": "Grammar Focus",
        "a": {"focus": "discoveries (passive)", "vocab": "invented, discovered, developed, experiment, breakthrough, research", "grammar": "Extended passive voice practice."},
        "b": {"focus": "AI & the future", "vocab": "artificial intelligence, automation, privacy, algorithm, ethical, data", "grammar": "Future forms and predictions: will be able to, is likely to, by 2050..."},
    },
    {
        "theme": "History & narrative", "class_type": "Grammar Focus",
        "a": {"focus": "narrating events", "vocab": "empire, revolution, war, treaty, era, leader", "grammar": "Mixed past tenses in historical narrative."},
        "b": {"focus": "reporting history", "vocab": "historians claim, is believed to, allegedly, source, archive, legacy", "grammar": "Reported speech + impersonal passive: It is said that... He is believed to..."},
    },
    {
        "theme": "Arts & opinions", "class_type": "Grammar Focus",
        "a": {"focus": "reviewing art", "vocab": "exhibition, masterpiece, critic, performance, composition, audience", "grammar": "Nuanced opinion language, all tenses."},
        "b": {"focus": "defending taste", "vocab": "subjective, appeal, provocative, refined, mainstream, taste", "grammar": "Evaluative structures: What strikes me is..., I find it..."},
    },
    {
        "theme": "Mock interview practice", "class_type": "Grammar Focus",
        "a": {"focus": "answering questions", "vocab": "strengths, weaknesses, motivation, achievement, teamwork, challenge", "grammar": "Full register range — formal oral practice."},
        "b": {"focus": "asking questions", "vocab": "opportunity, responsibilities, prospects, team, expectations, salary", "grammar": "Formal questions: Could you tell me...? I was wondering whether..."},
    },
    {
        "theme": "Comprehensive review", "class_type": "Review",
        "a": {"focus": "tenses & conditionals", "vocab": "review of the year's topics, all tenses, conditionals", "grammar": "Full grammar review: tenses and conditionals."},
        "b": {"focus": "passive, reported speech, subjunctive", "vocab": "review of the year's topics, passive, reporting, formal", "grammar": "Full grammar review: passive, reported speech, subjunctive."},
    },
    {
        "theme": "Bac exam preparation", "class_type": "Assessment",
        "a": {"focus": "mock oral", "vocab": "review of the year's topics, presentation, debate, document", "grammar": "Full mock exam — oral."},
        "b": {"focus": "mock written", "vocab": "review of the year's topics, essay, synthesis, comprehension", "grammar": "Full mock exam — written."},
    },
])

SCHOOL_CURRICULUM_BY_BAND = {0: BAND0_CURRICULUM, 1: CM1_CURRICULUM, 2: BAND2_CURRICULUM, 3: BAND3_CURRICULUM, 4: BAND4_CURRICULUM}

# CEFR hard constraints per band — ported from the local engine's
# BAND_CONSTRAINTS (index.html, 2026-09-18), injected into every AI prompt
# that generates student-facing content so the model can't quietly
# overestimate a class's level (the original bug: a band-2 class's script
# used second-conditional "What would happen if...?" throughout — grammar
# it hadn't been taught).
BAND_CONSTRAINTS = {
    0: {
        "label": "Pré-A1 / CP-CE2",
        "grammar_allowed": "to be (am/is/are), basic noun phrases, colours, numbers 1-20",
        "grammar_forbidden": "all verb tenses, negation with auxiliaries, questions",
        "max_vocab": 6,
        "vocab_note": "concrete objects only",
        # No cap on any band (2026-09-23, Kamal) — the sheet-count limit
        # was never the point; simplifying the English itself
        # (grammar_allowed/forbidden, max_vocab above) is what actually
        # helps French kids. A real CM1 (band 1) class came out with a
        # single sheet under the old max_sheets: 1 — too aggressive.
        "max_sheets": None,
        "instruction_max_words": None,
    },
    1: {
        "label": "A1 / CM1-CM2",
        "grammar_allowed": "Present Simple (I/you/he), can/can't, Have got, basic questions with Do/Does",
        "grammar_forbidden": "Present Continuous, past tenses, conditionals, passive",
        "max_vocab": 8,
        "vocab_note": "familiar topics (family, school, food, animals)",
        "max_sheets": None,
        "instruction_max_words": None,
    },
    2: {
        "label": "A2 / 6ème-4ème",
        "grammar_allowed": "Present Simple + Continuous, simple past (regular + top 10 irregular), comparatives, going to (future plans), basic modal verbs (must/should)",
        "grammar_forbidden": "Conditional 2 or 3, past continuous, passive voice, relative clauses",
        "max_vocab": 10,
        "vocab_note": "familiar everyday topics only",
        "max_sheets": None,
        "instruction_max_words": 8,
    },
    3: {
        "label": "B1 / 3ème-2nde",
        "grammar_allowed": "All past tenses, Conditional 1 and 2, passive voice, relative clauses",
        "grammar_forbidden": "Conditional 3, reported speech in complex forms, subjunctive",
        "max_vocab": 15,
        "vocab_note": None,
        "max_sheets": None,
        "instruction_max_words": None,
    },
    4: {
        "label": "B2 / 1ère-Terminale",
        "grammar_allowed": "All structures including Conditional 3, reported speech, subjunctive",
        "grammar_forbidden": None,
        "max_vocab": None,
        "vocab_note": None,
        "max_sheets": None,
        "instruction_max_words": None,
    },
}

# Adult general-English curriculum — CEFR-differentiated per level. `vocab`
# is an array, one entry per week within the block (block sizes: 7,7,5,6,7
# weeks — see MASTER_CURRICULUM). `grammar` stays one target for the whole
# block; `vocab` rotates every week. See curriculum_lookup.resolve_week_vocab.
ADULT_GENERAL_CURRICULUM = [
    {"block": 1, "level": "adult-a1", "theme": "Meeting people & daily life", "grammar": "Present simple: be/have, personal information", "vocab": [
        "hello, goodbye, my name is, nice to meet you",
        "jobs: teacher, doctor, engineer, student",
        "countries and nationalities: French, American, Japanese",
        "numbers 1-20, phone numbers, age",
        "family words: mother, father, brother, sister",
        "daily routine verbs: wake up, work, sleep",
        "days of the week, telling the time",
    ]},
    {"block": 1, "level": "adult-a2", "theme": "Past experiences & travel basics", "grammar": "Past simple: regular and irregular verbs", "vocab": [
        "transport: plane, train, car, bus",
        "airport and hotel words: check-in, luggage, reservation",
        "past time expressions: yesterday, last week, two years ago",
        "irregular past verbs: went, saw, took, had",
        "holiday activities: sightseeing, relaxing, exploring",
        "travel problems: delayed, lost, cancelled",
        "describing a trip: amazing, exhausting, unforgettable",
    ]},
    {"block": 1, "level": "adult-b1", "theme": "Life changes & routines", "grammar": "Present perfect vs past simple (experience vs finished time)", "vocab": [
        "life events: graduate, get married, move house",
        "frequency adverbs: always, usually, rarely, never",
        "daily/weekly routines: commute, exercise, unwind",
        "change verbs: change, improve, adapt, settle in",
        "time markers: since, for, just, already, yet",
        "personal achievements: promotion, qualification, milestone",
        "reflecting on the past: used to, look back on",
    ]},
    {"block": 1, "level": "adult-b2", "theme": "Storytelling & first impressions", "grammar": "Narrative tenses: past simple, past continuous, past perfect", "vocab": [
        "first impressions: striking, awkward, memorable",
        "narrative connectors: suddenly, meanwhile, eventually",
        "descriptive adjectives: vivid, chaotic, unexpected",
        "body language and tone: nervous, confident, hesitant",
        "scene-setting language: at that moment, in the background",
        "emotional reactions: astonished, relieved, embarrassed",
        "wrapping up a story: in the end, looking back",
    ]},
    {"block": 2, "level": "adult-a1", "theme": "Food, shopping & prices", "grammar": "can/can't, there is/are, basic questions", "vocab": [
        "food: bread, milk, eggs, fruit",
        "shops: supermarket, bakery, market, pharmacy",
        "prices and money: how much, expensive, cheap",
        "quantities: a lot of, some, a little",
        "containers: a bottle of, a bag of, a box of",
        "meals: breakfast, lunch, dinner, snack",
        "shopping requests: can I have, I'd like",
    ]},
    {"block": 2, "level": "adult-a2", "theme": "Directions & comparisons", "grammar": "Comparatives and superlatives, prepositions of place", "vocab": [
        "places in town: bank, station, park, library",
        "prepositions of place: next to, opposite, between",
        "giving directions: turn left, go straight, at the corner",
        "comparative adjectives: bigger, closer, cheaper",
        "superlative adjectives: the biggest, the nearest, the best",
        "transport around town: on foot, by bus, by bike",
        "asking for directions: excuse me, how do I get to",
    ]},
    {"block": 2, "level": "adult-b1", "theme": "Future plans & housing", "grammar": "going to / will, first conditional", "vocab": [
        "housing: rent, mortgage, flat, apartment",
        "rooms and features: spacious, furnished, balcony",
        "work plans: apply for, get promoted, change careers",
        "ambitions: hope to, plan to, aim to",
        "conditions and consequences: if, unless, as long as",
        "moving house: pack, move in, settle down",
        "talking about the future: eventually, in the long run",
    ]},
    {"block": 2, "level": "adult-b2", "theme": "Hypothetical situations & debate", "grammar": "Second conditional, agreeing and disagreeing", "vocab": [
        "opinion phrases: in my view, I'd argue that",
        "agreeing: absolutely, I couldn't agree more",
        "disagreeing: I see it differently, I'm not so sure",
        "hedging language: sort of, to some extent, arguably",
        "hypothetical situations: what if, imagine if, suppose",
        "weighing pros and cons: on the one hand, on balance",
        "concluding an argument: all things considered, ultimately",
    ]},
    {"block": 3, "level": "adult-a1", "theme": "Family & free time", "grammar": "Present continuous, possessive adjectives", "vocab": [
        "family members: mother, father, sister, brother, cousin",
        "possessive adjectives: my, your, his, her, our",
        "hobbies: reading, swimming, cooking, painting",
        "free time activities: watching TV, playing games",
        "present actions: is/are + verb-ing, right now",
    ]},
    {"block": 3, "level": "adult-a2", "theme": "Health & everyday advice", "grammar": "should / must / have to", "vocab": [
        "body parts: head, stomach, back, throat",
        "common illnesses: a cold, a headache, a fever",
        "giving advice: should, shouldn't, had better",
        "obligation: must, have to, need to",
        "at the pharmacy/doctor: prescription, appointment, symptoms",
    ]},
    {"block": 3, "level": "adult-b1", "theme": "Problems & giving advice", "grammar": "Modals of deduction and advice (should, might, must)", "vocab": [
        "everyday problems: run out of, break down, go wrong",
        "advice phrases: if I were you, why don't you",
        "deduction: must be, might be, can't be",
        "suggestions: how about, what about, I suggest",
        "resolving problems: sort out, deal with, fix",
    ]},
    {"block": 3, "level": "adult-b2", "theme": "Conditionals & negotiating solutions", "grammar": "First, second and third conditionals", "vocab": [
        "problem-solving verbs: tackle, address, resolve",
        "compromise language: meet halfway, find common ground",
        "real conditions: if + present, will + verb",
        "hypothetical conditions: if + past, would + verb",
        "past regrets: if + past perfect, would have",
    ]},
    {"block": 4, "level": "adult-a1", "theme": "Weather & simple plans", "grammar": "going to future, weather vocabulary", "vocab": [
        "weather words: sunny, rainy, cloudy, windy",
        "seasons: spring, summer, autumn, winter",
        "clothes for weather: coat, umbrella, sunglasses",
        "simple future plans: going to + verb",
        "weekend plans: going to visit, going to stay",
        "temperature and describing weather: hot, cold, mild, degrees",
    ]},
    {"block": 4, "level": "adult-a2", "theme": "Past continuous & storytelling", "grammar": "Past continuous vs past simple", "vocab": [
        "past continuous forms: was/were + verb-ing",
        "interrupted actions: while, when, at that moment",
        "story connectors: first, then, after that, finally",
        "simple story vocabulary: suddenly, luckily, unfortunately",
        "describing a scene: it was raining, everyone was",
        "retelling a story: so, in the end, that's why",
    ]},
    {"block": 4, "level": "adult-b1", "theme": "Comparing experiences & opinions", "grammar": "Comparative structures, linking words (although, however)", "vocab": [
        "opinion adjectives: interesting, boring, worthwhile, disappointing",
        "comparing experiences: more...than, less...than, as...as",
        "linking words: although, however, on the other hand",
        "giving reasons: because, since, due to",
        "contrasting ideas: whereas, while, in contrast",
        "summarising an opinion: overall, in short, to sum up",
    ]},
    {"block": 4, "level": "adult-b2", "theme": "Reported speech & current events", "grammar": "Reported speech: statements and questions", "vocab": [
        "news vocabulary: headline, report, coverage, source",
        "reporting verbs: say, tell, explain, mention",
        "reported statements: he said (that), she told me",
        "reported questions: he asked if, she wanted to know",
        "current affairs topics: economy, environment, technology",
        "discussing the news: according to, apparently, it's claimed that",
    ]},
    {"block": 5, "level": "adult-a1", "theme": "Review & simple self-introduction", "grammar": "Review of present simple/continuous and can", "vocab": [
        "review: greetings and personal information",
        "review: family and free time",
        "review: food and shopping",
        "review: weather and simple plans",
        "self-introduction: I am, I live, I like",
        "talking about ability: can, can't + verb",
        "end-of-year vocabulary: favourite, best memory, next year",
    ]},
    {"block": 5, "level": "adult-a2", "theme": "Review & simple past narrative", "grammar": "Review of past simple/continuous, simple storytelling", "vocab": [
        "narrative time expressions: once, one day, after that",
        "review: travel and directions vocabulary",
        "review: health and advice vocabulary",
        "review: past continuous storytelling vocabulary",
        "simple storytelling: beginning, middle, end",
        "describing feelings in a story: happy, surprised, worried",
        "sharing a memory: I remember, it was the time when",
    ]},
    {"block": 5, "level": "adult-b1", "theme": "Present perfect storytelling", "grammar": "Present perfect for experience (Have you ever...?)", "vocab": [
        "life experiences: have you ever, I've never",
        "achievements: accomplish, succeed, overcome",
        "review: future plans and housing vocabulary",
        "review: problems and advice vocabulary",
        "review: comparing experiences vocabulary",
        "bucket-list language: would like to, haven't...yet",
        "reflecting on a year: this year I've, so far I've",
    ]},
    {"block": 5, "level": "adult-b2", "theme": "Advanced storytelling, conditionals & open debate", "grammar": "Present perfect combined with conditionals", "vocab": [
        "abstract nouns: achievement, ambition, identity, perspective",
        "hypothetical vocabulary: were it not for, had I known",
        "review: hypothetical situations & debate vocabulary",
        "review: reported speech & news vocabulary",
        "open debate language: to what extent, it could be argued",
        "nuanced opinion language: admittedly, that said, granted",
        "closing reflections: looking ahead, in years to come",
    ]},
]

# Business English track — same per-week vocab rotation as
# ADULT_GENERAL_CURRICULUM above — grammar target holds for the whole
# block, vocab changes every week.
BUSINESS_CURRICULUM = [
    {"block": 1, "level": "biz-b1", "theme": "Introducing yourself & your company", "grammar": "Present simple for routines and facts", "vocab": [
        "set up, work for, job title",
        "be in charge of, department, team",
        "company facts: founded, headquartered, based in",
        "daily responsibilities: deal with, handle, manage",
        "introducing colleagues: this is, he/she works in",
        "company size: a small business, a multinational",
        "small talk at work: how's business, busy week",
    ]},
    {"block": 1, "level": "biz-b2", "theme": "Company structure & roles", "grammar": "Present simple/continuous for describing organisations, relative clauses", "vocab": [
        "run (a business), founder, CEO",
        "report to, line manager, direct report",
        "take over, take on, acquire",
        "org structure: hierarchy, subsidiary, headquarters",
        "relative clause connectors: who, which, that",
        "company roles: stakeholder, shareholder, board member",
        "describing change: restructure, reorganise, streamline",
    ]},
    {"block": 1, "level": "biz-c1", "theme": "Corporate culture & strategy", "grammar": "Passive voice for describing processes", "vocab": [
        "spin off, scale up, streamline",
        "corporate strategy: vision, mission, core values",
        "culture vocabulary: work ethic, inclusive, collaborative",
        "passive process language: is managed by, is overseen by",
        "growth vocabulary: expand, diversify, consolidate",
        "change management: drive change, embed, roll out",
        "strategic priorities: long-term goals, competitive edge",
    ]},
    {"block": 2, "level": "biz-b1", "theme": "Arranging meetings & simple emails", "grammar": "Future forms for arrangements (will/going to), polite requests", "vocab": [
        "set up (a meeting), schedule, arrange",
        "follow up, get back to, confirm",
        "email openers: I am writing to, further to",
        "email closers: looking forward to, best regards",
        "polite requests: could you, would you mind",
        "rescheduling: postpone, bring forward, push back",
        "meeting logistics: agenda, minutes, attendees",
    ]},
    {"block": 2, "level": "biz-b2", "theme": "Running meetings & correspondence", "grammar": "Modals for suggestions and polite disagreement", "vocab": [
        "carry out, put off, bring forward",
        "agenda language: item, action point, next steps",
        "suggestions: could we, why don't we, I suggest",
        "polite disagreement: I see your point, but; I'm not sure I agree",
        "correspondence phrases: as discussed, per our conversation",
        "chairing language: let's move on, shall we begin",
        "summarising a meeting: to sum up, action items",
    ]},
    {"block": 2, "level": "biz-c1", "theme": "Chairing meetings & diplomatic tone", "grammar": "Hedging and softening structures", "vocab": [
        "touch base, circle back, action point",
        "diplomatic phrasing: it might be worth considering",
        "hedging structures: it could be argued, to some extent",
        "softening disagreement: I take your point, however",
        "steering a meeting: let's park that, coming back to",
        "building consensus: broadly speaking, common ground",
        "closing diplomatically: I appreciate your input, moving forward",
    ]},
    {"block": 3, "level": "biz-b1", "theme": "Telephone basics", "grammar": "Present simple/continuous for phone routines, polite phrases", "vocab": [
        "put through, hold on, transfer the call",
        "phone greetings: speaking, this is, calling about",
        "get back to, call back, leave a message",
        "phone etiquette: could you repeat that, I didn't catch that",
        "ending a call: thanks for calling, talk soon",
    ]},
    {"block": 3, "level": "biz-b2", "theme": "Negotiating deals", "grammar": "Conditionals for proposals, modals for offers", "vocab": [
        "work out, come up with, propose",
        "meet halfway, reach an agreement, compromise",
        "making offers: we could offer, we'd be willing to",
        "conditional proposals: if you..., we would...",
        "closing a deal: shake on it, finalise the terms",
    ]},
    {"block": 3, "level": "biz-c1", "theme": "Advanced negotiation & persuasion", "grammar": "Complex conditionals, concession structures", "vocab": [
        "hammer out, thrash out, trade-off",
        "persuasive language: the key benefit is, what this means for you",
        "concession structures: while it's true that, granted",
        "complex conditionals: had we known, were it not for",
        "sealing an agreement: on that basis, we're aligned",
    ]},
    {"block": 4, "level": "biz-b1", "theme": "Simple presentations", "grammar": "Sequencing language (first, next, finally)", "vocab": [
        "point out, go through, move on to",
        "sequencing: first, next, after that, finally",
        "chart vocabulary: bar chart, pie chart, line graph",
        "describing data: increase, decrease, stay the same",
        "presentation openers: today I'll be talking about",
        "presentation closers: to conclude, thank you for listening",
    ]},
    {"block": 4, "level": "biz-b2", "theme": "Describing trends & giving opinions", "grammar": "Trend language (rise, fall, fluctuate), comparatives for data", "vocab": [
        "break down, roll out, bring up",
        "trend verbs: rise, fall, fluctuate, plateau",
        "trend adverbs: sharply, gradually, slightly",
        "comparatives for data: higher than, a slight increase on",
        "giving opinions on data: this suggests, it appears that",
        "forecasting: is expected to, is likely to",
    ]},
    {"block": 4, "level": "biz-c1", "theme": "Persuasive presentations & Q&A", "grammar": "Advanced rhetorical structures", "vocab": [
        "field a question, drill down, forecast",
        "rhetorical openers: imagine if, consider this",
        "persuasive structures: not only...but also, the real question is",
        "handling Q&A: that's a fair question, let me clarify",
        "deflecting difficult questions: I'll come back to that",
        "closing persuasively: the bottom line is, I urge you to",
    ]},
    {"block": 5, "level": "biz-b1", "theme": "Job interviews & career basics", "grammar": "Present perfect for experience, past simple for job history", "vocab": [
        "take on, apply for, look into",
        "job history: I worked as, I was responsible for",
        "experience: I have worked, I have managed",
        "interview phrases: tell me about yourself, why this role",
        "strengths and skills: I'm good at, I excel at",
        "career vocabulary: promotion, career change, career break",
        "ending an interview: thank you for your time, next steps",
    ]},
    {"block": 5, "level": "biz-b2", "theme": "Marketing & finance basics", "grammar": "Passive voice for processes, quantifiers for data", "vocab": [
        "cut back, branch out, budget",
        "marketing vocabulary: target audience, brand awareness, campaign",
        "finance vocabulary: revenue, profit, expenditure",
        "quantifiers for data: the majority of, a small proportion of",
        "passive process language: is allocated, is invested in",
        "marketing channels: social media, print, digital advertising",
        "review: presenting a budget or campaign",
    ]},
    {"block": 5, "level": "biz-c1", "theme": "Strategic marketing & financial reporting", "grammar": "Advanced passive/nominalisation for formal reports", "vocab": [
        "move up, ramp up, scale back",
        "financial reporting: quarterly results, year-on-year growth",
        "nominalisation: implementation, allocation, distribution",
        "formal passive: is projected to, has been forecast",
        "strategic marketing: positioning, differentiation, market share",
        "review: negotiation and persuasion vocabulary",
        "closing the year: annual review, outlook for next year",
    ]},
]

SKILL_OPTIONS = [
    {"key": "speaking", "label": "Speaking / talking"},
    {"key": "listening", "label": "Listening"},
    {"key": "reading", "label": "Reading"},
    {"key": "writing", "label": "Writing"},
]

EXERCISE_TYPES = [
    {"key": "gapfill", "label": "Gap fill"},
    {"key": "matching", "label": "Match the answers"},
    {"key": "spotmistake", "label": "Spot the mistake"},
    {"key": "multiplechoice", "label": "Multiple choice"},
    {"key": "truefalse", "label": "True or false"},
    {"key": "wordorder", "label": "Word order"},
    {"key": "guidedwriting", "label": "Guided writing"},
    {"key": "pictureqa", "label": "Picture-based questions"},
]

# "Special topic" — an optional one-off grammar focus a teacher can pick for
# any class, any week, overriding the normal weekly curriculum lookup.
# Available on all three tracks. Each topic has three complexity tiers so
# the same topic scales to the selected level — see
# curriculum_lookup.special_topic_tier for how a level maps to a tier.
SPECIAL_TOPICS = [
    {"key": "modals", "label": "Modal verbs", "theme": "Modal Verbs", "tiers": {
        "young": {"grammar": "can / can't for ability, and must / mustn't for simple classroom rules", "vocab": "can, can't, must, mustn't + everyday actions and classroom rules"},
        "mid": {"grammar": "can/could (ability, permission), must/have to (obligation), should (advice), mustn't vs don't have to (prohibition vs no obligation)", "vocab": "modal verbs of ability, obligation, and advice in everyday contexts"},
        "advanced": {"grammar": "the full modal range: may/might/could for possibility, must/can't for logical deduction, should have + past participle for past advice or regret", "vocab": "modal verbs of possibility, deduction, and hypothetical past advice"},
    }},
    {"key": "phrasalverbs", "label": "Phrasal verbs", "theme": "Phrasal Verbs", "tiers": {
        "young": {"grammar": "a handful of very common, literal phrasal verbs (get up, sit down, put on, take off)", "vocab": "phrasal verbs tied to daily routine and classroom actions"},
        "mid": {"grammar": "common separable and inseparable phrasal verbs in everyday and school/work contexts, with attention to word order for separable ones", "vocab": "high-frequency phrasal verbs for daily life, school, and simple work situations"},
        "advanced": {"grammar": "a wider range of phrasal verbs including less literal/idiomatic ones, three-word phrasal verbs, and register (informal vs formal alternatives)", "vocab": "phrasal verbs common in professional or nuanced everyday English, plus their more formal one-word equivalents"},
    }},
    {"key": "passive", "label": "Passive Voice", "theme": "Passive Voice", "tiers": {
        "young": {"grammar": "simple present passive only (is/are + past participle) for very concrete, familiar actions (The door is closed. The cake is made.)", "vocab": "simple everyday verbs that work well in the passive (make, close, clean, break)"},
        "mid": {"grammar": "passive voice across present simple, past simple, and going to/will future (be + past participle), and when to use passive vs active", "vocab": "process- and news-style verbs that commonly appear in the passive"},
        "advanced": {"grammar": "passive across a full range of tenses including present perfect and modals + passive (must be done, should have been sent), and passive reporting structures (It is said that...)", "vocab": "passive-voice-friendly vocabulary for reports, processes, and news"},
    }},
    {"key": "reportedspeech", "label": "Reported Speech", "theme": "Reported Speech", "tiers": {
        "young": {"grammar": "very simple reported statements in the present (She says (that) she likes... / He says he wants...) — no tense backshift needed yet", "vocab": "say and simple everyday statements about likes, wants, and feelings"},
        "mid": {"grammar": "reported statements and questions with tense backshift (present to past) and pronoun/time changes, plus say vs tell", "vocab": "reporting verbs: say, tell, ask, and everyday statement/question content"},
        "advanced": {"grammar": "reported statements, questions, and commands with full tense backshift, modal changes (will→would, can→could), and a range of reporting verbs (explain, suggest, admit, deny, promise)", "vocab": "a wider range of reporting verbs and the shifts in time/place expressions (today→that day, here→there)"},
    }},
    {"key": "conditionals", "label": "Conditionals", "theme": "Conditionals", "tiers": {
        "young": {"grammar": "zero conditional only, for simple facts and rules (If you heat ice, it melts. If it rains, we stay inside.)", "vocab": "simple cause-and-effect situations from daily life"},
        "mid": {"grammar": "zero and first conditional (real future possibilities: If it rains tomorrow, we will stay inside)", "vocab": "everyday plans and real future possibilities"},
        "advanced": {"grammar": "first, second, and third conditional (real future, hypothetical present/future, and hypothetical past), with mixed conditionals for higher levels", "vocab": "vocabulary for hypothetical and unreal situations, regrets, and imagined outcomes"},
    }},
    {"key": "relativeclauses", "label": "Relative Clauses", "theme": "Relative Clauses", "tiers": {
        "young": {"grammar": "very simple defining relative clauses with who and that only (The man who lives next door. The book that I like.)", "vocab": "simple people and object descriptions"},
        "mid": {"grammar": "defining relative clauses with who/which/that/whose, and when the relative pronoun can be dropped", "vocab": "descriptive vocabulary for people, places, and things"},
        "advanced": {"grammar": "defining and non-defining relative clauses (with comma intonation/punctuation), including whom and where/when as relative adverbs", "vocab": "more nuanced descriptive and linking vocabulary for extended descriptions"},
    }},
    {"key": "comparatives", "label": "Comparatives & Superlatives", "theme": "Comparatives & Superlatives", "tiers": {
        "young": {"grammar": "short adjective comparatives and superlatives only (big/bigger/biggest, small/smaller/smallest)", "vocab": "simple, familiar descriptive adjectives (big, small, fast, slow, tall, short)"},
        "mid": {"grammar": "comparative and superlative forms for short and long adjectives (more/most), plus as...as for equal comparison", "vocab": "a wider range of descriptive adjectives for people, places, and things"},
        "advanced": {"grammar": "comparative/superlative forms including irregulars, less/fewer, intensifiers (much, a lot, slightly) with comparatives, and nuanced equal/unequal comparison structures", "vocab": "precise, nuanced descriptive adjectives for comparison in professional or academic contexts"},
    }},
    {"key": "questionformation", "label": "Question Formation", "theme": "Question Formation", "tiers": {
        "young": {"grammar": "simple yes/no questions and Wh-questions with to be and simple present (What is this? Do you like...?)", "vocab": "basic question words: what, who, where, when"},
        "mid": {"grammar": "yes/no and Wh-questions across present/past simple and continuous, plus question words how much/how many/why", "vocab": "a fuller range of question words and everyday question contexts"},
        "advanced": {"grammar": "question tags, indirect/embedded questions (Could you tell me where...?), and subject vs object questions", "vocab": "polite/indirect question framing for professional and formal contexts"},
    }},
    {"key": "irregularverbs", "label": "Irregular Verbs", "theme": "Irregular Verbs", "tiers": {
        "young": {"grammar": "a few irregular present-tense and plural forms only (have → has, go → goes, do → does; child → children, man → men, foot → feet) — no past tenses", "vocab": "have/has, go/goes, do/does, child/children, man/men, foot/feet"},
        "mid": {"grammar": "the most common irregular verbs in the past simple (go–went, see–saw, eat–ate, have–had, make–made, take–took, get–got, give–gave, come–came, do–did), taught in small same-sound groups and practised in short sentences; past participles (went–gone) only if the class's level allows them", "vocab": "the top irregular verbs in three forms, grouped by sound pattern (buy–bought, bring–brought, think–thought)"},
        "advanced": {"grammar": "the full irregular verb table in all three forms (infinitive, past simple, past participle), with confusable pairs (lie/lay, rise/raise) and irregular verbs inside perfect tenses and the passive", "vocab": "irregular verbs in three forms, grouped by pattern, plus commonly confused pairs"},
    }},
    {"key": "vocabbuilding", "label": "Vocabulary Building", "theme": "Vocabulary Building", "tiers": {
        "young": {"grammar": "no new grammar — recycle the class's known structures while learning new words in small topic sets, using pictures, actions and games", "vocab": "a small set of new topic words (max 6), each linked to a picture or action"},
        "mid": {"grammar": "word families and word-building (noun/verb/adjective forms), common prefixes and suffixes (un-, re-, -ful, -less), synonyms and opposites, and guessing meaning from context", "vocab": "word families, prefixes/suffixes, synonyms/opposites and common collocations (make/do, take/have)"},
        "advanced": {"grammar": "advanced word formation, collocations, connotation (formal vs informal, positive vs negative), idioms and phrasal verbs, and choosing the most precise word", "vocab": "academic and idiomatic vocabulary, collocations, and register pairs"},
    }},
    {"key": "tensesrun", "label": "Tenses Run-through", "theme": "Tenses Run-through", "tiers": {
        "young": {"grammar": "a friendly run-through of only the structures this class already knows (to be, have got, can/can't, present simple), with quick contrasts between them and lots of speaking", "vocab": "high-frequency verbs already taught"},
        "mid": {"grammar": "a run-through of the tenses the class has met (present simple and continuous, past simple, going to; at B1 also past continuous and present perfect), using time lines and signal words (always, now, yesterday, tomorrow, already, ever) to choose the right one", "vocab": "time expressions and signal words for each tense"},
        "advanced": {"grammar": "a full run-through of every tense on one timeline (simple, continuous, perfect and perfect continuous, past perfect, future forms), with signal words, contrasts and error correction", "vocab": "time expressions, signal words and linking words for narrative and formal writing"},
    }},
    {"key": "mocktest", "label": "Mock Test", "theme": "Mock Test", "tiers": {
        "young": {"grammar": "a short, friendly check-up (no pressure): listen and tick, read and match, write short answers — using only the language this class has already learnt", "vocab": "the words and structures taught so far this term"},
        "mid": {"grammar": "an exam-style mock in the style of the school's tests / DELF A2–B1: listening, reading comprehension, short written expression and a short oral, all on grammar the class has already met, with timing and exam tips", "vocab": "exam instruction words (tick, circle, complete, underline) and the year's vocabulary"},
        "advanced": {"grammar": "a full exam-style mock (Bac / Cambridge style): listening, reading comprehension, opinion or argument writing, and an oral presentation, with timing, marking criteria and exam technique", "vocab": "exam task vocabulary, linking words and formal register"},
    }},
    {"key": "phonetics", "label": "Pronunciation & Phonetics", "theme": "Pronunciation & Phonetics", "tiers": {
        "young": {"grammar": "phonics: letter–sound links, short and long vowel sounds, and the sounds French children find hardest ('th', 'h', 'r'), through chants, minimal pairs and games", "vocab": "simple words that show one target sound (ship/sheep, this/three, hat/at)"},
        "mid": {"grammar": "sounds French speakers struggle with (/θ/ and /ð/, /h/, short vs long vowels, final consonants, -ed endings, silent letters), word stress and minimal pairs, with a first look at phonemic symbols", "vocab": "minimal pairs and word-stress patterns in everyday words"},
        "advanced": {"grammar": "the phonemic chart, connected speech (linking, weak forms, elision), sentence stress and intonation, and reducing a French accent in fluent speech", "vocab": "phonemic transcription, stress-timed rhythm and intonation patterns"},
    }},
]
