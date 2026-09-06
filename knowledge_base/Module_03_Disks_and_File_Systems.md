# Module 03 — Disks and File Systems

| | |
|---|---|
| **INE source** | unit 4 — *Disks* (155 pp) · unit 5 — *File Systems* (317 pp) |
| **Feeds sessions** | `S4` |
| **Source text** | [`_source_text/INE_Unit_04_Disks.md`](_source_text/INE_Unit_04_Disks.md) · [`_source_text/INE_Unit_05_File_Systems.md`](_source_text/INE_Unit_05_File_Systems.md) |
| **Instructor delivery** | [`instructor/Session_03_Disks_and_File_Systems.md`](instructor/Session_03_Disks_and_File_Systems.md) |

> Condensed reference, our words, from INE's eCDFP courseware. Not published.
> Page cites `[U4 p86–104]` point into the source-text files, which are OCR — check any exact
> string on the source page before putting it in front of students.
>
> **OCR note that applies to this whole module.** The INE PDFs are video screen captures, so the
> machine read consistently turns `$` into `S` (`SMFT`, `SLogFile`, `SSTANDARD_INFORMATION`),
> loses the first row of several tables, and mangles superscripts (`2**`, `2™`, `272` are all
> exponents). Every `$`-name and every offset table below has been written back to its correct
> form; wherever the underlying source is genuinely unreadable it is marked `⚠ verify against
> source page` and the value is *not* guessed.

---

## 0 · What this module is for

After this module a student can take a raw disk image and answer *where* something is, not just
*what* it is: read sector 0 and say whether the disk is MBR or GPT, walk a partition table by hand,
find the file system's own metadata (the FAT, or `$MFT`), and turn a filename into a list of clusters
and an offset in the image. They can also say — precisely, and with the right hedges — what happens
to a file when a user deletes it, and therefore what is and is not recoverable, on a FAT thumb drive
versus on an NTFS system volume versus on an SSD that has been TRIMmed.

It sits directly after acquisition (S1–S2, units 1–3): the image exists and has been hashed, and now
the question is how to read it. It is the load-bearing module for everything after. **S5 (registry)
depends on students believing that a hive is just a file with an `$MFT` record like any other**, so
that "the registry" stops being magic. **S6 (super-timeline) depends on `$MFT` parsing**, because
`$STANDARD_INFORMATION` and `$FILE_NAME` timestamps are the backbone of the timeline that everything
else is pinned to. If a student leaves this module vague about `$MFT`, two later sessions collapse.

---

## 1 · Core concepts

### Sector
- **Definition** — the smallest unit of data a storage device will physically read or write, addressed
  as a whole; the device cannot hand you half a sector.
- **Why it exists** — magnetic media needs a fixed-size frame carrying sync, address and error
  correction around each chunk of user data; a variable-length read is not physically practical.
- **Where it shows up** — every offset in an image is ultimately a sector number; `mmls` and `fsstat`
  report their units in sectors; imaging tools count sectors, not bytes.
- **Example** — 512 bytes is the classic logical sector. Advanced Format (AF) drives moved to 4096
  bytes. Total capacity = cylinders × heads × sectors-per-track × sector size. `[U4 p26–28]`
- **In the case (D19)** — EVI-SRC01's partition starts at LBA 2048 (the usual 1 MiB alignment), so
  every TSK command against that volume needs `-o 2048` or the tool reads the wrong bytes and
  reports "no file system".
`[U4 p26–28]`

### Cluster (allocation unit)
- **Definition** — the smallest unit of space a *file system* will allocate to a file; one cluster is
  a whole number of contiguous sectors.
- **Why it exists** — tracking every 512-byte sector on a large volume would make the allocation map
  enormous. Grouping sectors shrinks the map at the cost of wasting the tail of the last cluster.
- **Where it shows up** — sectors-per-cluster is fixed at format time and stored in the boot record
  (FAT BPB offset 13, NTFS `$Boot` offset 13). Everything downstream — the FAT chain, an NTFS
  runlist, `blkcat` — is expressed in clusters.
- **Example** — INE's FAT32 sample: 512 bytes/sector × 2 sectors/cluster = 1024-byte cluster; a 512-byte
  file fills one sector and wastes three. A 1024-byte file in a 4-sector cluster wastes two.
  `[U5 p33–45]`
- **In the case (D19)** — the exfil USB is FAT32 with 4096-byte clusters (`fsstat` reports
  `Cluster Size: 4096`), so every deleted staged file left up to 4 KB of recoverable slack behind it.
`[U5 p33–45, p47–48]`

### CHS and LBA addressing
- **Definition** — CHS addresses a sector by its physical geometry (cylinder, head, sector); LBA
  addresses it by a single running number starting at zero.
- **Why it exists** — CHS was how the BIOS talked to real spinning geometry. Its three-byte field
  (10 bits C, 6 bits S, 8 bits H) caps a drive at 1024 × 255 × 63 × 512 bytes ≈ **7.84 GiB**, which
  disks blew past; LBA removes the geometry from the address entirely.
- **Where it shows up** — MBR partition entries still carry *both* a starting/ending CHS and a
  starting LBA, for backward compatibility. GPT is LBA-only.
- **Example** — CHS `(0,0,1)` is LBA `0`. Sectors count from 1 in CHS and from 0 in LBA — the single
  most common off-by-one in this material. Conversion:
  `LBA = ((C × heads_per_cylinder) + H) × sectors_per_track + S − 1`.
  INE's exercise (16 heads/cyl, 63 sectors/track, CHS `(2,3,4)`) works out to
  `((2×16)+3)×63 + 4 − 1 = 35×63 + 3 = 2208`. The answer slide is blank in the OCR; the arithmetic
  above is from INE's own formula. `[U4 p29–41]`
`[U4 p29–41]`

### Volume vs partition
- **Definition** — after Brian Carrier: a **partition** is a run of *consecutive* sectors; a **volume**
  is a collection of sectors that are *logically* consecutive but need not be physically contiguous.
- **Why it exists** — the two words are used interchangeably in the wild and it breaks reasoning about
  spanned, striped and mirrored sets. Every partition is a volume; not every volume is a partition.
- **Where it shows up** — a whole unpartitioned disk is one volume; two disks spanned into one drive
  letter is one volume across two disks; a partition of disk 1 plus all of disk 2 is one volume.
- **Example** — Windows assigns a drive letter per volume, not per disk. A stock Windows install has
  at least two partitions: a small System Reserved / EFI partition and the OS partition. `[U4 p73–81]`
- **In the case (D19)** — reporting "the evidence was on the C: volume" is not the same statement as
  "the evidence was on physical disk 0"; the report must say which.
`[U4 p69–83, p134–139]`

### NAND page, block and plane — and the erase asymmetry
- **Definition** — inside an SSD, a **page** is the smallest readable/writable unit; a **block** is the
  smallest *erasable* unit and holds many pages; blocks are grouped into planes.
- **Why it exists** — NAND cells can be programmed individually but only reset in bulk. That single
  physical constraint is the root of every SSD forensic problem.
- **Where it shows up** — you never see it directly. The controller's flash translation layer (FTL)
  hides it, which is exactly the problem: the LBA the OS asks for and the physical page holding that
  data are not fixed to each other.
- **Example** — INE's numbers: page 4 KB, block = 128 pages, plane = 128 blocks. You can write one
  4 KB page, but to erase anything you must erase all 128 pages of its block at once. `[U4 p61–65]`
- **In the case (D19)** — the workstation disk in EVI-SRC01 is an SSD, so "the staging archive was
  deleted three days before seizure" and "the staging archive is unrecoverable" are both true, and
  the second is a *consequence of the hardware*, not of the suspect being careful.
`[U4 p57–66]`

### TRIM, wear levelling and garbage collection  ⚠ **not covered by INE units 4 or 5**
- **Definition** — **TRIM** is an ATA/NVMe command by which the operating system tells the SSD that
  certain LBAs no longer hold live data. **Garbage collection** is the controller then erasing those
  blocks on its own schedule. **Wear levelling** is the controller moving live data around so no block
  wears out first.
- **Why it exists** — because a block must be erased before it can be rewritten, an SSD that does not
  know which pages are dead has to do a slow read-modify-erase-write cycle on every write. TRIM lets
  the drive pre-erase in the background and stay fast.
- **Where it shows up** — nowhere you can observe from the file system. The OS issues TRIM on delete,
  on quick format, and on partition delete. Check the OS side with `fsutil behavior query
  DisableDeleteNotify` (0 = TRIM enabled). ⚠ command not from INE — verify before demoing.
- **Example** — a file is deleted on a TRIMmed SSD. The `$MFT` record and `$UsnJrnl` entry may survive
  and prove the file *existed*. The clusters return **zeroes**, permanently, often within seconds, and
  they return zeroes even through a write blocker, because the erase happened inside the drive before
  seizure. Carving finds nothing. Slack analysis finds nothing. There is no undo.
- **In the case (D19)** — this is why the exfiltrated archive is proven by `$MFT` and `$UsnJrnl`
  metadata and by the *USB copy*, and not by recovering the file body from the workstation SSD.
- **This is the single most important "what you cannot recover" fact in the course.** INE's SSD
  section (`[U4 p57–66]`) says only that SSDs "pose challenges" and that mishandling them may make
  evidence inadmissible, and then points at Belkasoft's SSD article series without ever naming TRIM.
  The gap is recorded in §7; the concept is taught anyway because the course needs it.
`[U4 p57–66]` (concept absent from source — see §7)

### Slack
- **Definition** — allocated storage a file does not use. **File slack**: sectors allocated to a file
  in its last cluster that the file never wrote into. **RAM slack**: the padding from the end of the
  file's data to the end of its *last written sector*. **MFT slack**: leftovers inside an `$MFT`
  record after a resident file grew and its data moved out. **Volume slack**: sectors between the end
  of the file system and the end of the partition that declared it.
- **Why it exists** — allocation is granular (clusters) and I/O is granular (sectors), so both round
  up, and rounding up leaves whatever was there before.
- **Where it shows up** — the tail of every allocated cluster on every volume; INE's rule of thumb is
  that unused *bytes* in an allocated sector are of limited value, while unused *sectors* in an
  allocated cluster are gold, because they hold the previous file's content intact.
- **Example** — INE's worked case: 4 KB clusters. `file.txt` (8 KB) occupies clusters 8000–8001, all
  16 sectors. Deleted. `file2.pdf` (5 KB) is written into the same two clusters and uses 10 sectors.
  The remaining **6 sectors × 512 = 3072 bytes** of `file.txt` are still readable inside space that
  the file system calls allocated. `[U5 p225–238]`
- **In the case (D19)** — slack on the USB is where fragments of an earlier collection pass survive
  even though the current directory listing shows only the last archive.
`[U5 p225–239]`

### Allocated, unallocated, and what "deleted" actually means
- **Definition** — *allocated* means a metadata structure currently claims those clusters. *Unallocated*
  means nothing claims them. Neither says anything about whether the bytes are still there.
- **Why it exists** — deleting content costs I/O; deleting a pointer costs almost nothing. Every
  mainstream file system therefore deletes the pointer.
- **Where it shows up** — FAT: the directory entry's first name byte becomes `0xE5` and the file's FAT
  chain entries are zeroed. NTFS: the in-use flag in the `$MFT` record header is cleared and the
  clusters are marked free in `$Bitmap`. In both, the content is untouched.
- **Example** — `istat` on a deleted FAT entry reports `Not Allocated` but still prints the size,
  timestamps and a name of `_EPORT.CSV` — the underscore is TSK rendering the `0xE5` that overwrote
  the `R` of `report.csv`. `[U5 p138, p292]`
- **In the case (D19)** — on the FAT32 USB the deleted staging archives are still enumerable with
  `fls`; on the NTFS SSD they are not recoverable at all. Same user action, two different outcomes,
  because of the medium.
`[U5 p16–17, p138–140]`

### Resident vs non-resident (NTFS)
- **Definition** — an NTFS attribute is **resident** when its content sits inside the 1024-byte `$MFT`
  record, and **non-resident** when the record holds only a runlist pointing at clusters elsewhere.
