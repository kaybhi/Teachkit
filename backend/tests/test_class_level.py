"""Curriculum preset regression: /api/syllabus/generate must scale CEFR/vocab by the
user's class_level. NOTE: this test regenerates the active syllabus (destructive) — run last."""
import pytest

from conftest import BASE_URL


def _set_level(client, level):
    r = client.put(f"{BASE_URL}/api/profile", json={"class_level": level}, timeout=30)
    assert r.status_code == 200, r.text[:300]
    assert r.json()["class_level"] == level
    assert "password_hash" not in r.json()


def _generate(client):
    r = client.post(f"{BASE_URL}/api/syllabus/generate", json={
        "priorities": ["Speaking", "Listening", "Reading", "Writing"],
        "activity_types": ["Games", "Pair work", "Songs"],
    }, timeout=60)
    assert r.status_code == 200, r.text[:300]
    doc = r.json()
    assert len(doc["lessons"]) == 32
    return doc


class TestClassLevelPresets:
    def test_baseline_cm2(self, client):
        _set_level(client, "CM2")
        doc = _generate(client)
        assert doc["class_level"] == "CM2"
        l0 = doc["lessons"][0]
        assert l0["cefr_level"] == "A1"
        assert len(l0["vocabulary"]) == 10
        assert doc["share_enabled"] is False
        assert len(doc["share_token"]) == 20

    def test_cm1_scales_down(self, client):
        _set_level(client, "CM1")
        doc = _generate(client)
        assert doc["class_level"] == "CM1"
        l0 = doc["lessons"][0]
        assert l0["cefr_level"] == "A1"
        assert len(l0["vocabulary"]) < 10, "CM1 vocabulary should be shorter than baseline"
        # A1 everywhere for CM1
        assert all(l["cefr_level"] == "A1" for l in doc["lessons"])

    def test_5eme_scales_up(self, client):
        _set_level(client, "5ème")
        doc = _generate(client)
        assert doc["class_level"] == "5ème"
        l0 = doc["lessons"][0]
        assert "A2" in l0["cefr_level"], f"expected A2 for 5ème, got {l0['cefr_level']}"
        assert len(l0["vocabulary"]) == 10
        # persisted class_level surfaces on GET active
        got = client.get(f"{BASE_URL}/api/syllabus/active", timeout=30).json()
        assert got["class_level"] == "5ème"
        assert got["id"] == doc["id"]

    def test_6eme_keeps_template_levels(self, client):
        _set_level(client, "6ème")
        doc = _generate(client)
        assert doc["lessons"][7]["cefr_level"] == "A1-A2"
        assert doc["lessons"][9]["cefr_level"] == "A2"

    def test_restore_cm2_and_share(self, client):
        """Leave the account in a usable state for the next agent."""
        _set_level(client, "CM2")
        doc = _generate(client)
        r = client.post(f"{BASE_URL}/api/syllabus/{doc['id']}/share", json={"enabled": True}, timeout=30)
        assert r.status_code == 200
        token = r.json()["share_token"]
        import requests
        assert requests.get(f"{BASE_URL}/api/public/syllabus/{token}", timeout=30).status_code == 200
        print(f"\nRESTORED: syllabus={doc['id']} share_token={token} class_level=CM2 (packs/homework wiped)")
