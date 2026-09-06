---
room: Supplemental Memory
url: https://tryhackme.com/room/supplementalmemory
module: Advanced Endpoint Investigations → **Memory Analysis** — the module's **capstone**, and the
        last room in it. 🟢 The module page names all eight rooms in order: Memory Analysis
        Introduction · Memory Acquisition · Volatility Essentials · Windows Memory & Processes ·
        Windows Memory & User Activity · Windows Memory & Network · **Linux Memory Analysis** ·
        Supplemental Memory. ⚠️ The seventh is on our do-not-extract list (**D38**) and sits
        immediately before this room. **It creates no dependency — room 32 is Windows-only.**
feeds: `S6-09` (capstone shape), `S6-10` (Volatility 3), `S2-03`, and the memory homework track.
       🟢🟢 **The first room in all 32 to publish an acquisition hash** (§2.3) — and it publishes an
       **MD5 only** (§3 #1). **Rooms 31 and 32 are the same error in opposite directions: room 31
       recommends MD5/SHA-1, room 32 practises it.**
       🟢🟢 Supplies **three reusable lateral-movement lineage signatures** (§2.1) — the most
       directly transplantable teaching asset found in the Priority-3 set.
difficulty / time: **Medium** · 60 min · 5 tasks · 15 scored questions · Premium ·
                   **1,976 completions · 53 recommends.** 🔴 **The same module's intro room has
                   13,179 completions. 85% of the people who start this module never reach its
                   capstone** (§8).
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (accordion loop, 5/5 tasks, 10,360 chars)
completeness: **all 5 tasks read in full.** 0 sections NOT READ.
              ⚠️ **Filed as Priority 3, but this note is not short, and that is a considered
              deviation.** The Priority-3 label was assigned from the room's position in the path
              outline, not from its content. **The content is a hands-on lab with real evidence,
              three reusable signatures and a new plugin.** Rooms 30 and 31 earned short notes;
              this one did not.
              🔴 **R8 — the room publishes plaintext SSH credentials for the lab VM.** The fact is
              recorded; **the value is not reproduced anywhere in this note.**
              ⚠️ **The lab machine was NOT started and no Volatility plugin was run** (§4). Every
              artifact claim below is read from the room's own worked examples and question stems,
              **not from the dump.** Where that limits a claim, it is said in the box.
---

## 1. What the room teaches

**How to recognise lateral movement from a process tree — as three named, literal, transplantable
signatures — and then how to find who ran what, with a plugin our notes have never mentioned.**

🟢🟢 **This is the strongest applied room in the Priority-3 set and the best-designed memory room in
the extraction after room 25.** It does one thing rooms 30 and 31 do not: **it hands the student a
detection pattern in the shape they will meet it in an alert queue** — parent, child, grandchild,
with the payload name left arbitrary. Task 3 gives all three as raw `pstree` fragments:

- **PsExec** — `services.exe → psexesvc.exe → <payload>`
- **WMI** — `svchost.exe → wmiprvse.exe → <payload>`
- **PowerShell Remoting** — `svchost.exe → wsmprovhost.exe → cmd.exe → conhost.exe + <payload>`

**Each is drawn from a different named intrusion set's dump** — `ransomhub.dmp`, `conti.dmp`,
`FIN12.dmp` — which is a small touch that does real work: it says *these are three ways in, not three
variants of one*. 🟢 **We should copy the device wholesale** (§5.2).

🟢🟢 **It publishes the evidence hash.** *"File Name: `WIN-015-20250522-111717.dmp`  ·  File MD5 Hash:
`15fd7b30b20b53e7374aa8894413c686`  ·  File Location: `/home/analyst/memory/WIN-015`"* —
**the first room in thirty-two to publish any acquisition hash at all.** After thirty-one rooms of
handing students evidence with no integrity claim attached, one room finally does the thing every one
of them tells students to do. 🔴 **And it is an MD5** (§3 #1).

🟢 **It introduces `windows.getsids --pid N`** — process owner SID *and* group membership, in one
command, entirely offline. **No note in our corpus mentions this plugin**, and it closes a real gap:
we teach students to find a malicious process and have never taught them how to answer *"running as
whom, with what group rights?"* from the image alone.

🟢 **One question stem is correctly hedged** — *"which well-known hacker tool is **most likely** the
malicious process?"* **"Most likely" is the epistemically honest form** and it is the third hedged
stem found in thirty-two rooms.

**What it gets wrong:**

- 🔴🔴 **The three signatures are presented as facts with no falsifiability caveat whatsoever** — no
  PPID spoofing (**T1134.004**), no PID reuse, no `psscan` diff, and — the sharpest one —
  **no mention that PsExec's remote service name is a documented command-line option.** §3 #2, and
  **M4**.
- 🔴 **MD5 as the sole integrity value.** §3 #1.
- 🔴 **The Volatility symbol download is euphemised as *"initial setup and caching"*.** **D2** —
  on an air-gapped lab it does not slow down, it fails. §3 #7.
- 🔴 **`precooked/` hides the failure.** Same defect as room 25's tip 3, in a room whose whole point
  is running the plugins. §5.4.
- 🔴 **A SID is a scored answer** — **D41** borderline. §6.
- ⚠️ **Task 4's teaching example silently changes topic.** It is headed *privilege escalation via
  service*, and the worked example is genuinely that; **but the room's own Task 5 recap claims the
  student "uncovered privilege escalation and credential dumping indicators", and no task teaches a
  credential-dumping artifact at all.** §2.8.

## 2. Artifacts — one 6-box block each

⚠️ **The lab was not started** (§4). These blocks describe the artifacts **the room teaches**, sourced
from its worked examples and question stems. Where a claim would need plugin output to stand, the box
says so.

### 2.1 The process-tree lineage as a lateral-movement signature

- **What it is** — a parent→child→grandchild chain in `windows.pstree` whose **middle term is the
  service the remote-execution mechanism starts on the target**: `psexesvc.exe` for PsExec,
  `wmiprvse.exe` for WMI, `wsmprovhost.exe` for PowerShell Remoting. **The payload name is arbitrary;
  the middle term is the signature.**
- **Where it lives** — the `_EPROCESS` list in the memory image, reached by `windows.pstree` (which
  walks the same active-process list as `pslist` — **M4**).
- **What it proves** — 🟢🟢 **that a remote-execution mechanism ran on this host, and which one.**
  That is a strong, specific, mechanism-level finding, and it is exactly the shape a triage analyst
  needs.
- **What it does NOT prove** — three things, and 🔴🔴 **the room states none of them**:
  1. ⚠️ **That the lineage is real.** **PPID is an attacker-settable field** — `T1134.004`, *"a
     process 'explicitly forges its parent'"* (**M4**). A forged PPID produces this exact picture
     with no remote execution behind it.
  2. 🔴🔴 **That the absence of `psexesvc.exe` means PsExec was not used.** Microsoft's own PsExec
     page documents the switch: ***"-r | Specifies the name of the remote service to create or
     interact with."*** **The service name the room teaches as a signature is a documented
     command-line option.** A one-flag rename defeats it, and **the room teaches the signature as
     though it were a property of the tool.**
  3. ⚠️ **Who did it.** A lineage names a mechanism, never an operator (**O4**'s rule, restated for
     memory).
- **How to parse it** — `vol -f <dump> windows.pstree`, then 🟢 **diff against `windows.psscan`**
  (**M4**): `pstree` cannot show unlinked or terminated processes, and **the interesting middle term
  is often already gone.** ⚠️ **A `psscan`-only hit is usually just a terminated process — the
  boring explanation is usually right.**
- **Anti-forensics / false-positive caveat** — 🟢 **false positives are real and boring**:
  `wmiprvse.exe` under `svchost.exe` is the **normal** state of any host that has ever answered a WMI
  query, and `wsmprovhost.exe` is the normal state of any host managed by PowerShell Remoting.
  🔴🔴 **The signature is the grandchild, not the middle term** — and the room's three fragments,
  read as diagrams rather than as hypotheses, teach the student to alert on the middle term.
  ⚠️ **Source strength is uneven and we must say so:** `wsmprovhost.exe` is confirmed by Microsoft's
  own PowerShell Remoting documentation; **the full WMI chain is corroborated only by a community
  DFIR source** (§3 #3).

### 2.2 `windows.getsids` — the process owner and its group membership

- **What it is** — the plugin that answers *"running as whom?"* from the image alone. Volatility 3's
  own description: ***"Print the SIDs owning each process."***
- **Where it lives** — the process token in the memory image; names are resolved from a **bundled
  well-known-SID table plus the `ProfileList` registry key read out of the image's own hives**.
  🟢🟢 **Entirely offline — no live host, no exported hive, no network lookup.** That matters for a
  cold-lab exercise and it is worth stating to students explicitly.
- **What it proves** — 🟢 **the security context a process was running in**, including group
  membership, which is what turns *"a suspicious binary ran"* into *"a suspicious binary ran with
  Domain IT Administrators rights."* **That second sentence is the one that changes an incident's
  severity.**
- **What it does NOT prove** — ⚠️ **that the human owning the account did it.** The room's own
  scenario is the counter-example it does not draw: **Cain's credentials were stolen from another
  host**, so every artifact bearing his SID on WIN-015 is evidence of a *credential*, not of *Cain*.
  🔴 **The room asks for the SID and the group as scored answers and never says this**, which is the
  single most useful sentence available in the whole room.
- **How to parse it** — `vol -f <dump> windows.getsids --pid <N>`; `--pid` is a documented, optional
  list filter. ⚠️ **Verified against Volatility 3 v2.28.0** (**M6** — bind the version).
  ⚠️ **Name resolution can fail silently**: if the relevant `ProfileList` data is not resident in the
  image, the SID prints unresolved. **An unresolved SID is a paging outcome, not a finding.**
- **Anti-forensics / false-positive caveat** — ⚠️ **Tokens can be manipulated** (`T1134` — *"Access
  Token Manipulation"*): a process may run under a token it stole rather than one it was granted, and
  `getsids` reports the token, which is the correct behaviour and the wrong conclusion if read as
  *"this user launched it"*.

### 2.3 The published acquisition hash and the dump filename

- **What it is** — the room's evidence header: file name `WIN-015-20250522-111717.dmp`, **MD5
  `15fd7b30b20b53e7374aa8894413c686`**, location `/home/analyst/memory/WIN-015`. 🟢🟢 **Two good
  practices in three lines**: an integrity value published with the evidence, and a filename that
  encodes **host + acquisition date + acquisition time**.
- **Where it lives** — in the room brief; in ours it belongs in the evidence manifest and the
  acquisition log.
- **What it proves** — 🟢 **that the file the student holds is the file the room shipped** — and
  nothing more. **A hash is a transfer check, not a provenance claim.**
- **What it does NOT prove** — 🔴🔴 **that the evidence is unaltered, because it is an MD5.** **K7**
  and CERT/CC VU#836068: MD5 answers *"have we seen this file before?"*, not *"is this file
  unaltered?"* ⚠️ **And the filename's timestamp is unqualified** — `20250522-111717` in whose time
  zone? **A forensic filename with a local, unlabelled timestamp is a dating error waiting to
  happen**, and the fix costs one character: `Z`.
- **How to parse it** — `sha256sum` on receipt, recorded next to the room's MD5, **both in the log**.
- **Anti-forensics / false-positive caveat** — ⚠️ **A published hash invites the wrong inference**:
  students read it as *"the evidence is sound"* when it only means *"the download is intact."*
  🟢 **The distinction is a good five-minute discussion and this room is the only place in the path
  that makes it available.**

### 2.4 The full image path of a suspicious process

- **What it is** — Task 4's first question asks for ***"a full path to the process"***, not a name.
  🟢🟢 **That is the right question**, and it is the one artifact in the room that directly defeats
  masquerading (`T1036`): `C:\Windows\System32\svchost.exe` and
  `C:\Users\Public\svchost.exe` are the same name and different findings.
- **Where it lives** — the process image path in the `_EPROCESS`/PEB structures, surfaced by
  `windows.pslist`, `windows.dlllist` and `windows.cmdline`.
- **What it proves** — 🟢 **which file on disk was mapped as this process's image.**
- **What it does NOT prove** — ⚠️ **that the file is still there, or that it is what it was.** The
  path is a string recorded at load time; **the binary can be deleted or replaced afterwards and the
  path in memory does not change.** 🔴 And **the path is read from the same attacker-writable
  structures as the command line where `windows.cmdline` is used** (**M1**).
- **How to parse it** — 🟢 **prefer `windows.pslist` for the image path over the PEB-derived
  sources**, and 🟢🟢 **corroborate against a disk artifact** — Prefetch, Amcache, `$MFT` — which is
  exactly **M7**'s memory/disk pairing rule and the thing this room, being memory-only, cannot do.
- **Anti-forensics / false-positive caveat** — ⚠️ **A legitimate path is not exculpatory**: DLL
  search-order abuse and process hollowing both produce a correct system path with wrong contents.

### 2.5 The process command line

- **What it is** — Task 4 asks ***"What was the malicious command line executed by the process?"***
  and then, from it, infers the tool.
- **Where it lives** — 🔴🔴 **the PEB's `RTL_USER_PROCESS_PARAMETERS`, which is in the process's own
  writable address space.**
- **What it proves** — 🟢 the arguments as they stand **in memory at acquisition time**.
- **What it does NOT prove** — 🔴🔴 **that those are the arguments the process was launched with.**
  **M1** — the PEB is attacker-writable, and a process can rewrite its own command line after start.
  ⚠️ **The room asks the question with no caveat**, exactly as room 25 did, and this is the second
  room in the module to do it.
- **How to parse it** — `windows.cmdline`; 🟢 **corroborate with the 4688 command-line field where it
  exists** — ⚠️ but **L1**: that field is **off by default** and needs two switches, so on most
  hosts there is nothing to corroborate against. **That is the honest state of command-line evidence
  and it deserves saying once, loudly, in `S6-10`.**
- **Anti-forensics / false-positive caveat** — ⚠️ **The inference the room actually wants is
  tool identification from argument shape**, which is sound tradecraft and is **not** the same claim
  as *"this is what was typed"*. 🟢 **Teach them as two separate steps** — the room merges them.

### 2.6 Discovery-tool execution

- **What it is** — Task 3's *"Which processes related to discovery activity were executed by the
  threat actor on this host?"* — the built-in enumeration binaries an operator runs on arrival.
- **Where it lives** — the process list; and, for processes that have already exited, 🟢 **only
  `windows.psscan`** (**M4**).
- **What it proves** — 🟢 **that enumeration commands ran on this host during the dump's lifetime.**
- **What it does NOT prove** — ⚠️ **that the attacker ran them.** Discovery binaries are the same
  binaries administrators and monitoring agents use all day. 🔴🔴 **The room's stem asserts the
  attribution inside the question** — *"executed by the threat actor"* — **which hands the student
  the conclusion and grades them on the list.** The defensible finding is *"these discovery processes
  ran; those in the lineage from §2.1 are attributable to the intrusion, the rest are not."*
- **How to parse it** — 🟢 **the useful discriminator is not the binary, it is the parent**: a
  discovery process whose ancestor is the §2.1 middle term is intrusion activity; the same binary
  under `explorer.exe` on the console is an admin.
- **Anti-forensics / false-positive caveat** — ⚠️ **Discovery is the easiest activity to hide in the
  noise and the hardest to alert on**, which is why the parent matters more than the name.
  ⚠️ **Answer format *"in alphabetical order"* is a grader's convenience, not tradecraft** — it
  discards the execution order, which is the part that tells you what the operator was looking for.

### 2.7 The C2 connection in memory

- **What it is** — Task 3's final question: ***"the Command and Control IP address that the threat
  actor connected to from this host… Format: IP Address:Port."***
- **Where it lives** — the network structures recovered by `windows.netscan` / `windows.netstat`.
- **What it proves** — 🟢 **that a connection object existed, to that endpoint, owned by that
  process.** 🟢🟢 **The process-to-socket binding is the part memory gives you that a firewall log
  does not** — this is **M7**'s pairing seen from the memory side.
- **What it does NOT prove** — ⚠️ **that the connection succeeded, or carried anything.** A recovered
  socket structure may be a **closed, failed or stale** connection — and **memory is a smear, not a
  snapshot**, so its state field may be inconsistent with the rest of the image.
  🔴 **The room's stem says "connected to", which asserts more than `netscan` can support.**
- **How to parse it** — `windows.netscan` for the widest recovery, ⚠️ **accepting that pool-scanning
  returns terminated connections**; 🟢 **corroborate with a network artifact** if one exists.
- **Anti-forensics / false-positive caveat** — ⚠️ **An IP:port is an infrastructure identifier and
  nothing more** — it names a rendezvous point, never an actor (**O5**'s rule, restated).
  🟢 **This is a good, cheap place to teach that discipline**, because the temptation to name the
  group from the IP is at its strongest here.

### 2.8 Credential dumping — the artifact the room claims and does not teach

- **What it is** — Task 5's recap tells the student they *"uncovered privilege escalation and
  credential dumping indicators"*, and the room's own description promises *"credential theft"*.
  🔴🔴 **No task teaches a credential-dumping artifact.** Task 4 teaches **privilege escalation via
  service manipulation** and asks the student to identify a *"well-known hacker tool"* from its
  command line. **The dumping is inferred from the tool's name.**
- **Where it lives** — nowhere in this room. In reality: LSASS process memory (`T1003.001`), and the
  handle to it.
- **What it proves** — ⚠️ **that a tool associated with credential dumping was present and
  argued as though it were dumping.** That is a real and reportable finding.
- **What it does NOT prove** — 🔴🔴 **that credentials were obtained.** And here is the finding that
  matters for us: **L5 — credential dumping leaves no default-on record.** There is no event, no
  default log, no artifact that says *"credentials were taken"*. **The honest answer to "were
  credentials dumped?" on this evidence is: a tool that does that ran; whether it succeeded is not
  determinable from this dump.**
- **How to parse it** — 🟢 **the available corroboration is a handle to `lsass.exe` from a process
  that has no business holding one** — `windows.handles --pid <N>` — **which the room never runs.**
  🟢🟢 **That is a two-minute addition that would convert the room's weakest inference into its
  strongest artifact**, and it is the single best idea to take from this room by inverting it (§5.2).
- **Anti-forensics / false-positive caveat** — ⚠️ **Naming the tool from the command line is exactly
  the "plausible story" failure mode** documented in `shockandsilence.md` §2.8: the argument shape is
  compelling, the conclusion is one inference beyond the evidence, and the room's own hedge —
  ***"most likely"*** — is the correct instinct applied to the wrong question. 🟢 **Hedge the
  outcome, not the identification.**

## 3. Tools and commands

**Commands the room actually puts on screen:** `vol -f <dump> windows.psscan` (the brief's example),
`vol -f <dump> windows.pstree` (three times), `vol -f <dump> windows.getsids --pid <N>` (twice).
**That is all.** Everything else is implied by the questions — `windows.netscan` for §2.7,
`windows.cmdline` for §2.5.

### CURRENCY CHECK

| # | claim as the room teaches it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"File MD5 Hash: `15fd7b30b20b53e7374aa8894413c686`"* — published as **the** integrity value for the evidence, with no SHA-256 alongside | 🟢🟢 **Publishing a hash at all is correct and unique in this corpus** — thirty-one rooms hand over evidence with no integrity value whatsoever. 🔴 **But MD5 alone cannot carry the claim.** **K7** and CERT/CC VU#836068: *"Weaknesses in the MD5 algorithm allow for collisions in output. As a result, attackers can generate cryptographic tokens or other data that illegitimately appear to be authentic."* 🟢🟢 **Rooms 31 and 32 are the same defect in its two forms — one recommends MD5/SHA-1 in doctrine, the other practises it in a lab** — and **that pairing is a better teaching artifact than either room alone** (§5.1). **Our version: publish both, attest to the SHA-256.** | block **K7** · [CERT/CC VU#836068](https://www.kb.cert.org/vuls/id/836068) |
| 2 | `services.exe → psexesvc.exe → <payload>` taught as **the** PsExec signature | 🔴🔴 **Defeated by a documented flag, and the room does not say so.** Microsoft Learn, PsExec: ***"-r  Specifies the name of the remote service to create or interact with."*** **The service name is an operator-supplied parameter.** ⚠️ **NOT VERIFIED: the default name.** Microsoft's own PsExec page documents the rename switch but **never states the unmodified default service name anywhere on the page** — a full-text search for `PSEXESVC` in any case returns zero hits. 🟢🟢 **This is the most valuable single fact in the room's whole currency check, and it inverts the lesson: the durable signature is the *shape* — an unfamiliar service binary spawned directly by `services.exe` from a remote logon — not the string `psexesvc.exe`.** | [Microsoft Learn — PsExec](https://learn.microsoft.com/en-us/sysinternals/downloads/psexec) |
| 3 | `svchost.exe → wmiprvse.exe → <payload>` taught as **the** WMI signature | ⚠️ **Substantially right, but the source strength is weaker than the room implies and we must not overstate it.** Microsoft Learn confirms only the hosting relationship — *"the CPU is consumed by the WmiPrvse.exe process, and there are a few instances where svchost.exe hosting the WMI service (Winmgmt) is consuming high CPU usage"* — which is a **troubleshooting KB, not an architecture reference**, and it does not state that a remotely-created payload is a child of `WmiPrvSE.exe`. 🔴 **No Microsoft Learn page stating the full chain was found.** The full chain is corroborated by a **widely-cited community DFIR source**: *"The process WmiprvSE.exe is what spawns the process defined in the CommandLine parameter of the Create method."* 🟢 **Teach it — and cite it honestly as community-verified, not vendor-documented.** | [MS Learn — WMI high CPU](https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/troubleshoot-wmi-high-cpu-issues) · [Threat Hunter Playbook](https://threathunterplaybook.com/hunts/windows/190810-RemoteWMIExecution/notebook.html) ⚠️ **secondary** |
| 4 | `svchost.exe → wsmprovhost.exe → cmd.exe → …` taught as **the** PowerShell Remoting signature | 🟢🟢 **Confirmed on Microsoft's own PowerShell documentation** — ***"When a local computer connects to a remote computer, WS-Management establishes a connection and uses a plug-in for PowerShell to start the PowerShell host process (Wsmprovhost.exe) on the remote computer."*** **This is the one signature of the three with a first-party source, and the only one we can put on a slide without a caveat about provenance.** | [MS Learn — PowerShell Remoting FAQ](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/powershell-remoting-faq) |
| 5 | `vol -f <dump> windows.getsids --pid <N>` | 🟢 **Current and correct.** Verified against **Volatility 3 v2.28.0**. Plugin `volatility3.plugins.windows.getsids`, class `GetSIDs`, described as ***"Print the SIDs owning each process"***; `--pid` is a documented optional list filter. 🟢🟢 **And the property worth teaching: it is entirely offline.** Name resolution uses a bundled well-known-SID table plus the **`Microsoft\Windows NT\CurrentVersion\ProfileList`** key read from the hives **inside the image** — no live host, no exported hive, no network. ⚠️ **Which also means an unresolved SID is a paging outcome, not a finding** (§2.2). **M6: bind the version when we teach it.** | [volatility3 docs — getsids](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.getsids.html) |
| 6 | the ATT&CK IDs this room's answers require | 🟢 **All current, checked against ATT&CK v19.2** (**L7** — cite the version, not the date): `T1021.002` SMB/Windows Admin Shares (v1.3) · `T1047` Windows Management Instrumentation (v1.6) · `T1021.006` Windows Remote Management (v1.2) · `T1003.001` OS Credential Dumping: LSASS Memory (v1.5) · `T1134.004` Access Token Manipulation: Parent PID Spoofing (v2.0) · `T1036` Masquerading (v2.0). **None deprecated, none revoked.** 🟢 **The room cites no stale IDs — unlike room 29 (Q3) and room 30.** | [attack.mitre.org updates](https://attack.mitre.org/resources/updates/) |
| 7 | *"The first time you run a Volatility plugin, it may take a while to complete due to initial setup and caching. This is expected behaviour."* | 🔴 **Euphemism, and the same one D2 was written for.** What happens on first run is a **symbol download from the Volatility symbol server**. On a connected VM it is slow; **on an air-gapped forensic workstation it does not complete at all**, and the student meets an error, not a wait. 🟢 **Our version says the word "download", names the dependency, and ships the symbol pack with the image** (**D2**). | block **D** · **D2** |
| 8 | *"you can find some pre-cooked results from Volatility plugins in the following directory… `/home/analyst/memory/WIN-015/precooked`"* | 🔴 **The same defect as room 25's tip 3**, and worse here because **running the plugins is the entire skill this room exists to teach.** 🟢 **Pre-computed output is defensible when the wait is the obstacle; it is not defensible when the command is the lesson.** ⚠️ **And it silently masks #7** — a student whose symbol download fails will use `precooked/`, finish the room, and never learn that the dependency exists. **Our version: pre-cooked output is a fallback the student must ask for, and asking is logged as a hint.** | rooms 25, 32 |

### Back-propagation resolved by this pass

Two items left **NOT VERIFIED** in rooms 30 and 31 were closed by the same research pass and have
been patched into those notes (§8):

- 🟢🟢 **Guymager does NOT claim built-in write-blocking — refuted from its own documentation.**
  Room 31 #3 is confirmed as an error. Guymager's homepage: ***"Guymager is a free forensic imager
  for media acquisition"***, features limited to *"Generates flat (dd), EWF (E01) and AFF images,
  supports disk cloning"*; its man page adds *"Guymager should be run with root privileges, as other
  users do not have access to physical devices normally"* — **which is the opposite of a write
  blocker: it documents that the tool needs raw device access.** A full-text search for
  *write block* / *write-block* / *write blocker* / *write protect* returns **zero matches in either
  source.**
- 🟢🟢 **RAMMap is an analysis tool, not an acquisition tool.** Microsoft Learn: ***"RAMMap is an
  advanced physical memory usage analysis utility for Windows Vista and higher"***, used *"to analyze
  application memory usage, or to answer specific questions about how RAM is being allocated."*
  **No claim anywhere that it writes a dump.** Room 30's implication that it is an acquisition tool
  is not supported.

### NOT VERIFIED

- 🔴 **PsExec's default remote service name.** Microsoft documents the rename switch but not the
  default. **Do not put the string `psexesvc.exe` on a slide as "the" name without a source** — the
  finding that survives is #2's *shape* formulation, which needs no default name at all.
- **The full WMI parent→child→grandchild chain against a first-party Microsoft source** (#3). Only a
  community source states it.
- **Every artifact claim in §2 against actual plugin output** — **the lab machine was not started**
  (§4). The room's worked examples are quoted accurately; **whether the dump matches them is
  untested.**
- **The history of cold vs live forensics** (room 31 #2) — still open after this pass; not attempted.
- **`/dev/mem` restrictions** (room 30 #3) — still open; not attempted.

## 4. Evidence used

**Room evidence:** one memory image, `WIN-015-20250522-111717.dmp`, of a Windows workstation, with an
MD5 published and a filename encoding host + date + time. Delivered on a Linux analysis VM with
Volatility 3 and a `precooked/` directory of plugin output.

🔴 **The VM was not started and nothing was run.** The room's brief was read from the task pane with
the lab machine `Off`. **This is a real limitation of this note and it is stated rather than
papered over**: §2's boxes describe the artifacts the room teaches and the claims its questions make,
**not observations from the dump.** The three lineage fragments in §2.1, the `getsids` output shape
in §2.2 and the evidence header in §2.3 are quoted from the room's own text and are reliable as
*what the room says*; **no answer was derived, and none is recorded here.**

⚠️ **The room publishes plaintext SSH credentials for the lab VM** (a username and a password, in the
Machine Access block). **R8: the fact is the finding; the value is not reproduced.** 🔴 **This is now
the pattern, not the exception** — the great majority of hands-on rooms in this path ship a working
credential pair in the brief, and **our labs must not, because our repo is public (D22) and because a
credential in a brief is a credential in a search index.**

**Our equivalent — `EVS-10`, and it is cheap.** The memory image `S6-10` already requires is the same
evidence. **The additions this room justifies are three lines in the manifest, not a new capture:**
a published **SHA-256** (and an MD5 beside it, labelled *lookup only*), a filename in the
`HOST-YYYYMMDDThhmmssZ` form, and **one staged remote-execution lineage** — `wsmprovhost.exe`, since
it is the signature with a first-party source (§3 #4).

## 5. Lab design worth reusing

### 5.1 🟢🟢 Publish the hash with the evidence — and use rooms 31 + 32 as the paired example

**Thirty-one rooms hand a student evidence with no integrity value attached. One publishes a hash.**
That fact alone is worth five minutes of `S1-06`, and it lands harder because of what the hash is.

🟢🟢 **The strongest teaching artifact in the Priority-3 set is the pair, not either room:**

| | room 31 | room 32 |
|---|---|---|
| what it does | **recommends** MD5 and SHA-1 for evidence integrity | **publishes** an MD5 as the evidence's integrity value |
| audience | 13,306 completions, **305 recommends** | 1,976 completions, 53 recommends |
| the lesson | doctrine can be stale | **and the stale doctrine is what gets built** |

**One is the belief; the other is the practice that follows from it, in the same learning path, in
rooms written by the same platform.** 🟢 **That is not a gotcha — it is the clearest available
demonstration that a wrong default propagates**, and it makes the `S1-06` argument without needing
a single slide about collision mathematics.

### 5.2 🟢🟢 Teach a signature as parent → child → *arbitrary* grandchild — then break it in the same breath

**The room's three `pstree` fragments are the best-shaped teaching device in the Priority-3 set.**
They are short, literal, visually parallel, and they leave the payload name variable, which teaches
the student to look at structure instead of strings. **Take the device.**

🟢🟢 **And then do the thing the room does not: break one of them on the next slide.** Microsoft
documents PsExec's `-r` switch; **renaming the service is a supported feature of the tool.** The
exercise writes itself:

1. Show the three signatures. Let the students learn them.
2. Show a fourth tree with an unfamiliar service binary under `services.exe` and ask: *is this
   PsExec?*
3. Show the `-r` documentation.
4. **Rewrite the signature together** — from *"look for `psexesvc.exe`"* to *"look for an unfamiliar
   service binary spawned directly by `services.exe`, correlated with a remote logon."*

🟢🟢 **That fourth step is the whole lesson of the course in miniature: a signature that names a
string is a signature with a shelf life; a signature that names a structure survives the rename.**
It also produces, for free, a genuine **"cannot be determined"** moment (§6).

**Second inversion, same task family:** §2.8's missing `windows.handles` step. The room infers
credential dumping from a tool name; **our version asks for the handle to `lsass.exe`, and then asks
whether even that proves credentials were obtained.** (It does not — **L5**.)

### 5.3 🟢 The hedged stem, and where the hedge belongs

***"…which well-known hacker tool is most likely the malicious process?"*** — **the third correctly
hedged stem in thirty-two rooms**, and the instinct is right. ⚠️ **But it is hedging the wrong
clause.** Identifying a tool from a distinctive argument string is not the uncertain step; **whether
the tool achieved anything is.** 🟢 **Move the hedge:** name the tool without a hedge, then ask
separately — *"what, if anything, does this prove was obtained?"* — where the honest answer is
*nothing*.

### 5.4 🟢 Two defects, both familiar, neither dangerous

- **`precooked/` masks the symbol-download dependency** (§3 #7, #8). Not a safety defect — **an
  evidence-of-learning defect.** A student can complete this room without ever running Volatility.
- **Plaintext lab credentials in the brief** (§4). Not new; **now demonstrably the platform norm**,
  and the reason **D41** and **R8** exist.

🟢 **No safety or handling defect. The running total is unchanged at 11** — and it is worth noting
that **the four Priority-3 rooms produced exactly one defect between them (room 29's), while the
seven Honeynet rooms produced four.** Hands-on rooms carry the risk; concept rooms carry the errors.

## 6. Question patterns

**15 scored questions across 5 tasks** — 1 gate in Task 1, 1 gate in Task 2, **7 in Task 3**,
**5 in Task 4**, 1 gate in Task 5. **Twelve real questions.** The shapes:

| shape | count | example | our verdict |
|---|---|---|---|
| **identify a process from a lineage** | 2 | *"Which executed process provides evidence of this activity?"* | 🟢 **good** — the answer is a structural read, not a lookup |
| **give the ATT&CK ID** | 2 | *"What is the MITRE technique ID associated with the lateral movement method used?"* | 🟢 **good and current** (§3 #6) — 🟢🟢 **and it is asked *after* the mechanism is identified, which is the right order.** Mapping is the conclusion, never the search key |
| **give an identifier from the evidence** | 3 | *"What is the Security Identifier (SID) of the user account…"*, *"the name of the domain-related security group…"*, *"a full path to the process"* | ⚠️ **the path question is excellent** (§2.4); 🔴 **the SID question is D41-borderline** — a SID is a durable identifier of a data subject, and *"copy this string"* is not a forensic skill. 🟢 **Ask what the SID's group membership *means for severity* instead** |
| **give an IP:port** | 1 | *"the Command and Control IP address… Format: IP Address:Port"* | ⚠️ **fine as a lookup, weak as a question** — and its stem asserts *"connected to"* (§2.7) |
| **list processes, alphabetically** | 1 | *"Which processes related to discovery activity were executed by the threat actor…"* | 🔴 **the stem hands over the attribution** (§2.6), and **alphabetical order discards execution order**, which is the informative part |
| **reproduce a command line** | 1 | *"What was the malicious command line executed by the process?"* | 🔴 **M1 uncaveated** (§2.5) — second room in the module to do this |
| **infer the tool** | 1 | *"which well-known hacker tool is most likely…"* | 🟢🟢 **the best question in the room** — hedged, inferential, and it rewards recognising argument shape |
| **evasion technique ID** | 1 | *"Which MITRE ATT&CK technique ID corresponds to the method the attacker employed to evade detection…"* | 🟢 **good** — asks for a technique from observed behaviour rather than from a name |

🔴 **Thirty-second room, no "cannot be determined" question — and this is the last room in the
extraction, so the tally closes at 0 of 32.** ⚠️ **That is the single most consistent finding of the
entire extraction.** Across thirty-two rooms, six modules and two learning paths, **no room ever asks
a student to conclude that the evidence does not support a conclusion** — and in at least six of them
(24, 25, 27, 28, 30, and this one) **the honest answer to a question the room actually asks is
"not determinable from this evidence."**

🟢🟢 **Room 32 supplies three of them for free**, and they need no new evidence:

1. *"Was PsExec used on this host?"* — after the `-r` documentation (§5.2). **Not determinable from
   the service name.**
2. *"Were credentials obtained?"* — §2.8. **A dumping tool ran; success is not recorded anywhere.**
3. *"Did the C2 connection carry data?"* — §2.7. **A socket structure is not a session.**

**This is the design point the whole extraction has been converging on, and it lands on the last
room:** the "cannot be determined" question is not a gimmick or a difficulty knob. **It falls out of
the evidence whenever you ask what an artifact actually proves** — which is what §2's fourth box has
been doing thirty-two times.

## 7. Figures

- **F44 — the three lineage signatures, side by side, with the payload node greyed.** Three columns,
  identical vertical structure, **the middle term boxed in colour and the grandchild greyed with the
  label "arbitrary"**. Our own drawing; the room's are plain text (**D22**).
- **F45 — the same figure with a fourth column: PsExec after `-r`.** Identical structure, middle term
  renamed to something unremarkable, **the boxed colour removed.** 🟢🟢 **F44 and F45 as consecutive
  slides are the whole of §5.2** — build the signature, then break it.
- **F46 — "what the tool proves" ladder for §2.8.** Four rungs, ascending: *a binary is present* →
  *it ran* → *it held a handle to `lsass.exe`* → *credentials were obtained*. **The top rung is drawn
  above the line and greyed, with "no artifact records this — L5" beside it.** Reusable for any
  outcome-versus-capability question in the course.

**Figure numbering: F44–F46. Next free is F47.**

## 8. Fit against our material

### 🔴 The Priority-3 label is wrong for this room, and the reason is worth recording

Rooms 29, 30 and 31 earned their skim: two are concept walkthroughs, one is a survey. **Room 32 is a
Medium-difficulty hands-on lab with real evidence, three transplantable signatures, a plugin our
corpus had never named, and the corpus's only published acquisition hash.** It was filed Priority 3
because of **where it sits in the path outline — last, under a "supplemental" title — not because of
what is in it.**

🟢 **The lesson for our own course: "supplemental" in a syllabus is a position, not a judgement.**
We have a `S6-09`/`S6-10` ordering problem of exactly this shape, and it is worth checking that
nothing valuable is sitting at the end of our own list under a modest heading.

### 🔴🔴 The module's attrition, and what it actually measures

The **Memory Analysis** module's completion counts, in module order:

| # | room | completions |
|---|---|---|
| 1 | Memory Analysis Introduction | **13,179** (free) |
| 4 | Windows Memory & Processes | 3,015 |
| 5 | Windows Memory & User Activity | 2,511 |
| 6 | Windows Memory & Network | 2,382 |
| 8 | **Supplemental Memory** | **1,976** |

**85% of the people who start this module never reach its capstone.** ⚠️ **But the cliff is in the
wrong place for the obvious reading.** The drop is **13,179 → 3,015 — 77% — between room 1 and
room 4**, and **that is exactly the free-to-premium boundary**, not a difficulty boundary. After the
paywall the curve is gentle: 3,015 → 2,511 → 2,382 → 1,976, **each step losing 5–17%.**

🟢🟢 **This corrects the reading I took from the Honeynet curve.** There, attrition was difficulty.
**Here, one commercial boundary accounts for more loss than four rooms of increasing difficulty
combined** — and **our students are past that boundary on day one.** ⚠️ **So the Honeynet
attrition numbers are a usable difficulty signal and these are not**, and **D40's carry-through
design should be calibrated on the Honeynet curve alone.** The honest per-room difficulty signal in
this module is the post-paywall slope, and **it is shallow: the module does not shed people as it
gets harder.**

### Rows this strengthens

- **`S6-10`** — 🟢🟢 **the largest gain.** `windows.getsids` as a named plugin with its offline
  property stated; the `pslist`/`psscan` diff as a required step, not an option; **and F44/F45 as the
  session's centrepiece.** The three signatures give `S6-10` the thing it lacked: **a reusable
  pattern the student leaves with**, rather than a sequence of plugin invocations.
- **`S6-09`** (capstone shape) — the lineage-then-break exercise (§5.2) and the three
  "cannot be determined" questions (§6). 🟢🟢 **This is where the tally finally gets closed.**
- **`S1-06`** — 🟢🟢 **the rooms 31 + 32 pair** (§5.1). **Better than the room-31 example alone**,
  which was already the best available.
- **`S1-07`** — the filename convention, and the timezone gap: `HOST-YYYYMMDDThhmmssZ`.
- **`S2-03`** — the evidence header as a manifest template.
- **`S1`** — §2.2's uncollected sentence: **an artifact bearing a stolen account's SID is evidence of
  a credential, not of a person.** The room's own scenario supplies it and the room never says it.

### Back-propagation

🟢 **Two corrections pushed back, both from this pass's research, both closing NOT VERIFIED items:**

- **`intro-to-cold-system-forensics.md` §3 #3** — the Guymager write-blocking claim is now
  **refuted from Guymager's own documentation**, not merely doubted. Patched: verdict upgraded from
  *NOT VERIFIED* to refuted, with the homepage and man-page quotations and the zero-match search
  result. **Done in this pass.**
- **`memory-analysis-introduction.md` §3 #3** — **RAMMap is confirmed an analysis utility, not an
  acquisition tool**, from Microsoft Learn. Patched with the quotation. **Done in this pass.**

🟢 **No ATT&CK corrections needed** — this room's IDs are all current at v19.2 (§3 #6), which makes
it **the only room in the last four with no stale technique ID.**

⚠️ **One correction to my own earlier reasoning, recorded rather than deleted** (the room-28
precedent): in the Honeynet module note I read a completion curve as a pure difficulty signal. **This
module shows a commercial boundary producing a larger drop than four difficulty steps.** The Honeynet
reading survives — those six rooms sit entirely inside the paywall, so no boundary confounds them —
**but the method needed the caveat and did not have it.** Added above.

### Minutes

**Net zero, and this is the last room, so the number is final.**

Everything lands in `S6-09` and `S6-10`, which are the two rows that were already going to carry the
memory capstone. **F44/F45 replace planned content rather than adding to it** — they are a better
version of the "identify the malicious process" walkthrough `S6-10` already budgeted.

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-seventh and final room to carry the S5 overdraft. Thirty-two rooms have now been
extracted and not one of them changed it. It is a structural problem in our own split and no further
research will move it** — **the re-split is the next piece of work and it is not blocked on
anything.**

### Decisions logged from this room

- **D42** — currency-block items are cited as **"block R5"**, never bare; bare **R1–R8** always means
  a hard rule. 🔴 **Block R is the first block letter that collides with the rule numbers**, and R8
  is the credential rule — the most-cited rule in the project. Caught while writing, fixed in place.
- **D43** — 🔴🔴 **a completion curve is a difficulty signal only within one access tier.** The
  correction to my own Honeynet method (§8 above), and the reason D40's calibration stands on the
  Honeynet numbers alone.
- **D44** — 🟢🟢 **signatures are taught as structures, never strings, and one taught signature is
  broken on the following slide.** PsExec + `-r` is the worked instance; **F44/F45** are the slides.

### Out of scope

Linux memory analysis (**D38**, and it is the room immediately preceding this one in the module).
The full PsExec/WMI/WinRM protocol internals — **we teach the host-side artifact, not the wire.**

### Still unresolved

Unchanged, plus one addition: 🆕 **PsExec's default remote service name is undocumented by
Microsoft** (§3 #2). **This does not block anything** — the *shape* formulation in §5.2 is stronger
than the string and needs no default name — **but if a slide is ever going to print `psexesvc.exe`,
it needs a source first.**

## 9. Links

**Room** — <https://tryhackme.com/room/supplementalmemory>
**Module** — <https://tryhackme.com/module/memory-analysis> — 🟢 **eight rooms, named and ordered in
§ frontmatter.** This room is the capstone.
**Companion notes** — `memory-analysis-introduction.md` (room 30, the same module's opening room —
🟢 **read the two together: the pair is the module's own attrition story**) ·
`windows-memory-and-processes.md`, `windows-memory-and-user-activity.md`,
`windows-memory-and-network.md` (the module's operational core) · `volatility-essentials.md` ·
`lostinramslation.md` (**M1**–**M4**, and the other uncaveated command-line question) ·
`intro-to-cold-system-forensics.md` (room 31 — **the MD5 pair, §5.1**) ·
`shockandsilence.md` §2.8 (the plausible-story failure mode) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **D**, **K7**, **L1**, **L5**, **L7**, **M1**, **M4**, **M6**,
**M7**, **O4**, **O5**, and new block **R**.

**Citations from §3:**

- #1 — CERT/CC VU#836068 <https://www.kb.cert.org/vuls/id/836068> · block **K7**
- #2 — Microsoft Learn, PsExec <https://learn.microsoft.com/en-us/sysinternals/downloads/psexec>
  (⚠️ default service name **NOT VERIFIED** — absent from the page)
- #3 — <https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/troubleshoot-wmi-high-cpu-issues>
  (partial, first-party) · <https://threathunterplaybook.com/hunts/windows/190810-RemoteWMIExecution/notebook.html>
  (⚠️ community source, full chain)
- #4 — <https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/powershell-remoting-faq>
- #5 — <https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.getsids.html> ·
  v2.28.0 per <https://pypi.org/project/volatility3/>
- #6 — ATT&CK v19.2 <https://attack.mitre.org/resources/updates/> ·
  T1021.002 <https://attack.mitre.org/techniques/T1021/002/> ·
  T1047 <https://attack.mitre.org/techniques/T1047/> ·
  T1021.006 <https://attack.mitre.org/techniques/T1021/006/> ·
  T1003.001 <https://attack.mitre.org/techniques/T1003/001/> ·
  T1134.004 <https://attack.mitre.org/techniques/T1134/004/> ·
  T1036 <https://attack.mitre.org/techniques/T1036/>
- **Back-propagation sources** — Guymager <https://guymager.sourceforge.io/> and
  <https://manpages.debian.org/testing/guymager/guymager.1.en.html> ·
  RAMMap <https://learn.microsoft.com/en-us/sysinternals/downloads/rammap>