- **Why it exists** — a small file costs a whole cluster if stored outside; putting it in the record
  it already needs is free. NTFS therefore stores tiny files entirely inside the `$MFT`.
- **Where it shows up** — the non-resident flag is one byte at offset 8 of every attribute header
  (`0x01` = non-resident). `$STANDARD_INFORMATION` and `$FILE_NAME` are always resident; `$DATA` may
  be either.
- **Example** — INE's threshold is "under 700 bytes → resident, over 700 → non-resident". A 300-byte
  `.lnk` or a short script exists *only* inside the `$MFT`; imaging just the data area would lose it,
  and carving unallocated space will never find it. `[U5 p199–201, p218]`
- **In the case (D19)** — the small PowerShell downloader dropped by the malicious document is under
  the threshold, so its entire body lives in the `$MFT` and comes out of an `$MFT` parse, not out of a
  file export.
`[U5 p199–210, p218]`

### Fixup array (update sequence array)
- **Definition** — a corruption check NTFS applies to multi-sector structures: the last two bytes of
  each sector are moved into an array in the header and replaced with a single update sequence number.
- **Why it exists** — a 1024-byte record spans two 512-byte sectors. If one sector was written and the
  other was not, the record is silently half-old. Matching signatures at both sector tails detects it.
- **Where it shows up** — `FILE` records in `$MFT`, `INDX` records in directory indexes, and `RCRD` /
  `RSTR` records in `$LogFile`.
- **Example** — a hand-parse of an `$MFT` record that ignores fixups will read two bytes of garbage at
  offset 510 and again at 1022. Every real parser undoes the substitution before interpreting.
  `[U5 p181–186]`
`[U5 p181–186]`

### File carving
- **Definition** — recovering files from raw data by recognising their own structure and content,
  with no file system metadata involved at all.
- **Why it exists** — the metadata is what usually goes first: formatted device, corrupted file
  system, wiped partition table, deleted directory entry. The bytes can outlive the map.
- **Where it shows up** — run against unallocated space (`blkls` output), against a whole image, or
  against a memory dump or packet capture — carving is not disk-only.
- **Example** — header/footer carving of JPEG: find `FF D8 FF`, read forward to `FF D9`, write it out.
  It works only when the file is contiguous, unfragmented, uncompressed and its header survived.
  `[U5 p240–256]`
- **In the case (D19)** — carving the USB's unallocated space recovers the exfiltrated documents;
  carving the SSD's unallocated space recovers nothing, for the TRIM reason above.
`[U5 p240–261]`

---

## 2 · Artifacts  (R10 six-box, one table per artifact)

### Master Boot Record (MBR)

