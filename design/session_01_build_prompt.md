# session_01_build_prompt.md — the build prompt for eCDFP Session 1

**Written 2026-08-29.** Paste §§1–12 below into a fresh session as one prompt. Everything it needs
is either in the repo at a path it names, or stated inline. It assumes no memory of this
conversation.

> **Two corrections built into the prompt, read these first.**
>
> 1. **Diagrams cannot be image files.** `design/design_system.md` §5 is locked: *"Hand-authored
>    inline SVG only. No image files for diagrams, no diagram libraries."* That is not a limitation
>    here — §4.3's `[data-node]` / `[data-detail]` pairing is exactly the "dynamic diagram" you
>    want, and it is already wired into `session.js` and asserted by the Part 9 gate.
> 2. **Screenshots cannot be lifted from TryHackMe, CyberDefenders or the web.** The repo is
>    **public** (`D22`) and those are third-party copyrighted interfaces. `Resources/DRIVE/`
>    already sets the rule: *link and credit, never rehost.* The instructor decks are worse — they
>    carry a real Windows SID, local paths, machine models and a personal email address, and
>    `knowledge_base/README.md` §6 makes regenerating them a release gate. **So every screenshot in
>    Session 1 is captured fresh on FOR-WS01**, which is what the privacy gate demands anyway.
>
> Session 1 makes this easy: `design/tools_by_session.md` shows S1 needs **no forensic software at
> all** — `Get-FileHash`, `sha256sum` and a text editor. It is a **diagram-heavy, screenshot-light**
> session, and saying so out loud on day one is itself a teaching point.

---

## 1 · Role and mission

You are building **Session 1 of the eCDFP digital forensics diploma at ITGate Academy** —
*Forensic Foundations, Evidence Integrity & Chain of Custody*.

Produce the **complete instructor package plus the student-facing HTML teaching page**, at a
standard where another instructor could teach the session from your output without asking you a
question.

**Invoke the `ecdfp-session-package` skill for the markdown, and `ecdfp-session-html` for the page.**
They own the fixed structures. Do not invent your own.

## 2 · Read these before writing anything — in this order

| # | Path | Take from it |
|---|---|---|
| 1 | `00_INSTRUCTIONS.md` | Parts 4, 8, 9, 11 — the build order, the gate, the no-stage-directions rule |
| 2 | `DECISIONS.md` | D1, D7, D15–D23, D25, D37, D48. **Read D7 and D20 twice — they are the course** |
| 3 | `design/session_map.md` | **S1's 13 blocks and their exact minutes.** Reproduced in §4 below |
| 4 | `design/scope_decisions.md` | D15 session shape · D17 pre-built VM · D18 evidence pre-download · D19 the case · D20 the rubric |
| 5 | `design/design_system.md` | §1.2 the FINDING/INTERPRETATION colour pair · §4.3 interactive panels · **§5 diagram rules** · §8 the nine HTML rules |
| 6 | `design/tools_by_session.md` | The S1 table — and §1, the three tools that cannot ship |
| 7 | `knowledge_base/Module_01_Data_Acquisition.md` | §1 concepts · §2 artifacts on the R10 six-box template · §4 worked findings triples · §6 teaching notes · §7 gaps |
| 8 | `knowledge_base/Module_05_Logs_Timelines_and_Reporting.md` | §2 *the fixed course report template* — the S1 handout |
| 9 | `knowledge_base/instructor/Session_01_Introduction_and_Acquisition.md` | §1 running order · §2 the labs as actually run · **§6 the slides that carry personal data** |
| 10 | `Resources/LABS/thm-free-labs.md` | §3.1, §3.2, §3.3 — the three S1 rooms and how each is meant to be used |
| 11 | `Resources/LABS/cyberdefenders-free-labs.md` | §3.1 Red Stealer — the 15-minute hash example |
| 12 | `knowledge_base/thm/initialaccesspot.md` | The MD5-for-lookup vs SHA-256-for-integrity contrast — the best hashing content in the corpus |
| 13 | `knowledge_base/thm/intro-to-cold-system-forensics.md` | ⚠️ **The counter-example.** It recommends MD5/SHA-1 for evidence integrity. Use it as the mistake students must catch |
| 14 | `Resources/DRIVE/drive-inventory.md` | `Digital forensics reports/` holds two sample reports — the thing the report lesson most needs |
| 15 | `docs/assets/base_template.html` · `docs/assets/css/ecdfp.css` · `docs/assets/js/session.js` | The page skeleton, the only stylesheet, and the script that drives the `[data-node]` panels. **Never author a page from scratch and never fork the stylesheet** |

