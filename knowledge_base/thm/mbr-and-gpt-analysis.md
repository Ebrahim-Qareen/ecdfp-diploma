---
room: MBR and GPT Analysis
url: https://tryhackme.com/room/mbrandgptanalysis
module: File System Analysis (Section 1 of Advanced Endpoint Investigations)
feeds: S4 — `S4-04` MBR (direct hit) · `S4-05` GPT (direct hit) · **`S4-10` Case 04** —
       Task 5 is essentially our case, already designed, including the proof step.
       Also `S2-06` FTK Imager.
difficulty / time: Medium · **80 min** · 8 tasks (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

The first sector of a disk, byte by byte — both partitioning schemes — and what happens to the
boot process when someone changes those bytes. It opens with the boot chain (power → POST →
locate bootable device → MBR/GPT → bootloader → kernel), then dissects MBR's 512 bytes and GPT's
five components in a hex editor, then runs two incident scenarios.

The teaching device is consistent and good: **every structure is taught as byte offsets you can
find yourself**, and every address is resolved with the same arithmetic — reverse the
little-endian bytes, convert to decimal, multiply by the 512-byte sector size, jump to that offset.
Learn it once in the MBR task, reuse it four times in the GPT task.

The room's own framing is worth keeping: the disk is a building, the partitions are rooms, and
**the MBR/GPT is the map**. Damage the map and nothing else matters.

## 2. Artifacts — one 6-box block each

### 2.1 MBR — bootloader code (bytes 0–445)

- **What it is** — the initial bootloader, 446 bytes.
- **Where it lives** — sector 0, offsets `0x000`–`0x1BD`.
- **What it proves** — its job is to find the bootable partition in the partition table and load
  the second-stage bootloader from it. Forensically: whether the code is stock or has been
  replaced.
- **What it does NOT prove** — the room is honest that disassembling it is out of scope, and
  without that you cannot tell *what* modified code does. Non-standard bytes here are an
  indicator, not a conclusion — and legitimate boot managers (GRUB, vendor tooling) write their
  own code here.
- **How to parse it** — HxD at offset 0. Comparison against a known-good MBR is the practical
  method; disassembly is the thorough one.
- **Anti-forensics / false-positive caveat** — this is where **bootkits live**, and the room's key
  point is why: **the MBR executes before the OS, so it runs before any OS-level protection
  exists.** Reinstalling the OS does not remove it.

### 2.2 MBR — partition table (bytes 446–509)

- **What it is** — four 16-byte entries describing up to four partitions.
- **Where it lives** — offsets `0x1BE`–`0x1FD`. Each entry:
  | offset | len | field |
  |---|---|---|
  | 0 | 1 | **Boot indicator** — `80` bootable, `00` not |
  | 1–3 | 3 | Starting CHS address |
  | **4** | 1 | **Partition type** — e.g. `07` = NTFS, `EE` = GPT protective |
  | 5–7 | 3 | Ending CHS address |
  | **8–11** | 4 | **Starting LBA** (little-endian) |
  | **12–15** | 4 | **Number of sectors** (little-endian) |
- **What it proves** — how many partitions exist, which is bootable, each one's filesystem type,
  **where each starts** and **how big it is**. Two computations carry the whole task:
  - **locate**: reverse LBA → decimal → **× 512** → that byte offset is the partition start
  - **size**: reverse sector count → decimal → **× 512** = size in bytes
- **What it does NOT prove** — the partition type byte is a **declaration, not a detection**:
  `07` says "treat me as NTFS", it does not verify an NTFS volume is there. CHS addresses are
  legacy and unreliable on modern disks — the room says so and tells you to use LBA. And a
  partition table lists what the map *claims*; a hidden or carved-out region simply is not in it.
- **How to parse it** — HxD; select bytes and read the decimal in the Data Inspector's `Int32`,
  with **Byte Order set to Little Endian** so the reversal is done for you.
- **Anti-forensics / false-positive caveat** — the table is 64 bytes, so **wiping four numbers
  makes a disk look empty while every byte of data remains**. That is the entire basis of the
  Task 5 scenario and of our `S4-10`.

### 2.3 MBR signature (bytes 510–511)

- **What it is** — the two-byte end marker, `55 AA`.
- **Where it lives** — offsets `0x1FE`–`0x1FF`; also the practical way to find where the MBR ends
  in a hex editor.
- **What it proves** — that the sector is structured as a boot record. Its **absence or alteration
  makes the system unbootable.**
- **What it does NOT prove** — that the boot code is valid, or that the partition table is intact.
  It is a two-byte magic number, nothing more — and it is present on a **protective** MBR too, so
  `55 AA` alone does not distinguish MBR from GPT.
- **How to parse it** — read the last two bytes of sector 0.
- **Anti-forensics / false-positive caveat** — the room gives both causes and this is the useful
  part: these bytes get corrupted by **bad sectors** *and* are **deliberately changed by malware**.
  **The artifact cannot tell you which** — a textbook finding-vs-interpretation split.

### 2.4 GPT — protective MBR

- **What it is** — a decoy MBR in sector 0 of a GPT disk, so BIOS-era tools do not mistake the
  disk for unpartitioned and damage it.
- **Where it lives** — sector 0. Same three components as a real MBR, with differences:
  bootloader code is **typically all `00`** (occasionally legacy placeholder code) and performs no
  boot function; the partition table holds **one** entry with the rest zeroed; signature `55 AA`.
- **What it proves** — 🟢 **the single most useful byte in this block: partition type `EE` in the
  one entry means "this is a GPT disk".** That is your first-glance scheme identification.
- **What it does NOT prove** — nothing about the actual partitions; the protective entry exists
  only to claim the whole disk. Its bootloader code being zeros is normal and is **not** evidence
  of wiping.
- **How to parse it** — HxD at offset 0; check byte 4 of the first partition entry (`0x1C2`).
- **Anti-forensics / false-positive caveat** — a disk with a protective MBR but a destroyed GPT
  header still *looks* like a GPT disk while being unusable, which is exactly the ambiguity an
  examiner has to resolve.

### 2.5 GPT — primary header

- **What it is** — the GPT's blueprint: 92 meaningful bytes at the start of sector 1, padded to
  512 with zeros.
- **Where it lives** — sector 1, immediately after the protective MBR. Fourteen fields:
  | bytes | field | note |
  |---|---|---|
  | 0–7 | **Signature** | `45 46 49 20 50 41 52 54` = `EFI PART` |
  | 8–11 | Revision | `00 00 01 00` = v1.0 |
  | 12–15 | Header size | `5C 00 00 00` = **92** |
  | **16–19** | **CRC32 of header** | tamper/corruption check |
  | 20–23 | Reserved | |
  | 24–31 | Current LBA | should be 1 |
  | **32–39** | **Backup LBA** | where the backup header lives |
  | 40–47 | First usable LBA | |
  | 48–55 | Last usable LBA | |
  | 56–71 | **Disk GUID** | 16 bytes, mixed endian |
  | 72–79 | Partition entry array LBA | usually 2 |
  | 80–83 | Number of partition entries | `80 00 00 00` = **128** |
  | 84–87 | Size of each entry | `80 00 00 00` = **128 bytes** — *not* the partition's size |
  | **88–91** | **CRC32 of partition array** | |
- **What it proves** — the disk's identity (GUID), its layout, where the backups are, and — via the
  two CRC32s — **whether the header or the partition array has been altered**.
- **What it does NOT prove** — 🔴 **a CRC32 mismatch tells you the bytes changed. It cannot tell
  you whether that was malware, a failing disk, or a tool that wrote the structure badly.** CRC32
  is an error-detecting checksum, not a cryptographic integrity check — it is **not** collision
  resistant, so a matching CRC is not proof of authenticity either. The room presents both CRCs as
  tamper indicators without saying this; **we must.**
- **How to parse it** — HxD at sector 1 (offset 512). LBAs resolve with the same reverse → decimal
  → ×512 arithmetic.
- **Anti-forensics / false-positive caveat** — an attacker who edits the header can **recompute the
  CRC32 trivially**, so a clean checksum on a suspect disk means very little.

### 2.6 GPT — partition entry array

- **What it is** — up to 128 entries of 128 bytes each, describing every partition.
- **Where it lives** — from sector 2 (per the header's *Partition entry array LBA*). Each entry:
  | bytes | len | field |
  |---|---|---|
  | 0–15 | 16 | **Partition type GUID** — mixed endian |
  | 16–31 | 16 | Unique partition GUID — mixed endian |
  | 32–39 | 8 | Starting LBA |
  | 40–47 | 8 | Ending LBA |
  | 48–55 | 8 | Attributes (bootable / hidden / normal flags) |
  | 56–127 | 72 | **Partition name, UTF-16** |
- **What it proves** — every partition's type, identity, extent and name. Unused entries are all
  `00`, so **counting non-zero entries counts the real partitions**.
- **What it does NOT prove** — the type GUID is a declaration like the MBR type byte, and the
  partition name is **free text set at creation** — an attacker names a partition whatever they
  like. Attributes are flags, not enforcement.
- **How to parse it** — 🟢 **the mixed-endian GUID rule, which is the fiddliest thing in the room
  and worth teaching explicitly**: reverse the **first 4** bytes, reverse the **next 2**, reverse
  the **next 2**, then leave the **remaining 8** as they are.
  Worked: `28 73 2A C1 | 1F F8 | D2 11 | BA 4B | 00 A0 C9 3E C9 3B`
  → **`C12A7328-F81F-11D2-BA4B-00A0C93EC93B`** = **EFI System Partition**.
  Partition names decode from UTF-16.
- **Anti-forensics / false-positive caveat** — the room states none. Ours: entries can be zeroed to
  hide a partition while its data remains — the GPT equivalent of the MBR table wipe, and the
  **backup array (§2.7) is where you catch it.**

### 2.7 GPT — backup header and backup partition entry array

- **What it is** — GPT's redundancy, and the reason it replaced MBR.
- **Where it lives** — **backup GPT header in the last sector of the disk**; **backup partition
  entry array immediately before it**. The primary header's *Backup LBA* field points at it.
- **What it proves** — a second, independent copy of the layout. 🟢 **Forensically this is the
  cross-check the MBR never had: primary versus backup disagreement localises tampering**, and
  recovery is possible where an MBR would be unrecoverable.
- **What it does NOT prove** — agreement between primary and backup proves only that **both are
  consistent**, not that either is original — the room's own Task 7 notes advanced malware
  encrypting *both*. And a backup that matches a tampered primary means the attacker updated both.
- **How to parse it** — resolve the *Backup LBA* from the primary header, jump there in HxD.
- **Anti-forensics / false-positive caveat** — as above: redundancy raises the bar, it does not
  close the door. Targeting the **ESP directly** (§2.8) sidesteps it entirely.

### 2.8 EFI System Partition and the `.efi` bootloaders

- **What it is** — on a GPT/UEFI disk the bootloader is **not** in the partition structure at all;
  it is a set of files.
- **Where it lives** — the **EFI System Partition**, type GUID `C12A7328-F81F-11D2-BA4B-00A0C93EC93B`,
  holding `.efi` files — the room names `bootmgr.efi` and `bootx64.efi`.
- **What it proves** — which bootloader files exist and what they contain. The room's Task 8
  scenario finds **an encoded string planted in unused space inside `bootmgr.efi`** — a real and
  transferable technique: examine slack and padding inside a signed binary, not just the code.
- **What it does NOT prove** — a modified `.efi` does not prove it ever executed. And the room's
  own framing supplies the limit: **tampered files only run if Secure Boot is disabled**, because
  Secure Boot verifies digital signatures at load. **So the state of Secure Boot is part of the
  finding** — without it, "the file was modified" and "the bootkit ran" are different claims.
- **How to parse it** — mount/extract the ESP, open the `.efi` in HxD, inspect padding regions.
- **Anti-forensics / false-positive caveat** — `.efi` files are legitimately updated by OS and
  firmware updates; a changed hash is expected after patching.

## 3. Tools and commands

| tool | version the room uses | action | what it outputs |
|---|---|---|---|
| **HxD** | **not stated** | `File > Open` on `C:\Analysis\MBR`, `\GPT`, `\bootmgr.efi`, `\MBR_Corrupted_Disk.001` | hex + ASCII + Data Inspector |
| HxD | — | `Search > Go to`, value in **dec** | jumps to a computed offset |
| HxD | — | Data Inspector → `Int32`, **Byte Order = Little Endian** | decimal value of selected bytes |
| **FTK Imager** | **not stated** | `File > Add Evidence Item > Image File` | disk tree; **"Unrecognized file system"** when the MBR is broken |
| `msinfo32` | n/a | Run → `msinfo32` → **BIOS Mode**: `Legacy` or `UEFI` | firmware type |
| PowerShell | n/a | `Get-Disk` | partition scheme per disk |

### CURRENCY CHECK — cross-referenced to `_TOOL_CURRENCY_2026-08-28.md`

| item | result |
|---|---|
| **HxD** | **2.5.0.0, 11 Feb 2021** — still free for private and commercial use, still opens physical disks and RAM. **5.5 years without a release**, single maintainer. Nothing here breaks; name a fallback in the setup guide. |
| **FTK Imager** | free build is **8.3**; Exterro now also ships a separate **FTK Imager Pro** line (8.2 SP1). **Pin the product and version in our setup guide** — `S2-06` and this room both depend on it. |
| `msinfo32` / `Get-Disk` | built-in, unversioned, both current in form. |
| MBR/GPT structural facts | the room's figures check out as standard: MBR **2 TB / 4 partitions** (2³² × 512 B), GPT **128 partitions**, GPT header **92 bytes**, entry size **128 bytes**, ESP type GUID as given. |
| Room's version claims | **none stated for any tool** — ninth room running. The pattern is now the path's, not any one room's. |

**No new tools.** Everything this room uses was already covered in the currency file — which is
itself a useful signal: the S4 block runs on **HxD + FTK Imager + Autopsy + EZ Tools + the carvers**,
and that is the whole toolset our `CLEAN-TOOLS` snapshot needs for S4.

## 4. Evidence used

- Four prepared files on a Windows lab VM under `C:\Analysis\`:
  `MBR` (an extracted 512-byte MBR) · `GPT` (the first two GPT components) ·
  `MBR_Corrupted_Disk.001` (a full disk image with a damaged MBR) · `bootmgr.efi` (tampered).
- **Not downloadable. No licence offered. Not reusable.**
- Lab credentials published inline again — **deliberately not recorded here (R8).**
- **Nothing to flag for `ecdfp-evidence`.**

### ✅ Third confirmation of the Tier 1 route — and this one is the cheapest yet

Rooms 6 and 8 showed we can build FAT32 and carving images ourselves. This room shows the same for
**partition structures, and it is smaller still**: `EVS-07` (which `S4-04`, `S4-05` and `S4-10`
already name) needs only

- a small disk image with a **known-good MBR**, and a copy with the **partition table zeroed** and
  the **`55 AA` signature altered** — that is the Task 5 exercise, and staging it is two hex edits;
- a **GPT** image for the protective-MBR / header / entry-array walk.

**A 512-byte structure is the least expensive evidence in the entire course.** Combined with room 6's
FAT32 set and room 8's carving set, `ecdfp-evidence` can source **all of S4's evidence as Tier 1**,
with no reliance on public corpora and no compromise staging on EVI-SRC01. That is a materially
better position than `design/evidence_sets.md` currently assumes.

## 5. Lab design worth reusing

1. **🟢 Task 5 is our `S4-10`, already designed — including the proof step.** Row `S4-10` reads
   *"Case 04 — wiped partition table, recover it and prove the recovery"*. The room's scenario:
   a server is unbootable after a malicious attachment; two MBR fields are corrupted (a partition's
   starting LBA, and "a critical component that must be the same across all MBRs" — i.e. `55 AA`);
   repair them; **then reopen in FTK Imager and confirm it changes from "Unrecognized file system"
   to a readable tree.** That last step is the *prove* half of the row, and it is a genuinely good
   verification: **binary, visible, and impossible to fake by asserting it.** Take the shape whole.
2. **🟢 One arithmetic, taught once, reused five times.** Reverse little-endian → decimal → ×512 →
   go to offset. It appears for the MBR partition start, the partition size, and then four GPT LBA
   fields. **That is what fluency looks like in a 20-minute row** — one skill, many applications.
3. **🟢 Two ways to find the same boundary.** The MBR ends at 512 bytes — count 32 rows of 16 bytes,
   *or* look for `55 AA`. Teaching both gives students a check on themselves.
4. **🟢 Cross-check the hex against the OS's own view.** The room shows the partition table in HxD
   and then the same partitions in Windows Disk Management. Cheap, and it builds the habit of
   corroborating a raw reading against an independent source.
5. The **mixed-endian GUID** procedure is fiddly enough that it needs the step-by-step treatment the
   room gives it — do not summarise it in our material, reproduce the steps.

### 🔴 What we must NOT copy — the third safety defect in the S4 block

**Task 5 has students open the evidence image in HxD, type corrected bytes over it, and save in
place.** The room even coaches them past the *"There is not enough space on the disk"* warning by
**declining the backup** and saving anyway.

That is a direct violation of **R9** — hash, then work on a copy; working on an original image is a
defect, not a shortcut — and it destroys the ability to prove the evidence was not tampered with,
which is criterion 1 of the D20 rubric.

**Our `S4-10` does the same exercise on a verified copy**, with the hash recorded before and after,
and the original untouched. The repair is the same two edits; the difference is the discipline.

This is now the **third** method defect in the S4 block:
| room | defect |
|---|---|
| 6 · FAT32 | paste a recovered PowerShell script into a live shell |
| 8 · File Carving | `binwalk -e` on supplied images with no isolation (CVE-2022-4510) |
| **9 · MBR/GPT** | **edit and save the evidence image in place** |

Three rooms, three different ways to compromise an investigation. **Collectively they are the best
argument our course has for why method is taught before tooling** — and a ready-made S1 discussion:
*"here are three published forensics exercises; find what each one does wrong."*

## 6. Question patterns

~20 questions across 8 tasks. Tasks 4 and 7 are read-only with a single completion gate.

- **Recall questions are cheap but well targeted** — POST, which firmware supports GPT, the magic
  number, max partitions. These test the structure facts an exam actually asks for.
- **🟢 Computation questions carry the room**, and they are the transferable ones: *"size of the
  second partition (rounded to the nearest GB)"* forces reverse → decimal → ×512 → convert;
  *"partition type GUID of the 2nd partition"* forces the mixed-endian rule; *"first byte at the
  starting LBA of the partition"* forces the locate-and-jump procedure. **All three are answerable
  from a 512-byte file with no VM** — the same cheap-homework property FAT32 had.
- **The Task 5 chain is a real investigation in miniature**: how many partitions → what is at the
  repaired LBA → partition type → size → the flag inside the recovered filesystem. **Each answer
  is only reachable if the previous repair was correct**, which is self-verifying by design.
- **Still no explicit "cannot be determined" answer** — ninth room. Candidates this room hands us,
  and they are strong: *"the `55 AA` signature is wrong — was this malware or a bad sector?"* →
  **cannot be determined from the MBR alone** (§2.3, and the room states both causes) ·
  *"the GPT header CRC32 does not match — does that prove tampering?"* → **no** (§2.5).

## 7. Figures we would need to draw

The room references a boot-process flow diagram and an MBR structure diagram but delivers both as
images; the rest are HxD screenshots. Three need our own inline SVG:

| what is needed | our SVG spec (one line) |
|---|---|
| the 512-byte MBR, to scale | one horizontal bar divided proportionally — **446 bytes bootloader · 64 bytes partition table (four 16-byte cells) · 2 bytes `55 AA`** — with the four cells expanded below into the six labelled fields, captioned "64 bytes decide whether the disk exists" |
| MBR vs GPT layout | two stacked disk strips: MBR = one sector doing everything; GPT = protective MBR (sector 0) · header (1) · entry array (2+) · **… backup array · backup header at the far end** — with a dashed link joining primary and backup, captioned "the map, and the copy of the map" |
| the LBA arithmetic | a four-step strip — bytes as stored → reversed → decimal → **× 512 → offset** — using the room's own `00 08 00 00` → `2048` → `1,048,576`, since that single chain is reused five times in the room |

The third is the highest-value diagram in the S4 block: it is one picture that unlocks both this
room and the FAT32 room. Never their images (D22).

## 8. Fit against our material

### ✅ Part 1's mapping is correct — fourth room in a row

Mapped to `S4` / `S4-04` `S4-05`. Correct, and it also supplies `S4-10`.

### Rows this strengthens

- **`S4-04`** *"MBR partitioning — structure, partition table, boot record"*, 18 min — **fully
  sourced**: byte offsets, all six partition-entry fields, both computations, `55 AA`.
- **`S4-05`** *"GPT partitioning — header, entries, protective MBR"*, 15 min — **fully sourced**,
  and richer than the row implies: the row names three components, the room gives **five** (the two
  backups) plus the ESP. The backups are the forensically interesting part and should be in the row.
- **`S4-10`** *"Case 04 — wiped partition table, recover it and prove the recovery"*, 35 min
  **[INVESTIGATION]** — **the room supplies the whole case shape**, including the FTK Imager
  verification. See §5.
- **`S2-06`** FTK Imager — a second worked path, and a nice non-obvious use: *reading* a broken
  image to confirm a repair, not acquiring one.

### One row-text amendment worth proposing

`S4-05` currently reads *"GPT partitioning — header, entries, protective MBR"*. Suggest:
*"…header, entries, protective MBR, **and the backup header/array that make GPT recoverable**"*.
No minute change — the backups are the reason GPT replaced MBR, and they are the cross-check that
`S4-04` has no equivalent for.

### Minutes

`S4-04` (18) + `S4-05` (15) = **33 min** against the room's 80, with `S4-10` (35) taking the case.
Same remedy as rooms 6–8: the byte-level computations are **ideal homework** — a 512-byte file,
no VM, self-checking answers. **S4 stays at 220. This room adds 0 rows.**

**S4 is now fully sourced across four rooms (6, 7, 8, 9) with a net cost of zero minutes:**
`S4-03` · `S4-04` · `S4-05` · `S4-06` · `S4-07` · `S4-08` · `S4-09` · `S4-10` all have material.
Only `S4-01`/`S4-02` (HDD/SSD internals) remain unsourced from THM — and they are physical-media
topics no room in this path covers.

**S5 remains at 65 minutes overdrawn** (rooms 1–5).

### Out of scope

Nothing. Entirely on-topic. The bootkit/ransomware/wiper survey in Tasks 4 and 7 is attacker
context our students already have from CEH/eCIR — **reference it, do not re-teach it**
(`scope_decisions.md` line 193).

## 9. Links

- Room: <https://tryhackme.com/room/mbrandgptanalysis>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 1)
- Partition-type byte reference (MBR) and partition-type GUID lookup (GPT) — the room links both;
  worth keeping as linked resources for `S4-04`/`S4-05` (link, never rehost — D22).
- Malware families the room cites for the ATT&CK/context slide: **Petya** (encrypts the MBR),
  **Bad Rabbit** (overwrites the MBR with its own bootloader), **Shamoon** (overwrites the MBR with
  random data). Useful, verifiable names for a case-hook page.
- Tool currency for HxD and FTK Imager: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md`

END OF NOTE.
