# session_blueprint.md — eCDFP content methodology, rebuilt

**Built 2026-09-06 (`D59`) from a three-source review.** This file says *how much* content each
session carries, *where every piece came from*, and *how a session is delivered*. The row-level map
is `topic_map.md`; this is the reasoning behind it.

Sources reviewed in full — audits kept in `design/review/`:

| Source | What it is | Audit |
|---|---|---|
| `Resources/Instructor` | 8 sessions the previous instructor actually delivered — 380 slides, 242 screenshots | `review/instructor_audit.md` |
| `Resources/INE_eCDFP` | 10 official units — 2,218 pages, 173 distinct sections. **The mandatory coverage baseline** | `review/ine_coverage_audit.md` |
| `Resources/THM` | 33 TryHackMe room extractions — the delivery model to copy | `review/thm_harvest.md` |

---

## 1 · What the review found

### 1.1 Total volume is right — distribution was not

The previous instructor's eight sessions carry **~1,176 evidenced teaching minutes**. Our budget is
**1,230**. The course was never too big. It was mis-distributed:

| | Sessions 1–5 | Session 6 |
|---|---|---|
| INE units carried | one each | **four** (U7 Network, U8 Logs, U9 Timeline, U10 Reporting) |
| INE pages | 1,680 across five sessions | **516 in one session** |
| Rate against a 1.0 pp/min benchmark | 0.9–1.1 | **2.43** |
| What the previous instructor spent on the same material | — | **462 min** (his S6 200 + S7 194 + S8 68) |

**We were asking one 205-minute session to deliver 462 minutes of material.** That is the single
largest defect the review found, and everything in §2 follows from fixing it.

### 1.2 Eleven INE sections had no home — not seven

The existing mapping declared 15 orphans and recommended placing seven. Re-checked against the OCR
text: **173 distinct sections, all accounted for, but eleven orphans genuinely must be placed** —
238 pages. The largest is **§3.7.4 Executable Analysis, 69 pages, the biggest single section INE
ships**, dropped entirely by the `D58` re-cut. All eleven now have a row (§3).

### 1.3 The previous material's real weaknesses

Measured, not asserted — these are what our build must not repeat:

| Defect | Evidence | Our rule |
|---|---|---|
| **Six challenges, zero answer keys** | Nothing he set is resolved anywhere; three were shared by dead file-host links | Every challenge ships with a key, in-repo |
| **The CTF does not exist** | The deck titled *Reporting & CTF Challenge* contains no brief, evidence, questions or scoring | Case 06 is built and graded (§2.6) |
| **Six phantom labs** | S03 announces MBR repair, GPT repair and MFTECmd and shows none | Never plan a build from his lab-agenda slides |
| **No case carries across sessions** | Every lab ran against his own live machine | `EVS-02` carries S2 → S6 |
| **No finding is ever written down** | 15 registry keys opened in S04, no conclusion stated | Findings vs interpretation, every session, `D7` |
| **Content taught but never shown** | ShimCache (in a slide *title*), Prefetch, ShellBags, RecentDocs, the whole plaso chain | A topic without a demo is not a topic |

Hard errors to correct where we reuse his material: *"triage = three images"* (S01 s35); AES/DES/RC4
listed under a *Hash function* heading (S06 s35); the timestomp rule stated backwards (S07 pt2 s19);
`MCAB` for MACB; `ControlSet001` read without checking `Select\Current`.

### 1.4 What is genuinely good in his material — lift it

1. **S02's paired recovery demo** — `$I`/`$R` Recycle Bin recovery (the name survives) followed
   immediately by PhotoRec carving (files come back named by offset). Two labs, one lesson. → S4/S5.
2. **S03's corrupted-GPT hex walkthrough** — disk overwritten with `41`, `EFI PART` found at
   `00000200`, primary header placed beside its backup. INE never shows a damaged disk. → `S4-04`.
3. **S01's continuous acquisition lab** — image → verify → RAM → logical/AD1 → mount → triage, with a
   three-tool mount comparison where Arsenal's *write original* sits on screen as a selectable
   option. → `S2-08`.