| | |
|---|---|
| **What it is** | The first sector of an MBR-scheme disk: 446 bytes of boot code, a 64-byte partition table of four 16-byte entries, and a 2-byte signature. |
| **Where it lives** | LBA 0 / CHS (0,0,1). Decimal offsets within the sector: `0–445` boot code, `446–509` partition table (`446–461` #1, `462–477` #2, `478–493` #3, `494–509` #4), `510–511` signature `0x55AA`. Each 16-byte entry: `0` boot indicator (`0x80` = active), `1–3` starting CHS, `4` partition-type descriptor, `5–7` ending CHS, `8–11` starting LBA, `12–15` size in sectors. |
| **What it proves** | That the disk was partitioned under the MBR scheme; the on-disk start offset, length and declared type of up to four primary partitions; which one was flagged bootable. It gives you the `-o` values every downstream TSK command needs. |
| **What it does NOT prove** | The type byte is a *declaration*, not a measurement — a partition marked `0x07` (NTFS) may hold FAT, ext4, an encrypted container, or nothing at all, and a partition marked `0x00` may still hold a live file system that the entry has simply been edited to hide. It does not prove the disk has only four partitions (extended/logical partitions are described elsewhere, in EBRs), does not prove the listed partitions are the only regions with data (gaps, HPA and unpartitioned space are invisible here), and does not prove the boot code was ever executed or that the system booted from this disk. A rewritten MBR carries no record of what it said before. |
| **How to parse it** | `mmls disk.dd` for the layout; `mmstat disk.dd` for the scheme; byte-level in WinHex or Active@ Disk Editor with the MBR template applied; `dd if=disk.dd bs=512 count=1 \| xxd` for the raw sector. |
| **Anti-forensics / false positive** | Zeroing sector 0 makes a disk look unformatted while every partition survives untouched — the standard "wiped partition table" scenario, recoverable with TestDisk. Conversely a *protective* MBR (single entry of type `0xEE` spanning the disk) is not a damaged MBR; it is a healthy GPT disk, and tools that "fix" it destroy evidence. Partition entries can be hand-edited to conceal a partition from Windows while leaving it perfectly readable to a forensic tool. |

`[U4 p86–104]`

### Extended Boot Record (EBR) chain

| | |
|---|---|
| **What it is** | The linked list that lets an MBR disk carry more than four partitions: one primary entry is converted to an *extended* partition, and inside it a chain of EBRs each describe one logical partition. |
| **Where it lives** | First sector of the extended partition, then one EBR at the start of each subsequent logical partition. Same 512-byte structure as an MBR, but **usually only two of the four entries are used**: entry 1 describes this logical partition, entry 2 points at the next EBR. |
| **What it proves** | The existence, order, offsets and sizes of logical partitions that the MBR's four entries cannot describe. Following the chain to its end proves you have enumerated all of them. |
| **What it does NOT prove** | The chain proves only what the *last tool to write it* recorded. A truncated chain does not prove there are no further logical partitions — the pointer can be zeroed while the partitions themselves remain intact further down the disk, so "mmls showed three" is never the same claim as "the disk has three". INE warns explicitly that partitioning tools implement extended partitions differently, so a byte layout that looks wrong may be a vendor quirk rather than tampering, and an EBR's own offsets are relative in ways that vary by tool. Nothing in an EBR proves the described region was ever formatted or used. |
| **How to parse it** | `mmls disk.dd` follows the chain automatically and labels extended and logical entries; verify by hand in a disk editor by walking each EBR's second entry until it reads all zeroes. |
| **Anti-forensics / false positive** | Breaking one link hides every logical partition after it from the OS and from naive parsers, while leaving the data intact — a cheap, effective and easily reversed hiding technique. A "free space" gap reported by `mmls` between logical partitions is often just alignment padding, not concealment; do not report it as hidden data without carving it first. |

`[U4 p94–99]`

### GPT — protective MBR, header, entry array, backups

| | |
|---|---|
| **What it is** | The GUID Partition Table scheme: a protective MBR, a header, an array of 128-byte partition entries, and a full backup of both at the end of the disk. |
| **Where it lives** | LBA 0 protective MBR (a single entry of type `0xEE` spanning the disk, or 2 TB of it); LBA 1 GPT header; LBA 2 onward the partition entry array; LBA n−1 backup entry array; LBA n (last sector) backup header. Header fields: `"EFI PART"` signature (8), revision (4), header size (4), header CRC32 (4), reserved (4), this header's LBA (8), backup header LBA (8), first usable LBA (8), last usable LBA (8), disk GUID (16), starting LBA of the entry array (8), number of entries (4), size of each entry (4), entry-array CRC32 (4), then reserved padding — 420 bytes of it on a 512-byte-sector disk. Entry layout: `0x00` partition type GUID (16), `0x10` unique partition GUID (16), `0x20` first LBA (8, little-endian), `0x28` last LBA inclusive (8), `0x30` attribute flags (8), `0x38` name (72 bytes = 36 UTF-16 characters). |
| **What it proves** | Up to 128 partitions with 64-bit LBAs, each with a *stable unique GUID* and a human-readable label; a checksummed, duplicated description of the disk layout; and — via the CRC32s — whether the primary copy has been altered since it was written. |
| **What it does NOT prove** | The type GUID is again a declaration, not a measurement: `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` means "someone wrote basic-data here", not "there is an NTFS file system here". A valid header CRC proves internal consistency only — a complete, freshly written GPT is perfectly self-consistent and says nothing about what the disk held before. The partition name field is free text set by whoever formatted the disk, so a partition labelled "Backup" proves nothing about its contents. Matching primary and backup copies does not prove the layout is original; both can be rewritten together. And the protective MBR proves nothing except that a GPT-aware tool wrote it. |
| **How to parse it** | `mmls disk.dd` (TSK understands GPT natively and prints the GUID types); disk editor with a GPT template; read the last sector for the backup header when the primary is damaged. |
| **Anti-forensics / false positive** | The single highest-value recovery move in this module: if the primary GPT is corrupt, **the backup at the end of the disk usually restores it in full** — INE stresses doing this on a working copy of the image, never the original. A disk whose protective MBR was "repaired" by a legacy tool can present as a 2 TB MBR disk while being much larger; do not conclude the disk is 2 TB from the protective entry. Attribute flags can hide a partition from the OS boot process without hiding it from a forensic parser. |

`[U4 p108–133]` — ⚠ two OCR cautions. The type GUIDs render with capital `O` where the value is zero; the three INE lists (Microsoft Reserved, Basic data, Linux filesystem data) are standard published values and are written correctly above, but verify on the page before putting them on a slide. And the header field list at `[U4 p123]` is jumbled by the OCR — every field named above does appear there, and the 420-byte trailing reserve is confirmed independently at `[U4 p125]`, but the *order and the two 4-byte entry-count/entry-size fields* are reconstructed into canonical layout rather than read cleanly off the page. Check the order before teaching a byte-offset walk.

### Host Protected Area (HPA) and Device Configuration Overlay (DCO)

| | |
|---|---|
| **What it is** | Regions at the end of an ATA drive that the drive itself reports as not existing, so the operating system never addresses them. HPA is set by the `SET_MAX_ADDRESS` family; DCO hides capacity even more thoroughly, below HPA. |
| **Where it lives** | Between the drive's reported maximum LBA and its true native maximum. Detected by comparing the answers to two ATA commands: `IDENTIFY_DEVICE` (what the drive admits to) against `READ_NATIVE_MAX_ADDRESS` (what it actually has). INE's example screen shows an ID sector max of 100 000 000, an HPA native max of 156 301 488 and a DCO max of 625 142 447 — three different "sizes" for one disk. |
| **What it proves** | That the drive's addressable capacity has been reduced below its native capacity, and by exactly how many sectors. If the hidden region contains data, it proves data exists in a region normal OS-level imaging never touches. |
| **What it does NOT prove** | An HPA is overwhelmingly likely to be *the vendor's*, not the suspect's — laptop recovery partitions, diagnostic utilities, BIOS-flash staging areas and anti-theft services all live there legitimately, so its mere presence is not evidence of concealment and must never be reported as such. It does not prove who set it or when: there is no timestamp on an HPA. It does not prove the hidden content was hidden deliberately or was ever accessed. And a *clean* comparison does not prove nothing was hidden — a DCO can have been set and removed before seizure, leaving no trace of either event. |
| **How to parse it** | `hdparm -N /dev/sda` on Linux; TSK; ATATool (Data Synergy); `dmesg` kernel messages. Commercial: EnCase, FTK, Atola Bandura, OSForensics — several offer "image HPA" and "remove HPA" separately. Detect first, image the hidden region as its own file, and document before removing anything. |
| **Anti-forensics / false positive** | INE names the abuse case directly: rootkits and illegal material stored where formatting cannot reach. Removing an HPA to image it is a **destructive change to the evidence device** — it must be authorised, documented and, where possible, done after the visible area is already imaged and hashed. Some hardware write blockers pass the ATA commands through and some do not, so "hdparm reported no HPA" may be a fact about your blocker rather than about the disk. |

`[U4 p134–141]`

### Partition gaps, unpartitioned space and volume slack

| | |
|---|---|
| **What it is** | Sectors inside the disk that no partition entry claims (inter-partition gaps, space before the first partition, space after the last), plus sectors inside a partition that lie beyond the end of the file system it holds (volume slack). |
| **Where it lives** | Anywhere `mmls` prints an `Unallocated` row, and between `fsstat`'s reported file-system size and the partition length reported by `mmls`. WinHex labels these regions explicitly as "Partition gap" and "Unpartitioned space" in its volume tree. |
| **What it proves** | That addressable sectors exist which no file system will ever show you. If they contain non-zero data, it proves the region was written at some point. |
| **What it does NOT prove** | Almost all such space is ordinary and innocent — 1 MiB alignment padding before the first partition, the tail of a disk that did not divide evenly, the remains of an earlier, larger partition scheme. Non-zero content there does not prove concealment, does not prove the current user wrote it, and very often is nothing more than an earlier install's leftovers that were never zeroed. It does not prove a "hidden partition" exists: a boot sector signature found in a gap is just as likely to be a stale artefact of a previous layout as a deliberately unlinked volume. Never report a gap as hidden data on the strength of its existence — carve it, identify what is in it, and report that instead. |
| **How to parse it** | `mmls disk.dd` and read the `Unallocated` rows; extract with `dd` using the reported offset and length, or `blkls`; then `foremost` / `photorec` / `bulk_extractor` over the extract; `sigfind` to hunt boot-sector signatures inside it. |
| **Anti-forensics / false positive** | Deliberately unlinking a partition and leaving its VBR intact is the classic hidden-partition trick and is why INE devotes a video to locating partition gaps. Equally, a disk that once held a larger partition will show a stale VBR in the gap that some tools will confidently mount as a "recovered partition" that never existed in this configuration. |

`[U4 p68, p141]` · `[U5 p275–277]`

### FAT32 boot sector (BPB + EBPB)

| | |
|---|---|
| **What it is** | The first sector of a FAT volume: the jump instruction, an OEM string, the BIOS Parameter Block describing the geometry of the file system, the Extended BPB with the volume's identity, bootstrap code, and the `0x55AA` signature. |
| **Where it lives** | Sector 0 of the partition, backed up at sector 6 in FAT32's 32-sector reserved area (sectors 0 and 6 boot sector, 1 and 7 FSINFO, 2 and 8 bootstrap). FAT32 layout: `0–2` jump, `3–10` OEM name, `11–63` BPB, `64–89` EBPB, `90–509` bootstrap, `510–511` signature. Key BPB fields at decimal offsets: `11` bytes/sector, `13` sectors/cluster, `14` reserved sector count, `16` number of FATs, `21` media type, `24` sectors/track, `26` heads, `28` hidden sectors, `32` total sectors (32-bit), `36` sectors per FAT (32-bit), `40` extended flags, `44` first cluster of root directory, `48` FSINFO sector, `50` backup boot sector. ⚠ the offset column in the OCR is damaged; the field *order* above is reliable, the numeric offsets should be checked on the page. |
| **What it proves** | Everything you need to compute where anything else is: cluster size, where FAT#1 starts (reserved sector count), where FAT#2 starts (reserved + sectors-per-FAT), where the data area starts (reserved + 2 × sectors-per-FAT), and where the root directory is (cluster 2). Plus the volume serial number and label. |
| **What it does NOT prove** | The OEM name and the file system ID string are *cosmetic* — INE's sample reads `MSDOS5.0` and `FAT32`, but these are free-form bytes written by whatever formatted the volume and are trivially editable; they do not prove which OS or utility created the volume. The volume serial number is derived from the format timestamp and is not unique, not tamper-evident, and not a device identifier — two volumes can share one. "Hidden sectors = 128" tells you where the partition starts *according to the format tool*, which can disagree with the actual partition table. And a valid boot sector does not prove the volume is bootable or was ever booted. |
| **How to parse it** | `fsstat image.dd -o <offset>` prints the whole thing decoded; disk editor with a FAT32 boot sector template; compare sector 0 against the backup at sector 6 — a mismatch is itself a finding. |
| **Anti-forensics / false positive** | If sector 0 is destroyed, the backup at sector 6 rebuilds the volume — TestDisk does this automatically. A volume label of `NO NAME` in the boot sector alongside a different label in the root directory (INE's sample shows boot-sector `NO NAME`, root-directory `SUSPECT1`) is normal, not tampering: Windows stores the working label in the root directory entry and often never updates the boot sector copy. |

`[U5 p56–84]`

### FSINFO sector (FAT32)

| | |
|---|---|
| **What it is** | A FAT32-only performance hint sector holding a cached free-cluster count and a "next free cluster" pointer, so the OS does not have to scan the whole FAT to answer "how much space is left". |
| **Where it lives** | Sector 1 of the reserved area (backed up at sector 7); its location is named at BPB offset 48. Layout: `0–3` signature, `4–483` reserved, `484–487` second signature, `488–491` free cluster count, `492–495` next free cluster, `496–507` reserved, `508–511` `0xAA550000`. ⚠ the OCR table skips the `488–491` row; the field is confirmed by INE's own worked example, which reads a free-cluster value there. |
| **What it proves** | The volume's cached idea of free space at the moment the file system was last cleanly updated. INE's worked example: `0x155C0100` little-endian → `0x00015C15` → 89 109 free clusters × 2 sectors/cluster = 178 218 sectors × 512 = 91 247 616 bytes. |
| **What it does NOT prove** | It is explicitly a **hint, not an authority** — the specification permits it to be stale and file systems are allowed to ignore it. A free-cluster count that disagrees with a count derived from the FAT itself does not prove data was hidden or that the volume was tampered with; it usually just proves the volume was dismounted uncleanly. It says nothing about *which* clusters are free, nothing about deleted content, and cannot be used to argue a capacity discrepancy on its own. Any claim about "missing space" must be reconstructed from the FAT, not from FSINFO. |
| **How to parse it** | Disk editor at reserved-area sector 1; `fsstat` reports the derived free sector count as `Free Sector Count (FS Info)` — note that TSK labels the provenance, which is a good habit to point out to students. |
| **Anti-forensics / false positive** | The number is trivially editable and nothing validates it, so it is a poor basis for any conclusion. INE's reason for teaching the arithmetic is exactly right though: doing it by hand and comparing against the partition size is how you first notice that a volume is smaller than the space it claims to occupy. |

`[U5 p85–92]`

### The File Allocation Table itself

| | |
|---|---|
| **What it is** | An array with one entry per cluster in the data area, doubling as a free-space bitmap and as the linked list that chains a file's clusters together. |
| **Where it lives** | Immediately after the reserved area; FAT32 keeps two copies (FAT#1 then FAT#2), each `sectors-per-FAT` long. FAT32 entry values: `0x?0000000` free; `0x?0000001` reserved; `0x?0000002`–`0x?FFFFFEF` in use, value = next cluster; `0x?FFFFFF0`–`0x?FFFFFF6` reserved; `0x?FFFFFF7` bad cluster; `0x?FFFFFF8`–`0x?FFFFFFF` end of chain. The top 4 bits are unused — FAT32 addresses with 28 bits. Cluster 0 holds the media descriptor plus `FF FF FF` (`0xF8FFFFFF` on a hard disk); cluster 1 carries the dirty-volume flag. |
| **What it proves** | For every live file, the complete, ordered list of clusters holding its content — including out-of-order and fragmented layouts. For the volume as a whole, exactly which clusters are claimed and which are free. A `0xF7` entry proves the file system was told that cluster is bad. |
| **What it does NOT prove** | A cluster marked free does not prove it is empty — that is the whole basis of recovery. Conversely a cluster marked in-use does not prove the file that claims it is intact. Critically, **the FAT retains no history**: when a file is deleted its chain entries are zeroed, so the FAT can never tell you what a now-free cluster used to belong to, and it cannot be used to reassemble a fragmented deleted file. A `0xF7` bad-cluster mark does not prove the media is failing — marking good clusters bad is a documented data-hiding technique — and a clean FAT does not prove no deletions occurred. Two FAT copies agreeing proves only that the OS updated both, not that either is correct. |
| **How to parse it** | `fsstat` prints the FAT contents in sectors with chain ends (`32776-32783 (8) -> EOF`); `istat` shows a file's sector list; by hand, from the boot sector: FAT#1 = reserved sector count, FAT#2 = reserved + sectors-per-FAT. |
| **Anti-forensics / false positive** | FAT#1 and FAT#2 diverging is a genuine anomaly worth reporting — but the far more common cause is an unclean dismount, not tampering, so check cluster 1's dirty flag before making a claim. |

`[U5 p95–110]`

### FAT32 directory entry — Short File Name and Long File Name

| | |
|---|---|
| **What it is** | The 32-byte record that gives a file its name, attributes, timestamps, starting cluster and size. Names longer than 8.3 get additional 32-byte LFN records stacked *before* the SFN in the directory. |
| **Where it lives** | Inside the data area — a directory is just a file whose content is an array of these records; the root directory starts at cluster 2. **SFN**: `0` first name char / status byte, `1–7` name, `8–10` extension, `11` attributes, `13` create-time tenths, `14` create time, `16` create date, `18` last-access date, `20` first cluster high word, `22` last-modified time, `24` last-modified date, `26` first cluster low word, `28` size (4 bytes → 4 GB ceiling). Status byte: `0xE5` deleted, `0x00` never used, `0x05` the name genuinely starts with `0xE5`. Attributes: `0x01` read-only, `0x02` hidden, `0x04` system, `0x08` volume label, `0x0F` LFN, `0x10` directory, `0x20` archive. **LFN**: `0` sequence (`0x01`, `0x02`… with the final entry ORed with `0x40`), `1–10` name chars 1–5, `11` attributes (`0x0F`), `12` reserved, `13` checksum of the SFN 8.3 name, `14–25` chars 6–11, `26–27` reserved, `28–31` chars 12–13; 13 UTF-16 characters per entry, tail padded with `0xFF`. |
| **What it proves** | The name a user saw, four timestamps, the file's size, its attribute flags, and the number of its **first** cluster. For a deleted file it still proves all of that, because deletion changes only the first byte of the name. |
| **What it does NOT prove** | FAT timestamps are the weakest in the course and students consistently over-read them: they are **local time with no time-zone record**, last-write is stored to 2-second granularity, and last-access is a *date only* with no time at all — so "accessed 18 Aug 2017" is a date bucket, not an event, and comparing a FAT time to an NTFS UTC time without converting is a reporting error. For a deleted entry, the surviving first-cluster number proves only where the file *began*; the chain is gone, so recovering more than the first cluster is an assumption of contiguity, not a finding — and if the file was fragmented, "recovered" content beyond the first fragment may belong to an entirely different file. A `0xE5` byte does not prove *when* the deletion happened. An 8.3 alias like `ELEARN~1.DOC` does not prove the long name; the mapping is only guaranteed while both records survive together. |
| **How to parse it** | `fls -l image.dd -o <offset>` lists entries with type, metadata address, name and all four timestamps (deleted entries prefixed `*`); `istat` for one entry; `ffind -d` to resolve deleted entries only; disk editor at the directory's cluster for the raw bytes. |
| **Anti-forensics / false positive** | The tilde number after the first six characters depends on collision order within the directory, so `~1` does not mean "first created". A file whose name legitimately begins with `0xE5` is stored as `0x05` — a parser that does not handle this reports a live file as deleted. Directory entries can be hand-edited: attributes, timestamps and the starting cluster are all writable with a disk editor and none of it is checksummed. |

`[U5 p111–133, p138–140]` — ⚠ the OCR renders the date and time bit-field widths as "bytes" (`7 bytes 4 bytes 5 bytes`); they are **bits** — date = 7 bits year from 1980, 4 bits month, 5 bits day; time = 5 bits hour, 6 bits minute, 5 bits two-second units. Verify on the page.

### NTFS Volume Boot Record (`$Boot`)

| | |
|---|---|
| **What it is** | The NTFS boot sector, which is simultaneously a file — `$Boot`, `$MFT` record number 7 — and the only structure on an NTFS volume that lives at a fixed location. |
| **Where it lives** | Sector 0 of the partition (and mirrored at the volume's last sector). Its size in sectors follows the cluster size — an 8-sector VBR on a 4 KB-cluster volume. Fields: `3` OEM ID (`NTFS    `), `11` bytes per sector, `13` sectors per cluster, `14` reserved sectors (**always 0** on NTFS, because the boot sector is at the volume start), `21` media descriptor (`0xF8` for a hard disk), `40` total sectors, **`48` logical cluster number of `$MFT`**, `56` logical cluster number of `$MFTMirr`, then clusters-per-MFT-record, clusters-per-index-buffer and the volume serial number. Several fields at offsets 16, 20 and 22 must be zero or NTFS refuses to mount the volume. |
| **What it proves** | Where `$MFT` starts. That is the entire reason to read it: `$MFT` can be anywhere on the volume, and this is the only pointer to it. It also proves cluster size, so every LCN in every runlist can be converted to a byte offset. |
| **What it does NOT prove** | An intact VBR does not prove the volume is intact — `$MFT` can be destroyed while `$Boot` is pristine. The OEM ID `NTFS` is a plain byte string, so its presence does not prove a valid NTFS file system and its absence does not prove there is none (the mirror at the last sector may still be good). The volume serial number is not a hardware identifier and changes on every reformat, so it cannot be used to say "this is the same disk"; at most it says "this is the same *formatting event*". Reserved-sector fields being zero is a mount requirement, not evidence of anything. |
| **How to parse it** | `fsstat image.dd -o <offset>`; disk editor with an NTFS boot sector template; recover from the mirror in the volume's last sector, or with TestDisk's "rebuild NTFS boot sector". |
| **Anti-forensics / false positive** | Because `$MFT`'s location is only recorded here, zeroing the VBR is a cheap way to make a volume unmountable — and one of the more satisfying recoveries to demo, since the mirror or a TestDisk rebuild brings it straight back. Do not mistake a volume whose VBR points at an `$MFT` that has been overwritten for a volume with a damaged VBR; check the `FILE` signature at the target offset. |

`[U5 p160–172]`

### `$MFT` record

| | |
|---|---|
| **What it is** | The Master File Table: one record per file and per directory on the volume, including a record describing `$MFT` itself. Each record is a header plus a sequence of variable-length attributes and an `0xFFFFFFFF` end marker. **This is the single most important artifact in the course.** |
| **Where it lives** | `$MFT` is record 0, at the LCN named in `$Boot` offset 48; records are normally 1024 bytes each. NTFS reserves ~12.5 % of the volume as the *MFT Zone* to keep it contiguous. Records 0–15 are the metadata files: `$MFT` 0, `$MFTMirr` 1, `$LogFile` 2, `$Volume` 3, `$AttrDef` 4, `.` (root directory) 5, `$Bitmap` 6, `$Boot` 7, `$BadClus` 8, `$Secure` 9, `$UpCase` 10, `$Extend` 11, 12–15 reserved. `$ObjId`, `$Quota`, `$Reparse` and `$UsnJrnl` live under `$Extend`. Header fields: `0` signature `FILE` (`0x46494C45`, or `BAAD` if unusable), `4` offset to fixup array, `6` fixup entry count, `8` `$LogFile` sequence number (LSN), `16` sequence number, `18` hard link count, `20` offset to first attribute, `22` flags, `24` real size of record, `28` allocated size (usually 1024), `32` file reference to base record, `40` next attribute ID, then the record's own number. |
| **What it proves** | That a file with a given name, size, timestamps, parent directory and cluster layout existed on this volume. It proves this **whether or not the file's content still exists** — which is why it is the backbone of the S6 timeline. The sequence number proves how many times that record slot has been reused. A non-zero base-record reference proves the record is an extension of another. And because `$MFT` has a record for every metadata file, it proves the core lesson for S5: **a registry hive is a file with an `$MFT` record like any other file**. |
| **What it does NOT prove** | An `$MFT` record does **not** prove the file's content is still on the disk — on a TRIMmed SSD the record can be perfectly readable while its clusters return zeroes, and this is the most common wrong inference in the whole module. A record marked not-in-use does not prove *when* the file was deleted; the record carries no deletion timestamp. Timestamps in the record are what the file system was *told*, not what physically happened — they are writable through documented API calls and by any timestomping tool, so a creation time is a claim, not an observation. The record does not prove a human created the file, does not prove it was ever opened, and does not prove the named user account was the one at the keyboard. Finally, a record that has been reused proves that the *slot* was reused; whatever names or data still visible inside it may belong to a different, older file entirely. |
| **How to parse it** | Extract `$MFT` with TSK (`icat image.dd -o <offset> 0 > MFT.raw`) or from a mounted image, then `MFTECmd.exe -f MFT.raw --csv . --csvf mft.csv` and open the CSV in **Timeline Explorer** to sort and filter. TSK direct: `fls -r -m C: image.dd -o <offset> > body.txt` then `mactime -b body.txt`. `istat image.dd -o <offset> <entry>` for one record's attributes and cluster runs. ⚠ MFTECmd and Timeline Explorer are **not in INE units 4 or 5** — see §7. |
| **Anti-forensics / false positive** | Timestomping targets `$STANDARD_INFORMATION` first because that is what Explorer shows; comparing it against `$FILE_NAME` in the same record is the standard detection (see below). `$MFT` records for small files hold the entire file content resident, so an "empty" unallocated space does not mean nothing was there. Deliberately fragmenting `$MFT` past the MFT Zone, or overwriting `$MFT` with a crafted file, are known destructive techniques — a `BAAD` signature means the OS itself flagged the record unusable, which is worth reporting but is far more often disk corruption than an attack. |

`[U5 p154–197]` — ⚠ the OCR's header-flag table starts at `0x02` (directory) and lists `0x04`/`0x08` as "Unknown"; the `0x01` row — **record in use**, the bit that deletion clears — is missing from the machine read. Verify on the page before teaching the flag byte. Also: `[U5 p180]` says a record "is around 48 bytes", which is the *header* size, not the record size (1024 bytes); do not repeat the slide's phrasing.

### `$STANDARD_INFORMATION` (attribute `0x10`)

| | |
|---|---|
| **What it is** | The always-resident attribute holding a file's four canonical timestamps, its DOS-style attribute flags, its owner and security IDs, and its last USN. |
| **Where it lives** | Inside the `$MFT` record; 48 bytes minimum, 72 maximum. Offsets within the attribute content: `0x00` created, `0x08` modified, `0x10` MFT entry changed, `0x18` accessed (all 8-byte FILETIME, 100 ns since 1601, UTC), `0x20` flags, `0x24` max versions, `0x28` version, `0x2C` class ID, `0x30` owner ID, `0x34` security ID (an index into `$Secure`, **not** a Windows SID), `0x40` update sequence number (an index into `$UsnJrnl`). Flags include `0x0002` hidden, `0x0004` system, `0x0020` archive, `0x0200` sparse, `0x0400` reparse point, `0x0800` compressed, `0x2000` not content indexed, `0x4000` encrypted. |
| **What it proves** | The MACB set that Windows Explorer, `dir` and almost every forensic tool display by default, in UTC. The `0x10` MFT-changed timestamp proves when the *record* was last modified, which is a different event from the file being written. |
| **What it does NOT prove** | These four values are the **easiest timestamps on Windows to forge** — `SetFileTime` is a documented API and every timestomping tool writes here. A creation time therefore proves what was written into the field, not when the file came into existence, and must never be reported as "the file was created at". Last-accessed is worse than unreliable: Windows has disabled last-access updates by default since Vista, so an access time that equals the creation time proves the feature was off, not that the file was never opened. The security ID is an index into `$Secure` and is *not* a SID — reading it as a user account is a common and serious error. And none of these timestamps identify a person; they are file-system events, not user actions. |
| **How to parse it** | `MFTECmd` puts all four in the CSV as `Created0x10`, `LastModified0x10`, `LastRecordChange0x10`, `LastAccess0x10`; `istat` prints them per record; TSK `fls -m` / `mactime` builds them into a body file for S6. |
| **Anti-forensics / false positive** | Comparing `0x10` against `0x30` (`$FILE_NAME`) in the same record is the standard timestomp check, because most tools rewrite only `0x10`. But a `0x10` earlier than `0x30` is *not* proof of tampering on its own — file copies, archive extraction, installers and restores all produce that pattern legitimately, so the finding is "an inconsistency exists", and the interpretation must be argued separately. Sub-second precision that is exactly zero across all four values is a stronger indicator than ordering alone. |

`[U5 p212–215]`

### `$FILE_NAME` (attribute `0x30`)

| | |
|---|---|
| **What it is** | The resident attribute holding the file's name, its parent directory's file reference, its own second set of four timestamps, and its allocated and real sizes. A file has one per namespace — typically both a long name and an 8.3 alias. |
| **Where it lives** | Inside the `$MFT` record. `0x00` parent directory file reference (8 bytes: 6-byte entry number + 2-byte sequence number), `0x08` created, `0x10` modified, `0x18` MFT modified, `0x20` accessed, `0x28` allocated size, `0x30` real size, `0x38` flags, `0x3C` reparse value, `0x40` name length, `0x41` namespace, `0x42`+ the name in UTF-16. |
| **What it proves** | The file's name and — via the parent reference — its full path, which is how a flat `$MFT` becomes a directory tree. Its four timestamps are the ones Windows Explorer never shows, so they are the comparison set for detecting timestomping. |
| **What it does NOT prove** | `$FILE_NAME` timestamps are **not** immune to forgery — they are harder to reach from user mode, but they are not a trusted clock, and reporting them as ground truth overstates the case. They record when the *name record* was last touched, which changes on rename and on move, so a `0x30` creation time can legitimately be later than the file's real creation. A parent reference proves the directory record the name pointed to at the time; if that record has since been reused for a different directory, resolving the path today gives a wrong answer, which is exactly what the parent's sequence number exists to detect. Multiple `$FILE_NAME` attributes on one record prove namespaces, not multiple files. And a name proves nothing about content — extension and content are unrelated on NTFS. |
| **How to parse it** | `MFTECmd` emits the `0x30` timestamps as separate columns (`Created0x30`, …) precisely so they can be compared against `0x10` in Timeline Explorer; `istat` prints them; `ffind` resolves an entry number back to a path. |
| **Anti-forensics / false positive** | A record whose parent reference points at a reused directory record produces a confidently wrong path — always check that the parent's sequence number matches. Long-name/short-name pairs mean one file, not two; a naive parser double-counts them and inflates file counts in a report. |

`[U5 p216–217]`

### `$DATA` (attribute `0x80`) — resident, non-resident and runlists

| | |
|---|---|
| **What it is** | The attribute that holds the file's actual content, either inline in the record or as a list of cluster runs pointing elsewhere on the volume. |
| **Where it lives** | Inside the `$MFT` record when resident. When non-resident, the attribute header carries: `16` starting VCN, `24` ending VCN, `32` offset to the runlist, `34` compression unit size, `40` allocated size, `48` real size, `56` initialised data size, `64`+ the data runs. A run is a starting cluster plus a length; **VCN** is the cluster's sequence number within the file, **LCN** is its number on the volume counted from the first cluster after the VBR. Runs need not ascend — out-of-order runs are the normal signature of a file written into space freed by an earlier file. |
| **What it proves** | For a resident file, the content itself, in full, inside the `$MFT`. For a non-resident file, the exact ordered cluster list — which means the exact byte offsets in the image, which means you can extract it, hash it, and prove fragmentation. `initialised data size` below `real size` proves the tail of the allocated space was never written by this file. |
| **What it does NOT prove** | A runlist proves where the content *was placed*, not that it is still there — the clusters may since have been reallocated to another file, and on a TRIMmed SSD they may have been physically erased while the runlist remains perfectly intact. Extracting a runlist's clusters therefore does not prove you have recovered the original file, and the extracted bytes must be validated (signature, hash, does it open) before being reported as the file. `real size` is what the metadata claims; it does not prove that many bytes of valid content exist. And for a deleted file, the runlist may still be present in the record — which makes recovery easy but does *not* mean the file system still considers those clusters yours. |
| **How to parse it** | `icat image.dd -o <offset> <entry>` extracts by entry number; `istat` prints the runs as sector ranges; `blkcat` reads a run directly; `MFTECmd` reports resident content and run information in its output. INE devotes a video to walking data runs by hand — worth doing once. |
| **Anti-forensics / false positive** | Sparse and compressed files have runlists that include holes and compressed units; reading them as plain runs produces garbage that looks like carved data. A resident file leaves *no trace whatsoever in unallocated space*, so "we carved the disk and found nothing" is not evidence that a small file never existed. |

`[U5 p199–211, p218]` — INE's 700-byte resident/non-resident threshold `[U5 p201]` is a teaching simplification; see §7.

### Alternate Data Stream (a second, named `$DATA`)

| | |
|---|---|
| **What it is** | NTFS permits more than one `$DATA` attribute per file. The unnamed one is what you see; any named one is an alternate data stream, invisible to Explorer, to `dir` without `/R`, and to file size reporting. |
| **Where it lives** | In the same `$MFT` record as the host file (or in an extension record). Addressed as `filename:streamname`. INE's demonstration: `echo "DFP Course" > course.txt` then `echo "Hidden Data" > course.txt:file.txt` creates a second `$DATA`; read it back with `notepad course.txt:file.txt` while `more course.txt` shows only the original content. |
| **What it proves** | That data exists which the file's apparent size and the ordinary directory listing do not account for. The stream's name and content are both recoverable. `Zone.Identifier` streams in particular prove a file arrived through a mechanism that applied Mark-of-the-Web. |
| **What it does NOT prove** | Most ADS on a real system are entirely benign and system-generated — `Zone.Identifier` on every download, `SmartScreen` data, thumbnail and property streams — so finding an ADS does **not** prove concealment and reporting it as "hidden data" without identifying it is a rubric failure. An ADS does not prove the host file's owner created it; the stream is attached to the file and travels with copies to NTFS destinations. A stream's content proves nothing about whether it was ever executed or read. And the absence of ADS proves nothing: copying a file to FAT, exFAT, a ZIP, or across most network shares silently strips every stream, so "no ADS present" may be an artefact of how the file reached you. |
| **How to parse it** | `dir /R` on a live system; `Get-Item -Stream *` in PowerShell; `streams.exe` (Sysinternals); in an image, an `$MFT` parse lists every `$DATA` attribute with its name — `MFTECmd` reports ADS explicitly. ⚠ only the `echo`/`notepad`/`more` commands above come from INE; the rest are outside the source. |
| **Anti-forensics / false positive** | ADS is a genuine hiding technique and INE flags it as such, but the far more common examiner error is the opposite one — treating routine `Zone.Identifier` streams as suspicious. Establish the baseline first. Note also that an executable can be *run* from a stream on older Windows, so an ADS is not necessarily inert data. |

`[U5 p219–221]`

### `$LogFile`

| | |
|---|---|
| **What it is** | NTFS's transaction log: a circular record of metadata changes, written before the changes are committed, so that an interrupted operation can be rolled back or replayed at mount. |
| **Where it lives** | `$MFT` record 2, at the volume root. Its records use the `RCRD` and `RSTR` signatures and, like `$MFT` records, carry fixup arrays. Each `$MFT` record header stores the LSN of the last `$LogFile` entry that touched it (offset 8). |
| **What it proves** | The *sequence and nature* of metadata operations — file created, renamed, deleted, attribute changed — often including old and new values, at a resolution finer than any timestamp field, and for operations whose `$MFT` records have since been reused. It is the closest thing NTFS has to an audit trail of the file system itself. |
| **What it does NOT prove** | `$LogFile` is **circular and small** (commonly 64 MB), so it holds hours to a few days on a busy volume — its absence of an event proves nothing at all, only that the log has wrapped. It logs *metadata*, not content, so it cannot tell you what was written into a file. It records file-system operations, not user intent or user identity: a deletion in the log does not name a human. And because entries can be partially overwritten by the wrap, a parsed record may be internally inconsistent — a half-record is not evidence of tampering. |
| **How to parse it** | Extract with `icat image.dd -o <offset> 2 > LogFile.bin`, then a dedicated parser (`LogFileParser`, `NTFS Log Tracker`) — ⚠ **no `$LogFile` parser is named anywhere in INE units 4 or 5**; verify the current tool before the session. TSK's `jls` / `jcat` handle file-system journals generically but NTFS support is limited. |
| **Anti-forensics / false positive** | Wrapping is the dominant effect and it looks like deliberate log destruction to a student. Filling a volume with churn to force a wrap is a real anti-forensic technique, but so is a normal Windows Update. Report "no entry found within the log's retained window", never "no such event occurred". |

`[U5 p151, p157, p186]` — INE names `$LogFile` as record 2, describes journaling in one paragraph, and notes that its `RCRD`/`RSTR` records use fixups. It teaches no structure and no parsing. Everything above beyond those three facts is outside the source — see §7.

### `$UsnJrnl` (`$Extend\$UsnJrnl:$J`)

| | |
|---|---|
| **What it is** | The Update Sequence Number journal: a per-volume change log recording, for each change, the affected file's reference number, its name, its parent reference, a timestamp and a reason code (created, data overwrite, rename old/new name, delete, security change, close). |
| **Where it lives** | Under `$Extend`, as an ADS: `$Extend\$UsnJrnl:$J` holds the records, `:$Max` holds the size configuration. `$J` is a sparse file — the front of it reads as zeroes. The last USN written for a file is stored in that file's `$STANDARD_INFORMATION` at offset `0x40`. |
| **What it proves** | That a named file was created, renamed, written to or deleted, with a timestamp, **even when the file and its `$MFT` record are long gone**. For the D19 arc it is the artifact that survives collection-and-staging cleanup: the archive was created, grew, and was deleted, each with a time, each with a name. |
| **What it does NOT prove** | The journal is capped and rolls, so — exactly as with `$LogFile` — absence proves nothing but the window. A reason code of `FileDelete` proves the file-system operation, **not** that a person chose to delete it: installers, updaters, antivirus and the applications themselves delete constantly. It records names and references, **never content**, so it cannot show what was in a file. It records no user account and no process, so attributing a change to a person requires other artifacts entirely. And a `DataOverwrite` reason does not distinguish a one-byte edit from a complete rewrite. |
| **How to parse it** | `MFTECmd.exe -f "$J" --csv . --csvf usn.csv`, then Timeline Explorer; resolve parent references against the `$MFT` CSV to rebuild full paths. ⚠ **not in INE units 4 or 5** — see §7. |
| **Anti-forensics / false positive** | The journal can be deleted or resized by an administrator (`fsutil usn deletejournal`), and its deletion is itself a finding. A sparse `$J` whose first megabytes read as zeroes is *normal*, not evidence of wiping. Because entries reference file numbers, a reused `$MFT` slot can make an old journal entry resolve to a completely unrelated modern file — always check sequence numbers. |

`[U5 p174, p214]` — INE names `$UsnJrnl` twice: once in the metadata-file table as "journaling for files and directory information", once as the target of the USN field in `$STANDARD_INFORMATION`. Nothing else. Everything above is outside the source — see §7.

### Slack space (file slack, RAM slack, MFT slack)

| | |
|---|---|
| **What it is** | Content from a previous file, surviving inside space the file system currently regards as allocated to a *different*, live file. |
| **Where it lives** | **File slack**: the sectors of a file's last cluster beyond the last sector it wrote. **RAM slack**: the bytes between end-of-file and end-of-that-last-written-sector. **MFT slack**: the tail of an `$MFT` record whose resident `$DATA` grew and moved out. Any structure that is not filled to the end of its storage location is a candidate. |
| **What it proves** | That the recovered bytes were physically present on this medium and were written before the current occupant. INE's worked example yields 3072 bytes of a deleted 8 KB file surviving inside the allocated space of the 5 KB file that replaced it. |
| **What it does NOT prove** | Slack content has **no metadata at all** — no name, no timestamp, no owner, no path — so it proves the bytes existed, never when they were written, who wrote them, or what file they came from. A recovered fragment cannot be attributed to a specific deleted file without independent corroboration, and stating that it "came from" a named file is an interpretation, not a finding. It does not prove the current file's user ever saw the fragment; they almost certainly did not. A fragment that spans the slack boundary may be two unrelated files' bytes read as one. And because slack has no order, two fragments recovered from the same volume cannot be assumed to be from the same original file. |
| **How to parse it** | `blkls image.dd -o <offset> -s` extracts slack specifically (`blkls` without flags gives unallocated); grep or `bulk_extractor` the extract for strings; `blkcalc` maps a hit in the extract back to a cluster in the original image — that mapping is what makes a slack finding reportable. |
| **Anti-forensics / false positive** | INE's own note that RAM slack "is no longer found in modern operating systems" is right in effect: modern Windows pads the tail of the last sector rather than leaking memory, so do not teach RAM slack as a live memory-disclosure source. Wiping tools that overwrite file content often do **not** touch slack, which is why slack survives "secure delete"; conversely, defragmentation moves files and destroys slack wholesale with no malicious intent at all. |

`[U5 p225–239]`

### Carved file (from unallocated space)

| | |
|---|---|
| **What it is** | A file reconstructed from raw bytes by signature and structure alone, with no file system metadata involved. |
| **Where it lives** | Wherever the bytes are: unallocated clusters, slack, a partition gap, an unpartitioned region, a memory dump, a packet capture. |
| **What it proves** | That a byte sequence matching a known file format is physically present on the medium, at a specific offset. If the carved file opens and renders, it proves that content existed on the disk. |
| **What it does NOT prove** | A carved file arrives with **no name, no path, no timestamps and no owner** — every one of those is gone with the metadata, so a carved image can never be reported as "the file the user downloaded on the 3rd" without an independent source for the name and date. It does not prove the file was ever deliberately saved: browser and application caches, thumbnails, print spools and installers write files the user never chose. It does not prove the file was complete — carving assumes contiguity, and INE is explicit that once clusters are not stacked in order, carving mistakes will happen, so a carved file may silently contain another file's data in the middle. Two carved copies do not prove two files existed; one file plus one cache copy is likelier. And the absence of carving results proves nothing on a TRIMmed SSD, where the bytes are gone rather than hidden. |
| **How to parse it** | `blkls image.dd -o <offset> > unalloc.blks` then `foremost -t all -i unalloc.blks -o out/` or `photorec` interactively; Autopsy runs PhotoRec against unallocated space as a built-in ingest module; `bulk_extractor` for features (emails, URLs, card numbers) rather than whole files; `blkcalc` to map any hit back to its cluster in the source image. ⚠ INE names foremost, scalpel, PhotoRec and bulk_extractor but gives **no command lines** for any of them — verify flags against current tool documentation. |
| **Anti-forensics / false positive** | INE's own list of carving weaknesses is the honest one to teach: it is slow, it produces many invalid and partial results, it emits more data than went in, and by default it does not tell you where anything came from. Header-only carving with a maximum-size cutoff produces confident-looking files that are mostly unrelated bytes. Always record and report the source offset of a carved file — that is the only thing tying it to the evidence. |

`[U5 p240–261, p296–297, p308, p311–313]`

---

## 3 · Tools

> **Provenance of the command lines below.** INE demonstrates only these: `mmls disk.dd`,
> `mmcat Disk.dd 2 > Parition-FAT32.dd`, `mmstat Disk.dd`, `fsstat Disk.dd -o 2048`,
> `fls SUSPECT-USBv3-FAT32.dd`, `ffind SUSPECT-USBv3.dd -o 2048 21`,
> `istat SUSPECT-USBv3.dd -o 2048 21`, `ifind SUSPECT-USBv3.dd -o 2048 -n _EPORT.CSV`,
> `blkls SUSPECT-USBv3.dd -o 2048 > SUSPECT-USBv3.blks`, `fiwalk SUSPECT-USBv3.dd -X files.xml`,
> `hdparm -N /dev/sda`, and the ADS `echo` / `more` / `notepad` sequence. It names the `-f`, `-o`,
> `-l`, `-m`, `-a`, `-d`, `-u` and `-n` options. **Every other flag and invocation in this table is
> ours, not INE's** — verify each against current tool documentation before demoing it.

| Tool | What it is for | Command / entry point | Output | Caveat |
|---|---|---|---|---|
| `mmls` (TSK) | Media-management layer: read the partition scheme and layout | `mmls disk.dd` | Table of slot, start, end, length, description; includes unallocated rows and extended/logical entries | Understands MBR and GPT; the `Start` column is the `-o` value for every other TSK command |
| `mmcat` (TSK) | Extract one partition out of a whole-disk image | `mmcat Disk.dd 2 > Partition-FAT32.dd` | Raw partition image | Slot number comes from `mmls`; INE's slide spells the output file `Parition-FAT32.dd` — a typo in the source |
| `mmstat` (TSK) | Report the partition map type only | `mmstat Disk.dd` | Scheme name | Same information `mmls` already gives |
| `fsstat` (TSK) | File-system layer: decode the boot sector / VBR and layout | `fsstat Disk.dd -o 2048` | FS type, OEM name, volume ID and label, sector and cluster size, free sector count, FAT contents / MFT layout | **Must** be pointed at a partition, not a whole disk — the commonest first-run failure |
| `fls` (TSK) | File-name layer: list names, types, metadata addresses, deleted entries | `fls -r -l image.dd -o 2048` · `fls -r -m C: image.dd -o 2048 > body.txt` | Name listing; `*` marks deleted; `-m` emits a body file for timelines | The body-file output is the direct input to S6's super-timeline |
| `ffind` (TSK) | Resolve a metadata address back to a path | `ffind image.dd -o 2048 21` | `/report.csv` | `-a` all occurrences, `-d` deleted only, `-u` undeleted only |
| `istat` (TSK) | Metadata layer: everything about one record | `istat image.dd -o 2048 21` | Allocation state, attributes, size, name, MAC times, allocated sectors | On NTFS prints each attribute and its runs — the quickest way to show resident vs non-resident |
| `icat` (TSK) | Extract a file by metadata address | `icat image.dd -o 2048 0 > MFT.raw` | File content to stdout | Entry `0` is `$MFT`, entry `2` is `$LogFile` — this is how you get them out of an image |
| `ifind` (TSK) | Find the metadata address for a name | `ifind image.dd -o 2048 -n _EPORT.CSV` | Entry number | Useful when you have a name from a report and need the record |
| `ils` (TSK) | List metadata entries, including unallocated ones | `ils image.dd -o 2048` | Entry list with times and state | Surfaces records with no directory entry pointing at them |
| `blkls` (TSK) | Data-unit layer: extract unallocated space (or slack) | `blkls image.dd -o 2048 > image.blks` | Concatenated data units | Feed the output to a carver; `-s` for slack rather than unallocated |
| `blkcalc` (TSK) | Map an offset in `blkls` output back to the original image | `blkcalc image.dd -o 2048 -u <unit>` | Original data-unit number | The step that makes a carved or grepped hit reportable; INE spells it `blkalc` once `[U5 p271]` and `blkcalc` once `[U5 p296]` — `blkcalc` is correct |
| `blkcat` / `blkstat` (TSK) | Display a data unit / its statistics | `blkcat image.dd -o 2048 <unit>` | Raw bytes / allocation state | Verifying a runlist by hand |
| `mactime` (TSK) | Turn a body file into a chronological timeline | `mactime -b body.txt -d > timeline.csv` | Sorted MACB timeline | The bridge from this module into S6 |
| `sigfind` (TSK) | Hunt a byte signature at sector boundaries | `sigfind -t ntfs image.dd` | List of matching offsets | How you find a stray VBR in a partition gap |
| Autopsy | GUI over TSK; end-to-end triage | Add Data Source → image | Directory tree, hash filtering, timeline, keyword search, web artifacts, PhotoRec carving, EXIF, STIX IoC scan | v4 on Windows; v2 (HTML) is dead — do not use the interface in INE's older screenshots |
| WinHex (X-Ways) | Disk editor with a forensic volume tree | GUI | Sector view, templates, partition gap / unpartitioned space labelled explicitly | INE's primary hex tool; commercial |
| Active@ Disk Editor | Disk editor: navigate by offset, sector or file-system entry | GUI | Templates and compare view, bookmarks, Unicode search | INE's other recommendation; integrates with Active@ Undelete |
| HxD | General hex editor | GUI | Hex view, checksums | INE notes it had not been updated for some time; fine for bytes, weak on volumes |
| TestDisk | Partition table and boot sector recovery | `testdisk image.dd` | Rebuilt partition table; recovered FAT32/NTFS boot sectors; undelete | Also fixes FAT tables and rebuilds `$MFT` from `$MFTMirr`; the tool for the wiped-partition-table lab |
| PhotoRec | File carving independent of the file system | `photorec image.dd` (interactive) | Carved files by type into an output directory | Same project as TestDisk; runs inside Autopsy as an ingest module |
| foremost | Header/footer carving with content validation | `foremost -t all -i unalloc.blks -o out/` | Carved files plus `audit.txt` | Requires contiguous allocation; ⚠ command line is not from INE |
| scalpel | Rewrite of foremost, faster and leaner | `scalpel -c scalpel.conf -o out/ image.dd` | Carved files | Signature set is config-driven; ⚠ command line is not from INE |
| bulk_extractor | Feature extraction rather than file recovery | `bulk_extractor -o out/ image.dd` | `email.txt`, `url.txt`, `ccn.txt`, histograms | Stream-based and parallel; scans without seeking; ⚠ command line is not from INE |
| fiwalk | Walk an image and dump per-file metadata | `fiwalk SUSPECT-USBv3.dd -X files.xml` | XML: inode, name, partition, size, allocation state, timestamps, byte runs, MD5 and SHA-1 | Good for bulk comparison and for scripted diffs between two images |
| `hdparm` | Detect and manage HPA | `hdparm -N /dev/sda` | Reported vs native max sectors | Linux, against a physical device; removing an HPA changes the evidence |
| ATATool / Atola / OSForensics / EnCase / FTK | HPA and DCO detection and imaging | GUI | Max user / native / disk LBA | INE's screenshot shows a DCO-locked drive where max disk LBA could not be read |
| **MFTECmd** | Parse `$MFT`, `$J`, `$Boot`, `$LogFile` headers to CSV | `MFTECmd.exe -f MFT.raw --csv . --csvf mft.csv` | CSV with `0x10` and `0x30` timestamps as separate columns | ⚠ **not in INE units 4 or 5** — see §7. The tool S4 actually teaches |
| **Timeline Explorer** | Sort, filter and tag large forensic CSVs | Open the MFTECmd CSV | Filtered, taggable grid | ⚠ **not in INE units 4 or 5**. Pairs with MFTECmd; reused in S5 and S6 |
| MftCarver / PowerForensics | Carve `$MFT` records from unallocated space; PowerShell FS access | per project docs | Recovered `FILE` records / objects | Named only in INE's reference lists, never demonstrated |

---

## 4 · Findings vs interpretation — worked from this module

> **FINDING** — `$MFT` entry 41205 contains a `$FILE_NAME` attribute reading `collect.7z`, a
> `$STANDARD_INFORMATION` creation time of 2026-03-11 22:14:07 UTC, a real size of 184 320 bytes, a
> non-resident `$DATA` attribute with a runlist of clusters 812 440–812 484, and a header flag byte
> with the in-use bit clear. Reading those clusters from the image returns 45 clusters of `0x00`.
> **INTERPRETATION** — a file named `collect.7z` of roughly 180 KB existed on this volume and was
> subsequently deleted; its content is not recoverable from these clusters, and the pattern of a
> complete, intact runlist pointing at uniformly zeroed clusters is what TRIM on an SSD produces.
> **CANNOT PROVE** — that the file contained the exfiltrated documents; that the suspect deleted it
> (an installer, a cleanup script or the archiver itself could have); *when* it was deleted, since
> the record carries no deletion timestamp; or that the zeroes are the result of deliberate wiping
> rather than routine garbage collection. Reporting "the suspect wiped the archive" from this finding
> is exactly the leap the rubric penalises.

> **FINDING** — On the FAT32 volume, `fls -r -l` lists a directory entry whose first name byte is
> `0xE5` (TSK renders it `_ollect.7z`), a last-modified date of 2026-03-11, a starting cluster of
> 4 812, and a size of 184 320 bytes. The FAT entries for clusters 4 812 onward all read
> `0x00000000`.
> **INTERPRETATION** — the file was deleted from this volume: the directory entry survives with its
> metadata but its cluster chain has been released. The first cluster is still recorded, so if the
> file was written contiguously, the 45 clusters from 4 812 will reconstruct it — and that is
> testable by hashing the result against the archive's known hash.
> **CANNOT PROVE** — that clusters 4 813 onward belonged to this file. The chain is gone; contiguity
> is an *assumption*, and if any of those clusters were reallocated the reconstructed file will
> silently contain another file's bytes. Until the reconstruction is validated (it opens, it hashes
> to the expected value), "recovered `collect.7z`" is a hypothesis, not a finding.

> **FINDING** — `$MFT` entry 22910 has `$STANDARD_INFORMATION` created = 2019-07-14 03:22:11.0000000
> UTC and `$FILE_NAME` created = 2026-03-09 08:41:52.4813366 UTC. All four `$SI` timestamps carry
> zeroes in the sub-second field; all four `$FN` timestamps do not.
> **INTERPRETATION** — the `$SI` timestamps have been rewritten after the file was created. The
> combination of an `$SI` set years earlier than `$FN` *and* uniformly zeroed sub-second precision is
> characteristic of a timestomping utility, which typically writes only `$SI` and only to
> second resolution.
> **CANNOT PROVE** — that the *`$FN`* timestamps are the true creation time; they record when the
> name record was last written, which changes on rename and move. Nor does it prove who ran the tool,
> or when the tampering happened — the tampering event itself has no timestamp. And `$SI` earlier
> than `$FN` alone would prove nothing: file copies, archive extraction and restores all produce it
> legitimately. The zeroed precision is what raises this from anomaly to indicator.

> **FINDING** — `blkls` output from the USB volume, carved with `foremost`, yields a 612 KB JPEG at
> offset 0x1F4A000 in the extract, which `blkcalc` maps to cluster 32 040 of the source image. The
> image renders and shows a company document photographed on a desk.
> **INTERPRETATION** — this JPEG was physically present on the USB device and is no longer referenced
> by any live directory entry, so it was deleted or the volume was formatted after it was written.
> **CANNOT PROVE** — its filename, its path, when it was written, when it was deleted, or who put it
> there — carving discards every one of those. It does not prove it was ever deliberately saved by a
> user rather than written by a camera-import tool or a thumbnail cache, and it does not prove the
> file is complete: if the original was fragmented, the middle of this JPEG may be another file's
> bytes. The only defensible provenance statement is the source offset.

> **FINDING** — `$MFT` entry 33871 for `invoice_Q4.docx` contains two `$DATA` attributes: an unnamed
> one of 84 992 bytes and a second named `:cfg` of 5 120 bytes whose content begins with `MZ`.
> **INTERPRETATION** — a PE executable is stored in an alternate data stream attached to a document.
> The unnamed stream is the document a user would see; the named stream is not visible to Explorer,
> `dir`, or the file's reported size, and its presence is consistent with deliberate concealment.
> **CANNOT PROVE** — that the stream was ever executed, that the document's author created the
> stream, or that the user knew it was there. ADS travel with a file across NTFS copies, so the
> stream may predate this machine entirely. And most ADS on any real system are benign
> (`Zone.Identifier`, SmartScreen data) — the finding here rests on the `MZ` header and the stream
> name, not on the mere existence of an ADS.

> **FINDING** — `mmls` on EVI-SRC01 reports no partitions and the first sector reads as 512 bytes of
> `0x00`. `sigfind -t ntfs` reports an NTFS boot sector signature at sector 2 048, and `fsstat
> EVI-SRC01.dd -o 2048` decodes a valid NTFS file system with 1 953 522 168 total sectors.
> **INTERPRETATION** — the partition table was destroyed while the file system itself was left
> intact; the volume begins at the standard 1 MiB alignment offset and can be analysed directly, or
> the table can be rebuilt (on a working copy) with TestDisk.
> **CANNOT PROVE** — that the partition table was destroyed *deliberately*. A failed partitioning
> operation, a bad disk-cloning run, a boot-sector virus, or a bad-sector failure at LBA 0 all
> produce the same result, and none of them leave a signature distinguishing them from a wipe.
> It also does not prove there was only one partition — a rebuilt table is a reconstruction from the
> volumes that can still be found, not a record of what the table originally said.

---

## 5 · Exam-relevant points

- Brian Carrier's four analysis layers — physical media, volume, file system, application/OS — and
  that eCDFP works in the first three.
- A **volume** need not be physically contiguous; a **partition** must be. Every partition is a
  volume; not every volume is a partition.
- Sector = smallest **physical** unit (512 B, or 4096 B on Advanced Format). Cluster = smallest
  **logical** allocation unit. Cluster size is fixed at format time and recorded in the boot record.
- CHS: 3 bytes, 10 bits cylinder + 8 bits head + 6 bits sector; ranges C 0–1023, H 0–254, S **1–63**.
  Ceiling 1024 × 255 × 63 × 512 ≈ 7.84 GiB. CHS `(0,0,1)` = LBA `0`.
- `LBA = ((C × heads_per_cylinder) + H) × sectors_per_track + S − 1`. Be able to run it both ways.
- MBR: sector 0 · 446 boot code · 64-byte table of four 16-byte entries at 446 · `0x55AA` at 510.
  Entry: boot indicator `0x80`, starting CHS, type byte, ending CHS, starting LBA, size in sectors.
- MBR limits: **4 primary partitions**, **2 TiB** (32-bit sector count). More partitions require an
  extended partition holding a chain of EBRs, each usually with two entries used.
- GPT: protective MBR type `0xEE` at LBA 0 · header at LBA 1 (`"EFI PART"`) · entries from LBA 2 ·
  backups at the end of the disk · **128 partitions** · 64-bit LBAs · CRC32 on header and entry
  array · no extended partitions. Backup recovery of a corrupt GPT is a stock exam scenario.
- Booting from GPT requires UEFI; mounting GPT for data access does not.
- HPA is detected by comparing `IDENTIFY_DEVICE` against `READ_NATIVE_MAX_ADDRESS`; `hdparm -N`.
- SSD: page = smallest read/write (4 KB), block = smallest **erase** unit (128 pages), plane = 128
  blocks. Read/write a page, erase only a whole block.
- **TRIM**: the OS tells the SSD which LBAs are dead; the controller erases them on its own schedule;
  deleted data returns zeroes and is unrecoverable even through a write blocker.
- FAT: reserved area · FAT#1 · FAT#2 · data area. FAT12/16 reserved = 1 sector; FAT32 = 32 sectors,
  with the boot sector mirrored at 6, FSINFO at 1 and 7, bootstrap at 2 and 8.
- FAT#1 = reserved sector count. FAT#2 = reserved + sectors-per-FAT. Data area = reserved +
  2 × sectors-per-FAT. Root directory = cluster 2. Clusters 0 and 1 are reserved.
- FAT32 uses **28** of 32 bits. Entry *value* `0x?0000000` = free, `0x?FFFFFF7` = bad,
  `0x?FFFFFF8`+ = end of chain; anything else *is* the number of the next cluster in the chain.
- **FAT deletion**: first name byte → `0xE5`; the file's FAT chain entries are zeroed; the starting
  cluster in the directory entry survives; content stays until overwritten. Know all four.
- SFN attributes: `0x01` read-only, `0x02` hidden, `0x04` system, `0x08` volume label, `0x0F` LFN,
  `0x10` directory, `0x20` archive. LFN holds 13 UTF-16 chars per entry, stacked before the SFN, last
  entry's sequence ORed with `0x40`, tied to the SFN by a 1-byte checksum.
- Subdirectory entries always have size 0 and contain `.` and `..`.
- NTFS: **everything is a file**. Records 0–15 are metadata files — memorise `$MFT` 0, `$MFTMirr` 1,
  `$LogFile` 2, `$Volume` 3, `$AttrDef` 4, root 5, `$Bitmap` 6, `$Boot` 7, `$BadClus` 8, `$Secure` 9,
  `$UpCase` 10, `$Extend` 11.
- `$Boot` (record 7) is the only fixed-position structure; its offset 48 holds the LCN of `$MFT`.
- `$MFT` records are 1024 bytes, start with `FILE` (`BAAD` if unusable), carry a fixup array, and
  hold a `$LogFile` sequence number, a sequence number (reuse count) and a hard link count.
- MFT Zone ≈ 12.5 % of the volume, reserved to keep `$MFT` contiguous.
- File Reference Number = 6-byte entry number + 2-byte sequence number.
- Attribute IDs: `0x10` `$STANDARD_INFORMATION`, `0x30` `$FILE_NAME`, `0x50` `$SECURITY_DESCRIPTOR`,
  `0x60` `$VOLUME_NAME`, `0x70` `$VOLUME_INFORMATION`, `0x80` `$DATA`, `0x90` `$INDEX_ROOT`,
  `0xA0` `$INDEX_ALLOCATION`, `0xB0` `$BITMAP`, `0xC0` `$REPARSE_POINT`.
- Resident vs non-resident: INE's threshold is 700 bytes; non-resident flag is `0x01` at attribute
  header offset 8; non-resident content is addressed by a **runlist** of (start cluster, length).
  VCN = position within the file; LCN = position on the volume.
- Two `$DATA` attributes = an **alternate data stream**. `file.txt:hidden.txt`.
- Fixup arrays appear in `FILE`, `INDX`, `RCRD` and `RSTR` records.
- Slack: file slack (unused sectors in an allocated cluster — the useful kind), RAM slack (padding to
  the end of the last written sector — historical), MFT slack. INE's worked answer: 3072 bytes.
- Carving needs the header intact and the file contiguous, unfragmented and uncompressed. Techniques:
  header/footer, header + maximum size, structure-based, content-based.
- TSK prefixes: `mm` media management, `fs` file system, `f` file name, `i` metadata, `blk` content,
  `j` journal. Universal options `-f <fstype>` and `-o <offset>`.

---

## 6 · Teaching notes

**Demo live, in this order.** `mmls` → `fsstat -o` → `fls -r -l -o` → `istat -o` on one deleted file
→ `icat` it out. Five commands, one image, and the whole layer stack becomes visible in ten minutes.
Then repeat exactly the same five commands on the NTFS volume so the students see that the *layers*
are constant and only the structures change. Finish with `icat ... 0 > MFT.raw` and MFTECmd, so the
`$MFT` arrives as the natural end of a chain they have already walked, not as a magic tool.

**Where students reliably go wrong.**

1. **Forgetting `-o`.** `fsstat` against a whole-disk image fails with a message that reads like a
   corrupt image. Nearly every student hits this once. Make them hit it deliberately in the first
   five minutes so the error is familiar rather than alarming.
2. **"Deleted means gone."** They arrive believing it, and the FAT walkthrough fixes it — but then
   they over-correct into "deleted always means recoverable", which TRIM demolishes. Teach both
   halves in the same session or you will have taught a falsehood either way.
3. **Reading a type byte as a fact.** `0x07` in an MBR entry is a claim. Every year someone reports
   "the partition was NTFS" on the strength of the type byte alone.
4. **CHS sectors starting at 1.** The off-by-one in the LBA conversion. Have them do INE's exercise
   `(2,3,4)` with 16 heads and 63 sectors/track by hand; the answer is 2208, and the students who
   get 2209 are the ones who will get every offset wrong for the rest of the course.
5. **Confusing the `$MFT` record size with the header size.** The slide says "around 48 bytes";
   that is the header. The record is 1024. Say this out loud when the slide appears.
6. **Treating any ADS as malicious.** Show `Zone.Identifier` on a downloaded file first, then the
   crafted one. The lesson is the baseline, not the technique.
7. **Reporting slack content as belonging to a named file.** It has no metadata. Make them state the
   source offset instead — that habit is worth more than the recovery itself.

**Spend the time here.** `$MFT` is the load-bearing dependency for two later sessions. Students need
to leave believing three things without hesitation: a registry hive is a file with an `$MFT` record
(S5 dies otherwise); `$STANDARD_INFORMATION` and `$FILE_NAME` each hold four timestamps and they can
disagree (S6 dies otherwise); and a small file's entire content can live inside its `$MFT` record.
If the session runs long, cut the FAT boot-sector byte-by-byte walk before you cut any of this.

**TRIM deserves its own five minutes and a moment of silence.** It is the only place in the course
where the honest answer to "can we recover it?" is *no, and no tool will change that*. Demonstrate
it if the lab hardware allows: delete a file on an SSD-backed volume, wait, read the clusters, show
the zeroes, then show the `$MFT` record still sitting there with a perfectly good runlist. That
single contrast — intact metadata, erased content — is the most useful image in the whole session.

**Leave to homework.** The FAT BPB field-by-field walk (`[U5 p64–84]`) is twenty slides of the same
diagram in the source; give them the offsets table and a hex dump and let them fill in the values
themselves. Likewise the LFN checksum, the GPT header field list, and the SCSI/ATAPI interface
history — all recognition-level material that costs classroom time and yields little.

**Do not teach from these slides as they stand.** The FAT and NTFS structure slides are a wall of
repeated diagrams; the useful content is the offsets, and the offsets are what the OCR damaged most.
Rebuild them as one table per structure and check every offset against the source page first.

**Out of scope, named and skipped.** These units are Windows- and disk-centric; nothing here needs
Linux, macOS or mobile file system internals, and none is written up. TSK, foremost, PhotoRec,
scalpel and bulk_extractor are Linux *tools used against Windows evidence* and are in scope.
ext2/3/4, HFS+, UFS and YAFFS2 appear only in TSK's supported-format list `[U5 p266]` and are not
taught. exFAT is named at `[U5 p31]` and explicitly dropped by INE.

---

## 7 · Gaps, cautions and disagreements

**Topics the course needs that these units do not cover** (gap rows):

1. **TRIM, garbage collection and wear levelling — entirely absent.** Unit 4's SSD section
   `[U4 p57–66]` covers NAND pages, blocks and planes, states that SSDs "pose challenges" and that
   mishandling may render evidence inadmissible, and then hands the student off to Belkasoft's
   article series without naming a single mechanism. Since TRIM is the course's central
   "what you cannot recover" fact, §1 and §2 teach it from outside the source and say so.
2. **MFTECmd and Timeline Explorer — absent.** INE teaches `$MFT` structure thoroughly and then
   offers no modern parser for it; its tooling is WinHex, Active@, TSK, Autopsy and TestDisk, with
   MftCarver and PowerForensics named only in a reference list. The Eric Zimmerman tools that S4
   actually uses, and that S5 and S6 depend on, must be supplied by us.
3. **NTFS file deletion is never explained.** FAT deletion gets a four-step slide `[U5 p138]`; NTFS
   gets nothing beyond "entries that no longer belong to a file will be reused" `[U5 p196]`. The
   in-use flag, the `$Bitmap` release and the parent index entry removal all have to come from us —
   and the OCR has additionally lost the `0x01` flag row `[U5 p188]`, so there is no way to teach it
   from the source even by inference.
4. **`$LogFile` and `$UsnJrnl` are named, not taught.** `$LogFile` gets one paragraph on journaling
   and a mention of `RCRD`/`RSTR` fixups; `$UsnJrnl` gets a table row and a field reference. No
   structure, no retention behaviour, no parser, no `$Extend\$UsnJrnl:$J` path. Both are core S6
   inputs.
5. **`$SI` vs `$FN` timestamp comparison.** `[U5 p216]` hints that `$FILE_NAME` timestamps let you
   "check if any file timestamp manipulation has been applied" and then never shows how. The
   technique is ours.
6. **INDX / `$I30` analysis.** `$INDEX_ROOT` and `$INDEX_ALLOCATION` are named `[U5 p222]` and INDX
   fixups mentioned `[U5 p186]`, but recovering deleted directory-entry evidence from index slack is
   not covered.
7. **Volume slack and partition slack are not defined.** File slack, RAM slack and MFT slack are
   taught well; the space between the end of a file system and the end of its partition is never
   named, and partition gaps appear only in a video title `[U4 p141]` and a WinHex screenshot.
8. **No carving command lines anywhere.** foremost, scalpel, PhotoRec and bulk_extractor are each
   given a features slide and no syntax `[U5 p308–313]`. Every command in §3 for those four tools is
   from outside the source and is marked.
9. **Full-disk encryption is absent from both units.** No BitLocker, no recovery key, no encrypted
   volume detection. This is a first-order acquisition dependency and an obvious "what you cannot
   recover" case.
10. **Volume Shadow Copies.** Listed as NTFS feature 7 `[U5 p146]` and never mentioned again. VSS is
    a major recovery source for S5 and S6.
11. **Modern interfaces.** The interface list stops at ATA/SATA/ATAPI/SCSI `[U4 p42–52]`. No NVMe, no
    M.2, no USB mass storage, no eMMC/UFS — and NVMe is what students will actually meet.
12. **Advanced Format (512e vs 4Kn)** is named once `[U4 p27]` and never developed, though it changes
    every offset calculation.
13. **exFAT** is named and explicitly excluded `[U5 p31]`, but it is the default on large removable
    media and will appear on real USB evidence.
14. **`$Recycle.Bin` (`$I`/`$R` files)** is nowhere in these two units — deletion is taught at the
    file-system layer only.
15. **Sparse files, compression, hard links and reparse points** are listed as NTFS features
    `[U5 p146]` and never expanded; each changes how a runlist must be read.

**Where the INE material is dated:**

- NTFS size limits `[U5 p148]` are quoted at the Windows 7 / Server 2008 R2 implementation figures
  (16 TB max file, 256 TB max volume). Current Windows supports substantially larger volumes with
  larger cluster sizes. Teach the architectural limits and flag the implementation numbers as
  version-dependent.
- The default-cluster-size tables `[U5 p48, p147]` cite a Microsoft KB for Windows 7 / Vista / 2000.
  Still broadly right at 4 KB for typical volumes, but check before quoting a specific row.
- Autopsy v2 (the HTML frontend in the screenshots at `[U5 p304]`) is dead. INE says so at
  `[U5 p301]`; use v4 only, and do not show the old interface.
- HxD `[U4 p145]` is described as not recently updated; it has been maintained since.
- The NTFS boot chain diagram `[U5 p159]` names `Ntldr or BootMgr`. `Ntldr` is pre-Vista.
- The OS list for NTFS `[U5 p145]` stops at Windows 10 / Server 2016.
- Belkasoft's SSD article series `[U4 p66]` is dated 2012/2014/2016. The physics has not changed;
  the drive behaviour and the tooling have.

**Places where INE is wrong or misleading enough to correct in class** (INE still wins for exam
answers — the disagreement is recorded, not resolved against the course):

- **MFT Zone.** `[U5 p156]` says that after formatting a 100 GB disk "around 12.5 GB are already
  gone... you cannot use them". That is not how the MFT Zone works: it is reserved for *preferential*
  MFT allocation, Windows reports the full free space, and user data is allocated into the zone once
  the volume fills. Teach 12.5 % as the reservation figure (it is the exam answer) and correct the
  "gone" framing out loud.
- **The 700-byte resident threshold.** `[U5 p201, p218]` state it as a hard rule. In reality an
  attribute is resident when it fits in the record's remaining free space, which depends on how many
  other attributes the record already holds — so the real boundary varies, roughly 600–700 bytes for
  a typical file. Answer 700 on the exam; know why a 650-byte file is sometimes non-resident.
- **RAM slack.** `[U5 p236]` says modern operating systems "pad the sector with random garbage".
  Modern Windows zero-fills. The forensic conclusion is the same either way — no memory disclosure,
  no recoverable evidence — but do not teach "random garbage" as fact.
- **Sectors per track.** `[U4 p26]` says an IBM-PC compatible track holds 63 sectors "as six bits
  used for no. of sectors", conflating the CHS *addressing* limit with physical geometry. Real drives
  use zone bit recording and have varying sectors per track; 63 is the ceiling of a 6-bit field, not
  a measurement of a platter.
- **`$MFT` record size.** `[U5 p180]` says every entry "is around 48 bytes". That is the header. The
  record is 1024 bytes (`[U5 p189]` says so correctly, two slides later). The source contradicts
  itself; the 1024 figure is right.
- **Metadata file numbering.** `[U5 p157]` gives a coherent table (`$MFT` 0 … `$Extend` 11, 12–15
  reserved). `[U5 p174]` repeats it with the record numbers scrambled by OCR (`$MFTMirr` 2,
  `$UpCase` 20, `$Extend` 22, "22=45 Reserved", "16-23 Unused"). Use p157; ignore p174's numbers.
- **`blkcalc` vs `blkalc`.** `[U5 p271]` spells it `blkalc`, `[U5 p296]` spells it `blkcalc`. The
  tool is `blkcalc`.

**OCR uncertainty that matters** (all marked in place above as well):

- `[U5 p188]` — the `$MFT` header flag table is missing its `0x01` (record in use) row and calls
  `0x04` and `0x08` "Unknown". **This is the single most consequential OCR loss in the module**,
  because `0x01` is the bit that deletion clears. Verify on the page before teaching it.
- `[U5 p86]` — the FSINFO layout table skips the free-cluster-count row at offsets 488–491, even
  though the worked example three slides later reads a value from it.
- `[U5 p165]` — the NTFS `$Boot` offset column is garbled (`26 3`, `49) 2`, `22 2`). The field order
  is reliable; the numeric offsets are not.
- `[U5 p116, p118]` — the FAT date and time bit-field widths are printed as "bytes"; they are bits.
  The worked-answer slides (`[U5 p117, p119]`) are blank in the OCR, so there is no cross-check.
- `[U5 p203]` — the attribute-flag list gives only `0x0001` Compressed and then stops.
- `[U5 p217]` — the `$FILE_NAME` field at `0x20` is labelled "File Modification Time", duplicating
  the `0x10` row; it is the access time. The `0x00` parent-directory-reference row is missing.
- `[U5 p195]` — the File Reference Number example shows twelve hex digits (6 bytes) while the text
  says "the entire 8 bytes".
- `[U4 p34, p109]` · `[U4 p127]` · `[U5 p148]` — every exponent in these units is destroyed by OCR
  (`2™`, `272`, `2**`, `2°`, `2®`). Recompute rather than reading them.
- `[U4 p40]` — the LBA conversion exercise's answer slide is blank. §1 shows the working.
- `[U4 p130]` — the GPT type GUIDs render capital `O` where the value is zero.
- `[U4 p80]` — the Disk Management screenshot's System Reserved size reads as "330MB 88MB 25%";
  unreadable, and not worth quoting.
- `[U5 p47, p147]` — the FAT cluster-count and NTFS default-cluster-size tables are largely lost.

**A structural caution about the source itself.** Unit 5's PDF bookmarks drift badly in the back
half: pages 240–264 are bookmarked `5.4 Data Unit Layer Tools` but are actually the File Carving
section (the slide headers read "5.4 File Carving"); pages 281–283 are bookmarked `5.1 Introduction`
but are the `fsstat` slides; 284–292 are bookmarked `5.2 FAT` but are `fls`/`ffind`/`istat`; 294 is
bookmarked `5.3 NTFS` but is `icat`. Section numbers `5.2.5.1` and `5.3.3` do not exist at all, and
`5.2.3` is titled "Boot Strap 7 Reserved Sectors" where the original clearly read "&". §8 maps by
page range rather than by bookmark title for this reason — **cite pages to students, never section
numbers.**

---

## 8 · Section index → source pages

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `4.1` | Introduction | 3–16 | §0 · §1 (layers of analysis) |
| `4.2` | Hard Disk Drives | 17–42, 67–68 | §1 (Sector; CHS and LBA) · §5 |
| `4.2.1` | Interface Types | 43–52 | §6 (homework — recognition only); NVMe gap in §7 |
| `4.2.2` | BIOS | 53–56 | §2 (MBR — boot code and the jump to sector 0) |
| `4.2.3` | Solid State Drives | 57–66 | §1 (NAND page/block/plane; TRIM) · §7 gap 1 |
| `4.3` | Volumes & Partitions | 69–83, 134, 137, 139 | §1 (Volume vs partition) · §2 (Partition gaps; HPA/DCO) |
| `4.4` | Disk Partitioning - Jumpers | 84–85, 105–107 | §6 (homework — PATA jumpers, recognition only) |
| `4.4.1` | MBR Partitioning | 86–104 | §2 (Master Boot Record; Extended Boot Record chain) |
| `4.4.2` | GPT Partitioning and UEFI | 108–133 | §2 (GPT — protective MBR, header, entry array, backups) |
| `4.4.3` | Hidden Protected Area (HPA) | 135–136, 138, 140–141 | §2 (Host Protected Area and Device Configuration Overlay) |
| `4.5` | Tools | 142–145 | §3 (disk editors) |
| `4.5.1` | WinHex | 146 | §3 |
| `4.5.2` | Active@Disk | 147–155 | §3 |
| `5.1` | Introduction | 3–28, 281–283 | §1 (Allocated/unallocated; what deletion means) · §3 (`fsstat`) |
| `5.2` | FAT File System Analysis | 29–49, 96–97, 102–105, 141–143, 284–292 | §1 (Cluster) · §2 (FAT itself) · §3 (`fls`, `ffind`, `istat`) |
| `5.2.1` | FAT Structures | 50–58 | §2 (FAT32 boot sector — reserved-area layout) |
| `5.2.1.1` | Boot Sector | 59–67 | §2 (FAT32 boot sector) |
| `5.2.1.2` | BIOS Parameter Block | 68–80 | §2 (FAT32 boot sector) · §6 (byte-walk → homework) |
| `5.2.1.3` | Extended BIOS Parameter Block | 81–84 | §2 (FAT32 boot sector — volume serial and label) |
| `5.2.2` | FSINFO Sector | 85–92 | §2 (FSINFO sector) |
| `5.2.3` | Boot Strap 7 Reserved Sectors | 93–94 | — *nothing forensic* (bootstrap is empty; `0x55AA` noted in §2) |
| `5.2.4` | FAT Area | 95, 98–101, 106–110 | §2 (The File Allocation Table itself) |
| `5.2.5` | Data Area | 111–114 | §2 (FAT32 directory entry) · §1 (Cluster) |
| `5.2.5.2` | Short File Name | 115–119 | §2 (FAT32 directory entry — SFN) |
| `5.2.5.3` | Long File Name | 127 | §2 (FAT32 directory entry — LFN) |
| `5.2.6` | File Allocation | 134–138 | §2 (The FAT itself — chain walkthrough) · §5 |
| `5.2.7` | File Deletion | 139–140 | §1 (What deletion means) · §2 (FAT32 directory entry) · §4 |
| `5.3` | NTFS File System Analysis | 120–126, 128–133, 144–153, 294 | §1 (Resident vs non-resident) · §2 (`$MFT`) · §3 (`icat`) |
| `5.3.1` | NTFS Structure | 154–160 | §2 (`$MFT` record — metadata files 0–15, MFT Zone) |
| `5.3.1.1` | Volume Boot Record | 161–172 | §2 (NTFS Volume Boot Record `$Boot`) |
| `5.3.1.2` | Master File Table | 173–197 | §2 (`$MFT` record) · §1 (Fixup array) · §6 |
| `5.3.2` | NTFS Attributes | 198–224 | §2 (`$STANDARD_INFORMATION`, `$FILE_NAME`, `$DATA`, ADS) |
| `5.3.4` | FILE and RAM Slack | 225–239 | §1 (Slack) · §2 (Slack space) · §4 |
| `5.4` | Data Unit Layer Tools | 240–264, 296–298 | §1 (File carving) · §2 (Carved file) · §3 (`blkls`, `blkcalc`) |
| `5.5` | The Sleuthkit (TSK) | 265–280 | §3 (whole TSK block) · §5 (layer prefixes) |
| `5.5.3` | Metadata Layer Tools | 293 | §3 (`ifind`, `istat`, `icat`, `ils`) |
| `5.5.4` | Data Unit Layer Tools | 295 | §3 (`blkstat`, `blkls`, `blkcalc`, `blkcat`) |
| `5.6` | Other Tools | 299–317 | §3 (Autopsy, TestDisk, PhotoRec, fiwalk, foremost, scalpel, bulk_extractor) |
