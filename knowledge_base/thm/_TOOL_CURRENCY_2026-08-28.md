---
title: Tool currency check — S2 and S4 tool set
scope: Verification pass run ahead of extracting the S4 file-system rooms. Three parallel
       research agents, primary sources only. Covers imaging/partition, carving/hex, and
       NTFS/MFT/timeline tooling.
checked: 2026-08-28
owner: this file is working material for `ecdfp-intake` and the S2/S4 session builds.
       `ecdfp-evidence` owns nothing here. Re-run before any session that teaches these tools.
---

# Tool currency — S2 / S4 tool set, verified 2026-08-28

Every row below was checked against a **primary** source (vendor site, official repo, official
docs). Anything that could not be confirmed is in the **NOT VERIFIED** section of its block and
must not be printed in student material until it is.

---

## A. Imaging and partition tools

| tool | version | date | licence | flags verified | breaking change since ~2024 |
|---|---|---|---|---|---|
| Autopsy | **4.23.1** | 7 May 2026 (year inferred) | Apache 2.0 | n/a (GUI) | **Yes** — see A1 |
| The Sleuth Kit | **4.15.0** (GitHub) vs **4.14.0** (download page) | 15 Apr 2026 | IBM/Common Public Licence | **Yes, all 5** | No CLI breakage |
| Arsenal Image Mounter | **3.13.368** | 5 Aug 2026 | AGPLv3 source; Free Mode + Pro (~$907/yr) | n/a | **Yes** — .NET 10 |
| dc3dd | **7.3.1** | 25 Apr 2023 | GPLv2 | Yes (mirror, not vendor) | Upstream dormant 3+ yrs |
| `dd` (coreutils) | 9.11 | Apr 2026 | GPLv3+ | Yes | **Editorially** — see A5 |

### A1 — 🔴 Autopsy: Keyword Search no longer runs by default

Autopsy 4.23.0 release notes: the **Keyword Search module and email regexp search are disabled at
ingest by default** ("its slow"). The module still ships on Windows — it is *deselected*, not
removed. **Any lab step that says "run ingest, then check keyword hits" now yields zero hits**
unless the student ticks the box. PhotoRec Carver likewise ships but has always needed ticking.

**How to apply:** `S2` and `S4` lab steps must show the ingest-module checklist explicitly, with
the boxes to tick called out. This is a one-line lab fix that otherwise burns 20 minutes of class.

### A2 — Autopsy 4.23.1 bundles TSK 4.14.0, not 4.15.0

The Linux install instructions call for `sleuthkit-java_4.14.0-1_amd64.deb`. Do not teach
"Autopsy 4.23 = TSK 4.15".

### A3 — TSK version contradiction: report both

`sleuthkit.org/sleuthkit/download.php` still advertises **4.14.0 (Apr 2025)**; the GitHub releases
page and sleuthkit.org's own news line both show **4.15.0 (Apr 2026)**. **GitHub is authoritative**
— it hosts the artifacts and the vendor news corroborates it. The download page is stale.
This is the same failure mode as the RECmd README (room 4): **a project's own README/download page
can be older than its releases.** Worth teaching as a currency-check lesson in its own right.

### A4 — Arsenal Image Mounter now requires .NET 10

Since v3.12.344 (Mar 2026). A setup guide specifying .NET Framework or .NET 8 will fail.
Vendor baseline: Windows 10 1703+/11/Server 2016+ x64, **bare metal — not inside a hypervisor**.
🔴 **This matters for our lab (Part 6): FOR-WS01 is a VMware VM.** Confirm AIM works in the guest
before `S2` depends on it, or plan a fallback mounter.

### A5 — `dd` is no longer GNU's recommendation for damaged media

The coreutils manual now says: for failing storage devices, other tools ease saving data before
the device dies, **e.g. GNU ddrescue**. `conv=noerror,sync` still works and is still correct for
preserving offsets (`conv=sync` pads each input block with NULs to `ibs` size), but presenting it
as best practice for a *failing* drive contradicts the vendor manual.
**Teach:** `ddrescue` for damaged media · `dd`/`dc3dd` for healthy media.

### A6 — dc3dd is dormant, not dead

Last release 7.3.1 (Apr 2023), 3+ years stale, no deprecation notice, still packaged by Kali.
**But Debian bookworm ships 7.2.646**, so a lesson assuming 7.3.1 behaviour may not match on
Debian. Frame it as "still usable, no longer actively developed."
Confirmed options: `hash=`, `log=`, `hlog=`, `hof=`, `hofs=`, `ofs=`, `wipe=`.
**`verify=` and `progress=` do not exist — do not teach them.**

### A7 — TSK command syntax, all five confirmed intact

- `mmls [-t mmtype] [-o offset] [-i imgtype] [-b sector] [-BrvV] [-aAmM] image`
  `-t` accepts `dos`, `mac`, `bsd`, `sun`, **`gpt`**. **GPT needs no special flag** — omitting `-t`
  autodetects; `-t gpt` only forces it. `-r` recurses into *DOS* partitions specifically.
- `fsstat [-f fstype] [-i imgtype] [-o offset] [-b sector] [-tvV] image`
- `fls [-adDFlpruvV] [-m mnt] [-z zone] [-f fstype] [-s sec] [-i imgtype] [-o offset] image [inode]`
  **`-m` requires a mount-point string.** `fls -r -m / image.dd > body.txt` remains valid.
- `icat [-hrsvV] [-f fstype] [-i imgtype] [-o offset] [-b sector] image inode`
  ⚠️ **`-h` is NOT help** — it means "skip holes in sparse files". Pre-empt this in class.
- `blkls [-aAelsvV] ...` — was named `dls` before TSK 3.0.0 (2008). Only matters against old textbooks.

### A8 — Autopsy dropped 32-bit Windows (since 4.20.0)

Only `autopsy-4.23.1-64bit.msi` and the zip are offered.

### NOT VERIFIED — block A

- dc3dd flags confirmed only via a **man-page mirror**, not a vendor primary. Debian/Ubuntu
  renderings returned empty DESCRIPTION sections; SourceForge source browser blocked by robots.txt.
- Autopsy 4.23.1's **release year** — GitHub omits the year for current-year releases; sleuthkit.org
  news lists 4.23.0 only, and `updates.xml` still advertises 4.23.0.
- TSK 4.15.0's **release year**, same reason.
- coreutils 9.11 / Apr 2026 taken from man7.org, not gnu.org. ⚠️ the gnu.org HTML manual fetch
  returned a **garbled `conv=` list** (invented a `conv=pad`, gave `fdatasync`'s definition for
  `sync`) — man7's rendering is correct. Do not quote gnu.org's HTML for `conv=`.
- AIM 3.13.368's date format is ambiguous (`08-05-2026`); read as MM-DD-YYYY.

---

## B. Carving and hex tools

| tool | version | last release | licence / free? | flags verified | maintained? |
|---|---|---|---|---|---|
| foremost | **1.5.7** | not stated upstream | public domain | **Yes** — `-t -i -o -c`, `foremost.conf` | **Upstream dead**, distro-maintained |
| scalpel | 2.0 | **no release ever published** | Apache 2.0 | No | **ABANDONED — self-declared** |
| PhotoRec / TestDisk | **7.2** (7.3-WIP beta) | 22 Feb 2024 | **GPLv2+, free** | n/a | Active |
| bulk_extractor | **2.2.0** | 18 Aug 2024 | open source, free | **Yes** — `-o/--outdir` **REQUIRED**, `-e`, `-x`, `-E` | Active-ish |
| WinHex (X-Ways) | **21.8** | 25 May 2026 | commercial; **45-day eval exists** | n/a | Very active |
| HxD | **2.5.0.0** | **11 Feb 2021** | **still free**, incl. commercial use | disk + RAM editing present | Stale 5.5 yrs |

### B1 — 🔴 scalpel must be dropped or explicitly framed as legacy

The upstream repo's own description reads *"It is not being actively maintained"*, the README says
*"No official releases are being made"*, and **there is no published release at all**. Teaching
scalpel as current is indefensible. **Use foremost or PhotoRec for the live exercise**; mention
scalpel only as historical context.

### B2 — 🔴 foremost: send students to `apt`, not SourceForge

Upstream is dead (project "Last Update: 2013"), and worse, **the SourceForge files area serves only
1.5.5 (2008) while the homepage serves 1.5.7** — a student following the obvious download link gets
an *older* binary than the lesson assumes. **Debian ships 1.5.7-12, updated Jul 2026.**
Good news: all four taught flags are intact and unrenamed.

### B3 — 🔴 WinHex free mode is too crippled for several obvious lab tasks

Per the official manual, the evaluation build: 45-day limit · **will not save files larger than
200 KB** · **cannot write disk sectors** · cannot edit virtual memory · shows reminders.
Script execution needs a Professional licence.
**Any lab step that writes to a disk, edits RAM, or saves a carved file over 200 KB fails on the
free version.** Part 4 puts WinHex homework in S3 and S4 — **that homework must be re-scoped to
read-only, sub-200 KB tasks, or moved to HxD.**

### B4 — WinHex pricing is now partly subscription and version-gated

Specialist and Lab are 1- or 2-year non-perpetual. Personal/Professional perpetual licences bundle
updates only to a cutoff with surcharges beyond. **Never print prices or tier lists in durable
material** — they will be stale within a year.

### B5 — bulk_extractor 1.x → 2.x is a breaking change

BE2 was a major refactor (C++17, new option parser). `-o`, `-e`, `-x` survived, but
**`-o/--outdir` is now REQUIRED** — a BE1-era command without it fails. Also: **Kali packages
2.1.1 while upstream is 2.2.0**, so the version banner students see will not match a lesson written
against 2.2.0.

### B6 — HxD is fine today but single-maintainer and 5.5 years stale

Still free (private *and* commercial), still edits physical disks and RAM. No lesson breaks now.
Name a fallback in the setup guide in case it goes dark mid-course.

### B7 — PhotoRec/TestDisk is the safest tool in the set

GPLv2+, genuinely free, actively released, PhotoRec still bundled with TestDisk. Caution: 7.2 is
~2.5 years old; the 7.3-WIP beta is **not** suitable to teach against.

### NOT VERIFIED — block B

- foremost 1.5.7's **release date** — upstream publishes none anywhere; `CHANGES` has no dates.
  **Do not print a 1.5.7 release date.**
- scalpel's v2.0 date and its **command-line flags** — no man page rendered on the repo; commits
  page blocked by robots.txt.
- WinHex's **per-edition feature matrix** — the comparison page returned navigation chrome only on
  three attempts. Evaluation limits above come from the official manual PDF, which is primary.
- bulk_extractor 2.2.0's exact **year** — the latest-release page omitted it; 2024 taken from the
  full releases listing.

---

## C. NTFS, MFT and timeline tools

| tool | version | date | licence | flags verified | breaking change |
|---|---|---|---|---|---|
| MFTECmd | **2026.5.0** | not shown | MIT | **Yes** — `-f --csv --csvf --body --de` | **Yes — see C1** |
| Timeline Explorer | 2026.5.0 | not shown | not published | n/a | none |
| plaso / log2timeline | **20260720** | 20 Jul 2026 | Apache-2.0 | **Yes** — all three tools alive | minor, see C5 |
| analyzeMFT | **3.1.1** | 13 Aug 2025 | MIT | partially | **Yes — 3.x rewrite, new maintainer** |
| NTFS Log Tracker | 1.9 | 21 Jun 2025 | not stated (free) | n/a | v1.9 moved to 64-bit |
| dfir_ntfs | 1.1.20 | 31 Oct 2025 | GPL-3.0 | n/a | none |

### C1 — 🔴🔴 MFTECmd does NOT parse `$LogFile`, and its own README says it does

The source contains, verbatim:

```
case FileType.LogFile:
    Log.Warning("$LogFile not supported yet. Exiting");
    return;
```

The in-code `-f` description reads `File to process ($MFT | $J | $Boot | $SDS | $I30)`.
The **README's copy-pasted help block still lists `$LogFile`.**

**Teach: MFTECmd parses `$MFT`, `$J`, `$Boot`, `$SDS`, `$I30` — not `$LogFile`.**
This is the single most dangerous item in this document: anyone verifying against the README rather
than the source gets it wrong, and the failure is silent until a student runs it in class.
It also makes a superb live demonstration of **why the currency check exists**.

### C2 — `$I30` (INDX) support is new and undocumented in the README

If we teach index-attribute parsing, MFTECmd now does it.

### C3 — `--body` requires `--bdl`

