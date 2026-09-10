# Instructor delivery audit — Eng. Mohab Mustafa's eCDFP, 8 sessions

**Audited 2026-09-06.** Content-volume and pedagogy audit of the previous instructor's delivered
course, for the rebuild.

**Sources read in full:** the eight condensed notes in `knowledge_base/instructor/`
(`Session_01` … `Session_08`) plus `README.md`, cross-checked against the nine raw OCR files in
`knowledge_base/_source_text/Instructor_Session_*.md` (7,483 lines). Where the condensed note and
the raw OCR disagree, the raw OCR is cited. Slide-level claims below are traceable to a numbered
slide in the raw text.

**What this is not.** It is not a summary of what he taught — the notes already do that. It is an
answer to four questions: how much content is really there, what shape it was delivered in, how
good it is, and how many minutes it represents against the rebuilt 6 x 220 min (`D1`, `D26`).

---

## 0 · Headline volume table

Counts are of *delivered* content, evidenced by a slide or screenshot. Announced-but-not-shown
items are counted separately in the "phantom" column, because that distinction is the single most
important finding in this audit.

| # | Session | Slides | Shots | Teaching topics | Demos | Labs (real) | Labs (phantom) | Challenges | Answer keys | Est. minutes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | Introduction & Acquisition | 70 | 30 | ~29 | 1 | 5 | 2 | 0 | — | **180–200** |
| 02 | Data Representation & File Examination | 38 | 24 | ~11 | 2 | 5 | 1 | 2 | 0 | **130–150** |
| 03 | Disks & File Systems | 40 | 21 | ~19 | 2 | **0** | **3** | 1 (CTF) | 0 | **120** evidenced |
| 04 | Practical Windows Forensics pt 1 | 39 | 30 | ~8 | 0 | 7 | 0 | 0 | — | **175–190** |
| 05 | Practical Windows Forensics pt 2 | 23 | 18 | ~2 | 0 | 8 (4 new) | 0 | 1 | 0 | **100** (60–70 new) |
| 06 | Network Forensics | 72 | 52 | ~40 | 2 | 2 | 0 | 1 (7 pcaps) | 0 | **190–200** |
| 07 | Log & Timeline Analysis (2 decks) | 68 | 44 | ~37 | 9 | 0 | 0 | 0 | — | **190–200** |
| 08 | Reporting & CTF | 30 | 23 | ~21 | **0** | **0** | 0 | 1 (absent) | 0 | **65–75** |
| | **Total** | **380** | **242** | **~167** | **16** | **27** | **6** | **6** | **0** | **~1,150–1,190** |

**Read three columns together and the course's real problem appears.** 27 real labs is a strong
number. 6 phantom labs — announced on an agenda slide and never shown — is a lot. **Zero answer
keys, for six challenges, is the finding.** Not one exercise he set has a recorded expected answer,
marking scheme or solution slide anywhere in the source set.

---

## 1 · Per-session content volume

### Session 01 — Introduction to Digital Forensics & Acquisition
`Session 1.pdf` · 70 slides · 30 screenshots · INE units 1 + 2

**Topics in his order** (slide ranges from `Session_01…md` §1):

1. Cybercrime · forensic science · definition of digital forensics (9–15)
2. Crime scene vs evidence — *"the crime scene is the device, the evidence is the data"* (14)
3. Public vs private investigations, with examples (15)
4. The three fundamentals — evidence, tools, scientific method (16–20)
5. Digital evidence life cycle — acquire / chain of custody / analyse / present (21–27)
6. Sources of evidence; volatile vs non-volatile; live vs static (28–31)
7. Five analysis steps: image → verify → preserve → analyse → validate (32–39)
8. Forensic soundness (39)
9. What acquisition is, why we acquire, never work the first image (40–43)
10. Order of volatility — **one bullet, no ordered list** (44)
11. Acquisition methods: disk-to-disk, disk-to-image (46)
12. RAW vs proprietary image formats; EWF / IDIF / sgzip named (47)
13. Source/destination swap warning (48)
14. Sparse acquisition (49)
15. Write protection (50)

~29 distinct teaching points across 42 concept slides. Then one continuous lab, slides 51–69.

| Metric | Count |
|---|---|
| Demos | 1 — portable FTK Imager build (53) |
| Labs | 5 — physical image + verify (54–57) · RAM capture (58–59) · logical drive + AD1 folder (60–61) · mount three ways (62–66) · KAPE triage (67–69) |
| Phantom labs | 2 — `dd` imaging and HashCalc validation, both on the slide-52 objective list, neither shown |
| Challenges | 0 graded. One rhetorical question with no on-slide answer (59, *"Can we verify ram image ?"*) |
| Case narrative | **None** |

**Tools with real invocations:**

| Tool | Version | Command / action as delivered |
|---|---|---|
| FTK Imager | 4.7.3.81 | `File > Create Disk Image` > Physical Drive > `\\.\PHYSICALDRIVE1`; fragment 1500 MB, compression 0, *Verify images after they are created* ticked |
| PowerShell | — | `Get-FileHash MDS` **(OCR; likely `Get-FileHash '.\hard drive.001' -Algorithm MD5`)** |
| FTK Imager | 4.7.3.81 | `File > Capture Memory…` (dialog itself not on slide) |
| FTK Imager | 4.7.3.81 | `File > Image Mounting`, Mount Method `Block Device / Read Only` |
| Arsenal Image Mounter | — | four mount modes incl. `Disk device, write original` |
| OSFMount | — | Mount Virtual Disk > `\\.\PhysicalDrive<n>`, `Properties: Read-only` |
| gkape (KAPE GUI) | 1.3.0.2 | `.\kape.exe --tsource C: --tdest F:\ --tflush --target KapeTriage --gui` |

### Session 02 — Data Representation & File Examination
`Session 2.pdf` · 38 slides · 24 screenshots · INE unit 3

**Topics in his order:** digital data / binary (5) · ASCII table (6) · data representation, RGB,
video as frames (7) · HDD vs SSD "logically the same" (8) · cluster allocation (9) · what deletion
does (10–11) · when data is really gone (12) · file structure header/data/EOF (13) · header as
metadata, EXIF named (14) · magic bytes (15) · disk carving + Gary Kessler table (16) ·
closing principle *"digital forensics is not about just using tools"* (38). **~11 topics.**

