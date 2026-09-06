---
room: Lost in RAMslation
url: https://tryhackme.com/room/lostinramslation
module: **Honeynet Collapse — stage 3 of 6.** *"Investigate the third, memory forensics part of the
        HoneyNet Collapse!"* Challenge room (Priority 2). Target `SRV-DMZ-GW` (172.16.8.15, DMZ).
feeds: 🟢🟢 **`S2-03`, `S6-10` and the memory-analysis homework track.** Supplies the answer to the
       problem room 24 posed — **memory recovers the command line the disk never recorded** — and
       then **undercuts it**, because the string lives in a buffer the process can rewrite (§2.2).
       🔴🔴 **Q5's own worked example contradicts what Q5 asks for** (§6) — the sharpest
       instructional error found in 25 rooms, and it is a genuinely useful lesson once inverted.
difficulty / time: **Hard** · 60 min · 2 tasks · 7 questions (6 scored + 1 "Let's go!") · Premium ·
                   1,500 completions · 38 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, analysis approach, tips and all question stems
              including Q5's format example. 0 sections NOT READ.
              🔴 **Room ships plaintext SSH credentials in the task body — not reproduced (R8).**
              Fifth Priority-2 room to do so.
              ⚠️ **Answers NOT READ** — lab machine not started. §2 is reconstructed from the 6
              scored questions and 3 tips, as for rooms 18–24.
              🟢 **Volatility currency was NOT re-researched** — blocks **D**, **E10** already carry
              it, verified 2026-08-28. §3 cites them rather than spending budget twice.
---

## 1. What the room teaches

**That memory answers the question the disk could not — and that the answer is a claim the process
made about itself.** Those two sentences are the whole value of this room, and the second one is not
in it.

Room 24 ended on a closed loop: an attacker dumps credentials with a signed Microsoft LOLBin, and the
only thing that would distinguish the act is the command line, which **is not recorded on a default
Windows host** (block **L1**). **This room's Q3 asks for exactly that command line**, and it is
answerable — because `windows.cmdline` reads it out of the process's **PEB**, which exists in RAM
whether or not anyone enabled process-creation auditing.

🟢🟢 **That is the single most useful cross-room finding in the module so far**, and it is the honest
argument for why memory acquisition comes first (**D9**, order of volatility): *not* "memory is
richer", but **"memory holds specific artifacts that the disk is not configured to record."**

**🔴🔴 And then the correction, which the room never makes.** The command line lives in
`PEB → ProcessParameters → CommandLine` — a **user-mode buffer inside the process's own address
space**, writable by that process. ATT&CK **T1564.010 Process Argument Spoofing** describes the
attack precisely: an adversary may *"execute a process with malicious command-line arguments then
patch the memory with benign arguments that may bypass **subsequent process memory analysis**."*
**So `windows.cmdline` output is a claim by the process about itself, not a kernel record.** §2.2.

**The scenario is the module's best-written and its most quietly damning:**

> *"I just need one solid answer, not ten theories" — the project manager complained.*
> *"The logs for SRV-DMZ-GW looked normal, but the engineering team kept reporting odd slowdowns."*

🟢🟢 **Three failures in two sentences, and none of them is technical.** The logs *looked* normal —
which after room 24 we know may mean *nothing was configured to log*. The users reported the symptom
and were not believed. And **a manager applied schedule pressure to an investigation**, which is how
"one solid answer" becomes a premature conclusion. ⚠️ *"Matthew was lost chasing the process
responsible"* — the same Matthew whose domain hash was stolen in stage 2, now the investigator.
**The room does not comment on that, and it is the most interesting unexamined fact in the module.**

**What it gets wrong:**

- 🔴🔴 **Q5's format example contradicts Q5's question.** It asks for *"the first five bytes … of the
  **Meterpreter shellcode** injected"* and offers **`4d5a9000`** as the example — which is
  **`MZ`, the DOS/PE header magic.** Raw shellcode has no MZ. An MZ at the start of an injected
  region means an **injected PE image**, which is a different technique with a different ATT&CK ID.
  §2.6. **The example primes students to find the thing that would falsify the question.**
- 🔴 **Q5 also names the family in the stem** — *"the Meterpreter shellcode"* — before the student has
  looked at a byte. Same pattern as room 24 Q3.
- ⚠️ **Tip 3 — *"Some output has been prefetched in `/home/ubuntu/out`"*** — is a kindness that
  removes the most instructive failure mode. Volatility's first run on an unseen image **fetches
  Windows symbols from Microsoft's symbol server** (**D2**), which is exactly what breaks in an
  air-gapped lab. **Pre-computing the output hides the problem our own lab will hit.**
- ⚠️ **"Volatility is installed" — no version.** Given the **2026-09-25 removal wave** (**E10**),
  which is **27 days after this extraction**, a room that names no version is a room whose commands
  may stop working within the month. 🟢 None of *this* room's plugins are in that wave, but the
  general point stands and applies to our own material.

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 6 scored questions plus 3 tips. Mapping: Q1 → 2.1 · Q2/Q4 → 2.3 ·
Q3 → 2.2 · tip 1 → 2.4 · Q5 → 2.5 and 2.6 · Q6 → 2.7 · the dump itself → 2.8.

### 2.1 The initial malicious file, seen from memory

- **What it is** — Q1: *"What is the absolute path to the initial malicious file executed on this
  host?"*
- **Where it lives** — several places at once, and **they are not equally trustworthy**:
  **`_EPROCESS.SeAuditProcessCreationInfo`** (annotated *"filename and path"*) — the kernel's own
  record of the image path; **`_EPROCESS.ImageFileName`** — a truncated name, **15 bytes on Windows
  7+, 14 printable characters surviving in practice** (**E10**); **`windows.dlllist`**, whose first
  entry is the image; **`windows.filescan`** + **`windows.dumpfiles`** for the file object in the
  cache; and the PEB's `ImagePathName` (same caveat as §2.2).
- **What it proves** — that an image at that path was loaded into a process that existed at capture
  time.
- **What it does NOT prove** — 🔴🔴 **that the file is still on disk, or that it ever was.** A file
  object in memory proves the *path the loader used*; the file may have been deleted immediately
  after execution, and on a memory-only artifact **you cannot check its hash against the disk copy
  unless the disk copy survives.** ⚠️ `windows.dumpfiles` recovers **cached pages**, so a partially
  paged-out file is recovered **incomplete** — and an incomplete file has a different hash, which
  will not match anything.
  🔴🔴 **And "initial" is an interpretation, not an observation.** Nothing in memory is labelled
  *first*. It is established by the **process tree** (§2.3) and creation times, and both have the
  reliability problems that block sets out. **Q1's word "initial" is doing work the artifact cannot
  do alone.**
  ⚠️ **`ImageFileName` truncates at 14–15 characters** — a long, deliberately similar filename can
  be indistinguishable from a legitimate one in `pslist` output. **Always read the full path from
  `SeAuditProcessCreationInfo` or `dlllist`, never the short name** — which is also §2.4's point.
- **How to parse it** — `vol -f image windows.pslist`, then `windows.dlllist --pid N`;
  `windows.filescan | grep <name>` then `windows.dumpfiles --virtaddr <offset>`. ⚠️ **`vol`, not
  `vol.py`, on a pip install** (**D4**).
