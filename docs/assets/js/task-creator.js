/* ============================================================================
   task-creator.js -- eCDFP Diploma
   The "add a task" modal behind #taskList. Lets a student add their own
   follow-up during class. In-memory only, same reason as homework.js.
   ========================================================================= */
(function () {
  'use strict';

  var modal = document.getElementById('taskModal');
  var list  = document.getElementById('taskList');
  if (!modal || !list) return;

  var openBtn  = document.querySelector('[data-action="add-task"]');
  var form     = modal.querySelector('form');
  var input    = modal.querySelector('#taskText');
  var lastFocus = null;

  function open() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    if (input) { input.value = ''; input.focus(); }
  }

  function close() {
    modal.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function add(text) {
    var t = (text || '').trim();
    if (!t) return;

    var li = document.createElement('li');
    var id = 'task-' + Date.now();

    var cb = document.createElement('input');
    cb.type = 'checkbox'; cb.id = id;

    var label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = t;

    li.appendChild(cb);
    li.appendChild(label);
    list.appendChild(li);

    document.dispatchEvent(new CustomEvent('ecdfp:task-added', { detail: { text: t } }));
  }

  if (openBtn) openBtn.addEventListener('click', open);

  [].slice.call(modal.querySelectorAll('[data-action="close-modal"]')).forEach(function (b) {
    b.addEventListener('click', close);
  });

  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) { e.preventDefault(); close(); }
  });

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      add(input ? input.value : '');
      close();
    });
  }
})();
