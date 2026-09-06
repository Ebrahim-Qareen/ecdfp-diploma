---
room: NTFS Analysis
url: https://tryhackme.com/room/ntfsanalysis
module: File System Analysis (Section 1 of Advanced Endpoint Investigations)
feeds: S4 — `S4-07` NTFS (direct hit) · `S4-08` MFTECmd/Timeline Explorer (direct hit) ·
       `S4-03` slack. Also `S2-06` FTK Imager, and it independently confirms the
       `$LogFile` finding from `_TOOL_CURRENCY_2026-08-28.md`.
difficulty / time: Medium · **90 min** · 8 tasks · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

NTFS structure and its four forensically important metadata files, worked on a **live** Windows
volume: `$MFT`, `$LogFile`, `$UsnJrnl:$J`, and `$I30`. Acquisition is FTK Imager against the
physical drive; parsing is MFTECmd into CSV, read in Timeline Explorer.

The strongest content is the **MFT column reference** (§2.2) and the **USN reason-code table**
(§2.6) — both are the kind of lookup material a student needs in front of them during an exam and
which our `S4-07`/`S4-08` rows currently only gesture at.

It is also the room where **a defect we predicted from the tool documentation shows up in
practice** — see §3. That makes it unusually valuable as a teaching example, quite apart from its
content.

## 2. Artifacts — one 6-box block each

### 2.1 Partition Boot Sector (PBS)

- **What it is** — the first sector of an NTFS volume; the equivalent of FAT32's boot sector.
- **Where it lives** — sector 0 of the volume. Contents named by the room: jump instruction to
  bootstrap code · file-system type indicator · **location of the MFT and the MFT Mirror** ·
  the BIOS Parameter Block · end-of-sector marker **`0x55AA`**.
- **What it proves** — where the `$MFT` and `$MFTMirr` start, and the volume's cluster geometry.
  Everything else on the volume is located from here.
- **What it does NOT prove** — nothing about files or activity. And a `0x55AA` signature proves
  the sector is *formatted as* bootable, not that the volume boots or was ever booted.
- **How to parse it** — FTK Imager's structure view, or a hex editor at offset 0.
- **Anti-forensics / false-positive caveat** — the room states the right one: the PBS is a
  **rootkit and bootkit target**, so it is checked for tampering and for BPB integrity. Cross-check
  against the volume's backup boot sector, exactly as in FAT32.

### 2.2 `$MFT` — the Master File Table

- **What it is** — the database holding one record per file and directory on the volume.
- **Where it lives** — volume root, located via the PBS. **Fixed-size records, typically 1 KB.**
  Each record holds attributes: File Name · Standard Information (link count, timestamps, flags) ·
  attributes (MACB, read-only, hidden…) · **File Data — resident inside the record if the file is
  small enough, otherwise a pointer to clusters** · File Index · Security Information (ACL).
- **What it proves** — the room's parsed-CSV column reference, which is the most useful thing in
  the room:
  | column | what it gives you |
  |---|---|
  | **Entry Number** | unique record id |
  | **Parent Entry Number** | reconstructs the directory tree |
  | **Sequence Number** | **increments when a record is REUSED** — separates an old file from a new one occupying the same entry |
  | File Name | |
  | **Timestamps** | creation · modification · access · **MFT-record modification** (metadata) |
  | Flags | file / directory / unused |
  | Entry Flags | read-only, hidden, system — hidden+system is a malware tell |
  | **In Use** | **false = the record persists but the file is deleted** |
  | Logical Size | actual data size |
  | Physical Size | allocated size — the difference **is slack** |
- **What it proves, in one line** — that a file **existed**, with its full metadata and position in
  the tree, **even after deletion**.
- **What it does NOT prove** — content, unless the file was small enough to be resident. It does
  not prove *who* acted, and — critically — **`In Use = false` does not mean the data is still
  recoverable**, only that the record survives. And a **reused** entry (rising Sequence Number)
  means the previous occupant's record is gone: absence of a record is not absence of a file.
