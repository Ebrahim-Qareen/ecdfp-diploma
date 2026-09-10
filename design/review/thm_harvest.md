# TryHackMe Harvest — what the eCDFP rebuild should take from the Advanced Endpoint Investigations path

**Source:** `knowledge_base/thm/` — 32 room notes plus one module-arc analysis
(`honeynet-collapse-module.md`), extracted 2026-08-28/29 by `ecdfp-web-extract`.
252 artifacts documented on the R10 six-box template.
**Purpose of this document:** a course-build map. It answers five questions — what each room
teaches, how THM teaches it, which labs are reusable, where our coverage is strong or thin, and
which specific explanations are worth copying.

**Reading rule.** The room notes are analysis, not walkthroughs. They contain no room solutions
and no lab credentials, and this document keeps that discipline. Where a room's own defect is
useful teaching material, it is named; where it endangers evidence or the analyst, it is flagged.

---

## 1 · Room → forensics topic index

**Type key:** `T` = teaching / guided walkthrough · `C` = challenge (unguided, assessed) ·
`H` = hybrid (guided tasks plus an unguided challenge) · `I` = info / concept only.
**Scope key:** ✅ in scope · ⚠️ partly · ❌ out of scope by D38 (Linux/macOS).

### 1.1 File System Analysis → S4

| Room | Primary topic | Artifacts taught | Tools | Type | Difficulty · time | Scope |
|---|---|---|---|---|---|---|
| **MBR and GPT Analysis** | Boot chain and partitioning, byte by byte | MBR bootloader (0–445) · partition table (446–509) · `55 AA` signature · GPT protective MBR · primary header · partition entry array · backup header + array · ESP and `.efi` | HxD, `msinfo32`, PowerShell, FTK Imager | T | Medium · 80 min | ✅ |
| **FAT32 Analysis** | FAT32 structure from first principles to hex, plus three attacker techniques | Boot sector / BPB · reserved area (FSInfo, backup boot sector) · FAT and cluster chains · SFN entry · LFN entry · `0xE5` deleted marker · timestamps as anti-forensic target | HxD, Autopsy | H | **Hard** · 90 min | ✅ |
| **NTFS Analysis** | NTFS metadata files on a live volume | Partition Boot Sector · `$MFT` · `$MFTMirr` · NTFS system files (`$Bitmap`, `$BadClus`, `$UpCase`) · `$LogFile` · `$UsnJrnl:$J` · `$I30` · Alternate Data Streams | FTK Imager, MFTECmd, Timeline Explorer | T | Medium · 90 min | ✅ |
| **File Carving** | Recovering files from content alone | File signatures / magic bytes · unallocated space · slack space · embedded EXIF metadata · fragmented remnants · MBR as a formatting indicator | Okteta, `dd`, ExifTool, binwalk, foremost, scalpel | H | Medium · 90 min | ✅ |
| **Diskrupt** | **S4 capstone** — repair, partitions, NTFS, journal, carving, FAT32 in one image | MBR boot sector + signature · partition table entry · derived partition size · `$SI` vs `$FN` · `$UsnJrnl:$J` · ZIP signatures · FAT32 `0xE5` entries · the challenge's own anti-forensic layer | Student's choice (stated as an assessed skill) | **C** | **Hard** · 120 min | ✅ |

### 1.2 Windows Endpoint Investigation → S5 / S6

| Room | Primary topic | Artifacts taught | Tools | Type | Difficulty · time | Scope |
|---|---|---|---|---|---|---|
| **Compromised Windows Analysis** | Root-cause analysis by pivoting on timestamps | Scheduled Tasks · LNK (Recent Items) · Prefetch · Amcache · ShimCache/AppCompatCache · RDP logon events · Defender-disabled event | PECmd, LECmd, AmcacheParser, Timeline Explorer, Event Viewer | T | Easy · 75 min | ✅ |
| **Windows User Activity Analysis** | What a *user did* — 12 artifacts in three families | Registry hive files and mapped keys · dirty hives + transaction logs · TypedPaths · WordWheelQuery · RecentDocs · ComDlg32 LastVisitedMRU · OpenSavePidlMRU · UserAssist · RunMRU · ShellBags · LNK · JumpLists | regedit, Registry Explorer, ShellBags Explorer, LECmd, JumpList Explorer, FTK Imager | T | Medium · 60 min | ✅ |
| **Windows User Account Forensics** | Account lifecycle across four stores | Security event log lifecycle · SAM · `NTDS.dit` · authentication event IDs · NTLM network traffic · Group Policy artifacts | Event Viewer, `ntdsutil`, DSInternals, Wireshark, GPMC | T | Medium · 60 min | ⚠️ (≈half is AD, out of S5 scope) |
| **Expediting Registry Analysis** | Registry **acquisition and fast parsing** — method, not artifacts | System identity / control set · TimeZoneInformation · network history · SAM as RegRipper renders it · registry transaction logs | FTK Imager, KAPE, Registry Explorer, RECmd, RegRipper, EZViewer | T | Medium · **120 min** | ✅ (fits S2 better than S5) |
| **Windows Applications Forensics** | Live triage of installed applications | Scheduled task creation events · service installation events · tasks on disk · services in registry · Firefox / Chrome artifacts · browser extensions · Edge cache · Outlook mailbox + attachment cache · Teams message store · OneDrive sync logs | Event Viewer, PowerShell, DB Browser for SQLite, ChromeCacheView, XstReader, `ms_teams_parser`, OneDriveExplorer | T | Medium · 60 min | ⚠️ (no Prefetch/Amcache — mapping was wrong) |
| **Windows Network Analysis** | Live network triage with built-in tooling only | **SRUM (`SRUDB.dat`)** · Windows Firewall log · `Get-NetTCPConnection` · DNS client cache · hosts file · `netstat` · `pktmon` · `qwinsta` / `Get-SmbConnection` | PowerShell, netstat, pktmon, SRUM parser | T | Medium · 45 min | ✅ |
| **Logless Hunt** | Log analysis **when the Security log is cleared** | IIS / Apache access logs · `ConsoleHost_history.txt` · PowerShell 400/403/600/800 · script block 4104 · TerminalServices RDP · scheduled tasks (log, XML, registry) · Defender operational · Defender DetectionHistory | Event Viewer, PowerShell | **H** | Medium · 90 min | ✅ |
| **Blizzard** | **Multi-host intrusion investigated in reverse order** | Chromium browsing history · browser downloads · local email store · remote logon · execution evidence · Run-key persistence · a second non-registry implant · plaintext credential file | Hindsight, browser SQLite, Registry Explorer, EZ Tools | **C** (3 machines) | Medium · 90 min | ✅ (forced the browser-forensics decision, D35) |

### 1.3 Disk Image Analysis → S2 / S4

| Room | Primary topic | Artifacts taught | Tools | Type | Difficulty · time | Scope |
|---|---|---|---|---|---|---|
| **Forensic Imaging** *(free)* | Linux acquisition end to end | Block-device inventory · write blocker (taught, not used) · **the examiner's audit trail** · raw image · integrity check · the mounted image (the room's central defect) · loop device · device identity | `lsblk`, `df`, `script`, `dc3dd`, `md5sum`, `mount`, `losetup` | T | Easy · 45 min | ✅ |
| **Autopsy** | Autopsy GUI: the five-step case workflow | The `.aut` case file and folder · a case whose image is missing · data sources and image formats · ingest modules · By Extension vs By MIME Type · the S/C/O columns · Data Sources Summary and report · the Timeline | Autopsy (room ships 4.12; current **4.23.1**) | T | Easy · 60 min | ✅ |
| **Intro to Cold System Forensics** | Dead-box vocabulary and ethics | The cold/live decision · order of volatility · disk imaging and write blocking · chip-off and JTAG · secure storage · chain of custody · the toolset · the mounting step | None — concept only | **I** | Info · 60 min | ✅ (⚠️ three factual errors) |
| **DiskFiltration** | Insider taking data out on a USB stick | USBSTOR serial · device-to-user and first connection · **WordWheelQuery (dead on Win11 23H2+)** · ShellBags · Prefetch execution count · Recycle Bin `$I` · document metadata and file signatures · personal hotspot | Autopsy (pre-ingested case) | **C** | **Hard** · 120 min | ✅ |

### 1.4 Memory Analysis → S2-03 / S6-10

| Room | Primary topic | Artifacts taught | Tools | Type | Difficulty · time | Scope |
|---|---|---|---|---|---|---|
| **Memory Analysis Introduction** *(free)* | Memory-forensics vocabulary | Volatile memory as an evidence class · memory hierarchy and swap · kernel vs user space · stack/heap/`.text` · full dump · process dump · pagefile / `hiberfil.sys` · **the anti-forensics catalogue** | None — concept only | **I** | Info · 45 min | ✅ (⚠️ dead ATT&CK ID) |
| **Memory Acquisition** | Acquisition as a **decision process**, not a command | Full memory dump · process dump · pagefile / swapfile · hibernation file · hypervisor memory-state files · crash dump | FTK Imager, `procdump64`, DumpIt, LiME, hypervisor snapshots | T | Easy · 60 min | ✅ |
| **Volatility Essentials** | Volatility 3 as a working tool | `pslist` · `psscan` · `pstree` · handles · `netstat`/`netscan` · `dlllist` · `malfind`/`vadinfo` · SSDT, modules, drivers | Volatility 3 (**2.28.0**) | T | Medium · 60 min | ✅ |
| **Windows Memory & Processes** | Kernel structures **plus** a full triage workflow | `_EPROCESS` · `_ETHREAD` · PEB · TEB · parent–child lineage · cross-view `psxview` · module path and load time · dumped section objects | Volatility 3, `comm` for baseline diff | T | Medium · 75 min | ✅ |
| **Windows Memory & User Activity** | Who was at the keyboard — ending in **VBA recovered from RAM** | Session table · loaded registry hives · UserAssist · process command line · open handles · `Normal.dotm` from RAM · `vbaProject.bin` · the responder's own tool inside the evidence | Volatility 3, `unzip`, `olevba` | T | Medium · 60 min | ✅ |
| **Windows Memory & Network** | The network third — C2, injection, YARA, payload recovery | `netscan` socket objects · `malfind` injected regions · `vadyarascan` hit · PowerShell payload from a process dump · **exfiltration strings (capability, not occurrence)** · listening port bind vs reverse · host IP · lateral-movement target | Volatility 3, YARA, `strings` | T | Medium · 60 min | ✅ |
| **Supplemental Memory** | Lateral-movement **lineage signatures**, and process ownership | Process-tree lineage as a signature · `windows.getsids` · the published acquisition hash · full image path · command line · discovery-tool execution · C2 connection · credential dumping | Volatility 3 | T (module capstone) | Medium · 60 min | ✅ |

