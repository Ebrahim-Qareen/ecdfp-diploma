# P01 outline — Foundations and the deliverable

**OUTLINE GATE (`D9`). Approved before any document or HTML exists.**
Page `P01` · **70 topic minutes** · topics `T01` (45) + `T02` (25) · evidence **none required**.

Source: `packages/session-01/` (`S1-01`–`S1-05`) and `knowledge_base/Module_01_Data_Acquisition.md`.

---

## Why this page can be built today

It is the only page besides `P02`/`P03` whose evidence gate passes — `T01` and `T02` need no
evidence set at all. Everything from `P04` on is blocked on `EVS-02/03/04/09`.

---

## `T01` — Foundations & Forensic Principles · 45 min

Parts, from the map: `S1-01` what DF is (10) · `S1-02` forensic principles (10) ·
`S1-03` what makes evidence defensible (10) · `S1-05` toolkit verify + `CLEAN-TOOLS` (15).

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory** | 14 | Opens the course, so the bridge is to the *track*, not a previous topic: *in eCIR you contained an incident — this course proves it.* Then the mandate and the evidence life cycle (6), and the forensic principles: minimal footprint, always work on a copy, **repeatable vs reproducible** (8). |
| **Guided practice** | 15 | `SIMSCREEN T01-1` — verify the tool set and take the `CLEAN-TOOLS` snapshot on `FOR-WS01`, instructor-led, students following on their own machine. |
| **Independent** | 12 | **Two sorting exercises, not a lecture.** (a) six statements sorted *may write / may not write* — 4 min. (b) five short scenarios: admissible or not, and **whose failure it is** — 8 min. This is how `S1-01`'s claim table and all of `S1-03` are delivered. |
| **Report stage** | 4 | Open the report. Fill **§1 Case identification** and **§3 Authorisation & scope** for the carry-through case. |

**Theory 14 / 45 = 31 %** — inside `D79`'s 35 % ceiling.
**How:** the old S1 guide spent 47 minutes lecturing `S1-01`+`S1-02`+`S1-03`. Two of those blocks
are *judgement*, and judgement is taught by making the student judge, not by being told. Moving the
may/may-not table and the whole defensibility test into the independent part is what makes the
budget work — and it is better teaching, not a compromise to satisfy a rule.

## `T02` — The Forensic Report · 25 min

Part: `S1-04` the fixed report template (25). **`D7` calls this the point of the diploma.**

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory** | 8 | Bridge from `T01`: *you now know what makes evidence defensible — this is the document where you have to prove it.* The twelve sections, and the finding / interpretation / cannot-prove split. |
| **Guided practice** | 10 | Work one **FINDING → INTERPRETATION → CANNOT PROVE** triple live, on the board, from a real artifact line. The two line formats they must write from memory. What is banned in Findings. |
| **Independent** | 5 | The student writes their own triple from one supplied artifact line, and it is peer-checked against the `D20` rubric. |
| **Report stage** | 2 | The report is now open for the whole course. Mark **§2 Executive summary**, **§9 Interpretation**, **§11 Conclusions** as *written last* (`D85`). |

**Theory 8 / 25 = 32 %.**

---

## Figures

| ID | Pattern (`D94`) | What it shows |
|---|---|---|
| `P01-F1` | **2 + 3** parallel rows, spotlight, looping | **Relevant · Reliable · Competent** — INE's three-part test, one row each. The spotlight adds what a table cannot: **who owns each**, and that only *authenticity*, inside Reliable, is the examiner's. The old S1 guide said "no figure here" because a diagram that re-labels the bullets has failed — this one carries the ownership dimension, which is why it earns its place |
| `P01-F2` | **2 + 3** parallel rows, spotlight, looping | **FINDING / INTERPRETATION / CANNOT PROVE** — the course's core lesson, and the one figure `R10` and `D20` both point at |
| `P01-F3` | **5** accumulation | The twelve report sections filling **out of order** as topics complete — the visual argument for `D85` |
| `SIMSCREEN T01-1` | **11** | Verify the tool set → take the `CLEAN-TOOLS` snapshot. **Key step: the snapshot is taken BEFORE any case work** — that is what makes every later case reproducible from a known state |

`T02` gets **no SIMSCREEN**: nothing on a screen is the decision. `D96` rule 4 — if no step
qualifies, the procedure does not need one.

---

## Page structure (`D88`)

Cover · how this page works + objectives · **no recap** (first page of the course) ·
`T01` bridge / theory / guided / independent / report stage / knowledge check ·
`T02` the same six · cheat sheet + *what you can now sign* · homework + the report sections it
feeds · references (INE M1 intro, M5 §2).

**At least one *"this artifact cannot prove that"* question** — it belongs on `T02`, where the
concept is taught.

---

## 🔴 One thing needs deciding before `T02` is written

`packages/session-01/report_template.md` has **10 sections**; **`D85` specifies 12**.

| `D85` | Existing 10-section template |
|---|---|
| 1 Case identification | 1 Case reference |
| **2 Executive summary** | **absent** |
| 3 Authorisation & scope | 2 Scope and authorisation |
| **4 Chain of custody** | folded into 3 Evidence received |
| 5 Evidence inventory + hashes | 3 Evidence received |
| 6 Tools & methods | 4 Tools and versions |
| **7 Acquisition details** | folded into 5 Method |
| 8 Findings | 6 Findings |
| 9 Interpretation | 7 Interpretation |
| 10 Limitations | 9 Limitations |
| 11 Conclusions | 8 Conclusion |
| 12 Appendices | 10 Exhibits |

Three sections are genuinely new — **executive summary**, **chain of custody as its own section**,
and **acquisition details**. The `D20` rubric currently cites the old numbers (`§3·§10`, `§4·§5`,
`§6`, `§7·§9`) and must be re-pointed in the same change, or criterion 1 will cite a section that
no longer means what it meant.

**Recommendation: adopt the 12 and re-point the rubric.** The three additions are what a
professional report has and the old template lacked; and the rubric's *wording* does not change —
only the section numbers it points at, so `D20`'s "never changes" promise holds.

---

## Not in this page

The hash itself, chain of custody as a practice, write blocking, hex and magic bytes, Case 01 —
all `P02`/`P03`. `P01` establishes what the work is and what it produces, and nothing else.
