# REVIEW_PASS.md — the improvement pass over all 14 built pages

Ebrahim's brief (2026-09-09), after the build finished: review every topic and improve it on
seven dimensions. This file turns that brief into one checklist applied to every page, so the
pass is uniform and inspectable. One page at a time; both gates green before it is called done.

## The seven dimensions, as concrete checks

**D1 — Shape and delivery.** The fixed per-topic path is present and in order:
simple intro tied to the previous topic → theory, each part with a practical picture of it →
INSTRUCTOR DEMO (I run it) → YOUR TURN (student, solo or team) → CHEAT SHEET → TASK → references last.
`P01`–`P09` were built in v1 and are retrofitted to shape-v2 here; `P10`–`P14` are already v2 and are
checked, not rebuilt. Professional topic names kept (title rules in `page_structure.md`).

**D2 — Appearance is correct and works.** CSS, boxes, prose and every diagram render right at all
five widths (1400/1100/900/700/480), no clipped viewBox, no ragged right edge, no overflow, no dead
Play button. This is what the render gate asserts — so D2 = render gate green + a human look at the
screenshots, not just a pass.

**D3 — Highly visual, more than theory.** Every section earns a picture that teaches, not decorates
(`D93`/`D94`): a stepped diagram, a SIMSCREEN, a real photograph of the physical thing, or an image
rendered from real evidence. Every lab and SIMSCREEN follows the REAL steps of the real tool —
verified against the THM writeups in `Resources/THM/`, the INE modules in `Resources/INE_eCDFP/`, and
the tool's own current docs. No stylised drawing of a finding. Prefer running the real tool and
capturing its real output over recreating it, where the container can.

**D4 — Content strength.** Every claim traceable to THM labs + the instructor decks + INE, and to the
real evidence in `design/evidence_sets.md`. The audits already done: `design/review/thm_harvest.md`,
`instructor_audit.md`, `ine_coverage_audit.md`.

**D5 — Heavy simplification, still professional.** English and Arabic both readable at normal speed,
once. Every technical term stays in English inside the Arabic (`الـ hash`, `byte`). No literary MSA,
no wall of theory a beginner cannot hold. `D76` rules + `D128` "does a reader get it at normal speed".

**D6 — Progressive order, everything from the beginning.** Nothing used before the screen that defines
it. Students are weak in DF: file system, disk image, analysis, the tools are each explained from
zero, in small direct steps, with the tool actually applied in the lab.

**D7 — Strongest content, organised system.** The site, the roadmap, the naming, the evidence, the
cheat sheets all cohere. Do anything else that is recommended and record it.

## Per-page checklist (tick all, then gate)

1. Read the page end to end; note the current screen order.
2. Shape: dividers present and in the v2 order; INSTRUCTOR DEMO + YOUR TURN split; CHEAT SHEET screen
   present; TASK carries report stage + a grading line; `Where we are` has the one bridge paragraph
   naming what the previous page gave.
3. Order: definition-before-use holds across the whole page.
4. Visual: every part has a teaching picture; labs/SIMSCREENs match real tool steps; add real photos
   or evidence renders where a physical thing or a finding is the subject (every new image → a row in
   `design/image_sources.md`).
5. Simplify: sweep EN + AR for anything a tired student re-reads; keep terms in English.
6. Gate: `python3 scripts/density_gate.py docs/page-NN/index.html` PASS, then stage + `node
   testing/render_gate.js` zero findings. Read the screenshots.
7. Log one row in `DECISIONS.md`; update this file's status line; report to Ebrahim in short Egyptian
   Arabic.

## Generator map (how each page is edited)

| Page | Source of truth | How to change it |
|---|---|---|
| `P01`,`P02` | hand-written `docs/page-0N/index.html`, patched by `~/build/p0N.py` | edit HTML directly, keep patch script in sync |
| `P03` | hand-written `docs/page-03/index.html`, no generator | edit HTML directly |
| `P04`–`P14` | `~/build/pNN/gen.py`+`assemble.py` → `docs/page-NN/index.html` | edit generator, regenerate, never hand-edit output |

## Status
- [x] P01  - [x] P02  - [x] P03  - [x] P04  - [x] P05  - [x] P06  - [x] P07
- [x] P08  - [x] P09  - [x] P10  - [x] P11  - [x] P12  - [x] P13  - [x] P14

## Result — pass complete (2026-09-10)
All 14 pages retrofitted/verified to shape-v2 and green on both gates (density + render, 5 widths). `order_gate` on `design/topic_map.md` PASS. `P01`&ndash;`P09` regrouped and given cheat sheets; `P10`&ndash;`P14` verified (no rebuild needed). Docs reconciled: `image_sources.md` (held note + spare), `order_gate` EVS table, all 14 cover labels aligned. Open item for Ebrahim: whether to split `P05` (145 min).
