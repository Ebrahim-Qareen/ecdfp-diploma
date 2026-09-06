# session_time_estimates.md — bottom-up topic timing, re-packed into 6 sessions

**Built 2026-08-29.** Supersedes the *pacing* conclusion of `ine_session_mapping.md` (which said
nine sessions) — **not** its content mapping, which still stands. The difference is one input that
analysis did not have: **what the students already know.**

`topic_map.md` allocated minutes **top-down** — every session forced to exactly 220 (`D26`). This
file estimates each topic **bottom-up**: what it actually costs to teach *these* students, then
packs the result into six sessions.

**Nothing here is applied.** `topic_map.md`, `coverage_matrix.md` and `DECISIONS.md` are untouched.

---

## 1 · The input that changes the answer

Students arrive having completed, in order:

**CCNA → MCSA → Linux Administration → SOC → CEH → eCIR → _eCDFP_**

`scope_decisions.md` already carries the rule — *"Never re-teach CCNA, Windows, Linux, AD, CEH or
eCIR content. Reference it and move on"* — but `topic_map.md`'s minutes were never re-derived
against it. That is the correction this file makes.

> ⚠ **`scope_decisions.md` §1 says eCDFP is the "fourth course after SOC → CEH → eCIR".** With
> CCNA, MCSA and Linux Administration in front of those it is the **seventh**. That line needs a
> correction and a `DECISIONS.md` row.

**Verified against the courses on disk, not assumed.** `CEH_Course/docs` (4 sessions built) and
`ECIR_Course/docs` (9 sessions) were searched for every eCDFP key term. The result is unusually
clean — the two courses split the eCDFP syllabus almost perfectly in half:

| Already taught — hits in CEH / eCIR | Zero hits in either — genuinely new |
|---|---|
| hashing · MD5 / SHA-256 · E01 (light) · chain of custody (eCIR S5) · write blocker (light) · Volatility (eCIR S6) · Wireshark + **the display-filter set** (eCIR S8) · tcpdump · pcap · NetFlow / sFlow / IPFIX · DNS · DHCP · ARP · TLS · SMTP + `Received:` headers (eCIR S7) · Windows event logs · 4624 · 1102 · Sysmon · syslog · IIS / Apache logs · registry (as detection) · EXIF · ATT&CK · timeline *concept* | **Prefetch · ShimCache · Amcache · UserAssist · shellbags · USBSTOR · LNK / jumplists · Recycle Bin · `$MFT` · NTFS · FAT32 · slack space · MBR · GPT · carving · file signature / magic bytes · PE headers · ADS · KAPE · plaso · log2timeline · OSCAR** |

Read the right-hand column: it is **disk and file-system internals, Windows forensic artifacts, and
super-timelines**. That is the actual eCDFP course. Everything else is revision.

**The rate applied:**

| Status | Meaning | Time factor |
|---|---|---|
| `KNOWN` | taught **and practised** in a prior course | ~0.4× — recall it, then teach only the forensic twist |
| `PARTIAL` | concept known, the forensic angle is new | ~0.7× — reframe, do not re-teach |
| `NEW` | nothing before touched it | **1.0×, and often more than `topic_map` allowed** |

---

## 2 · The result — six sessions fits

| | Topics | Old minutes | **Re-estimated** | Change |
|---|---:|---:|---:|---:|
| `KNOWN` — 10 topics | 10 | 159 | **83** | **−76** |
| `PARTIAL` — 20 topics | 20 | 333 | 311 | −22 |
| `NEW` — 20 topics | 20 | 328 | **424** | **+96** |
| Investigations + rituals | 14 | 410 | 390 | −20 |
| | **64** | **1,230** | **1,208** | **−22** |

**Capacity is 1,230 topic minutes (6 × 205). The content needs 1,208. It fits, with 22 to spare.**

The mechanism is a transfer, not a saving: **76 minutes come off what students already know and go
straight into the artifacts nothing before taught.** Three topics with no `topic_map` row are
absorbed at the same time — HPA/DCO (8), NTFS journals (10), PE analysis (25).

