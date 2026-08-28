// Class-type / level tables — ported from the validated lesson-planner
// engine (index.html SCHOOL_LEVELS/ADULT_LEVELS/BUSINESS_LEVELS, lines
// 442-471 as of 2026-08-14). Mirrors backend/curriculum_data.py — keep the
// two in sync if either changes.

export const SCHOOL_LEVELS = [
  { id: "cp", label: "CP", cefr: "Pré-A1" },
  { id: "ce1", label: "CE1", cefr: "Pré-A1" },
  { id: "ce2", label: "CE2", cefr: "Pré-A1" },
  { id: "cm1", label: "CM1", cefr: "A1" },
  { id: "cm2", label: "CM2", cefr: "A1+" },
  { id: "6e", label: "6ème", cefr: "A1/A2" },
  { id: "5e", label: "5ème", cefr: "A2" },
  { id: "4e", label: "4ème", cefr: "A2+" },
  { id: "3e", label: "3ème", cefr: "B1" },
  { id: "2nde", label: "2nde", cefr: "B1+" },
  { id: "1ere", label: "1ère", cefr: "B2" },
  { id: "term", label: "Terminale", cefr: "B2+" },
];

export const ADULT_LEVELS = [
  { id: "adult-a1", label: "A1", cefr: "A1" },
  { id: "adult-a2", label: "A2", cefr: "A2" },
  { id: "adult-b1", label: "B1", cefr: "B1" },
  { id: "adult-b2", label: "B2", cefr: "B2" },
];

export const BUSINESS_LEVELS = [
  { id: "biz-b1", label: "B1", cefr: "B1" },
  { id: "biz-b2", label: "B2", cefr: "B2" },
  { id: "biz-c1", label: "C1", cefr: "C1" },
];

export const CLASS_TYPES = [
  { key: "school", label: "School (CP–Terminale)", levels: SCHOOL_LEVELS },
  { key: "adult", label: "Adult general English", levels: ADULT_LEVELS },
  { key: "business", label: "Business English", levels: BUSINESS_LEVELS },
];

export function levelsForClassType(classType) {
  return CLASS_TYPES.find((c) => c.key === classType)?.levels || SCHOOL_LEVELS;
}

export function defaultLevelId(classType) {
  return levelsForClassType(classType)[0]?.id || "cm2";
}