- **How to parse it** — `MFTECmd.exe -f <$MFT> --csv <dir> --csvf <name>.csv`, then Timeline
  Explorer. ⚠️ see §3 for a defect in the room's own version of this command.
- **Anti-forensics / false-positive caveat** — the room does not state one for `$MFT` directly, but
  its MACB discussion supplies it: **timestomping.** Unlike FAT32, NTFS gives you a second opinion —
  `$MFT` `$STANDARD_INFORMATION` timestamps versus `$FILE_NAME` timestamps, and the `$UsnJrnl`.
  ⚠️ **The room never makes the `$SI` vs `$FN` distinction**, which is the single most important
  timestomp-detection technique in NTFS. **Our `S4-07` must add it — this room will not supply it.**

### 2.3 `$MFTMirr` — the MFT mirror

- **What it is** — a duplicate of the **first few records** of the `$MFT`.
- **Where it lives** — a separate area of the disk, located via the PBS.
- **What it proves** — a redundant copy for cross-verifying `$MFT` integrity when the primary is
  damaged or altered.
- **What it does NOT prove** — 🔴 **it is NOT a full backup.** It mirrors only the first few
  records — the metadata files themselves, not user files. The room's phrasing ("duplicate copy of
  the first few records") is correct, but a student skimming will remember "backup of the MFT" and
  be wrong. **Say the limit out loud.**
- **How to parse it** — same tooling as `$MFT`.
- **Anti-forensics / false-positive caveat** — a mismatch between `$MFT` and `$MFTMirr` in the
  mirrored range is a tampering indicator; agreement across only those few records proves nothing
  about the rest.

### 2.4 NTFS system files

- **What it is** — the reserved metadata files that run the filesystem.
- **Where it lives** — the volume root. The room's list: `$MFT` · `$MFTMirr` · **`$LogFile`** ·
  **`$Bitmap`** (allocated vs free clusters) · `$Boot` · **`$BadClus`** (bad sectors) ·
  `$UpCase` (case-insensitive comparison table). `$UsnJrnl` lives under **`$Extend`**.
- **What it proves** — the room flags three as forensically interesting and is right about each:
  `$LogFile` gives a history of filesystem operations · `$Bitmap` shows recent cluster allocation
  and deletion · **`$BadClus` may expose sectors deliberately marked bad to hide data.**
- **What it does NOT prove** — `$Bitmap` is a current-state map, not a history; a free cluster does
  not mean the data is gone. And a genuinely bad sector is far more common than a hiding place —
  `$BadClus` entries are a lead, never a finding.
- **How to parse it** — FTK Imager to export; MFTECmd for the ones it supports (see §3).
- **Anti-forensics / false-positive caveat** — `$BadClus` abuse is the classic one and the room
  names it.

### 2.5 `$LogFile` — the transaction journal

- **What it is** — NTFS's write-ahead metadata transaction log. Records metadata changes **before**
  they are committed, so the volume can be replayed or rolled back after a crash.
- **Where it lives** — volume root.
- **What it proves** — the room says "a history of file system operations", and per our currency
  check the fuller truth is that it records the **before and after** of each metadata operation —
  making it the highest-fidelity journal NTFS has.
- **What it does NOT prove** — 🔴 **anything older than a few hours.** It is a small, **fixed-size
  circular** file; oldest records are overwritten continuously, commonly holding only **two to
  three hours** of normal usage. **The room never mentions this**, which is a serious omission: a
  student who finds nothing in `$LogFile` may conclude nothing happened.
- **How to parse it** — 🔴🔴 **the room never does.** It names `$LogFile` as one of NTFS's two
  journals, tells students in Task 4 to **export it to the Evidence folder**, and then analyses
  only `$J`. No explanation is given. **The reason is that MFTECmd — the only parser the room
  teaches — cannot parse it** (see §3). Use **dfir_ntfs** (GPL-3.0, CLI) or **NTFS Log Tracker**.
- **Anti-forensics / false-positive caveat** — the short retention *is* the caveat, and it is the
  reason `$LogFile` and `$UsnJrnl` are used together rather than interchangeably.