| Metric | Count |
|---|---|
| Demos | 2 — `xxd` on a JPEG (15) · Explorer Properties + ExifTool (18–19) |
| Labs | 5 — HxD raw view + signature analysis + Kessler lookup (21–23) · `$I`/`$R` Recycle Bin recovery with FTK Imager + read-only mount (25–26) · TestDisk partition repair (27–29) · PhotoRec carving (30–32) · Xiao steganography (33–36) |
| Phantom labs | 1 — *"Automated file analysis with autopsy"* is on the slide-17 agenda; slide 37 gives only a download link |
| Challenges | 2 — **EXIF GPS: name the city the photo was taken in** (20) · **identify the extension of these files** (24). Both distributed by Google Drive link. No answer key for either. |

**Tools:** `xxd website.jpg | head` → `ffd8 ffe0 0010 4a46 4946` · ExifTool (output shown, command
not on slide) · HxD · FTK Imager 4.7.3.81 · TestDisk 7.3-WIP `testdisk_win.exe` · PhotoRec 7.3-WIP
`photorec_win.exe` → `recup_dir.1` + `report.xml` · Xiao Steganography · Autopsy (named only).

### Session 03 — Disks & File Systems
`Session 3.pdf` · 40 slides · 21 screenshots · INE units 4 + 5

**Topics in his order:** where evidence is stored (5–6) · HDD components (7) · platters → tracks →
sectors, the 63-sector note (8–9) · SSDs "complex", "handle carefully or evidence inadmissible"
(10–12) · disk vs volume vs partition (13) · partitioning schemes (14) · MBR limits — 4 primaries,
2 TB (15) · MBR sector layout 446/64/2 (16) · MBR vs VBR placement (17) · GPT — 128 partitions,
UEFI (19) · GPT LBA layout with backups (20) · file systems defined (24–25) · FAT family 12/16/32/
exFAT (26) · cluster worked example (27) · FAT32 reserved area (28) · FAT deletion and `0xE5`
(29–31) · NTFS 13 features (32) · NTFS system files in WinHex (33) · NTFS metadata table (34) ·
`$MFT` record structure (35). **~19 topics — 472 pages of INE source in 40 slides.**

| Metric | Count |
|---|---|
| Demos | 2 — corrupted GPT in hex, `EFI PART` at offset `00000200` (22–23) · WinHex NTFS system-file listing (33) |
| Labs | **0 delivered** |
| Phantom labs | **3** — slide 18 (analyse MBR with 010 Editor; fix a corrupted MBR) · slide 21 (analyse GPT with 010 Editor; fix a corrupted GPT) · slide 36 (fix file system with TestDisk; recover with PhotoRec; analyse `$MFT` with MFTECmd). Named, no steps, no evidence file, no screenshots. |
| Challenges | 1 — *"CTF Time"* (38) with a Google Forms submission link (39). **No brief, no questions, no evidence, no scoring.** |
| Homework | Build a Windows 10 VM before next session (40) |

**Tools:** WinHex (shown) · 010 Editor (named on both lab agendas, never on screen) · MFTECmd
(named, never shown here).

### Session 04 — Practical Windows Forensics, part 1
`session 4.pdf` · 39 slides · 30 screenshots · INE unit 6

**Topics in his order:** NTFS metadata files in WinHex (5–6) · MFT record structure (7) · the four
Windows evidence sources — NTFS, Registry, Event Logs, Other artifacts (8) · the **"PWF: Disk
Analysis Process" roadmap** (9) · ADS concept (11) · where the hives live (19) · registry as
*"the black box of your Windows machine"* (20). **~8 topics.** Everything else is hands-on.

| Metric | Count |
|---|---|
| Demos | 0 as a separate class — the whole back half is lab |
| Labs | 7 — ADS hide (11–12) · TestDisk (13) · PhotoRec (14) · KAPE triage (15) · MFTECmd (16–18) · **Registry Explorer 15-step walk (19–36)** · RegRipper (37–39) |
| Registry walk steps | **15 numbered steps, one key per slide** |
| Challenges | **0.** No wrap-up slide either — the deck stops on the bulk one-liner. |

**Tools with real invocations:**

```
notepad file.txt
notepad file.txt:secret
.\kape.exe --tsource C: --tdest "D:\kape image" --tflush --target KapeTriage --gui
mkdir output
MFTECmd.exe -f $MFT --csv output --csvf parsed_mft.csv
MFTECmd.exe -f $MFT --de 92530
rip.exe -r registries/SYSTEM -p timezone
rip.exe -r registries/SYSTEM -p del
for /r %i in (*) do (rip.exe -r %i -a > %i.txt)
```

Registry Explorer 2.0.0.0 · Timeline Explorer 2.0.0.1 · MFTECmd 1.2.2.1 · KAPE 1.3.0.2 ·
RegRipper 3.0 · TestDisk/PhotoRec 7.3-WIP · Excel.

**Keys actually opened:** `ComputerName` · `Windows NT\CurrentVersion` · `TimeZoneInformation` ·
`Tcpip\Parameters\Interfaces\{GUID}` · `Control\Windows\ShutdownTime` · `Windows Defender` ·
`ProfileList\<SID>` · `Enum\USBSTOR` · `Services` · `FirewallPolicy\FirewallRules` · `SAM\Users` ·
`CurrentVersion\Uninstall` · `CurrentVersion\App Paths`.

### Session 05 — Practical Windows Forensics, part 2
`session 5.pdf` · 23 slides · 18 screenshots · INE unit 6

**Ten of twenty-three slides are repeats of session 4** (4, 5, 6, 8, 9, 10, 11, 13, 14, 15) — the
same screenshots, not merely the same topics.

| Metric | Count |
|---|---|
| Topics | ~2, both repeats (evidence sources; process roadmap) |
| Labs | 8 total, **4 genuinely new** — BAM (16) · Amcache (17) · UserAssist (19) · MRU family (20–23). The other four are recap (8–10), RegRipper bulk (11–12), MFTECmd (13–15), firewall (18). |
| Challenges | 1 — *"Windows forensics challenge (find serial of connected usb)"* on the agenda slide (7), evidence at an `easyupload.io` link. **Set, never walked. No answer key, no evidence description, no marking scheme.** |
| Numbering defects | `#4` used on both slides 12 and 13; `#9` never appears |

