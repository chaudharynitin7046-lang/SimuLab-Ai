import os
import json
import logging
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class SimulationResponse(BaseModel):
    title: str = Field(..., description="Catchy simulation title")
    concept_breakdown: str = Field(..., description="2-3 sentence Feynman explanation")
    user_instructions: str = Field(..., description="How to interact with sliders/controls")
    simulation_html: str = Field(..., description="Complete valid HTML/JS/CSS document string")

SYSTEM_PROMPT = """You are a Staff-Level Canvas HTML5 Engineer, Mathematician, and STEM Educator for SimuLab AI.
Your task is to generate a fully self-contained HTML5 Canvas 2D interactive simulation for the user's requested STEM or Mathematics concept (algebra, calculus, trigonometry, linear algebra, geometry, chaos theory, Fourier analysis, physics, etc.).

STRICT ENGINEERING & MATHEMATICAL LAWS:
1. ZERO EXTERNAL DEPENDENCIES: Output MUST use 100% vanilla JavaScript Canvas API and inline CSS inside a single HTML string. NEVER include <script src="...">, Three.js, p5.js, Tailwind CDN, or external fonts inside simulation_html.
2. MATHEMATICAL CONCEPT BREAKDOWN: Include formal LaTeX mathematical formulas inside `concept_breakdown` using standard $inline_math$ or $$display_math$$ syntax (e.g., $f(x) = \\sin(x)$, $F = G \\frac{m_1 m_2}{r^2}$).
3. MANDATORY INTERACTIVITY: Every simulation MUST include at least 2 real-time UI sliders (<input type="range">) or toggles wired directly into the animation loop so changing them updates the canvas rendering immediately.
4. ANIMATION CLEANUP & ERROR BOUNDARY:
   - Use requestAnimationFrame for the loop.
   - Attach window.addEventListener('beforeunload', ...) to cancelAnimationFrame.
   - Attach window.onerror handler that calls: window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
5. DARK MODE AESTHETIC: Background color must be #0f172a (dark slate), text #f8fafc, accent colors cyan (#06b6d4), emerald (#10b981), violet (#8b5cf6), or rose (#f43f5e).
6. RESPONSIVE: Canvas must auto-resize to fill its container window width/height.

Respond ONLY with valid JSON conforming to the requested schema.
"""

async def generate_simulation(concept: str) -> SimulationResponse:
    """
    Generate an interactive STEM simulation using Google Generative AI (Gemini).
    Includes a self-healing retry loop (up to 2 retries) on JSON or schema parsing failures.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not configured.")

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    # Use gemini-1.5-flash or available model
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )

    prompt = f"STEM Concept to Simulate: {concept}"
    max_retries = 2
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
            if last_error:
                full_prompt += f"\n\nPREVIOUS ATTEMPT FAILED WITH ERROR:\n{last_error}\nPlease fix the JSON formatting and schema compliance strictly."

            response = model.generate_content(full_prompt)
            raw_text = response.text.strip()
            
            # Clean potential markdown wrapping if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            parsed_data = json.loads(raw_text)
            validated_response = SimulationResponse(**parsed_data)
            return validated_response

        except (json.JSONDecodeError, ValidationError, Exception) as e:
            logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
            last_error = str(e)
            if attempt == max_retries:
                raise RuntimeError(f"Failed to generate valid simulation after {max_retries + 1} attempts. Last error: {e}")
