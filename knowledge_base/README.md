# knowledge_base — eCDFP Diploma

**Condensed course reference, built 2026-08-29 from `Resources/`.** Owned by `ecdfp-intake`
(Part 11). Not published — the repo is public (`D22`) and this folder is gitignored.

Everything here comes from three source sets and nothing else: INE's official eCDFP courseware
(10 units, 2,218 pages), Eng. Mohab Mustafa's own teaching decks (9 files, 380 slides), and
TryHackMe's *Advanced Endpoint Investigations* path (32 rooms, extracted through the logged-in
browser per `D34`).
Where the two disagree on technical meaning, **INE is the truth for this course** and the
disagreement is recorded rather than silently resolved.

---

## 1 · What is here

```
knowledge_base/
├── README.md                                    ← this file
├── Module_01_Data_Acquisition.md                ← the five condensed module files
├── Module_02_Data_Representation_and_File_Examination.md
├── Module_03_Disks_and_File_Systems.md
├── Module_04_System_and_Network_Forensics.md
├── Module_05_Logs_Timelines_and_Reporting.md
│
├── instructor/                                  ← how the material was actually delivered
│   ├── README.md                                    the mapping table
│   └── Session_01…Session_08 *.md                   8 notes, one per instructor session
│
├── thm/                                         ← practice-room intelligence (32 rooms)
│   ├── README.md                                    room → session map + the 10 decisions it produced
│   ├── <room-slug>.md                               32 room notes + 1 module-arc analysis
│   └── _TOOL_CURRENCY_2026-08-28.md                 186 KB, blocks A–Q — PROJECT-WIDE, read before any currency check
│
└── _source_text/                                ← the verbatim layer (see §5)
    ├── INE_Unit_01 … INE_Unit_10 *.md               10 files, page-marked
    └── Instructor_Session_01 … _08 *.md             9 files, slide-marked
```

**Two layers, on purpose.** The module files are the reference you teach from — our words,
condensed, structured. `_source_text/` is the searchable archive underneath them: every page of
every source, so a claim can always be traced back and a section that was cut can always be
recovered. Page cites in the module files (`[U6 p128–148]`) point straight into it.

**Three source families, each in its own folder.** The `Module_0N` files are what eCDFP *teaches*;
`instructor/` is how it *was taught* before the rebuild; [`thm/`](thm/README.md) is where the
*practice and case design* comes from — 252 artifacts on the same six-box template, plus ten
decisions (`D35`–`D44`) that these rooms settled. All three cross-link.

---

## 2 · The module map — three numbering systems, reconciled

Three different numberings are in play and they do **not** line up. This table is the
reconciliation; use it whenever a document says "M3" or "session 5" and you need to know which.

| Module file | INE units (the PDFs in `Resources/INE_eCDFP/`) | Pages | Instructor sessions | eCDFP sessions |
|---|---|---:|---|---|
| [`Module_01_Data_Acquisition`](Module_01_Data_Acquisition.md) | **1** Introduction to Digital Forensics · **2** Data Acquisition | 378 | 1 | `S1` · `S2` |
| [`Module_02_Data_Representation_and_File_Examination`](Module_02_Data_Representation_and_File_Examination.md) | **3** Data Representation & Files Examination | 247 | 2 | `S3` |
| [`Module_03_Disks_and_File_Systems`](Module_03_Disks_and_File_Systems.md) | **4** Disks · **5** File Systems | 472 | 3 | `S4` |
| [`Module_04_System_and_Network_Forensics`](Module_04_System_and_Network_Forensics.md) | **6** Windows Forensics · **7** Network Forensics | 884 | 4 · 5 · 6 | `S5` · `S6` |
| [`Module_05_Logs_Timelines_and_Reporting`](Module_05_Logs_Timelines_and_Reporting.md) | **8** Log Analysis · **9** Timeline Analysis · **10** Reporting | 237 | 7 · 8 | `S1` (template) · `S6` |
| | | **2,218** | | |

**Why five files and not ten.** `ecdfp-intake` fixes the target as one condensed file per INE
module, M1–M5, with a second source for the same module **merged into the existing file** — and
`coverage_matrix.md` and `topic_map.md` already reference M1–M5 throughout. INE ships the
material as ten numbered units; those are preserved intact in `_source_text/` and indexed in §8
of every module file, so nothing is lost by grouping them.

**Reading `topic_map.md` against this table:** its `INE source` column uses M1–M5, so
`S4-07 → M3` means unit 4 or 5, and `S6-06 → M5` means unit 8, 9 or 10.

---

## 3 · What each module file contains

Every module file follows the same eight sections:

