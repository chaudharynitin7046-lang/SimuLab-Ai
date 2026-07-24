"""
Pre-seeded hero simulations for SimuLab AI (Physics & Mathematics).
Each payload is a full, valid HTML5 Canvas document with inline CSS and vanilla JS.
"""

HERO_DEMOS = {
    "fourier_series": {
        "title": "Fourier Series Wave Synthesis & Epicycles",
        "concept_breakdown": "Any periodic function $f(t)$ can be represented as a sum of harmonic sine and cosine waves: $$f(t) = \\frac{a_0}{2} + \\sum_{n=1}^{\\infty} \\left( a_n \\cos(n \\omega t) + b_n \\sin(n \\omega t) \\right)$$ Rotating complex epicycles visually decompose and synthesize complex signal waveforms in real time.",
        "user_instructions": "Adjust Number of Harmonics ($N$) and Rotation Speed ($\\\\omega$) to witness how higher harmonic vectors approximate sharper step functions.",
        "simulation_html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fourier Series Epicycles</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
    #controls { display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }
    .control-group { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    label { color: #94a3b8; font-weight: 500; }
    input[type="range"] { accent-color: #06b6d4; cursor: pointer; }
    span.val { color: #06b6d4; font-family: monospace; min-width: 2.5rem; }
    #canvas-container { flex: 1; position: relative; width: 100%; height: 100%; }
    canvas { display: block; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="harmonics">Harmonics (N):</label>
      <input type="range" id="harmonics" min="1" max="25" step="1" value="7">
      <span id="harmonicsVal" class="val">7</span>
    </div>
    <div class="control-group">
      <label for="speed">Rotation Speed:</label>
      <input type="range" id="speed" min="0.005" max="0.04" step="0.005" value="0.015">
      <span id="speedVal" class="val">1.0x</span>
    </div>
  </div>
  <div id="canvas-container">
    <canvas id="simCanvas"></canvas>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const harmonicsInput = document.getElementById('harmonics');
      const speedInput = document.getElementById('speed');
      const harmonicsVal = document.getElementById('harmonicsVal');
      const speedVal = document.getElementById('speedVal');

      let width, height;
      let animId;
      let time = 0;
      let wavePath = [];

      harmonicsInput.addEventListener('input', (e) => harmonicsVal.textContent = e.target.value);
      speedInput.addEventListener('input', (e) => speedVal.textContent = (parseFloat(e.target.value) / 0.015).toFixed(1) + 'x');

      function resize() {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        wavePath = [];
      }
      window.addEventListener('resize', resize);
      resize();

      function render() {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const N = parseInt(harmonicsInput.value);
        const speed = parseFloat(speedInput.value);

        const epicentreX = width * 0.28;
        const epicentreY = height * 0.5;

        let x = epicentreX;
        let y = epicentreY;

        // Draw rotating epicycles for Square Wave: 4 / (n * pi) * sin(n * t)
        for (let i = 0; i < N; i++) {
          const prevX = x;
          const prevY = y;
          const n = i * 2 + 1; // Odd harmonics
          const radius = (height * 0.22) * (4 / (n * Math.PI));

          x += radius * Math.cos(n * time);
          y += radius * Math.sin(n * time);

          // Draw circle
          ctx.strokeStyle = `rgba(6, 182, 212, ${0.4 - i * 0.015})`;
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.arc(prevX, prevY, radius, 0, Math.PI * 2);
          ctx.stroke();

          // Draw rotating radius vector
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(x, y);
          ctx.stroke();
        }

        // Add synthesized point to wave history
        wavePath.unshift(y);
        if (wavePath.length > width * 0.55) {
          wavePath.pop();
        }

        // Draw connecting line to wave plot
        const waveStartX = width * 0.52;
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.6)';
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(waveStartX, y);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw synthesized waveform graph
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        for (let i = 0; i < wavePath.length; i++) {
          const wx = waveStartX + i;
          const wy = wavePath[i];
          if (i === 0) ctx.moveTo(wx, wy);
          else ctx.lineTo(wx, wy);
        }
        ctx.stroke();

        // Highlight pen point
        ctx.fillStyle = '#f43f5e';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();

        time += speed;
        animId = requestAnimationFrame(render);
      }

      animId = requestAnimationFrame(render);

      window.addEventListener('beforeunload', () => {
        if (animId) cancelAnimationFrame(animId);
      });

      window.onerror = function(msg, url, line) {
        window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
      };
    })();
  </script>
</body>
</html>"""
    },
    "lorenz_attractor": {
        "title": "Lorenz Chaotic Attractor & Differential Systems",
        "concept_breakdown": "The Lorenz system is a system of three non-linear ordinary differential equations: $$\\frac{dx}{dt} = \\sigma(y - x), \\quad \\frac{dy}{dt} = x(\\rho - z) - y, \\quad \\frac{dz}{dt} = xy - \\beta z$$ It exhibits deterministic chaos where minute changes in initial conditions yield radically divergent trajectories ('Butterfly Effect').",
        "user_instructions": "Adjust Prandtl Number ($\\\\sigma$) and Rayleigh Number ($\\\\rho$) to observe dynamic trajectory evolution in 3D projection space.",
        "simulation_html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lorenz Chaotic Attractor</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
    #controls { display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }
    .control-group { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    label { color: #94a3b8; font-weight: 500; }
    input[type="range"] { accent-color: #8b5cf6; cursor: pointer; }
    span.val { color: #8b5cf6; font-family: monospace; min-width: 2.5rem; }
    #canvas-container { flex: 1; position: relative; width: 100%; height: 100%; }
    canvas { display: block; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="sigma">Prandtl (σ):</label>
      <input type="range" id="sigma" min="2" max="25" step="0.5" value="10">
      <span id="sigmaVal" class="val">10.0</span>
    </div>
    <div class="control-group">
      <label for="rho">Rayleigh (ρ):</label>
      <input type="range" id="rho" min="10" max="50" step="1" value="28">
      <span id="rhoVal" class="val">28</span>
    </div>
  </div>
  <div id="canvas-container">
    <canvas id="simCanvas"></canvas>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const sigmaInput = document.getElementById('sigma');
      const rhoInput = document.getElementById('rho');
      const sigmaVal = document.getElementById('sigmaVal');
      const rhoVal = document.getElementById('rhoVal');

      let width, height;
      let animId;

      // Lorenz state
      let x = 0.1, y = 0, z = 0;
      const beta = 8 / 3;
      const dt = 0.01;
      let points = [];
      let angleY = 0;

      sigmaInput.addEventListener('input', (e) => {
        sigmaVal.textContent = parseFloat(e.target.value).toFixed(1);
        resetSystem();
      });
      rhoInput.addEventListener('input', (e) => {
        rhoVal.textContent = e.target.value;
        resetSystem();
      });

      function resetSystem() {
        x = 0.1; y = 0; z = 0;
        points = [];
      }

      function resize() {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        resetSystem();
      }
      window.addEventListener('resize', resize);
      resize();

      function render() {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const sigma = parseFloat(sigmaInput.value);
        const rho = parseFloat(rhoInput.value);

        // Step 5 Lorenz iterations per frame
        for (let i = 0; i < 5; i++) {
          const dx = sigma * (y - x) * dt;
          const dy = (x * (rho - z) - y) * dt;
          const dz = (x * y - beta * z) * dt;
          x += dx;
          y += dy;
          z += dz;
          points.push({ x, y, z });
          if (points.length > 2500) points.shift();
        }

        angleY += 0.005;
        const scale = Math.min(width, height) / 70;
        const cosA = Math.cos(angleY);
        const sinA = Math.sin(angleY);

        ctx.lineWidth = 1.2;
        ctx.beginPath();

        for (let i = 0; i < points.length; i++) {
          const p = points[i];
          // 3D rotation around Y axis
          const rx = p.x * cosA - p.y * sinA;
          const ry = p.x * sinA + p.y * cosA;
          const rz = p.z;

          const px = width / 2 + rx * scale;
          const py = height / 2 + (rz - 25) * scale;

          if (i === 0) {
            ctx.moveTo(px, py);
          } else {
            ctx.lineTo(px, py);
          }
        }

        // Gradient stroke styling
        const grad = ctx.createLinearGradient(0, 0, width, height);
        grad.addColorStop(0, '#8b5cf6');
        grad.addColorStop(0.5, '#06b6d4');
        grad.addColorStop(1, '#f43f5e');
        ctx.strokeStyle = grad;
        ctx.stroke();

        // Current trajectory lead dot
        if (points.length > 0) {
          const last = points[points.length - 1];
          const rx = last.x * cosA - last.y * sinA;
          const rz = last.z;
          const px = width / 2 + rx * scale;
          const py = height / 2 + (rz - 25) * scale;

          ctx.fillStyle = '#f8fafc';
          ctx.beginPath();
          ctx.arc(px, py, 4, 0, Math.PI * 2);
          ctx.fill();
        }

        animId = requestAnimationFrame(render);
      }

      animId = requestAnimationFrame(render);

      window.addEventListener('beforeunload', () => {
        if (animId) cancelAnimationFrame(animId);
      });

      window.onerror = function(msg, url, line) {
        window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
      };
    })();
  </script>
</body>
</html>"""
    },
    "solar_system": {
        "title": "N-Body Solar System Orbital Dynamics",
        "concept_breakdown": "Orbital mechanics are governed by Newton's law of universal gravitation: $$F = G \\frac{m_1 m_2}{r^2}$$ Planets maintain tangential velocity while undergoing centripetal gravitational acceleration, tracing out stable elliptical orbits.",
        "user_instructions": "Use the Gravity and Sun Mass sliders to alter orbital velocities and gravitational pull in real time.",
        "simulation_html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Solar System Simulation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
    #controls { display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }
    .control-group { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    label { color: #94a3b8; font-weight: 500; }
    input[type="range"] { accent-color: #06b6d4; cursor: pointer; }
    span.val { color: #06b6d4; font-family: monospace; min-width: 2.5rem; }
    #canvas-container { flex: 1; position: relative; width: 100%; height: 100%; }
    canvas { display: block; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="gravity">Gravity Multiplier:</label>
      <input type="range" id="gravity" min="0.1" max="3" step="0.1" value="1.0">
      <span id="gravityVal" class="val">1.0x</span>
    </div>
    <div class="control-group">
      <label for="sunMass">Sun Mass:</label>
      <input type="range" id="sunMass" min="0.5" max="3" step="0.1" value="1.0">
      <span id="sunMassVal" class="val">1.0x</span>
    </div>
  </div>
  <div id="canvas-container">
    <canvas id="simCanvas"></canvas>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const gravityInput = document.getElementById('gravity');
      const sunMassInput = document.getElementById('sunMass');
      const gravityVal = document.getElementById('gravityVal');
      const sunMassVal = document.getElementById('sunMassVal');

      let width, height, centerX, centerY;
      let animId;

      function resize() {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        centerX = width / 2;
        centerY = height / 2;
      }
      window.addEventListener('resize', resize);
      resize();

      gravityInput.addEventListener('input', (e) => gravityVal.textContent = parseFloat(e.target.value).toFixed(1) + 'x');
      sunMassInput.addEventListener('input', (e) => sunMassVal.textContent = parseFloat(e.target.value).toFixed(1) + 'x');

      const planets = [
        { name: 'Mercury', distance: 60, radius: 4, speed: 0.04, color: '#a1a1aa', angle: 0 },
        { name: 'Venus', distance: 100, radius: 7, speed: 0.025, color: '#fde047', angle: 1 },
        { name: 'Earth', distance: 150, radius: 8, speed: 0.015, color: '#38bdf8', angle: 2, moon: { distance: 16, radius: 2, speed: 0.08, angle: 0 } },
        { name: 'Mars', distance: 200, radius: 6, speed: 0.01, color: '#f87171', angle: 3 },
        { name: 'Jupiter', distance: 270, radius: 16, speed: 0.005, color: '#fb923c', angle: 4 },
        { name: 'Saturn', distance: 340, radius: 12, speed: 0.003, color: '#fef08a', angle: 5, ring: true }
      ];

      const stars = Array.from({ length: 120 }, () => ({
        x: Math.random() * 2000,
        y: Math.random() * 2000,
        r: Math.random() * 1.5,
        alpha: Math.random() * 0.8 + 0.2
      }));

      function render() {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        stars.forEach(star => {
          ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
          ctx.beginPath();
          ctx.arc(star.x % width, star.y % height, star.r, 0, Math.PI * 2);
          ctx.fill();
        });

        const G = parseFloat(gravityInput.value);
        const M = parseFloat(sunMassInput.value);

        const sunRadius = 24 * Math.cbrt(M);
        const sunGlow = ctx.createRadialGradient(centerX, centerY, 5, centerX, centerY, sunRadius * 2);
        sunGlow.addColorStop(0, '#fef08a');
        sunGlow.addColorStop(0.4, '#eab308');
        sunGlow.addColorStop(1, 'rgba(234, 179, 8, 0)');
        
        ctx.fillStyle = sunGlow;
        ctx.beginPath();
        ctx.arc(centerX, centerY, sunRadius * 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#fef08a';
        ctx.beginPath();
        ctx.arc(centerX, centerY, sunRadius, 0, Math.PI * 2);
        ctx.fill();

        planets.forEach(p => {
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.15)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.arc(centerX, centerY, p.distance, 0, Math.PI * 2);
          ctx.stroke();

          p.angle += p.speed * G * Math.sqrt(M);
          const px = centerX + Math.cos(p.angle) * p.distance;
          const py = centerY + Math.sin(p.angle) * p.distance;

          if (p.ring) {
            ctx.strokeStyle = 'rgba(254, 240, 138, 0.4)';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.ellipse(px, py, p.radius * 2, p.radius * 0.8, Math.PI / 4, 0, Math.PI * 2);
            ctx.stroke();
          }

          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(px, py, p.radius, 0, Math.PI * 2);
          ctx.fill();

          if (p.moon) {
            p.moon.angle += p.moon.speed * G;
            const mx = px + Math.cos(p.moon.angle) * p.moon.distance;
            const my = py + Math.sin(p.moon.angle) * p.moon.distance;
            ctx.fillStyle = '#cbd5e1';
            ctx.beginPath();
            ctx.arc(mx, my, p.moon.radius, 0, Math.PI * 2);
            ctx.fill();
          }
        });

        animId = requestAnimationFrame(render);
      }

      animId = requestAnimationFrame(render);

      window.addEventListener('beforeunload', () => {
        if (animId) cancelAnimationFrame(animId);
      });

      window.onerror = function(msg, url, line) {
        window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
      };
    })();
  </script>
</body>
</html>"""
    },
    "neural_net": {
        "title": "Interactive Perceptron & Neural Propagation",
        "concept_breakdown": "Artificial neural networks process signals through weighted activation functions: $$y = \\sigma \\left( \\sum_{i=1}^n w_i x_i + b \\right)$$ Clicking nodes triggers forward-pass activation pulses across interconnected synapse layers.",
        "user_instructions": "Click any neuron node to fire a pulse. Adjust Signal Speed and Bias Sensitivity sliders to observe real-time propagation.",
        "simulation_html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neural Network Simulation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
    #controls { display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }
    .control-group { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    label { color: #94a3b8; font-weight: 500; }
    input[type="range"] { accent-color: #10b981; cursor: pointer; }
    span.val { color: #10b981; font-family: monospace; min-width: 2.5rem; }
    .hint { font-size: 0.75rem; color: #64748b; margin-left: auto; }
    #canvas-container { flex: 1; position: relative; width: 100%; height: 100%; }
    canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="speed">Signal Speed:</label>
      <input type="range" id="speed" min="0.005" max="0.05" step="0.005" value="0.02">
      <span id="speedVal" class="val">1.0x</span>
    </div>
    <div class="control-group">
      <label for="bias">Bias Sensitivity:</label>
      <input type="range" id="bias" min="-1" max="1" step="0.1" value="0.2">
      <span id="biasVal" class="val">+0.2</span>
    </div>
    <div class="hint">⚡ Click any node to fire a pulse</div>
  </div>
  <div id="canvas-container">
    <canvas id="simCanvas"></canvas>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const speedInput = document.getElementById('speed');
      const biasInput = document.getElementById('bias');
      const speedVal = document.getElementById('speedVal');
      const biasVal = document.getElementById('biasVal');

      let width, height;
      let animId;
      const layersConfig = [3, 5, 5, 2];
      let nodes = [];
      let connections = [];
      let pulses = [];

      speedInput.addEventListener('input', (e) => {
        const mult = (parseFloat(e.target.value) / 0.02).toFixed(1);
        speedVal.textContent = mult + 'x';
      });
      biasInput.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        biasVal.textContent = (val >= 0 ? '+' : '') + val.toFixed(1);
      });

      function initNetwork() {
        nodes = [];
        connections = [];
        pulses = [];

        const layerXGap = width / (layersConfig.length + 1);

        layersConfig.forEach((count, layerIdx) => {
          const x = layerXGap * (layerIdx + 1);
          const nodeYGap = height / (count + 1);
          for (let i = 0; i < count; i++) {
            nodes.push({
              id: `${layerIdx}-${i}`,
              layer: layerIdx,
              x: x,
              y: nodeYGap * (i + 1),
              radius: 16,
              activation: Math.random(),
              pulseAlpha: 0
            });
          }
        });

        nodes.forEach(source => {
          nodes.filter(target => target.layer === source.layer + 1).forEach(target => {
            connections.push({
              from: source,
              to: target,
              weight: (Math.random() * 2 - 1)
            });
          });
        });
      }

      function resize() {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
        initNetwork();
      }
      window.addEventListener('resize', resize);
      resize();

      function firePulse(fromNode) {
        fromNode.pulseAlpha = 1.0;
        connections.filter(c => c.from === fromNode).forEach(c => {
          pulses.push({
            connection: c,
            progress: 0
          });
        });
      }

      setInterval(() => {
        const inputNodes = nodes.filter(n => n.layer === 0);
        const randomNode = inputNodes[Math.floor(Math.random() * inputNodes.length)];
        if (randomNode) firePulse(randomNode);
      }, 1500);

      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        nodes.forEach(n => {
          const dist = Math.hypot(n.x - mx, n.y - my);
          if (dist <= n.radius * 1.5) {
            firePulse(n);
          }
        });
      });

      function render() {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const currentSpeed = parseFloat(speedInput.value);
        const bias = parseFloat(biasInput.value);

        connections.forEach(c => {
          const weightEffect = c.weight + bias;
          ctx.strokeStyle = weightEffect >= 0 
            ? `rgba(16, 185, 129, ${0.15 + Math.abs(weightEffect) * 0.25})`
            : `rgba(239, 68, 68, ${0.15 + Math.abs(weightEffect) * 0.25})`;
          ctx.lineWidth = Math.max(1, Math.abs(weightEffect) * 3);
          ctx.beginPath();
          ctx.moveTo(c.from.x, c.from.y);
          ctx.lineTo(c.to.x, c.to.y);
          ctx.stroke();
        });

        for (let i = pulses.length - 1; i >= 0; i--) {
          const p = pulses[i];
          p.progress += currentSpeed;

          const px = p.connection.from.x + (p.connection.to.x - p.connection.from.x) * p.progress;
          const py = p.connection.from.y + (p.connection.to.y - p.connection.from.y) * p.progress;

          const glow = ctx.createRadialGradient(px, py, 1, px, py, 8);
          glow.addColorStop(0, '#10b981');
          glow.addColorStop(1, 'rgba(16, 185, 129, 0)');

          ctx.fillStyle = glow;
          ctx.beginPath();
          ctx.arc(px, py, 8, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#6ee7b7';
          ctx.beginPath();
          ctx.arc(px, py, 3, 0, Math.PI * 2);
          ctx.fill();

          if (p.progress >= 1.0) {
            firePulse(p.connection.to);
            pulses.splice(i, 1);
          }
        }

        nodes.forEach(n => {
          if (n.pulseAlpha > 0) {
            n.pulseAlpha -= 0.02;
          }

          ctx.shadowColor = '#10b981';
          ctx.shadowBlur = 10 * n.pulseAlpha;

          ctx.fillStyle = n.layer === 0 ? '#06b6d4' : (n.layer === layersConfig.length - 1 ? '#f43f5e' : '#1e293b');
          ctx.strokeStyle = '#10b981';
          ctx.lineWidth = 2 + n.pulseAlpha * 3;

          ctx.beginPath();
          ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          ctx.shadowBlur = 0;

          ctx.fillStyle = `rgba(255, 255, 255, ${0.4 + n.activation * 0.6})`;
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.radius * 0.4, 0, Math.PI * 2);
          ctx.fill();
        });

        animId = requestAnimationFrame(render);
      }

      animId = requestAnimationFrame(render);

      window.addEventListener('beforeunload', () => {
        if (animId) cancelAnimationFrame(animId);
      });

      window.onerror = function(msg, url, line) {
        window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
      };
    })();
  </script>
</body>
</html>"""
    },
    "wave_interference": {
        "title": "Dual Wave Source Interference Patterns",
        "concept_breakdown": "When coherent wave fronts meet, displacement amplitudes superimpose: $$y(r, t) = A_1 \\sin(k r_1 - \\omega t) + A_2 \\sin(k r_2 - \\omega t)$$ In-phase overlaps yield constructive interference (bright crests), while out-of-phase overlaps cancel out (dark nodal lines).",
        "user_instructions": "Adjust Frequency ($\\\\omega$) and Wavelength ($\\\\lambda$) sliders to alter spatial node density live.",
        "simulation_html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wave Interference Simulation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
    #controls { display: flex; gap: 1rem; padding: 0.75rem 1rem; background-color: #1e293b; border-bottom: 1px solid #334155; align-items: center; flex-wrap: wrap; z-index: 10; }
    .control-group { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    label { color: #94a3b8; font-weight: 500; }
    input[type="range"] { accent-color: #8b5cf6; cursor: pointer; }
    span.val { color: #8b5cf6; font-family: monospace; min-width: 2.5rem; }
    #canvas-container { flex: 1; position: relative; width: 100%; height: 100%; }
    canvas { display: block; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="controls">
    <div class="control-group">
      <label for="freq">Frequency (ω):</label>
      <input type="range" id="freq" min="0.5" max="4" step="0.1" value="2.0">
      <span id="freqVal" class="val">2.0</span>
    </div>
    <div class="control-group">
      <label for="lambda">Wavelength (λ):</label>
      <input type="range" id="lambda" min="15" max="70" step="1" value="35">
      <span id="lambdaVal" class="val">35px</span>
    </div>
  </div>
  <div id="canvas-container">
    <canvas id="simCanvas"></canvas>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('simCanvas');
      const ctx = canvas.getContext('2d');
      const freqInput = document.getElementById('freq');
      const lambdaInput = document.getElementById('lambda');
      const freqVal = document.getElementById('freqVal');
      const lambdaVal = document.getElementById('lambdaVal');

      let width, height;
      let animId;
      let time = 0;
      const stepSize = 4;

      freqInput.addEventListener('input', (e) => freqVal.textContent = parseFloat(e.target.value).toFixed(1));
      lambdaInput.addEventListener('input', (e) => lambdaVal.textContent = e.target.value + 'px');

      function resize() {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = canvas.parentElement.clientHeight;
      }
      window.addEventListener('resize', resize);
      resize();

      function render() {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        const freq = parseFloat(freqInput.value);
        const wavelength = parseFloat(lambdaInput.value);
        const k = (2 * Math.PI) / wavelength;
        time += 0.04 * freq;

        const s1 = { x: width * 0.35, y: height * 0.5 };
        const s2 = { x: width * 0.65, y: height * 0.5 };

        for (let x = 0; x < width; x += stepSize) {
          for (let y = 0; y < height; y += stepSize) {
            const r1 = Math.hypot(x - s1.x, y - s1.y);
            const r2 = Math.hypot(x - s2.x, y - s2.y);

            const z1 = Math.sin(k * r1 - time);
            const z2 = Math.sin(k * r2 - time);
            const z = (z1 + z2) / 2;

            if (z > 0) {
              const alpha = Math.min(1, z * 0.8);
              ctx.fillStyle = `rgba(139, 92, 246, ${alpha})`;
            } else {
              const alpha = Math.min(1, Math.abs(z) * 0.8);
              ctx.fillStyle = `rgba(6, 182, 212, ${alpha})`;
            }
            ctx.fillRect(x, y, stepSize, stepSize);
          }
        }

        [s1, s2].forEach((src, idx) => {
          ctx.fillStyle = '#f8fafc';
          ctx.beginPath();
          ctx.arc(src.x, src.y, 6, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#c084fc';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(src.x, src.y, 10 + Math.sin(time * 2 + idx) * 3, 0, Math.PI * 2);
          ctx.stroke();
        });

        animId = requestAnimationFrame(render);
      }

      animId = requestAnimationFrame(render);

      window.addEventListener('beforeunload', () => {
        if (animId) cancelAnimationFrame(animId);
      });

      window.onerror = function(msg, url, line) {
        window.parent.postMessage({ type: 'SIM_ERROR', error: msg, line: line }, '*');
      };
    })();
  </script>
</body>
</html>"""
    }
}
