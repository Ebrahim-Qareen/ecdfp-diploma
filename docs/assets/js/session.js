/* ============================================================================
   session.js -- eCDFP Diploma
   Paged navigation, sidebar sync, keyboard shortcuts, break timer, and the
   data-node / data-detail diagram panels.
   Shared by every session page. Never inlined, never forked per session.
   ========================================================================= */
(function () {
  'use strict';

  var pages = [].slice.call(document.querySelectorAll('.page'));
  if (!pages.length) return;

  var links   = [].slice.call(document.querySelectorAll('.page-list a'));
  var prevBtn = document.querySelector('[data-nav="prev"]');
  var nextBtn = document.querySelector('[data-nav="next"]');
  var counter = document.querySelector('.page-nav .counter');
  var current = 0;

  function indexFromHash() {
    var m = /^#p(\d+)$/.exec(window.location.hash || '');
    if (!m) return 0;
    var i = parseInt(m[1], 10) - 1;
    return (i >= 0 && i < pages.length) ? i : 0;
  }

  function show(i, pushHash) {
    if (i < 0 || i >= pages.length) return;
    current = i;

    pages.forEach(function (p, n) {
      var on = n === i;
      p.classList.toggle('is-active', on);
      p.setAttribute('aria-hidden', on ? 'false' : 'true');
    });

    links.forEach(function (a, n) {
      if (n === i) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    if (prevBtn) prevBtn.disabled = (i === 0);
    if (nextBtn) nextBtn.disabled = (i === pages.length - 1);
    if (counter) counter.textContent = (i + 1) + ' / ' + pages.length;

    var active = links[i];
    if (active && active.scrollIntoView) {
      active.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }

    if (pushHash) {
      var id = pages[i].id || ('p' + (i + 1));
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', '#' + id);
      } else {
        window.location.hash = id;
      }
    }

    window.scrollTo(0, 0);
    startTimerFor(pages[i]);
    document.dispatchEvent(new CustomEvent('ecdfp:page', { detail: { index: i, page: pages[i] } }));
  }

  links.forEach(function (a, n) {
    a.addEventListener('click', function (e) { e.preventDefault(); show(n, true); });
  });
  if (prevBtn) prevBtn.addEventListener('click', function () { show(current - 1, true); });
  if (nextBtn) nextBtn.addEventListener('click', function () { show(current + 1, true); });

  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    if (document.querySelector('.modal:not([hidden])')) return;

    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); show(current + 1, true); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(current - 1, true); }
    else if (e.key === 'Home') { e.preventDefault(); show(0, true); }
    else if (e.key === 'End')  { e.preventDefault(); show(pages.length - 1, true); }
  });

  /* ------------------------------------------------------------ break timer */
  var tick = null;

  function startTimerFor(page) {
    if (tick) { clearInterval(tick); tick = null; }
    var card = page.querySelector('[data-timer]');
    if (!card) return;

    var mins = parseInt(card.getAttribute('data-timer'), 10);
    if (!(mins > 0)) return;

    var out = card.querySelector('.break-timer');
    if (!out) return;

    var left = mins * 60;

    function paint() {
      var m = Math.floor(left / 60), s = left % 60;
      out.textContent = m + ':' + (s < 10 ? '0' : '') + s;
    }
    paint();

    var toggleBtn = card.querySelector('[data-timer-action="toggle"]');
    var resetBtn  = card.querySelector('[data-timer-action="reset"]');

    function stop() {
      if (tick) { clearInterval(tick); tick = null; }
      if (toggleBtn) toggleBtn.textContent = 'Resume';
    }
    function start() {
      if (tick || left <= 0) return;
      if (toggleBtn) toggleBtn.textContent = 'Pause';
      tick = setInterval(function () {
        left -= 1;
        if (left <= 0) {
          left = 0;
          paint();
          clearInterval(tick); tick = null;
          card.classList.add('is-done');
          var done = card.getAttribute('data-timer-done');
          if (out) out.textContent = done || "Time's up";
          if (toggleBtn) toggleBtn.textContent = 'Start';
          return;
        }
        paint();
      }, 1000);
    }
    if (toggleBtn) toggleBtn.addEventListener('click', function () {
      if (tick) stop(); else { card.classList.remove('is-done'); start(); }
    });
    if (resetBtn) resetBtn.addEventListener('click', function () {
      stop();
      left = mins * 60;
      card.classList.remove('is-done');
      paint();
      if (toggleBtn) toggleBtn.textContent = 'Start';
    });
    start();
  }

  /* -------------------------------------------- data-node / data-detail panels
     Exactly one [data-detail] per [data-node]. The Part 9 gate asserts the
     pairing; this only wires up what is already correct.                     */
  function wireNodes(root) {
    var nodes = [].slice.call(root.querySelectorAll('[data-node]'));
    nodes.forEach(function (node) {
      var key = node.getAttribute('data-node');
      var panel = root.querySelector('[data-detail="' + (window.CSS && CSS.escape ? CSS.escape(key) : key) + '"]');
      if (!panel) return;

      node.setAttribute('role', node.getAttribute('role') || 'button');
      node.setAttribute('tabindex', node.getAttribute('tabindex') || '0');
      node.setAttribute('aria-pressed', 'false');
      node.setAttribute('aria-controls', panel.id || (panel.id = 'detail-' + key));
      panel.hidden = true;

      function toggle() {
        var open = panel.hidden;
        nodes.forEach(function (o) {
          var k = o.getAttribute('data-node');
          var p = root.querySelector('[data-detail="' + (window.CSS && CSS.escape ? CSS.escape(k) : k) + '"]');
          if (p) p.hidden = true;
          o.setAttribute('aria-pressed', 'false');
        });
        panel.hidden = !open;
        node.setAttribute('aria-pressed', open ? 'true' : 'false');
      }

      node.addEventListener('click', toggle);
      node.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
      });
    });
  }
  wireNodes(document);

  /* ---------------------------------------------- figure play controls (D51)
     Every animated figure sits behind an explicit control -- nothing here
     starts an animation on its own. SMIL binds to the DOM click event, and an
     SVG <g> has no .click() method, so Enter/Space dispatches a real
     MouseEvent rather than calling one.                                      */
  function wirePlay(root) {
    [].slice.call(root.querySelectorAll('.svg-play')).forEach(function (btn) {
      btn.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter' && e.key !== ' ') return;
        e.preventDefault();
        btn.dispatchEvent(new MouseEvent('click',
          { bubbles: true, cancelable: true, view: window }));
      });
    });
  }
  wirePlay(document);

  /* ------------------------------------------------------------------ print */
  var printBtn = document.querySelector('[data-action="print"]');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });

  /* ------------------------------------------------------------------- boot
     Navigating to #pN on an already-loaded document does not re-run this
     script, so the initial page is resolved here and on hashchange.         */
  show(indexFromHash(), false);
  window.addEventListener('hashchange', function () { show(indexFromHash(), false); });

  window.ECDFP = { show: show, get current() { return current; }, total: pages.length };
})();
