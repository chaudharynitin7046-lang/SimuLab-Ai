import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_demos():
    response = client.get("/api/demos")
    assert response.status_code == 200
    data = response.json()
    assert "fourier_series" in data
    assert "lorenz_attractor" in data
    assert "solar_system" in data
    assert "neural_net" in data
    assert "wave_interference" in data
    assert "simulation_html" in data["fourier_series"]

def test_generate_unlimited_any_topic():
    # Test generation for arbitrary custom topics
    for topic in ["quantum entanglement", "photosynthesis light reaction", "sorting algorithm quicksort"]:
        response = client.post("/api/generate", json={"concept": topic})
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "concept_breakdown" in data
        assert "user_instructions" in data
        assert "simulation_html" in data
        assert "<canvas" in data["simulation_html"].lower()
