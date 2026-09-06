# session_map.md — the eCDFP session map

**Current plan: 8 sessions × 4 h = 32 h.** Saved 2026-08-29 at Ebrahim's direction.
This is the compact map. The reasoning is in [`plan_8_sessions.md`](plan_8_sessions.md);
the timing model is in [`session_time_estimates.md`](session_time_estimates.md); the INE
source mapping is in [`ine_session_mapping.md`](ine_session_mapping.md).

> **Status: proposal, not yet ratified.** `topic_map.md` still carries the locked 6-session
> map and `ecdfp-intake` owns it. This file contradicts **`D1`** (6 × 4 h) and **`D38`**
> (Linux out of scope), and `coverage_matrix.md` is `★ LOCKED` at six sessions. Four
> `DECISIONS.md` rows are owed before anything is built — see `plan_8_sessions.md` §5.

**Budget.** 240 min slot → 220 teaching → **205 topic minutes** (`D15`/`D23`), of which
15 min is the hash-verify + chain-of-custody closing ritual, every session.

---

## The map

| # | Session | Min | New | Character |
|---|---|--:|:-:|---|
| **S1** | Forensic Foundations, Evidence Integrity & Chain of Custody | 201 | 3 | mostly revision + the report template |
| **S2** | Acquisition — Live Response, Memory & Media | 199 | 4 | half revision; imaging is new |
| **S3** | Data Representation & File Examination | 205 | 3 | half new |
| **S4** | Partitions & File Systems — MBR, GPT, FAT, NTFS | 205 | 6 | **all new** |
| **S5** | Windows Forensics I — Registry, System Config & USB | 187 | 4 | **all new** |
| **S6** | Windows Forensics II — Execution & User Activity | 203 | 8 | **all new** |
| **S7** | Linux Forensics — File Systems, Artifacts & Logs | 205 | 9 | **all new** |
| **S8** | Network Forensics, Timelines, Reporting & Capstone | 204 | 3 | mostly revision + plaso |
| | **Total** | **1609** | **40** | capacity 1640 · spare 31 |

**"New" = nothing in CCNA → MCSA → Linux Administration → SOC → CEH → eCIR taught it.**
That prerequisite stack is why 32 hours is enough: roughly a third of INE's 2,196 pages
are revision for this cohort. Never size this course from INE page count alone.

---

## Session content

### S1 — Forensic Foundations, Evidence Integrity & Chain of Custody

**201 min** · 13 blocks · **3 new**

| Block | Status | Min |
|---|:-:|--:|
| What digital forensics is - mandate, evidence lifecycle, what you may not claim | `PARTIAL` | 10 |
| Forensic principles - volatility order, minimal footprint, repeatability, work on a copy | `PARTIAL` | 12 |
| Defensible evidence - relevance, authenticity, integrity, admissibility | `PARTIAL` | 10 |
| Cryptographic hashing - what a hash proves and what it does NOT | `KNOWN` | 8 |
| Chain of custody - the form and the discipline | `PARTIAL` | 10 |
| **Write blocking - hardware vs software, and how to PROVE one was used** | `NEW` | 12 |
| **The fixed forensic report template - findings vs interpretation (D7)** | `NEW` | 30 |
| **Course roadmap - Windows, Linux and what each platform can and cannot show** | `NEW` | 10 |
| Analyst toolkit verify + CLEAN-TOOLS snapshot (install = pre-work) | `KNOWN` | 12 |
| Physical vs logical acquisition - what each captures and misses | `PARTIAL` | 12 |
| Image formats - E01 vs raw (dd) vs AD1, compression, embedded verification | `PARTIAL` | 15 |
| [INVESTIGATION] Case 01 - verify 4 files against a signed manifest | `INV` | 45 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **201** |

### S2 — Acquisition — Live Response, Memory & Media

**199 min** · 12 blocks · **4 new**

