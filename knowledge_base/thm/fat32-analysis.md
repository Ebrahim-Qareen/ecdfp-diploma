---
room: FAT32 Analysis
url: https://tryhackme.com/room/fat32analysis
module: File System Analysis (Section 1 of Advanced Endpoint Investigations)
feeds: S4 — `S4-06` FAT (direct hit, and far deeper than the row allows) · `S4-03` slack ·
       `S4-09` carving/recovery · `S4-10` the case model. Also gives us the MITRE mapping
       pattern R17 requires and a **Tier 1 evidence route we had not considered** (§4).
difficulty / time: **Hard** · **90 min** · 11 tasks (as stated by the room)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 11 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

FAT32 from first principles to hex, then three attacker techniques against it, then an unguided
challenge. It is the **deepest and most rigorous room in the batch so far** — rated Hard, 90
minutes, and it earns both.

Its structure is the best argument for our own Tier B shape: **structure → technique catalogue →
one MITRE technique per task, each done manually in a hex editor and then again with a tool →
unguided challenge.** Every practical task is explicitly labelled with its ATT&CK technique ID.

The room's own justification for teaching a 1996 filesystem is worth reusing verbatim in class:
FAT32 survives because it is lightweight and universally compatible, it caps at 4 GB per file and
2 TB per volume, and **it has no permission model at all** — so anyone can read or alter anything
on it. That last point is why attackers reach for FAT32-formatted USBs.

## 2. Artifacts — one 6-box block each

### 2.1 Boot sector / BIOS Parameter Block

- **What it is** — the first sector of a FAT32 volume, holding the metadata that makes the volume
  readable at all.
- **Where it lives** — **sector 0** of the partition, 512 bytes. Key fields and offsets, all
  little-endian:
  | field | offset | note |
  |---|---|---|
  | Jump instruction | `0x00–0x02` | `EB 58 90` |
  | OEM name | `0x03–0x0A` | e.g. `MSDOS5.0` — the formatting tool |
  | Bytes per sector | `0x0B–0x0C` | typically 512 |
  | Sectors per cluster | `0x0D` | |
  | **Reserved sectors** | `0x0E–0x0F` | **where FAT1 starts** |
  | Number of FATs | `0x10` | normally 2 |
  | Media descriptor | `0x15` | `0xF8` = fixed disk |
  | Hidden sectors | `0x1C–0x1F` | sectors before this partition |
  | Total sectors 32 | `0x20–0x23` | **must be non-zero on FAT32** |
  | **Sectors per FAT** | `0x24–0x27` | **where FAT2 starts** |
  | Flags (mirroring) | `0x28–0x29` | `0` = mirroring enabled |
  | Root directory cluster | `0x2C–0x2F` | usually 2 |
  | FSInfo sector | `0x30–0x31` | usually 1 |
  | Backup boot sector | `0x32–0x33` | usually 6 |
  | Boot sector signature | `0x1FE–0x1FF` | `55 AA` |
- **What it proves** — the geometry needed to compute every other offset on the volume, plus the
  formatting tool (OEM name) and volume size. **FAT1 offset = reserved sectors × sector size.
  FAT2 offset = (reserved sectors + sectors per FAT) × sector size.**
- **What it does NOT prove** — anything about file activity. It is volume metadata. The OEM name
  is a string written at format time and is trivially editable — it suggests a formatting tool,
  it does not attest to one. Several BPB fields (`Total Sectors` 16-bit, `Sectors per FAT` 16-bit,
  `Max Root Dir Entries`) are **zero on FAT32 by design** and mean "look at the extended BPB", not
  "corrupted".
- **How to parse it** — HxD (or any hex editor) at offset 0, reading little-endian; or Autopsy,
  which surfaces the same values in the image structure view.
- **Anti-forensics / false-positive caveat** — the room states none directly, but its own
  technique table names *"Volume Serial Number and Boot Sector Analysis"* for detecting tampering,
  and *"Analyzing FAT Table Corruption or Manipulation"* by **comparing FAT1 against FAT2**. The
  backup boot sector at sector 6 gives the same cross-check for the BPB. **Teach the cross-check:
  a lone value is a reading, a value that agrees with its backup is a finding.**

### 2.2 Reserved area — FSInfo and the backup boot sector

