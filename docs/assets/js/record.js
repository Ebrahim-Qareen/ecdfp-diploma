/* ============================================================================
   record.js -- eCDFP Diploma - cumulative Chain-of-Custody record engine.

   One unbroken custody record per case. Each session's record page shows every
   earlier session's custody entries collapsed at the top ("carried forward"),
   with the current session open. The chain runs seizure -> acquisition ->
   examination -> report as one continuous document.

   Storage is SHARED across every record page on this origin under one key
   (`ecdfp-case-file`), so what a student records in an early session already
   appears in later sessions on the same browser. Saving MERGES -- a page only
   writes the ids it shows, never wiping another session's entries. Namespaced
   ids (`s1-...`, `s2-...`) keep the chain accumulating without collision.
   Nothing is uploaded. The exported HTML/PDF is the record of authority.

   Markup contract:
     <... data-record="s1" data-record-title="..." data-current="s1">
       .rec-head    inputs with [data-field] + [data-label]      (case header, filled once)
       .rec-bar     [data-progress] [data-progress-bar] [data-saved] + export/clear buttons
       [data-gate="s1-auth"]  the authorization-gate warning (references the gate step's id)
       [data-record-body] > .rec-group            (details = carried-forward | section = current)
          each .rec-group has [data-group-title]; inside: .rec-sec | .rec-step | .rec-free
          .rec-step has input[data-check] (+ [data-active][data-current] on the current
             session's active steps), a .rec-name, optional .rec-cmd, a .rec-detail panel
             revealed by .rec-toggle, and a textarea[data-notes]
          .rec-free is a free-text block (e.g. the custody-transfer log) with [data-notes]
   ========================================================================== */
