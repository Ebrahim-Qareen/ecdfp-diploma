---
room: Diskrupt
url: https://tryhackme.com/room/diskrupt
module: File System Analysis — **challenge room** (Priority 2)
feeds: **S4 — this is the S4 capstone, already built.** Its four stated prerequisites are exactly
       our four S4 teaching rows, and its question chain is our session in order.
       Also **S1** (its premise is "modify the evidence") and **D19** (carry-through case design).
difficulty / time: **Hard** · 120 min · 1 task · Premium · 2,908 completions · 67 recommends
                   · carries a **Badge**
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: the room is a **single task** — scenario, prerequisites, lab instructions and
              **12 questions**. All read in full. 0 sections NOT READ.
              🔴 Room ships plaintext VM credentials — **deliberately not reproduced here (R8)**.
              Per Part 2, a Priority-2 room is extracted for **scenario shape and question
              design**, not walkthrough content — there is no walkthrough to extract. §2 below is
              therefore reconstructed **from the questions**, which is the only artifact evidence
              the room exposes.
---

## 1. What the room teaches

Nothing — deliberately. **It is an assessment**, and it is the closest thing in the whole path to
what `S4` should end with.

The scenario: an insider at a research firm is suspected of stealing a paper on quantum-resistant
cryptography and destroying the traces. *"An unexpected system failure left behind fragments of
critical evidence"*, and the student is handed one image, `challenge.001`, with six objectives:

> *Fix the damaged disk · Examine the partitions · Find evidence of access to sensitive research
> documents · If any files were deleted or tampered with · What are the hidden files on the disk ·
> Carve out important files deleted from the disk.*

**🟢🟢 Its four stated prerequisites are our four S4 rows, in our order**: MBR and GPT Analysis ·
FAT32 Analysis · NTFS Analysis · File Carving. **Someone else has already validated the S4
architecture we designed independently**, and built the capstone that sits on top of it. That is
worth more to us than any individual finding.

**🟢 And its best line is an instruction, not a fact:**

> *"Not all tools are required to solve this challenge. As it is in real-life cases, you must
> figure out which tools work best for the situation."*

**Tool selection as the assessed skill.** Seventeen teaching rooms handed students a command; this
one hands them a problem. **That sentence belongs in our capstone brief verbatim.**

**🔴 But its premise is a forensic error.** The first objective is *"Fix the damaged disk"*, and
the first question asks which bytes were corrupted — which the room expects students to establish
by **repairing the evidence image**. That is room 9's defect promoted from a step to a
**title**. See §5.

## 2. Artifacts — one 6-box block each

Reconstructed from the twelve questions; the room exposes no walkthrough. Each block is the
artifact a question **requires**, with our own 6-box treatment.

### 2.1 The MBR boot sector and its signature

- **What it is** — the first 512 bytes of the disk: bootstrap code (0x000–0x1BD), the four 16-byte
  partition table entries (0x1BE–0x1FD), and the **two-byte signature `55 AA` at 0x1FE**.
