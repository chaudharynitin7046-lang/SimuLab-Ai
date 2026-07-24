document.addEventListener('DOMContentLoaded', () => {
  const simFrame = document.getElementById('simFrame');
  const conceptTitle = document.getElementById('conceptTitle');
  const conceptBreakdown = document.getElementById('conceptBreakdown');
  const userInstructions = document.getElementById('userInstructions');
  const promptInput = document.getElementById('promptInput');
  const generateBtn = document.getElementById('generateBtn');
  const tickerCard = document.getElementById('tickerCard');
  const tickerLogs = document.getElementById('tickerLogs');
  const tickerTimer = document.getElementById('tickerTimer');
  const demoBtns = document.querySelectorAll('.demo-btn');
  const errorBoundary = document.getElementById('errorBoundary');
  const errorMessage = document.getElementById('errorMessage');
  const regenerateErrBtn = document.getElementById('regenerateErrBtn');

  let heroDemos = {};
  let currentConcept = 'solar_system';
  let tickerInterval = null;

  // 1. Fetch pre-seeded hero demos on load
  async function fetchHeroDemos() {
    try {
      const res = await fetch('/api/demos');
      if (res.ok) {
        heroDemos = await res.json();
        // Auto-load solar system immediately
        if (heroDemos['solar_system']) {
          loadDemo('solar_system');
        }
      }
    } catch (err) {
      console.error('Failed to load hero demos:', err);
    }
  }

  // 2. Load demo payload into iframe & update breakdown card
  function loadDemo(demoKey) {
    const demo = heroDemos[demoKey];
    if (!demo) return;

    currentConcept = demoKey;
    hideError();

    // Update active button state
    demoBtns.forEach(btn => {
      if (btn.dataset.demo === demoKey) {
        btn.className = 'demo-btn active px-3 py-1 text-xs font-medium rounded-lg transition-all duration-200 bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/30';
      } else {
        btn.className = 'demo-btn px-3 py-1 text-xs font-medium rounded-lg transition-all duration-200 text-slate-300 hover:text-white hover:bg-slate-700/60';
      }
    });

    // Update Feynman Breakdown Card
    conceptTitle.textContent = demo.title;
    conceptBreakdown.textContent = demo.concept_breakdown;
    userInstructions.textContent = demo.user_instructions;

    // Inject into iframe via srcdoc
    simFrame.srcdoc = demo.simulation_html;
  }

  // Demo pill click handlers
  demoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const demoKey = btn.dataset.demo;
      loadDemo(demoKey);
    });
  });

  // 3. Multi-step loading ticker
  const TICKER_STEPS = [
    "Parsing physics constraints...",
    "Architecting Canvas 2D loop...",
    "Sanitizing JS animation IDs...",
    "Binding interactive sliders...",
    "Rendering!"
  ];

  function startTicker() {
    tickerCard.classList.remove('hidden');
    tickerLogs.innerHTML = '';
    let startTime = Date.now();

    tickerInterval = setInterval(() => {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      tickerTimer.textContent = `${elapsed}s`;
    }, 100);

    TICKER_STEPS.forEach((step, idx) => {
      setTimeout(() => {
        const line = document.createElement('div');
        line.className = 'ticker-line flex items-center gap-2';
        line.innerHTML = `
          <span class="text-cyan-500">❯</span>
          <span>${step}</span>
        `;
        tickerLogs.appendChild(line);
      }, idx * 400);
    });
  }

  function stopTicker() {
    if (tickerInterval) clearInterval(tickerInterval);
    setTimeout(() => {
      tickerCard.classList.add('hidden');
    }, 1000);
  }

  // 4. Generate Simulation
  async function generateSimulation() {
    const prompt = promptInput.value.trim();
    if (!prompt) {
      promptInput.focus();
      promptInput.classList.add('ring-2', 'ring-rose-500');
      setTimeout(() => promptInput.classList.remove('ring-2', 'ring-rose-500'), 1500);
      return;
    }

    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-75', 'cursor-not-allowed');
    hideError();
    startTicker();

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ concept: prompt })
      });

      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}`);
      }

      const data = await res.json();

      // Update Breakdown Card & iframe
      conceptTitle.textContent = data.title;
      conceptBreakdown.textContent = data.concept_breakdown;
      userInstructions.textContent = data.user_instructions;
      simFrame.srcdoc = data.simulation_html;

    } catch (err) {
      console.error('Generation error:', err);
      showError(`Failed to generate simulation: ${err.message}`);
    } finally {
      stopTicker();
      generateBtn.disabled = false;
      generateBtn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
  }

  generateBtn.addEventListener('click', generateSimulation);
  promptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      generateSimulation();
    }
  });

  // 5. Error Recovery Boundary
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SIM_ERROR') {
      console.warn('Caught runtime JS error in simulation iframe:', event.data);
      showError(`Runtime Error in Canvas: "${event.data.error}" (Line ${event.data.line || 'N/A'})`);
    }
  });

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBoundary.classList.remove('hidden');
  }

  function hideError() {
    errorBoundary.classList.add('hidden');
  }

  regenerateErrBtn.addEventListener('click', () => {
    hideError();
    if (promptInput.value.trim()) {
      generateSimulation();
    } else {
      loadDemo('solar_system');
    }
  });

  // Initialize
  fetchHeroDemos();
});