### 2.6 `$UsnJrnl:$J` — the change journal

- **What it is** — a higher-level record of changes to files, directories and attributes.
- **Where it lives** — **`$Extend\$UsnJrnl`**, with two components:
  **`$Max`** (journal maximum size and allocation policy) and **`$J`** (the actual change records).
  ✅ **`$J` is itself implemented as an Alternate Data Stream** — a genuinely good detail that ties
  §2.8 to journaling, and the room states it.
- **What it proves** — a per-change record with a reason code. The room's opcode table, worth
  lifting into our cheat sheet:
  | reason | meaning |
  |---|---|
  | `USN_REASON_DATA_OVERWRITE` | data overwritten |
  | `USN_REASON_DATA_EXTEND` | file grew |
  | `USN_REASON_DATA_TRUNCATION` | file shrank |
  | `USN_REASON_NAMED_DATA_OVERWRITE` | **an alternate data stream** was overwritten |
  | `USN_REASON_NAMED_DATA_EXTEND` | an ADS was extended |
  | `USN_REASON_FILE_CREATE` | created |
  | `USN_REASON_FILE_DELETE` | **deleted** |
  | `USN_REASON_RENAME_OLD_NAME` | renamed — **old name recorded** |
  | `USN_REASON_CLOSE` | handle closed after changes |
  Rename tracking is the standout: `$J` lets you follow a file through renames and to deletion,
  which no other artifact in this room does.
- **What it does NOT prove** — **it records that a change happened and the file it happened to —
  not what the change was.** No original data, no before/after content. That is precisely the
  division of labour with `$LogFile`: **`$J` for the long tail of *what* was touched, `$LogFile`
  for the short high-fidelity window of *how*.** The room lists the distinction as a key point but
  never demonstrates it, because it never parses `$LogFile`.
- **How to parse it** — `MFTECmd.exe -f <$J> --csv <dir> --csvf USNJrnl.csv`. MFTECmd correctly
  auto-identifies the input as a USN journal.
  ⚠️ **Add `-m <$MFT>` to resolve parent paths** — without it the `$J` output has no full paths.
  **The room does not use `-m`** (see §3).
- **Anti-forensics / false-positive caveat** — the room states none. Ours: `$J` is trimmed lazily
  at NTFS checkpoints once it exceeds `MaximumSize + AllocationDelta`, so retention is
  volume-and-activity dependent — **longer than `$LogFile`, but not unbounded.** Teach the
  contrast as relative, never as a fixed number of days.

### 2.7 `$I30` — the index allocation attribute

- **What it is** — a directory's index of the files and subdirectories it contains.
- **Where it lives** — **inside a directory**, as an NTFS Index Allocation attribute. Visible per
  directory in FTK Imager.
- **What it proves** — filename · **From Slack** · file size · parent directory · **MACB
  timestamps** · attributes (read-only, hidden, directory/file, archive/compressed/encrypted,
  system). Its real value: **entries for files that were deleted, renamed or moved out of the
  directory persist in the index's slack**, so `$I30` can show what a folder used to contain.
- **What it does NOT prove** — that the file still exists anywhere, or where it went. A slack entry
  is a residue of a past index state — it survives **only until overwritten**, so absence proves
  nothing. It also carries no content.
- **How to parse it** — `MFTECmd.exe -f <$I30> --csv <dir>\ --csvf i30.csv`, then filter the
  **From Slack** column to isolate the departed entries. ✅ `$I30` support is real — our currency
  check found it in MFTECmd's in-code file-type list; **note it is missing from MFTECmd's README**,
  so this room is the practical confirmation.
- **Anti-forensics / false-positive caveat** — the room states none. The slack is overwritten as
  the directory changes, so a busy directory retains little; a quiet one retains a lot. **Volume of
  slack evidence is a function of directory activity, not of attacker carelessness.**

### 2.8 Alternate Data Streams (ADS)

- **What it is** — additional named data streams attached to a file or directory beyond its primary
  stream.
