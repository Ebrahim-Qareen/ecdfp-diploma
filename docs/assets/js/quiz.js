/* ============================================================================
   quiz.js -- eCDFP Diploma
   In-page knowledge checks. Mixed .q.mcq (immediate feedback) and
   <details class="q reveal"> (free recall). No score is kept and nothing is
   stored -- these are teaching checks, not assessment. Grading is the
   forensic report (D20).
   ========================================================================= */
(function () {
  'use strict';

  [].slice.call(document.querySelectorAll('.q.mcq')).forEach(function (q) {
    var opts = [].slice.call(q.querySelectorAll('.opts li'));
    var fb   = q.querySelector('.feedback');
    if (!opts.length) return;

    opts.forEach(function (li) {
      var input = li.querySelector('input[type="radio"]');
      if (!input) return;

      input.addEventListener('change', function () {
        opts.forEach(function (o) { o.classList.remove('correct', 'wrong'); });

        opts.forEach(function (o) {
          var i = o.querySelector('input[type="radio"]');
          if (!i) return;
          var right = o.hasAttribute('data-correct');
          if (right) o.classList.add('correct');
          else if (i.checked) o.classList.add('wrong');
        });

        if (fb) {
          var chosen = li.hasAttribute('data-correct');
          var why = li.getAttribute('data-why') || '';
          fb.textContent = (chosen ? 'Correct. ' : 'Not quite. ') + why;
          fb.style.color = chosen ? 'var(--accent-green)' : 'var(--accent-amber)';
        }
      });
    });
  });
})();