- **Where it lives** — LBA 0, sector 0, offset 0 of `challenge.001`.
- **What it proves** — that the disk is describable. Q1 (*"What are the corrupted bytes in the boot
  sector that caused the disk to be damaged?"*) is really asking **which bytes a tool needed and
  did not find** — almost certainly the `55 AA` signature, since its absence is what makes every
  partition tool refuse the image while the partition table itself sits intact two bytes earlier.
- **What it does NOT prove** — 🔴 **that a missing signature means damage.** `55 AA` is absent by
  design on a great many things — a partitionless volume image, a raw filesystem dump, a carved
  fragment. **"The tool refused to open it" is a tool state, not a finding about the disk.**
  ⚠️ And a *valid* signature proves nothing either: two bytes are trivially reinstated by anyone
  wanting the disk to look intact.
- **How to parse it** — read the first sector in a hex viewer and check offset **0x1FE**; or
  `xxd -l 512 challenge.001`; or let `mmls` fail and read *why*. 🟢 **Note that all three of those
  are read-only** — see the caveat.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **you do not need to repair anything to answer
  this question, and you should not.** The partition entries are readable at their fixed offsets
  whether or not the signature is present; `mmls -o` and manual offset arithmetic both work on a
  "damaged" image. **Our version asks students to identify the corruption and then proceed
  *without* fixing it** — and, if a repair is genuinely required, to do it **on a working copy,
  hashed before and after, with the change recorded** (**R9**).

### 2.2 A partition table entry

- **What it is** — 16 bytes per partition: boot flag, starting CHS, **partition type byte**, ending
  CHS, **starting LBA (4 bytes)** and **total sectors (4 bytes)**.
- **Where it lives** — MBR offsets `0x1BE`, `0x1CE`, `0x1DE`, `0x1EE`. Within each entry, starting
  LBA at `+0x08` and total sectors at `+0x0C`.
- **What it proves** — where each partition begins and how long it is. Q2 asks for **the bytes
  representing the total sectors of the second partition, in little endian** — i.e. it wants the
  raw field, not the decoded number, which is the right way to ask because it forces the student to
  locate the field rather than read a tool's output.
- **What it does NOT prove** — 🔴 **that a partition is where the table says it is.** The table is
  a claim; the filesystem boot sector at that LBA is the corroboration. A doctored entry points at
  nothing, and a **deleted** partition leaves its filesystem intact with no entry at all —
  which is the whole basis of partition-recovery carving. ⚠️ **CHS values are vestigial** and
  routinely disagree with LBA on modern disks; **read LBA, ignore CHS.**
- **How to parse it** — by hand at the offsets above, or `mmls`, or `fdisk -l`. 🟢 **Ask for it by
  hand at least once** — Q2's little-endian phrasing is exactly the exercise.
- **Anti-forensics / false-positive caveat** — ⚠️ **little-endian is where students lose the mark,
  not where they lose the understanding.** `00 20 00 08` is `0x08002000`. Our version shows the
  byte order conversion once and then assesses the concept, not the arithmetic.

### 2.3 Partition size, derived

- **What it is** — total sectors × bytes per sector, expressed in GB. Q3 and Q4 ask for both
  partitions to two decimal places.
- **Where it lives** — nowhere. **It is a calculation**, from §2.2's field and the sector size.
- **What it proves** — that the student converted the field correctly and knew the sector size.
- **What it does NOT prove** — 🔴🔴 **and this is the trap worth teaching**: the answer depends on
  **two assumptions the question does not state.** Is the sector size 512 or 4096? Is "GB" 10⁹ or
  2³⁰ (GiB)? **Those two choices give four different answers**, and only one is marked correct.
  ⚠️ The room's own example format (`15.25`) implies a convention it never declares.
- **How to parse it** — `total_sectors × 512 ÷ 1024³` for GiB, `÷ 10⁹` for GB. **Read the sector
  size from the filesystem boot sector rather than assuming 512.**
- **Anti-forensics / false-positive caveat** — 🟢 **our version states its units.** A question whose
  answer turns on an undeclared convention is testing whether the student guessed the marker's
  habit, not whether they understand the structure. **This is a question-design lesson, and it is
  the most transferable thing in the room** — see §6.

### 2.4 NTFS file timestamps — `$STANDARD_INFORMATION` vs `$FILE_NAME`

- **What it is** — the two independent timestamp sets NTFS keeps per file, each with created,
  modified, MFT-changed and accessed.
- **Where it lives** — attribute `0x10` (`$STANDARD_INFORMATION`) and attribute `0x30`
  (`$FILE_NAME`), both inside the file's `$MFT` record.
- **What it proves** — Q5 (*"when was the text file related to the password created on the
  system?"*) and Q7 (*"When this file was first found on this disk?"*) are the same artifact asked
  twice. 🟢 **Q7's phrasing is unusually careful** — *"first found on this disk"* rather than
  "created" — which is precisely the distinction between a file's own history and its history
  **on this volume**, and it is the right way to ask.
- **What it does NOT prove** — 🔴🔴 **`$STANDARD_INFORMATION` is user-writable and is what every
  timestomping tool edits. `$FILE_NAME` is kernel-maintained and is not.** A `$SI` creation time
  earlier than its `$FN` creation time is the classic timestomp signature. **A single timestamp
  quoted without saying which attribute it came from is not a finding**, and neither question says.
  ⚠️ Also: `$SI` has 100-nanosecond resolution while many tools display seconds — an "identical"
  pair of timestamps may differ.
- **How to parse it** — `MFTECmd -f $MFT --csv <out>` gives both attribute sets in separate
  columns; `fls`/`istat` from TSK; Autopsy's file metadata pane. ⚠️ Per block C, `MFTECmd`'s
  `--body` output requires `--bdl`.
- **Anti-forensics / false-positive caveat** — 🟢 **this is where our version diverges hardest from
  the room.** The scenario is an insider *"attempting to erase all traces of her actions"* —
  **which is a timestomping scenario the room never asks about.** Our capstone asks: *"Compare `$SI`
  and `$FN` for this file. What do you conclude?"* **That question has a real answer and the room
  left it on the table.**

### 2.5 The `$UsnJrnl:$J` change journal

- **What it is** — NTFS's record of *what changed*, in order, with a reason code per change.
- **Where it lives** — `\$Extend\$UsnJrnl`, alternate data stream `$J` (sparse), with `$Max`
  holding the size configuration.
- **What it proves** — Q8 is the best question in the room: *"What is the entry number of the
  directory in the Journal that was created and then deleted for exfiltration purposes?"* 🟢 **A
  create-then-delete pair in `$J` survives after both the directory and its `$MFT` record are
  gone.** The journal is the only artifact on the disk that records the *sequence*.
- **What it does NOT prove** — 🔴 **why**, and the question's phrasing gives it away: *"created and
  then deleted **for exfiltration purposes**"* asserts a motive the journal cannot carry. `$J`
  records **USN, timestamp, filename, parent reference and a reason bitmask** — `FILE_CREATE`,
  `FILE_DELETE`, `RENAME_OLD_NAME`, `CLOSE`. **It does not record purpose, process or user.**
  ⚠️ It is also **circular and short** — days to weeks on a busy volume — and a directory's contents
  are not in the journal, only its own entries.
- **How to parse it** — `MFTECmd -f $J --csv <out>`; ⚠️ **per block C, `$J` needs `-m` to resolve
  parent paths**, and without it you get filenames with no location. Cross-reference against `$MFT`
  and `$LogFile`.
- **Anti-forensics / false-positive caveat** — 🔴 **`$J` is deletable and disable-able**
  (`fsutil usn deletejournal`), and doing so is itself an anti-forensic act with its own trace.
  🟢 **Contrast with `$LogFile`, which is ~2–3 hours circular and records the transactions rather
  than the changes** — the two answer different questions and block C settles which is which.
  **`$J` for "what happened over days", `$LogFile` for "what happened just now."**

### 2.6 ZIP signatures, for carving

- **What it is** — the byte patterns that bound a ZIP archive: local file header **`50 4B 03 04`**
  (`PK\x03\x04`) at the start, **End of Central Directory `50 4B 05 06`** (`PK\x05\x06`) at the end.
- **Where it lives** — anywhere in unallocated space. Q9 and Q10 ask for the **starting offset of
  the first ZIP after offset `0x4E7B00000`** and its **ending offset**.
- **What it proves** — that a recoverable archive exists at a known extent. 🟢 **Asking for both
  offsets is good design** — a header alone is a lead; a header *and* a plausible footer is a
  carvable file, and the pair is what a carve actually needs.
- **What it does NOT prove** — 🔴🔴 **that the bytes between them are one file.** Carving assumes
  **contiguity**, and a fragmented archive carved header-to-footer produces a corrupt file that
  still opens far enough to look real. ⚠️ **And `PK\x03\x04` is not "a ZIP"** — it is the container
  signature for **every OOXML document (`.docx`, `.xlsx`, `.pptx`), every JAR, every APK, every
  ODF file, and every EPUB.** A header hit tells you the container format and nothing about the
  content. ⚠️ The EOCD can also legitimately appear inside a nested archive.
- **How to parse it** — the offsets by hand in a hex editor (which is what the question wants), then
  `dd if=… bs=1 skip=<start> count=<len>` or PhotoRec/`foremost` for the extraction. Verify with
  `file` and `unzip -l` **before** trusting it.
- **Anti-forensics / false-positive caveat** — 🔴 **Q11 (*"the flag hidden within the file inside
  the zip"*) requires extracting and opening an archive recovered from a suspect disk.** Per rooms
  8, 12 and 13, that is the containment step nobody teaches. **A disposable directory, `unzip -l`
  first, and no execution** — and in our version, said out loud.

### 2.7 FAT32 deleted directory entries

- **What it is** — a 32-byte directory entry whose first byte has been overwritten with **`0xE5`**
  to mark it free, leaving the rest — name, attributes, timestamps, starting cluster, size —
  intact.
- **Where it lives** — the FAT32 partition's directory clusters. Q12 asks for the name of a
  **deleted disk-wiping executable** installed in the FAT32 partition.
- **What it proves** — 🟢 **the name and metadata of a deleted file survive deletion**, and in FAT
  they survive in a form a student can read by eye in a hex editor. Q12's answer is a filename that
  no longer exists in any listing.
- **What it does NOT prove** — 🔴🔴 **that the file's data is still there, or ever ran.** Deletion
  frees the cluster chain; **FAT32 keeps only the *starting* cluster in the entry**, so recovering
  a fragmented deleted file is guesswork past the first fragment. ⚠️ **The first character of the
  filename is destroyed by the `0xE5` marker** — the recoverable name is `?IPER.EXE`, not
  `WIPER.EXE`, and the missing letter is inferred, not read. **That is a finding-versus-inference
  distinction sitting inside a single filename**, and it is the best small example of D7 in the
  entire challenge.
- **How to parse it** — hex-read the directory cluster and look for `E5` at entry offset 0; or
  `fls -r` / PhotoRec / Autopsy's deleted-files view. **Cross-check against the LFN entries
  preceding the short entry** — the long filename may survive intact even when the 8.3 entry's
  first byte does not.
- **Anti-forensics / false-positive caveat** — 🟢 **the artifact here is not the wiper, it is the
  wiper's absence-with-a-name.** Someone installed a disk-wiping tool and removed it; the entry is
  the trace of both acts. ⚠️ But **the name alone does not prove it ran** — no prefetch, no
  Amcache, no `$J` create/delete pair means no execution evidence. **Our version asks for both:
  the name, and what would prove it was used.**

### 2.8 The challenge's own anti-forensic layer

- **What it is** — the story the artifacts tell together: a damaged boot sector, a directory created
  and deleted, hidden files, carved-out archives, and a wiping tool that was installed and removed.
- **Where it lives** — across all four structures above, in two filesystems, on one image.
- **What it proves** — 🟢🟢 **that the six objectives are one narrative, not six exercises.**
  The insider accessed a document, staged it in a directory, archived it, deleted the staging, ran
  or installed a wiper, and the disk ended up unreadable. **Every question is a step in that
  sequence**, and the sequence is the assessment.
- **What it does NOT prove** — 🔴 **any of it, as motive.** The room's own questions repeatedly
  assert what they should be asking: *"created and then deleted **for exfiltration purposes**"* ·
  *"the sensitive pdf document **accessed**"* · *"a tool related to **disk wiping**"*. **Each
  embeds the conclusion in the prompt.** ⚠️ And the scenario itself opens with *"the suspicion is on
  the newly joined intern Fatima, who has been seen around the research lab a few times"* — which is
  **prejudicial framing presented as case background**, and a student who starts there will
  interpret every ambiguous artifact against her.
- **How to parse it** — 🟢 the correct order is the one the room implies: structure (MBR) →
  geometry (partitions) → filesystem metadata (`$MFT`, `$J`) → unallocated (carving) → the second
  filesystem (FAT32). **That order is `S4`'s running order and it is validated here.**
- **Anti-forensics / false-positive caveat** — 🟢🟢 **this is the finding that matters for D19.**
  The challenge proves that **one image can carry a whole incident across two filesystems**, and
  that the carry-through case we want is buildable. **But ours must ask what the artifacts show
  before asking what they mean** — and must not name a suspect in the brief.

## 3. Tools and commands

**The room names no tools.** That is deliberate and it is the point:

> *"The machine has all the required tools."*
> *"Not all tools are required to solve this challenge. As it is in real-life cases, you must
> figure out which tools work best for the situation."*

🟢🟢 **Tool selection is the assessed skill.** After seventeen rooms that hand the student a command
and ask them to read its output, this one hands them a problem. **Adopt this stance for our
capstone brief.**

The tool set the twelve questions actually require, from our own reading:

| step | what is needed | our lab's tool |
|---|---|---|
| read sector 0, find the corruption | a hex viewer | HxD · `xxd -l 512` |
| decode the partition table | offsets + little-endian, by hand | hex viewer, then `mmls` to check |
| enumerate partitions on a "damaged" image | offset-aware parsing **without repair** | `mmls`, `fdisk -l`, `mmls -o` |
| NTFS timestamps (`$SI` **and** `$FN`) | `$MFT` parser | `MFTECmd -f $MFT --csv` |
| the change journal | `$J` parser | `MFTECmd -f $J --csv` ⚠️ **needs `-m` for parent paths** |
| locate a ZIP after a given offset | signature search | hex editor search for `50 4B 03 04` |
| extract by offset | byte-exact extraction | `dd bs=1 skip=<start> count=<len>` |
| verify the carve | type + integrity | `file`, `unzip -l` (**never `unzip` blind**) |
| FAT32 deleted entries | directory-cluster read | hex viewer for `E5`; `fls -r`; PhotoRec |

### CURRENCY CHECK

**No new tools are named, so nothing new to verify.** Everything the challenge requires is already
covered:

| item | where |
|---|---|
| `MFTECmd` does **not** parse `$LogFile` despite its README | `_TOOL_CURRENCY` **C1** |
| `$J` needs `-m` for parent paths | **C4** |
| `--body` requires `--bdl` | **C3** |
| `$LogFile` (~2–3 h circular) vs `$UsnJrnl` (days–weeks) | **C8** |
| `scalpel` unmaintained · `foremost` via `apt` not SourceForge | **B1**, **B2** |
| **WinHex free build will not save >200 KB or write sectors** | **B3** — 🔴 **directly relevant: a student on the free build cannot do the repair this challenge's title asks for** |
| HxD 2.5.0.0 is fine but stale | **B6** |
| PhotoRec/TestDisk 7.2 is the safest tool in the set | **B7** |
| Autopsy 4.23.1; **Keyword Search, Plaso and Malware Scan OFF by default** | **A1** / **E1** |

⚠️ **One live consequence.** Block B3 established that the free WinHex build **cannot write
sectors and cannot save files over 200 KB**. **The room's premise — "fix the damaged disk" — is
therefore not performable in our lab on the free tooling**, which is a second, practical reason
our version teaches reading the structures rather than repairing them (§2.1).

## 4. Evidence used

- **`challenge.001`** — a single raw split-image segment on the lab VM's Desktop, in an `Evidence`
  folder. **A multi-partition disk carrying at least one NTFS and one FAT32 volume**, with a
  deliberately corrupted boot sector, deleted files in both filesystems, and at least one ZIP in
  unallocated space past offset `0x4E7B00000` (≈ **21 GB in**, so the image is large).
- **Not downloadable. No licence offered. Not reusable.** **Nothing for `ecdfp-evidence`.**
- 🔴 The room prints **plaintext VM credentials**. Not reproduced here (**R8**).

### 🟢🟢 But it is the blueprint for `EVS-06`, and we can build it

**Everything this image does, we can construct** — and rooms 6, 8 and 9 already gave us three of the
four pieces:

| the challenge's feature | how we build it |
|---|---|
| a corrupted boot sector | **two hex edits on 512 bytes** — room 9's finding exactly |
| an MBR with two partitions | `fdisk` on a file, then `losetup` — room 15's `EVS-05` route |
| an NTFS volume with real timestamps | `mkfs.ntfs` on a loop partition, then populate it |
| a FAT32 volume with a deleted executable | room 6's self-made FAT32 image, plus a delete |
| a create-then-delete directory in `$J` | `mkdir` then `rmdir` on the mounted NTFS volume |
| a ZIP in unallocated space | write it, delete it, do not wipe — room 8's carving-target route |
| a timestomped file | ⚠️ **new**, and worth adding — it is the finding the room forgot (§2.4) |

**This is `EVS-06`: one self-made multi-partition image that carries the whole S4 story.** Cost:
one afternoon of scripting, no licence, no download, fully reproducible, and — unlike CFReDS — **we
control every answer**, which means the assessment key is ours and cannot be found online.

🟢 **And note the pairing.** CFReDS (room 16) gives us a **real** disk with a **published** answer
key — perfect for teaching, unusable for grading. `EVS-06` gives us a **synthetic** disk with a
**private** key — unusable as "real evidence", perfect for grading. **Use both, for the two
different jobs.**

### 🔴 One thing we must NOT copy: the scenario's framing

> *"The suspicion is on the newly joined intern Fatima, who has been seen around the research lab a
> few times. She, being the insider with direct access to the laboratory resources, is suspected of
> stealing the research…"*

**A named suspect, a status marker ("newly joined intern"), and "seen around a few times" offered as
if it were evidence — before a single artifact is examined.** A student who reads that brief and
then finds an ambiguous timestamp will resolve it against her. **That is exactly the failure mode
D7 and D20 criterion 4 exist to catch, and it is baked into the case setup rather than the
questions.**

🟢 **Our brief states the alert, the scope and the questions. It does not name a suspect, and it
does not editorialise about anyone's tenure or movements.** If the case has a person in it, the
student's job is to find out whether the artifacts support that, and **a well-built case includes at
least one artifact that does not.**

## 5. Lab design worth reusing

1. **🟢🟢 The prerequisite chain.** Four named rooms — MBR/GPT, FAT32, NTFS, File Carving —
   assessed together in one image. **That is `S4`'s four teaching rows and its capstone, and an
   independent source has validated the structure.** Strongest architectural confirmation we have
   received.
2. **🟢🟢 "Not all tools are required… you must figure out which tools work best."** Tool selection
   as the assessed skill. **Verbatim into our capstone brief.**
3. **🟢 One image, two filesystems.** NTFS and FAT32 in one exercise, so the student must recognise
   *which* filesystem they are in before choosing a technique. **Nothing else in the path does
   this**, and it is the difference between knowing two filesystems and knowing you have to tell
   them apart.
4. **🟢 Ask for raw bytes at least once.** Q2's *"the bytes representing the total sector… (Little
   Endian)"* forces the student to the offset instead of to a tool's decoded output. **Keep one
   question like this per structure.**
5. **🟢 Ask for both ends of a carve.** Q9 and Q10 want start **and** end offset — because a header
   alone is a lead and the pair is a file (§2.6).
6. **🟢 A defined starting offset for the carving question** (*"after the offset 4E7B00000"*).
   Bounds a 21 GB search into a tractable exercise without giving the answer away. **Good
   assessment craft.**
7. **🟢 120 minutes, Hard, badge-bearing.** The right weight for a capstone, and useful calibration:
   **our S4 capstone should be scoped at about two hours**, not the 30 minutes a session row
   implies.
8. **🔴 Do NOT reuse: "Fix the damaged disk" as an objective** (§5 below).
9. **🔴 Do NOT reuse: the named-suspect framing** (§4).

### 🔴 Safety defect #7 — the first one that is the *premise*, not a step

The room's first objective and first question require the student to **repair the evidence image**.
Room 9 (MBR and GPT Analysis) had students edit and save an evidence image in place; **this room
makes that the point of the exercise and puts it in the room's own description** (*"Fix the damaged
disk"*).

**It is also unnecessary.** The partition entries sit at fixed offsets and are readable whether or
not `55 AA` is present; `mmls`, manual arithmetic and offset-based mounting all work on the image as
found. **The repair buys convenience, not access.**

**Our version, in one line:** *identify the corruption, state what it prevents, and proceed without
repairing it — and if you must repair, do it on a copy, hash before and after, and record the
change* (**R9**).

| room | defect | who is at risk |
|---|---|---|
| 6 · FAT32 | paste-recovered PowerShell into a live shell | the analyst |
| 8 · File Carving | `binwalk -e` with no isolation (CVE-2022-4510) | the analyst |
| 9 · MBR/GPT | edit and save the evidence image in place | **the evidence** |
| 12 · Memory & Processes | dump live malware to the home directory | the analyst |
| 13 · Memory & User Activity | `unzip` hostile OOXML in `~`; live C2 URL unflagged | the analyst |
| 15 · Forensic Imaging | verify the hash, then mount read-write, never re-verify | **the evidence** |
| **18 · Diskrupt** | **"fix the damaged disk" — repairing the evidence is the objective** | **the evidence** |

🟢 **Seven defects, and the split holds: four endanger the analyst's machine, three endanger the
evidence.** ⚠️ **And the three evidence defects are all in `S4`/`S2` disk work** — rooms 9, 15 and
18. **That is not a coincidence; it is a blind spot in how disk forensics is taught, and naming it
is the S1 exercise.** Write it.

## 6. Question patterns

**12 questions, one task, no scaffolding.** Question design is what we came for, so this section is
the point of the note.

**🟢 The chain is correct and it is our session in order:**

| # | question | artifact | our row |
|---|---|---|---|
| 1 | corrupted bytes in the boot sector | MBR signature | `S4-04` |
| 2 | total-sector bytes of partition 2, little endian | partition table entry | `S4-05` |
| 3–4 | size of each partition in GB | derived | `S4-05` |
| 5 | when the password text file was created | `$MFT` timestamps | `S4-07` |
| 6 | full name of the sensitive PDF accessed | `$MFT` / access artifacts | `S4-07` |
| 7 | when the file was **first found on this disk** | `$FN` creation | `S4-07` |
| 8 | Journal entry number of a created-then-deleted directory | `$UsnJrnl:$J` | `S4-07` |
| 9–10 | start and end offset of the first ZIP after `0x4E7B00000` | carving | `S4-09` |
| 11 | the flag inside the ZIP | extraction | `S4-09` |
| 12 | name of the deleted disk-wiping executable | FAT32 `0xE5` entry | `S4-06` |

**Every question is single-artifact and single-answer**, which is our case rule — and **the sequence
is a narrative**, which is what makes it a capstone rather than a quiz.

**🟢 Three questions are genuinely well made.** Q2 (raw bytes, little endian — forces the offset) ·
Q7 (*"first found on this disk"* — the right way to ask about `$FN`) · Q9+Q10 (both ends of the
carve, bounded by a given offset).

**🔴 Four questions embed their own conclusion:**
- *"…created and then deleted **for exfiltration purposes**"* — `$J` records a reason **bitmask**,
  not a purpose.
- *"the **sensitive** pdf document **accessed**"* — "sensitive" is a classification, and "accessed"
  is a claim the artifact may not support.
- *"a tool related to **disk wiping** was installed and then deleted"* — the entry gives a name; the
  category is the marker's inference.
- *"the corrupted bytes… that **caused the disk to be damaged**"* — assumes causation, and assumes
  the disk is damaged rather than that a tool refused it.
**Each hands the student the interpretation and asks only for the lookup.** That is the inverse of
what we grade.

**🔴 Two questions have undeclared conventions** (Q3, Q4 — 512 vs 4096-byte sectors, GB vs GiB;
§2.3). **Four possible right answers, one accepted.**

**🔴 And the eighteenth room in a row with no "cannot be determined" answer** — in a room built
entirely from artifacts that cannot carry the weight the questions put on them:

| the room could have asked | correct answer |
|---|---|
| *"Does `$J` show why the directory was created and deleted?"* | **No.** It records USN, timestamp, name, parent reference and a reason bitmask. **Purpose, process and user are absent.** |
| *"The recovered filename is `?IPER.EXE`. What was the file called?"* | **Cannot be determined from the 8.3 entry** — the first character is destroyed by the `0xE5` marker. Check the LFN entries; otherwise the letter is inferred. |
| *"Does the deleted wiper's directory entry prove it ran?"* | **No.** Execution needs prefetch, Amcache or a `$J` sequence. **A name is installation evidence at best.** |
| *"The `$SI` creation time is earlier than `$FN`. Which is right?"* | **`$FN` is kernel-maintained; `$SI` is user-writable.** The discrepancy is the finding — **and the room never asks it.** |
| *"You carved a ZIP header-to-footer. Is it one file?"* | **Not established** — carving assumes contiguity; verify with `unzip -l` before trusting it. |

🟢🟢 **The fifth of those is the one to build the capstone around.** The scenario is explicitly
about *"attempting to erase all traces"*, the image is an NTFS volume, and **timestomping is the
one anti-forensic technique the room sets up and never asks about.** Our capstone asks it, and
D20 criterion 4 rewards the student who reports the discrepancy rather than a timestamp.

## 7. Figures we would need to draw

Figures present in the room: **none.** A challenge room is a scenario page and a question list.

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **the S4 capstone map** | the six objectives as a left-to-right chain — repair/read MBR → partitions → NTFS metadata → `$J` → carve → FAT32 — with **each step tagged with the S4 row that taught it**; caption *"one image, four techniques, one story"* | **highest** — this is the session-closing slide |
| 2 | **sector 0, annotated** | the 512 bytes as a strip: bootstrap `0x000–0x1BD` · four partition entries at `0x1BE/0x1CE/0x1DE/0x1EE` · **`55 AA` at `0x1FE` accented and marked "two bytes; absence stops every tool and hides nothing"**; one entry exploded to show boot flag · type byte · **start LBA at +0x08** · **total sectors at +0x0C** | **highest** |
| 3 | **`$SI` vs `$FN`** | one `$MFT` record, two timestamp blocks side by side — **`$SI` labelled "user-writable — what timestomping edits"**, **`$FN` labelled "kernel-maintained"** — with a discrepancy drawn between the creation times and the caption *"the difference is the finding"* | **highest** — the question the room forgot |
| 4 | **the three NTFS change records compared** | `$MFT` (**state now**) · `$LogFile` (**transactions, ~2–3 h circular**) · `$UsnJrnl:$J` (**changes, days–weeks**) as three timelines of different length over the same incident, with the create-then-delete pair visible only in `$J` | **high** |
| 5 | **what a `0xE5` deletion destroys** | a 32-byte FAT directory entry drawn twice, before and after — **only byte 0 changed** — with the recoverable fields (name chars 2–11, attributes, timestamps, **starting cluster only**, size) accented and the lost first character and cluster chain greyed; caption *"`?IPER.EXE` — the letter is inferred, not read"* | **high** |
| 6 | **carving assumes contiguity** | one ZIP drawn contiguous and one fragmented across three extents, both carved header-to-footer — the second producing a file that **opens far enough to look real**; caption *"a header and a footer are not a file"* | **high** |
| 7 | **`EVS-06` build sheet** | the synthetic image as an exploded diagram — MBR (2 hex edits) · NTFS partition (timestomped file · created-then-deleted dir · deleted ZIP) · FAT32 partition (deleted wiper) — each block annotated with the one command that creates it | medium — **an instructor figure, not a student one** |

Figure 3 is the one that turns this challenge from a lookup exercise into a forensics exercise.
Never their images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct — and this room outranks its Priority-2 label

Mapped to *"S4 case — wiped partition table"*. **True, and understated.** This is not a case to
mine for ideas; **it is the S4 capstone, already designed, with its prerequisite chain matching our
teaching rows one for one.** Part 1's row should read: **S4 capstone model — validates the S4
architecture; blueprint for `EVS-06`.**

### Rows this strengthens

- **`S4-04` / `S4-05`** MBR and partitions — Q1–Q4 are the assessment for both rows, and Q2's
  raw-bytes phrasing is the model for how to ask.
- **`S4-06`** FAT32 — Q12, and the `0xE5` first-character problem (§2.7) is a better teaching point
  than anything room 6 supplied.
- **`S4-07`** NTFS — Q5–Q8, plus **the `$SI`/`$FN` question the room omits**, which is the row's
  real content.
- **`S4-09`** carving — Q9–Q11, with the bounded-offset design worth copying.
- **The S4 capstone** — 🟢🟢 **calibrated at two hours, Hard.** Our session budget assumes far
  less; **this is evidence the capstone needs its own block, not a tail-end row.**
- **`S1`** — safety defect #7, and 🟢 **the observation that all three evidence-endangering defects
  are in disk work** (rooms 9, 15, 18). That pattern is the exercise.
- **`ecdfp-evidence`** — **`EVS-06`**, the synthetic multi-partition image (§4).
- **D19 carry-through** — the proof that one image can carry a whole incident across two
  filesystems, plus a clear statement of what our brief must not do (§4).

### Four things our S4 capstone must do differently

1. **Do not repair the evidence.** Identify the corruption, state what it blocks, work around it
   (§5). If a repair is unavoidable: **copy, hash, document.**
2. **Ask the `$SI`/`$FN` question.** The scenario is about erasing traces and the room never asks
   the one question that would detect it.
3. **State units and sector size** in any question whose answer is a calculation.
4. **Do not name a suspect in the brief**, and include at least one artifact that does not support
   the obvious reading.

### Minutes

**No new rows.** Everything here lands in `S4`'s existing four teaching rows and its capstone.
⚠️ **But the two-hour calibration is a real signal** — if our capstone is currently budgeted at a
single 15–20 minute row, **that is a structural mismatch, not a content gap.** Flagging it for the
S4 review rather than adjusting minutes here.

**S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Thirteenth room carrying the S5 overdraft.**

### Out of scope

Registry, memory, network, event logs — **none appear**, and correctly so: this is a pure disk
challenge. Malware analysis of the recovered ZIP contents — out. **No scope conflict.**

### Still unresolved

**Browser forensics** — eighteenth room, no `DECISIONS.md` row.
**S4 capstone weighting** — new, and now evidenced.

## 9. Links

- Room: <https://tryhackme.com/room/diskrupt>
- Room's stated prerequisites, all four already extracted:
  `mbr-and-gpt-analysis.md` · `fat32-analysis.md` · `ntfs-analysis.md` · `file-carving.md`
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (File System Analysis)
- ⚠️ The room has a public **Write-ups** tab. **Do not consult or link it** — third-party
  walkthroughs of a live challenge, and our questions must be ours (**D22**, and the answer-key
  hygiene rule from `autopsy.md` §4).
- NTFS/timeline tool currency, incl. `MFTECmd`'s `$LogFile` gap and the `$J -m` flag:
  `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block C**
- Carving and hex-tool currency, incl. **the free WinHex build's write/save limits**: **block B**
- Companion evidence routes: `forensic-imaging.md` §4 (**`EVS-05`**, the loop-device technique that
  builds `EVS-06`) and `autopsy.md` §4 (**CFReDS**, the real-image counterpart)