- **Anti-forensics / false-positive caveat** — 🟢 **the kernel-side path is the one to trust.** Where
  the PEB's `ImagePathName` and `SeAuditProcessCreationInfo` disagree, **the disagreement is the
  finding** — a process claiming to be something the kernel recorded differently is §2.4 caught in
  the act.

### 2.2 `windows.cmdline` — the artifact that answers room 24, and cannot be trusted

- **What it is** — Q3: *"What was the full command line used by the attacker to launch initial
  execution on this host?"* **The block this note exists for.**
- **Where it lives** — the process's own **PEB**. Volatility 3's plugin does exactly this:
  `peb = context.object(… "_PEB" …, offset=proc.Peb)` then
  `return peb.ProcessParameters.CommandLine.get_string()`, under the docstring *"Extracts the cmdline
  from PEB"*. Microsoft: `PEB.ProcessParameters` is *"A pointer to an RTL_USER_PROCESS_PARAMETERS
  structure that contains process parameter information such as the command line."*
- **What it proves** — 🟢🟢 **the invocation, including arguments — on a host where nothing was
  configured to record it.** This is the concrete answer to block **L1**: *Audit Process Creation* is
  off by default, the command-line policy is off by default, Prefetch stores no arguments — **and the
  PEB has the string anyway.** **That is the strongest single argument for memory acquisition in the
  course**, and it is more precise than "memory has more stuff in it."
- **What it does NOT prove** — 🔴🔴🔴 **that the process ran with those arguments.** The PEB is
  **user-mode memory inside the process itself**, so the process can overwrite it. ATT&CK
  **T1564.010 Process Argument Spoofing** (tactic **Stealth**): adversaries *"hide process
  command-line arguments by overwriting process memory"* and may *"override the PEB to modify the
  command-line arguments"* via `WriteProcessMemory()`, so as to *"execute a process with malicious
  command-line arguments then patch the memory with benign arguments that may bypass subsequent
  process memory analysis."*
  ⚠️ **A second, subtler variant needs no overwrite at all:** set the `UNICODE_STRING`'s **Length**
  shorter than the buffer, leaving the real arguments present but unread — the parent creates the
  child `CREATE_SUSPENDED`, patches the PEB, then `ResumeThread`. **A truncated-looking command line
  is therefore itself worth a second look**, and the raw buffer beyond `Length` is worth carving.
  🔴 **Neither `_EPROCESS.SeAuditProcessCreationInfo` nor `ImageFileName` can corroborate it** — both
  are the **image path**, not the command line. **No kernel structure stores the command line.**
  🟢 **The one genuinely independent source is console memory** — `windows.consoles` / `windows.cmdscan`
  (*"Looks for Windows console buffers"*), which recovers what was typed, from `conhost`, not from the
  target's PEB. ⚠️ **Only for console-launched commands** — useless against a process started by an
  injected thread or a service.
  ⚠️ **And it usually fails for exited processes.** The plugin's own error path reads *"Required
  memory at … is not valid (process exited?)"* — a `psscan`-recovered terminated process has had its
  address space torn down, so **`psscan` finds the process and `cmdline` cannot read it.**
- **How to parse it** — `vol -f image windows.cmdline`; corroborate with `windows.consoles`.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **the reporting rule follows directly and it is
  the cleanest D20 criterion-4 example in the corpus:** *"the PEB of PID 1234 contains the string X"*
  is a **finding**; *"the attacker ran X"* is an **interpretation** that assumes the PEB was not
  patched. **A clean-looking command line is never exculpatory.** 🟢 Corroborate against
  §2.3's process tree, §2.5's injected regions, and the on-disk artifacts from room 24 — **agreement
  across independent sources is the only thing that upgrades this from claim to finding.**

### 2.3 The process tree — and how much of it is real

