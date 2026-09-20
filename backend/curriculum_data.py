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
    rows = []
    week = 1
    for t in topics:
        span = t.get("weeks", 2)
        if span > 2:
            raise ValueError(f'Curriculum topic "{t["theme"]}" spans {span} weeks — max is 2')
        for _ in range(span):
            rows.append({
                "week": week,
                "theme": t["theme"],
                "vocab": t["vocab"],
                "grammar": t["grammar"],
                "class_type": t["class_type"],
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
    {"theme": "Hello & introductions", "vocab": "hello, goodbye, my name is, yes, no", "grammar": "Hello! My name is... What's your name?", "class_type": "Vocabulary Focus"},
    {"theme": "Colours", "vocab": "red, blue, yellow, green, black, white", "grammar": "It's + colour: It's red.", "class_type": "Vocabulary Focus"},
    {"theme": "Numbers 1-10", "vocab": "one to ten", "grammar": "Counting objects: How many? One, two...", "class_type": "Vocabulary Focus"},
    {"theme": "Classroom objects", "vocab": "pen, book, bag, chair, table, pencil", "grammar": "It's a...: It's a pen.", "class_type": "Vocabulary Focus"},
    {"theme": "Family", "vocab": "mum, dad, sister, brother, baby, family", "grammar": "This is my...: This is my mum.", "class_type": "Vocabulary Focus"},
    {"theme": "Pets & animals", "vocab": "cat, dog, bird, fish, rabbit, hamster", "grammar": "It's a...: It's a cat.", "class_type": "Vocabulary Focus"},
    {"theme": "Body parts", "vocab": "head, hand, foot, eye, ear, nose", "grammar": "It's my...: It's my hand.", "class_type": "Vocabulary Focus"},
    {"theme": "Fruit & food", "vocab": "apple, bread, milk, egg, banana, water", "grammar": "It's a/an...: It's an apple.", "class_type": "Vocabulary Focus"},
    {"theme": "Toys", "vocab": "ball, doll, kite, car, teddy bear, blocks", "grammar": "It's a...: It's a ball.", "class_type": "Vocabulary Focus"},
    {"theme": "Clothes", "vocab": "hat, shoes, coat, dress, t-shirt, socks", "grammar": "It's a/are...: It's a hat. They are shoes.", "class_type": "Vocabulary Focus"},
    {"theme": "Weather", "vocab": "sunny, rainy, cold, hot, windy, cloudy", "grammar": "It's + weather word: It's sunny.", "class_type": "Vocabulary Focus"},
    {"theme": "Shapes", "vocab": "circle, square, triangle, star, heart, box", "grammar": "It's a...: It's a circle.", "class_type": "Vocabulary Focus"},
    {"theme": "Numbers 11-20", "vocab": "eleven to twenty", "grammar": "Counting extension, How many?", "class_type": "Vocabulary Focus"},
    {"theme": "Farm animals", "vocab": "cow, sheep, horse, duck, pig, hen", "grammar": "It's a...: It's a cow.", "class_type": "Vocabulary Focus"},
    {"theme": "Transport", "vocab": "car, bus, train, bike, plane, boat", "grammar": "It's a...: It's a car.", "class_type": "Vocabulary Focus"},
    {"theme": "Review & end-of-year show", "vocab": "review of favourite words from the year", "grammar": "Review: It's a.../This is my.../My name is...", "class_type": "Review"},
])