**Why this differs from `ine_session_mapping.md`'s "nine sessions".** That analysis measured INE's
2,196 pages against classroom minutes and knew nothing about the students. Its finding stands for
a cold-start audience. For *this* cohort roughly a third of INE's pages are revision, and the
course fits — **which is exactly why the instructor's own session 1 covered INE units 1 *and* 2 in
one sitting.** The instructor was pacing to the room; the topic map was pacing to the book.

**What has not changed:** the honest verdict on S4 and S5. They are the two sessions where nothing
is revision, and they are the two that grew.

### Per session

| Session | Old | **New** | Load |
|---|---:|---:|---|
| **S1** Foundations, Integrity & Acquisition I | 240 | **191** | 14 min spare |
| **S2** Acquisition II — Live, Memory & Media | 215 | **199** | 6 spare |
| **S3** Data Representation & File Examination | 190 | **197** | 8 spare |
| **S4** Partitions & File Systems | 175 | **204** | full |
| **S5** Windows Forensics | 205 | **216** | ⚠ **+11 over 205** — uses 11 of the slot's 20 min slack |
| **S6** Network, Timelines, Reporting & Capstone | 205 | **201** | 4 spare |
| | **1,230** | **1,208** | |

*"Old" is the `topic_map` minutes of the topics now in that session — sessions were re-cut, so these
do not read 205 each.*

**S5 is the only session over budget, and deliberately.** It holds seven consecutive `NEW`
artifacts with no prior-course support anywhere, including the ShimCache/Amcache
presence-vs-execution box the whole session exists to land. Options: run the 240-minute slot fully
(11 min of its 20 min slack), or move Recycle Bin + VSS to homework (−15).

---

## 3 · The six sessions, topic by topic

`Prior` names the course that already covered it. `Old` is the `topic_map.md` minute;
`New` is the bottom-up estimate. **Bold** rows are `NEW` — nothing before eCDFP taught them.

### S1 — Forensic Foundations, Evidence Integrity & Acquisition I

**191 min** (240 under the old map) · 12 blocks · 2 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| What digital forensics is - mandate, evidence lifecycle, what you may not claim | eCIR S5 · SOC | `PARTIAL` | 15 | 10 |
| Forensic principles - order of volatility, minimal footprint, repeatability, work on a copy | eCIR S5/S6 | `PARTIAL` | 20 | 12 |
| Defensible evidence - relevance, authenticity, integrity, admissibility | eCIR S5 · CEH S1 legal | `PARTIAL` | 12 | 10 |
| Cryptographic hashing for evidence - what a hash proves and what it does NOT | CEH S4 · SOC · eCIR | `KNOWN` | 18 | 8 |
| Chain of custody - the form and the discipline | eCIR S5 | `PARTIAL` | 12 | 10 |
| **Write blocking - hardware vs software, and how to PROVE one was used** | eCIR (light) | `NEW` | 8 | **12** |
| **The fixed forensic report template - findings vs interpretation (D7)** | eCIR 1-page IR report only | `NEW` | 25 | **30** |
| Analyst toolkit verify + CLEAN-TOOLS snapshot (install = pre-work) | eCIR S2 · CEH S1 lab builds | `KNOWN` | 20 | 12 |
| Physical vs logical acquisition - what each captures and misses | MCSA disk mgmt | `PARTIAL` | 20 | 12 |
| Image formats - E01 vs raw (dd) vs AD1, compression, embedded verification | eCIR (light) | `PARTIAL` | 15 | 15 |
| [INVESTIGATION] Case 01 - verify 4 files against a signed manifest | - | `-` | 60 | 45 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **240** | **191** |

### S2 — Acquisition II: Live Response, Memory & Storage Media

