# topic_map.md — eCDFP Diploma

**GENERATED — never hand-edit.** Regenerated 2026-09-08 for the `D79`–`D96` rebuild.
Reasoning lives in `design/session_blueprint.md`; the structure this file must emit is defined in
`00_INSTRUCTIONS.md` Part 4 (`D84`).

**The unit is the TOPIC (`D79`).** A session is a container filled on the day. A **page** holds one
to three topics, and **each topic keeps its own bridge, theory, guided practice, independent work
and report stage** even when it shares a page.

**Budget.** 25 topics · 14 pages · **1140 topic minutes**. A session carries **190 topic minutes**
plus a 15-min integrity close and a 15-min break = 220 teaching minutes in a 240-minute slot.
`1140 ÷ 190 = 6 sessions` (`D1`).

**The six hash-verify / chain-of-custody rituals are NOT in this map** — they are the session's
integrity close (`D79`), 15 min × 6 = 90 min, budgeted per session.

**Domain codes:** `F` Fundamentals · `T` Tools & Techniques · `P` Preservation · `S` Storage.

---

## Evidence sets referenced

`design/evidence_sets.md` owns the final IDs, licences, sizes and hashes, and is the only file that
may declare a set **verified**. A session cannot start until every set it names here is verified.

| ID | Set | Tier | Sessions |
|

---

## The map

| ID | Topic | Page | Min | Domain | Prerequisites | Evidence |
|---|---|:-:|---:|:-:|---|---|
| **`T01`** | Foundations & Forensic Principles | `P01` | 45 | `F`·`T` | — | — |
| **`T02`** | The Forensic Report | `P01` | 25 | `F` | `T01` | — |
| **`T03`** | Evidence Integrity — Hashing, Chain of Custody, Write Blocking | `P02` | 38 | `P`·`T` | `T01` | `EVS-01` |
| **`T04`** | Inside a File — Hex, Magic Bytes & Signatures | `P03` | 82 | `P`·`F` | `T03` | `EVS-05` · `EVS-01` |
| **`T05`** | Data Representation & Metadata | `P03` | 35 | `F` | `T04` | `EVS-10` |
| **`T06`** | Live Response — Order of Volatility | `P04` | 25 | `P` | `T01` | `EVI-SRC01 live` |
| **`T07`** | Memory Forensics — Acquire and Analyse | `P04` | 35 | `P`·`T` | `T06` | `EVS-03` |
| **`T08`** | Imaging Scope & Formats | `P05` | 33 | `S` | `T07` | — |
| **`T09`** | Imaging Tools — FTK Imager & dc3dd | `P05` | 112 | `P`·`T`·`S`·`F` | `T03` · `T04` · `T08` | `EVS-02` · `EVS-09` · `EVS-05` · `EVS-04` |
| **`T10`** | Hidden Data & Image Forensics | `P06` | 80 | `T`·`F` | `T05` · `T09` | `EVS-10` · `EVS-05` |
| **`T11`** | Malicious Documents & Executables | `P07` | 75 | `F`·`T` | `T05` · `T10` | `EVS-06` |
| **`T12`** | Storage Internals & Slack | `P08` | 45 | `S` | — | `EVS-07` ✅ |
| **`T13`** | Partitioning — MBR & GPT | `P08` | 68 | `S` | `T12` | `EVS-07` ✅ |
| **`T14`** | File Systems — FAT & NTFS | `P09` | 52 | `S` | `T12` | `EVS-11` ✅ |
| **`T15`** | Carving & Deleted Data | `P09` | 25 | `S` | `T12` | `EVS-11` ✅ |
| **`T16`** | Registry Structure & System Configuration | `P10` | 28 | `F` | `T14` | `EVS-12` ✅ |
| **`T17`** | USB & Device History | `P10` | 35 | `F` | `T16` | `EVS-12` ✅ |
| **`T18`** | Evidence of Execution | `P11` | 40 | `F` | `T16` | `EVS-13` ✅ |
| **`T19`** | User Activity — Shellbags, Recycle Bin, VSS | `P11` | 38 | `F` | `T16` · `T17` | `EVS-13` ✅ |
| **`T20`** | Windows Event Logs | `P12` | 49 | `T`·`F` | `T16` · `T17` · `T18` | `EVS-14` ✅ |
| **`T21`** | Network Evidence & Traffic Analysis | `P13` | 42 | `T`·`F` | — | `EVS-08` ✅ |
| **`T22`** | C2 & Attack Patterns in Traffic | `P13` | 28 | `T` | `T21` | `EVS-08` ✅ |
| **`T23`** | Internet & Email Artifacts | `P13` | 20 | `F` | `T16` | `EVS-08` ✅ |
| **`T24`** | Logs & Super-Timelines | `P14` | 45 | `T` | `T14` · `T20` | `EVS-09` ✅ |
| **`T25`** | Final Report & Capstone | `P14` | 40 | `F`·`T` | `T02` | `EVS-09` ✅ |