Verbatim: *"--bdl is also required when using this option"*. `--bdl` takes the drive letter alone
(`C`, not `C:\`). **A lab step running `--body` on its own will fail.**
`--blf` toggles LF vs CRLF — matters if the bodyfile feeds `mactime` on Linux.

### C4 — `$J` needs `-m` for parent paths

`-m` supplies the `$MFT` when `-f` points at a `$J`, to resolve parent paths in the CSV. Without it
the output has no full paths. Common lesson gap.

### C5 — plaso syntax confirmed; one legacy trap

- `log2timeline.py --storage-file timeline.plaso /PATH/image.E01` — **the storage file is a flag,
  not positional.** Pre-2018 tutorials using `log2timeline.py timeline.plaso image.E01` are broken.
- `psort.py -o l2tcsv -w out.l2tcsv timeline.plaso` — **`l2tcsv` is still present**, not deprecated.
- `psteal.py --source <image> -w out.csv`
- Install: docker is the documented quickest route; Ubuntu via `ppa:gift/stable` then
  `apt install plaso-tools`; pip works. Docs: *"use a packaged release unless you are the
  adventurous type"*, and *"no older than 6 months"*.
- ⚠️ plaso's own Ubuntu page heading reads "Ubuntu 26.04 LTS (noble)" — **noble is 24.04**, so that
  page is internally inconsistent. Re-check before printing a version in a lab sheet.
- ⚠️ The `/releases` listing renders `20260512` as newest while `/releases/latest` and PyPI give
  **20260720**. Use 20260720.

### C6 — analyzeMFT changed hands and was rewritten

Now maintained by Benjamin Cance (`rowingdude/analyzeMFT`); the old `dkovar` URL redirects there.
v3.x is a ground-up rewrite with a much larger CLI (`--csv --json --sqlite --hash --chunk-size
--hash-processes --list-profiles --create-config`). **Any lesson built on 2.x is stale.**
It is **not** formally deprecated. Recommend: **MFTECmd primary, analyzeMFT as the cross-platform
Python alternative** — not as "superseded".

### C7 — the current tools for `$LogFile` / `$UsnJrnl` are neither MFTECmd nor Autopsy

- **NTFS Log Tracker 1.9** — GUI, Windows. Parses `$LogFile` and `$UsnJrnl:$J`, carves UsnJrnl
  records, accepts `$MFT` for path resolution, and v1.9 added **timestamp-manipulation detection**.
  Distributed via a Google Drive link from the author's site.
- **dfir_ntfs 1.1.20** — CLI, **GPL-3.0**, parses `$MFT`, `$J`, `$LogFile`, volumes, images, VSCs.
  **Better choice for us**: scriptable and explicitly licensed, which NTFS Log Tracker is not.

### C8 — `$LogFile` vs `$UsnJrnl` — the settled answer, for `S4-07`

`$LogFile` is NTFS's **transaction log**: Microsoft describes it as a journal of NTFS metadata
transactions, written *before* the metadata itself so the volume can be rolled back or forward —
log records containing a transaction's metadata operations are guaranteed to reach disk before the
modified metadata does. Because it logs the **before and after** of each metadata operation it is
far richer forensically, but it is a **small fixed-size circular file**: oldest entries are
overwritten once capacity is reached, commonly holding only **two to three hours** of normal usage.

`$UsnJrnl:$J` is a higher-level **change journal** recording only *a description of the change and
the name of the file or directory* — no original data, no record of what the change actually was —
and it is trimmed only lazily at NTFS checkpoints once it exceeds `MaximumSize` + `AllocationDelta`.

**`$UsnJrnl` therefore persists far longer** (practitioner consensus: days to weeks vs hours).
The two are used together: **`$J` for the long tail of *what* was touched, `$LogFile` for the short
high-fidelity window of *how*.**

> Teach the retention contrast as **relative**, never as a fixed figure — it is volume-size and
> activity dependent, and no primary source states a number for `$UsnJrnl`.

Sources: Microsoft "NTFS Metafiles" ($LogFile = File 2); Microsoft Windows Server 2003 NTFS
recoverability docs (write-ahead guarantee); Microsoft "Change Journals" and
"Creating, Modifying, and Deleting a Change Journal" / `fsutil usn` (checkpoint trimming);
Galhuber & Luh / Nordvik et al., *Artifacts for Detecting Timestamp Manipulation in NTFS*,
DFRWS 2020 (circular overwrite, the 2–3 hour figure).

### NOT VERIFIED — block C

- **MFTECmd and Timeline Explorer release dates** — vendor page shows none; the MFTECmd repo has no
  published releases. `2026.5.0` implies May 2026 but is not stated.
- **Timeline Explorer's licence** — no repo, no licence text. Free to download is evident; a formal
  licence claim is not. Do not print one.
- **NTFS Log Tracker's licence/cost** — the author's page states none; distribution is a bare Google
  Drive link. Widely used as freeware, but **do not print a licence claim**.
- **A specific `$UsnJrnl` retention figure** — no primary or peer-reviewed source states one.
- **analyzeMFT's last-commit date** — tag v3.1.1 / PyPI 13 Aug 2025 confirmed; 2026 activity is not.
- **plaso 20260720's changelog** — release body is only "Release of version 20260720", so
  undocumented breaking changes between 20250918 and 20260720 cannot be ruled out.

---

## What this changes in our material — action list

| # | Action | Where |
|---|---|---|
| 1 | Show the Autopsy ingest-module checklist explicitly; Keyword Search is OFF by default | `S2`, `S4` guided labs |
| 2 | **Re-scope the WinHex homework** to read-only, sub-200 KB tasks, or switch to HxD | Part 4 → S3, S4 homework |
| 3 | Drop scalpel; use foremost or PhotoRec. Install foremost via `apt`, never SourceForge | `S4-09` file carving |
| 4 | Teach `ddrescue` for damaged media, `dd`/`dc3dd` for healthy | `S2-04`, `S2-07` |
| 5 | **Verify Arsenal Image Mounter works inside the VMware guest** (.NET 10, vendor says bare metal) | Part 6 lab build, before `S2` |
| 6 | Teach MFTECmd as **not** parsing `$LogFile`; use dfir_ntfs for `$LogFile`/`$J` | `S4-07`, `S4-08` |
| 7 | `--body` always with `--bdl`; `$J` always with `-m` | `S4-08` lab steps |
| 8 | Pin plaso ≥ 20260720 and use `--storage-file` | `S6-07` |
| 9 | Use the TSK-download-page-vs-GitHub and MFTECmd-README-vs-source contradictions as the **live example of why the currency check exists** | `S1` or `S2` method segment |

**Re-run this check before any session that teaches these tools.** Forensic tooling rots fast, and
three of the nine actions above exist only because a project's own documentation was wrong.

---

## D. Memory forensics — acquisition and analysis

Added 2026-08-28 alongside the Memory Acquisition room extraction.

| tool | version | date | licence / free? | verified | maintained |
|---|---|---|---|---|---|
| **Volatility 3** | **2.28.0** | **30 Apr 2026** | Volatility Software Licence, free | Yes | Active |
| Volatility 2 | 2.6.1 | **repo archived 16 May 2025** | open source | Yes | **NO — EOL** |
| WinPmem | `v4.1.dev1` (pre-release); production = `go-winpmem_amd64_1.0-rc2_signed.exe` | year not published | Apache 2.0 | Partial | Low activity |
| MAGNET DumpIt for Windows | no version published | page updated 7 May 2025 | free (email gate) | Partial | Yes |
| Magnet RAM Capture | **1.20** | **24 Jul 2019** | free | Yes | **7 years stale** |
| Belkasoft Live RAM Capturer | **not published** | not published | free (email gate) | **No** | unknown |
| FTK Imager (free) | **8.3** | not published | free, registration | Partial | Yes (+ paid Pro line) |

### D1 — 🔴🔴 `windows.malfind` has been RENAMED to `windows.malware.malfind`

The old path is now a deprecation shim carrying `removal_date="2026-06-07"` — **a date that has
already passed.** It still runs today and emits a `FutureWarning`, but *"will be removed in the
first release after"* that date. **Teach `windows.malware.malfind`**; mention the old name as a
legacy alias only. Any slide or grading key using `windows.malfind` either prints a warning in
front of the class now or hard-fails at the next Volatility release.

**Every other plugin checked is live and correctly named** (each source file verified, none a
shim): `windows.info` · `pslist` · `psscan` · `pstree` · `cmdline` · `netscan` · `netstat` ·
`dlllist` · `handles` · `filescan` · `dumpfiles` · `registry.hivelist` · `registry.printkey`.

### D2 — 🔴🔴 Volatility 3 downloads Windows symbols from Microsoft's symbol server on demand

**This breaks our lab.** Part 6 states the forensics lab is offline and evidence VMs air-gapped
(and D29 exists because of it). Volatility 3 generates Windows symbol tables **from the network**
the first time it processes an image — so the first `windows.info` in class will stall or fail with
a symbol error.

**How to apply:** pre-populate `volatility3/symbols/` on the `CLEAN-TOOLS` snapshot (D17) for every
OS build our evidence uses, and verify offline before `S2`/`S6`. This is a lab-blocking item, not a
nicety. Note the irony worth teaching: **Volatility 2 failed offline because you picked the wrong
profile; Volatility 3 fails offline because it cannot reach the symbol server.**

### D3 — Profiles are gone in Volatility 3

Vol2 required `--profile=Win7SP1x64` and an `imageinfo`/`kdbgscan` workflow to find it; a wrong
profile gave silently wrong output. **Vol3 has no `--profile` at all** — it reads the kernel PDB
GUID out of the image and fetches matching symbols automatically ("automagic"). The command
collapses to `vol -f image.raw windows.pslist`, and the v3 counterpart of `imageinfo` is simply
`windows.info`. Auto-generation is **Windows-only**; Linux/macOS symbol tables are still manual.

**Any course material written from Volatility 2 gets this wrong in two directions** — it teaches a
mandatory profile step that no longer exists, and a profile-identification workflow that has no v3
equivalent.

### D4 — `vol`, not `vol.py`, on a pip install

The official quick-start is `vol -f <image> windows.info`. `vol.py` still exists **in a git clone**
and works, but a `pip install volatility3` puts no `vol.py` on disk. **Decide which install method
the lab uses and write every command to match.**

### D5 — 🔴 WinPmem: the fixed driver and the signed driver are mutually exclusive

**CVE-2024-10972** (GHSA-q5vw-gwwh-j8r7, CVSS **7.3**, published 16 Dec 2024): WinPmem's driver
exposes `\\.\pmem` and accepts unvalidated IOCTLs via `IRP_MJ_DEVICE_CONTROL` (CWE-20 + CWE-367
TOCTOU). **Fixed in 4.1.** But the vendor's own release notes say the only production binary,
`go-winpmem_amd64_1.0-rc2_signed.exe`, *"contains the old drivers"* — because they cannot sign the
new ones. The 4.1 driver is **test-signed only**, requiring `bcdedit /set testsigning on` and a
reboot, which is not acceptable on an evidence machine.

**How to apply:** do not present WinPmem as a no-caveats default. It is an excellent **BYOVD case
study** — a forensic tool whose own driver is the vulnerability.

### D6 — Magnet RAM Capture is stale and does not claim Windows 11

1.20, **July 2019**. Vendor lists XP/Vista/7/8/10 and Server 2003/2008/2012 — **no Windows 11, no
Server 2016+**. Still free and still listed, but out of scope by its own vendor for a modern lab
VM. **MAGNET DumpIt for Windows** (x86/x64/ARM64) is the sensible substitution.

### D7 — DumpIt outputs a crash dump, not raw — and that is fine

Magnet: DumpIt *"generates full memory Microsoft crash dumps"*; raw output *"remained a legacy
feature"*. ✅ **Volatility 3 reads crash dumps natively** (`WindowsCrashDump32/64Layer`, dump types
`0x01` complete and `0x05` bitmap, auto-selected) — so `vol -f memory.dmp windows.pslist` works with
no extra flags. Also: it is **"MAGNET DumpIt for Windows"** now; any slide branding it "Comae
DumpIt" or linking comae.com is dead.

### D8 — There is no read-only memory acquisition

Physical memory is unreachable from user mode on modern Windows, so **every credible acquirer loads
a kernel driver**. The acquisition binary, its DLLs, its allocations and the driver itself occupy
physical pages — **the tool writes to the thing it is measuring.** Three consequences to teach:

1. A memory capture is never a pristine observation the way a write-blocked disk image is. **The
   tool, its version and the exact time are part of the evidence** and belong in the notes.
2. A small footprint is a **forensic property**, not a convenience — the real argument for a
   single-purpose static acquirer over a GUI suite on the target.
3. **Driver signing is the modern operational bottleneck.** Secure Boot and signature enforcement
   block unsigned/test-signed acquirers on a correctly configured Windows 11 host, and disabling
   enforcement is itself a documented modification of the evidence system.

### D9 — Order of volatility: memory before disk, and the citation is still current

**RFC 3227 (BCP 55)**, *Guidelines for Evidence Collection and Archiving*, Feb 2002, §2.1 — an
example order of volatility placing **registers/cache → routing table, ARP cache, process table,
kernel statistics, memory → temporary file systems → disk → remote logging → physical
configuration → archival media**. Memory is tier 2, disk tier 4. BCP, not merely Informational, and
not obsoleted. <https://www.rfc-editor.org/rfc/rfc3227.txt>
NIST SP 800-86 is confirmed **Final and not withdrawn** — cite it as further reading only; the
volatility ordering was not confirmed from its landing page.

### NOT VERIFIED — block D

- **WinPmem release dates (year)** — GitHub renders no year; API and tags blocked.
- **FTK Imager 8.3 release date** — not published on any reachable Exterro page.
- **MAGNET DumpIt version and switches** — nothing published; support article is JS-rendered.
  **Run `DumpIt.exe /?` and capture the output before teaching any switch.**
- **Belkasoft Live RAM Capturer version/date** — Belkasoft publishes neither. **Given no published
  version, do not make it a primary lab tool.**
- **Which Volatility release introduced the `windows.malware` reorganisation** — confirmed by source
  code, but no changelog names it.
- **`procdump` current version** — the room shows **v11.0 (2022 copyright)**; not independently
  checked this pass.
- **Volatility's `windows.hyperv` plugin** — named by the Memory Acquisition room for `.vmrs` files;
  not in the plugin set verified above. Confirm before teaching.

---

## E. Additions and corrections from rooms 12–16 (appended 2026-08-28)

Sourced from `windows-memory-and-processes.md`, `windows-memory-and-user-activity.md`,
`windows-memory-and-network.md`, `forensic-imaging.md` and `autopsy.md`. Each full note carries the
citation; this block is the index.

### E1 — 🔴 Correction to **A1**: THREE Autopsy ingest modules are off by default, not one

A1 recorded "Keyword Search is OFF by default". Verified in `IngestJobSettings.java`
(`develop`, 2026-08-28):

```java
private static final Set<String> DEFAULT_DISABLED_MODULES = Stream.of(
        "Plaso", "Keyword Search", MalwareScanIngestModuleFactory.getDisplayName()
).collect(Collectors.toSet());
```

**Keyword Search · Plaso · Malware Scan.** Everything else loaded is on by default.
**Impact: a guided lab that expects keyword hits or a plaso timeline silently produces neither.**

### E2 — Autopsy and Sleuth Kit release dates now confirmed (closes an A-block NOT VERIFIED)

- **Autopsy 4.23.0 — 15 Apr 2026**; **4.23.1 — 7 May 2026** (packaging fix only: *"released as a
  Develop build, instead of Release"*). Actively maintained; commits into May 2026; development
  under **Sleuth Kit Labs** (formerly Basis Technology). No wind-down announcement.
- **Sleuth Kit 4.15.0 — 15 Apr 2026.** ⚠️ A3's contradiction stands: the **download page is stale**;
  the **sleuthkit.org news feed is the reliable source**.
- ⚠️ **Third-party sources are a year behind** — Wikipedia still lists 4.22.1 / April 2025. Do not
  cite them.
- Current user docs: `https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/`.
  **Autopsy is Apache 2.0**; the website and Sleuth Kit Labs branding are **not** covered by that
  grant.

### E3 — 🔴🔴 NSRL RDS is now SQLite-only — old hash-set import instructions are broken

> *"The NSRL has completed the transition away from the RDS 2.XX text file format, and will only be
> publishing the RDSv3 SQLite database format moving forward."*

Current **RDS 2026.06.1, published 1 June 2026**. Distributions: Modern PC · Legacy PC · Android ·
iOS, each full/delta and standard/minimal, shipped as **SQLite in ZIP**.
**The `NSRLFile.txt` path is gone. Re-verify our Autopsy hash-set import steps before `S2` ships.**

### E4 — Autopsy supported formats and data sources (corrects the room's list)

Data-source types (4.23.0): *Disk Image or VM File · Local Disk · Logical Files · Unallocated Space
Image Files · Autopsy Logical Imager Results · XRY Text Export*.
Image formats: Raw Single · Raw Split · EnCase `.e01` · VMDK · **VHD and VHDX**.
**VDI and AFF4 are NOT supported. L01 has only "limited support"**, via *Logical Files*.
Report modules (nine): HTML · Excel · Save Tagged Hashes · Extract Unique Words · **CASE-UCO** ·
Files–Text · **Google Earth KML** · **Portable Case** · **TSK Body File**.

### E5 — 🔴🔴 Mounting an evidence image read-write MODIFIES it

Four independent mechanisms, all verified:
1. **Mount count and mount time** — every rw mount writes `s_mnt_count` and `s_mtime` in the ext4
   superblock. **This alone changes the hash of a perfectly clean image.**
2. **`s_last_mounted`** — the kernel writes the examiner's own mount path into the evidence.
3. **atime** — the default is `relatime`, and *"the file's last access time is always updated if it
   is more than 1 day old"*, which is true of every file on an evidence image.
4. **Journal replay** on a dirty image — the kernel's ext4 doc: *"ext4 will replay the journal (and
   thus write to the partition) **even when mounted 'read only'**."*

🔴 **`-o ro` alone is NOT sufficient.** `mount(8)`: *"you may want to mount an ext3 or ext4
filesystem with the `ro,noload` mount options or set the block device itself to read-only mode."*

**Correct forms for our labs:**
```bash
sudo losetup -r -f --show evidence.dd                  # read-only at the block layer, first
sudo mount -o ro,noload,noatime,nodev,noexec /dev/loopN /mnt/case
sudo mount -t ntfs-3g -o ro,noatime,nodev,noexec,show_sys_files,streams_interface=windows \
     /dev/loopN /mnt/case
```
`show_sys_files` exposes `$MFT`/`$LogFile`/`$UsnJrnl` and `streams_interface=windows` exposes ADS —
**both are off by default and both are what S4/S5 depend on.**

### E6 — Software vs hardware write-blocking, and the NIST CFTT gap

- **`losetup -r` is enforced** by the loop driver. **`blockdev --setro` is advisory** — its man page
  says *"the currently active access to the device may not be affected"*, and filesystem drivers
  have historically written through it.
- 🔴 **NIST CFTT has never tested a Linux software write blocker.** Software Write Block spec is
  **v3.0, dated 2003**; its procedure document is titled *"…Interrupt 0x13 Based…"*; newest SWB
  report **Jan 2008**. The **Hardware** programme is live — spec v2.0, reports dated **16 Dec 2025**.
  **Say this plainly: software write-blocking on Linux is effective and unvalidated.**

### E7 — Acquisition tool currency (extends A5–A6)

| tool | status 2026-08-28 |
|---|---|
| **dc3dd** | **7.3.1** (Apr 2023) — dormant upstream, **actively packaged** (Debian `7.3.1-4`, Sep 2025). ⚠️ The Debian **man page footer still reads 7.2.646** even on 7.3.1. Hashing: `hash=` (repeatable: md5/sha1/sha256/sha512), `log=`, `hlog=`, `verb=`. ⚠️ **`hashlog=`/`hashconv=` are dcfldd options, not dc3dd.** |
| **dcfldd** | **1.9.3**, Debian `1.9.3-2` (Aug 2025) — volunteer-maintained after upstream death, **more recently released than dc3dd**. `hashwindow=` gives piecewise hashing. |
| **GNU ddrescue** | ✅ **1.30, Jan 2026** — current. The **mapfile** is what `dd` has no equivalent of: resumable rescue, no re-reading of good areas. |
| **Guymager** | **0.8.13 (Aug 2021)** upstream — stale, but **packaged in Debian as recently as Feb 2026**. Writes **dd, E01 and AFF**. |
| **libewf / `ewfacquire`** | ⚠️ upstream marked **"Status: experimental"**, newest artefact a **pre-release (20240506)**; **distros ship the 2014 stable** (Debian `20140816-2`, Nov 2025; Kali `20140816`). `ewfacquire` still exists. |
| **E01 vs AFF4** | **E01 remains the interchange standard. AFF4-L has NOT replaced it** — it appears in EnCase and AXIOM Cyber *alongside* E01. **Teach E01; mention AFF4-L.** |

**Recommendation for our lab:** Guymager or `ewfacquire` for the primary acquisition (E01 +
metadata + integrated verify) · `ddrescue` for damaged media · `dc3dd`/`dcfldd` as the "raw dd with
hashing" teaching step · **never plain `dd`**.

### E8 — HPA / DCO, and a typo that propagates

- 🔴 **`hparn` is not a command.** It is **`hdparm`**, and **`-I`** (query the drive now), not `-i`
  (the kernel's cached copy from boot). The typo originates in the Forensic Imaging room and has
  been copied into third-party write-ups.
- **`hdparm -N`** returns current-max **and** native-max sectors; a difference *"indicates how many
  sectors of the disk are currently hidden from the operating system, in the form of a Host
  Protected Area."* **`--dco-identify`** covers DCO.
- 🔴🔴 **`-N <value>` and `--dco-restore` are WRITE commands to the drive configuration.**
  **Detect and document only.**
- Other identity sources: `lsblk -o NAME,SERIAL,MODEL` · `smartctl -i` · `udevadm info` (`ID_SERIAL`,
  `ID_MODEL`, `ID_WWN`).

### E9 — Bash audit-trail semantics (for the S2 audit-trail exercise)

- `HISTSIZE=-1` and `HISTFILESIZE=-1` are **correct** (negative = unlimited / no truncation).
- ⚠️ **`HISTTIMEFORMAT="%F-%R "` yields `YYYY-MM-DD-HH:MM`** — `%R` is `%H:%M`. **Use `%F %T ` for
  seconds**; minute granularity cannot order two commands in the same minute.
- 🔴 **Bash writes history at shell EXIT**, not per command: *"When a shell with history enabled
  exits, the last $HISTSIZE lines are copied…"*. `shopt -s histappend` only changes
  append-vs-overwrite at that same write. **Add `PROMPT_COMMAND='history -a'`.** Even then a
  hung-then-killed command is never recorded — **`script` is the audit trail; history is the
  convenience copy.**
- ⚠️ **`script --timing` is deprecated** in current util-linux; use **`--log-timing`** (+ `--log-io`),
  replay with `scriptreplay`. `ttyrec` still packaged but redundant; `asciinema` 3.0 (Sep 2025) is
  better for producing teaching material.

### E10 — Volatility 3 additions (extends block D)

| item | result |
|---|---|
| release | **2.28.0, 30 Apr 2026**. ⚠️ **Do not cite 2.28.2** — that is the `develop` version; there is no such tag, and ReadTheDocs `/en/latest/` shows it. **Pin `/en/stable/`.** |
| 🔴 **more deprecated aliases** | Beyond `malfind`: **`windows.psxview` → `windows.malware.psxview`** and **`windows.ldrmodules` → `windows.malware.ldrmodules`**, both `removal_date="2026-06-07"` — **already past**, surviving in 2.28.0 only because that release predates the date. |
| 🔴🔴 **`apihooks` does not exist in Volatility 3** | Volatility 2 only, never ported. No `apihooks.py` anywhere under `plugins/windows/`. **A student who types it gets an unknown-plugin error.** |
| 🔴🔴 **second wave, removal 2026-09-25** | `windows.amcache` · `windows.cachedump` · `windows.hashdump` · `windows.lsadump` · `windows.scheduled_tasks` → **`windows.registry.*`**. ✅ **Checked: no existing room note names these — no back-propagation needed.** ✅ `windows.registry.hivelist` and `windows.registry.userassist` already live under `registry.` and are **not** in the wave. |
| 🔴 **`--yara-rules` renamed to `--yara-string`** | Valid `vadyarascan` flags: `--pid`, `--yara-file`, `--yara-string`, `--yara-compiled-file`, `--insensitive`, `--wide`, `--max-size`. |
| `windows.sessions` | ✅ current. 🔴 **`Create Time` is `_EPROCESS.CreateTime` — a PROCESS start, not a logon time.** No SID column (`User Name` comes from the `USERNAME`/`USERDOMAIN` **environment variables**); `Session Type` is the `SESSIONNAME` env var verbatim, not a LogonType. |
| `windows.memmap` | ✅ current. `--pid` is a **single int**, not a list. `--dump` writes `pid.<PID>.dmp`. ⚠️ **Re-running in the same directory appends a counter rather than overwriting.** |
| `windows.netscan` / `netstat` | ✅ both current, **identical ten-column set**. `netscan` = pool scan (recovers closed sockets, some false positives); `netstat` = live `tcpip.sys` structures. 🔴 **`netstat` hard-fails without tcpip symbols** — *"Unable to locate symbols for the memory image's tcpip module"* — **relevant to an air-gapped lab.** |
| `_EPROCESS.ImageFileName` | **15 bytes** on Windows 7+ (16 on Vista and earlier). **14 printable characters survive in practice.** |

### E11 — ATT&CK currency (repo-wide)

- 🔴🔴 **ATT&CK v19 renamed TA0005 from "Defense Evasion" to "Stealth"**; the remainder split into
  **TA0112 "Defense Impairment"**. Validated against **Enterprise v19.2** (v19 released 2026-04-28;
  v19.2 point release 2026-08-06). ✅ **Back-propagated to `fat32-analysis.md`; repo grep clean.**
- 🔴🔴 **`T1043 Commonly Used Port` is DEPRECATED** — *"Please use Non-Standard Port where
  appropriate."* Deprecated in **ATT&CK v7, July 2020**. Replacement **T1571 Non-Standard Port**,
  and the logic inverted: T1043 flagged *common* ports, T1571 flags *uncommon* pairings.
- 🔴 **T1055.002 is "Portable Executable Injection", not "Reflective DLL Injection".** Reflective
  loading is **T1620 Reflective Code Loading** (tactic **Stealth**). T1055.001 is
  **Dynamic-link Library Injection**.
- 🔴 **T1547.001 is "Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder"** —
  ⚠️ not T1037.005 "Startup Items", which is **macOS-only**. The two parents are near-twins:
  **T1037 Initialization Scripts** vs **T1547 Autostart Execution**.
- ➕ **T1137.001 Office Application Startup: Office Template Macros** — the correct ID for malicious
  VBA in `Normal.dotm`. Platforms **Office Suite, Windows**; last modified 12 May 2026.
- ⚠️ **T1021.004 SSH lists ESXi, Linux and macOS — not Windows.** Check the platform field before
  citing any sub-technique.
- ➕ **No ATT&CK ID distinguishes a bind shell from a reverse shell.** Use **T1571** for a listener
  on a non-standard port; **T1095** for a raw non-application-layer channel; **T1205** only for a
  dormant listener woken by a signal.

### E12 — 🟢🟢 CFReDS: the evidence finding (see `autopsy.md` §4)

**NIST CFReDS "Data Leakage Case"** is a **US Government work in the public domain under
17 U.S.C. §105.** NIST's terms permit free modification and redistribution with attribution.
**Linking is unambiguously fine; commercial training use is unrestricted; rehosting is permitted.**

Supplies **NTFS (PC) · exFAT (RM#1) · FAT32 (RM#2) · UDF/optical (RM#3)** from one scenario, in
**both E01 and raw**, with **published SHA-1 hashes** and a **46-question answer key**.
🔴 **The answer key is instructor-only.** ⚠️ Downloads live on **`cfreds-archive.nist.gov`** even
though the portal is `cfreds.nist.gov`. ⚠️ The raw variants are **7-Zip split archives**
(`.7z.001`), not raw-split segments — extract before adding to Autopsy.

**Second candidate: the CFReDS Hacking Case** (31 Q&A). ⚠️ NIST's own scenarios appear unchanged
since ~2019–2020.

### NOT VERIFIED — block E

- Exact PR/merge date for `windows.psxview`'s addition (GitHub API rate-limited; bracketed between
  Volatility 3 **2.8.0** and **2.11.0**).
- Meanings of UserAssist GUIDs `{9E04CAB2-…}` and `{FA99DFC7-…}` — genuine GUIDs, **no source
  documents what they track**. **Do not assert a meaning.**
- Whether `olevba` officially accepts a bare `vbaProject.bin` — the documented input list is
  containers only. **Use the container form and do not make the claim.**
- Newest CFReDS dataset date — portal API truncates; NIST-authored sets appear static since
  ~2019–2020.
- Autopsy feature-by-feature behaviour with a missing image — no doc enumerates it; the
  metadata-vs-content split in `autopsy.md` §2.2 is read off the Portable Case design.
- Exact date of the most recent `oletools` commit (GitHub API 403). Released **0.60.2 (Jul 2024)**;
  development head **0.60.3** per a changelog entry dated **2026-01-26**.

---

## F. Live Windows response — SRUM, KAPE, pktmon (appended 2026-08-28, from room 17)

Full citations in `windows-network-analysis.md` §3.

### F1 — 🔴🔴 KAPE IS NO LONGER FREE FOR COMMERCIAL USE — closes the block-A/B NOT VERIFIED item

Official KAPE FAQ, verbatim:

> *"KAPE is free for any local, state, federal or international government agency. KAPE is also free
> for educational, research, and internal company use."*
> **"As of January 1, 2026 KAPE IS NO LONGER AVAILABLE for commercial use (i.e. when used on a
> third-party network and/or as part of a paid engagement)."**

✅ **Our classroom use is educational and remains free.**
🔴 **Our students are practising analysts.** Anyone doing paid client work or third-party IR
**cannot use KAPE for it as of 1 Jan 2026**, and we teach KAPE in S4 and S5. **Needs a
`DECISIONS.md` row — recommendation: teach KAPE for the concepts and pair every KAPE step with a
free standalone alternative (the EZ Tools underneath it are separately free).**

### F2 — KAPE version, finally verified after four attempts

**KAPE core is 1.3.0.2, released 22 Dec 2022.** Nothing newer exists.
🟢 **Important nuance: "KAPE is stale" is wrong.** The **core binary** has not moved since 2022;
**KapeFiles (targets and modules) ships by commit and is updated continuously** — its releases page
reads *"There aren't any releases here."*
⚠️ **There is no stable direct download URL** — it is form-gated on Kroll's product page, which is
why every bookmarked file URL 404s.

**Route, for future reference:** `github.com/*/tree/*` and `/commits/*` are robots-disallowed and
`api.github.com` returns 403; KapeDocs renders client-side only. The way in is
`raw.githubusercontent.com/EricZimmerman/KapeDocs/master/navigation.md`, which lists every page path
verbatim — including `Pages/0.-Changelog.md`.

### F3 — 🟢🟢 SRUM: a first-rank artifact we did not have

**`C:\Windows\System32\sru\SRUDB.dat`**, an **ESE/JET Blue** database. The Network Data Usage
Monitor table **`{973F5D5C-1D90-4944-BE8E-24B94231A174}`** carries **`BytesSent` and `BytesRecvd`
per application per user per hour**; `SruDbIdMapTable` resolves the app to a string and the user to
a **SID**. **This is the only host-side answer to "how much data left, through what, and when."**

Other tables: `{DD6636C4-…}` network connectivity · `{D10CA2FE-…FA89}` application resource usage ·
`{5C8CF1C7-…}` app timeline · `{FEE4E14F-…}` energy · `{D10CA2FE-…FA86}` push notifications.

**Limits to teach:**
- **Hourly buckets** — you cannot time a transfer from SRUM, only the hour.
- **Two-tier**: a **Tier1 in-memory store updated every 60 s**, a **Tier2 on-disk database updated
  hourly** and at shutdown. **Up to an hour exists only in RAM.** ⚠️ **From Windows 10 2004 onward
  the shutdown write is not guaranteed.**
- 🔴 **The "last hour is staged in the registry" advice is LEGACY** — true on Windows 8/8.1, false
  on 10/11, where the registry holds table names only. **The last hour is in memory** — a fresh
  argument for memory-first acquisition.
- **VPN attribution is wrong by design** — bytes are attributed to the **VPN client**, not the
  originating app.
- **No destination.** Volume and process only.
- **Retention is per-table**: ~60 days for network and application usage, **7 days** for App
  Timeline, 5 years for long-term (`}LT`) tables. **Teach "roughly 30–60 days, varies by table."**
- ⚠️ **`SruDbIdleRetentionPeriod` / `SruDbRolloverTimeSpan` — NOT VERIFIED, likely fabricated.**
  These circulate in DFIR write-ups; exact-phrase searches return nothing and no source documents
  any registry value controlling SRUM retention. **Do not put them in our material.**

**Acquisition:** the file is **locked on a live host** and usually **dirty** when copied. Repair
before parsing: `esentutl.exe /r sru /i` then `esentutl.exe /p SRUDB.dat`. **VSS preserves
historical SRUM state** and is how you exceed the retention window.

### F4 — SRUM parsers, both corrected

- 🔴 **KAPE has no `SRUMDump` module.** `Modules/Apps/SRUMDump.mkape` **404s**. What exists is
  **`Modules/EZTools/SrumECmd.mkape`** (Category `SRUMDatabase`,
  `-d %sourceDirectory% --csv %destinationDirectory%`), one of the 15 processors inside
  **`!EZParser.mkape`**. Target **`Targets/Windows/SRUM.tkape`** collects `C:\Windows\System32\SRU\`
  recursively **plus the SOFTWARE hive and its `.LOG*` files** — because SrumECmd wants `-r`.
- **`SrumECmd`** (Eric Zimmerman) — **current version 2026.5.0**, CSV output:
  `SrumECmd.exe -f SRUDB.dat -r SOFTWARE --csv <out>`.
- 🔴 **`srum-dump` was rewritten and the XLSX template is gone.** Current **v3.2 (Jun 2025)**;
  v3.0 announced in SANS ISC **27 Apr 2025**. **Version 3 IS the rewrite** — there is no
  "srum-dump2". Inputs: **SRUDB.dat (required)** + **SOFTWARE hive (optional)**; configuration is
  `srum_dump_config.json`; output XLSX **or CSV**. **`SRUM_TEMPLATE.xlsx` survives only in stale
  forks — any instruction to supply a template is obsolete.**

### F5 — 🔴🔴 `Get-WmiObject` is REMOVED in PowerShell 6/7

Superseded in PowerShell **3.0**; Microsoft lists it under *"Cmdlets removed from PowerShell"*:
*"The following WMI v1 cmdlets were removed from PowerShell: Register-WmiEvent, Set-WmiInstance,
Invoke-WmiMethod, **Get-WmiObject**, Remove-WmiObject."*

**Any of our material using `Get-WmiObject` will fail on PowerShell 7.** Replacement:
`Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $($_.OwningProcess)"`.
✅ `Get-NetTCPConnection`, `Get-NetUDPEndpoint` (NetTCPIP), `Get-DnsClientCache` (DnsClient) and
`Get-SmbConnection` (SmbShare) are all current and **all three modules are "Natively Compatible"
with PowerShell 7**.

### F6 — `pktmon` corrections

- Present since **Windows 10 1809**, documented from **build 19041 (2004)**; current on Win10/11 and
  Server 2016/2019/2022/2025.
- Verbs: `filter · list · start · stop · **status** · **unload** · counters · reset · etl2txt ·
  etl2pcap · **hex2pkt** · help`. ⚠️ **`comp` is a `start` parameter, not a verb.**
- Defaults: `PktMon.etl` · **512 MB** · **circular** · **`--pkt-size` 128 bytes (packets are
  truncated!)** · `--flags 0x012`. ⚠️ **The widely repeated "768 MB memory" figure is not in
  Microsoft's documentation** — memory mode's buffer is governed by `--file-size`.
  ⚠️ Microsoft documents only the **file name**, not a directory — it lands in the **cwd**, which
  from an elevated prompt is `System32`. Requires elevation (third-party sources; **Microsoft Learn
  does not state it**).
- 🔴🔴 **Cannot see loopback** — *"the Windows loopback implementation does not use NDIS."* Local
  proxies, C2 relays and `127.0.0.1` pivots are invisible.
- 🔴 **`etl2pcap` discards the drop reports and stack-component attribution** — *"all information
  about the packet drop reports and packet flow through the networking stack is lost in pcapng
  format output."* Dropped packets need a second `--drop-only` pass. **802.11 captures convert
  incorrectly** and Wireshark mis-decodes them.

### F7 — Windows Firewall logging is OFF by default

*"No logging occurs until you set one of following two options"* — **Log dropped packets** and
**Log successful connections**, independently defaulting to **No**, **per profile**.
Path `%windir%\system32\logfiles\firewall\pfirewall.log`; **default max size 4,096 KB** (settable to
32,767 KB), one prior generation as `.old`.
Fields include **`path` = SEND / RECEIVE / FORWARD / UNKNOWN**.
**Contains no payload, no process name, no PID, no user — and nothing from before logging was
enabled.** 🟢 **The cleanest "absence is not evidence of absence" artifact we have.**

### F8 — `netstat -n` and `qwinsta`

- 🔴 **`netstat` without `-n` makes the evidence host resolve names** — *"no attempt is made to
  determine names"* is what `-n` buys. Without it: the DNS cache and SRUM's network tables are
  contaminated at collection time, the operator may be tipped off, and the command hangs on
  unreachable DNS. **Teach `netstat -anob`.** ⚠️ `-b` *"can be time-consuming and will fail unless
  you have sufficient permissions"* — which is what `Can not obtain ownership information` means.
  🟢 `Get-NetTCPConnection` never resolves names.
- 🔴 **`qwinsta` shows NO source IP.** Columns are SESSIONNAME · USERNAME · ID · STATE · TYPE ·
  DEVICE. RDP source IP comes from **Event 1149** in
  `Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational` (`Param3`),
  **4624 LogonType 10**, and **4778/4779**; session lifecycle from
  `…TerminalServices-LocalSessionManager/Operational` IDs **21–25**.
  ⚠️ **1149 fires on channel establishment, not authentication** — *"this event does not indicate a
  successfully authenticated RDP session has taken place"*. **1149 without a matching 4624 is the
  brute-force pattern.**

### F9 — `Get-DnsClientCache`

Memory-only; destroyed by reboot, `Clear-DnsClientCache` / `ipconfig /flushdns`, TTL expiry, or
**stopping the `Dnscache` service** — and a stopped Dnscache is itself a finding.
The `TimeToLive` column is the **remaining** lifetime in seconds, so **original TTL minus observed
TTL ≈ seconds since the lookup**. 🟢 **Collect it before running anything that resolves names.**

### NOT VERIFIED — block F

- **SRUM retention registry values** (`SruDbIdleRetentionPeriod`, `SruDbRolloverTimeSpan`) — no
  source anywhere. Very likely fabricated; **do not teach**.
- **`pktmon` "768 MB memory"** — not documented and contradicted by `--file-size`.
- **Microsoft's own statement that `pktmon` requires elevation** — not on Microsoft Learn; confirmed
  only by third-party sources.
- **Microsoft root cause for `Can not obtain ownership information`** — the Microsoft Q&A thread has
  no accepted answer. Two causes observed: unelevated shell (documented) and protected/System
  processes (observed).
- **The canonical acquisition methods for a locked `SRUDB.dat`** — KAPE and offline/bootable
  acquisition are cited; raw NTFS read and VSS-as-acquisition are not stated in a citable source
  (VSS appears only as a retention-extension technique).
- **`srum-dump` 3.2's release year** — GitHub renders "05 Jun" without a year; anchored to 2025 via
  the SANS ISC v3 announcement of 2025-04-27.
- **Commands for the room's two empty sections** — named pipes (`Get-ChildItem \\.\pipe\`) and WinRM
  sessions (`Get-WSManInstance -ResourceURI shell -Enumerate`). **Verify on a live host before
  teaching.**

---

## G. Windows log sources — PowerShell, Task Scheduler, RDP, Defender, web (appended 2026-08-29, from room 19)

Full citations in `logless-hunt.md` §3.

### G1 — 🔴🔴 PowerShell script block logging has THREE states, not two

| policy state | effect |
|---|---|
| **Not Configured** (default) | **automatic script block logging is ACTIVE** — Microsoft: *"PowerShell automatically logs script blocks when they have content often used by malicious scripts… a record of last resort."* |
| **Enabled** | everything logged, level **Verbose** |
| **explicitly Disabled** / `EnableScriptBlockLogging = 0` | **even the record of last resort is gone** |

🟢 **Hunt for the value `0`, not for the key's absence** —
`HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging\EnableScriptBlockLogging = 0`
**is a defence-evasion IOC.**
⚠️ Level distinguishes the mechanism: **Verbose = policy-driven, Warning = automatic suspicious
subset.** (The Warning level is DFIR-sourced, not Microsoft-documented.)

### G2 — 🔴🔴 PowerShell 7 logs to a different channel under a different policy key

- **pwsh 7 → `PowerShellCore/Operational`**, policy at
  `HKLM\Software\Policies\Microsoft\`**`PowerShellCore`**`\ScriptBlockLogging`.
- **Windows PowerShell 5.1 → `Microsoft-Windows-PowerShell/Operational`**, policy at
  `…\Windows\PowerShell\…`.
- 🔴 **An organisation that enabled script block logging via the Windows PowerShell GPO has ZERO
  coverage of pwsh 7.** ⚠️ The pwsh provider must also have been registered
  (`$PSHOME\RegisterManifest.ps1`) or **the channel may not exist on the host.**
- 🟢 **But pwsh shares `ConsoleHost_history.txt` with 5.1** (`$Host.Name` is `ConsoleHost` for both)
  — the one place it does not evade.
- ➕ Transcription policies are keyed the same way (`…\PowerShellCore\Transcription`).

### G3 — PSReadLine history: incremental, per-host, and lossy by design

- Path `$Env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\`**`$($Host.Name)_history.txt`** —
  ⚠️ **per-host**: VS Code writes `Visual Studio Code Host_history.txt`. **Collect the folder, not a
  filename.**
- 🟢 **Written incrementally, not at exit** — default `HistorySaveStyle` is `SaveIncrementally`:
  *"Save history after each command is executed."* **A killed session still leaves history** —
  the **opposite** of bash (block **E9**). Say this explicitly; students assume they match.
- `MaximumHistoryCount` = **4096**; ⚠️ overflow behaviour undocumented — **do not teach a
  truncation mechanism.**
- 🔴 **Lossy by design**: lines containing `password`, `asplaintext`, `token`, `apikey`, `secret`
  are **never written**, and **`-AddToHistoryHandler` suppresses arbitrary commands.**
- ⚠️ Exclusion of non-interactive `-Command` / `-EncodedCommand` is **observed, not
  Microsoft-documented** — demonstrate in lab.

### G4 — the classic `Windows PowerShell` channel is the best default-on artifact

**400** EngineStart · **403** EngineStop · **600** provider start/stop · **800** pipeline
(*inconsistently logged*).
🟢 **`HostApplication` carries the full command line including `-EncodedCommand`, with zero
configuration** — so a base64 payload is recoverable even with 4104 off.
🟢 **600 with `ProviderName = WSMan` indicates PowerShell remoting.**
➕ **Transcription is a fourth source** — it captures **command output**, which 4104 does not; off by
default; can be pointed at a **central share**, out of the attacker's reach.

### G5 — 🔴🔴 Hidden scheduled tasks via `SD` deletion (Tarrask)

Deleting the **`SD` (Security Descriptor)** value under
`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\<task>` makes the task
**vanish from `schtasks /query`, Autoruns and the Task Scheduler GUI while it continues to run.**
Microsoft (Tarrask): *"removal of this value results in the task 'disappearing' from
'schtasks /query' and Task Scheduler."* Requires **SYSTEM**.

🟢 **The mechanism is the lesson: the task is not obfuscated, it is made unreadable — and the
enumerating tools fail OPEN, silently omitting it rather than erroring.**
🟢 **Detection is a cross-check, not a scan:** diff `TaskCache\Tree` subkeys against the XML in
`C:\Windows\System32\Tasks`; a Tree entry with no XML, or a missing/null `SD`, is the IOC.
`Tree` values also store **a hash of the XML** — a second integrity check. Tool: `HiddenTaskHunter`.

### G6 — Task Scheduler and RDP channels

- ⚠️ **`Microsoft-Windows-TaskScheduler/Operational` is off by default** — confirmed by two
  independent technical sources, **but Microsoft never states it.** Say so.
  **Consequence: on an unmanaged endpoint the primary task evidence is the registry TaskCache plus
  the XML, not this channel.** Enable with
  `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true`; the GUI's *"Enable All Tasks
  History"* is the same switch.
- IDs: **106** registered (**names the registering user**) · **100** started · **129** created task
  process (**gives the PID**) · 102 completed · **140** updated · **141** deleted · 142 disabled ·
  **200/201** action started/completed (**names the executable and the return code**) ·
  110/118/119 triggered by user/boot/logon. 🟢 **Triage pair: 106 + 200/129.**
- ➕ **Security 4698** carries the **full task XML** and, on Windows 10 1903+, the **parent process
  of the creation**. ⚠️ Governed by **Audit Other Object Access Events**; **its OS default is NOT
  VERIFIED** — Microsoft publishes a *recommendation* table easily misread as defaults. **Check with
  `auditpol /get /subcategory:"Other Object Access Events"`.**
- **RDP `…TerminalServices-LocalSessionManager/Operational`** (on by default): **21** logon ·
  **22** shell start (*proves an interactive desktop*) · **23** logoff · **24** disconnect ·
  **25** reconnect · 39/40 disconnect with reason code. **Session ID is the join key.**
  🔴 **Only successful logons appear — failures are Security 4625.**
  🔴 **Filter out `Source Network Address = LOCAL` or you will over-count RDP logons** — the most
  common student error with this artifact.
  ⚠️ **1149 fires BEFORE 21 and is not authentication** (*"a client launched RDP and reached the
  login prompt before entering any credentials"*). Chain: **1149 → 4624 type 10 → 21 → 22**;
  **1149 with no matching 21 = scanning or failed credentials.** NLA-dependent; sources disagree.
  (Consistent with block **F8**.)

### G7 — 🔴 Windows Defender: event 5013 is Tamper Protection, not exclusions

| ID | meaning |
|---|---|
| **1116** | malware detected |
| **1117** | action taken (**`Action: Allow` is the highest-value field in the channel**) |
| **5001** | real-time protection disabled |
| **5004** | real-time protection configuration changed |
| **5007** | configuration changed (carries *"Old value"* / *"New value"*) |
| **5010** | antispyware disabled |
| **5012** | antivirus disabled |
| **5013** | 🔴 **Tamper Protection blocked a change** — *not* exclusion creation |

🟢 Which makes 5013 **more** useful: **a burst of it is an attacker actively failing to weaken
Defender.** ➕ **5001 alone does not cover a full AV disable — add 5010 and 5012.**
🟢 `Detection Source: AMSI` bridges to the PowerShell section; **a 1116 with no matching 1117 =
detected but not remediated.**

**Exclusions** live in **two** keys — `HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions` (local)
and `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions` (GPO) — subkeys **Paths,
Extensions, Processes, IpAddresses**. 🟢 One-liner: `MpCmdRun.exe -CheckExclusion -Path <path>`.
⚠️ **Exclusion creation surfacing as a 5007 is inferred** — no published sample shows a 5007 naming
an `Exclusions\Paths` value. **Generate one with `Add-MpPreference -ExclusionPath` and capture it
before teaching it.**

### G8 — Defender DetectionHistory is a second, independent store

`%ProgramData%\Microsoft\Windows Defender\Scans\History\Service\DetectionHistory\<n>\`.
🟢 **Richer than the event log**: SHA-256 and MD5, **`SpawningProcessName`**, **the creating user**,
and the user's response (quarantine/allow/remove).
🟢 **Independent of the event log — diff them; a detection in one and not the other is selective
tampering.** ⚠️ The **Windows Security GUI reads DetectionHistory, not the event log.**
Parser: **DHParser** (`jklepsercyber/defender-detectionhistory-parser`), or the Velociraptor
artifacts `Windows.Applications.DefenderDHParser` / `…DefenderHistory`.

### G9 — 🔴 IIS logs User-Agent, Referer and username BY DEFAULT

Default `logExtFileFlags`: `Date, Time, ClientIP, **UserName**, ServerIP, Method, UriStem,
UriQuery, TimeTaken, HttpStatus, Win32Status, ServerPort, **UserAgent**, HttpSubStatus, **Referer**`.
Genuinely **off**: `BytesRecv`, `BytesSent`, **`Cookie`**, **`Host`**, `ProtocolVersion`, `SiteName`,
`ComputerName`. Default path root `%SystemDrive%\inetpub\logs\LogFiles`; format **W3C**; logging
**on**; period Daily; truncateSize 20 MB.

⚠️ **Time-sensitive:** *"Starting with the February 2026 Windows Update, `BytesRecv` and `BytesSent`
are included by default … on Windows 11 and Windows Server 2019 and later."* **Current now, absent
on any older or unpatched host — teach reading the `#Fields:` line, never assuming.**
🟢 Highest-value missing field is **`Host`** (no per-tenant attribution); second is **`Cookie`**.

**Apache**: `\Apache24` **is** the Apache project's documented default ServerRoot — ⚠️ but the ASF
ships no Windows binary, so third-party builds may sit elsewhere. **Resolve `ServerRoot` from
`httpd.conf`.** ⚠️ **The shipped `CustomLog` uses `common`, which has NO User-Agent and NO
Referer** — a default Apache logs *less* than a default IIS.
⚠️ Apache error-log gotcha: *"'File does not exist' messages for 404 responses are logged at `info`
level and will not appear in the error log with the default `LogLevel` of `warn`"* — **directory
brute-forcing is invisible there; read the access log.**

### G10 — 🔴 Web access logs contain no request body

Neither IIS's default field set nor Apache `combined` carries one. **A webshell operated over POST
leaves a line indistinguishable from a legitimate form submission — same URI, same 200, same UA.**
Also absent: response bodies, and almost all request headers (no `Authorization`, no
`X-Forwarded-For`).
🟢 **IIS rotation does not delete** — it opens a new file and keeps the old ones; Microsoft ships no
cleanup and documents *"running a script … in a scheduled task"* as the approach. **So the deletion
mechanism on a typical IIS host is an administrator's own scheduled task — which G5 says an attacker
can create or hide. Check for a scheduled task that deletes web logs.**
⚠️ Absent logs are as often *"users turn off logging completely"* as anti-forensics.

### NOT VERIFIED — block G

- PSReadLine overflow behaviour at `MaximumHistoryCount`; and the PSReadLine version that made
  incremental saving the default.
- Exclusion of non-interactive `-Command` from `ConsoleHost_history.txt` (observed, not documented).
- The **Warning** level for automatic script block logging (DFIR-sourced, not Microsoft).
- `Microsoft-Windows-TaskScheduler/Operational` default state **per Microsoft** (two independent
  sources agree it is off; Microsoft is silent).
- **Audit Other Object Access Events** OS default — check with `auditpol`, do not read Microsoft's
  recommendation table as a statement of defaults.
- RDP event **261** message text — do not teach a definition.
- Defender **`file:_` / `webfile:_`** path prefixes — real in the wild, undocumented by Microsoft.
- A sample **5007** showing an `Exclusions\Paths` value.
- IIS **`W3SVC<n>`** subfolder convention per Microsoft (root confirmed; subfolder is observed).
- Apache log rotation as a **documented** anti-forensics technique (mechanics documented, abuse
  inferred).

---

## H. Browser, email and chat artifacts (appended 2026-08-29, from room 20)

Full citations in `blizzard.md` §3. **Scope decided in `DECISIONS.md` D35.**

### H1 — 🟢🟢 The WebView2 convergence: browsing, email and chat are one artifact family

| app | local evidence |
|---|---|
| Edge / Chrome | `%LOCALAPPDATA%\{Microsoft\Edge,Google\Chrome}\User Data\<profile>\` |
| **new Outlook (`olk.exe`)** | **`%LOCALAPPDATA%\Microsoft\Olk\EBWebView\`** — Chromium disk-cache format (`data_0`…`data_3`, `index`) |
| **new Teams** | **`%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\EBWebView\Default\IndexedDB\`** |

**All three are WebView2 (Chromium) profile directories.** One technique now covers three artifact
families. ⚠️ The new-Outlook path is **observation-derived, not Microsoft-documented** — teach it as
such.

### H2 — 🔴 Chromium timestamps: same epoch as FILETIME, different unit

Microseconds since **1601-01-01 UTC** (Chromium's header: *"an absolute point in coordinated
universal time (UTC)"* — **not localised on write**).
`datetime(v/1000000 - 11644473600, 'unixepoch')`.
🔴 **FILETIME is 100-ns intervals — a factor of 10. The #1 student conversion error.**
Firefox `places.sqlite` is microseconds since **1970** UTC.
🟢 **Teaching point:** the browser value *is* UTC on disk, so "in UTC" means *apply no timezone*;
event logs are also stored UTC but every viewer renders them local. **Storage timezone and display
timezone are different questions — say which you are reporting.**

### H3 — 🟢🟢 `visits.transition`: click vs redirect vs automatic

Core type in the low byte (`0xFF`), qualifiers above (`0xFFFFFF00`).
**Deliberate:** `TYPED(1)`, `GENERATED(5)`, `FORM_SUBMIT(7)`, `AUTO_BOOKMARK(2)`.
**Automatic:** `AUTO_SUBFRAME(3)`, `AUTO_TOPLEVEL(6)`, `RELOAD(8)`.
**`IS_REDIRECT_MASK = 0xC0000000`** — `SERVER_REDIRECT (0x80000000)`, `CLIENT_REDIRECT (0x40000000)`.
🟢 **`CHAIN_END` without `CHAIN_START` is the landing URL; `CHAIN_START` without `CHAIN_END` is a hop
the user never saw rendered. A `LINK` transition carrying `SERVER_REDIRECT` means the user clicked
something else and was carried here** — the signature of a phishing redirect.
`visits.from_visit` / `opener_visit` rebuild the chain rather than inferring it.

### H4 — 🔴🔴 A history row may not be from this machine, or from a human

`VisitSource`: `SOURCE_SYNCED` (another device) · `SOURCE_EXTENSION` ·
`SOURCE_{FIREFOX,IE,SAFARI}_IMPORTED` · `SOURCE_OS_MIGRATION_IMPORTED` · **`SOURCE_ACTOR` —
"Added by the GLIC actor"**.
⚠️ **Agentic browsing writes history rows no human generated.** New in 2026; no course covers it.
`originator_cache_guid` / `originator_visit_id` are the tell.
**Absence** is equally weak: Incognito writes **no** visit row (*"Chrome retains bookmarks that you
save and files that you download when you exit Incognito"* — **look outside the profile**), and
`Profile 1`/`Profile 2`/`Guest Profile`/`System Profile` are **separate databases** —
**examining only `Default` is an incomplete examination.**

### H5 — 🟢🟢 Cleared history usually survives on disk

SQLite `secure_delete` is **off by default**, and freelist leaf pages are deliberately never read or
written *"in order to reduce disk I/O"* — deleted records persist intact until the pages are reused.
⚠️ **DB Browser for SQLite will not show them** (it reads the b-tree, not the freelist).
⚠️ **Chromium History does NOT use WAL by default** (`kHistoryDatabaseWriteAheadLogging` is
`FEATURE_DISABLED_BY_DEFAULT`) — expect `History-journal`. **But WAL is persistent once set**, so
**collect `History`, `-journal`, `-wal` and `-shm` and check which exist.**

### H6 — `downloads`: four separable claims, not one

**requested** → `downloads_url_chains.chain_index = 0`, `tab_url`, `referrer`
**arrived** → `state`, `received_bytes == total_bytes`, non-zero `end_time`, populated **`hash`
(raw SHA-256 of contents)**, `current_path == target_path`
**served from elsewhere** → the **highest** `chain_index` — *"the link looked like X but delivered
from Y"* in one query
**opened** → `opened = 1`, `last_access_time` — **a separate and much stronger claim**

⚠️ **Do not trust the enum**: the on-disk schema comment says `1=complete, 4=interrupted`; the
in-memory enum is `IN_PROGRESS=0, COMPLETE=1, CANCELLED=2, INTERRUPTED=3`. **They differ. Validate
empirically or use a parser.**
🟢 `hash` bridges to disk and to threat intel **even when the file is deleted**; `danger_type`
firing means the browser warned and the user overrode it — **user-intent evidence.**

### H7 — 🔴🔴 Outlook: classic to 2029, but new Outlook has no OST

- Classic: `.ost` at `%LOCALAPPDATA%\Microsoft\Outlook\`, `.pst` under `Documents\Outlook Files\`.
  *"supported until at least 2029"* — **the OST lesson is current.**
- **New Outlook does not use an OST at all** — see H1. **If `olk.exe` is running, stop looking.**
- 🔴 **A sent message does NOT prove the owner sent it — Microsoft's own words.** On **Send As**:
  *"Allows the delegate to send messages as if they came directly from the mailbox or group.
  **There's no indication that the message was sent by the delegate.**"* Add AiTM token/cookie theft.
  🟢 **Check `PidTagSentRepresenting*` vs `PidTagSender*` — divergence records a delegate.**
  **Authority is server-side**: Unified Audit Log, sign-in logs, message tracking.
- ⚠️ **Internal mail may carry no internet headers.** `PidTagTransportMessageHeaders` is required
  only *"for outgoing messages with recipients who have an SMTP address type, and for incoming
  messages from a sender who has an SMTP address type"* — **Exchange-to-Exchange mail may have no
  `Received:` chain. Absent headers are the expected state, not evidence of tampering.**

### H8 — Teams moved, and the technique survives

Classic `%APPDATA%\Microsoft\Teams\IndexedDB\*.leveldb` → new path in H1. Three changes:
**Roaming → Local**, into an **MSIX package container** (roaming-profile assumptions break), and
**Electron → WebView2**. 🟢 **Storage tech unchanged — still IndexedDB over LevelDB.**
⚠️ `forensicsim` **v0.8.5 (Jul 2024)** is two years stale and validated only to Teams 2.0 v48 —
**teach the method and validate against data you generated yourself.**

### H9 — Tooling, Aug 2026

| tool | version | note |
|---|---|---|
| **Hindsight** | **v2026.06 (8 Jul 2026)** | 🟢 **now parses Firefox** as well as Chromium |
| **XstReader** | **v1.14 (Jan 2025)** | free, C#, reads `.ost` with **no Outlook installed**; CLI export |
| **libpff / `pffexport`** | alpha, **20231205** | 🟢 **`-m recovered` recovers deleted PST/OST items** |
| **DB Browser for SQLite** | 3.13.0 (Aug 2024) | fine for schemas; **useless for freelist recovery** |
| **Autopsy Recent Activity** | current | parses IE, Edge, Chromium, Firefox, Safari |
| **forensicsim** | v0.8.5 (Jul 2024) | stale — see H8 |
| **BrowsingHistoryView** | 2.62 | NirSoft; broad browser coverage |
| **Eric Zimmerman** | — | ⚠️ **ships NO browser parser.** `SQLECmd` only via a community map — **say this, or students will look for one** |

⚠️ **KAPE target names**: `Targets/**Browsers**/Chrome.tkape` and `EdgeChromium.tkape` — **not
`Targets/Apps/`, and not `Edge.tkape`.** Also `BrowserCache.tkape`.

### H10 — Edge extras, and one to validate

- ➕ **Collections** — `…\Edge\User Data\<profile>\Collections\collectionsSQLite`. **User-curated
  intent** (deliberately saved URLs, images, typed notes) that **survives history clearing**. No
  Chrome equivalent. Worth one slide.
- ⚠️ **`WebCacheV01.dat`** — IE11 is retired; **IE mode is supported "through at least 2029"**, and
  KAPE still collects `…\AppData\Local\Microsoft\Windows\WebCache\`. **But no current source
  confirms it is still meaningfully populated on Windows 11** — the fullest Microsoft reference is
  Windows 8 era. **Validate on our own image before teaching it as live.**

### H11 — Defanging has a citable source

**IETF Internet-Draft `draft-grimminck-safe-ioc-sharing-12`** (Active, last revised 2026-06-10,
intended status Informational): *"Replace 'http' and 'https' schemes with 'hxxp' and 'hxxps'"* ·
*"Replace every period ('.') in domain names and IP addresses with '[.]'"* · *"Replace the '@'
character … with '[@]'"* · *"Using encoded characters (such as %2e for '.') SHOULD be avoided."*
⚠️ **A draft is not an RFC** — cite it as a convention with a source.
🟢 **The rationale is the teaching point** — SANS ISC: clicking a live IOC *"could not only affect
the security of the user/computer but it could also leak data or **pollute statistics**"*: it
**contaminates the telemetry the investigation depends on and can tip off the adversary.**
➕ **Teach refanging as a deliberate, logged step.**

### NOT VERIFIED — block H

- Microsoft-primary documentation for **Edge's default user-data path** (corroborated by KAPE and a
  Microsoft Q&A answer; treat as high-confidence, not primary).
- Microsoft-primary documentation for **classic Outlook's default `.ost`/`.pst` paths** — the
  support article now serves the new-Outlook version; best available is a Microsoft-employee Q&A.
- The **full `downloads.state` integer mapping** — the schema comment is verified, the conversion
  function body is not. **Validate empirically.**
- **`WebCacheV01.dat` currency on Windows 11** — see H10.
- The **Chrome `Cache\Cache_Data` subfolder name** — `Cache` is primary; the subfolder appears only
  in Brave and new-Outlook observations. **Collect `Cache\` recursively.**
- **Firefox download annotation attribute names** (`downloads/destinationFileURI`,
  `downloads/metaData`) — schemas verified, the literal strings are not.
- Whether **Firefox `places.sqlite` uses WAL** by default — not investigated.
- Whether **prefetch/prerender creates `visits` rows** — deliberately not asserted; the redirect,
  subframe and sync arguments in H3/H4 make the same point with full sourcing.
- Whether **SQLECmd ships browser maps** by default.
- A **CISA advisory** with an explicit defanging note — the IETF draft and SANS ISC are stronger
  citations anyway.

---

## I. USB, Explorer search terms and deletion artifacts (appended 2026-08-29, from room 21)

Full citations in `diskfiltration.md` §3.

### I1 — 🔴🔴🔴 `WordWheelQuery` is NO LONGER POPULATED on Windows 11 23H2+

*"in Windows 11 23H2 the WordWheelQuery value is no longer populated"* — searches now run
*"as you type rather than on pressing enter"*, querying the search index directly.
**13cubed Registry Cheat Sheet v2.0 now bounds it: *"Explorer search history (Windows 11 22H2 /
Server 2022 and earlier)."***

🔴 **An empty key on a modern host means nothing** — not "no search", not "cleared".
⚠️ 24H2/25H2 not separately tested; both sources stop at 23H2.
🟢 **Successor: `HKCU\…\Explorer\TypedPaths`** — records searches as `search-ms:` URIs carrying the
term and the target folder, ⚠️ **but only ONE timestamp for the whole key.**
✅ **Back-propagated to `windows-user-activity.md` §2.4.**
🔴 **Lab-build gate: if `FOR-WS01`/`EVI-SRC01` are Win11 23H2+, this artifact cannot be staged.**

### I2 — 🔴 Windows Search index changed format in Windows 11

Vista→Win10: one **ESE** database,
`%PROGRAMDATA%\Microsoft\Search\Data\Applications\Windows\Windows.edb`.
**Windows 11: three SQLite databases — `Windows.db`, `Windows-gather.db`, `Windows-usn.db`.**
🟢 **This is where the search terms went (I1), and it is a new unexploited S5 artifact.**
⚠️ **`ActivitiesCache.db` (Windows Timeline) is deprecated** — *"no longer being actively
maintained, its database remains for now."* Legacy only.

### I3 — USB device identity and the `&` rule

`HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR\<Type>&Ven_&Prod_&Rev_\<instance ID>`.
⚠️ **VID/PID are under `Enum\USB`, not `USBSTOR`**, which is mass-storage only.
Timestamps at `…\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\`: **`0064` first install
(Win7+)** · **`0066` last connected (Win8+)** · **`0067` last removal (Win8+)**.
⚠️ **Sources disagree on the `0064`/`0065` labels — test before labelling a slide.**

**The `&` rule**: *"If the second character of the unique instance ID is a '&', then the ID was
generated by the system, as the device did not have a serial number."*
🔴 **Teach it as an indicator, not a proof.** SANS: *"It turns out this is not exactly correct."*
**Microsoft never documents it** — only that an instance ID contains *"serial number information, if
supported by the underlying bus, or some kind of location information."*
🔴 Same source: *"the USBSTOR key does NOT contain all USB devices that have been attached."*
🟢 Supporting fact: **serial numbers are mandatory for USB mass storage**, optional elsewhere.

**The attribution chain**: `USBSTOR` serial → **`HKLM\SYSTEM\MountedDevices`** (drive letter +
**volume GUID**) → **`HKCU\…\Explorer\MountPoints2`** (**which user**) → ShellBags / LNK.
⚠️ `MountPoints2` is *"supporting evidence, not a definitive device identifier on its own."*
➕ `HKLM\SOFTWARE\Microsoft\Windows Portable Devices\Devices` holds the **volume label**.

### I4 — 🔴 `setupapi.dev.log` timestamps are LOCAL TIME

`C:\Windows\INF\setupapi.dev.log`, ANSI text, sections `>>> [Device Install …]` /
`>>> Section start yyyy/mm/dd hh:mm:ss.sss`. Microsoft: *"The local time is based on a 24-hour
clock."* **Every other artifact in this family is UTC on disk — normalise before correlating.**
⚠️ Records the **first driver install only**, and **rotates** to
`setupapi.dev.<YYYYMMDD-HMMSS>.log` — **collect the whole `INF` directory.**
⚠️ Win11 24H2/25H2 presence not explicitly confirmed — validate on our image.

### I5 — ShellBags: what they do and do not prove

`USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\{BagMRU,Bags}`.
🟢 **Proves** the full path to a folder *"even if the folder is deleted or the drive is no longer
connected"*, with per-user attribution — **the only artifact that recovers a disconnected USB's
folder structure.**
🔴 **Does NOT prove**: *"parent folders are logged even without direct access"* ·
*"denied access attempts still create entries without view preferences"* ·
*"only folders are recorded"* — **a ShellBag never shows a file was opened.**
🟢 **Applied view preferences discriminate traversal from real use.**
🟢 **Join on the volume GUID (I3) to prove the ShellBag belongs to *this* device.**

### I6 — `$Recycle.Bin` `$I` format, v1 vs v2

`C:\$Recycle.Bin\<SID>\` — one subdirectory per user **named by SID** (the attribution);
`$I<random>` metadata, `$R<random>` content.

| offset | v2 (Win10/11) | v1 (Vista–8.1) |
|---|---|---|
| 0 | version `02` | version `01` |
| 8 | file size | file size |
| 16 | **deletion FILETIME** | **deletion FILETIME** |
| 24 | **4-byte path length** | 520-byte fixed path field |
| 28 | path, UTF-16LE | — (total 544 bytes) |

⚠️ **NOT VERIFIED: whether the v2 length field counts bytes or UTF-16 characters** — sources
conflict and the canonical references are offline. **Test it.**
🔴 **A Shift+Delete never touches the Recycle Bin** — no `$I` at all.
Tool: **`RBCmd` 2026.5.0**.

### I7 — `$UsnJrnl` deletion signature (Microsoft reason flags)

`USN_REASON_FILE_DELETE` **0x00000200** · `RENAME_OLD_NAME` **0x00001000** ·
`RENAME_NEW_NAME` **0x00002000** · `CLOSE` **0x80000000**.
Microsoft: a rename generates **two** records, *"and when a file or directory closes, a final USN
record is generated with the `USN_REASON_CLOSE` flag set."*
🟢 **Recycle-then-empty reads as a SEQUENCE**: rename pair into `$Recycle.Bin` → `FILE_DELETE`+
`CLOSE`. **It survives the emptying and distinguishes a recycle from a Shift+Delete.**

### I8 — PDF author lives in two places, and they can disagree

DocInfo **`/Author`** ↔ XMP **`dc:creator`**. PDF/A requires them to match *"on a
character-by-character basis"* where both exist — **but nothing states which wins on conflict.**
🟢 **A mismatch indicates editing by a writer unaware of the XMP stream — report both values and the
discrepancy; never silently pick one.** Tool: **ExifTool 13.59 (27 May 2026)**.

### I9 — File-type identification: no single authoritative tool

A 2023 peer-reviewed comparison of ten tools found *"significant disparity in accuracy and
behavior"*. Fidentify 94.4–98.1%, *"robust to a modification of file extensions"*; `file`
*"clearly the quickest solution with good performance"*; TrID has the largest signature database.
🟢 **The asymmetry is the lesson**: extension spoofing is *"a very convenient and easy way"* to
hide something; header spoofing *"alters the internal structure of the file and makes it not
readable anymore."* **Layer signature + hash + metadata + entropy.**

### I10 — ⚠️ EZ Tools GUI are .NET 9 ONLY — a lab-build requirement

ShellBags Explorer **2026.5.0** · `SBECmd` **2026.5.0** · `RBCmd` **2026.5.0**.
*"All GUI tools are updated to use .net 9 only. Legacy net4 versions are no longer available."*
🔴 **The `CLEAN-TOOLS` snapshot (D17) must include .NET 9.** CLI tools still ship both runtimes.

### I11 — ATT&CK: parents cited where sub-techniques exist

**T1078.003** Valid Accounts: Local Accounts · **T1560.001** Archive Collected Data: Archive via
Utility · **T1048.003** Exfiltration Over Unencrypted Non-C2 Protocol (the right one for an HTTP
upload tool). ✅ T1083, T1070.004, T1059.001 verified correct.
🔴 **TA0005 is "Stealth"** (v19, last modified 2026-05-12) — **third room to print "Defense
Evasion"**; ✅ repo already grepped clean, but do not copy a room's ATT&CK table verbatim.

### NOT VERIFIED — block I

- The `0064`/`0065` DEVPKEY label mapping (13cubed and ElcomSoft disagree; no Microsoft page prints
  the GUID/PID pair).
- `WordWheelQuery` on Windows 11 **24H2/25H2** specifically.
- `setupapi.dev.log` population on Win11 24H2/25H2.
- Whether the `$I` v2 length field counts **bytes or characters**.
- `$LogFile` deletion signatures (only `$UsnJrnl` was researched this pass).
- **WLAN profile / `NetworkList` key layout and value semantics** — needed for the hotspot artifact
  (`diskfiltration.md` §2.8) and **not researched. Do before teaching.**
- Forensic interpretation of `FriendlyName` / `ContainerID` under `USBSTOR`.
- Current poppler / `pdfinfo` version.

---

## J. Linux endpoint artifacts (appended 2026-08-29, from room 22 — ExfilNode)

🔴 **Scope note first: Linux forensics is OUT of scope per `scope_decisions.md`, reaffirmed as
D38.** This block exists for two reasons only — the **S1 cross-platform contrast table (D38, figure
F1)**, and so that an instructor who is asked a Linux question in class does not answer from 2019
knowledge. **Do not build a lab from this block.**

### J1 — 🔴🔴 `/var/log/auth.log` is conditional, not universal

**Ubuntu Server still has it, through 26.04 LTS.** rsyslog `8.2512.0-1ubuntu4.1` is present in the
26.04 cloud and live-server manifests, and `50-default.conf` still routes
`auth,authpriv.* → /var/log/auth.log`. **Debian dropped rsyslog from the default install at Debian
12**, not 13: *"From bookworm, `rsyslog` is no longer installed by default."* So Debian 12/13 have
**no `auth.log`, no `syslog`, no `kern.log`** — journal only. ⚠️ Ubuntu **Desktop** 26.04's manifest
carries no rsyslog line either (moderate confidence; verify on a real image).
**Teach the triage check, not the path.**
Sources: <https://www.debian.org/releases/bookworm/amd64/release-notes/ch-information.en.html> ·
<https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest>

### J2 — 🔴🔴🔴 `last` / `wtmp` / `btmp` / `lastlog` are GONE on Debian 13 and Ubuntu 25.04+

The largest Linux finding in the project, and the exact counterpart of **I1** (`WordWheelQuery`).
Debian 13 release notes: *"The **util-linux** package no longer provides the `last` or `lastb`
commands, and the **login** package no longer provides `lastlog`… these files will not be usable
after 2038 because they do not allocate enough space to store the login time… and the upstream
developers do not want to change the file formats."*

- Ubuntu 26.04: **no package provides `/usr/bin/lastlog`**; **no package ships `/var/log/wtmp` or
  `/var/log/btmp`**; systemd is built **without utmp** (*"In Ubuntu, systemd is no longer built with
  utmp support"*), so `/run/utmp` is never created and **`who` and `w` return nothing.**
- Successors are **SQLite** and **not installed by default**: `wtmpdb` → `/var/log/wtmp.db`
  (upstream `/var/lib/wtmpdb/wtmp.db`); `lastlog2` → `/var/lib/lastlog/lastlog2.db`.
- ⚠️ **Your analysis workstation may no longer ship a `last` binary either.** Bring a parser.
- 🟢 The survivor in util-linux is **`lslogins`** (`--failed` replaces `lastb`).

**The generalisable lesson, and the reason this belongs in S1:** *an artifact can be deleted by a
decision that has nothing to do with forensics.* Here it was **Y2038**.
Sources: <https://www.debian.org/releases/stable/release-notes/issues.html> ·
<https://documentation.ubuntu.com/release-notes/25.04/> ·
<https://manpages.debian.org/unstable/wtmpdb/wtmpdb.8.en.html>

### J3 — 🔴🔴 Journal retention is SIZE-driven, not time-driven

`journald.conf(5)`: `SystemMaxUse=` defaults to **10 % of the filesystem, capped at 4 G**;
**`MaxRetentionSec=`** has *"the default of 0 (which turns off this feature)"*. **There is no
defensible "the logs go back N days."** Bound every negative claim to the observed first and last
journal timestamps. ⚠️ If `/var/log/journal/` does not exist the journal was **volatile** and did not
survive the last reboot — **NOT VERIFIED** whether it exists on a stock Debian 13 / Ubuntu 26.04
image; one command on the image settles it.
Source: <https://man7.org/linux/man-pages/man5/journald.conf.5.html>

### J4 — 🔴🔴 `/etc/timezone` is gone; `/etc/localtime` is authoritative

Debian `tzdata`: `2022g-3` *"Stop creating /etc/timezone"* → `2024b-5` **"Only create /etc/timezone
if it already exists"**, removal scheduled for *"Debian 13 'Trixie'"*. Ubuntu 26.04's `tzdata`
ships **no files under `/etc`**. `/etc/localtime` is a **symlink** into `/usr/share/zoneinfo/`, is
what `timedatectl` reads and writes, and *"If /etc/localtime is missing, the default 'UTC' timezone
is used."*
🟢🟢 **Journal records carry no timezone at all** — µs since the Unix epoch — so **`journalctl --utc`
is mandatory** or the timeline is silently wrong by the *analyst's* offset. **Compare I4**, where
`setupapi.dev.log` was local while everything around it was UTC: same class of error, opposite
direction.
Sources: <http://metadata.ftp-master.debian.org/changelogs/main/t/tzdata/stable_changelog> ·
<https://man7.org/linux/man-pages/man5/localtime.5.html> · <https://systemd.io/JOURNAL_FILE_FORMAT/>

### J5 — 🔴🔴 `.bash_history` has no timestamps and is silently lossy BY DEFAULT

- **`HISTCONTROL=ignoreboth` is Ubuntu's default** in `/etc/skel/.bashrc`. Bash manual: *"lines
  which begin with a space character are not saved in the history list."* **One leading space
  suppresses a command with no gap, no marker and no count anomaly.**
- **`HISTTIMEFORMAT` is not set by default** (an open Launchpad request to add it is the proof), so
  the file is **ordered, not dated**.
- *"When a shell with history enabled exits, the last $HISTSIZE lines are copied…"* — **writes
  happen on clean exit**, not per command. Without `histappend` the last shell to exit **overwrites**
  the file.
- 🟢 **The asymmetry worth teaching:** a *cleared* history is itself an anomaly; `ignorespace`
  produces a file that looks entirely normal. **The sloppy anti-forensic is visible; the default one
  is not.**
Sources: <https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html> ·
<https://bugs.launchpad.net/ubuntu/+source/bash/+bug/2039508>

### J6 — 🔴 ext4 crtime: `stat` shows it, 128-byte inodes do not have it, and it CAN be forged

- **The "you need `debugfs` because `stat` cannot show crtime" premise is stale by seven years.**
  `statx()` (Linux 4.11+) exposes `STATX_BTIME`; coreutils **8.31** (2019): *"stat now prints file
  creation time when supported by the file system."* Current coreutils **9.11 (Apr 2026)**, `%w`/`%W`.
  🟢 TSK `istat` shows **`File Created:`**; Autopsy exposes a **Created Time** column.
- `debugfs -R 'stat <131074>' /dev/…` — **angle brackets required** for the inode-number form;
  **read-only by default** without `-w`. Pomeranz's decoding rule: the low two bits of the `_extra`
  field are **not** nanoseconds — divide by 4.
- 🔴 **`i_crtime` is at inode offset `0x90`**, past the end of a **128-byte inode**, so such a
  filesystem has neither crtime nor sub-second precision. `mke2fs` defaults to **256 bytes** today.
- 🔴🔴 **crtime and ctime are forgeable.** Pomeranz: *"I was frustrated after reading yet another
  person claiming (incorrectly) that you cannot set `ctime` and `btime` in Linux file systems."*
  `debugfs -w` + `set_inode_field`, **even on a mounted filesystem.**
- `touch` **cannot** set ctime — `utimensat(2)` has no ctime parameter and *"The status change time
  (ctime) will be set to the current time, even if the other time stamps don't actually change."*
- 🔴 **The "inode number ordering vs timestamps" heuristic is NOT VERIFIED and was dropped** — no
  citation found, and ext4's Orlov/flex_bg allocator makes the premise doubtful.
- **Report phrasing:** *"inconsistent with normal filesystem behaviour"*, **never** *"proof of
  tampering"* — a D20 criterion-4 rule arriving as a technical fact.
Sources: <https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html> ·
<https://man7.org/linux/man-pages/man1/stat.1.html> ·
<https://righteousit.com/2024/09/04/more-on-ext4-timestamps-and-timestomping/>

### J7 — 🔴🔴 Linux has NO `USBSTOR` equivalent

USB attach/detach evidence exists **only in the kernel log**, which rotates by size (J3).
`announce_device()` in `drivers/usb/core/hub.c` emits `idVendor=`/`idProduct=`, then a
*"New USB device strings: … SerialNumber=N"* line **whose values are string-descriptor indices, not
the serial**, then the separate **`SerialNumber: <value>`** line — which is **absent entirely** when
the device has no serial descriptor (`show_string()` returns early on NULL). **Windows fabricates an
instance ID and flags it with the `&` convention (I3); Linux is simply silent.**
🔴 `usb_disconnect()` logs only `USB disconnect, device number %d` — **no serial, no VID/PID** — so
connect/disconnect must be correlated on the `usb N-M:` bus/port prefix, which can be ambiguous
across a reboot.
**Persistent vs volatile on a dead image:** `/sys` **volatile** · `/run/udev` **volatile** (tmpfs) ·
`lsusb` live-only · `/etc/udev/rules.d` persistent but holds **rules, not history** ·
`/var/log/journal/` **persistent, size-rotated** · `kern.log`/`syslog` persistent **only where
rsyslog exists**. ⚠️ `/var/lib/systemd/` is **NOT** a USB artifact — do not teach it as one.
Source: <https://raw.githubusercontent.com/torvalds/linux/master/drivers/usb/core/hub.c>

### J8 — 🔴🔴 `journalctl _COMM=sshd` now UNDER-COLLECTS

OpenSSH **9.8** (1 Jul 2024) split the daemon — *"some log messages will be tagged with as
originating from a process named "sshd-session" rather than "sshd"."* **10.0** split again, moving
*"the user authentication phase… to a new sshd-auth binary."* The `Accepted …` line comes from
`auth_log()`, i.e. from **`sshd-auth`** on ≥10.0. Ubuntu 26.04 ships **10.2**; current upstream is
**10.5 (11 Aug 2026)**.
✅ **The line format is unchanged** — `Accepted %s for %s from %s port %d ssh2` — and carries three
fields worth teaching: the **`invalid user ` prefix** for nonexistent accounts, the
`method/submethod` pair, and **the key fingerprint** appended on publickey accepts.
⚠️ `SyslogFacility` default is **AUTH (4)**, so `SYSLOG_FACILITY=10` (authpriv) catches sudo/PAM but
**misses sshd**. 🟢 Plain `grep` of `auth.log` is unaffected; only journald filters break.
Sources: <https://www.openssh.com/txt/release-9.8> ·
<https://raw.githubusercontent.com/openssh/openssh-portable/master/auth.c>

### J9 — cron, systemd timers, and Autopsy's Linux blind spot

- **`/var/spool/cron/crontabs/<user>`** on Debian/Ubuntu vs **`/var/spool/cron/<user>`** on
  RHEL/Fedora. 🔴 **`/etc/crontab` and `/etc/cron.d/*` carry a `user` field; user crontabs do not** —
  six fields plus command vs five. **Miscounting reads the username as part of the schedule.**
- A crontab entry is **configuration, not execution**. Execution is a separate log line —
  `CRON[12345]: (root) CMD (…)`, default `-L 1` *"log the start of all cron jobs"* — which on a
  journald-only host is in the binary journal and may have rotated away.
- `journalctl **-u** cron`, **not** `_COMM=cron`: `-u` also captures the output of jobs in the unit's
  cgroup. ⚠️ Unit is `cron.service` on Debian/Ubuntu, **`crond.service`** on RHEL.
- ⚠️ **systemd timers have not replaced cron; they run alongside it** and are equally usable for
  persistence: `/etc/systemd/system/*.timer` (*"System units created by the administrator"*),
  `/run/systemd/system`, `/usr/lib/systemd/system`, `~/.config/systemd/user/`. **A `.timer` needs its
  `.service` — collect both.** 🔴 **An examiner who greps only cron misses the class.**
- Rest of the sweep: `~/.bashrc`/`~/.profile`/`/etc/profile.d/` (**T1546.004**), `/etc/rc.local`
  (still functional via `systemd-rc-local-generator`, which itself says *"strongly recommended to
  avoid"*), `/etc/init.d/`, `/etc/update-motd.d/`, `/var/spool/cron/atjobs`, `~/.config/autostart/`.
- 🔴 **Autopsy has NO ingest module for bash history, crontabs or `auth.log`.** 4.23.0's headline
  parsers (*"Prefetch, SRU, Thumbcache, Regripper"*) are all Windows. **The workaround is the Plaso
  ingest module**, which ships `bash_history`, `zsh_extended_history`, `syslog`, `utmp`, `dpkg.log`
  and `selinux` parsers — **but no cron parser.** Autopsy gives you the filesystem, the timestamps
  and the timeline; **Linux persistence analysis is done by hand.**
- ⚠️ The room ships **Autopsy 4.21.0 (29 Aug 2023)** — three years old to the day at extraction.
  Current **4.23.1 (7 May 2026)**.
Sources: <https://manpages.debian.org/stable/cron/crontab.1.en.html> ·
<https://man7.org/linux/man-pages/man5/systemd.unit.5.html> ·
<https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html>

### J10 — ATT&CK deltas found this pass (extends E11, I11)

Enterprise **v19.2, released 6 Aug 2026** (major v19: 28 Apr 2026).

- 🔴 **T1552.003 renamed "Bash History" → *Shell History*** (v2.0, 24 Oct 2025). ✅ Repo grepped —
  the old name appears **nowhere**, so this is forward-looking only.
- 🔴 **T1070.006 Timestomp and T1564.001 Hidden Files and Directories are both under tactic
  *Stealth*** (both v2.0, 12 May 2026) — consistent with the TA0005 → TA0112 split in **E11**.
  ✅ `fat32-analysis.md` already carries the correction.
- 🔴 **`scp` is encrypted → T1048.002 (Asymmetric Encrypted), NOT T1048.003.** `.003` is
  *Unencrypted Non-C2* and covers plain-HTTP/FTP `curl`/`wget` only. **Do not group scp with them.**
  ✅ Both existing repo uses of `.003` are cleartext HTTP and remain correct.
- ✅ Confirmed: **T1052.001** Exfiltration over USB (Exfiltration; Linux/Windows/macOS — **no
  ESXi**) · **T1053.003** Cron (Execution, Persistence, Privilege Escalation) · **T1021.004** SSH
  (**ESXi, Linux, macOS — still no Windows**) · **T1546.004** Unix Shell Configuration Modification.

### NOT VERIFIED — block J

- Which file supplies room 22's Q7 answer (`/etc/hosts` vs `known_hosts` vs `~/.ssh/config`).
- Whether `/var/log/journal/` exists on a stock Debian 13 / Ubuntu 26.04 image (compile-time default).
- Exact `HISTSIZE` / `HISTFILESIZE` in Ubuntu's `/etc/skel/.bashrc`.
- Octal permissions of `/var/spool/cron/crontabs` (man page states the model in prose only).
- Current-kernel format string for the `new high-speed USB device number N using xhci_hcd` line —
  function and file confirmed, wording not retrieved. **Do not quote it.**
- A Fedora change proposal retiring utmp/wtmp — only the **F43 *Migrate to lastlog2*** change is
  confirmed. **Do not cite a Fedora utmp release number.**
- Whether Ubuntu **Desktop** 26.04 truly lacks rsyslog (manifest suggests yes; verify on a real image).
- Which systemd unit per-connection sshd records land under with socket activation (affects whether
  `journalctl -u ssh` is complete).
- The SANS *Breaking Time* paper body (robots-blocked) — reading-list item only.
- The "inode number ordering vs timestamps" timestomp heuristic — **dropped, not merely unverified.**

---

## K. Web-facing Linux host, auditd, bootloader access and a MAJOR ATT&CK revocation (appended 2026-08-29, from room 23 — Initial Access Pot)

🔴 **Scope note: the Linux-specific items here are out of scope per D38** and exist for the S1
contrast table (figure F1) and for instructor answers. **K6, K7 and K8 are IN scope and repo-wide.**

### K1 — 🔴🔴 READ THIS FIRST: T1562 was REVOKED, and log-clearing moved out of T1070

**Bigger than the E11 Stealth rename, because this is a revocation, not a rename.** ATT&CK **v19,
28 Apr 2026** release notes list under revocations:

> *"Impair Defenses (revoked by Disable or Modify Tools)"* · *"Indicator Blocking (revoked by Disable
> or Modify Tools)"* · *"Spoof Security Alerting (revoked by Disable or Modify Tools: Modify or Spoof
> Tool UI)"*

**The successor is `T1685` "Disable or Modify Tools", tactic Defense Impairment (TA0112), v1.0,
12 May 2026**, with six sub-techniques:

| new ID | name | was |
|---|---|---|
| T1685.001 | Disable or Modify Windows Event Log | T1562.002-ish |
| T1685.002 | Disable or Modify Cloud Log | T1562.008 |
| T1685.003 | Modify or Spoof Tool UI | T1562.009 / Spoof Security Alerting |
| **T1685.004** | **Disable or Modify Linux Audit System Log** | **T1562.012** |
| **T1685.005** | **Clear Windows Event Logs** | **T1070.001** |
| **T1685.006** | **Clear Linux or Mac System Logs** | **T1070.002** |

🔴🔴 **So `T1070.001` is no longer the ID for clearing Windows event logs — it is `T1685.005`.**
Independently confirmed by fetching the parent: **`T1070` "Indicator Removal" is live at v3.0
(12 May 2026), tactic Stealth**, and its sub-technique list is now
`.003 .004 .005 .006 .007 .008 .009 .010` — **`.001` and `.002` are absent.**

✅ **Repo checked, not assumed: `T1562` appears nowhere, and we cite only `T1070.004`, `.006` and
`.009`, all still live under T1070. Zero back-propagation.**
🔴 **But `S6-06` (Windows event logs) must use `T1685.005` when it is written.** This block is the
reminder.

Two smaller deltas from the same restructure: **`T1548.001`, `T1548.003` and `T1505.003` are now
single-tactic** — Privilege Escalation, Privilege Escalation, Persistence respectively. A dual
Defense-Evasion mapping for any of them is stale.
✅ Unchanged: **T1190** (Initial Access) · **T1110.001 Password Guessing** — the right sub-technique
for a web login form, **not `.004` Credential Stuffing** unless reused *pairs* were sprayed (and per
**K3** the access log cannot tell you) · **T1046** (Discovery) · **T1053.003** (Execution,
Persistence, Privilege Escalation) · **T1546.004** Unix Shell Configuration Modification.
Sources: <https://attack.mitre.org/resources/updates/updates-april-2026/> ·
<https://attack.mitre.org/techniques/T1685/> · <https://attack.mitre.org/techniques/T1070/>

### K2 — 🔴🔴 auditd is NOT installed by default on Ubuntu

The 24.04.3 and 26.04.1 **live-server manifests** contain only `libaudit-common` and `libaudit1` —
the shared library PAM and systemd link against, which **loads no rules**. **The `auditd` package is
absent, so a stock Ubuntu Server has no `/var/log/audit/` at all.** It is realistic only on a
CIS/STIG-hardened host or one running an EDR that ships rules.

- Paths: `auditd.conf(5)` — *"The default path is /var/log/audit/audit.log if not explicitly set"*;
  rules in `/etc/audit/rules.d/*.rules`, compiled by `augenrules` into `/etc/audit/audit.rules`.
  🟢 **A mismatch between `rules.d/` and the compiled file is an anti-forensic tell.**
- 🟢🟢 **`auid` is why auditd matters.** Red Hat: it *"records the Audit user ID, that is the
  loginuid… **is inherited by every process even when the user's identity changes**, for example, by
  switching user accounts with the `su - john` command."* **`auid=1000 uid=0` = "user 1000 escalated
  and is now root."** No other default artifact gives that.
- Timestamps: `msg=audit(EPOCH.mmm:SERIAL)` — *"the Unix time format - seconds since 00:00:00 UTC on
  1 January 1970"*, **UTC**; the serial stitches multi-record events. `a0`–`a3` are the first four
  syscall args *"encoded in hexadecimal notation"*.
- 🔴 **Retention:** upstream ships `max_log_file = 8` (MiB), `num_logs = 5`,
  `max_log_file_action = ROTATE` → **~40 MiB ceiling**, hours on a noisy host.
  `disk_full_action = SUSPEND` **stops writing while the box keeps running** — fill the disk, create
  a silent gap. ⚠️ The Debian/Ubuntu-patched `auditd.conf` is **NOT VERIFIED**; read it off the box.
- 🔴🔴 **It does not survive root.** `auditctl -e 0` … act … `-e 1` leaves **no marker**; `-D` deletes
  all rules. **Only `-e 2` changes the answer:** *"Any attempt to change the configuration in this
  mode will be audited and denied. The configuration can only be changed by rebooting the machine."*
  **Check `auditctl -s` before trusting an audit log**, and under `-e 2` treat an **unexplained
  reboot** as a first-class indicator.
- Queries: `ausearch -k <key> -i` · `-ts`/`-te` (accept `boot`, `today`, `yesterday`, `checkpoint`) ·
  **`-ul <auid>`** for the attribution pivot · `aureport -k|-au|-x|--summary`.
- 🟢 Even with no auditd, `journald.conf`'s `Audit=` *"Defaults to yes in the default journal
  namespace"*, so `journalctl _TRANSPORT=audit` has the always-on record types — **but not syscall or
  file-watch records.**
Sources: <https://manpages.debian.org/testing/auditd/auditd.conf.5.en.html> ·
<https://manpages.debian.org/testing/auditd/auditctl.8.en.html> ·
<https://raw.githubusercontent.com/linux-audit/audit-userspace/master/init.d/auditd.conf> ·
<https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest>

### K3 — 🔴🔴 Apache/nginx access logs hold no credentials, and request count ≠ attempt count

**In scope — this extends G9/G10 (IIS) to the other two servers.**

- Apache default `combined`: `%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"`.
  nginx `combined`: `$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent
  "$http_referer" "$http_user_agent"`.
- 🔴🔴 **`%u` / `$remote_user` is the HTTP-auth user only** — *"If the document is not password
  protected, this part will be `-`"*. An application login (WordPress, any form POST) never sets it,
  **so the log records no username.**
- 🔴🔴 **Neither logs the request body by default.** Apache's `mod_log_config` defines no format
  string for it; nginx's `$request_length` is a **byte count**. **No credentials, ever.**
- 🟢 Both log **Referer and User-Agent** by default — same as IIS (**G9**) — and both are
  attacker-controlled strings.
- 🔴 **Rotation, not the attack, bounds the visible window.** ⚠️ Ubuntu's logrotate policy for both,
  and the literal `/var/log/apache2` and `/var/log/nginx` paths, are **NOT VERIFIED** from primary
  docs (the mechanism is `${APACHE_LOG_DIR}` via `/etc/apache2/envvars`). **Read both off the
  evidence — which is better practice anyway.**
Sources: <https://httpd.apache.org/docs/2.4/logs.html> ·
<https://httpd.apache.org/docs/2.4/mod/mod_log_config.html> ·
<https://nginx.org/en/docs/http/ngx_http_log_module.html>

### K4 — 🟢🟢 WordPress: 200 on failed login, 302 on success

**The single most useful investigative technique found this pass.** From core `wp-login.php`:
success calls `wp_safe_redirect( $redirect_to ); exit;`, and `wp_safe_redirect()`'s signature is
`( string $location, int $status = 302, … )` — **default 302**. Failure sets `$errors` and falls
through to re-render the form, and **`status_header()` appears nowhere in the file** → **200**.

> **A run of `POST /wp-login.php → 200` is failures. The first `POST → 302` is the successful
> credential, and its timestamp is the compromise time.** Corroborate with `GET /wp-admin/ → 200`
> from the same address seconds later.

⚠️ Two limits: a plugin or `login_redirect` filter can change the destination (**still a 30x, not a
200**), and a security plugin or WAF may answer 403/429 — **if the pattern is absent, look for a
plugin before concluding nothing happened.**

- 🔴 **WordPress logs logins nowhere by default.** Core fires `wp_login_failed` *"after a user login
  has failed"* with the username; **if nothing subscribes, nothing is written** — no table, no file.
- 🔴🔴 **`xmlrpc.php` destroys request-counting.** `system.multicall` loops an array of `methodCall`s
  inside **one** POST; WordPress's own doc calls it *"a frequent brute-force target (especially the
  `system.multicall` method)"*. **Twelve log lines can be thousands of guesses.** XML-RPC is still
  **enabled by default** (`xmlrpc_enabled` — *"Default true"*). Against `wp-login.php`, one POST ≈
  one attempt, so counting *is* valid there — **the validity depends on which page was hit.**
- 🔴 **`wp-content/uploads/` must be web-server-writable** in every install (WordPress hardening:
  `/wp-content/` is *"intended to be writable by … the web server process"* while `plugins/` *"should
  be writable only by your user account"*), and **the hardening doc does not address blocking PHP
  execution there** — so **an uploaded `.php` in `uploads/` executes on a stock install.**
- Current WordPress: **7.1 "Mary Lou", 19 Aug 2026**.
Sources: <https://raw.githubusercontent.com/WordPress/WordPress/master/wp-login.php> ·
<https://developer.wordpress.org/reference/functions/wp_safe_redirect/> ·
<https://developer.wordpress.org/advanced-administration/security/brute-force/> ·
<https://developer.wordpress.org/advanced-administration/security/hardening/>

### K5 — Linux privesc: state vs event, and the mechanism `ls -l` cannot show

🟢🟢 **The generalisable idea is in scope even though the commands are not** — it is the same lesson
as `S5-06`'s *presence vs execution*.

**Only `sudo` produces a persistent timestamped record of an event.** SUID/SGID, capabilities, a
writable unit and a PATH hijack are **configuration state** — they show the opportunity existed when
you looked, not that anyone took it.

- `sudoers(5)`: logging *"default is to log to syslog(3)"*, facility *"Defaults to authpriv"*,
  success priority *"Defaults to notice"*; format
  `username : TTY=… ; PWD=… ; USER=… ; GROUP=… ; TSID=… ; COMMAND=…`.
  🔴 **But `sudo /bin/bash` logs one line and everything in that shell is invisible** — which is
  exactly the gap `auid` (K2) fills.
- ⚠️ **`find / -perm -4000`, not `4000`** — `find(1)`: `-perm -mode` means *"All of the permission
  bits mode are set"*; bare `4000` means *exactly* those bits.
- 🔴🔴 **File capabilities are invisible to `ls -l`.** `capabilities(7)`: the sets are *"stored in an
  extended attribute … named `security.capability`"*. An xattr is **not a mode bit**, so no character
  in the permission string can represent it — a `cap_setuid+ep` binary looks exactly like
  `-rwxr-xr-x root root`. **`getcap -r /` is a separate mandatory step.**
- 🟢 Free detection rule from `cron(8)`: *"/etc/crontab and the files in /etc/cron.d must be owned by
  root, and must not be group- or other-writable"* — a group-writable file there is **both the
  vulnerability and the flag**.
- ⚠️ Octal modes of the crontab spool: still **NOT VERIFIED** (carried from block J).
Sources: <https://www.sudo.ws/docs/man/sudoers.man/> ·
<https://man7.org/linux/man-pages/man7/capabilities.7.html> ·
<https://man7.org/linux/man-pages/man1/find.1.html>

### K6 — 🔴🔴 Console access with unprotected GRUB is equivalent to root (IN SCOPE)

**Platform-neutral, and the best justification for write blocking we have found.** GNU GRUB manual:
*"anyone can select and edit any menu entry, and anyone can get direct access to a GRUB shell
prompt."* **No password by default**; `superusers` + `password_pbkdf2` are opt-in (and `password`
stores plaintext in `grub.cfg`).

`bootparam(7)`: `init=` *"sets the initial command to be executed by the kernel"* — so appending
**`init=/bin/bash rw`** gives a **root shell as PID 1, before any userspace security control
initialises**: no PAM, no `auth.log`, no `auid`, no auditd rules, no AppArmor. **Nothing records it.**

🔴 GRUB's own rationale — *"physical console access already implies other security vulnerabilities"* —
**fails silently on a VM or in cloud**, where "console" is the hypervisor's and there is no physical
barrier at all.

**The encryption nuance students get backwards:** FDE with a **boot-time passphrase** defeats this
(the root filesystem is ciphertext; there is nothing to mount). FDE that **auto-unlocks** — TPM-sealed
with no PIN, a keyfile in an unencrypted `/boot`, provider-managed cloud keys — **does not**: booting
to a shell unlocks the disk for the attacker exactly as for the owner. **A GRUB password is not a
substitute for FDE, and FDE is not automatically a substitute for a GRUB password.**

🔴🔴 **Handling rule, and it is the ninth safety defect in the corpus:** this is also how an *examiner*
gets a shell on a box whose credentials are unknown — **and it destroys all volatile evidence, mounts
and modifies the disk, and leaves no record distinguishing the examiner's boot from the attacker's.**
**For acquisition, boot external read-only media and image the disk. Never `init=/bin/bash` a machine
you intend to treat as evidence.**
⚠️ **NOT VERIFIED:** whether Ubuntu's `friendly-recovery` passes `sulogin --force` (which would give a
passwordless root shell, since Ubuntu locks root). Mechanism documented in `sulogin(8)`; invocation
not. **Teach the `init=/bin/bash` route, which is fully verified.**
Sources: <https://www.gnu.org/software/grub/manual/grub/html_node/Authentication-and-authorisation.html> ·
<https://man7.org/linux/man-pages/man7/bootparam.7.html> ·
<https://man7.org/linux/man-pages/man8/sulogin.8.html>

### K7 — 🟢🟢 MD5: lookup yes, integrity no — and NIST does both (IN SCOPE, `S1-06`)

CERT/CC **VU#836068**, *"MD5 vulnerable to collision attacks"*: *"Weaknesses in the MD5 algorithm
allow for collisions in output. As a result, attackers can generate cryptographic tokens or other
data that illegitimately appear to be authentic."* **The break is in collision resistance;
preimage resistance is not practically broken — which is exactly why lookup still works.**

🟢🟢 **The teaching card:** NIST's own **NSRL** ships *"Cryptographic hash values (MD5 and SHA-1) of
the file's content"* that *"uniquely identify the file even if, for example, it has been renamed"*,
used *"to eliminate known files … during criminal forensic investigations"*. VirusTotal's file-report
`id` is documented as *"SHA-256, SHA-1 or MD5 identifying the file"*. **The same agency publishes MD5
hash sets for forensics and excludes MD5 from approved cryptography, because they are different
problems.**

> **MD5 answers "have we seen this exact file before?" It does not answer "is this file unaltered?"
> Use it to look things up; never to prove integrity — and never as the hash you attest to in a
> report or on a chain-of-custody form.**

**Acceptable:** VirusTotal/NSRL/IOC lookups, dedup, matching an IOC list that publishes only MD5, a
secondary hash beside a strong one. **Not acceptable:** the acquisition hash (use SHA-256), verifying
a download, anything where an adversary influences the content.
**Drill the habit: record SHA-256 *and* MD5 for every artifact.**
⚠️ **NOT VERIFIED:** a NIST-authored sentence naming MD5 (FIPS 180-4 §1) — not read. CERT/CC carries
the break; NSRL carries the lookup.
Sources: <https://www.kb.cert.org/vuls/id/836068> ·
<https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl/about-nsrl/nsrl> ·
<https://docs.virustotal.com/reference/file-info>

### K8 — 🟢 Cross-reference: `T1070.003 Clear Command History`

Live under T1070 (v3.0, Stealth). **This is the ID for `history -c` / `unset HISTFILE` / symlinking
`~/.bash_history` to `/dev/null`**, discussed in **J5** without an ID attached. Recorded here so the
mapping exists when the material is written.

### NOT VERIFIED — block K

- Ubuntu **logrotate** policy for Apache and nginx; the literal `/var/log/apache2` and
  `/var/log/nginx` paths from a primary doc.
- The **Debian/Ubuntu-patched `auditd.conf`** (upstream values given).
- A direct *"ROTATE deletes old logs"* sentence — established by contrast with `keep_logs`, whose
  documented purpose is *"This prevents audit logs from being overwritten."* Flagged as inference.
- Whether Ubuntu's **`friendly-recovery` passes `sulogin --force`**.
- A **NIST-authored sentence naming MD5** (FIPS 180-4 §1).
- Octal permissions of `/var/spool/cron/crontabs` (carried from block J).

---

## L. Windows execution, credential and ATT&CK corrections (appended 2026-08-29, from room 24 — Elevating Movement)

🟢 **All of block L is IN SCOPE.** Room 24 is the first fully in-scope room of the Honeynet Collapse
module.

### L1 — 🔴🔴🔴 Command-line evidence: TWO switches, both off by default

Microsoft, verbatim, on the same page:
- *Audit Process Creation* — **"Default: Not configured"**
- *Include command line in process creation events* — **"Default setting: Not Configured (not
  enabled)"**, and *"If you disable or don't configure this policy setting, the process's command
  line information won't be included in Audit Process Creation events."*
- GPO path: `Administrative Templates\System\Audit Process Creation`.

**So on a stock host there is no 4688 at all, and where 4688 exists the arguments are absent.**
⚠️ The **registry value name** behind the policy is **NOT VERIFIED** — the page gives the GPO path
only. **Use the policy name in student-facing material, never an unverified registry path.**

**Where a command line CAN come from, ranked by default availability:**

| source | full command line? | default? |
|---|---|---|
| Security **4688** | only with the extra policy | 🔴 **no — neither switch** |
| **Sysmon 1** | 🟢 yes | 🔴 not installed by default |
| **PowerShell 4104** | 🟢 if PowerShell was the vehicle | 🟢 partially — three states (**G1**) |
| **PSReadLine `ConsoleHost_history.txt`** | 🟢 as typed | 🟢 yes, lossy (**G3**) |
| Task Scheduler **200/201** | executable + return code only | 🔴 no (**G6**) |
| **Prefetch** | 🔴 **NO** | 🟢 yes |
| Amcache / ShimCache | 🔴 no | 🟢 yes |

🔴 **L1b — Prefetch does NOT store command-line arguments.** It records the executable and the files
it referenced. *"`rundll32.exe` ran"* and *"the command line was `rundll32.exe comsvcs.dll,
MiniDump …"* are different claims. **This is the most common wrong turn in a Windows execution
question and `S5-05` must state it explicitly.**

🟢 **Teach the negative as the deliverable:** *"execution of X at T is established by Prefetch;
arguments are not recoverable because process creation auditing was not enabled."* **Finding plus
stated limitation = D20 criterion 4.**
Source: <https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing>

### L2 — 🔴🔴 Amcache: three corrections, two of them new

Key **`Root\InventoryApplicationFile`**; hash field **`FileId`**. Other fields: `LowerCaseLongPath`,
`Name`, `OriginalFileName`, `Publisher`, `Version`, `BinaryType`, `ProductName`, `LinkDate`, `Size`,
`IsOsComponent`, `ProgramId`.

1. 🔴 **`FileId` is SHA-1 with four zeroes prepended** — *"the SHA-1 hash with 'four zeroes appended
   to the beginning of the hash'"*. **Strip `0000` before any lookup.** A raw paste into VirusTotal
   returns nothing and the student concludes "unknown".
2. 🔴🔴 **The hash covers only the first 31,457,280 bytes (~30 MB), not the whole file.**
   **For any binary over 30 MB the Amcache hash can never match VirusTotal or NSRL**, and **two files
   sharing their first 30 MB share a `FileId`.** ⚠️ **Amcache's hash is an identification aid, not an
   integrity value** — the same distinction as MD5 in **K7**, from a different direction.
3. 🔴🔴 **Amcache does NOT prove execution.** Cyber Triage: entries *"should generally not be used to
   prove program execution. Safer to interpret data as evidence of existence."* Securelist rates
   `InventoryApplicationFile` presence-only — *"with no data on whether or when they ran."*
   🟢 **Independently confirms `S5-06`'s existing presence-vs-execution framing.** Execution must come
   from **Prefetch** or the task's **200/201** records.

🟢 **What it does prove, and it is valuable:** a file with this path, size and SHA-1 **was present on
the volume at a known time, and the entry survives the file's deletion.** **For "was the binary
replaced?", two entries for one path with two different `FileId` values is the finding** — corroborate
with `$MFT`, `$UsnJrnl` (`DataOverwrite`), and the Authenticode signature state.
Sources: <https://securelist.com/amcache-forensic-artifact/117622/> ·
<https://blog.nviso.eu/2022/03/07/amcache-contains-sha-1-hash-it-depends/> ·
<https://www.cybertriage.com/blog/shimcache-and-amcache-forensic-analysis-2026/>

### L3 — 🔴 NTLM in 2026: neither "dead" nor "fine"

- **All versions deprecated** (June 2024) — *"All versions of NTLM, including LANMAN, NTLMv1, and
  NTLMv2, are no longer under active feature development and are deprecated."*
- 🔴 **NTLMv1 is REMOVED, not merely deprecated** — *"NTLMv1 is removed starting in Windows 11,
  version 24H2 and Windows Server 2025."* ⚠️ But *"remnants of NTLMv1 cryptography are still present
  in some scenarios, such as when using MS-CHAPv2 in a domain-joined environment."*
- 🟢 **NTLMv2 still works and is still enabled by default.** A phased plan to disable NTLM by default
  was announced **Feb 2026 for a future release** — **not today.**
- **The NT hash is unchanged:** `NTOWFv1(Passwd, User, UserDom) = MD4(UNICODE(Passwd))` —
  **MD4 of the UTF-16LE password, unsalted, uniterated.** 🟢 **Unsalted and uniterated is the lesson:
  identical passwords produce identical hashes across every account in the forest.**
- **Stored in:** `NTDS.dit` (`unicodePwd`) for domain accounts — *"Passwords at rest are stored in
  several attributes of the Active Directory database (NTDS.DIT file)"* — and the **SAM** for local
  accounts. ⚠️ **A SAM dump is not a domain compromise**; a domain user's hash on a member server
  comes from **LSASS** (a cached session), not SAM. **Conflating the two stores is the most common
  student error here.**
Sources: <https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features> ·
<https://support.microsoft.com/en-us/topic/upcoming-changes-to-ntlmv1-in-windows-11-version-24h2-and-windows-server-2025-c0554217-cdbc-420f-b47c-e02b2db49b2e> ·
<https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/464551a8-9fc4-428e-b3d3-bc5bfb2e73a5>

### L4 — 🔴🔴 Credential Guard is far narrower than it is usually taught

Microsoft: *"Starting in **Windows 11, 22H2** and **Windows Server 2025**, Credential Guard is enabled
by default on **domain-joined, non-DC systems that meet hardware requirements**."*
**Edition table: Enterprise YES · Education YES · Pro NO · Pro Education/SE NO.**

**Five gates, all of which must hold: 22H2+ · domain-joined · non-DC · Enterprise/Education ·
VBS-capable hardware.**

- **What it stops:** *"protecting NTLM password hashes, Kerberos Ticket Granting Tickets (TGTs), and
  credentials stored by applications as domain credentials"* — *"Malware running in the operating
  system with administrative privileges can't extract secrets that are protected by VBS."*
- 🔴🔴 **What it does NOT stop, verbatim:** *"Credential Guard doesn't provide protections for the
  Active Directory database or the Security Accounts Manager (SAM)."* Also: *"doesn't provide
  protection from privileged system attacks originating from the host."*

🟢🟢 **Net, and state it plainly to students: pass-the-hash is current practice, not history.** Three
gaps keep it alive — **SAM is explicitly unprotected**, CG is **off by default on Pro, non-domain-
joined, DCs and VBS-incapable hardware**, and **NTLMv2 is still enabled by default** so a hash is
still an accepted authenticator.
Source: <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/>

### L5 — 🔴🔴 Credential dumping leaves no default-on record

- **Sysmon 10 (ProcessAccess)** is the artifact of record — **Sysmon is not installed by default.**
- **Defender ASR** *"Block credential stealing from the Windows local security authority subsystem"*
  exists but ⚠️ **ASR rules are not enabled by default.** ⚠️ **GUID NOT VERIFIED — cite by name.**
- Security **4656/4663** on LSASS require a SACL nobody sets.
- **`rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <pid> <out> full`** is a **signed
  Microsoft LOLBin** — no file to find, no hash to look up. **The only anomaly is the command line,
  which L1 shows is usually missing.**
- 🟢 **Method inversion:** do not hunt the dump, hunt its **consequences** — a logon by an account
  with no business on the host, a `.dmp` in a temp path, an unexpected `rundll32.exe` in Prefetch.
  Check Defender **`DetectionHistory`** independently of the event log (**G8**).

### L6 — 🔴🔴 ATT&CK: no `T1574` sub-technique fits an overwritten scheduled-task binary

`T1574.010` is **services-only** by MITRE's own opening sentence — *"Adversaries may execute their own
malicious payloads by hijacking the binaries used by **services**."* The full sub-technique list
(.001 DLL · .004 Dylib · .005 Executable Installer File Permissions Weakness · .006 Dynamic Linker
Hijacking · .007–.009 Path Interception · .010/.011 Services · .012 COR_PROFILER · .013
KernelCallbackTable · .014 AppDomainManager) **contains no scheduled-task entry.**
**Correct mapping: `T1053.005` Scheduled Task/Job: Scheduled Task.** **Teach `.010` as the *services*
analogue and name the trap.**

Current tactics for this chain: **T1021.001** Lateral Movement · **T1003.001** / **T1003.002**
Credential Access · **T1550.002** Lateral Movement · **T1078.002 → Stealth, Persistence, Privilege
Escalation, Initial Access** · **T1053.005** Execution, Persistence, Privilege Escalation ·
**T1574 → Stealth, Execution**. ⚠️ **Two carry the Stealth tactic** — consistent with **E11**/**K1**.

### L7 — ⚠️ Correction to K1: cite the ATT&CK *version*, not the date

**K1 states "v19.2, released 6 August 2026."** That date comes from MITRE's **updates page**;
the **`attack-stix-data` `index.json` lists only to v19.1 (12 May 2026)**, with v19.0 on 28 Apr 2026.
Not a contradiction — the STIX index lags the site — **but do not print "6 August 2026" in
student-facing material. Cite "ATT&CK v19.2" and leave the date off.**
Source: <https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json>

### L8 — 🔴 The named pattern: every evidence defect is "act on the live system"

Ten safety/handling defects logged (rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24). **Four endanger the
analyst's machine; six endanger the evidence — and all six evidence defects are the same error:**
acting on the live system instead of collecting, verifying, then analysing a copy.

Room 24's instance is the subtlest and the most instructive: **running EZ Tools on the live host
creates new Prefetch entries and new `InventoryApplicationFile` rows for those tools** — in the exact
two artifacts the investigation depends on — and the examiner's RDP logon writes 4624/21/22 records
of the same class as the attacker's. 🟢 **Turn it into the lesson: students see their own footprint
in the evidence, which is the most convincing argument for minimal footprint there is.**
**This needs a named slide in `S2-01`/`S2-02`.**

### NOT VERIFIED — block L

- The **registry value name** behind *Include command line in process creation events*.
- The **ASR rule GUID** for LSASS credential-stealing protection, and the event ID an ASR block
  raises.
- The OS default for ***Audit Other Object Access Events*** (governs Security 4698) — carried from
  **G6**.
- **ATT&CK v19.2's exact release date** — see L7.

---

## M. Memory artifact semantics — what each structure is worth (appended 2026-08-29, from room 25 — Lost in RAMslation)

🟢 **All of block M is IN SCOPE.** It extends blocks **D** and **E10**, which already carry the
Volatility *environment* (version, renames, symbols, plugin currency). **M covers what the artifacts
mean**, which those blocks do not.

### M1 — 🔴🔴🔴 `windows.cmdline` reads the PEB, and the PEB is attacker-writable

**This is the most important memory finding in the project, and it cuts both ways.**

🟢 **First the good half — it answers block L1.** On a default Windows host *Audit Process Creation*
is off, the command-line policy is off, and Prefetch stores no arguments. **The PEB has the string
anyway.** Volatility 3's plugin is documented *"Extracts the cmdline from PEB"* and executes
`peb.ProcessParameters.CommandLine.get_string()`; Microsoft: `PEB.ProcessParameters` is *"A pointer
to an RTL_USER_PROCESS_PARAMETERS structure that contains process parameter information such as the
command line."* **That is the concrete, specific argument for memory-first acquisition — better than
"memory is volatile."**

🔴🔴 **Now the correction.** The PEB is **user-mode memory inside the process's own address space.**
ATT&CK **T1564.010 Process Argument Spoofing** (tactic **Stealth**): adversaries *"hide process
command-line arguments by overwriting process memory"*, may *"override the PEB to modify the
command-line arguments"* with `WriteProcessMemory()`, and can *"execute a process with malicious
command-line arguments then patch the memory with benign arguments that may bypass **subsequent
process memory analysis**."*

⚠️ **A second variant needs no overwrite:** set the `UNICODE_STRING` **Length** shorter than the
buffer — parent spawns the child `CREATE_SUSPENDED`, patches the PEB, `ResumeThread`. The real
arguments are still there, unread. **A suspiciously short command line is worth carving past
`Length`.**

- 🔴 **No kernel structure stores the command line.** `_EPROCESS.SeAuditProcessCreationInfo`
  (*"filename and path"*) and `_EPROCESS.ImageFileName` are the **image path** — they can refute a
  masqueraded path (**M5**), they cannot recover spoofed arguments.
- 🟢 **The one independent source is console memory** — `windows.consoles` / `windows.cmdscan`
  (*"Looks for Windows console buffers"*). ⚠️ **Console-launched commands only** — useless against an
  injected thread or a service.
- ⚠️ **Usually unavailable for exited processes**: the plugin's error path is *"Required memory at …
  is not valid (process exited?)"*. **So `psscan` finds the process and `cmdline` cannot read it.**

**Reporting rule:** *"the PEB of PID N contains string X"* is a **finding**; *"the attacker ran X"* is
an **interpretation** assuming the PEB was not patched. **A clean-looking command line is never
exculpatory.**
Sources: <https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/cmdline.html> ·
<https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb> ·
<https://attack.mitre.org/techniques/T1564/010/> ·
<https://blog.nviso.eu/2020/02/04/the-return-of-the-spoof-part-2-command-line-spoofing/>

### M2 — 🔴 `malfind`: the usual one-line description of its criterion is wrong

Docstring: *"Lists process memory ranges that **potentially** contain injected code."* **Candidates,
not findings.**

**Actual criterion, from the source** — not simply "RWX with no file backing":
`"EXECUTE" in protection_string and "WRITE" in protection_string`, **and**
`(vad.get_private_memory() == 1 and vad.get_tag() == "VadS") or (vad.get_private_memory() == 0 and
protection_string != "PAGE_EXECUTE_WRITECOPY")`.
**File-backed regions are NOT universally excluded — only WRITECOPY ones.** Volatility 3 also
inspects `PAGE_EXECUTE_READ` **dirty** pages *"to detect non-writable memory regions having been
injected using elevated WriteProcessMemory()"*.

- 🔴 **Paged-out regions are skipped** — *"entirely unavailable due to paging, entirely consisting of
  zeros, or a combination of the two"*. **Injected code that has been paged out does not appear.**
- 🔴🔴 **JIT is the dominant false positive.** Elastic: *"JIT code … generates assembly code at
  runtime which lives in unbacked or floating memory regions"*, and *".NET or Java applications are
  a couple of examples which use JIT techniques."* Also EDR that *"inject[s] code to some or all
  processes"*, and packers/DRM that *"decrypt or deobfuscate their core functionality in memory."*
  ⚠️ **A named list of benign processes is NOT VERIFIED — teach the categories, never a safe-list.**
- 🟢 **The workflow is subtractive:** `malfind` produces candidates; the analyst removes the
  explainable ones **using the hosting process's identity**. A hit in a .NET app is nearly
  meaningless; the same hit in `notepad.exe` is nearly conclusive. **Context does the work.**
- 🔴 Plugin is **`windows.malware.malfind`** (**D1**); `--yara-string`, not `--yara-rules` (**E10**).
Sources: <https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/malware/malfind.html> ·
<https://www.elastic.co/security-labs/hunting-memory>

### M3 — 🟢🟢 `4D 5A` in an injected region means a PE image, not shellcode

Microsoft: *"The first two bytes of the specified image has 0x5a4d, which is \"MZ\""*; the PE spec
places the MS-DOS stub *"at the front of the EXE image"*, with the PE signature offset at `0x3c`.
Elastic: reflective DLL injection leaves *"the full MZ/PE header"* at the start of unbacked
executable memory, and *"Typical code sections are of type 'Image' and map to a file on disk.
However, these are type 'Private' and do not map to a file on disk."*

| first bytes | what it is | ATT&CK |
|---|---|---|
| `4D 5A …` | a **PE image** injected into the process | **T1055.002** Portable Executable Injection (**Stealth**, Privilege Escalation) · **T1620** Reflective Code Loading (**Stealth**) when loaded without touching disk |
| not `4D 5A` | **raw shellcode** — instructions, no headers | **T1055** family; the stub is a loader, not an image |

✅ **T1055.001** DLL Injection — Stealth, Privilege Escalation.
⚠️ **Absence of MZ does not prove raw shellcode** — reflective loaders routinely strip the header once
mapped; the section layout still betrays it. 🟢 **Report the region's structure, not five bytes.**
🟢🟢 **Teaching link: this is `S3-02`/`S3-03`'s file-signature lesson arriving in memory instead of on
disk.** One cross-reference ties the two sessions together.
Sources: <https://learn.microsoft.com/en-us/archive/blogs/coreinternals/portable-executable-file-format-on-memory-dump> ·
<https://learn.microsoft.com/en-us/windows/win32/debug/pe-format> · <https://attack.mitre.org/techniques/T1620/>

### M4 — 🔴🔴 A process tree is a hypothesis, not a diagram

- **`pslist`** walks `PsActiveProcessHead` — *"does not detect hidden or unlinked processes (but
  psscan can do that)"*. **`pstree`** *"enumerates processes using the same technique as `pslist`, so
  it will also not show hidden or unlinked processes."* **`psscan`** scans `_POOL_HEADER` pool tags
  and *"can find processes that previously terminated (inactive) and processes that have been hidden
  or unlinked by a rootkit"* — ⚠️ though *"rootkits can still hide by overwriting the pool tag
  values."* **Run `pslist` and `psscan` and diff.**
