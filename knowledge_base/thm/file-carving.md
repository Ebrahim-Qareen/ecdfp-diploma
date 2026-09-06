---
room: File Carving
url: https://tryhackme.com/room/filecarving
module: File System Analysis (Section 1 of Advanced Endpoint Investigations)
feeds: S4 — `S4-09` file carving (direct hit) · `S4-03` slack space.
       Carries the **most serious safety finding of the whole batch** (§3, CVE-2022-4510)
       and confirms the scalpel abandonment from `_TOOL_CURRENCY_2026-08-28.md`.
difficulty / time: Medium · **90 min** · 7 tasks · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 7 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

Recovering files **from content alone**, with no filesystem metadata to help — the technique you
fall back on when the volume was formatted, the records were wiped, or the file was never in a
directory to begin with. Manual carving by header/footer in a hex editor and with `dd`, then
automated carving with foremost, scalpel and binwalk, then an unguided capstone.

The room's cleanest idea, and the one worth taking whole, is the **explicit contrast between data
recovery and file carving**: recovery reads the filesystem's own bookkeeping and dies when that
bookkeeping is gone; carving ignores it entirely and reads the bytes. That distinction is exactly
what `S4-09` needs to open with, and it explains *why* carving sits after `S4-07` in our map.

The lab is **Ubuntu**, which suits us — Part 6 already provisions FOR-LNX01 for `dd`, foremost,
PhotoRec and bulk_extractor.

## 2. Artifacts — one 6-box block each

### 2.1 File signatures — headers, footers, magic bytes

- **What it is** — the fixed byte sequences that begin (and often end) a file format, independent
  of any filesystem.
- **Where it lives** — at the first bytes of the file's data, wherever on the medium that data sits.
  The room's reference table, which converts directly into our cheat sheet:
  | type | header | footer | note |
  |---|---|---|---|
  | JPEG | `FF D8 FF E0` (commonly `FF D8 FF`) | `FF D9` | |
  | PNG | `89 50 4E 47 0D 0A 1A 0A` | `49 45 4E 44 AE 42 60 82` | chunk-structured |
  | PDF | `25 50 44 46` (`%PDF`) | `25 25 45 4F 46` (`%%EOF`) | |
  | DOCX | `50 4B 03 04` | `50 4B 05 06` | **it is a ZIP** |
  | GIF | `47 49 46 38 39 61` / `…37 61` | `00 3B` | GIF89a / GIF87a |
  | ZIP | `50 4B 03 04` | `50 4B 05 06` | |
- **What it proves** — that data of a given format **begins** at this offset. With a footer, it
  bounds the file, and the byte range between them can be extracted.
- **What it does NOT prove** — 🔴 **the header does not prove the file is what it claims**, and more
  importantly for us: **DOCX and ZIP share a signature**, so a signature match narrows the format
  family, not the format. The room's own capstone question turns on exactly this — it asks for the
  "actual file type" of something binwalk labelled XML. A header also says nothing about whether
  the bytes in between are intact, complete, or belong to one file.
- **How to parse it** — search for the hex sequence in **Okteta**, note the start and end offsets,
  convert to decimal, then either select-and-save the range or:
  ```
  dd if=<image> of=<out>.png bs=1 skip=<start_decimal> count=<end - start>
  ```
  **`count` is `ending offset − starting offset`, in bytes.** That arithmetic is the whole lesson.
- **Anti-forensics / false-positive caveat** — the room mentions false positives under "technical
  barriers" but does not dwell. Ours: a signature is three or four bytes and **occurs by chance in
  large images constantly**. Every carve must be validated by opening the file or reading its
  metadata — which is why §2.4 matters. Headers are also trivially forged to disguise a file type.

### 2.2 Unallocated space after a format or delete

- **What it is** — the data that survives when the filesystem's references to it are removed.
- **Where it lives** — anywhere on the medium not currently allocated. The room's tell for a
  formatted drive: **the MBR is present but its partition table is empty**, while file fragments
  remain further into the image.
- **What it proves** — that a file **existed** and, if enough of it survives, what it contained. The
  room mounts `Challenge3_deleted_disk.img` and finds only `lost+found` — then carves real files
  out of it. That contrast, run live, is the most persuasive demonstration in the room.
- **What it does NOT prove** — **when** the data was written or deleted, or by whom. Carving
  recovers content and loses *all* metadata: no filename, no timestamps, no path. The room states
  this obliquely; we should state it flatly. It also cannot prove the file is complete — only that
  the recovered bytes parse.