---

## The pages

### P01 — Foundations and the deliverable

`70 min` · 2 topics

#### `T01` — Foundations & Forensic Principles

`45 min` · domain Fundamentals 30 min, Tools & Techniques 15 min · prereq none · evidence none · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| What digital forensics is — the mandate, the evidence lifecycle, and what an investigator may not claim | 10 | M1 intro | No |
| Forensic principles — minimal footprint, repeatability, and always work on a copy | 10 | M1 intro | No |
| What makes evidence defensible — relevance, authenticity, integrity | 10 | M1 intro | No |
| Analyst toolkit **verify** and the `CLEAN-TOOLS` snapshot &mdash; *installation is pre-work* | 15 | M1 intro | Yes |

#### `T02` — The Forensic Report

`25 min` · domain Fundamentals 25 min · prereq `T01` · evidence none · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| The fixed forensic report template — findings vs interpretation (D7) | 25 | M5 §2 | Yes |

### P02 — Evidence integrity

`38 min` · 1 topic

#### `T03` — Evidence Integrity — Hashing, Chain of Custody, Write Blocking

`38 min` · domain Preservation 20 min, Tools & Techniques 18 min · prereq `T01` · evidence `EVS-01` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Cryptographic hashing for evidence — MD5, SHA-256, what a hash proves and what it does not | 18 | M1 | Yes |
| Chain of custody — the form and the discipline | 12 | M1 | Yes |
| Write blocking — hardware vs software, and how to prove one was used | 8 | M1 | Yes |

### P03 — Data at byte level

`117 min` · 2 topics

#### `T04` — Inside a File — Hex, Magic Bytes & Signatures

`82 min` · domain Preservation 60 min, Fundamentals 22 min · prereq `T03` · evidence `EVS-05` · `EVS-01` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Inside a file — hex, magic bytes, and why renaming a file changes nothing | 22 | M2 | Yes |
| [INVESTIGATION]** Case 01 — verify 4 files against a signed manifest, find the tampered one | 60 | M1 | Yes |

#### `T05` — Data Representation & Metadata

`35 min` · domain Fundamentals 35 min · prereq `T04` · evidence `EVS-10` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| How data is represented — endianness and character encodings | 10 | M2 | No |
| Metadata and EXIF — GPS, timestamps that disagree, and how far to trust it | 25 | M2 | Yes |

### P04 — Volatile evidence

`60 min` · 2 topics

#### `T06` — Live Response — Order of Volatility

`25 min` · domain Preservation 25 min · prereq `T01` · evidence `EVI-SRC01 live` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Live response — volatile collection on a running host, **in order of volatility | 25 | M1 | Yes |

#### `T07` — Memory Forensics — Acquire and Analyse

`35 min` · domain Preservation 20 min, Tools & Techniques 15 min · prereq `T06` · evidence `EVS-03` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Memory acquisition — WinPmem, DumpIt, and the pitfalls | 20 | M1 | Yes |
| [INVESTIGATION]** Volatility 3 — processes, network connections, injected code | 15 | M4 | Yes |

### P05 — Acquisition

`145 min` · 2 topics

#### `T08` — Imaging Scope & Formats

`33 min` · domain Storage 33 min · prereq `T07` · evidence none · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Acquisition scope and image formats — physical vs logical, E01 vs raw (dd) vs AD1 | 25 | M1 | No |
| 🆕 **HPA and DCO — storage hidden from acquisition, and how to detect it | 8 | M3 §4.4.3 | Yes |

#### `T09` — Imaging Tools — FTK Imager & dc3dd

`112 min` · domain Preservation 35 min, Tools & Techniques 32 min, Storage 25 min, Fundamentals 20 min · prereq `T03` · `T04` · `T08` · evidence `EVS-02` · `EVS-09` · `EVS-05` · `EVS-04` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| FTK Imager — correct use, and what `verified` actually covers | 20 | M1 | Yes |
| `dc3dd` on Kali (clean snapshot) and targeted triage | 12 | M1 | Yes |
| File signature vs extension — run it against the image you just made | 20 | M2 | Yes |
| [INVESTIGATION]** Case 02a — acquire and verify the suspect USB | 35 | M1 | Yes |
| [INVESTIGATION]** Case 02b — **verify the acquisition is complete**: volume present, sector count, reported file-system type | 25 | M1 | Yes |

