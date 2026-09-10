# page_structure.md — the fixed shape of every teaching page

**Derived from `Resources/Instructor/Session 1.pdf` and `Session 2.pdf`** — the previous ITGate
instructor's decks, which students found clear. This file exists because our rebuilt pages were
**not** clear, and the difference was structural, not cosmetic.

---

## What the instructor's deck does that ours did not

| # | Device | In the source deck | In our pages (before) |
|---:|---|---|---|
| 1 | **Named parts** | `Part 1: Introduction to digital forensics` &middot; `Part 2: Data acquisition` &middot; `LAB time` | none — 20 screens in a flat row |
| 2 | **Section dividers** | bare title slides: `Fundamentals` &middot; `Digital Evidence lifecycle` &middot; `Sources of digital evidence` &middot; `Analysis steps` | none |
| 3 | **&ldquo;We are here&rdquo;** | Session 2 slide 4: the lifecycle diagram with the current stage marked | none |
| 4 | **Numbered sequences** | `#1 Acquiring an evidence` &middot; `#2 analysis` &middot; `#3 presentation`; then `#1 Creating a forensic image` &hellip; `#5 Analysis validation` | none |
| 5 | **Plain descriptive titles** | *What is digital forensics?* &middot; *What is acquisition?* &middot; *What are the magic bytes?* &middot; *What happens when you delete a file?* | *A hash proves less than you think* &middot; *You observed a state, not an event* &middot; *Four different truths, one identical result line* |
| 6 | **Bottom-up build** | Session 2 reaches magic bytes at **slide 15**, after: what is digital data &rarr; ASCII &rarr; data representation &rarr; storage devices &rarr; allocation &rarr; deletion &rarr; file structure &rarr; file header | our `P03` opened hex on **screen 3**, with no foundation under it |

**Item 5 is the one that did the most damage.** An editorial headline is memorable and
**un-navigable**. A student who wants to find the part about magic bytes can scan a sidebar of
*&ldquo;What are the magic bytes?&rdquo;* and find it instantly; they cannot find *&ldquo;You observed a state, not
an event&rdquo;* at all. Every page reading like a different piece of writing is what makes a course feel
like a new series each week.

---

## The fixed shape — every page, from now on  (v2, `D136`)

Ebrahim's brief for the shape, 2026-09-09: *a simple introduction that ties the topic to the one before
it → the theory, each part with a practical picture of it → the practical, for the instructor first →
then for the student, alone or as a team → a cheat sheet → a task → and the references last.* Students
arrive knowing little digital forensics, so every part is explained from the beginning, in small steps.

```
[1]  Cover                     the page, its parts, and its minutes
[2]  Where we are              the lifecycle figure with THIS page marked, and ONE paragraph
                               that says what the previous page gave us and what this one adds
[3]  What you will be able to do
─────────────────────────────  PART 1 — <plain name>            <- divider screen
[4]  What is <the thing>?      definition first, always, in one sentence a beginner can hold
[5]  How it works              mechanism — with a figure or a SIMSCREEN on the same screen
[6]  #1 / #2 / #3 ...          numbered where the content is a sequence
[7]  What it does NOT do       the limits, as their own screen
─────────────────────────────  PART 2 — <plain name>            <- divider screen
 ...
─────────────────────────────  INSTRUCTOR DEMO                   <- divider screen
[n]  the walkthrough           SIMSCREEN or real screenshots; the instructor drives, the
                               student watches and asks. Every step is a real command on real
                               evidence, in the order it is actually run
─────────────────────────────  YOUR TURN                         <- divider screen
[n]  the student lab           the same evidence, a different question; solo or in a team of
                               two; numbered steps, one deliverable, a stated time
─────────────────────────────  CHEAT SHEET                       <- divider screen
[n]  one screen                the commands, offsets, structures and rules of this page, in a
                               form the student can keep open in the next lab
─────────────────────────────  TASK                              <- divider screen
[n]  the assessment            what is handed in before the next page, and how it is graded
[n]  Report stage              which sections of the report this page advances, and why now
─────────────────────────────
[n]  Summary                   what you can now state, and because of what
[n]  References                the sources, the evidence note, and what comes next
```

**What changed from v1.** LAB TIME became two parts — **INSTRUCTOR DEMO** and **YOUR TURN** — because a
lab the instructor runs and a lab the student runs are different screens with different verbs. A
**CHEAT SHEET** screen is new and mandatory: it is the one screen a student keeps open. ON YOUR OWN and
HOMEWORK merged into **TASK**, which carries the report stage. Everything from v1 that is a *device* —
dividers, `Where we are`, plain titles, the definition rule — is unchanged.

**Pages `P01`–`P09` were built in v1 and are retrofitted in the review pass; `P10` onward are built in v2.**

## Title rules

1. **Descriptive, not editorial.** *What is a hash?* not *A hash proves less than you think*.
2. **Question form for a concept, noun form for a thing, verb form for a procedure.**
   *What are magic bytes?* &middot; *File structure* &middot; *Verify the toolkit*.
3. **A title names its content so it can be found in the sidebar.** If you cannot guess what is on
   the screen from its title alone, the title is wrong.
4. **Numbered when sequential.** `#1`, `#2`, `#3` — the student always knows how many are left.
5. **No cleverness in a title.** The insight belongs in the body, in a `.finding` box, or in the
   figure caption — all three of which we have, and all three are better places for it.

## The definition rule

**Never use a term on the screen before the screen that defines it.** `P03` used hex, then bytes,
then signatures — and defined none of them first. The source deck spends ten slides getting to
magic bytes, and that is why it is followed.

Order for anything new: **what it is &rarr; how it works &rarr; how attackers/reality abuse it &rarr;
what it does not establish &rarr; how you use it.**

## The "where we are" figure (`D123`)

Every page opens on a **`Where we are`** screen, and that screen carries the lifecycle figure
`dg-lc-pNN` — the five stages with the current one marked `▲ WE ARE HERE`. It is generated, not
hand-drawn: `lifecycle(dom_id, here, foot_en, band=None)`.

**The marker must move between pages, or the device is decoration.** Two pages claiming the same
stage is a defect, and it is how `P03` shipped saying *stage 2*.

| Page | Stage | Why |
|---|---|---|
| `P01` | none — a band under all five | It is the map, not a place on it: the principles every stage obeys, and the document all five feed. |
| `P02` | 2 &middot; PRESERVE | Integrity, chain of custody, write blockers. The blocker is a stage-1 device that exists entirely to serve stage 2 — say so in the caption. |
| `P03` | 3 &middot; ANALYSE | Identifying a file is the first act of analysis. |

## The divider screen

`<section class="page divider">` with `.divider-inner` — kicker, bilingual `<h2>`, rule, bilingual
lede, and a `divider-meta` line giving **screen count and minutes**, so the student can see the size
of what they are entering.

Five per page is the working density (`P01` 26 screens / 5, `P02` 25 / 5, `P03` 31 / 5): the two
named PARTS, `LAB TIME`, `ON YOUR OWN`, `REPORT STAGE`.

`is-part` belongs on the **divider's** sidebar entry and on nothing else. `P01` and `P02` shipped
with it on content screens, so the sidebar announced a part and then opened a lesson.
`density_gate.py` now asserts `divider screens == is-part entries`.
