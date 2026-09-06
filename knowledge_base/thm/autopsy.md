---
room: Autopsy
url: https://tryhackme.com/room/btautopsye0
module: Disk Image Analysis
feeds: **S2** (`S2-08` Autopsy walkthrough) and **S4** (tool reps across FAT32/NTFS/carving).
       Also **S6-06** (timeline) and **S3** (MIME vs extension).
       🟢🟢 **AND IT SOLVES OUR TIER 2 EVIDENCE PROBLEM — see §4. Read that section first.**
difficulty / time: Easy · 60 min · 9 tasks · Premium · **46,319 completions · 1,003 recommends**
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 9 tasks read in full. 0 sections NOT READ.
              🔴 Room ships plaintext RDP credentials in Task 1 — **deliberately not reproduced
              here (R8)**.
---

## 1. What the room teaches

Autopsy as a GUI: the five-step case workflow, the data-source types, what ingest modules are, the
five panes of the interface, the Data Sources Summary, report generation, and the Timeline. Then a
seven-question mini-investigation against a prepared case.

At **46,319 completions and 1,003 recommends** it is the most-taken room we have extracted by a
factor of two and a half. It is competently written, it is the only GUI-tool room in the path, and
it is **seven years out of date** — its own documentation links point at Autopsy **4.12.0**,
generated **18 September 2019**, against a current **4.23.1**.

**🟢🟢 But the single most valuable thing in this room is one sentence in Task 9:**

> *"The disk image used with this room's development was created and released by the NIST under the
> Computer Forensic Reference Data Sets CFReDS Project."*

That is the **NIST CFReDS "Data Leakage Case"** — a full corporate-data-theft scenario with a PC
image, three removable-media images, published SHA-1 hashes, and a **46-question answer key** — and
it is a **US Government work in the public domain under 17 U.S.C. §105.** **We can link it, our
students can download it, and we could legally rehost it.** See §4. This resolves the largest open
item in our evidence plan and it arrived as a footnote in an introductory room.

**The room's structural weakness** is that it describes two of Autopsy's three important
capabilities and then explicitly declines to use either: *"we will not cover ingest modules in this
room"*, and *"the actual disk image is not in the attached VM."* Students learn to navigate a case
someone else built, over an image that is not there. **That is a fine 60-minute introduction and it
is not `S2-08`.** With CFReDS in hand, ours can be the real thing.

## 2. Artifacts — one 6-box block each

### 2.1 The case file (`.aut`) and its case folder

- **What it is** — Autopsy's container for an investigation: the `.aut` project file plus a case
  folder holding the SQLite/PostgreSQL database, the Solr keyword index, logs, exported files and
  reports.
- **Where it lives** — under the **Base Directory** chosen at case creation. The room teaches the
  three creation fields — **Case Name**, **Base Directory**, **Case Type (Single-User vs
  Multi-User)** — and that is the right frame.
- **What it proves** — 🟢 **the case, not the evidence.** All ingest results, artifacts, tags,
  comments, timestamps and the keyword index live here; the disk image does not. That distinction
  is what makes §2.2 possible and it is the most useful thing in the room's first half.
- **What it does NOT prove** — 🔴 **nothing about the evidence's integrity.** The `.aut` is a
  working file, not an evidence container — it is written to constantly, it has no internal hash of
  the source, and it is not what you archive. ⚠️ **Case Type is a one-way decision at creation**:
  Single-User (SQLite) and Multi-User (PostgreSQL + Solr + ActiveMQ) are not interchangeable
  afterwards.
- **How to parse it** — File → Open Case, point at the `.aut`. ⚠️ **The "Optional Information"
  screen the room says can be *"left blank for our purposes"* is the case metadata** — examiner
  name, case number, organisation. **In our material it is never optional**; it is the top of the
  chain-of-custody record and it is what appears in the generated report.
- **Anti-forensics / false-positive caveat** — ⚠️ **the case folder is not the evidence and the
  evidence is not the case folder.** Archive the image and its hashes separately; a `.aut` alone is
  reproducible only if the image is still findable at the recorded path.

### 2.2 A case whose image is missing

- **What it is** — the situation the room's whole lab runs in: *"the actual disk image is not in the
  attached VM, certain Autopsy sections will not display any actual data, only the metadata for
  that row within the local database."*
- **Where it lives** — Autopsy detects the absence and raises a relocate-or-continue dialog; the
  room tells students to click **No** and carry on.
- **What it proves** — 🟢 **exactly where the boundary between metadata and content lies**, which is
  a genuinely good lesson the room never names. **Still works without the image:** the full
  filesystem metadata tree (names, paths, MFT timestamps, sizes, allocated/deleted flags), every
  previously generated ingest artifact (web history, registry artifacts, EXIF, accounts, interesting
  files), tags and comments, **the Timeline** (built from database timestamps), MD5s **already
  computed and stored**, and **keyword search** — because the Solr index lives in the case folder,
  not in the image.
- **What it does NOT prove** — 🔴 **anything requiring a byte read.** No file preview, no hex view,
  **no extraction**, no new hashing, no new ingest run, no carving of unallocated space, no new
  keyword indexing. **A student cannot verify a single one of their own findings against the
  evidence.** Autopsy's own Portable Case documentation makes the boundary explicit: in a portable
  case *"although the original images … appear in the tree, their contents are not included"*, which
  is why *"a copy of any tagged file is made into the case folder."*