- **What it is** — the rest of the reserved region ahead of the FAT.
- **Where it lives** — sector 0 boot · **sector 1 FSInfo** · sectors 2–5 reserved ·
  **sector 6 backup boot sector** · sector 7 onward additional reserved, up to the FAT.
- **What it proves** — FSInfo holds the free-cluster count and the next free cluster; the backup
  boot sector holds a second copy of the BPB.
- **What it does NOT prove** — FSInfo is a **performance hint, not an authority**. Windows does
  not keep it perfectly current, so a free-cluster count that disagrees with the FAT is normal,
  not evidence. Never quote FSInfo as a finding about free space.
- **How to parse it** — hex editor at sector 1 and sector 6.
- **Anti-forensics / false-positive caveat** — the same as above: mismatch between the boot sector
  and its sector-6 backup is a tampering indicator worth chasing.

### 2.3 File Allocation Table and cluster chains

- **What it is** — the map of which clusters belong to which file, and which are free.
- **Where it lives** — FAT1 immediately after the reserved area; **FAT2 immediately after FAT1**.
  Each entry is 4 bytes; **only 28 bits are used** — that 32-bit entry is what names the filesystem.
  FAT index N corresponds to data-region cluster N, and **indices 0 and 1 are reserved virtual
  clusters, so real data starts at cluster 2**.
- **What it proves** — the full cluster chain of a file, in order, including fragmentation. Entry
  values:
  | value | meaning |
  |---|---|
  | `00 00 00 00` | free cluster |
  | `00 00 00 02` – `0F FF FF F6` | in use — value is the **next** cluster in the chain |
  | `0F FF FF F7` | bad cluster |
  | `0F FF FF F8` – `0F FF FF FF` | end of chain |
  | `FF FF FF FF` | end of chain (simplified form) |
- **What it does NOT prove** — content. The FAT says which clusters a file *occupies*, not what is
  in them, and after deletion the chain is unlinked while the data usually remains. It also cannot
  tell you *why* a cluster is marked bad — `0F FF FF F7` is a documented hiding place.
- **How to parse it** — hex editor at the computed offset; read each 4-byte entry reversed
  (little-endian).
- **Anti-forensics / false-positive caveat** — the room supplies a good nuance: **`0F FF FF FF`
  and `FF FF FF FF` both mark end-of-chain**, differing only in the top 4 reserved bits; some tools
  process those bits and some do not, so **two tools can legitimately render the same entry
  differently**. Standards prefer `0F FF FF FF`. That is a tool-disagreement lesson with a concrete
  example — rare and valuable.

### 2.4 Short File Name (SFN) directory entry

- **What it is** — the 32-byte record carrying a file's metadata.
- **Where it lives** — the root directory, starting at the data area's cluster 2. Layout:
  | offset | size | field |
  |---|---|---|
  | `0x00` | 11 | name in 8.3 form (`ABOUT_~1TXT`) |
  | **`0x0B`** | 1 | **attributes** — READ_ONLY `0x01` · **HIDDEN `0x02`** · SYSTEM `0x04` · VOLUME_ID `0x08` · DIRECTORY `0x10` · ARCHIVE `0x20` |
  | `0x0D` | 1 | creation time, tenths of a second |
  | `0x0E` | 2 | creation time — bits 0-4 = 2-second count, 5-10 = minutes, 11-15 = hours |
  | `0x10` | 2 | creation date — bits 0-4 = day, 5-8 = month, **9-15 = years since 1980** |
  | `0x12` | 2 | last access **date** |
  | `0x14` | 2 | first cluster, high word |
  | `0x16` | 2 | last modification time |
  | `0x18` | 2 | last modification date |
  | `0x1A` | 2 | first cluster, low word |
  | `0x1C` | 4 | file size (max 4 GiB − 1) |
- **What it proves** — name, attributes, three timestamps, starting cluster, size. **File size 0
  with the DIRECTORY attribute is how you tell a directory from a file.**
- **What it does NOT prove** — 🔴 **the timestamps are the weak point and the room is explicit
  about why: FAT32 has no journaling.** There is no second record to check a timestamp against, so
  a timestomped SFN entry is internally consistent and undetectable from the entry alone. Also:
  **last access is a DATE only, with no time** — a 2-second granularity on creation and no
  granularity at all on access. Do not present FAT32 timestamps with NTFS-level confidence.
- **How to parse it** — HxD at the root-directory offset, or Autopsy, whose **File Metadata tab
  exposes the Sleuth Kit `istat` output** including attributes, starting sector and length.
