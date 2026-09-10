# ine_coverage_audit.md — INE eCDFP courseware coverage audit

**Built 2026-09-06** directly from `knowledge_base/_source_text/INE_Unit_01..10_*.md` — the OCR of
the ten official INE PDFs — and checked against `design/ine_session_mapping.md`,
`design/topic_map.md` (locked 6-session), and `design/plan_8_sessions.md` / `design/session_map.md`
(proposed 8-session).

**Premise of this audit.** INE's courseware is the mandatory coverage baseline: students must finish
100 % of it. Every finding below is measured against that requirement, not against the exam blueprint.

**Method.** Every INE unit file carries a `## Contents` table transcribed from the PDF, and a matching
set of `## N.N` body headings. Both were extracted mechanically and cross-checked (they agree row for
row in all ten units). Page weight = the page range of each section in the source PDF. All numbers in
this file are machine-counted, not estimated.

---

## 1 · Section inventory per unit

**Corpus totals: 10 units · 2,218 PDF pages · 196 contents rows · 173 distinct section numbers ·
2,196 pages carried inside a section range** (the remaining 22 are covers and front matter).

`Rows` = lines in the PDF contents table. `Sections` = distinct section numbers; INE returns to a
topic and re-uses its number, most heavily in Units 4 and 5, so `Rows` > `Sections` there.
`In-class` = pages classified `CORE` or `ORPHAN` in `ine_session_mapping.md` §10 — the pages that
must be taught in a room. `Share` is of the 2,196 indexed pages.

| Unit | Title | PDF pp | Indexed pp | Rows | Sections | In-class pp | Share | Relative size |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **U1** | Introduction to Digital Forensics | 193 | 190 | 25 | 22 | 162 | 8.7 % | medium |
| **U2** | Data Acquisition | 185 | 183 | 17 | 17 | 175 | 8.3 % | medium |
| **U3** | Data Representation & File Examination | 247 | 246 | 25 | 25 | 223 | 11.2 % | large |
| **U4** | Disks | 155 | 153 | 20 | 13 | 125 | 7.0 % | small |
| **U5** | File Systems | 317 | 315 | 36 | 25 | 274 | 14.3 % | large |
| **U6** | **Windows Forensics** | 429 | 426 | 21 | 20 | **389** | **19.4 %** | **largest by teaching load** |
| **U7** | **Network Forensics** | 455 | 452 | 33 | 32 | 317 | **20.6 %** | **largest by page count** |
| **U8** | Log Analysis | 121 | 119 | 6 | 6 | 87 | 5.4 % | small |
| **U9** | Timeline Analysis | 53 | 51 | 7 | 7 | 51 | 2.3 % | smallest |
| **U10** | Reporting | 63 | 61 | 6 | 6 | 61 | 2.8 % | smallest |
| | **Total** | **2,218** | **2,196** | **196** | **173** | **1,864** | 100 % | |

**Structural note on Units 4 and 5.** These two units are the only ones where INE's contents table
interleaves — it opens `4.3 Volumes & Partitions`, leaves it, returns, leaves again, returns twice
more. Unit 4 has 20 rows for 13 sections; Unit 5 has 36 rows for 25. `ine_session_mapping.md`
consolidates each repeat into one row with a combined page range (e.g. `4.4.3` → `135–136, 138,
140–141`). That is the correct handling and it loses nothing, but it is the reason two different
row counts are both true of the same corpus.

### The twelve heaviest sections in the corpus

These twelve sections carry 458 pages — 21 % of INE — between them.

