---
room: Memory Acquisition
url: https://tryhackme.com/room/memoryacquisition
module: Memory Analysis (Section 6 of Advanced Endpoint Investigations)
feeds: S2 — **`S2-03` memory acquisition (direct hit)** · `S2-01` order of volatility ·
       `S2-02` live response · `S2-04` physical vs logical.
       Reveals a **fourth Tier 1 evidence route** (§4) and a **lab-blocking Volatility 3
       problem** (§3) that affects `S6-10` and the whole Volatility homework track.
difficulty / time: Easy · 60 min · 7 tasks · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 7 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

**The decisions you make before you touch the tool.** It is the only room in the batch that treats
acquisition as a *process* rather than a command: what part of memory to capture, when, with which
tool, in which format, and how integrity is proved — then works those decisions through Windows,
Linux, four hypervisors and the cloud.

Its framing is unusually close to ours: *"The memory acquisition process does not start when you
capture an image of the RAM. It starts well before that as a sequence of well-defined choices you
have outlined in your incident response plan."* That is `S2-01` and the D20 integrity criterion
stated by a third party, and it makes the room a better fit for **`S2-03`** than its Part 1 mapping
suggests.

Rated Easy, and it is — but the *judgement* content is the most transferable in the whole batch.

## 2. Artifacts — one 6-box block each

### 2.1 Full memory dump

- **What it is** — the entire contents of physical RAM copied to non-volatile storage.
- **Where it lives** — nowhere until you make it; the output file is whatever path you choose.
  Formats the room lists, with our reading of each:
  | format | note |
  |---|---|
  | `.raw` / `.mem` | raw physical dump; **the compatibility default** |
  | `.dmp` | Windows crash-dump format; several sub-types, usually needs configuring |
  | `.vmem` `.vmsn` `.vmss` `.bin` `.sav` | hypervisor memory-state files (`.sav` needs conversion) |
  | `.core` | ELF process dump (Linux `gcore`) |
  | EWF | Expert Witness, from EnCase |
  | `.lime` | LiME structured full dump |
- **What it proves** — everything resident at one instant: running processes, network connections,
  injected code, credentials, decrypted content, and material that exists **nowhere on disk** —
  the room's fileless-malware scenario is the clean example.
- **What it does NOT prove** — 🔴 **anything about a moment other than the one captured.** RAM
  changes continuously; a dump is a single frame, and the room's "evidence destruction" scenario
  (user reboots before capture) makes the cost of missing that frame concrete. It also does not
  prove what happened *before* — no history, no journal.
- **How to parse it** — Volatility 3 (see §3), which the room justifies on format breadth: raw,
  EWF, Windows crash dump, Windows hibernation, VirtualBox core, VMware `.vmss`/`.vmsn`, LiME,
  QEMU and more.
- **Anti-forensics / false-positive caveat** — 🔴 **the one that matters most, and the room states
  it only obliquely: there is no read-only memory acquisition.** Capturing requires loading a
  kernel driver and running a binary on the live target, and both occupy physical pages — **the
  tool writes to the thing it is measuring.** A memory image is never the pristine observation a
  write-blocked disk image is. Tool, version and exact time are therefore *part of the evidence*.
  The room also names attacker interference — encrypted memory, tools that fight acquisition.

### 2.2 Process dump

- **What it is** — the memory of one process: heap, stack, code, loaded modules.
- **Where it lives** — a `.dmp` you create. Windows default naming
  `PROCESSNAME_YYMMDD_HHMMSS.dmp`.
- **What it proves** — injected code, in-process malware behaviour, and — the room's chosen example
  — **credential material in `lsass.exe`**, the process that manages authentication and tokens, and
  the standard Mimikatz target.
- **What it does NOT prove** — anything outside that process: no network state, no other processes,
  no kernel. And 🔴 **the default dump type is nearly useless forensically** — `-mm` (minidump)
  carries only basic process information; **`-ma` (full) is required** for malware analysis or
  credential extraction. A lab that omits `-ma` produces a file that looks right and contains
  nothing useful.
- **How to parse it** — capture with
  `.\procdump64.exe -ma lsass.exe C:\TMP -accepteula` (SysInternals), then Volatility or a debugger.
- **Anti-forensics / false-positive caveat** — the room states none. Ours: dumping `lsass` is
  itself a **detection-worthy action** — EDR flags it because it is exactly what an attacker does.
  Doing it during an investigation on a monitored host will generate alerts, and that belongs in
  the notes before it belongs in the SOC queue.