4. **S04's "Disk Analysis Process" roadmap slide** — a whole curriculum on one page. → S5 opener.
5. **S08 slide 30** — *"Don't say 'in my opinion Mr. X has committed this crime.' You are not the
   judge."* → moved to **`S1-04`**, where it shapes the report template from day one.

---

## 2 · The rebuild — 6 × 4 h held (`D1`), content redistributed

### 2.1 The three moves that fixed Session 6

| Move | Recovers | Justification |
|---|--:|---|
| **Capstone leaves session time** → graded take-home CTF released at the end of S5, debriefed in S6 | **45 min** | The previous instructor promised a CTF and never built one. As a take-home it becomes real work with a real rubric instead of 45 rushed minutes |
| **Windows event logs + SID→name mapping move to S5** | **14 min** | The artifacts already live there. It also closes `GAP-09` — Case 05 asked *which user* and nothing mapped a SID to a name |
| **INE's TCP/IP block (§7.2\*, 135 pp) declared explicit pre-work** | **~110 min** | CCNA → SOC → eCIR already taught TCP/IP, Wireshark display filters, tcpdump, pcap, DNS/DHCP/ARP/TLS. Stated as a prerequisite check, not silently assumed |

Session 6 becomes **Network Forensics, Logs, Timelines & Reporting** — four subjects with honest
time each, and its per-session domain split lands within 1 minute of the locked target.

### 2.2 Session content volume — the calibration table

| # | Session | INE units (in-class pp) | Previous instructor | THM rooms backing it | Our budget |
|---|---|---|--:|---|--:|
| **S1** | Foundations, Integrity & Chain of Custody | U1 (162) | S01 part | Cold System Forensics · Forensic Imaging | 205 |
| **S2** | Acquisition — Disk, Memory & Live Response | U2 (175) + §4.4.3 | S01 part | Forensic Imaging · Memory Acquisition · Windows Incident Surface · Expediting Registry Analysis | 205 |
| **S3** | Data Representation, Hidden Information & File Examination | U3 (223) | S02 (131) | File Carving · Autopsy | 205 |
| **S4** | Storage Devices, Partitions & File Systems | U4 (125) + U5 (274) | S03 (122) | MBR/GPT · FAT32 · NTFS · File Carving · **Diskrupt** | 205 |
| **S5** | Windows Forensics — Registry, User Activity & Execution | U6 (389) | S04+S05 (277) | Compromised Windows · User Activity · User Accounts · Applications · **DiskFiltration** · **Blizzard** | 205 |
| **S6** | Network, Logs, Timelines & Reporting | U7 (182 net of pre-work) + U8 (87) + U9 (51) + U10 (61) | S06+S07+S08 (462) | Windows Network Analysis · **Logless Hunt** · Volatility Essentials · Memory ×4 | 205 |

**Read the S4, S5 and S6 rows together.** S4 and S5 carry the material nothing in the prerequisite
stack ever taught — file systems and Windows artifacts. They are the course. S6 looks worst on page
count and is the most pre-known. Never size a session from INE page count alone.

### 2.3 Where the eleven homeless INE sections landed

| INE § | Title | pp | Now taught in |
|---|---|--:|---|
| `3.7.4` | Executable Analysis | 69 | **`S3-05`** — restored, 25 min |
| `7.1.1` | Network Attacks | 40 | **`S6-06`** — new, 12 min |
| `8.4` | Web Server Logs | 30 | **`S6-10`** — new investigation, 25 min |
| `6.8` + `6.8.1` | Browser Forensics + IE | 33 | **`S6-07`** — new, with email (closes `GAP-01`/`D35`) |
| `7.6.4` | Statistical Flow Analysis | 16 | `S6-05` — merged |
| `6.3.2` | ThumbCache | 15 | `S3-06` — merged into image forensics |
| `8.6` | Syslog | 15 | `S6-10` |
| `7.7` | Email Forensics | 13 | **`S6-07`** — the only header-analysis content INE ships |
| `10.6` | Report Samples | 12 | `S6-09` |
| `7.8` | OSCAR methodology | 11 | `S6-01` — merged |
| `4.4.3` | HPA and DCO | 5 | **`S2-07`** — new, 8 min |
| `8.2` | Logging Infrastructure | 5 | `S6-10` — folded |