- ⚠️ **A `psscan`-only process is usually just *terminated*.** That is the boring explanation and it
  is usually right — do not report a rootkit because of a diff.
- 🔴 **PID reuse:** Windows releases a PID once the last handle closes, so **a recorded PPID can
  resolve to an unrelated later process.** Real on long-uptime servers.
- 🔴🔴 **Parent PID spoofing — ATT&CK T1134.004** (**Stealth**, Privilege Escalation): a process
  *"explicitly forges its parent"* via `EXTENDED_STARTUPINFO` + `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS`
  through `UpdateProcThreadAttribute` → `CreateProcess`, *"resulting in mismatched/implausible
  lineage."* **PPID is an attacker-settable field.**
- 🟢 **Falsifiability check: `CreateTime` ordering — a child cannot predate its claimed parent.**
  ⚠️ **Our own synthesis, not a quoted source — demonstrate it in the lab before teaching it.**
Sources: <https://github.com/volatilityfoundation/volatility/wiki/Command-Reference> ·
<https://devblogs.microsoft.com/oldnewthing/20110107-00/?p=11803> ·
<https://attack.mitre.org/techniques/T1134/004/>

### M5 — 🔴 `T1036.005` has been RENAMED

Now **"Masquerading: Match Legitimate *Resource* Name or Location"**, tactic **Stealth** — *"Adversaries
may match or approximate the name or location of legitimate files, Registry keys, or other resources
when naming/placing them."* **The word "Resource" was added; older material says "Match Legitimate
Name or Location".** ✅ **Repo grepped: `T1036` appears nowhere — forward-looking only.**