### 2.3 Pagefile / swapfile

- **What it is** — virtual memory paged out to disk.
- **Where it lives** — `pagefile.sys` and `swapfile.sys` on the system volume.
- **What it proves** — memory from **suspended or recently terminated** processes — content that
  has already left RAM. A second bite at data the live capture missed.
- **What it does NOT prove** — no structure and no ownership. The pagefile is a bag of 4 KB pages
  with **no process attribution and no timestamps**; you can carve strings and artifacts from it,
  but attributing a page to a process or a time generally is not possible from the pagefile alone.
- **How to parse it** — 🟢 **FTK Imager's Capture Memory dialog offers an explicit "include the
  page file" option**, so it can be collected in the same operation as RAM. The room notes it can
  be large.
- **Anti-forensics / false-positive caveat** — the room states none. It can be disabled by policy,
  and it is cleared at shutdown on hardened systems (`ClearPageFileAtShutdown`) — **absence is a
  configuration fact, not an attacker fact.**

### 2.4 Hibernation file

- **What it is** — a compressed RAM snapshot written when Windows hibernates.
- **Where it lives** — `hiberfil.sys`, Windows only.
- **What it proves** — 🟢 **a full memory capture from a machine that is powered off.** The room's
  scenario is the useful one: a fraud investigation where the system is off and you cannot tip the
  employee off — the hibernation file gives you memory anyway.
- **What it does NOT prove** — it is memory **as of the moment of hibernation**, which may be days
  old, and it says nothing about activity since. It exists only if hibernation is enabled and was
  actually used.
- **How to parse it** — Volatility 3 reads 32- and 64-bit Windows hibernation files directly.
- **Anti-forensics / false-positive caveat** — the room states none. Hibernation is commonly
  disabled on desktops and servers, and `hiberfil.sys` is overwritten on each hibernate — **you get
  the last one, not a history.**

### 2.5 Hypervisor memory-state files

- **What it is** — the RAM of a guest VM, written to disk by the hypervisor on snapshot or suspend.
- **Where it lives** — by platform:
  | hypervisor | file | how |
  |---|---|---|
  | **VMware / vSphere** | **`.vmsn`** (+ `.vmem`) | snapshot the VM; **Volatility reads `.vmsn` directly, no conversion** |
  | Hyper-V | `.vmrs` | `Checkpoint-VM` or `Save-VM`, then copy from the Snapshots folder |
  | VirtualBox | `.elf` | `VBoxManage debugvm "<vm>" dumpvmcore --filename <out>.elf` |
  | KVM | `.raw` | `virsh dump <vm> /path/dump.raw --memory-only` |
- **What it proves** — the same as a full memory dump, **without running anything inside the
  guest**. 🟢 That is the forensically important property: **no driver load, no binary on the
  target, no footprint in the sample.** It is the closest thing to a read-only memory acquisition
  that exists.
- **What it does NOT prove** — snapshotting is not invisible: it briefly stuns the VM and is
  visible to the guest and to hypervisor logs, so a sufficiently aware attacker can notice.
  Timing and format still constrain what the frame contains.
- **How to parse it** — Volatility 3; the room names a `windows.hyperv` plugin for `.vmrs`
  (⚠️ unverified — see §3).
- **Anti-forensics / false-positive caveat** — the room states none. Snapshot chains complicate
  provenance: **record which snapshot, taken when, from which VM** — a `.vmsn` with no chain of
  custody is just a file.

### 2.6 Crash dump

- **What it is** — memory written by the OS when it crashes, if configured to do so.
- **Where it lives** — Windows: configured under `sysdm.cpl` → Advanced → Startup and Recovery →
  *Write debugging information* (dump type, destination, overwrite behaviour). Linux: `kdump` for
  the kernel, plus `core_pattern`/`apport` for processes.
- **What it proves** — memory state at the moment of failure — which matters because **a malicious
  process can be what caused the crash.** It is also the fallback the room recommends for cloud
  VMs, where no built-in memory acquisition exists: configure a full crash dump, trigger a crash,
  detach the disk, attach it read-only to an analysis VM.
- **What it does NOT prove** — 🔴 **the default dump type is small and unhelpful.** Windows offers
  several; only a **complete** dump is a full memory capture. And the "overwrite existing dump"
  setting means **you may only ever have the most recent crash** — earlier evidence is gone.
