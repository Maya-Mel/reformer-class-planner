from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_unknown_level_is_rejected():
    response = client.post("/class", json={"level": "Beginner"})
    assert response.status_code == 400

def test_unknown_condition_is_rejected():
    response = client.post("/class", json={"level": "beginner", "conditions": ["knee injury"]})
    assert response.status_code == 400