- **How to parse it** — for teaching navigation and artifact interpretation, a case-only
  distribution is viable and cheap. **For extraction, hashing or verification exercises it is
  useless.** ⚠️ Note this is *not* documented feature-by-feature by Autopsy; the split above is
  read off the database/Portable-Case design and should be stated as such.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **the deeper problem is epistemic.** A student
  working a case they did not build, over an image they cannot read, is **taking every artifact on
  trust** — which is precisely the habit D7 exists to break. **Ours ships the image.**

### 2.3 Data sources and image formats

- **What it is** — what Autopsy will ingest.
- **Where it lives** — Add Data Source. **Current (4.23.0) full list**: *Disk Image or VM File* ·
  *Local Disk* · *Logical Files* · *Unallocated Space Image Files* · *Autopsy Logical Imager
  Results* · *XRY Text Export*.
- **What it proves** — 🟢 the room's most useful practical detail: **with a multi-segment image
  (E01/E02/E03…) you point at the first file only and Autopsy handles the rest.** Students
  reliably get this wrong.
- **What it does NOT prove** — 🔴 **the room's format list is incomplete and one row is wrong.**
  Current supported disk-image formats: Raw Single (`.img .dd .raw .bin`) · Raw Split
  (`.001 .aa`) · EnCase (`.e01`) · **VMDK** · **VHD and VHDX**. **VHDX is missing from the room.**
  **VDI and AFF4 are not supported** — do not promise them. ⚠️ **L01 has only "limited support"**
  and arrives through *Logical Files*, not as a disk image. 🔴 And the room's fourth row,
  **"Lab Machines (For example: `*.vmdk`, `*.vhd`)"**, is a mis-transcription — those are disk-image
  formats *inside* "Disk Image or VM File", not a data-source type. "Lab Machines" is TryHackMe's
  own UI vocabulary leaking into a technical list.
- **How to parse it** — for our lab: **E01 for the primary evidence** (metadata, compression,
  integrated verification), raw for the tooling exercises. **The mobile import path is `XRY Text
  Export`** — there is no Cellebrite data-source type in current Autopsy.
- **Anti-forensics / false-positive caveat** — ⚠️ **`Unallocated Space Image Files` is a separate
  data-source type for a reason**: a blob with no filesystem is ingested differently from a disk.
  Students who add a carved chunk as a "Disk Image" get nothing and assume the tool failed.

### 2.4 Ingest modules

- **What it is** — Autopsy's plug-ins; each extracts one class of artifact. Configurable at
  add-data-source time, or later via right-click → **Run Ingest Modules**.
- **Where it lives** — results populate the **Results** node in the Tree Viewer; alerts appear in
  the **Ingest Inbox**; progress in the Status Area.
- **What it proves** — 🟢 the room's honest operational warnings are worth keeping: **ingest is
  resource-intensive** (*"expect significant performance issues"*), it runs by default on
  **All Files, Directories, and Unallocated Space**, and **the results depend on the dataset** —
  *"If you choose a module to retrieve specific data that is unavailable in the drive, there will be
  no results."*
- **What it does NOT prove** — 🔴🔴 **that the module ran at all.** **Three modules are DISABLED by
  default in current Autopsy**, verified in source: **Keyword Search**, **Plaso**, and
  **Malware Scan**. **A student who expects keyword hits and never enables the module gets silence
  and concludes there is nothing there.** The room, written against 4.12, never mentions this — and
  it teaches Keyword Search as a headline feature two tasks later. **This is the single most
  important currency correction in the room.**
- **How to parse it** — enable deliberately, module by module, and **record which modules ran with
  what settings** — it is part of the method section of any report. ⚠️ **The room says the Keyword
  Search module *"does not have per-run settings"*. That is now false**: 4.23 gives it built-in
  expression toggles (Phone Numbers, IP Addresses, Email Addresses, URLs), an "Add text to Solr
  Index" checkbox and OCR options.
- **Anti-forensics / false-positive caveat** — 🔴 **the room describes ingest and then refuses to
  run it** (*"we will not cover ingest modules in this room"*). **Ingest configuration is the single
  most consequential decision an Autopsy examiner makes** — it determines what exists to be found —
  and it is the one thing the most-taken Autopsy room on the internet does not practise. **`S2-08`
  must.**

### 2.5 File Types: By Extension vs By MIME Type

- **What it is** — two independent classifications of the same files, side by side under **Views →
  File Types**.
- **Where it lives** — Tree Viewer → Views → File Types → *By Extension* / *By MIME Type* (also
  *By Deleted Files* and *By File Size*).
- **What it proves** — 🟢🟢 **the room's best single teaching line, quoted as written:**
  *"An adversary can rename a file with a misleading file extension, so the file will be
  'miscategorized' By Extension but will be categorized appropriately By MIME Type."*
  **The disagreement between the two views is the finding**, and it is one click away.
