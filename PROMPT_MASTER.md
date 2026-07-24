# SIMULAB AI — MASTER AGENT EXECUTION CONTRACT (v3.0 Unified)

## SECTION 1: MISSION

You are a Staff-Level Python Architect and AI Systems Engineer. Build **"SimuLab AI"** — a
production-grade educational web app that uses an LLM to dynamically generate interactive,
real-time HTML5 Canvas 2D simulations for abstract STEM concepts, returned as structured JSON
and rendered live in the browser.

---

## SECTION 2: NON-NEGOTIABLE ENGINEERING LAWS

1. **File Boundaries & Encapsulation** — Backend logic lives in `/app`, frontend assets in
   `/static`, tests in `/tests`. Do not scatter random files in the project root.
2. **Zero Hallucinated Dependencies** — Every LLM-generated simulation must be 100% vanilla
   JavaScript Canvas API + inline CSS. Never allow the LLM to inject `<script src="...p5.js">`,
   Three.js, external fonts, or any CDN inside generated simulation code. (Tailwind via CDN is
   permitted only in the app shell itself, not in generated sims.)
3. **Git Checkpoint Protocol** — Act as a disciplined engineer. After **every** completed step:
   - Run the step's verification command and capture the output.
   - **Stop and show me the verification receipt before committing.** Wait for my go-ahead on
     the first few steps; once I say "auto-commit from here," you may proceed without asking.
   - If verification passes, stage exact files (`git add <files>`) and commit with a semantic
     message: `feat: [step name] - [what was built]`.
   - If verification fails, diagnose, fix, and re-test. **Never commit broken code.**
4. **Verification Receipts Required** — Never claim a step is "done" without running a real
   command (`pytest`, `python -m py_compile`, `curl`, etc.) and pasting the console output as
   proof.

---

## SECTION 3: TECH STACK

- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic v2, `python-dotenv`, `httpx`, `pytest`.
- **AI Integration:** `google-generativeai` as the default SDK (swap to `openai` or `anthropic`
  via an environment variable if I ask), using structured/JSON-mode output. If no API key is
  present, the backend must fall back cleanly to a local mock so development never blocks on a
  missing key.
- **Frontend:** Single-page app served by FastAPI — HTML5, Tailwind CSS via CDN `<script>` tag
  (zero-build), vanilla JS. Dark-mode aesthetic: `bg-slate-900`, `text-slate-100`, cyan/emerald
  accents.
- **Version Control:** Git, with a commit at every verified checkpoint (see Section 2, Law 3).

---

## SECTION 4: THE "WOW FACTOR" SPECIFICATION

1. **Live Simulation Workspace** — Split-screen UI.
   - *Left panel:* prompt textarea, "Generate" button, a "Feynman Concept Breakdown" card, and a
     terminal-style loading ticker.
   - *Right panel:* a sandboxed `<iframe id="simFrame" sandbox="allow-scripts">` that renders the
     simulation via `srcdoc`.
2. **Mandatory Interactivity** — Every generated simulation must include at least 2 real-time UI
   sliders/toggles (e.g., gravity, mass, frequency, temperature) wired directly into the
   animation loop so changes apply instantly.
3. **Instant Magic (Pre-Seeded Demos)** — Hardcode 3 breathtaking, pre-validated simulations in
   `/app/demos.py` that load instantly with zero API latency:
   - `solar_system` — N-body orbital mechanics with gravity and mass sliders.
   - `neural_net` — a visual perceptron network where clicking nodes fires animated signal
     pulses and adjusts weights.
   - `wave_interference` — two overlapping ripple generators with frequency and wavelength
     controls.
4. **Live Agent Logging** — While a new simulation is generating, show a multi-step
   terminal-style ticker: `"Parsing physics constraints..."` → `"Architecting Canvas loop..."` →
   `"Sanitizing JS animation IDs..."` → `"Rendering!"`
5. **Error Recovery Boundary** — If an injected simulation throws a runtime JS error inside the
   iframe, catch it via a `window.postMessage` handler and display a clean "Regenerating
   Simulation..." state instead of a blank or broken iframe.

---

## SECTION 5: TECHNICAL ARCHITECTURE & SCHEMAS

### Backend (`/app`)

Strict Pydantic v2 response model:

```python
class SimulationResponse(BaseModel):
    title: str = Field(..., description="Catchy simulation title")
    concept_breakdown: str = Field(..., description="2-3 sentence Feynman explanation")
    user_instructions: str = Field(..., description="How to interact with sliders/controls")
    simulation_html: str = Field(..., description="Complete valid HTML/JS/CSS document string")
```

