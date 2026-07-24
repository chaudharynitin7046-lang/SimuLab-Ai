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

SYSTEM_PROMPT = """You are a Staff-Level Canvas HTML5 Engineer, Scientist, and STEM Educator for SimuLab AI.
Your task is to generate a fully self-contained HTML5 Canvas 2D interactive simulation for ANY requested user topic across Mathematics, Physics, Chemistry, Biology, Computer Science, Astronomy, Engineering, or Economics.

STRICT ENGINEERING & MATHEMATICAL LAWS:
1. ZERO EXTERNAL DEPENDENCIES: Output MUST use 100% vanilla JavaScript Canvas API and inline CSS inside a single HTML string. NEVER include <script src="...">, Three.js, p5.js, Tailwind CDN, or external fonts inside simulation_html.
2. MATHEMATICAL CONCEPT BREAKDOWN: Include formal LaTeX mathematical formulas inside `concept_breakdown` using standard $inline_math$ or $$display_math$$ syntax (e.g., $f(x) = \\sin(x)$, $F = G \\frac{m_1 m_2}{r^2}$, $\\frac{dx}{dt} = f(x)$).
3. MANDATORY INTERACTIVITY: Every simulation MUST include at least 2 real-time UI sliders (<input type="range">) or toggles wired directly into the animation loop so changing them updates the canvas rendering immediately.
4. ANIMATION CLEANUP & ERROR BOUNDARY:
   - Use requestAnimationFrame for the loop.
   - Attach window.addEventListener('beforeunload', ...) to cancelAnimationFrame.
   - Attach window.onerror handler that calls: window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
5. DARK MODE AESTHETIC: Background color must be #0f172a (dark slate), text #f8fafc, accent colors cyan (#06b6d4), emerald (#10b981), violet (#8b5cf6), or rose (#f43f5e).
6. RESPONSIVE: Canvas must auto-resize to fill its container window width/height.

Respond ONLY with valid JSON conforming to the requested schema.
"""