- **What it does NOT prove** — 🔴 **MIME detection is signature-based and therefore also
  spoofable.** A file with a forged magic number is classified by the forgery. It also does not
  prove intent: **extension/type mismatches occur constantly and innocently** — files with no
  extension, `.dat` blobs, container formats, and every OOXML document (which is a ZIP). **A
  mismatch is a lead, not a finding.** ⚠️ And Autopsy has a dedicated **File Extension Mismatch
  Detector** module for this — the room mentions its *global settings* in Task 9 and never connects
  it to the tip.
- **How to parse it** — expand both trees and compare; or run the mismatch module and read the
  Results node. **Corroborate with the file's own header in the hex view before calling it.**
- **Anti-forensics / false-positive caveat** — 🟢 **this is our `S3` and `S4` bridge**: it is the
  same signature-versus-metadata argument as file carving (room 8) and the same
  claim-versus-record structure as PEB-vs-kernel in memory (room 13). **One principle, three
  sessions.** Worth naming explicitly.

### 2.6 The S / C / O columns

- **What it is** — three narrow columns in the Result Viewer that most students never decode.
- **Where it lives** — the Result Viewer table header.
- **What it proves** — per current Autopsy documentation:
  **(S)core** *"indicates whether the item is interesting or notable"* — a red exclamation for
  notable, a yellow triangle for suspicious, set by an ingest module **or by the analyst**.
  **(C)omment** *"indicates whether the item has a comment in the Central Repository or has a
  comment associated with a tag."*
  **(O)ther occurrences** *"indicates how many data sources in the Central Repository contain this
  item."*
- **What it does NOT prove** — 🔴 **"notable" is a label somebody applied, not a fact about the
  file.** A red exclamation means a hash set or a rule matched, or an analyst clicked. Reporting a
  Score as a finding is reporting the tool's opinion. ⚠️ **The O column is empty unless the Central
  Repository is enabled and populated** — it is opt-in (SQLite single-user or PostgreSQL
  multi-user), and it can also be switched off entirely in View Options for performance. **A zero
  is not "never seen before"; it is usually "no repository".**
- **How to parse it** — hover for the reason; check *which* module set the Score before quoting it.
- **Anti-forensics / false-positive caveat** — 🟢 **the Occurrence column is the best small
  illustration in the room of a general rule**: *an empty column can mean "no data" or "no
  configuration", and the two are indistinguishable from the screen.* **Use it.**

### 2.7 The Data Sources Summary and the generated report

- **What it is** — an at-a-glance overview across nine categories, and an exportable report.
- **Where it lives** — the Summary tab per data source; **Generate Report** for the export.
- **What it proves** — 🟢 the room's advice is good: *"It is suggested that you view the summary of
  the data sources before starting an investigation. This will give you a general idea about the
  system and artifacts."* **Orient before you dig.** 🟢 And its low-resource tip is genuinely
  practical: *"You can use the tool to parse the data and generate the report, then continue to
  analyze through the generated report without a need for Autopsy."*
- **What it does NOT prove** — 🔴 **the summary is a count, not an analysis.** *"this is an overview
  of the total findings"* — the room says so, and students still treat the percentages as
  conclusions. ⚠️ **And the report is a dead end for investigation**: *"reports don't have
  additional search options, so you must manually find artifacts for the event of interest."*
- **How to parse it** — 🔴 the room only ever generates **HTML**. Current Autopsy ships **nine**
  report modules: HTML · **Excel (`.xlsx`)** · Save Tagged Hashes · Extract Unique Words ·
  **CASE-UCO (JSON)** · Files–Text (tab/comma delimited) · **Google Earth KML** ·
  **Portable Case** · **TSK Body File**. 🟢 **Two of those matter to us and neither is in the room:
  the TSK Body File feeds `mactime`/plaso for `S6` timelines, and CASE-UCO is the
  interchange format for handing findings to another tool.**
- **Anti-forensics / false-positive caveat** — ⚠️ **a report is a snapshot of a case state.** It
  carries no record of which ingest modules ran with which settings unless you put it there —
  which is why the **Optional Information** the room skips (§2.1) matters.

### 2.8 The Timeline

- **What it is** — every timestamped event in the case, plotted.
- **Where it lives** — a separate Timeline window; three panes — **Filters**, **Events**,
  **Files/Contents** — and three view modes: **Counts** (bar chart), **Details** (clustered,
  collapsible), **List** (table).
- **What it proves** — 🟢 **volume and shape before detail.** The room's own example is the lesson:
  *"for `/Windows`, there are 130,257 events between 2009-06-10 and 2010-03-18."* **Clustering,
  pinning and hiding are how you make that readable**, and the room teaches all three
  (expand/collapse, pin/unpin, hide/unhide into Hidden Descriptions).
- **What it does NOT prove** — 🔴🔴 **that the timestamps mean what they appear to mean.** A
  timeline built from filesystem metadata inherits **every** limitation of that metadata:
  timestomping, timezone interpretation, second-vs-100ns resolution, `$STANDARD_INFORMATION` vs
  `$FILE_NAME` (room 7), and clock skew on the source host. **The Timeline renders; it does not
  validate.** ⚠️ It also does not prove completeness — events only exist for artifacts that ingest
  produced, and three modules are off by default (§2.4).
