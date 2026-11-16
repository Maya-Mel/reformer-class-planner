from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_unknown_level_is_rejected():
    response = client.post("/class", json={"level": "Beginner"})
    assert response.status_code == 400

def test_unknown_condition_is_rejected():
    response = client.post("/class", json={"level": "beginner", "conditions": ["knee injury"]})
    assert response.status_code == 400

def test_valid_request_sends_fields_to_agent(monkeypatch):
    def fake_run_agent(request):
        return f"FAKE CLASS FOR: {request}"

    monkeypatch.setattr("api.run_agent", fake_run_agent)

    response = client.post("/class", json={
        "level": "beginner",
        "conditions": ["pregnancy"],
        "focus_areas": ["glutes"],
    })

    assert response.status_code == 200
    assert "pregnancy" in response.json()["lesson"]
    assert "glutes" in response.json()["lesson"]