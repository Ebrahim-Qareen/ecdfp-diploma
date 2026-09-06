# eCDFP — Session 2 build prompt
*Paste everything below into a fresh Claude session inside the `ECDFP_Course` project.
It is self-contained: it assumes no memory of any earlier conversation.*

---

## 1 · The job

Build **Session 2 — Acquisition: Disk, Memory & Live Response**: the nine markdown documents in
`packages/session-02/`, the teaching page at `docs/session-02/index.html`, and the figures.

**Invoke `ecdfp-session-package` for the markdown and `ecdfp-session-html` for the page.**
They own the fixed structures. Do not invent your own.

**Session 1 is built and live.** S2 is not a fresh start — it continues a running case, reuses a
finished design system, and inherits a report the students have already begun. §3 is the part you
must not skim.

---

## 2 · Read these first, in this order

| # | Path | Why |
|---|---|---|
| 1 | `00_INSTRUCTIONS.md` | Parts 4, 8, 9, 11 — the build order, the gate, the no-stage-directions rule |
| 2 | `DECISIONS.md` | **`D51`–`D55` are new since S1 and they change how you build.** Also `D7` · `D15`–`D23` · `D41` · `D47` · `D48` |
| 3 | `design/topic_map.md` | **S2's 10 rows and their exact minutes.** This is the ratified map. Reproduced in §5 |
| 4 | `design/design_system.md` | §1.2 the colour pair · §4.2 questions · **§4.4 `.split` and §4.5 `.gui`** · §5 diagrams · §8 the nine rules |
| 5 | `packages/session-01/build_log.md` | **§14 what changed in the second pass, §15 the labs. Read the "still open" list — you inherit it** |
| 6 | `docs/session-01/index.html` | the finished page. **Copy its patterns exactly.** Do not redesign |
| 7 | `design/evidence_sets.md` | `EVS-01` verified; `EVS-02`/`03`/`04`/`09` **not started**. See §4 — this is the gate |
| 8 | `design/tools_by_session.md` | the S2 table — FTK Imager 8.3, Volatility 3, OSFMount, Arsenal, `dc3dd`, KAPE — and §1, the three tools that cannot ship |
| 9 | `knowledge_base/Module_01_Data_Acquisition.md` | §1 concepts · §2 the R10 artifact tables · §4 worked findings triples · §6 teaching notes · §7 gaps |
| 10 | `knowledge_base/instructor/Session_01_Introduction_and_Acquisition.md` | §2 the FTK Imager labs **as actually run** · §4 what the deck adds · **§6 the slides carrying personal data** |
| 11 | `scripts/gen_session_record.py` | the cumulative record engine. **S2's step data already exists in it** |
| 12 | `Resources/LABS/thm-free-labs.md` · `cyberdefenders-free-labs.md` | §3.5 `forensicimaging` · §3.6 `kape` · §3.7 memory · and `D46`: **no free lab teaches acquisition as a decision** |

**Do not read** `knowledge_base/_source_text/` unless a claim needs tracing to its page.

---

## 3 · What Session 1 established — inherit all of it

### 3.1 The design system is finished. Use it, do not rebuild it.

`docs/assets/css/ecdfp.css` now has **sections 15, 16 and 17** added during S1. Every component
below exists and is documented. **Adding CSS is a last resort; using these is the default.**

| Component | What it is for |
|---|---|
| `.finding` `.interpretation` `.limitation` | the `D7` three-way split — solid / dashed / dotted borders, chip labels |
| `.coc` | a chain-of-custody line |
| `.artifact` + `.artifact-grid` | the **R10 six-box** artifact card |
| `.vs` | two cards side by side — *you may write* / *you may not write* |
| `.steps` | a numbered strip. **Content goes in a `<span>`** — a bare `<b>` becomes its own grid cell and breaks the layout |
| `.facts` | big numbers with labels |
| `.rule` | one sentence in large type that has to land |
| `.gui` / `.gui-row` | a **mock window** — title bar, dots, mono body with `.p .ok .no .d` line classes |
| `.split` | content beside a narrow sticky column |
| `figure.photo` | a photo, 560 px, shrink-to-fit, centred |
| `.q.mcq` | `li[data-correct][data-why]` + `input[type=radio]` + `.feedback` |
| `.break-card[data-timer="15"]` · `.cheat` · `#taskList` + `[data-task-counter]` | break page · cheat sheet · homework |
| `.svg-play` | the play control on an animated figure |

