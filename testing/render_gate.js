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

    return {
      docScroll: de.scrollWidth > de.clientWidth + 1,
      scrollW: de.scrollWidth, clientW: de.clientWidth,
      over, svgBad, pairing, pageCount, navCount, minWidthOK, activeCount,
      hrefs: [...document.querySelectorAll('[href], [src], [download]')]
              .map(e => e.getAttribute('href') || e.getAttribute('src'))
              .filter(Boolean)
    };
  });

  if (res.docScroll) fail(label, 'document horizontal overflow', `scrollWidth ${res.scrollW} > clientWidth ${res.clientW}`);
  res.over.forEach(o => fail(label, 'element wider than viewport outside a scroll container', o));
  res.svgBad.forEach(s => fail(label, 'SVG outside viewBox', s));
  res.pairing.forEach(p => fail(label, 'data-node / data-detail pairing', p));
  if (!res.minWidthOK) fail(label, 'load-bearing CSS missing', '.page-layout > * { min-width: 0 } is not in effect');
  if (res.pageCount && res.pageCount !== res.navCount) {
    fail(label, 'page count vs sidebar entries', `${res.pageCount} .page vs ${res.navCount} sidebar links`);
  }
  if (res.pageCount && res.activeCount !== 1) {
    fail(label, 'exactly one page visible', `${res.activeCount} pages carry .is-active`);
  }
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
