import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.demos import HERO_DEMOS
from app.llm import generate_simulation, SimulationResponse

load_dotenv()

app = FastAPI(
    title="SimuLab AI",
    description="Unlimited Interactive STEM & Mathematics Simulation Generator using LLMs & HTML5 Canvas",
    version="3.0.0"
)

class GenerateRequest(BaseModel):
    concept: str = Field(..., min_length=1, description="Any STEM, Math, or scientific concept to simulate")

@app.get("/api/demos")
async def get_demos():
    """Return pre-seeded hero simulations."""
    return HERO_DEMOS

@app.post("/api/generate", response_model=SimulationResponse)
async def generate_simulation_endpoint(request: GenerateRequest):
    """
    Dynamically generate an interactive Canvas 2D simulation for ANY requested topic.
    Uses LLM generation with fallback to domain-specific procedural simulation generation.
    """
    try:
        return await generate_simulation(request.concept)
    except Exception as e:
        from app.llm import generate_procedural_simulation
        return generate_procedural_simulation(request.concept)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SimuLab AI Backend API running."}