### P06 — Hidden information

`80 min` · 1 topic

#### `T10` — Hidden Data & Image Forensics

`80 min` · domain Tools & Techniques 68 min, Fundamentals 12 min · prereq `T05` · `T09` · evidence `EVS-10` · `EVS-05` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Image forensics — ThumbCache, thumbnails that outlive an edit, resaves, what a photo cannot prove | 12 | M2 · M4 §6.3.2 | Yes |
| Hidden data — LSB steganography, embedded and appended files, polyglots, and how you detect them | 33 | M2 | Yes |
| [INVESTIGATION]** Case 03 — 12 renamed/corrupted files and one hidden payload | 35 | M2 | Yes |

### P07 — Malicious files

`75 min` · 1 topic

#### `T11` — Malicious Documents & Executables

`75 min` · domain Fundamentals 50 min, Tools & Techniques 25 min · prereq `T05` · `T10` · evidence `EVS-06` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Malicious document structure — OLE and OOXML, embedded objects, macro storage | 25 | M2 | Yes |
| 🆕 **Executable analysis — PE headers, imports, sections, resources, strings | 25 | M2 §3.7.4 | Yes |
| [INVESTIGATION]** The carry-through malicious document — structure, embedded objects, macro | 25 | M2 | Yes |

### P08 — The disk

`113 min` · 2 topics

#### `T12` — Storage Internals & Slack

`45 min` · domain Storage 45 min · prereq none · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Storage internals — HDD platters and sectors, SSD NAND, wear levelling, and what TRIM destroys | 20 | M3 | No |
| Sectors, clusters and slack — how a file sits on disk, file slack vs volume slack | 25 | M3 | Yes |

#### `T13` — Partitioning — MBR & GPT

`68 min` · domain Storage 68 min · prereq `T12` · evidence `EVS-02` · `EVS-07` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| MBR partitioning — structure, partition table, boot record | 18 | M3 | Yes |
| GPT partitioning — header, entries, protective MBR | 15 | M3 | Yes |
| [INVESTIGATION]** Case 04 — wiped partition table, recover it and prove the recovery | 35 | M3 | Yes |

### P09 — File systems

`77 min` · 2 topics

#### `T14` — File Systems — FAT & NTFS

