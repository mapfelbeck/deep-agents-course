"""API smoke tests. The agent generation is stubbed so tests run offline."""

import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
# Avoid the sandbox SOCKS proxy tripping the OpenAI client during import.
for _var in ("ALL_PROXY", "all_proxy", "HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"):
    os.environ.pop(_var, None)

import pytest
from fastapi.testclient import TestClient

from app import routers
from app.main import app


@pytest.fixture
def client(monkeypatch):
    # Stub the background generation so no model/network call happens.
    def fake_generation(interview_id, job_id, role, resume_path):
        from app.db import SessionLocal
        from app.models_db import Interview, Job

        db = SessionLocal()
        try:
            interview = db.get(Interview, interview_id)
            job = db.get(Job, job_id)
            interview.sheet_md = "## Section\n\n1. First question?\n"
            interview.resume_md = None
            interview.status = "ready"
            job.status = "done"
            db.commit()
        finally:
            db.close()

    monkeypatch.setattr(routers.interviews, "run_generation", fake_generation)
    return TestClient(app)


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_roles_are_listed(client):
    res = client.get("/api/roles")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_list_and_notes_flow(client):
    created = client.post("/api/interviews", data={"role": "Software Engineering"})
    assert created.status_code == 201
    ids = created.json()
    interview_id = ids["interview_id"]

    # Background task ran the stub; interview should be ready.
    detail = client.get(f"/api/interviews/{interview_id}").json()
    assert detail["status"] == "ready"
    assert "First question" in detail["sheet_md"]

    # Notes autosave round-trip.
    saved = client.put(
        f"/api/interviews/{interview_id}/notes",
        json={"notes_md": "<!-- note:a0 -->\nlooks strong\n<!-- /note -->"},
    )
    assert saved.status_code == 200
    fetched = client.get(f"/api/interviews/{interview_id}/notes").json()
    assert "looks strong" in fetched["notes_md"]

    # Appears in history.
    listing = client.get("/api/interviews").json()
    assert any(item["id"] == interview_id for item in listing)


def test_rejects_bad_upload_type(client):
    res = client.post(
        "/api/interviews",
        data={"role": "Software Engineering"},
        files={"resume": ("resume.txt", b"hello", "text/plain")},
    )
    assert res.status_code == 400