**Three checks, SANS *Find Evil*:** *"process names that appear legitimate but originate from the
**wrong directory path** or with the **wrong parent process or SID**"* — `svchost.exe` expected at
*"`%SystemRoot%\System32\svchost.exe`"*, parent *"services.exe"* — plus *"Checking for signed code can
help reveal suspicious executables"*, and misspellings such as *"scvhost.exe or lssass.exe"*.
🔴 ⚠️ **All three checks are attacker-influenceable** (side-loading into a genuine binary, spoofed
parent per **M4**, signed-but-malicious). ⚠️ **And `_EPROCESS.ImageFileName` truncates at 15 bytes**
(**E10**), so **the name column is the least reliable column on screen and the one students read
first.**
Sources: <https://attack.mitre.org/techniques/T1036/005/> ·
<https://networkforensic.dk/Tools/Files/cheat-sheets/Poster_Find_Evil.pdf>

### M6 — ⚠️ Every Volatility command in our material needs a version bound

The `malfind` shim carries `removal_date="2026-06-07"` — **already past** (**D1**) — and the second
rename wave (`amcache`, `cachedump`, `hashdump`, `lsadump`, `scheduled_tasks` → `windows.registry.*`)
removes on **2026-09-25**, which is **27 days after this extraction**.
🟢 None of room 25's plugins are in that wave, and `pslist`/`psscan`/`pstree`/`cmdline`/`netscan`/
`netstat`/`filescan`/`dumpfiles`/`dlllist` are all verified live. **But a lab or grading key with no
version bound is a time bomb, and the shim is the worked example.**

