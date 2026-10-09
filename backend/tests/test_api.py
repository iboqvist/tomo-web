import os

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.main import app, init_db


@pytest.fixture
def client():
    init_db()
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("TRUNCATE sessions")
    yield TestClient(app)


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_sessions_newest_first(client):
    client.post("/api/sessions", json={"started_at": "2026-09-30T08:00:00Z", "duration_sec": 1500})
    client.post("/api/sessions", json={"started_at": "2026-09-30T09:00:00Z", "duration_sec": 600})
    assert [s["duration_sec"] for s in client.get("/api/sessions").json()] == [600, 1500]


def test_rejects_invalid_session(client):
    response = client.post(
        "/api/sessions", json={"started_at": "2026-09-30T08:00:00Z", "duration_sec": -1}
    )
    assert response.status_code == 422