| INE § | Section | Unit | pp | Treatment |
|---|---|:-:|---:|---|
| `3.7.4` | EXE Analysis | U3 | **69** | **ORPHAN** |
| `6.5.2` | User Hives | U6 | 62 | CORE |
| `6.5.1` | Registry Artifacts | U6 | 48 | CORE |
| `7.9.1` | HTTP (second block) | U7 | 47 | CORE |
| `7.5.2.2` | SSL/TLS | U7 | 43 | CORE |
| `7.1.1` | Network Attacks | U7 | **40** | **ORPHAN** |
| `5.2` | FAT File System Analysis | U5 | 39 | CORE |
| `6.9` | Skype Forensics | U6 | 37 | CUT |
| `6.5` | Windows Registry | U6 | 37 | CORE |
| `8.3` | Using Linux Tools for Log Analysis | U8 | 32 | CUT |
| `8.4` | Web Logs | U8 | **30** | **ORPHAN** |
| `6.7` | USB Forensics | U6 | 30 | CORE |

Three of the twelve largest sections in the whole courseware are orphans, and one of them is the
single largest section INE ships.

---

## 2 · Verification of the 178-section figure and the 15 orphans

### 2.1 The 178 figure is correct, and no section is missing

`ine_session_mapping.md` §10 was extracted and diffed against the OCR contents tables of all ten
units. Result:

| Check | Result |
|---|---|
| Distinct section numbers in OCR text | **173** |
| Distinct section numbers in `ine_session_mapping.md` §10 | **173** |
| Sections in OCR text but **absent** from the mapping | **0** |
| Sections in the mapping but not in the OCR text (invented) | **0** |
| Rows in the mapping | **178** = 173 distinct + 5 genuine repeats |
| The 5 repeats | `1.2`, `1.8`, `1.9`, `6.5.1`, `7.4` |
| Indexed pages, OCR | 2,196 — matches the mapping exactly |

**Verdict: the mapping accounts for every section in the OCR text. The 178 figure is sound and the
audit found nothing unmapped.** The only reconciliation needed is the 196-vs-178 row count, and that
is the Unit 4 / Unit 5 consolidation described in §1 — not a coverage gap.

### 2.2 The 15 orphans, verified — keep or drop

All fifteen were confirmed present in the OCR text at the stated page weights. **276 pages, 12.6 %
of the corpus.** The call below is made against the stated requirement that students finish 100 % of
INE's content: "drop" is reserved for material that genuinely carries no forensic technique.

| INE § | Section | pp | Call | Reasoning |
|---|---|---:|:-:|---|
| `3.7.4` | EXE Analysis (PE headers, imports, sections, resources, strings) | **69** | **MUST PLACE** | The largest single section INE ships. Five `Module_02` artifacts are stranded on it. The carry-through case teaches the malicious document and never opens the binary it drops. Not droppable under any reading of the baseline |
| `7.1.1` | Network Attacks | **40** | **MUST PLACE** (may compress) | 40 pages, and the only place INE names attack patterns on the wire. Defensible as recognition-only at ~15 min, but it cannot simply vanish |
| `8.4` | Web Logs (IIS W3C, Apache combined) | **30** | **MUST PLACE** | Two `Module_05` artifacts stranded. Web logs are the most common real-world log evidence and are examinable under Tools & Techniques |
| `6.8.1` | Internet Explorer | 24 | **MUST PLACE** (merge) | Merge with `6.8` into one browser-forensics topic, as `D35` already proposes. The IE-specific detail can compress hard; the technique cannot be dropped |
| `7.6.4` | Statistical Flow Analysis (NetFlow / IPFIX) | 16 | **MUST PLACE** | It is what remains when payload is encrypted — and after `7.5.2.2` SSL/TLS (43 pp) it is the answer to the question that section raises |
| `6.3.2` | ThumbCache | 15 | **PLACE as reference** | Real artifact, real technique, low classroom yield. A reference sheet plus a five-minute mention satisfies the baseline |
| `8.6` | Syslog | 15 | **PLACE as reference** | Format knowledge, not a technique. Reference sheet. Note it currently lands only in the Linux session |
| `7.7` | Email Forensics (`Received:` chains) | 13 | **MUST PLACE** | This is the attribution technique in Unit 7. Dropping it removes the only header-analysis content in the course |
| `10.6` | Report Samples | 12 | **MUST PLACE** | Students are told what a good report section contains and never shown one. For a mixed-ability room this is the highest-value 12 pages in Unit 10 |
| `7.8` | OSCAR | 11 | **MUST PLACE** | INE's own named methodology for network investigation. Examinable framing; cheap to teach |
| `6.8` | Browser Forensics | 9 | **MUST PLACE** (merge) | See `6.8.1` |
| `6.3.5` | Libraries (`.library-ms`) | 6 | **DROPPABLE → reference** | Genuinely marginal. A line in a Windows-artifact reference sheet discharges it |
| `6.3.6` | Windows Search History | 6 | **DROPPABLE → reference** | Same. Reference sheet |
| `4.4.3` | Hidden Protected Area / DCO | 5 | **MUST PLACE** | Five pages, but they describe storage hidden *from acquisition* — it belongs next to imaging, not in a footnote. The `Module_03` artifact already exists |
| `8.2` | Logging Infrastructure | 5 | **DROPPABLE → fold** | Framing pages. Fold into the Windows event-log block |