- **Anti-forensics / false-positive caveat** — attributes are a single byte with no permission
  system behind them: **setting HIDDEN is a one-byte edit anyone can make.** That is the entire
  basis of T1564.001 on FAT32.

### 2.5 Long File Name (LFN) directory entry

- **What it is** — the companion entries that carry a filename longer than 8.3.
- **Where it lives** — immediately **before** its SFN entry, 32 bytes each, UTF-16, split
  5 + 6 + 2 characters across offsets `0x01`, `0x0E`, `0x1C`. Attribute byte is `0x0F`.
  Byte 0 carries a **sequence number plus last-entry and deleted flags**; `0x0D` holds a
  **checksum of the short name** binding the LFN to its SFN.
- **What it proves** — the real filename, and — via the checksum — which SFN it belongs to. A long
  name may span several LFN entries, reassembled by sequence number.
- **What it does NOT prove** — nothing on its own; it carries no timestamps, no size, no cluster.
  The LFN is a label, the SFN is the record. **Its `0x1A` "first cluster" field is always zero** —
  a legacy compatibility field, not evidence.
- **How to parse it** — hex editor, reading the three name fragments in order and reversing UTF-16
  pairs.
- **Anti-forensics / false-positive caveat** — the room states none. The checksum link is the
  cross-check: an LFN whose checksum does not match the following SFN has been tampered with or
  belongs to a deleted entry that was partially overwritten.

### 2.6 Deleted entries — the `0xE5` marker

- **What it is** — how FAT32 records a deletion.
- **Where it lives** — **byte 0 of the directory entry is overwritten with `0xE5`**; the FAT chain
  is freed. The rest of the entry — attributes, timestamps, starting cluster, size — **survives
  intact**, and so does the file content until those clusters are reused.
- **What it proves** — that a file was deleted, plus everything the entry still holds: its
  timestamps, its size, and **its starting cluster, which is what makes recovery possible**. The
  room recovers a deleted PowerShell script whole from its starting cluster.
- **What it does NOT prove** — **who deleted it or when.** `0xE5` carries no timestamp of its own,
  and the surviving timestamps are the file's, not the deletion's. It also does not prove the
  content is complete — only the first cluster is recorded, and the chain is gone, so **a
  fragmented deleted file cannot be reassembled from the entry alone.** The room's example
  recovers cleanly because the file is contiguous; say so when teaching it.
- **How to parse it** — hex editor scanning directory clusters for entries beginning `E5`; or
  Autopsy, which surfaces deleted files in place and in `$RECYCLE.BIN`, with **Extract File(s)**
  on the right-click menu.
- **Anti-forensics / false-positive caveat** — the first character of the original filename is
  **destroyed** by the `0xE5` byte, which is why recovered names show as `?STRIKE~1.PS1`. Also
  note the room's own finding that root-directory clusters can be **non-contiguous** — it had to
  follow the FAT chain to find the rest of the directory entries. **Scanning only the first
  cluster of the root directory silently misses deleted files.**

### 2.7 Timestamps as an anti-forensics target (T1070.006)

- **What it is** — creation, last-access and last-modified times, and their manipulation.
- **Where it lives** — the SFN entry (§2.4).
- **What it proves** — a timeline, when consistent.
- **What it does NOT prove** — 🔴 the room's central caveat: **FAT32 implements no journaling, so
  there is no second source to validate a timestamp against.** Detection is therefore
  *inference from inconsistency*, never proof. The room's honest list of what you can actually do:
  cross-reference against external logs (e.g. Windows event logs), use file-integrity monitoring,
  or hunt for the timestomping tool itself.
- **How to parse it** — manually per SFN entry, or **Autopsy's Timeline view**, adjusting the date
  range and switching the scale to Linear to make sparse years visible.
- **Anti-forensics / false-positive caveat** — **the best teaching content in the room.** Two
  inconsistency patterns to hunt: creation later than modification or access, and timestamps wildly
  out of line with neighbours. **And the essential false positive: modified-before-created is
  completely normal** — copying a folder preserves modification times while resetting creation and
  access. The room's worked example turns on a *different* anomaly: an **access date earlier than
  the modified date**, and in Autopsy's timeline a **File Accessed event in a year with no
  preceding File Creation event**. That is a genuinely good finding-vs-interpretation exercise.