(function () {
  'use strict';

  var root = document.querySelector('[data-record]');
  if (!root) return;

  var KEY = 'ecdfp-case-file';                        // shared across every record page on this origin
  var CUR = root.getAttribute('data-current') || '';  // current session prefix, e.g. "s1"

  var fields = [].slice.call(root.querySelectorAll('[data-field]'));
  var checks = [].slice.call(root.querySelectorAll('input[data-check]'));
  var notes  = [].slice.call(root.querySelectorAll('[data-notes]'));

  /* ---------- shared, merge-safe storage ---------------------------------- */
  function loadRaw() {
    try { var r = localStorage.getItem(KEY); return r ? JSON.parse(r) : null; }
    catch (e) { return null; }
  }
  function save() {
    var s = loadRaw() || {}; s.f = s.f || {}; s.c = s.c || {}; s.n = s.n || {};
    fields.forEach(function (el) { s.f[el.getAttribute('data-field')] = el.value; });
    checks.forEach(function (el) { s.c[el.getAttribute('data-check')] = el.checked; });
    notes.forEach(function (el)  { s.n[el.getAttribute('data-notes')]  = el.value; });
    try { localStorage.setItem(KEY, JSON.stringify(s)); flash(); } catch (e) {}
    updateProgress(); refreshGate();
  }
  function load() {
    var s = loadRaw();
    if (s) {
      fields.forEach(function (el) { var k = el.getAttribute('data-field'); if (s.f && k in s.f) el.value = s.f[k]; });
      checks.forEach(function (el) { var k = el.getAttribute('data-check'); if (s.c && k in s.c) el.checked = !!s.c[k]; syncStep(el); });
      notes.forEach(function (el)  { var k = el.getAttribute('data-notes'); if (s.n && k in s.n) el.value = s.n[k]; autoGrow(el); });
    }
    updateProgress(); refreshGate();
  }

  function syncStep(cb) { var step = cb.closest('.rec-step'); if (step) step.classList.toggle('done', cb.checked); }

  /* ---------- progress (all steps shown on the page) ---------------------- */
  var pill = root.querySelector('[data-progress]');
  var bar  = root.querySelector('[data-progress-bar]');
  function updateProgress() {
    var total = checks.length, done = 0;
    checks.forEach(function (el) { if (el.checked) done++; });
    if (pill) pill.textContent = done + ' / ' + total + ' steps';
    if (bar)  bar.style.width = total ? (100 * done / total).toFixed(1) + '%' : '0%';
  }

  /* ---------- authorization gate ------------------------------------------
     Only the CURRENT session's active steps are gated, and only against the
     current session's own authorization step. Tick an active step before the
     authorization is signed off and the warning shows. */
  var gate = root.querySelector('[data-gate]');
  function refreshGate() {
    if (!gate) return;
    var authBox = root.querySelector('input[data-check="' + gate.getAttribute('data-gate') + '"]');
    var ok = authBox && authBox.checked;
    var jumped = checks.some(function (el) {
      return el.hasAttribute('data-active') && el.hasAttribute('data-current') && el.checked && !ok;
    });
    gate.classList.toggle('show', !!jumped);
  }

  /* ---------- saved flash -------------------------------------------------- */
  var saved = root.querySelector('[data-saved]'), st;
  function flash() {
    if (!saved) return;
    saved.classList.add('show');
    clearTimeout(st);
    st = setTimeout(function () { saved.classList.remove('show'); }, 1200);
  }

  /* ---------- expand / collapse a step's reference panel ------------------- */
  [].forEach.call(root.querySelectorAll('.rec-step .rec-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var step = btn.closest('.rec-step');
      btn.setAttribute('aria-expanded', step.classList.toggle('open') ? 'true' : 'false');
    });
  });

  function autoGrow(el) {
    if (!el || el.tagName !== 'TEXTAREA') return;
    el.style.height = 'auto';
    el.style.height = (el.scrollHeight + 2) + 'px';
  }

  fields.forEach(function (el) { el.addEventListener('input', save); });
  notes.forEach(function (el)  { el.addEventListener('input', function () { autoGrow(el); save(); }); });
  checks.forEach(function (el) { el.addEventListener('change', function () { syncStep(el); save(); }); });

  /* ---------- cumulative export (in session order) ------------------------- */
  function esc(s) { return (s || '').replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function nl2br(s) { return esc(s).replace(/\n/g, '<br>'); }
  function slug(s) { return (s || '').trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40); }

  var EXPORT_CSS =
    'body{font:14px/1.62 "Segoe UI",-apple-system,Roboto,Arial,sans-serif;color:#1a1f2b;background:#fff;max-width:900px;margin:30px auto;padding:0 26px}' +
    '.doc-h{border-bottom:3px solid #0a63b0;padding-bottom:12px;margin:0 0 6px}' +
    '.doc-h h1{font-size:22px;margin:0 0 4px;letter-spacing:-.01em}' +
    '.doc-h .sub{color:#5b6675;font-size:12.5px}' +
    '.stamp{background:#f4f7fb;border:1px solid #d8e0ea;border-left:3px solid #0a63b0;border-radius:0 5px 5px 0;padding:9px 13px;margin:12px 0 6px;font-size:12px;color:#33405a}' +
    'h2{font-size:16.5px;margin:26px 0 6px;color:#12233b;border-bottom:1px solid #e3e7ec;padding-bottom:5px}' +
    'h3{font-size:13px;margin:18px 0 8px;color:#0a63b0;letter-spacing:.4px;text-transform:uppercase}' +
    'h4{font-size:13.5px;margin:16px 0 6px}' +
    'table.meta{border-collapse:collapse;margin:12px 0 4px;font-size:13px;width:100%}' +
    'table.meta th{text-align:left;padding:5px 16px 5px 0;color:#54606f;font-weight:600;vertical-align:top;white-space:nowrap;width:1%}' +
    'table.meta td{padding:5px 0;border-bottom:1px solid #eef1f5}' +
    '.step{margin:0 0 13px;padding:0 0 11px;border-bottom:1px solid #eceff3}' +
    '.s-h{margin:0 0 6px;font-weight:600;font-size:14px}' +
    '.s-h .bx{display:inline-block;width:15px;height:15px;line-height:15px;text-align:center;border:1px solid #9aa4b2;border-radius:3px;margin-right:8px;font-size:11px;color:#0a7d3c;vertical-align:baseline}' +
    '.step.done .s-h .bx{background:#0a7d3c;border-color:#0a7d3c;color:#fff}' +
    '.step .cmd{font-family:Consolas,monospace;font-size:12px;color:#0a4f8a;background:#f2f5f9;border:1px solid #e0e6ee;border-radius:4px;padding:1px 7px}' +
    '.s-f{white-space:normal;font-size:13px;color:#26303f;background:#f7f9fb;border-left:3px solid #0a63b0;padding:8px 12px;border-radius:0 5px 5px 0;margin-top:6px}' +
    '.s-f em{color:#98a2b3}' +
    '.free{background:#f7f9fb;border:1px solid #e0e6ee;border-left:3px solid #0a63b0;border-radius:0 5px 5px 0;padding:10px 13px;margin:0 0 10px}' +
    '.free .s-f{background:#fff;border-left-color:#c9d3df}' +
    'footer{margin-top:32px;padding-top:12px;border-top:1px solid #e3e7ec;color:#8a94a2;font-size:11px}' +
    '.auth{margin-top:26px;padding-top:12px;border-top:2px solid #0a63b0}' +
    '.auth .cert{font-size:12.5px;color:#54606f;margin:0 0 18px}' +
    '.sig{display:flex;gap:40px;flex-wrap:wrap}' +
    '.sig>div{flex:1 1 240px}' +
    '.sig .ln{display:block;border-bottom:1px solid #333;height:28px;margin-bottom:5px}' +
    '.sig .lb{font-size:11.5px;color:#54606f}' +
    '.runfoot{display:none}' +
    '@media print{.runfoot{display:block;position:fixed;bottom:5mm;left:0;right:0;font-size:10px;' +
    'color:#8a94a2;border-top:1px solid #e3e7ec;padding-top:4px}' +
    '.step,.free,.auth{break-inside:avoid}}';

  function emitStep(node, out) {
    var cb = node.querySelector('[data-check]'), done = cb && cb.checked;
    var name = (node.querySelector('.rec-name') || {}).textContent || '';
    var cmd  = (node.querySelector('.rec-cmd')  || {}).textContent || '';
    var note = (node.querySelector('[data-notes]') || {}).value || '';
    out.push('<div class="step' + (done ? ' done' : '') + '">');
    out.push('<p class="s-h"><span class="bx">' + (done ? '&#10003;' : '&nbsp;') + '</span>' + esc(name.trim()) +
             (cmd ? ' <span class="cmd">' + esc(cmd.trim()) + '</span>' : '') + '</p>');
    out.push('<div class="s-f">' + (note ? nl2br(note) : '<em>&mdash; not recorded &mdash;</em>') + '</div>');
    out.push('</div>');
  }

  function buildExport() {
    var title = root.getAttribute('data-record-title') || document.title;
    var out = ['<div class="doc-h"><h1>' + esc(title) + '</h1>' +
               '<div class="sub">Chain-of-Custody Record &middot; eCDFP Diploma &middot; ITGate Academy</div></div>'];
    out.push('<div class="stamp">This exported document is the record of authority for submission. ' +
             'The browser-saved copy is a working copy only (per browser, not synced between devices).</div>');

    var meta = [];
    fields.forEach(function (el) {
      var label = el.getAttribute('data-label') || el.getAttribute('data-field');
      if (el.value) meta.push('<tr><th>' + esc(label) + '</th><td>' + nl2br(el.value) + '</td></tr>');
    });
    if (meta.length) out.push('<table class="meta">' + meta.join('') + '</table>');

    var groups = root.querySelectorAll('[data-record-body] .rec-group');
    [].forEach.call(groups, function (g) {
      out.push('<h2>' + esc(g.getAttribute('data-group-title') || '') + '</h2>');
      [].forEach.call(g.querySelectorAll('.rec-sec, .rec-step, .rec-free'), function (node) {
        if (node.classList.contains('rec-sec')) {
          out.push('<h3>' + esc(node.textContent.replace(/\s+/g, ' ').trim()) + '</h3>');
        } else if (node.classList.contains('rec-step')) {
          emitStep(node, out);
        } else { // rec-free
          var lab = (node.querySelector('.rec-free-label') || {}).textContent || '';
          var val = (node.querySelector('[data-notes]') || {}).value || '';
          out.push('<div class="free"><h4>' + esc(lab.trim()) + '</h4>' +
                   '<div class="s-f">' + (val ? nl2br(val) : '<em>&mdash; not recorded &mdash;</em>') + '</div></div>');
        }
      });
    });

    /* case-level blocks — the custody-transfer log and the disposition of
       originals and derivative works (SWGDE 18-Q-002 §5.6). One per case, not
       per session, so the chain reads as one continuous record. */
    var caseBlocks = root.querySelectorAll('[data-case-blocks] .rec-free');
    if (caseBlocks.length) {
      out.push('<h2>Case record</h2>');
      [].forEach.call(caseBlocks, function (node) {
        var lab = (node.querySelector('.rec-free-label') || {}).textContent || '';
        var val = (node.querySelector('[data-notes]') || {}).value || '';
        out.push('<div class="free"><h4>' + esc(lab.trim()) + '</h4>' +
                 '<div class="s-f">' + (val ? nl2br(val) : '<em>&mdash; not recorded &mdash;</em>') + '</div></div>');
      });
    }

    /* authorization — SWGDE 18-Q-002 §5.7: the authorizer's name and signature */
    var exName = (root.querySelector('[data-field="examiner"]') || {}).value || '';
    out.push('<div class="auth"><h2>Authorization</h2>' +
      '<p class="cert">I certify that the entries above are a true and complete record of my handling and ' +
      'examination of this item, and that the chain of custody is unbroken except where expressly noted.</p>' +
      '<div class="sig">' +
      '<div><span class="ln"></span><span class="lb">' + (exName ? esc(exName) : 'Examiner') + ' &mdash; signature</span></div>' +
      '<div><span class="ln"></span><span class="lb">Date</span></div>' +
      '</div></div>');

    var caseRef = (root.querySelector('[data-field="case_id"]') || {}).value || '';

    return '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<title>' + esc(title) + '</title><style>' + EXPORT_CSS + '</style></head><body>' +
      out.join('\n') +
      '<footer>Generated ' + esc(new Date().toLocaleString()) + ' &middot; eCDFP Chain-of-Custody Record &middot; ITGate Academy' +
      '<br>Structure follows SWGDE 18-Q-002, SWGDE 18-F-002 and ISO/IEC 27037.</footer>' +
      '<div class="runfoot">' + (caseRef ? 'Case ' + esc(caseRef) + ' &middot; ' : '') +
      'Chain-of-Custody Record &middot; ' + esc(title) + '</div>' +
      '</body></html>';
  }

  function download() {
    var caseField = root.querySelector('[data-field="case_id"]');
    var name = 'eCDFP-CoC-' +
      (slug(caseField && caseField.value) || new Date().toISOString().slice(0, 10)) + '.html';
    var blob = new Blob([buildExport()], { type: 'text/html' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 200);
  }
  var dl = root.querySelector('[data-export-html]'); if (dl) dl.addEventListener('click', download);
  var pf = root.querySelector('[data-export-pdf]');  if (pf) pf.addEventListener('click', function () { window.print(); });

  /* ---------- clear THIS session only (two-click confirm, no browser dialog)
     Earlier sessions' custody entries are never touched -- you do not silently
     erase a chain. */
  var clr = root.querySelector('[data-clear]');
  if (clr) {
    var armed = false, ct, original = clr.textContent;
    clr.addEventListener('click', function () {
      if (!armed) {
        armed = true; clr.textContent = 'Erase this session?'; clr.classList.add('arm');
        ct = setTimeout(function () { armed = false; clr.textContent = original; clr.classList.remove('arm'); }, 3000);
        return;
      }
      clearTimeout(ct); armed = false; clr.textContent = original; clr.classList.remove('arm');
      var s = loadRaw() || { f: {}, c: {}, n: {} }; s.c = s.c || {}; s.n = s.n || {};
      checks.forEach(function (el) {
        if (el.hasAttribute('data-current')) { el.checked = false; syncStep(el); delete s.c[el.getAttribute('data-check')]; }
      });
      notes.forEach(function (el) {
        var k = el.getAttribute('data-notes');
        if (CUR && k.indexOf(CUR + '-') === 0) { el.value = ''; autoGrow(el); delete s.n[k]; }
      });
      try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
      updateProgress(); refreshGate();
    });
  }

  load();
})();