**Summary of the call: 11 of 15 must be placed (238 pp), 2 place as reference sheets (30 pp), 3 are
genuinely droppable into reference or a fold (17 pp).** Nothing in the fifteen is pure filler. The
`ine_session_mapping.md` recommendation of "seven new rows" is too thin against a 100 %-coverage
baseline — the honest number is eleven.

### 2.3 What was already declared out of scope (not orphans, but worth restating)

Three sections totalling **86 pages** are marked `CUT` in the mapping. Under a 100 % coverage
requirement these need an explicit, written student-facing exclusion:

| INE § | Section | pp | Status |
|---|---|---:|---|
| `6.9` | Skype Forensics | 37 | `CUT` — dated application, but it is 37 INE pages with no exclusion note in `scope_decisions.md` |
| `8.3` | Using Linux Tools for Log Analysis | 32 | `CUT` — yet the 8-session plan's Linux session depends on exactly this content. Contradiction, see §5 |
| `1.4.2.5` | Devices | 17 | `CUT` — mobile/IoT device sources; consistent with the cloud-and-mobile exclusion already written |

A further **129 pages** are `REF` (reference, not lecture time) and **68 pages** `PREWORK`. Those are
legitimate treatments, but they mean **966 pages — 44 % of INE — currently sit outside the classroom**
under the locked 6-session plan.

---

## 3 · Coverage gap check against the 8-session plan

### 3.1 Unit → session

`plan_8_sessions.md` describes sessions as *teaching blocks*, not as INE sections, so no INE-section
mapping exists for it. The table below was derived by matching each block to the INE sections that
supply it, using the plan's own "Build from" lines plus block-title matching.

| Session | Min | INE units and sections it carries | In-class pp |
|---|---:|---|---:|
| **S1** Foundations, Integrity & CoC | 201 | **U1** (all in-class) · U2 `2.1.2`, `2.2`, `2.5.1`, `2.5.3`, `2.6` · U10 `10.4` | 234 |
| **S2** Acquisition — Live Response, Memory & Media | 199 | **U2** (remainder) · U4 `4.1`, `4.2`, `4.2.2`, `4.2.3`, `4.4.3` | 181 |
| **S3** Data Representation & File Examination | 205 | **U3** (all in-class, incl. `3.7.4`) | 223 |
| **S4** Partitions & File Systems | 205 | U4 `4.3`, `4.4.1`, `4.4.2`, `4.5.1` · **U5** (all in-class) | 338 |
| **S5** Windows Forensics I — Registry & USB | 187 | **U6** `6.1`, `6.2`, `6.5`, `6.5.1`, `6.5.1.1`, `6.5.2`, `6.7` | 190 |
| **S6** Windows Forensics II — Execution & User Activity | 203 | **U6** `6.3*`, `6.4*`, `6.6`, `6.8`, `6.8.1` | 199 |
| **S7** Linux Forensics | 205 | **no INE unit** — TryHackMe rooms + U8 `8.3` (`CUT`) / `8.6` | **0** |
| **S8** Network, Timelines, Reporting & Capstone | 204 | **U7** · **U8** · **U9** · U10 (remainder) | 499 |
| | **1,609** | | **1,864** |