### M7 — 🟢🟢 The memory/disk pair, stated once for reuse

**Rooms 24 and 25 together make one argument, and it should be taught as one:**

1. **The disk usually has no command line** — two audit switches, both off by default (**L1**), and
   Prefetch stores no arguments.
2. **Memory has it anyway**, in the PEB (**M1**).
3. **But the PEB is a claim the process makes about itself** (**M1**, T1564.010).
4. **So the finding is corroboration across independent sources** — PEB, console buffers, the
   kernel-side image path, the process tree, and whatever the disk did record.

🔴 **Teaching either half alone produces a wrong belief:** half 1 alone says "you cannot know";
halves 1–2 alone say "memory is authoritative." **Both are wrong. Ship them together.**

### NOT VERIFIED — block M

- A **named list of benign processes** that routinely trip `malfind` (categories verified only).
- The **`CreateTime`-ordering falsifiability check** — our own synthesis; demonstrate before teaching.
- Whether **parent-process memory or in-memory ETW** offers an independent command-line recovery path
  in Volatility 3 — not supported as far as could be verified.

---

## N. Exfiltration, archives and anti-forensics (appended 2026-08-29, from room 26 — CRM Snatch)

🟢 **All of block N is IN SCOPE.** Room 26 is the only stage of the module whose working shape is
ours — a disk image, offline, with EZ Tools.

