# P01 · Build log

**Built 2026-09-08.** First page of the `D70`–`D99` rebuild, and the first page built under the
topic architecture.

---

## What was built

| # | Document | Lines | Note |
|--:|---|---:|---|
| 1 | `instructor_guide.md` | 234 | |
| 2 | `student_guide.md` | 159 | bilingual |
| 3 | `guided_lab.md` | 130 | bilingual · **6 steps = `SIMSCREEN T01-1`** |
| 4 | `student_activity.md` | 79 | bilingual · two sorts + the triple |
| 5 | `quiz.md` | 10 Q | bilingual stems, English options |
| 6 | `quiz_answer_key.md` | 23 | every answer justified |
| 7 | `homework.md` | 57 | bilingual |
| 8 | `homework_answer_key.md` | 47 | model triple + marking bands |
| 9 | `report_stage.md` | 101 | §1 · §3 complete, §6 one row, §8/§9 shaped |
| 10 | `instructor_script_ar.md` | 222 | six fixed sections |
| 11 | `build_log.md` | this | |

**Eleven of eleven.**

---

## What was verified

- Minutes re-parsed from `design/topic_map.md`: `T01` 45 + `T02` 25 = **70**.
- Part split totals 45 and 25; theory **31 %** and **32 %**, both inside `D79`'s 35 % ceiling.
- `guided_lab.md`: 6 steps, 6 *expected result* rows, 6 *verify* rows, **exactly one 🔑 key step**.
- `quiz.md`: 10 questions, 10 bilingual stems, options English.
- `instructor_script_ar.md`: 6 sections, matching `D77`.
- Evidence gate: **`T01` and `T02` require no evidence set.** `P01` is one of only three pages that
  can be built before the acquisition run.

---

## Decisions taken during the build

### 1 · The outline's own minute split was wrong, and was corrected before writing

The approved outline gave theory 16 min for material the previous S1 guide spent **47 minutes**
lecturing (`S1-01` 15 + `S1-02` 20 + `S1-03` 12). Compressing the lecture would have failed.

**The fix was structural, not editorial:** two of those three blocks are *judgement*, and judgement
is taught by making the student judge. The may/may-not claim table and the entire three-part
admissibility test moved into the independent part.

New split `14 / 15 / 12 / 4`. **Theory 31 %.** This is better teaching, not a compromise to satisfy
a rule — and it is why the independent part of `T01` is two sorting exercises rather than a lab.

### 2 · `D81` invalidated a teaching argument in the source material

The old S1 instructor guide used the Linux column of the cross-platform table as *"the argument for
the Windows-weighted syllabus"*, citing `D38` — Linux out of scope.

**`D81` reversed `D38`.** The table survives; the conclusion changed to *"why the taught course is
Windows-weighted, and where the rest lives"*. The instructor script carries an explicit answer for
the question, because a student will ask it and *"out of scope"* is now a wrong answer.

### 3 · A "no figure here" note was overridden, with a reason

The old guide argued against a diagram for `S1-03`: *"a diagram that only re-labels the bullets
beside it has failed."* Correct.

`P01-F1` is kept because it carries something the table cannot: **who owns each test**, revealed as
the spotlight walks, ending on the fact that **only authenticity is the examiner's**. If that
dimension is ever dropped from the figure, the figure goes with it.

### 4 · The report template collision (`D99`)

`T02` teaches the template, and the template in the repo had **10 sections** against `D85`'s **12**.
Adopted the 12 and re-pointed the `D20` rubric in the same change. Canonical source is now
`design/report_template.md`; `packages/session-01/report_template.md` was deleted.

---

## What is still open

| | |
|---|---|
| ⚠️ **The worked model report is not written.** | `D85` rule 2 — a complete model, **on a different case from the student's**. `T02` is where students first ask for it. The `docs/report/` page carries the structure and one worked triple, which is enough to teach from |
| ⚠️ **`TOOLS.sha256` has never actually been generated.** | `scripts/install/make_tools_manifest.ps1` is written and `labs/setup_guide.md` Step 8 calls it — but it has not been run on a real `FOR-WS01`. **Run it before the first class**, or the lab still stops at step 1 |
| ⚠️ **The page has not been render-gated.** | Part 9 at 1400/1100/900/700/480, then `density_gate.py`. The structural check (26 assertions) passes; the visual one has not run |
| ⚠️ **`density_gate.py` has not been updated for `D78`.** | It still counts all visible words, including Arabic. Until it is fixed it will fail every bilingual page for the wrong reason |

## Closed since the first pass

| | |
|---|---|
| ✅ Page built | `docs/page-01/index.html` — **21 screens** (`D101`), 25/25 structural checks pass. First built as one 504-line scroll; rebuilt as a deck after review — see `D101` |
| ✅ `SIMSCREEN T01-1` built | 6 recreated screens, 6 steps, one key step, all bilingual, hotspots DOM-resolved |
| ✅ `P01-F1` · `P01-F2` · `P01-F3` built | `D94` patterns 2/3 and 5, as the new `.cmp` component in `ecdfp.css` §22 |
| ✅ `docs/report/` exists | generated from `design/report_template.md` |
| ✅ `TOOLS.sha256` blocker addressed | generator script + `setup_guide.md` Step 8 |
| ✅ Card is live | `docs/index.html` and `docs/roadmap.html` link `P01`; `docs/session-01/` deleted (`D90`) |

## Three things found by rendering, not by reading

The structural check passed 25/25 while the page was visibly wrong twice. Screenshots caught what
assertions could not:

1. **The page was one long scroll.** Rebuilt as **21 screens** (`D101`).
2. **The Arabic was thrown to the far right** of a 1136 px column. `margin-inline-end` resolves
   against the element's own `rtl` direction, so it pushed the opposite way (`D102`).