### 3.2 Sections with no home in the 8-session plan

Ten orphans were restored by the 8-session plan. **Five were not**, and two more are only weakly
covered. Verified by keyword search of `plan_8_sessions.md` against each orphan.

| INE § | Section | pp | Status in the 8-plan |
|---|---|---:|---|
| `7.1.1` | Network Attacks | **40** | ❌ **No home.** No block mentions network attacks. S8's "Identifying C2 traffic" covers a fraction |
| `6.3.2` | ThumbCache | 15 | ❌ **No home.** No block in S5 or S6 |
| `7.7` | Email Forensics | 13 | ❌ **No home.** No email block anywhere in the plan |
| `10.6` | Report Samples | 12 | ⚠️ **Weak.** S8's "The final forensic report" is `PARTIAL` 15 min and is the rubric, not worked samples |
| `6.3.5` | Libraries | 6 | ❌ **No home.** Not mentioned |
| `6.3.6` | Windows Search History | 6 | ❌ **No home.** Not mentioned |
| `8.2` | Logging Infrastructure | 5 | ⚠️ **Weak.** Implicitly folded into S8's Windows event-log block; not named |
| `6.9` | Skype Forensics | 37 | ❌ Still `CUT`, still unwritten as an exclusion |
| `8.3` | Linux Log Tools | 32 | ⚠️ Marked `CUT`, yet S7 lists it as a build source — see §5 |

**Restored by the 8-plan (confirmed present as blocks):** `3.7.4` EXE Analysis → S3 · `8.4` Web Logs
→ S7 · `6.8` + `6.8.1` Browser → S6 · `7.6.4` Statistical Flow → S8 · `7.8` OSCAR → S8 · `4.4.3`
HPA/DCO → S2 · `8.6` Syslog → S7.

**Uncovered total: 80 pages hard-uncovered (`7.1.1`, `6.3.2`, `7.7`, `6.3.5`, `6.3.6`), 17 pages
weakly covered (`10.6`, `8.2`).** Under a 100 %-coverage baseline these need blocks or written
exclusions before any build starts.

**One placement problem that is not a gap but reads like one.** `8.4` Web Logs (30 pp) and `8.6`
Syslog (15 pp) are both restored — but into **S7, the Linux session, which is not examinable.**
Web-log analysis is examinable content sitting in a non-examinable session. It should be lifted into
S8 or duplicated there.

---

## 4 · Weight imbalance

### 4.1 The rate

`ine_session_mapping.md` establishes the benchmark empirically: S1 as mapped carries 205 in-class
pages into 205 topic minutes — **1.00 page per minute** — with S2 at 0.70 and S3 at 1.05. That is
this course's demonstrated sustainable rate, and every figure below is measured against it. Each
session supplies **205 topic minutes** (240 min slot → 220 teaching → 205 after the break).

### 4.2 Load per session under the 8-session plan

| Session | In-class pp | Capacity (pp at 1.0/min) | pp/min | Verdict |
|---|---:|---:|---:|---|
| **S1** Foundations & Integrity | 234 | 205 | **1.14** | ⚠️ 29 pp over — absorbable |
| **S2** Acquisition | 181 | 205 | **0.88** | ✅ 24 pp of headroom |
| **S3** Data Representation | 223 | 205 | **1.09** | ⚠️ at benchmark, tight |
| **S4** Partitions & File Systems | 338 | 205 | **1.65** | ❌ **1.6× over — 133 pp homeless** |
| **S5** Windows I | 190 | 205 | **0.93** | ✅ correctly sized |
| **S6** Windows II | 199 | 205 | **0.97** | ✅ correctly sized |
| **S7** Linux | **0** | 205 | **0.00** | ⚠️ **205 min carrying zero INE pages** |
| **S8** Network, Timelines, Reporting & Capstone | 499 | 205 | **2.43** | ❌ **2.4× over — 294 pp homeless** |
| | **1,864** | 1,640 | 1.14 avg | |

