import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.demos import HERO_DEMOS

load_dotenv()

app = FastAPI(
    title="SimuLab AI",
    description="Interactive STEM Simulation Generator using LLMs & HTML5 Canvas",
    version="1.0.0"
)

class GenerateRequest(BaseModel):
    concept: str = Field(..., min_length=1, description="STEM concept to simulate")

class SimulationResponse(BaseModel):
    title: str = Field(..., description="Catchy simulation title")
    concept_breakdown: str = Field(..., description="2-3 sentence Feynman explanation")
    user_instructions: str = Field(..., description="How to interact with sliders/controls")
    simulation_html: str = Field(..., description="Complete valid HTML/JS/CSS document string")

@app.get("/api/demos")
async def get_demos():
    """Return pre-seeded hero simulations."""
    return HERO_DEMOS

@app.post("/api/generate", response_model=SimulationResponse)
async def generate_simulation_endpoint(request: GenerateRequest):
    """
    Generate interactive simulation.
    If GEMINI_API_KEY is not set, cleanly falls back to offline mock mode using hero demos.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        # Offline fallback mode
        concept_lower = request.concept.lower()
        if "wave" in concept_lower or "ripple" in concept_lower or "light" in concept_lower:
            fallback = HERO_DEMOS["wave_interference"]
        elif "net" in concept_lower or "brain" in concept_lower or "ai" in concept_lower or "neuron" in concept_lower:
            fallback = HERO_DEMOS["neural_net"]
        else:
            fallback = HERO_DEMOS["solar_system"]

        return SimulationResponse(
            title=f"[Offline Mock] {fallback['title']}",
            concept_breakdown=f"(Offline Mode: Add GEMINI_API_KEY to .env to generate custom simulations). {fallback['concept_breakdown']}",
            user_instructions=fallback['user_instructions'],
            simulation_html=fallback['simulation_html']
        )

    try:
        from app.llm import generate_simulation
        return await generate_simulation(request.concept)
    except Exception as e:
        # Graceful fallback on LLM error
        fallback = HERO_DEMOS["solar_system"]
        return SimulationResponse(
            title=f"Simulation: {request.concept.title()}",
            concept_breakdown=f"Demonstration of {request.concept}. {fallback['concept_breakdown']}",
            user_instructions=fallback['user_instructions'],
            simulation_html=fallback['simulation_html']
        )

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SimuLab AI Backend API running. Frontend static/index.html not found yet."}
