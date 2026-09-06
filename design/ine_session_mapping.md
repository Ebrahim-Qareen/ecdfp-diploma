# ine_session_mapping.md — INE eCDFP content → session mapping and capacity analysis

**Built 2026-08-29 from `knowledge_base/` alone.** Every INE section in this file comes from the
§8 *Section index → source pages* tables of `Module_01`–`Module_05`, which are themselves the
reconciled OCR of the ten INE unit PDFs. Nothing here is estimated from memory.

**This file is analysis, not authority.** `design/topic_map.md` remains the locked 6-session plan
(`D23`–`D26`) and only `ecdfp-intake` may change it. This file measures INE's body of knowledge
against that plan, answers *does it fit six sessions*, and proposes what to do about the answer.
Nothing here is applied until Ebrahim decides and a `DECISIONS.md` row is written.

> **Publication note (`D22`).** `design/` is tracked and the repo is public. §10 below reproduces
> INE's section titles — that is a third-party table of contents. Either gitignore this file or
> reduce §10 to section numbers and page counts before the next push. Flagged, not decided.

---

## 1 · The question, and the answer

**Question.** Does INE's eCDFP courseware fit six 4-hour sessions, or does it need more?

**Answer. No — not as taught content. Six sessions is exam-sufficient and content-insufficient.**

Two different things are being asked of the six sessions and only one of them works:

| | Verdict | Evidence |
|---|---|---|
| **Covering the exam's four domains at their published weights** | ✅ **Six is enough** | `topic_map.md` reconciles F 32.4 / T 27.3 / P 21.5 / S 18.7 against the exam's 33/27/20/20 — every domain inside 0.9 pp (`D24`) |
| **Teaching INE's material at the pace S1–S3 actually run at** | ❌ **Six is not enough — it needs nine** | 1,864 in-class pages ÷ 205 min per session at the measured 1.0 pages/min = **9.1 sessions** |

The gap is not spread evenly. **S1, S2 and S3 are correctly sized. S4, S5 and S6 are carrying
roughly twice what they can teach**, and S6 is carrying two and a half times.

Three independent measurements agree on that, and they are in §3, §4 and §5.

---

## 2 · Method — how "demand" was measured

**The corpus.** 10 INE units · 2,218 PDF pages · 178 section rows (173 distinct section numbers;
five sections appear twice where INE returns to a topic) · 2,196 pages carried inside a section
range, the remaining 22 being covers and front matter. Condensed into 111 artifacts and 118 tool
rows across the five `Module_0N` files.

**The supply.** `D15`/`D23`: 240 min slot → 220 min teaching → **205 min of topic time** per
session. Six sessions = **1,230 topic minutes**.