### 4.3 What this says

**The 8-session plan fixes Windows and leaves the two real problems untouched.**

- **Windows is solved.** U6's 389 in-class pages split cleanly into S5 (190) and S6 (199). Both land
  under 1.0 pp/min. This is the plan's genuine achievement and it should be kept.
- **S8 is the 6-session plan's failure, unchanged.** The locked 6-plan had S6 at 504 pp / 2.46 pp/min.
  The 8-plan has S8 at 499 pp / 2.43. **Adding two sessions moved the network/timeline/reporting
  overload by 5 pages.** S8 is asked to teach at 2.8× the pace of S2 in the same plan.
- **S4 is the second pressure point.** U5 File Systems alone is 274 in-class pages — more than a
  session at benchmark rate — and S4 also carries U4's partitioning. 338 pp into 205 min.
- **S7 spends a full session on zero INE pages.** See §5.

### 4.4 Units against their allotted time

| Unit | In-class pp | Minutes it needs at 1.0 pp/min | Minutes allotted in the 8-plan | Balance |
|---|---:|---:|---:|---|
| **U7 Network Forensics** | 317 | 317 | ~110 (share of S8) | ❌ **−207 min · needs 2.9× its time** |
| **U6 Windows Forensics** | 389 | 389 | 390 (S5 + S6) | ✅ **balanced — the split worked** |
| **U5 File Systems** | 274 | 274 | ~165 (share of S4) | ❌ **−109 min · needs 1.7×** |
| **U3 Data Representation** | 223 | 223 | 205 (S3) | ⚠️ −18 min |
| **U1 Introduction** | 162 | 162 | ~150 (share of S1) | ⚠️ −12 min |
| **U8 Log Analysis** | 87 | 87 | ~25 (share of S8) | ❌ **−62 min · needs 3.5×** |
| **U2 Data Acquisition** | 175 | 175 | ~185 (S2 + share of S1) | ✅ balanced |
| **U9 Timeline Analysis** | 51 | 51 | ~46 (share of S8) | ✅ roughly balanced |
| **U10 Reporting** | 61 | 61 | ~45 (S1 + S8 shares) | ⚠️ −16 min |
| **U4 Disks** | 125 | 125 | ~130 (S2 + S4 shares) | ✅ balanced |

**The two named suspects, quantified.** Unit 06 (Windows) at 429 PDF pages and Unit 07 (Network) at
455 are indeed the two largest units — together **884 PDF pages, 40 % of the entire courseware**, and
**706 in-class pages, 38 % of all teaching demand**. But they are no longer the same problem:

- **Unit 06 is the largest by teaching load (389 in-class pp) and it is now correctly resourced.**
  The 8-plan's Windows split gives it 390 minutes. This is fixed.
- **Unit 07 is the largest by raw pages (455) but 135 of them are `PREWORK` or `REF`** — the entire
  `7.2*` TCP/IP fundamentals block (68 pp) is pre-work for a cohort that already holds CCNA, and DHCP,
  ICMP, ARP and cryptography (65 pp) are reference. **Its real teaching demand is 317 pages, and it is
  allotted roughly 110 minutes inside a shared S8. That is the single worst imbalance in the plan.**

**Unit 07 alone justifies a session of its own.** At benchmark rate it needs 1.5 sessions; it is
currently given about half of one.

---

## 5 · Exam-domain reality check

### 5.1 INE unit → eCDFP exam domain

The four domains and their published weights are transcribed in `coverage_matrix.md` §2. The table
below allocates each INE unit wholly to its dominant domain — the only allocation that can be made
mechanically, without judgement calls inside a unit.

