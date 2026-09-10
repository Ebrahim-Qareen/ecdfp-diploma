# P02 · Build log — Evidence integrity

Built 2026-09-08. Topic `T03` · 38 min · evidence `EVS-01`.
First page built under the frozen design contract (`D109`).

---

## What was built

| # | File | Lines | Note |
|---:|---|---:|---|
| 1 | `instructor_guide.md` | 179 | the four not-proves as a table, not a lecture |
| 2 | `student_guide.md` | 172 | self-review walkthrough |
| 3 | `guided_lab.md` | 220 | 9 steps, verification line on each |
| 4 | `student_activity.md` | 71 | five-scenario sort + the THM defect hunt |
| 5 | `quiz.md` | 119 | 10 questions, 6 objectives |
| 6 | `quiz_answer_key.md` | 27 | with the marking note on Q4/Q9 |
| 7 | `homework.md` | 75 | 4 tasks, ~80 min |
| 8 | `homework_answer_key.md` | 83 | model answers for tasks 3 and 4 |
| 9 | `report_stage.md` | 84 | Sections 4 and 5 |
| 10 | `instructor_script_ar.md` | 185 | spoken Egyptian, the instructor's own voice (`D77`) |
| 11 | `build_log.md` | this | |

---

## What was verified

- **Evidence gate (`D91`).** `EVS-01` is Tier 1, ours, deterministic from `scripts/make_evs01.py`,
  and already published. `sha256sum -c` re-run during the build: **3 OK, 1 FAILED**, as designed.
- **The seeded difference was read from the generator, not guessed.** `scripts/make_evs01.py`
  lines 154–156: `Acquisition started : 2026-03-04 09:14:02 UTC` → `…09:14:03 UTC`. The lab and
  both answer keys quote that exact pair.
- **Every claim about `EVS-01`'s contents was read from the files**, not from the outline: the
  acquisition log's `NOTE ON SCOPE OF VERIFICATION`, the custody form's re-hash line, and the
  notebook-page-41 storage line are all quoted from the real text.
- **Budget.** 13 + 12 + 9 + 4 = **38 min**. Theory 13/38 = **34 %**, inside `D79`'s 35 % ceiling.
- **No tool introduced that the course has not taught.** `Get-FileHash` and `sha256sum` only.
  `mount` appears as a *defect to identify*, not as a tool the student runs — it is taught in `P05`.

---

## The one thing that made this page

`EVS-01` ships a **deliberately failing checksum**, and the failure is **one second in a
timestamp**. That single design choice, made weeks ago for a different session, turned out to carry
the whole topic:

- a mismatch that is **not** tampering, so `FAILED` has to be read as a question;
- a **one-character** change producing a completely different digest, which is the avalanche
  property met from the consequence side rather than the demo side;
- and the point that lands hardest — **a one-second edit and a total file replacement produce the
  same `FAILED` line**. The hash has no magnitude.

None of that would have worked with a synthetic "corrupted file". The failure had to be small,
plausible and boring.

---

## Decisions this page did NOT make

`D109` froze the look. This page invented nothing: deck of screens, bilingual layer, the three
encoded boxes, one SIMSCREEN, `D94` reveal figures, the word *Section*, report stage at the end.
**That is the point of freezing it** — `P01` cost two days of decisions and `P02` cost none.

---

## Judgement calls worth recording

**1 · We show INE getting it wrong.** Screen 8 puts `[U2 p143]` ("hashes prove the file has not
been tampered with") beside `[U2 p144]` (store the hash separately). We teach the correction *and*
name the source. Approved by Ebrahim at the outline gate.

The argument: a student who never sees an authority be imprecise learns to trust authorities
instead of evidence. That is the opposite of what this course is for. The framing in both the
guide and the script is explicit that this is **not** a point scored off INE.

**2 · Same for TryHackMe.** The Forensic Imaging room verifies a hash and then invalidates it on
the next page, to 18,481 completions. We use it as the independent exercise — and both the guide
and the script require the instructor to say, in the same breath, that the room's Task 2 audit
trail is the best thing in fourteen rooms reviewed.

**3 · Write blocking is not a separate block.** The map gives it 8 minutes. Teaching it as its own
segment would make it a hardware catalogue. It is taught instead as *the thing that makes the
before-hash and the after-hash comparable* — inside the hashing story, ending on the pair of source
hashes that is the actual technical proof.

---

## What is still open

- [ ] **The HTML page is not built yet.** Next step. Must pass `density_gate.py` and
      `render_gate.js` before review.
- [ ] **`FIG P02-F1` and `FIG P02-F2` are specified but not authored.** Both are `D94` reveal
      figures; the CSS exists (`.cmp`), so this is content, not infrastructure.
- [ ] **`SIMSCREEN T03-1` steps are written in `guided_lab.md` but not yet encoded** as the
      component's step list. The `.wu` terminal screens exist in `win-ui.css`.
- [ ] **The two INE slide images are not in the repo** (`R9`/`D22` — we do not rehost). Screen 8
      must reproduce the *claim* in our own words with the citation, not the slide image. This is
      a real constraint on the strongest moment on the page and needs care in the build.
- [ ] **Nobody has taught this page yet.** The 34 % theory figure is a plan, not a measurement.

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
