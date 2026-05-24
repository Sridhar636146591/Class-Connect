/* Campus Community Hub — Global Enhancements */

(function () {
  /* ── Cursor Glow ── */
  const glow = document.createElement('div');
  glow.className = 'cursor-glow';
  document.body.appendChild(glow);
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top  = e.clientY + 'px';
  });

  /* ── Particle Canvas ── */
  const canvas = document.createElement('canvas');
  canvas.id = 'particle-canvas';
  document.body.prepend(canvas);
  const ctx = canvas.getContext('2d');

  let W, H, particles = [];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const COLORS = ['rgba(124,111,255,', 'rgba(255,92,92,', 'rgba(0,229,192,', 'rgba(255,201,71,'];

  function spawn() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.4 + 0.4,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      alpha: Math.random() * 0.5 + 0.1,
      pulse: Math.random() * Math.PI * 2,
    };
  }

  for (let i = 0; i < 90; i++) particles.push(spawn());

  function draw() {
    ctx.clearRect(0, 0, W, H);
    const now = Date.now() / 1000;
    particles.forEach(p => {
      p.pulse += 0.012;
      const alpha = p.alpha * (0.7 + 0.3 * Math.sin(p.pulse));
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color + alpha + ')';
      ctx.fill();

      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > W || p.y < 0 || p.y > H) {
        p.x = Math.random() * W;
        p.y = Math.random() * H;
      }
    });

    // Draw faint lines between nearby particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 90) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = 'rgba(124,111,255,' + (0.06 * (1 - dist/90)) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();

  /* ── Scroll Reveal ── */
  const revealEls = document.querySelectorAll('.reveal, .list-card, .menu-box');
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('visible');
          obs.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(el => obs.observe(el));
  }

  /* ── Live Search Filter ── */
  const searchInput = document.getElementById('live-search');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const q = this.value.toLowerCase().trim();
      document.querySelectorAll('.list-card[data-searchable]').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }

  /* ── Button ripple ── */
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('button, input[type="submit"], .btn');
    if (!btn) return;
    const ripple = document.createElement('span');
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 1.5;
    ripple.style.cssText = `
      position:absolute; width:${size}px; height:${size}px;
      border-radius:50%;
      background:rgba(255,255,255,0.22);
      left:${e.clientX - rect.left - size/2}px;
      top:${e.clientY - rect.top - size/2}px;
      transform:scale(0); pointer-events:none;
      animation: rippleAnim 0.55s ease-out forwards;
    `;
    if (!document.getElementById('ripple-style')) {
      const s = document.createElement('style');
      s.id = 'ripple-style';
      s.textContent = '@keyframes rippleAnim{to{transform:scale(1);opacity:0;}}';
      document.head.appendChild(s);
    }
    btn.style.position = btn.style.position || 'relative';
    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });

  /* ── Auto-dismiss flash messages ── */
  document.querySelectorAll('.toast').forEach(t => {
    setTimeout(() => {
      t.style.animation = 'toastIn 0.35s reverse forwards';
      setTimeout(() => t.remove(), 400);
    }, 4000);
  });

  /* ── Page-load typing effect for h1 on splash ── */
  const splashH1 = document.querySelector('.splash-hero-title');
  if (splashH1) {
    const text = splashH1.getAttribute('data-text') || splashH1.textContent;
    splashH1.textContent = '';
    let i = 0;
    const type = () => {
      if (i < text.length) {
        splashH1.textContent += text[i++];
        setTimeout(type, 45);
      }
    };
    setTimeout(type, 500);
  }
})();
