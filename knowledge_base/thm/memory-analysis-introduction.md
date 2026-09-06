---
room: Memory Analysis Introduction
url: https://tryhackme.com/room/memoryanalysisintroduction
module: Advanced Endpoint Investigations — **walkthrough room**, concept-only. **Priority 3.**
feeds: `S2-03` (memory acquisition) and the `S6-10` homework track — **as vocabulary and structure,
       not as technique.** Blocks **D**, **E10** and **M** already carry everything operational.
       🔴🔴 **Its one real contribution is a defect: it cites a dead ATT&CK ID and the live one for
       the same behaviour, in the same task** (§3 #1).
difficulty / time: Info-level walkthrough · 45 min · 6 tasks · 15 scored questions ·
                   **free** · 13,179 completions · 278 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (accordion loop, 6/6 tasks)
completeness: **all 6 tasks read in full** (~16 KB). 0 sections NOT READ.
              ⚠️ **Priority 3, and this note is deliberately short.** The room is pure concept —
              **no lab machine, no evidence, no commands to run** — so §2 describes *memory regions
              and dump types as artifact sources* rather than parsed artifacts. **That is a
              considered deviation, not padding.**
              🟢 No credentials; nothing to withhold under R8.
              ⚠️ **Task 5 is an off-platform interactive exercise on an external site** and was NOT
              visited (§4).
---

## 1. What the room teaches

**The vocabulary of memory forensics, competently, to an audience that has none — and it is the
right room to point a student at before `S2-03`, not a source for it.**

13,179 completions and 278 recommends make it the most-completed room in this extraction, and the
content is a clean sweep of the concepts: volatile memory and why it is collected first; the memory
hierarchy and how **swap leaks RAM contents to disk**; kernel space versus user space; the four
regions of a user process; dump types; and a genuinely good anti-forensics catalogue.

🟢🟢 **Two sentences are better than their length suggests.** First: *"some forensic artifacts may
reside in RAM while others may be temporarily stored in swap files"* — **which is the argument for
treating the pagefile as an acquisition target rather than an afterthought**, and our own `S2-03`
does not currently make it. Second: *"encryption keys are often found on the heap, while shell
commands may be on the stack"* — **a concrete reason to care about memory *structure* rather than
treating a dump as an undifferentiated blob.**

🟢 **And its anti-forensics list is the most complete in the corpus** — unlinked modules, **DKOM**,
code injection, memory patching, API hooking, encrypted or packed payloads, and **trigger-based
payloads that only unpack under specific conditions.** That last one is rarely taught and is a
genuine limit on what any single acquisition can contain.

**What it gets wrong, and one of the three is serious:**

- 🔴🔴 **It cites `T1086` for in-memory PowerShell — a dead identifier — and then cites the live
  `T1059.001` for PowerShell four paragraphs later, in the same task.** §3 #1.
- 🔴🔴 **Its "Credential Access (MITRE ATT&CK: T1003)" heading is followed immediately by content
  about `T1071 – Application Layer Protocol`.** The T1003 section has no body: **the heading and the
  text under it are about different things**, and a student reading it learns that credential access
  is C2. §3 #2.
- 🔴 **It lists Sysinternals RAMMap as a memory-capture tool.** RAMMap analyses physical memory
  *usage*; it does not produce a memory image. §3 #3.
- ⚠️ **It offers `dd` over `/dev/mem` or `/proc/kcore` for Linux acquisition** — hedged with
  *"depending on kernel protections"*, which is doing a great deal of work. §3 #3.

## 2. Artifacts — one 6-box block each

⚠️ **This room has no evidence and no commands.** The blocks below therefore treat **memory regions
and dump types as artifact *sources***, which is what the room actually teaches. Operational detail
lives in blocks **D**, **E10** and **M** and is not repeated.

### 2.1 Volatile memory as an evidence class

- **What it is** — *"stored data that holds system and user-level data while the computer runs.
  When the system is powered off or restarted, this data is lost."*
- **Where it lives** — RAM, and — critically — **partly on disk** (§2.2).
- **What it proves** — the room's list is accurate: running processes and loaded executables, open
  connections and ports, logged-in users and recent commands, **decrypted content including
  encryption keys**, and **injected code or fileless malware**. 🟢🟢 **The last two are the ones that
  justify the whole discipline** — they exist nowhere else.
- **What it does NOT prove** — 🔴🔴 **that any of it was true during the incident.** The room says
  memory *"provides a snapshot of system activity"* — ⚠️ **and our own knowledge base is sharper: a
  dump is *"a smear, not a snapshot"***, and it proves state *"at capture time only … a process seen
  here does not prove it was running during the incident, and a process absent here does not prove it
  never ran."* **The room's word "snapshot" is the single most common misconception in memory
  forensics and it uses it four times.**
- **How to parse it** — out of scope for this room; **D**, **E10**, **M**.
- **Anti-forensics / false-positive caveat** — 🟢 the room's own framing is right: memory is
  prioritised *"as early as possible"*, which is **D9**'s order of volatility.

### 2.2 The memory hierarchy and swap — evidence that leaks to disk

- **What it is** — registers → cache → RAM → disk, plus **virtual memory** mapped to RAM *"or, if
  needed, to disk-based swap space."*
- **Where it lives** — `pagefile.sys` on Windows; a swap partition or swapfile on Linux.
- **What it proves** — 🟢🟢 **that RAM contents can outlive a reboot**, in fragments.
- **What it does NOT prove** — 🔴 **that a swap fragment was ever coherent.** Paged-out content is
  **written in page-sized pieces at arbitrary times**, so a string recovered from swap has no
  reliable process attribution, no timestamp and no guarantee that adjacent pages belong together.
  ⚠️ **And it cuts the other way:** because paging is opportunistic, **absence from swap proves
  nothing at all.**
  🔴 **This is also why `malfind` skips paged-out regions** (**M2**) — *"entirely unavailable due to
  paging"* — so **injected code that has been paged out is invisible in the dump and may be sitting
  in the pagefile instead.**
- **How to parse it** — the pagefile is a separate acquisition target and a separate analysis;
  strings-and-carving, not structured parsing.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the transferable point for `S2-03`: acquiring
  RAM without the pagefile is a partial acquisition, and should be recorded as one.**

### 2.3 Kernel space versus user space

- **What it is** — *"Kernel space is reserved for the operating system and low-level services… User
  space contains processes launched by the user or applications. Each process gets its own separate
  space, protected from others."*
- **Where it lives** — the address-space split, visible in a full dump and absent from a process dump.
- **What it proves** — where an artifact sits, and therefore what privilege produced it.
- **What it does NOT prove** — 🔴 **that kernel-space structures are trustworthy.** The room's own
  Task 3 undercuts its Task 2: **DKOM** *"alters kernel structures to hide processes, threads, or
  drivers from standard system tools."* **So the space that carries the most authority is the space
  an attacker with kernel access can rewrite** — which is exactly why `psscan`'s pool-tag scan exists
  and why even that is defeatable (**M4**).
  ⚠️ **And process isolation is a runtime guarantee, not an evidential one** — a full dump contains
  every process's memory regardless of the protection between them, **which is the memory-side
  version of P2's "imaging removes the enforcer."**
- **How to parse it** — Volatility; **D**, **M**.
- **Anti-forensics / false-positive caveat** — 🟢 **a process dump cannot contain kernel evidence**,
  so *"we took a memory dump"* is an incomplete statement until the **type** is named (§2.5–2.6).

### 2.4 Stack, heap, `.text` and data sections

- **What it is** — the four regions the room names inside a user process: **stack** (*"temporary data
  like function arguments and return addresses"*), **heap** (*"dynamic memory allocation during
  runtime"*), **executable (.text)** (*"the actual code or instructions the CPU runs"*), and **data
  sections** (globals).
- **Where it lives** — within each process's address space.
- **What it proves** — 🟢🟢 **where to look.** *"Encryption keys are often found on the heap, while
  shell commands may be on the stack"* is a rule of thumb that turns a blind search into a targeted
  one.
- **What it does NOT prove** — ⚠️ **that a value found in a region is what the region implies.**
  Heap allocations are reused; a key-shaped blob on the heap may be freed memory from a prior
  allocation, and **freed does not mean zeroed.** 🔴 **Stack frames are especially transient** — a
  returned function's frame is overwritten by the next call, so *"shell commands may be on the
  stack"* is opportunistic, not reliable.
  🔴🔴 **And `.text` being *writable* is the whole basis of `malfind`** (**M2**): the finding is not
  what is in a region but **that the region's protection does not match its purpose.** ⚠️ The room
  describes the regions and never mentions their protections, which is the forensically interesting
  property.
- **How to parse it** — `windows.malware.malfind`, `vadinfo`, YARA over VADs (`--yara-string`,
  **E10**).
- **Anti-forensics / false-positive caveat** — 🟢 **legitimate RWX is routine** (JIT, EDR, packers —
  **M2**), so region protections are candidates, not findings.

### 2.5 The full memory dump

- **What it is** — *"Captures all RAM, including user and kernel space."*
- **Where it lives** — produced by the acquisition; on Windows also **`%SystemRoot%\MEMORY.DMP`**
  (kernel crash dumps).
- **What it proves** — the broadest available view.
- **What it does NOT prove** — 🔴🔴 **completeness.** *"All RAM"* is the tool's intent, not its
  result: device-mapped regions, memory the driver cannot read, and pages in flight during a
  streaming capture all produce gaps. ⚠️ **And the collector is inside the sample** — our knowledge
  base: *"self-incriminating by construction — the collector must load a driver and allocate memory,
  so some of what you capture is your own footprint."*
  🔴 **A crash dump is not a forensic acquisition.** `MEMORY.DMP` is written by the OS on a bugcheck,
  in a **structured format for debugging**, at a moment nobody chose. **Useful, opportunistic, and
  not equivalent** — the room lists it beside WinPmem without distinguishing them.
- **How to parse it** — Volatility 3; **D**, **E10**.
- **Anti-forensics / false-positive caveat** — ⚠️ **there is no read-only memory acquisition**
  (**D8**) — the act of collecting changes the thing collected, which is unique to this evidence
  class and worth stating plainly.

### 2.6 The process dump

- **What it is** — *"Captures the memory of a single running process."*
- **Where it lives** — produced on demand; `windows.memmap --pid N --dump` (**E10**).
- **What it proves** — one process's address space in detail.
- **What it does NOT prove** — 🔴🔴 **anything about the rest of the system, including whether this
  process is the interesting one.** A process dump presupposes the triage that identified it —
  **so it is an output of an investigation, not an input to one.**
  ⚠️ **It contains no kernel structures**, so process listings, network tables and DKOM evidence are
  all absent. 🔴 **And a dump of a process whose PEB was patched carries the patched values**
  (**M1**) — the dump preserves the lie faithfully.
- **How to parse it** — as a PE-and-strings problem rather than a Volatility one.
- **Anti-forensics / false-positive caveat** — 🟢 **the honest use is reverse engineering and IOC
  extraction**, which is what the room says: *"Helpful for reverse engineering or isolating malicious
  behavior within a specific application."*

### 2.7 Pagefile, swap and `hiberfil.sys`

- **What it is** — RAM contents that reached disk. *"On Windows, this is stored in `pagefile.sys`,
  and on Linux, in the swap partition or swapfile"*; plus **`%SystemDrive%\hiberfil.sys`**, which
  *"can also be parsed to extract RAM contents saved when the machine enters hibernation mode."*
- **Where it lives** — on the disk image, which means **a disk acquisition already contains partial
  memory evidence.**
- **What it proves** — 🟢🟢 **that memory evidence survives a power-off.** For a machine that was
  hibernated rather than shut down, `hiberfil.sys` is a **dated, compressed RAM image sitting in the
  file system** — and it is the only artifact in this room that a *dead-box* examiner can use.
- **What it does NOT prove** — 🔴 **that it is current.** `hiberfil.sys` reflects the last hibernation,
  which may be weeks old, and **is stale by construction**; the pagefile is fragmentary (§2.2).
  ⚠️ **Both may be absent by policy** — hibernation is commonly disabled on servers, and the pagefile
  can be disabled or cleared at shutdown by a Group Policy setting. **Absence is a configuration
  finding, not an anti-forensic one.**
- **How to parse it** — `hiberfil.sys` needs a converter before Volatility; the pagefile is
  strings-and-carving.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the reason this block matters: it is the
  overlap between S2's memory work and S4's disk work**, and our map keeps them in separate
  sessions. **One cross-reference costs a sentence.**

### 2.8 The anti-forensics catalogue

- **What it is** — the room's seven-item list of what defeats acquisition and analysis.
- **Where it lives** — n/a; a taxonomy.
- **What it proves** — nothing on its own. 🟢 **It is a checklist of reasons a clean-looking dump may
  be lying.**
- **What it does NOT prove** — ⚠️ **that any of it is present.** 🔴 **The one worth singling out is
  the last: *"Trigger-based payloads — some memory-resident malware only unpacks or runs when
  specific conditions are met, limiting what analysts can capture during routine acquisition."***
  **That is a limit no acquisition technique can overcome**, and it means **a clean dump is evidence
  about the moment of capture and nothing more.** ⚠️ The room states it and does not draw the
  conclusion.
  🔴 **"API hooking" needs a currency note:** the room names `ReadProcessMemory` and
  `ZwQuerySystemInformation` as hook targets — 🟢 correct — **but `apihooks` does not exist in
  Volatility 3 at all** (**E10**), so a student who goes looking for the obvious tool finds nothing.
- **How to parse it** — `windows.malware.*` (**D1**), `psscan` vs `pslist` diffs (**M4**).
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the catalogue's real value is as a
  *limitations* paragraph for a report**: each item is a reason a negative result is not a clean
  bill of health, which is **D20** criterion 4 in list form.

## 3. Tools and commands

**The room names no commands and has no lab.** The table records only what it *names*.

| named | our note |
|---|---|
| Mimikatz | 🟢 correct as the canonical credential-dumping example |
| built-in crash dumps, `%SystemRoot%\MEMORY.DMP` | ⚠️ opportunistic, not an acquisition — §2.5 |
| Sysinternals **RAMMap** | 🔴🔴 **not a capture tool** — #3 |
| WinPmem, FTK Imager | 🟢 correct; ⚠️ WinPmem's driver caveat is **D5** |
| `hiberfil.sys` | 🟢 correct, and the dead-box angle — §2.7 |
| **LiME** | 🟢 correct and current for Linux |
| `dd` over `/dev/mem` or `/proc/kcore` | 🔴 heavily restricted on modern kernels — #3 |

### CURRENCY CHECK

| # | claim as the room teaches it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"In-Memory Script Execution (T1086)"* / *"T1086 – PowerShell"* | 🔴🔴 **`T1086` is not a live technique, and the room contradicts itself.** Four paragraphs later the same task cites **`T1059.001 – Command and Scripting Interpreter: PowerShell`**, which **is** current (Execution). ⚠️ **NOT VERIFIED with a quotable deprecation banner** — `https://attack.mitre.org/techniques/T1086/` returned an **empty document**, where every other technique page fetched during this project returned content, and neither a MITRE page nor a mirror could be found stating the replacement in words. **Treat that as a reproducible negative, not as proof.** 🟢 **The practical instruction is unambiguous either way: use `T1059.001`; never `T1086`.** | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) · negative fetch of `attack.mitre.org/techniques/T1086/` |
| 2 | *"Credential Access (MITRE ATT&CK: T1003)"* | 🔴🔴 **The heading has no matching content.** The text immediately beneath it is about **`T1071 – Application Layer Protocol: Command and Control`** — fileless C2 over HTTP/HTTPS/DNS. **A student reading the section learns that credential access is C2.** Both IDs are individually correct (**T1003** OS Credential Dumping → Credential Access; **T1071** → Command and Control); **the editing is what is broken**, and in an introductory room aimed at people with no prior model, a mismatched heading is worse than a wrong ID. | [T1003](https://attack.mitre.org/techniques/T1003/) · [T1071](https://attack.mitre.org/techniques/T1071/) |
| 3 | *"tools like built-in crash dumps, Sysinternals' RAMMap, or third-party utilities such as WinPmem and FTK Imager can be used to generate full or selective memory captures"* | 🔴 **RAMMap does not generate memory captures.** It is a physical-memory **usage analysis** tool — it shows how RAM is allocated by type, and its save function writes a usage snapshot, not RAM contents. **WinPmem and FTK Imager are correct; RAMMap does not belong in the list.** ⚠️ **And `dd` over `/dev/mem` is not a working technique on modern Linux** — `CONFIG_STRICT_DEVMEM` restricts `/dev/mem` to a small range of device memory, and `/proc/kcore` is similarly constrained. The room's hedge (*"depending on kernel protections"*) is technically true and practically misleading: **LiME is the answer, and the others are historical.** 🟢🟢 **The RAMMap half is now CONFIRMED against Microsoft Learn** (back-propagated from room 32, 2026-08-29): *"RAMMap is an advanced physical memory usage **analysis** utility for Windows Vista and higher"*, used *"to analyze application memory usage, or to answer specific questions about how RAM is being allocated"* — **and the page makes no claim anywhere that RAMMap writes a dump.** The room's inclusion of it in a list of capture tools is unsupported by the vendor's own description. ⚠️ **The `/dev/mem` half remains NOT VERIFIED** — stated from general knowledge, not checked against a kernel source in either pass. **Check it before it appears on a slide.** | [MS Learn — RAMMap](https://learn.microsoft.com/en-us/sysinternals/downloads/rammap) · ⚠️ `/dev/mem` still **NOT VERIFIED** |
| 4 | the rest of the ATT&CK set | ✅ **All correct as cited:** `T1053.005` Scheduled Task · `T1543.003` Windows Service · `T1547.001` Registry Run Keys / Startup Folder · `T1021.002` SMB/Windows Admin Shares · `T1021.006` WinRM · `T1059.001` PowerShell · `T1047` WMI. 🟢 **A good spread for an intro room**, and — unlike room 29 — **none of these has been revoked or moved.** | current ATT&CK technique pages |

### NOT VERIFIED

- **A quotable MITRE deprecation banner for `T1086`** (#1). The negative fetch is reproducible;
  the wording is not sourced.
- **`/dev/mem` restrictions** (#3) — still asserted from general knowledge, flagged, not
  cited. **Verify before it reaches a slide.**
- ~~**RAMMap's capabilities** (#3).~~ 🟢 **CLOSED 2026-08-29** — confirmed an analysis
  utility, not an acquisition tool, from Microsoft Learn. See the updated #3 row.
- **Task 5's external interactive exercise** — not visited (§4).

## 4. Evidence used

**None.** No lab machine, no dump, no commands. 🔴 **`ecdfp-evidence` action: none** — `EVS-10`
remains unallocated, **ninth room running.**

⚠️ **Task 5 sends the student to an external site** for an interactive drag-and-drop exercise and a
flag. **Not visited**, and worth noting as a design point rather than a fault: 🔴 **an off-platform
dependency is a link that can rot**, and for our own material — which must run **offline in the lab**
(Part 6, **D29**) — **it is simply unavailable.** 🟢 **The idea (a term-to-definition matching drill)
is sound and reproducible locally in `quiz.js` (D32) at no cost.**

## 5. Lab design worth reusing

### 5.1 🟢 Concepts before tools, with the tools named but not used

The room teaches the *model* — hierarchy, spaces, regions, dump types — and names the tools without
running them. 🟢🟢 **That is the right shape for the 20 minutes of `S2-03` that precede the first
acquisition**, and it is what our row currently lacks: we go to WinPmem quickly.

### 5.2 🟢🟢 The anti-forensics catalogue as a limitations paragraph

§2.8. **Adopt directly**: the seven items become the **standing limitations list** for any
memory-based finding, and **"trigger-based payloads" is the one that justifies the whole list** —
it is a reason no acquisition can be complete.

### 5.3 ⚠️ An interactive drill, off-platform

§4. **Adopt the idea, host it ourselves.**

### 5.4 🟢 Safety and handling defects

**None.** No lab, no evidence, nothing to endanger.

**Running total: 11 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24, 29. Four endanger the
analyst's machine; seven endanger the evidence. Unchanged.**

## 6. Question patterns

**15 scored questions, all recall.** *"What is the slowest component in the memory hierarchy?"*,
*"Which file on Windows systems stores memory during hibernation?"* — 🟢 **appropriate for an
introductory concept room**, and it would be unfair to fault a vocabulary room for testing
vocabulary.

⚠️ **Two are answered by the room's own errors.** *"What MITRE technique ID is associated with
in-memory PowerShell execution?"* has the expected answer **`T1086`** — a dead identifier — 🔴 **so a
student who answers correctly has learned something false**, and the room's own later text
contradicts it.

**🔴 Thirtieth room, no "cannot be determined" question** — and for once the format genuinely excuses
it. 🟢 **But the room's own material supplies the best one in the corpus for `S2-03`:**

| the room could have asked | correct answer |
|---|---|
| *"The memory dump shows no malicious process. Is the host clean?"* | 🔴🔴 **Cannot be determined**, and the room supplies the reason itself: *"Trigger-based payloads — some memory-resident malware only unpacks or runs when specific conditions are met, limiting what analysts can capture during routine acquisition."* **A clean dump is evidence about the moment of capture and nothing more.** |
| *"A process appears in the dump. Was it running during the incident?"* | 🔴🔴 **No** — a dump is *"a smear, not a snapshot"*; it proves state at capture time only. **The room says "snapshot" four times.** |
| *"Nothing was found in RAM. Was there nothing in memory?"* | 🔴 **Not established** — paged-out content sits in `pagefile.sys`/swap and is absent from the dump (§2.2), which is also why `malfind` skips paged regions (**M2**). |

## 7. Figures

🟢🟢 **The first room in ten with real conceptual figures — and they are the ones we need.** The
memory hierarchy is rendered as a top-to-bottom flow beginning `CPU Registers`, and the RAM-structure
and region material is diagrammed. ⚠️ **Not enumerated or opened individually** — the screenshot of
Task 2 shows the hierarchy figure directly, and the DOM query was not run. **Recorded as seen-in-page,
not inspected.**

🔴 **D22 forbids reuse**, so ours are our own — but **F38 and F39 below are cheap and we do not have
them.**

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F38 | **The memory hierarchy, with the forensic annotation the room omits** | Registers → cache → RAM → disk, each band labelled with **what an examiner can acquire from it and how**: registers/cache *"not acquirable"*, RAM *"acquire first (D9)"*, **swap/pagefile *"RAM contents already on disk — acquire with the image"***, disk *"S4"*. | **🔴 P1** | §2.2 — it fixes the room's diagram by adding the only column we care about, and it ties `S2-03` to `S4`. |
| F39 | **A process's address space** | Stack / heap / `.text` / data drawn in one process box, each annotated with **what is found there** (return addresses and shell fragments; keys and buffers; code; globals) **and its expected protection** — with one region drawn **RWX and highlighted** as the `malfind` case. | **🟢 P2** | §2.4 — the room describes the regions and never mentions protections, which is the forensically interesting property. |

## 8. Fit against our material

### ⚠️ Part 1's Priority 3, *"skim, context only"* — correct this time.

Unlike room 29, the classification holds: **this room contributes vocabulary, two figures and one
defect.** 🟢 **It is, however, the right thing to point a student at as pre-reading before `S2-03`**,
and that is a real use — **a free, 45-minute, 13,179-completion concept room is a better prerequisite
than a reading list.**

### Rows this strengthens

- **`S2-03`** — 🟢 **the concepts-before-tools opening** (§5.1), **figure F38**, and 🔴 **the pagefile
  as an acquisition target** (§2.2, §2.7), which our row does not currently treat as one.
- **`S6-10`** — §2.8's anti-forensics catalogue as the **standing limitations list** for memory
  findings.
- **`S4`** ↔ **`S2-03`** — 🟢🟢 **one cross-reference**: `hiberfil.sys` and `pagefile.sys` are memory
  evidence *inside the disk image*, so the two sessions overlap and neither currently says so.
- **`S6-06`** — 🔴 **the `T1086` error joins room 29's `T1070.001`/`T1562.002` as the second
  worked example of stale ATT&CK in a current, popular, free room.** **Two rooms, three dead IDs.**

### Back-propagation

🟢 **None.** ✅ `T1086` appears nowhere in the repo. ✅ `T1071`, `T1547.001`, `T1543.003`, `T1021.002`,
`T1021.006`, `T1047` appear nowhere. ✅ `T1003`, `T1053.005`, `T1059.001` already present and correct.

### Minutes

**Net zero.** Content into `S2-03` and `S6-10`, both as framing rather than new material.
**No new rows.** 🟢 **Nothing lands in S5.**

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-fifth room carrying the S5 overdraft.**

### Out of scope

Nothing — the room is entirely within `S2-03`'s subject, at a level below it.

### Still unresolved

Unchanged from room 29: **S5 re-split** (four-row overload list, `S2-02` on watch) · **S4 capstone
weighting** · **Lab OS version** · **three `CLEAN-TOOLS` items** (FTK Imager, Volatility symbols,
toolbox hashes on read-only media) · **D19 has no per-session host map**, still gating **F7**/**D40** ·
**`ecdfp-case` not installed** · **no room note through `ecdfp-intake`.**

## 9. Links

**Room** — <https://tryhackme.com/room/memoryanalysisintroduction>
**Companion notes** — `memory-acquisition.md`, `volatility-essentials.md`,
`windows-memory-and-processes.md`, `windows-memory-and-network.md` (the operational material this
room precedes) · `lostinramslation.md` (**M1**–**M4**) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **D**, **E10**, **M**, and new block **R**.

**Citations from §3:**

- #1 — T1059.001 <https://attack.mitre.org/techniques/T1059/001/> ·
  ⚠️ negative fetch of <https://attack.mitre.org/techniques/T1086/>
- #2 — T1003 <https://attack.mitre.org/techniques/T1003/> ·
  T1071 <https://attack.mitre.org/techniques/T1071/>
- #3 — ⚠️ **NOT VERIFIED**, flagged rather than cited
- #4 — T1053.005 <https://attack.mitre.org/techniques/T1053/005/> ·
  T1543.003 <https://attack.mitre.org/techniques/T1543/003/> ·
  T1547.001 <https://attack.mitre.org/techniques/T1547/001/> ·
  T1021.002 <https://attack.mitre.org/techniques/T1021/002/> ·
  T1047 <https://attack.mitre.org/techniques/T1047/>