- **Where it lives** — attached to any NTFS file or directory; `$UsnJrnl:$J` is itself one.
- **What it proves** — that extra content is associated with a file **without changing the file's
  apparent size or appearance in a directory listing**.
- **What it does NOT prove** — ADS is a legitimate NTFS feature in constant benign use (the
  Zone.Identifier mark-of-the-web is the everyday example). **Presence of an ADS is not evidence of
  hiding.** The room introduces ADS in Task 4 and then never demonstrates finding one — no `dir /r`,
  no `Get-Item -Stream`, no worked example. **A real gap for us to fill in `S4-07`.**
- **How to parse it** — **the room teaches no method.** Ours to supply.
- **Anti-forensics / false-positive caveat** — see above; also note ADS do not survive a copy to
  FAT32 or exFAT, which is both an evidence-loss risk and a detection opportunity.

## 3. Tools and commands

| tool | version the room uses | exact command / action | what it outputs |
|---|---|---|---|
| **FTK Imager** | **not stated** | `File > Add Evidence Item > Physical Drive` → first option → `Partition > NONAME [NTFS] > [root]` | live volume structure |
| FTK Imager | — | select → right-click → **Export Files** to `Desktop\Evidence` | `$MFT`, `$LogFile`, `$I30`, `$Extend`, `$UsnJrnl` |
| **MFTECmd** | **not stated** | `MFTECmd.exe --help` | switch list |
| MFTECmd | — | `MFTECmd.exe -f ..\Evidence\$MFT --csv ..\Evidence --csvf ..\Evidence\MFT_record.csv` | parsed MFT CSV — ⚠️ **defective, see below** |
| MFTECmd | — | `MFTECmd.exe -f ..\Evidence\$J --csv ..\Evidence --csvf USNJrnl.csv` | parsed USN journal CSV |
| MFTECmd | — | `MFTECmd.exe -f ..\Evidence\$I30 --csv ..\Evidence\ --csvf i30.csv` | parsed `$I30` CSV |
| **Timeline Explorer** | **not stated** | opens the CSV automatically | sortable / filterable grid |

### CURRENCY CHECK — verified 2026-08-28, cross-referenced to `_TOOL_CURRENCY_2026-08-28.md`

| item | result |
|---|---|
| 🔴🔴 **`$LogFile` — the prediction confirmed in the wild** | Our currency pass found that **MFTECmd does not parse `$LogFile`** — its source says `"$LogFile not supported yet. Exiting"` — **while its own README still lists `$LogFile` as supported.** This room is the practical consequence: it names `$LogFile` as one of NTFS's two journals, has students **export it in Task 4**, and then **never parses it**, without a word of explanation. Students collect evidence the taught toolset cannot open. **Teach the truth and name the alternative: `dfir_ntfs` (GPL-3.0, CLI, parses `$MFT`, `$J` and `$LogFile`) or NTFS Log Tracker 1.9.** |
| ✅ `$I30` supported | confirmed in MFTECmd's in-code file-type list (`$MFT \| $J \| $Boot \| $SDS \| $I30`) and demonstrated by this room — **but absent from the README.** Second independent case of MFTECmd's README being wrong. |
| 🔴 **the room's `$MFT` command is malformed** | `--csv` is the **directory**; `--csvf` is a **file name**. The room's Task 5 passes a **full path** to `--csvf` (`..\Evidence\MFT_record.csv`) while its Task 6 and Task 7 pass a bare name (`USNJrnl.csv`, `i30.csv`). **The room contradicts itself between tasks.** Teach the bare-filename form. |
| ⚠️ **`-m` missing for `$J`** | parsing `$J` without `-m <$MFT>` leaves the CSV **with no parent paths**. The room omits it entirely. Any lab of ours that parses `$J` must include it. |
| ⚠️ `--body` / `--bdl` | not used by the room, but if we teach bodyfile output for `mactime`, **`--body` requires `--bdl`**, and `--bdl` takes the drive letter alone. |
| **MFTECmd / Timeline Explorer** | **2026.5.0**, MIT (MFTECmd). Timeline Explorer publishes **no licence text** — do not print a licence claim. |
| **FTK Imager** | free build is now **8.3**, and Exterro ships a separate **FTK Imager Pro** line. Pin the product and version in our setup guide. |
| Room's version claims | **none stated for any tool** — seventh room running. |