### 3.2 Rules S1 learned the hard way — do not rediscover them

1. **`.gui` is never a screenshot.** It renders a real command and its real output as styled text,
   and the caption says so. Anything that would be mistaken for a capture of a real product is a
   screenshot, and screenshots are taken on `FOR-WS01` or not used.
2. **SMIL cannot interpolate a CSS `var()`.** Animating `fill` to `var(--accent-red)` renders
   **white**. Cross-fade a second shape instead.
3. **Isometric figures: one baseline, captions below.** A staircase layout puts labels on the
   shapes. Every S1 attempt at a staircase had to be flattened.
4. **`overflow-wrap`:** `break-word` for prose and table cells; `anywhere` only for code, paths and
   digests. `anywhere` on a table cell split the number **10** across two lines.
5. **Never nest an `<a>` inside an `<a>`.** It is invalid HTML, the browser un-nests it, and the
   card visibly splits in two.
6. **Read the folder before acting on the folder.** Five photos were moved out of `docs/` on a
   suspected licence problem while `IMAGE-CREDITS.md` sat unread in the same directory.
7. **Read what a checker actually says.** Six times in this project a checker was wrong rather
   than the content — a `style="[^"]*"` scan matching the tail of `font-style="italic"`, a link
   check failing on a file that existed outside the sandbox copy, and so on.

### 3.3 The numbers S1 settled

| | |
|---|---|
| Visible words per page | **~240.** These pages are projected and talked over, not read |
| Figure captions | **one sentence** |
| R10 box 4 | still the longest of the six, but **~3–4×** the shortest, not 15×. Use bullets |
| Questions | **all multiple choice** (`D52`), and the correct answer **rotates A→B→C→D** so it is never always the same letter |

---

## 4 · 🔴 The gate — read this before anything else

**Part 8 step 0: a session whose evidence is not verified and hashed does not start.**

| Set | Needed by | Status |
|---|---|---|
| `EVS-02` — `EVI-SRC01` disk image, E01 **and** raw | `S2-05` `S2-06` | ⛔ **not started** |
| `EVS-03` — memory capture from `EVI-SRC01` | `S2-03` | ⛔ not started |
| `EVS-04` — the suspect USB image | `S2-08` `S2-09` `S2-10` | ⛔ not started |
| `EVS-09` — a triage collection set | `S2-07` | ⛔ not started |

**S1 got past this because its evidence was four text files a script could generate. S2 cannot.**
An E01 image, a memory dump and a USB image are **Tier 1 or Tier 2 only** — `ecdfp-evidence`
forbids synthesising any of them, because a fabricated image is a lie told to students about what a
forensic artifact looks like.

**So the first thing you do is ask, not build:**

> Call `ecdfp-evidence`. Report which of the four sets exist. If none do, say so plainly, name S2
> as the session that cannot start, and **stop for a decision** — Tier 1 (stage `EVI-SRC01` in the
> lab and image it ourselves) or Tier 2 (NIST CFReDS, per `D36`, linked and never rehosted).
> Do not offer to build the theory pages meanwhile. The outline depends on what the evidence
> actually contains.

⚠️ **`labs/` still does not exist and `FOR-WS01` has never been built.** Tier 1 depends on it.

---

## 5 · The session — 10 blocks, 205 minutes

From `design/topic_map.md`. **Do not re-derive these and do not use `design/session_map.md`,
which is an unratified 8-session proposal.**