### N1 — 🟢🟢 `rclone obscure` is obfuscation, and rclone's own docs say so

**The best "obfuscation is not encryption" example in the project**, because the vendor states it.

- *"In the rclone config file, human-readable passwords are obscured. Obscuring them is done by
  encrypting them and writing them out in base64."* — then the warning that matters:
  ***"This is not a secure way of encrypting these passwords as rclone can decrypt them - it is to
  prevent 'eyedropping'."***
- **`rclone reveal` reverses it.** ⚠️ **The command has no documentation page** (404 on rclone.org) —
  undocumented is not hidden, and that is worth saying to students.
- 🔴 **rclone *prints* `*** ENCRYPTED ***`** for the field. **That string is not what the file
  contains and is actively misleading.**
- 🔴🔴 *"Many equally important things (**like access tokens**) are not obscured in the config
  file."* **An OAuth token for a cloud remote can sit in cleartext — a bigger finding than the
  password.**
- **Real protection exists:** `rclone config encryption set` — *"Set or change the config file
  encryption password"*. **An encrypted `rclone.conf` is a different investigation; students should
  tell the two apart on sight.**
- **Config path:** `%APPDATA%/rclone/rclone.conf` (Windows); `$XDG_CONFIG_HOME/rclone/rclone.conf`
  or `~/.config/rclone/rclone.conf` (Unix). ⚠️ `--config` can point anywhere — **grep for the section
  header, do not trust the default path.**
- **What the file gives an examiner:** remote name, `type` (e.g. `mega`), `user`, `pass`.
- **No log by default** — *"`--log-file` … This is not active by default."* Flags worth grepping:
  `copy`, `sync`, `--transfers`, `--config`, `--no-check-certificate`.
- **Tradecraft:** ATT&CK software **S1040** — *"Rclone has been used in a number of ransomware
  campaigns, including those associated with the Conti and DarkSide Ransomware-as-a-Service
  operations."* **T1567.002 names the combination** — *"Rclone can exfiltrate data to cloud storage
  services such as Dropbox, Google Drive, Amazon S3, and MEGA."*
- 🔴 **Genuinely dual-use: presence is not exfiltration.** Proof chain: binary present → Prefetch
  (ran) → `rclone.conf` (remote configured) → command line (what was copied) → **network or
  provider-side evidence for bytes leaving, which a disk image does not contain.**
- 🔴🔴 **Handling rule the room omits: recovering the credential does not authorise using it.**
  Logging in to the attacker's cloud account is unauthorised access to a third-party service.
Sources: <https://rclone.org/commands/rclone_obscure/> · <https://rclone.org/docs/> ·
<https://rclone.org/mega/> · <https://attack.mitre.org/software/S1040/> ·
<https://attack.mitre.org/techniques/T1567/002/>

### N2 — 🔴🔴 PowerShell 400/403 bracket an ENGINE INSTANCE, not a session

- IDs, classic **`Windows PowerShell`** channel: **400** *"Engine state is changed from None to
  Available"* · **403** *"…from Available to Stopped"* · **600** provider lifecycle (a `WSMan`
  provider indicates remoting).
- 🟢 **On by default** — Microsoft: *"By default, only the following event types are enabled:
  `$LogEngineLifecycleEvent`, `$LogEngineHealthEvent`, `$LogProviderLifecycleEvent`,
  `$LogProviderHealthEvent`."* **This is the concrete support for G4's claim that the classic channel
  is the best default-on PowerShell artifact.**
- 🔴 ***"This event cannot be strictly correlated to a logon session."*** Every host that loads the
  engine emits its own pair — `powershell.exe`, the ISE, and **any .NET/COM application hosting
  `System.Management.Automation`**. One RDP session with three console launches = **three pairs**.
  **Last-403 minus first-400 is a plausible-looking wrong answer.**
- 🟢 **Method:** pin the pair by **`RunspaceId`**; corroborate `HostApplication`/`HostName`
  (`ConsoleHost` = local, `ServerRemoteHost` = remote); bracket against **4624 t10 / 4634**.
  ⚠️ **Even then it measures engine availability, not attacker activity** — an idle console counts.
- ⚠️ **4103/4104 are in `Microsoft-Windows-PowerShell/Operational`, off by default** — see **G1** for
  the three-state nuance, **G2** for PowerShell 7's separate channel.
Sources: <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_eventlogs?view=powershell-5.1> ·
<https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-module-powershell.html>

### N3 — 🔴🔴 Shadow copy deletion: no dedicated event ID, and TWO common IOCs are WRONG

**Both of these were assumptions going in, and both were refuted. They are widely repeated.**

- ❌ **Application event 524 is NOT a shadow-copy artifact.** Provider `Microsoft-Windows-Backup`,
  *"The system catalog was deleted"* — it records **backup-catalog** deletion (`wbadmin delete
  catalog`). ⚠️ JPCERT adds it *"may also occur in normal operation."*