| § | Section | What it is for |
|---|---|---|
| 0 | What this module is for | What a student can do afterwards, and where it sits in `S1`–`S6` |
| 1 | Core concepts | Definition → why it exists → where it shows up → example → how it appears in the `D19` case |
| 2 | **Artifacts** | Every artifact on the **R10 six-box template**. This is the section the course leans on |
| 3 | Tools | Tool · purpose · command · output · caveat |
| 4 | Findings vs interpretation | Worked FINDING / INTERPRETATION / CANNOT PROVE triples from that module's own material |
| 5 | Exam-relevant points | What eCDFP actually asks |
| 6 | Teaching notes | Where students go wrong; what to demo live; what to set as homework |
| 7 | Gaps, cautions and disagreements | Tagged `[missing]` `[dated]` `[OCR]` `[disagreement]` |
| 8 | Section index → source pages | Every INE section mapped to the heading that covers it, or `—` with a reason |

**The six boxes (R10)**, in order: what it is · where it lives (exact path) · what it proves ·
**what it does NOT prove** · how to parse it (tool + command) · one anti-forensics or
false-positive caveat.

The fourth box is the one that matters. `D7` makes findings-versus-interpretation the course's
core lesson and `D20` grades it as criterion 4 of a rubric that never changes across the six
sessions. No *does NOT prove* box in this knowledge base is shorter than 57 words, and the
longest — ShimCache presence-versus-execution, in
[`Module_04`](Module_04_System_and_Network_Forensics.md) — runs to 257, because that is the
misread the whole `S5` session exists to prevent.

**What was built:**

| Module | Lines | Artifacts (§2) | Tool rows (§3) | §7 items |
|---|---:|---:|---:|---:|
| 01 Data Acquisition | 486 | 13 | 17 | 25 |
| 02 Data Representation & File Examination | 667 | 16 | 21 | 31 |
| 03 Disks & File Systems | 881 | 19 | 30 | 41 |
| 04 System & Network Forensics | 889 | 46 | 35 | 37 |
| 05 Logs, Timelines & Reporting | 624 | 17 | 15 | 38 |
| | **3,547** | **111** | **118** | **172** |

---

## 4 · Where to start, by task

| If you are… | Read |
|---|---|
| building `S1` or `S2` | `Module_01` §2 (hashing, chain of custody, write blocking, imaging) + `Module_05` for the report template + [`instructor/Session_01`](instructor/Session_01_Introduction_and_Acquisition.md) |
| building `S3` | `Module_02` — especially §4, where signature-vs-extension lives + [`instructor/Session_02`](instructor/Session_02_Data_Representation_and_File_Examination.md) |
| building `S4` | `Module_03` §2 — `$MFT`, MBR/GPT, slack, carving. Read §7 first: TRIM is absent from the source and has to come from outside |
| building `S5` | `Module_04` §2A. The ShimCache and Prefetch boxes are the session + [`instructor/Session_04`](instructor/Session_04_Practical_Windows_Forensics.md) and [`Session_05`](instructor/Session_05_Practical_Windows_Forensics_part_2.md), which carry the real lab commands |
| building `S6` | `Module_04` §2B + `Module_05` in full + [`instructor/Session_06`](instructor/Session_06_Network_Forensics.md), [`Session_07`](instructor/Session_07_Log_and_Timeline_Analysis.md), [`Session_08`](instructor/Session_08_Reporting_and_CTF.md) |
| writing a guided lab | the instructor notes' §2 — that is where every recovered command is |
| designing a case or capstone | [`thm/README.md`](thm/README.md) §2 — Diskrupt is an `S4` capstone already built, Blizzard is the `S6-09` shape, and the Honeynet Collapse arc is analysed as one design |
| checking a tool version or artifact path | [`thm/_TOOL_CURRENCY_2026-08-28.md`](thm/_TOOL_CURRENCY_2026-08-28.md) **first** — blocks A–Q already hold most of it |
| looking for gaps to fill | every module's §7, tagged `[missing]` |
| checking a claim | the module's page cite → the matching file in `_source_text/` |

---

## 5 · How this was built, and what that means for trusting it

**The INE PDFs have no text layer.** They are screen captures of the INE video player —
one 1366×768 (or 1304×768) JPEG per page, re-compressed through iLovePDF. `pdftotext` returns
20 characters across 20 pages. Every one of the 2,218 pages was therefore **OCR'd**.

The pipeline, in order: extract the embedded JPEG per page → **crop away the player chrome**
(right-hand outline sidebar, bottom transport bar, page counter) so only the slide panel is read
→ OCR the body at 2× → separately binarise and OCR the gold title bar at 4× to recover the
`N.N` section number → reconcile the two, vote on a canonical name per section number, and
repair OCR digit slips (`7↔1`, `5↔9`, `8↔0/3/6`) only where a better-supported variant appears
on a neighbouring page. Result: INE's own section structure, rebuilt — 26 sections for unit 1,
22 for unit 6, and so on, each with its true page range.

