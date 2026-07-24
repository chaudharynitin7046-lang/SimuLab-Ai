import pytest
import json
from unittest.mock import patch, MagicMock
from app.llm import SimulationResponse, generate_simulation

def test_simulation_response_model():
    valid_payload = {
        "title": "Double Pendulum Chaos",
        "concept_breakdown": "Chaotic motion sensitive to initial conditions.",
        "user_instructions": "Move sliders to set pendulum lengths.",
        "simulation_html": "<!DOCTYPE html><html><body><canvas></canvas></body></html>"
    }
    model = SimulationResponse(**valid_payload)
    assert model.title == "Double Pendulum Chaos"
    assert "<canvas" in model.simulation_html

@patch.dict("os.environ", {"GEMINI_API_KEY": "fake_test_key"})
@patch("google.generativeai.GenerativeModel")
@pytest.mark.asyncio
async def test_generate_simulation_mock_success(mock_model_cls):
    mock_model_instance = MagicMock()
    mock_model_cls.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "title": "Quantum Wavepacket Dispersion",
        "concept_breakdown": "Wavepacket spreading over time.",
        "user_instructions": "Adjust mass slider.",
        "simulation_html": "<!DOCTYPE html><html><body><canvas></canvas></body></html>"
    })
    mock_model_instance.generate_content.return_value = mock_response

    result = await generate_simulation("quantum wavepacket")
    assert isinstance(result, SimulationResponse)
    assert result.title == "Quantum Wavepacket Dispersion"

@patch.dict("os.environ", {"GEMINI_API_KEY": "fake_test_key"})
@patch("google.generativeai.GenerativeModel")
@pytest.mark.asyncio
async def test_generate_simulation_retry_healing(mock_model_cls):
    mock_model_instance = MagicMock()
    mock_model_cls.return_value = mock_model_instance

    # First attempt fails with invalid JSON, second attempt succeeds
    bad_response = MagicMock()
    bad_response.text = "INVALID JSON STRING"

    good_response = MagicMock()
    good_response.text = json.dumps({
        "title": "Heat Conduction 2D",
        "concept_breakdown": "Fourier law heat dissipation.",
        "user_instructions": "Adjust conductivity.",
        "simulation_html": "<!DOCTYPE html><html><body><canvas></canvas></body></html>"
    })

    mock_model_instance.generate_content.side_effect = [bad_response, good_response]

    result = await generate_simulation("heat conduction")
    assert result.title == "Heat Conduction 2D"
    assert mock_model_instance.generate_content.call_count == 2
