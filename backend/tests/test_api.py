import os
import uuid

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


def test_list_is_empty_initially(client):
    response = client.get("/api/sessions")
    assert response.status_code == 200
    assert response.json() == []


def test_create_session(client):
    response = client.post(
        "/api/sessions", json={"started_at": "2026-09-30T08:00:00Z", "duration_sec": 300}
    )
    assert response.status_code == 201

    session = response.json()
    assert session.get("started_at") == "2026-09-30T08:00:00Z"
    assert session.get("duration_sec") == 300
    assert session.get("id") is not None
    assert uuid.UUID(session.get("id"))


@pytest.mark.parametrize("json", [{"started_at": "2026-09-30T08:00:00Z"}, {"duration_sec": 300}])
def test_missing_session_field_should_reject(client, json):
    response = client.post("/api/sessions", json=json)
    assert response.status_code == 422


def test_sessions_newest_first(client):
    client.post("/api/sessions", json={"started_at": "2026-09-30T08:00:00Z", "duration_sec": 1500})
    client.post("/api/sessions", json={"started_at": "2026-09-30T09:00:00Z", "duration_sec": 600})
    assert [s["duration_sec"] for s in client.get("/api/sessions").json()] == [600, 1500]


@pytest.mark.parametrize("duration,status_code", [(-1, 422), (0, 201), (86400, 201), (86401, 422)])
def test_duration_bounds(client, duration, status_code):
    response = client.post(
        "/api/sessions", json={"started_at": "2026-09-30T08:00:00Z", "duration_sec": duration}
    )
    assert response.status_code == status_code
