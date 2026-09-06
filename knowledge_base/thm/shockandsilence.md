---
room: Shock and Silence
url: https://tryhackme.com/room/shockandsilence
module: **Honeynet Collapse — stage 5 of 6.** *"Investigate the fifth, File System part of the
        Honeynet Collapse!"* Challenge room (Priority 2). Target `DC-01` (172.16.2.4, **CORE**) —
        the domain controller.
feeds: 🟢🟢 **The most `S4`-relevant room in the whole extraction.** `S4-07` (`$MFT`, ADS,
       `$LogFile`, `$UsnJrnl`), `S4-08`, `S2-04`/`S2-05` (physical vs logical imaging) and `S6-09`.
       🔴🔴 **Carries the single best "cannot be determined" finding of the project: the room's own
       Q3 is structurally unanswerable from the evidence the room supplies** (§2.5).
       🟢🟢 **And Q5 is the first question in 27 rooms that deliberately tests a limit** (§6).
difficulty / time: **Hard** · 60 min · 2 tasks · 6 questions (5 scored + 1 "Let's go!") · Premium ·
                   1,209 completions · 23 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, scenario, lab paths, tips and all question stems.
              0 sections NOT READ.
              🔴 **Room ships a plaintext RDP password in the task body — not reproduced (R8).**
              Seventh Priority-2 room to do so.
              ⚠️ **The ransom note's contents are referenced by the scenario but not shown in the
              task text**, and the lab was not started — so Q5's evidence was NOT READ.
              ⚠️ **Answers NOT READ.** §2 reconstructed from the 5 scored questions, the scenario
              paragraph and the named evidence file, as for rooms 18–26.
---

## 1. What the room teaches

**That the evidence you are given determines which questions can be answered — and this room hands
over evidence that cannot answer one of its own questions.**

The image is named in the tips: **`.\Artifacts\DC-01-NTFS-Logs.ad1`**, described as *"Disk image
containing NTFS logs"*. Two things follow, and neither is decoration:

1. 🔴🔴 **`.ad1` is a *logical* container, not a disk image.** AccessData's own guide: *"AD1 and L01
   are both custom content images, and contain full file structure, but do not contain any drive
   geometry other other physical drive data"* — against E01/raw images, which *"are drive images that
   have the disk, partition, and file structure as well as drive data."* **So there is no unallocated
   space, no slack, no carving, and nothing that was not deliberately exported.** §2.1.
2. 🔴🔴🔴 **`$UsnJrnl` does not record which process made a change**, and Microsoft says so: the
   change journal *"logs only the fact of a change to a file and the reason for the change"* and
   *"does not record enough information to allow reversing the change."* **So Q3 — *"Which executable
   file initiated the encryption process on the system?"* — cannot be answered from NTFS logs.**
   §2.5.

🟢 **The room is almost certainly leaning on the ransomware binary's *filename appearing in the
journal* when it was written to disk** — which is a real and useful inference, but it is
**"a binary of this name was created shortly before the encryption began"**, not **"this executable
performed the encryption."** ⚠️ **The room's stem asserts the second.** **That gap is the most
teachable thing in the module**, and §6 makes it the corpus's best "cannot be determined" row.

**🟢🟢 And then the room does something no other room in 27 has done. Q5 reads:**

> *"**Go beyond the obvious** — which ransomware group targeted the organisation?"*

**"Go beyond the obvious" is a question deliberately warning that the surface answer is wrong** — and
the research says exactly why it would be. Ransom notes and file extensions identify a **payload
family**, not an actor: **the LockBit 3.0 and Babuk builders were leaked**, and Sophos documents
crews *"deploying ransomware in an environment, purporting to be LockBit, and hoping that referencing
a prolific and well-known ransomware scheme will be enough to convince victims to pay."* 🟢🟢 **A
question that punishes attribution-by-extension is the first question in the corpus that tests a
limit rather than a lookup, and it deserves loud credit** (§6).

**The scenario is the module's "shock", and its framing is the best of the six:**

> *"Logan Hall had enjoyed a productive week and decided Friday was the perfect time to roll out new
> Group Policies to the DC-01 domain controller. Confident and calm, he remoted in — but what he saw
> made his blood run cold."*

⚠️ **Friday afternoon, on a domain controller, by an administrator with legitimate reason to be
there.** 🟢 **Note the trap the scenario sets and does not spring:** Logan was about to push Group
Policy from a DC, which is the classic domain-wide ransomware deployment path (**T1484.001**). **The
room never says GPO was the vector** — so *"was Logan's planned change the delivery mechanism, or a
coincidence?"* is a genuine open question the evidence must settle. **Do not assume it. §2.8.**

**And the evidence is honest about its own poverty:** *"a partial disk image of DC-01 acquired
**after** the encryption."* 🟢🟢 **Acquired after** is the key phrase — every timestamp on the volume
has been touched by the encryption run, and the acquisition captured the aftermath, not the event.

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 5 scored questions, the scenario and the named evidence file. Mapping:
the image itself → 2.1 · Q1 → 2.2 · Q2 → 2.3 · Q3 → 2.4 and 2.5 · Q4 → 2.6 · Q5 → 2.7 ·
the DC context → 2.8.

### 2.1 The AD1 logical image — what it is, and what it cannot contain