## 4. Evidence used

- A **live Windows VM** with FTK Imager, EZ Tools and Timeline Explorer pre-installed. Evidence is
  exported from the running physical drive into `Desktop\Evidence`.
- **Size: not stated. Not downloadable. No licence offered. Not reusable.**
- Lab credentials published inline again — **deliberately not recorded here (R8).**
- **Nothing to flag for `ecdfp-evidence`.**
- ⚠️ **Methodological note worth teaching:** this room acquires from a **live physical drive** with
  no write blocker, no hashing, and no chain of custody. Room 4 (`expregistryforensics`) argues at
  length that live acquisition leaves traces and that cold acquisition behind a write blocker is
  what makes a result reproducible and court-defensible. **The path contradicts itself between
  rooms, and our version follows room 4.** Contrast the two in class — it is a free lesson in why
  method matters more than tooling.

## 5. Lab design worth reusing

1. **🟢 The column reference in Task 5 is the single most reusable asset in the room.** Each MFT
   CSV column with *Description* and *Importance*. That is exactly the shape of a cheat-sheet page
   (Part 8 requires one per session with a Print button), and it converts to our format unchanged.
   The **Sequence Number** and **In Use** entries in particular are the ones students misread.
2. **🟢 Collect once, parse many.** Task 4 exports every metadata file into one Evidence folder;
   Tasks 5–7 then parse them one at a time. That mirrors a real triage workflow and means the
   acquisition step is taught once rather than repeated — good use of scarce class minutes.
3. **🟢 Same tool, three inputs, auto-detected type.** MFTECmd is pointed at `$MFT`, then `$J`, then
   `$I30`, and it identifies each. **One command shape, three artifacts** — that is a timed tool
   repetition in the exam's sense, and it is the cheapest fluency we can build.
4. The `$I30` **From Slack** filter is a neat single-click demonstration of "this directory used to
   contain more than it does" — visual, immediate, and hard to misread.

What **not** to copy: the live-drive acquisition with no integrity step (§4); the unexplained
`$LogFile` dead end (§3); and the room's habit of naming a concept (ADS, `$Bitmap`, `$BadClus`)
without ever demonstrating how to find it.

## 6. Question patterns

~15 questions across 8 tasks; T5 carries 7 and T6 carries 4.

- **Single-artifact discipline is strong.** Each question names the artifact implicitly by the task
  it sits in: MFT for entry numbers, parent paths and In-Use state; `$J` for rename counts and
  deletion times; `$I30` for slack counts and parent entries.
- **🟢 The best question in the room is a negative one**: *"According to the MFT record, is the
  anti-forensics tool currently present on the disk? (yay or nay)"* — the answer comes from the
  **In Use** column, and it teaches that **the record persisting is not the file persisting.**
  That is the closest any room in this batch has come to a criterion-4 question. **Adopt this
  exact shape.**
