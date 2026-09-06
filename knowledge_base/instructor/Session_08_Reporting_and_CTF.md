# Instructor Session 08 — Reporting & CTF Challenge

| | |
|---|---|
| **Deck** | `Resources/Instructor/session 8.pdf` — 30 slides, 23 screenshots |
| **INE material covered** | unit 10 — see [`Module_05_Logs_Timelines_and_Reporting.md`](../Module_05_Logs_Timelines_and_Reporting.md) |
| **Feeds eCDFP session** | `S6` (and, for the report template, back to `S1`) |
| **Source text** | [`../_source_text/Instructor_Session_08_Reporting_CTF_Challenge.md`](../_source_text/Instructor_Session_08_Reporting_CTF_Challenge.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Pure lecture, no tools, thirty slides in two halves. **Slides 6–19 are thirteen numbered
reporting tips** — a craft checklist, delivered as one tip per slide. **Slides 20–30 walk the
report structure** section by section, in the order the sections appear in the document. It
closes on the strongest slide in the entire course.

Two things to know before planning around it. First, **the deck's screenshots are the content**
— almost every slide is a title in the text layer with the body rendered as an image, so
everything below came out of OCR rather than the PDF text layer. Second, **the CTF named in the
deck's own title does not appear in the deck.** There is no challenge brief, no evidence list,
no scoring scheme, no questions. Whatever was run was run outside these slides. See §5 —
this matters, because `S6-09` is a capstone and this was the only prior art for it.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–4 | Course outline, session title, evidence-lifecycle "we are here" marker | `admin` |
| 5 | Section header — reporting tips | `admin` |
| 6 | Tip 1 — time management: reporting, paperwork and testimony are part of the job | `concept` |
| 7–8 | Tip 2 — references must be current; the Windows 7 remote-exploit example | `concept` |
| 9 | Tip 3 — reporting is not a stage after the work; never reverse-engineer the report | `concept` |
| 10 | Tip 4 — provide reasoning; analysis as its own section | `concept` |
| 11 | Tip 5 — avoid absolute terms ("we are sure", "we are certain") | `concept` |
| 12 | Tip 6 — have a template | `concept` |
| 13 | Tip 7 — structured document; a reader must find a section without reading it all | `concept` |
| 14 | Tip 8 — use the past tense | `concept` |
| 15 | Tip 9 — avoid 25–30 word sentences | `concept` |
| 16 | Tip 10 — write down what you did **not** do, and why | `concept` |
| 17 | Tip 11 — avoid jargon; readers may have no IT background | `concept` |
| 18 | Tip 12 — one term per concept; don't alternate synonyms | `concept` |
| 19 | Tip 13 — one date/time format throughout, including tool output | `concept` |
| 20 | Section header — report structure | `admin` |
| 21 | Cover / title page — case serial number, client name | `concept` |
| 22 | Table of contents | `concept` |
| 23 | Executive summary — written for a non-technical senior decision-maker | `concept` |
| 24–25 | Objective section — client request, reasons, goals; **scope is assigned, not just evidence** | `concept` |
| 26 | Evidence section — serial number, hash value, acquiring investigator, chain of custody | `concept` |
| 27 | Analysis section — tools used; "otherwise the report may be refused in court" | `concept` |
| 28 | Crime reconstruction — events in the sequence the investigator believes they occurred | `concept` |
| 29 | Conclusion / report summary | `concept` |
| 30 | **Don't state your opinion unless asked — you are not the judge** | `concept` |

## 2 · Labs and demos — what was actually run

**None.** This is the only deck in the course with no tool, no command and no screenshot of
software. That is defensible for the material, but it means the reporting session was never
practised — and in the rebuilt course the report is the assessment of record, graded every
session on one fixed rubric. `S6` cannot inherit "lecture only" here.

What the deck *does* provide is a section-by-section structure, which is the raw material for
the fixed template. Reproduced as delivered:

| # | Section | What the deck says it contains |
|---|---|---|
| 1 | Cover / title page | Case serial number, client name, anything identifying the report — "for archiving purposes" |
| 2 | Table of contents | So a reader can find a section without reading the whole report |
| 3 | Executive summary | High-level description of the case and the most important findings; written for a senior non-technical manager making a decision. The deck calls this "the most difficult, but the important task" |
| 4 | Objective | The client's request, the reasons behind the investigation, the goals at the start. Slide 25 adds: a case arrives with a **scope and objective**, not just evidence |
| 5 | Evidence | Exhaustive list — serial number, **hash value**, name/ID of the investigator who first acquired it, "alongside other chain of custody related information" |
| 6 | Analysis | The technical section, per item of evidence, **including the tools used**. "Crucial to make this section clear and consistent. Otherwise, the report may be refused in court" |
| 7 | Crime reconstruction | The investigator's own reconstruction — events listed in the sequence they are believed to have occurred |
| 8 | Conclusion / summary | The most important parts of the report, restated |

**How this maps to the course's fixed four-criterion rubric** (`D20` — Integrity · Method ·
Findings · Separation). The deck's structure covers the rubric almost exactly, which is the
useful discovery here:

| Rubric criterion | Carried by |
|---|---|
| **Integrity** | §5 Evidence — hashes, acquirer, chain of custody |
| **Method** | §6 Analysis — tools named, steps consistent and repeatable |
| **Findings** | §6 Analysis — facts, each tied to a named artifact |
| **Separation** | §7 Crime reconstruction (interpretation) kept structurally apart from §6 (fact); tips 4, 5 and 10 supply the language rules |