## 3. Tools and commands

| tool | version the room uses | action | what it outputs |
|---|---|---|---|
| **HxD** | **not stated** | `File > Open` the `.001` image; **`CTRL+G`** to go to a hex offset | raw bytes, Decode Text column, Data Inspector |
| **Autopsy** | **not stated** | New Case → Add Data Source → *Disk Image or VM file* → Configure Ingest → Finish | image structure tree, per-file metadata |
| Autopsy — File Metadata tab | — | scroll to *"From the Sleuth Kit istat Tool"* | attributes, starting sector, length |
| Autopsy — Timeline | — | toolbar → Timeline; set range; **Scale → Linear** | event graph by year, drill to event list |
| Autopsy — extraction | — | right-click → **Extract File(s)** | the recovered file |

The room teaches **no CLI at all** — no `mmls`, no `fsstat`, no `fls`. Everything is hex editor or
GUI. See §5.

### CURRENCY CHECK — cross-referenced against `_TOOL_CURRENCY_2026-08-28.md`

| item | result |
|---|---|
| **HxD** | **2.5.0.0, released 11 Feb 2021** — still free for private *and* commercial use, still opens physical disks and RAM. **5.5 years without a release**; single maintainer. No lesson breaks today, but name a fallback in the setup guide. |
| **Autopsy** | **4.23.1**. 🔴 **Keyword Search and email regexp are now OFF by default at ingest.** The room selects only *Recent Activity* and *File Type Identification*, so its own walkthrough is unaffected — but any lab step of ours that expects keyword hits must tick the box explicitly. |
| Autopsy — 32-bit dropped | since 4.20.0; 64-bit only. |
| Autopsy ↔ TSK version | Autopsy 4.23.1 bundles **TSK 4.14.0**, not 4.15.0. Do not conflate. |
| Sleuth Kit `istat` | the room reaches TSK output *through Autopsy's GUI* without naming it as TSK. Our material should name it — `istat` is the CLI equivalent and belongs in `S4-08`. |
| Room's version claims | **none stated for any tool** — sixth room running. This is now a documented pattern across the whole path, not a per-room lapse. |
| ⚠️ Lab OS mismatch | the room's VM is **Windows Server 2019**. Our FOR-WS01 is Windows 10/11 (Part 6). Nothing here depends on the difference, but note it — room 1's prefetch caveat (*not enabled by default on Server*) shows the path is not consistent about which OS it assumes. |

## 4. Evidence used