3. **Every SIMSCREEN pointer sat in the corner.** A figure inside a hidden screen measures 0x0
   (`D103`).

**Render the page before calling it done.** Playwright at `file://` + a coordinate assertion is
cheap and it is the only thing that caught any of these.

## Density, measured correctly

| | |
|---|---|
| Total English words | **2 977** (limit 4 000) |
| Average per screen | **141** (limit 180) |
| Screens over 250 prose words | **none** |

Measured the `D78` way: Arabic excluded (it is a parallel track, not extra content), and `.wu`
recreated screens and `.cmp` figures excluded (they are figures, not prose). A naive count that
includes them reports two screens "over" and both are false positives — worth knowing before
`density_gate.py` is updated.

## Two components were added to the kit during this build

Both because the page needed them and `D96` says a page supplies screens and steps, never CSS:

- **`ecdfp.css` §22 `.cmp`** — the `D94` parallel-rows + spotlight comparison figure. Looping, no
  button, `prefers-reduced-motion` renders every row at once.
- **`win-ui.css` §12 `.wu-snaptree`** — VMware snapshot lineage. Reusable: snapshot state returns in
  `T06`, `T09` and every case reset.

`P01` was the first real test of whether `win-ui.css` could carry a **non-dialog application**. It
could: the VMware window is title bar + menu bar + two stacked dropdowns + status bar, all existing
components.

## One thing found that was not a `P01` problem

`docs/resources/report.html` published a **third** report template — 7 sections. See `D100`.

## Layout pass 2026-09-08 — four defects, all found by rendering, none by reading

Ebrahim's note was *"there is space left and right — make it one line, not two, on every page."*
That reads like a measure problem. It was not; widening the measure changed nothing. Four separate
bugs, each invisible in the source:

1. **`text-wrap:nowrap` on every first table cell (`D105`).** Written for short label columns,
   applied to prose ones — and it swallowed the Arabic explanation too, so the cell's max-content
   width became one enormous line. `p10`'s two-column table resolved to **849 px / 179 px**; the
   right cell wrapped its Arabic to **seven lines**. Now **500 px / 520 px**.
   *The symptom was in the second column; the bug was in the first.*
2. **`.ar` was `width:fit-content` (`D106`).** Its start edge — the right one, where an Arabic
   reader begins — landed at 1094 px in one block and 799 px in the next. Now a full-width
   right-aligned block, so the hairline runs as one straight rule down the page.
3. **The sidebar held 210 px between 900 px and 1099 px (`D105`).** In that band a two-column table
   got ~223 px per cell. The sidebar now collapses at 1099 px; the deck nav loses nothing.
4. **The SIMSCREEN pointer (`D107`).** A `+30` in `simscreen.js` compensating for an `inset:-30px`
   in `simscreen.css` — so the spotlight had been 30 px off its target at **every** width since it
   was built. And `transform:scale` on narrow screens became `zoom`, which broke the hotspot maths
   a second way: `getBoundingClientRect()` is zoomed, `style.left` is not, so the pointer landed at
   *z × z* and pointed at **NetworkMiner** instead of the selected **TOOLS.sha256**.

**All four are now asserted, not remembered.** Three checks added to `testing/render_gate.js`,
mutation-tested the same day: **6 of 7 injected defects caught**, the seventh a non-defect
(`testing/README.md` has the table). The two SIMSCREEN assertions are behavioural — the pointer
must land on the element the step *declares*, and the spotlight must indicate the same place as the
pointer. The first version only checked "the ring is inside the window somewhere", which is exactly
what let a 30 px offset ship.

**Result:** `node testing/render_gate.js docs/page-01/index.html` → **PASS, zero findings** at
1400 / 1100 / 900 / 700 / 480.

**Standing lesson, now paid for twice:** render the page and assert a coordinate. Every one of
these passed the structural check. None of them survived a screenshot.


### Reversal the same day — `D108`

`D106` (full-width right-aligned `.ar`) was **reverted after Ebrahim saw it**. It fixed a real
measurement — the Arabic's start edge moved from block to block — with a cure that cost more than
the defect: on a wide column the explanation landed at the far right, level with nothing. What a
reader looks for is **the line above**, not a column edge. `D102`'s placement is back.

Also reverted in the same pass: `.ss-cap p{max-width:78ch}` is gone. It used half the SIMSCREEN
frame and pushed the caption's Arabic onto a third line. Caption now **980 px of 1022**, Arabic
**3 lines → 2**.

**The gate check flipped with it, and the first version of the flip was worthless.** It compared
box edges — but a full-width `.ar` and a `fit-content` one start their *box* at the same place, so
it passed the exact layout it was written to reject. The mutation test caught that; nothing else
would have. It now measures the painted text on single-line blocks only.

## Visual pass 2026-09-08 (`D113`)

Ebrahim: *"more diagrams, more visual content, real images — not material that looks like a
newspaper."* Added in this pass, and both gates re-run clean afterwards:

- **Hand-authored inline SVG mechanism figures** in the new `.dgm` component — figure id, `D94`
  pattern tag, dark ground, bilingual caption. Each one shows a *mechanism*, not a re-labelling of
  the bullets beside it.
- **Real photographs**, in `.photo` / `.photo-row`, each with its licence line rendered as part of
  the component. The five files were already in the repo, licensed and hash-verified, and had been
  **orphaned by the topic rebuild**; `design/image_sources.md` now ties every file to the page that
  uses it, which `D93` required and nothing had ever written.
- **A visual on 16 of the page's screens.**

Two defects the gates caught in this pass: two SVG text lines ran past their `viewBox` at every
width, and `figure.photo` overflowed at 480 px because `width:max-content` resolves to a long
caption's unwrapped width (`D114`).
