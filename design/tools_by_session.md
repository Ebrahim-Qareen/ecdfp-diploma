# tools_by_session.md — the forensic tool set, session by session

**Built 2026-08-29.** Every version and licence below was verified against the vendor's own page or
repository on that date. **This file supersedes the `Tools/` folder in the training Drive**
(`Resources/DRIVE/drive-inventory.md`).

**Two rules this file exists to enforce:**

1. 🔴🔴 **Licence before capability.** A tool students cannot legally use after the course is a tool
   we have mistaught. **D37** was written when KAPE turned out to bar commercial use. **This pass
   found two more of the same shape** — one already in the Drive folder, one waiting one version
   ahead. See §1.
2. ⚠️ **Version-bind every command we teach** (**M6**, **L7**). A command is only correct against a
   stated version.

---

## 1. 🔴🔴 Read this first — three tools that cannot be shipped as they are

### 1.1 RegRipper 4.0 is the next KAPE, and we were about to walk into it

The Drive ships **RegRipper3.0-master.zip**, which is **MIT-licensed and fine**. 🟢

🔴🔴 **But active development has moved to RegRipper 4.0, and its licence says:**

> ***"This version is free for personal and academic (college/university) use ONLY. RegRipper4.0 may
> not be included in vendor products, vendor training, nor in any distribution."***

**ITGate Academy is a paid training provider. "Vendor training" and "any distribution" are exactly
what we do.** 🔴 **So: stay on RegRipper 3.0, and record why.** New plugins and the MITRE ATT&CK
mappings land in 4.0 — **that is a capability we decline on licence grounds, not an oversight.**

⚠️ **This is the second tool in this course to carry that clause, and nobody flagged it.** The
lesson is **D48**: check the licence of the *next* version, not only the one in hand.
Source: <https://github.com/keydet89/RegRipper4.0> · 3.0 licence:
<https://github.com/keydet89/RegRipper3.0>

### 1.2 010 Editor is commercial software — 30-day trial only

The Drive ships **010EditorWin64Installer15.0.1.exe**. SweetScape's licence:
***"effective for 30 days following the date you install the Software"***. **There is no free tier.**

🔴 **Do not distribute it to students.** 🟢 **HxD does everything this course needs from a hex
editor and is free for commercial use** (§2, S3). **Use HxD; mention 010 Editor as the paid option
professionals often buy.**
Source: <https://www.sweetscape.com/010editor/manual/License.htm>

### 1.3 Xiao Steganography has no living vendor

The Drive ships **xiao-steganography-2-6-1-es-en.exe**. 🔴 **No working author site could be found**
— every copy available is a third-party mirror, and those mirrors date the release to **2010 or
earlier**.

⚠️ **NOT VERIFIED: whether it triggers AV detections or ships bundled installers.** No authoritative
source was found either way and rumour is not repeated here. **But the absence of any vendor site is
itself the finding:** we would be asking students to run an unsigned Windows executable, sourced
from a download mirror, on a machine they use for coursework. 🔴 **Do not distribute it.**
🟢 **If steganography is taught at all, `zsteg`, `stegsolve`, `binwalk` or plain `exiftool` +
`strings` cover it with live, sourceable projects** — and **`S3-08`'s point is the concept, not the
tool.**

---

## 2. The tool set, session by session

**Legend — Role:** 🟢🟢 **CORE** (taught and examined) · 🟢 **SUPPORTING** (used in a lab) ·
⚠️ **MENTION** (named, not used).
**All versions verified 2026-08-29. Re-verify before each session build (M6).**

### S1 — Forensic Foundations, Evidence Integrity & Chain of Custody

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| `sha256sum` / `Get-FileHash` | OS built-in | — | 🟢🟢 **CORE** | 🔴 **The whole of `S1-06`.** **K7**: MD5 and SHA-1 answer *"have we seen this file before?"*; only SHA-2/SHA-3 answer *"is this file unaltered?"* **Record MD5 if a corpus publishes one; attest to SHA-256.** |
| `md5sum` | OS built-in | — | ⚠️ **MENTION** | **Taught as a lookup key only, and explicitly not as an integrity control.** Room 31 recommends it for integrity and is the counter-example (see the lab catalogues). |
| A text editor + a manifest | — | — | 🟢🟢 **CORE** | `S1-07`. **The chain of custody is a document, not a tool** — no software produces it, and that is the lesson. |