- **How to parse it** — start in **Counts** to find the interesting period, switch to **Details** to
  cluster, then **List** to read. **Export a TSK Body File** (§2.7) when you need the same data in
  `mactime` or plaso.
- **Anti-forensics / false-positive caveat** — 🟢 **the volume itself is the pedagogic point**:
  130,257 events in one folder is why "look at the timeline" is not a method. **A timeline needs a
  question.** That belongs in `S6-06`.

## 3. Tools and commands

Autopsy is a GUI, so this is a navigation map rather than a command table.

| task | where | note |
|---|---|---|
| create case | New Case → Case Name / Base Directory / **Case Type** | Single-User vs Multi-User is **irreversible** |
| case metadata | "Optional Information" screen | 🔴 room says leave blank — **never optional for us** |
| open case | Open Case → `.aut` | missing-image dialog → "No" to continue metadata-only |
| add evidence | Add Data Source → **Disk Image or VM File** | point at the **first** segment of a multi-part E01 |
| configure ingest | at add time, or right-click source → **Run Ingest Modules** | 🔴 **3 modules off by default** — §2.4 |
| navigate | Tree Viewer → Data Sources / Views / Results / Tags / Reports | |
| spot renamed files | Views → File Types → **By Extension** vs **By MIME Type** | the disagreement is the finding |
| extract a file | Result Viewer → right-click → **Extract File(s)** | ⚠️ needs the image present |
| ad-hoc search | top right → **Keyword Search** / Keyword Lists | 🔴 requires the module to have been enabled |
| overview | data source → **Summary** tab (9 categories) | orient before digging |
| report | **Generate Report** → 9 modules | room uses HTML only |
| timeline | Tools → Timeline → Counts / Details / List | pin, hide, cluster |

### CURRENCY CHECK — verified 2026-08-28

| # | item | result |
|---|---|---|
| 1 | 🔴 **the room is pinned to Autopsy 4.12.0** | Every documentation link is `…/user-docs/**4.12.0**/…`, and that page is stamped **"Generated on Wed Sep 18 2019"**. Current is **4.23.1 (7 May 2026)**, docs at `…/user-docs/**4.23.0**/`. **Seven years.** |
| 2 | ✅ **Autopsy is actively maintained** | 4.23.0 released **15 Apr 2026**; 4.23.1 on 7 May 2026 is a packaging fix (*"released as a Develop build, instead of Release"*). Sleuth Kit **4.15.0** same day. Commits into May 2026 by Brian Carrier. Development is under **Sleuth Kit Labs** (formerly Basis Technology). **No funding or wind-down announcement.** ⚠️ **Several third-party sources — Wikipedia included — still list 4.22.1 / April 2025. Do not cite them.** |
| 3 | 🔴🔴 **three ingest modules are DISABLED by default** | Verified in `IngestJobSettings.java`: `DEFAULT_DISABLED_MODULES = { "Plaso", "Keyword Search", MalwareScan }`. **Everything else is on by default.** **A lab that expects keyword hits produces silence if nobody enables the module** — and this room teaches Keyword Search as a headline feature. **This is the correction that must reach `S2-08` first.** |
| 4 | 🔴 **"Keyword Search … does not have per-run settings" is now false** | 4.23 docs: *"The Ingest Settings for the Keyword Search module allow the user to enable or disable the specific built-in search expressions, Phone Numbers, IP Addresses, Email Addresses, and URLs."* Plus an "Add text to Solr Index" checkbox and OCR options. **The room's Interesting-Files-vs-Keyword-Search contrast no longer holds.** |
| 5 | 🔴 **the data-source list is incomplete and one row is wrong** | Current types: *Disk Image or VM File · Local Disk · Logical Files · Unallocated Space Image Files · Autopsy Logical Imager Results · XRY Text Export*. Formats: Raw Single · Raw Split · EnCase `.e01` · VMDK · **VHD and VHDX**. **VHDX missing from the room. VDI and AFF4 are NOT supported.** **L01 has only "limited support"**, via *Logical Files*. The room's **"Lab Machines (*.vmdk, *.vhd)"** row is a mis-transcription — those are formats, not a source type. |
| 6 | ⚠️ **mobile import is `XRY Text Export`** | There is **no Cellebrite data-source type** in current Autopsy documentation. Relevant if any mobile content lands in our scope. |
| 7 | ✅ **YARA Analyzer ships** | Documented at `…/4.23.0/yara_page.html`; needs user-supplied rules; can run on all files or executables only. **Room mentions it once in Task 9 and never uses it.** 🟢 This is the natural bridge from room 14's `vadyarascan` — **same rules, disk side.** |
| 8 | ✅ **Central Repository still drives the O column** | SQLite (single-user) or PostgreSQL (multi-user); **opt-in**, prompted at startup since 4.15. Without it the O column is empty — **and an empty O is indistinguishable from "never seen before."** |
| 9 | 🔴 **nine report modules, not one** | HTML · **Excel** · Save Tagged Hashes · Extract Unique Words · **CASE-UCO (JSON)** · Files–Text · **Google Earth KML** · **Portable Case** · **TSK Body File**. 🟢 **Body File → `mactime`/plaso for `S6-06`; CASE-UCO for tool interchange.** Neither is in the room. |
| 10 | ⚠️ **Autopsy is Apache 2.0** | *"The Autopsy code is released under the Apache License, Version 2."* **Screenshots and redistribution in courseware are fine**, preserving licence and notices. ⚠️ **But the website and the Autopsy/Sleuth Kit Labs branding are "© 2026 Sleuth Kit Labs" and are NOT covered by that grant** — our slides use our own screenshots of our own cases, never lifted marketing assets. |
| 11 | 🔴 **NSRL RDS has changed format — this breaks old hash-set instructions** | Current **RDS 2026.06.1, published 1 June 2026**. NIST: *"The NSRL has completed the transition away from the RDS 2.XX text file format, and will only be publishing the RDSv3 SQLite database format moving forward."* Distributions: Modern PC · Legacy PC · Android · iOS, each full/delta and standard/minimal, **SQLite in ZIP**. **The `NSRLFile.txt` import path is gone.** ⚠️ **Verify our Autopsy hash-set import steps against RDSv3 SQLite before `S2-08` ships.** |
| 12 | ✅ **Sleuth Kit 4.15.0** (15 Apr 2026) | Consistent with `_TOOL_CURRENCY_2026-08-28.md` block A, which also noted the **download page still advertises 4.14.0** — the news feed is the reliable source. |
| 13 | ⚠️ **Autopsy 4.23 added an MCP server and a Cyber Triage integration** | Noted for awareness only; **out of scope for eCDFP** and not to be taught. |
| 14 | ⚠️ Keyword Search default (cross-check) | Block A recorded *"Keyword Search now OFF by default"* from the 4.23 notes; **confirmed here from source**, together with **Plaso** and **Malware Scan**, which block A did not have. **Update block A.** |

