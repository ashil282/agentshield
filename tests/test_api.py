from fastapi.testclient import TestClient
from agentshield.api import app
def test_health(): assert TestClient(app).get("/health").json()["status"]=="ok"
def test_unknown_scenario_404(): assert TestClient(app).post("/api/v1/runs",json={"scenario_id":"missing"}).status_code==404