🟢 **No installers needed for S1.** That is worth saying to students on day one: **the most important
session in the course needs no forensic software at all.**

### S2 — Acquisition: Disk, Memory & Live Response

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| **FTK Imager** | **8.3** (Exterro) | 🟢 Free | 🟢🟢 **CORE** | *"delivers reliable data imaging and preview, completely for free."* 🔴 **The Drive ships 4.7.3.81 — several majors stale.** ⚠️ **And there is a separate PAID "FTK Imager Pro" — do not download that one by mistake.** |
| **Arsenal Image Mounter** | **3.13.368** | 🟢 Free Mode / paid Pro | 🟢 **SUPPORTING** | *"If Arsenal Image Mounter is run without a license, it will run in 'Free Mode' and provide core functionality."* ⚠️ **BitLocker handling, VM launch and Recon reports are Professional-tier.** Drive ships 3.11.303 — stale. |
| **OSFMount** | **3.3.1000** | 🟢 Free, commercial use OK | 🟢 **SUPPORTING** | PassMark confirm redistribution: *"no cost and you can distribute the complete unmodified binary package as you want."* 🟢 **The safest mounting tool to hand students.** |
| `dd` / `dcfldd` | OS | GPL | ⚠️ **MENTION** | **A5**: `dd` is no longer the recommendation for damaged media. **A6**: `dc3dd` is dormant, not dead. |
| **Volatility 3** | **2.28.2** | VSL | 🟢🟢 **CORE** (acquisition context) | 🔴🔴 **NOT IN THE DRIVE FOLDER.** **D2**: first run downloads symbols — **on an air-gapped lab it fails, it does not merely wait. Ship the symbol pack.** |

| **BriMor Live Response Collection** | current build | 🟢 Free | 🟢🟢 **CORE** | The collector the old build refused to name. `Windows_Live_Response.bat`, menu: Triage / Memory / Complete / Secure-Complete. ⚠️ **Free, but not licensed for commercial use** — name **Velociraptor** (Apache 2.0) as the alternative wherever that matters. |
| **Velociraptor** | 0.75 | 🟢 Apache 2.0 | 🟢 **SUPPORTING** | Free for commercial use, which BriMor is not. Offered alongside, not instead. |
| **WinPmem** | `winpmem_mini_x64_rc2` | 🟢 Apache 2.0 | 🟢🟢 **CORE** | Memory capture. ⚠️ **A capture smaller than installed RAM is truncated, not compressed** — size is the completeness check, and it is the S2 quiz answer. |
| **DumpIt** | Magnet, current | 🟢 Free | ⚠️ **MENTION** | One-click alternative to WinPmem; no options, which is the point and the limitation. |
| `hdparm` | OS (Linux) | GPL | 🟢🟢 **CORE** | `hdparm -N <dev>` reports `max sectors = reported/true`. **Run it before the imager, never after** (`S2-07`). |

🔴 **Nothing in either the Drive kit or any external lab teaches acquisition as a decision.**
**D46**: not one of CyberDefenders' 82 free labs does it either. **`S2-01`–`S2-05` and `S2-09` are
ours alone.**