### 1.5 Honeynet Collapse — one incident across six rooms

Read `honeynet-collapse-module.md` first: it analyses the arc as a single design.
All six are **Hard · 60 min · 2 tasks**, five with six scored questions.

| # | Room | Host / platform | Primary topic | Artifacts taught | Scope |
|---:|---|---|---|---|---|
| ① | **Initial Access Pot** | `deceptipot-demo`, **Linux** | A honeypot in the DMZ as the entry point | Web access logs · dropped PHP webshell · SUID/sudoers state · `sudo`'s own log · auditd syscall records · persistence + MD5 · the bootloader as an access path · the honeypot's own capture data | ❌ |
| ② | **Elevating Movement** | `SRV-IT-QA`, Windows | Lateral movement + credential dumping | RDP logon · scheduled task and the binary it runs · Amcache · malware-family attribution · command-line evidence (and why it is usually absent) · LSASS/SAM access · the NT hash · spending the stolen credential | ✅ |
| ③ | **Lost in RAMslation** | `SRV-DMZ-GW`, Windows memory | Memory answering what the disk never recorded | The malicious file seen from memory · `windows.cmdline` (PEB) · the process tree · masquerading · `malfind` · MZ vs shellcode · network artifacts · the memory image's own provenance | ✅ |
| ④ | **CRM Snatch** | `SRV-CRM-01`, Windows disk | The complete collection→exfiltration leg | Remote session from a disk image · PowerShell engine lifecycle · C2 from PowerShell logs · rclone and what it leaves · **`rclone.conf` as the exfiltration proof** · the password-protected archive · event-log wiping · shadow-copy deletion | ✅ |
| ⑤ | **Shock and Silence** | `DC-01`, NTFS logs | Ransomware on a DC, and **the limits of the evidence given** | The AD1 logical image · `Zone.Identifier` · the original filename in the journal · the encryption run as a `$UsnJrnl` pattern · **process attribution the evidence cannot support** · the appended extension · ransom note and attribution · what the host being a DC changes | ✅ |
| ⑥ | **The Last Trial** | Remote laptop, **macOS** | A *second, unrelated* compromise | The quarantine pair · installation time · `TCC.db` · the C2 URL · Launch Agents/Daemons · the APFS image and a safe mount · `mac_apt` · the lure | ❌ |

### 1.6 Context-only

| Room | Primary topic | Artifacts taught | Tools | Type | Difficulty · time | Scope |
|---|---|---|---|---|---|---|
| **Windows Incident Surface** *(free)* | **Live response, and trusting your own tools first** | The PowerShell profile as an anti-forensic trap · environment variables and execution-flow hijack · system profile and timezone · local accounts and groups · sessions and connections · autostart (`Userinit`, netsh helper DLL) · services and scheduled tasks · processes, temp paths, hidden volume | A supplied trusted toolbox (`CMD-DFIR`, `PS-DFIR`), PsLoggedon, autorunsc | T | Info · **180 min** | ✅ (**strongest S2-02 source**) |
| **ExfilNode** | A second machine because the first machine's attribution is contestable | Linux login records · system timezone · USB attach/detach · shell config as an artifact · `.bash_history` · remote-host artifacts · ext4 inode timestamps · cron | Linux CLI, Autopsy | **C** | Medium · 70 min | ❌ |


---

## 2 · THM's teaching pattern — the template to copy

The path is written by many authors, but the shape repeats closely enough to state as rules. What
follows is the observed pattern, then the rules that follow from it, then the pattern's one
systemic failure — which is our largest opportunity.

### 2.1 The repeating room template

```
Task 1  Scenario / briefing        an alert or a symptom, a host, an environment, an objective
Task 2  Concept and structure      what the artifact IS, drawn or tabled, before any tool
Task 3  Location and acquisition   where it lives on disk / in RAM, and how to get it out
Task 4  Manual read                the raw structure, in a hex editor or an unparsed file
Task 5  Tooled read                the same artifact through the parser, same answer, faster
Task 6  Technique catalogue        what an attacker does TO this artifact (often ATT&CK-titled)
Task 7  Applied scenario           the artifact used to answer an investigative question
Task 8  Unguided challenge         same evidence, no scaffolding, "use the tools you think fit"
```

Not every room carries all eight, but the **order never inverts**: concept → location → manual →
tool → abuse → applied → unguided.

### 2.2 How a concept is introduced

1. **A one-line physical analogy, then straight to structure.** MBR/GPT: *"the disk is a building,
   the partitions are rooms, and the MBR/GPT is the map. Damage the map and nothing else matters."*
   The analogy is never developed past one sentence.
2. **A justification for why this old/obscure thing still matters.** FAT32: it survives because it
   is lightweight and universally compatible, caps at 4 GB per file and 2 TB per volume, and
   **has no permission model at all** — which is why attackers reach for FAT32 USBs. The reason to
   care comes *before* the structure, not after.
3. **The artifact's purpose is stated as a side effect.** Windows User Activity closes with:
   Windows keeps these records to improve user experience, not for forensics; the evidentiary value
   is a by-product. That single frame explains why the artifacts are inconsistent, undocumented and
   version-dependent.

### 2.3 How much theory before hands-on

**Roughly 20–30 % theory, front-loaded, then never revisited.** Concrete measurements:

| Room | Theory tasks | Hands-on tasks |
|---|---|---|
| FAT32 Analysis | 5 of 11 | 6 (three techniques + challenge) |
| MBR and GPT | 3 of 8 | 5 (two hex dissections + two incident scenarios) |
| Volatility Essentials | 2 of 8 | 6 (two cases) |
| Memory Acquisition | 2 of 7 | 5 (Windows, Linux, hypervisors, cloud) |
| Logless Hunt | 2 of 8 | 6 (one log source per attack phase) |

The concept-only rooms (Intro to Cold System Forensics, Memory Analysis Introduction) are **sold as
pre-reading**, not as sessions. That is a defensible separation and worth copying: put vocabulary in
a pre-read, keep session minutes for the artifact.

### 2.4 How an artifact is explained — the six moves

Every well-written room follows the same internal order, which is the R10 six-box template
arrived at independently:

| # | Move | Example (NTFS `$UsnJrnl:$J`) |
|---|---|---|
| 1 | **What it is** | a higher-level record of changes to files, directories and attributes |
| 2 | **Where it lives** | `$Extend\$UsnJrnl`, with `$Max` (policy) and `$J` (the records) — and `$J` is itself an ADS |
| 3 | **What it proves** | a per-change record with a reason code; rename tracking lets you follow a file through renames to deletion |
| 4 | **What it does NOT prove** | it records *that* a change happened and *to what* — not what the change was. No before/after content |
| 5 | **How to parse it** | `MFTECmd.exe -f <$J> --csv <dir> --csvf USNJrnl.csv`, plus `-m <$MFT>` to resolve paths |
| 6 | **The caveat** | trimmed lazily at checkpoints; retention is volume-and-activity dependent — teach the contrast as relative, never as a fixed number of days |

**The rooms are strong on moves 1–3 and 5, weak on 4 and 6.** That asymmetry is the single
consistent finding across all 32 rooms and it is where our material differentiates.

### 2.5 How questions are posed

Observed question shapes, ranked by how well they teach:

| Shape | Example | Verdict |
|---|---|---|
| **Compute, don't look up** | *"At which offset does the FAT2 table start?"* — forces `(reserved sectors + sectors per FAT) × 512 → hex` | 🟢🟢 best in the corpus; needs no VM, no image, no network |
| **Purely hypothetical structure** | *"File B's chain starts at cluster F and ends at cluster 10 — what is the FAT entry at cluster F?"* | 🟢🟢 answerable with no evidence at all; the cheapest high-quality assessment format found |
| **Negative state** | *"According to the MFT record, is the anti-forensics tool currently present on the disk? (yay/nay)"* — the answer is the **In Use** column | 🟢🟢 teaches that the record persisting is not the file persisting |
| **Tool reports X, what is actually true?** | *"What is the actual file type of the file found in Question 1?"* after binwalk reported XML | 🟢🟢 a signature match is a hypothesis |
| **Method contrast, forced by the question** | *"Aside from the scheduled tasks from Windows Event Logs, what does the SECOND malicious scheduled task execute?"* | 🟢🟢 the question itself teaches that the log-based sweep was incomplete |
| **Warn against the obvious** | *"**Go beyond the obvious** — which ransomware group targeted the organisation?"* | 🟢🟢 punishes attribution-by-file-extension |
| **Compose a command** | *"What will the contents of a `_kape.cli` file be if you want to collect from C: to D: using the RegistryHives target?"* | 🟢 tests tool fluency on paper |
| **Chain where each answer is the next filter** | Task created at T → LNKs just before T → Prefetch just after → Amcache for path/hash → event logs around the window | 🟢 self-verifying by construction |
| **Single-value lookup** | *"What is the Offset(V) of the process with PID 5672?"* (the task names the file to grep) | 🔴 tests file navigation, not analysis |
| **Definition recall with no artifact** | *"What type of account…"*, *"What centrally manages…"* | 🔴 a quiz question in a forensics room |
| **Threat-intel inference** | *"From our current information, what malware is present on the system?"* | 🔴 invites naming a family from a filename |

**Answer-format discipline** is inconsistent but correct where present: timestamp masks
(`YYYY-MM-DD HH:MM:SS`), offset masks (`XXXXXXXX`), *"alphabetical order"*, *"without spaces"*,
*"Full URL"*, **`format: defanged URL`**, and — best of all — *"in the UTC timezone"* on artifacts
that are UTC-native and local elsewhere. Windows Incident Surface is the only room that makes
defanging a **graded habit** (six times), and it asks for **SHA-256, not MD5**, four times.

### 2.6 How difficulty ramps

**Three different ramps are used, and they are not interchangeable.**

1. **Within a room — scaffolding removal.** Guided task → same technique on new data → unguided
   challenge with no pivots supplied. FAT32 adds a fourth level in one sentence: *"if you want a
   more demanding challenge, you can answer all the questions using only the HxD editor."* That is
   a mixed-ability class solved for the cost of one line.
2. **Across a module — prerequisite chaining.** Diskrupt names four prerequisite rooms and assesses
   all four in one image. The prerequisite list *is* the syllabus.
