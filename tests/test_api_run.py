from fastapi.testclient import TestClient
from agentshield.api import app

def test_create_run_returns_expected_contract():
    response = TestClient(app).post("/api/v1/runs", json={"scenario_id": "direct-ignore"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario_id"] == "direct-ignore"
    assert payload["observed"] == "blocked"
    assert payload["passed"] is True