## 4. Evidence used — 🟢🟢 THE FINDING THAT MATTERS

The room's Task 9 names its own source:

> *"The disk image used with this room's development was created and released by the NIST under the
> Computer Forensic Reference Data Sets CFReDS Project."*

**It is the NIST CFReDS "Data Leakage Case"**, and the match is positive on four independent points:
the Sticky Note author **"Informant"** (the scenario's suspect is *"Iaman Informant"*), the **2015**
web-search dates (the answer key's timeline runs **22–25 March 2015**), the **SECRET seed files**
accessed from a network drive, and the **USB + CD removable media**.

### What it is

> *"'Iaman Informant' was working as a manager of the technology development division at a famous
> international company OOO that developed state-of-the-art technologies and gadgets."*
> *"At the security checkpoint, although his devices (a USB memory stick and a CD) were briefly
> checked (protected with portable write blockers), there was no evidence of any leakage."*

A complete corporate data-theft scenario with **four separate acquisitions**, one of them a UDF
optical disc — which is a filesystem we would otherwise have no evidence for at all.

| target | formats offered | size |
|---|---|---|
| **PC** (the room's image) | DD (7-Zip split, `pc.7z.001`–`.003`) **and** EnCase (`pc.E01`–`.E04`) | 5.05 GB / 7.28 GB |
| **RM#1** USB, **exFAT** | EnCase | 74.5 MB |
| **RM#2** USB, **FAT32** | DD and EnCase | 219 / 243 MB |
| **RM#3** CD-R, **UDF** | RAW+CUE, DD, EnCase | 78.6–92.8 MB |
| **seed files** | 7z | 150 MB |

**Published SHA-1 hashes for all 14 downloadable files**, and a **46-question answer key** (v1.32,
23 Jul 2018) containing the scenario, target-system specifications, a day-by-day suspect timeline,
the acquisition hashes, "practice points", and questions with answers across email, web history,
file operations, deleted-data recovery and **anti-forensics**.

### 🟢🟢 The licence — this is why it matters

> *"This data/work was created by employees of the National Institute of Standards and Technology
> (NIST), an agency of the Federal Government. Pursuant to title 17 United States Code Section 105,
> works of NIST employees are not subject to copyright protection in the United States."*

NIST's own terms allow the data to be *"modified and redistributed freely"*, provided we
*"explicitly acknowledge the National Institute of Standards and Technology as the source"* and,
if modified, *"carry a notice stating that you changed the data."* Supplied **AS IS**, no warranty.

**Verdict, for `ecdfp-evidence` and D22:**

- ✅ **Linking is unambiguously fine.** No registration, no click-through licence, no terms gate.
- ✅ **Commercial training use is unrestricted.**
- ✅ **Redistribution/rehosting is legally permitted** — with attribution — which no other corpus in
  our plan allows. **We still link rather than rehost (D22), but now by choice, not necessity.**
- ⚠️ Two caveats to note once: NIST warns the work *"may be subject to foreign copyright"* (relevant
  for delivery outside the US); and the **seed files** specifically were *"created based on MS
  Office files randomly selected from Govdocs1"*, so rehosting `seed-files.7z` would pull Digital
  Corpora's terms in too. **Linking sidesteps both.**

### What this changes in our evidence plan

**Tier 2 was our weakest tier.** It now has a scenario-grade anchor with an answer key, four
filesystems, and a licence that permits anything we might want.

| our need | what CFReDS supplies |
|---|---|
| `S2` a real image to acquire, verify and open | **PC image in both E01 and raw**, with published hashes |
| `S4` **FAT32** | RM#2 |
| `S4` **exFAT** | RM#1 — **we had no exFAT evidence at all** |
| `S4` **UDF / optical** | RM#3 — **likewise nothing** |
| `S4`/`S5` NTFS on a real system | the PC image |
| `S5` registry, user activity, USB history | the PC image + the removable media, **the same story across both** |
| assessment | **46 questions with published answers** — a calibration baseline for our own |
| anti-forensics | the answer key has a section on it |

🔴 **But the answer key is instructor-only.** It is a public PDF at a guessable URL; our questions
must not be its questions, and the file must never appear in a student handout.

⚠️ **Operational notes.** Downloads live on **`cfreds-archive.nist.gov`** even though the current
portal is **`cfreds.nist.gov`** — the portal records link back to the archive host, so **do not
treat the archive domain as disposable**. Budget bandwidth: **5–7 GB** for the PC image. The raw
variants are **7-Zip split archives** (`.7z.001`), *not* raw-split segments — students must
extract before adding to Autopsy, and will otherwise try to feed `.7z.001` to Autopsy as
"Raw Split" and fail.

### Other CFReDS material worth a row in `practice_platforms.md`

**Scenario + answer key** (the useful kind): **Data Leakage Case** (46 Q&A) · **Hacking Case**
(Dell CPi laptop, "Mr. Evil" wardriving, 31 Q&A) · **Rhino Hunt** (DFRWS 2005).
**Technique test images** (no narrative): Registry Forensics · Deleted File Recovery ·
**File Carving** · Container Files · Memory Images · Mobile (chip-off/JTAG) · Drone Images ·
Basic Mac Image · Unicode string search.

⚠️ **Currency caveat**: NIST's own CFReDS scenarios appear unchanged since **~2019–2020** (portal
metadata shows NIST entries at 2019-08-26). The portal is still being added to — third-party sets
including **Cellebrite CTF 2024** are present — but treat the NIST scenarios as stable, not fresh.
Newest-dataset date **NOT VERIFIED**.

🟢 **The Hacking Case is a second candidate for `S4`/`S5`**, and its 31-question key gives us a
second calibration set.

## 5. Lab design worth reusing

1. **🟢🟢 The five-step workflow, stated first.** *Create/open case → select data source → configure
   ingest → review artifacts → create report.* Five lines, correct, and it gives students a mental
   model before a single click. **Open `S2-08` with it verbatim.**
2. **🟢🟢 By Extension vs By MIME Type** (§2.5). One click, one principle, and it links `S3`, `S4`
   and `S5`. **Keep the room's wording.**
3. **🟢 Summary before investigation.** *"view the summary of the data sources before starting an
   investigation"* — orientation as an explicit step, not an accident.
4. **🟢 The report-as-workaround tip.** Parse with Autopsy, then read the report on a machine that
   cannot run Autopsy. **Directly useful for our students' modest lab VMs**, and it doubles as the
   answer to "what do I take to a meeting".
5. **🟢 Honest resource warnings.** *"Running ingest is resource-intensive… expect significant
   performance issues"*; *"Browsing long results might end up with a system freeze."* **Say the
   same** — students blame themselves for a slow tool.
6. **🟢 The S/C/O decode** (§2.6). Three columns nobody explains, explained.
7. **⚠️ Timeline: teach clustering before content.** The room's `/Windows` cluster of **130,257
   events** is the argument for filters, and it makes itself.
8. **🔴 Do NOT reuse: "Optional Information … can be left blank for our purposes."** It is the case
   metadata and it is the top of the custody record. **Our version fills it in and shows it
   appearing in the generated report.**

### ✅ No safety defect — but two handling gaps

Nothing in this room endangers the analyst or the evidence: it is read-only navigation of a
prepared case. Two omissions still matter for us:

- 🔴 **The room prints plaintext RDP credentials in Task 1.** Not reproduced here (**R8**). **Our
  material never ships credentials in a slide or handout** — they live in the private lab sheet.
- ⚠️ **Autopsy writes to its case folder constantly and can extract files to disk.** Ingest,
  extraction and report generation all produce artifacts on the examiner's machine. **`S2-08` must
  say where the case folder lives, that it is not evidence, and that extracted files from a hostile
  image are hostile files** — the containment lesson from rooms 12 and 13 applies to a GUI exactly
  as it does to a shell.

**Defect tally unchanged at six** (rooms 6, 8, 9, 12, 13, 15 — see `forensic-imaging.md` §5).

## 6. Question patterns

**17 questions across 9 tasks** — the most of any room extracted — and they split cleanly by task.

**⚠️ Tasks 2–4: five questions, three of which are "read the task" or "click".** One real recall
item (*"What is the file extension of the Autopsy files?"* → `.aut`) and one that is arguably a
trick: *"What is the disk image name of the 'e01' format?"* asks the student to read a filename off
a screenshot.

**🟢 Tasks 5–6: six navigation questions, and they are well built** — *"Expand the 'Data Sources'
option; what is the number of available sources?"* · *"What is the number of the detected 'Removed'
files?"* · *"What is the filename found under the 'Interesting Files' section?"* ·
*"What is the full name of the operating system version?"* · *"What percentage of the drive are
documents?"* · *"Generate an HTML report… what is the job number of the 'Interesting Files
Identifier' module?"* **Each forces the student into a specific pane they would otherwise never
open**, and the last one requires actually generating a report. That is the right use of a GUI
room.

**🟢🟢 Task 7 is the room at its best.** Seven questions against a scenario, and **each names a
different artifact class**: installed programs (version `6.2.0.2962`) · a **password hint** · a
**network-drive IP** for the SECRET files · the **most-frequent web search term** · a **specific
search at 3/25/2015 21:46:44** · an **MD5 of an interesting binary** · **a Sticky Note**. One
question, one artifact, one defensible answer — **which is our case rule exactly.** The Sticky Note
question in particular is a lovely find: it is `StickyNotes.snt` / the modern `plum.sqlite`, an
artifact most students have never heard of, and its answer is a human sentence rather than a hash.

**🟢 Task 8's two timeline questions are correctly scoped** — a count on a specific date, and
"the majority of file events occurred on what date" — both requiring the Counts view and a filter.

### 🔴 Sixteenth room, no question whose answer is "cannot be determined"

And this room's structure makes the candidates unusually sharp, because **the image is missing**:

| the room could have asked | correct answer |
|---|---|
| *"The MD5 of the interesting binary is X. Verify it."* | **Cannot be done** — the image is absent; the stored hash is a value copied from a prior run, not something you can recompute. |
| *"The Occurrence column is empty. Has this file been seen in other cases?"* | **Cannot be determined** — an empty O means "no Central Repository" far more often than "never seen". |
| *"Keyword Search returned nothing. Does the term appear on the disk?"* | **Cannot be determined** — the module is off by default and the index may never have been built. |
| *"A file is `.jpg` By Extension and `application/zip` By MIME. Was it deliberately renamed?"* | **A lead, not a finding** — mismatches occur innocently in bulk. |
| *"The Score column shows a red exclamation. Is the file malicious?"* | **No** — it means a module or an analyst applied a label. |

**Five, all arising from the room's own screen, none asked.** 🟢 **Our `S2-08` asks the first
three, because they are the three that stop a student trusting a GUI.**

### 🔴 The deeper assessment problem

**Every Task 7 answer is a value the student reads out of a database somebody else populated, over
an image they cannot open.** There is no step at which a finding can be checked against the
evidence. That is acceptable for a free-tier introduction; it is **not** acceptable for a
certification course, and it is exactly what **§4 lets us fix** — our students run their own ingest
over the real CFReDS image and can verify every answer they give.

## 7. Figures we would need to draw

The room is almost entirely annotated screenshots of Autopsy — **all of them at version 4.12, all
of them theirs, none reusable (D22)**. We must reshoot every one against **4.23.1** with our own
case. That is a production task, not a design task, and it should be scheduled: **`S2-08` needs
roughly a dozen screenshots and they cannot be borrowed.**

| # | what is needed | our spec (one line) | priority |
|---|---|---|---|
| 1 | **the five-step workflow** | five boxes left to right — case → data source → **ingest configuration** → review → report — with the ingest box accented and captioned *"the only step that decides what exists to be found"* | **highest** |
| 2 | **what survives without the image** | the case folder and the image drawn as two objects, with a table between them: **in the case** (metadata tree · ingest artifacts · tags · keyword index · timeline · stored hashes) vs **only in the image** (file content · extraction · new hashing · carving · new ingest); caption *"a case is a set of claims about an image"* | **highest** |
| 3 | **By Extension vs By MIME Type** | one file shown twice — filed under `.jpg` in one tree and `application/zip` in the other — with a third panel showing the actual header bytes; caption *"two views, one file, and the disagreement is the lead"* | **high** |
| 4 | **default-off modules** | the ingest configuration panel redrawn with **Keyword Search, Plaso and Malware Scan** struck out and labelled *"OFF by default in 4.23"*, and the consequence spelled out: *"a search that returns nothing"* | **high** |
| 5 | **the CFReDS evidence set** | the four acquisitions as one exhibit board — PC (NTFS) · RM#1 (exFAT) · RM#2 (FAT32) · RM#3 (UDF) — each tagged with the session it serves, over the caption *"one scenario, four filesystems, public domain"* | **high** — this is the slide that sells the lab |
| 6 | **S / C / O decoded** | the three column headers magnified, each with its icon states and, under O, **"empty = no Central Repository, not 'never seen'"** | medium |
| 7 | **the Autopsy panes** | the five-area layout labelled once, cleanly, from our own 4.23 screenshot | medium — needed, but it is a screenshot job |

## 8. Fit against our material

### ⚠️ Part 1's mapping is right but too narrow

Mapped to **S2 · S4**, "tool reps". True as far as it goes. **This room reaches further**, and
Part 1 should be amended to: `S2-08` (Autopsy walkthrough) · **`S2` evidence sourcing (§4)** ·
`S3` (MIME vs extension) · `S4` (filesystem reps across four filesystems) · `S6-06` (timeline and
body-file export).

### Rows this strengthens

- **`S2-08`** — the room supplies the structure (workflow, panes, summary, report) and **we supply
  everything that makes it real**: current version, the three default-off modules, a real image,
  and ingest actually run.
- **`S2` / `ecdfp-evidence`** — 🟢🟢 **§4 is the row that matters.** CFReDS gives us a
  scenario-grade Tier 2 anchor with **NTFS, FAT32, exFAT and UDF**, published hashes, and a
  permissive licence. **exFAT and UDF we did not have at all.**
- **`S4`** — four filesystems from one story, so the same suspect's actions can be traced across
  media. That is a better teaching frame than four unrelated images.
- **`S6-06`** — the **TSK Body File** report module feeds `mactime`/plaso directly, connecting
  Autopsy to the timeline material from `_TOOL_CURRENCY` block C.
- **`S3`** — the extension/MIME split is the same signature-versus-metadata argument as carving.
- **Assessment calibration** — 46 published questions with answers for Data Leakage, plus 31 for
  the Hacking Case. **Instructor-only.**

### Five things `S2-08` must do differently from the room

1. **Ship the image.** CFReDS Data Leakage PC, E01, linked from NIST (§4).
2. **Run ingest**, and **enable Keyword Search, and say why it was off.**
3. **Fill in the case metadata**, and show it appearing in the generated report.
4. **Generate more than HTML** — the **Body File** at minimum, to hand to `S6-06`.
5. **Screenshot everything against 4.23.1**, from our own case. Nothing borrowed (**D22**).

### Minutes

`S2-08` already exists as a row. Everything above is **replacement content** for it — a better
image, a corrected module list, an ingest step that actually runs — plus **slides** (§7) and an
**evidence-sourcing decision** that costs no session time at all. The CFReDS download is homework
before the session, not classroom minutes.

**No new rows. S2 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Eleventh room carrying the S5 overdraft.**

### 🔴 Two decisions this room forces

1. **`ecdfp-evidence` must record the CFReDS route** — Tier 2, linked not rehosted (D22), with the
   licence note, the archive-host caveat, and the instructor-only flag on the answer key. **This is
   the largest single addition to the evidence plan and it should be written up before more rooms
   are extracted.**
2. **`_TOOL_CURRENCY_2026-08-28.md` block A needs updating**: it recorded *"Keyword Search now OFF
   by default"*; the source shows **Plaso and Malware Scan are off too**, and adds Autopsy
   **4.23.1 / 7 May 2026**, Sleuth Kit **4.15.0 / 15 Apr 2026**, and the **NSRL RDSv3 SQLite-only**
   change.

### Out of scope

Multi-User cases (PostgreSQL/Solr/ActiveMQ) — correctly out. Mobile via XRY — out. Autopsy's new
MCP server and Cyber Triage integration — out, and **not to be taught**. Third-party modules —
mentioned, not taught. **No scope conflict.**

### Still unresolved

**Browser forensics** — sixteenth room, still no `DECISIONS.md` row. ⚠️ **And this room makes it
urgent**: Task 7 asks two web-history questions (*"What web search term has the most entries?"*,
*"What was the web search conducted on 3/25/2015 21:46:44?"*), and the CFReDS image is full of
browser artifacts. **Autopsy extracts them by default. We will be teaching browser forensics
whether or not we decide to.** **Decide it.**

## 9. Links

- Room: <https://tryhackme.com/room/btautopsye0>
- **NIST CFReDS Data Leakage Case** — portal record
  <https://cfreds.nist.gov/all/NIST/DataLeakageCase> ·
  **downloads and scenario**
  <https://cfreds-archive.nist.gov/data_leakage_case/data-leakage-case.html> ·
  **SHA-1 hashes** <https://cfreds-archive.nist.gov/data_leakage_case/hash_values.html> ·
  🔴 **answer key (INSTRUCTOR ONLY)**
  <https://cfreds-archive.nist.gov/data_leakage_case/leakage-answers.pdf>
- **CFReDS Hacking Case** <https://cfreds-archive.nist.gov/Hacking_Case.html> ·
  answers <https://cfreds-archive.nist.gov/images/TestAnswers.pdf> (instructor only)
- CFReDS portal <https://cfreds.nist.gov/> · archive (**where the files actually live**)
  <https://cfreds-archive.nist.gov/> · NIST project page
  <https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/cfreds>
- **NIST licensing / §105 statement**
  <https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications>
- **NSRL current RDS (RDSv3 SQLite only)**
  <https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds>
- Autopsy: <https://www.autopsy.com/> · repo <https://github.com/sleuthkit/autopsy> ·
  **current user docs** <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/> ·
  data sources <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/ds_page.html> ·
  ingest <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/ingest_page.html> ·
  keyword search <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/keyword_search_page.html> ·
  YARA <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/yara_page.html> ·
  central repo <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/central_repo_page.html> ·
  reporting <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/reporting_page.html> ·
  timeline <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/timeline_page.html>
- ⚠️ The room's own links point at **4.12.0** (Sep 2019) — <https://sleuthkit.org/autopsy/docs/user-docs/4.12.0/>
- Sleuth Kit news (the reliable version source, not the download page)
  <https://www.sleuthkit.org/>
- Imaging/partition tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block A**
  — **needs the updates listed in §8.**
