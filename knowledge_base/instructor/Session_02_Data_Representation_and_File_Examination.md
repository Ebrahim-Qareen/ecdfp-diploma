# Instructor Session 02 — Data Representation & File Examination

| | |
|---|---|
| **Deck** | `Resources/Instructor/Session 2.pdf` — 38 slides, 24 screenshots |
| **INE material covered** | unit 3 — see [`Module_02_Data_Representation_and_File_Examination.md`](../Module_02_Data_Representation_and_File_Examination.md) |
| **Feeds eCDFP session** | `S3` |
| **Source text** | [`../_source_text/Instructor_Session_02_Data_Representation_File_Examination.md`](../_source_text/Instructor_Session_02_Data_Representation_File_Examination.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Twelve lecture slides then a single continuous lab. The lecture arc is deliberately linear and
short: binary → ASCII → RGB/video → how a file is allocated to clusters → what deletion actually
does → file structure (header / data / EOF) → magic bytes → carving. Everything after slide 17 is
hands-on, and the lab is unusually wide — six distinct tool exercises in one block, ending on a
signature-analysis task set as homework via a shared drive link.

The deck closes on the sentence that matters most for the rebuilt course: *"digital forensics is
not about just using tools, you must follow a scientific procedure."* That is the same point
`S1-02` makes about repeatability, restated where students have just spent two hours in tools.

Note that the deck teaches **deletion and cluster allocation here**, ahead of the file-systems
session. In the rebuilt six-session shape those belong to `S4`. See §5.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–4 | Course outline, session title, evidence-lifecycle "we are here" marker | `admin` |
| 5–7 | Digital data, ASCII table, data representation (RGB, video as frames) | `concept` |
| 8 | Storage devices — HDD vs SSD, "logically the same" | `concept` |
| 9–12 | Cluster allocation · what deletion does · when data is really gone | `concept` |
| 13–14 | File structure — header / data / EOF; header as metadata, EXIF named | `concept` |
| 15 | Magic bytes, with a live `xxd` of a JPEG | `demo` |
| 16 | Disk carving; Gary Kessler signature table as the reference | `concept` |
| 17 | **Lab agenda slide** — the six exercises that follow | `admin` |
| 18–19 | File metadata via Explorer properties · EXIF via ExifTool | `demo` |
| 20 | **Task** — identify the city a photo was taken in (EXIF GPS) | `challenge` |
| 21–23 | HxD raw view · file-signature analysis · Gary Kessler lookup | `lab` |
| 24 | **Task** — identify the extension of a set of files | `challenge` |
| 25–26 | Manual file recovery from `$RECYCLE.BIN` with FTK Imager; mount image | `lab` |
| 27–29 | TestDisk — disk/partition-table repair walk-through | `lab` |
| 30–32 | PhotoRec — automated carving, results in `recup_dir.1` | `lab` |
| 33–36 | Steganography — concept, stego-vs-original, hiding a file with Xiao | `lab` |
| 37 | Autopsy for automated analysis (download link only) | `admin` |
| 38 | Closing principle — procedure over tools | `concept` |

## 2 · Labs and demos — what was actually run

### Magic bytes on the command line · slide 15
**Tools:** `xxd`
**Evidence used:** an arbitrary JPEG (`website.jpg` in the screenshot)
**Steps as demonstrated:**

1. Dump the first bytes of the file:

```
xxd website.jpg | head
```

Output shown begins `ffd8 ffe0 0010 4a46 4946` — the JPEG SOI marker `FF D8` followed by
`FF E0` and the ASCII `JFIF` identifier, visible in the decoded column.

**What this lab teaches:** the header is *in the bytes*, not in the name — the single fact the
whole session rests on.

### File metadata from the shell and the GUI · slides 18–19
**Tools:** Explorer → Properties → Details; **ExifTool**
**Evidence used:** a `.dotx` template (properties) and a Nikon COOLPIX P6000 JPEG (EXIF)
**Steps as demonstrated:**

1. Right-click → Properties → Details on an Office file. The screenshot shows `Authors`,
   `Last saved by`, `Revision number`, `Program name`, `Date last saved`, `Total editing time`,
   and — importantly — the **Remove Properties and Personal Information** link.
2. Run ExifTool against an image. Output shown includes `Make : NIKON`,
   `Camera Model Name : COOLPIX P6000`, `Software : Nikon Transfer 1.1 W`,
   `Modify Date : 2008:11:01 21:15:08`, `Date/Time Original : 2008:10:22 16:38:20`,
   `Create Date : 2008:10:22 16:38:20`, exposure/ISO/flash fields.
   `⚠ OCR — verify` on `F Number 2 ALT` (a mangled f-stop value).

The exact ExifTool invocation is **not visible** on the slide — only its output. The standard
form is `exiftool <file>`; recover the actual command from the slide before handing it out.

**What this lab teaches:** two timestamps that disagree (`Modify Date` 2008-11-01 vs
`Date/Time Original` 2008-10-22) and a `Software` field naming the transfer tool — the raw
material for a findings-vs-interpretation exercise. Note the deck does **not** draw that
conclusion; it is available and unused.

### EXIF GPS challenge · slide 20
A photo is distributed by shared link and students must name the city it was taken in.
`⚠` The link is a Google Drive URL (see §5) — treat as unverified and re-host on the course share.

### Raw view and signature analysis in HxD · slides 21–23
**Tools:** **HxD** hex editor; Gary Kessler's file-signature table
**Evidence used:** a JPEG, then `File02` from a "File Type Analysis Part 1" exercise set
**Steps as demonstrated:**

1. Open the file in HxD; read offset `00000000` in the hex pane against the Decoded-text pane.
   For the JPEG: `FF D8 FF E0 00 10 4A 46 49 46` → `ÿØÿà..JFIF`.
2. For `File02` the decoded text reads
   `... Windows Internet Explorer 8>..Subject: Blackboard Learn..Date: Fri, 6 Jul 2012 08:32:08 -0700..MIME-Version: 1.0..Content-Type: multipart/related;` with
   `X-MimeOLE: Produced By Microsoft MimeOLE V6.00.2900.6157` —
   i.e. an **MHTML / `.mht` saved-page or `.eml`-family file**, identified purely from its
   opening bytes.
3. Cross-check the signature against `garykessler.net`; the screenshot shows the table around
   `46 49 4C 45` (`FILE` — NTFS MFT entry), `46 4C 56 01` (FLV), `47 49 46 38 37 61` / `39 61`
   (GIF87a / GIF89a), `46 72 6F 6D 3A 20` (`From: ` — EML).

**Evidence-set note:** the "File Type Analysis Part 1" folder is exactly the shape `EVS-05`
needs (12 renamed / corrupted files). It is a strong candidate to adopt rather than rebuild —
route it through `ecdfp-evidence` for licensing and hashing before use.

**What this lab teaches:** identify by header, then confirm against a reference table — never
by extension.

### Manual recovery from the Recycle Bin with FTK Imager · slides 25–26
**Tools:** **FTK Imager 4.7.3.81** (as shown), including *File → Image Mounting*
**Evidence used:** a 1 GB GPT disk image (`image hard drive 1GB.001`), NTFS volume
**Steps as demonstrated:**

1. Add the `.001` image as an evidence item. The tree shows
   `Microsoft reserved partition (1) [15MB]` and
   `Basic data partition (2) [1006MB] → New Volume [NTFS]`, then the NTFS system files
   `$BadClus`, `$Extend`, `$RECYCLE.BIN`, `$Secure`, `$UpCase`,
   `System Volume Information`, `[unallocated space]`.
2. Descend into `$RECYCLE.BIN\S-1-5-21-<user SID>\` — the file list shows the
   `$I` / `$R` pair convention: `$I9XJ6ZK.jpg` (94 bytes) alongside `$R9XJ6ZK.jpg`
   (231,719 bytes), and likewise `$IMPH6FM.jpg` / `$RMPH6FM.jpg`.
   `⚠` The real SID is visible in the screenshot — replace it before reuse.
3. Export / preview the `$R` file to recover the content; the preview pane renders the image.
4. **Mount Image To Drive** with `Mount Type: Physical & Logical`,
   `Mount Method: Block Device / Read Only`, next available drive letter — so the mounted
   image is browsable without writing to it.

**What this lab teaches:** the `$I`/`$R` pair, and that "deleted" in the Recycle Bin means
*moved and renamed*. The `Read Only` mount method is the write-blocking lesson from `S1-08`
applied in software — call that out explicitly.

### Partition-table repair with TestDisk · slides 27–29
**Tools:** **TestDisk 7.3-WIP (September 2024)**, `testdisk_win.exe`
**Evidence used:** the same 1 GB virtual disk, presented as `\\.\PhysicalDrive4 - 1063 MB / 1014 MiB`
**Steps as demonstrated:**

1. Launch from the tool folder:

```
testdisk_win.exe
```

2. Log choice: `[ Create ]` a new log file / `[ Append ]` / `[ No Log ]`.
   **Choose `Create` and keep `testdisk.log`** — it is the contemporaneous record of what the
   tool did, and the course grades exactly that under criterion 1 of the rubric.
3. Select the media and `[Proceed]`.
4. Partition-table type: TestDisk detects and hints `EFI GPT partition table type has been
   detected`; options shown are `[Intel]` `[EFI GPT]` `[Humax]` `[Mac]` `[None]` `[Sun]` `[XBox]`.
   The slide reproduces the warning: *do NOT select `None` for media with only a single
   partition*.

**What this lab teaches:** partition-table recovery is a guided, logged operation — and it
**writes**, so it happens on a copy. The deck does not say this; add it.

### Automated carving with PhotoRec · slides 30–32
**Tools:** **PhotoRec 7.3-WIP**, `photorec_win.exe` (ships with TestDisk)
**Steps as demonstrated:**

1. Launch:

```
photorec_win.exe
```

2. Select the virtual disk; note it is listed `(RO)` — read-only.
3. Select the partition. The screenshot shows
   `2 P MS Data 16384 2076671 2060288 [Basic data partition] [New Volume]`.
4. Run to completion. Output: `<n> files saved in /testdisk-7.3-WIP/recup_dir directory.` →
   `Recovery completed.`
5. Browse `recup_dir.1`. Recovered files are shown named by offset, not by original name:
   `10011328.jpg`, `10011784.jpg`, `10012904.docx`, `10014480.pdf`, `10014960.mp4`,
   `10030632.jpg`, plus `report.xml`.

**What this lab teaches:** carving recovers *content*, never *names, paths or timestamps* —
the clearest possible demonstration of what a carved file cannot prove. Pair it directly with
the FTK Imager recovery above, where the name survived because the file system record did.

### Steganography with Xiao Steganography · slides 33–36
**Tools:** **Xiao Steganography** (nakasoft), Notepad
**Evidence used:** `picture.bmp` (1280 × 853, 24-bit) and a `secret.txt` containing `top secret`
**Steps as demonstrated:**

1. `Add Files` → load target file (`picture.bmp`), then attach `secret.txt`, then `Next`.
2. Slides 34–35 show a stego image beside its original ("No Message" vs
   "Attack at midnight") — visually identical.
3. `Extract Files` recovers the payload from a carrier.

**What this lab teaches:** a file's bytes can carry more than its type implies — and that a
visual comparison proves nothing. `⚠` Xiao is old, unmaintained Windows freeware; see §6.

### Autopsy · slide 37
Named as the automated-analysis tool with a download link only — **no walkthrough in the deck.**

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| Recycle Bin `$I` / `$R` pair | `<volume>\$RECYCLE.BIN\S-1-5-21-<SID>\$I…` and `$R…` | `$I` holds original name/path/size/deletion time; `$R` holds content | [M04 §2A](../Module_04_System_and_Network_Forensics.md) |
| NTFS system files | `$BadClus` · `$Extend` · `$Secure` · `$UpCase` at volume root | Shown in the FTK Imager tree as proof they are ordinary files | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| JPEG signature | `FF D8 FF E0` … `JFIF` at offset 0 | File-type identification | [M02 §2](../Module_02_Data_Representation_and_File_Examination.md) |
| NTFS MFT entry signature | `46 49 4C 45` (`FILE`) | Shown in the Kessler table | [M03 §2](../Module_03_Disks_and_File_Systems.md) |
| EXIF fields | `Make`, `Camera Model Name`, `Software`, `Modify Date`, `Date/Time Original`, `Create Date` | Device attribution and timeline | [M02 §2](../Module_02_Data_Representation_and_File_Examination.md) |
| Office document properties | Explorer → Properties → Details | `Authors`, `Last saved by`, `Revision number`, `Total editing time` | [M02 §2](../Module_02_Data_Representation_and_File_Examination.md) |
| PhotoRec output | `<toolpath>\recup_dir.1\` + `report.xml` | Carved output, offset-named | [M03 §2](../Module_03_Disks_and_File_Systems.md) |

## 4 · What this deck adds beyond the INE material

- **A working carving toolchain INE never shows.** INE unit 3 teaches signatures and structure
  but its tooling is dated; TestDisk/PhotoRec 7.3-WIP (Sept 2024) and HxD are current and free.
- **The `$I`/`$R` recovery walkthrough**, which INE unit 3 does not cover at all — it is unit 6
  material, brought forward here because it makes "deleted ≠ gone" concrete in one screen.
- **Two ready-made student challenges** (EXIF-GPS city; identify-the-extension) with evidence
  already assembled.
- **A steganography block.** INE unit 3 covers data hiding conceptually (`3.6 Data Hiding
  Locations`); the deck makes it hands-on.
- **The Gary Kessler signature table** as a named, citable reference students can keep.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted, and needed for `S3`:**

- **Malicious document structure** — OLE vs OOXML, embedded objects, macros. INE covers this at
  length (`3.7.1 DOCX Analysis`, `3.7.3 PDF Analysis`, `3.7.4 EXE Analysis`, ~120 pages). The
  deck has none of it. This is the single largest gap, and it is precisely the D19 carry-through
  artefact for `S3-09`.
- **Endianness and number-base conversion** (INE `3.2.3`–`3.2.6`) — assumed, never taught.
- **Metadata locations inside the `$MFT`** (INE `3.4.1.1`) — the deck teaches metadata only via
  Explorer and ExifTool.
- **TrID** — INE's signature-identification tool; the deck uses manual lookup instead.

**Delivered here but belonging to `S4` in the rebuilt course:** cluster allocation (slide 9),
file deletion mechanics (slides 10–12), TestDisk partition repair (27–29), PhotoRec (30–32).
Moving carving and partition repair into `S4` frees roughly 40 minutes in `S3` — close to what
the malicious-document block needs.

**Resources cited on slides** (all `unverified` — do not link from `docs/` until checked):

- `https://www.garykessler.net/library/file_sigs.html` — file-signature reference (slide 16)
- `https://www.autopsy.com/download/` — Autopsy (slide 37)
- Google Drive shared link, EXIF-GPS challenge photo (slide 20)
- Google Drive shared link, identify-the-extension file set (slide 24)

## 6 · Cautions before reuse

- **Personal data in screenshots — regenerate on the course lab before reuse:**
  - **slide 21** — HxD title bar shows the presenter's own profile path (`C:\Users\<name>\Downloads\…`).
  - **slides 22, 27, 28, 29, 30, 31, 32** — the presenter's working tree
    (`D:\Work\IT Gate\eCDFP\Tools\…`) is visible in the title bar and console prompt of every
    TestDisk/PhotoRec/HxD capture.
  - **slides 25, 26** — an FTK Imager case path (`E:\Cases\Case 1\Evidence 1 Dell PC\…`) **and a
    real Windows user SID** in the `$RECYCLE.BIN` path.
  - **slide 26** — the Mount dialog lists the presenter's physical drives by model
    (TOSHIBA MQ04ABF100, PM991 NVMe Samsung 256GB, ST1000LM035). Same on slides 28–30.
- **Google Drive links (slides 20, 24) are single points of failure** for two graded tasks.
  Re-host both file sets on the academy share and hash them via `ecdfp-evidence`.
- **Xiao Steganography (slide 36)** is abandonware from an unmaintained site. For a public,
  reproducible lab prefer `steghide`, `zsteg` or OpenStego; keep Xiao only if the classroom
  image already carries it.
- **Tool versions are early-2025 and mostly still current**: FTK Imager 4.7.3.81,
  TestDisk/PhotoRec 7.3-WIP (Sept 2024). Confirm before the run — FTK Imager in particular has
  moved under Exterro and its download flow changes.
- **OCR-unresolved and worth checking on the slide:** the ExifTool `F Number` value (slide 19);
  the ASCII table images (slide 6) are readable but scrambled in places — use a clean table
  rather than this screenshot; the file-recovery counts in the PhotoRec completion line
  (slide 31) did not resolve.
- **Slide 8 asserts HDD and SSD are "logically the same".** True for the file system; false for
  recoverability, because of TRIM. INE does not name TRIM either — see
  [`Module_03`](../Module_03_Disks_and_File_Systems.md) §7. Correct this in delivery.
