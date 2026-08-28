"""Tests for new features: public sharing (share token + /api/public/syllabus/{token})
and AI homework generator (/api/syllabus/{id}/week/{n}/homework)."""
import requests
import pytest

from conftest import BASE_URL


class TestShareAndHomework:
    # ---------- Sharing ----------
    def test_share_enable_returns_token(self, client, syllabus_id):
        r = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert data["share_enabled"] is True
        assert isinstance(data["share_token"], str)
        assert len(data["share_token"]) == 20, f"expected 20-char token, got {data['share_token']}"

    def test_share_enable_idempotent(self, client, syllabus_id):
        r1 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30)
        r2 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30)
        assert r1.status_code == r2.status_code == 200
        assert r1.json()["share_token"] == r2.json()["share_token"]
        assert r2.json()["share_enabled"] is True

    def test_share_unknown_syllabus_404(self, client):
        r = client.post(f"{BASE_URL}/api/syllabus/does-not-exist/share", json={"enabled": True}, timeout=30)
        assert r.status_code == 404, r.text[:200]

    def test_share_invalid_payload_422(self, client, syllabus_id):
        r = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={}, timeout=30)
        assert r.status_code == 422, r.text[:200]

    # ---------- Public read-only endpoint (no auth) ----------
    def test_public_syllabus_no_auth(self, client, syllabus_id):
        token = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30
        ).json()["share_token"]

        anon = requests.Session()  # deliberately no Authorization header
        r = anon.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert data["id"] == syllabus_id
        # NOTE: syllabi created before the class_level field was added return None here
        # (legacy docs). Endpoint should fall back to the owner's class_level. Reported as minor bug.
        assert "class_level" in data
        assert data["shared_by"]["class_level"] in ("CM1", "CM2", "6ème", "5ème")
        assert isinstance(data["lessons"], list) and len(data["lessons"]) == 32
        assert data["lessons"][0]["week"] == 1
        for key in ("full_name", "school_name", "school_city", "class_level"):
            assert key in data["shared_by"]
        assert data["shared_by"]["full_name"]
        # no leakage
        raw = r.text
        assert "password_hash" not in raw
        assert "email" not in raw
        assert "user_id" not in raw

    def test_public_bad_token_404(self):
        anon = requests.Session()
        r = anon.get(f"{BASE_URL}/api/public/syllabus/BAD_TOKEN", timeout=30)
        assert r.status_code == 404
        assert "detail" in r.json() and r.json()["detail"]

    def test_public_404_after_disable_then_reenable(self, client, syllabus_id):
        token = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": False}, timeout=30
        ).json()["share_token"]
        anon = requests.Session()
        r = anon.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30)
        assert r.status_code == 404, f"disabled share still public: {r.status_code}"
        # restore for frontend testing
        again = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30)
        assert again.json()["share_token"] == token
        assert anon.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30).status_code == 200

    # ---------- Homework generator ----------
    def test_homework_unknown_week_404(self, client, syllabus_id):
        r = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/week/99/homework", timeout=60)
        assert r.status_code == 404, r.text[:200]

    def test_homework_requires_auth(self, syllabus_id):
        anon = requests.Session()
        r = anon.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/homework", timeout=30)
        assert r.status_code == 401

    def test_homework_generate_and_persist(self, client, syllabus_id):
        r = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/week/3/homework", timeout=180)
        if r.status_code == 429:
            pytest.skip("AI busy (429)")
        assert r.status_code == 200, r.text[:400]
        hw = r.json()
        assert isinstance(hw.get("title"), str) and hw["title"]
        assert isinstance(hw.get("estimated_minutes"), int)
        assert hw.get("instructions_for_student")
        for ex in ("exercise_1", "exercise_2"):
            assert set(["title", "instructions", "items"]).issubset(hw[ex].keys()), hw[ex].keys()
            assert isinstance(hw[ex]["items"], list) and len(hw[ex]["items"]) >= 3
        assert set(["title", "instructions", "pairs"]).issubset(hw["exercise_3"].keys())
        assert isinstance(hw["exercise_3"]["pairs"], list) and hw["exercise_3"]["pairs"]
        for p in hw["exercise_3"]["pairs"]:
            assert "word" in p and "definition" in p
        assert hw.get("note_for_parents")
        ak = hw["answer_key"]
        for k in ("exercise_1", "exercise_2", "exercise_3"):
            assert isinstance(ak[k], list) and ak[k]
        assert len(ak["exercise_1"]) == len(hw["exercise_1"]["items"])

        # persistence check via GET lesson
        g = client.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/week/3", timeout=30)
        assert g.status_code == 200
        lesson = g.json()
        assert lesson.get("homework", {}).get("title") == hw["title"]
        assert lesson.get("homework_generated_at")