**Do not read** `knowledge_base/_source_text/` unless a claim needs tracing to its page. It is
verbatim third-party courseware, machine-read and not proofread.

## 3 · Who is in the room — this changes everything about depth

**~5 students, offline classroom, every student at a keyboard.** eCDFP is the **seventh** course in
their track:

**CCNA → MCSA → Linux Administration → SOC → CEH → eCIR → eCDFP**

**Never re-teach what they already have. Reference it and move on.** Verified against the CEH and
eCIR course sites:

| Already theirs — recall in one line, do not teach | New to them — this is where the time goes |
|---|---|
| hashing, MD5/SHA-256, the chain-of-custody *concept* (eCIR S5), Volatility, Wireshark and its filter set (eCIR S8), tcpdump, event logs, 4624, 1102, Sysmon, ATT&CK, the IR lifecycle | **write blocking and how to *prove* it · the forensic report as a legal instrument · findings vs interpretation as a graded discipline · what a hash does NOT prove** |

**The tone that follows from this:** they are not beginners, they are practitioners crossing from
*detection* into *evidence*. The shift is from *"is this bad?"* to *"can I defend this in front of
someone whose job is to break it?"* Open the session on that sentence.

## 4 · The session — 13 blocks, 201 minutes, non-negotiable

240-minute slot → 220 teaching → **205 topic minutes** (`D15`/`D23`), of which 15 is the closing
ritual. Shape: **~130 integrated · 15 break · ~45 investigation · 15 ritual.**

| # | Block | Status | Min |
|---|---|:-:|--:|
| 1 | What digital forensics is — the mandate, the evidence lifecycle, what an investigator may not claim | `PARTIAL` | 10 |
| 2 | Forensic principles — order of volatility, minimal footprint, repeatability, always work on a copy | `PARTIAL` | 12 |
| 3 | Defensible evidence — relevance, authenticity, integrity, admissibility | `PARTIAL` | 10 |
| 4 | Cryptographic hashing — what a hash proves and what it does **not** | `KNOWN` | 8 |
| 5 | Chain of custody — the form and the discipline | `PARTIAL` | 10 |
| 6 | **Write blocking — hardware vs software, and how to prove one was used** | `NEW` | 12 |
| 7 | **The fixed forensic report template — findings vs interpretation (`D7`)** | `NEW` | **30** |
| 8 | **Course roadmap — Windows, Linux, and what each platform can and cannot show** | `NEW` | 10 |
| 9 | Analyst toolkit verify + `CLEAN-TOOLS` snapshot *(install is pre-work)* | `KNOWN` | 12 |
| 10 | Physical vs logical acquisition — what each captures and misses | `PARTIAL` | 12 |
| 11 | Image formats — E01 vs raw (dd) vs AD1, compression, embedded verification | `PARTIAL` | 15 |
| 12 | **[INVESTIGATION]** Case 01 — verify 4 files against a signed manifest, find the tampered one | — | 45 |
| 13 | **[RITUAL]** Hash-verify + chain-of-custody close | — | 15 |
| | **Total** | | **201** |