| # | Block | Min | Hands-on | New? |
|---|---|--:|:-:|:-:|
| `S2-01` | Order of volatility **in practice** — the collection sequence, and what you destroy by getting it wrong | 15 | No | — |
| `S2-02` | **Live response** — volatile data collection on a running host | 25 | Yes | 🔴 |
| `S2-03` | **Memory acquisition** — why it comes first, the tools, the pitfalls | 20 | Yes | 🔴 |
| `S2-04` | Physical vs logical acquisition — what each captures and what each misses | 20 | No | — |
| `S2-05` | Image formats — E01 vs raw (`dd`) vs AD1, compression, embedded verification | 15 | No | 🔴 |
| `S2-06` | **FTK Imager** — correct use and verification. *Instructor demo: imaging `EVI-SRC01`* | 20 | Yes | — |
| `S2-07` | `dc3dd` on `FOR-LNX01`, and KAPE targeted triage | 15 | Yes | 🔴 |
| `S2-08` | **[INVESTIGATION]** Case 02a — acquire and verify the suspect USB | 35 | Yes | — |
| `S2-09` | **[INVESTIGATION]** Case 02b — examine the acquired image's partition and file-system structure | 25 | Yes | — |
| `S2-10` | **[RITUAL]** Hash-verify + chain-of-custody close | 15 | Yes | — |
| | **Total** | **205** | **155 min** | |

**Shape (`D15`/`D23`):** integrated **130** · break **15** · investigation **60** · ritual **15**
= **220** teaching, inside a 240 slot.

**Where the break falls.** After `S2-05`, at minute 95. `S2-06`'s FTK Imager demo needs an
uninterrupted run and imaging takes real wall-clock time — start it before the break if the
hardware allows.

> 🔴 **`S2-02`, `S2-03`, `S2-05` and `S2-07` are the new material and they carry the session.**
> Everything else the students have met in eCIR or in S1. **Reference it and move on.**

---

## 6 · Simple English — this is a hard requirement, not a preference

The students are practitioners, not native English speakers. Write so the meaning survives being
read quickly on a projector.

| Do | Do not |
|---|---|
| short sentences — one idea each | 25–30 word sentences |
| plain words: *use*, *show*, *stop*, *prove* | *utilise*, *demonstrate*, *preclude*, *evidence* (as a verb) |
| the same word for the same thing, every time | synonyms for variety |
| define a term once, then use it | assume it was picked up |
| active voice: *the tool writes a log* | *a log is written by the tool* |

**Banned everywhere, from `Module_05`:** two date formats in one document · two terms for one thing
· jargon with no glossary entry · any sentence assigning guilt.

**Test each page:** read it aloud. If you run out of breath, the sentence is too long.

---

## 7 · Diagrams — one for every block, and they move

**This is the part of the brief that matters most.** S1 shipped 12 figures for 10 blocks; S2 should
match or beat it. **Every block in §5 gets at least one figure.** A block with only prose has
failed.

### The rules (`design_system.md` §5, locked)

Hand-authored **inline SVG only** · no image files for diagrams, no libraries · everything inside
the `viewBox` · **arrows never cross label text** · `stroke-width` ≥ 1.5 · text ≥ 12 units ·
colours from tokens via `var(--…)` · `role="img"` with `<title>` as the **first** child · wrapped in
`.svg-wrap` · **exactly one `[data-detail]` per `[data-node]`** — the gate fails on a duplicate or
an orphan.

### Animation (`D51`)

A figure may animate **when the animation shows a mechanism over time**, and only behind an
explicit play control. **No autoplay. No loop. No GIF. No JavaScript.**

```
<g id="f4play" class="svg-play" role="button" tabindex="0"> … </g>
<animate attributeName="x" from="…" to="…" begin="f4play.click" dur="1.5s" fill="freeze"/>
```

**S1 animated 5 of 12. S2 should animate more — this session is about processes that happen over
time, which is exactly what animation is for.**

### The figures to build