| Exam domain | Exam weight | INE units | In-class pp | Share of INE demand | Δ vs exam |
|---|---:|---|---:|---:|---:|
| **Fundamentals of Digital Forensics** | 33 % | U1 · U3 · U6 · U10 | 835 | **44.8 %** | **+11.8 pp** |
| **Digital Forensics Tools & Techniques** | 27 % | U7 · U8 · U9 | 455 | **24.4 %** | −2.6 pp |
| **Preservation of Evidence** | 20 % | U2 | 175 | **9.4 %** | **−10.6 pp** |
| **Storage Device Fundamentals** | 20 % | U4 · U5 | 399 | **21.4 %** | +1.4 pp |
| | 100 % | | **1,864** | 100 % | |

**INE's page distribution does not match the exam blueprint, and this matters for how the course is
built.** Two divergences are large:

- **Fundamentals is 11.8 pp over-weighted in INE**, almost entirely because Unit 06 Windows Forensics
  (389 in-class pages, the largest teaching load in the corpus) sits inside it. Windows artifact work
  is really a Fundamentals/Tools hybrid, and INE's own volume on it exceeds the exam's appetite.
- **Preservation is 10.6 pp under-weighted in INE.** Unit 02 Data Acquisition is the only unit wholly
  dedicated to it (175 pp), but the exam wants 20 %. The gap is real and it is why chain of custody,
  evidence integrity and the hash-verify ritual must be taught from U1 `1.4.1*`, U10 `10.4` and the
  course's own ritual structure rather than from Unit 02 alone.

**This does not contradict `coverage_matrix.md`.** That file reconciles to within 1.2 pp on every
domain by allocating *inside* units — splitting Windows across Fundamentals and Tools, and counting
the per-session chain-of-custody ritual and the report template toward Preservation. That is the
correct approach. The point of the table above is that **the reconciliation is doing real work: you
cannot simply teach INE proportionally and land on the exam weights.** Any re-cut of the plan must
re-run that allocation rather than assume page-share equals domain-share.

### 5.2 What is in the plan and NOT in INE

| Plan element | Minutes | In INE? | Note |
|---|---:|:-:|---|
| **S7 — Linux Forensics (whole session)** | **205** | ❌ **No** | See below |
| S2 — "Acquiring a Linux host — dd/dc3dd, read-only mounting, loop devices" | 12 | ❌ No | Linux content inside an otherwise INE-sourced session |
| S1 — "Course roadmap — Windows, Linux and what each platform can and cannot show" | 10 | ⚠️ Partial | Framing; the cross-platform contrast is not INE material |
| S8 — Volatility 3 investigation | 10 | ⚠️ Thin | INE `2.5.6` Memory Forensic Tools is 8 pp; the depth taught exceeds the source |
| S4 — "NTFS journals — `$LogFile` and `$UsnJrnl`" | 10 | ⚠️ Thin | Not a named INE section; adjacent to `5.3.2` NTFS Attributes |
| S6 — "ShimCache and Amcache" | 28 | ⚠️ Partial | INE `6.4.2` Application Compatibility Cache is 10 pp; Amcache is not an INE section |

**The Linux finding, stated plainly.** The plan's own §2 confirms it and this audit independently
verified it against all 2,196 indexed pages: **INE's eCDFP courseware does not teach Linux forensics.**
There is no `bash_history`, no `crontab`, no "Linux forensics" heading; `ext2/3/4` appears once in
passing. The only Linux-adjacent INE content is `8.3` Using Linux Tools for Log Analysis (32 pp) — and
that section is already marked **`CUT`** in `ine_session_mapping.md`. So S7's INE backing is
**zero pages of `CORE` content, and at most 47 pages if the `CUT` decision on `8.3` is reversed.**

### 5.3 The non-examinable share

| Measure | Value |
|---|---|
| Topic minutes in the 8-session plan | **1,609** |
| Topic minutes on Linux (S7) | **205** |
| Plus Linux blocks inside other sessions (S2 `12` + S1 `10`) | **22** |
| **Non-examinable share — S7 alone** | **205 / 1,609 = 12.7 %** |
| **Non-examinable share — all Linux content** | **227 / 1,609 = 14.1 %** |
| Non-examinable share against full capacity (8 × 205 = 1,640) | 12.5 % / 13.8 % |
| Diploma hours spent on non-examinable material | **~3.4 h of 32 h** |