**Block 7 is the longest block in the session and it is the point of the whole diploma.** `D7` makes
findings-versus-interpretation the course's core lesson; `D20` grades it as criterion 4 of a rubric
that never changes across all sessions. If block 7 is thin, the session has failed regardless of
how good the rest is.

**Block 6 is the one real gap.** `Module_01` §7 lists *"how to prove a write blocker was used"* as
`[missing]` — INE asserts write blocking and never shows the proof trail. Build the proof trail
explicitly: the before/after hash, the tool's own log, the photograph, the custody line.

## 5 · The spine — every example comes from one case

**`D19`, the carry-through incident.** All eight sessions cut into the *same* evidence at
increasing depth. Session 1 is where students meet it:

> A finance-department user at a fictional company opens a malicious document received by email.
> Malware executes and establishes persistence, beacons to an external C2 server, and the operator
> uses harvested credentials over RDP to reach a second host. Data is collected, staged, archived
> and copied to a USB device. Ransomware tooling is staged but **never fires** — the intrusion is
> caught first. The host is powered down and imaged in Session 2.

**Session 1's slice:** the host has been seized and nothing has been analysed yet. S1 is about
*what has to be true before analysis is allowed to start.* Every worked example, the quiz, the
homework and Case 01 use this incident. Fictional company, fictional users, **no real PII, no real
malware, documentation IP ranges only** (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).

## 6 · Diagrams — twelve, hand-authored, interactive

**This is the part of the brief that matters most. Build every one.**

**The rules (`design_system.md` §5, locked):** hand-authored **inline SVG only** · no image files,
no diagram libraries · everything inside the `viewBox` · **arrows never cross label text** ·
`stroke-width` ≥ 1.5 · text ≥ 12 units · colours from tokens via `fill="var(--...)"` only ·
`role="img"` with a `<title>` first child · wrapped in `.svg-wrap` so it scrolls in its own
container.

**"Dynamic" means §4.3, not animation.** Put `[data-node]` on the parts of the SVG a student should
be able to interrogate, and give each exactly one matching `[data-detail]` panel that appears on
click. **Exactly one `data-detail` per `data-node`** — the Part 9 gate fails on a duplicate or an
orphan. Animation is section-entrance only; nothing loops, glows or pulses.

| # | Diagram | Block | What it must show — and the interaction |
|---:|---|:-:|---|
| **F1** | **The evidence lifecycle** | 1 | seize → acquire → verify → analyse → interpret → document → present. **Click a stage → what goes wrong there, and which session teaches it.** The spine of the whole diploma |
| **F2** | **Order of volatility as a ladder** | 2 | CPU registers/cache → RAM → network state → running processes → disk → remote logs → archival media, each with its survival window. **Click a rung → what you destroy by collecting the one below it first** |
| **F3** | **FINDING vs INTERPRETATION** | 7 | 🔴 **The most important figure in the course.** One artifact → two branches. Left: what the artifact *states*. Right: what an analyst *concludes*. A third, dimmed branch: **what it cannot prove.** Use the `D7` colour pair from `design_system.md` §1.2 — this figure is where the palette earns its existence. **Click any of the three → a worked example from `Module_01` §4** |
| **F4** | **Chain of custody as a transfer timeline** | 5 | Each hop carries who · when · why · hash. **Click a hop → the entry that must exist.** Include one deliberately broken hop and let students find it |
| **F5** | **What a hash proves** | 4 | file → function → digest, then three outcomes: match, mismatch, and the collision case. **Click each → the exact sentence you may write in a report, and the sentence you may not** |
| **F6** | **MD5 vs SHA-256 — two different questions** | 4 | A fork: *"have we seen this file before?"* → lookup, MD5 acceptable · *"is this file unaltered?"* → integrity, SHA-2/SHA-3 only. Mark the `intro-to-cold-system-forensics` position on the wrong branch — **name the room and say why it is wrong** |
| **F7** | **Write blocking — the data path** | 6 | Two paths side by side: unprotected (writes reach the evidence) and blocked (hardware inline vs software driver, and where each intercepts). **Click either → the proof trail: before/after hash, tool log, photograph, custody line** |
| **F8** | **Physical vs logical acquisition** | 10 | One disk, two capture envelopes drawn over it. Physical reaches slack, unallocated, HPA/DCO; logical reaches allocated files only. **Click a region → what is lost and which later session needed it** |
| **F9** | **Image container anatomy** | 11 | E01 (header, segments, embedded CRC + hash, case metadata) vs raw `dd` (bytes, nothing else) vs AD1 (logical, custom content). **Click a container → what its verification actually verifies** |
| **F10** | **The report template, mapped to the rubric** | 7 | The fixed section list down one side, the four `D20` criteria — Integrity · Method · Findings · Separation — down the other, with lines joining section to criterion. **Click a criterion → what full marks look like** |
| **F11** | **The `D19` case, and where each session cuts into it** | 5, 8 | The six-stage chain across the named hosts, with **Session 1's slice highlighted and the other seven dimmed**. Re-used in every later session with a different stage lit |
| **F12** | **The shape of a session** | opening | 240 slot → 220 teaching → 130 integrated · 15 break · 45 investigation · 15 ritual. Students should know the rhythm by minute five, and see the ritual coming |

