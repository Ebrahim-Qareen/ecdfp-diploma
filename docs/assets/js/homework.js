/* ============================================================================
   homework.js -- eCDFP Diploma
   #taskList checkboxes. Progress is in-memory for the session only -- nothing
   is written to browser storage, because the homework of record is the
   forensic report submitted to the instructor (D20/D21), not a tick in a page.
   ========================================================================= */
(function () {
  'use strict';

  var list = document.getElementById('taskList');
  if (!list) return;

  var counter = document.querySelector('[data-task-counter]');
  /* If the counter IS the list (or wraps it), the textContent write below
     replaces every <li> with "0 / 5" and the homework silently disappears.
     That shipped on three session pages. Refuse such a counter outright. */
  if (counter && (counter === list || counter.contains(list))) counter = null;

  function paint() {
    var items = [].slice.call(list.querySelectorAll('li'));
    var done = 0;
    items.forEach(function (li) {
      var cb = li.querySelector('input[type="checkbox"]');
      var on = !!(cb && cb.checked);
      li.classList.toggle('done', on);
      if (on) done += 1;
    });
    if (counter) counter.textContent = done + ' / ' + items.length;
  }

  list.addEventListener('change', function (e) {
    if (e.target && e.target.type === 'checkbox') paint();
  });

  document.addEventListener('ecdfp:task-added', paint);
  paint();
})();