**Keys opened:** `bam\State\UserSettings\<SID>` (117 rows) · `Amcache.hve\Root\InventoryApplication`
· `NTUSER.DAT\…\Explorer\UserAssist` (226 rows) · `RunMRU` · `Office\<ver>\<app>\User MRU\
LiveId_<hash>\File MRU` · `Place MRU` · `WinRAR`.

### Session 06 — Network Forensics
`session 6.pdf` · 72 slides · 52 screenshots · INE unit 7 — the longest deck in the course

**Sixty slides of fundamentals before the first lab.** Topics in his order: OSI model (4) · PDU per
layer (5) · client-server (6) · unicast/multicast/broadcast (7) · switch L2 (8–9) · router L3 (10) ·
protocol metadata (11) · application layer (12) · transport layer (13) · ports and the well-known
range (14–17) · **ephemeral source ports** (18) · TCP vs UDP (19) · three-way handshake with
sequence arithmetic (20) · handshake in Wireshark (21) · UDP segment (22) · data link (23) ·
48-bit MAC = OUI + NIC (24) · common protocols (25–26) · HTTP in the clear (27) · GET/POST (28) ·
request anatomy (29–30) · response codes 1xx–5xx (31) · HTTPS as `Application Data (23)` (32–33) ·
symmetric vs asymmetric (34) · hash functions (35) · SSL/TLS (36) · SMTP verbs (37–39) · FTP
cleartext (40) · SSH (41) · DNS and record types (42–43) · DHCP (44–45) · ICMP (46–47) · ARP (48) ·
**OSCAR, six steps** (49–55) · acquisition and wiretapping by medium (56–58) · rogue DHCP, port
scanning, MAC flooding, ARP poisoning (59–63). **~40 topics.**

| Metric | Count |
|---|---|
| Demos | 2 — handshake in a live capture (21) · `arp -a` (48) |
| Labs | 2 — live Wireshark capture and save as pcapng (65–67) · work a challenge pcap: filter, recover chat + username, extract an email attachment, verify in HxD, repeat in NetworkMiner (68–72) |
| Challenges | 1 set — `evidence01.pcap` … `evidence07.pcap`, distributed by `easyupload.io` link (64). **No answer key. Almost certainly the LMG Security / forensicscontest.com "Ann's Bad AIM" corpus** — which *does* have a published key, if the provenance confirms. |

**Tools:** Wireshark 4.4.1 · display filter `ip.addr == 192.168.1.158` (the **only** filter in
72 slides) · HxD · NetworkMiner · `arp -a`.

### Session 07 — Log & Timeline Analysis (delivered in two parts)
`session 7 part 1.pdf` 47 slides + `session 7 part 2.pdf` 21 slides · 44 screenshots · INE units 8 + 9

**Part 1 topics:** why logs matter (4) · what a log / log message is (5–7) · stimuli differ by
source (8) · message types (9) · text log formats (10) · database transaction logs (11) · locating
logs (12) · filtering and normalization (13) · central logging interface (14) · web logs (15–16) ·
**Apache combined format walked field by field** (17–18) · `mod_log_forensic` (19) · Windows event
logs (20) · Security channel (21) · **the `eventlog` registry key with `MaxSize`/`Retention`** (22) ·
legacy/modern event ID table (23) · syslog facility codes (24–25) · severity codes (26) · Cisco
device configuration (27).

**Part 2 topics:** sequence beats single event (4–5) · what belongs in a timeline (6) · two
approaches — super timeline vs the Carvey targeted approach (7–10) · temporal proximity (11–12) ·
time formats, FILETIME and Unix (13) · MACB in NTFS and FAT (14–16) · **two Windows time-rules
matrices** (17–18) · timestomp detection (19). **~37 topics across both decks.**

| Metric | Count |
|---|---|
| Demos | **9** — Event Viewer filter on 4624 (29–31) · DeepBlueCLI (32–33) · IIS feature install + W3C log + field dialog (34–37) · `cat`/`grep`/`cut` pipeline (38–41) · Apache XSS (43) · Apache SQLi (44) · FTP daemon log (45) · PostgreSQL transaction log (47) · FTK Imager Export Directory Listing (pt2 s20) |
| Labs | **0 student labs.** All nine are instructor-driven demos; part 1 slide 28 says "Lab time" and what follows is screen work. |
| Challenges | 0. A standing announcement of the closing CTF sits on pt1 s1–2. |
| Timeline tools run | **Zero.** No plaso, no `log2timeline`, no `fls`, no `mactime`, no Timeline Explorer. Part 2 teaches timeline theory and never builds a timeline. |

**Tools and commands:**

```
.\DeepBlue.ps1 .\security.evtx
cat scanresult.txt
cat scanresult.txt | grep report
cat scanresult.txt | grep report | cut -d" " -f5        # printed as -d""
cat access.log | grep or
head postgresql-8.3-main.log.1
```

Event Viewer (`Filter Current Log` → Event ID `4624`) · DeepBlueCLI (from a `-master` folder, no
URL anywhere) · IIS 10.0 · Notepad · FTK Imager.

### Session 08 — Reporting & CTF Challenge
`session 8.pdf` · 30 slides · 23 screenshots · INE unit 10

**Pure lecture. No tool, no command, no software screenshot anywhere in the deck.**

**Thirteen numbered reporting tips** (6–19), one per slide: time management · references must be
current · reporting is not a stage after the work · provide reasoning · avoid absolute terms · have
a template · structured document · use the past tense · avoid 25–30 word sentences · **write down
what you did not do, and why** · avoid jargon · one term per concept · one date/time format
throughout.

**Eight report sections** (21–30): cover/title page · table of contents · executive summary ·
objective · evidence · analysis · crime reconstruction · conclusion. Closing slide 30:
*"Don't state your opinion unless asked — you are not the judge."*

| Metric | Count |
|---|---|
| Topics | ~21 |
| Demos / Labs | **0** |
| Challenges | The deck is titled *Reporting & CTF Challenge* and **contains no challenge at all** — no brief, no evidence manifest, no questions, no scoring, no key |

---
## 2 · His structure — the repeating shape of a session

### The pattern

**`admin (course outline + "we are here") → concept block → "Lab time" divider + objective list →
continuous tool run → [sometimes] challenge link → [sometimes] homework → closing principle`**

It is remarkably consistent. Six of the eight decks open with the same three or four slides —
course outline, session title, and an **evidence-lifecycle "we are here" marker** that highlights
which phase of `acquire → analyse → present` the session sits in. That orientation slide is the
best structural habit in the whole set and it is free to copy.