### S3 — Data Representation & File Examination

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| **HxD** | **2.5.0.0** | 🟢 *"free of charge for private and commercial use"* | 🟢🟢 **CORE** | **The hex editor for this course.** ⚠️ Last updated **2021** — stable, not abandoned, but say so rather than being caught out. **Replaces 010 Editor (§1.2).** |
| **ExifTool** | **13.59** | 🟢 Artistic / GPL | 🟢🟢 **CORE** | `S3-05` metadata. Drive ships 13.22 — stale. 🟢🟢 **Pair it with `secretrendezvous.docx`** (`drive-inventory.md`): a 2009 internal timestamp under a 2026 upload date is a ready-made *"which date is the evidence?"* exercise. |
| `file` / TrID | OS / current | 🟢 Free | 🟢🟢 **CORE** | `S3-02`, `S3-03` — signature versus extension. |
| **CyberChef** | web, current | 🟢 Apache 2.0 | 🟢 **SUPPORTING** | Decoding chains. 🟢 Runs offline from a local copy — **worth shipping for an air-gapped room.** |
| `oledump` / `olevba` | current | 🟢 Free | 🟢 **SUPPORTING** | Document macros. **The CyberDefenders `Obfuscated` lab uses exactly these — and `sha256sum`, not `md5sum`.** |
| ~~Xiao Steganography~~ | — | 🔴 **no vendor** | 🔴 **DROP** | §1.3. |

### S4 — Storage Devices, Partitions & File Systems

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| **Autopsy** | **4.23.1** | 🟢 Apache 2.0 | 🟢🟢 **CORE** | 🔴🔴 **NOT IN THE DRIVE FOLDER**, and it is the single most-used tool in the course. ⚠️ **O1: Autopsy cannot open AD1.** **E4**: neither VDI nor AFF4. **Match the format to the tool, every time.** |
| **MFTECmd** | **0.5.0.1** | 🟢 MIT | 🟢🟢 **CORE** | `$MFT`, `$UsnJrnl`, `$LogFile`. 🟢 **Install via `Get-ZimmermanTools`** — the vendor's own method: *"Use Get-ZimmermanTools to download all programs at once and keep your tool set current."* **Better than shipping a frozen zip.** |
| **TestDisk / PhotoRec** | 🟢 **stable 7.2** | 🟢 GPL v2+ | 🟢🟢 **CORE** | `S4-07` partition recovery, `S3-07` carving. 🔴 **The Drive ships `7.3-WIP` — and 7.3 is STILL work-in-progress in Aug 2026.** ⚠️ **Ship the 7.2 stable release, not the beta.** A course does not teach on a beta. |
| The Sleuth Kit | current | 🟢 Free | 🟢 **SUPPORTING** | `mmls`, `fls`, `istat` — the command-line view behind Autopsy's GUI. |

⚠️ **E5, and four of the corpus's seven evidence defects:** `-o ro` is **necessary and not
sufficient** — mounting still writes mount count, mount time, `s_last_mounted` and atimes, and
**replays the journal on a dirty image**. Use `ro,noload,noatime` over `losetup -r`, and **prefer a
tool that cannot write at all.**

### S5 — Windows Forensics: Registry, User Activity & Execution

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| **RegRipper 3.0** | 3.0 | 🟢 MIT | 🟢🟢 **CORE** | 🔴🔴 **Stay on 3.0. Do NOT move to 4.0 — see §1.1.** 🟢 The Drive's `RegRipper-plugins.csv` becomes the `S5-02` handout. |
| **Registry Explorer** | current | 🟢 MIT | 🟢🟢 **CORE** | Zimmerman. Transaction-log replay is the reason to prefer it over a raw hive read. |
| **AppCompatCacheParser** | current | 🟢 MIT | 🟢🟢 **CORE** | `S5-06` ShimCache. ⚠️ **ShimCache records presence, not execution** — the CyberDefenders `Sysinternals` lab teaches it without saying so. |
| **PECmd** / **LECmd** | current | 🟢 MIT | 🟢🟢 **CORE** | Prefetch (`S5-05`), LNK and jump lists (`S5-04`). |
| **Timeline Explorer** | current | 🟢 MIT | 🟢 **SUPPORTING** | Meets students early on a small dataset, then carries into `S6-05`. |
| Event Log Explorer / `evtx_dump` | current | mixed | 🟢 **SUPPORTING** | ⚠️ **Check the licence of the GUI before distributing; the CLI parsers are safe.** |

🔴🔴 **L1 — state this once, loudly:** the 4688 command-line field needs **two** switches and is
**off by default**. **On most hosts there is nothing to corroborate a command line against.**

### S6 — Network Forensics, Timelines, Reporting & Capstone