**Verified:** every page `1..N` of all ten units is covered by a section range; the declared page
count matches the PDF page count for all ten; 2,155 of 2,218 pages carry OCR-able text (the 63
that do not are section dividers and full-bleed diagrams, and are marked as such in place).

**What this means when you use it.** The prose is reliable. **Exact strings are not automatically
reliable** — a registry path, a hex signature, a byte offset, a command flag. Anywhere the OCR
was uncertain the text carries `⚠ verify against source page` and a page cite; there are 100+ of
those markers across the five modules, and they are honest. Check the page before a string goes
in front of students.

The nine instructor decks are ordinary PowerPoint exports, so their slide text is **exact**.
Their embedded screenshots — 242 of them — were OCR'd, and those are where the lab commands
live, so the same caution applies to anything in a screenshot block.

---

## 6 · Provenance, licence and privacy

**Checked before extraction and again across the full extracted corpus.**

- **INE units.** No watermark, no "licensed to" string, no account name, no personal identifier
  on any page. The only ownership mark is the footer `© 2020 INE — All Rights Reserved`. PDF
  metadata carries a single field: `Producer: iLovePDF`. These are purchased courseware,
  screen-captured and re-compressed by the owner.
- **Instructor decks.** Authored in Microsoft PowerPoint for Microsoft 365, February–March 2025,
  `Author: mohab mustafa` on one file. The instructor's own material.
- **Emails found in the corpus** are all tool banners (PhotoRec, Eric Zimmerman's tools, KAPE)
  or INE's own demo data — with one exception, below.

**Two consequences that matter:**

1. **`_source_text/` is verbatim third-party courseware and must never be published.** It is
   gitignored and stays that way. The module files are transformed work — our words, our
   structure — and are also unpublished, per Part 2. `docs/` gets neither.
2. **The instructor's personal data is present in the source screenshots** — local profile and
   working paths, machine and drive models, a real Windows user SID, a home-network capture with
   real IPs and MAC addresses, and one personal email address (Session 7 part 1, around slides
   32–33). **None of it was carried into any file in this knowledge base** — the module and
   instructor notes are clean, verified by scan. But the underlying slides are not, and every
   instructor note's §6 names the exact slide numbers that need their screenshots regenerated on
   the course lab before any of them goes onto a new slide. Treat that as a release gate, the
   same way `D22` makes the credential and PII scans a gate rather than hygiene.

---

## 7 · Known limits

- **Section numbers in `_source_text/INE_Unit_07_Network_Forensics.md` are partly wrong.** Unit 7's
  gold title bar OCR'd badly and four sections carry a mis-numbered label (`7.9.9` for DHCP,
  `7.9.6` for ICMP, and similar). The **names and page ranges are correct**; only the numbers
  drift. Cite pages to students, never unit-7 section numbers.
- **Unit 5's own PDF bookmarks drift after p240** — INE's fault, not the OCR's. Same rule: cite
  pages.
- **The module files are long** — roughly half the source length rather than the ~10 % a summary
  would be. That is a deliberate consequence of R10: 111 artifacts × six mandatory boxes sets a
  floor, and the instruction was to spend words on the *does NOT prove* boxes. They are a
  reference to look things up in, not a document to read end to end.
- **`_source_text/` is machine-read, not proofread.** It is a search index and a provenance
  trail. It is not teaching material and should never be pasted into a session page.

---

## 8 · Next

1. **Turn `[missing]` items into gap rows.** 172 items sit across the five §7 sections; the ones
   tagged `[missing]` belong in `design/scope_decisions.md` as the gap list Phase 2's exit gate
   asks for. The biggest: how to *prove* a write blocker was used (`M01`), TRIM (`M03`), C2
   beaconing (`M04`), and a sample report (`M05`).
2. **Propose `topic_map.md` rows** for anything these modules justify that the map does not yet
   carry — through `ecdfp-intake`, with the minute gate run before any row is written
   (every session totals exactly 220, `D26`).
3. **Route the candidate evidence sets through `ecdfp-evidence`.** Two surfaced in the decks:
   the "File Type Analysis" renamed-file set (`EVS-05` shape, instructor session 2) and the
   `evidence01`–`evidence07` network captures (instructor session 6) whose origin looks like a
   known public corpus — neither is verified, and only `ecdfp-evidence` may say otherwise.
4. **Ask the instructor for the CTF brief.** Session 8's deck is titled "Reporting & CTF
   Challenge" and contains no challenge. `S6-09`'s capstone has no prior art without it.