- **How to parse it** — foremost / scalpel / PhotoRec / binwalk (see §3).
- **Anti-forensics / false-positive caveat** — data survives **only until overwritten**. A failed
  carve is not evidence of secure wiping, and a successful one is not evidence of carelessness.

### 2.3 Slack space

- **What it is** — the unused remainder of an allocated cluster, which may still hold bytes from a
  previous occupant.
- **Where it lives** — between the end of a file's real data and the end of its last cluster.
- **What it proves** — residual content of a **previously stored** file. The room's scenario 2 finds
  an MPEG transport stream sitting in the slack of an ext4 image.
- **What it does NOT prove** — any association between the residual data and the file that now owns
  the cluster. **They are unrelated by definition** — one merely inherited the other's space. Reading
  slack content as belonging to the current file is a serious analytical error and the room does not
  warn against it.
- **How to parse it** — `binwalk <image>` to list embedded signatures with decimal and hex offsets,
  then the hex editor to find the true start of the stream, then `binwalk -e` to extract.
- **Anti-forensics / false-positive caveat** — slack is small and constantly recycled; its contents
  are fragmentary by nature. The room's own binwalk output is a good illustration of noise —
  "TROC filesystem", "MySQL ISAM index file", "device tree image" in a disk image are **almost
  certainly false positives**, and the room never says so. **Teach that list as a false-positive
  exercise.**

### 2.4 Embedded metadata (EXIF and friends)

- **What it is** — descriptive data carried inside the file itself.
- **Where it lives** — within the file's own structure. The room distinguishes three kinds usefully:
  **embedded** (EXIF in a JPEG — camera settings, location, timestamps) · **extended** (OS-held file
  attributes) · **external** (logs and database records about the file).
- **What it proves** — for a carved file, metadata is often **the only surviving context**, since
  carving discards filesystem metadata entirely. It also **validates the carve**: if ExifTool parses
  it, the byte range was right.
- **What it does NOT prove** — embedded metadata is written by the creating application and is
  freely editable. EXIF timestamps and GPS are claims, not measurements. And the `File Modification
  Date/Time` ExifTool reports on a carved file is **the date you carved it**, not anything about the
  original — a trap the room's own sample output walks right past.
- **How to parse it** — `exiftool <file>`.
- **Anti-forensics / false-positive caveat** — metadata is routinely stripped, and its absence means
  nothing. See §3 for a version problem with the room's ExifTool.

### 2.5 Fragmented file remnants

- **What it is** — a file whose data is not in contiguous blocks.
- **Where it lives** — scattered across the medium, in an order only the (now missing) filesystem
  knew.
- **What it proves** — potentially the file, if the fragments can be ordered correctly.
- **What it does NOT prove** — 🔴 **this is carving's hard limit and the room is honest about it.**
  Header-footer carving assumes contiguity. Where a file is fragmented you must locate the pieces,
  reassemble them using knowledge of the format, and **accept partial recovery where data is
  simply gone**. A partially recovered file must never be presented as the file.
- **How to parse it** — no tool solves this reliably; the room correctly calls it "as much an art as
  a science". Scalpel's two-pass design claims some fragmentation handling.
- **Anti-forensics / false-positive caveat** — a carve that silently runs from a real header past
  the true end into unrelated data produces a file that **opens** and is **wrong**. Foremost's
  maximum-file-size setting exists precisely to bound this, and it means every carved file has a
  plausible-but-unverified tail.

### 2.6 The MBR as a formatting indicator

- **What it is** — the first sector, read not for partition data but for its *absence*.
- **Where it lives** — sector 0.
- **What it proves** — the room's inference: MBR present, **partition table empty**, but file
  fragments deeper in the image ⇒ the volume was **formatted, not securely wiped**. A neat,
  cheap triage judgement.
- **What it does NOT prove** — which format operation, when, or by whom. And an empty partition
  table has innocent causes (a freshly prepared disk, a non-partitioned volume). It is a lead.
- **How to parse it** — hex editor at offset 0.
- **Anti-forensics / false-positive caveat** — a **secure** wipe leaves the same empty table with no
  recoverable fragments; the difference between "formatted" and "wiped" is what you find *after*
  sector 0, not in it.

## 3. Tools and commands

