---
room: Elevating Movement
url: https://tryhackme.com/room/elevatingmovement
module: **Honeynet Collapse — stage 2 of 6.** *"Investigate the second, Windows part of the Honeynet
        Collapse!"* Challenge room (Priority 2). Target `SRV-IT-QA` (172.16.8.216, DMZ).
feeds: 🟢🟢 **First fully in-scope room of the chain.** `S5-05`/`S5-06` (evidence of execution),
       `S6-06` (event logs), `S5-01`, and the S6-09 capstone.
       🔴🔴 **Carries a question-design defect we must never copy: the answer to a graded question
       is a usable credential** (§6). And two hard corrections — **Amcache's SHA-1 covers only the
       first ~30 MB of a file**, and **no T1574 sub-technique fits an overwritten scheduled-task
       binary** (§3 #2, #6).
difficulty / time: **Hard** · 60 min · 2 tasks · 7 questions (6 scored + 1 "Let's go!") · Premium ·
                   2,643 completions · 50 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, diagram, lab setup, tips and all question stems,
              including the two answer-format examples. 0 sections NOT READ.
              🔴 **Room ships plaintext RDP credentials in the task body — not reproduced (R8).**
              Fourth Priority-2 room to do so.
              🔴🔴 **Q6's expected answer is an NTLM hash — i.e. the room's answer key contains a
              credential.** Not reproduced, and not obtainable here in any case (§6).
              ⚠️ **Answers NOT READ** — lab machine not started. §2 is reconstructed from the 6
              scored questions and 3 tips, as for rooms 18–23.
              🟢 **The module diagram is byte-identical to room 23's** — same asset ID
              `678ecc92c80aa206339f0f23-1750969983020.svg`. That is the state-carrying mechanism
              confirmed empirically, not inferred (§5.1).
---

## 1. What the room teaches

**That the attacker's second host is chosen for them by how the organisation actually works** — and
that almost every artifact this room depends on is **off by default**.

The pivot is a Slack-shaped message, and it is the most realistic sentence in the module:

> *"Hey Emily, when you are done with DeceptiPot deployment, can you take a look at SRV-IT-QA? It
> became unstable after we replaced the motherboard, so maybe you can debug what's going on there.
> ~ Matthew"*

🟢🟢 **Four things are doing work in that one message, and all four are ordinary IT practice:**

1. **Emily is sent to a second machine** — so the credentials stolen at stage 1 arrive somewhere new
   without the attacker doing anything.
2. **She works "from a local admin account"** — the standard workaround for a flaky box, and the
   reason a privilege boundary is already blurred before the attacker touches it.
3. **The box is *expected* to misbehave** — *"unstable after we replaced the motherboard"* is
   **pre-authorised cover for every anomaly the attacker generates.** 🔴 A crash, a service restart,
   a scheduled task failing — all of it reads as the known hardware fault. **That is the sharpest
   detective-control failure in the module and it costs the attacker nothing.**
4. **Tip 2 — *"Other IT administrators often log in to this machine"*** — makes the host a
   credential reservoir. It is a QA server; it is also, in effect, a jump box nobody designated.

**The room then asks six questions that trace: RDP in → replace a scheduled task's binary → dump
credentials → move laterally with a domain account.** That is a complete, correct, teachable chain.

**🔴🔴 But the artifacts it relies on are mostly not there by default, and the room never says so.**
This is the same defect as room 23's auditd tip, one platform over:

- **Q4 asks for a full command line.** Microsoft's own documentation: *Audit Process Creation* is
  **"Default: Not configured"**, and *Include command line in process creation events* is
  **"Default setting: Not Configured (not enabled)"** — *"If you disable or don't configure this
  policy setting, the process's command line information won't be included in Audit Process
  Creation events."* **So on a stock host there is no 4688 at all, and where 4688 exists the command
  line is absent.** §3 #1.
- **Task Scheduler Operational is off by default** (**G6**), so the task-registration record may not
  exist either.
- **Sysmon is not installed by default**, so LSASS handle access (event 10) is not recorded.
- ⚠️ **Q1's RDP evidence is the exception** — `TerminalServices-LocalSessionManager/Operational`
  **is** on by default (**G6**), which is precisely why RDP is the most reliable question in the room.

**🔴🔴 And it commits a defect we must never copy: Q6's answer is a credential.** *"What is the NTLM
hash of matthew.collins' domain password?"* An NT hash **is** an authenticator — it is what
pass-the-hash passes. The room therefore has a public answer key containing a usable domain
credential for its own fictional environment, and it trains students that submitting one is normal.
**§4 and §6.** Under **R8** this note reproduces neither it nor the room's RDP password.

🟢 **What it gets right, and it is not small:** the chain is honest about *why* stage 2 exists.
Stage 1 gave the attacker a foothold and Emily's domain credentials; stage 2 is where those
credentials are **spent** and upgraded. **The room never says "the attacker pivoted" — it shows the
business reason a human being carried the credentials to the next box.**

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 6 scored questions plus 3 tips (see frontmatter). Mapping: Q1 → 2.1 ·
Q2 → 2.2 and 2.3 · Q3 → 2.4 · Q4 → 2.5 and 2.6 · Q6 → 2.7 · Q5 → 2.8.

### 2.1 RDP logon on the server — the one artifact that is on by default

- **What it is** — the record that a remote interactive session began. Q1: *"When did the attacker
  perform RDP login on the server?"*, answer format `2025-01-15 19:30:45`.
- **Where it lives** — three channels, and the join key is the **session ID**:
  **`Microsoft-Windows-TerminalServices-LocalSessionManager/Operational`** — **21** logon ·
  **22** shell start · **23** logoff · **24** disconnect · **25** reconnect. 🟢 **On by default.**
  **`…TerminalServices-RemoteConnectionManager/Operational`** — **1149**.
  **Security** — **4624 LogonType 10** (RemoteInteractive), **4625** for failures, 4778/4779
  reconnect/disconnect.
- **What it proves** — that a session was established for a named account from a source address at a
  time. 🟢🟢 **Event 22 (shell start) is the strong one — it proves an interactive desktop actually
  loaded**, not merely that authentication succeeded.
- **What it does NOT prove** — 🔴🔴 **that 1149 is a successful logon.** It fires *before*
  authentication completes — a client reached the login prompt. **1149 with no matching 21 is
  scanning or failed credentials, not access.** The correct chain is **1149 → 4624 type 10 → 21 →
  22**, and reporting a 1149 timestamp as "the attacker logged in" is the classic error.
  🔴 **Over-counting is the second classic error:** filter out `Source Network Address = LOCAL` or
  console sessions inflate the count (**G6**).
  🔴 **And none of it proves *who* was at the keyboard** — it proves a credential was used. Given
  that stage 1 stole Emily's credentials, **a logon as Emily is the expected appearance of the
  attacker**, which is the whole point of the stage.
  ⚠️ **Nor does the source address prove origin** — an RDP session relayed through stage 1's host
  shows that host's address, which is exactly what the module's diagram predicts.
- **How to parse it** — `EvtxECmd` to CSV, then Timeline Explorer; join LocalSessionManager 21/22/23
  to Security 4624/4634 on session ID; ⚠️ **normalise to UTC before joining** — the two channels are
  both UTC on disk but Event Viewer renders local.
- **Anti-forensics / false-positive caveat** — ⚠️ **the channels are small and roll fast.** 🔴 And
  clearing them is now **T1685.005 "Clear Windows Event Logs", not T1070.001** (§3 #6, block K).
  🟢 **A cleared log is itself an event** — Security **1102** and System **104** — and their absence
  alongside a suspiciously short log is a finding.

### 2.2 The scheduled task, and the binary it runs

- **What it is** — Emily's *"periodic system checker automation"* (tip 1), whose target executable
  the attacker overwrote. Q2: *"What is the full path to the binary that was replaced for
  persistence and privesc?"*
- **Where it lives** — the task definition in **`C:\Windows\System32\Tasks\<name>`** (XML, and the
  `<Command>` element is the answer to Q2), mirrored in the registry at
  **`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree|Tasks`**. Execution
  and registration records in **`Microsoft-Windows-TaskScheduler/Operational`** (106 registered ·
  200/201 action started/completed · 129 process created) and **Security 4698** (carries the full
  task XML).
- **What it proves** — that a task was configured to run a named executable, as a named principal,
  on a trigger. 🟢🟢 **The privesc is in the principal, not the binary** — a task registered to run
  as SYSTEM or a domain admin turns a file write into an elevation.
- **What it does NOT prove** — 🔴🔴 **that the binary at that path today is the binary the task ran
  yesterday.** The task definition points at a **path**; the attacker changed the **file**. **The
  task XML is therefore evidence of the mechanism and not of the payload**, and §2.3 is where the
  substitution is actually shown.
  🔴 **Task Scheduler Operational is OFF by default** (**G6**), so the registration and execution
  records may simply not exist — **on an unmanaged endpoint the primary task evidence is the registry
  TaskCache plus the XML file.** ⚠️ Security **4698** is governed by *Audit Other Object Access
  Events*, whose OS default is **NOT VERIFIED** (**G6**) — check `auditpol /get /subcategory:"Other
  Object Access Events"` before relying on it.
  🔴 **And the task may be invisible to enumeration.** Deleting the **`SD`** value under
  `TaskCache\Tree\<task>` makes it vanish from `schtasks /query`, Autoruns and the GUI **while it
  keeps running** (**G5**, Tarrask). **The enumerating tools fail open.**
- **How to parse it** — read the XML directly; `RECmd` over `SOFTWARE` for `TaskCache`; `EvtxECmd`
  for the channel. 🟢 **The Tarrask cross-check is the method, not a scan:** diff `TaskCache\Tree`
  subkeys against the XML files in `System32\Tasks`; a Tree entry with no XML, or a missing `SD`, is
  the IOC — and `Tree` also stores **a hash of the XML**, giving a second integrity check.
- **Anti-forensics / false-positive caveat** — 🟢 **the legitimate task is the camouflage.** Emily
  created a real automation for a real reason; the attacker did not add a task, they **repointed an
  existing one's payload**. **A "new task" hunt finds nothing here** — which is precisely why the
  detection has to be *file* integrity (§2.3), not *task* enumeration.

### 2.3 Amcache — proving the binary was replaced, and the two limits nobody teaches

- **What it is** — a registry hive recording files present on the volume, **including a SHA-1**. The
  artifact that makes Q2/Q3 answerable at all.
- **Where it lives** — `C:\Windows\AppCompat\Programs\Amcache.hve`, key
  **`Root\InventoryApplicationFile`**, hash in the **`FileId`** field. Alongside:
  `LowerCaseLongPath`, `Name`, `OriginalFileName`, `Publisher`, `Version`, `BinaryType`,
  `ProductName`, `LinkDate`, `Size`, `IsOsComponent`, `ProgramId`.
- **What it proves** — 🟢🟢 **that a file with this path, size and hash existed on this volume at a
  known time — and it survives the file's deletion**, so it proves prior presence of things no
  longer on disk. **For "was the binary replaced?", two Amcache entries for one path with two
  different `FileId` values is the finding.**
- **What it does NOT prove** — 🔴🔴🔴 **three limits, and two of them are new to this project:**
  1. 🔴🔴 **Amcache does NOT prove execution.** Cyber Triage: entries *"should generally not be used
     to prove program execution. Safer to interpret data as evidence of existence."* Securelist rates
     `InventoryApplicationFile` as presence only — *"with no data on whether or when they ran."*
     **This is `S5-06`'s existing "presence vs execution" lesson, independently confirmed**, and it
     means **Q3's "the replaced binary" needs Prefetch or the task's own 200/201 records to be tied
     to an actual run.**
  2. 🔴🔴 **`FileId` is SHA-1 with four zeroes prepended** — *"the SHA-1 hash with 'four zeroes
     appended to the beginning of the hash'"*. **Strip `0000` before any lookup.** A student who
     pastes the raw value into VirusTotal gets nothing and concludes the file is unknown.
  3. 🔴🔴 **The hash covers only the first 31,457,280 bytes (~30 MB), not the whole file.**
     **So for any binary over 30 MB the Amcache hash will never match VirusTotal or NSRL** — and,
     worse for us, **two different files that share their first 30 MB share a `FileId`.** ⚠️ **This
     is the most consequential single fact in the note**: it means Amcache's hash is an
     *identification aid*, not an integrity value — the same distinction as MD5 in block **K7**,
     arriving from a different direction.
  ⚠️ Carvey's standing warning applies: analysts *"should not consider artifacts in isolation … but
  should instead look to multiple data sources and artifacts, viewed together."*
- **How to parse it** — `AmcacheParser` to CSV, then Timeline Explorer. Corroborate the replacement
  with **`$MFT`** (a new `$STANDARD_INFORMATION` vs `$FILE_NAME` divergence at that path),
  **`$UsnJrnl`** (`DataOverwrite`/`FileCreate` reason flags on that file), **Prefetch** for execution,
  and the **Authenticode signature state** — a system-looking binary that is unsigned, or signed by
  the wrong publisher, is the fastest tell.
- **Anti-forensics / false-positive caveat** — ⚠️ **legitimate updates also change a binary's hash at
  a stable path.** The finding is a hash change **with no corresponding patch, installer or update
  record** — so the Amcache entry must be read beside `Setup`/`WindowsUpdateClient` events and the
  publisher field, never alone. 🟢 **`Publisher` and `IsOsComponent` are the cheap discriminators**
  and they are already in the same row.

### 2.4 Malware family attribution — a different kind of claim

- **What it is** — Q3: *"What is the type or malware family of the replaced binary?"*
- **Where it lives** — not on the disk at all. It comes from **external reputation** — a VirusTotal
  or Google Threat Intelligence lookup of the hash from §2.3 — or from static/dynamic triage.
- **What it proves** — that vendors who have seen this sample **assign it a family label**.
- **What it does NOT prove** — 🔴🔴 **that the label is a fact about the file.** Family names are
  **vendor opinions and they disagree** — the same sample is routinely `Mimikatz`, `HackTool`,
  `Riskware` and `Generic.Trojan` across engines, and "family" for a commodity tool often names the
  *tool*, not an actor. ⚠️ **A detection count is not a severity score**, and a low count on a
  freshly compiled binary means *unknown*, not *clean*.
  🔴🔴 **And this is the block where the reporting rule bites hardest (D20 criterion 4).** *"The
  binary at `C:\…\checker.exe` has SHA-1 X"* is a **finding**. *"It is Mimikatz"* is an
  **interpretation** resting on a third party's classifier. **They must appear in different
  sections of the report, and the vendor and lookup date must be named** — because the answer changes
  as engines update.
  ⚠️ **Handling:** submitting a client's binary to a public multi-scanner **discloses it**. On a real
  engagement that is a decision, not a step — hash lookup first, sample submission only with consent.
  **The room models the opposite by asking for the family with no caveat.**
- **How to parse it** — hash lookup first (strip the `0000`, and check the file is under 30 MB before
  trusting an Amcache-derived hash — §2.3); `strings`, imports and the Authenticode state for local
  triage; **record the engine, verdict and date**.
- **Anti-forensics / false-positive caveat** — 🟢 **the useful inversion:** if a binary sitting at a
  system-looking path is **unknown to every engine**, that is more interesting than a confident
  family label, not less — bespoke tooling is the expensive kind. **Absence of reputation is a
  finding, and the room's question shape cannot express it.**

### 2.5 Command-line evidence — and why it is usually absent

- **What it is** — Q4: *"Which full command line was used to dump the OS credentials?"*
- **Where it lives** — 🔴 **on a default host, nowhere.** The candidates, ranked by whether they
  exist without configuration:
  | source | carries the command line? | on by default? |
  |---|---|---|
  | **Security 4688** | only with the extra policy | 🔴 **No — neither part** |
  | **Sysmon event 1** | 🟢 yes, fully | 🔴 not installed by default |
  | **PowerShell script block (4104)** | 🟢 yes, if PowerShell was the vehicle | 🟢 **partially — three states (G1)** |
  | **PSReadLine `ConsoleHost_history.txt`** | 🟢 yes, as typed | 🟢 yes, but lossy (**G3**) |
  | **Task Scheduler 200/201** | the executable and return code, not full args | 🔴 no (**G6**) |
  | **Prefetch** | 🔴 **no — it records the executable and referenced files, not arguments** | 🟢 yes |
  | **Amcache / ShimCache** | 🔴 no | 🟢 yes |
- **What it proves** — with 4688 + the policy, or Sysmon 1: the exact invocation, its parent process
  and the user context. **That is the strongest single line of evidence in a Windows intrusion.**
- **What it does NOT prove** — 🔴🔴🔴 **that it happened, if it is absent.** Microsoft's own words:
  *Audit Process Creation* — **"Default: Not configured"**; *Include command line in process creation
  events* — **"Default setting: Not Configured (not enabled)"**, and *"If you disable or don't
  configure this policy setting, the process's command line information won't be included in Audit
  Process Creation events."* **Two independent switches, both off.** So the honest answer to *"what
  command line did they use?"* on an unmanaged host is usually **"not recoverable"**, and the room
  can ask it only because its lab enabled something it never names.
  🔴 **Prefetch is the trap.** It is on by default and students reach for it — **but a `.pf` records
  the executable and the files it touched, not the arguments.** *"`rundll32.exe` ran"* and *"the
  command line was `rundll32.exe comsvcs.dll, MiniDump …`"* are different claims, and only the second
  answers Q4.
  ⚠️ **PSReadLine is the sleeper** (**G3**): if the attacker typed into PowerShell,
  `ConsoleHost_history.txt` has the line **even with no logging configured at all** — but it is
  per-host, incremental and lossy by design, so **absence there proves nothing.**
- **How to parse it** — `EvtxECmd` for 4688/4104; `PECmd` for Prefetch (**to show execution, not
  arguments**); read `ConsoleHost_history.txt` directly.
- **Anti-forensics / false-positive caveat** — 🟢 **teach the negative as the deliverable.** The
  professional output here is *"the command line is not recoverable on this host because process
  creation auditing was not enabled; execution of `rundll32.exe` at 14:22 is established by
  Prefetch"* — **a finding plus a stated limitation, which is exactly D20 criterion 4.** ⚠️ **The
  room's question shape cannot accept that answer**, and that is the gap our version closes.

### 2.6 LSASS and SAM access — what records the act of dumping

- **What it is** — the credential-theft step itself. Techniques: `procdump -ma lsass.exe`,
  **`rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <pid> <out> full`** (a LOLBin — signed,
  Microsoft, present on every host), `reg save HKLM\SAM` + `HKLM\SYSTEM`, and `ntdsutil`/VSS for
  `ntds.dit` on a DC.
- **Where it lives** — 🔴 **there is essentially no default-on Windows artifact that records LSASS
  being read.** What exists: **Sysmon event 10 (ProcessAccess)** with a `GrantedAccess` mask —
  **not installed by default**; **Defender ASR** *"Block credential stealing from the Windows local
  security authority subsystem"* — ⚠️ **ASR rules are not enabled by default** and must be configured;
  **Security 4656/4663** on LSASS only with a SACL nobody sets. **Secondary traces:** the **dump file
  on disk** (`$MFT`, `$UsnJrnl`, and its size), Prefetch for `procdump.exe`/`rundll32.exe`, and
  §2.5's command line if it survived.
- **What it proves** — that a process obtained a handle to LSASS with dump-capable rights, or that a
  dump artefact exists on disk.
- **What it does NOT prove** — 🔴🔴 **absence proves nothing at all here, and this is the strongest
  case of it in the corpus.** With no Sysmon, no ASR and no SACL, a full LSASS dump on a default
  Windows host leaves **no direct record of the read** — only whatever the attacker forgot to delete.
  🟢 **Which flips the method:** you do not hunt the dump, you hunt **its consequences** — a new
  logon by an account that has no business on this host (§2.8), a `.dmp` in a temp path, or an
  unexpected `rundll32.exe` in Prefetch.
  🔴 **`reg save HKLM\SAM` leaves the output file and Prefetch for `reg.exe`** — but **`reg.exe` runs
  legitimately all the time**, so the finding is the *output file*, not the tool.
  ⚠️ **And a SAM dump is not a domain compromise.** SAM holds **local** account hashes; Q6 asks for a
  **domain** user's hash, which comes from LSASS (a cached logon of that user — tip 2's *"other IT
  administrators often log in to this machine"*), not from SAM. **Conflating the two stores is the
  most common student error in this scenario.**
- **How to parse it** — `PECmd` for Prefetch; `MFTECmd` for a `.dmp` and its timestamps; `EvtxECmd`
  over Defender and Sysmon channels if present. 🟢 **Check Defender's `DetectionHistory` store
  independently of the event log** (**G8**) — it carries SHA-256, the spawning process and the user,
  and a detection in one store and not the other is selective tampering.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the LOLBin is the point.** `rundll32.exe` and
  `comsvcs.dll` are signed Microsoft binaries present on every Windows host — **there is no file to
  find, no hash to look up, and nothing to flag as malicious.** The only thing that is anomalous is
  the *combination*, which lives in the command line — **the artifact §2.5 just showed is usually
  missing.** That closed loop is the honest state of Windows endpoint forensics without EDR, and it
  is worth saying to students plainly.

### 2.7 The NT hash — what it is, and what possessing it proves in 2026

- **What it is** — Q6: *"What is the NTLM hash of matthew.collins' domain password?"* 🔴 **Not
  reproduced (R8), and the question itself is the defect — §6.**
- **Where it lives** — for **local** accounts, the **SAM** hive; for **domain** accounts,
  **`NTDS.dit`** on a DC (attribute `unicodePwd`) and, on a member server, **in LSASS for any account
  with a cached session**. Microsoft: *"Passwords at rest are stored in several attributes of the
  Active Directory database (NTDS.DIT file)"* and *"On domain members and workstations, local user
  account password hashes are stored in a local Security Account Manager (SAM) Database located in
  the registry."*
- **What it proves** — that the account's password hashes to this value. The construction is
  unchanged and is worth showing once: **`NTOWFv1(Passwd, User, UserDom) = MD4(UNICODE(Passwd))`** —
  **MD4 of the UTF-16LE password, unsalted, no iteration.** 🟢 **Unsalted and uniterated is the whole
  lesson**: identical passwords produce identical hashes across every account and every machine in
  the forest, which is what makes both cracking and reuse cheap.
- **What it does NOT prove** — 🔴🔴 **it is not "just a hash" — it is an authenticator.** In NTLM,
  possession of the NT hash is sufficient to authenticate; the plaintext is never needed. **That is
  why pass-the-hash exists and why an NT hash must be handled as a credential, not as a finding**
  (§6). ⚠️ It also does **not** prove the attacker cracked or knows the password.
  🔴 **Currency, and it is more nuanced than "NTLM is dead":**
  - **All NTLM versions are deprecated** — Microsoft: *"All versions of NTLM, including LANMAN,
    NTLMv1, and NTLMv2, are no longer under active feature development and are deprecated."*
  - **NTLMv1 is *removed*, not merely deprecated** — *"NTLMv1 is removed starting in Windows 11,
    version 24H2 and Windows Server 2025."* ⚠️ But *"remnants of NTLMv1 cryptography are still
    present in some scenarios, such as when using MS-CHAPv2 in a domain-joined environment."*
  - **NTLMv2 still works and is still enabled by default.** Microsoft announced a phased plan
    (Feb 2026) to disable NTLM by default in a **future** release — **not today.**
  - **So the NT hash is still stored, still dumpable and still usable.** *"NTLM is going away"* is
    true as a direction and false as a present-tense fact, and a course that teaches either extreme
    is wrong.
- **How to parse it** — out of scope as an exercise. **What we teach is the handling rule**, §6.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **Credential Guard is the modern mitigation and
  it is far narrower than it is usually taught.** Microsoft: *"Starting in Windows 11, 22H2 and
  Windows Server 2025, Credential Guard is enabled by default on domain-joined, non-DC systems that
  meet hardware requirements"* — and the edition table is **Enterprise yes, Education yes, Pro NO,
  Pro Education/SE NO.** **Five gates: 22H2+, domain-joined, non-DC, Enterprise/Education, VBS-capable
  hardware.**
  🔴🔴 **And even when on, *"Credential Guard doesn't provide protections for the Active Directory
  database or the Security Accounts Manager (SAM)."*** So **local** hashes remain dumpable. Combined
  with NTLMv2 still being enabled by default, **pass-the-hash is current practice, not history** —
  and telling students otherwise would be a factual error.

### 2.8 Lateral movement — spending the stolen credential

- **What it is** — Q5: *"Using the stolen credentials, when did the attacker perform lateral
  movement?"*, answer format `2025-01-15 19:30:45`. On the diagram this is **② → ③**, `SRV-IT-QA` →
  `SRV-DMZ-GW`.
- **Where it lives** — **on the source host**: Security **4648** (*explicit credentials* — the
  highest-value single event for this question, because it fires when a process authenticates as
  someone other than the logged-on user), Prefetch for `mstsc.exe`/`psexec`/`wmic`,
  **`HKCU\Software\Microsoft\Terminal Server Client\Servers`** (destinations typed into mstsc), the
  RDP **bitmap cache** `%LOCALAPPDATA%\Microsoft\Terminal Server Client\Cache\*.bmc`, and
  `Default.rdp`. **On the destination**: the §2.1 channels, with **4624 LogonType 3** (network) or
  **10** (RDP).
- **What it proves** — that a credential was used from this host toward another host at a time.
  🟢🟢 **4648 is the pivot event and deserves its own slide** — it names the *source* account, the
  *target* account and the *target server* in one record, which is precisely the "stolen credential
  spent" moment.
- **What it does NOT prove** — 🔴🔴 **that the movement succeeded.** Source-side artifacts prove an
  *attempt*: 4648 fires whether or not authentication succeeds, and a `Terminal Server Client\Servers`
  entry records that a destination was **typed**, not that it was reached. **Success requires the
  destination's own logs** — which, on this module's map, is the next room.
  ⚠️ **`Terminal Server Client\Servers` is per-user and MRU-shaped** — it records destinations, not
  times, and a busy admin's key is full of legitimate entries.
  🔴 **The bitmap cache is the one that over-promises.** It can yield fragments of what was displayed
  in the remote session — striking in a report — but it is **tile-fragmented, unordered and
  undated**, so it supports "this content appeared on screen at some point", not a timeline.
  ⚠️ **And "lateral movement" is an interpretation.** The finding is *"a network logon to
  172.16.8.15 using domain credentials at T"*; **that it was hostile follows from context, not from
  the record.**
- **How to parse it** — `EvtxECmd` for 4648/4624; `RECmd` over `NTUSER.DAT` for the Terminal Server
  Client keys; `PECmd` for the client binaries. 🟢 **The join that answers Q5 honestly is 4648 on
  the source paired with 4624 on the destination**, and stating that you only have one half is a
  legitimate finding.
- **Anti-forensics / false-positive caveat** — ⚠️ **this is a QA server that IT administrators use
  by design** (tip 2). **Admin-to-server RDP is the baseline here, not the anomaly** — so the
  discriminator is not *that* a lateral connection happened but **which account, from which session,
  at what hour, to a destination that account never touches.** 🟢 **Teach the query as a deviation
  from a baseline**, which is the same shape as room 23's *"find sudo by a service account"*.

## 3. Tools and commands

The room names no commands. Tip 3 says only *"You might need to use EZ tools for this scenario."*
The table is what the questions require.

| purpose | tool / command | note |
|---|---|---|
| RDP logon time (Q1) | `EvtxECmd` → Timeline Explorer; LocalSessionManager 21/22 + Security 4624 t10 | 🟢 on by default — #4 |
| task definition (Q2) | read `C:\Windows\System32\Tasks\<name>`; `RECmd` over `SOFTWARE` for `TaskCache` | 🔴 channel off by default (**G6**) |
| binary replacement (Q2) | `AmcacheParser` — two `FileId` values at one path | 🔴 strip `0000`; ~30 MB limit — #2 |
| execution (Q2/Q3) | `PECmd` (Prefetch) | 🔴 **no command line** — #1 |
| malware family (Q3) | hash lookup (VT/GTI) | ⚠️ vendor opinion, not a fact — §2.4 |
| command line (Q4) | `EvtxECmd` for 4688/4104; `ConsoleHost_history.txt` | 🔴🔴 **both audit switches off by default** — #1 |
| file substitution corroboration | `MFTECmd` (`$MFT`, `$UsnJrnl`) | `DataOverwrite` reason flag |
| lateral movement (Q5) | `EvtxECmd` 4648/4624; `RECmd` over `NTUSER.DAT` | 🟢 4648 is the pivot event — §2.8 |
| the NTLM hash (Q6) | — | 🔴🔴 **we do not set this question** — §6 |

### CURRENCY CHECK

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"Which full command line was used to dump the OS credentials?"* — assumes a command line is recoverable | 🔴🔴🔴 **Two independent switches, both off by default.** Microsoft: *Audit Process Creation* — **"Default: Not configured"**. *Include command line in process creation events* — **"Default setting: Not Configured (not enabled)"**, and *"If you disable or don't configure this policy setting, the process's command line information won't be included in Audit Process Creation events."* GPO path: `Administrative Templates\System\Audit Process Creation`. **So on a stock host there is no 4688 at all; where 4688 exists, the arguments are absent.** ⚠️ The registry value name behind the policy is **NOT VERIFIED** — the Microsoft page gives the GPO path only; use the GPO name, not a registry path, in our material. 🔴 **Prefetch does NOT carry arguments** — it records the executable and referenced files; students reach for it and get the wrong claim. 🟢 **PSReadLine `ConsoleHost_history.txt` is the default-on sleeper** (**G3**) if PowerShell was the vehicle. **Teach the negative finding as the deliverable.** | [MS: command-line process auditing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing) |
| 2 | *(implicit)* "Amcache gives you the binary's hash" | 🔴🔴 **True, with two limits that change the answer.** The hash is in **`Root\InventoryApplicationFile`**, field **`FileId`**, and it is **SHA-1 with four zeroes prepended** — *"the SHA-1 hash with 'four zeroes appended to the beginning of the hash'"*. **Strip `0000` before any lookup.** 🔴🔴 **And it covers only the first 31,457,280 bytes (~30 MB), not the whole file** — so **for any binary over 30 MB the Amcache hash will never match VirusTotal or NSRL**, and two files sharing their first 30 MB share a `FileId`. **Amcache's hash is an identification aid, not an integrity value** — the same distinction as MD5 in block **K7**. Other fields: `LowerCaseLongPath`, `Name`, `OriginalFileName`, `Publisher`, `Version`, `BinaryType`, `ProductName`, `LinkDate`, `Size`, `IsOsComponent`, `ProgramId`. | [Securelist, Amcache](https://securelist.com/amcache-forensic-artifact/117622/) · [NVISO](https://blog.nviso.eu/2022/03/07/amcache-contains-sha-1-hash-it-depends/) |
| 3 | *(implicit)* "Amcache shows the malware ran" | 🔴🔴 **No — Amcache is presence, not execution.** Cyber Triage: entries *"should generally not be used to prove program execution. Safer to interpret data as evidence of existence."* Securelist rates `InventoryApplicationFile` as presence only — *"with no data on whether or when they ran."* Carvey: analysts *"should not consider artifacts in isolation … but should instead look to multiple data sources and artifacts, viewed together."* 🟢 **This independently confirms `S5-06`'s existing framing** (*presence vs execution*) from a second direction, and it means **execution must come from Prefetch or the task's own 200/201 records.** | [Cyber Triage, 2026](https://www.cybertriage.com/blog/shimcache-and-amcache-forensic-analysis-2026/) · [Securelist](https://securelist.com/amcache-forensic-artifact/117622/) · [Carvey](http://windowsir.blogspot.com/2024/11/program-execution-shimcacheamcache-myth.html) |
| 4 | *(implicit)* RDP evidence is reliable | 🟢 **The one default-on artifact in the room** — `TerminalServices-LocalSessionManager/Operational` (**G6**, already verified). Chain **1149 → 4624 t10 → 21 → 22**; **1149 is not authentication** and fires before it; filter `Source Network Address = LOCAL`. 🔴 **Clearing these logs is now `T1685.005`, not `T1070.001`** — #6. | block **G6**; [T1685](https://attack.mitre.org/techniques/T1685/) |
| 5 | *(implicit)* "the NTLM hash is the prize" | 🔴 **More nuanced than either "NTLM is dead" or "NTLM is fine".** Microsoft: *"All versions of NTLM, including LANMAN, NTLMv1, and NTLMv2, are no longer under active feature development and are deprecated"* (June 2024), and *"NTLMv1 is removed starting in Windows 11, version 24H2 and Windows Server 2025"* — ⚠️ though *"remnants of NTLMv1 cryptography are still present in some scenarios, such as when using MS-CHAPv2 in a domain-joined environment."* **NTLMv2 still works and is still on by default**; a phased plan to disable NTLM by default was announced **Feb 2026 for a future release**. The **NT hash is unchanged**: `NTOWFv1(Passwd, User, UserDom) = MD4(UNICODE(Passwd))` — unsalted, uniterated — stored in `NTDS.dit` (`unicodePwd`) and the **SAM**. 🔴🔴 **Credential Guard is narrower than taught:** *"Starting in Windows 11, 22H2 and Windows Server 2025, Credential Guard is enabled by default on domain-joined, non-DC systems that meet hardware requirements"* — **Enterprise and Education only; Pro is NO.** And *"Credential Guard doesn't provide protections for the Active Directory database or the Security Accounts Manager (SAM)."* **Net: pass-the-hash is current practice, not history.** | [MS deprecated features](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features) · [NTLMv1 removal](https://support.microsoft.com/en-us/topic/upcoming-changes-to-ntlmv1-in-windows-11-version-24h2-and-windows-server-2025-c0554217-cdbc-420f-b47c-e02b2db49b2e) · [MS-NLMP NTOWFv1](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/464551a8-9fc4-428e-b3d3-bc5bfb2e73a5) · [passwords technical overview](https://learn.microsoft.com/en-us/windows-server/security/kerberos/passwords-technical-overview) · [Credential Guard](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/) |
| 6 | ATT&CK mapping for this chain | 🔴🔴 **One real mapping trap: no `T1574` sub-technique fits an overwritten scheduled-task binary.** `T1574.010` is **services-only** by MITRE's own opening sentence — *"Adversaries may execute their own malicious payloads by hijacking the binaries used by **services**."* The full sub-technique list (.001 DLL, .004 Dylib, .005 Executable Installer File Permissions Weakness, .006 Dynamic Linker Hijacking, .007–.009 Path Interception, .010/.011 Services, .012 COR_PROFILER, .013 KernelCallbackTable, .014 AppDomainManager) **has no scheduled-task entry.** **Correct mapping: `T1053.005`.** Teach `.010` as the *services* analogue and name the trap. Current tactics: **T1021.001** Lateral Movement · **T1003.001**/**T1003.002** Credential Access · **T1550.002** Lateral Movement · **T1078.002 Valid Accounts: Domain Accounts → Stealth, Persistence, Privilege Escalation, Initial Access** · **T1053.005** Execution, Persistence, Privilege Escalation · **T1574 → Stealth, Execution**. ⚠️ **Two of these now carry the Stealth tactic** (T1078.002, T1574) — consistent with **E11**/block **K1**. ⚠️ **v19.2's exact release date is NOT VERIFIED** — MITRE's `index.json` lists only to **v19.1 (12 May 2026)**; v19.0 was 28 Apr 2026, and block **K1**'s "6 Aug 2026" comes from the updates page, not the STIX index. **Cite the version, not the date.** | [T1574.010](https://attack.mitre.org/techniques/T1574/010/) · [T1053.005](https://attack.mitre.org/techniques/T1053/005/) · [T1078.002](https://attack.mitre.org/techniques/T1078/002/) · [attack-stix-data index](https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json) |
| 7 | *(implicit)* "the credential dump left a trace" | 🔴🔴 **On a default host, essentially not.** **Sysmon 10 (ProcessAccess)** is the artifact of record and **Sysmon is not installed by default**. **Defender's ASR rule** *"Block credential stealing from the Windows local security authority subsystem"* exists but ⚠️ **ASR rules are not enabled by default**. Security 4656/4663 on LSASS need a SACL nobody sets. **`rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <pid> <out> full` is a signed-Microsoft LOLBin** — no file to find, no hash to look up. **The only anomaly is the command line, which #1 just showed is usually missing.** ⚠️ **ASR GUID NOT VERIFIED** — not retrieved; cite the rule by name. 🟢 Check Defender **`DetectionHistory`** independently of the event log (**G8**). | block **G8**; §2.6 |

### NOT VERIFIED — carried forward honestly

- **The registry value name** behind *Include command line in process creation events* (the Microsoft
  page gives the GPO path only). **Use the policy name in our material, not a registry path.**
- **The ASR rule GUID** for LSASS credential-stealing protection, and the event ID an ASR block
  raises. **Cite the rule by name until confirmed.**
- **The OS default for *Audit Other Object Access Events*** (governs Security 4698) — carried from
  **G6**; check with `auditpol`.
- **ATT&CK v19.2's exact release date** — `index.json` lags at v19.1 (12 May 2026). **Cite the
  version, not the date**, and correct block K's "6 Aug 2026" to "per the updates page" if it is ever
  used in student-facing material.
- **Which artifact the room actually intends for Q4** — the lab has enabled something it does not
  name. Not determinable without running it.

## 4. Evidence used

**A two-machine lab — AttackBox plus a Windows target reached over RDP.** No image, no download, no
hash. Same disposition as rooms 22 and 23.

- **Downloadable?** ⚠️ **No.** **Reusable?** 🔴 **No** — not obtainable.
- **`ecdfp-evidence` action: none.** 🔴 **Third room running with no evidence set.** `EVS-10` remains
  unallocated. ⚠️ **That is now a pattern worth naming: the entire Honeynet Collapse module is
  live-VM-only, so it can contribute scenario design and question design but never evidence.**
  Our S5/S6 material still needs a Windows intrusion image, and **no room in the Priority-2 set will
  supply one.**

### 🔴🔴 The credential defects — two, and the second is the serious one

**First, the familiar one:** the room **publishes plaintext RDP credentials** in the task body
(not reproduced — **R8**). Fourth Priority-2 room. Our answer is in room 23 §4.

**Second, and this is new: Q6's expected answer *is* a credential.**

> *"What is the NTLM hash of matthew.collins' domain password?"*

🔴🔴 **An NT hash is not a hash-as-evidence; it is an authenticator.** Per §2.7, NTLM authentication
takes the hash directly — the plaintext is never required — and **NTLMv2 is still enabled by default
on current Windows.** So:

1. **The room's public answer key contains a working domain credential** for its own environment.
   Every write-up that publishes the answer republishes it. 🟢 Harmless here because the environment
   is fictional and disposable — **but the shape is the problem, not the blast radius.**
2. **It trains the wrong reflex.** A student who learns that "submit the hash" is a normal deliverable
   will paste a real one into a ticket, a chat, or a report appendix on their first engagement.
3. ⚠️ **It is also a weak forensic question.** *"What is the hash?"* tests whether you ran a parser.
   *"Which account's credentials were exposed on this host, and how do you know?"* tests the
   investigation — **and has the same evidentiary payload without the credential.**

**Our rule, and it should be explicit in the question-design guidance:**

> **No eCDFP question may have a credential as its answer.** Ask **which** account was compromised,
> **when**, **from what artifact**, and **what that does and does not prove**. Where a secret must be
> recorded at all, it goes to the restricted appendix by reference — *path, offset, timestamp* — never
> by value. **This applies to NT hashes, Kerberos tickets, API keys and WLAN PSKs equally**, because
> all four are authenticators.

🟢 This generalises **R8** from *"do not reproduce credentials in notes"* to *"do not design
questions whose answers are credentials"*, which is the version that actually reaches students.

### Critique of the scenario brief

🟢🟢 **The best single detail in the module is the cover story.** *"It became unstable after we
replaced the motherboard"* means **every anomaly the attacker produces has a pre-approved innocent
explanation.** No other room in the corpus builds an alibi into the environment.

**Use it verbatim in `S1`**, paired with room 23's brief: room 23 shows a control failure that
*creates* the exposure; this one shows a narrative that *conceals* it. ⚠️ **And it is the honest
counter-example to alert triage** — the "known issue" that makes a real intrusion unremarkable is
exactly why the SIEM was never consulted until everything was encrypted.

⚠️ **One flaw:** the brief states outright that *"the threat actor continued the attack. With the
entry point secured and Emily's domain credentials stolen…"* — **the student is told the conclusion
of stage 1 as the premise of stage 2.** 🟢 **Defensible for a chained module** (it is the catch-up
state, §5.1) and much less objectionable than room 22's announced betrayal, **but our version should
mark such text visibly as *given context*, not as findings** — otherwise students inherit
conclusions they did not establish, which is a D20 criterion-4 habit failure in slow motion.

## 5. Lab design worth reusing

### 5.1 🟢🟢 The module map is byte-identical across rooms — state carried by an asset, not by prose

Verified rather than assumed: the diagram in this room is the **same file** as room 23's —
asset ID `678ecc92c80aa206339f0f23-1750969983020.svg`, 1760 × 670, same alt text. The rooms differ
only in the sentence naming the stage (*"the second attack stage (#2 on the network diagram)"*).

🟢🟢 **That is the cheapest continuity mechanism imaginable**: one asset, six rooms, one sentence of
delta. It confirms room 23 §5.1's reading and strengthens the recommendation — **F7 is drawn once and
referenced, not redrawn per session.** ⚠️ Our version adds what theirs lacks: **highlight the current
stage** rather than leaving the reader to find the number.

### 5.2 🟢🟢 The cover story — an alibi built into the environment

§4 covers it. **Adopt for D19.** Our carry-through incident should include one pre-existing,
documented, benign fault that plausibly explains a class of the attacker's noise. It costs one
sentence in the scenario and it converts *"why didn't anyone notice?"* from a plot hole into a
lesson.

### 5.3 🟢 The attacker never picks the second host — the organisation hands it over

§1 covers it. **Adopt for the S6 capstone brief.** Lateral movement in most teaching material is a
technical event; here it is a **work assignment**. That framing is more accurate and it makes the
control discussion (why does a QA box hold domain-admin sessions?) unavoidable.

### 5.4 ⚠️ Tip 3 is the whole tooling curriculum in six words

*"You might need to use EZ tools for this scenario."* 🟢 Correct, and it matches our **S4-08**/**S5**
tooling. ⚠️ **But EZ Tools GUI are .NET 9 only** as of `2026.5.0` (**I10**) — **the `CLEAN-TOOLS`
snapshot (D17) must include .NET 9**, already logged after room 21 and confirmed again here.

### 5.5 🔴 Safety and handling defects

**One new, and it is subtle enough that we would probably have shipped it ourselves — the tenth in
the project.**

🔴🔴 **The room has students RDP into the live evidence host as Administrator and run the analysis
tools *on it*.** Tip 3 recommends EZ Tools; the lab gives an RDP session and nothing else.

**Why that is a defect and not just untidy:**

1. **The tools contaminate the exact artifacts under examination.** Running `PECmd`,
   `AmcacheParser` or `RECmd` on the live host **creates new Prefetch entries and new
   `InventoryApplicationFile` rows for those tools** — in the two artifacts (§2.3, §2.5) the room's
   own questions depend on. 🔴 **The examiner's activity becomes indistinguishable in kind from the
   subject's**, in the same data set.
2. **The student's own RDP logon writes 4624/21/22 records** into the channel they are about to use
   to answer Q1 — the same class of record as the attacker's, minutes later.
3. **A first interactive logon creates a profile**, writes `NTUSER.DAT`, and touches ShellBags,
   RecentDocs and JumpLists — the S5 artifact family entire.

**This is the Windows counterpart of room 22's mount defect and room 23's bootloader defect, and it
completes the pattern**: all six evidence defects in the corpus are *"act on the live system"*
rather than *"collect, verify, then analyse a copy."*

🟢 **In fairness the room is a live-response exercise, and live response is legitimate** — our own
**S2-02** teaches it. **The defect is the absence of the ordering rule**, not the activity.

**Our version:** live response is explicitly framed as **collection**, not analysis — the student
collects with a documented, minimal-footprint toolset, **hashes what they collected**, and then
**analyses the copy on `FOR-WS01`**. Every tool run on the subject host is recorded in the
chain-of-custody form as an examiner action (the same habit room 23 §5.5 asks for), **so the
Prefetch and Amcache entries the examiner created are explainable rather than confusing.**
🟢🟢 **And that is a better lesson than the defect it fixes:** students see their own footprint in
the evidence, which is the most convincing argument for minimal footprint there is.

**Running total: 10 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24. Four endanger the analyst's
machine; six endanger the evidence. All six evidence defects are "act on the live system instead of
collecting first."** 🔴 **That is now a named pattern and it needs a slide in `S2-01`/`S2-02`.**

## 6. Question patterns

**Six scored questions across two tasks, tracing a clean four-step chain** — RDP in → replace the
task's binary → dump credentials → move laterally. 🟢 **The order is the intrusion's order**, so a
student who answers in sequence has reconstructed the stage without being told its shape.

**🟢 Answer formats are specified on both timestamp questions** (`2025-01-15 19:30:45`) — consistent
with rooms 19–23. ⚠️ **But no timezone is stated**, and this room spans three event channels plus
registry timestamps. **A format without a timezone is half a format**, and our rows must say `UTC`.

**⚠️ Stems assert their conclusions, again** — *"the binary that was replaced **for persistence and
privesc**"* · *"**the** malware family"* · *"the command line used to **dump the OS credentials**"* ·
*"**Using the stolen credentials**, when did the attacker perform lateral movement?"*. **Seventh room
running.** 🔴 **Q3 is the worst of them: *"What is the type or malware family"* presumes the binary
has a family** — §2.4 shows that unknown-to-every-engine is a legitimate and more interesting result,
and the question shape forbids it.

**🔴🔴 And Q6 should not exist in this form — its answer is a credential.** Full argument in §4. It is
the first *question-design* defect in the corpus serious enough to become a rule, and the rule is:
**no eCDFP question may have a credential as its answer.**

**🔴 Twenty-fourth room, no "cannot be determined" question** — and this room is the sharpest case yet,
because **the room's own artifacts are mostly off by default**, so "not recoverable" is the *realistic*
answer to two of its six questions:

| the room could have asked | correct answer |
|---|---|
| *"What was the full command line of the credential-dumping process?"* — i.e. **the room's own Q4** | 🔴🔴🔴 **On a default host: not recoverable.** *Audit Process Creation* is **"Default: Not configured"** and the command-line policy is **"Not Configured (not enabled)"**. **The best row in the corpus so far, because the room asks this question as though it always has an answer.** The professional output is *"execution of `rundll32.exe` at T is established by Prefetch; arguments are not recoverable because process creation auditing was not enabled."* |
| *"Prefetch shows `rundll32.exe` ran. What arguments did it take?"* | 🔴🔴 **Cannot be determined — Prefetch does not store arguments.** It records the executable and referenced files. The single most common wrong turn in this scenario. |
| *"Amcache shows the malicious binary. When did it run?"* | 🔴🔴 **Cannot be determined from Amcache — it proves presence, not execution** (*"no data on whether or when they ran"*). Execution needs Prefetch or the task's 200/201 records. |
| *"The Amcache `FileId` doesn't match any VirusTotal entry. Is the binary unknown?"* | 🔴🔴 **Not established.** Two reasons: the leading **`0000`** was probably not stripped, and **the hash only covers the first ~30 MB**, so a larger binary can never match. **A negative lookup here is a tooling artefact, not a finding.** |
| *"Event 1149 appears at 03:12. Did the attacker log in then?"* | 🔴 **No.** 1149 fires **before** authentication. **1149 with no matching 21 is scanning or failed credentials.** |
| *"No Sysmon event 10 for LSASS. Was LSASS dumped?"* | 🔴🔴 **Cannot be determined.** Sysmon is not installed by default, ASR rules are not enabled by default, and 4656/4663 need a SACL nobody sets. **A full LSASS dump on a default host leaves no direct record of the read.** |
| *"`Terminal Server Client\Servers` lists 172.16.8.15. Did the attacker reach it?"* | ⚠️ **Not established** — the key records a destination that was **typed**, not reached, and carries no time. Success needs the destination's own logs. |
| *"The task XML points at `checker.exe`. Is that the malicious binary?"* | 🔴 **Not from the XML.** The task names a **path**; the attacker changed the **file**. Mechanism ≠ payload. |
| *"`schtasks /query` shows no suspicious task. Is there persistence?"* | 🔴🔴 **Cannot be determined** — an `SD`-deleted task keeps running while vanishing from `schtasks`, Autoruns and the GUI (**G5**). **The enumerating tools fail open.** |

🟢🟢 **Nine, and two of them are the room's own questions.** Q4 in particular is a question whose
honest answer is *"not recoverable"* on any host the students will actually meet — **which is the
clearest evidence yet that the missing question type is not a stylistic preference but a correctness
issue.**

## 7. Figures

**Only one non-decorative image, and it is the module map — byte-identical to room 23's** (§5.1),
already transcribed in `initialaccesspot.md` §7. ⚠️ **The remaining 14 images were not enumerated
individually**; the DOM query filtered for diagram-like alt text and returned exactly one hit. On the
evidence of rooms 22–23 the rest are room icon, banner, hero, avatars and the target-machine
placeholder. **Recorded as filtered-not-exhaustive rather than claimed as decorative.**

🔴 **So: fifth room running with no room-specific conceptual figure** — a 60-minute investigation
across eight artifact families, three event channels and a registry hive, with one reused topology
diagram and nothing else.

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F14 | **On by default, or not** | Two columns of Windows artifacts — **default-on** (Prefetch, Amcache, ShimCache, LocalSessionManager 21/22, Security 4624, PSReadLine) against **requires configuration** (4688, 4688 + command line, Task Scheduler Operational, Sysmon 1/10, ASR, SACL-based 4663). Each "requires" row tagged with what turns it on. | **🔴 P1** | **The most important idea in the room.** It is why Q4's honest answer is often "not recoverable", and it is the Windows half of the D38 contrast table. |
| F15 | **Anatomy of an Amcache `FileId`** | The value drawn as `0000` + 40 hex chars, the prefix struck through and labelled *"strip before lookup"*; beside it a file bar with the first 30 MB shaded *"hashed"* and the remainder *"not hashed"*, and a callout: *"two files sharing their first 30 MB share a FileId."* | **🔴 P1** | §2.3's two limits — the difference between an identification aid and an integrity value. |
| F16 | **The RDP event chain** | Timeline: **1149 → 4624 t10 → 21 → 22**, with 1149 boxed in amber and labelled *"not authentication — fires before credentials"*, and a branch showing **1149 with no 21 = scanning or failure**. | **🔴 P1** | §2.1's two classic errors, both of which produce a wrong timestamp in a report. |
| F17 | **4648 as the pivot** | Source host and destination host; one 4648 record on the source expanded to show *source account · target account · target server*; a dashed arrow to the destination's 4624 labelled *"success lives here, not here."* | **🟢 P2** | §2.8 — attempt vs success, and why one host is half a finding. |
| F18 | **The NT hash and its five gates** | `MD4(UTF-16LE(password))` shown unsalted and uniterated, with two identical passwords producing identical hashes; beside it Credential Guard's five gates as a funnel (22H2+ · domain-joined · non-DC · Enterprise/Education · VBS hardware), and **SAM drawn outside the protected boundary**. | **🟢 P2** | §2.7 — why pass-the-hash is current, not historical, stated precisely enough to survive a student objection. |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 2"* — correct, and it undersells it.

**This is the first fully in-scope room of the module** and the strongest single source we have found
for **`S5-05`/`S5-06`** and for the *default-on vs configured* distinction that shapes every Windows
artifact lesson. Amend the Part 1 row to say so.

### Rows this strengthens

- **`S5-06`** (*"Amcache and ShimCache — presence vs execution, and the classic misreading"*) —
  🟢🟢 **the row is named for exactly this and the room supplies three corrections**: Amcache proves
  presence not execution (independently confirmed, §3 #3), the **`0000` prefix**, and the
  **~30 MB hash truncation**. **The last is new to the project and changes what students are told to
  do with the value.** Plus figure **F15**.
- **`S5-05`** (Prefetch) — 🔴 **add the negative explicitly: Prefetch does not store command-line
  arguments.** It is the most common wrong turn in this scenario and the row currently does not say
  it.
- **`S6-06`** (*"Windows event logs for the timeline — what survives, what is cleared, what is never
  written"*) — 🟢🟢 **figure F14 belongs here and the row's own title asks for it.** *"What is never
  written"* is precisely the 4688 finding. 🔴 **And log clearing here maps to `T1685.005`, not
  `T1070.001`** (block **K1**) — the first row in the map that actually needs that correction.
- **`S5-01`/`S5-02`** — the Task Scheduler artifact trio (XML · `TaskCache` · channel) and the
  Tarrask `SD` cross-check (**G5**), which is a registry-structure lesson as much as a persistence one.
- **`S6-09`** (capstone) — **4648 as the pivot event** (F17) and the source-vs-destination split.
- **`S1-04`** (report template) — 🟢🟢 **§2.4's finding-vs-interpretation split is the cleanest worked
  example we have**: *"the binary has SHA-1 X"* is a finding; *"it is Mimikatz"* is an interpretation
  resting on a third-party classifier, and **the vendor and lookup date must be named.**
- **`S2-01`/`S2-02`** — 🔴 **the named pattern from §5.5**: all six evidence defects in the corpus are
  *act on the live system instead of collecting first.*

### Back-propagation

🟢 **One, and it is small.** Block **K1** states ATT&CK **v19.2, released 6 August 2026**. The date
comes from MITRE's **updates page**; the **`attack-stix-data` index lists only to v19.1 (12 May
2026)**. Not a contradiction — the STIX index lags the site — **but the note now says "cite the
version, not the date"**, and block K should be read with that caveat. ✅ **No other correction:
T1562 still absent from the repo; T1070.004/.006/.009 still live; and this room's IDs
(T1021.001, T1003.001/.002, T1550.002, T1078.002, T1053.005, T1574) appear nowhere in the repo yet.**

**Third room running with no substantive back-propagation.**

### Minutes

**Net zero.** Every item lands as content or a correction inside a named existing row — `S5-05`,
`S5-06`, `S6-06`, `S5-01`, `S6-09`, `S1-04`, `S2-01`. **No new rows.**

⚠️ **But an honest caveat that is starting to matter:** three rooms running have landed "net zero,
into existing rows." **That is true row-by-row and cannot stay true indefinitely** — `S5-06` has now
absorbed material from rooms 21, 23 and 24, and at some point a 20-minute row with four rooms'
findings in it is overfull even though no row count changed. 🔴 **This should be checked during the
S5 re-split, not assumed away.** Recorded so the re-split has the list.

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Nineteenth room carrying the S5 overdraft.** ⚠️ **And this room does add to S5 — three
corrections into `S5-06` and one into `S5-05`** — so the two-room reprieve ends here.

### Out of scope

Windows privilege-escalation tradecraft, Mimikatz operation, and RDP administration. ⚠️ One item sits
on the line: **pass-the-hash mechanics**. We are a forensics course, not an offensive one — **but
§2.7's currency (NTLMv1 removed, NTLMv2 default-on, Credential Guard's five gates, SAM unprotected)
is exactly the context an examiner needs to say what a stolen hash means.** **One slide in `S5`,
framed as "what does possessing this prove", not "how to use it."**

### Still unresolved

- **S5 re-split** — nineteenth room, and now with a second dimension: **row-level overload inside
  `S5-06`**, not just session totals.
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- **🆕 No Windows intrusion image anywhere in the Priority-2 set.** §4. The whole Honeynet module is
  live-VM-only. **S5 and S6 still need an image, and extraction will not supply one** — it has to be
  staged on `EVI-SRC01` per **D19**, or sourced from CFReDS (**D36**).
- **D19 has no per-session host map** (room 23) — still open, still gating F7.
- **`ecdfp-case` skill** not installed.
- ⚠️ **`knowledge_base/` EXISTS** — corrected 2026-08-29 while extracting room 25. It was
  built the same day from `Resources/` by `ecdfp-intake`: five condensed module files, an
  `instructor/` folder of 8 session notes, and `_source_text/` holding 10 INE units (2,218 pages)
  plus 9 instructor decks. **`evidence/`, `packages/`, `cases/` and `labs/` still do not exist.**
  🔴 **And the sharper point survives the correction: not one of the room notes has been through
  `ecdfp-intake`.** The knowledge base was built from INE courseware and the instructor's own
  decks — **none of the THM research has landed in it.**

## 9. Links

**Room** — <https://tryhackme.com/room/elevatingmovement>
**Module** — Honeynet Collapse, stage 2 of 6. Previous: <https://tryhackme.com/room/initialaccesspot>.
Next: <https://tryhackme.com/room/lostinramslation>.
**Companion notes** — `initialaccesspot.md` (the module map, transcribed) ·
`honeynet-collapse-module.md` (the arc, written after stage 6) ·
`windows-user-activity.md` and `expediting-registry-analysis.md` (S5 artifacts this corrects) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **G5–G8**, **I10**, **K1** and new block **L**.

**Citations from §3, by finding:**

- #1 command line — MS, *Command line process auditing*
  <https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing>
- #2, #3 Amcache — Securelist <https://securelist.com/amcache-forensic-artifact/117622/> ·
  NVISO <https://blog.nviso.eu/2022/03/07/amcache-contains-sha-1-hash-it-depends/> ·
  Cyber Triage <https://www.cybertriage.com/blog/shimcache-and-amcache-forensic-analysis-2026/> ·
  Carvey <http://windowsir.blogspot.com/2024/11/program-execution-shimcacheamcache-myth.html>
- #4 RDP — block **G6** (already verified) ·
  T1685 <https://attack.mitre.org/techniques/T1685/>
- #5 NTLM and Credential Guard — MS deprecated features
  <https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features> ·
  NTLMv1 removal
  <https://support.microsoft.com/en-us/topic/upcoming-changes-to-ntlmv1-in-windows-11-version-24h2-and-windows-server-2025-c0554217-cdbc-420f-b47c-e02b2db49b2e> ·
  MS-NLMP `NTOWFv1`
  <https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/464551a8-9fc4-428e-b3d3-bc5bfb2e73a5> ·
  Passwords technical overview
  <https://learn.microsoft.com/en-us/windows-server/security/kerberos/passwords-technical-overview> ·
  Credential Guard
  <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/> ·
  Disabling NTLM by default (Feb 2026)
  <https://techcommunity.microsoft.com/blog/windows-itpro-blog/advancing-windows-security-disabling-ntlm-by-default/4489526>
- #6 ATT&CK — T1574.010 <https://attack.mitre.org/techniques/T1574/010/> ·
  T1053.005 <https://attack.mitre.org/techniques/T1053/005/> ·
  T1078.002 <https://attack.mitre.org/techniques/T1078/002/> ·
  T1021.001 <https://attack.mitre.org/techniques/T1021/001/> ·
  T1003.001 <https://attack.mitre.org/techniques/T1003/001/> ·
  T1550.002 <https://attack.mitre.org/techniques/T1550/002/> ·
  STIX index <https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json>
- #7 credential dumping — blocks **G7**/**G8**; §2.6
