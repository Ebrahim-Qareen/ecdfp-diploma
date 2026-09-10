/* ============================================================================
   render_gate.js -- the Part 9 verification gate (render half).

   Usage:  node testing/render_gate.js <file-or-dir> [more...]
   Exit:   0 = zero findings, 1 = findings.

   TWO TRAPS, BOTH ALREADY PAID FOR (Part 9) -- encoded here as guards, not
   as comments, so they cannot be re-introduced silently:

     1. The Playwright option key is `viewport`, NOT `viewportSize`.
        `viewportSize` is silently ignored and the whole suite passes while
        proving nothing. assertOptionKey() below fails the run if the key
        ever drifts.
     2. Navigating to url#pN on an ALREADY-LOADED document does not re-run the
        page script. Every page under test gets its own full page.goto() with
        the hash, never a hash assignment on a live document.
   ========================================================================= */
'use strict';

const fs   = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const WIDTHS = [1400, 1100, 900, 700, 480];
const HEIGHT = 900;

/* ---- trap 1 guard --------------------------------------------------------
   Build the context options in one place and assert the key spelling. */
function contextOptions(width) {
  const opts = { viewport: { width, height: HEIGHT } };
  if (!('viewport' in opts) || 'viewportSize' in opts) {
    throw new Error('GATE ABORTED: option key must be `viewport`, not `viewportSize`.');
  }
  return opts;
}

const findings = [];
function fail(where, check, detail) { findings.push({ where, check, detail }); }

function collect(target) {
  const st = fs.statSync(target);
  if (st.isFile()) return [target];
  const out = [];
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith('.html')) out.push(p);
    }
  })(target);
  return out.sort();
}