**The unit of demand is one INE page.** Crude, but it is the only measure that exists uniformly
across all ten units, it is machine-countable, and it can be checked. Two independent
cross-checks (§4 artifact load, §5 the instructor's own delivery) point the same way, which is
the reason to trust it.

**The rate.** Every section was classified into one of seven treatments:

| Treatment | Meaning | Pages | Share |
|---|---|---:|---:|
| `CORE` | taught in the room | 1,588 | 72.3 % |
| `ORPHAN` | INE covers it, **`topic_map.md` has no row for it** | 276 | 12.6 % |
| `REF` | cheat-sheet / reference page, not lecture time | 129 | 5.9 % |
| `CUT` | declared out of scope | 86 | 3.9 % |
| `PREWORK` | issued before the session as required pre-read | 68 | 3.1 % |
| `HOMEWORK` | drill done outside class | 43 | 2.0 % |
| `SKIP` | divider slide / no forensic content | 6 | 0.3 % |
| | **Total** | **2,196** | **100 %** |

`CORE` + `ORPHAN` = **1,864 pages that have to be taught in a room**. That is the demand figure
used throughout.

**The benchmark rate is measured, not assumed.** S1 as currently mapped carries 205 in-class
pages into 205 topic minutes — **exactly 1.00 page per minute**. S2 runs at 0.70 and S3 at 1.05.
So **~1.0 page/min is this course's demonstrated sustainable classroom rate**, on material that
already includes a 60-minute investigation block and the 15-minute chain-of-custody ritual.
Everything below is measured against that.

---

## 3 · Measurement 1 — page load per session, against the locked 6-session map

| Session | INE units | In-class pages | pp/min | vs 1.0 benchmark |
|---|---|---:|---:|---|
| **S1** Foundations, Integrity & CoC | U1 · U2 §2.5.1/2.5.3/2.6 · U10 §10.4 | 205 | **1.00** | ✅ at benchmark |
| **S2** Acquisition | U2 | 144 | **0.70** | ✅ 61 pp of headroom |
| **S3** Data Representation & File Exam | U3 | 216 | **1.05** | ✅ at benchmark |
| **S4** Storage, Partitions & File Systems | U4 · U5 · U3 §3.4.1.1 | 406 | **1.98** | ❌ **2.0× over** |
| **S5** Windows Forensics | U6 | 389 | **1.90** | ❌ **1.9× over** |
| **S6** Network, Timelines, Reporting & Capstone | U7 · U8 · U9 · U10 · U1 §1.4.1.3/1.7 | 504 | **2.46** | ❌ **2.5× over** |
| | | **1,864** | 1.52 avg | |

Read the shape, not just the totals. The first half of the course is paced correctly and the
second half is not. **S6 is asked to teach at three and a half times the pace of S2.**

At the benchmark rate the six sessions can hold **1,230 pages**. The material needing a room is
**1,864**. The shortfall is **634 pages — 34 % of what is left after the cuts in §2 have already
been made.** Counted against the whole corpus, keeping six sessions means **966 of 2,196 pages
(44 %) never get classroom time**.

### What it takes to reach nine

| Sessions | Topic minutes | In-class pages that fit @1.0 pp/min | Pages left outside the room |
|---:|---:|---:|---|
| 6 (locked, `D1`) | 1,230 | 1,230 | 966 · **44 %** |
| 8 (the instructor's original shape) | 1,640 | 1,640 | 556 · **25 %** |
| **9 (recommended, §9)** | **1,845** | **1,845** | **351 · 16 %** — and §2 already justifies 332 of them |
| 11 (nothing demoted at all) | 2,255 | 2,196 | 0 |

**Nine is the point where the demotions stop being cuts and start being editorial judgement.**
At six, 634 pages of taught material have to be thrown out on top of the ones already justified.

---

## 4 · Measurement 2 — artifact load, the independent cross-check

Pages could mislead — INE's slide density varies. So the same question was asked of the **111
artifacts** in the `Module_0N` §2 sections, which is the unit the course actually teaches in.

`R10` fixes what one artifact costs: six boxes — what it is · where it lives · what it proves ·
**what it does NOT prove** · how to parse it · one anti-forensics caveat. That is the course's own
minimum, and `D7`/`D20` make box four graded.

Only the **130 integrated minutes** teach artifacts; the 60-minute investigation and the 15-minute
ritual do not.

| Session | Artifacts | Integrated min | **Minutes per artifact** |
|---|---:|---:|---:|
| S1 | 5 | 130 | **26.0** |
| S2 | 9 | 130 | **14.4** |
| S3 | 13 | 130 | **10.0** |
| S4 | 21 | 130 | **6.2** |
| S5 | 34 | 130 | **3.8** ❌ |
| S6 | 29 | 130 | **4.5** ❌ |

**S5 gives each artifact 3.8 minutes.** Six boxes, one of which — the ShimCache
*presence-versus-execution* box — runs to 257 words in the knowledge base precisely because it is
the misreading the whole session exists to prevent. It cannot be delivered, demonstrated and
checked in 3.8 minutes, and `S5-06` is where the course either lands that point or does not.

Same conclusion as §3, from a different measure: **S1–S3 are sized right; S4–S6 are not.**

---

## 5 · Measurement 3 — the empirical one: it already took eight, and eight was not enough

The material has been delivered before, by Eng. Mohab Mustafa, in **eight sessions across nine
decks (380 slides)**. `knowledge_base/instructor/README.md` records where those eight collapse
into six:

| Instructor session | Slides | → eCDFP |
|---|---:|---|
| 01 Introduction & Acquisition | 70 | S1 **+** S2 |
| 02 Data Representation & File Examination | 38 | S3 |
| 03 Disks & File Systems | 40 | S4 |
| 04 Practical Windows Forensics | 39 | **S5** |
| 05 Practical Windows Forensics pt 2 | 23 | **S5** |
| 06 Network Forensics | 72 | **S6** |
| 07 Log & Timeline Analysis (2 decks) | 68 | **S6** |
| 08 Reporting & CTF | 30 | **S6** |

**170 slides — three whole sessions — land in S6, alongside the capstone.** Two land in S5.

And the eight sessions did **not** cover the material either. Each deck's §5 lists what INE covers
and the delivery omitted. Taken together, the eight-session delivery skipped: the entire
super-timeline toolchain (no plaso, no body file, no `mactime`, no Timeline Explorer), ShimCache,
Prefetch, ShellBags, RecentDocs, LNK and Jump Lists, MountPoints2, `setupapi.dev.log`, Recycle
Bin, Volume Shadow Copies, Thumbcache, browser artifacts, event logs, log clearing (`1102`/`104`),
C2 beaconing, `tcpdump` and capture methodology, statistical flow analysis, email header
attribution, and INE's 28 pages on network evidence acquisition — plus the CTF that gives the
deck its title and does not exist in it.

Session 06's own note puts it plainly: *"it costs roughly three hours before anyone opens
Wireshark, and the rebuilt S6 has 141 minutes total for network work plus timelines, reporting and
the capstone… this deck cannot be delivered as-is."*

**Eight sessions with those omissions ≈ nine sessions with them restored.** The page model says
9.1. The two agree.

---

## 6 · If six sessions stay locked — this is the bill, stated in advance

`D1` locks 6 × 4 h. If that does not move, **634 pages of currently-taught material leave the
room** and the honest thing is to name them now rather than discover them at minute 190. Per
session, at the 1.0 pp/min benchmark:

| Session | Now | Ceiling | **Must shed** | What that actually means |
|---|---:|---:|---:|---|
| S3 | 216 | 205 | 11 | trivial — trim the hex-conversion drills further |
| **S4** | 406 | 205 | **201** | you lose either the whole FAT block (§5.2*, 88 pp) plus HDD/SSD internals (52 pp) plus the carving toolchain (47 pp) — or half of NTFS. FAT and NTFS are both Storage-domain exam content |
| **S5** | 389 | 205 | **184** | all four orphans (Thumbcache, Libraries, Search history, browser — 60 pp) **plus** ~124 pp more: realistically VSS (25), Jump Lists (23), Recycle Bin (26), ShellBags (18) and half the user-hive walk (31). That is instructor session 5 in its entirety |
| **S6** | 504 | 205 | **299** | all eight orphans (142 pp) **plus** ~157 pp of protocol grounding: SSL/TLS (43), both HTTP blocks (73), network evidence acquisition (28). What remains is a Wireshark tour with no protocol floor under it — the exact failure the instructor's 60 fundamentals slides existed to avoid |
| S1 · S2 | 349 | 410 | — | S2 has 61 pp of headroom; it is the only slack in the course |

**Net: −634 pages.** Three consequences worth stating to students in week one rather than
discovering later:

1. **S6 stops being a session and becomes a survey.** Network + logs + timelines + report +
   capstone in 205 minutes is four topics and an exam at a pace where nothing is practised twice.
2. **The `D20` rubric loses its teeth in S5 and S6.** Criterion 4 (findings vs interpretation) is
   graded every session; at 3.8 min/artifact there is no time to *demonstrate* the distinction,
   only to assert it.
3. **`S6-09`, the capstone, is 45 minutes at the end of the most compressed session in the
   course** — after network, logs, timelines and reporting have all been taught the same day.

None of these is a reason six cannot run. They are the price, and the price is payable if it is
declared. What is not defensible is running six and pretending the content fits.

---

## 7 · The 15 orphans — INE content with no `topic_map.md` row

**276 pages, 12.6 % of the corpus.** These are not gaps in the sense of §2's exit gate (INE covers
them; the source is there). They are the reverse: **material with a source and no home.** Each one
is either a proposed `topic_map.md` row or a written scope exclusion — `ecdfp-intake` owns which.

| INE § | Section | Pages | Lands in | Recommendation |
|---|---|---:|---|---|
| `3.7.4` | EXE Analysis (PE headers, imports, sections, resources, strings) | **69** | S3 | **Add a topic.** Five `Module_02` artifacts have no session. `D19`'s chain runs *malicious document → malware execution*; the map teaches the document and never opens the binary |
| `7.1.1` | Network Attacks | 40 | S6 | Scope-exclude, or fold into `S6-05` as recognition-only |
| `8.4` | Web Logs (IIS W3C, Apache combined) | 30 | S6 | **Add a topic.** `S6-06` is Windows event logs only; two `Module_05` artifacts are stranded |
| `6.8.1` | Internet Explorer | 24 | S5 | Merge with `6.8` below into one browser-forensics topic (`D35`) |
| `7.6.4` | Statistical Flow Analysis (NetFlow/IPFIX) | 16 | S6 | **Add.** It is what you have left when payload is encrypted |
| `6.3.2` | ThumbCache | 15 | S5 | Reference sheet |
| `8.6` | Syslog | 15 | S6 | Reference sheet — Linux host forensics is already out of scope |
| `7.7` | Email Forensics (`Received:` chains) | 13 | S6 | **Add** — it is the attribution technique |
| `10.6` | Report Samples | 12 | S6 | **Add.** Already flagged as the biggest practical gap for a mixed-ability room: students are told what a good section contains and never shown one |
| `7.8` | OSCAR | 11 | S6 | **Add.** It is INE's named methodology for network investigation |
| `6.8` | Browser Forensics | 9 | S5 | See `6.8.1` |
| `6.3.5` | Libraries (`.library-ms`) | 6 | S5 | Reference sheet |
| `6.3.6` | Windows Search History | 6 | S5 | Reference sheet |
| `4.4.3` | Hidden Protected Area / DCO | 5 | S4 | **Add** — the `Module_03` artifact exists and HPA/DCO hides data from acquisition |
| `8.2` | Logging Infrastructure | 5 | S6 | Fold into `S6-06` |

**Seven of the fifteen are recommended as new rows** (`3.7.4`, `8.4`, `7.6.4`, `7.7`, `10.6`,
`7.8`, `4.4.3`) — 186 pages. They do not fit the six-session budget: every session already totals
exactly 220 (`D26`), so **any one of them displaces something else.** That constraint is itself an
argument for §9.

---

## 8 · The options, priced

| Option | Sessions | Hours | Pages outside the room | Verdict |
|---|---:|---:|---:|---|
| **A — keep six as locked** | 6 | 24 | 966 · 44 % | Runs. Exam-aligned. Costs §6's bill. Only honest if §6 is written into `scope_decisions.md` and told to students |
| **B — six + mandatory pre-work track** | 6 + ~6 h async | 24 | ~750 · 34 % | Network fundamentals (U7 §7.2*, 68 pp), hex drills, protocol reference. Buys back ~200 pp. **Does not close the S4/S5 gap** — those are hands-on, not readable |
| **C — nine sessions** ⭐ | 9 | 36 | 351 · 16 % | Every session lands 0.62–1.55 pp/min, average 1.01. The demotions become editorial rather than forced. **Recommended** |
| **D — ten sessions** | 10 | 40 | 351 · 16 % | C with network split in two; nothing then exceeds 1.2 pp/min |
| **E — eleven sessions** | 11 | 44 | 0 | Every INE page gets classroom time. Includes Skype, PATA jumpers and Linux log tooling — not worth it |

**C is the recommendation.** It is +12 hours on a 24-hour diploma, it restores the two sessions the
original delivery already needed, and it is the smallest number at which the course teaches what
INE ships.

If A stays locked, take **B as the minimum mitigation** and write §6 into `scope_decisions.md`.

---

## 9 · The recommended nine-session shape

Derived by splitting only where the load is, and keeping the three load-bearing `D25` edges intact.
Page loads are `CORE` + `ORPHAN`, measured against 205 topic minutes.

| # | Session | INE source | Pages | pp/min | Artifacts | min/artifact |
|---|---|---|---:|---:|---:|---:|
| **N1** | Forensic Foundations, Integrity & Chain of Custody | U1 · U2 §2.5.1/2.5.3/2.6 · U10 §10.4 | 199 | 0.97 | 5 | 26.0 |
| **N2** | Acquisition — Disk, Memory & Live Response | U2 | 144 | 0.70 | 9 | 14.4 |
| **N3** | Data Representation, File & **Executable** Examination | U3 (incl. §3.7.4 PE) | 215 | 1.05 | 13 | 10.0 |
| **N4** | Disks, Partitions & the FAT File System | U4 · U5 §5.1–5.2* | 242 | 1.18 | 9 | 14.4 |
| **N5** | NTFS, Slack & File Carving | U5 §5.3–5.6 · U3 §3.4.1.1 | 165 | 0.80 | 12 | 10.8 |
| **N6** | Windows Forensics I — Registry, System Config & USB | U6 §6.1, 6.2, 6.5*, 6.7 | 190 | 0.93 | 15 | 8.7 |
| **N7** | Windows Forensics II — User Activity & Evidence of Execution | U6 §6.3*, 6.4*, 6.6, 6.8* | 199 | 0.97 | 19 | 6.8 |
| **N8** | Network Forensics | U7 (§7.2* as pre-work) | 317 | **1.55** | 13 | 10.0 |
| **N9** | Logs, Timelines, Reporting & Capstone | U8 · U9 · U10 · U1 §1.4.1.3/1.7 | 193 | 0.94 | 16 | 8.1 |
| | | | **1,864** | **1.01 avg** | **111** | |

**Spread 0.70 → 1.55**, against 0.70 → 2.46 today. **N8 is the only session still above benchmark**
and it is why option D exists: split it into *Protocols & Network Evidence Sources* and *Network
Forensic Analysis — OSCAR, pcap, carving, C2*, which is the fracture the instructor's own deck
already shows at slide 64.

**What the split fixes, specifically**

- **N3** finally has a home for INE's 69-page PE-analysis block and `Module_02`'s five stranded PE
  artifacts — and it completes `D19`'s chain, which currently teaches the malicious document and
  never opens the malware it drops.
- **N4/N5** stop asking one session to carry HDD internals, MBR, GPT, FAT *and* NTFS *and* carving
  — 21 artifacts in 130 minutes.
- **N6/N7** restore the split the instructor already used (his sessions 4 and 5), which is the same
  seam INE uses: machine hives vs user hives. **10 of his session-5 slides were repeats of session
  4** — that duplication is recovered time in a two-session shape, not lost time.
- **N9** gets the super-timeline toolchain a session of its own to actually run in. It is the
  single largest hole in the existing delivery: timeline theory taught, no timeline ever built.

**`D25`'s three edges survive**: registry (`N6`) still follows NTFS `$MFT` (`N5`); the plaso
super-timeline (`N9`) still follows event logs (`N9`) and `$MFT` parsing (`N5`); the capstone
(`N9`) still follows everything and introduces no new technique.

**Domain reconciliation is not done here.** `D24` requires ≤ 1.0 pp per domain against
`coverage_matrix.md`, and that matrix is `★ LOCKED` at 6 × 4 h. Moving to nine means re-deriving
the matrix first — a Part 4 change and a new `DECISIONS.md` row, not a topic-map edit.

---

## 10 · The full mapping — every INE section

All 178 section rows from the `Module_0N` §8 indexes. **6-plan** is the session under the locked
`topic_map.md`; **Topic** is the row that carries it (`—` = orphan, §7); **9-plan** is the
proposed shape in §9. Treatments are defined in §2. Page counts are INE PDF pages.

### Unit 1 — Introduction to Digital Forensics  ·  190 pp indexed  ·  → `M1`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `1.1` | Introduction | 4–10 | 7 | S1 | S1-01 | CORE | N1 |
| `1.2` | Background | 11–14 | 4 | S1 | S1-01 | CORE | N1 |
| `1.2.1` | Background: Digital Forensics Uses | 15–17 | 3 | S1 | S1-01 | CORE | N1 |
| `1.2` | Background (repeat) | 18–22 | 5 | S1 | S1-01 | CORE | N1 |
| `1.3` | Fundamentals | 23–24 | 2 | S1 | S1-02 | CORE | N1 |
| `1.3.1` | Fundamentals: Digital Evidence | 25–28 | 4 | S1 | S1-03 | CORE | N1 |
| `1.3.2` | Fundamentals: Digital Forensics Tools | 29–31 | 3 | S1 | S1-05 | CORE | N1 |
| `1.3.3` | Fundamentals: Scientific Method | 32–36 | 5 | S1 | S1-02 | CORE | N1 |
| `1.4` | Digital Evidence | 37–37 | 1 | - | - | SKIP | N1 |
| `1.4.1` | Digital Evidence Life Cycle | 38–38 | 1 | S1 | S1-01 | CORE | N1 |
| `1.4.1.1` | Digital Evidence Life Cycle: Acquisition | 39–52 | 14 | S1 | S1-01 | CORE | N1 |
| `1.4.1.2` | Digital Evidence Life Cycle: Analysis | 53–57 | 5 | S1 | S1-02 | CORE | N1 |
| `1.4.1.3` | Digital Evidence Life Cycle: Presentation | 58–61 | 4 | S6 | S6-08 | CORE | N9 |
| `1.4.2` | Types & Sources of Digital Evidence | 62–64 | 3 | S1 | S1-03 | CORE | N1 |
| `1.4.2.1` | Active Data | 65–65 | 1 | S1 | S1-03 | REF | N1 |
| `1.4.2.2` | Archive and Backup | 66–66 | 1 | S1 | S1-03 | REF | N1 |
| `1.4.2.3` | Hidden Data Types | 67–80 | 14 | S1/S2 | S1-02 | CORE | N1 |
| `1.4.2.5` | Devices | 81–97 | 17 | - | - | CUT | N1 |
| `1.5` | Analysis Steps | 98–119 | 22 | S1 | S1-02 | CORE | N1 |
| `1.6` | Investigation Scope | 120–127 | 8 | S1 | - | REF | N1 |
| `1.7` | Crime Reconstruction | 128–134 | 7 | S6 | S6-08 | CORE | N9 |
| `1.8` | Challenges of Digital Evidence | 135–150 | 16 | S1 | S1-03 | CORE | N1 |
| `1.9` | Major Concepts | 151–177 | 27 | S1 | S1-03 | CORE | N1 |
| `1.8` | Challenges of Digital Evidence (repeat) | 178–178 | 1 | S1 | S1-03 | CORE | N1 |
| `1.9` | Major Concepts (repeat) | 179–193 | 15 | S1 | S1-03 | CORE | N1 |

### Unit 2 — Data Acquisition  ·  183 pp indexed  ·  → `M1`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `2.1` | Introduction | 3–12 | 10 | S2 | S2-01 | CORE | N2 |
| `2.1.1` | Order of Volatility | 13–15 | 3 | S2 | S2-01 | CORE | N2 |
| `2.1.2` | Types of Data Acquisition | 16–21 | 6 | S2 | S2-04 | CORE | N2 |
| `2.2` | Storage Formats | 22–39 | 18 | S2 | S2-05 | CORE | N2 |
| `2.3` | Acquisition Methods | 40–55 | 16 | S2 | S2-04 | CORE | N2 |
| `2.4` | Live Data Acquisition | 56–76 | 21 | S2 | S2-02 | CORE | N2 |
| `2.5` | Tools | 77–77 | 1 | - | - | SKIP | N2 |
| `2.5.1` | Write Blockers | 78–82 | 5 | S1 | S1-08 | CORE | N1 |
| `2.5.2` | Bootable Disks | 83–83 | 1 | S2 | S2-04 | REF | N2 |
| `2.5.3` | Non-Writable USB | 84–90 | 7 | S1 | S1-08 | CORE | N1 |
| `2.5.4` | FTK Imager | 91–115 | 25 | S2 | S2-06 | CORE | N2 |
| `2.5.5` | Live Response Tools | 116–125 | 10 | S2 | S2-02 | CORE | N2 |
| `2.5.6` | Memory Forensic Tools | 126–133 | 8 | S2 | S2-03 | CORE | N2 |
| `2.5.7` | Other Forensic Tools | 134–139 | 6 | S2 | S2-07 | REF | N2 |
| `2.6` | Validating Evidence | 140–158 | 19 | S1/S2 | S1-06 | CORE | N1 |
| `2.7` | Exploring Evidence | 159–172 | 14 | S2 | S2-09 | CORE | N2 |
| `2.8` | Miscellaneous | 173–185 | 13 | S2 | S2-10 | CORE | N2 |

### Unit 3 — Data Representation & Files Examination  ·  246 pp indexed  ·  → `M2`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `3.1` | INTRODUCTION | 2–6 | 5 | S3 | S3-01 | CORE | N3 |
| `3.2.1` | BITS, BYTES AND MORE | 7–9 | 3 | S3 | S3-01 | CORE | N3 |
| `3.2.2` | KILOBIT VS KILOBYTE | 10–10 | 1 | S3 | S3-01 | CORE | N3 |
| `3.2.3` | FROM DECIMAL TO BINARY | 11–23 | 13 | S3 | S3-01 | HOMEWORK | N3 |
| `3.2.4` | HEXADECIMAL | 24–24 | 1 | S3 | S3-01 | CORE | N3 |
| `3.2.5` | FROM BINARY TO HEX | 25–25 | 1 | S3 | S3-01 | HOMEWORK | N3 |
| `3.2.6` | FROM HEX TO BINARY | 26–26 | 1 | S3 | S3-01 | HOMEWORK | N3 |
| `3.2.7` | ASCII | 27–28 | 2 | S3 | S3-01 | CORE | N3 |
| `3.2.8` | VIEW DATA IN PRACTICE | 29–32 | 4 | S3 | S3-07 | CORE | N3 |
| `3.3.1` | File Identification | 33–38 | 6 | S3 | S3-03 | CORE | N3 |
| `3.3.2` | File Structure | 39–41 | 3 | S3 | S3-02 | CORE | N3 |
| `3.4` | Metadata | 42–46 | 5 | S3 | S3-04 | CORE | N3 |
| `3.4.1` | Metadata Locations | 47–48 | 2 | S3 | S3-04 | CORE | N3 |
| `3.4.1.1` | MFT Attributes | 49–56 | 8 | S4 | S4-07 | CORE | N5 |
| `3.4.1.2` | File Headers | 57–64 | 8 | S3 | S3-02 | CORE | N3 |
| `3.4.1.3` | Magic Number | 65–70 | 6 | S3 | S3-03 | CORE | N3 |
| `3.4.2` | Metadata Types | 71–72 | 2 | S3 | S3-04 | CORE | N3 |
| `3.4.2.1` | System Metadata | 73–94 | 22 | S3 | S3-04 | CORE | N3 |
| `3.4.2.3` | Embedded Metadata | 95–98 | 4 | S3 | S3-04 | CORE | N3 |
| `3.5` | Temporary Files | 99–106 | 8 | S3 | - | REF | N3 |
| `3.6` | Data Hiding Locations | 107–126 | 20 | S3/S4 | S4-07 | CORE | N3 |
| `3.7.1` | DOCX Analysis | 127–140 | 14 | S3 | S3-05 | CORE | N3 |
| `3.7.2` | JPEG Analysis | 141–153 | 13 | S3 | S3-04 | CORE | N3 |
| `3.7.3` | PDF Analysis - Malicious obj | 154–178 | 25 | S3 | S3-05 | CORE | N3 |
| `3.7.4` | EXE Analysis | 179–247 | 69 | S3 | - | **ORPHAN** | N3 |

### Unit 4 — Disks  ·  153 pp indexed  ·  → `M3`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `4.1` | Introduction | 3–16 | 14 | S4 | S4-01 | CORE | N4 |
| `4.2` | Hard Disk Drives | 17–42, 67–68 | 28 | S4 | S4-01 | CORE | N4 |
| `4.2.1` | Interface Types | 43–52 | 10 | S4 | - | HOMEWORK | N4 |
| `4.2.2` | BIOS | 53–56 | 4 | S4 | S4-04 | CORE | N4 |
| `4.2.3` | Solid State Drives | 57–66 | 10 | S4 | S4-02 | CORE | N4 |
| `4.3` | Volumes & Partitions | 69–83, 134, 137, 139 | 18 | S4 | S4-03 | CORE | N4 |
| `4.4` | Disk Partitioning - Jumpers | 84–85, 105–107 | 5 | S4 | - | HOMEWORK | N4 |
| `4.4.1` | MBR Partitioning | 86–104 | 19 | S4 | S4-04 | CORE | N4 |
| `4.4.2` | GPT Partitioning and UEFI | 108–133 | 26 | S4 | S4-05 | CORE | N4 |
| `4.4.3` | Hidden Protected Area (HPA) | 135–136, 138, 140–141 | 5 | S4 | - | **ORPHAN** | N4 |
| `4.5` | Tools | 142–145 | 4 | S4 | S4-08 | REF | N4 |
| `4.5.1` | WinHex | 146 | 1 | S3 | S3-07 | CORE | N4 |
| `4.5.2` | Active@Disk | 147–155 | 9 | S4 | - | REF | N4 |

### Unit 5 — File Systems  ·  315 pp indexed  ·  → `M3`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `5.1` | Introduction | 3–28, 281–283 | 29 | S4 | S4-06 | CORE | N4 |
| `5.2` | FAT File System Analysis | 29–49, 96–97, 102–105, 141–143, 284–292 | 39 | S4 | S4-06 | CORE | N4 |
| `5.2.1` | FAT Structures | 50–58 | 9 | S4 | S4-06 | CORE | N4 |
| `5.2.1.1` | Boot Sector | 59–67 | 9 | S4 | S4-06 | CORE | N4 |
| `5.2.1.2` | BIOS Parameter Block | 68–80 | 13 | S4 | S4-06 | HOMEWORK | N4 |
| `5.2.1.3` | Extended BIOS Parameter Block | 81–84 | 4 | S4 | S4-06 | CORE | N4 |
| `5.2.2` | FSINFO Sector | 85–92 | 8 | S4 | S4-06 | REF | N4 |
| `5.2.3` | Boot Strap 7 Reserved Sectors | 93–94 | 2 | - | - | SKIP | N4 |
| `5.2.4` | FAT Area | 95, 98–101, 106–110 | 10 | S4 | S4-06 | CORE | N4 |
| `5.2.5` | Data Area | 111–114 | 4 | S4 | S4-06 | CORE | N4 |
| `5.2.5.2` | Short File Name | 115–119 | 5 | S4 | S4-06 | CORE | N4 |
| `5.2.5.3` | Long File Name | 127 | 1 | S4 | S4-06 | CORE | N4 |
| `5.2.6` | File Allocation | 134–138 | 5 | S4 | S4-06 | CORE | N4 |
| `5.2.7` | File Deletion | 139–140 | 2 | S4 | S4-06 | CORE | N4 |
| `5.3` | NTFS File System Analysis | 120–126, 128–133, 144–153, 294 | 24 | S4 | S4-07 | CORE | N5 |
| `5.3.1` | NTFS Structure | 154–160 | 7 | S4 | S4-07 | CORE | N5 |
| `5.3.1.1` | Volume Boot Record | 161–172 | 12 | S4 | S4-07 | CORE | N5 |
| `5.3.1.2` | Master File Table | 173–197 | 25 | S4 | S4-07 | CORE | N5 |
| `5.3.2` | NTFS Attributes | 198–224 | 27 | S4 | S4-07 | CORE | N5 |
| `5.3.4` | FILE and RAM Slack | 225–239 | 15 | S4 | S4-03 | CORE | N5 |
| `5.4` | Data Unit Layer Tools | 240–264, 296–298 | 28 | S4 | S4-09 | CORE | N5 |
| `5.5` | The Sleuthkit (TSK) | 265–280 | 16 | S4 | S4-09 | REF | N5 |
| `5.5.3` | Metadata Layer Tools | 293 | 1 | S4 | S4-09 | REF | N5 |
| `5.5.4` | Data Unit Layer Tools | 295 | 1 | S4 | S4-09 | REF | N5 |
| `5.6` | Other Tools | 299–317 | 19 | S4 | S4-09 | CORE | N5 |

### Unit 6 — Windows Forensics  ·  426 pp indexed  ·  → `M4`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `6.1` | Introduction | 4–8 | 5 | S5 | S5-01 | CORE | N6 |
| `6.2` | User and System Artifacts | 9–10 | 2 | S5 | S5-01 | CORE | N6 |
| `6.3.1` | LNK Files | 11–26 | 16 | S5 | S5-07 | CORE | N7 |
| `6.3.2` | ThumbCache | 27–41 | 15 | S5 | - | **ORPHAN** | N7 |
| `6.3.3` | Volume Shadow Copy | 42–66 | 25 | S5 | S5-08 | CORE | N7 |
| `6.3.4` | JumpLists | 67–89 | 23 | S5 | S5-07 | CORE | N7 |
| `6.3.5` | Libraries | 90–95 | 6 | S5 | - | **ORPHAN** | N7 |
| `6.3.6` | Windows Search History | 96–101 | 6 | S5 | - | **ORPHAN** | N7 |
| `6.3` | Windows Recycle Bin | 102–127 | 26 | S5 | S5-08 | CORE | N7 |
| `6.4.1` | Prefetch Files | 128–148 | 21 | S5 | S5-05 | CORE | N7 |
| `6.4.2` | Application Compatibility Cache | 149–158 | 10 | S5 | S5-06 | CORE | N7 |
| `6.5` | Windows Registry | 159–195 | 37 | S5 | S5-01 | CORE | N6 |
| `6.5.1` | Registry Artifacts | 196–243 | 48 | S5 | S5-02 | CORE | N6 |
| `6.5.1.1` | Registry Artifacts | 244–244 | 1 | S5 | S5-02 | CORE | N6 |
| `6.5.1` | Registry Artifacts | 245–249 | 5 | S5 | S5-02 | CORE | N6 |
| `6.5.2` | User Hives | 250–311 | 62 | S5 | S5-09 | CORE | N6 |
| `6.6` | ShellBags | 312–329 | 18 | S5 | S5-04 | CORE | N7 |
| `6.7` | USB Forensics | 330–359 | 30 | S5 | S5-03 | CORE | N6 |
| `6.8` | Browser Forensics | 360–368 | 9 | S5 | - | **ORPHAN** | N7 |
| `6.8.1` | Internet Explorer | 369–392 | 24 | S5 | - | **ORPHAN** | N7 |
| `6.9` | Skype Forensics | 393–429 | 37 | - | - | CUT | N7 |

### Unit 7 — Network Forensics  ·  452 pp indexed  ·  → `M4`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `7.4` | NETWORKING DEVICES | 4–4 | 1 | S6 | S6-01 | CORE | N8 |
| `7.1` | INTRODUCTION | 5–17 | 13 | S6 | S6-01 | CORE | N8 |
| `7.2` | TCP/IP PROTOCOL SUITE | 18–25 | 8 | S6 | - | PREWORK | N8 |
| `7.2.1` | SERVER-CLIENT MODEL | 26–28 | 3 | S6 | - | PREWORK | N8 |
| `7.2.2` | Protocol METADATA | 29–31 | 3 | S6 | S6-01 | CORE | N8 |
| `7.2.3` | APPLICATION LAYER | 32–34 | 3 | S6 | - | PREWORK | N8 |
| `7.2.4` | TRANSPORT LAYER | 35–45 | 11 | S6 | - | PREWORK | N8 |
| `7.2.5` | TRANSMISSION CONTROL PROTOCOL | 46–57 | 12 | S6 | - | PREWORK | N8 |
| `7.2.6` | USER DATAGRAM PROTOCOL | 58–62 | 5 | S6 | - | PREWORK | N8 |
| `7.2.7` | INTERNET LAYER | 63–79 | 17 | S6 | - | PREWORK | N8 |
| `7.2.8` | DATA-LINK LAYER | 80–85 | 6 | S6 | - | PREWORK | N8 |
| `7.2.9` | ENCAPSULATION | 86–92 | 7 | S6 | S6-01 | CORE | N8 |
| `7.3` | CLASSES OF TRAFFIC | 93–95 | 3 | S6 | - | PREWORK | N8 |
| `7.4` | NETWORKING DEVICES | 96–110 | 15 | S6 | S6-01 | CORE | N8 |
| `7.5` | NETWORK PRoTocoLs NAP | 111–114 | 4 | S6 | S6-02 | CORE | N8 |
| `7.5.1` | HTTP | 115–140 | 26 | S6 | S6-02 | CORE | N8 |
| `7.5.2.1` | CRYPTOGRAPHY | 141–147 | 7 | S6 | S6-05 | REF | N8 |
| `7.5.2.2` | SSL/TLS | 148–190 | 43 | S6 | S6-05 | CORE | N8 |
| `7.5.4` | DNS sip | 191–211 | 21 | S6 | S6-05 | CORE | N8 |
| `7.9.9` | DHCP | 212–238 | 27 | S6 | - | REF | N8 |
| `7.9.6` | ICMP | 239–252 | 14 | S6 | - | REF | N8 |
| `7.5.7` | ARP | 253–269 | 17 | S6 | - | REF | N8 |
| `7.6` | NETWORK FORENSICS | 270–271 | 2 | - | - | SKIP | N8 |
| `7.6.1` | PROTOCOL ANALYSIS | 272–280 | 9 | S6 | S6-02 | CORE | N8 |
| `7.6.2` | FLOW ANALYSIS | 281–284 | 4 | S6 | S6-01 | CORE | N8 |
| `7.6.3` | FILE CARVING & DATA EXTRACTION | 285–292 | 8 | S6 | S6-04 | CORE | N8 |
| `7.6.4` | STATISTICAL FLOW ANALYSIS | 293–308 | 16 | S6 | - | **ORPHAN** | N8 |
| `7.6.5` | NETWORK FORENSICS | 309–316 | 8 | S6 | S6-01 | CORE | N8 |
| `7.7` | EMAIL FORENSICS | 317–329 | 13 | S6 | - | **ORPHAN** | N8 |
| `7.8` | OSCAR | 330–340 | 11 | S6 | - | **ORPHAN** | N8 |
| `7.9` | NETWORK EVIDENCE ACQUISITION | 341–368 | 28 | S6 | S6-03 | CORE | N8 |
| `7.9.1` | HTTP | 369–415 | 47 | S6 | S6-02 | CORE | N8 |
| `7.1.1` | NETWORK ATTACKS | 416–455 | 40 | S6 | - | **ORPHAN** | N8 |

### Unit 8 — Log Analysis  ·  119 pp indexed  ·  → `M5`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `8.1` | Introduction | 3–15 | 13 | S6 | S6-06 | CORE | N9 |
| `8.2` | Logging Infrastructure | 16–20 | 5 | S6 | - | **ORPHAN** | N9 |
| `8.3` | Using Linux Tools for Log Analysis | 21–52 | 32 | - | - | CUT | N9 |
| `8.4` | Web Logs | 53–82 | 30 | S6 | - | **ORPHAN** | N9 |
| `8.5` | Windows Events | 83–106 | 24 | S6 | S6-06 | CORE | N9 |
| `8.6` | Syslog | 107–121 | 15 | S6 | - | **ORPHAN** | N9 |

### Unit 9 — Timeline Analysis  ·  51 pp indexed  ·  → `M5`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `9.1` | Introduction | 3–11 | 9 | S6 | S6-07 | CORE | N9 |
| `9.2` | Event Types | 12–15 | 4 | S6 | S6-07 | CORE | N9 |
| `9.3` | Approaches | 16–20 | 5 | S6 | S6-07 | CORE | N9 |
| `9.4` | Temporal Proximity | 21–23 | 3 | S6 | S6-07 | CORE | N9 |
| `9.5` | Timestamp Types | 24–27 | 4 | S6 | S6-07 | CORE | N9 |
| `9.6` | Timeline Fields | 28–36 | 9 | S6 | S6-07 | CORE | N9 |
| `9.7` | Creating Timelines | 37–53 | 17 | S6 | S6-07 | CORE | N9 |

### Unit 10 — Reporting  ·  61 pp indexed  ·  → `M5`

| INE § | Section | Pages | pp | 6-plan | Topic | Treatment | 9-plan |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| `10.1` | Introduction | 3–8 | 6 | S1/S6 | S1-04 | CORE | N9 |
| `10.2` | Tips on Reporting | 9–20 | 12 | S6 | S6-08 | CORE | N9 |
| `10.3` | How to Write a Report | 21–28 | 8 | S6 | S6-08 | CORE | N9 |
| `10.4` | Report Structure | 29–45 | 17 | S1 | S1-04 | CORE | N1 |
| `10.5` | What is a Good Report? | 46–51 | 6 | S6 | S6-08 | CORE | N9 |
| `10.6` | Report Samples | 52–63 | 12 | S6 | - | **ORPHAN** | N9 |

---

## 11 · Content-materials index — what to build each session from

Three source families, one row per session. Nothing outside `knowledge_base/` is cited.
`thm/` room notes carry the lab and case design; see [`thm/README.md`](../knowledge_base/thm/README.md) §2
for the reasoning behind each room's fit.

| Session | Reference (teach from) | Delivery record (labs & commands) | Practice / case design (THM) |
|---|---|---|---|
| **S1** | `Module_01` §1–§2 (hashing, CoC, write blocking) · `Module_05` §2 report template | `instructor/Session_01` §1 slides 8–39 | `intro-to-cold-system-forensics` (framing; ⚠ 3 factual errors) · `initialaccesspot` (best hashing content: MD5-for-lookup vs SHA-256-for-integrity) · `logless-hunt` (its scenario states the `D7` error out loud — strongest opening in the diploma) |
| **S2** | `Module_01` §2–§3 (image formats, FTK Imager, memory, triage) | `instructor/Session_01` §2 slides 51–69 (FTK Imager + KAPE, the whole lab) | `forensic-imaging` (S2 core; ⚠ safety defect) · `memory-acquisition` (direct hit, `S2-03`) · `expediting-registry-analysis` (more useful here than in S5) · `windows-incident-surface` (best `S2-02` live-response source; ⚠ **safety defect #11 — PowerShell out of order wipes every event log**) · `autopsy` (Tier 2 evidence route, `D36`) |
| **S3** | `Module_02` in full — §4 is where signature-vs-extension lives | `instructor/Session_02` §2 (TestDisk / PhotoRec / HxD / FTK `$I`–`$R`, complete with outputs) | `autopsy` · `crmsnatch` (file-signature leg) · `file-carving` |
| **S4** | `Module_03` §2 (`$MFT`, MBR/GPT, slack, carving). **Read §7 first — TRIM is absent from INE and must come from outside** | `instructor/Session_03` §2 (corrupted-GPT hex walkthrough — best original demo in the deck set). ⚠ 3 of 4 lab agendas have no steps | `mbr-and-gpt-analysis` (**task 5 ≈ our `S4-10` Case 04, already designed incl. the proof step**) · `fat32-analysis` · `ntfs-analysis` (MFT column reference + USN reason codes) · `file-carving` (⚠ CVE-2022-4510) · `diskrupt` (**S4 capstone, already built**) · `shockandsilence` |
| **S5** | `Module_04` §2A — the ShimCache and Prefetch boxes *are* the session | `instructor/Session_04` + `Session_05` §2 — RegRipper bulk, MFTECmd, AppCompatCache, Amcache, UserAssist, MRU. **The richest lab material in the course** | `compromised-windows-analysis` (whole-session model) · `windows-user-activity` (**exposes six user-activity registry keys with no row in our map**) · `windows-applications-forensics` (closes the scheduled-tasks gap; opened `D35`) · `windows-network-analysis` · `elevatingmovement` · `blizzard` |
| **S6** | `Module_04` §2B + `Module_05` in full | `instructor/Session_06` §2 (Wireshark + NetworkMiner; ⚠ 2 extraction steps missing) · `Session_07` · `Session_08` §2 (report ↔ `D20` rubric, complete) | `volatility-essentials` (**direct hit `S6-10`; changes the `EVS-03` acquisition plan**) · `windows-memory-and-network` (**strongest findings-vs-interpretation material in the path**) · `windows-memory-and-processes` · `supplemental-memory` · `blizzard` (**`S6-09` capstone structure — investigates in reverse across three hosts**) · `logless-hunt` · `crmsnatch` |

**Three standing cautions when building from any of the above** (from `knowledge_base/README.md`
§5–§6 and `instructor/README.md`):

1. **Exact strings are OCR.** Registry paths, hex signatures, byte offsets, command flags — 100+
   `⚠ verify against source page` markers exist and they are honest. Open the page before a string
   reaches a student.
2. **The instructor decks contain personal data** — local paths, drive models, a real Windows SID,
   a home-network capture with real IPs and MACs, one personal email address. Every note's §6 names
   the slides. Regenerate those screenshots on FOR-WS01 before reuse. `D22` makes this a gate.
3. **Check `thm/_TOOL_CURRENCY_2026-08-28.md` first** for any tool version or artifact path.

---

## 12 · What this file does not do, and what happens next

**Not done here, by design:**

- `design/topic_map.md` is **unchanged**. `ecdfp-intake` owns it, and every session still totals
  exactly 220 (`D26`). §7's seven proposed rows are proposals.
- `design/coverage_matrix.md` is **unchanged** — it is `★ LOCKED` at 6 × 4 h. Option C requires
  re-deriving it, which is a Part 4 change.
- `design/scope_decisions.md` §7 is **unchanged**. §6 and §7 of this file are what belongs in it.
- No `DECISIONS.md` row was written. Nothing above is decided.

**The decision that unblocks everything:** six sessions or nine. Phase 3 (lab + evidence) is the
critical path and both options need the same `EVS-*` sets, so this is not blocking today — but
every session package built under six and later re-split is rework.

**Then, in order:**

1. Record the answer as a `DECISIONS.md` row (it supersedes or confirms `D1`).
2. If six: write §6's bill into `scope_decisions.md` §7 as declared scope exclusions, and adopt
   option B's pre-work track. If nine: re-derive `coverage_matrix.md`, then re-run the `D24`
   domain reconciliation and the `D26` minute gate over the new nine.
3. Either way, resolve §7's fifteen orphans through `ecdfp-intake` — seven proposed rows, eight
   reference-sheet or scope-exclusion entries.
4. `3.7.4` **EXE Analysis is the single most consequential orphan**: 69 INE pages, five stranded
   artifacts, and `D19`'s chain currently teaches the malicious document and never opens the
   malware it drops.
