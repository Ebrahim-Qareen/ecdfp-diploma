# plan_8_sessions.md — the 8-session shape, with Linux forensics

**Built 2026-08-29** at Ebrahim's request: grow the diploma to **8 × 4 h = 32 h** and bring Linux
forensics into scope. Supersedes the six-session pack in `session_time_estimates.md`; the timing
model and the prior-knowledge evidence behind it are unchanged and still apply.

**Nothing is applied.** `topic_map.md`, `coverage_matrix.md`, `scope_decisions.md` and
`DECISIONS.md` are untouched. §5 lists the four locked decisions this proposal contradicts.

---

## 1 · The shape

**93 blocks · 1,609 topic minutes · capacity 1,640 (8 × 205) · 31 spare.** Every session lands at
or under 205.

| # | Session | Min | Character |
|---|---|---:|---|
| **S1** | Forensic Foundations, Evidence Integrity & Chain of Custody | 201 | mostly revision + the report template |
| **S2** | Acquisition — Live Response, Memory & Media | 199 | half revision, imaging is new |
| **S3** | Data Representation & File Examination | 205 | half new |
| **S4** | Partitions & File Systems — MBR, GPT, FAT, NTFS | 205 | **all new** |
| **S5** | Windows Forensics I — Registry, System Config & USB | 187 | **all new** |
| **S6** | Windows Forensics II — Execution & User Activity | 203 | **all new** |
| **S7** | **Linux Forensics — File Systems, Artifacts & Logs** | 205 | **all new** |
| **S8** | Network, Timelines, Reporting & Capstone | 204 | mostly revision + plaso |
| | | **1,609** | |

**What the two extra sessions bought:**

| Gained | How |
|---|---|
| **Linux forensics as a full session** | S7, new |
| **Windows forensics split in two** | S5 / S6 — it was one 216-minute session, over budget, with seven consecutive new artifacts |
| **Five orphans restored** | UserAssist + BAM · browser forensics (`D35`) · OSCAR · statistical flow analysis · `ControlSet`/`Select`, `$LogFile`/`$UsnJrnl`, ADS and evidence-affecting keys as blocks of their own |
| **Room to breathe** | S5 sits at 187 — the first session in any plan with real slack |

Block mix: 40 `NEW` (670 min) · 24 `PARTIAL` (359) · 11 `KNOWN` (95) · 10 investigations (365) ·
8 rituals (120).

---

## 2 · Linux — it is sourced, not invented

**INE's eCDFP does not teach Linux forensics.** Across all 2,218 pages: no `bash_history`, no
`crontab`, no "Linux forensics"; `ext2/3/4` once in passing. So this session cannot be built from
the INE modules, and the project rule is that a topic with no source is a gap that gets researched
or removed — never taught from memory.

**It does not have to be.** Two TryHackMe rooms already extracted into `knowledge_base/thm/` are
Linux forensics on the same R10 six-box template — **16 artifacts between them**:

| Source | What it carries |
|---|---|
| [`exfilnode.md`](../knowledge_base/thm/exfilnode.md) — **100 % Linux**, medium, 70 min | Linux login records (wtmp/btmp/lastlog) · timezone on a dead image · **USB attach/detach, and why Linux has no USBSTOR** · shell config as an artifact — the alias that hides the command · `.bash_history` and the silent-omission trap · remote-host and name-resolution artifacts · **ext4 inode timestamps and what "likely timestomped" actually means** · cron and the rest of Linux persistence |
| [`initialaccesspot.md`](../knowledge_base/thm/initialaccesspot.md) — Linux host `SRV-DMZ`, Honeynet Collapse step 1 | web-server access logs and the status code that dates the compromise · the dropped PHP webshell · **SUID, sudoers and the one nobody checks** · `sudo`'s own log · **auditd syscall records and the field that survives escalation** · persistence · the bootloader as an access path |
| INE `8.3` Linux log tools (32 pp) + `8.6` Syslog (15 pp) | `grep`/`cut`/`awk` pipelines, syslog format — **free for this cohort** (Linux Administration + SOC already taught it) |
| The Sleuthkit — `fls`, `istat`, `icat`, `blkls`, `mactime` | already taught in S4; **works on ext2/3/4 unchanged**, so the tooling transfers at zero cost |

**Two things still to do before S7 can be built:**

1. **There is no `Module_06` for Linux.** The 16 artifacts live in room notes, not in a condensed
   module on the six-box template. That is an `ecdfp-intake` job — the same shape as M1–M5.
2. **`exfilnode` is the case, and it needs an evidence set.** Its own note records that it is the
   *"first of 22 rooms to contribute no evidence set — `EVS-10` stays unallocated."* `EVS-10` is
   now allocated: the Linux exfiltration node. `ecdfp-evidence` owns it.

**The elegant integration.** `D19`'s carry-through chain already has *RDP lateral movement to a
second host*. **Make that second host Linux.** Then S7 is not a bolt-on module — it is the same
incident seen from the other machine, and the capstone genuinely spans two platforms. `exfilnode`
is literally built that way: a second machine, motivated by the first machine's limit.

**What it costs, stated plainly: Linux is not on the eCDFP exam.** S7 is **205 minutes — 12.7 % of
the diploma — on non-examinable material.** That is a competence decision, not an exam decision,
and it is defensible for a cohort that already holds Linux Administration. But it should be said
out loud to students, and `coverage_matrix.md` should reconcile the exam domains *excluding* S7
rather than pretending Linux time counts toward them.

---

## 3 · The eight sessions, block by block

`NEW` = nothing in CCNA / MCSA / Linux Administration / SOC / CEH / eCIR taught it.

### S1 — Forensic Foundations, Evidence Integrity & Chain of Custody