async function auditOnePage(ctx, fileUrl, hash, label) {
  const page = await ctx.newPage();
  const consoleErrors = [];
  const netFailures = [];

  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => consoleErrors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => netFailures.push(r.url() + ' :: ' + (r.failure() || {}).errorText));
  page.on('response', r => { if (r.status() >= 400) netFailures.push(r.url() + ' :: HTTP ' + r.status()); });

  /* trap 2: a full load per page under test, hash included in the URL. */
  await page.goto(fileUrl + (hash || ''), { waitUntil: 'load' });
  await page.waitForTimeout(90);
  /* The SIMSCREEN ring animates into place (500ms), and place() can re-run when
     the figure scrolls into view -- so a fixed timeout is a guess that fails at
     some widths and not others. Wait for the ring to STOP MOVING instead: that
     is the condition the check actually needs, and it cannot go stale. */
  if (await page.$('.page.is-active .simscreen')) {
    await page.waitForFunction(() => {
      const r = document.querySelector('.page.is-active .ss-ring');
      if (!r) return true;
      const now = r.getBoundingClientRect().top;
      const was = window.__ringWas;
      window.__ringWas = now;
      return was !== undefined && Math.abs(now - was) < 0.5;
    }, { timeout: 4000, polling: 160 }).catch(() => {});
    await page.evaluate(() => { delete window.__ringWas; });
  }

  const res = await page.evaluate(() => {
    const de = document.documentElement;
    const vw = de.clientWidth;

    const over = [];
    document.querySelectorAll('body *').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      if (r.right <= vw + 1 && r.left >= -1) return;
      // allowed only inside a designated scroll container
      let p = el.parentElement, scroller = false;
      while (p && p !== document.body) {
        const pc = getComputedStyle(p);
        if (pc.overflowX === 'auto' || pc.overflowX === 'scroll') { scroller = true; break; }
        p = p.parentElement;
      }
      if (cs.position === 'fixed') return;
      if (!scroller) {
        over.push((el.tagName.toLowerCase()) + (el.className && typeof el.className === 'string'
          ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '')
          + ' [' + Math.round(r.left) + '..' + Math.round(r.right) + '] vw=' + vw);
      }
    });

    // SVG text escaping its viewBox
    const svgBad = [];
    document.querySelectorAll('svg[viewBox]').forEach((svg, i) => {
      const vb = svg.getAttribute('viewBox').trim().split(/[\s,]+/).map(Number);
      if (vb.length !== 4 || vb.some(isNaN)) { svgBad.push('svg#' + i + ' bad viewBox'); return; }
      const [vx, vy, vwB, vhB] = vb;
      svg.querySelectorAll('text, tspan, rect, circle, line, path, polygon, polyline').forEach(n => {
        let b; try { b = n.getBBox(); } catch (e) { return; }
        if (b.width === 0 && b.height === 0) return;
        const pad = 0.5;
        if (b.x < vx - pad || b.y < vy - pad ||
            b.x + b.width > vx + vwB + pad || b.y + b.height > vy + vhB + pad) {
          svgBad.push('svg#' + i + ' <' + n.tagName + '> ' +
            JSON.stringify({x:+b.x.toFixed(1),y:+b.y.toFixed(1),w:+b.width.toFixed(1),h:+b.height.toFixed(1)}) +
            ' outside viewBox ' + vb.join(' '));
        }
      });
    });

    // data-node <-> data-detail pairing
    const nodes = [...document.querySelectorAll('[data-node]')];
    const pairing = [];
    nodes.forEach(n => {
      const k = n.getAttribute('data-node');
      const m = document.querySelectorAll('[data-detail="' + (window.CSS && CSS.escape ? CSS.escape(k) : k) + '"]');
      if (m.length !== 1) pairing.push('data-node="' + k + '" has ' + m.length + ' matching data-detail (need exactly 1)');
    });
    [...document.querySelectorAll('[data-detail]')].forEach(d => {
      const k = d.getAttribute('data-detail');
      if (!document.querySelector('[data-node="' + (window.CSS && CSS.escape ? CSS.escape(k) : k) + '"]')) {
        pairing.push('orphan data-detail="' + k + '" with no data-node');
      }
    });

    // page count vs sidebar entry count
    const pageCount = document.querySelectorAll('.page').length;
    const navCount  = document.querySelectorAll('.page-list a').length;

    // the load-bearing rule must actually be in effect
    const pl = document.querySelector('.page-layout');
    let minWidthOK = true;
    if (pl) {
      minWidthOK = [...pl.children].every(c => {
        const mw = getComputedStyle(c).minWidth;
        return mw === '0px' || mw === '0';
      });
    }

    const activeCount = document.querySelectorAll('.page.is-active').length;

    /* D105 -- a container so narrow that the Arabic inside it cannot read.
       The bug always shows in a DIFFERENT column from the one that causes it,
       so the check is on the victim: any .ar whose available content width is
       under 260px on a screen wider than 700px is a starved column. */
    const pgActive = document.querySelector('.page.is-active');
    const arStarved = [];
    /* D108 -- the Arabic box must sit UNDER the English it explains: its box
       starts at the same edge the English starts at. Checked as a coordinate,
       because `margin-inline-end` silently resolves the wrong way on an rtl
       element and the rule then reads correct while doing the opposite. */
    const arDrift = [];
    if (pgActive && vw > 700) {
      pgActive.querySelectorAll('.ar').forEach(a => {
        /* D119 part dividers centre their title and their Arabic together.
           "Arabic starts where the English starts" is a rule about left-aligned
           prose; on a centred card both are centred, which is the same
           relationship expressed differently. */
        if (a.closest('.divider-inner')) return;
        const par = a.parentElement, ps = getComputedStyle(par);
        const avail = par.clientWidth - parseFloat(ps.paddingLeft) - parseFloat(ps.paddingRight);
        const lh = parseFloat(getComputedStyle(a).lineHeight) || 20;
        const lines = Math.round(a.getBoundingClientRect().height / lh);
        if (lines > 1 && avail < 260) {
          arStarved.push(pgActive.id + ' :: ' + Math.round(avail) + 'px container, ' +
                         lines + ' lines :: ' + a.textContent.slice(0, 40));
        }
        /* Assert the PAINTED TEXT, not the box. A full-width right-aligned .ar
           and a fit-content one both START their box at the parent's content
           edge -- the difference is where the glyphs land, so a box-edge check
           passes the very layout it is meant to reject (it did).
           Only single-line blocks discriminate: a wrapping .ar fills the
           column either way. getBoundingClientRect().left is the BORDER box, so
           the content edge is border + padding in -- miss the border and every
           .note reads as 3px adrift. */
        if (lines === 1) {
          const rng = document.createRange(); rng.selectNodeContents(a);
          const tr = rng.getBoundingClientRect();
          const contentLeft = par.getBoundingClientRect().left +
                              parseFloat(ps.borderLeftWidth) + parseFloat(ps.paddingLeft);
          const gap = Math.round(tr.left - contentLeft);
          if (gap > 3) {
            arDrift.push(pgActive.id + ' :: starts ' + gap + 'px right of the English it ' +
                         'explains :: ' + a.textContent.slice(0, 40));
          }
        }
      });
    }

    /* D107 -- every SIMSCREEN step must land its ring on its own target.
       Read the declared targets off the instance, never re-derive them. */
    const simBad = [];
    /* ONLY the visible page. A SIMSCREEN inside a hidden .page measures 0x0 and
       place() deliberately declines to run (D103) -- checking it there would
       fail 20 of 21 screens for doing the right thing. */
    (pgActive ? pgActive.querySelectorAll('.simscreen') : []).forEach(root => {
      const ring = root.querySelector('.ss-ring');
      const win  = root.querySelector('.wu.on');
      if (!ring || !win) { simBad.push(root.id + ' :: no ring or no visible screen'); return; }
      if (!win.getBoundingClientRect().width) return;   // not laid out yet
      const r = ring.getBoundingClientRect(), w = win.getBoundingClientRect();
      const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      if (cx < w.left - 4 || cx > w.right + 4 || cy < w.top - 4 || cy > w.bottom + 4) {
        simBad.push(root.id + ' :: ring at ' + Math.round(cx) + ',' + Math.round(cy) +
                    ' is outside its window');
        return;
      }
      /* the real assertion: the ring must sit on the element the step DECLARES
         it points at. "Inside the window" passes a 30px offset; this does not. */
      const tid = root.dataset.ssTarget;
      const tgt = tid && document.getElementById(tid);
      if (!tid) { simBad.push(root.id + ' :: step published no target (place() never ran)'); return; }
      if (!tgt) { simBad.push(root.id + ' :: declared target #' + tid + ' is not in the DOM'); return; }
      const t = tgt.getBoundingClientRect();
      if (cx < t.left - 6 || cx > t.right + 6 || cy < t.top - 6 || cy > t.bottom + 6) {
        simBad.push(root.id + ' :: ring at ' + Math.round(cx) + ',' + Math.round(cy) +
                    ' misses its target #' + tid + ' [' + Math.round(t.left) + '..' +
                    Math.round(t.right) + ' x ' + Math.round(t.top) + '..' + Math.round(t.bottom) + ']');
      }
      /* The spotlight must indicate the same place as the pointer (D107).
         Compare what place() COMPUTED for each, not the rendered ring: the ring
         animates over 500ms and place() can re-run when the figure scrolls into
         view, so a rendered frame measures the transition, not the maths. */
      const spot = (root.dataset.ssSpot || '').split(',').map(Number);
      const want = (root.dataset.ssRing || '').split(',').map(Number);
      if (spot.length === 2 && !spot.some(isNaN) && want.length === 2 && !want.some(isNaN)) {
        const d = Math.round(Math.hypot(spot[0] - want[0], spot[1] - want[1]));
        if (d > 6) {
          simBad.push(root.id + ' :: spotlight is ' + d + 'px from the pointer ' +
                      '(spot ' + spot[0] + ',' + spot[1] + ' vs ring ' + want[0] +
                      ',' + want[1] + ')');
        }
      }
    });

    /* ---- D124: ONE RIGHT EDGE ------------------------------------------
       Every block in the page flow must end at the same x. Three different
       right edges on one screen (1476 / 1298 / 1086) is what "empty space on
       the right" looks like, and no single rule was wrong -- `ch` caps
       resolve against each element's OWN font-size, so equal numbers give
       unequal pixels. The assertion is on the RESULT, which is the only
       place the defect is visible.
       Exempt by design: a divider is a centred title card, a photograph has
       a natural size, a SIMSCREEN window sits on a desktop (D117).         */
    const ragged = [];
    (function () {
      const pg = document.querySelector('.page.is-active');
      if (!pg) return;
      const EX = '.divider-inner, figure.photo, .kicker, .ss-holder';
      const seen = [];
      for (const el of pg.children) {
        if (el.matches(EX) || el.querySelector(EX)) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.display === 'inline') continue;
        const b = el.getBoundingClientRect();
        if (b.width < 40) continue;
        seen.push({ t: el.tagName.toLowerCase() + '.' + ((el.className||'').split(' ')[0]||''),
                    r: Math.round(b.right) });
      }
      if (seen.length < 2) return;
      const edges = seen.map(x => x.r);
      const spread = Math.max.apply(null, edges) - Math.min.apply(null, edges);
      if (spread > 2) {
        ragged.push(pg.id + ' :: ' + spread + 'px of ragged right edge -- ' +
                    seen.map(x => x.t + '@' + x.r).join(', '));
      }
    })();

    return {
      docScroll: de.scrollWidth > de.clientWidth + 1,
      scrollW: de.scrollWidth, clientW: de.clientWidth,
      over, svgBad, pairing, pageCount, navCount, minWidthOK, activeCount,
      arStarved, arDrift, simBad, ragged,
      hrefs: [...document.querySelectorAll('[href], [src], [download]')]
              .map(e => e.getAttribute('href') || e.getAttribute('src'))
              .filter(Boolean)
    };
  });

  if (res.docScroll) fail(label, 'document horizontal overflow', `scrollWidth ${res.scrollW} > clientWidth ${res.clientW}`);
  res.over.forEach(o => fail(label, 'element wider than viewport outside a scroll container', o));
  res.svgBad.forEach(s => fail(label, 'SVG outside viewBox', s));
  res.ragged.forEach(r => fail(label, 'ragged right edge (D124)', r));
  res.pairing.forEach(p => fail(label, 'data-node / data-detail pairing', p));
  if (!res.minWidthOK) fail(label, 'load-bearing CSS missing', '.page-layout > * { min-width: 0 } is not in effect');
  if (res.pageCount && res.pageCount !== res.navCount) {
    fail(label, 'page count vs sidebar entries', `${res.pageCount} .page vs ${res.navCount} sidebar links`);
  }
  if (res.pageCount && res.activeCount !== 1) {
    fail(label, 'exactly one page visible', `${res.activeCount} pages carry .is-active`);
  }
  (res.arStarved || []).forEach(a => fail(label, 'Arabic in a starved container (D105)', a));
  (res.arDrift   || []).forEach(a => fail(label, 'Arabic not under its English (D108)', a));
  (res.simBad    || []).forEach(a => fail(label, 'SIMSCREEN pointer off its window (D107)', a));
  consoleErrors.forEach(e => fail(label, 'console error', e));
  netFailures.forEach(e => fail(label, 'failed request', e));

  await page.close();
  return res;
}

