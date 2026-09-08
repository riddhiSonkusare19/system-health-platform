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


def test_metrics_endpoint(client):
    resp = client.get("/metrics")

    assert resp.status_code == 200
    assert "app_cpu_usage_percent" in resp.get_data(as_text=True)