# Band 1 — CM1 (ages 9-10, the year before CM2). Present Simple, have got,
# can/can't, Do/Does questions. Deliberately distinct progression from CM2
# (CM2 already has its own detailed year, one grade ahead).
CM1_CURRICULUM = build_weekly_curriculum([
    {"theme": "All about me", "vocab": "name, age, hello, nice to meet you", "grammar": "I am / My name is / I am nine.", "class_type": "Vocabulary Focus"},
    {"theme": "Family", "vocab": "mum, dad, brother, sister, grandma, grandpa", "grammar": "Have got: I've got a brother.", "class_type": "Grammar Focus"},
    {"theme": "School subjects", "vocab": "maths, English, art, sport, music, break", "grammar": "Do you like...? Yes I do / No I don't.", "class_type": "Grammar Focus"},
    {"theme": "Age & counting", "vocab": "numbers to 20, old, young, birthday", "grammar": "How old are you? I am nine.", "class_type": "Grammar Focus"},
    {"theme": "Pets & animals", "vocab": "dog, cat, rabbit, fish, hamster, bird", "grammar": "Have got: I've got a dog. He's got a cat.", "class_type": "Grammar Focus"},
    {"theme": "Daily routine", "vocab": "wake up, eat breakfast, go to school, sleep", "grammar": "Present Simple he/she: She wakes up at 7.", "class_type": "Grammar Focus"},
    {"theme": "Food & likes", "vocab": "pizza, chocolate, vegetables, fruit, like", "grammar": "Do you like...? Yes I do / No I don't.", "class_type": "Grammar Focus"},
    {"theme": "Sports & abilities", "vocab": "swim, run, jump, play football, ride a bike", "grammar": "Can/can't: I can swim. I can't fly.", "class_type": "Grammar Focus"},
    {"theme": "My house", "vocab": "bedroom, kitchen, garden, big, small", "grammar": "Have got: My house has got a garden.", "class_type": "Grammar Focus"},
    {"theme": "Hobbies", "vocab": "draw, read, dance, play games, watch TV", "grammar": "Present Simple: I play football on Saturdays.", "class_type": "Grammar Focus"},
    {"theme": "Clothes & weather", "vocab": "coat, hat, boots, cold, hot, rain", "grammar": "Present Simple: I wear a coat when it's cold.", "class_type": "Grammar Focus"},
    {"theme": "Jobs", "vocab": "teacher, doctor, farmer, works, every day", "grammar": "Present Simple -s: My dad is a teacher. He works...", "class_type": "Grammar Focus"},
    {"theme": "Time & schedule", "vocab": "o'clock, morning, afternoon, evening", "grammar": "Do/Does questions: What time do you wake up?", "class_type": "Grammar Focus"},
    {"theme": "Animal abilities", "vocab": "fly, swim, climb, run fast, jump high", "grammar": "Can/can't: Birds can fly. Fish can't walk.", "class_type": "Grammar Focus"},
    {"theme": "Free time", "vocab": "weekend, friends, park, games, fun", "grammar": "Present Simple review, mixed persons.", "class_type": "Review"},
    {"theme": "All about me — review", "vocab": "review of the year's topics", "grammar": "Full review: have got, can/can't, Present Simple.", "class_type": "Review"},
])

# Band 2 — 6e/5e/4e (ages 11-14, all share this band's grammar ceiling).
# Present Simple+Continuous, simple past, comparatives, going to, must/should.
# FORBIDDEN for this band: Conditional 2/3, past continuous, passive,
# relative clauses — so "going to" and "must/should" are as far as this
# group goes on future/obligation; the old flat block string that later
# pushed Present Perfect + Conditional 1 onto this group (band-3 content)
# is not carried over here.
BAND2_CURRICULUM = build_weekly_curriculum([
    {"theme": "Introductions & routines", "vocab": "introduce yourself, hobbies, school, family", "grammar": "Present Simple review: I go to school by bus.", "class_type": "Review"},
    {"theme": "Daily routines + frequency", "vocab": "always, usually, sometimes, never, routine", "grammar": "Present Simple + adverbs of frequency.", "class_type": "Grammar Focus"},
    {"theme": "What's happening now", "vocab": "right now, at the moment, look, listen", "grammar": "Present Continuous: What are you doing?", "class_type": "Grammar Focus"},
    {"theme": "Be/have & personal info", "vocab": "hungry, cold, tired, right, have got", "grammar": "Be/have traps: I am hungry (not I have hungry).", "class_type": "Grammar Focus"},
    {"theme": "Yesterday (regular verbs)", "vocab": "watched, played, walked, cooked, yesterday", "grammar": "Past Simple regular verbs.", "class_type": "Grammar Focus"},
    {"theme": "Yesterday (irregular verbs)", "vocab": "went, saw, ate, had, did, top 10 irregulars", "grammar": "Past Simple top 10 irregular verbs.", "class_type": "Grammar Focus"},
    {"theme": "School rules", "vocab": "must, mustn't, uniform, homework, allowed", "grammar": "Must/mustn't for obligation and rules.", "class_type": "Grammar Focus"},
    {"theme": "Comparing things", "vocab": "bigger, smaller, more interesting, than", "grammar": "Comparatives: bigger than, more interesting than.", "class_type": "Grammar Focus"},
    {"theme": "Future plans", "vocab": "going to, weekend, holiday, plan", "grammar": "Going to for future plans: I'm going to visit...", "class_type": "Grammar Focus"},
    {"theme": "Hobbies & free time", "vocab": "review of hobby vocabulary", "grammar": "Present Simple/Continuous contrast review.", "class_type": "Review"},
    {"theme": "Health & advice", "vocab": "should, shouldn't, healthy, tired, sleep", "grammar": "Should/shouldn't for advice.", "class_type": "Grammar Focus"},
    {"theme": "Past experiences", "vocab": "trip, holiday, last year, ago", "grammar": "Past Simple review, regular + irregular mixed.", "class_type": "Grammar Focus"},
    {"theme": "Weekend plans extension", "vocab": "more going-to practice, invitations", "grammar": "Going to — extended practice, questions.", "class_type": "Grammar Focus"},
    {"theme": "Rules & the environment", "vocab": "recycle, mustn't, should, protect", "grammar": "Must/should review in a new context.", "class_type": "Grammar Focus"},
    {"theme": "Storytelling", "vocab": "review of past-tense vocabulary", "grammar": "Past Simple full review — tell a short story.", "class_type": "Review"},
    {"theme": "End of year review", "vocab": "review of the year's topics", "grammar": "Mixed review — oral + written checkpoint.", "class_type": "Review"},
])