- `app/demos.py` — the 3 hero demo payloads (full, valid HTML5 Canvas strings), pre-validated.
- `app/llm.py` — `generate_simulation(concept: str) -> SimulationResponse`. System prompt
  enforces the Section 2/4 guardrails (vanilla JS only, `requestAnimationFrame` cleanup on
  teardown, mandatory sliders, single-quoted strings inside the HTML string). Wrap the call in a
  **self-healing retry loop**: on `JSONDecodeError` or Pydantic validation failure, feed the
  error back to the LLM with instructions to fix the JSON/syntax, retrying up to 2 times before
  surfacing a clean error to the client.
- `app/main.py` — FastAPI app, mounts `/static`, exposes:
  - `GET /api/demos` — returns the 3 pre-seeded demos.
  - `POST /api/generate` — accepts `{"concept": "string"}`; if no API key is configured, falls
    back cleanly to a modified demo payload so development continues offline.

### Frontend (`/static`)

- `index.html`, `app.js`, `style.css`.
- Top navbar with project title and "Demo Mode" pills.
- On load: fetch `/api/demos` and render the first demo immediately (this is the "wow factor"
  moment — no waiting on an API call).
- On submit: animate the ticker, `POST /api/generate`, inject `response.simulation_html` into
  the iframe via `srcdoc`.

---

## SECTION 6: STEP-BY-STEP EXECUTION ROADMAP

Execute sequentially. Do not advance to the next step until the current one is verified.

### STEP 1 — Scaffolding, Environment & Project Memory
1. Create directories: `/app`, `/static`, `/tests`.
2. Create `requirements.txt`: `fastapi>=0.110.0`, `uvicorn>=0.28.0`, `pydantic>=2.0`,
   `google-generativeai>=0.4.0`, `pytest>=8.0.0`, `httpx>=0.27.0`, `python-dotenv>=1.0.0`.
3. Create `.env.example` with `GEMINI_API_KEY=your_key_here`, loaded via `dotenv`.
4. Create `.gitignore` ignoring `.env`, `__pycache__`, `.venv/`, `.pytest_cache/`.
5. Create `RULES.md` containing the Section 2 "Non-Negotiable Engineering Laws" verbatim, so
   future agent context windows retain project memory even after this file scrolls out of view.
6. **Verify:** init Git, install dependencies into a virtualenv, check `git status`.
7. **Commit #1:** `chore: initialize project structure and agent memory`.

### STEP 2 — Core API & Mock Data Engine
1. Build `/app/demos.py` with the 3 pre-seeded hero simulations.
2. Build `/app/main.py`: FastAPI init, mount `/static`, `GET /api/demos`, `POST /api/generate`
   with offline fallback when no API key is present.
3. **Verify:** `/tests/test_api.py` using `TestClient` — assert `/api/demos` returns 200 OK with
   valid JSON. Run `pytest`.
4. **Commit #2:** `feat: build core FastAPI router and offline demo fallback`.

### STEP 3 — LLM Integration & Self-Healing Architecture
1. Build `/app/llm.py`'s `generate_simulation()` service per Section 5.
2. Configure the system prompt to enforce all guardrails from Sections 2 and 4.
3. Add the auto-retry loop described in Section 5 (max 2 retries on JSON/schema failure).
4. **Verify:** unit test that mocks the LLM response to confirm schema validation and retry
   logic. Run `pytest`.
5. **Commit #3:** `feat: integrate structured LLM generation with auto-retry schema validation`.

### STEP 4 — Frontend Workspace & Iframe Sandboxing
1. Build `/static/index.html`, `/static/app.js`, `/static/style.css` per Section 5.
2. Implement the split-screen layout, ticker, and demo auto-load on page open.
3. Implement generate → ticker animation → `POST /api/generate` → inject into
   `<iframe sandbox="allow-scripts">` via `srcdoc`, plus the Error Recovery Boundary from
   Section 4.
4. **Verify:** start Uvicorn (`python -m uvicorn app.main:app`) in the background, confirm
   `/static/index.html` returns 200, confirm zero console/syntax errors.
5. **Commit #4:** `feat: build split-screen UI and secure iframe sandbox rendering`.

### STEP 5 — Final Verification & Test Suite
1. Run the full test suite: `pytest -v`.
2. Verify Python syntax across the backend: `python -m py_compile app/*.py`.
3. **Commit #5:** `test: finalize test suite and verify full system integrity`.

---

## SECTION 7: FINAL RECEIPT REQUEST

When Step 5 is complete, produce a Markdown summary receipt containing:

1. `git log --oneline` output proving all 5 incremental commits exist.
2. The final passing `pytest` terminal output.
3. Exact instructions for how I start the server and view the app locally.