**Quality bar.** A diagram that merely re-labels the bullet points beside it has failed. Each one
must show a **mechanism, a comparison, or a consequence** the prose cannot state as compactly.
Where a figure would only decorate, drop it and say so in the build log.

## 7 · Screenshots — original, captured on FOR-WS01, and few

**The rule, absolute:** no screenshot from TryHackMe, CyberDefenders, INE, the instructor decks, or
any web page is used. Public repo (`D22`), third-party interfaces, and the decks carry a real
Windows SID and a personal email address. **Link and credit; never rehost.**

**Capture these on the clean course VM**, save to `docs/session-01/img/`, PNG, ≤ 1600 px wide,
lossless-optimised, with a one-line caption naming the tool and its version:

| Shot | Shows | Block |
|---|---|:-:|
| `Get-FileHash -Algorithm SHA256` on the evidence file, PowerShell | the command, the digest, the version banner | 4 |
| `sha256sum -c manifest.sha256` — all four files, one FAILED | **the mismatch being caught** — the single most important screenshot in the session | 4, 12 |
| The signed manifest open in a text editor | what a manifest is: a text file, nothing more | 12 |
| The completed chain-of-custody form | a document, not a tool — that is the lesson | 5 |
| `CLEAN-TOOLS` snapshot in the hypervisor's snapshot manager | the known-good baseline you can always return to | 9 |
| FTK Imager's `.txt` verification log | the tool attesting to its own output — previewing S2 | 11 |

**Six is enough.** Do not pad. Anything a diagram can show belongs in §6, not here. A hardware
write blocker gets **F7**, not a product photo.

**Alt text is required on every image** and must state what the reader should notice, not what the
image is of.

## 8 · Labs and practice — linked, never rehosted, each with a stated role

**In class**

