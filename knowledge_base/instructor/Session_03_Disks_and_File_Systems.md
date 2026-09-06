# Instructor Session 03 — Disks & File Systems

| | |
|---|---|
| **Deck** | `Resources/Instructor/Session 3.pdf` — 40 slides, 21 screenshots |
| **INE material covered** | units 4–5 — see [`Module_03_Disks_and_File_Systems.md`](../Module_03_Disks_and_File_Systems.md) |
| **Feeds eCDFP session** | `S4` |
| **Source text** | [`../_source_text/Instructor_Session_03_Disks_File_Systems.md`](../_source_text/Instructor_Session_03_Disks_File_Systems.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Two named parts with a lab block at the end of each. **Part 1 · Disks** (slides 5–23): HDD
mechanics, SSD caution, the disk/volume/partition distinction, MBR then GPT, each closing on a
"Lab time" agenda slide. **Part 2 · File systems** (slides 24–36): FAT structure and deletion,
then NTFS features, metadata files and `$MFT`, closing on a third lab agenda. The session ends
with a CTF, a submission form, and a homework instruction to build a Windows 10 VM for next time.

The striking thing about this deck is the ratio: **472 pages of INE source compressed into 40
slides**, of which the substantive lecture is about 25. It works because the labs carry the
weight — but three of the four lab agendas name exercises whose steps appear nowhere in the
deck. See §2 and §6.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–4 | Course outline, session title, evidence-lifecycle marker | `admin` |
| 5–6 | Part 1 · Disks — where evidence is stored; wire evidence flagged as separate | `concept` |
| 7–9 | HDD components (platter, spindle, head, IDE connector); platters → tracks → sectors; the 63-sectors/6-bit note | `concept` |
| 10–12 | SSDs — "complex", "handle carefully or evidence inadmissible"; Belkasoft reading | `concept` |
| 13 | Disk vs volume vs partition | `concept` |
| 14–15 | Partitioning schemes; MBR limits — 4 primary partitions, 2 TB, since the 1980s | `concept` |
| 16–17 | MBR sector layout (446 / 64 / 2); MBR vs VBR placement | `concept` |
| 18 | **MBR lab agenda** — analyse MBR with 010 Editor; fix a corrupted MBR | `lab` |
| 19–20 | GPT — up to 128 partitions, >2 TB, UEFI; LBA layout with backups | `concept` |
| 21 | **GPT lab agenda** — analyse GPT with 010 Editor; fix a corrupted GPT | `lab` |
| 22–23 | A corrupted GPT disk in hex; primary vs backup GPT header side-by-side | `demo` |
| 24–25 | Part 2 · File systems — definition | `concept` |
| 26–28 | FAT family (12/16/32/exFAT); clusters worked example; FAT32 reserved area | `concept` |
| 29–31 | FAT deletion — the `0xE5` marker; before/after directory-entry diagrams | `concept` |
| 32 | NTFS — 13 core features listed | `concept` |
| 33 | NTFS system files seen in WinHex (`$`-prefixed, hidden) | `demo` |
| 34 | NTFS metadata-file table — name, file, record number, purpose | `concept` |
| 35 | `$MFT` record structure overview | `concept` |
| 36 | **File-system lab agenda** — TestDisk, PhotoRec, `$MFT` with MFTECmd | `lab` |
| 37 | Additional resource — MACB times article | `admin` |
| 38–39 | CTF time; Google Forms submission link | `challenge` |
| 40 | Homework — build a Windows 10 VM for next session | `admin` |

## 2 · Labs and demos — what was actually run

**Read this section with §6 open.** Three of the four lab blocks are *agenda slides only* — the
exercise is named, the steps are not in the deck. What follows separates what is demonstrated
from what is merely announced.

### MBR structure in hex · slides 16–17 (`demo`, supports the lab on 18)
**Tools:** hex viewer (the lab agenda names **010 Editor**)
**Steps as demonstrated:** the layout is given as a table rather than a live tool run —

| Offset (start) | Offset (end) | Length | Description |
|---|---|---|---|
| 0 | 445 | 446 | Code area |
| 446 | 509 | 64 | Master partition table |
| 510 | 511 | 2 | Boot-record signature |

Total 512 bytes = 1 sector. Slide 17 then draws the MBR/VBR distinction: the MBR is at the
start of the **whole disk**, the VBR at the start of a **partition**.

**What this lab teaches:** four 16-byte partition entries in 64 bytes, and a two-byte signature
that is the first thing to check when a table "disappears".

### MBR lab · slide 18 — **agenda only**
Named exercises: *analysing an MBR partition with 010 Editor*, *fixing a corrupted MBR
partition*. No screenshots, no steps, no evidence file named. Must be rebuilt from scratch —
see [`Module_03`](../Module_03_Disks_and_File_Systems.md) for the structures, and note
`S4-10` in the topic map already calls for a wiped-partition-table case (`EVS-07`).

### GPT structure and the corrupted-GPT demo · slides 20, 22–23
**Tools:** hex viewer
**Evidence used:** a deliberately corrupted GPT disk
**Steps as demonstrated:**

1. Slide 20 gives the layout: `Protective MBR (LBA 0)` → `GPT Header (LBA 1)` →
   `Partition Table (LBA 2)` → … → `Backup Partition Table (LBA n-1)` →
   `Backup GPT Header (LBA n)`.
2. Slide 22 shows the damaged disk in hex: sectors overwritten with a repeating `41` (`A`)
   pattern, and then at offset `00000200` the signature appears —
   `45 46 49 20 50 41 52 54` → `EFI PART`, followed by `00 00 01 00` (revision 1.0) and
   `5C 00 00 00` (header size 92).
   `⚠ OCR — verify` on the byte values beyond the signature; the dump is heavily damaged by OCR.
3. Slide 23 places the **primary GPT header beside its backup at the end of the disk**, byte for
   byte, as the recovery route.

**What this lab teaches:** GPT is self-healing by design — there are two of everything, and the
`EFI PART` signature is what you search for when the front of the disk is gone. This is the
strongest demo in the deck and maps directly onto `S4-05` and `S4-10`.

### GPT lab · slide 21 — **agenda only**
Named exercises: *analysing a GPT drive with 010 Editor*, *fixing a corrupted GPT partition*.
The corrupted disk from slides 22–23 is presumably the evidence, but it is not named or linked.

### FAT cluster allocation and deletion · slides 27, 29–31
**Tools:** none — diagrams
**Steps as demonstrated:**

1. Slide 27: a volume with **4 sectors per cluster**; `file1` at 512 bytes and `file2` at
   1024 bytes, drawn onto the sector grid. This is the slack-space setup, though the deck does
   not use the word.
2. Slide 29 states the deletion mechanics in text: the system does not erase data, it edits the
   directory entry, replacing **the first character of the file name with `0xE5`**, and marks
   the space free.
3. Slides 30–31: `Pic.jpg` before and after deletion, showing the directory entry becoming
   `_ic.jpg` while the cluster chain and content stay put.

**What this lab teaches:** deletion is a *name* operation, not a *data* operation — and the
recoverable window is until reuse.

### NTFS system files in WinHex · slide 33
**Tools:** **WinHex**
**Evidence used:** an NTFS volume (timestamps in the capture are July–September 2017)
**Steps as demonstrated:** open the volume in WinHex with hidden files shown. The listing
displays, with sizes and 1st-sector values:

`$AttrDef` (2.5 KB) · `$BadClus` (0 B) · `$Bitmap` (3.1 KB) · `$Boot` (8.0 KB, 1st sector 0) ·
`$LogFile` (2.0 MB) · `$MFT` (256 KB) · `$MFTMirr` (4.0 KB) · `$Secure` (0 B) ·
`$UpCase` (128 KB) · `$Volume` (0 B) · `$Extend` · `$RECYCLE.BIN` · root directory ·
`System Volume Information`.
`⚠ OCR — verify` the exact sizes; several are legible but a few digits are uncertain.

**What this lab teaches:** *the metadata is files*. This is the load-bearing idea for `S5` —
registry hives are files too, and you cannot carve or locate one without the file system.
Say it here, out loud, and reference it again in `S5-01`.

### NTFS metadata-file table · slide 34

| Name | File | Record | Purpose (as given) |
|---|---|---|---|
| Master file table | `$MFT` | 0 | A record for each file and directory on the volume |
| Master file table mirror | `$MFTMirr` | 1 | Recovery if the MFT fails |
| Log file | `$LogFile` | 2 | File-system metadata changes; helps recovery |
| Volume | `$Volume` | 3 | Volume information and label |
| Attribute definition | `$AttrDef` | 4 | All attributes used in the file system |
| Root file name index | `.` | 5 | The root directory |
| Cluster bitmap | `$Bitmap` | 6 | Free/used cluster tracking |
| Boot sector | `$Boot` | 7 | Mount + bootstrap code |
| Bad cluster file | `$BadClus` | 8 | Bad-cluster tracking |
| Security file | `$Secure` | 9 | Security descriptors for all files |
| Upcase table | `$UpCase` | 10 | Lowercase → Unicode uppercase mapping |
| NTFS extension directory | `$Extend` | 11 | Quotas, reparse points, extended features |
| — | — | 12–15 | Reserved |

`⚠` The slide prints the extension directory as `$Extended` and the reserved range as `22-15`;
both are OCR/typo artefacts — the file is `$Extend` and the range is 12–15.

### File-system lab · slide 36 — **agenda only**
Named exercises: *fix a file system with TestDisk*, *recover data with PhotoRec*, *analyse
`$MFT` with Eric Zimmerman's MFTECmd*. TestDisk and PhotoRec were walked through in
**Session 2** (slides 27–32) — reuse those steps. **MFTECmd has no walkthrough anywhere in this
deck**; the usable one is in
[`Session_05`](./Session_05_Practical_Windows_Forensics_part_2.md), where the command is on
screen.

### CTF and homework · slides 38–40
A CTF block with a Google Forms submission link (see §5), then the standing homework:
**a Windows 10 VM installed before the next session.** In the rebuilt course `D17` supersedes
this — FOR-WS01 ships pre-built and students install the tool set in `S1`.

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| MBR | LBA 0 of the physical disk; bytes 446–509 partition table, 510–511 signature | Partition table + boot code | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| VBR | Sector 0 of a partition | Distinguished from MBR by location | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| GPT header | LBA 1, signature `EFI PART` (`45 46 49 20 50 41 52 54`) | Primary header | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| GPT backup header | Last LBA of the disk | Recovery copy | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| GPT partition table | LBA 2 (and backup at LBA n−1) | Partition entries | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| FAT deleted-entry marker | First byte of the directory entry set to `0xE5` | Marks the entry free | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| NTFS metadata files | `$MFT`, `$MFTMirr`, `$LogFile`, `$Volume`, `$AttrDef`, `$Bitmap`, `$Boot`, `$BadClus`, `$Secure`, `$UpCase`, `$Extend` at volume root, records 0–11 | Hidden system files | [M03 §2](../Module_03_Disks_and_File_Systems.md) |

## 4 · What this deck adds beyond the INE material

- **The corrupted-GPT hex walkthrough (slides 22–23)** — INE unit 4 covers GPT structurally but
  never shows a damaged disk or the primary-vs-backup comparison. This is the deck's best
  original teaching asset and should survive into `S4` intact.
- **MFTECmd named as the `$MFT` tool.** INE's tooling is WinHex / Active@ / TSK / Autopsy /
  TestDisk — the Eric Zimmerman set does not appear in unit 5 at all. The topic map assumes
  MFTECmd + Timeline Explorer (`S4-08`), so the deck is the only in-project source for it.
- **010 Editor** as the structure-aware hex tool for partition work (INE uses WinHex).
- **Compression judgement.** The choice of what to cut from 472 pages is itself useful: HDD
  mechanics get three slides, FAT gets six, NTFS gets four, and everything else is lab.
- **The MACB-times reference** (andreafortuna.org, slide 37) — a compact external explainer for
  the timestamp material `S6` depends on.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted, and needed for `S4`:**

- **Slack space** — never named, in either part. INE covers `FILE and RAM Slack` at length
  (unit 5 `5.3.4`, pp. 225–239) and `S4-03` requires file slack vs volume slack.
- **NTFS deletion mechanics.** FAT deletion gets three slides; NTFS deletion gets none. (INE
  does not explain it either — see [`Module_03`](../Module_03_Disks_and_File_Systems.md) §7.)
- **`$MFT` attributes** — `$STANDARD_INFORMATION`, `$FILE_NAME`, `$DATA`, resident vs
  non-resident, and **ADS**. Slide 32 lists "Alternate Data Streams" as an NTFS feature and
  never returns to it. `S4-07` requires all of it.
- **`$LogFile` and `$UsnJrnl` as investigative sources** — listed in the metadata table as
  recovery machinery, never used as evidence.
- **HPA / DCO** (INE unit 4 `4.4.3`) — hidden areas, absent.
- **CHS vs LBA addressing** — implied by the 63-sectors note on slide 9, never explained.
- **TRIM.** Slides 10–12 warn that SSDs are "complex" and evidence may be "inadmissible", then
  outsource the explanation to three Belkasoft links. The mechanism is never named. This is the
  most important omission in the deck.
- **The Sleuth Kit** (INE unit 5 `5.5`, pp. 265–280) — `fsstat`, `blkcalc` and the layer tools.

**Resources cited on slides** (all `unverified` — do not link from `docs/` until checked):

- `https://belkasoft.com/ssd-2012` · `https://belkasoft.com/ssd-2014` ·
  `https://belkasoft.com/ssd-2016` — SSD forensics series (slide 12)
- `https://en.wikipedia.org/wiki/NTFS` — cited for the NTFS feature list (slide 32)
- `https://andreafortuna.org/2017/10/06/macb-times-in-windows-forensic-analysis/` — MACB times (slide 37)
- Google Forms link — CTF submission (slide 39)

## 6 · Cautions before reuse

- **Three of the four lab blocks are agenda slides with no steps** (slides 18, 21, 36). Do not
  plan `S4` assuming the labs exist — the MBR-repair and GPT-repair exercises and the MFTECmd
  run all have to be written. This is the single biggest reuse caution in the deck.
- **No personal data was found in this deck's screenshots** — unusually, the captures are
  diagrams, WinHex listings and hex dumps with no title bars or user paths. It is the cleanest
  of the nine decks for reuse. (Verify slide 33's WinHex capture at full resolution before
  publishing; the volume label and paths are cropped in the OCR but may be present in the image.)
- **Slide 15 says MBR "can only handle disks up to 2TB".** Correct in effect, but state the
  reason — a 32-bit LBA field at 512-byte sectors — or students memorise a number instead of a
  structure.
- **Slide 10's "handle carefully or you might find your evidence inadmissible"** is the right
  instinct with the wrong vocabulary. The issue is not admissibility, it is that the drive
  controller destroys data independently of the analyst. Teach TRIM and garbage collection here.
- **Slide 8 (Session 2) and slide 13 (this deck) together imply HDD and SSD differ only in
  hardware.** They do not differ for the file system and do differ completely for recovery.
- **010 Editor is commercial** ($59.95 at time of writing, 30-day trial). Every other tool in
  the course is free. Either budget for it, or rewrite the MBR/GPT labs around HxD or WinHex —
  both already used elsewhere in the course.
- **Slide 40's homework (build a Windows 10 VM) is superseded by `D17`** — FOR-WS01 ships
  pre-built. Do not carry this instruction forward.
- **OCR-unresolved and worth checking on the slide:** the hex byte values on slides 22–23 beyond
  the `EFI PART` signature; the exact file sizes in the WinHex listing on slide 33; `$Extended`
  and the `22-15` reserved range on slide 34 (both wrong as printed).