**Dropped on the record, not by accident:** `6.3.5` Libraries (6 pp) and `6.3.6` Search History
(6 pp) — superseded by shellbags and browser history respectively.

### 2.4 Session 3 — the trade that was made

`D58` added steganography, embedded data and image forensics to S3 and in doing so dropped INE's
largest section. The rebuild keeps the hidden-information material but stops it outweighing
executable analysis:

| Block | `D58` | `D59` | Change |
|---|--:|--:|---|
| Endianness and encodings | 15 | **10** | trimmed — hex is now owned by `S1-09` |
| Metadata and EXIF | 25 | 25 | — |
| Steganography | 25 | **33 (merged)** | merged with embedded/appended data; detection taught once |
| Embedded and appended data, polyglots | 20 | ↑ merged | — |
| Malicious document structure | 25 | 25 | — |
| **Executable analysis — PE headers, imports, sections, strings** | **absent** | **25** | **restored** |
| Image forensics | 20 | **12** | trimmed; absorbs ThumbCache |

The malicious document and the executable it drops are now one evidence chain: `S3-08` examines the
document, and the dropped binary is what `S3-05` taught the student to read.

### 2.5 Session 5 — the densest session, and how it holds

S5 carries INE Unit 6 — 389 in-class pages, the largest unit — against the previous instructor's
277 evidenced minutes. It holds because **~40 of those 277 minutes were literal duplication**
(10 of his S05's 23 slides repeat S04) and because THM covers this area more strongly than any
other: eight rooms, all teaching-grade.

Every integrated block was trimmed 2–4 minutes to fund the incoming event-log block. Nothing was
cut. Hands-on time is **185 minutes**, the highest in the course.

### 2.6 The capstone — Case 06

Built, not promised. Released at the close of S5, worked between sessions, debriefed in `S6-12`.

| | |
|---|---|
| **Evidence** | `EVS-02` disk image + `EVS-03` memory dump + `EVS-08` pcap and logs — the carry-through incident, end to end |
| **Model** | THM's *Blizzard* — reverse-order IR: impact → pivot → root cause, each answer becoming the next question |
| **Deliverable** | A written forensic report on the `S1-04` template, graded against the `D20` rubric |
| **Grading** | Findings vs interpretation separated; an unsupported interpretation costs more than a missed artifact |
| **Answer key** | Ships with the brief, in-repo |

---

## 3 · How a session is delivered — the fixed rules

Distilled from the THM harvest (`review/thm_harvest.md`) and binding on every session build.

### 3.1 The order never inverts

> **concept → where it lives → read it manually → read it with a tool → how an attacker abuses it →
> apply it to the case → unguided challenge**

Theory is ~25 % of session time, front-loaded once, never revisited. Vocabulary goes in the pre-read.

### 3.2 Every artifact gets six moves

1. What it is
2. Where it lives
3. What it proves
4. **What it does NOT prove**
5. How to parse it
6. The caveat

**Write moves 4 and 6 first** — every source we have is weakest there, and they are what separates
an analyst from a tool operator. `S5-06` (ShimCache: presence, not execution) is the model.

### 3.3 The nine build rules

1. **Open with a reported symptom, never an artifact name.** The scenario supplies the first pivot.
2. **Manual first, tool second, always** — and say why: structure is what lets you adjudicate when
   two tools disagree.
3. **Collect once, parse many.** One command shape, several inputs (MFTECmd → `$MFT`, `$J`, `$I30`).
4. **Every question is single-artifact, single-answer, and the sequence is a narrative.**
5. **State the answer format every time** — timestamp mask, timezone, units, sector size, defanged.
6. **A question stem says what to find, never why it happened.**
7. **Ask one "cannot be determined" question per session.** None of the 33 THM rooms does this. It
   is the cheapest way to teach the limits of evidence, and it is `D7` made practical.
8. **Where two artifacts record one event, make the disagreement the finding** — `pslist` vs
   `psscan`, `$SI` vs `$FN`, Defender log vs DetectionHistory.
9. **No answer may be a credential or a data subject's PII** (`D41`/`D47`). Where a source lab
   resolves to one, the question is excluded **and the exclusion is taught as the standard it is**.

### 3.4 Ramp difficulty by removing scaffolding

Not by relabelling it. Each lab carries a one-line harder mode — *"now answer using only the hex
editor"* — for the students who finish early. This is how one classroom serves mixed levels.

### 3.5 Scenario-writing rules

- Blame a **conclusion, not a person**. THM's *Logless Hunt* opens with a CTO asserting *"all event
  logs are empty, so hackers did not breach the servers"* — the best single opening in the corpus,
  and the one that opens our S6.
- State the anti-forensics up front; narrate the **discovery**, not the attack.
- The entry point is a **control failure**, not a stupid user.
- Include one artifact that does not fit, and one strand unrelated to the incident.

### 3.6 Every page carries a picture or a reason not to

Carried forward from `D58`. Micro-lab pages get a before/after or flow diagram, never three stacked
text panels. `.gui` panels are for real command output only, one per page.

### 3.8 Visual density — the rule the pages are measured against (`D61`)

The first S1 build failed on exactly this, and the failure is measurable, not a matter of taste:

| Measured on the old build | S1 | S2 | Rule |
|---|--:|--:|--:|
| Visible words on the page | **11,111** | 7,163 | **≤ 4,000** |
| Average words per page | **462** | 298 | **≤ 180** |
| Worst single page | **1,160** | 590 | **≤ 250** |
| Teaching pages carrying **no** visual | **5** | 6 | **0** |
| Times "hash" appears in the page text | **86** | — | **≤ 12** |
| Times "magic bytes" — a 22-minute hands-on block — appears | **1** | — | — |

**The diagnosis.** The page was doing two jobs at once: teaching surface *and* textbook. That is
why one concept was restated in eight places and the practical block that anchors the session
appeared once.

**The split that fixes it, and it is already in the document set:**

| Artefact | Job | Register |
|---|---|---|
| `docs/session-NN/index.html` | **the teaching surface** — what is on the projector | a visual with a caption |
| `packages/session-NN/student_guide.md` | **the textbook** — self-review, alone, after class | prose, as long as it needs to be |
| `packages/session-NN/instructor_guide.md` | the script — demo commands and expected output | prose + exact commands |

Prose that explains a concept a second time does not belong on the page. It belongs in the
student guide, once.

**The five checks, run by the Part 9 gate:**

1. **Every teaching page carries at least one visual** — inline SVG, `.gui`, `.artifact` 6-box,
   a table, or an annotated hex block. A page of prose alone is a defect.
2. **Never more than three consecutive `<p>`.** After three, a visual or a list must appear.
3. **Average ≤ 180 visible words per page; no page over 250.**
4. **A concept is named on at most two pages** — the page that teaches it, and the page that uses
   it. Tool names, the case name and the exhibit ID are exempt.
5. **The text is the caption for the visual, not the other way round.** If the diagram can be
   removed without loss, it was decoration and the page has not been built yet.

**Why this is not "less content".** The topic minutes do not change — 130 + 60 + 15 stands. What
changes is that a 10-minute theory block becomes one diagram the instructor talks over for ten
minutes, instead of 460 words the students read ahead of him and then stop listening.

### 3.7 The ownership rule (`D58`, still binding)

Each idea is taught in exactly one block and afterwards only *used*. A later session may name it in
one clause; it may not re-explain it. One documented exception: `verified` is taught twice on
purpose — S1 reads it in a log it was *handed*, S2 in a log the student *produced*.

---

## 4 · What is still open

| Item | Owner | Note |
|---|---|---|
| `EVS-02/03/04/09` not yet acquired | `ecdfp-evidence` | S2's evidence gate is still failing; S3–S6 all depend on `EVS-02` |
| `EVS-06` must now also carry the dropped executable | `ecdfp-evidence` | New requirement from `S3-05` |
| `EVS-08` must now also carry web-server and syslog sets | `ecdfp-evidence` | New requirement from `S6-10` |
| Case 06 brief, evidence bundle and answer key | session build | Does not exist in any source |
| Answer keys for every challenge | session build | Zero exist in the previous material |
| `coverage_matrix.md` per-session hours | — | Still allocated by hand, not row-derived; the course-level reconciliation is the gate that passed |
| `Module_06` | `ecdfp-intake` | Not required — Linux stays out of scope per `D38` |