| Block | Status | Min |
|---|:-:|--:|
| Order of volatility in practice - the collection sequence | `KNOWN` | 8 |
| Live response - volatile data collection on a running host | `PARTIAL` | 15 |
| Memory acquisition - why it comes first, tools, pitfalls | `PARTIAL` | 15 |
| HDD internals - platters, heads, sectors, CHS and LBA | `KNOWN` | 6 |
| SSD internals - NAND, wear levelling, TRIM and what it destroys | `PARTIAL` | 15 |
| **HPA and DCO - storage hidden from acquisition** | `NEW` | 8 |
| **FTK Imager - correct use and verification + demo: image EVI-SRC01** | `NEW` | 25 |
| **dc3dd and KAPE targeted triage** | `NEW` | 20 |
| **Acquiring a Linux host - dd/dc3dd, read-only mounting, loop devices** | `NEW` | 12 |
| [INVESTIGATION] Case 02a - acquire and verify the suspect USB | `INV` | 35 |
| [INVESTIGATION] Case 02b - examine partition and file-system structure | `INV` | 25 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **199** |

### S3 — Data Representation & File Examination

**205 min** · 11 blocks · **3 new**

| Block | Status | Min |
|---|:-:|--:|
| Bits, bytes, hex, endianness, character encodings | `KNOWN` | 8 |
| **File structure - header, body, trailer, magic bytes** | `NEW` | 22 |
| **File signature vs extension - the mismatch, and what it proves** | `NEW` | 20 |
| Metadata and EXIF - what it records and how far to trust it | `PARTIAL` | 14 |
| Clusters - how a file sits on disk, why a header survives a rename | `PARTIAL` | 10 |
| Malicious document structure - OLE and OOXML, embedded objects, macros | `PARTIAL` | 22 |
| Executable analysis - PE headers, imports, sections, resources, strings | `PARTIAL` | 25 |
| **Hex and metadata tooling - HxD/WinHex, ExifTool, TrID** | `NEW` | 14 |
| [INVESTIGATION] Case 03 - 12 renamed/corrupted files, identify each by header | `INV` | 30 |
| [INVESTIGATION] The carry-through malicious document | `INV` | 25 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **205** |

### S4 — Partitions & File Systems — MBR, GPT, FAT, NTFS

**205 min** · 10 blocks · **6 new**

| Block | Status | Min |
|---|:-:|--:|
| MBR - structure, partition table, boot record, at byte level | `PARTIAL` | 18 |
| GPT - protective MBR, header, entry array, backups | `PARTIAL` | 17 |
| **Sectors, clusters and slack - file slack, RAM slack, MFT slack** | `NEW` | 22 |
| **FAT - the FAT table, directory entries, what deletion actually does** | `NEW` | 26 |
| **NTFS - $MFT record, $STANDARD_INFORMATION, $FILE_NAME, resident vs non-resident** | `NEW` | 30 |
| **Alternate Data Streams - a second, named $DATA** | `NEW` | 10 |
| **NTFS journals - $LogFile and $UsnJrnl** | `NEW` | 10 |
| **MFTECmd and Timeline Explorer - parsing $MFT to CSV** | `NEW` | 12 |
| [INVESTIGATION] Case 04 - wiped partition table + carve the staged archive | `INV` | 45 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **205** |

### S5 — Windows Forensics I — Registry, System Config & USB

**187 min** · 11 blocks · **4 new**

| Block | Status | Min |
|---|:-:|--:|
| Registry structure - hives, keys, values, last-write time, transaction logs and dirty hives | `PARTIAL` | 20 |
| **ControlSet and the Select key - which control set was actually live** | `NEW` | 12 |
| Timezone, system identity and shutdown keys | `PARTIAL` | 12 |
| Network configuration and network history keys | `PARTIAL` | 12 |
| Services and autostart keys - persistence in the registry | `PARTIAL` | 18 |
| SAM accounts, ProfileList and LogonUI | `PARTIAL` | 15 |
| **USB device history - USBSTOR, MountedDevices, MountPoints2, setupapi.dev.log** | `NEW` | 25 |
| **Evidence-affecting configuration keys** | `NEW` | 8 |
| **RegRipper and Registry Explorer - the bulk parsing workflow** | `NEW` | 15 |
| [INVESTIGATION] Case 05a - which USB, which user, which account | `INV` | 35 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **187** |

