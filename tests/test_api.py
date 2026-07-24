import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_demos():
    response = client.get("/api/demos")
    assert response.status_code == 200
    data = response.json()
    assert "solar_system" in data
    assert "neural_net" in data
    assert "wave_interference" in data
    assert "simulation_html" in data["solar_system"]

def test_generate_offline_fallback():
    response = client.post("/api/generate", json={"concept": "quantum entanglement"})
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "concept_breakdown" in data
    assert "user_instructions" in data
    assert "simulation_html" in data
    assert "<canvas" in data["simulation_html"].lower()
