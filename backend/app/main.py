import os
import uuid
from functools import cache

import psycopg
from fastapi import FastAPI
from mangum import Mangum
from pydantic import AwareDatetime, BaseModel, Field

app = FastAPI(title="Tomo API")


@cache
def init_db():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS sessions ("
            "id uuid PRIMARY KEY, started_at timestamptz NOT NULL, duration_sec int NOT NULL)"
        )


def connect():
    init_db()
    return psycopg.connect(os.environ["DATABASE_URL"])


class SessionIn(BaseModel):
    started_at: AwareDatetime
    duration_sec: int = Field(ge=0, le=24 * 3600)


class Session(SessionIn):
    id: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/sessions")
def list_sessions() -> list[Session]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, started_at, duration_sec FROM sessions ORDER BY started_at DESC"
        ).fetchall()
    return [Session(id=str(id), started_at=at, duration_sec=sec) for id, at, sec in rows]


@app.post("/api/sessions", status_code=201)
def create_session(session_in: SessionIn) -> Session:
    session = Session(id=str(uuid.uuid4()), **session_in.model_dump())
    with connect() as conn:
        conn.execute(
            "INSERT INTO sessions (id, started_at, duration_sec) VALUES (%s, %s, %s)",
            (session.id, session.started_at, session.duration_sec),
        )
    return session


# AWS Lambda entry point
handler = Mangum(app, lifespan="off")