3. **Across a story — flat difficulty, varying artifact family.** The Honeynet Collapse arc is
   **all six rooms Hard · 60 min**; only the artifact family changes (Linux logs → Windows events →
   memory → disk → NTFS → macOS). **Completion counts show the real curve:** 3,562 → 2,643 →
   **1,500** → 1,246 → 1,209 → 1,236. The 43 % drop at stage 3 (memory) is the actual difficulty
   spike, and the labels do not show it. *Reject this ramp — a course is not a case.*

### 2.7 How state is carried between sessions

From the Honeynet arc, four mechanisms ranked by cost:

| Mechanism | What it does | Cost | Verdict |
|---|---|---|---|
| **One shared diagram, reused byte-identically** | Establishes topology, names every host, **numbers all six stages** — verified: two rooms serve the *same asset ID* | one SVG, drawn once | 🟢🟢 adopt |
| **A stage number in one sentence** | *"This room is about the Nth attack stage (#N on the network diagram)"* | one sentence per session | 🟢🟢 adopt — it turns the diagram into a scope statement |
| **Character continuity** | Emily (1–2), Matthew (2, 3, 4), Logan (5), Lucas (6) recur as colleagues, victims and investigators | free, if written once | 🟢🟢 the cheapest continuity there is |
| **An identical recap paragraph** | The same outcome paragraph verbatim in all six rooms | copy-paste | 🟢 adopt the idea, not the execution |

**The design rule that makes six chained rooms survivable:** *state the previous stage's conclusion
as given context, and supply fresh evidence for the current one.* Every room is independently
completable; **what carries is narrative, not data.** Its failure: given context is not visually
distinguished from findings, so a student inherits six conclusions they never established. **Fix is
typographic — mark the carried-forward block as *given context*.**

### 2.8 The systemic failure — and the rule it hands us

**Across 32 rooms, six modules and two learning paths, not one question has "cannot be determined"
as its answer.** In at least six rooms the honest answer to a question the room actually asks is
*not determinable from this evidence*:

| Room | Its own question | Why it cannot be answered as asked |
|---|---|---|
| Elevating Movement | *"Which full command line was used to dump the OS credentials?"* | *Audit Process Creation* is **Default: Not configured**, and the command-line policy is **Not Configured (not enabled)** |
| Lost in RAMslation | *"For how many seconds did the attacker maintain their PowerShell session active?"* | 400/403 bracket an **engine instance**, and cannot be strictly correlated to a logon session |
| Shock and Silence | *"Which executable file initiated the encryption process?"* | `USN_RECORD_V2` has **no process field** — the journal logs only the fact and reason of a change |
| The Last Trial | *"When was the malicious application installed?"* | a drag-and-drop app bypasses the OS mechanisms that record installation |

**Three of those four are the same underlying shape and it deserves its own name in the course:
the event was never recorded, rather than destroyed.** No anti-forensics was required to produce
any of them. That is a more important idea than *"the attacker cleared the logs."*

**The platform constraint that excuses TryHackMe and does not excuse us:** a challenge platform
needs a string in a box, so it *cannot* accept *"not determinable"*. **Our assessment is a written
report graded on a fixed rubric, so it can.** That is a concrete, defensible advantage of
report-based assessment and it should be said to students in S1.

### 2.9 The session-writing rules

These are the pattern above, stated as instructions.

**Structure**
1. Open with a **reported symptom or an alert**, never with an artifact name. The scenario supplies
   the first pivot; the student is never told "now open Task Scheduler" out of nowhere.
2. Order every session **concept → location → manual read → tooled read → attacker abuse →
   applied → unguided**. Never invert.
3. Cap front-loaded theory at ~25 % of session minutes. Push vocabulary into a pre-read.
4. Give every artifact the **six moves**, in order, with moves 4 (what it does NOT prove) and 6
   (the caveat) written first, since those are the two the source material is weakest on.
5. **Structure the session by attack phase, not by artifact list** where the content allows —
   Initial Access → Execution → Lateral Movement → Persistence → Credential Access, one artifact
   family each. The student learns the kill chain and the artifact map at the same time.
6. **Manual first, tool second, every single time**, and state the reason out loud: knowing the
   structure is what lets you adjudicate when two tools disagree.
7. **Collect once, parse many.** Teach acquisition once, then parse each artifact from the same
   collection — it mirrors real triage and saves scarce class minutes.
8. **One command shape, several inputs.** MFTECmd against `$MFT`, then `$J`, then `$I30` is three
   artifacts at the cost of one motion. That is the cheapest fluency available.

**Questions**
9. Every question is **single-artifact and single-answer**, and the sequence is a **narrative** —
   that is what makes a question set a capstone rather than a quiz.
10. **State the answer format** every time: timestamp mask, timezone, units, sector size,
    alphabetical ordering, defanged. Two Diskrupt questions have four defensible right answers and
    one accepted one, purely from undeclared units.
11. Prefer questions that **compute** over questions that look up. Hypothetical-structure questions
    need no evidence, no VM and no network — use them for homework.
12. **A stem says what to find, never why it happened.** Reject *"the USB device Liam used for
    exfiltration"*, *"the binary used by the attacker to exfiltrate data"*, *"the malicious
    persistent implant"*. Every one hands over the interpretation and asks only for the lookup.
13. **Ask at least one question per session whose answer is "cannot be determined from this
    evidence"** — and grade the reasoning, not the string.
14. **No question's answer may be a secret or a data subject's personal information.** Ask *which*
    account, *which* remote, *which* record — never the value. This covers NT hashes, Kerberos
    tickets, API keys, WLAN PSKs and archive passwords equally, because all are authenticators.
    Two rooms broke this; one asked for a named individual's email address out of stolen customer
    data.
15. **Ask for the ATT&CK ID *after* the mechanism is identified**, never as the search key.
    Mapping is a conclusion.
16. Where two artifacts record the same event independently, **make the disagreement the finding**.
    Four instances in the corpus: `pslist`/`psscan`, `cmdline`/`handles`, `$SI`/`$FN`, and Defender
    event log vs DetectionHistory. **Name it as a principle.**

**Scenario writing**
17. **Blame a conclusion, not a person.** Logless Hunt's CTO says *"All event logs are empty, so
    hackers did not breach the servers"* — the student has something to be sceptical about that is
    not a human being. Two rooms did the opposite: one named a suspect and editorialised about her
    tenure, another characterised the suspect's out-of-hours behaviour as grounds for suspicion.
18. **Explain why the evidence is thin** rather than saying the attacker deleted everything.
    *"Security controls are still being established… only network-level events are being audited"*
    is more realistic and it teaches that log coverage is a finding about the organisation.
19. **Give environmental context that constrains the hypothesis space**, not context that hints.
20. **State the anti-forensics in the brief.** It converts *"can you find the log entry"* into
    *"the log entry does not exist — now what?"*, which is the actual job, and makes a **negative
    finding** the expected deliverable rather than a failure.
21. **Narrate the discovery, not the attack.** Describe what the person saw — unfamiliar
    extensions, unreadable files, a ReadMe on the desktop — and stop.
22. Make the entry point **a control failure, not a user error**, and make the second host one the
    **organisation hands over** (a work assignment), not one the attacker picks.
23. Include **one pre-existing, documented, benign fault** that plausibly explains a class of the
    attacker's noise. One sentence, and it converts *"why didn't anyone notice?"* from a plot hole
    into a lesson.
24. Include **at least one artifact that does not support the obvious reading**, and one strand
    that turns out to be **unrelated**.

---

## 3 · Lab and challenge inventory

**Evidence reality check first.** Not one of the 33 rooms yields a reusable evidence set. Every
room is a live lab VM, or an image sitting inside a VM you cannot download from. No room publishes
an acquisition record (hash, tool, operator, capture time) except Supplemental Memory — and that
one publishes an **MD5**. **The Windows intrusion image must be staged on our own lab host or
sourced from NIST CFReDS. No further extraction changes this.**

**Placement key:** **G** = in-class guided lab · **H** = homework · **C** = capstone / CTF ·
**D** = demonstration only (not assessable).

### 3.1 Reusable hands-on exercises

