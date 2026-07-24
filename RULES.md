# NON-NEGOTIABLE ENGINEERING LAWS

1. **File Boundaries & Encapsulation** — Backend logic lives in `/app`, frontend assets in `/static`, tests in `/tests`. Do not scatter random files in the project root.
2. **Zero Hallucinated Dependencies** — Every LLM-generated simulation must be 100% vanilla JavaScript Canvas API + inline CSS. Never allow the LLM to inject `<script src="...p5.js">`, Three.js, external fonts, or any CDN inside generated simulation code. (Tailwind via CDN is permitted only in the app shell itself, not in generated sims.)
3. **Git Checkpoint Protocol** — Act as a disciplined engineer. After **every** completed step:
   - Run the step's verification command and capture the output.
   - **Stop and show me the verification receipt before committing.** Wait for my go-ahead on the first few steps; once I say "auto-commit from here," you may proceed without asking.
   - If verification passes, stage exact files (`git add <files>`) and commit with a semantic message: `feat: [step name] - [what was built]`.
   - If verification fails, diagnose, fix, and re-test. **Never commit broken code.**
4. **Verification Receipts Required** — Never claim a step is "done" without running a real command (`pytest`, `python -m py_compile`, `curl`, etc.) and pasting the console output as proof.