# Band 3 — 3e/2nde (ages 14-16). All past tenses, Conditional 1 & 2, passive,
# relative clauses. FORBIDDEN: Conditional 3, complex reported speech,
# subjunctive — simple reported speech (basic backshift) is fine here.
BAND3_CURRICULUM = build_weekly_curriculum([
    {"theme": "Settling in — past review", "vocab": "review of Past Simple from previous years", "grammar": "Past Simple review — narrating last summer.", "class_type": "Review"},
    {"theme": "In the middle of it", "vocab": "was/were + -ing, interrupted, while", "grammar": "Past Continuous: I was watching TV when...", "class_type": "Grammar Focus"},
    {"theme": "Life experiences", "vocab": "have been, have never, ever, already", "grammar": "Present Perfect for experience: I have been to...", "class_type": "Grammar Focus"},
    {"theme": "Real possibilities", "vocab": "if, will, possible, decision", "grammar": "Conditional 1: If it rains, I will stay home.", "class_type": "Grammar Focus"},
    {"theme": "Imagining things", "vocab": "if, would, imagine, hypothetical", "grammar": "Conditional 2: If I were rich, I would travel.", "class_type": "Grammar Focus"},
    {"theme": "What was done", "vocab": "was/were + past participle, by", "grammar": "Passive voice: The window was broken.", "class_type": "Grammar Focus"},
    {"theme": "Describing people & things", "vocab": "who, which, that, relative clause", "grammar": "Relative clauses: The man who lives next door...", "class_type": "Grammar Focus"},
    {"theme": "Telling a story", "vocab": "review of past-tense vocabulary", "grammar": "Mixed past tenses in narrative.", "class_type": "Grammar Focus"},
    {"theme": "Opinions & debate", "vocab": "in my opinion, I think, agree, disagree", "grammar": "Conditional 1 & 2 review in argument context.", "class_type": "Review"},
    {"theme": "Global issues", "vocab": "environment, pollution, solution, protect", "grammar": "Passive + relative clauses in context.", "class_type": "Grammar Focus"},
    {"theme": "Reporting what people say", "vocab": "said, told, that, reported", "grammar": "Simple reported speech: She said she was tired.", "class_type": "Grammar Focus"},
    {"theme": "News & media", "vocab": "headline, announced, confirmed, report", "grammar": "Passive review in news context.", "class_type": "Grammar Focus"},
    {"theme": "Ambitions & the future", "vocab": "hope, dream, would like to, career", "grammar": "Conditional 2 review — hypothetical futures.", "class_type": "Grammar Focus"},
    {"theme": "Culture & travel", "vocab": "review of travel/culture vocabulary", "grammar": "Relative clauses — extended practice.", "class_type": "Grammar Focus"},
    {"theme": "Mixed review", "vocab": "review of the year's topics", "grammar": "Mixed past tenses + conditionals review.", "class_type": "Review"},
    {"theme": "Exam preparation", "vocab": "review of the year's topics", "grammar": "Full mock exam — oral + written.", "class_type": "Assessment"},
])