**199 min** (215 under the old map) · 12 blocks · 3 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| Order of volatility in practice - the collection sequence | eCIR S6 collect-before-cut | `KNOWN` | 15 | 8 |
| Live response - volatile data collection on a running host | eCIR S6 | `PARTIAL` | 25 | 15 |
| Memory acquisition - why it comes first, tools, pitfalls | eCIR S6 Volatility (analysis) | `PARTIAL` | 20 | 15 |
| HDD internals - platters, heads, sectors, CHS and LBA | MCSA · general IT | `KNOWN` | 12 | 6 |
| SSD internals - NAND, wear levelling, TRIM and what it destroys | MCSA (admin view only) | `PARTIAL` | 18 | 15 |
| **HPA and DCO - storage hidden from acquisition** | none | `NEW` | — | **8** |
| Clusters - how a file sits on disk, why a header survives a rename | MCSA (light) | `PARTIAL` | 15 | 10 |
| **FTK Imager - correct use and verification + demo: image EVI-SRC01** | eCIR 1 mention | `NEW` | 20 | **25** |
| **dc3dd on Linux and KAPE targeted triage** | Linux Admin (CLI only) | `NEW` | 15 | **22** |
| [INVESTIGATION] Case 02a - acquire and verify the suspect USB | - | `-` | 35 | 35 |
| [INVESTIGATION] Case 02b - examine partition and file-system structure | - | `-` | 25 | 25 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **215** | **199** |

### S3 — Data Representation & File Examination

**197 min** (190 under the old map) · 10 blocks · 3 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| Bits, bytes, hex, endianness, character encodings | CCNA binary/hex · CEH | `KNOWN` | 20 | 8 |
| **File structure - header, body, trailer, magic bytes** | none | `NEW` | 20 | **22** |
| **File signature vs extension - the mismatch, and what it proves** | none | `NEW` | 20 | **20** |
| Metadata and EXIF - what it records and how far to trust it | eCIR (EXIF once) | `PARTIAL` | 20 | 15 |
| Malicious document structure - OLE and OOXML, embedded objects, macros | CEH malware · eCIR S7 phishing | `PARTIAL` | 25 | 22 |
| Executable analysis - PE headers, imports, sections, resources, strings | CEH malware basics | `PARTIAL` | — | 25 |
| **Hex and metadata tooling - HxD/WinHex, ExifTool, TrID** | none | `NEW` | 10 | **15** |
| [INVESTIGATION] Case 03 - 12 renamed/corrupted files, identify each by header | - | `-` | 35 | 30 |
| [INVESTIGATION] The carry-through malicious document | - | `-` | 25 | 25 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **190** | **197** |

### S4 — Partitions & File Systems: MBR/GPT, FAT, NTFS

**204 min** (175 under the old map) · 9 blocks · 5 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| MBR - structure, partition table, boot record, at byte level | MCSA (concept only) | `PARTIAL` | 18 | 22 |
| GPT - protective MBR, header, entry array, backups | MCSA (concept only) | `PARTIAL` | 15 | 18 |
| **Sectors, clusters and slack - file slack, RAM slack, MFT slack** | none | `NEW` | 20 | **22** |
| **FAT - the FAT table, directory entries, what deletion actually does** | none | `NEW` | 17 | **30** |
| **NTFS - $MFT record, $STANDARD_INFORMATION, $FILE_NAME, resident vs non-resident, ADS** | none | `NEW` | 20 | **30** |
| **NTFS journals - $LogFile and $UsnJrnl** | none | `NEW` | — | **10** |
| **MFTECmd and Timeline Explorer - parsing $MFT to CSV** | none | `NEW` | 10 | **12** |
| [INVESTIGATION] Case 04 - wiped partition table + carve the staged archive | - | `-` | 60 | 45 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **175** | **204** |

### S5 — Windows Forensics: Registry, USB, Execution & User Activity