| # | Figure | Block | What it must show, and what clicking does |
|---|---|:-:|---|
| **S2-F1** | **The collection sequence, running against the clock** ▶ | `S2-01` | The seven stores from S1, but now with a *collection job* moving down them. Press play: while you collect RAM, network state decays; while you collect the disk, both are already gone. **Click a store → what you lost by starting lower** |
| **S2-F2** | **Live response — what the OS tells you vs what is true** ▶ | `S2-02` | Two columns: what the collector reports, and what is actually on the machine. Press play: a rootkit hides three processes and the report still looks clean. **Click either side → the artifact that would catch it** |
| **S2-F3** | **The live-response output tree** | `S2-02` | `<HOSTNAME>_<date>_<time>\` → `ForensicImages\` + `LiveResponseData\` + the per-file hash list + `Processing_Details.txt`. **Click a branch → what it holds and what it cannot** |
| **S2-F4** | **Memory capture is a smear, not a snapshot** ▶ | `S2-03` | 🔴 The best animation in the session. A memory map with processes changing **while the capture head moves down it** — so the top of the dump and the bottom are from different moments. **Click → what that makes unreliable, and what it does not** |
| **S2-F5** | **What blocks a memory capture** | `S2-03` | Driver signing · Secure Boot · a hypervisor · an anti-cheat driver. **Click each → the error you actually see, and the way round it** |
| **S2-F6** | **Physical vs logical — two envelopes over one disk** | `S2-04` | One disk drawn once. Physical reaches slack, unallocated, HPA/DCO; logical reaches allocated files only. **Click a region → what is lost and which later session needed it** |
| **S2-F7** | **The four acquisition methods** | `S2-04` | disk-to-image · disk-to-disk (clone) · sparse · logical. **Click one → when it is right, and the evidence it forfeits** |
| **S2-F8** | **Image container anatomy** | `S2-05` | E01 (header · segments · per-chunk CRC · embedded hash · case metadata) vs raw `dd` (bytes, nothing else) vs AD1 (selected files only). **Click a container → what its verification actually verifies** |
| **S2-F9** | **What `verified` covers, and what it does not** ▶ | `S2-06` | 🔴 The `D7` figure of this session, and the direct sequel to `S1-F1`. The tool hashes what it **writes**, then what it **reads back** — and never re-reads the source. Press play to watch the loop close *without touching the drive*. **Click → the sentence you may write** |
| **S2-F10** | **`dd` · `dc3dd` · KAPE — three jobs, three tools** | `S2-07` | A comparison on four axes: hashes on the fly? · writes a log? · handles read errors? · scope. **Click a tool → its one command and its one catch** |
| **S2-F11** | **Targeted triage — what you take and what you leave** | `S2-07` | The disk, with the triage target set highlighted over it. **Click a target → what it collects and the question it can no longer answer** |
| **S2-F12** | **The `D19` case — Session 2's slice lit** | hook | The six stages from `S1-F10`, with **stage 0 (seizure and acquisition) now lit** and the rest still dim. Same figure, one stage further on |
| **S2-F13** | **The acquisition decision tree** | `S2-08` | Is the host running? → is the data encrypted? → is time short? → which method. The one thing **no free lab teaches** (`D46`) and therefore entirely ours |
| **S2-F14** | **The shape of a session** | opening | Reuse `S1-F12` unchanged. Students should recognise it |

**Quality bar.** A figure that re-labels the bullet points beside it has failed. Each must show a
**mechanism, a comparison, or a consequence** the prose cannot state as compactly. If a figure would
only decorate, drop it and say so in the build log.

---

## 8 · A small lab for every block — show, then they do

**This is new in S2 and it is the biggest change from S1.** Each block gets a **micro-lab**: you
demonstrate it, then the students repeat it immediately. Not one lab at the end — **one per block**.

### The fixed shape of a micro-lab

```
1  WATCH   one command or one action, done by the instructor.  2–3 min
2  DO      the same thing, on the student's own machine.       3–5 min
3  CHECK   one line they can compare against — pass or fail.
4  WHY     one sentence: what this proves, and what it does not.
```

Render it with the components that already exist:

- the command in `<pre><code>`
- the expected output in a **`.gui`** panel beside it, in a `.split`
- the check as a **`.lab-box`** verification line
- the *what it does not prove* as a **`.limitation`**

### The eight micro-labs

| Block | WATCH — you do | DO — they do | CHECK |
|---|---|---|---|
| `S2-01` | list what is on the host in volatility order | write the collection order for a given scenario | their order matches, and they can say what each step costs |
| `S2-02` | run the live-response collector | run it on their own VM | the output tree exists and the per-file hash list is complete |
| `S2-03` | capture RAM, note the elapsed time | capture their own RAM | dump size ≈ physical memory, and they recorded start **and** finish times |
| `S2-04` | image a small volume physically, then logically | do both on a 100 MB test volume | the two files differ in size — and they can say why |
| `S2-05` | create the same image as E01 and as raw | do both | E01 is smaller; `ewfverify` passes; the raw has no embedded hash to verify |
| `S2-06` | FTK Imager end to end, verification ticked | image the supplied test volume | the `.txt` log shows both digests and `verified` |
| `S2-07` | `dc3dd` with `hash=` and `log=` | same command on the test volume | the log contains the hash — which plain `dd` never produces |
| `S2-10` | fill one custody line on the record | fill their own | the record page shows the step closed |

⚠️ **Every micro-lab uses `EVS-02`/`03`/`04` or a scratch volume the student makes. Never the
original evidence, and never an unverified set.**

---

## 9 · The record — do not forget it

**`D55`. This is the deliverable the students carry from session to session, and it is the thing
most likely to be dropped.**

- The record lives at **`docs/session-NN/record.html`**, generated by
  **`scripts/gen_session_record.py`** — one template, per-session step data.
- **S2's step data already exists in that file** (`S("s2", "02", …)`). Read it. The page is already
  built at `docs/session-02/record.html`.
- It is **cumulative**: S2 shows S1 collapsed as *carried forward*, and S2 open.
- Its structure follows **SWGDE 18-Q-002**, **SWGDE 18-F-002** and **ISO/IEC 27037** — not a shape
  of our own. Do not restructure it.
- The **custody-transfer log and the disposition are case-level**. They are rendered once and never
  per session, or the chain fragments.

### What you must do with it in S2

| ☐ | |
|:-:|---|
| ☐ | **Review S1's record first.** The session opens by checking what the students already recorded — that is the recap |
| ☐ | Regenerate `docs/session-02/record.html` after any step-data change: `python3 scripts/gen_session_record.py` |
| ☐ | Link it from the S2 page — every session page links its own record |
| ☐ | `S2-10` closes the record, exactly as `S1-10` did |
| ☐ | Evidence IDs come from `design/evidence_sets.md` and are **never invented in the generator** |
| ☐ | Examples use placeholder digests, never real case data |

> **Open every session with the record and close every session with the record.** A student who
> has done six sessions should be holding one continuous document, not six disconnected ones.

---

## 10 · The case continues

**`D19`, the carry-through incident.** S1's slice was *everything that must be true before analysis
starts*. **S2 is where the evidence is actually created.**

> The finance workstation `EVI-SRC01` was seized and powered down in Session 1. In Session 2 it is
> acquired: live response first where the host is still running, then memory, then the disk. The
> suspect USB device is imaged too. **From this session on, every later session works on the images
> made here.**

**Session 2 is the origin of every artifact in sessions 3 to 6.** Say that out loud — it is the
reason the acquisition has to be right.

Fictional company, fictional users, **no real PII, no real malware, documentation IP ranges only**
(`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).