(async () => {
  const targets = process.argv.slice(2);
  if (!targets.length) { console.error('usage: node testing/render_gate.js <file-or-dir> ...'); process.exit(2); }

  const files = targets.flatMap(collect);
  if (!files.length) { console.error('no .html files found'); process.exit(2); }

  const browser = await chromium.launch();
  console.log('Part 9 render gate — widths ' + WIDTHS.join(' / ') + ' (option key: viewport)\n');

  for (const f of files) {
    const url = 'file://' + path.resolve(f);
    console.log('  ' + f);

    // discover page ids once, at the widest width
    const probeCtx = await browser.newContext(contextOptions(WIDTHS[0]));
    const probe = await probeCtx.newPage();
    await probe.goto(url, { waitUntil: 'load' });
    const ids = await probe.evaluate(() => [...document.querySelectorAll('.page')].map(p => p.id));
    await probe.close(); await probeCtx.close();

    for (const w of WIDTHS) {
      const ctx = await browser.newContext(contextOptions(w));
      if (!ids.length) {
        await auditOnePage(ctx, url, '', `${path.basename(f)} @${w}`);
      } else {
        // trap 2: reload per page, never a hash change on a live document
        for (const id of ids) {
          await auditOnePage(ctx, url, '#' + id, `${path.basename(f)}#${id} @${w}`);
        }
      }
      await ctx.close();
      console.log(`    ${String(w).padStart(4)}px  ${ids.length || 1} page(s) checked`);
    }
  }

  await browser.close();

  console.log('\n' + '='.repeat(70));
  if (!findings.length) {
    console.log('RENDER GATE: PASS — zero findings');
    process.exit(0);
  }
  console.log(`RENDER GATE: FAIL — ${findings.length} finding(s)\n`);
  const byCheck = {};
  findings.forEach(f => { (byCheck[f.check] = byCheck[f.check] || []).push(f); });
  for (const [check, list] of Object.entries(byCheck)) {
    console.log(`  [${list.length}] ${check}`);
    list.slice(0, 6).forEach(f => console.log(`        ${f.where} :: ${f.detail}`));
    if (list.length > 6) console.log(`        ... and ${list.length - 6} more`);
  }
  process.exit(1);
})().catch(e => { console.error('GATE ERROR:', e); process.exit(2); });