Tip 10 — *write down what you haven't done, and why* — is the one the deck flags as having
"no dedicated section". In the rebuilt template it does get one: **limitations**, and it is
half of criterion 4.

## 3 · Registry keys, paths and artifacts named on the slides

None. This deck names no artifact, path or key.

The one technical requirement it does state is that the **evidence section must carry the hash
value and the acquiring investigator** for every item — which is the same discipline `S1-06`,
`S1-07` and the per-session hash-verify ritual exist to build. Cross-reference:
[`Module_01 §2`](../Module_01_Data_Acquisition.md).

## 4 · What this deck adds beyond the INE material

- **Thirteen tips as a delivery-ready checklist.** INE unit 10 (`10.2 Tips on Reporting`) covers
  similar ground across 12 pages; the deck's one-tip-per-slide form is directly reusable as a
  student handout and as a self-check before submission.
- **Tip 5 (avoid absolute terms) and slide 30 (don't state your opinion)** are the deck's real
  contribution. Together they are the plainest statement of `D7` — findings versus
  interpretation — anywhere in the source material, in language a first-week student
  understands: *"Remember that the analysis is the investigator's interpretation of the
  evidence and not an absolute truth"*, and *"Don't say 'in my opinion Mr. X has committed this
  crime'"*. **Use slide 30 verbatim in `S1`**, on the day the report template is introduced —
  not in the last session where it currently sits.
- **Tip 3 — reporting is not a stage that comes after the work.** The instruction not to
  "reverse engineer" the report from finished analysis is the argument for the per-session
  report rather than one report at the end. It justifies `D20` directly.
- **Tip 10 — document what you did not do.** Rarely taught, and it is criterion 4's limitations
  requirement.
- **Tip 13 — one date/time format, including the format the tools emit.** This is the practical
  edge of the timestamp discipline `S6` depends on.
- **Slide 25 — "a case is assigned with a scope and objective, not only the evidence."**
  Feeds `S1-06` (investigation scope) as well as reporting.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted, and needed for `S6`:**

- **The CTF.** The deck is titled *Reporting & CTF Challenge* and contains no challenge — no
  brief, no evidence manifest, no questions, no scoring, no answer key. Session 3's deck ends on
  a "CTF Time" slide with a Google Forms submission link, and Session 5 sets a "find the serial
  of the connected USB" challenge with a file link, so competitive exercises clearly ran — but
  **none of the challenge material is in the source set**. `S6-09`'s capstone has to be built
  from scratch; the only prior art is those two scattered slides. Ask the instructor directly
  whether the CTF brief exists as a separate file.
- **A worked example or sample report.** INE unit 10 devotes `10.6 Report Samples` (pp. 52–63)
  to exactly this. The deck has no sample, no excerpt, and no before/after rewrite. For a mixed
  ability class this is the biggest practical gap — students are told what a good section
  contains and never shown one.
- **What makes a report good** (INE `10.5`) — as a set of assessable criteria rather than
  craft tips.
- **Timeline and chronology presentation** — crime reconstruction gets one slide (28) with no
  guidance on how to present a sequence of events, which is what a super-timeline produces.
- **Peer review.** `D16` puts students in pairs to peer-review each other's reports; the deck
  has nothing on reading someone else's report critically.
- **Court and testimony.** Tip 1 mentions "attending court sessions and providing testimonies"
  and slide 27 warns a report "may be refused in court" — neither is developed.

**Resources cited on slides:** none. This deck cites no URL. Its only external reference is
slide 17's bracketed `[2]`, a footnote marker whose bibliography does not appear in the deck.

## 6 · Cautions before reuse

- **No personal data found in this deck.** Every screenshot is rendered prose; there are no
  title bars, console prompts, file paths, user names or IP addresses. Along with Session 3,
  this is one of the two decks that can be reused without regenerating captures. Verify at full
  resolution before publishing, but the OCR shows nothing to redact.
- **The screenshots ARE the content.** Because the body text is rendered as images rather than
  live text, everything quoted above came through OCR. The wording is reliable at the sentence
  level, but **check any phrase before quoting it verbatim to students** — and rebuild these as
  real text if the deck is ever revised, so it is searchable and accessible.
- **Tip 2's example is now stale in a way that proves its own point.** Slide 8 cites *"there are
  no known remote exploits on Windows 7"* as a claim that was true before 2017, referring to a
  vulnerability found "earlier this year". Written in early 2025, that reads as 2025; the
  vulnerability meant is EternalBlue / MS17-010, from 2017. Either fix the year or — better —
  keep the slide and use the drift itself as the lesson.
- **Slide 27's "the report may be refused in court" is jurisdiction-dependent.** State the
  principle (a report must be clear, consistent and reproducible or it will not be relied on)
  without asserting a specific legal outcome. The course is taught in Egypt; admissibility
  rules are not uniform, and this is a claim students may repeat.
- **The deck teaches reporting last.** In the rebuilt course the template is introduced in
  `S1-04` and graded from `S1` onward, so **this material must be split**: the structure and
  tips 4, 5, 10, 11, 12, 13 and slide 30 move to `S1`; what remains in `S6` is assembling six
  sessions of findings into one document. Do not deliver it as a terminal lecture.
- **Nothing here is practised.** Pair every tip with the rubric criterion it serves and put the
  template in students' hands in session 1, or the tips stay advice rather than behaviour.
