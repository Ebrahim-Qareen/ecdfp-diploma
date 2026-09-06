# Instructor Session 01 — Introduction to Digital Forensics & Acquisition

| | |
|---|---|
| **Deck** | `Resources/Instructor/Session 1.pdf` — 70 slides, 30 screenshots |
| **INE material covered** | units 1–2 — see [`Module_01_Data_Acquisition.md`](../Module_01_Data_Acquisition.md) |
| **Feeds eCDFP session** | `S1` · `S2` |
| **Source text** | [`../_source_text/Instructor_Session_01_Introduction_to_Digital_Forensics_Acquisition.md`](../_source_text/Instructor_Session_01_Introduction_to_Digital_Forensics_Acquisition.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Two lecture halves and then one long tool lab. Slides 1–8 are cover and instructor introduction.
"Part 1: introduction to digital forensics" runs slides 8–39 — vocabulary (cybercrime, forensic
science, crime scene vs evidence), the three fundamentals, the three-phase evidence life cycle
(acquire → analyse → present), sources of evidence and volatility, then the five analysis steps
ending on forensic soundness. "Part 2: data acquisition" runs slides 40–50 and is short: why we
acquire, order of volatility, acquisition methods, image formats, sparse acquisition, write
protection. From slide 51 to slide 69 the deck is a **single continuous lab** built almost
entirely around FTK Imager, with KAPE bolted on at the end. Slide 70 closes on the deck's refrain
that forensics is a procedure, not a toolbox.

Roughly: **70 % lecture, 30 % lab** by slide count — but the lab slides carry the screenshots and
therefore nearly all of the reusable content. There is no case narrative and no evidence set; each
lab step is demonstrated against whatever disk happened to be attached to the presenter's machine.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–2 | Cover | `admin` |
| 3–6 | Instructor introduction and certification screenshots | `admin` |
| 7–8 | Session title; "Part 1" divider | `admin` |
| 9–15 | Cybercrime, forensic science, definition of digital forensics, crime scene vs evidence, public vs private investigations | `concept` |
| 16–20 | The three fundamentals (evidence, tools, scientific method); why the process is not the tool | `concept` |
| 21–27 | Digital evidence life cycle: acquisition, chain of custody, analysis, presentation | `concept` |
| 28–31 | Sources of digital evidence; volatile vs non-volatile; live vs static acquisition | `concept` |
| 32–39 | Five analysis steps: image → verify → preserve → analyse → validate; forensic soundness | `concept` |
| 40–45 | "Part 2" divider; what acquisition is, why we acquire, never work the first image, order of volatility, static vs dynamic | `concept` |
| 46–50 | Acquisition methods (disk-to-disk, disk-to-image), RAW vs proprietary formats, source/destination swap warning, sparse method, write protection | `concept` |
| 51–52 | Lab framing and objective list | `admin` |
| 53 | Portable FTK Imager on removable media | `demo` |
| 54–57 | Physical disk image, verify-on-creation, and independent hash check | `lab` |
| 58–59 | RAM capture; "can we verify a RAM image?" | `lab` |
| 60–61 | Logical drive image and logical folder (AD1) image | `lab` |
| 62–66 | Mounting the image three ways: FTK Imager, Arsenal Image Mounter, OSFMount | `lab` |
| 67–69 | KAPE targeted triage collection | `lab` |
| 70 | Closing message | `admin` |

## 2 · Labs and demos — what was actually run

Slide 52 lists eight lab objectives. **Two of them are never shown**: "Imaging using linux dd
utility" and the HashCalc half of "Validating image using FTK imager and HashCalc". Everything
below is what the screenshots actually evidence.

### Build a portable FTK Imager · slide 53
**Tools:** FTK Imager (version shown elsewhere in the deck as 4.7.3.81).
**Evidence used:** none — this is preparation of the responder's own kit.
**Steps as demonstrated:**
1. The FTK Imager program directory is copied wholesale onto removable media and run from there:
   `<removable>:\FTK Imager\FTK Imager.exe`, alongside its DLL set (`ADSHARED*.dll`,
   `ewfsconnect22.dll`, `libbfio.dll`, `libeay32.dll` and the Boost runtime).
2. Demonstrated visually only — no command is shown; there is no installer step on the slide.

**What the output showed:** an Explorer view of ~58 files, the largest being the imager
executable at about 4 MB, dated 10/31/2024 — i.e. an FTK Imager build of late 2024.
**What this lab teaches:** the responder brings the tool to the machine on their own media rather
than installing software on the suspect host. The deck never states that rationale — say it aloud.

### Physical disk image with FTK Imager, and verification · slides 54–57
**Tools:** FTK Imager 4.7.3.81; Windows PowerShell.
**Evidence used:** a 1 GB VMware virtual SCSI disk attached to the presenter's VM, addressed as
`\\.\PHYSICALDRIVE1`; output written to removable media as `hard drive` (raw/dd).
**Steps as demonstrated:**
1. `File ▸ Create Disk Image` ▸ source type **Physical Drive** ▸ select `\\.\PHYSICALDRIVE1`.
2. In *Select Image Destination*: destination folder, *Image Filename (Excluding Extension)* =
   `hard drive`, *Image Fragment Size (MB)* = `1500`, *Compression* = `0`, *Use AD Encryption*
   unticked. The dialog's own note is captured: `For Raw, E01, and AFF formats: 0 = do not fragment`.
3. On the *Create Image* summary: **Verify images after they are created** ticked;
   *Precalculate Progress Statistics* and *Create directory listings* left unticked. Image
   destination shown as `<removable>:\hard drive [raw/dd]`.
4. Independent re-hash of the finished image from PowerShell:
   ```
   Get-FileHash MDS
   ```
   `⚠ OCR — verify before use.` The prompt OCR's as `IPS F:\>` (read `PS F:\>`) and `MDS` is
   almost certainly `MD5`. **As printed:** `Get-FileHash MDS`. **Likely intended:**
   `Get-FileHash '.\hard drive.001' -Algorithm MD5` — the result grid on the same screenshot has
   columns `Algorithm Hash Path` with `MD5` in the first column and the image file in the third,
   which is what `-Algorithm MD5` produces. Recover the real line from the slide.

**What the output showed:**
- *Drive/Image Verify Results* reported `Sector count 2097152`, an MD5 and a SHA-1 row each with
  *Computed hash*, *Report Hash* and `Verify result: Match`, and
  `Bad block(s) in image: No bad blocks found in image`.
- The FTK Imager text log (slide 57) gives the geometry block — `Tracks per Cylinder: 255`,
  `Sectors per Track: 63`, `Bytes per Sector: 512`, `Sector Count: 2,097,152`,
  `Drive Model: VMware, VMware Virtual S SCSI Disk Device`, `Drive Interface Type: SCSI`,
  `Removable drive: False`, `Source data size: 1024 MB` — then
  `Acquisition started` / `Acquisition finished` (about 63 seconds apart), a `Segment list:` with
  a single file, and `MD5 checksum: … : verified` / `SHA1 checksum: … : verified`.
- The PowerShell MD5 matched the value in the log — that comparison is the point of slide 57.

⚠ **Do not reuse the literal digests.** The same MD5 and SHA-1 are printed on slides 56 and 57 and
the OCR resolves them differently each time (a `0` renders as another character, an `f` as `#`,
and the SHA-1 tail is truncated in one pane). Regenerate the hashes on the course lab image.
⚠ The image extension is likewise unreliable: the log pane shows the segment as `.001` in one
place and `.E01` in another, while the destination was chosen as `raw/dd`. Read it off the slide.

**What this lab teaches:** verify-on-creation is FTK Imager checking its own write-then-read round
trip; the PowerShell hash is a *second, independent* computation. Both are worth doing and neither
re-reads the source drive — see
[`Module_01` §2 · FTK Imager acquisition & verification log](../Module_01_Data_Acquisition.md).

### RAM capture · slides 58–59
**Tools:** FTK Imager.
**Evidence used:** the live memory of the presenter's own workstation.
**Steps as demonstrated:**
1. `File ▸ Capture Memory…` — the screenshot is of the open *File* menu with the whole command
   list visible (`Add Evidence Item`, `Add All Attached Devices`, `Image Mounting`,
   `Create Disk Image`, `Export Disk Image`, `Export Logical Image (AD1)`,
   `Add to Custom Content Image (AD1)`, `Create Custom Content Image (AD1)`, `Decrypt AD1 image`,
   `Verify Drive/Image`, `Obtain Protected Files`, `Detect EFS Encryption`, `Export Files`,
   `Export File Hash List`, `Export Directory Listing`).
2. **The capture dialog itself is not shown.** The destination path, the *Include pagefile* and
   *Create AD1 file* options and the resulting `.mem`/`.ad1` are all off-slide. This step is
   demonstrated visually only and must be rebuilt for the course lab.
3. Slide 59 is a single question — "Can we verify ram image ?" — with **no answer on the slide**.
   The answer was given verbally. For the rebuild: hash the dump after capture so custody of the
   *file* is provable, but you cannot re-hash the source, because memory changed while you read it;
   a RAM image is never bit-identical to any later read of the same machine.

**What this lab teaches:** volatile capture first, and the limit of hash verification when the
source will not hold still.

### Logical drive and logical folder images · slides 60–61
**Tools:** FTK Imager.
**Evidence used:** an NTFS volume, shown in *Select Drive* as `E:\ - New Volume [NTFS]`.
**Steps as demonstrated:**
1. `Create Disk Image` ▸ *Select Source* ▸ **Logical Drive** ▸ pick the volume from
   *Source Drive Selection*. The source list's own caption is captured:
   `(logical file-level analysis only; excludes deleted, unallocated, etc.)`.
2. Repeat with *Select Source* ▸ **Contents of a Folder**. FTK Imager's warning box is captured in
   full and is the best single artefact on the slide: the image "will include only logical files.
   It will not include any file system metadata, deleted files, unallocated space, etc. It cannot
   be converted to a sector image (such as .E01) because it does not store sector information."
3. Slide 61's own bullet: "Note: this will not contain either hidden files or deleted data".

**What this lab teaches:** the three source types are three different evidentiary scopes, and the
AD1 folder image is the narrowest. See
[`Module_01` §2 · AD1 logical image](../Module_01_Data_Acquisition.md).

### Mounting the image read-only — three tools · slides 62–66
**Tools:** FTK Imager; Arsenal Image Mounter; PassMark OSFMount.
**Evidence used:** the raw image produced earlier, referenced on the slides as
`<drive>:\hard drive.001`.
**Steps as demonstrated:**
1. **FTK Imager** — `File ▸ Image Mounting`. Settings shown: *Mount Type* `Physical & Logical`,
   *Drive Letter* `Next Available (F:)`, *Mount Method* `Block Device / Read Only`, *Write Cache
   Folder* left at default, then *Mount*. The mounted image appears in the *Mapped Image List*.
2. **Arsenal Image Mounter** — the *Mount options* dialog is captured with all four modes and
   their explanatory text: `Disk device, read only`; `Disk device, write temporary` (writes go to
   a differencing overlay, "required for launching virtual machines"); `Disk device, write
   original` — labelled in the tool's own words "Caution, modifications will be written to the
   original disk image"; and `Windows file system driver bypass, write original`. Also shown:
   `Sector size: 512`, `Create "removable" disk device` (emulates a USB stick, "may facilitate the
   successful mounting of images containing partitions rather than complete disks"), and
   `Automatically remount at Arsenal Image Mounter startup`.
3. Slide 64 shows the result in Explorer — the mounted volume appears beside the real disks as
   `New Volume (F:)`, `993 MB free of 0.98 GB`.
4. **OSFMount** — *Mount Virtual Disk*, step 1 of 4: `Disk image file (.img, .dd, .vmdk, .E01, …)`
   ▸ browse to the image ▸ *Next*. Slide 66 shows the *Mounted virtual disks* grid with
   `\\.\PhysicalDrive5`, `Emulation: Physical`, `Type: Disk`, `Size: 1 GB`,
   `Properties: Read-only`, plus *Dismount all* and *Exit*.
   ⚠ The device number OCR's as `\\\PhysicalDrives` — read the digit off the slide.

**What this lab teaches:** every mount is a decision about write access, and the tools phrase that
decision differently. Arsenal's "write original" option is the whole lesson on one screen: a mount
can destroy the evidence, and nothing stops you.

### KAPE targeted triage collection · slides 67–69
**Tools:** gkape (the KAPE GUI) v1.3.0.2, by Eric Zimmerman.
**Evidence used:** the live `C:` of the presenter's own workstation; output to removable media.
**Steps as demonstrated:**
1. In gkape: tick *Use Target options*; *Target source* `C:`; *Target destination* on removable
   media; select the compound target `KapeTriage` from the target list; `--gui` is implied by
   running the GUI. Module options left unticked (`Modules selected: 0`).
2. The *Current command line* box on slide 68 reads:
   ```
   . \kape.exe --tsource C: --tdest F:\ --tflush —-target KapeTriage --gui «
   ```
   `⚠ OCR — verify before use.` **As printed** above. **Likely intended:**
   `.\kape.exe --tsource C: --tdest F:\ --tflush --target KapeTriage --gui` — the OCR has inserted
   a space after the leading dot, rendered the `--` of `--target` as an em dash plus hyphen, and
   picked up a trailing guillemet from the text-box scroll arrow.
3. Slide 69 shows the same run with a named destination. The console echoes:
   ```
   command line:  --tsource C: --tdest F:\EVIDENCE --tflush --target KapeTriage --gui
   ```
   and the GUI box beneath it OCR's far worse:
   ```
   \kape.exe --tsource Cr tdest PEVIDENCE “tush target Raperniage “Gur
   ```
   `⚠ OCR — do not use this second form at all` — `Cr` is `C:`, `PEVIDENCE` is `F:\EVIDENCE`,
   `“tush` is `--tflush`, `Raperniage` is `KapeTriage`, `“Gur` is `--gui`. The console echo on the
   same slide is the trustworthy copy.

**What the output showed:** `KAPE version 1.3.0.2, Author: Eric Zimmerman`; `KAPE directory:
F:\KAPE`; the destination directory being flushed and recreated; `Found .4 targets. Expanding
targets to file list…` (⚠ the digit before `4` did not OCR); repeated
`Target ApplicationEvents with Id 2da16dbf-ea47-4a8e-a0ef-fc442c3109ba already processed.
Skipping!` — i.e. the compound target pulls the same sub-target through several paths and KAPE
de-duplicates; and the status bar `Targets available: 257 | Targets selected: 1 |
Modules available: 272 | Modules selected: 0`.

**What this lab teaches:** targeted collection when there is no time to image. Slide 67 states the
caveat correctly — "Must be used only when needed, for example if you don't have time to image an
entire hard drive." Pair it with
[`Module_01` §2 · Targeted (sparse) triage collection set](../Module_01_Data_Acquisition.md): what
is absent from a triage set is *uncollected*, not *absent from the disk*. The deck does not say
this; it is the most important sentence to add.

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| FTK Imager portable kit | `<removable>:\FTK Imager\` — executable plus ~58 DLLs | Run the imager from responder media, not from the suspect host | [`Module_01` §3 · FTK Imager](../Module_01_Data_Acquisition.md) |
| Source physical device | `\\.\PHYSICALDRIVE1` | The imaging source selected in *Physical Drive* mode | [`Module_01` §2 · Raw / `dd` image](../Module_01_Data_Acquisition.md) |
| Raw image set | `<dest>:\hard drive.001` (log also shows `.E01` — ⚠ inconsistent OCR) | Bit-for-bit image, fragment size 1500 MB, compression 0 | [`Module_01` §2 · Raw / `dd` image](../Module_01_Data_Acquisition.md) |
| FTK Imager acquisition log | Written beside the image, same base name, `.txt` | Geometry, source model/interface, acquisition start/finish, MD5 and SHA-1 with `: verified` | [`Module_01` §2 · FTK Imager acquisition & verification log](../Module_01_Data_Acquisition.md) |
| Drive geometry as reported | `255` tracks/cylinder · `63` sectors/track · `512` bytes/sector · `2,097,152` sectors · `1024 MB` | Proves what the interface reported, not what the platter holds | [`Module_01` §2 · FTK Imager log](../Module_01_Data_Acquisition.md) · [`Module_03` §1 · CHS and LBA](../Module_03_Disks_and_File_Systems.md) |
| Logical volume source | `E:\ - New Volume [NTFS]` | *Logical Drive* image scope | [`Module_01` §2 · AD1 logical image](../Module_01_Data_Acquisition.md) |
| AD1 folder image warning | FTK Imager dialog text, quoted in §2 above | States on-screen that metadata, deleted files and unallocated space are excluded | [`Module_01` §2 · AD1 logical image](../Module_01_Data_Acquisition.md) |
| FTK mount method | `Block Device / Read Only`, drive letter `Next Available (F:)` | Read-only mount of a raw image | [`Module_01` §2 · Write blocker and its proof trail](../Module_01_Data_Acquisition.md) |
| Arsenal mount modes | `Disk device, read only` · `write temporary` · `write original` · `Windows file system driver bypass, write original`; `Sector size: 512` | The four write postures a mount can take | [`Module_01` §2 · Write blocker and its proof trail](../Module_01_Data_Acquisition.md) |
| OSFMount mounted device | `\\.\PhysicalDrive<n>`, `Emulation: Physical`, `Properties: Read-only` | Presents an image file as a physical device | [`Module_01` §3 · Tools](../Module_01_Data_Acquisition.md) |
| KAPE install root | `<removable>:\KAPE\kape.exe` | Triage collector run from responder media | [`Module_01` §3 · KAPE](../Module_01_Data_Acquisition.md) |
| KAPE target | `KapeTriage` (compound target); `Targets available: 257`, `Modules available: 272` | The artefact selection actually collected | [`Module_01` §2 · Targeted (sparse) triage collection set](../Module_01_Data_Acquisition.md) |
| KAPE destination | `<dest>:\EVIDENCE`, flushed and recreated by `--tflush` | Collection output tree | [`Module_01` §2 · Targeted (sparse) triage collection set](../Module_01_Data_Acquisition.md) |

**No registry keys are named anywhere in this deck** — notably not
`StorageDevicePolicies\WriteProtect`, even though slide 50 insists on write-protected acquisition.

## 4 · What this deck adds beyond the INE material

- **KAPE, with a working command line.** `Module_01` §7 records this as gap **G6** — INE teaches
  sparse acquisition as a concept and names no tool, because KAPE post-dates the courseware. The
  deck closes that gap with a real invocation, the target name, and console output showing target
  de-duplication and the 257/272 catalogue counts. This is the single most valuable thing in the
  deck and should be lifted straight into S2.
- **Arsenal Image Mounter and OSFMount.** Neither appears in INE units 1–2 or in `Module_01` §3.
  Arsenal's four-way mode dialog is a better teaching aid for write protection than anything in
  the INE material, because it puts "write original" on screen as a selectable option.
- **The portable-imager pattern.** Running FTK Imager from removable media is standard practice
  that INE never states; the deck shows it as step one of the lab.
- **Windows-native verification.** INE demonstrates hashing with Linux `md5sum`/`sha512sum` and
  with HashCalc; the deck uses PowerShell `Get-FileHash`, which is what students will actually
  have on a Windows analysis box. Adopt it.
- **A continuous lab.** INE units 1–2 are read-then-watch. The deck's slides 51–69 are one
  unbroken sequence — image, verify, capture RAM, image logically, mount, triage — which is
  already close to the shape S2 needs.
- **Explicit "don't swap source and destination"** (slide 48), called out as a very common
  mistake. INE covers destination preparation but not this failure mode as bluntly.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted (INE covers it, the deck does not):**
- **Write blockers.** Slide 50 requires write-protected acquisition and then never shows a
  hardware blocker or the software fallback. `Module_01` §2 covers both, including the
  `StorageDevicePolicies\WriteProtect` registry method and the requirement to *prove* the block on
  a scratch stick.
- **`dd` and `dc3dd`.** Listed as a slide-52 lab objective; never demonstrated.
- **HashCalc.** Same — half of a slide-52 objective, never shown.
- **Order of volatility.** Slide 44 is one bullet ("you must follow the order of volatility") with
  no ordered list, no RFC 3227 reference and no worked example.
- **Chain of custody as a document.** Slide 25 shows a blank form image; no field is walked
  through, no hand-off is role-played, no re-hash-at-transfer step is taught.
- **E01/EWF internals** — segments, chunk CRCs, the embedded acquisition hash, compression cost.
  Slide 47 names EWF, IDIF and sgzip and stops.
- **Admissibility, legal authority and the expert-witness material** from unit 1.
- **Volatility (the memory framework), `bulk_extractor`, and the BriMor Live Response
  Collection** — all in `Module_01` §2/§3, none in the deck.
- **Full-disk encryption at acquisition**, anti-forensics, and time-zone/timestamp recording.
- **Any case narrative.** There is no carry-through incident, so no lab step is motivated by a
  question; students image a disk because the slide says to.

**Disagreement to carry forward:** slide 35 defines the "Triage method" as *"creating three images
of the evidence, as you may not have access to the evidence again"*. That is not what triage means
in this field, and the same deck uses the word correctly on slide 67 (targeted collection when
time is short). **INE is the course's truth here** — triage is scope reduction, not image
duplication. The *practice* slide 35 describes (make more than one copy while you still have the
exhibit) is sound; only the label is wrong. Teach it as "redundant copies", never as "triage".

**Resources cited on the slides** — recorded verbatim, `unverified`, not vouched for:
- `https://www.kroll.com/kape` — from the KAPE console banner, slide 69. `unverified`
- Slide 3 also cites the presenter's personal blog (a `gitbook.io` site) and personal YouTube
  channel. Both are deliberately **not reproduced here** — presenter personal data; see §6.
- No other URL appears anywhere in the 70 slides. There is no reading list.

## 6 · Cautions before reuse

- **Screenshots carrying the presenter's personal data — slides 1, 3, 4, 5, 6, 53, 66, 69.**
  None of these may be reused as-is.
  - **1, 3** — presenter name, education, certification list, personal blog and personal video
    channel links.
  - **4, 5, 6** — three certificate images showing full name, an EC-Council certification number,
    a Belkasoft certificate ID and issue/expiry dates. Replace with a plain credentials line.
  - **53** — Explorer window showing the presenter's own Quick Access tree and personal working
    folders. It also shows a pinned `mimikatz-master` folder: quite apart from the privacy issue,
    do not put an offensive-tooling folder on screen while teaching evidence handling.
  - **66** — Explorer sidebar with the presenter's pinned course and working folders.
  - **69** — the KAPE console banner prints `Machine name:` and `User:` for the presenter's own
    workstation. Regenerate this screenshot on the course lab VM; the interesting content (target
    de-duplication, the 257/272 counts, the OS build) survives regeneration.
  - Slide 57 additionally shows real acquisition timestamps from the presenter's VM (late February
    2025). Harmless, but regenerate for consistency with the course evidence set.
- **Tool and platform versions have moved since early 2025.**
  - FTK Imager 4.7.3.81, files dated 10/31/2024. Now an Exterro product; confirm the current build
    and its download location before the lab, and re-take slides 54–62 against it.
  - KAPE 1.3.0.2 with `Targets available: 257`, `Modules available: 272`. Both catalogues grow
    continuously — the counts on slide 69 will not match a current install, and the modern
    default target is `!SANS_Triage`, not the older `KapeTriage`. Verify the target name and the
    full command line against the installed version before class.
  - The console banner shows the host OS as `(10.0.19043)` — Windows 10 21H1, out of support.
    Rebuild the lab VM on a supported build.
  - Arsenal Image Mounter and OSFMount dialogs have both changed; re-shoot slides 63–66.
- **OCR that could not be resolved and matters.**
  - The PowerShell line reads `Get-FileHash MDS`; the real invocation must be read off slide 57.
  - **Every hash digest in this deck is unreliable.** The same MD5/SHA-1 pair is printed three
    times across slides 56 and 57 and resolves differently each time. Regenerate, never transcribe.
  - The image extension alternates between `.001` and `.E01` in the OCR of a single log pane while
    the format chosen was `raw/dd`.
  - Slide 68's `--target` renders as an em dash plus hyphen; slide 69's GUI command box is garbled
    beyond use (use the console echo on the same slide instead).
  - `Found .4 targets` on slide 69 has lost a leading digit.
  - The OSFMount device number renders as `\\\PhysicalDrives`.
- **Structural gaps to fill before this becomes S1/S2.** No write-blocker demonstration, no chain
  of custody walk-through, no `dd`, no answer on screen to slide 59's RAM-verification question,
  and no evidence set — every lab runs against an ad-hoc local disk. S1 and S2 need EVI-SRC01 and a
  chain-of-custody form to hang all of this on.
