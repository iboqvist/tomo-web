import os
import uuid
from functools import cache
from operator import attrgetter

import boto3
from fastapi import FastAPI
from mangum import Mangum
from pydantic import AwareDatetime, BaseModel, Field

app = FastAPI(title="Tomo API")


@cache
def table():
    # AWS_ENDPOINT_URL_DYNAMODB points boto3 at DynamoDB Local during development
    return boto3.resource("dynamodb").Table(os.getenv("TABLE_NAME", "tomo"))


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
    sessions = map(Session.model_validate, table().scan()["Items"])
    return sorted(sessions, key=attrgetter("started_at"), reverse=True)


@app.post("/api/sessions", status_code=201)
def create_session(session_in: SessionIn) -> Session:
    session = Session(id=str(uuid.uuid4()), **session_in.model_dump())
    table().put_item(Item=session.model_dump(mode="json"))
    return session


# AWS Lambda entry point
handler = Mangum(app, lifespan="off")
