# instructor/ — how the eCDFP material was actually delivered

Notes on **Eng. Mohab Mustafa's own teaching decks** for the eCDFP course (9 PDFs, 380 slides,
242 embedded screenshots, February–March 2025). One note per instructor session; session 7's two
parts are combined into one file.

These are **delivery records, not reference**. Technical explanation lives in the
[`Module_0N_*.md`](../README.md) files. What is here instead is the running order, the labs, and
above all **the exact commands, registry keys and tool invocations that were on screen** —
recovered by OCR from the screenshots, and unavailable anywhere else in the project. That is the
material a guided lab gets built from.

Not published. See [`../README.md`](../README.md) §6 for the provenance and privacy position.

---

## The mapping — 8 instructor sessions → 10 INE units → 6 eCDFP sessions

The original course ran **eight** sessions; the rebuild runs **six** (`D1`). The mapping is not
one-to-one, and the places it collapses are where teaching time has to be found.

| Instructor session | Deck | Slides · shots | INE units | Module | eCDFP session | Note |
|---|---|---:|---|---|---|---|
| [**01** Introduction & Acquisition](Session_01_Introduction_and_Acquisition.md) | `Session 1.pdf` | 70 · 30 | 1 · 2 | [M01](../Module_01_Data_Acquisition.md) | `S1` · `S2` | One deck feeds two rebuilt sessions |
| [**02** Data Representation & File Examination](Session_02_Data_Representation_and_File_Examination.md) | `Session 2.pdf` | 38 · 24 | 3 | [M02](../Module_02_Data_Representation_and_File_Examination.md) | `S3` | Carving and partition repair here belong in `S4` |
| [**03** Disks & File Systems](Session_03_Disks_and_File_Systems.md) | `Session 3.pdf` | 40 · 21 | 4 · 5 | [M03](../Module_03_Disks_and_File_Systems.md) | `S4` | 3 of 4 lab blocks are agenda slides only |
| [**04** Practical Windows Forensics](Session_04_Practical_Windows_Forensics.md) | `session 4.pdf` | 39 · 30 | 6 | [M04](../Module_04_System_and_Network_Forensics.md) | `S5` | ⚠ **04 + 05 both collapse into one `S5`** |
| [**05** Practical Windows Forensics pt 2](Session_05_Practical_Windows_Forensics_part_2.md) | `session 5.pdf` | 23 · 18 | 6 | [M04](../Module_04_System_and_Network_Forensics.md) | `S5` | ⚠ Richest lab material in the course |
| [**06** Network Forensics](Session_06_Network_Forensics.md) | `session 6.pdf` | 72 · 52 | 7 | [M04](../Module_04_System_and_Network_Forensics.md) | `S6` | ⚠ 60 slides of fundamentals before the first lab |
| [**07** Log & Timeline Analysis](Session_07_Log_and_Timeline_Analysis.md) | `session 7 part 1.pdf` + `part 2.pdf` | 68 · 44 | 8 · 9 | [M05](../Module_05_Logs_Timelines_and_Reporting.md) | `S6` | Two decks, one note |
| [**08** Reporting & CTF](Session_08_Reporting_and_CTF.md) | `session 8.pdf` | 30 · 23 | 10 | [M05](../Module_05_Logs_Timelines_and_Reporting.md) | `S6` | ⚠ The CTF is **not in the deck** |

**Read that right-hand column as the compression problem.** Instructor sessions 6, 7 and 8 —
170 slides — all land in the single rebuilt `S6`, alongside the capstone. Sessions 4 and 5 both
land in `S5`. Each note's §5 says what that costs and names what to cut, move to homework, or
issue as pre-work.

---

## What each note contains

| § | Section |
|---|---|
| 0 | Shape of the session — lecture/lab split, where the time goes |
| 1 | Running order — slide ranges, topic, and type (`concept` · `demo` · `lab` · `challenge` · `admin`) |
| 2 | **Labs and demos — what was actually run.** Commands, evidence, outputs. The reason this folder exists |
| 3 | Registry keys, paths and artifacts named on the slides, each linked to the module that explains it |
| 4 | What this deck adds beyond INE |
| 5 | What it omits that INE covers, and the resources it cites (all unverified) |
| 6 | Cautions before reuse — personal data by slide number, dated tools, dead links, OCR gaps |

---

## Three things to know before you use any of this

**1 · The lab commands are the value, and they are OCR.** Session 5 alone yields RegRipper bulk
parsing, MFTECmd, AppCompatCache and Amcache parsing, UserAssist and MRU keys — real invocations
with real output on screen. They are also machine-read from screenshots, so every one carries
`⚠ OCR — verify` where a character was uncertain. **Never paste a command from these notes into a
student handout without opening the slide.**

**2 · Personal data is in the source slides, not in these notes.** Every note was scanned and is
clean. The decks are not: local profile paths, working directories, drive models, a real Windows
SID, a home-network packet capture, and one personal email address in session 7's DeepBlueCLI
screenshots. Each note's §6 lists the exact slides. **Regenerate those screenshots on FOR-WS01
before any of them reaches a new slide** — the repo is public (`D22`), which makes this a release
gate, not tidiness.

**3 · Several "labs" are agenda slides with no steps.** Session 3 announces MBR repair, GPT repair
and an `$MFT` walkthrough and shows none of them. Session 6's extraction steps are missing at
exactly the two slides that mattered. Plan session builds against §2 of each note, not against
the deck's own lab-agenda slides.

---

## Where the reusable assets are

| Asset | Where | Status |
|---|---|---|
| Eric Zimmerman tool workflow (MFTECmd, AppCompatCacheParser, RegRipper bulk) | [Session 05](Session_05_Practical_Windows_Forensics_part_2.md) §2 | Commands recovered — verify against slides |
| Registry key list for `S5` (UserAssist, ShimCache/BAM, Amcache, App Paths, MRU) | [Session 05](Session_05_Practical_Windows_Forensics_part_2.md) §3 | Paths recovered |
| Wireshark + NetworkMiner workflow, live QUIC/DNS capture | [Session 06](Session_06_Network_Forensics.md) §2 | Two extraction steps missing |
| TestDisk / PhotoRec / HxD / FTK Imager `$I`–`$R` recovery | [Session 02](Session_02_Data_Representation_and_File_Examination.md) §2 | Complete, with outputs |
| Corrupted-GPT hex walkthrough, primary vs backup header | [Session 03](Session_03_Disks_and_File_Systems.md) §2 | Best original demo in the deck set |
| Report structure mapped to the `D20` four-criterion rubric | [Session 08](Session_08_Reporting_and_CTF.md) §2 | Complete |
| "File Type Analysis" renamed-file set (`EVS-05` candidate) | [Session 02](Session_02_Data_Representation_and_File_Examination.md) §2 | **Unverified** → `ecdfp-evidence` |
| `evidence01`–`evidence07` network captures | [Session 06](Session_06_Network_Forensics.md) §2 | **Unverified**, origin looks like a known public corpus → `ecdfp-evidence` |
| CTF brief / capstone prior art | — | **Missing.** Ask the instructor |