### The actual section headings, quoted

The dividers are almost always bare, and that bareness is itself the pattern — the slide is a
signpost, not content:

```
Lab time                                    (S01 s51, S02 s17, S03 s18/s21/s36, S07pt1 s28)
Evidence acquire lab                        (S01 s51)
Lab objectives                              (S01 s52)
LAB time                                    (S02 s17)
Practical windows forensics Lab time        (S04 s10, S05 s7)
CTF Time                                    (S03 s38)
Required in next session                    (S03 s40)
Part 1 : introduction to digital forensics  (S01 s8)
Part 2 : data acquisition                   (S01 s40)
```

And the objective list under the divider, verbatim from `Instructor_Session_01…md` slide 52:

```
Lab objectives
• Creating a portable version of FTK
• Using FTK imager to capture RAM
• Using FTK imager to capture image of suspect drive
• Capturing image for a logical folder
• Validating image using FTK imager and HashCalc
• Mounting image using FTK, OSFMount and arsenal image mounter
• Imaging using linux dd utility
• Using Eric Zimmerman tool KAPE to collect KAPE Triage
```

Same shape at `Session 4` slide 10 and `Session 5` slide 7, each ending with a **resources line** —
usually a GitHub cheat-sheet URL.

### How he opens

- Slides 1–4 of nearly every deck: course outline → session title → **evidence-lifecycle position
  marker**. Session 1 additionally spends slides 3–6 on his own credentials and certificates.
- No recap of the previous session. No stated learning outcomes. No entry question.

### How he closes

Inconsistently, and this is a real weakness:

- **S01 s70 and S02 s38** close on the same refrain — *"digital forensics is not about just using
  tools, you must follow a scientific procedure."* Strong, and worth keeping.
- **S03 s38–40** closes on CTF + submission form + homework.
- **S04** has **no wrap-up slide at all** — it stops mid-lab on the RegRipper one-liner.
- **S05** ends on a barely legible WinRAR screenshot.
- **S06** ends on the NetworkMiner lab slide.
- **S07 pt2 s21** is a bare "Close".
- **S08 s30** has the best closing slide in the course: *"Don't state your opinion unless asked."*

So: two of eight sessions close deliberately. Four just stop.

### Theory → demo → lab → challenge?

**Partly, and it degrades over the course.** The clean form appears in sessions 1, 2 and 6:
concept block, then a labelled lab block, then (in 2 and 6) a challenge with a download link.
Sessions 4 and 5 collapse into pure lab with almost no concept and **no challenge in session 4 at
all**. Session 7 is concept → demo with no student lab. Session 8 is concept only.

**Demos and labs are not distinguished.** There is no point at which the deck says "now you try."
Everything from the "Lab time" divider onward is the instructor at the keyboard; whether students
followed along is not recorded anywhere in the slides.

### Case narratives and carry-through

**There is no case narrative anywhere in the eight sessions, and no case is carried across
sessions.** This is the largest single pedagogical gap in the delivery.

- Every lab runs against whatever was attached to the presenter's machine at the time — his own
  `C:`, his own RAM, his own home network, a scratch 1 GB VMware disk.
- Nothing motivates a lab step with a question. Students image a disk because the slide says to.
- No finding, interpretation or "cannot prove" statement is written down in **any** of the eight
  sessions. The registry walk in session 4 opens fifteen keys and states no conclusion about any
  of them.
- The only continuity between sessions is tool continuity: KAPE output collected in session 4 is
  still open in session 5.

The closest thing to a narrative is session 6's challenge pcap, where a suspect IP and a person
named "Ann" give the lab a subject — and that narrative is borrowed from a public corpus, not
written by him.

---

## 3 · Quality assessment

Ratings are deliberately blunt. **Depth** is against what INE's corresponding unit covers.

| # | Session | Depth | Examples | Labs | Challenges | One-line verdict |
|---|---|---|---|---|---|---|
| 01 | Intro & Acquisition | **Adequate** | Adequate | **Strong** | **Absent** | The best lab sequence in the course, hung on nothing |
| 02 | Data Rep & File Exam | **Adequate** | **Strong** | **Strong** | Adequate (no keys) | Widest lab block per slide; misses the whole malicious-document half of the unit |
| 03 | Disks & File Systems | **Thin** | Adequate | **Absent** | **Absent** | 472 INE pages in 40 slides, three phantom labs, one excellent demo |
| 04 | Windows Forensics pt 1 | **Strong** | **Strong** | **Strong** | **Absent** | A competent tour that is not yet an investigation |
| 05 | Windows Forensics pt 2 | Adequate | **Strong** | Adequate | **Absent (unwalked)** | Richest artifacts in the course, thinnest treatment of them |
| 06 | Network Forensics | **Strong** (theory) / **Thin** (forensics) | Adequate | Adequate | Adequate (no keys) | Three hours of networking, forty minutes of network *forensics* |
| 07 | Log & Timeline | **Strong** (logs) / **Thin** (timelines) | **Strong** | **Absent** (demos only) | **Absent** | Nine real demos, and a timeline session that never builds a timeline |
| 08 | Reporting & CTF | Adequate | **Thin** | **Absent** | **Absent** | Excellent craft advice, never practised, and the CTF does not exist |

### What is GOOD and must be copied

**Session 01 — the continuous acquisition lab (slides 51–69).** Image → verify → capture RAM →
image logically → mount → triage, unbroken, in one sitting. This is already almost exactly the
shape the rebuilt `S2` needs. The three-tool mounting comparison (FTK / Arsenal / OSFMount) is
better than anything in INE because **Arsenal's dialog puts "write original" on screen as a
selectable option** — write-protection taught as a decision the analyst can get wrong.

**Session 01 — the KAPE block.** A real command line, the target name, and console output showing
target de-duplication and the 257/272 catalogue counts. INE names no triage tool at all. ⚠ but see
`D37`/`D48`: KAPE's licence bars commercial use, so this is a **teaching asset with a licence
problem**, not a drop-in.

**Session 02 — the paired recovery demonstration.** `$I`/`$R` Recycle Bin recovery (name survives,
because the file-system record survives) immediately followed by PhotoRec carving (files come back
named `10011328.jpg`, by offset, with no path and no timestamp). Two labs, one lesson, back to
back. **This pairing is the single best piece of teaching design in the eight sessions.**