**The compounding effect.** S7 does not merely add non-examinable time — it consumes one of only
eight sessions while INE's own material is already 30 % over capacity. Excluding S7, the plan has
**7 × 205 = 1,435 minutes for 1,864 in-class INE pages — a 1.30 pp/min average, 30 % above the
demonstrated sustainable rate.** The two extra sessions bought over the locked 6-session plan
delivered one session of real INE relief (the Windows split) and one session of new,
non-examinable scope.

**This is a competence decision, not an exam decision**, and it is defensible for a cohort that
already holds Linux Administration. But three things follow and should be written down:

1. **Tell students.** 12.7 % of the diploma is not on the exam. `scope_decisions.md` should say so.
2. **`coverage_matrix.md` must be re-derived excluding S7**, as `plan_8_sessions.md` §5 already
   concedes — otherwise Linux minutes are silently counted toward exam-domain weights they cannot
   satisfy.
3. **Resolve the `8.3` contradiction.** A section cannot be both `CUT` for scope and a named build
   source for a full session.

---

## 6 · Summary of findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **The 178-section figure is verified correct.** 173 distinct sections + 5 repeats. No INE section is absent from `ine_session_mapping.md` | §2.1 — mechanical diff, zero discrepancies |
| 2 | The 196-vs-178 row difference is the Unit 4 / Unit 5 contents-table interleaving, correctly consolidated — not a gap | §1 |
| 3 | **11 of the 15 orphans must be placed, not 7 as recommended.** Only 3 are genuinely droppable (17 pp) | §2.2 |
| 4 | **The 8-session plan leaves 80 pages hard-uncovered** — `7.1.1`, `6.3.2`, `7.7`, `6.3.5`, `6.3.6` — plus 17 weakly covered | §3.2 |
| 5 | Examinable web-log content (`8.4`, 30 pp) is placed in the non-examinable Linux session | §3.2 |
| 6 | **S8 is 2.43 pp/min — the 6-plan's failure, unmoved.** Two extra sessions improved it by 5 pages | §4.2 |
| 7 | **S4 is 1.65 pp/min.** U5 File Systems alone (274 pp) exceeds one session | §4.2 |
| 8 | **The Windows split works.** U6's 389 pp into S5 (190) + S6 (199), both under 1.0 pp/min | §4.4 |
| 9 | **Unit 07 is the worst imbalance: 317 in-class pages into ~110 minutes — it needs 2.9× its allotted time** | §4.4 |
| 10 | **S7 Linux carries zero INE pages.** 12.7 % of the diploma is non-examinable; 14.1 % counting Linux blocks elsewhere | §5.2, §5.3 |
| 11 | Excluding S7, the plan runs at **1.30 pp/min — 30 % over the demonstrated sustainable rate** | §5.3 |
| 12 | **INE's page distribution does NOT match the exam blueprint.** Fundamentals +11.8 pp over, Preservation −10.6 pp under. `coverage_matrix.md`'s within-unit allocation is doing real work and must be re-run for any new cut | §5.1 |

### What this audit recommends

1. **Split S8.** Network forensics needs its own session — Unit 7 is 317 in-class pages. This is the
   single highest-value change available and it is worth more than the Linux session.
2. **Place the five hard-uncovered orphans** (80 pp) or write explicit exclusions for them.
3. **Move `8.4` Web Logs out of S7 into the network/log session** — it is examinable content.
4. **Write the non-examinable share into `scope_decisions.md`** and re-derive `coverage_matrix.md`
   excluding S7.
5. **Resolve `8.3`** — `CUT` or a build source, not both.
6. If the diploma cannot grow past eight sessions, **the honest trade is S7 Linux against a network
   session.** Linux is 205 minutes of non-examinable time; Unit 7 is 317 pages of examinable INE
   material currently taught at 2.9× speed. Under a mandatory 100 %-INE-coverage baseline, that
   trade only goes one way.