def generate_procedural_simulation(concept: str) -> SimulationResponse:
    """
    Procedural simulation fallback for ANY topic when LLM API is unavailable.
    Generates a dynamic, interactive HTML5 Canvas simulation tailored to the requested topic.
    """
    concept_clean = concept.strip().title()
    concept_lower = concept.lower()

    if any(k in concept_lower for k in ["math", "calculus", "function", "graph", "sine", "cosine", "trig", "fourier", "fractal", "integral", "derivative"]):
        title = f"Mathematical Function & Vector Field: {concept_clean}"
        breakdown = f"Visualizing mathematical properties of ${concept_clean}$. Functions map continuous inputs to outputs through harmonic transformations: $$f(x, t) = A \\sin(k x - \\omega t) + B \\cos(n x)$$ The canvas plots real-time wave functions and vector derivatives dynamically."
        instructions = "Adjust Amplitude ($A$) and Frequency ($\\\\omega$) sliders to modify function curvature and phase velocity live."
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{concept_clean} Math Simulation</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}
    #controls {{ display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }}
    .control-group {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }}
    label {{ color: #94a3b8; font-weight: 500; }}
    input[type="range"] {{ accent-color: #06b6d4; cursor: pointer; }}
    span.val {{ color: #06b6d4; font-family: monospace; min-width: 2.5rem; }}
    #canvas-container {{ flex: 1; position: relative; width: 100%; height: 100%; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="amp">Amplitude (A):</label>
      <input type="range" id="amp" min="10" max="120" step="2" value="60">
      <span id="ampVal" class="val">60px</span>
    </div>
    <div class="control-group">
      <label for="freq">Frequency (ω):</label>
      <input type="range" id="freq" min="0.5" max="5" step="0.1" value="2.0">
      <span id="freqVal" class="val">2.0</span>
    </div>
  </div>
  <div id="canvas-container"><canvas id="simCanvas"></canvas></div>
  <script>
    (function() {{
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const ampInput = document.getElementById('amp');
      const freqInput = document.getElementById('freq');
      const ampVal = document.getElementById('ampVal');
      const freqVal = document.getElementById('freqVal');
      let width, height, animId, time = 0;

      ampInput.addEventListener('input', e => ampVal.textContent = e.target.value + 'px');
      freqInput.addEventListener('input', e => freqVal.textContent = parseFloat(e.target.value).toFixed(1));

      function resize() {{
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
      }}
      window.addEventListener('resize', resize);
      resize();

      function render() {{
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const A = parseFloat(ampInput.value);
        const w = parseFloat(freqInput.value);
        time += 0.03 * w;

        // Draw Coordinate Grid
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.stroke();

        // Draw Mathematical Function
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 3;
        ctx.beginPath();
        for (let x = 0; x < width; x += 2) {{
          const normX = (x - width / 2) * 0.02;
          const y = height / 2 - Math.sin(normX * w + time) * A - Math.cos(normX * 2.5) * (A * 0.4);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }}
        ctx.stroke();

        // Draw Vector Tangents
        ctx.fillStyle = '#10b981';
        for (let x = 50; x < width; x += 60) {{
          const normX = (x - width / 2) * 0.02;
          const y = height / 2 - Math.sin(normX * w + time) * A - Math.cos(normX * 2.5) * (A * 0.4);
          ctx.beginPath();
          ctx.arc(x, y, 4, 0, Math.PI * 2);
          ctx.fill();
        }}

        animId = requestAnimationFrame(render);
      }}
      animId = requestAnimationFrame(render);
      window.addEventListener('beforeunload', () => animId && cancelAnimationFrame(animId));
      window.onerror = (m, u, l) => window.parent.postMessage({{ type: 'SIM_ERROR', error: m, line: l }}, '*');
    }})();
  </script>
</body>
</html>"""

    elif any(k in concept_lower for k in ["chem", "molecule", "atom", "reaction", "gas", "thermo", "heat", "kinetic"]):
        title = f"Molecular Dynamics & Kinetics: {concept_clean}"
        breakdown = f"Interactive simulation of ${concept_clean}$. Particle velocities follow the Maxwell-Boltzmann kinetic distribution: $$E_k = \\frac{3}{2} k_B T$$ Collisions exchange momentum according to conservation laws."
        instructions = "Adjust Temperature ($T$) and Molecular Pressure sliders to observe particle collision frequency."
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{concept_clean} Molecular Simulation</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}
    #controls {{ display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }}
    .control-group {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }}
    label {{ color: #94a3b8; font-weight: 500; }}
    input[type="range"] {{ accent-color: #f43f5e; cursor: pointer; }}
    span.val {{ color: #f43f5e; font-family: monospace; min-width: 2.5rem; }}
    #canvas-container {{ flex: 1; position: relative; width: 100%; height: 100%; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="temp">Temperature (T):</label>
      <input type="range" id="temp" min="1" max="5" step="0.2" value="2.0">
      <span id="tempVal" class="val">2.0x</span>
    </div>
    <div class="control-group">
      <label for="count">Molecule Count:</label>
      <input type="range" id="count" min="20" max="150" step="10" value="60">
      <span id="countVal" class="val">60</span>
    </div>
  </div>
  <div id="canvas-container"><canvas id="simCanvas"></canvas></div>
  <script>
    (function() {{
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const tempInput = document.getElementById('temp');
      const countInput = document.getElementById('count');
      const tempVal = document.getElementById('tempVal');
      const countVal = document.getElementById('countVal');
      let width, height, animId;
      let particles = [];

      tempInput.addEventListener('input', e => tempVal.textContent = parseFloat(e.target.value).toFixed(1) + 'x');
      countInput.addEventListener('input', e => {{
        countVal.textContent = e.target.value;
        initParticles();
      }});

      function initParticles() {{
        particles = [];
        const num = parseInt(countInput.value);
        for (let i = 0; i < num; i++) {{
          particles.push({{
            x: Math.random() * (width || 500),
            y: Math.random() * (height || 500),
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            r: Math.random() * 4 + 4,
            color: Math.random() > 0.5 ? '#f43f5e' : '#38bdf8'
          }});
        }}
      }}

      function resize() {{
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        initParticles();
      }}
      window.addEventListener('resize', resize);
      resize();

      function render() {{
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const tempMult = parseFloat(tempInput.value);

        particles.forEach(p => {{
          p.x += p.vx * tempMult;
          p.y += p.vy * tempMult;

          if (p.x - p.r < 0 || p.x + p.r > width) p.vx *= -1;
          if (p.y - p.r < 0 || p.y + p.r > height) p.vy *= -1;

          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
        }});

        animId = requestAnimationFrame(render);
      }}
      animId = requestAnimationFrame(render);
      window.addEventListener('beforeunload', () => animId && cancelAnimationFrame(animId));
      window.onerror = (m, u, l) => window.parent.postMessage({{ type: 'SIM_ERROR', error: m, line: l }}, '*');
    }})();
  </script>
</body>
</html>"""

    elif any(k in concept_lower for k in ["bio", "cell", "gene", "dna", "population", "organism", "neural", "brain"]):
        title = f"Biological Agent & Cellular Automata: {concept_clean}"
        breakdown = f"Simulating self-organizing biological dynamics of ${concept_clean}$. Agent interactions follow population growth equations: $$\\frac{dN}{dt} = r N \\left(1 - \\frac{N}{K}\\right)$$ Organisms exhibit emergence and adaptive behavior."
        instructions = "Adjust Growth Rate ($r$) and Carrying Capacity ($K$) sliders live."
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{concept_clean} Biological Simulation</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}
    #controls {{ display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }}
    .control-group {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }}
    label {{ color: #94a3b8; font-weight: 500; }}
    input[type="range"] {{ accent-color: #10b981; cursor: pointer; }}
    span.val {{ color: #10b981; font-family: monospace; min-width: 2.5rem; }}
    #canvas-container {{ flex: 1; position: relative; width: 100%; height: 100%; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="rate">Growth Rate (r):</label>
      <input type="range" id="rate" min="0.5" max="3" step="0.1" value="1.5">
      <span id="rateVal" class="val">1.5x</span>
    </div>
    <div class="control-group">
      <label for="cluster">Cluster Radius:</label>
      <input type="range" id="cluster" min="20" max="150" step="5" value="60">
      <span id="clusterVal" class="val">60px</span>
    </div>
  </div>
  <div id="canvas-container"><canvas id="simCanvas"></canvas></div>
  <script>
    (function() {{
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const rateInput = document.getElementById('rate');
      const clusterInput = document.getElementById('cluster');
      const rateVal = document.getElementById('rateVal');
      const clusterVal = document.getElementById('clusterVal');
      let width, height, animId;
      let cells = [];

      rateInput.addEventListener('input', e => rateVal.textContent = parseFloat(e.target.value).toFixed(1) + 'x');
      clusterInput.addEventListener('input', e => clusterVal.textContent = e.target.value + 'px');

      function initCells() {{
        cells = [];
        for (let i = 0; i < 70; i++) {{
          cells.push({{
            x: Math.random() * (width || 500),
            y: Math.random() * (height || 500),
            r: Math.random() * 5 + 4,
            pulse: Math.random() * Math.PI * 2
          }});
        }}
      }}

      function resize() {{
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        initCells();
      }}
      window.addEventListener('resize', resize);
      resize();

      function render() {{
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const rMult = parseFloat(rateInput.value);
        const radiusLimit = parseFloat(clusterInput.value);

        cells.forEach((c, idx) => {{
          c.pulse += 0.03 * rMult;
          const currentRadius = c.r + Math.sin(c.pulse) * 2;

          ctx.fillStyle = '#10b981';
          ctx.beginPath();
          ctx.arc(c.x, c.y, currentRadius, 0, Math.PI * 2);
          ctx.fill();

          // Connect nearby cells
          for (let j = idx + 1; j < cells.length; j++) {{
            const c2 = cells[j];
            const dist = Math.hypot(c2.x - c.x, c2.y - c.y);
            if (dist < radiusLimit) {{
              ctx.strokeStyle = `rgba(16, 185, 129, ${{1 - dist / radiusLimit}})`;
              ctx.lineWidth = 1;
              ctx.beginPath();
              ctx.moveTo(c.x, c.y);
              ctx.lineTo(c2.x, c2.y);
              ctx.stroke();
            }}
          }}
        }});

        animId = requestAnimationFrame(render);
      }}
      animId = requestAnimationFrame(render);
      window.addEventListener('beforeunload', () => animId && cancelAnimationFrame(animId));
      window.onerror = (m, u, l) => window.parent.postMessage({{ type: 'SIM_ERROR', error: m, line: l }}, '*');
    }})();
  </script>
</body>
</html>"""

    else:
        # Generic Dynamic STEM / Physics Engine for any arbitrary concept
        title = f"Interactive System Dynamics: {concept_clean}"
        breakdown = f"Dynamic Canvas simulation of ${concept_clean}$. Governed by interactive state space vectors: $$\\mathbf{{x}}(t+1) = \\mathbf{{A}} \\mathbf{{x}}(t) + \\mathbf{{B}} \\mathbf{{u}}(t)$$ Real-time parameter tuning instantly transforms phase trajectory."
        instructions = "Adjust Velocity & Field Strength sliders to alter simulation dynamics in real time."
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{concept_clean} Simulation</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}
    #controls {{ display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }}
    .control-group {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }}
    label {{ color: #94a3b8; font-weight: 500; }}
    input[type="range"] {{ accent-color: #8b5cf6; cursor: pointer; }}
    span.val {{ color: #8b5cf6; font-family: monospace; min-width: 2.5rem; }}
    #canvas-container {{ flex: 1; position: relative; width: 100%; height: 100%; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="speed">Field Speed:</label>
      <input type="range" id="speed" min="0.5" max="4" step="0.1" value="2.0">
      <span id="speedVal" class="val">2.0x</span>
    </div>
    <div class="control-group">
      <label for="nodes">Node Density:</label>
      <input type="range" id="nodes" min="20" max="100" step="5" value="50">
      <span id="nodesVal" class="val">50</span>
    </div>
  </div>
  <div id="canvas-container"><canvas id="simCanvas"></canvas></div>
  <script>
    (function() {{
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const speedInput = document.getElementById('speed');
      const nodesInput = document.getElementById('nodes');
      const speedVal = document.getElementById('speedVal');
      const nodesVal = document.getElementById('nodesVal');
      let width, height, animId;
      let nodes = [];

      speedInput.addEventListener('input', e => speedVal.textContent = parseFloat(e.target.value).toFixed(1) + 'x');
      nodesInput.addEventListener('input', e => {{
        nodesVal.textContent = e.target.value;
        initNodes();
      }});

      function initNodes() {{
        nodes = [];
        const count = parseInt(nodesInput.value);
        for (let i = 0; i < count; i++) {{
          nodes.push({{
            x: Math.random() * (width || 500),
            y: Math.random() * (height || 500),
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            r: Math.random() * 3 + 3
          }});
        }}
      }}

      function resize() {{
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        initNodes();
      }}
      window.addEventListener('resize', resize);
      resize();

      function render() {{
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const spd = parseFloat(speedInput.value);

        nodes.forEach((n, idx) => {{
          n.x += n.vx * spd;
          n.y += n.vy * spd;

          if (n.x < 0 || n.x > width) n.vx *= -1;
          if (n.y < 0 || n.y > height) n.vy *= -1;

          ctx.fillStyle = '#8b5cf6';
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
          ctx.fill();

          for (let j = idx + 1; j < nodes.length; j++) {{
            const n2 = nodes[j];
            const dist = Math.hypot(n2.x - n.x, n2.y - n.y);
            if (dist < 100) {{
              ctx.strokeStyle = `rgba(139, 92, 246, ${{1 - dist / 100}})`;
              ctx.lineWidth = 1;
              ctx.beginPath();
              ctx.moveTo(n.x, n.y);
              ctx.lineTo(n2.x, n2.y);
              ctx.stroke();
            }}
          }}
        }});

        animId = requestAnimationFrame(render);
      }}
      animId = requestAnimationFrame(render);
      window.addEventListener('beforeunload', () => animId && cancelAnimationFrame(animId));
      window.onerror = (m, u, l) => window.parent.postMessage({{ type: 'SIM_ERROR', error: m, line: l }}, '*');
    }})();
  </script>
</body>
</html>"""

    return SimulationResponse(
        title=title,
        concept_breakdown=breakdown,
        user_instructions=instructions,
        simulation_html=html
    )

async def generate_simulation(concept: str) -> SimulationResponse:
    """
    Generate an interactive STEM simulation for ANY topic using Google Generative AI (Gemini).
    Includes auto-retry self-healing loop and fast procedural fallback for offline/unlimited generation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        logger.info("Using procedural simulation generator for topic: %s", concept)
        return generate_procedural_simulation(concept)

    import asyncio
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    models_to_try = ["gemini-2.0-flash", "gemini-flash-latest"]
    prompt = f"STEM / Academic Topic to Simulate: {concept}"

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.3
                }
            )

            full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
            
            # Execute with a 4.5s timeout per attempt so user never waits long
            response = await asyncio.wait_for(
                asyncio.to_thread(model.generate_content, full_prompt),
                timeout=4.5
            )
            raw_text = response.text.strip()
            
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            parsed_data = json.loads(raw_text)
            return SimulationResponse(**parsed_data)

        except Exception as e:
            logger.warning("Gemini model %s call failed or timed out: %s", model_name, e)
            continue

    # Instant seamless procedural generator fallback for ANY topic
    logger.info("Fast fallback to procedural simulation generator for topic: %s", concept)
    return generate_procedural_simulation(concept)