**Session 03 — the corrupted-GPT hex walkthrough (slides 22–23).** A disk overwritten with a
repeating `41`, then `EFI PART` found at offset `00000200`, then the primary header placed beside
its backup at the end of the disk. INE shows GPT structurally and never shows a damaged one. Best
original demo in the deck set.

**Session 04 — the "PWF: Disk Analysis Process" roadmap (slide 9).** A single slide that maps the
whole Windows unit: System & User Information (Registry) · File Analysis (NTFS) · Evidence of
Execution (BAM, ShimCache, Amcache, Prefetch) · Persistence (Run Keys, Startup Folder, Scheduled
Tasks, Services) · Event Log Analysis. It is a curriculum on one page and students can navigate by
it. Keep the slide; **deliver the right-hand column, which he never does.**

**Session 04 — deleted registry data shown twice, two ways.** Registry Explorer reporting `5,958`
and `30,680` unassociated deleted values on hive load, and RegRipper's `del` plugin printing
recovered key and value names. INE asserts deleted registry records are recoverable; this is the
only place in the course a student watches it happen.

**Session 04 — the `ProductName` trap.** Build `22631`, `DisplayVersion 23H2` — Windows 11 — with
`ProductName` reading `Windows 10 Home` and `CurrentVersion` frozen at `6.3`. A free, current,
exam-shaped teaching point sitting on a real screenshot.

**Session 05 — BAM (slide 16).** 117 rows of per-binary, per-SID last-execution times, with device
namespace paths (`\Device\HarddiskVolume3\…`), packaged apps as family names, and a textbook
installer-execution chain through `AppData\Local\Temp\is-*.tmp\…setup.exe`. Unit 6 does not teach
BAM at all.

**Session 05 — the SAM vs ProfileList pairing (slide 33).** *"A user is added to profilelists if it
have been already logged using GUI before."* Corrected, that is the actual lesson of two separate
registry steps and it is one sentence long.

**Session 06 — the manual-then-automated pattern.** Carve the attachment by hand in HxD, then do
the same job in one click with NetworkMiner. The order is right and the course should use it
everywhere.

**Session 06 — the live QUIC/DNS capture (slide 66).** Real, current traffic that is almost
entirely opaque, with **one readable DNS query in it**. The best available argument for why DNS and
flow metadata now carry the investigation. (Must be re-shot — it is his home network.)

**Session 07 — DeepBlueCLI (pt1 s32–33).** One command turns a 34,000-record Security log into
three named detections (`4672` repeated admin logons, `4732` group addition, `4720` user creation).
Not in units 8–10 anywhere.

**Session 07 — the IIS field-selection dialog (pt1 s37).** Ticking which W3C fields get recorded,
live. It makes *"a column that is not in `#Fields:` was never recorded"* something students watched
rather than read. Excellent.

**Session 07 — the three-command pipeline (pt1 s38–41).** `cat` → `grep` → `cut` reducing nmap
output to four bare IPs. The same three commands work on an exported `.evtx` or a plaso CSV.

**Session 07 — the two Windows time-rules matrices (pt2 s17–18).** Operation-by-operation (rename,
local move, volume move, copy, access, modify, creation, deletion) against `$STANDARD_INFORMATION`
and `$FILE_NAME`. Nothing equivalent in INE. ⚠ **These are SANS DFIR poster graphics** — the OCR
shows the SANS "COMPUTER FORENSICS and INCIDENT RESPONSE" mark on both. Attribution and licence
must be settled before reuse, and the OCR of both is destroyed so they have to be re-derived from
the original SANS reference.

**Session 08 — tips 5, 10 and slide 30.** *Avoid absolute terms* · *write down what you did not do,
and why* · *don't say "in my opinion Mr X committed this crime" — you are not the judge.* This is
the plainest statement of findings-vs-interpretation (`D7`) anywhere in the source material, in
language a first-week student understands.

**Session 08 — tip 3.** *Reporting is not a stage that comes after the work; never reverse-engineer
the report.* That is the argument for `D20`'s per-session report, delivered by the previous
instructor himself.

### What is WEAK, missing or wrong

**1 · Six challenges, zero answer keys.** Not one exercise he set has a recorded expected answer,
marking scheme or solution slide. The EXIF-GPS city task, the identify-the-extension set, the
session 3 CTF, the USB-serial challenge and the seven network captures are all set and none is
resolved anywhere in the source. Three of the five were distributed via **Google Drive or
`easyupload.io` links that are single points of failure and are probably already dead.**

**2 · The CTF does not exist.** The deck titled *Reporting & CTF Challenge* contains no challenge.
Session 3 ends on "CTF Time" plus a Google Form. Competitive exercises clearly ran; **none of the
material is in the source set.** `S6-09`'s capstone has no prior art and must be built from
scratch. *Ask the instructor directly whether a separate CTF brief file exists.*

**3 · Six phantom labs.** Session 3 announces MBR repair, GPT repair and an `$MFT`/MFTECmd
walkthrough and shows none of the three. Session 1 lists `dd` imaging and HashCalc validation as
lab objectives and shows neither. Session 2 promises Autopsy and gives a download link.
**Do not plan a session build against his lab-agenda slides.**

**4 · Topics stated and never demonstrated.** Beyond the phantom labs:
- **ShimCache** is in the session 5 slide-16 *title* and on the agenda; `…\Session Manager\
  AppCompatCache` is never opened and `AppCompatCacheParser` never runs. The promised ShimCache/BAM
  contrast — the whole point of the slide — is not delivered.
- **Prefetch** is on the roadmap slide in both sessions 4 and 5. No `PECmd`, no `.pf` file, ever.
- **ShellBags** is on the session 5 agenda. Never shown. No `SBECmd`.
- **RecentDocs** is visible in the tree at session 5 slide 20 and never opened.
- **The entire persistence column of his own roadmap** — Run keys, Startup folder, Scheduled Tasks
  — is never delivered in either Windows session. (`Services` is the one exception.)
- **`NTUSER.DAT` and `USRCLASS.DAT`** are named on session 4 slide 19 and not loaded until session 5.
- **The whole super-timeline toolchain.** No plaso, no `log2timeline`, no `fls`, no `mactime`, no
  body file, no TLN format. Part 2 of session 7 teaches timeline theory and builds no timeline.
- **Log clearing** — event IDs `1102`/`104`/`517` appear nowhere, despite an Event Viewer demo
  sitting next to the topic.