| # | Exercise | Source room | Evidence needed | What the student does | What they must find | Placement |
|---:|---|---|---|---|---|---|
| 1 | **The examiner's audit trail** | Forensic Imaging | none — a Linux shell | Set seven bash options, start `script`, save every command's output | Nothing to find — the deliverable *is* the transcript. Do this **before any evidence is touched** | **G** (S2's first practical) |
| 2 | **Loop-device acquisition** | Forensic Imaging | a self-made `.raw` file (`dd` + `mkfs`) — **Tier 1, free** | Attach read-only (`losetup -r`), verify the RO flag, image with `dc3dd hash=sha256`, verify, mount correctly, read a flag | The flag, and a matching hash either side | **G** |
| 3 | **The mount that breaks the hash** | Forensic Imaging (inverted) | the same loop image | Image, record SHA-256, mount **read-write**, re-compute SHA-256 | *"Do the two values match? Explain."* Same lab, same five minutes, opposite lesson | **G** — highest value in S2 |
| 4 | **MBR/GPT byte arithmetic** | MBR and GPT Analysis | a **512-byte file** — no VM, no image | Reverse little-endian → decimal → × 512 → jump to offset. Repeated for MBR partition start, partition size, four GPT LBA fields | Partition count, type GUID, size in GB, first byte at a starting LBA | **H** — self-checking, zero infrastructure |
| 5 | **Repair a wiped partition table and prove it** | MBR and GPT Analysis Task 5 | a disk image with two corrupted MBR fields (**two hex edits to stage**) | On a **verified copy**: identify the corrupted bytes, correct them, reopen in FTK Imager | The tree changes from *"Unrecognized file system"* to readable — **binary, visible, impossible to fake** | **G**, then **C** |
| 6 | **FAT32 structure walk in hex** | FAT32 Analysis | a self-made 64 MB FAT32 image — **Tier 1, cheapest evidence in the course** | Read the BPB, compute FAT1/FAT2/data-area offsets, walk a cluster chain, find `0xE5` entries | Offsets computed not looked up; the recoverable fields of a deleted entry | **G** concept, **H** arithmetic |
| 7 | **FAT32 hypothetical chain question** | FAT32 Analysis | **none at all** | Reason about a chain from stated start/end clusters | The FAT entry value | **H** — no evidence, no VM, no network |
| 8 | **The three FAT32 attacker scenarios** | FAT32 Analysis | four staged FAT32 images: hidden, timestomped, deleted, slack | One ATT&CK technique per task, worked by hand then repeated with a tool | The hidden file, the timestamp inconsistency, the recovered deleted file | **G** |
| 9 | **MFTECmd, three inputs, one motion** | NTFS Analysis | exported `$MFT`, `$J`, `$I30` (CSV is enough) | Same command shape against three artifacts, read in Timeline Explorer | Entry numbers, parent paths, In-Use state, rename chains, `From Slack` entries | **G**, arithmetic to **H** |
| 10 | **The `$J` rename chain** | NTFS Analysis | the `$J` CSV only | Follow one file through renames to deletion | What the file was called before renaming, how many renames, when deleted | **H** |
| 11 | **`$I30` From Slack filter** | NTFS Analysis | the `$I30` CSV only | Filter one column | What the folder *used to* contain vs what it contains now | **H** |
| 12 | **Mount it first, show it empty, then carve** | File Carving | a formatted-but-not-wiped image | Mount, see only `lost+found`, then carve real files out of it | Files that the filesystem says are not there | **G** — one command, one lesson |
| 13 | **Manual carve with exposed arithmetic** | File Carving | a small image with a known header/footer | Find header, find footer, subtract, `dd` with a computed `count` | Start and end offsets, file size, the extracted file | **G** then **H** |
| 14 | **Fragmented-file carve** | File Carving (our addition) | an image with one **deliberately fragmented** file | Carve header-to-footer and inspect the result | That the carve ran past the fragment into unrelated data — **carving's honest boundary** | **G** — no room stages this |
| 15 | **Autopsy end-to-end on a real case** | Autopsy + CFReDS | **NIST CFReDS Data Leakage Case** (public domain, published SHA-1) | Create the case, add the E01, **run ingest with Keyword Search enabled**, fill case metadata, generate HTML **and the TSK Body File** | Installed programs, a password hint, a network-drive IP, the most-frequent search term, an MD5, a Sticky Note | **G** |
| 16 | **Registry: raw view vs parsed view** | Windows User Activity | one hive | Show the key in `regedit` (hex, unreadable), then in Registry Explorer (decoded) | The same value twice — *a parser is an interpretation layer* | **D** → **G** |
| 17 | **Live vs cold registry acquisition, argued** | Expediting Registry Analysis | a live VM + a mounted image | Collect with FTK Imager on the live host, then observe the new entry the collection itself wrote into the execution-tracking keys | **The act of collecting changed the thing being collected** | **G** — the best single micro-lab in the corpus |
| 18 | **`Obtain Protected Files` is a trap** | Expediting Registry Analysis | a live Windows VM | Use the one-click button, then diff against a manual export | Amcache is **missing** — the one-click collection is silently incomplete | **G** — stage the failure, then recover from it |
| 19 | **The KAPE escalation arc** | Expediting Registry Analysis | a triage target | Manual export → automated collection → GUI parsing → CLI parsing → one-command collect-and-parse | Nothing new — the student *feels* the speed-up | **G** (pair every KAPE step with a free standalone alternative) |
| 20 | **Timestamp-pivot chain** | Compromised Windows Analysis | Scheduled Tasks, LNK, Prefetch, Amcache, event logs from one host | Each artifact's timestamp becomes the next artifact's filter | Task name → RAR name and creation time → executable, run count, last run → full path and SHA-1 → Defender-off time and attacker IP | **G**, then strip the pivots for **H** |
| 21 | **Rebuild the timeline yourself** | Compromised Windows Analysis Task 9 | the five CSVs already parsed | The room lists the activity rows and leaves the times blank | The completed timeline — essentially the report's Method + Findings in miniature | **H** |
| 22 | **The three-command PowerShell logging demonstration** | Logless Hunt Task 4 | a Windows VM with PowerShell | Run three commands, then check which of three log sources caught each | A 3×3 coverage table: interactive → history + 4104; `powershell -c` → 600 + 4104; script → 4104 only. **Extend with a 4th row for pwsh 7 and a 5th for transcripts** | **G** — the best comparison teaching in the path |
| 23 | **Verify the premise first** | Logless Hunt Task 2 | any Windows VM with a cleared log | Open Event Viewer and find the earliest Event ID in Security | That the log really is empty — *before* investigating why | **G** — a one-question opener worth keeping verbatim |
| 24 | **Log source per attack phase** | Logless Hunt | five uncleared channels on one host | Web access → PowerShell → RDP → Task Scheduler → Defender, in attack order | Ten linked findings across five channels forming one story | **G** (whole session) |
| 25 | **"Three of these RDP sessions are yours — identify them."** | Logless Hunt (our addition) | the room's own RDP log | Separate responder activity from subject activity | Their own 1149/4624/21/22 events | **G** — a 5-minute exercise no room teaches |
| 26 | **Every family taught twice: logs, then manual** | Windows Applications Forensics | a live Windows VM | Scheduled tasks via Event Viewer, then via the XML on disk, then via `Get-ScheduledTask`. Same arc for services | The task the logs never captured — *the log-based sweep was incomplete* | **G** |
| 27 | **Three users, one workstation** | Windows Applications Forensics | a multi-profile image | Attribute every artifact to a profile | *Which user* — a live question throughout, not an afterthought | **G** design constraint |
| 28 | **SRUM for exfiltration volume** | Windows Network Analysis | `SRUDB.dat` | Parse and sort by bytes sent per application per user per hour | The exfiltration process **by byte volume** — nothing else on Windows answers "how much left, through what, when" without a capture | **G** |
| 29 | **Five artifacts, five tools, one incident** | Windows Network Analysis | a live infected host | A listening port, the C2 process, the planted hosts-file domain, the SRUM volume outlier, the anomalous SMB share | Five findings, each needing a different tool | **G** |
| 30 | **Two live hosts, one attacking the other** | Windows Network Analysis | two VMs, one scripted beacon | Run the same command twice a few minutes apart | **Connection state changes** — live evidence moves | **D only** — no reproducible answer key |
| 31 | **The chicken-and-egg opening** | Windows Incident Surface Task 2 | a host with a staged malicious PowerShell profile | Inspect the profile **from Command Prompt**, because cmd has no profile to hijack | Four techniques in five lines: suppress history, clear **and stop** the event log service, re-enable cleartext credential caching | **G** — opening five minutes of live response |
| 32 | **A hashed toolbox on read-only media** | Windows Incident Surface | our own `CLEAN-TOOLS` build | Verify the toolbox hashes before trusting the tools | That the toolchain is **degraded by design** and that is acceptable | **G** |
| 33 | **Memory acquisition decision sheet** | Memory Acquisition | three written vignettes | Choose the capture type: unusual CPU on a known process → **process dump**; C2 beacon → **full dump**; hibernated machine → **`hiberfil.sys`** | Teaching *when not to take a full dump* | **G** — one page, no VM |
| 34 | **Hash immediately, name to a convention** | Memory Acquisition | any capture | `Get-FileHash` / `sha256sum` after every capture; filename `HOST-YYYYMMDDThhmmssZ` | The convention belongs in the IR playbook, not invented at the keyboard | **G** habit drill |
| 35 | **Volatility plugin pairs by evasion** | Volatility Essentials | one memory image | `pslist` → *"malware unlinks itself"* → `psscan`; `modules` → `driverscan` → `modscan` | **The second plugin's existence is the lesson about the first plugin's limits** | **G** |
| 36 | **Baseline differencing, with its own false positives named** | Windows Memory & Processes | a memory image plus a known-good process list | `comm -13` / `comm -23` against the baseline | The survivors — **and** why the technique lies: processes not running at baseline time, and names truncated by the 15-byte `ImageFileName` field | **G** |
| 37 | **Peel four format layers to reach source code** | Windows Memory & User Activity | one memory image with an infected Word session | memory image → file object (`dumpfiles`) → OOXML container (`unzip`) → OLE2 VBA stream → `olevba` | **Complete, readable VBA** with a hardcoded download URL | **G** — best single exercise in the corpus; closing act of the memory capstone |
| 38 | **User-space claim vs kernel-space record** | Windows Memory & User Activity | the same image | `cmdline` (PEB, user-writable) says Word was launched with the `.docm`; `handles` (kernel object table) says Word actually had it open | The same fact twice, from two trust levels — **make the corroboration rule explicit** | **G** |
| 39 | **Five tools, one escalating question** | Windows Memory & Network | one memory image | `netscan` finds a connection → `cmdline` shows no arguments → `malfind` finds injected code → `vadyarascan` tests the hypothesis → `memmap --dump` + `strings` recovers the payload | Each step motivated by the previous result, never by a syllabus | **G** |
| 40 | **`strings` shows capability, not occurrence** | Windows Memory & Network | one process dump | Grep the dump; find `[!] HttpSendRequestA failed.` **and** `[+] Hosts file exfiltrated to http://` — both in the static string table | **Did the exfiltration succeed? Cannot be determined.** | **G** — the single best teaching artifact found |
| 41 | **Lateral-movement lineage recognition** | Supplemental Memory | three `pstree` fragments (no dump needed) | Recognise the parent→child→grandchild shape with the payload name left arbitrary | PsExec `services.exe → psexesvc.exe → <payload>` · WMI `svchost.exe → wmiprvse.exe → <payload>` · PS Remoting `svchost.exe → wsmprovhost.exe → cmd.exe → conhost.exe + <payload>` | **G** then **H** — detection signatures taught as **structures, never strings** |
| 42 | **`windows.getsids --pid N`** | Supplemental Memory | one memory image | Get the process owner SID **and** group membership, offline, in one command | *"Running as whom, with what group rights?"* — a gap in most memory curricula | **G** |
| 43 | **Audit the case file against the evidence** | Windows Memory & Processes/User Activity/Network | the room's scenario page, network map and three plugin outputs — **no VM, no image, no tooling** | Adjudicate four documented contradictions | Narrative date vs artifact dates → **artifacts win**; `.dmp` vs `.mem` → **undecidable**; filename time vs narrative time → **filename wins** (FTK Imager launched 07:15:28); `WIN-001` vs the map's `WIN-012` → **the IP settles it**. **One row has no answer, and that is the point** | **H** or **G** warm-up — the best pure-reasoning exercise in the corpus |
| 44 | **E01 vs AD1, same incident** | Shock and Silence | the same case exported twice | Ask which questions each image can answer | A logical image forecloses every question the collector did not anticipate — **and Autopsy cannot open an AD1 at all** | **G** — one extra export |
| 45 | **Which sentences in this brief are evidence?** | DiskFiltration (inverted) | the room's own prejudicial brief | Classify each sentence: evidence, prejudice, or neither | *"Worked late hours"*, *"roaming around the server room"*, *"taking pictures"* — none of it digital evidence | **G** — 5 minutes, teaches the findings/interpretation split better than any artifact |

### 3.2 Challenge and capstone scenarios

| # | Scenario | Source | Evidence needed | The task | Must find | Placement |
|---:|---|---|---|---|---|---|
| **C1** | **Diskrupt — the S4 capstone, already designed** | Diskrupt | one multi-partition raw image: corrupted boot sector, NTFS + FAT32 volumes, timestomped file, created-then-deleted directory, a deleted ZIP in unallocated space past a stated offset, a deleted wiper in FAT32 | Twelve single-artifact questions forming one narrative. **Prerequisites are our four S4 teaching rows in our order.** *"Not all tools are required… as in real-life cases, you must figure out which tools work best"* | Corrupted bytes → partition sizes → `$MFT`/`$FN` timestamps → `$UsnJrnl` entry → carve start and end offsets → the flag → the deleted wiper name | **C** — 2 h, Hard. Needs its own block, not a tail-end row |
| **C2** | **Blizzard — three hosts, investigated in reverse** | Blizzard | three staged workstation/server images: patient zero (phishing email, browser redirect chain, download), the pivot (internal phish, payload with `opened=1`, implant + C2, plaintext credential file), the target (network logon, exfil binary, Run-key implant **and a second one**) | **Impact → Pivot → Root Cause.** Each machine's answer is the next machine's starting point | Nine of fifteen answers are timestamps — **set the assembled timeline as the deliverable, with the individual answers as its evidence** | **C** — the S6 capstone shape |
| **C3** | **DiskFiltration — the insider, with the answer key published first** | DiskFiltration | one workstation image: USB serial and first/last connect, WLAN hotspot profile, a password-protected zip from the USB, a PDF with a mismatched `/Author` vs XMP, an extensionless file, a stub binary executed *n* times, **both** a Recycle-Bin deletion and a Shift+Delete, browser history, PowerShell history | **Task 1 publishes the whole attack chain as an ATT&CK table.** Task 2 asks thirteen questions, and every one is *"prove that step happened, from an artifact"* | Eleven distinct artifacts, never the same one twice. **Initial access is `T1078 Valid Accounts` — there is no compromise**, so every artifact is a normal-use artifact | **C** or **H** — the best assessment idea in the corpus |
| **C4** | **Logless Hunt — the empty Security log** | Logless Hunt | one Windows host: cleared Security log, plus a web access log with a scan and an upload, PowerShell history/400/600/4104, **a pwsh 7 session that evades a 5.1-scoped policy**, RDP 21/24/25 with a source IP, a scheduled task, **a hidden `SD`-deleted task**, Defender 1116/1117 + DetectionHistory, and a Defender exclusion with its 5007 | Disprove the CTO's stated conclusion, walking five channels in attack order | Ten linked findings; each answer is the next question's input | **G** for the walkthrough half, **H** for the challenge half |
| **C5** | **CRM Snatch — exfiltration with the anti-forensics declared** | CRM Snatch | one disk image: a remote session, PowerShell engine records, rclone binary **and `rclone.conf`**, a password-protected archive, wiped event logs, deleted shadow copies | The brief states logs were wiped and shadow copies deleted. The student works **around** destroyed evidence | The exfiltration proof comes from **the tool's own configuration file left on disk**, not from traffic. Ask *"how many records were in the staged export, and how do you know?"* — never a password or a customer's email | **C** |
| **C6** | **Shock and Silence — deliberately partial evidence** | Shock and Silence | a **logical** image of NTFS logs only — no unallocated, no slack, no carving | Establish what can be established from the journal, and **be graded on what is correctly reported as unrecoverable** | The download URL from `Zone.Identifier`, the original filename, the encryption pattern — **and that the executable that initiated the encryption cannot be identified from `$UsnJrnl`**. Q5's stem warns: *"go beyond the obvious"* | **C** — the honest-limits capstone |
| **C7** | **Autopsy Task 7 mini-investigation** | Autopsy + CFReDS | the CFReDS Data Leakage PC image | Seven questions, **each naming a different artifact class** | Installed program version, a password hint, a network-drive IP for the SECRET files, the most-frequent web search, a specific dated search, an MD5, a Sticky Note (`StickyNotes.snt` / modern `plum.sqlite`) | **H** |
| **C8** | **Task 7 un-walked artifact set** | Expediting Registry Analysis | a second, un-walked registry artifact set | *"Use the tools of your own choice"* — four questions, no hand-holding | System name, the non-administrator account inside Administrators, the VPN-connected network, the registered organisation | **H** — the shape a student activity should take |
| **C9** | **Unassisted acquisition on a second machine** | Forensic Imaging Task 6 | a separate 1 GB loop device on a second host | Image it, hash it, mount it, read the flag — **no walkthrough** | The hash and the flag. **Add: re-hash after mounting and explain** | **H** — best-constructed practical assessment found |
| **C10** | **Volatility, two postures on one tool** | Volatility Essentials | two memory images | Case 001 is guided with a starting IOC handed over; Case 002 is post-incident with no lead at all | Same plugins, two investigative postures — the model for capstone vs teaching session | **G** (001) + **C** (002) |

### 3.3 Which evidence we can build ourselves — Tier 1 routes found

| Route | Source room | Cost | Serves |
|---|---|---|---|
| **Self-made FAT32 image** (~64 MB): hidden, timestomped, deleted contiguous + fragmented, slack | FAT32 Analysis | minutes | S4 FAT, slack, carving — **cheapest evidence in the course** |
| **Carving target**: write, delete or quick-format, do not wipe; plus one deliberately fragmented file | File Carving | minutes | S4 carving, and carving's honest boundary |
| **MBR/GPT structures**: a known-good MBR plus a copy with the partition table zeroed and `55 AA` altered — **two hex edits** | MBR and GPT Analysis | minutes | S4 partitioning + the recover-and-prove case |
| **Loop-device acquisition set** (`dd` + `mkfs` + `losetup`) | Forensic Imaging | minutes | The whole S2 acquisition lab, with no physical media and no write-blocker hardware. **Models the procedure, not the medium** — no HPA, DCO, bad sectors, SMART or serial |
| **Hypervisor memory snapshot** of our own staged host | Memory Acquisition | free | The memory image — genuine bytes, **no acquisition tool on the guest**, capturable at a chosen moment. ⚠️ **It is a pair, not a file**: capture, hash, list and distribute `<name>.vmem` **and** `<name>.vmss`/`.vmsn` together, same basename, same directory |
| **Multi-partition synthetic image** combining all of the above | Diskrupt | one afternoon | The S4 capstone, with a **private** answer key that cannot be found online |
| **Log/activity staging** (cleared Security log, web scan + upload, PowerShell across three channels, RDP, scheduled task, Defender + exclusion) | Logless Hunt | one scripted afternoon | The log-analysis session — configuration and activity, not an image |

**Tier 2 anchor:** the **NIST CFReDS Data Leakage Case** — a corporate data-theft scenario with a
PC image (**NTFS**, DD and EnCase), three removable-media images (**exFAT**, **FAT32**, **UDF**),
published SHA-1 hashes for all 14 files, and a **46-question answer key**. It is a US Government
work in the public domain, redistributable with attribution. **Pair it with the synthetic image:
CFReDS is real evidence with a public key — perfect for teaching, unusable for grading. The
synthetic image is the reverse.**

### 3.4 What must not be copied — the eleven safety and handling defects

| Defect | Room | Why it matters |
|---|---|---|
| **`binwalk -e` on supplied images with no isolation guidance** | File Carving | **CVE-2022-4510** path traversal. Extraction invokes dozens of third-party unpackers on attacker-controlled input — this is executing untrusted code. Disposable VM, unprivileged, never as root, never on the host holding the master, and on **v3** |
| **Opening PowerShell out of order wipes every event log on the evidence machine** | Windows Incident Surface | The staged profile clears **and stops** the event log service. The most destructive defect in the corpus |
| **Hash, then mount read-write, never re-hash** | Forensic Imaging | Mount count, mount time, `s_last_mounted`, atimes and journal replay all write to the image. Taught immediately after the verification step, to 18,000 people |
| **Editing the evidence image in place in a hex editor** | MBR and GPT Analysis; promoted to a *title* in Diskrupt (*"Fix the damaged disk"*) | Destroys the ability to prove non-tampering. **Identify the corruption, state what it blocks, work around it. If a repair is unavoidable: copy, hash, document** |
| **Pasting recovered PowerShell into a terminal** | FAT32 Analysis | Executing attacker-controlled code recovered from evidence |
| **Running EZ Tools on the live evidence host over RDP** | Elevating Movement; also Windows User Activity, Windows Applications Forensics | Contaminates the very Prefetch and Amcache about to be read |
| **Live acquisition with no write blocker, no hashing, no chain of custody** | NTFS Analysis | The path contradicts itself between rooms — Expediting Registry Analysis argues the opposite at length. **Contrast the two in class; it is a free lesson** |
| **MD5/SHA-1 recommended for evidence integrity** | Intro to Cold System Forensics | Directly contradicts current practice; SHA-256 is not mentioned |
| **Plaintext lab credentials in the task body** | ~29 of 33 rooms | Our repo is public; a credential in a brief is a credential in a search index. **Issue out of band** |
| **A question whose answer is a credential** | Elevating Movement (NT hash), CRM Snatch (cloud password), DiskFiltration (zip password), Blizzard (recovered password) | An NT hash is an **authenticator**, not evidence. Trains students to paste real ones into tickets |
| **A question whose answer is a data subject's PII** | CRM Snatch | *"What is Lucas's email address found in the exfiltrated data?"* — the exfiltrated set is the victim's most sensitive material, and an answer key containing it is a breach of the thing you were hired to protect |

---

## 4 · Coverage strength map

**Strength key:** 🟩 **strong** — a teaching room covers it directly and at depth ·
🟨 **partial** — covered, but incidentally, in a challenge only, or with a named structural gap ·
🟥 **none** — no room covers it.

| Course area | Strength | Rooms that cover it | What is covered | What is missing and must be sourced elsewhere |
|---|:--:|---|---|---|
| **Acquisition & imaging** | 🟩 | Forensic Imaging · Memory Acquisition · Expediting Registry Analysis · Intro to Cold System Forensics · Autopsy · Shock and Silence | The full Linux imaging procedure, the audit trail, hashing, verification, mounting; memory acquisition as a decision process across Windows, Linux, four hypervisors and cloud; **live vs cold argued rather than defined**, with the tool-trace paradox; image formats (raw / E01 / **AD1 logical**) | **HPA and DCO** (no room mentions either) · physical media, SMART, bus, serial, ATA command set, partial-failure modes · **write-blocking as a layered stack** (hardware vs `losetup -r` vs `blockdev --setro` vs `mount -o ro` — only the top two are controls) · Windows-side disk imaging procedure · **SHA-256 discipline** (Intro to Cold System Forensics recommends MD5/SHA-1) |
| **Disks — MBR / GPT** | 🟩 | MBR and GPT Analysis · Diskrupt · File Carving | Boot chain; MBR's 512 bytes field by field; GPT's **five** components including the **backup header and array**; ESP and `.efi`; the LBA arithmetic taught once and reused five times; the recover-and-**prove** case | Nothing material. Add the honest caveat the room omits: a wrong `55 AA` is **malware or a bad sector — not determinable from the MBR alone**; a failed GPT header CRC32 does **not** prove tampering |
| **FAT32** | 🟩 | FAT32 Analysis · Diskrupt · Autopsy (CFReDS RM#2) | Boot sector/BPB, reserved area, FAT and cluster chains, SFN and LFN, the `0xE5` marker, timestamps as an anti-forensic target — all worked in hex then repeated with a tool. **Deeper than any syllabus row needs** | Only the assessment gap: the room states *"FAT32 has no journaling"* and never tests it. Ask: *"from this image alone, can you determine when the timestamps were altered?"* → **no** |
| **NTFS / `$MFT`** | 🟩 | NTFS Analysis · Shock and Silence · Diskrupt · Autopsy | `$MFT` (with the full parsed-CSV column reference), `$MFTMirr`, `$LogFile`, `$UsnJrnl:$J` (with the reason-code table), `$I30` and its slack, ADS, `Zone.Identifier` | **`$SI` vs `$FN` timestamp comparison** — the single most important timestomp-detection technique in NTFS, and no teaching room makes the distinction (only Diskrupt implies it) · **any ADS detection method** (named, never demonstrated) · **`$LogFile` parsing** — MFTECmd cannot do it, so use `dfir_ntfs` or NTFS Log Tracker · `$LogFile`'s **2–3 hour circular retention**, never mentioned |
| **File carving & data representation** | 🟩 | File Carving · FAT32 Analysis · Diskrupt · Autopsy | Header/footer carving manually and with tools; the **recovery vs carving** distinction; slack space; unallocated space; embedded EXIF; MIME vs extension; little-endian and offset arithmetic throughout | **Fragmentation staged deliberately** — no room does it, and it is carving's honest boundary · the fact that **a carved file has no provenance** (no name, no path, no MACB) · encoding/number-system fundamentals are assumed, never taught · tool substitutions needed: drop scalpel (unmaintained), binwalk **v3** not v2, ExifTool 13.x not 11.88 |
| **Windows registry & system config** | 🟩 | Windows User Activity · Expediting Registry Analysis · Windows Incident Surface · Windows Applications Forensics · Windows User Account Forensics | Hive files and their mapped keys; **dirty hives and transaction logs**; ComputerName and control sets; TimeZoneInformation; network history; SAM; services in the registry; autostart (`Userinit`, Run keys, netsh helper DLL); four acquisition/parsing paths compared honestly | **KAPE's licence changed 1 Jan 2026** — teach it for concepts and pair every step with a free standalone alternative · **six user-activity registry keys have no row in our map** |
| **USB** | 🟨 | DiskFiltration (only) · ExfilNode (Linux, out of scope) | USBSTOR serial number; tying the device to a user and to a first connection; the **instance-ID heuristic** — if the second character is `&`, Windows generated the ID and **there is no serial number** | **No teaching room covers USB at all.** Missing: SetupAPI logs, MountedDevices, volume GUIDs, drive-letter mapping, `USBSTOR` vs `USB` vs `WpdBusEnum`, last-removal timestamps, and the distinction between *device connected* and *data copied* |
| **Execution artifacts** (Prefetch / ShimCache / Amcache / UserAssist) | 🟩 | Compromised Windows Analysis · Elevating Movement · Windows User Activity · Windows Memory & User Activity · DiskFiltration | Prefetch (run count, last run), Amcache (full path, SHA-1), ShimCache/AppCompatCache, UserAssist, LNK, Scheduled Tasks — taught in the order an investigator reaches for them, chained by timestamp | ⚠️ **Windows Applications Forensics contains neither Prefetch nor Amcache**, despite the original mapping · **Amcache's SHA-1 covers only the first ~30 MB of a file** · **UserAssist records GUI-initiated launches only** — a process-spawned binary leaves no entry, so absence proves nothing · **ShimCache proves presence and enumeration, not execution** |
| **User activity** (LNK / jumplists / shellbags / Recycle Bin) | 🟩 | Windows User Activity · DiskFiltration · Compromised Windows Analysis | Twelve artifacts across three families: TypedPaths, WordWheelQuery, RecentDocs, ComDlg32 LastVisitedMRU and OpenSavePidlMRU, UserAssist, RunMRU, ShellBags, LNK, JumpLists — each with location → forensic value → worked look → question. Plus Recycle Bin `$I` metadata | 🔴 **`WordWheelQuery` stopped being written at Windows 11 23H2** — the search-terms exercise cannot be staged on a current image · ShellBags log **parent folders even without direct access**, and a *denied* access still creates an entry · the `$I` timestamp is when the file went to the bin, **not when it was destroyed** — destruction is a `$UsnJrnl` sequence |
| **Browser forensics** | 🟨 | Blizzard · Windows Applications Forensics · Autopsy (Recent Activity) | Chromium history and downloads; Firefox, Chrome and Edge artifacts; browser extensions; Edge cache; a phishing-URL-to-first-access chain | **No structural teaching of the history database itself** — no visit `transition` types, no `from_visit` walking, no redirect-chain reconstruction, no deleted-row/freelist recovery, no profile enumeration, no InPrivate caveat. Blizzard's unasked questions define the gap precisely: *a `LINK` transition carrying a redirect flag means they clicked something else* |
| **Memory forensics** | 🟩 | Memory Analysis Introduction · Memory Acquisition · Volatility Essentials · Windows Memory & Processes · & User Activity · & Network · Supplemental Memory · Lost in RAMslation | **The strongest area in the path by a distance.** Concepts → acquisition decisions → Volatility 3 architecture → kernel structures (`_EPROCESS`, `_ETHREAD`, PEB, TEB) mapped to the plugin that reads each field → a full triage workflow with baseline differencing → user activity → network → lateral-movement lineage signatures | Volatility 3's **symbol tables must be pre-staged for an offline lab** · Volatility 2 is EOL (repo archived) — v2-era material is unsafe to build on · `windows.cmdline` reads a **user-writable PEB buffer**, so it is a claim by the process about itself (T1564.010 Process Argument Spoofing) · `malfind` **skips paged regions** |
| **Network forensics** | 🟨 | Windows Network Analysis · Windows Memory & Network · Windows User Account Forensics (one pcap) | **Host-side** network artifacts: SRUM (bytes per app, per user, per hour, ~30–60 days), the Windows Firewall log, `Get-NetTCPConnection`, DNS client cache, hosts file, `netstat`, `pktmon`, `qwinsta`, `Get-SmbConnection`; socket objects recovered from memory | 🔴 **There is no packet-analysis room in the path.** No pcap workflow, no protocol dissection beyond one NTLM sample capture, no flow analysis, no TLS/SNI, no DNS tunnelling, no HTTP object export. Everything network is inferred from the host. **This must be sourced entirely outside THM** |
| **Log analysis** | 🟩 | Logless Hunt · Windows Applications Forensics · Compromised Windows Analysis · Windows User Account Forensics · Blizzard | Five channels the attacker did **not** clear, in attack order; PowerShell's three log sources demonstrated rather than described; RDP session logs; Task Scheduler logs, XML and registry; Defender operational **and** DetectionHistory as two independent stores; account-lifecycle and authentication event IDs; **default on/off state stated for every channel** | Script block logging has **three** states, not two · **PowerShell 7 logs to a different channel under a different policy key**, so a 5.1-scoped policy is evaded · event 5013 is **not** exclusion creation · IIS logs User-Agent and Referer by default · an `SD`-deleted scheduled task runs and is invisible to `schtasks` — diff `TaskCache\Tree` against `System32\Tasks` |
| **Timeline analysis** | 🟨 | Compromised Windows Analysis · Autopsy · NTFS Analysis · Blizzard | Timestamp pivoting as the core skill (a time from one artifact becomes the filter for the next); Timeline Explorer as a CSV reader; Autopsy's Timeline view with counts and date filters; nine timestamps in Blizzard that assemble into a cross-host timeline | 🔴 **No room teaches super-timeline construction.** No `log2timeline`/plaso, no `mactime`, no body-file workflow, no timeline normalisation, no timezone reconciliation across sources. Autopsy's **TSK Body File** export is the bridge and no room uses it. **Timeline Explorer is a CSV viewer, not a timeline tool, and the path conflates them** |
| **Linux forensics** | 🟨 (excluded by decision) | Initial Access Pot · ExfilNode · File Carving · Forensic Imaging | Web access logs, PHP webshell, SUID/sudoers, `sudo`'s own log, auditd syscall records, cron persistence, bootloader access; login records (`wtmp`/`wtmpdb`/`lastlog2`), system timezone on a dead image, USB attach/detach (**Linux has no USBSTOR**), shell config as an artifact, `.bash_history` and its silent-omission trap, ext4 inode timestamps | **Out of scope by decision.** Three things are kept at zero session cost: the **cross-platform contrast table**, the **attribution problem** framing (*"he could argue he was framed as he did not own the workstation"*), and the **accomplice-betrayal** scenario shape. ⚠️ `auditd` is **not installed by default** on Ubuntu, so the room's evidence base is non-standard |
| **Reporting** | 🟥 | — | **Nothing.** Autopsy generates an HTML report as a click-through (one question asks for a module job number). Compromised Windows Analysis asks students to fill blank times into a timeline table. Windows Memory & Processes ships an *"Attack Phases Not Accounted For"* section — the only place in 33 rooms where an unresolved artifact is left unresolved on purpose | **Everything.** No room produces a written report, defines findings vs interpretation as a deliverable, teaches chain-of-custody documentation as an output, requires a stated limitation, or grades reasoning rather than a string. **This is the largest gap in the source material and the clearest place our course is not competing with it** |

### 4.1 Cross-cutting gaps worth naming

- **ATT&CK mappings are unreliable across the whole path** — revoked IDs, moved sub-techniques and
  outright mis-mappings appear in rooms authored as recently as 2025. One room cites a dead
  identifier and the live one for the same behaviour **in the same task**. Re-check every ID.
- **Zero "cannot be determined" questions in 33 rooms.** Roughly 60 ready-made candidates are
  documented across the notes, all answerable from evidence already on the student's screen.
- **Detection signatures are taught as strings.** Teach them as **structures** — a process lineage
  with the payload name left arbitrary, not a hardcoded filename.
- **No room publishes an acquisition record** except one, and that one publishes an **MD5**.
- **No room states a timezone** in a question on a module built entirely on timelines.

---

## 5 · Best-in-class examples worth stealing

Ten, ranked by what they do for the course. Quotes are the rooms' own words unless marked.

### 1 · The wrong conclusion, said out loud by a character — *Logless Hunt*

> *"They reviewed the Security and System logs on all our Windows servers and concluded, **'All
> event logs are empty, so hackers did not breach the servers.'** But guess what? A few days later,
> our website started showing some crypto scam ads and some servers were running at 100% CPU load!"*

The error and its consequence, in one paragraph, in a scenario the student reads **before touching
anything**. Their entire task is to disprove it. Note what it blames: **a conclusion, not a
person** — which is the opposite of the two rooms that named a suspect and editorialised about her
tenure and her movements. **This is the opening paragraph of the whole diploma.**

### 2 · `strings` shows what a program *can* print, never what it *did* print — *Windows Memory & Network*

The room greps a process dump, finds `[!] HttpSendRequestA failed.`, and concludes *"the process
tried a POST connection, but it seemed to fail."* The **same output also contains**
`[+] Hosts file exfiltrated to http://` — the success message. Both strings are in the binary's
static string table, and neither is a log entry.

**Did the exfiltration succeed? Cannot be determined.** One command, one screen, and the entire
findings-versus-interpretation distinction is visible at once. It is the single best teaching
artifact in the corpus and it costs nothing to reproduce.

### 3 · Demonstrate the difference, don't describe it — *Logless Hunt*, Task 4

Three PowerShell log sources, three test commands, one table:

| What was run | `ConsoleHost_history` | Event 600 | Event 4104 |
|---|:--:|:--:|:--:|
| `Write-Output 'TEST1'` typed interactively | ✅ | ✗ | ✅ |
| `powershell -c "Write-Output 'TEST2'"` from cmd | ✗ | ✅ | ✅ |
| `powershell ./script.ps1` (script content) | ✗ | ✗ | ✅ |

Three sources, three coverage profiles, one runnable demonstration — and the room ends it with
*"Check it out yourself!"* **Copy the design wholesale**, and extend it with a fourth row for
**pwsh 7** (different channel, different policy key) and a fifth for **transcripts**. This is how a
"what it does NOT prove" box should be *shown* rather than asserted.

### 4 · Investigate backwards — *Blizzard*

Three machines, three tasks, and the task titles are the method:

| Task | Title | Machine | Position in the attack |
|---|---|---|---|
| 1 | **Analysing the Impact** | the database server | **last** — the alert |
| 2 | **Backtracking the Pivot Point** | an IT employee's workstation | middle — lateral movement |
| 3 | **Discovering the Root Cause** | another user's workstation | **first** — initial access |

Every other room — and most course designs — runs forward from initial access. **Real incident
response does not.** You get an alert about the *end* of the attack and work backwards, and each
machine's findings tell you which machine to look at next. Task 1's answer is Task 2's starting
point. **It is also a better assessment property: a student who guesses on machine 1 cannot
proceed.**

Two supporting sentences are worth copying verbatim for their own sake:

> *"Since the security controls are still being established, alerts have only come from servers,
> and only network-level events are being audited."* — **explains why the evidence is thin without
> resorting to "the attacker deleted everything."**
> *"The infected database server is set up for internal access only and is not yet linked to other
> systems, as it is still in the setup phase. This information could help narrow down potential
> sources of the threat."* — **environmental context that constrains the hypothesis space. That is
> what a real IT team gives you, and using it is a skill.**

### 5 · The act of collecting changes the thing you are collecting — *Expediting Registry Analysis*

The room argues live vs cold acquisition properly, and its example is perfect: **running FTK Imager
on the live host to collect the evidence writes an entry into the very program-execution keys you
came for.** Concrete, checkable, and it turns an abstract integrity principle into a thing the
student can see happen.

The room's best sentence generalises it: you learn several tools **so you can cover one tool's
blind spots with another, and so you can fall back to first principles when two tools disagree.**
That is the whole argument for teaching structure before tooling, arriving from a third party.

### 6 · You cannot trust your own shell — *Windows Incident Surface*

> *"A PowerShell profile is a script that executes every time PowerShell is executed… before even
> executing PowerShell, we should look for traces of compromise in the PowerShell profile. Since we
> were going to use PowerShell to perform our analysis, **this creates a chicken and egg problem
> for us.**"*

And the answer is the right one: **bring your own tools, and start with Command Prompt** — *"unlike
PowerShell, it does not require a profile to execute, therefore making it immune to execution flow
hijack during startup."* The staged profile is the payoff, and it is four techniques in five lines:
suppress shell history, clear **and then stop** the event log service, and re-enable cleartext
credential caching. **This is the missing justification for a clean-tools snapshot**, which most
courses carry as a convenience with no stated rationale.

The room also names the cost honestly: *"you might come across missing features or receive error
messages while using this toolbox, since it is relying only on default environment variables. This
is expected."* **A trusted toolchain is degraded by design, and saying so up front is right.**

### 7 · Peel four format layers to reach source code — *Windows Memory & User Activity*

memory image → **dump the file object** out of `WINWORD.EXE` → it is `Normal.dotm`, an **OOXML
container** → `unzip` it → find `word/vbaProject.bin`, an **OLE2 stream** → `olevba` it → **complete,
readable VBA** with a hardcoded download URL, an `AutoOpen`/`Document_Open` pair, an ADODB stream
write and a `Shell filePath, vbHide`.

Five tools, one answer, and the answer is a real IOC. Each output is the next input, and the student
finishes holding attacker source code they extracted from RAM. **The best single exercise in the
corpus, and the right closing act for a memory capstone.**

Its quieter sibling from the same room is just as valuable: **`cmdline` reads a user-writable PEB
buffer; `handles` reads the kernel object table.** Running both is corroborating a user-space claim
with a kernel-space record — the same principle as `pslist`/`psscan`, `$SI`/`$FN`, and Defender's
event log vs DetectionHistory. **Four instances. Name it as a rule.**

### 8 · A question stem that warns you the obvious answer is wrong — *Shock and Silence*

> *"**Go beyond the obvious** — which ransomware group targeted the organisation?"*

The best question stem in 33 rooms, and it inverts the corpus's standard failure: instead of
asserting a conclusion in the stem, **it warns the student that the surface artifact will mislead
them.** The reasoning behind it is the lesson: ransom notes and appended file extensions identify a
**payload family, not an actor** — the LockBit 3.0 and Babuk builders were leaked, and crews deploy
ransomware *purporting to be LockBit* precisely because the name does the persuading.

It is the closest a text-box platform can get to a "cannot be determined" question. **Ours can go
one step further and accept the honest answer**, because our assessment is a written report.

### 9 · Two journals, two different memories — *NTFS Analysis*

> **`$J` for the long tail of *what* was touched; `$LogFile` for the short high-fidelity window of
> *how*.** *(the note's phrasing of the room's distinction)*

`$LogFile` records the **before and after** of each metadata operation, and is a small, fixed-size
**circular** file — commonly two to three hours of normal usage. `$UsnJrnl:$J` records **that** a
change happened and **to what**, with a reason code, and survives for days to weeks. Neither is a
substitute for the other, and the difference is *retention traded against fidelity*.

**Draw it:** one time axis, two retention bands to scale — a narrow high-detail band and a long thin
one — captioned *"the same event, two different memories."* Pair it with the FAT32 companion
diagram: one 32-byte directory entry drawn twice, **only byte 0 struck through in red**, every
surviving field tinted recoverable, captioned *"one byte changed, everything else still there."*
Those two figures make "deletion is not erasure" and "absence is not proof" visible in one glance
each.

### 10 · Some evidence is not destroyed — it was never recorded — *the Honeynet Collapse arc*

The same idea surfaces from four unrelated directions across the module: **no command line without
process-creation auditing enabled** · **no process field in the NTFS change journal** · **no receipt
for a drag-and-drop install** · **no attribution in a login record**. In every case the room asks a
question the evidence cannot answer, and in none of them did an attacker do anything to hide it.

> *That is the difference between an artifact an attacker removed and an artifact that never
> existed* — and it deserves to be a named category in the course, taught alongside anti-forensics
> rather than inside it.

### Honourable mentions — nine more, all cheap to adopt

| Idea | Room | Why |
|---|---|---|
| **Publish the attack chain as an ATT&CK table *before* the questions** | DiskFiltration | Every question becomes *"prove that step happened, from an artifact."* The student is not guessing what happened — they are finding evidence for a stated claim, which is what an examiner does. **And it makes the gaps visible**: a published step with no clean artifact is the lesson |
| **The entry point is a control failure, not a user error** | Initial Access Pot | A junior is told to prove the honeypot product works, with a deadline and no change process; the box goes into the **DMZ**, exposed to the internet, **over a weekend**. *"The initial access for a full domain compromise is a demo machine"* — and no one in the story is incompetent |
| **An alibi built into the environment** | Elevating Movement | *"It became unstable after we replaced the motherboard, so maybe you can debug what's going on there."* **Pre-authorised cover for every anomaly the attacker generates** — a crash, a service restart, a failing task all read as the known hardware fault. One sentence, and it converts *"why didn't anyone notice?"* from a plot hole into a lesson |
| **The attack arrives as a helpdesk ticket** | CRM Snatch | *"Finance says yesterday's customer CSV file vanished from the share."* **The missing file *is* the exfiltration**, reported as an IT fault. The detection worked and the routing destroyed it — a more interesting failure than "nobody noticed" |
| **Tool selection as the assessed skill** | Diskrupt | *"Not all tools are required to solve this challenge. As it is in real-life cases, you must figure out which tools work best for the situation."* Seventeen teaching rooms hand students a command; this one hands them a problem. **Put it in the capstone brief verbatim** |
| **These records exist for user experience; the evidence is a side effect** | Windows User Activity | One sentence that explains why user-activity artifacts are inconsistent, undocumented and version-dependent — and why `WordWheelQuery` could simply stop being written |
| **Teach plugins in evasion pairs, not alphabetically** | Volatility Essentials | `pslist` → *"malware unlinks itself"* → `psscan`. **The second plugin's existence is the lesson about the first plugin's limits**, and it maps straight onto the "what it does NOT prove" box |
| **Ship an unresolved artifact on purpose** | Windows Memory & Processes | A section headed **"Attack Phases Not Accounted For"**: *"you can only speculate… An educated guess would be…"* — the only room in 33 that reaches the end of its investigation and leaves something unplaced |
| **One strand turns out to be unrelated** | The Last Trial | *"Not every attack is targeted. Sometimes, your curiosity makes you fall into a trap."* After five rooms of one escalating chain, the sixth is a **coincidence** — two compromises, one organisation, one week, and the module refuses to connect them. **An analyst who assumes one story writes a wrong report** |

---

## 6 · The figures worth drawing

The rooms are almost entirely annotated screenshots and terminal transcripts — none of them
reusable, and most of them years out of date. The notes specify our own replacements. These are the
highest-value ones, collected in one place.

| Figure | Spec (one line) | Serves |
|---|---|---|
| **The numbered incident map** | One diagram, drawn once, reused on every session page: named hosts across named subnets with **all stages numbered** and **the current stage highlighted** (the source module never highlights). Documentation IP ranges only | Session continuity — the single cheapest device in the corpus |
| **The 512-byte MBR, to scale** | One horizontal bar divided proportionally: **446 bytes bootloader · 64 bytes partition table (four 16-byte cells) · 2 bytes `55 AA`**, one cell exploded into its six fields. Caption: *"64 bytes decide whether the disk exists"* | MBR |
| **The LBA arithmetic strip** | Four steps: bytes as stored → reversed → decimal → **× 512 → offset**, using one worked chain (`00 08 00 00` → `2048` → `1,048,576`). **One picture that unlocks both the MBR room and the FAT32 room** | MBR, GPT, FAT32 |
| **MBR vs GPT layout** | Two disk strips: MBR = one sector doing everything; GPT = protective MBR · header · entry array · **… backup array · backup header at the far end**, with a dashed link joining primary and backup. Caption: *"the map, and the copy of the map"* | GPT |
| **What a deletion actually destroys** | One 32-byte FAT directory entry drawn twice, **only byte 0 struck through in red**, every surviving field tinted recoverable. Caption: *"one byte changed, everything else still there"* | FAT32 — makes "deletion is not erasure" visible in one glance |
| **The two NTFS journals, to scale** | One time axis, two retention bands: `$LogFile` narrow and high-detail (*"before **and** after, ~hours"*), `$UsnJrnl:$J` long and thin (*"what changed, not how, ~days–weeks"*). Caption: *"the same event, two different memories"* | NTFS |
| **`$SI` vs `$FN`** | One `$MFT` record, two timestamp blocks side by side — **`$SI` labelled "user-writable — what timestomping edits"**, **`$FN` labelled "kernel-maintained"** — with a discrepancy drawn between the creation times. Caption: *"the difference is the finding"* | NTFS — the question the source rooms never ask |
| **Resident vs non-resident** | One MFT record drawn twice: small file with `$DATA` **inside** the record; large file with `$DATA` as a pointer out to cluster runs. Caption: *"under ~700 bytes, the file IS the record"* | NTFS |
| **Recovery vs carving** | Two paths to the same file — one reading the filesystem's index and stopping dead at a *"metadata destroyed"* break, one reading raw bytes straight through. Caption: *"one asks the index, one reads the shelf"* | Carving |
| **What carving loses** | A file card before and after: before = name, path, MACB, size, content; after = **content only**, everything else struck out. Caption: *"a carved file has no provenance"* | Carving — students consistently over-read carved files |
| **Carving assumes contiguity** | One file drawn contiguous, one fragmented across three extents, both carved header-to-footer — the second producing a file that **opens far enough to look real**. Caption: *"a header and a footer are not a file"* | Carving |
| **What a read-write mount writes** | The image as a byte strip with four write sites marked: `s_mnt_count`, `s_mtime`, `s_last_mounted` (**the examiner's own path**), journal replay, plus scattered atime updates — with **the hash shown before and after, different**, at the two ends | Acquisition — makes the defect undeniable |
| **The layered read-only stack** | Four stacked bands: **hardware write blocker** (enforced, NIST-tested) · **`losetup -r`** (enforced by the loop driver) · **`blockdev --setro`** (advisory) · **`mount -o ro`** (insufficient alone — journals replay). Caption: *"only the top two are controls"* | Acquisition — the figure students will still be using in five years |
| **HPA / DCO** | One drive as a bar: **visible LBA range** accented, **hidden HPA** and **DCO-removed** regions shaded, with `hdparm -N`'s two return values arrowed at the boundary. Caption: *"a naive image stops at the first number"* | Acquisition — no room mentions either |
| **The audit trail's two layers** | `script` transcript as a continuous ribbon vs `.bash_history` as discrete stamped entries, with **a crash marked on the timeline** and the history entries after it greyed out. Caption: *"history writes at exit; the transcript writes continuously"* | Acquisition |
| **What survives without the image** | Case folder and image as two objects with a table between them: **in the case** (metadata tree, ingest artifacts, tags, keyword index, timeline, stored hashes) vs **only in the image** (file content, extraction, new hashing, carving, new ingest). Caption: *"a case is a set of claims about an image"* | Autopsy |
| **By Extension vs By MIME Type** | One file shown twice — filed under `.jpg` in one tree, `application/zip` in the other — with a third panel showing the actual header bytes. Caption: *"two views, one file, and the disagreement is the lead"* | Autopsy, carving |
| **The capstone map** | The capstone's objectives as a left-to-right chain, **each step tagged with the teaching row that taught it**. Caption: *"one image, four techniques, one story"* | The session-closing slide |

---

## 7 · Tool currency — what the rooms teach vs what is current

Drawn from `_TOOL_CURRENCY_2026-08-28.md`. Cite its items as **"block R5"**, never bare `R5`.

| Tool | Room teaches | Current | Action |
|---|---|---|---|
| **Autopsy** | 4.12.0 (docs generated **18 Sep 2019**) | **4.23.1** | Reshoot **every** screenshot against 4.23.1 from our own case. **Keyword Search, Plaso and Malware Scan are OFF by default** — enable them and say why they were off |
| **Volatility** | v3, correctly (dynamic symbol resolution, `windows.info` replaces `imageinfo`) | **3 / 2.28.0** (30 Apr 2026) | Safe to build on. **Volatility 2 repo archived 16 May 2025 — EOL.** Pre-stage symbol tables for an offline lab |
| **MFTECmd** | `-f --csv --csvf` | **2026.5.0** | Add `-m <$MFT>` when parsing `$J` or paths are missing. **`$I30` support is real but absent from the README**; **`$LogFile` support is claimed and does not work** — use `dfir_ntfs` or NTFS Log Tracker |
| **EZ Tools (GUI)** | assorted | **2026.5.0** | **.NET 9 only** — the clean-tools snapshot must ship .NET 9 |
| **KAPE** | free, unrestricted | licence changed **1 Jan 2026** | Teach for concepts; **pair every step with a free standalone alternative** |
| **FTK Imager** | assorted | **8.3** (free, registration) | Keep — and it is the **only** way to open an AD1, which Autopsy cannot |
| **binwalk** | v2 conventions | **v3** | v2 extraction paths are wrong and v2 carries **CVE-2022-4510**. Teach v3, and teach the isolation lesson |
| **foremost** | SourceForge | **1.5.7**, upstream dead, distro-maintained | Install via `apt`, never SourceForge |
| **scalpel** | presented as current | unmaintained, no releases | **Drop** — mention as legacy only |
| **PhotoRec / TestDisk** | — | **7.2** (7.3-WIP), GPLv2+ | Keep — `S4-09`'s named pair (PhotoRec + foremost) was already correct |
| **ExifTool** | 11.88 | **13.55** | Update — six years of format support |
| **dc3dd** | 7.3.1 | **7.3.1** (Apr 2023), dormant upstream, **actively packaged** (Debian 7.3.1-4, Sep 2025) | Keep as the *"raw dd with hashing"* teaching step. ⚠️ The Debian man page footer still reads 7.2.646. **`hashlog=`/`hashconv=` are dcfldd options, not dc3dd** |
| **Guymager** | *"provides built-in write-blocking"* — **false** | 0.8.13 (2021) upstream, packaged Feb 2026 | Correct the claim. An imaging tool does not provide write blocking |
| **HxD** | current in room | **2.5.0.0** (Feb 2021) — stale but still free incl. commercial use | Keep |
| **Hindsight** | — | **v2026.06** — **now parses Firefox** as well as Chromium | Adopt for browser work |
| **DSInternals** | — | **7.1** | Keep |
| **Wireshark** | — | **4.6.8** | Keep |
| **EnCase Forensic** | named | renamed **OpenText Forensic**, term licensing | Rename |
| **Sysinternals RAMMap** | listed as a memory-**capture** tool | analyses physical memory *usage*; produces no image | Correct the claim |

---

## 8 · What to do next

1. **Take the three ready-made case designs.** Diskrupt is the S4 capstone, already built and
   prerequisite-validated against our own row order. MBR/GPT Task 5 is the recover-and-**prove**
   case including its verification step. Blizzard's reverse-order three-host structure is the
   shape the S6 capstone should have.
2. **Build the Tier 1 evidence.** FAT32 image, carving target, MBR/GPT structures, loop-device
   acquisition set, hypervisor memory snapshot (**as a `.vmem` + `.vmss`/`.vmsn` pair**), and the
   combined multi-partition synthetic image. One afternoon of scripting buys a private answer key
   that cannot be found online.
3. **Route the NIST CFReDS Data Leakage Case through evidence intake** — it is the Tier 2 anchor
   (NTFS · exFAT · FAT32 · UDF, E01 and raw, published SHA-1 hashes, 46-question key,
   public domain) and it still needs its IDs and hashes recorded.
4. **Write the question-design rules into the session template** — §2.9, items 9–16. The
   "cannot be determined" question is the differentiator, and the notes already contain roughly
   sixty ready-made candidates.
5. **Close the three real coverage gaps from outside THM**: packet/network analysis, super-timeline
   construction, and USB device forensics. Reporting is not a gap to close from a source — it is
   the part of the course that has no competitor in this material.
6. **Re-check every ATT&CK ID before it reaches a slide.** The rooms' mappings are unreliable, in
   material authored as recently as 2025.
7. **Handle the eleven safety defects before any of those techniques is demonstrated** — chiefly
   the binwalk CVE and the PowerShell-order event-log wipe.