**216 min** (205 under the old map) · 10 blocks · 6 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| Registry structure - hives, keys, values, where hives live, key last-write time | MCSA admin · eCIR detection | `PARTIAL` | 20 | 15 |
| System configuration artifacts - ControlSet/Select, timezone, network, system identity | MCSA admin | `PARTIAL` | 15 | 15 |
| **USB device history - USBSTOR, MountedDevices, MountPoints2, setupapi.dev.log** | none | `NEW` | 20 | **25** |
| **Shellbags - folder access that survives deletion** | none | `NEW` | 15 | **18** |
| **Prefetch - evidence of execution, run count, first and last run** | none | `NEW` | 20 | **20** |
| **ShimCache and Amcache - presence vs execution, and the classic misreading** | none | `NEW` | 20 | **28** |
| **LNK files and jumplists - file access, origin volume, what they prove** | none | `NEW` | 20 | **20** |
| **Recycle Bin ($I/$R) and Volume Shadow Copies** | none | `NEW` | 25 | **15** |
| [INVESTIGATION] Case 05 - which USB, which user, which program ran, when, how often | - | `-` | 35 | 45 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **205** | **216** |

### S6 — Network Forensics, Timelines, Reporting & Capstone

**201 min** (205 under the old map) · 11 blocks · 1 genuinely new

| Topic | Prior course | Status | Old | **New** |
|---|---|:-:|--:|--:|
| Network evidence sources - pcap, flow, logs, what each can and cannot prove | eCIR S8 (5 sources) · CCNA | `KNOWN` | 10 | 5 |
| Wireshark for investigators - display filters, follow stream, export objects | eCIR S8 filter set · CCNA · CEH | `KNOWN` | 25 | 12 |
| tcpdump and capture methodology - capture filters, ring buffers, what you lose | CCNA · CEH · eCIR | `KNOWN` | 10 | 6 |
| Network file carving - NetworkMiner, extracting transferred files | eCIR (light) | `PARTIAL` | 14 | 15 |
| Identifying C2 traffic - beaconing intervals, DNS anomalies, TLS fingerprints | eCIR S6 C2 (light) | `PARTIAL` | 16 | 22 |
| Windows event logs for the timeline - what survives, what is cleared, what is never written | SOC · eCIR S1/S3 · MCSA | `KNOWN` | 14 | 8 |
| **Super-timelines with plaso/log2timeline - body file, mactime, build, filter, pivot** | none | `NEW` | 23 | **40** |
| The final forensic report - six sessions of findings, D20 rubric applied | eCIR 1-page IR report | `PARTIAL` | 18 | 18 |
| [INVESTIGATION] Capstone - image + memory + pcap into one report | - | `-` | 45 | 50 |
| [INVESTIGATION] Volatility 3 - processes, connections, injected code | eCIR S6 Volatility | `KNOWN` | 15 | 10 |
| [RITUAL] Hash-verify + chain-of-custody close | - | `-` | 15 | 15 |
| **Total** | | | **205** | **201** |
---

## 4 · What moved, and why

| Move | From → To | Why |
|---|---|---|
| Physical vs logical acquisition · image formats (E01/raw/AD1) | S2 → **S1** | S1 lost 49 min to prior knowledge. Acquisition *theory* costs nothing to pull forward and it makes S1 a full session again |
| HDD internals · SSD/TRIM · **HPA/DCO** | S4 → **S2** | You acquire *from* a medium. HPA/DCO belongs with acquisition because it is storage the acquisition can miss — teaching it three sessions later is backwards |
| Clusters — how a file sits on disk | S3 → **S2** | It is what Case 02b already examines |
| File carving | own topic → **merged into S4's Case 04** | Carving *is* the recovery step. One 45-min investigation beats a 25-min lecture plus a 35-min case |
| **PE / executable analysis** | *nowhere* → **S3** | 69 INE pages and five stranded artifacts. `D19`'s chain teaches the malicious document and never opens the malware it drops |
| **NTFS journals — `$LogFile`, `$UsnJrnl`** | inside a 20-min NTFS row → **own 10-min block** | `$MFT` + attributes + ADS + two journals cannot be 20 minutes |
| Volatility 3 · Wireshark · event logs · tcpdump | — | Cut hard (−49 min combined). eCIR S6 and S8 already taught these with labs |