**5 · Labs with no evidence file.** Almost every lab in sessions 1, 4, 5 and 7 runs against the
**presenter's own live machine** — his `C:`, his RAM, his home network, his Office MRU. There is no
prepared evidence set anywhere in the course except the borrowed pcaps and two Google-Drive file
sets. This is why the reuse cautions are so long, and it is why nothing he ran is reproducible.

**6 · No finding is ever written down.** Fifteen registry keys opened in session 4, and no
statement of what any of them establishes. Defender's two `Disable*` values sit at `0` on screen —
"AV was not switched off" is a finding and it is never made. The install-date clustering in
`Uninstall` is a readable timeline and he does not point at it. **The eCDFP exam tests exactly this
and the course never rehearses it.**

**7 · Outright technical errors to correct before reuse:**

| Where | Error | Correction |
|---|---|---|
| S01 s35 | Defines "triage" as *"creating three images of the evidence"* | Triage is scope reduction. His own s67 uses the word correctly. Teach the practice as "redundant copies". |
| S02 s8 | HDD and SSD *"logically the same"* | True for the file system, false for recoverability. **TRIM is never named in the whole course.** |
| S03 s10 | SSDs — *"handle carefully or you might find your evidence inadmissible"* | Wrong vocabulary. The controller destroys data independently of the analyst. Teach TRIM and garbage collection. |
| S03 s15 | MBR *"can only handle disks up to 2TB"* | State the reason — a 32-bit LBA field at 512-byte sectors — or students memorise a number. |
| S04, S05 | `ControlSet001` read directly throughout | `Select\Current` decides which control set was live. INE is the course's truth. |
| S06 s35 | AES, DES and RC4 listed as *"common cryptographic algorithms"* under the heading **Hash function** | All three are ciphers. A student who confuses hashing with encryption fails criterion 1 of the rubric. |
| S06 s34 | RSA *"the most used cryptographic algorithm nowadays"* | Dated — ECDHE/ECDSA dominate TLS. |
| S07 pt2 s19 | Timestomp rule stated as `$STD_INFO > $FILE_NAME` | **Backwards for the common case.** Backdating makes `$STANDARD_INFORMATION` *earlier*. Teach: divergence in either direction is the signal, and the finding is "an inconsistency exists". |
| S07 pt2 s15 | Mnemonic given as **MCAB** | Every tool column, INE and Module 05 use **MACB**. Needless trap. |
| S07 pt1 s17/s42 | Apache log at `/var/www/apache2/logs` | Contradicted by his own screenshots at s43–44, which show `/var/log/apache2`. |
| S07 pt1 s45 | Slide titled *"Investigating RCE exploit"* | The screenshot is anonymous FTP logins from two different lab subnets. Title and evidence do not match. |
| S07 pt1 s31 | The demonstrated `4624` is **logon type 5** (service) | The "who logged on" lesson lands on a service account, and logon types are never defined. |
| S05 s13 | Titled *"analyzing $MFT with MFTEparser"* | No such tool. The screenshot is MFTECmd. |
| S08 s8 | *"no known remote exploits on Windows 7"*, vulnerability found *"earlier this year"* | Written in 2025, means EternalBlue/MS17-010 from 2017. The slide's own drift proves its own point about stale references. |
| S08 s27 | *"the report may be refused in court"* | Jurisdiction-dependent. State the principle without asserting a legal outcome. |