| Tool | Version | Licence | Role | Why, and the catch |
|---|---|---|---|---|
| **Wireshark** | **4.6.8** | 🟢 GPL v2 | 🟢🟢 **CORE** | 🔴🔴 **NOT IN THE DRIVE FOLDER.** `S6-02`, `S6-03`. |
| **Volatility 3** | **2.28.2** | VSL | 🟢🟢 **CORE** | `S6-10`. 🔴🔴 **NOT IN THE DRIVE FOLDER.** ⚠️ **M1: `windows.cmdline` reads the PEB, which the process can rewrite.** ⚠️ **M4: run `pslist` AND `psscan`, and diff.** 🟢 `windows.getsids --pid N` is fully offline. |
| **NetworkMiner** | **3.1** | 🟢 Free / $1300 Pro | 🟢 **SUPPORTING** | 🔴 Drive ships **2.9 — two majors behind.** ⚠️ **The free edition cannot parse PcapNG, has no packet carver and no CSV/Excel/JSON export.** **Teach the capture format around that limit, or the lab breaks.** |
| **plaso / log2timeline** | current | 🟢 Apache 2.0 | 🟢🟢 **CORE** | `S6-05` super-timeline. |
| **Brim / Zui** | current | 🟢 Free | ⚠️ **MENTION** | Used by three CyberDefenders labs; worth naming so students recognise it. |

---

## 3. What to actually ship students

**One folder, and it is not the Drive's.**

| Keep from the Drive (update first) | Add — currently missing | Drop |
|---|---|---|
| FTK Imager → **8.3** | 🔴🔴 **Autopsy 4.23.1** | 🔴 010 Editor (§1.2) |
| ExifTool → **13.59** | 🔴🔴 **Wireshark 4.6.8** | 🔴 Xiao Steganography (§1.3) |
| NetworkMiner → **3.1** | 🔴🔴 **Volatility 3 2.28.2** + **symbol pack** (D2) | ⚠️ `chellenge.rar` — unopened, unnamed, unknown |
| Arsenal Image Mounter → **3.13.368** | **Get-ZimmermanTools** (PECmd, LECmd, AppCompatCacheParser, Registry Explorer, Timeline Explorer) | |
| TestDisk → 🔴 **7.2 stable**, not the WIP beta | **plaso**, **CyberChef** (offline copy) | |
| HxD 2.5.0.0 ✅ · OSFMount 3.3.1000 ✅ · MFTECmd ✅ · RegRipper **3.0 only** ✅ | | |

🔴🔴 **The three tools the course depends on most — Autopsy, Volatility 3 and Wireshark — are not in
the kit at all**, while a paid hex editor and an abandoned steganography tool are. **That is the
headline: the kit is not stale so much as mis-aimed.**

## 4. Sources and open items

**Verified 2026-08-29** — SweetScape licence · Arsenal Recon downloads + README · ExifTool history +
README · Exterro FTK downloads · mh-nexus HxD licence · EricZimmerman/MFTECmd + ericzimmerman.github.io ·
Netresec NetworkMiner feature table · PassMark OSFMount forum · keydet89 RegRipper3.0 **and 4.0** ·
cgsecurity TestDisk download + wiki · volatilityfoundation/volatility3 + PyPI · sleuthkit/autopsy
releases · wireshark.org download + FAQ.

### NOT VERIFIED

- ⚠️ **Xiao Steganography's AV-detection and bundled-installer status** (§1.3). No authoritative
  source either way. **The recommendation to drop it rests on the absent vendor, not on a
  malware claim.**
- ⚠️ **RegRipper 3.0's formal deprecation status.** New plugins land in 4.0, but **3.0 carries no
  deprecation notice.** Our position is a licence choice, not a currency claim.
- ⚠️ **Event Log Explorer's licence** — GUI tools in that space are often paid. **Check before it
  goes in the student kit.**
- ⚠️ **`chellenge.rar`** in the Drive `Tools/` folder — **not opened, contents unknown.** The name is
  misspelled and it sits among installers. **Ask what it is before anyone runs it.**
- ⚠️ **No tool in this file has been installed or run in this pass.** Versions and licences are from
  vendor pages; **behaviour is not re-tested.**