---

## 11 · Deliver these

**`packages/session-02/`** — the nine fixed documents:
`session_plan.md` · `instructor_guide.md` · `student_guide.md` · `guided_lab.md` ·
`student_activity.md` · `quiz.md` · `homework.md` · `report_template.md` · `build_log.md`

**`docs/session-02/index.html`** — from `docs/assets/base_template.html`. Dark theme. All figures
inline. No inline CSS or JS. **`brief.html` and `record.html` already exist beside it — do not
overwrite either.**

**Notes on three of the nine:**

- **`report_template.md` never changes.** Copy S1's byte for byte. It is fixed from Session 1 and
  graded every session on the same four `D20` criteria. Changing it destroys the only signal that
  report writing is improving.
- **`quiz.md`** — 10 questions, **all MCQ** (`D52`), correct answer rotating A→B→C→D. At least
  three must ask *"finding or interpretation?"*. At least one must ask what `verified` does **not**
  cover.
- **`build_log.md`** — what you built, what you **verified and how**, and an honest open list.
  S1's had ten items. An empty one is almost always wrong.

---

## 12 · Constraints you will be checked against

1. **`D7`** — findings vs interpretation visible on every page, colour-coded, criterion 4 of `D20`.
2. **`R10`** — every artifact gets six boxes; **box 4 (*what it does NOT prove*) is never the
   shortest**. Use bullets, not a paragraph.