- ❌ **`volsnap` event 25 is NOT an attacker indicator.** *"The shadow copies of volume %2 were
  aborted because the diff area file could not grow in time"* — **a capacity/IO condition.**
- ⚠️ **Registry / `System Volume Information` remnants of deleted shadow copies: NOT VERIFIED.**
  No primary source found. **Do not teach it as fact.**
- 🔴 **What actually detects it is process creation:** Elastic's rule matches
  `process.name : "vssadmin.exe"` with `process.args : ("delete", "resize")` and
  `process.args : "shadows*"` — **so the artifact is Security 4688 with command-line auditing, or
  Sysmon 1, and block L1 established both are off by default.** Fallback: **Prefetch / Amcache /
  ShimCache for `vssadmin.exe` or `wmic.exe`**, plus 4104 if script-block logging caught it.
- **T1490 Inhibit System Recovery, tactic Impact** — MITRE names the command outright:
  *"vssadmin.exe delete shadows /all /quiet"*.
- ⚠️ **PowerShell 7:** `Get-WmiObject`/`Remove-WmiObject` are **removed** (**F5**) — expect
  `Get-CimInstance Win32_ShadowCopy | Remove-CimInstance`, logged to `PowerShellCore/Operational`
  (**G2**).
- 🟢🟢 **The honest professional answer:** *"deletion is inferred from the absence of shadow copies
  and the execution of `vssadmin.exe`; no direct record of the deletion exists on this host, because
  process command-line auditing was not enabled."* **Finding, method and stated limitation — D20
  criteria 2, 3 and 4 in one paragraph.**
Sources: <https://www.elastic.co/guide/en/security/8.19/volume-shadow-copy-deleted-or-resized-via-vssadmin.html> ·
<https://blogs.jpcert.or.jp/en/2024/09/windows.html> ·
<https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/dd364930(v=ws.10)> ·
<https://attack.mitre.org/techniques/T1490/>

### N4 — 🟢🟢 A password-protected archive is not opaque

**On a default archive the file names, sizes, timestamps and CRC32 values are readable without the
password.** The intuitive answer ("it's encrypted, so nothing") is wrong.

- **ZIP:** ZipCrypto and AES (WinZip AE-x, 7-Zip `-tzip -mem=AES256`) encrypt **data only**; the
  central directory keeps names, sizes and CRCs. Hiding them needs **Central Directory Encryption**,
  APPNOTE **bit 13** — *"Set when encrypting the Central Directory to indicate selected data values
  in the Local Header are masked to hide their actual values."*
- **7-Zip:** *"Enables or disables archive header encryption. **The default mode is he=off**."*
- **WinRAR:** *"If you set 'Encrypt file names' option, WinRAR will encrypt not only file data, but
  all other sensitive archive areas like file names, sizes, attributes, comments and other blocks"*
  and *"Without a password it is impossible to view even the list of files"* — **opt-in.**
- 🟢 **Investigative consequence:** you can prove *which* export was staged without cracking
  anything, and **a CRC32 match against the original file ties the archived item to a known file.**
  ⚠️ CRC32 is 32-bit — **strong corroboration, not identity.**
- 🟢🟢 **Generalise the instinct: enumerate before you decrypt.** It applies to encrypted containers,
  protected Office documents and locked databases. **The common student failure is giving up at the
  password prompt.**
- **T1560.001 Archive via Utility, tactic Collection.**
Sources: <https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.9.TXT> ·
<https://documentation.help/7-Zip/method.htm> · <https://documentation.help/WinRAR/HELPArcPassword.htm>

### N5 — 🟢 The shape of a cleared event log (what the attacker cannot remove)

Clearing is **destruction, not concealment** — the content is gone, and **absence of Security 1102 /
System 104 does not mean no clearing** (a second clear removes the first clear's record; selective
deletion never raises 1102 at all).

**Three structural tells survive, none of which the attacker touched:**
1. **Record-ID discontinuity** — a cleared channel restarts at **record ID 1**. *A channel whose
   earliest record is 1 on a server with months of uptime is a finding in itself.*
2. **The `.evtx` file's own `$MFT` timestamps and size.**
3. **Cross-channel disagreement** — e.g. `TerminalServices-LocalSessionManager/Operational` still
   holding sessions the Security log no longer mentions.

🔴 **ID correction:** clearing Windows event logs is **`T1685.005`** (Defense Impairment) —
*"Adversaries may clear Windows Event Logs to hide the activity of an intrusion"* — **not
`T1070.001`** (**K1**). **Room 26 is the first room in the corpus that actually needs it.**

🟢🟢 **And the asymmetry is the lesson:** `wevtutil cl` clears **event logs**. It does not touch the
registry, `$MFT`/`$UsnJrnl`, Prefetch/Amcache, or `ConsoleHost_history.txt` in the user profile.
**One source removed, four left** — which is the operational argument for **D25**'s ordering (file
systems before timelines).
Source: <https://attack.mitre.org/techniques/T1685/005/>

### N6 — 🔴🔴 Process rule: no secret AND no PII as a question's answer

**Room 24 gave us "no credential as an answer." Room 26 shows that was too narrow.** Its Q5 asks for
a **password**; its Q6 asks for **a named individual's email address taken from exfiltrated customer
data.**

> **No eCDFP question may have a secret or a data subject's personal information as its answer.**
> Ask *which* account, *which* remote, *which* record — never the value. Ask **"how many customer
> records were in the staged export, and how do you know?"**, never **"what is a customer's email
> address?"** Secrets and PII enter the record **by reference only** — path, offset, timestamp,
> record count — in the restricted appendix.

🟢🟢 **The replacement questions are strictly better forensics**: a record count exercises **N4**'s
archive-listing technique, a CRC comparison, and a stated limitation. An email address exercises
`Ctrl+F`. **D22 makes this a release-gate concern, not a style preference.**

⚠️ **Keep the narrative requirement, drop the disclosure:** the module needs the individual's
presence in the stolen data because that is how the final stage targets him. *"The export contains
records for N employees, including the lead developer"* preserves the plot with no PII in the answer
key.

### N7 — ⚠️ The stale checker contained this room's real password

Room 26's published RDP password is **verbatim one of the literal strings hardcoded in the
`/tmp/verify.py` blocklist** found on the device during room 22's verification.

**That is D39's entire argument in one observation:** the old checker was not a pattern set, it was
**a list of real room passwords** — itself a credential store, unable to generalise to an unseen
room, and **had it reached the public repo (D22) it would have been the leak it existed to prevent.**
✅ The current checker is pattern-based (7/7 leak shapes caught, 0 false positives) and lives in
`testing/verify_note.py`.

### NOT VERIFIED — block N

- **That room 26's exfiltration tool is rclone** — inferred from the question naming Mega; the
  artifact reasoning in **N1** holds for any sync tool with a config file.
- **Registry / `System Volume Information` remnants of deleted shadow copies.**
- **ATT&CK v19.2's release date** — carried from **L7**; cite the version only.

---

## O. Image formats, Mark of the Web and the limits of NTFS logs (appended 2026-08-29, from room 27 — Shock and Silence)

🟢 **All of block O is IN SCOPE**, and **O1 and O4 change existing rows** (`S2-04`/`S2-05`, `S4-07`).

### O1 — 🔴🔴 AD1 is a LOGICAL container, and Autopsy cannot open it

**`S2-05` already names AD1. This is what it means.**

- AccessData's own guide, verbatim: *"AD1 and L01 are both custom content images, and contain full
  file structure, but **do not contain any drive geometry other other physical drive data**."*
  Against: *"E01, S01, AFF, and 001 (RAW/dd) images are drive images that have the disk, partition,
  and file structure as well as drive data."* PRONOM: *"a file-level disk image format."*
- 🔴 **What a logical image LOSES:** unallocated space · file slack · deleted/unlinked records ·
  carveable fragments · partition table and volume geometry · **anything the collector did not tick.**
  **"I could not find X" on a logical image never distinguishes *X was absent* from *X was not
  collected*.**
- 🔴🔴 **Tool support is the practical shock.** **Autopsy / The Sleuth Kit: NO** — feature request
  open since **2015**, requester notes *"I haven't come across any open source tools that read AD1
  images."* **Arsenal Image Mounter: NO** — its list is Raw/DMG/AFF4/E01/Ex01/S01/VHD/VDI/XVA/VMDK/
  OVA/qcow. **7-Zip only via the third-party `Forensic7z` plugin.** One community tool:
  **AD1-tools** (Linux, v1.0, Jul 2024 — ⚠️ single author, **test before any lab use**).
  **On Windows, FTK Imager is effectively the only mainstream free route in.**
- **FTK Imager 8.3, Exterro (AccessData acquired Dec 2020), still free.** ⚠️ **Release date NOT
  VERIFIED.**
- 🔴 **Lab-build consequence: if we ever hand out a logical image, FTK Imager must be in
  `CLEAN-TOOLS` (D17)** — our students work in Autopsy (`S2-06`, `S4`) and would simply be unable to
  open it.
- 🟢🟢 **Best exercise it suggests:** supply the *same* incident twice — once as **E01**, once as an
  **AD1 of "the important files"** — and ask which questions each can answer. **That makes `S2-04`'s
  physical-vs-logical row real at the cost of one extra export.**
Sources: <https://arts.unimelb.edu.au/__data/assets/pdf_file/0011/2970587/Imager-3_1_4_UG.pdf> ·
<https://www.nationalarchives.gov.uk/pronom/fmt/842> ·
<https://github.com/sleuthkit/autopsy/issues/1402> ·
<https://arsenalrecon.com/products/arsenal-image-mounter/faqs>

### O2 — 🟢🟢 `Zone.Identifier`: the ADS that answers "where did this file come from"

**Gives `S4-07`'s ADS bullet an actual investigative purpose.**

- Stream, per MS-FSCC: **`file.ext:Zone.Identifier:$DATA`**, containing `[ZoneTransfer]` and
  **`ZoneId`**, optionally **`ReferrerUrl`** and **`HostUrl`**.
- **`HostUrl` = the direct URL of the file. `ReferrerUrl` = the page it was linked from.** Worked
  example: `ReferrerUrl=https://www.7-zip.org/download.html`,
  `HostUrl=https://www.7-zip.org/a/7z1900.exe`.
- **Zone values: 0 Local Machine · 1 Local intranet · 2 Trusted sites · 3 Internet · 4 Restricted.**
  **`ZoneId=3` is the one you will see.**
- 🔴 **URL fields are application-dependent:** *"HostUrl and ReferrerUrl are set by Microsoft Edge and
  Google Chrome"*; **Firefox only began including URL information in February 2021**; and
  *"If this is done in incognito mode, then the URL is not recorded."* **A bare `ZoneId=3` with no
  URL is a normal, complete result — not a failed search.**
- 🔴 **NTFS-only:** *"Files moved to FAT32, exFAT, or network shares using non-NTFS file systems will
  lose the stream."* 🟢 Survives NTFS→NTFS copies.
- ⚠️ **Archive propagation is current and contested:** archivers generally propagate MotW now
  (*"Sometimes this needs to be configured, like with 7-Zip"*), and **failing to do so is a tracked
  vulnerability class** — **CVE-2025-0411 / ZDI-25-045**: *"When extracting files from a crafted
  archive that bears the Mark-of-the-Web, 7-Zip does not propagate the Mark-of-the-Web to the
  extracted files."* **So absence on an extracted file may indict the archiver, not the attacker.**
- 🟢 **Asymmetry to teach:** **absence is weak** (`Unblock-File`, a FAT32 hop, or an app that never
  wrote one), **presence is strong** — the stream is written by the OS, not the attacker. **And
  deleting it leaves `USN_REASON_STREAM_CHANGE` in `$UsnJrnl`, which outlives the stream.**
- **Parsing:** `dir /r` · `Get-Item -Stream *` · `Get-Content -Stream Zone.Identifier` · `streams.exe`.
  🟢 `MFTECmd` surfaces the ADS from `$MFT` (a named `$DATA` attribute) — **names and sizes only.**
Sources: <https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/6e3f7352-d11c-4d76-8c39-2516a9df36e8> ·
<https://xkln.net/blog/identifying-the-source-of-downloaded-files/> ·
<https://www.dfir.co.za/2018/06/18/highway-to-the-danger-zone-identifier/> ·
<https://www.zerodayinitiative.com/advisories/ZDI-25-045/>

### O3 — `$UsnJrnl` reason flags, and the signature of a ransomware run

Microsoft's definitions, verbatim from `USN_RECORD_V2`:

| flag | value | meaning |
|---|---|---|
| `USN_REASON_DATA_OVERWRITE` | `0x00000001` | *"The data in the file or directory is overwritten."* |
| `USN_REASON_DATA_EXTEND` | `0x00000002` | *"The file or directory is extended (added to)."* |
| `USN_REASON_FILE_CREATE` | `0x00000100` | *"The file or directory is created for the first time."* |
| `USN_REASON_FILE_DELETE` | `0x00000200` | *"The file or directory is deleted."* |
| `USN_REASON_RENAME_OLD_NAME` | `0x00001000` | *"…renamed, and the file name … is the previous name."* |
| `USN_REASON_RENAME_NEW_NAME` | `0x00002000` | *"…renamed, and the file name … is the new name."* |
| `USN_REASON_STREAM_CHANGE` | `0x00200000` | *"A named stream is added to or removed from a file…"* (**O2**) |
| `USN_REASON_CLOSE` | `0x80000000` | *"The file or directory is closed."* |

🟢🟢 **Encryption signature, documented in the field:** *"Each original file generates a
`DATA_OVERWRITE` record (content replaced with ciphertext), followed by a `RENAME_NEW_NAME` record
(extension changed to `.locked`), followed by `FILE_DELETE` for the Volume Shadow Copy deletion
commands"*, at roughly **1,200 files per minute**.
🟢 **The RATE is the evidence** — no human renames a thousand files a minute, so the pattern
distinguishes automated encryption from user activity with no other artifact.
⚠️ **Join renames on `FileReferenceNumber`, never on name.**
⚠️ **The journal is trimmed lazily (C8)** — on an image acquired *after* the event, **the start of
the run may have aged out. Report first and last observed records as bounds, not as the run.**
⚠️ **Legitimate bulk operations look similar** (backup agent, AV scan, `robocopy`, encryption
rollout). Discriminators: a **new extension applied uniformly**, no corresponding change record, and
the hour.
Sources: <https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2> ·
<https://intel.mjolnirsecurity.com/artifact-usnjrnl>

### O4 — 🔴🔴🔴 `$UsnJrnl` has NO process attribution

**The strongest single "cannot be determined" finding of the extraction.**

`USN_RECORD_V2` has **no process or PID field**, and Microsoft states the limit twice: the change
journal *"logs only the fact of a change to a file and the reason for the change (for example, write
operations, truncation, lengthening, deletion, and so on)"*, and *"It does not record enough
information to allow reversing the change."* **`$MFT` and `$LogFile` carry none either.**

**So "which executable did this to the file system?" is not an NTFS-log question.** Attribution needs
**Security 4688 + command-line auditing** (off by default — **L1**), **Sysmon 1** (not installed by
default), **Prefetch** (execution, no arguments — **L1**), **Amcache** (presence, not execution —
**L2**), or **memory** (**M1**).

🟢 **The defensible finding shape, worth teaching verbatim:**
> *"`<name>.exe` was written to `<path>` at T₁; a mass `DATA_OVERWRITE` + `RENAME` pattern affecting
> N files began at T₂, ninety seconds later. The change journal records no process attribution, so
> the causal link is an inference from proximity and is not established by this evidence.
> Prefetch or Security 4688 with command-line auditing would settle it."*

**Finding · method · stated limitation · named next artifact — D20 criteria 2, 3 and 4 in one
paragraph.** 🟢🟢 **And note that no anti-forensics was required to create this gap: the attribution
was never recorded.** Same shape as **L1**, one layer down.

### O5 — Ransomware attribution: family, never actor

- **Builders leak.** SentinelOne: *"Source code leaks further complicate attribution, as more actors
  will adopt the tools"* — noting *"a noticeable trend that actors increasingly use the Babuk
  builder."*
- **Brands are impersonated deliberately.** Sophos, on the leaked LockBit 3.0 builder *"which enabled
  any attacker to use it"*: actors were seen *"deploying ransomware in an environment, purporting to
  be LockBit, and hoping that referencing a prolific and well-known ransomware scheme will be enough
  to convince victims to pay."*
- **RaaS separates payload from operator**; affiliates share one builder. **Brands rebrand.**
- 🟢🟢 **Phrasing rule for `S1-04`:** *"consistent with an X-family payload"*, **never** *"attributed
  to group X"*. Record the extension, note filename, contact and payment infrastructure **as
  findings**; the family label is an **interpretation** whose basis and date must be named.
- ⚠️ **Handling: do not visit attacker infrastructure** — same rule as **N1**.
Sources: <https://www.sentinelone.com/labs/hypervisor-ransomware-multiple-threat-actor-groups-hop-on-leaked-babuk-code-to-build-esxi-lockers/> ·
<https://www.sophos.com/en-us/blog/lockbit-in-action>

### O6 — ATT&CK additions, and a reinforcement of L7

✅ **T1486** Data Encrypted for Impact → **Impact** · **T1105** Ingress Tool Transfer → **Command and
Control** · **T1489** Service Stop → **Impact** · **T1490** Inhibit System Recovery → **Impact**.
🔴 **`T1484.001`'s parent has been RENAMED** — now ***"Domain or Tenant Policy Modification"***, so
the sub-technique is **"Domain or Tenant Policy Modification: Group Policy Modification"**, tactics
**Defense Impairment and Privilege Escalation**. ✅ Repo grepped: `T1484` appears nowhere.

⚠️ **MITRE's own pages now disagree on the current version's date** — the updates row reads
*"ATT&CK v19 | August 6, 2026 | Current version of ATT&CK | v19.2 on MITRE/CTI"*, while
`index.json` lists to **v19.1 (12 May 2026)** and v19.0 at 28 Apr 2026.
🔴 **Block L7's rule stands and is now doubly justified: cite the version, never the date.**

### NOT VERIFIED — block O

- **FTK Imager 8.3's release date.**
- **AD1-tools' maturity** — v1.0, single author. **Test before any lab use.**
- Whether room 27's `.ad1` contains **`$LogFile`** as well as `$MFT` and `$J` — *"NTFS logs"* is
  ambiguous, and the retention difference matters (**C8**).

---

## P. macOS provenance and enforcement (appended 2026-08-29, from room 28 — The Last Trial)

⚠️ **macOS is OUT OF SCOPE (D38), and this block is deliberately short.** It exists for the **F1
contrast table** and for **two platform-neutral lessons** (P2, P3). **No macOS module is planned.**

### P1 — 🟢🟢 macOS download provenance is SPLIT IN TWO — the F1 row

**The file carries a UUID; the URL lives in a user database.** That is the difference from Windows,
and it has real investigative consequences.

- **`com.apple.quarantine` xattr**, value form `0083;5991b778;Safari.app;BC4DFC58-…` —
  *"the quarantine value in hexadecimal, the time at which the xattr was attached, in hexadecimal,
  the app or agent responsible for creating the xattr, [and] a UUID referring to the entry for this
  quarantine flag in the QuarantineEvents database."* 🔴 **No URL in the xattr.**
- **`~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2`** — SQLite, table
  **`LSQuarantineEvent`**, columns `LSQuarantineTimeStamp`, `LSQuarantineDataURLString`,
  `LSQuarantineOriginURLString`, `LSQuarantineAgentName`, `LSQuarantineAgentBundleIdentifier`,
  `LSQuarantineEventIdentifier`. ⚠️ **Cocoa epoch — add 978,307,200 s** for Unix time.
- 🔴🔴 **The contrast to teach (against O2):**

| | Windows | macOS | Linux |
|---|---|---|---|
| where the URL lives | **in an ADS on the file** (`Zone.Identifier` → `HostUrl`) | **in a per-user SQLite DB**; the file holds only a UUID | **nowhere** |
| delete one record | affects **one file** | **strips provenance from every downloaded file at once** | n/a |
| file deleted | ADS dies with it | **DB row survives** | n/a |

**Each platform preserves what the other loses.** ⚠️ **Column semantics (`Data` vs `Origin`) NOT
VERIFIED** — secondary sources gloss them as file-URL vs referring-page, no primary source defines
them. **Teach the column names, not the gloss.**
⚠️ **Correction to a common assumption:** FAT/exFAT do **not** simply destroy xattrs — *"can preserve
xattrs in hidden shadow files"* (AppleDouble). **NFS strips them**; `xattr -d` removes them.
🔴 **Whether the DB is still populated on macOS 26 (Tahoe, current — 26.6.1 on 6 Aug 2026) is NOT
VERIFIED.** The xattr is confirmed current (Apr 2026 source); the DB path is unchanged in tooling;
**no source tested the DB on 26. Do not assert it.**
Sources: <https://eclecticlight.co/2020/10/29/quarantine-and-the-quarantine-flag/> ·
<https://eclecticlight.co/2026/04/24/the-secret-life-of-the-xattr/> ·
<https://docs.velociraptor.app/artifact_references/pages/macos.system.quarantineevents/>

### P2 — 🟢🟢 IN SCOPE: enforcement lives in the running OS, not in the data

**The most transferable idea in the room, and it is platform-neutral.**

macOS's **TCC** databases — user `~/Library/Application Support/com.apple.TCC/TCC.db`, system
`/Library/Application Support/com.apple.TCC/TCC.db` — **cannot be read on a live Mac**: *"you won't
be able to read your regular user TCC database unless it's from a TCC privileged process."*
⚠️ **Be precise about the mechanism: the user DB is TCC-protected; the system DB is SIP-protected**
(*"only a SIP bypass can write into it"*).

🟢🟢 **From a mounted image both are ordinary SQLite files** — `mac_apt` ships `plugins/tcc.py` to
parse them. **The protection is enforced by the running operating system; it is not carried by the
data, so it evaporates when the disk is read by something else.**

**Two consequences for `S2-04`, both worth teaching:**
1. **Offline analysis sees things live response cannot** — the same reason a Windows registry hive
   read from an image ignores the ACLs that guarded it.
2. 🔴 **An evidence image must be handled as sensitive data**, because **every access control the
   subject relied on is gone.**

**Artifact detail, for completeness:** the `access` table records *"the requesting application bundle
ID, the service being accessed, the authorization decision, and a timestamp"* — columns `service`,
`client`, `client_type`, `auth_value`, `auth_reason`, **`last_modified`**, `csreq`, `policy_id`,
`flags`, `prompt_count`. `auth_value` = *"denied(0), unknown(1), allowed(2), or limited(3)"*.
🔴 **`last_modified` is *last*, not first** — a granted/revoked/re-granted permission keeps one
timestamp. 🔴 **And a row is authorisation, not use** — *permission ≠ access*, the same distinction
as **L2**'s presence-vs-execution.
**ATT&CK T1548.006 Abuse Elevation Control Mechanism: TCC Manipulation, tactic Privilege Escalation.**
Sources: <https://book.hacktricks.wiki/en/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/index.html> ·
<https://github.com/ydkhatri/mac_apt/blob/master/plugins/tcc.py> ·
<https://attack.mitre.org/techniques/T1548/006/>

### P3 — 🟢 IN SCOPE: the event that was never recorded

**Third instance of a theme, and now clearly a theme.**

A **drag-and-drop application from a DMG produces no receipt and no `InstallHistory` entry** — the
mechanism *"bypasses the mechanisms built into OS X for recording installation and updating"*, and
*"If you want to keep a record of those events, you will need to keep your own notes, I am afraid."*
`/Library/Receipts/InstallHistory.plist` *"records App Store and Installer app installations"*;
`/var/db/receipts` holds *"Complete records of individual files installed by each package."*
**Neither covers drag-and-drop.**

