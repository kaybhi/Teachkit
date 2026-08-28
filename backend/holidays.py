"""French national education vacation calendar by zone.
Dates are inclusive ISO strings.
Source: education.gouv.fr official calendar.
"""
from datetime import date, timedelta

# Zones by academy — abbreviated common list
# 2025-2026 school year
CALENDAR_2025_2026 = {
    "A": [  # Besançon, Bordeaux, Clermont, Dijon, Grenoble, Limoges, Lyon, Poitiers
        ("Toussaint", "2025-10-18", "2025-11-03"),
        ("Noël", "2025-12-20", "2026-01-05"),
        ("Hiver", "2026-02-07", "2026-02-23"),
        ("Printemps", "2026-04-04", "2026-04-20"),
    ],
    "B": [  # Aix-Marseille, Amiens, Caen, Lille, Nancy-Metz, Nantes, Nice, Orléans-Tours, Reims, Rennes, Rouen, Strasbourg
        ("Toussaint", "2025-10-18", "2025-11-03"),
        ("Noël", "2025-12-20", "2026-01-05"),
        ("Hiver", "2026-02-21", "2026-03-09"),
        ("Printemps", "2026-04-18", "2026-05-04"),
    ],
    "C": [  # Créteil, Montpellier, Paris, Toulouse, Versailles
        ("Toussaint", "2025-10-18", "2025-11-03"),
        ("Noël", "2025-12-20", "2026-01-05"),
        ("Hiver", "2026-02-14", "2026-03-02"),
        ("Printemps", "2026-04-11", "2026-04-27"),
    ],
}

# 2026-2027 school year
CALENDAR_2026_2027 = {
    "A": [
        ("Toussaint", "2026-10-17", "2026-11-02"),
        ("Noël", "2026-12-19", "2027-01-04"),
        ("Hiver", "2027-02-06", "2027-02-22"),
        ("Printemps", "2027-04-03", "2027-04-19"),
    ],
    "B": [
        ("Toussaint", "2026-10-17", "2026-11-02"),
        ("Noël", "2026-12-19", "2027-01-04"),
        ("Hiver", "2027-02-20", "2027-03-08"),
        ("Printemps", "2027-04-17", "2027-05-03"),
    ],
    "C": [
        ("Toussaint", "2026-10-17", "2026-11-02"),
        ("Noël", "2026-12-19", "2027-01-04"),
        ("Hiver", "2027-02-13", "2027-03-01"),
        ("Printemps", "2027-04-10", "2027-04-26"),
    ],
}

ALL_YEARS = {"2025": CALENDAR_2025_2026, "2026": CALENDAR_2026_2027}


def _parse(s: str) -> date:
    return date.fromisoformat(s)


def get_holidays_for_year(school_year_start: str, zone: str) -> list:
    """Return list of {name, start, end} vacation windows for the given year & zone."""
    if not zone or zone == "none":
        return []
    year_key = school_year_start[:4] if school_year_start else "2025"
    cal = ALL_YEARS.get(year_key) or ALL_YEARS["2025"]
    zone_data = cal.get(zone.upper()) or []
    return [{"name": n, "start": s, "end": e} for (n, s, e) in zone_data]


def compute_current_school_week(school_year_start: str, zone: str) -> dict:
    """Compute the current school week (1-32), skipping vacation weeks entirely.
    Returns {current_week, total_weeks_elapsed, in_holiday, holiday_name}.
    """
    if school_year_start:
        start = _parse(school_year_start)
    else:
        today = date.today()
        year = today.year if today.month >= 8 else today.year - 1
        start = date(year, 9, 1)

    today = date.today()
    holidays = get_holidays_for_year(school_year_start or f"{start.year}-09-01", zone)

    if today < start:
        return {"current_week": 1, "total_weeks_elapsed": 0, "in_holiday": False, "holiday_name": ""}

    # Check if today is in a holiday window
    in_holiday = False
    holiday_name = ""
    for h in holidays:
        if _parse(h["start"]) <= today <= _parse(h["end"]):
            in_holiday = True
            holiday_name = h["name"]
            break

    # Count school days (Mon-Fri) from start to today, excluding holiday windows
    holiday_ranges = [(_parse(h["start"]), _parse(h["end"])) for h in holidays]

    def in_holiday_range(d):
        return any(a <= d <= b for a, b in holiday_ranges)

    school_days = 0
    d = start
    while d <= today:
        if d.weekday() < 5 and not in_holiday_range(d):  # Mon-Fri, not in holiday
            school_days += 1
        d += timedelta(days=1)

    # 5 school days = 1 week
    current_week = max(1, min(32, (school_days + 4) // 5))
    return {
        "current_week": current_week,
        "total_weeks_elapsed": school_days // 5,
        "in_holiday": in_holiday,
        "holiday_name": holiday_name,
    }
