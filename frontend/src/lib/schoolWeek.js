// Compute the current school-year week (1-32) given a school year start date (ISO string).
// If school_year_start is empty, default to Sept 1 of the current year (northern hemisphere school year).
export function getCurrentSchoolWeek(schoolYearStart) {
  let start;
  if (schoolYearStart) {
    start = new Date(schoolYearStart);
  } else {
    const now = new Date();
    // If we're past July, start = Sept 1 of this year, else Sept 1 of last year.
    const year = now.getMonth() >= 7 ? now.getFullYear() : now.getFullYear() - 1;
    start = new Date(year, 8, 1); // Sept 1
  }
  const now = new Date();
  const diffDays = Math.floor((now - start) / (1000 * 60 * 60 * 24));
  const week = Math.floor(diffDays / 7) + 1;
  if (week < 1) return 1;
  if (week > 32) return 32;
  return week;
}