| What | Source | Role | Min |
|---|---|---|--:|
| **Case 01 — the tampered file** | our own `EVS-01` (4 files + signed manifest, one altered) | the 45-minute investigation. Students verify, find the mismatch, and **write it up as a finding, not a conclusion** | 45 |
| **Red Stealer** — hash example | [CyberDefenders](https://cyberdefenders.org/blueteam-ctf-challenges/red-stealer/) · free · `Resources/LABS/cyberdefenders-free-labs.md` §3.1 | **shown, not assigned** — the cleanest illustration of block 4 in the catalogue | 15 |
| **Cold System Forensics** — the counter-example | THM `introtocoldsystemforensics` · **now free** | it recommends MD5/SHA-1 for evidence integrity. **Put it on screen and have the room find the error.** A published course being wrong is the best possible argument for block 4 | in block 4 |

**Pre-course task (issue before Session 1)**

- **THM — Intro to Digital Forensics** (`introdigitalforensics`, free, ~90 min, 295k completions).
  Covers blocks 1, 2 and part of 5. **S1 then opens on shared vocabulary instead of definitions.**
  Its hashing task is thin — say so; students still need block 4 from us.

**Homework (issue at the end of Session 1)**

- **THM — Digital Forensics Case B4DM755** (`caseb4dm755`, free, ~120 min) — the S1→S2 bridge, built
  around evidence that has to survive a courtroom. That framing *is* block 5, and it is rare.
- **Optional, 40 min:** THM — IR Philosophy and Ethics (`irphilosophyethics`) for blocks 5 and 6.

**Every one of these is a link plus a one-line reason. No screenshots, no copied task text, no
answers.** Where the catalogue file records a safety or currency defect for a room, carry that
warning into the student guide verbatim.

## 9 · Tools — S1 needs no forensic software, and that is a teaching point

From `design/tools_by_session.md` §2:

| Tool | Version | Role |
|---|---|---|
| `Get-FileHash` / `sha256sum` | OS built-in | **CORE** — the whole of block 4 |
| `md5sum` | OS built-in | **MENTION** — a lookup key, explicitly *not* an integrity control |
| A text editor + a manifest | — | **CORE** — the chain of custody is a document, not a tool |

> 🟢 **Open the session with this.** The most important session in the course needs no forensic
> software at all. Everything after it does — and none of it will save a student who skipped this.

**Three tools must not be distributed** (`tools_by_session.md` §1) — RegRipper **4.0** (bars vendor
training; stay on 3.0), 010 Editor (30-day trial, no free tier — use HxD), Xiao Steganography (no
living vendor). If any is mentioned, mention it as the finding, not the recommendation.

## 10 · Deliver these files

**`packages/session-01/`** — the nine fixed documents from `ecdfp-session-package`:
`session_plan.md` · `instructor_guide.md` · `student_guide.md` · `guided_lab.md` ·
`student_activity.md` · `quiz.md` · `homework.md` · `report_template.md` · `build_log.md`

**`docs/session-01/index.html`** — from `docs/assets/base_template.html`, following
`design_system.md` §8's nine rules. Dark theme only. All twelve figures inline. No inline CSS or JS.

**`docs/session-01/img/`** — the six screenshots.

**Notes on three of the nine:**

- **`report_template.md` is the session's most reused artifact.** It is handed out in S1 and graded
  every session after, unchanged, on the four `D20` criteria. Build it from `Module_05` §2, and
  make the findings/interpretation separation structural — a section boundary, not a heading colour.
- **`quiz.md`** — mixed MCQ and short answer. At least three questions must present an artifact and
  ask *"finding or interpretation?"* At least one must ask what a hash match does **not** prove.
- **`build_log.md`** — record what you cut and why, every `⚠ OCR — verify` string you resolved
  against a source page, and any figure you dropped as decorative.

## 11 · Constraints you will be checked against

1. **`D7` — findings vs interpretation is visible on every page**, colour-coded with the
   `design_system.md` §1.2 pair, and it is criterion 4 of the `D20` rubric.
2. **`R10` — every artifact gets six boxes**: what it is · where it lives (exact path) · what it
   proves · **what it does NOT prove** · how to parse it (tool + command) · one anti-forensics or
   false-positive caveat. The fourth box is never the shortest.
3. **Version-bind every command.** A command is correct only against a stated version
   (`tools_by_session.md`, rule 2). Re-verify versions on the build date.
4. **Student-facing files carry zero instructor stage directions** (Part 11; the Part 9 scan
   enforces it). No "ask the class", no "pause here", no timing notes in the student guide.
5. **No evidence bytes in the repo** (`R9`). Manifests and hashes only, both MD5 **and** SHA-256.
6. **Evidence is published by the end of the previous session** with both hashes (`D18`); students
   verify before class. `EVS-01` is **unverified** until `ecdfp-evidence` says otherwise — say
   `unverified` wherever it appears.
7. **Never link a page that does not exist** (`D30`), and never claim a session is published.
8. **Simple professional English.** Arabic is spoken in the room, never written in the material.
9. **Every OCR-sourced exact string** — a path, a flag, an offset — is verified against its source
   page before it reaches a student. There are 100+ `⚠ verify against source page` markers and they
   are honest.

## 12 · Order of work, and the exit gate

**Work in this order. Do not write HTML before the outline is approved (`D9`).**

1. Read §2's fifteen sources. Report anything that contradicts this brief **before** building.
2. Write a **page-by-page outline** — every block, its minutes, its figure, its screenshot, its
   check-for-understanding. **Stop and get it approved.**
3. Build `packages/session-01/` — the nine markdown documents.
4. Build the twelve figures as standalone inline SVG, each verified on its own before it goes in.
5. Build `docs/session-01/index.html` from the base template.
6. Capture the six screenshots on FOR-WS01, optimise, write alt text.
7. Run the exit gate below. Fix, re-run, and only then report done.

**The exit gate — assert each, and show the result, do not just claim it:**

| # | Check |
|---|---|
| 1 | Blocks total **201 min**; the session fits 205 with the ritual at 15 |
| 2 | All **12 figures** present, inline SVG, no image files, no libraries |
| 3 | Every `[data-node]` has **exactly one** matching `[data-detail]` — no orphans, no duplicates |
| 4 | Every SVG has `role="img"`, a `<title>` first child, and a `.svg-wrap` parent |
| 5 | No element or text escapes any `viewBox`; no arrow crosses a label |
| 6 | Page renders with **no horizontal scroll** at **1400 / 1100 / 900 / 700 / 480** px |
| 7 | Zero instructor stage directions in any student-facing file (Part 9 scan) |
| 8 | Zero credentials, zero real PII, zero real IPs — documentation ranges only |
| 9 | Every external link resolves; nothing links to an unbuilt page |
| 10 | Every image has alt text that says what to notice |
| 11 | Every command carries the version it was verified against, and the date |
| 12 | `EVS-01` is marked `unverified` everywhere it appears |
| 13 | The `D7` colour pair appears on every page that states a finding |
| 14 | Every artifact has all six `R10` boxes, and box 4 is not the shortest |

**Re-check by re-reading the written files, not your own variables.** This project has been burned
three times by checkers that were wrong — `testing/verify_note.py` prints a report, not `OK`, and
two "failures" in an earlier pass were bugs in the assertion, not the content. Read what the
checker actually says before you believe it.

---

## Notes for Ebrahim — not part of the prompt

**Four things to settle before you run this:**

| | Why it matters |
|---|---|
| **`packages/` does not exist yet** | S1 is the first package in the project. Create it and update `PROJECT.md` §2 in the same commit (`D11`) |
| **`docs/session-01/` holds only `brief.html`** (the hub stub); this prompt writes `index.html` beside it | Decide whether the brief stays as the hub card or the full page replaces it — `docs/index.html` and `roadmap.html` both link to the brief |
| **`EVS-01` is unverified** | Part 8 step 0 says a session cannot start until every set it names is verified and hashed. Run `ecdfp-evidence` on `EVS-01` first, or accept that S1 builds against a placeholder |
| **The session map now says 8 sessions; `topic_map.md` still says 6** | S1's blocks are identical either way, so this does **not** block S1 — but the four owed `DECISIONS.md` rows (`D1`, `D38`, `coverage_matrix.md`, `scope_decisions.md` §1) should land before S4 |

**One high-value input this prompt cannot use yet.** `Resources/DRIVE/` §1 records two sample
forensic reports in the training Drive — the single artifact the report lesson most needs and does
not have. They are inventoried but **not downloaded and not read**. Getting them through
`ecdfp-intake` before building block 7 would materially improve the session.