- **`$J` rename-chain questions** ("what was the file called before renaming", "how many rename
  operations against `secret_code.txt`", "when was it deleted") build a small narrative from one
  artifact. Good model for `S4-08`.
- **Still zero explicit "this cannot be determined" answers** — seventh room. But this room supplies
  two ready-made candidates and both are strong:
  - *"From `$J` alone, can you determine what the file contained when it was overwritten?"* → **no**
    (the room states `$J` records the change, not the data).
  - *"You found nothing in `$LogFile` for last Tuesday. Does that prove nothing happened?"* → **no**
    (circular, hours of retention).

## 7. Figures we would need to draw

Screenshots throughout of FTK Imager and Timeline Explorer — click paths and answers. Three concepts
need our own inline SVG:

| what is needed | our SVG spec (one line) |
|---|---|
| the two journals, side by side | a single time axis with two retention bands drawn to scale — `$LogFile` a narrow high-detail band ("before **and** after, ~hours"), `$UsnJrnl:$J` a long thin band ("what changed, not how, ~days-weeks") — captioned "the same event, two different memories" |
| an MFT record, resident vs non-resident | one record box with its attribute list, drawn twice: small file with `$DATA` **inside** the record; large file with `$DATA` as a pointer out to cluster runs — captioned "under ~700 bytes, the file IS the record" |
| what `$I30` slack retains | a directory index drawn as a row of entries, three greyed and struck through, labelled **From Slack**, with the live folder listing beside it showing only four — the room's own worked example, drawn |

The first is the one this room needed and does not have; it is also the diagram that carries the
`_TOOL_CURRENCY` finding. Never their images (D22).

## 8. Fit against our material

### ✅ Part 1's mapping is correct — second room in a row

Mapped to `S4-07` `$MFT`, ADS. Correct, and it also serves `S4-08`.

### Rows this strengthens

- **`S4-07`** — *"NTFS — `$MFT`, resident vs non-resident, ADS, `$LogFile` and `$UsnJrnl`"*, 20 min.
  The room covers every element of that row. **Two things it does NOT give us and we must source
  elsewhere: the `$SI` vs `$FN` timestamp comparison (§2.2) and any ADS detection method (§2.8).**
- **`S4-08`** — *"MFTECmd and Timeline Explorer — parsing `$MFT` to CSV"*, 10 min. The room supplies
  the exact command shape, the column reference, and — usefully — **two more input types** (`$J`,
  `$I30`) at no extra command complexity. `S4-08` should teach all three; it is the same motion.
- **`S4-03`** slack — `$I30` slack is a second, sharper example alongside file/volume slack.
- **`S2-06`** FTK Imager — a worked export path, though with the integrity caveat in §4.

### 🔴 `S4-07` must decide what to say about `$LogFile`

The row text names `$LogFile`. The taught toolset (`MFTECmd`, per `S4-08`) **cannot parse it**.
Three honest options for `ecdfp-intake`:

1. **Teach `$LogFile` conceptually and name `dfir_ntfs` as the tool**, without a hands-on step.
   Cost: ~2 min. Keeps the row honest and gives students somewhere to go.
2. **Add `dfir_ntfs` as a hands-on step.** Cost: ~8 min, and a new tool on the FOR-WS01 image.
3. **Drop `$LogFile` from the row text** and say in `scope_decisions.md` that NTFS journaling is
   taught via `$UsnJrnl` only.

**Recommendation: option 1.** It costs almost nothing, it is truthful, and — because MFTECmd's own
README wrongly claims `$LogFile` support — it doubles as the course's best live example of why the
tool-currency check exists. **This room and the currency file together make that lesson concrete.**

### Minutes

`S4-07` (20) + `S4-08` (10) = **30 min** against the room's 90. As with FAT32, we are not obliged
to match — but the same remedy applies: the `$J` rename-chain exercise and the `$I30` slack filter
are ideal **homework**, needing only the exported CSVs, no VM. **S4 stays at 220. This room adds 0
new rows**, and at most 2 minutes if option 1 above is taken — findable inside `S4-07`'s existing 20.

**S5 remains at 65 minutes overdrawn** (rooms 1–5). S4 is now confirmed sound across two rooms.

### Out of scope

Nothing. Entirely on-topic.

## 9. Links

- Room: <https://tryhackme.com/room/ntfsanalysis>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 1)
- Room's stated prerequisites: **FAT32 Analysis** (extracted — room 6) and **MBR and GPT Analysis**
  (Priority 1, not yet extracted). Our S4 order matches.
- `_TOOL_CURRENCY_2026-08-28.md` block C — MFTECmd's `$LogFile` refusal, the `$SI`/`$FN` gap,
  `dfir_ntfs` and NTFS Log Tracker as the alternatives, and the `$LogFile` vs `$UsnJrnl` retention
  answer for `S4-07`.

END OF NOTE.