**The three `D25` edges hold.** Registry (S5) still follows NTFS `$MFT` (S4); the plaso
super-timeline (S6) still follows event logs (S6) and `$MFT` parsing (S4); the capstone (S6) still
follows S1–S5 and introduces no new technique.

⚠ **The domain reconciliation (`D24`) is not re-run here.** Moving 76 minutes from `KNOWN` topics
into `NEW` ones shifts the Fundamentals / Tools / Preservation / Storage split, and
`coverage_matrix.md` is `★ LOCKED`. Re-run the ≤ 1.0 pp check before this becomes the plan.

---

## 5 · Linux forensics — where it is, and where it is not

**It is a declared exclusion, and INE does not teach it either.** Both halves matter:

- `scope_decisions.md` already excludes **Linux / macOS forensics**, reason recorded:
  *"eCDFP is Windows-weighted and 24 hours does not stretch. State this to students explicitly in S1."*
- **INE's own eCDFP courseware has no Linux host forensics.** Across all 2,218 pages: no
  `bash_history`, no `crontab`, no "Linux forensics"; `ext2/3/4` appears in one unit in passing.
  The exam is Windows-weighted and so is the courseware. There is nothing to restore.

**But Linux is in the course — as the platform, not the subject:**

| Where | What | Session |
|---|---|---|
| `dc3dd` imaging on Kali (clean snapshot) | acquisition from a Linux workstation | S2 |
| The Sleuthkit — `fls`, `istat`, `icat`, `blkls`, `blkcalc`, `mactime` | file-system and data-unit layer analysis | S4 |
| `log2timeline` / plaso, body files | super-timeline construction | S6 |
| PhotoRec · foremost · `bulk_extractor` | carving | S4 |
| INE §8.3 *Using Linux Tools for Log Analysis* (32 pp) · §8.6 Syslog (15 pp) | `grep` / `cut` / `awk` pipelines, syslog format | reference sheet |

**Those 47 pages are free for this cohort.** Linux Administration already taught the shell and
syslog; SOC and eCIR already taught log analysis. It becomes a one-page reference, not class time —
which is why it costs nothing to hand out and would cost 45 minutes to teach.

**If Linux host forensics is wanted anyway**, three options, cheapest first:

1. **Homework track (recommended, 0 class minutes).** The THM Honeynet Collapse arc opens on a
   Linux host — [`initialaccesspot`](../knowledge_base/thm/initialaccesspot.md), already extracted
   and flagged ⚠ Linux. Issue it as graded homework after S4. Their Linux Administration carries
   them; you grade the report against the same `D20` rubric.
2. **A 25-minute S6 block** — ext4 inodes vs `$MFT`, `/var/log` vs `.evtx`, `bash_history` vs
   UserAssist — taught as *contrast*, which is cheap because both sides are then known. Costs 25
   minutes of exam-weighted content and there are only 22 spare.
3. **A seventh session.** Only if the diploma is allowed to grow — and eCDFP's exam will not
   reward it.

**Recommendation: option 1, plus stating the exclusion out loud in S1** as `scope_decisions.md`
already requires. Students coming off Linux Administration will ask, and *"the exam is
Windows-weighted, here is the homework if you want it"* is a better answer than silence.

---

## 6 · What is still true from `ine_session_mapping.md`

- The **content mapping** (§10, all 178 INE sections → session) is unchanged and still correct.
- The **15 orphans** are unchanged. Three are absorbed above (PE analysis, HPA/DCO, `$LogFile`/
  `$UsnJrnl`); web logs, statistical flow, email headers, OSCAR and report samples still have no
  row — though the prior-course evidence now argues **email headers (eCIR S7) and web logs (SOC,
  eCIR) are `KNOWN`**, so a reference sheet closes them rather than a topic.
- The **publication gate** still applies: `design/` is tracked and the repo is public.
- **Eight sessions remains the comfortable shape.** Six now fits, but with S5 over budget and 22
  minutes of slack across the whole course. If the diploma can grow, splitting S4 and S5 — the
  two all-`NEW` sessions — is where the eighth and seventh sessions should go.