3. **Version-bind every command.** FTK Imager 8.3 · Volatility 3 2.28.0 · OSFMount 3.3.1000 ·
   Arsenal 3.13.368. **Re-verify on the build date.**
4. **Zero instructor stage directions in student-facing files** (Part 11, enforced by the scan).
5. **No evidence bytes in the repo** (`R9`). Manifests and hashes only, MD5 **and** SHA-256.
6. **`D41`** — no question has a secret or a person's data as its answer.
7. **`D47`** — every external lab is assigned with its known defect named in the assignment text.
8. **Never link a page that does not exist** (`D30`), and never nest an `<a>` in an `<a>`.
9. **Simple professional English.** Arabic is spoken in the room, never written in the material.
10. **Every OCR-sourced exact string** — a path, a flag, an offset — verified against its source
    page before it reaches a student.

---

## 13 · Order of work, and the exit gate

1. **Call `ecdfp-evidence` (§4).** If the sets do not exist, stop and report. **This comes first.**
2. Read §2's twelve sources. Report anything that contradicts this brief **before** building.
3. **Review `docs/session-01/record.html`** and S1's `build_log.md` open list.
4. Write a **page-by-page outline** — every block, its minutes, its figure, its micro-lab, its
   check. **Stop and get it approved** (`D9`).
5. Build `packages/session-02/` — the nine documents.
6. Build the figures as standalone inline SVG, each verified on its own before it goes in.
7. Build `docs/session-02/index.html`.
8. Regenerate `docs/session-02/record.html`.
9. Run the gate below. Fix, re-run, then report.

### The exit gate — assert each and **show the result**

| # | Check |
|---|---|
| 1 | Blocks total **205 min**; shape is 130 + 15 + 60 + 15 = 220 |
| 2 | Every block in §5 has at least one figure; all inline SVG, no image files, no libraries |
| 3 | Every `[data-node]` has **exactly one** matching `[data-detail]` |
| 4 | Every SVG has `role="img"`, `<title>` first, and a `.svg-wrap` parent |
| 5 | Nothing escapes any `viewBox`; no arrow crosses a label |
| 6 | `node testing/render_gate.js docs/session-02/index.html` → **PASS** at 1400/1100/900/700/480 |
| 7 | Zero stage directions in any student-facing file |
| 8 | Zero credentials, zero real PII, documentation IP ranges only |
| 9 | Every link resolves; **zero nested anchors** |
| 10 | Every image has alt text saying what to notice |
| 11 | Every command carries its version and the date verified |
| 12 | Every evidence set is either **verified** or clearly marked, with no invented hashes |
| 13 | Every block has a micro-lab with all four parts: WATCH · DO · CHECK · WHY |
| 14 | `record.html` regenerates cleanly and S1 appears as *carried forward* |
| 15 | Visible words per page ≈ 240 or fewer |

**Re-check by re-reading the written files, not your own variables.** This project has been burned
six times by checkers that were wrong — `testing/verify_note.py` prints a report, not `OK`.
**Read what the checker actually says before you believe it.**

---

## 14 · Inherited open items — you own these now

From `packages/session-01/build_log.md` §10:

| # | Open | Blocks S2? |
|--:|---|---|
| 2 | `cases/case-NN-*/` — `ecdfp-case` is **not installed** (7 of 8 skills) | S2 has **two** investigations. Yes |
| 3 | Five S1 screenshots never captured | No — the `.gui` panels carry the content |
| 4 | `labs/` does not exist; `FOR-WS01` unbuilt | **Yes.** Tier 1 evidence and every micro-lab depend on it |
| 5 | `D40`'s `F7` — `D19` as numbered stages across **named hosts** | **Yes.** `S2-F12` needs it |
| 6 | `DECISIONS.md` has duplicate rows `D45`–`D50` | No. Cite by date **and** subject |
| 8 | The two sample reports in the training Drive never opened | No |
| 10 | `scope_decisions.md` §1 says "fourth course"; it is the seventh | No |

**Items 4 and 5 are the two that will stop you.** Raise them at step 1, not at step 7.
