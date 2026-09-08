import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as c:
        yield c


def test_health_returns_up(client):
    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "UP"


def test_version_present(client):
    resp = client.get("/version")

    assert resp.status_code == 200
    assert "version" in resp.get_json()