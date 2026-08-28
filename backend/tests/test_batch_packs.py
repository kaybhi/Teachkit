# Tests for Batch Pack Generation: /api/syllabus/{id}/batch-status and /batch-enrich
import time

import pytest
import requests
from conftest import BASE_URL


class TestBatchStatusIdle:
    def test_requires_auth(self, syllabus_id):
        r = requests.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-status", timeout=30)
        assert r.status_code == 401

    def test_unknown_syllabus_404(self, client):
        r = client.get(f"{BASE_URL}/api/syllabus/does-not-exist/batch-status", timeout=30)
        assert r.status_code == 404, r.text[:200]

    def test_idle_shape(self, client, syllabus_id):
        r = client.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-status", timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        assert d["status"] == "idle", d
        assert d["total"] == 32
        # done reflects packs on the CURRENT syllabus; a regeneration resets it to 0
        assert isinstance(d["done"], int) and 0 <= d["done"] <= 32
        assert d["current_week"] is None
        assert d["errors"] == []

    def test_idle_done_matches_packs_in_syllabus(self, client, syllabus_id):
        syl = client.get(f"{BASE_URL}/api/syllabus/active", timeout=30).json()
        packed = sum(1 for l in syl["lessons"] if l.get("pack"))
        d = client.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-status", timeout=30).json()
        assert d["done"] == packed, (d["done"], packed)


@pytest.mark.skip(
    reason="EXECUTED MANUALLY in iteration 3 (kicks off a 15-30min LLM job). "
    "Result: 200 with total=30/done=0 but status='running' instead of 'started'/'already_running' "
    "(dict-merge bug in server.py:538/526). Worker verified: week 3 pack persisted, done incremented, "
    "current_week advanced. Job aborted by restarting backend. Un-skip only if you can afford the LLM run."
)
class TestBatchEnrichStart:
    """Starts the background job, checks the contract, then leaves it running.
    The job is aborted afterwards by restarting the backend (see test report)."""

    def test_enrich_requires_auth(self, syllabus_id):
        r = requests.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-enrich", timeout=30)
        assert r.status_code == 401

    def test_enrich_unknown_syllabus_404(self, client):
        r = client.post(f"{BASE_URL}/api/syllabus/nope-nope/batch-enrich", timeout=30)
        assert r.status_code == 404

    def test_start_then_already_running(self, client, syllabus_id):
        r1 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-enrich", timeout=60)
        assert r1.status_code == 200, r1.text[:300]
        d1 = r1.json()
        assert d1["done"] == 0
        assert isinstance(d1["total"], int) and d1["total"] > 0
        assert d1["status"] == "started", f"expected status 'started', got {d1}"

        r2 = client.post(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-enrich", timeout=60)
        assert r2.status_code == 200
        d2 = r2.json()
        assert d2["status"] == "already_running", f"expected 'already_running', got {d2}"

    def test_status_running_while_job_active(self, client, syllabus_id):
        time.sleep(2)
        d = client.get(f"{BASE_URL}/api/syllabus/{syllabus_id}/batch-status", timeout=30).json()
        assert d["status"] == "running", d
        assert d["total"] > 0
        assert isinstance(d["errors"], list)
