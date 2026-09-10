/* ============================================================================
   quiz.js -- eCDFP Diploma
   In-page knowledge checks. Every question is multiple choice (D52) and gives
   immediate feedback. No score is kept and nothing is stored -- these are
   teaching checks, not assessment. Grading is the forensic report (D20).

   Two markups are accepted, because both shipped:

     A. <div class="q mcq">            (design_system.md 4.2)
          <ul class="opts"><li data-correct data-why="..."><label><input type=radio>..
          <div class="feedback"></div>

     B. <div class="q mcq" data-correct="c">   (every topic page P01-P14)
          <label><input type="radio" name="q1" value="a"> ...</label>
          <div class="feedback">why c is right</div>

   Markup B carried the answer in a .feedback that was visible from the start
   and had no handler at all -- the radios did nothing. The feedback is now
   hidden until the student answers, and the verdict is prefixed to it.
   ========================================================================= */
(function () {
  'use strict';

  function markupA(q, opts, fb) {
    opts.forEach(function (li) {
      var input = li.querySelector('input[type="radio"]');
      if (!input) return;
      input.addEventListener('change', function () {
        opts.forEach(function (o) { o.classList.remove('correct', 'wrong'); });
        opts.forEach(function (o) {
          var i = o.querySelector('input[type="radio"]');
          if (!i) return;
          if (o.hasAttribute('data-correct')) o.classList.add('correct');
          else if (i.checked) o.classList.add('wrong');
        });
        q.classList.add('answered');
        if (fb) {
          var chosen = li.hasAttribute('data-correct');
          fb.textContent = (chosen ? 'Correct. ' : 'Not quite. ') + (li.getAttribute('data-why') || '');
          fb.style.color = chosen ? 'var(--accent-green)' : 'var(--accent-amber)';
        }
      });
    });
  }

  function markupB(q, fb) {
    var labels = [].slice.call(q.querySelectorAll('label'));
    var answer = (q.getAttribute('data-correct') || '').trim().toLowerCase();
    var base = fb ? fb.innerHTML : '';
    if (!labels.length || !answer) return;

    labels.forEach(function (label) {
      var input = label.querySelector('input[type="radio"]');
      if (!input) return;
      input.addEventListener('change', function () {
        var ok = String(input.value).trim().toLowerCase() === answer;
        labels.forEach(function (o) {
          var i = o.querySelector('input[type="radio"]');
          o.classList.remove('correct', 'wrong');
          if (!i) return;
          if (String(i.value).trim().toLowerCase() === answer) o.classList.add('correct');
          else if (i.checked) o.classList.add('wrong');
        });
        q.classList.add('answered');
        q.classList.toggle('is-right', ok);
        q.classList.toggle('is-wrong', !ok);
        if (fb) {
          fb.innerHTML = '<span class="verdict">' +
            (ok ? 'Correct.' : 'Not quite &mdash; the answer is <b>' + answer + '</b>.') +
            '</span> ' + base;
        }
      });
    });
  }

  [].slice.call(document.querySelectorAll('.q.mcq')).forEach(function (q) {
    var fb   = q.querySelector('.feedback');
    var opts = [].slice.call(q.querySelectorAll('.opts li'));
    if (opts.length) markupA(q, opts, fb);
    else markupB(q, fb);
  });
})();
