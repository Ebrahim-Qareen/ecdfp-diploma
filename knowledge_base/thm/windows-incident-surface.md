---
room: Windows Incident Surface
url: https://tryhackme.com/room/winincidentsurface
module: Advanced Endpoint Investigations — **walkthrough room**, not a challenge. **Priority 3.**
feeds: 🟢🟢 **`S2-02` (live response) — the strongest source we have found for it.** Also `S5-01`,
       `S5-05`, `S6-06` and the `S1` toolkit/`CLEAN-TOOLS` rationale (**D17**).
       🔴🔴 **Safety defect #11, and the most destructive in the corpus:** opening PowerShell before
       following the room's step order **wipes every event log on the evidence machine** (§5.4).
       🔴🔴 **And it independently validates block K1** — a 2025-authored DFIR room already cites two
       ATT&CK IDs that have since been revoked or moved (§3 #2).
difficulty / time: Info-level walkthrough · **180 min** · 9 tasks · 25 scored questions ·
                   **free (no Premium badge)** · 11,356 completions · 205 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (accordion loop, 9/9 tasks)
completeness: **all 9 tasks read in full — 47 KB of task text.** 0 sections NOT READ.
              ⚠️ **Priority 3 — this note is deliberately shorter than the Priority 2 set** and
              concentrates on what `S2-02` can use. The room is rich enough that a full-depth note
              would be justified; it is not written here because the extraction budget is committed
              elsewhere. **Say so rather than implying the room is thin.**
              🟢 **No credentials published** — and the room **redacts its own answers** (`[REDACTED]`)
              throughout the walkthrough, so students must run the commands. Nothing to withhold
              under R8.
              🟢 **Unlike rooms 18–28, §2 is NOT reconstructed from question stems** — this is a
              walkthrough that prints its commands and outputs, so the artifact analysis is grounded
              in what the room actually shows.
---

## 1. What the room teaches

**That the first thing a live-response analyst must establish is whether their own tools can be
trusted — and it makes that concrete in a way no other room in the corpus does.**

Task 2 is the whole reason to read this room. It opens on a genuine problem:

> *"A PowerShell profile is a script that executes every time PowerShell is executed… before even
> executing PowerShell, we should look for traces of compromise in the PowerShell profile. Since we
> were going to use PowerShell to perform our analysis, **this creates a chicken and egg problem for
> us.**"*

🟢🟢 **And the answer is the right one: bring your own tools.** The room ships a toolbox of trusted
shells and starts with **Command Prompt rather than PowerShell**, for a stated reason — *"unlike
PowerShell, it does not require a profile to execute, therefore, making it immune to execution flow
hijack during startup."* **That is a genuine, defensible piece of live-response tradecraft**, and it
is the missing justification for our own `CLEAN-TOOLS` snapshot (**D17**), which currently exists
mostly as a convenience.

**The staged profile is the payoff, and it is well built.** The room prints it in full:

```
Set-PSReadlineOption -HistorySaveStyle SaveNothing
Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue
…
wevtutil el | ForEach-Object {wevtutil cl $_}; Stop-Service -Name "eventlog" -Force
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" `
  -Name "UseLogonCredential" -Value 1 -PropertyType DWORD -Force
```

**Four distinct techniques in five lines** — suppress shell history, clear and then *stop* the event
log service, and re-enable cleartext credential caching. 🟢 **Every one of them fires the moment an
analyst opens PowerShell**, which is exactly the point.

**The rest of the room is a competent triage walk** — system profile, users and sessions, network
scope, autostart and registry, services and scheduled tasks, processes and directories — following
one attack chain through each: a mistyped admin account, a passwordless `Guest` session, a modified
`Userinit`, a netsh helper DLL loaded from a temp path, a fake `aurora-agent` "security" service, and
`INITIAL_LANTERN.exe` alongside `Invoke-SocksProxy.psm1` in a non-standard `AppData\SpcTmp\` folder.
🟢🟢 **Task 8 explicitly closes the loop back to Task 5** — *"Do you remember the network connections
with `ssh.exe` and `INITIAL.LANTERN.exe` that we got in Task #5?"* — **which is correlation taught as
a habit rather than asserted as a principle.**

**What it gets wrong:**

- 🔴🔴 **It booby-traps the evidence machine and never states the consequence.** §5.4. The room warns
  *"if you haven't performed the previous steps before executing PowerShell, please restart the VM"*
  — **but never says that opening PowerShell clears every event log and stops the eventlog service.**
- 🔴🔴 **Two of its ATT&CK IDs have been revoked or moved since it was written** (§3 #2), and a third
  has changed tactics. **A 2025-authored DFIR room, already stale.**
- 🔴 **The WDigest payoff is largely dead on a modern host** (§3 #1) — Credential Guard blocks it, and
  Microsoft now says plaintext is not stored *"even when `UseLogonCredential` is set to `1`"*.
- 🔴 **It uses `Get-WmiObject`** in Task 8, which is **removed in PowerShell 6/7** (**F5**).

## 2. Artifacts — one 6-box block each

🟢 Grounded in the room's printed commands and outputs, not reconstructed from question stems.

### 2.1 The PowerShell profile — an anti-forensic trap aimed at the investigator

- **What it is** — a script that runs every time PowerShell starts. **ATT&CK `T1546.013` Event
  Triggered Execution: PowerShell Profile**, tactics **Privilege Escalation + Persistence**.
- **Where it lives** — four files, and **the room's paths are the Windows PowerShell 5.1 tree**:
  `$PSHOME\profile.ps1` (all users, all hosts) · `$PSHOME\Microsoft.PowerShell_profile.ps1` (all
  users, current host) · `$HOME\Documents\WindowsPowerShell\profile.ps1` (current user, all hosts) ·
  `$HOME\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`.
  🔴 **PowerShell 7 uses a different tree** — `$HOME\Documents\**PowerShell**\Profile.ps1` — so
  **a live-response sweep must search both**, and a room that checks only one is incomplete on any
  host with pwsh installed. ⚠️ The 5.1 path strings are **NOT VERIFIED** against Microsoft in this
  pass; the 7 paths are.
- **What it proves** — that code was configured to run at every shell start, for a named scope.
- **What it does NOT prove** — 🔴🔴 **that it ran, or that the analyst has not already run it.** The
  profile executes on *shell start*, so **by the time you can query it with PowerShell you have
  already executed it.** That is the room's chicken-and-egg problem stated as an evidential one, and
  it is the sharpest live-response lesson in the corpus.
  ⚠️ **Scope matters and is easy to misreport** — an all-users/all-hosts profile affects every
  account; a current-user one is a single profile's problem. **"A malicious PowerShell profile was
  found" without naming which of the four is an incomplete finding.**
  🔴 **And absence proves nothing** — the same effect is achievable via `$PROFILE` redirection, a
  module autoload, or `PSModulePath` (§2.2).
- **How to parse it** — from **cmd.exe**, not PowerShell: `if exist "<path>" (echo …)` then `type`.
  🟢 **The room's own method is correct and worth copying verbatim** — resolve `$PSHOME` with
  `where powershell.exe`, resolve `$HOME` from `USERPROFILE`, then test all four paths.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the profile is not hiding; it is waiting.**
  ⚠️ **Legitimate profiles are common** — corporate environments deploy them for module loading and
  prompt customisation, so **the finding is the content, not the existence.** 🔴 **And note what this
  particular profile targets: the investigator.** Clearing logs and killing the eventlog service on
  *analyst* action is a deliberate trap, and **treating a suspect host as hostile to your tools is
  the correct default.**

### 2.2 Environment variables and execution-flow hijack

- **What it is** — the search paths and interpreters an analyst's commands will resolve through.
  **ATT&CK `T1574.007` Path Interception by PATH Environment Variable** — 🔴 **v2.0 (12 May 2026),
  and its tactics are now Stealth + Execution.** Any slide showing it under Persistence, Privilege
  Escalation or Defense Evasion is stale.
- **Where it lives** — the process environment (`set`), and persistently in
  `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment` and
  `HKCU\Environment`. The room's short-list of fields to check is good and worth reusing:
  **`ComSpec`** · **`Path`** · **`PSModulePath`** · **`Public`** · **`TEMP` / `TMP`**.
- **What it proves** — what a command name would have resolved to, for this process.
- **What it does NOT prove** — 🔴🔴 **that it matched at the time of the incident.** `set` shows
  **the environment of the process you ran it from**, inherited from its parent. **A hijack in
  another user's session, or one applied after your shell started, is invisible to it** — and the
  persistent registry values may differ from what any running process holds.
  ⚠️ **The room checks the live environment and not the registry**, which is the gap: **the live view
  is a snapshot of one process's inheritance chain.**
  🔴 And `ComSpec` pointing at a normal path proves the *variable* is clean, **not that
  `cmd.exe` at that path is the real one** — that needs a hash or signature check.
- **How to parse it** — `set > env_vars.txt` from a trusted shell; then compare against
  `HKLM\…\Session Manager\Environment` and `HKCU\Environment` from the registry, **and against a
  known-good baseline**.
- **Anti-forensics / false-positive caveat** — ⚠️ **`PSModulePath` is the underrated one.** A writable
  directory prepended there gives silent module hijack on every `Import-Module`, and it looks like an
  ordinary path list. 🟢 **The room lists it and then does not check it** — which is a gap worth
  filling in our version, since it is the same class of attack as the profile in §2.1.

### 2.3 System profile — and why the timezone is not an afterthought

- **What it is** — hostname, addresses, OS version and build, install date, last boot, architecture,
  **current date and timezone**, and the resultant set of policy.
- **Where it lives** — `Get-CimInstance Win32_NetworkAdapterConfiguration` · `Win32_OperatingSystem`
  · `Get-Date ; Get-TimeZone` · `Get-GPResultantSetOfPolicy -ReportType HTML` (🟢 still current on
  Server 2025, still produces HTML).
- **What it proves** — which machine you are on, in what state, referenced to what clock.
- **What it does NOT prove** — 🔴🔴 **that the clock is right.** The room says to *note* the time and
  timezone and to compare against *"the time at the organization wide NTP server"* — 🟢 **which is
  exactly right and almost always skipped.** **A host whose clock is wrong makes every timestamp in
  the investigation wrong by the same offset, silently**, and the only way to know is to compare
  against an external reference **at the time of collection**, because you cannot reconstruct it
  later.
  ⚠️ **And `LastBootUpTime` bounds far more than it looks** — it is the outer limit of everything
  volatile: process list, network connections, sessions. **A recent reboot is not an inconvenience,
  it is a scope statement.**
  🔴 **`InstallDate` is not the machine's age** — an image redeployment resets it.
- **How to parse it** — as above. 🟢🟢 **Record the timezone and the NTP delta in the case notes
  before anything else**, because every later artifact is read through it (**J4**, **O3**).
- **Anti-forensics / false-positive caveat** — ⚠️ **timezone and clock changes are themselves
  techniques** and leave traces in the event log — which, on this host, the profile in §2.1 has
  just cleared. 🟢 **`Get-GPResultantSetOfPolicy` is the room's best under-used idea**: policy is
  where an adversary makes changes durable (**`T1484.001`**, now *Domain or Tenant Policy
  Modification: Group Policy Modification* — **O6**), and an RSoP report is a cheap, complete
  snapshot.

### 2.4 Local accounts and groups — and the near-miss name

- **What it is** — who exists, who is privileged, and which names do not belong. **ATT&CK `T1136`
  Create Account (Persistence)**, **`T1098` Account Manipulation (Persistence + Privilege
  Escalation)**, **`T1078` Valid Accounts (Initial Access, Persistence, Privilege Escalation,
  Stealth)**.
- **Where it lives** — `Get-LocalUser`; `Get-CimInstance Win32_UserAccount -Filter
  "LocalAccount=True"` for `PasswordRequired` / `PasswordExpires` / `PasswordChangeable`; and
  `Get-LocalGroup` + `Get-LocalGroupMember` for membership. **On a dead image the same data is in the
  SAM hive.**
- **What it proves** — the account inventory and privilege assignment at collection time.
- **What it does NOT prove** — 🔴🔴 **that a suspicious-looking account is malicious, or that a
  normal-looking one is not.** The room's own finding is **three admin-like accounts of which one is
  *misspelled*** — a name-similarity signal, which is **`T1036` masquerading applied to accounts
  rather than files**, and subject to the same limit as **M5**: *the name is the least reliable
  column.* **The discriminators are creation time, SID, group membership and last-logon**, not
  spelling.
  🔴 **`PasswordRequired = False` on `Guest` is a configuration finding, not an intrusion finding** —
  it is the Windows default state for that account. **The intrusion finding is that it is *enabled*
  and *logged on*** (§2.5).
  ⚠️ **A local enumeration misses domain accounts entirely**, and this host is domain-joined by
  implication.
- **How to parse it** — the room's commands, piped through `tee` to a file — 🟢 **and `tee` on every
  command is itself good practice worth copying: the analyst's own output becomes contemporaneous
  notes.**
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the room's honesty here is its best moment:**
  *"these findings are not enough to jump to any conclusion without correlating with other artefacts
  and knowing the system's baseline configuration."* **That sentence is D20 criterion 4 in a
  walkthrough**, and it appears twice more in later tasks.

### 2.5 Sessions and network connections — the volatile pair

- **What it is** — who is logged on right now, and what the host is talking to. The room finds a
  **`Guest` session** and connections involving `ssh.exe`, **AnyDesk**, and a binary in a temp path.
- **Where it lives** — `PsLoggedon64.exe` (Sysinternals) for sessions; `Get-NetTCPConnection` joined
  to `Get-Process` for owning process **name and path**; `Get-CimInstance Win32_Share` for shares;
  `Get-NetFirewallProfile` and the room's `fw-summary.ps1` for firewall state and rules.
- **What it proves** — the state of sessions and sockets **at the instant of the query**.
- **What it does NOT prove** — 🔴🔴 **anything a moment later.** The room says it plainly —
  *"You may need to re-run the TCP connections command multiple times to validate all the findings
  above"* — 🟢 **which is the correct instruction and the reason live response is a sampling
  exercise, not an observation.** **Two runs disagreeing is not an error; it is the finding.**
  🔴 **A PID is not an identity** — the owning process may exit and its PID be reused (**M4**), so
  **join to the process *path*, which the room's query does.**
  ⚠️ **AnyDesk is the room's own worked example of dual-use** — *"Malicious actors often use this
  application to access the system remotely, but it can also be legitimately used."* 🟢 Correct, and
  the discriminator is the **two firewall rules pointing at two different drives**, not the presence
  of the tool.
  🔴 **All three firewall profiles disabled is a configuration finding**, and the room is careful:
  *"this can be suspicious if it is not a recognized configuration"* — **it is equally consistent
  with an EDR-managed host.**
- **How to parse it** — as above, **from the trusted toolbox**, with `tee`.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **this is the artifact class the §2.1 profile was
  built to destroy.** Sessions and sockets exist only in the running system; **the analyst who opens
  PowerShell first has killed the eventlog service and lost the historical half of this picture
  while the live half is still on screen.** ⚠️ **Order of volatility (D9) is not an abstraction
  here** — it is the difference between having this data and not.

### 2.6 Autostart — boot, logon, `Userinit`, and the netsh helper DLL

- **What it is** — the persistence sweep, and the room's best correlation chain.
- **Where it lives** — `autorunsc64.exe -a b * -h` (boot execute) and `-a l * -h` (logon), 🟢 **flags
  confirmed current** (`b` = *"Boot execute."*, `l` = *"Logon startups (this is the default)."*,
  `-h` = *"Show file hashes."*); `Get-CimInstance Win32_StartupCommand`; and the two registry values
  the room pivots on —
  `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\**Userinit**` and **`Shell`**.
  🔴 **The room cites no ID for this; the correct one is `T1547.004` Boot or Logon Autostart
  Execution: Winlogon Helper DLL** (Persistence + Privilege Escalation), whose description names both
  values: *"Winlogon\Userinit - points to userinit.exe … Winlogon\Shell - points to explorer.exe."*
- **What it proves** — that something is configured to execute at boot or at logon.
- **What it does NOT prove** — 🔴 **that it has executed, or that it is malicious.** Configuration,
  not event — the same *state vs event* distinction as room 23 §2.3. ⚠️ **`Userinit` legitimately
  holds `userinit.exe,` with a trailing comma**; the finding is the *appended* `cmd.exe`.
  🟢🟢 **The room's netsh pivot is the best-taught chain in the corpus and worth reproducing exactly:**
  `Userinit` runs `cmd.exe` → which silently launches `netsh.exe` → so check
  `HKLM\SOFTWARE\Microsoft\NetSh` → where one DLL entry has a **different pattern from every other**
  (a relative `.\` path rather than a bare DLL name). **ATT&CK `T1546.007` Event Triggered Execution:
  Netsh Helper DLL** — *"The paths to registered netsh.exe helper DLLs are entered into the Windows
  Registry at `HKLM\SOFTWARE\Microsoft\Netsh`."*
  ⚠️ **And the room is honest about why that is hard**: *"identifying this without any related
  pattern can be a rabbit hole, as we'd need to have a firm knowledge of the default and native
  functionality of the OS internals."* 🟢 **True, and it is the argument for a known-good baseline
  rather than for cleverness.**
- **How to parse it** — Autoruns with `-h`, output to file, **diffed against a baseline**.
  ⚠️ **Autoruns' VirusTotal option (`-v`) is off by default and requires accepting the terms** —
  🔴 **and submitting hashes from a client's machine is a disclosure decision, not a step** (same rule
  as **N1**/room 26 §2.4). **The room does not raise it.**
- **Anti-forensics / false-positive caveat** — 🟢 **Autoruns enumerates; it does not judge.** A
  hidden scheduled task with a deleted `SD` (**G5**) is invisible to it, and **the tools fail open.**
  🟢🟢 **The `.\` pattern anomaly is the transferable idea**: *the outlier in a list of similar
  entries is more informative than any single entry*, which generalises far beyond netsh.

### 2.7 Services and scheduled tasks — including the fake security agent

- **What it is** — the two background-execution stores. The room finds a service **`LMVCSS`** running
  from a temp path, and an **`aurora-agent`** service that *looks* like endpoint security, is set to
  **Auto**, and is **not running**.
- **Where it lives** — `Get-CimInstance Win32_Service` filtered on `State`, selecting
  **Name, DisplayName, State, StartMode, PathName, ProcessId** (🟢 the right field set); and
  `Get-CimInstance -Namespace Root/Microsoft/Windows/TaskScheduler MSFT_ScheduledTask` for tasks.
  On disk: `C:\Windows\System32\Tasks\` and the registry `TaskCache` (**G5**, room 24 §2.2).
- **What it proves** — configuration and current state.
- **What it does NOT prove** — 🔴🔴 **that a stopped security service was stopped by an adversary.**
  The room handles this well: *"we could have spotted an implementation of impairing defences … or it
  could be just an agent failure case"* — 🔴 **note the ID it uses, `T1562`, is now REVOKED into
  `T1685`** (§3 #2). 🟢🟢 **And the resolution is excellent tradecraft:** *"If you dig down into the
  details of the executable attached to this aurora-agent service, you'll come to know that it is not
  a legitimate aurora-agent file."* **The service name is a claim; the binary is the evidence.**
  ⚠️ **A service running from a temp path is strong but not conclusive** — badly packaged legitimate
  software does it too. **The finding is temp path *plus* a name with no vendor *plus* a hash nobody
  recognises.**
  🔴 **`State = Running` on a scheduled task is a moment's observation**, and the room correctly
  notes the numeric form (`4`) as well as the string.
- **How to parse it** — as above; then **hash the binary** (the room's questions ask for **SHA-256**,
  🟢 not MD5 — correct per **K7**), and check publisher and original filename.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the room asks for the *original filename* of the
  non-running service executable**, which is the PE version-info field — **a renamed binary keeps
  it**, and it is the cheapest unmasking in Windows forensics. ⚠️ Combine with **M5**'s three checks
  (path, parent, signature). 🔴 **And per room 24 §2.2, task and service *configuration* is not
  execution** — 200/201 or Prefetch is.

### 2.8 Processes, temp paths and the hidden volume

- **What it is** — the live process tree and the directories the attacker left things in. The room
  finds `ssh.exe` parented by the fake `aurora-agent`, `INITIAL_LANTERN.exe` in a non-standard
  `C:\Users\Administrator\AppData\SpcTmp\` beside `Invoke-SocksProxy.psm1`, an executable planted in
  the **Default** user profile's temp folder, and **a volume with no drive letter**.
- **Where it lives** — the room uses `Get-WmiObject Win32_Process` with `GetOwner()` for
  **Name / PID / PPID / User / CommandLine / Path** — 🔴 **`Get-WmiObject` is REMOVED in PowerShell
  6/7** (**F5**); use `Get-CimInstance`. Directories via `Get-ChildItem -Recurse -Force`; volumes via
  `Get-CimInstance Win32_Volume`.
- **What it proves** — parentage, command lines and file locations at the moment of the query.
- **What it does NOT prove** — 🔴🔴 **that the process tree is true.** PPIDs are attacker-settable
  (**`T1134.004`**) and PIDs are reused (**M4**) — **and the room's own Task 8 cites `T1036.009`,
  whose current name is *Break Process Trees* (tactic Stealth)**, i.e. the technique that makes its
  own method unreliable. ⚠️ **The room notes the parentage finding and does not caveat it.**
  🟢 **`CommandLine` from `Win32_Process` is a live read of the PEB** — so **the argument-spoofing
  caveat from block M1 applies here exactly**: it is a claim the process makes about itself.
  🔴 **A file in the `Default` user profile is a strong finding** — that profile is the template for
  *new* users, so anything planted there propagates. **The room finds it and does not say why it
  matters.**
  ⚠️ **A volume with no drive letter is not inherently suspicious** — recovery and EFI system
  partitions are unlettered by design. **The finding is an unlettered volume that is not one of
  those.**
- **How to parse it** — `Get-CimInstance Win32_Process`, `Get-ChildItem -Force` (**`-Force` is
  required or hidden items are missed** — the room uses it), `Get-CimInstance Win32_Volume`.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the room's closing move is the lesson:**
  `INITIAL_LANTERN.exe` sits next to `Invoke-SocksProxy.psm1`, **so the directory is the finding, not
  the file.** ⚠️ *"investigating directories can be overwhelming and intrusive… quick checks on the
  paths where suspicious instances are found could be fruitful"* — 🟢 **correct, and it is the
  triage-versus-exhaustive-analysis judgement the room opens with:** *"The goal isn't exhaustive
  analysis, rather efficient triage and actionable discovery."*

## 3. Tools and commands

Every command is the room's own; this table records what we would change.

| purpose | the room's command | our note |
|---|---|---|
| trusted shell | `CMD-DFIR.exe` from the toolbox | 🟢🟢 the room's best idea — **D17** rationale |
| environment | `set > env_vars.txt` | ⚠️ add the registry copies — §2.2 |
| PS profiles | `if exist … ` from cmd, then `type` | 🔴 **also search the PowerShell 7 tree** — #3 |
| system profile | `Get-CimInstance Win32_OperatingSystem` | 🟢 record timezone + NTP delta first |
| policy | `Get-GPResultantSetOfPolicy -ReportType HTML` | 🟢 still current on Server 2025 |
| users | `Get-LocalUser`; `Win32_UserAccount` | ⚠️ local only — domain accounts missed |
| sessions | `PsLoggedon64.exe` | ⚠️ **v1.35, effectively frozen since 2016** |
| connections | `Get-NetTCPConnection` + `Get-Process` | 🟢 joins on process **path**, not just PID |
| autostart | `autorunsc64.exe -a b * -h` / `-a l * -h` | 🟢 flags current; ⚠️ VT is a disclosure decision |
| services | `Win32_Service` → Name/State/StartMode/PathName | 🟢 correct field set |
| tasks | `MSFT_ScheduledTask` via CIM | ⚠️ add `TaskCache` cross-check (**G5**) |
| processes | `Get-WmiObject Win32_Process` | 🔴 **removed in PS 6/7 — use `Get-CimInstance`** (**F5**) |

### CURRENCY CHECK

| # | claim as the room teaches it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | the staged profile sets `UseLogonCredential=1` to capture cleartext credentials | 🔴🔴 **The technique is real; the payoff is largely dead on a modern host.** Path/value confirmed: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`, `UseLogonCredential`, DWORD. Setting 1 means *"the system will store cleartext credentials in LSA memory for the Wdigest SSP"*; *"On Windows 8.1 and 2012 R2+, the default is 0."* 🔴 **Credential Guard blocks it** — Microsoft lists *"WDigest (only SSO is blocked)"* among protocols CG restricts — **and CG is on by default**: *"Starting in Windows 11, 22H2 and Windows Server 2025, Credential Guard is enabled by default on devices which meet the requirements."* Microsoft goes further: *"Cleartext passwords are not being stored in LSASS on modern Windows by design, even when `UseLogonCredential` is set to `1`"*, and *"There is no supported process … to 'fully enable' WDigest on Windows 11 25H2."* 🟢🟢 **So teach it as a registry-artefact and intent indicator, not as a credential-dumping enabler** — and note **its presence *is* the finding**, since *"the `UseLogonCredential` value does not exist"* by default (⚠️ verified for Win7+KB2871997; **NOT VERIFIED** for Win10/11). **ATT&CK maps it to `T1112` Modify Registry (v3.0, Defense Impairment + Persistence)**, whose own procedure text names this exact key and value. | [MS, KB2871997 and WDigest](https://learn.microsoft.com/en-us/archive/blogs/kfalde/kb2871997-and-wdigest-part-1) · [CG considerations](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/considerations-known-issues) · [CG configure](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/configure) · [MS Q&A, WDigest on Win11](https://learn.microsoft.com/en-us/answers/questions/5869399/enable-wdigest-dont-work-on-windows-11) · [T1112](https://attack.mitre.org/techniques/T1112/) |
| 2 | the room's ATT&CK citations | 🔴🔴 **Two are revoked or moved, one changed tactics — in a room written in 2025.** ❌ **`T1070.001`** for clearing event logs → **now `T1685.005`** (block **K1**). ❌ **`T1562.002`** for stopping the eventlog service → **`T1562` was REVOKED into `T1685`** (**K1**). 🔴 **`T1574.007`** is still the right ID but is **v2.0 (12 May 2026) with tactics now Stealth + Execution**. 🔴 **`T1036.009`'s current name is "Break Process Trees"** (v2.0, Stealth) — the room says *"breaking process trees"*. ✅ Correct and unchanged: **`T1546.013`** PowerShell Profile (PrivEsc + Persistence) · **`T1546.007`** Netsh Helper DLL (PrivEsc + Persistence) · **`T1552.002`** Credentials in Registry (Credential Access) · **`T1070.003`** Clear Command History (Stealth) · **`T1136`** (Persistence) · **`T1098`** (Persistence + PrivEsc) · **`T1078`** (Initial Access, Persistence, PrivEsc, **Stealth**). ➕ **The room cites no ID for the `Userinit`/`Shell` modification; it is `T1547.004` Winlogon Helper DLL** (Persistence + PrivEsc). ⚠️ It also writes tactic IDs sloppily — `TA008` for TA0008, and a bare `1546`. 🟢🟢 **This is the corpus's best evidence that block K1 matters: a current, popular, free DFIR room is already teaching two dead IDs.** | [T1574.007](https://attack.mitre.org/techniques/T1574/007/) · [T1546.007](https://attack.mitre.org/techniques/T1546/007/) · [T1547.004](https://attack.mitre.org/techniques/T1547/004/) · [T1036.009](https://attack.mitre.org/techniques/T1036/009/) · block **K1** |
| 3 | the four PowerShell profile paths | 🔴 **The room lists the Windows PowerShell 5.1 tree only.** Microsoft's `about_Profiles` for **PowerShell 7** gives `$PSHOME\Profile.ps1` (AllUsersAllHosts), `$PSHOME\Microsoft.PowerShell_profile.ps1` (AllUsersCurrentHost), **`$HOME\Documents\PowerShell\Profile.ps1`** (CurrentUserAllHosts) and **`$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`** (CurrentUserCurrentHost), with CurrentUserCurrentHost highest precedence. **The 5.1 tree uses `Documents\WindowsPowerShell\` instead** — ⚠️ **NOT VERIFIED against Microsoft in this pass.** 🔴 **A live-response sweep must search both trees**, and a host with pwsh installed has eight candidate profiles, not four. | [MS `about_Profiles`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles) |
| 4 | the Sysinternals tooling | 🟢 **Autoruns v14.3 (17 Jun 2026)** — current, and the room's flags are correct: `b` *"Boot execute."*, `l` *"Logon startups (this is the default)."*, `-h` *"Show file hashes."* ⚠️ **PsLoggedOn is v1.35, page last updated March 2021, originally June 2016 — effectively frozen.** Still shipping and still works, but **do not present it as actively maintained.** 🔴 **Autoruns' VirusTotal integration is off by default and requires accepting the terms** (*"Before using VirusTotal features, you must accept the VirusTotal terms of service"*) — **and submitting a client's file hashes is a disclosure decision, not a step** (**N1**). | [Autoruns](https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns) · [PsLoggedOn](https://learn.microsoft.com/en-us/sysinternals/downloads/psloggedon) |
| 5 | `Get-WmiObject` in Task 8 | 🔴 **Removed in PowerShell 6/7** (**F5**, already verified). The room's process-listing command fails on any pwsh host. **Use `Get-CimInstance`.** ⚠️ The room uses `Get-CimInstance` everywhere else, so this is an inconsistency rather than a systematic error. | block **F5** |

### NOT VERIFIED

- **The Windows PowerShell 5.1 profile paths** against a Microsoft source (#3).
- **Whether `UseLogonCredential` is absent by default on Windows 10/11** specifically (#1).
- **Whether this room's VM is domain-joined** — the account descriptions imply a domain, and the
  room enumerates local accounts only (§2.4).

## 4. Evidence used

**One live Windows VM with a staged compromise, plus a supplied toolbox** at
`C:\Users\Administrator\Desktop\tools\` (`shells\` and `utils\`).

- **Downloadable?** ⚠️ **No.** **Reusable?** 🔴 **No.**
- **`ecdfp-evidence` action: none.** `EVS-10` remains unallocated — **eighth room running.**
- 🟢 **No credentials published**, and the room **redacts its own answers** throughout, so the
  walkthrough teaches the method without giving the answers away. **That is a better design than
  five of the six Honeynet rooms.**

### 🟢🟢 The toolbox is the finding

`tools\shells\` contains `CMD-DFIR.exe`, `PS-DFIR.exe` and a clean `PS-DFIR-Profile.ps1`;
`tools\utils\` contains `PsLoggedon64.exe`, `autorunsc64.exe` and helper scripts.

**This is the concrete form of `CLEAN-TOOLS` (D17)**, which our own design has as a snapshot with no
stated rationale beyond convenience. **The room supplies the rationale**: the analyst's shell is
itself attack surface, and the profile in §2.1 is the proof.

⚠️ **And it names the cost honestly** — *"you might come across missing features or receive error
messages while using this toolbox, since it is relying only on default environment variables. This is
expected."* 🟢 **A trusted toolchain is degraded by design**, and saying so up front is right.

**Two things our version adds:** the toolbox binaries are **hashed and the hashes published**, so a
student can verify their own tools before trusting them; and the toolbox lives on **read-only
media**, not on the subject's Desktop.

## 5. Lab design worth reusing

### 5.1 🟢🟢 The chicken-and-egg opening

§1. **Adopt for `S2-02` as the opening five minutes.** It reframes live response from *"run these
commands"* to *"establish that you can trust the thing running the commands"*, and it is the only
place in the corpus where that question is asked at all.

### 5.2 🟢🟢 A staged environment with one chain running through eight tasks

Mistyped admin → passwordless `Guest` session → `Userinit` → `cmd.exe` → `netsh.exe` → a helper DLL
in a temp path → a fake `aurora-agent` service → `ssh.exe` parented by it → `INITIAL_LANTERN.exe`
beside `Invoke-SocksProxy.psm1`. **Every task's finding is the next task's starting point**, and
Task 8 explicitly calls back to Task 5.

🟢 **Adopt the structure for the `S5-09` investigation row.** ⚠️ **And adopt the room's repeated
caveat with it** — *"not enough to jump to any conclusion without correlating with other artefacts
and knowing the system's baseline configuration"* — which appears three times and is the honest
counterweight to a chain that could otherwise read as a series of gotchas.

### 5.3 🟢 The outlier-in-a-list heuristic

The netsh DLL is found not because it is known-bad but because **its entry has a different shape from
every other entry in the same key** (a relative `.\` path). 🟢🟢 **That generalises well past netsh**
and is a cheap, teachable triage habit. ⚠️ **Pair it with the room's own honesty** that without the
pattern it *"can be a rabbit hole"* — the heuristic works because a baseline exists, not because the
analyst is clever.

### 5.4 🔴🔴 Safety and handling defects — one, and it is the most destructive in the corpus

**The room booby-traps the evidence machine and never states the consequence.**

If a student opens PowerShell before completing Task 2's steps, the staged profile runs:
`wevtutil el | ForEach-Object {wevtutil cl $_}; Stop-Service -Name "eventlog" -Force`.

**That clears *every* event log on the machine under investigation and stops the logging service.**

The room's only warning is operational, not evidential: *"if you haven't performed the previous steps
before executing PowerShell, please restart the VM."* ⚠️ **A restart does not restore cleared logs.**

**Why this is defect #11 and not merely a design quirk:**

1. **The destruction is triggered by the analyst's most natural first action** — opening PowerShell.
2. **The consequence is never stated.** A student who does it will not know what they lost, and the
   room's later tasks (§2.5, §2.6) depend on log-adjacent context.
3. 🔴 **The profile also sets `UseLogonCredential=1`** — so an unwary student **changes the security
   posture of the evidence machine** as well as destroying its logs. (⚠️ Per §3 #1, on a modern host
   that change is largely inert — **but it is still an unrequested modification of evidence.**)

🟢🟢 **And yet the staging is *pedagogically correct*** — this is exactly what a hostile host does,
and the room is right to build it. **The defect is the missing sentence, not the trap.**

**Our version:** the same trap, **with the consequence stated before the student touches anything** —
*"if you open PowerShell first, you will clear every event log on this host; that is the lesson, and
this is why we start with cmd"* — run on a **snapshot** that can be rolled back, and with the student
**recording the profile's hash and content before replacing it**, so the remediation is documented
rather than improvised. ⚠️ **The room's own remediation is a `ren`/`copy` with no hash and no
record** — it fixes the host and destroys the provenance of the fix.

**Running total: 11 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24, 29. Four endanger the
analyst's machine; **seven** endanger the evidence.** ⚠️ **This one breaks the L8 pattern:** the other
six evidence defects were *"act on the live system instead of collecting first"*; **this one is
"the evidence destroys itself when you touch it"**, which is a different and more interesting
category — and it is the only one in the corpus that is **deliberately staged**.

## 6. Question patterns

**25 scored questions across 9 tasks** — the largest set in the corpus, and a walkthrough rather than
a challenge, so the questions check comprehension of shown material rather than independent
investigation.

**🟢🟢 Three things it does better than the entire Priority-2 set:**

1. **It asks for SHA-256, not MD5** — four times. ✅ Correct per **K7**.
2. **It requires defanged answers** — *"Enter your answer in a defanged format"*, six times.
   ✅ Consistent with **H11**, and **the only room in the corpus to make defanging a graded habit.**
3. **It asks counting and identification questions rather than value-extraction ones** —
   *"What is the total number of suspicious accounts?"* is a judgement, not a lookup.

**⚠️ But one question is a `D41` violation** — *"What is the security identifier (SID) of the Guest
account?"* 🟢 **Borderline and defensible**: a SID is an identifier, not an authenticator, and the
Guest account's is well-known. **Recorded because the rule should be applied consistently, not
because this instance is harmful.**

**⚠️ Answer format is specified once** (*"MM/DD/YY HH:MM:SS XM"*) and **no timezone is given** —
despite Task 3 teaching the student to record the timezone. 🔴 **The room teaches the discipline and
then does not apply it to its own questions.**

**🔴 Twenty-ninth room, no "cannot be determined" question.** The walkthrough format makes this
harder to fault — but the room's *own text* supplies the material for several:

| the room could have asked | correct answer |
|---|---|
| *"The `aurora-agent` service is set to Auto and is not running. Did the adversary disable it?"* | ⚠️ **Not established** — the room says so itself: *"it could be just an agent failure case."* 🟢 **The resolution is the binary, not the state.** |
| *"All three firewall profiles are disabled. Is that an attacker action?"* | ⚠️ **Not established** — *"during some legitimate uses, like using alternative security layers, this is a normal configuration."* |
| *"`Guest` has `PasswordRequired = False`. Is that a compromise indicator?"* | 🔴 **No — that is the Windows default for `Guest`.** The finding is that it is **enabled and logged on.** |
| *"`UseLogonCredential=1` is set. Were cleartext credentials captured?"* | 🔴🔴 **Not on a modern host.** Credential Guard blocks WDigest SSO and is on by default from Win11 22H2 / Server 2025; Microsoft: plaintext is not stored *"even when `UseLogonCredential` is set to `1`."* **The registry value proves intent, not success.** |
| *"`ssh.exe` is parented by `aurora-agent`. Did that process spawn it?"* | ⚠️ **Not established from PPID alone** — parent spoofing (**T1134.004**) and PID reuse (**M4**). **And the room's own Task 8 cites `T1036.009` Break Process Trees**, i.e. the technique that defeats its method. |
| *"A volume has no drive letter. Is it hidden by the attacker?"* | 🔴 **Not necessarily** — recovery and EFI system partitions are unlettered by design. |
| *"No PowerShell profile exists on a second host. Is it clean?"* | ⚠️ **Not established** — the room checks **four 5.1 paths**; a host with pwsh has **eight**, in a different tree (§3 #3). |

🟢🟢 **Seven, and three come from sentences the room itself wrote.** ⚠️ **That is the pattern's final
form: the room states the uncertainty in its prose and then asks a question that does not admit
it.** **The gap is not knowledge — it is the answer box.**

## 7. Figures

**Not enumerated.** ⚠️ The room references screenshots in-line (*"the ones highlighted in the
screenshot above"*, the RSoP report interface), so **it does have figures** — but the DOM query was
not run and none was viewed. **Recorded as not-checked, not as absent.** 🟢 **First room in nine
where the honest answer is "it has some and I did not look"** rather than "it has none."

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F35 | **The chicken-and-egg** | Two panels. Left: analyst opens PowerShell → profile fires → event logs cleared, service stopped, WDigest flipped. Right: analyst opens the trusted `cmd.exe` → reads the profile → replaces it → *then* opens PowerShell. Caption: **"your shell is attack surface."** | **🔴 P1** | §2.1 and §5.4 — the `S2-02` opening, and the missing rationale for **D17**. |
| F36 | **One chain, eight artifact stores** | The room's chain drawn once — mistyped admin → Guest session → `Userinit` → `cmd.exe` → `netsh.exe` → helper DLL → fake service → `ssh.exe` → the temp folder — with each hop labelled by **which store answered it** (registry, service DB, process list, filesystem). | **🔴 P1** | §5.2 — correlation as a picture, and it doubles as the `S5-09` case map. |
| F37 | **The outlier in the list** | The `HKLM\SOFTWARE\Microsoft\NetSh` key rendered as a list of `name : dll` pairs, all bare filenames, **one with a `.\` relative path highlighted.** | **🟢 P2** | §5.3 — the cheapest triage habit in the room. |

## 8. Fit against our material

### ⚠️ Part 1 lists this as Priority 3, *"skim, context only"* — that was wrong, and it is worth saying.

**This is the best `S2-02` source in the corpus** and the only room that supplies a rationale for
`CLEAN-TOOLS` (**D17**). ⚠️ **The Priority-3 classification was made from a room title.** 🟢 **Amend
the Part 1 row**, and note the general lesson: **the priority list was a pre-extraction guess and
should be treated as one.**

### Rows this strengthens

- **`S2-02`** (*"Live response — volatile data collection on a running host"*, 25 min) — 🟢🟢 **gains
  its opening argument (§5.1), figure F35, and the whole trusted-toolchain rationale.** This row
  currently has a method and no *why*; the room supplies it.
- **`S1-05`** (*"Analyst toolkit install and the `CLEAN-TOOLS` snapshot"*) — 🟢🟢 **the same
  rationale, one session earlier.** ➕ **Two additions of ours: publish the toolbox hashes, and put
  it on read-only media** (§4).
- **`S5-01`/`S5-02`** — the environment-variable and `Userinit`/`Shell`/`NetSh` registry chain
  (§2.2, §2.6), with **`T1547.004`** and **`T1546.007`**, neither of which the room cites correctly.
- **`S5-05`/`S5-06`** — services and scheduled tasks (§2.7), and **the *original filename* field as
  the cheapest unmasking of a renamed binary.**
- **`S6-06`** — 🔴 **the room's `T1070.001` and `T1562.002` citations are the worked example of why
  block K1 matters.** Use it as the slide: *this is a current, popular room, already wrong.*
- **`S2-01`** — §5.4's defect is the most vivid order-of-volatility argument available: **the
  evidence destroys itself when you touch it.**

### Back-propagation

🟢 **None.** ✅ Checked: `T1112`, `T1546.007`, `T1546.013`, `T1547.004`, `T1552.002`, `T1574.007`,
`T1036.009`, `T1136`, `T1098` appear nowhere in the repo — all forward-looking. ✅ `T1078.002` is in
`elevatingmovement.md` and already correct.

### Minutes

**Net zero in rows.** Content into `S2-02`, `S1-05`, `S5-01`, `S5-02`, `S5-05`, `S5-06`, `S6-06`,
`S2-01`. **No new rows.**

⚠️ **`S2-02` is 25 minutes and gains a five-minute opening.** That is the first genuine *addition*
outside S5 in several rooms, and it should be absorbed by trimming the row's existing command drill,
not stacked on top. 🔴 **Row-overload list, unchanged and still outstanding: `S5-06`, `S5-08`,
`S6-06`, `S4-07` — plus `S2-02` now on watch.**

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-fourth room carrying the S5 overdraft.**

### Out of scope

Nothing material — this room is Windows live response, which is `S2-02`'s subject. ⚠️ One item sits
on the line: **the remediation step** (replacing the malicious profile). **We are a forensics course,
not an IR course** — but §5.4's point stands that **the remediation must be documented**, and that is
one sentence in `S1-07` (chain of custody), not a topic.

### Still unresolved

- **S5 re-split** — twenty-fourth room; four-row overload list, `S2-02` now on watch.
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- **FTK Imager in `CLEAN-TOOLS`** (room 27) · **Volatility symbol pre-population** (**D2**) ·
  🆕 **toolbox hashes published and toolbox on read-only media** (§4) — three open `CLEAN-TOOLS`
  items now.
- **D19 has no per-session host map** — still gating **F7** and **D40**.
- **`ecdfp-case` skill** not installed; **no room note through `ecdfp-intake`.**

## 9. Links

**Room** — <https://tryhackme.com/room/winincidentsurface>
**Companion notes** — `elevatingmovement.md` and `crmsnatch.md` (the Windows artifact base) ·
`lostinramslation.md` (**M1**, the PEB caveat that applies to this room's `CommandLine` field) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **F5**, **G5**, **K1**, **M4**, **N1**, and new block **Q**.

**Citations from §3, by finding:**

- #1 WDigest — MS, KB2871997 and WDigest
  <https://learn.microsoft.com/en-us/archive/blogs/kfalde/kb2871997-and-wdigest-part-1> ·
  Credential Guard considerations
  <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/considerations-known-issues> ·
  Credential Guard configure
  <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/configure> ·
  MS Q&A, WDigest on Windows 11
  <https://learn.microsoft.com/en-us/answers/questions/5869399/enable-wdigest-dont-work-on-windows-11> ·
  T1112 <https://attack.mitre.org/techniques/T1112/>
- #2 ATT&CK — T1574.007 <https://attack.mitre.org/techniques/T1574/007/> ·
  T1546.007 <https://attack.mitre.org/techniques/T1546/007/> ·
  T1546.013 <https://attack.mitre.org/techniques/T1546/013/> ·
  T1547.004 <https://attack.mitre.org/techniques/T1547/004/> ·
  T1036.009 <https://attack.mitre.org/techniques/T1036/009/> ·
  T1552.002 <https://attack.mitre.org/techniques/T1552/002/> · block **K1**
- #3 profile paths — MS `about_Profiles`
  <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles>
- #4 Sysinternals — Autoruns <https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns> ·
  PsLoggedOn <https://learn.microsoft.com/en-us/sysinternals/downloads/psloggedon>
- #5 `Get-WmiObject` — block **F5**