**201 min** · 13 blocks · **3 new**

Build from: `Module_01` · `Module_05` (report template) · `instructor/Session_01`

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

### S2 — Acquisition: Live Response, Memory & Media

**199 min** · 12 blocks · **4 new**

Build from: `Module_01` · `instructor/Session_01` §2 · thm `forensic-imaging`, `memory-acquisition`

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

Build from: `Module_02` · `instructor/Session_02` · thm `autopsy`, `file-carving`

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

### S4 — Partitions & File Systems: MBR, GPT, FAT, NTFS

**205 min** · 10 blocks · **6 new**

Build from: `Module_03` · `instructor/Session_03` · thm `mbr-and-gpt-analysis`, `fat32-analysis`, `ntfs-analysis`, `file-carving`, `diskrupt`

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

### S5 — Windows Forensics I: Registry, System Configuration & USB

**187 min** · 11 blocks · **4 new**

Build from: `Module_04` §2A · `instructor/Session_04` · thm `expediting-registry-analysis`, `windows-user-account-forensics`

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

### S6 — Windows Forensics II: Execution & User Activity

**203 min** · 11 blocks · **8 new**

Build from: `Module_04` §2A · `instructor/Session_05` · thm `windows-user-activity`, `windows-applications-forensics`, `compromised-windows-analysis`

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

### S7 — Linux Forensics: File Systems, Artifacts & Logs

**205 min** · 12 blocks · **9 new**

Build from: **thm `exfilnode` + `initialaccesspot`** · INE `8.3`/`8.6` · TSK on ext4 — ⚠ no `Module_06` yet

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

Build from: `Module_04` §2B · `Module_05` · `instructor/Session_06`–`08` · thm `blizzard`, `volatility-essentials`, `windows-memory-and-network`

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
---

## 4 · Sequencing — the prerequisite edges still hold

```
S1 integrity  ->  S2 acquisition  ->  S3 file examination
S4 partitions & file systems  ->  S5 registry  ->  S6 execution & user activity
S7 Linux (needs S4's file-system layer and S6's artifact discipline)
S8 timelines, reporting and the capstone  LAST
```

`D25`'s three load-bearing edges survive the split:

| Depends | On | Why |
|---|---|---|
| `S5` registry structure | `S4` NTFS `$MFT` | hives are files — you cannot locate or carve them without the file system |
| `S8` plaso super-timeline | `S8` event logs · `S4` `$MFT` parsing | a super-timeline is only meaningful once its inputs are understood |
| `S8` capstone | S1–S7, all | it introduces no new technique |

**One new edge, from the split:** `S6` evidence-of-execution depends on `S5`'s registry structure —
ShimCache, Amcache, UserAssist and BAM are all registry-resident. Keep S5 before S6.

**One new edge, from Linux:** `S7` ext4 inode timestamps are taught as a **contrast** with `$MFT`
`$STANDARD_INFORMATION` / `$FILE_NAME` (S4), and Linux's absent USBSTOR as a contrast with S5's USB
history. Both are cheap *because* the Windows side is already taught — S7 must not move earlier.

---

## 5 · What this proposal breaks — four locked decisions

Every one needs a dated `DECISIONS.md` row before any of this is built.

| Locked | Says | This proposal |
|---|---|---|
| **`D1`** | 6 × 4 h = 24 h | **8 × 4 h = 32 h.** The headline change |
| **`D38`** | Linux / macOS forensics out of scope; one cross-platform contrast table in S1 | **Linux in scope as a full session.** macOS stays out — `thelasttrial` remains the third column of a contrast table, not a session |
| **`coverage_matrix.md`** | ★ LOCKED, per-session domain hours for six sessions | must be **re-derived for eight**, and `D24`'s ≤ 1.0 pp reconciliation re-run — **excluding S7**, since Linux is not examined |
| **`scope_decisions.md`** §1 | "fourth course after SOC → CEH → eCIR" · Linux excluded row | prerequisite stack is **CCNA → MCSA → Linux Administration → SOC → CEH → eCIR** (seventh course), and the Linux exclusion row is withdrawn |

**Phase 3 impact — this is the real cost, and it is lab work, not writing:**

| Needs | Detail |
|---|---|
| **A Linux evidence host** | `FOR-LNX01` is the *analysis* workstation. S7 needs an *evidence* image — call it `EVI-LNX01` — staged with the exfiltration leg of `D19` |
| **`EVS-10`** | the Linux host image + its `/var/log` set. Previously unallocated; `ecdfp-evidence` owns the ID, licence and hashes |
| **`Module_06`** | the 16 Linux artifacts condensed onto the R10 six-box template — an `ecdfp-intake` job, currently only room notes exist |
| **`D19` restaging** | make the RDP lateral-movement target a Linux host so S7 is inside the carry-through case, not beside it |
| **Two more session packages** | `packages/session-07/` and `session-08/`, nine documents each, plus two `docs/session-NN/` pages |

---

## 6 · If 8 is still too many, or not enough

| | Sessions | What changes |
|---|---:|---|
| **6** (`session_time_estimates.md`) | 6 | Windows stays one 216-min session; Linux is homework only (the THM `initialaccesspot` room). Fits, tightly |
| **7** | 7 | Take **either** the Windows split **or** the Linux session, not both. Windows split is the stronger buy — it fixes an over-budget session; Linux is additive |
| **8** (this file) | 8 | Both. 31 min spare, no session over 205 |
| **9** | 9 | Split S4 into *Disks, Partitions & FAT* + *NTFS, Slack & Carving*. It is the third all-`NEW` session and the last real pressure point |

**Recommendation if the diploma must stop growing: 8 is the right stopping point.** Seven leaves an
over-budget session; nine buys comfort rather than coverage.
