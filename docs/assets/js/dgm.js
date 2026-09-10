/* ==========================================================================
   dgm.js — the stepped diagram driver  (D94 · D115)

   A diagram is a STATE MACHINE, not a picture. The whole structure is on
   screen from frame one (D94 pattern 1); stepping changes only which parts
   are lit, and the caption under it says what changed (pattern 8).

   Why a class driver and not SMIL: D51's SMIL rules exist because SMIL is
   hard to get right — one <animate> per element, computed keyTimes, no
   fill="freeze" at staggered offsets. A stepped class + a CSS transition has
   none of those traps, gives prev/next/play for free, and is the same
   interaction the student already learned from SIMSCREEN (D95).

   Markup contract:
     <figure class="dgm" id="X" data-mode="loop|story" data-interval="4200">
       <div class="dgm-body"><svg>… <g class="st" data-step="2">…</g> …</svg></div>
       <div class="dgm-cap"><p></p></div>
     </figure>
   Anything with data-step is dimmed unless the current step is >= its value
   (accumulate) or == its value (spotlight), set per figure by data-reveal.
   ========================================================================== */
(function (w, d) {
  'use strict';

  var Dgm = {};

  Dgm.init = function (sel, steps) {
    var root = d.querySelector(sel);
    if (!root || !steps || !steps.length) return;

    var body    = root.querySelector('.dgm-body');
    var capP    = root.querySelector('.dgm-cap p');
    var mode    = root.getAttribute('data-mode') || 'loop';
    var reveal  = root.getAttribute('data-reveal') || 'upto';   // upto | only
    var interval= parseInt(root.getAttribute('data-interval'), 10) || 4600;
    var reduced = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* controls — built here so a figure's markup stays pure content */
    var ctl = d.createElement('div');
    ctl.className = 'dgm-ctl';
    ctl.innerHTML =
      '<button class="dgm-btn" type="button" data-a="prev">&larr; Prev</button>' +
      '<button class="dgm-btn play" type="button" data-a="play">&#9654; Play</button>' +
      '<button class="dgm-btn" type="button" data-a="next">Next &rarr;</button>' +
      '<span class="dgm-dots"></span>' +
      '<span class="dgm-count"></span>';
    root.insertBefore(ctl, root.querySelector('.dgm-cap'));

    var dots = ctl.querySelector('.dgm-dots');
    steps.forEach(function (s, k) {
      var b = d.createElement('button');
      b.type = 'button'; b.className = 'dgm-dot' + (s.key ? ' k' : '');
      b.setAttribute('aria-label', 'Step ' + (k + 1));
      b.addEventListener('click', function () { stop(); go(k); });
      dots.appendChild(b);
    });
    var countEl = ctl.querySelector('.dgm-count');
    var playBtn = ctl.querySelector('[data-a="play"]');

    var i = 0, timer = null, playing = false;

    function paint() {
      var s = steps[i];
      Array.prototype.forEach.call(body.querySelectorAll('[data-step]'), function (el) {
        var n = parseInt(el.getAttribute('data-step'), 10);
        var on = (reveal === 'only') ? (n === i + 1) : (n <= i + 1);
        el.classList.toggle('on', on);
        /* the CURRENT step is lit brighter than the ones it accumulated on */
        el.classList.toggle('cur', n === i + 1);
      });
      capP.innerHTML = s.en + (s.ar ? '<span class="ar">' + s.ar + '</span>' : '');
      root.classList.toggle('key', !!s.key);
      Array.prototype.forEach.call(dots.children, function (b, k) {
        b.classList.toggle('on', k === i);
      });
      countEl.textContent = (i + 1) + ' / ' + steps.length;
    }

    function go(n) { i = (n + steps.length) % steps.length; paint(); }
    function next() { go(i + 1); }

    function play() {
      if (playing || reduced) return;
      playing = true; playBtn.innerHTML = '&#10073;&#10073; Pause';
      timer = w.setInterval(next, interval);
    }
    function stop() {
      playing = false; playBtn.innerHTML = '&#9654; Play';
      if (timer) { w.clearInterval(timer); timer = null; }
    }

    ctl.addEventListener('click', function (e) {
      var a = e.target.getAttribute && e.target.getAttribute('data-a');
      if (a === 'prev') { stop(); go(i - 1); }
      else if (a === 'next') { stop(); next(); }
      else if (a === 'play') { playing ? stop() : play(); }
    });

    go(0);

    /* D103's lesson, applied here: a figure inside a hidden .page is not
       laid out, and a looping figure running there is wasted work that also
       desynchronises the moment the student arrives. Start on arrival. */
    if (w.IntersectionObserver) {
      new w.IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { if (mode === 'loop' && !reduced) { go(0); play(); } }
          else stop();
        });
      }, { threshold: 0.15 }).observe(root);
    } else if (mode === 'loop') { play(); }

    /* reduced motion: show every step's state at once and hide the controls,
       so the figure still teaches without moving (D94 pattern 10). */
    if (reduced) {
      Array.prototype.forEach.call(body.querySelectorAll('[data-step]'), function (el) {
        el.classList.add('on');
      });
      ctl.setAttribute('hidden', 'hidden');
      capP.innerHTML = steps.map(function (s) { return s.en; }).join(' ');
    }
  };

  w.Dgm = Dgm;
})(window, document);