- **What it is** — the entire evidence base: `DC-01-NTFS-Logs.ad1`.
- **Where it lives** — `.\Artifacts\` on the analyst Desktop. **AD1 is AccessData's / Exterro's
  *custom content image* format**, produced by **FTK Imager** (current free version **8.3**;
  ⚠️ release date **NOT VERIFIED**). PRONOM: *"The AccessData Custom Content Image (AD1) file format
  is a file-level disk image format."*
- **What it proves** — that these specific files, with their metadata and folder paths, existed as
  exported.
- **What it does NOT prove** — 🔴🔴🔴 **anything about what was not exported, and that is most of the
  disk.** AccessData's guide states the loss plainly: AD1/L01 *"contain full file structure, but do
  not contain any drive geometry other other physical drive data."* **So the image has no
  unallocated space, no file slack, no deleted-and-unlinked records, no carveable fragments, no
  partition table and no volume geometry** — and **nothing the examiner did not tick.**
  🔴🔴 **Which means several natural investigative moves are simply unavailable here:** carving the
  deleted ransom note, recovering an overwritten `$LogFile` region, examining the pagefile, or
  checking whether the `$MFT` has entries the export omitted. **"I could not find X" on this image
  never distinguishes *X was not there* from *X was not collected*.**
  ⚠️ **And the selection was made by someone else, before you arrived** — **the scope of the
  acquisition is itself a finding to report**, not a given.
- **How to parse it** — 🔴🔴 **and here is the practical shock: almost nothing opens it.**
  **Autopsy and The Sleuth Kit cannot** — the feature request has been open since 2015, and the
  requester notes *"I haven't come across any open source tools that read AD1 images."*
  **Arsenal Image Mounter cannot** — its supported list is Raw/DMG/AFF4/E01/Ex01/S01/VHD/VDI/XVA/
  VMDK/OVA/qcow, **with no AD1 or L01.** 7-Zip only via the third-party **Forensic7z** plugin. There
  is one community tool, **AD1-tools** (Linux, v1.0, July 2024: `ad1info`, `ad1verify`, `ad1extract`,
  `ad1mount`). **On Windows, FTK Imager is effectively the only mainstream free route in.**
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the format choice is a teaching artifact in its
  own right, and it belongs in `S2-05`.** A logical image is the right tool for a targeted collection
  and the wrong one for an unknown-scope incident — **and a ransomware case on a domain controller is
  the definition of unknown scope.** ⚠️ **Teach the trade honestly:** AD1 is small, fast and
  defensible for *"collect these named artifacts"*; it forecloses every question you have not yet
  thought to ask. **On this evidence the examiner inherits someone else's guess about what mattered.**

### 2.2 `Zone.Identifier` — recovering the download URL

- **What it is** — Q1: *"What is the full URL from which the ransomware was downloaded to the
  system?"*
- **Where it lives** — an **NTFS alternate data stream** on the downloaded file, fully qualified as
  **`file.exe:Zone.Identifier:$DATA`**, containing an INI-style block:
  `[ZoneTransfer]` with **`ZoneId`**, and — this is the part that answers Q1 — **`HostUrl`** and
  **`ReferrerUrl`**. 🟢 **`HostUrl` is the direct URL of the file; `ReferrerUrl` is the page it was
  linked from.** **`ZoneId=3` means Internet** (0 Local Machine · 1 Local intranet · 2 Trusted ·
  3 Internet · 4 Restricted).
- **What it proves** — 🟢🟢 **that Windows recorded this file as arriving from that URL**, which is a
  remarkably direct answer to a question that usually needs browser artifacts. **It is also the
  cheapest possible demonstration that ADS are not exotic** — they are a default Windows mechanism
  carrying evidence, which is exactly `S4-07`'s point.
- **What it does NOT prove** — 🔴🔴 **that the URL is present at all, because writing it is
  application-dependent.** *"HostUrl and ReferrerUrl are set by Microsoft Edge and Google Chrome"*;
  Firefox writes the stream but only began including URL information **from February 2021**. **A bare
  `[ZoneTransfer] ZoneId=3` with no URL is a completely normal result** — it means the file came from
  the internet and the writing application did not record where.
  🔴 **Private browsing suppresses it entirely** — *"If this is done in incognito mode, then the URL
  is not recorded."*
  🔴🔴 **And the stream is fragile in a specific, teachable way: it exists only on NTFS.** It
  *"is only preserved on NTFS volumes. Files moved to FAT32, exFAT, or network shares using non-NTFS
  file systems will lose the stream."* 🟢 It **does** survive an NTFS→NTFS copy.
  ⚠️ **Archive extraction is the modern variable.** Archivers generally propagate the mark now —
  *"many archiving utilities will copy the MoTW from a download ZIP file to the extracted files.
  Sometimes this needs to be configured, like with 7-Zip"* — and **failing to propagate it is now a
  tracked vulnerability class**: CVE-2025-0411 / ZDI-25-045, *"When extracting files from a crafted
  archive that bears the Mark-of-the-Web, 7-Zip does not propagate the Mark-of-the-Web to the
  extracted files."* **So absence of the stream on an extracted file may mean the archiver, not the
  attacker.**
  ⚠️ **The URL is attacker-supplied data** — a redirector or a compromised legitimate host tells you
  where the bytes came from, not who owns the campaign.
- **How to parse it** — `dir /r`, `Get-Item -Stream *`, `Get-Content -Stream Zone.Identifier`, or
  `streams.exe`. 🟢 **`MFTECmd` surfaces the ADS from the `$MFT`** — an ADS is a *named `$DATA`
  attribute* in the record — **but names and sizes only; the content still needs extraction.**
  🟢🟢 **And `$UsnJrnl` records the stream's creation**: `USN_REASON_STREAM_CHANGE` (`0x00200000`) —
  *"A named stream is added to or removed from a file, or a named stream is renamed."*
- **Anti-forensics / false-positive caveat** — ⚠️ **the stream is trivially removable** —
  `Unblock-File`, or a copy through any non-NTFS medium — and **its absence is therefore weak
  evidence**. 🟢 **Its presence, however, is strong**, because it is written by the OS rather than by
  the attacker, and **an attacker who deletes it leaves a `STREAM_CHANGE` record in `$UsnJrnl` that
  outlives the stream.**

### 2.3 The original filename — what the journal remembers that the disk forgot

- **What it is** — Q2: *"What was the original file name of the ransomware executable downloaded to
  the host?"* The file was renamed after download; the current name is not the answer.
- **Where it lives** — **`$UsnJrnl:$J`**, in a matched pair Microsoft defines exactly:
  **`USN_REASON_RENAME_OLD_NAME` (`0x00001000`)** — *"The file or directory is renamed, and the file
  name in the USN_RECORD_V2 structure is the previous name"* — and **`USN_REASON_RENAME_NEW_NAME`
  (`0x00002000`)** — *"…the file name in the USN_RECORD_V2 structure is the new name."*
  Corroboration: the **`$MFT`**'s `$FILE_NAME` attributes, and `$LogFile` if the window is short
  enough (**C8**: hours, not days).
- **What it proves** — 🟢🟢 **that a file with a given `FileReferenceNumber` was known by name A and
  then by name B.** The **file reference number is the join key** — it is what makes the pair a *pair*
  rather than two unrelated names, and it is the thing students forget to use.
- **What it does NOT prove** — 🔴🔴 **that the rename was the attacker's, or that "original" means
  what the question implies.** A file may be renamed many times; **`$UsnJrnl` gives a sequence, and
  "original" is whichever end of that sequence the journal still reaches.** 🔴 **The journal is
  finite** — trimmed lazily at NTFS checkpoints past `MaximumSize` + `AllocationDelta` (**C8**) — so
  **an earlier rename may simply have aged out, and the "original" name you find may be an
  intermediate one.** ⚠️ **That is a limitation to state, not a caveat to omit.**
  🔴 **And a name is not an identity.** The same bytes under two names is one file; two different
  binaries under one name is two files. **The `FileReferenceNumber` distinguishes them; the name
  does not.**
- **How to parse it** — `MFTECmd` over `$J` with `-m` for parent paths (**C4**), into Timeline
  Explorer; **sort by `FileReferenceNumber`, not by name**, and read the record sequence.
  ⚠️ **`MFTECmd` does not parse `$LogFile`** despite its own README (**C1**) — for `$LogFile` use
  NTFS Log Tracker or equivalent.
- **Anti-forensics / false-positive caveat** — 🟢 **renaming is not anti-forensics here, it is
  ordinary tradecraft**, and the journal defeats it cheaply. ⚠️ **The genuine anti-forensic move is
  to disable or delete the journal** (`fsutil usn deletejournal`), which is loud: a journal that
  starts abruptly, or is absent on a server, is itself a finding.

### 2.4 The encryption run as a pattern in `$UsnJrnl`

- **What it is** — the signature of mass encryption, and the evidence behind Q3 and Q4.
- **Where it lives** — `$UsnJrnl:$J`, as thousands of records in a repeating per-file shape.
  Microsoft's definitions for the relevant reasons: **`USN_REASON_DATA_OVERWRITE` (`0x00000001`)** —
  *"The data in the file or directory is overwritten"*; **`USN_REASON_DATA_EXTEND` (`0x00000002`)** —
  *"The file or directory is extended (added to)"*; **`USN_REASON_FILE_CREATE` (`0x00000100`)**;
  **`USN_REASON_FILE_DELETE` (`0x00000200`)**; **`USN_REASON_CLOSE` (`0x80000000`)**.
- **What it proves** — 🟢🟢 **the shape, the scale and the timing of the encryption**, which is the
  most defensible thing this image can give. A documented real-world pattern: *"Each original file
  generates a `DATA_OVERWRITE` record (content replaced with ciphertext), followed by a
  `RENAME_NEW_NAME` record (extension changed to `.locked`), followed by `FILE_DELETE` for the Volume
  Shadow Copy deletion commands"*, at roughly **1,200 files per minute** in that case.
  🟢 **The rate is itself evidence** — a human does not rename a thousand files a minute, so the
  pattern distinguishes automated encryption from user activity without needing any other artifact.
- **What it does NOT prove** — 🔴🔴 **that the files were encrypted.** `$UsnJrnl` records **that data
  was overwritten and the file renamed** — *"only the fact of a change to a file and the reason for
  the change."* **It does not contain the data**, so *"the contents are now ciphertext"* is an
  inference from the file's current state, not from the journal.
  🔴 **Nor does it give an exact start and end.** The journal is trimmed lazily, and the image was
  *"acquired after the encryption"* — **the beginning of the run may have been trimmed while the end
  survives.** ⚠️ **Report the observed first and last record, and say they bound the run rather than
  define it.**
  ⚠️ **`FILE_DELETE` for shadow-copy deletion is a *correlation*, not proof of `vssadmin`** — the
  deletions appear as file deletions like any other (block **N3**).
- **How to parse it** — `MFTECmd` over `$J`; sort by timestamp; **count records per minute** to
  establish the rate; group by reason flag. 🟢 **Timeline Explorer's grouping is the right tool** and
  this is a genuinely good exercise for `S4-08`.
- **Anti-forensics / false-positive caveat** — ⚠️ **legitimate bulk operations look similar** — a
  backup agent, an antivirus full scan, a large `robocopy`, a disk-encryption rollout. 🟢 **The
  discriminators are the rename pattern (a *new extension* applied uniformly), the absence of a
  corresponding change record, and the hour** — not the volume of records alone.

### 2.5 🔴 Process attribution — the question this evidence cannot answer

- **What it is** — Q3: *"Which executable file initiated the encryption process on the system?"*
- **Where it lives** — 🔴🔴🔴 **nowhere in the evidence provided.** `USN_RECORD_V2` has **no process
  or PID field**, and Microsoft is explicit: the change journal *"logs only the fact of a change to a
  file and the reason for the change (for example, write operations, truncation, lengthening,
  deletion, and so on)"*, and *"It does not record enough information to allow reversing the
  change."* **`$MFT` and `$LogFile` carry no process attribution either.**
  **Process attribution requires artifacts this image does not contain:** Security **4688** with
  command-line auditing (**L1** — off by default), **Sysmon 1**, **Prefetch**, **Amcache**, or memory.
- **What it proves** — with the journal alone: **that a binary of a given name was created on the
  volume, and that a mass-encryption pattern began shortly afterwards.**
- **What it does NOT prove** — 🔴🔴🔴 **that the binary did it. This is the sharpest gap in the whole
  extraction, and it is in a graded question.** The defensible finding is:
  > *"`<name>.exe` was written to `<path>` at T₁; a mass `DATA_OVERWRITE` + `RENAME` pattern affecting
  > N files began at T₂, ninety seconds later. The change journal records no process attribution, so
  > the causal link between the two is an inference from proximity and is not established by this
  > evidence."*
  **That is a finding, a method and a stated limitation — D20 criteria 2, 3 and 4 — and it is a
  better answer than the room's expected one.**
  ⚠️ **Temporal proximity is the weakest form of causal argument**, and on a domain controller with
  ordinary administrative activity it is weaker still.
  🔴 **The honest escalation is to say what would settle it:** Prefetch (execution, no arguments —
  **L1**), Amcache (presence, not execution — **L2**), 4688 with command line, or a memory image
  (**M1**). **All four are absent from an `.ad1` of NTFS logs** (§2.1). **Naming the artifact you
  would need is itself a professional deliverable.**
- **How to parse it** — you cannot, from this image. 🟢 **The exercise is to establish the bound and
  request the rest** — which is what a real DFIR engagement does on day one.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **note that no anti-forensics was required to
  produce this gap.** The attacker did not remove process attribution from `$UsnJrnl`; **it was never
  there.** ⚠️ **That is a different and more important lesson than "the attacker deleted the
  evidence": some evidence is not deleted, it is simply never recorded** — the same shape as **L1**'s
  command-line finding, one layer down.

### 2.6 The appended extension — an identifier of a family, not an actor

- **What it is** — Q4: *"What file extension was appended to the encrypted files?"*
- **Where it lives** — the `RENAME_NEW_NAME` records (§2.3) and the `$MFT`'s `$FILE_NAME` attributes.
  🟢 **Trivially recoverable, and the one question in the room this evidence answers cleanly.**
- **What it proves** — that files were renamed to carry that suffix.
- **What it does NOT prove** — 🔴🔴 **the payload family, and certainly not the actor.** §2.7 is the
  full argument; in short, extensions are **configurable, reused and impersonated.** ⚠️ **And it does
  not prove encryption** (§2.4) — a rename is a rename. **A file with a strange extension that still
  opens is a wiper's decoy or a failed run, and both happen.**
  ⚠️ **Nor is the extension necessarily uniform** — some families vary it per host or per victim,
  which means **"the extension" may be a sample of one.**
- **How to parse it** — `MFTECmd` over `$J`; group by the new suffix; **count distinct extensions**,
  because more than one is a finding in itself.
- **Anti-forensics / false-positive caveat** — 🟢 **the extension is the most-quoted and
  least-probative artifact in a ransomware case**, which makes it the perfect object lesson: **it is
  the first thing everyone reports and the thing that supports the least weight.**

### 2.7 The ransom note and attribution — the room's best question

- **What it is** — Q5: *"**Go beyond the obvious** — which ransomware group targeted the
  organisation?"* ⚠️ **The note's contents were NOT READ** (the scenario references it; the task text
  does not reproduce it, and the lab was not started).
- **Where it lives** — the `ReadMe` file on the Desktop, plus the extension (§2.6) and whatever
  infrastructure the note names.
- **What it proves** — 🟢 **that a note bearing these markings was written to the volume.** That is
  the whole of the direct evidence.
- **What it does NOT prove** — 🔴🔴🔴 **which group did it, and the reason is structural rather than
  evidential:**
  1. **Builders leak.** SentinelOne: *"Source code leaks further complicate attribution, as more
     actors will adopt the tools"*, noting *"a noticeable trend that actors increasingly use the
     Babuk builder."* **A leaked builder emits output indistinguishable from the original crew's.**
  2. **Brands are impersonated deliberately.** Sophos, on the leaked LockBit 3.0 builder — *"which
     enabled any attacker to use it"* — records actors *"deploying ransomware in an environment,
     purporting to be LockBit, and hoping that referencing a prolific and well-known ransomware
     scheme will be enough to convince victims to pay."*
  3. **RaaS separates the payload from the operator.** Affiliates share one builder; the payload
     identifies the *service*, not the *customer*.
  4. **Brands rebrand**, and old notes persist.
  🟢🟢 **So the correct phrasing is "consistent with an X-family payload", never "attributed to group
  X"** — and that phrasing is a D20 criterion-4 deliverable.
- **How to parse it** — read the note; record the extension, the note filename, the contact and
  payment infrastructure, and any campaign identifier **as findings**; **treat the family label as an
  interpretation and name its basis and date.** ⚠️ **Do not visit attacker infrastructure** — the
  same handling rule as room 26 §2.5.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the room's own framing is the caveat, and this
  is the first time in 27 rooms that has been true.** *"Go beyond the obvious"* tells the student the
  surface answer is wrong. **Whether the intended answer is a decoy, a reused builder, or a detail in
  the infrastructure, the question shape teaches the right instinct**, and it is the one question in
  the corpus we should copy almost unaltered.

### 2.8 A domain controller as the target — what the host being a DC changes

- **What it is** — the scenario context: `DC-01`, encrypted, with the admin *"about to roll out new
  Group Policies"* when he found it.
- **Where it lives** — DC-specific artifacts, **almost none of which are in this image** (§2.1):
  `NTDS.dit` and its logs, `SYSVOL` (the GPO file store), the Directory Service and DFS Replication
  event channels, and the registry hives.
- **What it proves** — that the encrypted host held the domain's authentication database and its
  policy distribution point.
- **What it does NOT prove** — 🔴🔴 **that Group Policy was the deployment vector, and the scenario
  invites exactly that assumption.** Pushing ransomware to every domain member via GPO from a DC is
  the classic domain-wide play — **ATT&CK `T1484.001`, now named *"Domain or Tenant Policy
  Modification: Group Policy Modification"*** 🔴 (**the parent was renamed from "Domain Policy
  Modification"**), tactics **Defense Impairment and Privilege Escalation**.
  🟢 **But the room never claims it**, and the honest position is that **testing it requires `SYSVOL`
  and the Directory Service logs — neither of which is in an `.ad1` of NTFS logs.** ⚠️ **A student
  who reports "deployed via GPO" from this evidence has produced an interpretation with no supporting
  artifact**, and that is precisely the failure D20 criterion 4 exists to catch.
  🔴🔴 **Encrypting a DC also destroys the recovery path**, which is why the module's opening line —
  *"the backups corrupted and all SIEM data wiped clean"* — lands here: **the host that would
  authenticate a restore is the host that is encrypted.**
- **How to parse it** — from this image, you cannot pursue the DC-specific angle at all. 🟢 **The
  deliverable is the request:** name `SYSVOL`, the Directory Service channel, and the GPO version
  numbers as the evidence that would resolve it.
- **Anti-forensics / false-positive caveat** — ⚠️ **the most dangerous artifact here is the plausible
  story.** Ransomware on a DC + an admin about to edit Group Policy is a narrative that assembles
  itself, and **the evidence supplied cannot test it.** 🟢🟢 **That makes this room an unusually good
  exercise in refusing a tempting conclusion**, which is worth more than the four answerable
  questions combined.

## 3. Tools and commands

The room supplies tools rather than naming them: *"Analysis tools are located at `.\DFIR-Tools\*`"*.

| purpose | command | note |
|---|---|---|
| open the evidence | **FTK Imager 8.3** | 🔴🔴 **Autopsy and TSK cannot open `.ad1`** — #1 |
| download URL (Q1) | `Get-Content <file> -Stream Zone.Identifier` · `dir /r` · `streams.exe` | 🟢 **`HostUrl`** is the file's URL — #2 |
| ADS from the MFT | `MFTECmd -f $MFT` | 🟢 names and sizes only; content needs extraction |
| original name (Q2) | `MFTECmd -f $J -m` → Timeline Explorer | 🟢 **join on `FileReferenceNumber`** — #3 |
| encryption pattern (Q3/Q4) | `MFTECmd -f $J`; group by reason; count records/minute | 🟢 the rate is evidence — #3 |
| `$LogFile` | **NTFS Log Tracker**, not MFTECmd | 🔴 **MFTECmd does not parse `$LogFile`** (**C1**) |
| process attribution | — | 🔴🔴🔴 **not available from this evidence** — #4 |

⚠️ **`MFTECmd`'s `--body` requires `--bdl`** (**C3**); `$J` needs `-m` for parent paths (**C4**).

### CURRENCY CHECK

🟢 **Blocks C1–C8 already carry `$MFT`/`$LogFile`/`$UsnJrnl` semantics and tooling**, verified
2026-08-28. **Not re-researched.** This pass covers the format, the ADS, the reason flags and
attribution.

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"Disk image containing NTFS logs … `.ad1`"* | 🔴🔴 **AD1 is a *logical* container, not a disk image, and almost nothing opens it.** AccessData's guide: *"AD1 and L01 are both custom content images, and contain full file structure, but do not contain any drive geometry other other physical drive data"* — against *"E01, S01, AFF, and 001 (RAW/dd) images are drive images that have the disk, partition, and file structure as well as drive data."* PRONOM: *"a file-level disk image format."* **So: no unallocated space, no slack, no deleted/unlinked records, no carving, no partition table, and nothing not deliberately exported.** 🔴 **Autopsy/TSK cannot read it** — feature request open since **2015**, with the requester noting *"I haven't come across any open source tools that read AD1 images."* **Arsenal Image Mounter cannot** (its list is Raw/DMG/AFF4/E01/Ex01/S01/VHD/VDI/XVA/VMDK/OVA/qcow — no AD1/L01). 7-Zip only via the **Forensic7z** plugin. One community tool: **AD1-tools** (Linux, v1.0, Jul 2024). **On Windows, FTK Imager is effectively the only mainstream free route.** **FTK Imager 8.3, Exterro, still free** — *"Start your investigations with the free, trusted industry standard."* ⚠️ **8.3's release date NOT VERIFIED.** | [Cerbero, AD1](https://blog.cerbero.io/ad1-format-package/) · [PRONOM fmt/842](https://www.nationalarchives.gov.uk/pronom/fmt/842) · [FTK Imager 3.1.4 user guide](https://arts.unimelb.edu.au/__data/assets/pdf_file/0011/2970587/Imager-3_1_4_UG.pdf) · [Autopsy issue #1402](https://github.com/sleuthkit/autopsy/issues/1402) · [AIM FAQ](https://arsenalrecon.com/products/arsenal-image-mounter/faqs) · [AD1-tools](https://github.com/al3ks1s/AD1-tools) · [Exterro FTK Imager](https://www.exterro.com/digital-forensics-software/ftk-imager) |
| 2 | Q1: *"the full URL from which the ransomware was downloaded"* | 🟢🟢 **`Zone.Identifier` answers it, and `HostUrl` is the field.** MS-FSCC gives the stream as `sample.txt:Zone.Identifier:$DATA` containing `[ZoneTransfer]` / `ZoneId=3`; **ZoneId 3 = Internet** (0 Local Machine · 1 Local intranet · 2 Trusted · 3 Internet · 4 Restricted). Worked example: `ReferrerUrl=https://www.7-zip.org/download.html`, `HostUrl=https://www.7-zip.org/a/7z1900.exe` — *"both the referrer, and the direct URL of the file"*. 🔴 **But the URL fields are application-dependent**: *"HostUrl and ReferrerUrl are set by Microsoft Edge and Google Chrome"*; **Firefox only began including URL information in February 2021**; and *"If this is done in incognito mode, then the URL is not recorded."* **A bare `ZoneId=3` with no URL is a normal result.** 🔴 **NTFS-only** — *"Files moved to FAT32, exFAT, or network shares using non-NTFS file systems will lose the stream"* — though it survives NTFS→NTFS copies. ⚠️ **Archive propagation is a live issue**: archivers generally propagate MotW now (*"Sometimes this needs to be configured, like with 7-Zip"*), and **failure to do so is a tracked vulnerability class** — CVE-2025-0411 / ZDI-25-045: *"When extracting files from a crafted archive that bears the Mark-of-the-Web, 7-Zip does not propagate the Mark-of-the-Web to the extracted files."* 🟢 `MFTECmd` surfaces the ADS (a named `$DATA` attribute) — **names and sizes only.** 🟢 Its creation appears in `$UsnJrnl` as **`USN_REASON_STREAM_CHANGE` (`0x00200000`)** — *"A named stream is added to or removed from a file, or a named stream is renamed."* | [MS-FSCC Zone.Identifier](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/6e3f7352-d11c-4d76-8c39-2516a9df36e8) · [MS zone values](https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms537183(v=vs.85)) · [xkln, identifying the source](https://xkln.net/blog/identifying-the-source-of-downloaded-files/) · [dfir.co.za](https://www.dfir.co.za/2018/06/18/highway-to-the-danger-zone-identifier/) · [SANS ISC 31732](https://isc.sans.edu/diary/31732) · [ZDI-25-045](https://www.zerodayinitiative.com/advisories/ZDI-25-045/) |
| 3 | Q2/Q4: renames recoverable from NTFS logs | 🟢 **Yes, and Microsoft defines the flags exactly.** **`USN_REASON_RENAME_OLD_NAME` `0x00001000`** — *"The file or directory is renamed, and the file name in the USN_RECORD_V2 structure is the previous name"*; **`USN_REASON_RENAME_NEW_NAME` `0x00002000`** — *"…the file name … is the new name."* Also **`DATA_OVERWRITE` `0x00000001`**, **`DATA_EXTEND` `0x00000002`**, **`FILE_CREATE` `0x00000100`**, **`FILE_DELETE` `0x00000200`**, **`CLOSE` `0x80000000`**. 🟢🟢 **Encryption signature, documented in the field:** *"Each original file generates a `DATA_OVERWRITE` record (content replaced with ciphertext), followed by a `RENAME_NEW_NAME` record (extension changed to `.locked`), followed by `FILE_DELETE` for the Volume Shadow Copy deletion commands"*, at roughly **1,200 files/minute**. **The rate is itself evidence** — no human renames a thousand files a minute. ⚠️ **Join renames on `FileReferenceNumber`, not on name.** ⚠️ **The journal is trimmed lazily** (**C8**), and the image was acquired *after* the encryption — **the start of the run may have aged out; report first and last observed records as bounds.** | [MS `USN_RECORD_V2`](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2) · [MS change journal records](https://learn.microsoft.com/en-us/windows/win32/fileio/change-journal-records) · [Mjolnir, $UsnJrnl](https://intel.mjolnirsecurity.com/artifact-usnjrnl) |
| 4 | Q3: *"Which executable file initiated the encryption process?"* | 🔴🔴🔴 **NOT ANSWERABLE FROM THIS EVIDENCE, and this is the strongest finding of the extraction.** `USN_RECORD_V2` has **no process or PID field**, and Microsoft states the limit twice: the change journal *"logs only the fact of a change to a file and the reason for the change (for example, write operations, truncation, lengthening, deletion, and so on)"* and *"It does not record enough information to allow reversing the change."* **`$MFT` and `$LogFile` carry no process attribution either.** Attribution needs **4688 + command-line auditing** (off by default — **L1**), **Sysmon 1** (not installed by default), **Prefetch** (execution, no arguments — **L1**), **Amcache** (presence, not execution — **L2**), or **memory** (**M1**) — **and an `.ad1` of NTFS logs contains none of them** (#1). 🟢 **The room is presumably relying on the binary's *filename appearing in the journal* when it was written to disk — which supports "a binary of this name was created shortly before the run began", not "this executable performed the encryption."** | [MS change journal records](https://learn.microsoft.com/en-us/windows/win32/fileio/change-journal-records) · [MS `USN_RECORD_V2`](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2) |
| 5 | Q5: *"Go beyond the obvious — which ransomware group…"* | 🟢🟢 **The room is right to warn, and the reason is structural.** **Builders leak:** SentinelOne — *"Source code leaks further complicate attribution, as more actors will adopt the tools"*, with *"a noticeable trend that actors increasingly use the Babuk builder."* **Brands are impersonated:** Sophos on the leaked LockBit 3.0 builder — *"which enabled any attacker to use it"* — records actors *"deploying ransomware in an environment, purporting to be LockBit, and hoping that referencing a prolific and well-known ransomware scheme will be enough to convince victims to pay."* **Plus RaaS separating payload from operator, and rebranding.** 🟢 **Correct phrasing: "consistent with an X-family payload", never "attributed to group X."** | [SentinelOne, leaked Babuk](https://www.sentinelone.com/labs/hypervisor-ransomware-multiple-threat-actor-groups-hop-on-leaked-babuk-code-to-build-esxi-lockers/) · [Sophos, LockBit in action](https://www.sophos.com/en-us/blog/lockbit-in-action) |
| 6 | ATT&CK for this chain | ✅ **T1486** Data Encrypted for Impact → **Impact** · **T1105** Ingress Tool Transfer → **Command and Control** · **T1490** Inhibit System Recovery → **Impact** · **T1489** Service Stop → **Impact**. 🔴 **T1484.001 has been renamed** — the parent is now ***"Domain or Tenant Policy Modification"***, so the sub-technique is **"Domain or Tenant Policy Modification: Group Policy Modification"**, tactics **Defense Impairment and Privilege Escalation**. ✅ Repo grepped: `T1484` appears nowhere — forward-looking only. ⚠️ **Version reporting is genuinely inconsistent across MITRE's own pages** — the updates row reads *"ATT&CK v19 | August 6, 2026 | Current version of ATT&CK | v19.2 on MITRE/CTI"*, while `index.json` lists to v19.1 (12 May 2026) and v19.0 at 28 Apr 2026. **Block L7's rule stands and is now doubly justified: cite the version, never the date.** | [T1486](https://attack.mitre.org/techniques/T1486/) · [T1105](https://attack.mitre.org/techniques/T1105/) · [T1489](https://attack.mitre.org/techniques/T1489/) · [T1484.001](https://attack.mitre.org/techniques/T1484/001/) |

### NOT VERIFIED — carried forward honestly

- **FTK Imager 8.3's release date** — no dated release-notes page reachable.
- **The ransom note's contents**, and therefore what Q5's *"beyond the obvious"* points at.
- **Whether Group Policy was the deployment vector** — the scenario invites it; the evidence cannot
  test it (§2.8).
- **Whether this room's `.ad1` contains `$LogFile` as well as `$MFT` and `$J`** — *"NTFS logs"* is
  ambiguous and the distinction matters (**C8**: hours vs days of retention).
- **AD1-tools' maturity** — v1.0, July 2024, one author. **Do not put it in a lab without testing.**

## 4. Evidence used

**One logical image, `DC-01-NTFS-Logs.ad1`, plus a tool folder — both on the analyst Desktop.**

- **Downloadable?** ⚠️ **No.** **Reusable?** 🔴 **No.**
- **`ecdfp-evidence` action: none.** 🔴 **Sixth room running with no evidence set.** `EVS-10` remains
  unallocated. ⚠️ **The entire Honeynet Collapse module is live-VM-only — six for six.** **Our S4/S5
  Windows intrusion image must come from `EVI-SRC01` (D19) or CFReDS (D36).**

### 🟢🟢 The evidence format is the most valuable thing in the room

Every other room's evidence disposition has been *"can't use it, move on."* **This one changes what
we teach**, because **`S2-05` already has a row for image formats — *"E01 vs raw (dd) vs AD1"*** —
and this room supplies the missing half of it:

- **A logical image is a defensible answer to a scoped question and a trap for an unscoped one.**
  AD1 is small, fast, and exactly right for *"collect these named artifacts"*. On a ransomware
  incident of unknown scope it **forecloses every question the collector did not anticipate.**
- 🔴 **And the toolchain constraint is a lab-build fact, not a footnote:** our students work in
  **Autopsy** (`S2-06`, `S4`), and **Autopsy cannot open an AD1.** **If we ever hand out a logical
  image, FTK Imager must be in `CLEAN-TOOLS` (D17) and the students must be told why.**
- 🟢 **Best exercise it suggests:** give students the *same* incident twice — once as an E01 and once
  as an AD1 of "the important files" — and ask which questions each can answer. **That is `S2-04`'s
  physical-vs-logical row made real, at the cost of one extra export.**

### Critique of the scenario brief

🟢 **The narrative is the module's most vivid and its least prejudicial about *technique*.** It
describes what Logan saw — unfamiliar extensions, unreadable files, a ReadMe on the Desktop — and
stops. **It does not tell the student how the ransomware arrived, what it was, or who sent it.**
After five rooms of briefs that narrate the whole attack, **this one narrates only the discovery**,
which is exactly the position a real responder starts from.

⚠️ **One structural honesty problem, and it is the room's, not the story's:** *"analyze the only
available evidence — a partial disk image of DC-01 acquired after the encryption."* **The brief
acknowledges the evidence is partial and then asks a question that partiality makes unanswerable**
(§2.5). 🟢 **Our version turns that into the point:** state the evidence is partial, ask the student
to establish what they can, **and grade them on correctly identifying what they cannot.**

⚠️ **And the acquisition has no provenance again** — no hash, no tool, no operator, no time. Same
disposition as rooms 25 and 26: **noted, deliberately not counted as a defect** (`lostinramslation.md`
§4), because it is near-universal across the corpus and counting it late would be arbitrary.

## 5. Lab design worth reusing

### 5.1 🟢🟢 A question that warns you the obvious answer is wrong

Q5's *"Go beyond the obvious"* is **the single best question stem in 27 rooms**, and the reason is
that it inverts the usual failure: instead of asserting a conclusion in the stem (nine rooms running,
§6), **it warns the student that the surface artifact will mislead them.**

**Adopt the construction directly.** It is the closest thing in the corpus to a *"cannot be
determined"* question that a challenge platform can express — the platform needs a string answer, so
the room cannot accept *"unknowable"*, **but it can point the student past the artifact that looks
like the answer.** 🟢🟢 **Our version can go one step further and accept the honest answer**, because
our assessment is a written report (**D20/D21**), not a text box. **That is a concrete advantage of
report-based assessment and worth saying to students.**

### 5.2 🟢🟢 Evidence that is deliberately partial

*"Analyze the only available evidence — a partial disk image of DC-01 acquired after the
encryption."* 🟢 **Adopt for `S6-09`.** Real engagements begin with whatever survived, and **an
exercise built on complete evidence teaches a habit that never applies.**

⚠️ **But pair it with the fix the room omits (§4):** grade the student on **what they correctly
report as unrecoverable**, and require them to **name the artifact that would settle it** (§2.5).
🟢 **"Here is what I would need next, and why" is a professional deliverable**, and it is assessable.

### 5.3 🟢🟢 The evidence format as a lesson — `S2-04`/`S2-05`

§4 covers it. **The best single exercise this room suggests:** the same incident supplied twice,
once as **E01** and once as an **AD1 of "the important files"**, with the question *"which questions
can each answer?"* 🔴 **And the toolchain fact must ship with it: Autopsy cannot open an AD1**
(§3 #1), so **FTK Imager belongs in `CLEAN-TOOLS` (D17)** if we ever hand one out.

### 5.4 🟢 A narrative that stops at the discovery

§4 covers it. **Adopt the framing for D19's incident report exercise** — describe what the person
saw, not what happened. **Five of six rooms narrate the attack; this one narrates the moment of
discovery, and it is the better model.**

### 5.5 🟢 Safety and handling defects

**None new.** Offline analysis of a supplied image with supplied tools — **the correct pattern for
the third room running.**

🟢🟢 **Rooms 25, 26 and 27 are now a clean block of three**, and the reason is structural rather than
editorial: **stages 1–2 are live response by nature; stages 3–5 are post-incident analysis of
captured artifacts.** ⚠️ **That is worth teaching as its own point** — *the correct handling rule
depends on where in the incident you are standing* — and this module walks through both halves in
order, which is a better demonstration than a slide.

**Running total: 10 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24. Four endanger the analyst's
machine; six endanger the evidence. Unchanged for three rooms.**

## 6. Question patterns

**Five scored questions, the shortest set in the module**, tracing download → rename → execution →
extension → attribution. 🟢 **The order is the intrusion's order** and each answer feeds the next.

**🟢🟢 Q5 is the best question stem in the corpus** (§5.1) — the first that warns the student the
obvious artifact will mislead. **Twenty-seven rooms, one such question.**

**⚠️ But Q3 is the worst-founded question in the corpus**, and the two sit in the same room. *"Which
executable file initiated the encryption process on the system?"* asks for **process attribution from
NTFS logs**, which carry none (§2.5). 🔴 **The evidence supports "a binary of this name was written
shortly before the run", and the stem asserts causation.**

**⚠️ Stems assert conclusions, again** — *"the ransomware was downloaded"* · *"the ransomware
executable"* · *"initiated the encryption process"*. **Tenth room running.** 🟢 **Mildly defensible
here**, since the encryption is established fact from the scenario rather than a conclusion to prove.

**⚠️ No answer formats and no timezone**, on a room whose central artifact is a timestamped journal.

**🔴 Twenty-seventh room, no "cannot be determined" question — but Q5 is the closest any room has
come**, and the tally deserves the nuance:

| the room could have asked | correct answer |
|---|---|
| *"Which executable initiated the encryption?"* — **the room's own Q3** | 🔴🔴🔴 **Cannot be determined from this evidence.** `USN_RECORD_V2` has no process field; the journal *"logs only the fact of a change to a file and the reason for the change."* **The defensible answer is a bound plus a stated limitation plus a named next artifact.** **The best row in the entire corpus, because the evidence *and* the question are both the room's own.** |
| *"No `Zone.Identifier` on the binary. Was it downloaded from the web?"* | 🔴🔴 **Cannot be determined.** The stream is NTFS-only and is lost on any FAT32/exFAT/non-NTFS hop; incognito suppresses the URL; some applications never write one; and `Unblock-File` removes it. **Absence is weak evidence.** 🟢 **Its *presence*, though, is strong — it is written by the OS, not the attacker.** |
| *"`ZoneId=3` but no `HostUrl`. What was the download URL?"* | 🔴 **Unknown.** URL fields are application-dependent — set by Edge and Chrome, absent from Firefox before Feb 2021, suppressed in private browsing. **A bare `ZoneId=3` is a normal, complete result.** |
| *"The journal's earliest rename gives the original name. Is that the original?"* | ⚠️ **Not established.** `$UsnJrnl` is trimmed lazily; **the earliest surviving rename may be an intermediate one.** |
| *"N files were renamed to `.xyz`. Were they encrypted?"* | 🔴 **Not from the journal.** It records *that* data was overwritten and the file renamed, **not the data** — *"It does not record enough information to allow reversing the change."* **A rename is a rename; encryption is inferred from the files' current state.** |
| *"The extension and note match family X. Which group attacked?"* | 🔴🔴 **Cannot be determined.** Leaked Babuk and LockBit builders, RaaS affiliates sharing one builder, deliberate impersonation, rebranding. **"Consistent with an X-family payload", never "attributed to group X."** 🟢 **And the room agrees — this is what Q5 is testing.** |
| *"The admin was about to push GPO. Was GPO the delivery vector?"* | 🔴🔴 **Cannot be determined from an `.ad1` of NTFS logs** — testing it needs `SYSVOL`, the Directory Service channel and GPO version numbers, none of which are in the image. **The most tempting wrong answer in the room** (§2.8). |
| *"Nothing was recovered from unallocated space. Was nothing deleted?"* | 🔴🔴 **No — there is no unallocated space in a logical image.** *"AD1 and L01 … do not contain any drive geometry other other physical drive data."* **"I could not find X" here never distinguishes *X was absent* from *X was not collected*.** |

🟢🟢 **Eight rows, and three of them turn on the evidence format rather than the artifacts** — which
is new. ⚠️ **The pattern established over rooms 24–27 is now unambiguous: the "cannot be determined"
answer is repeatedly the *correct* answer to questions these rooms actually ask.** **The course
rationale should stop describing this as a gap in question design and start describing it as a
correctness finding about existing material.**

## 7. Figures

**No room-specific figure.** ⚠️ Images were **not enumerated** for this room — the module's pattern
(one reused topology SVG plus decorative assets) was established in rooms 23–24 and the DOM query was
not re-run. **Recorded as not-checked.**

🔴 **Eighth room running with no conceptual figure**, on a room about image formats, alternate data
streams and journal record structure — three things that are genuinely hard to describe in prose.

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F28 | **Physical vs logical image** | One disk drawn twice. **Left (E01/raw):** partition table, file system, allocated files, **slack and unallocated shaded and labelled**. **Right (AD1/L01):** only the ticked files and their metadata, with everything else greyed out and captioned *"not absent — never collected."* Footer strip: **"Autopsy opens the left one only."** | **🔴 P1** | §2.1 and `S2-04`/`S2-05`. The single most reusable figure this room suggests, and it fixes a row we already have. |
| F29 | **Anatomy of `Zone.Identifier`** | A file icon with a second stream branching off it, labelled `file.exe:Zone.Identifier:$DATA`, opened to show `[ZoneTransfer]`, `ZoneId=3`, `ReferrerUrl` (the page) and **`HostUrl` (the file) highlighted**. Side notes: *"Edge/Chrome write URLs; incognito does not"*, *"lost on FAT32/exFAT"*. | **🔴 P1** | §2.2 — makes ADS concrete for `S4-07` and answers a real investigative question. |
| F30 | **The encryption signature** | A `$UsnJrnl` extract as a repeating three-record block per file — `DATA_OVERWRITE` → `RENAME_OLD_NAME`/`RENAME_NEW_NAME` → `CLOSE` — stacked to show scale, with a **records-per-minute counter** in the margin and a human-activity baseline for contrast. | **🔴 P1** | §2.4 — the rate as evidence, and the best `S4-08` exercise in the corpus. |
| F31 | **What the journal does not have** | A `USN_RECORD_V2` drawn field by field, with a conspicuous **empty slot where a PID would be**, and arrows to the four artifacts that *do* attribute (4688+cmdline, Sysmon 1, Prefetch, memory) each tagged with whether it is on by default. | **🔴 P1** | §2.5 — the corpus's strongest "cannot be determined", as a picture. Pairs with **F14** (room 24) and **F19** (room 25). |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 5"* — correct, and it undersells it badly.

**This is the most `S4`-relevant room in the entire extraction**, and it also fixes an `S2` row we had
only half-specified. Amend the Part 1 row to name **`S4-07`, `S4-08`, `S2-04` and `S2-05`**.

### Rows this strengthens

- **`S4-07`** (*"NTFS — `$MFT`, resident vs non-resident, **ADS**, `$LogFile` and `$UsnJrnl`"*) —
  🟢🟢 **the row already lists ADS and this room gives it a purpose.** `Zone.Identifier` turns ADS
  from a curiosity into the artifact that answers *"where did this file come from"* — with figure
  **F29**, the `HostUrl`/`ReferrerUrl` distinction, and the NTFS-only fragility.
- **`S4-08`** (*"MFTECmd and Timeline Explorer — parsing `$MFT` to CSV"*) — 🟢🟢 **the encryption
  signature (§2.4) is the best exercise we have found for this row**: parse `$J`, group by reason
  flag, **count records per minute**, and show that the *rate* is the evidence. Figure **F30**.
  ⚠️ Reinforces **C4** (`-m` for parent paths) and **C1** (MFTECmd does **not** parse `$LogFile`).
- **`S2-04`/`S2-05`** (physical vs logical acquisition; image formats *"E01 vs raw (dd) vs AD1"*) —
  🟢🟢 **the row names AD1 and this room supplies what it means**: what a logical image loses, and
  🔴 **that Autopsy cannot open one.** Figure **F28**, plus §5.3's two-format exercise.
  🔴 **Lab-build consequence: if we ever hand out a logical image, FTK Imager must be in
  `CLEAN-TOOLS` (D17).**
- **`S6-09`** (capstone) — 🟢🟢 **deliberately partial evidence** (§5.2), graded on what the student
  correctly reports as unrecoverable and which artifact they request next.
- **`S1-04`** (report template) — §2.5's worked paragraph is the cleanest criterion-4 example yet:
  finding, method, stated limitation, and the named next artifact, in four sentences.
- **`S5-08`** (Volume Shadow Copies) — ⚠️ §2.4's note that shadow-copy deletion appears in `$UsnJrnl`
  as ordinary `FILE_DELETE` records, which **correlates with but does not prove** `vssadmin` (**N3**).

### Back-propagation

🟢 **None required, one item logged.** 🔴 **`T1484.001`'s parent has been renamed** to *"Domain or
Tenant Policy Modification"* — ✅ **repo grepped: `T1484` appears nowhere**, so this is
forward-looking only. ✅ `T1486`, `T1105`, `T1489` appear nowhere yet; `T1490` only in
`crmsnatch.md`, already correct.

⚠️ **And a reinforcement rather than a correction:** MITRE's own pages now disagree about the current
version's date — the updates row reads *"ATT&CK v19 | August 6, 2026 … v19.2 on MITRE/CTI"* while
`index.json` lists to v19.1 (12 May 2026). **Block L7's rule — cite the version, never the date — is
now doubly justified.** ✅ No note prints a bare date in student-facing form.

### Minutes

**Net zero in rows, and for once the additions land outside S5.** `S4-07`, `S4-08`, `S2-04`,
`S2-05`, `S6-09` and `S1-04` all gain content; **`S5-08` gains a one-line caveat.**

🟢 **That is a change worth noting after four rooms of S5 accumulation** — but ⚠️ **`S4-07` is a
20-minute row and has now taken material from rooms 21, 26 and 27**, so **the row-overload list grows
rather than moves**: **`S5-06`, `S5-08`, `S6-06`, `S4-07`.** 🔴 **Four rows, five consecutive rooms,
no row count change. The re-split must size rows, not count them** — stated for the fourth time.

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-second room carrying the S5 overdraft.**

### Out of scope

Ransomware reverse engineering, decryption, negotiation, and Active Directory recovery. ⚠️ **Two
items sit on the line and should be in:**

- **The attribution phrasing rule** (§2.7) — *"consistent with an X-family payload", never
  "attributed to group X"* — is **one sentence in `S1-04`** and it is exactly criterion 4.
- **"Name the artifact you would need next"** (§2.5) — one line in the report template, and it turns
  a dead end into a deliverable.

### Still unresolved

- **S5 re-split** — twenty-second room; **four-row overload list** (`S5-06`, `S5-08`, `S6-06`,
  `S4-07`).
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- **No Windows intrusion image in the Priority-2 set** — **six for six.** `EVS-10` unallocated.
- **🆕 FTK Imager in `CLEAN-TOOLS` (D17)** — required if any logical image is ever handed out (§4).
- **D19 has no per-session host map** — still gating **F7**.
- **Volatility symbol pre-population on `CLEAN-TOOLS`** (**D2**) — still not done.
- **`ecdfp-case` skill** not installed; **no room note through `ecdfp-intake`.**

## 9. Links

**Room** — <https://tryhackme.com/room/shockandsilence>
**Module** — Honeynet Collapse, stage 5 of 6. Previous: <https://tryhackme.com/room/crmsnatch>.
Next: <https://tryhackme.com/room/thelasttrial>.
**Companion notes** — `crmsnatch.md` (stage 4) · `initialaccesspot.md` (the module map) ·
`ntfs-analysis.md` and `forensic-imaging.md` (the `$MFT`/imaging base this room extends) ·
`autopsy.md` (**E4**, the supported-format list this room falls outside) ·
`honeynet-collapse-module.md` (the arc, after stage 6) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **C1–C8**, **E4**, **L1**, **L2**, **N3**, and new block **O**.

**Citations from §3, by finding:**

- #1 AD1 — Cerbero <https://blog.cerbero.io/ad1-format-package/> ·
  PRONOM fmt/842 <https://www.nationalarchives.gov.uk/pronom/fmt/842> ·
  FTK Imager user guide
  <https://arts.unimelb.edu.au/__data/assets/pdf_file/0011/2970587/Imager-3_1_4_UG.pdf> ·
  Autopsy issue #1402 <https://github.com/sleuthkit/autopsy/issues/1402> ·
  Arsenal Image Mounter FAQ <https://arsenalrecon.com/products/arsenal-image-mounter/faqs> ·
  Forensic7z <https://www.tc4shell.com/en/7zip/forensic7z/> ·
  AD1-tools <https://github.com/al3ks1s/AD1-tools> ·
  Exterro FTK Imager <https://www.exterro.com/digital-forensics-software/ftk-imager>
- #2 Zone.Identifier — MS-FSCC
  <https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/6e3f7352-d11c-4d76-8c39-2516a9df36e8> ·
  MS zone values
  <https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms537183(v=vs.85)> ·
  xkln <https://xkln.net/blog/identifying-the-source-of-downloaded-files/> ·
  dfir.co.za <https://www.dfir.co.za/2018/06/18/highway-to-the-danger-zone-identifier/> ·
  SANS ISC <https://isc.sans.edu/diary/31732> ·
  ZDI-25-045 <https://www.zerodayinitiative.com/advisories/ZDI-25-045/>
- #3, #4 `$UsnJrnl` — MS `USN_RECORD_V2`
  <https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2> ·
  MS change journal records
  <https://learn.microsoft.com/en-us/windows/win32/fileio/change-journal-records> ·
  Mjolnir Security <https://intel.mjolnirsecurity.com/artifact-usnjrnl>
- #5 attribution — SentinelOne
  <https://www.sentinelone.com/labs/hypervisor-ransomware-multiple-threat-actor-groups-hop-on-leaked-babuk-code-to-build-esxi-lockers/> ·
  Sophos <https://www.sophos.com/en-us/blog/lockbit-in-action>
- #6 ATT&CK — T1486 <https://attack.mitre.org/techniques/T1486/> ·
  T1105 <https://attack.mitre.org/techniques/T1105/> ·
  T1489 <https://attack.mitre.org/techniques/T1489/> ·
  T1484.001 <https://attack.mitre.org/techniques/T1484/001/>