### S6 — Windows Forensics II — Execution & User Activity

**203 min** · 11 blocks · **8 new**

| Block | Status | Min |
|---|:-:|--:|
| **Prefetch - evidence of execution, run count, first and last run** | `NEW` | 20 |
| **ShimCache and Amcache - presence vs execution, and the classic misreading** | `NEW` | 28 |
| **UserAssist and BAM - GUI execution and background activity** | `NEW` | 12 |
| **Shellbags - folder access that survives deletion** | `NEW` | 18 |
| **LNK files and jumplists - file access, origin volume, what they prove** | `NEW` | 20 |
| **RecentDocs, RunMRU and Terminal Server Client MRU** | `NEW` | 10 |
| **Recycle Bin ($I/$R) and legacy INFO2** | `NEW` | 10 |
| **Volume Shadow Copies - previous versions of the evidence** | `NEW` | 15 |
| Browser forensics - history, downloads, typed URLs (D35) | `PARTIAL` | 15 |
| [INVESTIGATION] Case 05b - which program ran, when, how many times | `INV` | 40 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **203** |

### S7 — Linux Forensics — File Systems, Artifacts & Logs

**205 min** · 12 blocks · **9 new**

| Block | Status | Min |
|---|:-:|--:|
| **ext4 - superblock, inodes, journal; and how it differs from $MFT** | `NEW` | 20 |
| **ext4 inode timestamps (atime/mtime/ctime/crtime) and proving a timestomp** | `NEW` | 18 |
| **Linux login records - wtmp, btmp, lastlog, and the family attackers delete** | `NEW` | 18 |
| **.bash_history - the intent artifact, and the silent-omission trap** | `NEW` | 15 |
| **Shell configuration as an artifact - the alias that hides the command** | `NEW` | 8 |
| **Linux persistence - cron, systemd units, rc.local, authorized_keys** | `NEW` | 20 |
| **Privilege-escalation state - SUID, sudoers, and sudo's own log** | `NEW` | 15 |
| **auditd and journald - syscall records, and what survives escalation** | `NEW` | 15 |
| /var/log and web-server access logs - the status code that dates a compromise | `KNOWN` | 12 |
| **USB attach and detach on Linux - and why there is no USBSTOR** | `NEW` | 9 |
| [INVESTIGATION] Case 06 - the Linux exfiltration node | `INV` | 40 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **205** |

### S8 — Network Forensics, Timelines, Reporting & Capstone

**204 min** · 13 blocks · **3 new**

| Block | Status | Min |
|---|:-:|--:|
| Network evidence sources - pcap, flow, logs, what each can and cannot prove | `KNOWN` | 5 |
| Wireshark for investigators - display filters, follow stream, export objects | `KNOWN` | 12 |
| tcpdump and capture methodology - capture filters, ring buffers, what you lose | `KNOWN` | 6 |
| Network file carving - NetworkMiner, extracting transferred files | `PARTIAL` | 12 |
| Identifying C2 traffic - beaconing intervals, DNS anomalies, TLS fingerprints | `PARTIAL` | 20 |
| **OSCAR - INE's network investigation methodology** | `NEW` | 8 |
| **Statistical flow analysis - NetFlow/IPFIX, and what flow shows when payload is encrypted** | `NEW` | 10 |
| Windows event logs for the timeline - what survives, what is cleared, what is never written | `KNOWN` | 8 |
| **Super-timelines with plaso/log2timeline - body file, mactime, build, filter, pivot** | `NEW` | 38 |
| The final forensic report - eight sessions of findings, D20 rubric applied | `PARTIAL` | 15 |
| [INVESTIGATION] Capstone - Windows image + Linux image + memory + pcap | `INV` | 45 |
| [INVESTIGATION] Volatility 3 - processes, connections, injected code | `KNOWN` | 10 |
| [RITUAL] Hash-verify + chain-of-custody close | `RIT` | 15 |
| **Total** | | **204** |