- **What it is** — Q2 (*"Which process ID (PID) was assigned…"*) and Q4 (*"the name of the final
  process in the chain"*). The chain **is** the answer to Q4, so the tree's reliability is the
  question.
- **Where it lives** — three plugins, three mechanisms:
  **`windows.pslist`** walks the doubly-linked list from `PsActiveProcessHead` — *"This plugin does
  not detect hidden or unlinked processes (but psscan can do that)."*
  **`windows.psscan`** scans physical memory for `_EPROCESS` **pool tags** — *"This can find
  processes that previously terminated (inactive) and processes that have been hidden or unlinked by
  a rootkit."*
  **`windows.pstree`** builds the tree from **PPIDs**, and *"enumerates processes using the same
  technique as `pslist`, so it will also not show hidden or unlinked processes."*
- **What it proves** — that these `_EPROCESS` structures existed, with these recorded parent IDs and
  creation times.
- **What it does NOT prove** — 🔴🔴🔴 **that the tree is the truth. Three independent problems:**
  1. 🔴 **`pstree` inherits `pslist`'s blindness.** An unlinked (DKOM) process is absent from the tree
     entirely — **so "the final process in the chain" is the final process *that is still linked*.**
     **Run `psscan` and diff.** ⚠️ And even `psscan` is defeatable: *"rootkits can still hide by
     overwriting the pool tag values (though not commonly seen in the wild)."*
  2. 🔴🔴 **PID reuse.** Windows recycles PIDs once the last handle closes, so **a child's recorded
     PPID can point at an unrelated process that later took that number.** On a long-uptime server
     this is not exotic.
  3. 🔴🔴 **Parent PID spoofing** — ATT&CK **T1134.004** (tactics **Stealth**, Privilege Escalation):
     a process *"explicitly forges its parent"* using `EXTENDED_STARTUPINFO` with
     `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` via `UpdateProcThreadAttribute` → `CreateProcess`,
     *"resulting in mismatched/implausible lineage."* **The PPID is an attacker-settable field.**
  🟢🟢 **The falsifiability check is `CreateTime` ordering: a child cannot predate its claimed
  parent.** A parent created *after* its supposed child refutes that edge outright. ⚠️ *(This
  inference is our own synthesis, not a quoted source — but it follows from the field's meaning and
  is trivially demonstrable in a lab.)*
- **How to parse it** — `windows.pslist`, `windows.psscan`, `windows.pstree`; diff the first two;
  sort by `CreateTime` and check every edge. ⚠️ **`windows.psxview` is now
  `windows.malware.psxview`** (**E10**).
- **Anti-forensics / false-positive caveat** — 🟢 **teach the tree as a hypothesis, not a diagram.**
  Every arrow is an assertion that can be checked three ways — creation-time ordering, image path
  (§2.1) and whether the parent's own memory shows it creating a child. **Q4's phrasing, "the final
  process in the chain", asks the student to trust every arrow at once.**

### 2.4 Masquerading — "threat actors tend to mimic system applications"

- **What it is** — tip 1, and the reason Q4's *"name of the final process"* is a trap as well as a
  question. ATT&CK **T1036.005** — 🔴 **now named *"Masquerading: Match Legitimate **Resource** Name
  or Location"***, tactic **Stealth**. **The word "Resource" was added; older material says "Match
  Legitimate Name or Location".**
- **Where it lives** — nowhere. It is a **comparison**, not a field: the process's name and path
  against what that name is supposed to be.
- **What it proves** — nothing on its own. 🟢 **A mismatch is the finding.**
- **What it does NOT prove** — 🔴🔴 **that a legitimate-looking name is legitimate, or that an
  odd-looking one is not.** Two failure directions, and students make both:
  ⚠️ **`_EPROCESS.ImageFileName` truncates at 15 bytes** (**E10**), so `svchost.exe` and a
  deliberately similar 14-character imposter can be **indistinguishable in a process listing**. The
  name column is the *least* reliable column on the screen and it is the one students read first.
  🔴 A legitimately named binary in the **wrong directory** is the classic case — SANS' *Find Evil*:
  look for *"process names that appear legitimate but originate from the **wrong directory path** or
  with the **wrong parent process or SID**"*, with `svchost.exe` expected at
  *"`%SystemRoot%\System32\svchost.exe`"* and parent *"services.exe"*.
  ⚠️ **And misspellings are the cheap tell** — *"scvhost.exe or lssass.exe"* — which means the
  *absence* of a misspelling proves nothing at all.
- **How to parse it** — three checks, in this order: **full path** vs the expected path (§2.1's
  kernel-side field, not the PEB); **parent process** (§2.3, with its reliability caveats);
  **signature/publisher**. 🟢 *"Checking for signed code can help reveal suspicious executables."*
  ⚠️ **Signature checking is a disk-side or reputation-side step** — a memory image gives you the
  path and the bytes, not a trusted verification chain.
- **Anti-forensics / false-positive caveat** — 🔴 **all three checks are attacker-influenceable.**
  The path can be genuine (a DLL side-loaded into a real `svchost.exe`), the parent can be spoofed
  (§2.3, T1134.004), and signed-but-malicious happens. 🟢🟢 **Which is why §2.5 exists: masquerading
  is defeated by looking at what the process *contains*, not what it is *called*.**

### 2.5 `malfind` — injected code, and what the plugin actually flags

- **What it is** — the plugin behind Q5. 🔴 **It is `windows.malware.malfind` now**; the old
  `windows.malfind` is a deprecation shim whose `removal_date="2026-06-07"` **has already passed**
  (**D1**) — it still runs and emits a `FutureWarning`, but a slide or grading key using the old name
  either warns in front of the class or hard-fails at the next release.
- **Where it lives** — it enumerates **VADs** and their protections. ⚠️ **The criterion is more
  specific than the usual summary "RWX with no file backing".** From the source, the region must be
  executable and writable — `if "EXECUTE" in protection_string and "WRITE" in protection_string` —
  **and** pass
  `if (vad.get_private_memory() == 1 and vad.get_tag() == "VadS") or (vad.get_private_memory() == 0
  and protection_string != "PAGE_EXECUTE_WRITECOPY")`.
  **So file-backed regions are *not* universally excluded** — only WRITECOPY ones are. Volatility 3
  additionally inspects `PAGE_EXECUTE_READ` **dirty** pages *"to detect non-writable memory regions
  having been injected using elevated WriteProcessMemory()"*, and skips regions that are *"entirely
  unavailable due to paging, entirely consisting of zeros, or a combination of the two."*
- **What it proves** — that a memory region exists with an unusual protection/backing combination and
  non-trivial content.
- **What it does NOT prove** — 🔴🔴 **that anything is malicious. The plugin says so itself:**
  *"Lists process memory ranges that **potentially** contain injected code."*
  🔴🔴 **Legitimate RWX is routine, and this is the single most important false-positive class in
  memory forensics.** Elastic: *"JIT code, another potential area for false positives, generates
  assembly code at runtime which lives in unbacked or floating memory regions"*, and
  *".NET or Java applications are a couple of examples which use JIT techniques."* Security products
  that *"inject code to some or all processes"* do the same, as do packers and DRM that
  *"decrypt or deobfuscate their core functionality in memory."*
  ⚠️ **Expect hits on a clean system.** ⚠️ **A named list of specific benign processes is NOT
  VERIFIED** from a top-tier source — the verified claim is the *categories* (.NET/CLR, Java, browser
  JS engines, EDR-injected processes). **Do not put a list of "safe to ignore" process names on a
  slide; teach the categories and make students justify each dismissal.**
  🔴 **Paging is the silent one:** a region *"entirely unavailable due to paging"* is skipped, so
  **injected code that has been paged out does not appear in `malfind` output at all.**
- **How to parse it** — `vol -f image windows.malware.malfind`; dump with `--dump`; then §2.6 to
  classify what came out. ⚠️ `windows.vadyarascan` takes **`--yara-string`, not `--yara-rules`**
  (**E10**).
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the honest workflow is subtractive**: `malfind`
  produces candidates, and the analyst *removes* the explainable ones (JIT, EDR, packers) using the
  hosting process's identity. **A `malfind` hit inside a .NET application is nearly meaningless; the
  same hit inside `notepad.exe` is nearly conclusive.** **Context, not the plugin, does the work** —
  and Q5 hands the student the context for free by naming the process in Q4.

### 2.6 MZ versus shellcode — the discrimination the room's own example breaks

- **What it is** — Q5: *"What are the first five bytes (in hex, e.g., `4d5a9000`) of the Meterpreter
  shellcode injected into it?"*
- **Where it lives** — the first bytes of the region `malfind` dumped (§2.5).
- **What it proves** — 🟢🟢 **which kind of injection happened**, which is a bigger finding than the
  bytes themselves:
  **`4D 5A` = `MZ`**, the DOS/PE header magic — Microsoft: *"The first two bytes of the specified
  image has 0x5a4d, which is \"MZ\""*, and the PE spec places the MS-DOS stub *"at the front of the
  EXE image"* with the PE signature offset at `0x3c`. **An MZ at the start of an injected region
  means a whole executable image was mapped into the process.** Elastic: reflective DLL injection
  leaves *"the full MZ/PE header"* at the start of unbacked executable memory, and
  *"Typical code sections are of type 'Image' and map to a file on disk. However, these are type
  'Private' and do not map to a file on disk."*
  **Raw shellcode has no MZ** — it begins with actual instructions.
- **What it does NOT prove** — 🔴🔴🔴 **and here the room contradicts itself.** Q5 asks for
  *"the Meterpreter **shellcode**"* and offers **`4d5a9000` — an MZ header — as the example.**
  **Those are different outcomes with different ATT&CK mappings:**
  | first bytes | what it is | ATT&CK |
  |---|---|---|
  | `4D 5A …` | a **PE image** injected into the process | **T1055.002 Portable Executable Injection** (Stealth, Privilege Escalation), or **T1620 Reflective Code Loading** (Stealth) when loaded without touching disk |
  | not `4D 5A` | **raw shellcode** — instructions, no headers | **T1055** family generally; the stub is a loader, not an image |
  ⚠️ **So the example primes students to look for the thing whose presence would falsify the
  question's premise.** 🟢 **Inverted, it is one of the best teachable moments in the corpus:**
  *"the question said shellcode and the example shows an MZ — which is it, and how would you know?"*
  🔴 **And the stem names the family** — *"the Meterpreter shellcode"* — before any byte is read.
  **Family attribution from five bytes is not identification**; it is pattern-matching against a
  remembered prologue, and it fails silently against any custom or encoded stager.
- **How to parse it** — dump the region and read the first bytes; **classify before naming**: MZ →
  PE injection, carve and hash the image; no MZ → shellcode, disassemble the entry rather than
  guessing a family.
- **Anti-forensics / false-positive caveat** — ⚠️ **an MZ can be stripped.** Reflective loaders
  routinely zero or skip the header once mapped, so **absence of MZ does not prove raw shellcode** —
  it may be a PE with its header erased, which the section layout still betrays. 🟢 **The honest
  finding is the region's structure, not its first five bytes**, and a report that says *"bytes X"*
  without saying *"consistent with a mapped PE / with a raw stub"* has recorded a value instead of a
  fact.

### 2.7 Network artifacts in memory — the 3389 connection

- **What it is** — Q6: *"Which is the IP address that the hosts perform a lateral movement using port
  3389?"* On the map this is **③ → ④**, `SRV-DMZ-GW` → `SRV-CRM-01` (172.16.2.9), crossing the
  DMZ/CORE boundary — **the single most important edge in the module** (room 23 §7).
- **Where it lives** — **`windows.netscan`** (pool-tag scan) and **`windows.netstat`** (live
  `tcpip.sys` structures). ✅ Both current, **identical ten-column output** (**E10**).
- **What it proves** — that a socket structure existed describing a connection between these
  endpoints on this port.
- **What it does NOT prove** — 🔴🔴 **that the connection was live at capture time.** `netscan`
  recovers **closed sockets from freed pool memory**, which is its strength and its trap: an entry may
  be minutes or hours stale, and **it produces false positives** (**E10**). 🟢 `netstat` reads live
  structures and is the corroborating view — 🔴 **but it hard-fails without tcpip symbols**
  (*"Unable to locate symbols for the memory image's tcpip module"*), **which is an air-gapped-lab
  problem, not a theoretical one** (**D2**).
  🔴 **And port 3389 is not RDP.** It is *the port RDP usually uses*. **A connection on 3389 proves a
  TCP session, not a protocol, not an interactive desktop, and not a successful logon** — that
  requires the destination's own event log (room 24 §2.1). ⚠️ **Q6's phrasing — *"perform a lateral
  movement using port 3389"* — folds all four claims into one**, and the artifact supports only the
  first.
  ⚠️ **Nor does an owning PID attribute reliably** — the owner may have exited and its PID been
  reused (§2.3).
- **How to parse it** — `windows.netscan` first (it works without tcpip symbols), then
  `windows.netstat` to corroborate; join the owning PID back to §2.3 and §2.2.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the honest finding pairs memory with the far
  end.** *"A socket structure in `SRV-DMZ-GW`'s memory records 172.16.8.15 → 172.16.2.9:3389"* is
  the finding; *"the attacker moved laterally to SRV-CRM-01"* is the interpretation, and **the room
  that proves it is stage 4.** **That is the module working as designed** (§5.1) and it is exactly
  the shape our S6 capstone should have.

### 2.8 The memory image itself — provenance, and what a dump does not contain

- **What it is** — `SRV-DMZ-GW-evidence.mem` at `/home/ubuntu/`. The room hands it over with **no
  hash, no acquisition tool, no capture time and no chain of custody.**
- **Where it lives** — the lab VM. ⚠️ Not downloadable (§4).
- **What it proves** — the machine's state **at capture time**, which is the examiner's arrival time.
- **What it does NOT prove** — 🔴🔴🔴 **four things, and our own `knowledge_base` already states the
  first better than most textbooks:** a RAM dump is *"a **smear, not a snapshot** — the machine keeps
  running while the capture streams, so pages captured at the start and at the end are from different
  moments and the image can contain structures that never coexisted; an inconsistent process list is
  a normal artifact of this, not evidence of anti-forensics."* It proves state *"at capture time
  only … a process seen here does not prove it was running during the incident, and a process absent
  here does not prove it never ran."* And it is *"self-incriminating by construction — the collector
  must load a driver and allocate memory, so some of what you capture is your own footprint."*
  🔴 **Paged-out data is simply absent** — which is why `malfind` skips paged regions (§2.5) and why
  the **pagefile** is a separate acquisition target, not an optional extra.
  🔴🔴 **And without provenance, none of it is defensible.** No hash means no integrity claim; no
  capture time means every timestamp in the analysis is unanchored; no tool name means the smear
  characteristics are unknown. **The room's evidence would fail D20 criterion 1 on arrival.**
- **How to parse it** — `windows.info` first, always: build, kernel base, **and the capture time**.
  ⚠️ **`windows.info` is the call that triggers the symbol download** (**D2**) — pre-populate
  `volatility3/symbols/` on the `CLEAN-TOOLS` snapshot (**D17**) before any offline session.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the room's omission is our exercise.** Hand
  students the same dump *with* an acquisition record — tool, version, operator, start and end time,
  hash — and have them state, from the elapsed capture time alone, **how wide the smear window is**
  and therefore how precisely any two observations can be ordered. **That converts "a smear, not a
  snapshot" from a memorised phrase into a number.**

## 3. Tools and commands

The room names one tool — *"Volatility is installed in the analyst's machine"* — with **no version**.
Tips 1 and 3 supply orientation and pre-computed output. The table is what the questions require.

| purpose | command | note |
|---|---|---|
| image identity + capture time | `vol -f img windows.info` | 🔴 **triggers the symbol download** (**D2**) |
| process list | `vol -f img windows.pslist` | misses unlinked processes — #4 |
| terminated / hidden | `vol -f img windows.psscan` | 🟢 diff against `pslist` |
| the chain (Q2, Q4) | `vol -f img windows.pstree` | 🔴 inherits `pslist`'s blindness — #4 |
| command line (Q3) | `vol -f img windows.cmdline` | 🔴🔴 **PEB — attacker-writable** — #1 |
| independent cmdline | `vol -f img windows.consoles` · `windows.cmdscan` | 🟢 console-launched only — #1 |
| image path (Q1) | `windows.dlllist --pid N` · `windows.filescan` + `windows.dumpfiles` | ⚠️ cached pages only — §2.1 |
| injected code (Q5) | `vol -f img windows.malware.malfind` | 🔴 **not `windows.malfind`** (**D1**) |
| YARA over VADs | `windows.vadyarascan --yara-string …` | 🔴 **not `--yara-rules`** (**E10**) |
| network (Q6) | `windows.netscan` then `windows.netstat` | ⚠️ scan = stale + FPs; netstat needs symbols (**E10**) |

⚠️ **`vol`, not `vol.py`, on a pip install** (**D4**). ⚠️ **Volatility 3 is 2.28.0 (30 Apr 2026)** —
**do not cite 2.28.2**, that is `develop`; pin `/en/stable/` (**E10**).

### CURRENCY CHECK

🟢 **Blocks D and E10 already carry the Volatility environment**, verified 2026-08-28 — version,
plugin renames, symbol-server dependency, `netscan`/`netstat` behaviour, `apihooks`, `_EPROCESS`
field widths. **Not re-researched.** This pass covers only what those blocks do not.

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"What was the full command line…"* — assumes the string is a record | 🔴🔴🔴 **It is a claim the process makes about itself.** Volatility 3's plugin is documented *"Extracts the cmdline from PEB"* and reads `peb.ProcessParameters.CommandLine.get_string()`; Microsoft: `PEB.ProcessParameters` is *"A pointer to an RTL_USER_PROCESS_PARAMETERS structure that contains process parameter information such as the command line."* **That buffer is user-mode memory inside the process.** ATT&CK **T1564.010 Process Argument Spoofing** (tactic **Stealth**): adversaries *"hide process command-line arguments by overwriting process memory"*, may *"override the PEB"* via `WriteProcessMemory()`, and can *"execute a process with malicious command-line arguments then patch the memory with benign arguments that may bypass subsequent process memory analysis."* ⚠️ **A second variant needs no overwrite** — shorten the `UNICODE_STRING` **Length** while leaving the buffer intact (parent spawns `CREATE_SUSPENDED`, patches, `ResumeThread`), so **carve past `Length`**. 🔴 **No kernel structure stores the command line** — `SeAuditProcessCreationInfo` and `ImageFileName` are the **image path**. 🟢 The one independent source is **`windows.consoles`/`cmdscan`** (*"Looks for Windows console buffers"*), console-launched commands only. ⚠️ **Usually unavailable for exited processes** — the plugin's own error path is *"Required memory at … is not valid (process exited?)"*. | [Vol3 cmdline source](https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/cmdline.html) · [MS PEB](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb) · [T1564.010](https://attack.mitre.org/techniques/T1564/010/) · [NVISO](https://blog.nviso.eu/2020/02/04/the-return-of-the-spoof-part-2-command-line-spoofing/) · [Vol3 consoles](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.consoles.html) |
| 2 | *(implicit)* "`malfind` finds injected code" | 🔴 **It lists candidates, and its own docstring says so:** *"Lists process memory ranges that **potentially** contain injected code."* ⚠️ **And the usual one-line summary of its criterion is wrong.** Source: it needs `"EXECUTE" in protection_string and "WRITE" in protection_string`, **and** `(private_memory == 1 and tag == "VadS") or (private_memory == 0 and protection_string != "PAGE_EXECUTE_WRITECOPY")` — **file-backed regions are not universally excluded**, only WRITECOPY ones. It also checks `PAGE_EXECUTE_READ` **dirty** pages *"to detect non-writable memory regions having been injected using elevated WriteProcessMemory()"*, and skips regions *"entirely unavailable due to paging, entirely consisting of zeros, or a combination of the two"* — 🔴 **so paged-out injected code does not appear at all.** 🔴🔴 **JIT is the dominant false positive:** *"JIT code … generates assembly code at runtime which lives in unbacked or floating memory regions"*, and *".NET or Java applications are a couple of examples"*; also EDR that *"inject[s] code to some or all processes"*, and packers/DRM that *"decrypt or deobfuscate their core functionality in memory."* ⚠️ **A named list of benign processes is NOT VERIFIED** — teach the categories, not a safe-list. 🔴 **The plugin is `windows.malware.malfind`** (**D1**). | [Vol3 malfind source](https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/malware/malfind.html) · [Vol3 malfind doc](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.malware.malfind.html) · [Elastic, Hunting in Memory](https://www.elastic.co/security-labs/hunting-memory) |
| 3 | Q5: *"first five bytes … of the Meterpreter shellcode"*, example **`4d5a9000`** | 🔴🔴 **The example is an MZ header, and MZ means it is not raw shellcode.** Microsoft: *"The first two bytes of the specified image has 0x5a4d, which is \"MZ\""*; the PE spec places the MS-DOS stub *"at the front of the EXE image"*. Elastic: reflective DLL injection leaves *"the full MZ/PE header"* at the start of unbacked executable memory, and *"Typical code sections are of type 'Image' and map to a file on disk. However, these are type 'Private' and do not map to a file on disk."* **So `4D 5A…` = an injected PE image (T1055.002 Portable Executable Injection — Stealth, Privilege Escalation; or T1620 Reflective Code Loading — Stealth), while raw shellcode has no header at all.** ⚠️ **Absence of MZ still does not prove raw shellcode** — reflective loaders routinely strip the header once mapped. 🟢 **Report the region's structure, not five bytes.** ✅ T1055.001 DLL Injection — Stealth, Privilege Escalation. | [MS PE on memory dump](https://learn.microsoft.com/en-us/archive/blogs/coreinternals/portable-executable-file-format-on-memory-dump) · [MS PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) · [Elastic](https://www.elastic.co/security-labs/hunting-memory) · [T1055.002](https://attack.mitre.org/techniques/T1055/002/) · [T1620](https://attack.mitre.org/techniques/T1620/) |
| 4 | Q4: *"the final process in the chain"* — assumes the tree is the truth | 🔴🔴 **Three independent reasons it may not be.** (a) `pstree` *"enumerates processes using the same technique as `pslist`, so it will also not show hidden or unlinked processes"*, while `psscan` *"can find processes that previously terminated (inactive) and processes that have been hidden or unlinked by a rootkit"* — ⚠️ though *"rootkits can still hide by overwriting the pool tag values."* **Run both and diff.** (b) 🔴 **PID reuse** — Windows releases a PID once the last handle closes, so a recorded PPID can resolve to an unrelated later process. (c) 🔴🔴 **Parent PID spoofing, ATT&CK T1134.004** (**Stealth**, Privilege Escalation): a process *"explicitly forges its parent"* via `EXTENDED_STARTUPINFO` + `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` through `UpdateProcThreadAttribute` → `CreateProcess`, *"resulting in mismatched/implausible lineage."* 🟢 **Falsifiability check: `CreateTime` ordering — a child cannot predate its claimed parent.** ⚠️ *(our own synthesis, not a quoted source)* | [Volatility Command Reference](https://github.com/volatilityfoundation/volatility/wiki/Command-Reference) · [Vol3 psscan](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.psscan.html) · [Vol3 pstree](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.pstree.html) · [MS, PID reuse](https://devblogs.microsoft.com/oldnewthing/20110107-00/?p=11803) · [T1134.004](https://attack.mitre.org/techniques/T1134/004/) |
| 5 | tip 1: *"Threat actors tend to mimic system applications"* | 🔴 **The ATT&CK technique has been RENAMED. It is now `T1036.005` "Masquerading: Match Legitimate **Resource** Name or Location"** (tactic **Stealth**) — *"Adversaries may match or approximate the name or location of legitimate files, Registry keys, or other resources when naming/placing them."* **Older material says "Match Legitimate Name or Location".** ✅ **Repo grepped: `T1036` appears nowhere — forward-looking correction only, no back-propagation.** 🟢 Three checks, from SANS *Find Evil*: *"process names that appear legitimate but originate from the **wrong directory path** or with the **wrong parent process or SID**"* — `svchost.exe` expected at *"`%SystemRoot%\System32\svchost.exe`"*, parent *"services.exe"* — plus *"Checking for signed code can help reveal suspicious executables"*, and misspellings like *"scvhost.exe or lssass.exe"*. ⚠️ **`_EPROCESS.ImageFileName` truncates at 15 bytes** (**E10**), so the name column is the least reliable one on screen. | [T1036.005](https://attack.mitre.org/techniques/T1036/005/) · [SANS Find Evil](https://networkforensic.dk/Tools/Files/cheat-sheets/Poster_Find_Evil.pdf) |
| 6 | *"Volatility is installed"* — no version named | ⚠️ **A room that names no version is a room whose commands may stop working within the month.** 🔴 **The second rename wave removes on 2026-09-25 — 27 days after this extraction** — taking `windows.amcache`, `cachedump`, `hashdump`, `lsadump`, `scheduled_tasks` to `windows.registry.*` (**E10**). 🟢 **None of this room's plugins are in that wave**, and `pslist`/`psscan`/`pstree`/`cmdline`/`netscan`/`netstat`/`filescan`/`dumpfiles`/`dlllist` are all verified live (**D1**). ⚠️ **But our own material must carry a version bound on every Volatility command**, and the `malfind` shim (`removal_date="2026-06-07"`, **already past**) is the worked example of why. | blocks **D1**, **E10** |
| 7 | tip 3: *"Some output has been prefetched in `/home/ubuntu/out`"* | ⚠️ **A convenience that hides the failure our lab will hit.** Volatility 3 fetches Windows symbols from Microsoft's symbol server on first use (**D2**) — *"This breaks our lab"*, since Part 6 requires it offline. **Pre-computing the output means students never meet the error**, and `windows.netstat` *"hard-fails without tcpip symbols"* (**E10**). 🟢 **Our version pre-populates `volatility3/symbols/` on `CLEAN-TOOLS` (D17) and says why**, rather than pre-computing the answers. | blocks **D2**, **E10** |

### NOT VERIFIED — carried forward honestly

- **A named list of specific benign processes that routinely trip `malfind`** — categories verified
  (.NET/CLR, Java, browser JS engines, EDR-injected), a top-tier named list not. **Teach categories.**
- **The `CreateTime`-ordering falsifiability check** is our own synthesis, not a quoted source. It
  follows from the field's meaning and is trivially demonstrable in a lab — **demonstrate it before
  putting it on a slide.**
- **Which Volatility version the room's lab runs.** Not determinable without starting it.
- **Whether the room's answer to Q5 is in fact an MZ or a shellcode prologue** — not determinable
  without running the lab, and §2.6 is written to cover both.

## 4. Evidence used

**A memory image inside a lab VM:** `SRV-DMZ-GW-evidence.mem` at `/home/ubuntu/`, with pre-computed
plugin output in `/home/ubuntu/out`.

- **Downloadable?** ⚠️ **No.** **Reusable?** 🔴 **No.**
- **`ecdfp-evidence` action: none.** 🔴 **Fourth room running with no evidence set.** `EVS-10` remains
  unallocated. ⚠️ **The whole Honeynet module is live-VM-only** — confirmed again — so **our S5/S6
  Windows intrusion image still has to be staged on `EVI-SRC01` (D19) or sourced from CFReDS (D36).**

### 🔴 Evidence with no provenance — noted, and deliberately not counted as a defect

The image arrives with **no hash, no acquisition tool or version, no operator, no capture start or
end time, and no chain of custody.** Against **D20 criterion 1** it would fail on arrival.

⚠️ **I am not adding this to the safety/handling tally, and the reason matters:** *"a training lab
ships evidence without a chain of custody"* is near-universal across the corpus, and counting it
here — in the twenty-fifth room — would be arbitrary and would inflate a number whose value is that
it is conservative. **The tally stays at 10.**

🟢🟢 **It is worth more as an exercise than as a complaint** (§2.8): hand students the same dump
*with* an acquisition record and have them compute, from the elapsed capture time alone, **how wide
the smear window is** and therefore how precisely two observations can be ordered.

### Critique of the scenario brief

🟢🟢 **The best-written brief in the module, and the only one whose failures are organisational
rather than technical.** *"I just need one solid answer, not ten theories"* · *"The logs for
SRV-DMZ-GW looked normal, but the engineering team kept reporting odd slowdowns"* · *"With deadlines
approaching and pressure mounting."*

**Three things to use verbatim in `S1`:**

1. **"The logs looked normal."** After room 24 we can say precisely what that may mean: **nothing was
   configured to log** (block **L1**). *"Normal" is not a finding; it is the absence of one*, and
   distinguishing *"no evidence of X"* from *"evidence of no X"* is the course's core habit.
2. **Users reported the symptom and were not believed.** The engineering team had the only real
   detection signal on the network and it was treated as noise.
3. 🔴 **A manager applying schedule pressure to an investigation.** *"One solid answer, not ten
   theories"* is a demand for **certainty ahead of evidence** — and **D20 criterion 4 exists to
   resist exactly that.** ⚠️ **The correct professional answer to that manager is a stated
   limitation**, not a faster conclusion, and students should rehearse saying so.

⚠️ **One unexamined fact:** the investigator here is **Matthew**, whose domain hash was stolen on the
previous host in stage 2. **The room never notes that the person chasing the intrusion is a
compromised account holder.** 🟢🟢 **That is a free and excellent exercise** — *"who should not be
running this investigation, and why?"* — and it is the kind of question a real DFIR engagement asks
in its first hour.

## 5. Lab design worth reusing

### 5.1 🟢🟢 The module's edge, investigated from one side

Q6 asks for the 3389 destination — **③ → ④, crossing the DMZ/CORE boundary**, the single most
important edge on the map (room 23 §7). **The room proves the connection from the source's memory and
stops there.** Whether it *succeeded* is stage 4's evidence.

🟢🟢 **That is the module working exactly as designed, and it is the shape our S6 capstone should
have**: each session establishes what its own host can support, states the limitation, and **the next
session closes it.** ⚠️ **It only works if the limitation is stated** — otherwise a student reads a
`netscan` row as a completed lateral movement, which is four claims from one artifact (§2.7).

### 5.2 🟢🟢 Memory as the answer to a disk-side gap

§1 covers it. **Adopt as the framing for `S2-03`.** The argument for memory-first is usually taught as
volatility ordering; **this pair of rooms makes it concrete and specific** — room 24 shows the command
line is not recorded on a default host, room 25 recovers it from the PEB. 🔴 **And the pair only
teaches the right lesson if §2.2's caveat travels with it**, or we will have replaced "the disk has
no record" with "memory is authoritative", which is worse.

### 5.3 ⚠️ Pre-computed output is the wrong kindness

Tip 3 removes the symbol-server failure (**D2**), which is the single most likely thing to break in
an offline classroom. 🟢 **Our version pre-populates the symbol store and tells students that is what
we did** — the fix is the lesson; hiding the failure is not.

### 5.4 🟢 The scenario's failures are organisational

§4 covers it. **Adopt all three for `S1`** — *"the logs looked normal"*, users disbelieved, and a
manager demanding one answer instead of ten theories.

### 5.5 🔴 Safety and handling defects

**None new.** The room is offline analysis of a captured image — **the safest working pattern in the
corpus**, and worth saying so after three rooms of live-system defects.

🟢🟢 **In fact it is the counter-example that completes the pattern from block L8.** Rooms 22, 23 and
24 all had students act on the live system; **this room hands over a captured artifact and has them
analyse it on an analyst machine.** That is the correct order — *collect, then analyse a copy* — and
**it is worth showing students the two side by side**, because the contrast makes the rule obvious in
a way a slide cannot.

⚠️ The provenance gap (§4) is real but deliberately **not** counted, for the reason given there.

**Running total: 10 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24. Four endanger the analyst's
machine; six endanger the evidence. Unchanged.**

## 6. Question patterns

**Six scored questions tracing one process chain** — initial file → PID → command line → final
process → injected code → outbound connection. 🟢 **The order is the analysis order**, and each answer
feeds the next, which is good design for a 60-minute investigation.

**⚠️ No answer formats are specified**, unlike rooms 19–24 — except Q5's, which is the one that causes
the trouble. 🔴 **And there are no timestamp questions at all**, which is unusual for a memory room
and quietly avoids the hardest thing about a memory image: **that everything in it shares one
approximate time** (§2.8).

**🔴🔴 Q5 is the sharpest instructional error found in 25 rooms.** It asks for *"the first five bytes
… of the **Meterpreter shellcode**"* and offers **`4d5a9000`** — an **MZ header** — as the example
format. **MZ means a mapped PE image, which is what shellcode is not** (§2.6). 🟢🟢 **Inverted, it is
the best five minutes in the room**: *"the question says shellcode and the example shows MZ — which
is it, and how would you tell?"* **Our version asks that question deliberately.**

**⚠️ Stems name their conclusions, again** — *"the **initial** malicious file"* · *"the **Meterpreter**
shellcode"* · *"perform a **lateral movement** using port 3389"*. **Eighth room running.** 🔴 Q6 is
the worst: **four claims folded into one stem** — a connection, on that port, that was RDP, that
constituted lateral movement — from an artifact that supports the first.

**🔴 Twenty-fifth room, no "cannot be determined" question** — and a memory image is the richest
possible source of them, because **every structure in it is either attacker-writable or
time-smeared:**

| the room could have asked | correct answer |
|---|---|
| *"`windows.cmdline` shows a benign command line for PID 1234. Was the process launched benignly?"* | 🔴🔴🔴 **Cannot be determined.** The PEB is user-mode memory the process can rewrite — **T1564.010**: *"execute a process with malicious command-line arguments then patch the memory with benign arguments that may bypass subsequent process memory analysis."* **A clean command line is never exculpatory.** The best row in the corpus so far, because it inverts the room's own Q3. |
| *"`pstree` shows `evil.exe` spawned by `explorer.exe`. Did the user launch it?"* | 🔴🔴 **Not established.** PPID is attacker-settable (**T1134.004**), and PIDs are reused. **Check `CreateTime` ordering — a child cannot predate its parent.** |
| *"`malfind` flags an RWX region in a .NET process. Is it injected code?"* | 🔴🔴 **Cannot be determined from `malfind` alone** — *"JIT code … lives in unbacked or floating memory regions"*, and *".NET or Java applications are a couple of examples."* The plugin lists what *"potentially"* contains injected code. |
| *"`malfind` shows nothing for PID 1234. Was code injected into it?"* | 🔴 **No.** Regions *"entirely unavailable due to paging"* are skipped — **paged-out injected code never appears.** |
| *"The injected region starts `4d5a90…`. What shellcode is it?"* — i.e. **the room's own Q5 example** | 🔴🔴 **Wrong question — that is a PE header, not shellcode.** The finding is *"a mapped PE image was injected"* (T1055.002 / T1620), and the family question needs the image, not five bytes. |
| *"`netscan` shows 172.16.2.9:3389. Did the attacker log into that host?"* | 🔴🔴 **Cannot be determined.** `netscan` recovers **closed** sockets from freed pool memory, so the entry may be stale; port 3389 is a port, not a protocol; and a session is not a logon. **The destination's own event log answers it — that is stage 4.** |
| *"`psscan` found a process `pslist` missed. Was it hidden by a rootkit?"* | ⚠️ **Not established** — `psscan` finds **terminated** processes too. **Terminated is the boring explanation and it is usually the right one.** |
| *"The dump shows process X running. Was it running during the incident?"* | 🔴🔴 **Cannot be determined.** Our own knowledge base already says it: a dump *"proves state at capture time only … a process seen here does not prove it was running during the incident, and a process absent here does not prove it never ran."* |

🟢🟢 **Eight, and three of them attack the room's own questions directly.** ⚠️ **Note what has
happened to this tally over four rooms:** the "cannot be determined" questions are no longer
hypothetical improvements — **in rooms 24 and 25 they are the *correct* answers to questions the rooms
actually ask.** That is a stronger claim than the one this project started with, and it should be
stated that way in the course rationale.

## 7. Figures

**No room-specific figure. The module map is present and byte-identical to rooms 23 and 24**
(§5.1 of `elevatingmovement.md`); ⚠️ **the remaining images were not enumerated individually** — the
DOM query was not re-run for this room, since rooms 23–24 established the pattern. **Recorded as
not-checked rather than claimed decorative.**

🔴 **Sixth room running with no conceptual figure**, and this is the one where it hurts most: a
60-minute memory investigation across process trees, VAD protections, PE headers and pool-scanned
sockets, **with no picture of any of it.**

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F19 | **Where the command line lives** | A process box with the **PEB** inside it shaded *"user-mode — the process can write here"*, and the kernel's `_EPROCESS` beside it holding `ImageFileName` / `SeAuditProcessCreationInfo` shaded *"kernel — image path only"*. A red arrow from the process back into its own PEB labelled **T1564.010**. Third panel: `conhost` memory, labelled *"independent, console only."* | **🔴 P1** | §2.2 — the whole point of the room, and the correction the room does not make. Pairs with **F14** (room 24) to make the disk/memory argument complete. |
| F20 | **MZ or not** | Two dumped regions side by side: one beginning `4D 5A 90 00…` labelled *"mapped PE image — T1055.002 / T1620"*, one beginning with instruction bytes labelled *"raw shellcode"*. A footnote: *"a stripped header looks like the second — check the section layout."* | **🔴 P1** | §2.6, and it turns the room's own broken example into the lesson. |
| F21 | **Three views of one process list** | Venn-ish diagram: `pslist` (linked, live), `psscan` (adds terminated + unlinked), `pstree` (= pslist, arranged). Each region annotated with what it can miss. | **🟢 P2** | §2.3 — why the answer to *"the final process in the chain"* depends on which plugin you ran. |
| F22 | **The smear window** | A horizontal time bar with capture start and end marked, pages sampled at different points, and two process boxes that **never coexisted** both present in the image. Caption: *"a smear, not a snapshot."* | **🔴 P1** | §2.8, and it converts our knowledge base's best sentence into a picture. Serves `S2-03` directly. |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 3"* — correct, and it is also the strongest single source for `S2-03`.

Amend the Part 1 row: **its value is the memory-versus-disk argument (§5.2) and the PEB caveat
(§2.2)**, not the Volatility mechanics, which blocks D and E10 already cover.

### Rows this strengthens

- **`S2-03`** (*"Memory acquisition — why it comes first, the tools, and the pitfalls"*) — 🟢🟢
  **the room supplies the row's best argument**: memory holds the command line that the disk is *not
  configured* to record (block **L1**), which is far more persuasive than "memory is volatile, take
  it first." Plus figure **F22** and the smear-window exercise (§2.8).
- **`S6-10`** (*"Volatility 3 in the capstone — processes, network connections, injected code"*) —
  🟢🟢 **this room is a template for that row, question for question.** Add **F19**, **F20**, **F21**,
  the `pslist`/`psscan` diff, and the `malfind`-as-candidates framing.
- **`S5-06`** — 🟢 §2.4's masquerading checks (path · parent · signature) sit beside *presence vs
  execution* as the second "the name is not the evidence" lesson. ⚠️ **`S5-06` has now taken material
  from rooms 21, 23, 24 and 25** — see the minutes note.
- **`S1-04`** (report template) — 🟢🟢 **§2.2 is the cleanest criterion-4 example in the corpus:**
  *"the PEB of PID 1234 contains string X"* is a finding; *"the attacker ran X"* is an interpretation
  that assumes the PEB was not patched.
- **`S1`** — the three organisational failures from §4, and the *"who should not be running this
  investigation"* question.
- **`S6-09`** — the stated-limitation handoff between stages (§5.1).

### 🔴 Back-propagation: two, and I performed the first

1. 🔴🔴 **`knowledge_base/` EXISTS — three of my own notes said it did not, and I have corrected all
   three.** It was built 2026-08-29 (the same day, in parallel with this extraction) by
   `ecdfp-intake` from `Resources/`: five condensed module files, an `instructor/` folder of 8
   session notes, and `_source_text/` holding **10 INE units (2,218 pages)** plus **9 instructor
   decks**. `exfilnode.md`, `initialaccesspot.md` and `elevatingmovement.md` were patched in place
   and re-verified (all three still PASS). ⚠️ **`evidence/`, `packages/`, `cases/` and `labs/` still
   do not exist.**
   🟢 **And the sharper point survives the correction: not one of the 25 room notes has been through
   `ecdfp-intake`.** The knowledge base was built from INE courseware and the instructor's own decks
   — **none of the THM research has landed in it.** ⚠️ **The handoff prompt's state description was
   simply out of date, which is a good argument for checking the filesystem rather than trusting a
   carried-forward summary.**
2. 🟢 **`T1036.005` has been renamed** to *"Match Legitimate **Resource** Name or Location"*.
   ✅ **Repo grepped: `T1036` appears nowhere — forward-looking only, nothing to patch.**

✅ Also checked and clean: `T1055.001/.002` and `T1620` appear only in
`windows-memory-and-network.md` §3 and block E11, **both already carrying the correct Stealth
tactic**; `T1564.010` and `T1134.004` are new to the repo.

### Minutes

**Net zero in rows, but the row-overload problem from room 24 is now measurable.**

Everything lands in `S2-03`, `S6-10`, `S5-06`, `S1-04`, `S1` and `S6-09` as content. **No new rows.**

🔴 **`S5-06` is 20 minutes and has now absorbed material from four rooms** (21 Amcache/ShimCache
misreading · 23 state-vs-event · 24 the `0000` prefix, the 30 MB truncation and presence-not-execution
· 25 masquerading checks). ⚠️ **"No new rows" has been true for four consecutive rooms while the
content inside one row roughly doubled.** **That is not free, and the S5 re-split must size `S5-06`
explicitly rather than counting rows.** Recorded with the list so the re-split has it.

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twentieth room carrying the S5 overdraft.**

### Out of scope

Meterpreter tradecraft, shellcode authoring, and Volatility plugin development. ⚠️ One item sits on
the line: **PE structure**. We teach headers and magic bytes in **`S3-02`/`S3-03`** (file signature vs
extension) — 🟢🟢 **and §2.6 is the same lesson arriving in memory instead of on disk.** **One
cross-reference in `S3-02`: "the MZ you learn here is the MZ that tells you a PE was injected in S6."**
**That costs one sentence and ties two sessions together.**

### Still unresolved

- **S5 re-split** — twentieth room, now with **`S5-06` row overload** as a sized, listed problem.
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- **No Windows intrusion image in the Priority-2 set** — confirmed for the fourth room running.
- **D19 has no per-session host map** — still gating figure **F7**.
- 🔴 **Volatility symbol pre-population on `CLEAN-TOOLS` (D17)** — **D2** flagged it as lab-blocking;
  this room's tip 3 shows what happens when a lab papers over it instead. **Still not done.**
- **`ecdfp-case` skill** not installed.
- ⚠️ **`knowledge_base/` exists but no room note has been intaken into it** — see back-propagation.

## 9. Links

**Room** — <https://tryhackme.com/room/lostinramslation>
**Module** — Honeynet Collapse, stage 3 of 6. Previous: <https://tryhackme.com/room/elevatingmovement>.
Next: <https://tryhackme.com/room/crmsnatch>.
**Companion notes** — `elevatingmovement.md` (stage 2 — block **L1**, the disk-side gap this room
answers) · `initialaccesspot.md` (the module map) · `memory-acquisition.md`,
`volatility-essentials.md`, `windows-memory-and-processes.md`, `windows-memory-and-network.md` (the
Volatility base this room builds on) · `honeynet-collapse-module.md` (the arc, after stage 6) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **D**, **E10**, and new block **M**.

**Citations from §3, by finding:**

- #1 command line and the PEB — Vol3 `cmdline` source
  <https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/cmdline.html> ·
  MS `PEB` <https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb> ·
  T1564.010 <https://attack.mitre.org/techniques/T1564/010/> ·
  NVISO, command-line spoofing
  <https://blog.nviso.eu/2020/02/04/the-return-of-the-spoof-part-2-command-line-spoofing/> ·
  Vol3 `consoles` <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.consoles.html> ·
  McAfee, `_EPROCESS` field annotations
  <https://www.mcafee.com/blogs/other-blogs/mcafee-labs/in-ntdll-i-trust-process-reimaging-and-endpoint-security-solution-bypass/>
- #2 `malfind` — Vol3 source
  <https://volatility3.readthedocs.io/en/stable/_modules/volatility3/plugins/windows/malware/malfind.html> ·
  Vol3 doc <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.malware.malfind.html> ·
  Elastic, *Hunting in Memory* <https://www.elastic.co/security-labs/hunting-memory>
- #3 MZ and PE injection — MS, PE format on a memory dump
  <https://learn.microsoft.com/en-us/archive/blogs/coreinternals/portable-executable-file-format-on-memory-dump> ·
  MS PE format <https://learn.microsoft.com/en-us/windows/win32/debug/pe-format> ·
  T1055.002 <https://attack.mitre.org/techniques/T1055/002/> ·
  T1055.001 <https://attack.mitre.org/techniques/T1055/001/> ·
  T1620 <https://attack.mitre.org/techniques/T1620/>
- #4 process enumeration — Volatility Command Reference
  <https://github.com/volatilityfoundation/volatility/wiki/Command-Reference> ·
  Vol3 `psscan` <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.psscan.html> ·
  Vol3 `pstree` <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.pstree.html> ·
  MS, PID reuse <https://devblogs.microsoft.com/oldnewthing/20110107-00/?p=11803> ·
  T1134.004 <https://attack.mitre.org/techniques/T1134/004/>
- #5 masquerading — T1036.005 <https://attack.mitre.org/techniques/T1036/005/> ·
  SANS *Find Evil* <https://networkforensic.dk/Tools/Files/cheat-sheets/Poster_Find_Evil.pdf>
- #6, #7 Volatility environment — blocks **D1**, **D2**, **D4**, **E10** (verified 2026-08-28)
