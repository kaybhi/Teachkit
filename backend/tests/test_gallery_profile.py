"""Tests for new features: profile family_emails, share listed_in_gallery, public gallery."""
import requests
import pytest

from conftest import BASE_URL


# ---------- PUT /api/profile family_emails ----------
class TestFamilyEmails:
    def test_profile_accepts_and_persists_family_emails(self, client):
        emails = ["alice.parent@school.fr", "bob.parent@school.fr"]
        r = client.put(f"{BASE_URL}/api/profile", json={"family_emails": emails}, timeout=30)
        assert r.status_code == 200, r.text[:300]
        body = r.json()
        assert body.get("family_emails") == emails
        assert "password_hash" not in body
        assert "_id" not in body

        me = client.get(f"{BASE_URL}/api/auth/me", timeout=30)
        assert me.status_code == 200
        mbody = me.json()
        assert isinstance(mbody.get("family_emails"), list)
        assert mbody["family_emails"] == emails

    def test_profile_empty_family_emails_list(self, client):
        r = client.put(f"{BASE_URL}/api/profile", json={"family_emails": []}, timeout=30)
        assert r.status_code == 200, r.text[:300]
        # empty list is falsy-but-not-None; must still persist
        assert r.json().get("family_emails") == []
        me = client.get(f"{BASE_URL}/api/auth/me", timeout=30).json()
        assert me.get("family_emails") == []
        # restore
        emails = ["alice.parent@school.fr", "bob.parent@school.fr"]
        client.put(f"{BASE_URL}/api/profile", json={"family_emails": emails}, timeout=30)
        assert client.get(f"{BASE_URL}/api/auth/me", timeout=30).json()["family_emails"] == emails

    def test_profile_requires_auth(self):
        r = requests.put(f"{BASE_URL}/api/profile", json={"family_emails": []}, timeout=30)
        assert r.status_code == 401


# ---------- GET /api/public/gallery ----------
class TestPublicGallery:
    def test_gallery_no_auth_required_and_shape(self, client, syllabus_id):
        # ensure listed
        s = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share",
                        json={"enabled": True, "listed_in_gallery": True}, timeout=30)
        assert s.status_code == 200, s.text[:300]
        token = s.json()["share_token"]
        assert s.json()["listed_in_gallery"] is True

        r = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30)
        assert r.status_code == 200, r.text[:300]
        items = r.json()
        assert isinstance(items, list)
        assert len(items) >= 1
        tokens = [i["share_token"] for i in items]
        assert token in tokens
        item = next(i for i in items if i["share_token"] == token)
        for key in ["share_token", "class_level", "lesson_count", "created_at", "teacher"]:
            assert key in item, f"missing {key}"
        assert isinstance(item["lesson_count"], int) and item["lesson_count"] > 0
        assert set(item["teacher"].keys()) == {"full_name", "school_name", "school_city"}

    def test_gallery_leaks_no_sensitive_data(self):
        r = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30)
        assert r.status_code == 200
        raw = r.text.lower()
        for banned in ["password", "password_hash", "email", "user_id", "_id", "@"]:
            assert banned not in raw, f"gallery response leaks '{banned}'"

    def test_unlisting_removes_from_gallery(self, client, syllabus_id):
        before = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30).json()
        s = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share",
                        json={"enabled": True, "listed_in_gallery": False}, timeout=30)
        assert s.status_code == 200
        assert s.json()["listed_in_gallery"] is False
        token = s.json()["share_token"]

        after = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30).json()
        assert len(after) == len(before) - 1
        assert token not in [i["share_token"] for i in after]

        # public share link still works even when unlisted
        pub = requests.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30)
        assert pub.status_code == 200
        assert "lessons" in pub.json()

        # re-enable listing
        s2 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share",
                         json={"enabled": True, "listed_in_gallery": True}, timeout=30)
        assert s2.status_code == 200 and s2.json()["listed_in_gallery"] is True
        again = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30).json()
        assert token in [i["share_token"] for i in again]

    def test_share_disabled_hides_from_gallery(self, client, syllabus_id):
        s = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share",
                        json={"enabled": False}, timeout=30)
        assert s.status_code == 200
        token = s.json()["share_token"]
        items = requests.get(f"{BASE_URL}/api/public/gallery", timeout=30).json()
        assert token not in [i["share_token"] for i in items]
        assert requests.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30).status_code == 404
        # restore
        s2 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share",
                         json={"enabled": True, "listed_in_gallery": True}, timeout=30)
        assert s2.status_code == 200

    def test_share_toggle_requires_auth(self, syllabus_id):
        r = requests.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/share", json={"enabled": True}, timeout=30)
        assert r.status_code == 401

    def test_share_invalid_syllabus(self, client):
        r = client.post(f"{BASE_URL}/api/syllabus/does-not-exist/share", json={"enabled": True}, timeout=30)
        assert r.status_code == 404


# ---------- Regression: dashboard stats source data ----------
class TestStatsSourceData:
    def test_active_syllabus_lessons_shape(self, client):
        r = client.get(f"{BASE_URL}/api/syllabus/active", timeout=30)
        assert r.status_code == 200
        doc = r.json()
        lessons = doc["lessons"]
        assert len(lessons) == 32
        packed = sum(1 for l in lessons if l.get("pack"))
        hw = sum(1 for l in lessons if l.get("homework"))
        print(f"active syllabus {doc['id']}: packed={packed} homework={hw}")
        assert hw >= 1, "expected at least one homework for stats test"
        assert all("week" in l and "title" in l for l in lessons)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