🟢🟢 **The general lesson for `S1-03`:** *some questions are unanswerable not because evidence was
destroyed, but because the event was never one the system records.* **Three instances now:**
**L1** (no command line without auditing) · **O4** (`$UsnJrnl` has no process field) · **P3** (no
receipt for drag-and-drop). ⚠️ **And each has a different fallback with different weight** — here,
quarantine time (*download*, not install), bundle timestamps (the *copy*), or FSEvents. **Three
artifacts, three answers, one word: "installed."**
Source: <https://eclecticlight.co/2015/09/25/what-was-installed/>

### P4 — Tooling, and a format-compatibility rule

- **`apfs-fuse`** (sgan81) — *"a **read-only** FUSE driver for the new Apple File System"*; writing is
  an explicit Limitation. Supports *"software encrypted volumes and fusion drives"* and *"mounting
  snapshots and sealed volumes"*. 🟢🟢 **Read-only by design — a mount command that cannot produce
  E5's defect.** **Principle worth adopting: prefer a tool that cannot write over one that must be
  told not to.**
- **`mac_apt`** (Yogesh Khatri) **v1.29.0, 11 Feb 2026** — *"Works on E01, VMDK, AFF4, DD, split-DD,
  DMG (no compression), SPARSEIMAGE, UAC collections, Velociraptor collected files (VR) & mounted
  images"*. **No mount required.** ⚠️ **An automated report's silence is the plugin's silence, not the
  disk's** — and **P3** is the worked example.
- 🔴 **Format-compatibility rule, now evidenced three ways:** `mac_apt` reads **AFF4 and DMG**;
  **Autopsy reads neither AFF4 (E4) nor AD1 (O1)**. **No single tool reads every container — settle
  format compatibility before choosing an evidence set, not after.**
Sources: <https://github.com/sgan81/apfs-fuse> · <https://github.com/ydkhatri/mac_apt>

### P5 — ATT&CK: persistence, and the exfiltration mapping that is NOT room 26's

✅ **T1204.002** User Execution: Malicious File → **Execution** · **T1543.001** Launch Agent
(*"created with user level privileges and execute with user level permissions"*) → **Persistence,
Privilege Escalation** · **T1543.004** Launch Daemon (*"require elevated privileges to install, are
executed for every user on a system prior to login"*) → **Persistence, Privilege Escalation**.
⚠️ **Checked specifically: neither T1543 sub-technique carries the Stealth tactic**, despite the
TA0005 rename (**E11**) making that an easy wrong assumption.

🔴 **Exfiltration mapping — do not reuse room 26's.** An HTTP POST to **attacker infrastructure** is
**T1041 Exfiltration Over C2 Channel** — *"Adversaries may steal data by exfiltrating it over an
existing command and control channel"*. **T1567.002 is *Exfiltration to Cloud Storage*** and is scoped
to services like Dropbox, Drive or S3 (block **N1**, rclone → Mega). **The destination decides which,
not the protocol.**

### NOT VERIFIED — block P

- **`QuarantineEventsV2` population on macOS 26 (Tahoe).**
- **`LSQuarantineDataURLString` vs `LSQuarantineOriginURLString` semantics.**

---

## Q. Live-response tradecraft and stale ATT&CK in the wild (appended 2026-08-29, from room 29 — Windows Incident Surface)

🟢 **All of block Q is IN SCOPE.** Room 29 is the best `S2-02` (live response) source in the corpus,
and it was mis-filed as Priority 3 from its title alone.

### Q1 — 🟢🟢 The analyst's shell is attack surface — the rationale D17 was missing

A **PowerShell profile runs every time PowerShell starts** (**`T1546.013`**, PrivEsc + Persistence),
so **querying it with PowerShell means you have already executed it.** The room states the problem
exactly: *"this creates a chicken and egg problem for us."*

**The answer is bring-your-own-tools, and the reason is specific:** start with **`cmd.exe`**, which
*"unlike PowerShell, it does not require a profile to execute, therefore, making it immune to
execution flow hijack during startup."*

🔴 **Profile paths — search BOTH trees.** Microsoft's `about_Profiles` for **PowerShell 7**:
`$PSHOME\Profile.ps1` · `$PSHOME\Microsoft.PowerShell_profile.ps1` ·
**`$HOME\Documents\PowerShell\Profile.ps1`** · **`$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`**
(CurrentUserCurrentHost has highest precedence). **Windows PowerShell 5.1 uses
`Documents\WindowsPowerShell\` instead** — ⚠️ **NOT VERIFIED against Microsoft.**
**A host with pwsh installed therefore has eight candidate profiles, not four**, and a sweep that
checks one tree is incomplete.
⚠️ **Related and unchecked by the room: `PSModulePath`.** A writable directory prepended there gives
silent module hijack on every `Import-Module`, and looks like an ordinary path list.

🟢🟢 **For D17 / `S1-05` / `S2-02`:** our `CLEAN-TOOLS` snapshot currently exists as a convenience.
**This is its rationale.** ➕ **Two additions of ours:** publish the toolbox **hashes** so students
can verify their own tools, and keep the toolbox on **read-only media**, not on the subject's
Desktop. ⚠️ **And name the cost honestly, as the room does** — a trusted toolchain is degraded by
design (*"you might come across missing features … This is expected"*).
Sources: <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles> ·
<https://attack.mitre.org/techniques/T1546/013/>

### Q2 — 🔴🔴 WDigest `UseLogonCredential`: the artifact is live, the payoff is dead

`HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`, value **`UseLogonCredential`**,
DWORD. Setting **1** means *"the system will store cleartext credentials in LSA memory for the
Wdigest SSP"*; *"On Windows 8.1 and 2012 R2+, the default is 0."* **So 1 re-enables it.**

🔴 **But on a modern host it no longer yields plaintext.** Credential Guard restricts
*"WDigest (only SSO is blocked)"*, and **CG is on by default**: *"Starting in Windows 11, 22H2 and
Windows Server 2025, Credential Guard is enabled by default on devices which meet the requirements."*
Microsoft goes further: *"Cleartext passwords are not being stored in LSASS on modern Windows by
design, **even when `UseLogonCredential` is set to `1`**"*, and *"There is no supported process … to
'fully enable' WDigest on Windows 11 25H2."*

🟢🟢 **Teach it as a registry artifact and an intent indicator, not as a credential-dumping enabler**
— and note that **its presence is the finding**: *"the `UseLogonCredential` value does not exist"* by
default (⚠️ verified for Win7+KB2871997; **NOT VERIFIED** for Win10/11).
**ATT&CK maps it to `T1112` Modify Registry** (v3.0, **Defense Impairment + Persistence**), whose own
procedure text names this exact key and value. Follow-on collection is **`T1003.001`**.
⚠️ **Pairs with L4** — Credential Guard's five gates mean *"CG is on"* is itself an assumption to
check, not a given.
Sources: <https://learn.microsoft.com/en-us/archive/blogs/kfalde/kb2871997-and-wdigest-part-1> ·
<https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/considerations-known-issues> ·
<https://learn.microsoft.com/en-us/answers/questions/5869399/enable-wdigest-dont-work-on-windows-11> ·
<https://attack.mitre.org/techniques/T1112/>

### Q3 — 🔴🔴 Stale ATT&CK IDs in a current, popular room — the worked example for K1

**A free, 11,356-completion DFIR walkthrough authored in 2025 already cites two dead IDs and one with
changed tactics.** This is the evidence that **K1** is not a pedantic correction.

| the room cites | status Aug 2026 |
|---|---|
| **`T1070.001`** for clearing event logs | ❌ **moved — now `T1685.005`** (**K1**) |
| **`T1562.002`** for stopping the eventlog service | ❌ **`T1562` REVOKED into `T1685`** (**K1**) |
| **`T1574.007`** Path Interception by PATH Env Var | ✅ ID correct — 🔴 **v2.0 (12 May 2026), tactics now Stealth + Execution** |
| **`T1036.009`** "breaking process trees" | ✅ ID correct — 🔴 **current name is "Break Process Trees"** (v2.0, Stealth) |
| `T1546.013` PowerShell Profile | ✅ PrivEsc + Persistence |
| `T1546.007` Netsh Helper DLL | ✅ PrivEsc + Persistence |
| `T1552.002` Credentials in Registry | ✅ Credential Access |
| `T1070.003` Clear Command History | ✅ Stealth |
| `T1136` / `T1098` / `T1078` | ✅ Persistence / Persistence+PrivEsc / IA+Persistence+PrivEsc+**Stealth** |
| *(no ID given)* for `Winlogon\Userinit` and `Shell` | ➕ **`T1547.004` Winlogon Helper DLL** (Persistence + PrivEsc) — *"Winlogon\Userinit - points to userinit.exe … Winlogon\Shell - points to explorer.exe"* |

⚠️ It also writes tactic IDs sloppily — `TA008` for TA0008, and a bare `1546`.
🟢 **Use this table as an `S6-06` slide:** *this is a current, popular, free room, already wrong.*

### Q4 — 🟢🟢 The `Userinit` → `cmd` → `netsh` → helper-DLL chain

**The best-taught correlation chain in the corpus**, and worth reproducing exactly:

`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit` holds
`userinit.exe,` **plus an appended `cmd.exe`** → which silently launches `netsh.exe` → so check
**`HKLM\SOFTWARE\Microsoft\NetSh`** → where one DLL entry has **a different shape from every other**
(a relative `.\` path instead of a bare filename). **`T1546.007`** — *"The paths to registered
netsh.exe helper DLLs are entered into the Windows Registry at `HKLM\SOFTWARE\Microsoft\Netsh`."*

🟢🟢 **The transferable heuristic: the outlier in a list of similar entries is more informative than
any single entry.** ⚠️ **And the room is honest about why it works** — without the pattern it
*"can be a rabbit hole, as we'd need to have a firm knowledge of the default and native functionality
of the OS internals."* **The heuristic works because a baseline exists, not because the analyst is
clever.**

### Q5 — Sysinternals currency, and a disclosure trap

- 🟢 **Autoruns v14.3 (17 Jun 2026)** — current. Flags confirmed: **`-a b`** *"Boot execute."* ·
  **`-a l`** *"Logon startups (this is the default)."* · **`-h`** *"Show file hashes."*
- ⚠️ **PsLoggedOn v1.35** — page last updated **March 2021**, originally 2016. **Still shipping and
  still works, but do not present it as actively maintained.**
- 🔴 **Autoruns' VirusTotal integration is off by default and requires accepting the terms**
  (*"Before using VirusTotal features, you must accept the VirusTotal terms of service"*).
  **Submitting a client's file hashes is a disclosure decision, not a step** — same rule as **N1**.
  **The room does not raise it.**
- 🔴 **The room uses `Get-WmiObject`** for its process listing — **removed in PowerShell 6/7**
  (**F5**). Use `Get-CimInstance`. (It uses CIM everywhere else, so this is an inconsistency.)
- 🟢 **`Get-GPResultantSetOfPolicy -ReportType HTML` is still current** and documented for Windows
  Server 2025 — an under-used, cheap, complete snapshot of policy, which is where an adversary makes
  changes durable (**`T1484.001`**, **O6**).
Sources: <https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns> ·
<https://learn.microsoft.com/en-us/sysinternals/downloads/psloggedon>

### Q6 — 🔴🔴 A new class of safety defect: evidence that destroys itself when touched

**Defect #11**, and the first of its kind in the corpus. The room stages a PowerShell profile
containing `wevtutil el | ForEach-Object {wevtutil cl $_}; Stop-Service -Name "eventlog" -Force`.
**Opening PowerShell — the analyst's most natural first action — clears every event log on the
machine under investigation and stops the logging service**, and the profile also flips WDigest.

**The room's only warning is operational**, not evidential: *"if you haven't performed the previous
steps before executing PowerShell, please restart the VM."* ⚠️ **A restart does not restore cleared
logs.**

🟢🟢 **The staging is pedagogically correct — this is what a hostile host does. The defect is the
missing sentence.** **Our version:** state the consequence *before* the student touches anything, run
it on a rollback-able snapshot, and have the student **hash and record the profile before replacing
it** — the room's own `ren`/`copy` remediation fixes the host and destroys the provenance of the fix.

⚠️ **This breaks the L8 pattern.** The other six evidence defects were *"act on the live system
instead of collecting first"*; **this one is "the evidence destroys itself when you touch it"** — a
different category, and the only **deliberately staged** one.
**Running total: 11 defects — four endanger the analyst's machine, seven the evidence.**

### NOT VERIFIED — block Q

- The **Windows PowerShell 5.1** profile paths against a Microsoft source.
- Whether **`UseLogonCredential` is absent by default on Windows 10/11** specifically.

---

## Block R — the Priority-3 rooms (29–32), and the module boundaries they revealed

> 🔴🔴 **NAMING COLLISION — read this before citing anything in this block.** The project's hard
> rules are numbered **R1–R8**, and **R8 is "never reproduce a credential."** This is the first
> currency block whose letter is **R**, so `R5` and `R8` are now ambiguous on their own.
> **From here on, every reference to an item in this block must be written as "block R5",
> "block R8" — never bare.** Bare `R1`–`R8` always means the rule. Logged as **D42**.

**Written 2026-08-29, after rooms 30, 31 and 32.** Rooms 30 and 31 reference this block by name from
their §9. **Scope: the four skim rooms plus the two module rosters they gave us for free.**
⚠️ **Block R also carries the two corrections that closed NOT VERIFIED items in rooms 30 and 31** —
both have been patched into those notes, and both are recorded here as the authoritative version.

### R1 — 🟢🟢 The two module rosters, taken from the breadcrumb, not guessed

Two rooms gave us a full module membership list for the cost of one click, and **both are worth
keeping because our own module map was inferred from the path outline rather than read**.

**Disk Image Analysis** (from room 31, Task 6): Forensic Imaging · Autopsy · DiskFiltration ·
ExfilNode. ✅ Confirms rooms 16, 21 and 22 belong to that module.

**Memory Analysis** (from room 32's breadcrumb → module page), **in order**:

1. Memory Analysis Introduction — room 30 · **free**
2. Memory Acquisition — `memory-acquisition.md`
3. Volatility Essentials — `volatility-essentials.md`
4. Windows Memory & Processes — `windows-memory-and-processes.md`
5. Windows Memory & User Activity — `windows-memory-and-user-activity.md`
6. Windows Memory & Network — `windows-memory-and-network.md`
7. **Linux Memory Analysis** — ⚠️ **deliberately not extracted (D38)**; reconciled against the
   do-not-extract table in `_EXTRACTION_PROMPT.md`, where it is listed. **Not a gap.**
8. **Supplemental Memory** — room 32, **the capstone**

The module page also names its own prerequisites and successor: *"Need to know: Windows Endpoint
Investigation"* → **Memory Analysis** → *"Next steps: Disk Image Analysis"*. 🟢 **That ordering is
the reverse of ours** — we teach disk before memory. **Neither is wrong; but it is worth one
sentence in the instructor notes that the platform our students may also be using teaches it the
other way round.**
Sources: <https://tryhackme.com/module/memory-analysis> · room 31 Task 6

### R2 — 🔴🔴 Attrition measures the paywall before it measures difficulty

**Correction to my own method, recorded rather than deleted.** After the Honeynet module I read a
completion curve as a difficulty signal. The Memory Analysis module refutes that as a general rule:

| # | room | completions | step |
|---|---|---|---|
| 1 | Memory Analysis Introduction (**free**) | 13,179 | — |
| 4 | Windows Memory & Processes (premium) | 3,015 | 🔴 **−77%** |
| 5 | Windows Memory & User Activity | 2,511 | −17% |
| 6 | Windows Memory & Network | 2,382 | −5% |
| 8 | Supplemental Memory | 1,976 | −17% |

🔴🔴 **One commercial boundary accounts for more loss than four rooms of increasing difficulty
combined.** After the paywall the slope is shallow — **the module does not shed people as it gets
harder.**

🟢 **The Honeynet reading survives, for a stated reason:** all six of those rooms sit inside the
paywall, so no boundary confounds them. **Rule going forward: a completion curve is a difficulty
signal only across rooms of the same access tier.** ⚠️ **D40's carry-through design should be
calibrated on the Honeynet curve alone**, and any future use of completion counts must state the
tier.

### R3 — 🟢🟢 CLOSED: Guymager does not provide write blocking (room 31 #3)

**Refuted from the tool's own documentation**, closing a NOT VERIFIED item.
Homepage: ***"Guymager is a free forensic imager for media acquisition"***; features limited to
*"Generates flat (dd), EWF (E01) and AFF images, supports disk cloning"*. Man page:
***"Guymager should be run with root privileges, as other users do not have access to physical
devices normally"*** — **the opposite of a write blocker; it documents that the tool needs raw
device access.** A full-text search for *write block* / *write-block* / *write blocker* /
*write protect* returns **zero matches in either source**.
🔴 **Combined with E6 — NIST CFTT has never tested a Linux software write blocker — the correct
teaching line is: the imager never blocks; the blocker is a separate thing, and on Linux it is
untested.**
Sources: <https://guymager.sourceforge.io/> ·
<https://manpages.debian.org/testing/guymager/guymager.1.en.html>

### R4 — 🟢🟢 CLOSED: RAMMap is an analysis tool, not an acquisition tool (room 30 #3)

Microsoft Learn: ***"RAMMap is an advanced physical memory usage analysis utility for Windows Vista
and higher"***, used *"to analyze application memory usage, or to answer specific questions about
how RAM is being allocated."* **The page contains no claim that RAMMap writes a memory image or
dump file.** Room 30 lists it among tools that *"can be used to generate full or selective memory
captures"*; **that is unsupported by the vendor's own description.**
⚠️ **Still open from the same row: `/dev/mem` / `CONFIG_STRICT_DEVMEM` restrictions** — asserted
from general knowledge in both passes, never checked against a kernel source. **Do not slide it.**
Source: <https://learn.microsoft.com/en-us/sysinternals/downloads/rammap>

### R5 — 🔴🔴🔴 The PsExec service name is a command-line parameter, and this breaks a taught signature

**The single most useful currency finding in the Priority-3 set.** Room 32 teaches
`services.exe → psexesvc.exe → payload` as **the** PsExec signature, with no caveat.

Microsoft Learn, PsExec parameter table: ***"-r  Specifies the name of the remote service to create
or interact with."*** **The service name is operator-supplied.** A one-flag rename defeats a
string-matching detection, and **the documentation for defeating it ships with the tool.**

⚠️ **NOT VERIFIED — the default service name.** Microsoft's PsExec page documents the rename switch
but **never states the unmodified default anywhere**; a full-text search for `PSEXESVC` in any case
returns zero hits on that page. 🔴 **Do not print `psexesvc.exe` on a slide as "the" name without a
source.**

🟢🟢 **The durable formulation, which needs no default name at all:** *an unfamiliar service binary
spawned directly by `services.exe`, correlated with a remote logon.* **A signature that names a
string has a shelf life; a signature that names a structure survives the rename.** This is figure
**F45** and §5.2 of `supplemental-memory.md`, and it is the cheapest available demonstration of the
whole course's argument about detection engineering.
Source: <https://learn.microsoft.com/en-us/sysinternals/downloads/psexec>

### R6 — ⚠️ The three lateral-movement lineages have three different source strengths

**Room 32 presents all three as equivalent facts. They are not, and our slides must not either.**

| lineage | strength | source |
|---|---|---|
| **WinRM** → `wsmprovhost.exe` | 🟢🟢 **first-party, explicit** | Microsoft PowerShell docs: *"WS-Management establishes a connection and uses a plug-in for PowerShell to start the PowerShell host process (Wsmprovhost.exe) on the remote computer."* |
| **WMI** → `svchost.exe` → `wmiprvse.exe` → payload | ⚠️ **first-party partial + community for the full chain** | MS Learn confirms only the hosting relationship, in a **troubleshooting KB**: *"the CPU is consumed by the WmiPrvse.exe process, and there are a few instances where svchost.exe hosting the WMI service (Winmgmt) is consuming high CPU usage."* The spawn relationship is stated only by a community DFIR source: *"The process WmiprvSE.exe is what spawns the process defined in the CommandLine parameter of the Create method."* |
| **PsExec** → `services.exe` → `psexesvc.exe` → payload | 🔴 **defeated by a documented flag (block R5); default name undocumented** | see block **R5** |

🟢 **Teach all three — and mark the provenance on the slide.** ⚠️ **The habit being taught is not the
three strings; it is asking "how do I know this?" of a signature before deploying it.**
Sources: <https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/powershell-remoting-faq> ·
<https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/troubleshoot-wmi-high-cpu-issues> ·
<https://threathunterplaybook.com/hunts/windows/190810-RemoteWMIExecution/notebook.html> ⚠️ **secondary**

### R7 — 🟢 `windows.getsids` — a plugin the corpus was missing, and it is fully offline

Volatility 3 **v2.28.0**, plugin `volatility3.plugins.windows.getsids`, class `GetSIDs`:
***"Print the SIDs owning each process."*** `--pid` is a documented optional list filter.

🟢🟢 **The property worth teaching is that it needs nothing outside the image.** SID→name resolution
uses a **bundled well-known-SID table** plus the **`Microsoft\Windows NT\CurrentVersion\ProfileList`
key read from the hives inside the memory image** — no live host, no separately exported hive, no
network lookup. **That makes it safe on an air-gapped workstation, unlike the symbol download (D2).**

⚠️ **Two caveats to state with it:**
- **An unresolved SID is a paging outcome, not a finding** — if the `ProfileList` data is not
  resident, the SID prints raw.
- **It reports the token, which may have been stolen** (`T1134`). **"Running as" is not "launched
  by".** 🔴🔴 And room 32's own scenario is the counter-example it never draws: **the account's
  credentials were stolen from another host, so every artifact bearing that SID is evidence of a
  credential, not of a person.**
Sources: <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.getsids.html> ·
<https://pypi.org/project/volatility3/>

### R8 — 🟢 ATT&CK spot-check for the memory capstone, at v19.2

All current, none deprecated or revoked (**L7** — cite the version, not the date):
`T1021.002` SMB/Windows Admin Shares (v1.3) · `T1047` Windows Management Instrumentation (v1.6) ·
`T1021.006` Windows Remote Management (v1.2) · `T1003.001` OS Credential Dumping: LSASS Memory
(v1.5) · `T1134.004` Access Token Manipulation: Parent PID Spoofing (v2.0) · `T1036` Masquerading
(v2.0).

🟢 **Room 32 is the only room in the last four with no stale technique ID** — rooms 29 (**Q3**) and
30 both cite dead IDs. ⚠️ **Which is a data point for K1/L7 and not a reason to relax: the room
that happens to be current today is current by luck, not by a maintenance process.**
Source: <https://attack.mitre.org/resources/updates/>

### R9 — 🔴 The pattern the four skim rooms share: doctrine ages worse than technique

**Rooms 29–32 produced one safety defect between them and five factual errors** — and **every one of
the errors is in a *doctrinal* statement, not in a command**:

- room 31 — *"use MD5 and SHA-1"* (doctrine) · *"Guymager provides write blocking"* (product claim) ·
  inverted history (narrative)
- room 30 — RAMMap listed as a capture tool (product claim) · a revoked ATT&CK ID beside its live
  replacement (reference)
- room 32 — a service name taught as a signature (doctrine)

🟢🟢 **Not one is a broken command.** The commands in all four rooms run. **What has rotted is the
advice around them** — which is exactly the failure mode a course inherits invisibly, because
students copy the sentence, not the syntax. ⚠️ **And the most-recommended room in the whole
extraction (room 31, 305 recommends) carries three of the six.** **Popularity is not currency**, and
that sentence has now earned its place in `S1-06`.

### NOT VERIFIED — block R

- **PsExec's default remote service name** (block **R5**) — absent from Microsoft's page.
- **The full WMI spawn chain against a first-party source** (block **R6**) — community source only.
- **`/dev/mem` / `CONFIG_STRICT_DEVMEM` restrictions** (block **R4**) — carried over from room 30,
  unattempted in this pass.
- **The history of cold vs live forensics** (room 31 #2) — carried over, unattempted.
- **Room 32's artifact claims against actual plugin output** — the lab VM was not started.
