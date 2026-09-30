import os

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

os.environ |= {
    "AWS_ACCESS_KEY_ID": "test",
    "AWS_SECRET_ACCESS_KEY": "test",
    "AWS_DEFAULT_REGION": "eu-north-1",
    "TABLE_NAME": "tomo-test",
}
os.environ.pop("AWS_ENDPOINT_URL_DYNAMODB", None)

from app.main import app, table  # noqa: E402


@pytest.fixture
def client():
    with mock_aws():
        table.cache_clear()
        boto3.client("dynamodb").create_table(
            TableName="tomo-test",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield TestClient(app)
    table.cache_clear()


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