| tool | version the room uses | exact command | what it outputs |
|---|---|---|---|
| **Okteta** | not stated | GUI; `Edit > Go to Offset…`, offset coding **decimal** | raw hex + ASCII |
| **`dd`** | n/a | `dd if=<img> of=<out> bs=1 skip=<start> count=<end-start>` | the carved byte range |
| **ExifTool** | **11.88** (in the room's own output) | `exiftool <file>` | embedded metadata |
| **binwalk** | not stated | `binwalk <image>` | signature list, decimal + hex offsets |
| **binwalk** | not stated | `binwalk -e <image>` | ⚠️ extraction — **see the CVE below** |
| **foremost** | not stated | `foremost -i <img> -o <dir> -c /etc/custom_foremost.conf` | carved files in per-type subdirs |
| **foremost** | not stated | `foremost -t pdf,jpg,png -i <img> -o <dir> -c <conf>` | restricted to named types |
| **scalpel** | not stated | `scalpel <img> -o <dir> -c /etc/scalpel/scalpel.conf` | carved files |
| PhotoRec / EnCase / hex editors | not stated | described only, not used | — |

### CURRENCY CHECK — run 2026-08-28, primary sources

| item | result |
|---|---|
| 🔴🔴 **`binwalk -e` on evidence is a documented RCE risk — CVE-2022-4510** | Path traversal (CWE-22) in binwalk's PFS extractor, **binwalk 2.1.2b–2.3.3**, CVSS **7.8 HIGH**. A crafted image extracted with **`-e`** escapes the output directory and writes a malicious binwalk plugin into `$HOME/.config/binwalk/plugins`, which **executes on the analyst's next binwalk run** — code execution on the examiner's workstation, triggered by the act of examining evidence. **The room instructs students to run `binwalk -e` on supplied images and says nothing about this.** |
| binwalk v3 hardening | the Rust rewrite adds a `Chroot` struct, `safe_path_join`, `sanitize_path` (strips `..`) and a symlink check — real structural improvement over v2's per-plugin extraction. **Use v3.** |
| 🔴 **binwalk extraction paths have changed** | v2: `_<file>.extracted/` in the CWD. **v3: `extractions/<file>.extracted/<HEXOFFSET>/`** — no leading underscore, nested, one subdir per offset. **The room's `ls _Challenge2_slack_space.img.extracted/` is v2-only and will fail on v3.** |
| binwalk current | **3.1.0 (Rust), 31 Oct 2024**, MIT. New `-c/--carve`; `-d/--directory` for output. ⚠️ **`-d` meant recursion depth in v2** — a v2-era handout using `-d 3` now creates a directory called `3`. |
| ⚠️ **`pip install binwalk` gives 2015 software** | PyPI is frozen at **2.1.0 (Jan 2015)**. Install v3 from cargo or the GitHub release, never pip. The old usage wiki is also gone — any link to it is dead. |
| 🔴 **scalpel is self-declared unmaintained** | Canonical repo `sleuthkit/scalpel`; README: *"It is not being actively maintained"*, *"No official releases are being made"*, no release tags. Ubuntu ships `1.60+git20240110` while the README cites 2.0 — irreconcilable. **Second confirmation of the finding in `_TOOL_CURRENCY_2026-08-28.md`.** |
| 🔴 **scalpel does NOT auto-load `/etc/scalpel/scalpel.conf`** | The man page: without `-c`, it uses **`scalpel.conf` in the current directory**. Ubuntu ships the `/etc` copy but it is not default. The room passes `-c` explicitly, so its command works — **but any lab of ours claiming a default config path is wrong and students get zero carves.** |
| ⚠️ **both carvers ship with all patterns commented out** | scalpel's README says the default config has every pattern disabled and must be edited first. Budget lab time. |
| ⚠️ **both carvers refuse a non-empty output directory** | The room warns about this for foremost and scalpel. Real, and it bites on every re-run. |
| ✅ foremost switches | `-i`, `-o`, `-c`, `-t` **all confirmed current**. Config order: `./foremost.conf` then `/etc/foremost.conf`. Note the man page is **section 8** — `man 1 foremost` fails. |
| 🔴 **ExifTool 11.88 is ~6.5 years old** | Released **20 Feb 2020**; current is **13.55 production / 13.59 development (2026)**. If the room's VM really ships 11.88, six years of format support are missing — modern HEIF/AVIF, current camera raw, video metadata. **Teach the production version (13.55), not the headline dev number.** |
| ⚠️ **"EnCase Forensic" no longer exists under that name** | OpenText: *"OpenText Forensic is the same product as EnCase Forensic… renamed to align with the OpenText cybersecurity portfolio."* Newest confirmed **OpenText Forensic CE 25.3**; licensing is **one-year term-based**, not perpetual. Any slide saying "EnCase Forensic v8, perpetual dongle" is wrong on three counts. |
| ✅ Okteta | **0.26.27 (5 May 2026)**, GPL-2.0/3.0, healthy, in Ubuntu **universe** (needs enabling). |
| Room's version claims | **none stated for any tool** — eighth room running. |

## 4. Evidence used

- Four images on an Ubuntu lab VM under `/home/ubuntu/Desktop/Carving_Challenges/`:
  `Challenge1_Manual_Carve_usb.img` (formatted USB, PNG to recover) ·
  `Challenge2_slack_space.img` (~1 GB ext4, media file in slack) ·
  `Challenge3_deleted_disk.img` (mounts empty, files carvable) ·
  `Carving_Capstone.dd`.
- **Not downloadable. No licence offered. Not reusable.**
- **Nothing to flag for `ecdfp-evidence` from the room itself.**

### ✅ But the same Tier 1 insight as room 6 applies, and more strongly

`S4-09` needs a carvable image. Per Part 5 we cannot synthesise E01/raw images as *evidence of a
compromise* — but **a carving target is not a compromise artifact**. It is a small volume with known
files written and then deleted or formatted, and we can build it ourselves in minutes:

| scenario | staging | teaches |
|---|---|---|
| formatted volume | write files, quick-format, do not wipe | `S4-09`, header/footer carving |
| deleted files | write, delete, do not overwrite | `S4-09`, foremost/PhotoRec |
| slack residue | large file → delete → small file in the same cluster | `S4-03` |
| **fragmented file** | force fragmentation, then carve | **the limit of carving — §2.5** |

The fourth is the one no THM room stages deliberately, and it is the one that teaches carving's
honest boundary. **Recommend `ecdfp-evidence` scope this alongside the FAT32 set from room 6** —
same construction method, same distribution, both Tier 1.

## 5. Lab design worth reusing

1. **🟢 Mount it first and show it empty.** Task 5 mounts `Challenge3_deleted_disk.img`, shows only
   `lost+found`, and *then* carves real files out of it. **Nothing else in the batch makes "the
   filesystem is not the data" as vivid.** One command, one lesson. Take it exactly.
2. **🟢 Manual before automated, with the arithmetic exposed.** Find header, find footer, subtract,
   `dd`. The student computes `count` themselves. That single subtraction is what makes the
   automated tools comprehensible rather than magic — and it is checkable in one line.
3. **🟢 The data-recovery vs file-carving contrast** (§1), given as two labelled lists — when each
   works, when each fails. This is the framing `S4-09` should open with.
4. Three scenarios of escalating difficulty — formatted volume → slack residue → deleted files —
   then an unguided capstone, matching room 6's shape.
5. The capstone asks for **"the actual file type"** of something a tool mislabelled. Excellent: it
   tests the §2.1 caveat rather than merely stating it.

### 🔴 What we must NOT copy — safety, again

**The room tells students to run `binwalk -e` on supplied disk images with no isolation guidance.**
Given CVE-2022-4510 that is a live risk, and it is the second safety defect in the S4 block after
room 6's "paste the recovered PowerShell into a terminal".

**Our version teaches the opposite as a first-class lesson:** extraction invokes dozens of
third-party unpackers on attacker-controlled input, so **`binwalk -e` is executing untrusted code**.
Run it in a disposable VM, unprivileged, never as root, never on the host holding the evidence
master, and on **v3**. That is a one-slide addition and it is the kind of judgement that separates
an analyst from a tool operator.

Also not to copy: presenting **scalpel** as current tooling (§3), and letting binwalk's obvious
false positives pass without comment (§2.3).

## 6. Question patterns

~15 questions across 7 tasks; the capstone carries 4.

- **Single-artifact discipline holds**, and several questions require **computation**, matching
  room 6's best trait: offsets, file sizes in KB, playback length in seconds, "starting,ending"
  offset pairs.
- **🟢 The best question in the room is a trap by design**: *"What is the actual file type of the
  file found in Question 1?"* — after binwalk reported it as XML. It teaches that a signature match
  is a hypothesis. **This is the closest the whole batch has come to a criterion-4 question that
  isn't about absence.** Adopt the pattern: have a tool report something, then ask what is actually
  true.
- **Still no explicit "cannot be determined" answer** — eighth room. Candidates this room hands us,
  both strong: *"From the carved PNG alone, can you determine when it was deleted?"* → **no**
  (carving discards all filesystem metadata) · *"Does the residual media file in slack belong to the
  file currently occupying that cluster?"* → **no** (§2.3).

## 7. Figures we would need to draw

Screenshots of Okteta and terminal output throughout. Three concepts need our own inline SVG:

| what is needed | our SVG spec (one line) |
|---|---|
| header–footer carving, and where it breaks | a byte ribbon with a header marker, a footer marker and the span between shaded "carved" — then the same ribbon with the file split into three separated fragments and the naive carve shown running straight past into unrelated data, captioned "contiguous assumed, fragmented in practice" |
| recovery vs carving | two paths to the same file — one reading the filesystem's directory/MFT/FAT and stopping dead at a "metadata destroyed" break, one reading raw bytes straight through — captioned "one asks the index, one reads the shelf" |
| what carving keeps and what it loses | a file card before and after: before = name, path, MACB timestamps, size, content; after = **content only**, everything else struck out — the point being that a carved file has no provenance |

The third is the most important for D7: a carved file is a *finding* with no timeline attached, and
students consistently over-read them. Never their images (D22).

## 8. Fit against our material

### ✅ Part 1's mapping is correct — third room in a row

Mapped to `S4` / `S4-09`. Correct.

### Rows this strengthens

- **`S4-09`** *"file carving — PhotoRec/foremost, and carving the staged archive"*, 25 min
  **[INVESTIGATION]**. The room supplies the signature table, the `dd` arithmetic, the foremost
  invocation and config model, and the mount-it-empty demonstration. **This row is now fully
  sourced.**
- **`S4-03`** slack — a second worked example, on ext4 rather than NTFS.
- **`S2-05`/`S2-07`** — `dd` usage, though see the currency file: GNU now points at **ddrescue** for
  damaged media.

### Tool substitutions `S4-09` must make

| room teaches | our row should teach | why |
|---|---|---|
| scalpel | **drop it** (mention as legacy only) | self-declared unmaintained, no releases |
| binwalk v2 conventions | **binwalk v3**, with the CVE lesson | v2 extraction paths are wrong; v2 has the traversal CVE |
| ExifTool 11.88 | **13.55 production** | six years of format support |
| EnCase Forensic | **OpenText Forensic** | renamed; term licensing |
| foremost | **keep** — but install via `apt`, never SourceForge | upstream dead, distro alive (per `_TOOL_CURRENCY`) |

`S4-09` already names **PhotoRec/foremost**, which — pleasingly — is the correct pair. **The row was
right before we checked.** Add binwalk as the embedded/slack tool with its safety caveat.

### Minutes

`S4-09` is 25 min against the room's 90. Same remedy as rooms 6 and 7: the manual offset arithmetic
and the `dd` extraction make excellent **homework** — they need only a small image, no VM, and the
answer is checkable. **S4 stays at 220. This room adds 0 rows.**

**S5 remains at 65 minutes overdrawn** (rooms 1–5). **S4 is sound across three rooms** — 6, 7 and 8
have collectively added zero minutes while fully sourcing `S4-06`, `S4-07`, `S4-08` and `S4-09`.

### Out of scope

The room's lab is Ubuntu and it recaps ext/inode structure. **That is analysis-platform Linux, not
Linux forensics** — Part 6 already provisions FOR-LNX01 for exactly this. The ext2/3/4 recap in
Task 2 is out of scope and should not be carried into `knowledge_base/`.

## 9. Links

- Room: <https://tryhackme.com/room/filecarving>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 1)
- Room's stated prerequisites: Linux File System Analysis, **FAT32 Analysis** (room 6),
  **NTFS Analysis** (room 7), EXT Analysis (out of scope).
- File-signature reference the room recommends: **GCK's File Signatures Table** — worth keeping as a
  linked resource for `S4-09` (link, never rehost — D22).
- **CVE-2022-4510** binwalk path traversal: <https://nvd.nist.gov/vuln/detail/CVE-2022-4510> ·
  advisory <https://github.com/advisories/GHSA-3cm8-v4mc-gppg>
- binwalk v3: <https://github.com/ReFirmLabs/binwalk> · ExifTool: <https://exiftool.org/> ·
  Okteta: <https://apps.kde.org/okteta/> · scalpel: <https://github.com/sleuthkit/scalpel>
- OpenText Forensic (formerly EnCase): <https://www.opentext.com/products/forensic>

END OF NOTE.