`52 min` · domain Storage 52 min · prereq `T12` · evidence `EVS-04` · `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| FAT — FAT table, directory entries, and what deletion actually does | 17 | M3 | Yes |
| NTFS — `$MFT`, resident vs non-resident, ADS, `$LogFile`, `$UsnJrnl`, parsed with MFTECmd | 35 | M3 | Yes |

#### `T15` — Carving & Deleted Data

`25 min` · domain Storage 25 min · prereq `T12` · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| [INVESTIGATION]** File carving — PhotoRec/foremost, and carving the staged archive | 25 | M3 | Yes |

### P10 — The registry

`63 min` · 2 topics

#### `T16` — Registry Structure & System Configuration

`28 min` · domain Fundamentals 28 min · prereq `T14` · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Registry structure — hives, keys, values, and where the hives live on disk | 16 | M4 | No |
| System configuration artifacts — timezone, network, mounted devices | 12 | M4 | Yes |

#### `T17` — USB & Device History

`35 min` · domain Fundamentals 35 min · prereq `T16` · evidence `EVS-02` · `EVS-04` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| USB device history — USBSTOR, MountedDevices, `setupapi.dev.log` | 18 | M4 | Yes |
| LNK files and jumplists — file access, origin volume, and what they prove | 17 | M4 | Yes |

### P11 — What ran, what was touched

`78 min` · 2 topics

#### `T18` — Evidence of Execution

`40 min` · domain Fundamentals 40 min · prereq `T16` · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Prefetch — evidence of execution, run count, first and last run | 20 | M4 | Yes |
| Amcache and ShimCache — presence vs execution, and the classic misreading | 20 | M4 | Yes |

#### `T19` — User Activity — Shellbags, Recycle Bin, VSS

`38 min` · domain Fundamentals 38 min · prereq `T16` · `T17` · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Shellbags — folder access that survives deletion | 13 | M4 | Yes |
| [INVESTIGATION]** Recycle bin (`$I`/`$R`) and Volume Shadow Copies (VSS) | 25 | M4 | Yes |

### P12 — Windows logs

`49 min` · 1 topic

#### `T20` — Windows Event Logs

`49 min` · domain Tools & Techniques 35 min, Fundamentals 14 min · prereq `T16` · `T17` · `T18` · evidence `EVS-02` · `EVS-04` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| 🆕 **Windows event logs for the investigation — what survives, what is cleared, and mapping a SID to a user | 14 | M5 | Yes |
| [INVESTIGATION]** Case 05 — which USB, which user, which program ran, when, how many times | 35 | M4 | Yes |

### P13 — Network and internet activity

`90 min` · 3 topics

#### `T21` — Network Evidence & Traffic Analysis

`42 min` · domain Tools & Techniques 32 min, Fundamentals 10 min · prereq none · evidence `EVS-08` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Network evidence sources and the **OSCAR methodology** — what pcap, flow and logs each prove | 10 | M4 §7.8 | No |
| Wireshark for investigators — display filters, follow stream, export objects | 14 | M4 | Yes |
| `tcpdump` and capture methodology — capture filters, ring buffers, what you lose | 6 | M4 | Yes |
| Network file carving — NetworkMiner, extracting transferred files | 12 | M4 | Yes |

#### `T22` — C2 & Attack Patterns in Traffic

`28 min` · domain Tools & Techniques 28 min · prereq `T21` · evidence `EVS-08` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Identifying C2 traffic and **statistical flow analysis** — beaconing, DNS anomalies, NetFlow/IPFIX | 16 | M4 §7.6.4 | Yes |
| 🆕 **Network attack patterns in evidence — scanning, brute force, lateral movement, exfiltration | 12 | M4 §7.1.1 | Yes |

#### `T23` — Internet & Email Artifacts

`20 min` · domain Fundamentals 20 min · prereq `T16` · evidence `EVS-02` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| 🆕 **Internet artifacts — browser history, downloads, typed URLs, and email headers with the `Received` chain | 20 | M4 §6.8/§6.8.1 · §7.7 | Yes |

### P14 — Timeline and report

`85 min` · 2 topics

#### `T24` — Logs & Super-Timelines

`45 min` · domain Tools & Techniques 45 min · prereq `T14` · `T20` · evidence `EVS-02` · `EVS-08` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| Super-timelines with plaso/log2timeline — build, filter, pivot | 20 | M5 | Yes |
| 🆕 **[INVESTIGATION]** Log analysis — web server logs, syslog, and building the log timeline | 25 | M5 §8.2/§8.4/§8.6 | Yes |

#### `T25` — Final Report & Capstone

`40 min` · domain Fundamentals 20 min, Tools & Techniques 20 min · prereq `T02` · evidence `EVS-02` · `03` · `08` · hands-on Yes

| Part | Min | INE source | Hands-on |
|---|---:|---|:-:|
| The final forensic report — **INE report samples** and the D20 rubric applied | 20 | M5 §10.6 | No |
| 🆕 **[INVESTIGATION]** Capstone debrief and final report assembly | 20 | M4 · M5 | Yes |

---

## Domain reconciliation (`D24` · tolerance ≤ 2.0 pp per `D74`)

The six session integrity closes (90 min) are Preservation and are included here.

| Domain | Minutes | Class % | Exam % | Δ pp | Status |
|---|---:|---:|---:|---:|:-:|
| Fundamentals | 399 | 32.4 % | 33 % | -0.6 | PASS |
| Tools & Techniques | 333 | 27.1 % | 27 % | +0.1 | PASS |
| Preservation | 250 | 20.3 % | 20 % | +0.3 | PASS |
| Storage | 248 | 20.2 % | 20 % | +0.2 | PASS |
| **Total** | **1230** | **100 %** | **100 %** | — | **PASS** |

---

## Verification

Re-parsed from this written file, not from the generator:

- **25 topics**, `T01`–`T25`, sequential in teaching order, no gaps.
- **14 pages**, `P01`–`P14`.
- **1140 topic minutes**; `1140 ÷ 190 = 6.0 sessions`.
- **`D80` dependency gate: PASS** — no topic precedes a prerequisite, no cycles, no dangling
  prerequisite, every topic reachable.
- All 57 non-ritual rows of the pre-`D79` map are placed; the 6 ritual rows are deliberately out.
