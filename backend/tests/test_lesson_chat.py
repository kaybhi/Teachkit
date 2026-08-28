"""Tests for the new lesson chat endpoint + regression on existing endpoints."""
import requests
from conftest import BASE_URL


# ---------- module: lesson chat ----------
class TestLessonChat:
    def test_chat_requires_auth(self, syllabus_id):
        r = requests.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/chat",
            json={"message": "hello", "history": []}, timeout=30,
        )
        assert r.status_code in (401, 403), f"expected 401/403 got {r.status_code}"

    def test_chat_unknown_syllabus_404(self, client):
        r = client.post(
            f"{BASE_URL}/api/syllabus/does-not-exist-1234/week/1/chat",
            json={"message": "hello", "history": []}, timeout=60,
        )
        assert r.status_code == 404, r.text[:300]
        assert "not found" in r.json()["detail"].lower()

    def test_chat_unknown_week_404(self, client, syllabus_id):
        r = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/999/chat",
            json={"message": "hello", "history": []}, timeout=60,
        )
        assert r.status_code == 404, r.text[:300]
        assert "week" in r.json()["detail"].lower()

    def test_chat_basic_response(self, client, syllabus_id):
        r = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/chat",
            json={"message": "Give me a 3-minute warmer for this lesson.", "history": []},
            timeout=120,
        )
        assert r.status_code == 200, r.text[:500]
        body = r.json()
        assert set(body.keys()) == {"response"}, body.keys()
        txt = body["response"]
        assert isinstance(txt, str)
        assert 30 <= len(txt) <= 1500, f"len={len(txt)}: {txt[:200]}"
        assert "You (coach)" not in txt

    def test_chat_with_history_is_coherent(self, client, syllabus_id):
        history = [
            {"role": "user", "content": "What is the grammar focus of this lesson?"},
            {"role": "assistant", "content": "The focus is on the target grammar for week 1."},
        ]
        r = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/chat",
            json={"message": "Now level that down for a weaker pupil.", "history": history},
            timeout=120,
        )
        assert r.status_code == 200, r.text[:500]
        txt = r.json()["response"]
        assert 30 <= len(txt) <= 1500, f"len={len(txt)}"

    def test_chat_validation_missing_message(self, client, syllabus_id):
        r = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/chat", json={"history": []}, timeout=60,
        )
        assert r.status_code == 422, r.status_code

    def test_chat_empty_message(self, client, syllabus_id):
        r = client.post(
            f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1/chat",
            json={"message": "   ", "history": []}, timeout=120,
        )
        # Should not 500; ideally 422/400 for empty input
        assert r.status_code != 500, r.text[:300]


# ---------- module: regression on existing endpoints ----------
class TestRegression:
    def test_school_week(self, client):
        r = client.get(f"{BASE_URL}/api/school-week", timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        assert isinstance(d.get("current_week"), int)
        assert "in_holiday" in d

    def test_public_gallery(self):
        r = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30)
        assert r.status_code == 200, r.text[:300]
        assert isinstance(r.json(), list)

    def test_homework_exists(self, client, syllabus_id):
        r = client.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/week/1", timeout=30)
        assert r.status_code == 200, r.text[:300]
        lesson = r.json()
        assert "_id" not in lesson
        assert lesson.get("homework"), "week 1 homework missing (expected seeded)"
        assert lesson.get("pack"), "week 1 teacher pack missing (expected seeded)"

    def test_profile_family_emails(self, client):
        r = client.get(f"{BASE_URL}/api/auth/me", timeout=30)
        assert r.status_code == 200, r.text[:300]
        prof = r.json()
        assert "_id" not in prof
        if not prof.get("family_emails"):
            up = client.put(
                f"{BASE_URL}/api/profile",
                json={"family_emails": ["alice.parent@school.fr", "bob.parent@school.fr"]},
                timeout=30,
            )
            assert up.status_code == 200, up.text[:300]
            again = client.get(f"{BASE_URL}/api/auth/me", timeout=30)
            assert len(again.json()["family_emails"]) == 2