**8 · Outdated and licence-blocked tools.** Pinned across the decks: FTK Imager **4.7.3.81**
(current is 8.3), KAPE **1.3.0.2**, MFTECmd **1.2.2.1**, Registry Explorer **2.0.0.0**, Timeline
Explorer **2.0.0.1**, RegRipper **3.0** with plugins dated `v.20090727`–`v.20230710`,
TestDisk/PhotoRec **7.3-WIP** (a beta — stable is 7.2, per `D49`), Wireshark **4.4.1**, nmap
**7.01**, PostgreSQL **8.3**, IIS **10.0** samples from 2017, host OS **Windows 10 21H1** (out of
support). Two tools must be dropped outright per `D49`: **010 Editor** (paid, and it carries two of
session 3's phantom labs) and **Xiao Steganography** (abandonware, no living vendor). Nobody ever
asks whether `bam v.20200427` parses a 2024 BAM layout correctly.

**9 · Personal data is everywhere.** Slide-level lists are in §6 of each note. The worst three:
**S05 s21** — Office File MRU listing sixteen full paths into his private working tree, exposing
other clients' and other courses' material by name, with a `LiveId_<hash>` Microsoft-account
identifier. **S07 pt1 s32** — DeepBlueCLI printing his **personal email address** as the detected
username. **S06 s66** — a live capture of his own home network with real MACs and a Google
account-login DNS query. Also: **S01 s53** shows a pinned `mimikatz-master` folder on screen during
an evidence-handling lesson. Only **sessions 3 and 8 are clean.**

**10 · Volume is badly distributed against the syllabus.** Session 6 spends ~128 minutes on
networking fundamentals — material this cohort already has from CCNA and eCIR
(`session_time_estimates.md` §1) — and ~40 minutes on network forensics. Session 3 spends 40 slides
on the two INE units (4 + 5, 156 KB of source) that `session_time_estimates.md` identifies as
**genuinely new to these students**. The compression is applied in exactly the wrong places.

---
## 4 · Volume calibration — the key number

### Method

Minutes are estimated from delivered slide type, not from slide count alone:
**admin ≈ 0.5 min · concept ≈ 2.0–2.5 min · demo ≈ 4–6 min · lab step ≈ 5–8 min**, with lab blocks
costed against the actual work on screen (a 1 GB image takes 63 s in his own log, plus setup and
narration). Phantom labs are costed at **zero** because there is no evidence they were run.

### Per session

| # | Session | Admin | Concept | Demo | Lab | **Evidenced total** | As a slot |
|---|---|---:|---:|---:|---:|---:|---|
| 01 | Intro & Acquisition | 12 | 84 | 5 | 83 | **184** | ~3 h |
| 02 | Data Rep & File Exam | 5 | 26 | 10 | 90 (incl. 15 challenge) | **131** | ~2 h 15 |
| 03 | Disks & File Systems | 5 | 72 | 15 | 30 (CTF only) | **122** | ~2 h |
| 04 | Windows Forensics pt 1 | 5 | 20 | 0 | 151 | **176** | ~3 h |
| 05 | Windows Forensics pt 2 | 10 | 5 | 0 | 86 | **101** | ~1 h 45 |
| 06 | Network Forensics | 4 | 128 | 8 | 60 | **200** | ~3 h 20 |
| 07 | Log & Timeline (pt1+pt2) | 8 | 100 | 86 | 0 | **194** | ~3 h 15 (over 2 sittings) |
| 08 | Reporting & CTF | 5 | 63 | 0 | 0 | **68** | ~1 h 10 |
| | **Total** | **54** | **498** | **124** | **500** | **~1,176 min** | **~19.6 h** |

### The calibration that matters

**~19.6 hours of evidenced content across 8 sessions ≈ 147 min per session.** If the original slots
were three hours, he ran at roughly 82 % fill — plausible, with the balance going to the off-deck
CTF blocks, questions and setup.

**8 sessions × ~3 h ≈ 24 h. The rebuild is 6 × 4 h = 24 h (`D1`).** The total is the same. This is
not a compression problem, it is a **repackaging** problem — with three real exceptions:

1. **Session 5's duplication is free money.** Ten of twenty-three slides are literal repeats of
   session 4. Merging 04 + 05 into one `S5` costs nothing to remove and recovers **~40 minutes**.
2. **Session 6's fundamentals are free money for *this* cohort.** ~128 minutes of OSI/TCP/HTTP/DNS/
   DHCP/ARP that CCNA and eCIR already delivered (`session_time_estimates.md` §1 verified this
   against the built courses on disk). Moving slides 4–48 to pre-work recovers **~110 minutes** and
   is the only option that preserves the labs.
3. **Sessions 3 and 8 are under-built, not over-built.** 122 and 68 evidenced minutes against
   INE units that need far more. Session 3 in particular carries three phantom labs where the
   rebuilt `S4` needs real ones.

**Net:** roughly **150 minutes** are recoverable from duplication and cohort-redundant theory, and
roughly **150 minutes of new build** are required (session 3's three phantom labs, ShimCache,
Prefetch, ShellBags, the whole plaso toolchain, the capstone, and six answer keys). **They very
nearly cancel.** The rebuild is not short of time — it is short of *evidence sets and answer keys*.

### His 8 sessions against INE's 10 units

| INE unit | Source size | Instructor session | Relationship |
|---|---:|---|---|
| 01 Introduction to Digital Forensics | 58 KB | **S01** (slides 8–39) | **Two units compressed into one session** |
| 02 Data Acquisition | 67 KB | **S01** (slides 40–69) | ↑ same session; unit 2 gets the whole lab |
| 03 Data Representation & Files Examination | 64 KB | **S02** | 1:1 — but ~120 pages of malicious-document analysis dropped |
| 04 Disks | 46 KB | **S03** (Part 1, slides 5–23) | **Two units compressed into one session** |
| 05 File Systems | **111 KB** | **S03** (Part 2, slides 24–36) | ↑ same session. 156 KB of source → 40 slides. **The worst compression in the course.** |
| 06 Windows Forensics | **148 KB** | **S04 + S05** | **One unit split across two sessions** — the only split, and correct: it is the largest unit |
| 07 Network Forensics | 133 KB | **S06** | 1:1, but 3/4 of the session is pre-requisite networking, not forensics |
| 08 Log Analysis | 37 KB | **S07 part 1** | **Two units across one session delivered in two parts** |
| 09 Timeline Analysis | 21 KB | **S07 part 2** | ↑ nominally its own deck; no tool ever run |
| 10 Reporting | 18 KB | **S08** | 1:1, lecture only |

**Compressions (2 INE units → 1 session):** S01 (units 1+2), S03 (units 4+5), S07 (units 8+9 —
mitigated by the two-part delivery).
**Split (1 INE unit → 2 sessions):** S06 Windows Forensics → S04 + S05.

**The mismatch to carry into the rebuild:** he gave **one session** to units 4 + 5 (156 KB, and the
material `session_time_estimates.md` flags as *genuinely new* to this cohort) and **one session** to
unit 7 (133 KB, three-quarters of which this cohort already knows). Invert that weighting.

---

## 5 · Reusable assets

Ranked by value. "Lift" = usable with light editing. "Rebuild" = the idea is good, the artefact is not.

### Tier 1 — lift, with regenerated screenshots

| Asset | Where | Note |
|---|---|---|
| **Continuous acquisition lab sequence** — image → verify → RAM → logical/AD1 → mount → triage | `Session_01…md` §2, slides 51–69 | Already the shape `S2` needs. Add an evidence set and a chain-of-custody form. |
| **Three-tool mount comparison**, Arsenal's four write modes on screen | S01 slides 62–66 | Best write-protection teaching aid in the source set |
| **`$I`/`$R` recovery paired with PhotoRec carving** | `Session_02…md` §2, slides 25–32 | Two labs, one lesson: name survives vs name does not. **Copy the pairing exactly.** |
| **Corrupted-GPT hex walkthrough**, `EFI PART` at `00000200`, primary beside backup | `Session_03…md` §2, slides 22–23 | Best original demo in the deck set. Maps to `S4-05`/`S4-10`. |
| **"PWF: Disk Analysis Process" roadmap** | `Session_04…md` slide 9 | A curriculum on one page. Keep the slide, deliver the persistence column he skipped. |
| **BAM table** — 117 rows, device-namespace paths, installer chain in `Temp\is-*.tmp` | `Session_05…md` §2 Lab 4, slide 16 | Only per-SID last-execution table in the course. Re-shoot on lab evidence. |
| **Manual-then-automated pattern** — HxD carve then NetworkMiner | `Session_06…md` §2 Lab 2, slides 70–72 | Use this ordering everywhere in the rebuild |
| **DeepBlueCLI triage** — 34,000 records → three named leads in one command | `Session_07…md` §2, pt1 s32–33 | **Must be re-shot** — his personal email is in the output |
| **`cat` → `grep` → `cut` pipeline** | S07 pt1 s38–41 | Three processes from "a file I cannot read" to "a list I can count" |
| **IIS W3C field-selection dialog** | S07 pt1 s34–37 | Makes "a field not in `#Fields:` was never recorded" a thing students watch |
| **The 13 reporting tips**, one per slide | `Session_08…md` §2, slides 6–19 | Directly reusable as a student handout and a pre-submission self-check |
| **The 8-section report structure** | S08 slides 21–30 | Maps almost exactly onto the `D20` four-criterion rubric — see the crosswalk in `Session_08…md` §2 |

### Tier 2 — quotable lines and analogies

- *"A crime scene in digital forensics is the electronic device; the evidence is the data stored,
  transmitted and processed inside it."* — S01 s14. Clean, and it survives translation.
- *"Digital forensics is not about just using tools, you must follow a scientific procedure."* —
  S01 s70 and S02 s38, his closing refrain. Use it as the course's own.
- **"The registry is the black box of your Windows machine."** — S04 s20.
- *"Don't say 'in my opinion Mr. X has committed this crime.' You are not the judge."* — **S08 s30.**
  **Use verbatim in `S1`**, on the day the report template is introduced — not in the last session
  where it currently sits.
- *"Remember that the analysis is the investigator's interpretation of the evidence and not an
  absolute truth."* — S08 tip 5.
- *"Write down what you have not done, and why."* — S08 tip 10. Rarely taught; it is criterion 4's
  limitations requirement.
- *"Reporting is not a stage that comes after the work — never reverse-engineer the report."* —
  S08 tip 3. This is the argument for `D20`, made by the previous instructor.
- *"A case is assigned with a scope and objective, not only the evidence."* — S08 s25. Feeds `S1-06`.
- **The SAM vs ProfileList distinction** — S05 s33: SAM lists every account, ProfileList only those
  that have interactively logged on. One sentence, two registry steps.
- **"The metadata is files."** — implied by S03 s33's WinHex listing. Say it out loud: registry
  hives are files too, which is why you cannot locate one without the file system.

### Tier 3 — lab scenarios and challenge questions worth rebuilding

| Scenario | Origin | What it needs |
|---|---|---|
| **"Find the city this photo was taken in"** (EXIF GPS) | S02 s20 | Re-host the image, write the key. Excellent 10-minute opener. |
| **"Identify the extension of these files"** — 12 renamed/corrupted files, "File Type Analysis Part 1" | S02 s24 | Strong `EVS-05` candidate. Route through `ecdfp-evidence` for licence + hashing. |
| **"Find the serial of the connected USB"** | S05 s7 | Re-host evidence, name the artifact family in the question, write the key. Self-contained take-home. |
| **`evidence01`–`evidence07` network captures** | S06 s64 | Almost certainly the **LMG Security / forensicscontest.com "Ann's Bad AIM"** corpus — which has a published answer key. Confirm provenance, link the original publisher, do not re-host. |
| **Renamed-file signature hunt in HxD** — `File02` resolving to MHTML from its opening bytes | S02 s21–23 | The `X-MimeOLE`/`Subject:`/`Date:` header is a genuinely satisfying reveal |
| **XSS and SQLi in an Apache access log** | S07 pt1 s43–44 | Real 2024-dated evidence on a DVWA host. `grep or` also matching every URL containing "or" is a *better* lesson than a clean hit. |
| **PostgreSQL unclean shutdown and recovery** | S07 pt1 s47 | A database writing its own timeline, in the host's local zone — the normalisation problem, demonstrated |

### Tier 4 — diagrams described in the text (rebuild as SVG per `design_system.md` §5)

- **Evidence life cycle "we are here" marker** — appears in six of eight decks. Adopt as a standing
  page element.
- **MBR sector layout** — 446 code / 64 partition table / 2 signature, as a 512-byte strip (S03 s16).
- **GPT LBA layout** — Protective MBR (LBA 0) → Header (LBA 1) → Table (LBA 2) → … → Backup Table
  (LBA n−1) → Backup Header (LBA n) (S03 s20).
- **FAT cluster allocation** — 4 sectors/cluster, `file1` 512 B and `file2` 1024 B drawn onto the
  sector grid. This is the slack-space setup and he never uses the word (S03 s27).
- **FAT deletion before/after** — `Pic.jpg` → `_ic.jpg`, cluster chain unchanged (S03 s30–31).
- **NTFS metadata-file table** — records 0–11 with purpose (S03 s34). Correct `$Extended` → `$Extend`
  and `22-15` → 12–15.
- **TCP three-way handshake with real numbers** — `SYN seq:100` / `SYN-ACK seq:200 ack:101` /
  `ACK seq:101 ack:201`, with the state machine annotated (S06 s20).
- **Central logging interface** — log server fed by router, switch, firewall, application server
  (S07 pt1 s14).
- **Windows time-rules matrices ×2** — ⚠ SANS poster graphics; re-derive from the original SANS
  reference, settle attribution, and do not transcribe the destroyed OCR.
- **Report-structure spine**, 8 sections mapped to the 4 rubric criteria (S08 s21–30).

### Explicitly NOT reusable

- Every hash digest in session 1 (the same MD5/SHA-1 pair resolves differently three times).
- Session 5 slide 21 (Office File MRU) — client confidentiality, in any form.
- Session 7 pt1 s32 (DeepBlueCLI) — personal email address in the output.
- Session 6 s66 — live home-network capture.
- Session 1 s53 — Explorer view with a pinned `mimikatz-master` folder.
- Session 3 slide 40's homework (build a Windows 10 VM) — superseded by `D17`.
- 010 Editor and Xiao Steganography — dropped by `D49`.
- Session 5 slides 20, 22, 23 (RunMRU, Place MRU, WinRAR) — values panes are illegible; re-shoot.
- Session 7 pt2 s17–18 as OCR'd — both matrices are destroyed.

---

## 6 · What to ask the instructor

1. **Does a CTF brief exist as a separate file?** Session 3 ran one, session 8 is titled for one,
   and neither deck contains any of it. This is the only prior art for `S6-09`.
2. **Are the answer keys anywhere?** Six challenges, none resolved in the source set.
3. **Where did `evidence01`–`evidence07` come from?** If it is the forensicscontest.com corpus,
   there is a published key and a clean licensing route.
4. **The "File Type Analysis Part 1" set** — his own build, or downloaded? Decides whether `EVS-05`
   is adopted or rebuilt.
5. **Which slides were narrated over?** Several labs (TestDisk results, FTK's memory dialog,
   `Follow TCP Stream`, the NetworkMiner run) exist only as spoken steps. A recording, if one
   exists, is worth more than the decks for those five moments.

---

*Audit complete. Sources: `knowledge_base/instructor/*.md` (8 notes + README) and
`knowledge_base/_source_text/Instructor_Session_*.md` (9 raw OCR files), read in full 2026-09-06.*