- **How to parse it** — Volatility 3 reads Windows crash dumps natively.
- **Anti-forensics / false-positive caveat** — this is **retrospective configuration**: it only
  helps if it was set *before* the incident. Turning it on during an investigation captures
  nothing about what already happened.

## 3. Tools and commands

| tool | version the room uses | exact command / action | output |
|---|---|---|---|
| **FTK Imager** | **not stated** | `File > Capture Memory`; set path, filename, **page-file option**; Capture | `.mem` full dump |
| **procdump64** | **v11.0** (shown in the room's output) | `.\procdump64.exe -ma lsass.exe C:\TMP -accepteula` | full process `.dmp` |
| PowerShell | n/a | `Get-FileHash -Path '<file>' -Algorithm MD5` | integrity hash |
| `sysdm.cpl` | n/a | Advanced → Startup and Recovery → Write debugging information | crash-dump config |
| Hyper-V | n/a | `Checkpoint-VM` / `Save-VM`, then copy the `.vmrs` | guest RAM |
| VirtualBox | n/a | `VBoxManage debugvm "<vm>" dumpvmcore --filename <out>.elf` | guest RAM |
| KVM | n/a | `virsh dump <vm> /path/dump.raw --memory-only` | guest RAM |
| vSphere | n/a | snapshot, copy `.vmsn` from the datastore | guest RAM |
| *(Linux — out of scope)* | | LiME `insmod lime-*.ko "path=… format=lime"`, `gcore`, `kdump`, `apport` | |

The room's tool survey — **commercial**: EnCase Forensic, CaptureGUARD (PCIe/ExpressCard),
F-Response, Cellebrite UFED, PCILeech · **free**: FTK Imager, Magnet RAM Capture, DumpIt,
WinPmem/LinuxPmem, LiME.

### CURRENCY CHECK — full detail in `_TOOL_CURRENCY_2026-08-28.md` block D

| item | result |
|---|---|
| 🔴🔴 **Volatility 3 fetches Windows symbols over the network** | It generates symbol tables from Microsoft's symbol server on demand. **Part 6 makes our lab offline and the evidence VMs air-gapped** — so the first `windows.info` in class stalls or fails. **Pre-populate `volatility3/symbols/` in the `CLEAN-TOOLS` snapshot (D17) and verify offline before `S2` and `S6`.** Lab-blocking. |
| 🔴🔴 **`windows.malfind` renamed to `windows.malware.malfind`** | The old path is a shim with `removal_date="2026-06-07"` — **already passed**. Still runs, emits a `FutureWarning`, removed at the next release. Affects `S6-10` and the Volatility homework track. |
| **Volatility 3 current = 2.28.0** (30 Apr 2026) | Volatility 2 repo **archived 16 May 2025** — EOL. Do not teach v2 as an alternative. |
| **No profiles in Vol3** | No `--profile=`, no `imageinfo`/`kdbgscan` workflow; the v3 counterpart is `windows.info`. Any material written from Vol2 gets this wrong twice over. |
| `vol` vs `vol.py` | pip install ⇒ **`vol`**; git clone ⇒ `vol.py` also works. Pick one for the lab and write every command to match. |
| 🔴 **WinPmem CVE-2024-10972** (CVSS 7.3) | Driver accepts unvalidated IOCTLs on `\\.\pmem`. **Fixed in 4.1 — but the only production-signed binary "contains the old drivers."** Fix and signature are mutually exclusive. Excellent **BYOVD case study**; not a no-caveats default. |
| 🔴 Magnet RAM Capture **1.20, Jul 2019** | Vendor lists no Windows 11 and no Server 2016+. Substitute **MAGNET DumpIt for Windows** (x86/x64/ARM64). |
| DumpIt output | **crash dumps, not raw** — raw is "a legacy feature". ✅ Volatility 3 reads crash dumps natively, so this is fine. Also: it is **"MAGNET DumpIt for Windows"** now; "Comae DumpIt" and comae.com links are dead. |
| ✅ **FTK Imager page-file option confirmed** | The currency agent could not verify the Capture Memory dialog from Exterro's docs; **this room documents the step directly** ("Choose whether to include the page file or not"). Cross-confirmed. FTK Imager free = **8.3**, plus a paid **Pro** line. |
| ⚠️ `procdump` v11.0 | shown in the room's own output (2022 copyright). **Not independently verified this pass.** |
| ⚠️ `windows.hyperv` plugin | named by the room for `.vmrs`; **not in the verified plugin set. Confirm before teaching.** |
| Room's version claims | **none stated for any tool** — tenth room running. |

## 4. Evidence used

- Two lab VMs — Windows Server 2019 (FTK Imager + SysinternalsSuite) and Ubuntu Desktop (LiME
  pre-installed, **no internet**). Students create their own dumps.
- **Nothing downloadable, nothing reusable.** Credentials published inline — **not recorded (R8)**.
- **Nothing to flag for `ecdfp-evidence` from the room itself.**

### ✅ FOURTH Tier 1 route — and this one solves `EVS-03` outright

`EVS-03` (the memory image behind `S2-03` and `S6-10`) is the evidence set with no obvious Tier 1
source: Part 5 forbids synthesising memory dumps, and a public corpus means a Tier 2 licence check.

**§2.5 removes the problem. Our lab is VMware Workstation (Part 6).** Snapshot EVI-SRC01 mid-incident
and the hypervisor writes the guest's RAM to `.vmsn`/`.vmem` — **which Volatility 3 reads with no
conversion.** That gives us:

- **genuine memory bytes from our own staged compromise** (D19), perfectly aligned with the same
  incident as every other artifact;
- **no acquisition tool on the guest** — no driver, no WinPmem CVE, no footprint in the sample;
- a capture we can take **repeatedly and at a chosen moment** in the attack chain, which is exactly
  what the room's "timing" argument says is the hard part.

**Recommend `ecdfp-evidence` scope `EVS-03` as a VMware snapshot of EVI-SRC01.** With the FAT32
(room 6), carving (room 8) and MBR/GPT (room 9) sets, **S2, S4 and S6 can now all be sourced Tier 1
from our own lab.** That is a materially stronger position than `evidence_sets.md` assumes.

## 5. Lab design worth reusing

1. **🟢 Four questions before any tool.** *What part of memory? Which tool/technique? When? How do I
   ensure integrity?* The room asks them up front and then answers them on every platform. **That is
   `S2-03`'s spine**, and it converts to a one-page decision checklist for the student guide.
2. **🟢 Scenario-driven type selection.** Three vignettes justify three different captures: unusual
   CPU on a known process → **process dump** (a full dump would be too slow and too noisy); C2
   beacon → **full dump**; powered-off system that hibernated → **`hiberfil.sys`**. Teaching *when
   not to take a full dump* is unusual and correct.
3. **🟢 Hash immediately, then work on the copy.** Every single capture in the room is followed by
   `Get-FileHash`/`md5sum`, with the reason stated: multiple parties will handle the image and
   changes contaminate it. **This is R9 and D20 criterion 1 taught by repetition** rather than
   assertion — and it is the discipline rooms 6, 8 and 9 all violated. Take the pattern whole.
4. **🟢 Name the file to a convention set in advance.** `Hostname_Date.mem`,
   `HOSTNAME-HHMMSS-DDMMYYYY.lime` — and the room repeatedly says the convention belongs in the IR
   playbook, not invented at the keyboard. Small, professional, and it feeds our chain-of-custody
   line (R9) directly.
5. **🟢 Timing taught through failure.** The "evidence destruction" vignette — the user reboots
   before you arrive — makes volatility visceral in a way a definition cannot. Good `S2-01` hook.
6. The question format in Task 3 is worth stealing: **"enter the complete command"** to produce a
   named triage dump. It tests composition, not recall — the same virtue as the FAT32 room's
   arithmetic questions.

**Nothing in this room needs a safety warning** — the first S2/S4 room in the batch that can be
said of. It is careful throughout.

## 6. Question patterns

~12 questions across 7 tasks.

- **Composition questions again**: *"enter the complete command"* for a triage process dump with a
  specified filename format; *"modify this command to output `.raw` over TCP 5555"*; *"modify this
  command to calculate an MD5"*. **Three questions that require reading a tool's option set and
  assembling a command** — the closest thing to a timed tool repetition on paper.
- **Concept-recall questions are well aimed**: which file holds hibernated memory, which tool dumps
  a Linux process, what "keeping track of all hosts" is called (asset management).
- **One question is genuinely conceptual**: *"a threat actor shuts down the target after
  exfiltrating — what do we call that?"* → anti-forensics. Good, because it makes the student
  classify behaviour rather than recall a fact.
- **Still no explicit "cannot be determined" answer** — tenth room. But this room hands us the
  strongest one yet, because the limit is structural rather than incidental:
  *"Your memory image shows process X running. Can you determine whether it was running an hour
  earlier?"* → **no** — a dump is one frame, and RAM keeps no history (§2.1).
  Second candidate: *"the pagefile contains this string — which process wrote it?"* → **cannot be
  determined from the pagefile alone** (§2.3).

## 7. Figures we would need to draw

The room is unusually light on screenshots. Three concepts need our own inline SVG:

| what is needed | our SVG spec (one line) |
|---|---|
| the order of volatility (never drawn) | a vertical ladder from most to least volatile — registers/cache · **memory** · temp filesystems · **disk** · remote logs · physical config · archival — with a "seconds → years" survival axis beside it and memory/disk highlighted, captioned **RFC 3227 §2.1** |
| the six capture types and what each reaches | one RAM block with six labelled extraction arrows — full dump · process dump · region dump · pagefile · `hiberfil.sys` · VM state file — each tagged with the one question it answers, and pagefile/hiberfil/VM-state visually offset as **"on disk, not live"** |
| the acquisition footprint | the target's RAM with the acquirer's own driver and binary drawn **inside** the sample, overwriting pages, captioned "the observer is in the frame — there is no write-blocker for memory" |

The third is the diagram the room needed and does not have, and it is the one that makes §2.1's
caveat impossible to forget. Never their images (D22).

## 8. Fit against our material

### ⚠️ Part 1 maps this to `S2` / `S2-03` — correct, but it feeds four rows, not one

`S2-03` *"Memory acquisition — why it comes first, the tools, and the pitfalls"*, 20 min, is the
direct hit and the room covers every word of it. But it also strengthens:

- **`S2-01`** order of volatility — the RFC 3227 ladder and the "user rebooted" vignette
- **`S2-02`** live response — the four-questions checklist and the footprint problem
- **`S2-04`** physical vs logical — the format table (`.raw`/`.mem` vs `.dmp` vs VM state)
- **`S6-10`** Volatility 3 — indirectly, via the format-compatibility argument and §3's findings

Suggest Part 1's Feeds column read **`S2`** rather than `S2-03` alone.

### 🔴 Two items that must reach the lab build, not just the notes

1. **Pre-stage Volatility 3 symbols on `CLEAN-TOOLS`** (§3). Our lab is offline by design; Volatility
   3 expects a network. **This will fail in class on the first command** unless handled at image
   build time. Affects `S2-03`, `S6-10` and the Volatility homework track.
2. **Decide the acquisition tool for `S2-03`'s hands-on** and pin it. FTK Imager 8.3 is the safe
   default — it is already on the FOR-WS01 list (Part 6), it is free, it does Capture Memory with
   the page-file option, and it avoids the WinPmem driver-signing/CVE problem entirely.

### Minutes

`S2-03` is 20 min against the room's 60. The room's Linux half is out of scope, which removes
roughly a third, and the hypervisor task is directly useful rather than extra. **No new rows
needed.** The four-questions checklist and the naming/hashing discipline fit inside the existing
20 minutes because they are *framing*, not content.

**S2 stays at 220. S4 stays at 220. S5 remains 65 minutes overdrawn** (rooms 1–5).

### Out of scope

**Task 4 (Linux memory acquisition — LiME, `gcore`, `kdump`, `apport`) is out of scope** per
`scope_decisions.md` line 192. Recorded as a boundary decision; not carried into `knowledge_base/`.
The **cloud** material in Task 5 is likewise excluded (line 194) — though its crash-dump-and-detach
technique is a neat idea worth one sentence, since it is really a *disk* acquisition method.
The hypervisor half of Task 5 is **firmly in scope** and is the most valuable part of the room
for us (§4).

## 9. Links

- Room: <https://tryhackme.com/room/memoryacquisition>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 6)
- Room's stated prerequisites: **Memory Analysis Introduction** (Priority 3, not yet extracted),
  Windows Fundamentals, Linux Fundamentals.
- The room cites ***The Art of Memory Forensics*** as its source for the definition of acquisition —
  worth keeping as a reading reference for `S2`/`S6` (link and credit, never rehost — D22).
- **RFC 3227 (BCP 55)** order of volatility: <https://www.rfc-editor.org/rfc/rfc3227.txt>
- **CVE-2024-10972** WinPmem driver: <https://github.com/advisories/GHSA-q5vw-gwwh-j8r7>
- Volatility 3: <https://github.com/volatilityfoundation/volatility3> ·
  Vol2→Vol3 migration: <https://volatility3.readthedocs.io/en/latest/vol2to3.html>
- Full memory-tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block D**

END OF NOTE.