# Band 4 — 1ère/Terminale (ages 16-18). Full grammar range, no vocab limit.
BAND4_CURRICULUM = build_weekly_curriculum([
    {"theme": "Settling in — advanced review", "vocab": "no fixed limit", "grammar": "Mixed tense review, advanced self-presentation.", "class_type": "Review"},
    {"theme": "Regrets", "vocab": "no fixed limit", "grammar": "Conditional 3: If I had studied, I would have passed.", "class_type": "Grammar Focus"},
    {"theme": "Reporting in detail", "vocab": "no fixed limit", "grammar": "Complex reported speech with backshift.", "class_type": "Grammar Focus"},
    {"theme": "Formal suggestions", "vocab": "no fixed limit", "grammar": "Subjunctive: It is essential that he be on time.", "class_type": "Grammar Focus"},
    {"theme": "Debate & persuasion", "vocab": "no fixed limit", "grammar": "Mixed advanced structures in argument.", "class_type": "Grammar Focus"},
    {"theme": "Media literacy", "vocab": "no fixed limit", "grammar": "Passive + reported speech in news analysis.", "class_type": "Grammar Focus"},
    {"theme": "Culture & literature", "vocab": "no fixed limit", "grammar": "Relative clauses + nuanced vocabulary.", "class_type": "Grammar Focus"},
    {"theme": "Global issues & solutions", "vocab": "no fixed limit", "grammar": "Conditional 2 & 3 mixed — proposing solutions.", "class_type": "Grammar Focus"},
    {"theme": "University & career", "vocab": "no fixed limit", "grammar": "Formal register, subjunctive practice.", "class_type": "Grammar Focus"},
    {"theme": "Ethics & society", "vocab": "no fixed limit", "grammar": "Abstract discussion, advanced connectors.", "class_type": "Grammar Focus"},
    {"theme": "Science & technology", "vocab": "no fixed limit", "grammar": "Extended passive voice practice.", "class_type": "Grammar Focus"},
    {"theme": "History & narrative", "vocab": "no fixed limit", "grammar": "Mixed past tenses + reported speech.", "class_type": "Grammar Focus"},
    {"theme": "Arts & opinions", "vocab": "no fixed limit", "grammar": "Nuanced opinion language, all tenses.", "class_type": "Grammar Focus"},
    {"theme": "Mock interview practice", "vocab": "no fixed limit", "grammar": "Full register range — formal oral practice.", "class_type": "Grammar Focus"},
    {"theme": "Comprehensive review", "vocab": "no fixed limit", "grammar": "Full grammar review, all structures.", "class_type": "Review"},
    {"theme": "Bac exam preparation", "vocab": "no fixed limit", "grammar": "Full mock exam — oral + written.", "class_type": "Assessment"},
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
        "max_sheets": 1,
        "instruction_max_words": None,
    },
    1: {
        "label": "A1 / CM1-CM2",
        "grammar_allowed": "Present Simple (I/you/he), can/can't, Have got, basic questions with Do/Does",
        "grammar_forbidden": "Present Continuous, past tenses, conditionals, passive",
        "max_vocab": 8,
        "vocab_note": "familiar topics (family, school, food, animals)",
        "max_sheets": 1,
        "instruction_max_words": None,
    },
    2: {
        "label": "A2 / 6ème-4ème",
        "grammar_allowed": "Present Simple + Continuous, simple past (regular + top 10 irregular), comparatives, going to (future plans), basic modal verbs (must/should)",
        "grammar_forbidden": "Conditional 2 or 3, past continuous, passive voice, relative clauses",
        "max_vocab": 10,
        "vocab_note": "familiar everyday topics only",
        "max_sheets": 2,
        "instruction_max_words": 8,
    },
    3: {
        "label": "B1 / 3ème-2nde",
        "grammar_allowed": "All past tenses, Conditional 1 and 2, passive voice, relative clauses",
        "grammar_forbidden": "Conditional 3, reported speech in complex forms, subjunctive",
        "max_vocab": 15,
        "vocab_note": None,
        "max_sheets": 2,
        "instruction_max_words": None,
    },
    4: {
        "label": "B2 / 1ère-Terminale",
        "grammar_allowed": "All structures including Conditional 3, reported speech, subjunctive",
        "grammar_forbidden": None,
        "max_vocab": None,
        "vocab_note": None,
        "max_sheets": 3,
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
]
