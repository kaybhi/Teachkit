# Tests for the School Holidays feature: GET /api/school-week and PUT /api/profile holiday_zone
import requests
from conftest import BASE_URL


class TestAuthBasics:
    def test_login_shape(self, auth_token):
        assert isinstance(auth_token, str)

    def test_me_requires_token(self):
        r = requests.get(f"{BASE_URL}/api/auth/me", timeout=30)
        assert r.status_code == 401

    def test_school_week_requires_token(self):
        r = requests.get(f"{BASE_URL}/api/school-week", timeout=30)
        assert r.status_code == 401


class TestSchoolWeek:
    def test_school_week_shape(self, client):
        r = client.get(f"{BASE_URL}/api/school-week", timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        for k in ("current_week", "total_weeks_elapsed", "in_holiday", "holiday_name", "holidays"):
            assert k in d, f"missing {k} in {d}"
        assert isinstance(d["current_week"], int) and 1 <= d["current_week"] <= 32
        assert isinstance(d["total_weeks_elapsed"], int)
        assert isinstance(d["in_holiday"], bool)
        assert isinstance(d["holiday_name"], str)
        assert isinstance(d["holidays"], list)

    def test_zone_c_has_four_holidays(self, client):
        me = client.get(f"{BASE_URL}/api/auth/me", timeout=30).json()
        assert me.get("holiday_zone") == "C", f"expected zone C baseline, got {me.get('holiday_zone')}"
        d = client.get(f"{BASE_URL}/api/school-week", timeout=30).json()
        assert len(d["holidays"]) == 4, d["holidays"]
        names = [h["name"] for h in d["holidays"]]
        assert names == ["Toussaint", "Noël", "Hiver", "Printemps"], names
        for h in d["holidays"]:
            assert set(h.keys()) == {"name", "start", "end"}
        # Zone C specific winter break
        hiver = next(h for h in d["holidays"] if h["name"] == "Hiver")
        assert hiver["start"] == "2026-02-14", hiver

    def test_zone_switch_persists_and_changes_calendar(self, client):
        try:
            r = client.put(
                f"{BASE_URL}/api/profile",
                json={"holiday_zone": "A", "school_year_start": "2025-09-01"},
                timeout=30,
            )
            assert r.status_code == 200, r.text[:300]
            assert r.json()["holiday_zone"] == "A"
            assert r.json()["school_year_start"] == "2025-09-01"
            assert "_id" not in r.json() and "password_hash" not in r.json()

            me = client.get(f"{BASE_URL}/api/auth/me", timeout=30).json()
            assert me["holiday_zone"] == "A"

            d = client.get(f"{BASE_URL}/api/school-week", timeout=30).json()
            hiver = next(h for h in d["holidays"] if h["name"] == "Hiver")
            assert hiver["start"] == "2026-02-07", hiver
        finally:
            back = client.put(
                f"{BASE_URL}/api/profile",
                json={"holiday_zone": "C", "school_year_start": "2025-09-01"},
                timeout=30,
            )
            assert back.status_code == 200
            assert back.json()["holiday_zone"] == "C"

    def test_zone_none_returns_no_holidays(self, client):
        try:
            r = client.put(f"{BASE_URL}/api/profile", json={"holiday_zone": "none"}, timeout=30)
            assert r.status_code == 200
            d = client.get(f"{BASE_URL}/api/school-week", timeout=30).json()
            assert d["holidays"] == []
            assert d["in_holiday"] is False
        finally:
            client.put(f"{BASE_URL}/api/profile", json={"holiday_zone": "C"}, timeout=30)