- Five FAT32 images on a Windows Server 2019 lab VM in `C:\FAT32_analysis\`:
  `FAT32_structure.001` (**64 MB**, per the room's own Total-Sectors arithmetic),
  `FAT32_HIDDEN.001`, `FAT32_TIMESTOMP.001`, `FAT32_DELETED.001`, `FAT32_CHALLENGE.001`.
- **Not downloadable. No licence offered.** Lab credentials published inline again —
  **deliberately not recorded here (R8).**
- **Nothing to flag for `ecdfp-evidence` from the room itself.**

### ✅ But this room reveals a Tier 1 route we had not considered — flag this to `ecdfp-evidence`

Part 5 rules out synthesising `.evtx`, E01/raw images, memory dumps and hives — correctly. **But a
FAT32 volume is the exception that proves the rule: we can make a real one ourselves, trivially.**
Format a small virtual disk or USB as FAT32, populate it, then stage each scenario:

| scenario | how it is staged | teaches |
|---|---|---|
| hidden | set the HIDDEN attribute (`0x02`) on a file and a directory | `S4-06`, T1564.001 |
| timestomp | alter timestamps, leaving one inconsistency | `S4-06`, T1070.006 |
| deleted | delete a **contiguous** file, and a **fragmented** one | `S4-06`, `S4-09`, T1070.004 |
| slack | write a small file into a large cluster | `S4-03` |

That is **Tier 1 — our own acquisition, genuine bytes, no licence question, ~64 MB, distributable
on the classroom USB**, and it directly serves `EVS-04` (the suspect USB) which `S4-06` already
names. It is by far the cheapest Tier 1 evidence in the whole course, and it needs no compromise
staging on EVI-SRC01. **Recommend `ecdfp-evidence` scope this as a distinct set.**

## 5. Lab design worth reusing

**The strongest room in the batch for design, and three ideas are worth taking wholesale.**

1. **🟢 One MITRE technique per task, in the task title.** Tasks 7, 8 and 9 are literally named
   `T1564.001 Hidden Files and Directories`, `T1070.006 Indicator Removal: Timestomp`,
   `T1070.004 File Deletion and T1070.009 Clear Persistence`. **R17 requires us to map findings to
   ATT&CK; this room shows the mapping can be the organising principle rather than a chip added
   afterwards.** Strong candidate for how S4's catalogue chapter is titled.
2. **🟢 Manual first, tool second — every single time.** Each scenario is worked by hand in HxD and
   then repeated in Autopsy, and the room states the reason plainly: manual analysis is slow and
   error-prone, but knowing the structure is what lets you adjudicate **when two tools disagree**.
   That is our `S1`/`S2` integrity argument arriving from a third party, and it pairs with the
   `0F FF FF FF` vs `FF FF FF FF` example in §2.3 where tool disagreement is *documented*.
3. **🟢 The challenge offers a harder mode.** Task 10: *"if you want a more demanding challenge,
   you can answer all the questions using only the HxD editor."* **One sentence that
   differentiates a mixed-level class** — exactly the D16/mixed-ability problem our
   `student_activity.md` has to solve. Steal the pattern for every session.
4. Techniques are catalogued before they are used (Task 6), split into *Filesystem Integrity and
   Structural Analysis* vs *Data Recovery and Content Analysis*, each mapped to the FAT32 fields it
   needs. A good scaffold, though see below.
5. The room repeatedly makes students **compute an offset from the boot sector** rather than handing
   it over — `reserved sectors × 512 → hex`. That is the arithmetic our students must own, and it
   is checkable in one line.

### 🔴 What we must NOT copy — a safety defect

**Task 9 instructs the student to copy the recovered PowerShell script and paste it into a
PowerShell window to see what it does.** The sandbox caveat appears only afterwards, as a note
attached to the question. That is backwards, and it violates our standing rules directly:

- **R9** — evidence is handled on a copy; you do not execute recovered content to identify it.
- **`scope_decisions.md`** — malware reverse engineering is out of course; *"the course examines
  artifacts of execution, not the binary."*
- **D19** — no real malware sample anywhere in our material.

**Our version recovers the script and reads it. It never runs it.** This is worth naming in class
as a published-teaching-material defect, alongside room 4's plaintext SCP password — students
should leave the course able to spot bad practice in the sources they learn from.

Also not to copy: the room's technique tables (Task 6) name techniques but **no tools**, despite the
task being titled *"Analysis Techniques and Tools"*. Our equivalent must name the tool per technique.

## 6. Question patterns

~20 questions across 11 tasks, of which Task 10's challenge carries **8**.

- **🟢 The best question design of any room so far, because several questions require the student to
  COMPUTE, not look up**: *"At which offset does the FAT2 table start?"* — which forces
  `(reserved sectors + sectors per FAT) × 512 → hex`. And a purely hypothetical one:
  *"file B's chain starts at cluster F and ends at cluster 10 — what is the FAT entry at cluster F?"*
  **answerable with no image at all, purely from understanding the structure.** That is the
  cheapest high-quality assessment format we have seen; it needs no evidence, no VM, and no
  network. **Adopt it for `S4-06` homework.**
- **Answer formats are specified** (`XXXXXXXX` for offsets, `name.extension`, "without spaces") —
  same discipline as room 5.
- **The challenge is genuinely unguided** and spans all three techniques plus structure — the shape
  our `student_activity.md` should take.
- **Still zero "this cannot be determined" answers** — sixth room, same omission. And this room
  hands us the strongest candidate yet, because it *states* the limit and never tests it:
  **"FAT32 has no journaling"** → *"from this image alone, can you determine when the timestamps
  were altered?"* Answer: **no.** Add it.

## 7. Figures we would need to draw

Many screenshots of HxD and Autopsy panes — i.e. click paths and answers. Three concepts deserve
our own inline SVG, and the first is the one the room references but never adequately draws:

| what is needed | our SVG spec (one line) |
|---|---|
| the FAT32 volume map | a proportional horizontal bar: Reserved (boot 0 · FSInfo 1 · backup 6) → FAT1 → FAT2 → Data Area (root dir at cluster 2 → data region), with the two offset formulas annotated **on the boundaries they compute** |
| a cluster chain across the FAT and the data region | two parallel rows — FAT entries above, data clusters below — with arrows hopping 9→10→11→12 and the final `0F FF FF FF` flagged EOF, plus one greyed "deleted: chain freed, data intact" variant beside it |
| what deletion actually destroys | one SFN entry drawn as 32 labelled bytes, with **only byte 0 struck through in red** and every surviving field tinted as recoverable — captioned "one byte changed, everything else still there" |

The third is the single most useful diagram for `S4-06`: it makes "deletion is not erasure" visible
in one glance. Never their images (D22).

## 8. Fit against our material

### ✅ Part 1's mapping is correct for this room — the first one that is

Part 1 maps it to **S4 / `S4-06`**. That is right. (Rooms 2, 4 and 5 were all mis-mapped.)

### 🔴 But `S4-06` is 17 minutes and this room is 90

`S4-06` reads: *"FAT — FAT table, directory entries, and what deletion actually does"* · **17 min**.
The room covers the same ground at Hard difficulty in 90 minutes plus a challenge.

We are not obliged to match a THM room's depth — our course is 24 hours across six domains, and
FAT32 is one row. But the gap is large enough to force a decision:

- **The 17 minutes is defensible** if `S4-06` teaches: the three areas, the SFN attribute byte and
  timestamps, the `0xE5` marker, and "deletion unlinks the chain, the data stays". That is the
  exam-relevant core and it fits.
- **What will not fit** is manual boot-sector arithmetic in hex, LFN reassembly, and cluster-chain
  walking. Those are the room's best content and they are *hands-on* content.

**Recommendation to `ecdfp-intake` — no new row, no minute cost:** move the deep material to
**homework**, using the hypothetical question format from §6 (no image, no VM required), exactly as
Part 4 already does with the WinHex and Volatility homework tracks. `S4-06` keeps its 17 minutes and
teaches the concepts; the offset arithmetic and chain-walking become a take-home worksheet.
**This is the first room in the batch that adds real value without adding minutes.**

### Rows this strengthens

- **`S4-06`** — direct hit; supplies the entire structure reference and the `0xE5` mechanics.
- **`S4-03`** slack — the room's technique table names *Slack Space Analysis* explicitly.
- **`S4-09`** carving / recovery — the deleted-file recovery walk is a cleaner worked example than
  a carver, because it recovers *by structure* rather than by header signature. **Worth teaching
  both and contrasting them: structure-based recovery needs an intact directory entry, carving does
  not but loses the filename.**
- **`S4-10`** the case — Task 10's shape (one image, eight questions, unguided, optional harder
  mode) is close to what Case 04 should look like.
- **`EVS-04`** — see §4; a self-made FAT32 image is the cheapest Tier 1 evidence in the course.

### ⚠️ One dependency note

The room's stated prerequisites include **Autopsy** and **Intro to Cold System Forensics** — both
Priority 1 / 3 rooms in our Part 1 list, both still unextracted. Our S4 ordering puts FAT32 before
them. Not a defect for instructor notes, but if anyone runs these hands-on, do Autopsy first.

### S5 overdraft — unchanged

This room touches S4 only. **S5 remains at 65 minutes demanded** (rooms 1–5). S4 is at exactly 220
and this room, on the recommendation above, adds **0**.

### Out of scope

Nothing. Entirely on-topic for `S4`.

## 9. Links

- Room: <https://tryhackme.com/room/fat32analysis>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 1)
- Room's stated prerequisites: Pre Security, **Intro to Cold System Forensics** (Priority 3),
  **Autopsy** (Priority 1) — both in our extraction list, neither yet extracted.
- MITRE techniques the room maps to FAT32, worth carrying into `S4` as the chapter's ATT&CK row:
  **T1006** Direct Volume Access · **T1564.001** Hidden Files and Directories ·
  **T1564.005** Hidden File System · **T1070.004** File Deletion · **T1070.006** Timestomp ·
  **T1070.009** Clear Persistence · **T1027.001** Binary Padding — most under **TA0005**, which
  **ATT&CK v19 renamed from "Defense Evasion" to "Stealth"** (the remainder split off as
  **TA0112 Defense Impairment**). Verified 2026-08-28 against Enterprise **v19.2**. **Do not print
  "Defense Evasion" on a slide.** Source of the correction: `windows-memory-and-user-activity.md` §3 #16.
- Tool currency for HxD and Autopsy: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md`

END OF NOTE.
