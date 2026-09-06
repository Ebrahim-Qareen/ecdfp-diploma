---
room: Logless Hunt
url: https://tryhackme.com/room/loglesshunt
module: Windows Endpoint Investigation — **challenge/guided hybrid** (Priority 2)
feeds: **S5** (`S5-08` event logs beyond Security) and **S6** (`S6-01` log sources, `S6-07` timeline).
       Also **S1** — 🟢🟢 **its scenario states the D7 error out loud and is the best opening for
       the whole diploma.**
       🔴 Carries **five** corrections our material must make before it ships.
difficulty / time: Medium · 90 min · 8 tasks · Premium · 4,496 completions · 109 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
              🔴 Room ships plaintext RDP credentials in Task 2 — **deliberately not reproduced
              here (R8)**.
              Room self-describes as a hybrid: *"includes both guided walkthroughs along with
              independent challenges"* — so unlike Diskrupt it carries real teaching content.
---

## 1. What the room teaches

**That "the Security log is empty" is not a finding.** The customer's CTO says it in the scenario,
and the sentence is the whole course in miniature:

> *"They reviewed the Security and System logs on all our Windows servers and concluded, **'All
> event logs are empty, so hackers did not breach the servers.'** But guess what? A few days later,
> our website started showing some crypto scam ads and some servers were running at 100% CPU load!"*

🟢🟢 **That is D7 stated by a character, with the consequence attached, in a scenario a student
reads before touching anything.** It is the best single paragraph we have found in nineteen rooms
and **`S1` should open with it.**

The room then walks five log sources the threat actor did **not** clear, in attack order: **web
access logs** (initial access) → **PowerShell logs** (execution) → **RDP session logs** (lateral
movement) → **Task Scheduler logs** (persistence) → **Windows Defender logs** (credential access).
One attack chain, five channels, and a working answer to *"what do I look at when 4624 is gone?"*

**🟢🟢 And Task 4 contains the best artifact-comparison teaching in the entire path.** Three
PowerShell log sources, and rather than describing the differences it **demonstrates** them with
three test commands and a table of which source caught which:

| what was run | ConsoleHost_history | 600 | 4104 |
|---|---|---|---|
| `Write-Output 'TEST1'` typed interactively | ✅ | ✗ | ✅ |
| `powershell -c "Write-Output 'TEST2'"` from cmd | ✗ | ✅ | ✅ |
| `powershell ./loglesshunt.ps1` (script content) | ✗ | ✗ | ✅ |

**Three sources, three coverage profiles, one runnable demonstration.** Copy this design wholesale
— it is exactly how our 6-box "what it does NOT prove" should be *shown* rather than asserted.

**🔴 But five things in it are wrong or incomplete**, and every one is the kind of error that makes
a student miss evidence: script block logging has **three** states not two (§2.4); **PowerShell 7
logs somewhere else entirely** (§2.4); **event 5013 is not exclusion creation** (§2.7); **IIS logs
User-Agent and Referer by default** (§2.1); and the room never names the reason its own web log
could not answer its own webshell question (§2.1). All in §3.

## 2. Artifacts — one 6-box block each

### 2.1 Web access logs (IIS / Apache)

- **What it is** — one line per HTTP request, written by the web server itself.
- **Where it lives** — **IIS: `%SystemDrive%\inetpub\logs\LogFiles\W3SVC<n>\`** (root confirmed by
  Microsoft; the `W3SVC<n>` subfolder is convention — read the site ID from IIS Manager).
  **Apache on Windows: `<ServerRoot>\logs\`**, and `C:\Apache24` **is** the Apache project's own
  documented default ServerRoot — the room is right. ⚠️ **Resolve `ServerRoot` from `httpd.conf`
  rather than assuming**: *"The filename for the access log is relative to the `ServerRoot` unless
  it begins with a slash."*
- **What it proves** — source IP · timestamp · method · URI · status · bytes. In this scenario
  that is enough to see a scan (many 404s from one IP), the upload (a `POST` that returns 200), and
  the webshell's path.
- **What it does NOT prove** — 🔴🔴 **what was actually sent or executed, because there is no
  request body in either format.** IIS's default field set has no body field; Apache's `combined`
  has none. **Every credential, every webshell command and every SQLi payload delivered by POST is
  absent.** 🟢 **The room demonstrates this and never says it**: Task 3 finds the uploaded
  backdoor in the web log, and Task 4 has to go to **PowerShell logs** to find out what the
  attacker typed into it — *because the web log could not tell you.* **Name that. It is the best
  "what this artifact cannot do" moment in the room and it is sitting there unlabelled.**
  ⚠️ Also absent: response bodies, and almost all request headers (no `Authorization`, no
  `X-Forwarded-For`, no custom headers).
- **How to parse it** — `Get-Content …\access.log`; for real work import to the **analyst's**
  machine. 🔴 **Read the `#Fields:` header line first** and never assume the field set (§3 #7).
- **Anti-forensics / false-positive caveat** — 🟢 **IIS rotation does not delete** — it opens a new
  file daily or at `truncateSize` and keeps the old ones; Microsoft ships no cleanup, so
  *"running a script … in a scheduled task"* is the documented approach. **That inverts the threat:
  the deletion mechanism is an administrator's own scheduled task — which §2.6 says an attacker can
  create or modify.** 🟢 **Check for a scheduled task that deletes web logs.** ⚠️ And absent logs
  are as often misconfiguration as anti-forensics — *"many users turn off logging completely"* to
  control disk usage.

### 2.2 `ConsoleHost_history.txt` — the PowerShell history file

- **What it is** — PSReadLine's line-editor history, the direct analogue of `~/.bash_history`.
- **Where it lives** — `$Env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\$($Host.Name)_history.txt`.
  ⚠️ **Per-user *and* per-host.** `$Host.Name` is `ConsoleHost` for the normal console — hence the
  familiar filename — but **a VS Code session writes `Visual Studio Code Host_history.txt`** and ISE
  writes elsewhere again. **Enumerate the whole PSReadLine directory, not one filename.**
  🟢 **PowerShell 7 shares the same file** (`$Host.Name` is `ConsoleHost` for pwsh too), which is
  the one place pwsh does *not* evade (contrast §2.4).
- **What it proves** — commands **typed interactively**. Enabled by default from PowerShell 5.x /
  Windows 10 on. 🟢 **And it is written incrementally, not at exit** — the default
  `HistorySaveStyle` is `SaveIncrementally`: *"Save history after each command is executed and share
  across multiple instances."* **A killed or crashed attacker session still leaves its history**,
  which is the opposite of the bash behaviour room 15 warned us about (`history` writes at exit).
  **Say that out loud; students assume the two behave the same.**
- **What it does NOT prove** — 🔴🔴 **it is lossy by design, in three ways.**
  1. **Non-interactive commands are absent.** `powershell -c "…"`, `-EncodedCommand`, and anything
     a webshell runs windowlessly leave nothing here — which is exactly the room's TEST2 case.
     ⚠️ Microsoft never states this exclusion in so many words; **demonstrate it in lab rather than
     citing it.**
  2. **PowerShell itself censors it.** Command lines containing `password`, `asplaintext`, `token`,
     `apikey` or `secret` are **not written to the file at all**. **The most interesting command an
     attacker types is the one most likely to be missing.**
  3. **`-AddToHistoryHandler` lets an attacker suppress arbitrary commands** with one line.
  ⚠️ `MaximumHistoryCount` defaults to **4096**; overflow behaviour is undocumented — **do not
  teach a specific truncation mechanism.**
- **How to parse it** — it is a plain text file; read it, and check the file's own mtime against the
  session timeline. **Collect the whole PSReadLine folder.**
- **Anti-forensics / false-positive caveat** — 🔴 **it is a user-writable text file in the user's
  own profile.** Deleting or editing it needs no privilege at all. **Absence proves nothing; and
  unlike an event log, tampering leaves no gap in a sequence number.**

### 2.3 The classic `Windows PowerShell` channel — 400 / 403 / 600 / 800

- **What it is** — PowerShell's original, always-on logging: engine and provider lifecycle.
- **Where it lives** — Event Viewer → **Applications and Services Logs → Windows PowerShell**.
- **What it proves** — 🟢🟢 **the full command line, including `-EncodedCommand`, with zero
  configuration.** The `HostApplication` field records *"the binary path at the origin of the
  powershell activity and … the commandline arguments provided to powershell.exe."*
  **400** EngineStart · **403** EngineStop · **600** provider start/stop (the room's ID) ·
  **800** Pipeline Execution Details. ⚠️ **The room names only 600. `400` carries the same
  `HostApplication` field and fires on every PowerShell start** — teach the pair.
  🟢 **600 with `ProviderName = WSMan` indicates PowerShell remoting** — a free lateral-movement
  indicator the room does not mention.
- **What it does NOT prove** — 🔴 **what happened inside the session.** The room states this well:
  *"it logs only the creation of the PowerShell console but won't show any other commands launched
  within the same PowerShell session."* One 600 covers an entire interactive session of any length.
  ⚠️ **800 is documented as inconsistently logged** — do not build a timeline on it.
- **How to parse it** — filter the `Windows PowerShell` channel for 400/600 and read
  `HostApplication`. ⚠️ **This is where a base64 `-enc` blob shows up even with 4104 off** — decode
  it and you have the payload without any policy having been enabled.
- **Anti-forensics / false-positive caveat** — 🟢 **this is the highest-value default-on PowerShell
  artifact and the room undersells it.** Against a host where nobody enabled script block logging,
  **400/600 plus the history file is the entire PowerShell picture** — and between them they cover
  both of the room's first two test cases.

### 2.4 Script block logging — event 4104

- **What it is** — the full, **de-obfuscated** text of every script block PowerShell compiles.
- **Where it lives** — `Microsoft-Windows-PowerShell/Operational`. 🔴🔴 **For PowerShell 7 it is a
  different channel entirely: `PowerShellCore/Operational`** — see the caveat.
- **What it proves** — everything the other two sources miss, including script file contents and
  base64-decoded commands. The room is right that this is where 4104 *"shines"*.
- **What it does NOT prove** — 🔴🔴 **the room says "disabled by default" and that is only
  two-thirds true. There are THREE states:**

  | policy state | what happens |
  |---|---|
  | **Not Configured** (the default) | **automatic script block logging is ACTIVE** — PowerShell *"automatically logs script blocks when they have content often used by malicious scripts… a record of last resort"* |
  | **Enabled** | everything logged, at level **Verbose** |
  | **explicitly Disabled** / `EnableScriptBlockLogging = 0` | 🔴 **even the record of last resort is gone** — Microsoft: *"To disable automatic script block logging, set the … feature to 'Disabled'. Alternatively, specify '0' for the EnableScriptBlockLogging registry key."* |

  🟢🟢 **So an empty Operational channel does not mean "logging was off". It may mean someone turned
  it off.** `EnableScriptBlockLogging = 0` under
  `HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging` **is a defence-evasion
  IOC, and hunting for the value `0` rather than its absence is the lesson.**
  ⚠️ Level tells you which mechanism produced the event: **Verbose = policy-driven full logging,
  Warning = the automatic suspicious-content subset.** (The Warning level is DFIR-sourced, not
  Microsoft-documented — cite it as such.)
- **How to parse it** — filter `…/Operational` for 4104 and read `ScriptBlockText`.
  ⚠️ **4103 is a different thing** — module/pipeline logging, requiring its own policy.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **PowerShell 7 evades a Windows PowerShell
  policy completely.** pwsh logs to **`PowerShellCore/Operational`** and reads its policy from
  **`HKLM\Software\Policies\Microsoft\PowerShellCore\ScriptBlockLogging`** — *a different key*.
  **An organisation that enabled script block logging through the Windows PowerShell GPO has zero
  coverage of pwsh 7.** ⚠️ And the PowerShell 7 provider must have been registered
  (`$PSHOME\RegisterManifest.ps1`) or **the channel may not exist on the host at all.**
  **The room never mentions PowerShell 7. Ours must** — it is the single most likely way a modern
  attacker defeats everything this task teaches.
  ➕ **A fourth source the room omits: transcription.** `Start-Transcript` / the transcription
  policy captures **command output**, which 4104 does not — 4104 gives you the decoded code,
  transcripts give you what it printed. Off by default; writes to the user's Documents folder by
  default, **or to a central share**, which puts it out of the attacker's reach.

### 2.5 RDP session logs — TerminalServices-LocalSessionManager

- **What it is** — the RDP session lifecycle, in a low-noise channel that has nothing to do with
  the Security log.
- **Where it lives** — `Microsoft-Windows-TerminalServices-LocalSessionManager/Operational`
  (`…\winevt\Logs\Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx`).
  **Enabled by default.**
- **What it proves** — **21** logon succeeded · **22** shell start (*proves an interactive desktop,
  not just a session*) · **23** logoff · **24** disconnected · **25** reconnection succeeded ·
  **39/40** disconnect with reason code. Fields: **User**, **Session ID**, **Source Network
  Address**. 🟢 **Session ID is the join key** — chain 21 → 22 → 24 → 25 → 23 into one timeline.
  The room's four questions are exactly this chain.
- **What it does NOT prove** — 🔴 **that a login attempt failed, because failures are not in this
  channel at all.** The room says *"only successful RDP logins are logged"* and is correct.
  **Failures are Security 4625** — so on a host with the Security log cleared, **you have no failure
  evidence at all**, which is worth stating rather than leaving implied. ⚠️ It also does not prove
  *what the user did* once connected.
- **How to parse it** — filter for 21/24/25 and read Source Network Address.
  🔴 **Filter out `LOCAL` first.** The room correctly notes the value exists (*"indicates local
  login and can occur during system startup and usage of hypervisor utilities"*) — ⚠️ **but does not
  say that failing to exclude it makes students over-count RDP logons, which is the single most
  common error with this artifact.**
- **Anti-forensics / false-positive caveat** — ⚠️ **know the order.**
  **RemoteConnectionManager 1149** fires **before** 21, and it does **not** mean credentials were
  accepted: *"This does NOT indicate successful credential authentication. It signifies successful
  network-level connection establishment — a client launched RDP and reached the login prompt before
  entering any credentials."* 🟢 **The correct chain is `1149` (reached the prompt) → `4624 type 10`
  (credentials accepted) → `21` (session logon) → `22` (desktop up), and 1149 without a matching 21
  is scanning or failed credentials.** ⚠️ The 1149 semantics are **NLA-dependent** and sources
  disagree — teach the distinction, not an absolute.

### 2.6 Scheduled tasks — logs, XML, and the registry

- **What it is** — persistence, and the three independent places it leaves traces.
- **Where it lives** — **(a)** `Microsoft-Windows-TaskScheduler/Operational`; **(b)** the task XML
  at `C:\Windows\System32\Tasks`; **(c)** the registry at
  `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\{Tree,Tasks}`.
  🟢 **The room's correlation list is right and worth copying**: logs for the activity, XML for the
  creation time and content, the GUI as an alternative, and process-creation logs for context.
- **What it proves** — **106** task registered (**and it names the registering user** — the
  attribution field) · **100** started · **129** created task process (**and it gives the PID** —
  the pivot into process telemetry) · **102** completed · **140** updated · **141** deleted ·
  **200/201** action started/completed (**names the executable actually launched, with its return
  code**) · **110/118/119** triggered by user/boot/logon. 🟢 **The triage pair is 106 (who
  registered it) + 200 or 129 (what it actually ran).**
  ➕ **Security 4698** carries the **complete task XML**, and on Windows 10 1903+ also the
  **parent process of the creation** — but it is in the Security log, which this scenario has lost.
- **What it does NOT prove** — 🔴 **that the channel was ever recording.** The room says
  TaskScheduler/Operational is *"disabled by default"* and *"it is common to see it enabled, as IT
  administrators often use it to debug their scheduled tasks"* — ⚠️ **that matches two independent
  technical sources, but Microsoft never states the default anywhere.** Say so. **On a typical
  unmanaged endpoint your scheduled-task evidence is the registry TaskCache plus the XML, not this
  channel** — teach that ordering, because the room's does not.
- **How to parse it** — enable/verify with
  `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true`; the GUI's *"Enable All Tasks
  History"* button is the same switch. Read the XML for author, creation date, triggers, actions and
  RunAs principal.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **hidden scheduled tasks, and the mechanism is
  elegant enough to teach on its own.** Deleting the **`SD` (Security Descriptor)** value under
  `…\TaskCache\Tree\<task>` makes the task **vanish from `schtasks /query`, Autoruns and Task
  Scheduler while continuing to run** — Microsoft's own Tarrask analysis: *"removal of this value
  results in the task 'disappearing' from 'schtasks /query' and Task Scheduler."* It needs
  **SYSTEM** (Tarrask stole a token from `lsass.exe` to get it).
  🟢 **The mechanism is the lesson: the task is not obfuscated, it is made unreadable — and the
  enumerating tools fail OPEN, silently omitting it rather than erroring.** ⚠️ **Detection is a
  cross-check, not a scan**: compare `TaskCache\Tree` subkeys against the XML files in
  `System32\Tasks` — a Tree entry with no XML, or a missing/null `SD`, is the IOC. (`Tree` values
  also store **a hash of the XML**, giving a second integrity check.)
  **This is our best anti-forensics artifact for S5 and the room does not mention it.**

### 2.7 Windows Defender operational logs

- **What it is** — every detection, remediation and configuration change the AV engine makes.
- **Where it lives** — `Microsoft-Windows-Windows Defender/Operational`. **Enabled by default.**
- **What it proves** — 🟢 **when the attacker is careless, this channel narrates the intrusion.**
  **1116** malware detected · **1117** action taken. Fields: **Name** (threat family), `Severity`,
  `Category`, **Path**, **Detection Origin**, `Detection Type`, **Detection Source**, **User**,
  **Process Name**, and on 1117 the **Action**.
  🟢 **Two fields the room does not call out and should:** `Detection Source: AMSI` is the bridge
  straight back to §2.4 (*"primarily used to protect scripts (PowerShell, VBS)"*), and
  **`Action: Allow` on a 1117 is the highest-value single field in the channel** — it means someone
  overrode the detection. ⚠️ **A 1116 with no matching 1117 = detected but not remediated.**
- **What it does NOT prove** — 🔴 **the room's ID list is wrong on one entry.** It says *"5007 and
  5013 upon modification of its settings or exclusion creation."* **5007 is correct**
  (`MALWAREPROTECTION_CONFIG_CHANGED`, carrying *"Old value"* / *"New value"*). **5013 is NOT
  exclusion creation — it is Tamper Protection blocking a change**: *"If Tamper protection is
  enabled then any attempt to change any of Defender's settings is blocked. Event ID 5013 is
  generated and states which setting change was blocked."*
  🟢 **Which makes 5013 more useful than the room thinks**: a burst of 5013 is an attacker
  **actively trying and failing** to weaken Defender.
  ➕ **And 5001 is not the whole disable story**: add **5004** (real-time protection configuration
  changed), **5010** (antispyware disabled) and **5012** (antivirus disabled).
- **How to parse it** — filter the channel for 1116/1117/5001/5004/5007/5010/5012/5013.
  For **exclusions**, check **both** registry keys —
  `HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions` (local) **and**
  `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions` (GPO) — with subkeys
  **Paths, Extensions, Processes, IpAddresses**. 🟢 **One-liner worth teaching:**
  `MpCmdRun.exe -CheckExclusion -Path <path>`.
- **Anti-forensics / false-positive caveat** — ⚠️ **the `file:_` / `webfile:_` path prefixes the
  room's field list implies are real in the wild but are NOT documented by Microsoft** — demonstrate
  them from a lab EICAR detection rather than putting them on a slide as fact.
  🔴 And exclusion creation surfacing as a 5007 is **inferred, not proven** — no published sample
  shows a 5007 naming an `Exclusions\Paths` value. **Generate one in lab with
  `Add-MpPreference -ExclusionPath` and capture it before teaching it.**

### 2.8 Defender DetectionHistory — the second, independent store

- **What it is** — the detection database behind the **Windows Security GUI**, entirely separate
  from the event log.
- **Where it lives** — `%ProgramData%\Microsoft\Windows Defender\Scans\History\Service\
  DetectionHistory\<numbered folder>\`.
- **What it proves** — 🟢🟢 **more than the event log does.** Threat names, file locations,
  timestamps, **SHA-256 and MD5 hashes**, **the spawning process**, **the user who created the
  file**, and threat-status IDs recording the **user's response** (quarantine / allow / remove).
  **`SpawningProcessName` plus the creating user is richer than anything in a 1116.**
- **What it does NOT prove** — ⚠️ it is a binary format, undocumented, and needs a parser.
  🔴 And it is **just as deletable as the event log** — the room is right that an attacker must
  clear both, and right that most only clear one.
- **How to parse it** — **DHParser** (`jklepsercyber/defender-detectionhistory-parser`, the tool
  from the SANS post the room links), or the Velociraptor artifacts
  `Windows.Applications.DefenderDHParser` / `Windows.Applications.DefenderHistory`. JSON output.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **this is the room's best structural idea and it
  states it explicitly:** *"the mentioned Windows Defender event logs and threat detection history
  you see in the graphical interface do not depend on each other. To remove detection traces, threat
  actors have to both delete the event logs and delete 'database' entries."*
  **Two independent stores of the same facts means you can diff them, and a detection present in one
  and missing from the other is direct evidence of selective tampering.** ⚠️ Note the dependency
  runs one way for the UI: *"If this DetectionHistory file … is deleted, the Windows Security blurb
  disappears along with it"* — **the GUI reads DetectionHistory, not the event log.**

## 3. Tools and commands

The room uses **Event Viewer** throughout and names almost no tooling — appropriate for a room whose
premise is *"investigate with built-in tools"*. Paths and channels are the content:

| artifact | location | default state |
|---|---|---|
| IIS access logs | `%SystemDrive%\inetpub\logs\LogFiles\W3SVC<n>\` | **on** |
| Apache access logs | `<ServerRoot>\logs\` (default ServerRoot `\Apache24`) | on, format `common` |
| PowerShell history | `$Env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\$($Host.Name)_history.txt` | **on** |
| PowerShell classic | Applications and Services Logs → **Windows PowerShell** (400/403/600/800) | **on** |
| PowerShell 5.1 script blocks | `Microsoft-Windows-PowerShell/Operational` (4104) | **three states — §2.4** |
| **PowerShell 7 script blocks** | 🔴 **`PowerShellCore/Operational`** | separate policy key |
| PowerShell transcripts | user's Documents, or a central share | off |
| RDP sessions | `…TerminalServices-LocalSessionManager/Operational` (21/22/23/24/25/39/40) | **on** |
| RDP connection attempts | `…TerminalServices-RemoteConnectionManager/Operational` (1149) | on |
| Scheduled tasks | `Microsoft-Windows-TaskScheduler/Operational` (106/100/129/…) | ⚠️ **off** |
| Task definitions | `C:\Windows\System32\Tasks` (XML) | n/a |
| Task registry | `HKLM\…\Schedule\TaskCache\{Tree,Tasks}` | n/a |
| Defender events | `Microsoft-Windows-Windows Defender/Operational` (1116/1117/5001/5004/5007/5010/5012/5013) | **on** |
| Defender detections | `%ProgramData%\Microsoft\Windows Defender\Scans\History\Service\DetectionHistory\` | **on** |
| Defender exclusions | `HKLM\SOFTWARE\{,Policies\}Microsoft\Windows Defender\Exclusions` | n/a |

Commands worth adding to our version:

```
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true    # enable task history
auditpol /get /subcategory:"Other Object Access Events"            # is 4698 on? check, don't assume
MpCmdRun.exe -CheckExclusion -Path <path>                          # is this path excluded?
reg query "HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"   # hunt for value 0
```

### CURRENCY CHECK — verified 2026-08-29

| # | item | result |
|---|---|---|
| 1 | 🔴🔴 **"ScriptBlock Logging… disabled by default" is two-thirds of the story** | **Three states, not two.** *Not Configured* leaves **automatic script block logging active** — Microsoft: *"PowerShell automatically logs script blocks when they have content often used by malicious scripts… a record of last resort."* *Enabled* logs everything at **Verbose**. **Explicitly *Disabled* (or `EnableScriptBlockLogging = 0`) kills the automatic subset too** — Microsoft states this as the documented way to switch it off. 🟢 **So hunt for the value `0`, not for the key's absence — a `0` is a defence-evasion IOC.** ⚠️ Level distinguishes the mechanism: **Verbose = policy, Warning = automatic** (Warning level is DFIR-sourced, not Microsoft-documented). |
| 2 | 🔴🔴 **PowerShell 7 logs to a different channel and reads a different policy key** | pwsh writes to **`PowerShellCore/Operational`**, policy at `HKLM\Software\Policies\Microsoft\**PowerShellCore**\ScriptBlockLogging`. **An organisation that enabled script block logging via the Windows PowerShell GPO has ZERO coverage of pwsh 7.** ⚠️ The provider must also have been registered (`$PSHOME\RegisterManifest.ps1`) or the channel may not exist. 🟢 **But pwsh shares `ConsoleHost_history.txt` with 5.1** — one place it does not evade. **The room never mentions PowerShell 7.** |
| 3 | 🔴 **event 5013 is Tamper Protection, not exclusion creation** | The room says *"5007 and 5013 upon modification of its settings or exclusion creation."* **5007 is right; 5013 is `MALWAREPROTECTION_SCAN_CANCELLED` by symbolic name but Microsoft's message is Tamper Protection blocking a change.** 🟢 Which makes it *more* useful: **a burst of 5013 is an attacker actively failing to weaken Defender.** ➕ Add **5004**, **5010**, **5012** — 5001 alone does not cover a full AV disable. |
| 4 | 🔴 **IIS logs User-Agent, Referer and username BY DEFAULT** | Default `logExtFileFlags`: `Date, Time, ClientIP, UserName, ServerIP, Method, UriStem, UriQuery, TimeTaken, HttpStatus, Win32Status, ServerPort, **UserAgent**, HttpSubStatus, **Referer**`. Genuinely **off**: `BytesRecv`, `BytesSent`, **`Cookie`**, **`Host`**, `ProtocolVersion`, `SiteName`, `ComputerName`. ⚠️ **Time-sensitive:** *"Starting with the February 2026 Windows Update, `BytesRecv` and `BytesSent` are included by default … on Windows 11 and Windows Server 2019 and later."* **Current as of now, absent on any unpatched or older host** — teach reading the `#Fields:` line, never assuming. 🟢 **Highest-value missing field is `Host`** (no per-tenant attribution on a shared server); second is `Cookie` (session hijacking invisible). |
| 5 | ✅ **`C:\Apache24` is genuinely Apache's own default** | *"The default configuration of the source distribution expects the server to be installed into `\Apache24`."* The room is right. ⚠️ **But the ASF ships no Windows binary** — third-party builds (Apache Lounge, WampServer) may sit at `C:\Program Files\Apache Software Foundation\Apache2.4\`. **Resolve `ServerRoot` from `httpd.conf`.** ⚠️ **Apache's shipped `CustomLog` uses `common`, which has NO User-Agent and NO Referer** — so a default Apache logs *less* than a default IIS. Good compare-and-contrast slide. |
| 6 | ⚠️ **TaskScheduler/Operational default: the room is right, Microsoft never says so** | Confirmed *"not enabled by default"* by NXLog, and *"present but logging disabled by default on many builds"* by Forenza. **No Microsoft statement exists.** Say that in class. 🟢 **The GUI's "Enable All Tasks History" and the channel's Enable Log are the same switch.** **Consequence for our ordering: on an unmanaged endpoint the primary task evidence is the registry TaskCache plus the XML, not this channel.** |
| 7 | 🔴🔴 **hidden scheduled tasks via `SD` deletion** — the room omits it entirely | Microsoft (Tarrask): *"removal of this value results in the task 'disappearing' from `schtasks /query` and Task Scheduler."* Requires **SYSTEM** (Tarrask stole a token from `lsass.exe`). Binary Defense: *"the SD value defines the Security Descriptor… common scheduled task auditing tools such as `schtasks.exe`, Autoruns, and Task Scheduler are unable to read the details of the task due to a lack of permissions"* — **and the task still executes.** 🟢 **Detection is a cross-check**: `TaskCache\Tree` subkeys vs the XML in `System32\Tasks`; `Tree` also stores a **hash of the XML**. Tooling: `HiddenTaskHunter`. **Our best S5 anti-forensics artifact.** |
| 8 | ✅ **PSReadLine history is written incrementally, not at exit** | Default `HistorySaveStyle` is **`SaveIncrementally`** — *"Save history after each command is executed."* 🟢 **A killed attacker session still leaves history** — the opposite of bash (room 15, block E9). ⚠️ **Per-host filename** `$($Host.Name)_history.txt` — VS Code and ISE write elsewhere; **collect the whole PSReadLine folder.** ⚠️ `MaximumHistoryCount` = **4096**; overflow behaviour undocumented. 🔴 **Lossy by design**: lines containing `password`, `asplaintext`, `token`, `apikey`, `secret` are **never written**, and `-AddToHistoryHandler` suppresses arbitrary commands. |
| 9 | ➕ **the classic channel is undersold — teach 400 as well as 600** | 400 (EngineStart), 403 (EngineStop), 600 (provider), 800 (pipeline, *inconsistently logged*). **`HostApplication` carries the full command line including `-EncodedCommand`, with zero configuration.** 🟢 **600 with `ProviderName = WSMan` indicates PowerShell remoting** — free lateral-movement signal. |
| 10 | ➕ **transcription is a missing fourth PowerShell source** | Captures **command output**, which 4104 does not. Off by default; writes to the user's Documents **or a central share** — the central-share option puts it beyond the attacker's reach. Policy keys differ for pwsh 7, same as #2. |
| 11 | ✅ **RDP: the room is right on 21/24/25, LOCAL, and success-only** | ➕ **Add 22 (shell start — proves an interactive desktop) and 23 (formal logoff).** 🔴 **State that `LOCAL` must be filtered out or students over-count RDP logons** — the single most common error with this artifact, and the room notes the value without warning about the consequence. 🔴 **Failures are Security 4625, which this scenario has lost** — say so rather than leaving it implied. |
| 12 | ⚠️ **1149 fires BEFORE 21 and does not mean authentication** | *"This does NOT indicate successful credential authentication. It signifies successful network-level connection establishment — a client launched RDP and reached the login prompt before entering any credentials."* Chain: **1149 → 4624 type 10 → 21 → 22**. **1149 without a matching 21 = scanning or failed credentials.** ⚠️ NLA-dependent, and published sources disagree — teach the distinction, not an absolute. (Consistent with `windows-network-analysis.md` §2.8.) |
| 13 | ➕ **DetectionHistory is richer than the event log** | Confirmed path. Yields SHA-256 and MD5, **`SpawningProcessName`**, **the creating user**, and the user's response (quarantine/allow/remove). Parser: **DHParser** (`jklepsercyber/defender-detectionhistory-parser`) or the Velociraptor artifacts. 🟢 **The two stores are independent — diff them; a detection in one and not the other is selective tampering.** ⚠️ The **GUI reads DetectionHistory, not the event log.** |
| 14 | ⚠️ **two Defender details to demonstrate, not assert** | The **`file:_` / `webfile:_` path prefixes** are real in the wild but **undocumented by Microsoft**. And **no published sample shows a 5007 naming an `Exclusions\Paths` value** — exclusion→5007 is inferred. **Generate both in lab (EICAR; `Add-MpPreference -ExclusionPath`) and capture the real events before teaching them.** |
| 15 | ➕ **Security 4698 carries the full task XML — and the parent process** | On Windows 10 1903+ it adds `ClientProcessId`/`ParentProcessId` — **the process that created the task**, which is gold for attribution. Governed by **Audit Other Object Access Events**; ⚠️ **its OS default is NOT VERIFIED** — Microsoft publishes a *recommendation* table that is easily misread as defaults. **Check with `auditpol`, don't assume.** Same subcategory yields 4699 deleted / 4700 enabled / 4701 disabled / 4702 updated. |
| 16 | 🔴 **web access logs contain no request body** | Neither IIS's default field set nor Apache `combined` has one. **A webshell operated over POST leaves a line indistinguishable from a legitimate form submission — same URI, same 200, same UA.** 🟢 **The room demonstrates this and never names it** (§2.1). ⚠️ Apache error-log gotcha: *"'File does not exist' messages for 404 responses are logged at `info` level and will not appear in the error log with the default `LogLevel` of `warn`"* — **directory brute-forcing is invisible in a default error log; read the access log.** |
| 17 | 🟢 **IIS rotation does not delete — which inverts the threat** | IIS opens a new file daily or at `truncateSize` and **keeps the old ones**; Microsoft ships no cleanup and documents *"running a script … in a scheduled task"* as the approach. **So the deletion mechanism on a typical IIS host is an administrator's own scheduled task — which §2.6 says an attacker can create or modify.** 🟢 **Check for a scheduled task that deletes web logs.** ⚠️ And absent logs are as often *"users turn off logging completely"* as anti-forensics. |

## 4. Evidence used

- **A live Windows VM (`HR01-SRV`)** with a completed intrusion on it, reached over RDP. The Security
  and System logs have been cleared; the five channels in §2 have not.
- **Not downloadable. No image. Nothing for `ecdfp-evidence`.**
- 🔴 The room prints **plaintext RDP credentials**. Not reproduced here (**R8**).

### 🟢🟢 But the scenario design is the most reusable thing in nineteen rooms

Three elements, all cheap to reproduce and all of which we lack:

**1. The wrong conclusion, stated by a character, before any evidence.** The CTO's *"All event logs
are empty, so hackers did not breach the servers"* — followed by the crypto-scam ads and the 100%
CPU. **The student is shown the error and its consequence in the same paragraph, and their whole
task is to disprove it.** ⚠️ Note how different this is from Diskrupt's brief (room 18), which
named a suspect and editorialised about her tenure. **This brief blames a *conclusion*, not a
person** — it gives the student something to be sceptical about that isn't a human being. **That is
the model.**

**2. A deliberately unglamorous host.** *"our old HR server (HR01-SRV). We hosted salary review
automations there that got unpopular, and the server is now rarely used."* **The forgotten,
low-value, unpatched box is where real intrusions start**, and saying so costs one sentence.

**3. A partial, hedged alert as the starting point.** *"we noticed a spike in HTTP traffic from the
Users' subnet and **suspect** it to be a part of the attack. We would appreciate seeing any evidence
you can find there!"* — a lead, an admitted uncertainty, and an open-ended ask. **Not "find the
malware."**

### 🟢 `EVS-07` — and this one is nearly free

Everything this room needs is **configuration plus activity**, not an image:

| the room's artifact | how we produce it on `EVI-SRC01` |
|---|---|
| cleared Security log | `wevtutil cl Security` — and it is itself the anti-forensics artifact |
| web access log with a scan and an upload | any small web app + a `dirb`-style pass + one POST |
| PowerShell history / 400 / 600 / 4104 | just run the commands; three of the four are on by default |
| **a pwsh 7 session that evades a 5.1-scoped policy** | ➕ **new, and the best exercise here** — §3 #2 |
| RDP 21/24/25 with a source IP | connect from the second VM |
| a scheduled task | `schtasks /create` |
| **a hidden task (`SD` deleted)** | ➕ **new** — requires SYSTEM; the Tarrask technique, §3 #7 |
| Defender 1116/1117 + DetectionHistory | drop **EICAR**, then a second sample; capture both stores |
| a Defender exclusion + its 5007 | `Add-MpPreference -ExclusionPath` — **and capture the real event** (§3 #14) |

**Cost: one scripted afternoon on a VM we already have. No licence, no download, and — unlike
CFReDS — the answers are ours.** 🟢 **And two of the rows are exercises no room in the path
teaches**, which is where our version beats the source.

## 5. Lab design worth reusing

1. **🟢🟢 The CTO's wrong conclusion as the opening line.** §4. **`S1` opens with this.**
2. **🟢🟢 The three-command PowerShell demonstration** (§1). Three sources, three test commands, a
   table of which caught which, and *"Check it out yourself!"* **Copy the design exactly** — and
   extend it with a **fourth row for pwsh 7** and a **fifth for a transcript**, which turns the
   room's best teaching device into something better than the original.
3. **🟢🟢 Structure the session by attack phase, not by artifact.** Initial Access → Execution →
   Lateral Movement → Persistence → Credential Access, one log source each. **The student learns
   the kill chain and the log map at the same time**, and every task title carries the phase.
   **This is how `S5-08` and `S6-01` should be laid out.**
4. **🟢 Two independent stores of the same fact, stated as such** (§2.8). The room explains that
   Defender's event log and DetectionHistory are independent, that an attacker must clear both, and
   that most clear one. **Generalise it into a rule:** *when two artifacts record the same event
   independently, the disagreement is the finding.* It is the same rule as `pslist`/`psscan`
   (room 11), `cmdline`/`handles` (room 13), and `$SI`/`$FN` (room 18). **Four instances now — make
   it a named principle.**
5. **🟢 Correlate, don't just query.** The scheduled-task section lists four sources for one task
   (channel + XML + GUI + process logs) and says why each is needed. **Right instinct, and the model
   for every artifact block we write.**
6. **🟢 Honest about defaults.** The room flags which channels are on and off, and *"it is common to
   see it enabled, as IT administrators often use it to debug their scheduled tasks."* **Default
   state is part of the artifact, and stating it is what separates a log list from a method.**
7. **🟢 Named the intended audience** — *"DFIR team members and SOC L2/L3 analysts"* — and warned
   about the format: *"includes both guided walkthroughs along with independent challenges. Prepare
   for both!"* **Small, professional, and it sets expectations.**
8. **⚠️ Do NOT reuse the plaintext credentials in the task body** (**R8**).

### ✅ No safety defect — and it is the first room in the path with an anti-forensics thesis

Nothing here endangers the analyst or the evidence; it is read-only log analysis over RDP. ⚠️ The
one handling note our version must add: **the student is connected over RDP, so their own session
generates 1149 / 4624 / 21 / 22 events in the very channel they are examining** — the
responder-footprint problem from rooms 13 and 17, in the artifact under investigation.
🟢 **Which makes it an exercise rather than a warning: "three of the RDP sessions in this log are
yours. Identify them."**

**Defect tally unchanged at seven** (rooms 6, 8, 9, 12, 13, 15, 18 — table in `diskrupt.md` §5).

## 6. Question patterns

**20 questions across 8 tasks**, and the design is the strongest of any room extracted.

**🟢🟢 Every task is one attack phase, one log source, four questions.** Tasks 3–7 each ask four
questions of a single channel, and the four **walk the same artifact from identification to
detail**. Task 3, for example: *what is the web app's title* (orientation) → *which IP scanned it*
(the lead) → *absolute path of the uploaded file* (the artifact) → *what would you call the
uploaded malware/backdoor* (classification). **Orient → lead → artifact → classify, four times
over.** That is a reusable question template and we should adopt it.

**🟢 Answer formats are specified where they matter** — *"(format: 2025-01-05 15:30:45)"*,
*"(format: HOSTNAME\USER)"*. ⚠️ **Contrast room 18, where two questions turned on undeclared
units.** This room does it right; say so in our own question-writing guidance.

**🟢 Task 2's single question is a genuinely clever opener**: *"After launching the VM, open Event
Viewer. What is the earliest Event ID you see in the Security logs?"* — **the student's first act is
to confirm the log really is empty.** Verify the premise before investigating it. **Keep this.**

**🟢 The chain is a real narrative**, and each answer is the next question's input: the scanning IP
→ the uploaded webshell → the first command through it → the download URL → the Defender exclusion
→ the tunnelled service → the RDP login that used it → the scheduled task that made it persistent →
the Mimikatz detection → the command that dumped LSASS. **Ten links, five channels, one story.**

**⚠️ But the questions are still all single-value extraction**, and several embed their answer:
*"which remote access service was tunnelled"* presumes tunnelling; *"the file name of the downloaded
**Mimikatz** executable"* names the tool in the prompt; *"which **Mimikatz** command was used to
extract hashes from LSASS memory"* likewise. **The room's prose is careful; its question stems give
things away.**

**🔴 Nineteenth room, no question whose answer is "cannot be determined"** — and here the omission
is sharpest, because **the room's entire thesis is about what absent logs do and do not mean.**
Candidates, all from artifacts already on the student's screen:

| the room could have asked | correct answer |
|---|---|
| *"The Security log is empty. Was the host breached?"* | **Cannot be determined from the Security log.** ✅ **The room asks the student to verify it is empty and never asks what that means** — the one question its own scenario was built to pose. |
| *"There are no 4104 events. Was script block logging off?"* | **Cannot be determined** — Not Configured still logs suspicious blocks. **Check whether `EnableScriptBlockLogging` is `0`** (§2.4). |
| *"The attacker used PowerShell. Why is there no 4104 for it?"* | **They may have used pwsh 7**, which logs to a different channel under a different policy key (§2.4). |
| *"`schtasks /query` shows no malicious task. Is there persistence?"* | **Not established** — an `SD`-deleted task runs and is invisible to `schtasks`. **Diff `TaskCache\Tree` against `System32\Tasks`** (§2.6). |
| *"The web log shows a POST returning 200. What was sent?"* | **Cannot be determined** — access logs contain no request body (§2.1). |
| *"Defender logged no detection for the webshell. Was it clean?"* | **No** — check DetectionHistory separately, and check the **exclusion** the attacker created first (§2.7). |

🟢🟢 **Six, and every one is a different *reason* an artifact can be silent**: it was cleared · the
policy has three states · the tool logs elsewhere · the ACL was removed · the field was never
captured · a second store exists. **That list is the syllabus for `S5-08`, and it is the single
best thing this room gave us.**

## 7. Figures we would need to draw

Figures present in the room: **screenshots of Event Viewer**, one per channel, showing a real event
with its fields. Useful in kind, not reusable (**D22**) — and ours must be reshot anyway because
several of the room's ID claims are wrong (§3).

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **six reasons a log is silent** | six panels, each an empty Event Viewer pane with a different cause beneath — **cleared** · **policy has three states** · **the tool logs to another channel** · **the ACL was removed and the tool failed open** · **the field was never captured** · **a second store holds it** — over one caption: *"'empty' is a question, not an answer"* | **highest** — this is the `S5-08` session slide, and it is `S1`'s thesis in one image |
| 2 | **the PowerShell coverage matrix** | the room's three test commands as rows, extended to five — interactive · `-c` · script file · **pwsh 7** · **with a transcript** — against five columns (history · 400/600 · 4104 5.1 · 4104 Core · transcript), ticks and crosses filled in, with the **pwsh 7 row showing crosses under the 5.1 columns** accented | **highest** |
| 3 | **script block logging's three states** | a three-position switch — *Not Configured* (**automatic suspicious logging ON**) · *Enabled* (**everything, Verbose**) · *Disabled* (**nothing, not even the record of last resort**) — with `EnableScriptBlockLogging = 0` flagged beneath the third as **an IOC**; caption *"hunt for the zero, not the absence"* | **highest** |
| 4 | **the hidden scheduled task** | `TaskCache\Tree\<task>` and `System32\Tasks\<task>.xml` side by side, the **`SD` value struck out**, and three tools (`schtasks`, Autoruns, Task Scheduler GUI) drawn hitting an ACL wall and **returning nothing rather than an error** — while an arrow shows the task still executing; caption *"the tools fail open"* | **high** |
| 5 | **the attack chain against the log map** | the five phases left to right — Initial Access · Execution · Lateral Movement · Persistence · Credential Access — each with the channel that caught it and **its default state (on/off) as a coloured dot**; the Security log drawn across the top as a **struck-through band** | **high** — the room's structure, made visible |
| 6 | **the RDP event sequence** | `1149` → `4624 type 10` → `21` → `22` → `24` → `25` → `23` on one timeline, with **1149 annotated "reached the prompt — NOT authenticated"**, **a 1149 with no following 21 marked as the brute-force pattern**, and a `LOCAL` row greyed with *"filter this out or you will over-count"* | **high** |
| 7 | **two independent stores** | Defender's event log and DetectionHistory as two boxes recording the same detection, with a **diff arrow between them** and *"clearing one leaves the other"*; footnoted with the other three instances of the same principle (`pslist`/`psscan`, `cmdline`/`handles`, `$SI`/`$FN`) | medium |
| 8 | **what a web access log line does and does not carry** | one log line exploded field by field, with a **greyed panel beside it** for everything absent — request body, headers, response body — captioned *"a POST webshell command looks exactly like a form submission"* | medium |

Figures 1 and 3 are the ones that change how a student reads an empty pane. Never their images
(**D22**).

## 8. Fit against our material

### ⚠️ Part 1 under-rates this room badly

Part 1 lists it as *"S5 case — execution evidence with logs cleared. Strong anti-forensics caveat
material."* **That is right but reads as a case to mine.** It is a **guided teaching room with five
artifact families we do not currently cover**, and its scenario design is the best in the path.
**Amend Part 1 to:** *S5/S6 — the non-Security log-source syllabus, the attack-phase session
structure, and the `S1` opening scenario. Promote to Priority 1 in practice.*

### Rows this strengthens

- **`S5-08`** *event logs beyond Security* — 🟢🟢 **this room is the row.** Five channels, their
  default states, their coverage gaps and their evasions. **Fully sourced, and richer than what we
  had planned.**
- **`S6-01`** log sources · **`S6-07`** timeline — the five-channel map and the ten-link chain.
- **`S1`** — 🟢🟢 **the opening scenario** (§4), plus the **six-reasons-a-log-is-silent** figure,
  which is D7 rendered as a single image.
- **S5 anti-forensics** — three techniques the room supplies or implies and no other room does:
  **`SD`-deleted hidden tasks** · **`EnableScriptBlockLogging = 0`** · **Defender exclusions
  created pre-emptively**. ➕ Plus the one it demonstrates without naming: **using pwsh 7 to sidestep
  a 5.1-scoped policy.**
- **`ecdfp-evidence`** — **`EVS-07`** (§4), a configuration-and-activity evidence set costing one
  scripted afternoon.
- **Question-writing guidance** — the *orient → lead → artifact → classify* template (§6), and the
  contrast with room 18 on declaring answer formats.

### Five things our version must do that the room does not

1. **Teach the three states of script block logging**, and hunt for `EnableScriptBlockLogging = 0`.
2. **Cover PowerShell 7** — different channel, different policy key, same history file.
3. **Correct the Defender ID list** — 5013 is Tamper Protection; add 5004/5010/5012.
4. **Add hidden scheduled tasks (`SD` deletion)** — the room's persistence section has no
   anti-forensics at all.
5. **Name the reason the web log cannot answer the webshell question** — no request body. The room
   demonstrates it and leaves it unsaid.

### 🔴 One cross-room consistency item

`windows-network-analysis.md` §2.8 and this note both cover **RDP source-IP artifacts**, from
different directions — that room from `qwinsta` (live), this one from LocalSessionManager
(historical). ✅ **They agree**: 1149 fires first and is not authentication; 21/24/25 carry Source
Network Address; failures are 4625. **When `S6-02` and `S5-08` are written, use one figure (§7 #6)
across both** rather than two overlapping ones.

### Minutes

Everything here lands in **existing rows** — `S5-08`, `S6-01`, `S6-07`, `S1` — as content, figures
and exercises. ⚠️ **But `S5-08` is currently scoped as one row and this room is 90 minutes of
material for it.** That is the second time a Priority-2 room has signalled that an S5 row is
under-scoped (room 18 did the same for the S4 capstone).

**No new rows. S5 unchanged at its current shape.**

**S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Fourteenth room carrying the S5 overdraft — and this room adds material to S5 rather than
relieving it.** The re-split is now the largest open item in the project.

### Out of scope

Web-application exploitation itself (how the shell got uploaded) — correctly out; we investigate,
we do not exploit. Mimikatz usage — the room names the command and does not teach it, which is the
right line. Sysmon and EDR — absent, and arguably belong in `S6-01` as the modern answer to these
channels' gaps. **No scope conflict.**

### Still unresolved

**Browser forensics** — nineteenth room, no `DECISIONS.md` row.
**S5 re-split** — fourteenth room carrying it; now compounded by this room's volume.
**S4 capstone weighting** — from room 18, still open.

## 9. Links

- Room: <https://tryhackme.com/room/loglesshunt>
- Room's stated prerequisites: Log Analysis Module · Windows Event Logs.
- **PowerShell logging**: about_Logging 5.1
  <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1>
  · 🔴 **about_Logging_Windows 7.6 (the `PowerShellCore/Operational` channel)**
  <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.6>
  · 🟢 **"PowerShell ♥ the Blue Team" — the automatic-script-block-logging paragraph**
  <https://devblogs.microsoft.com/powershell/powershell-the-blue-team/>
  · about_PSReadLine <https://learn.microsoft.com/en-us/powershell/module/psreadline/about/about_psreadline?view=powershell-7.6>
  · Set-PSReadLineOption <https://learn.microsoft.com/en-us/powershell/module/psreadline/set-psreadlineoption?view=powershell-5.1>
- **Scheduled tasks**: Microsoft Tarrask analysis (the `SD`-deletion technique; the microsoft.com
  URL 403s to automated fetch — syndicated copy)
  <https://thewindowsupdate.com/2022/04/12/tarrask-malware-uses-scheduled-tasks-for-defense-evasion/>
  · Binary Defense, *Diving into Hidden Scheduled Tasks*
  <https://binarydefense.com/resources/blog/diving-into-hidden-scheduled-tasks>
  · event 106 <https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/dd363640(v=ws.10)>
  · event 129 <https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/cc774964(v=ws.10)>
  · Security 4698 <https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698>
- **RDP**: Ponder The Bits, *Windows RDP-Related Event Logs*
  <https://ponderthebits.com/2018/02/windows-rdp-related-event-logs-identification-tracking-and-investigation/>
- **Defender**: 🔴 **the authoritative event-ID table (5013 = Tamper Protection)**
  <https://learn.microsoft.com/en-us/defender-endpoint/troubleshoot-microsoft-defender-antivirus>
  · command-line arguments (`-CheckExclusion`, `-GetFiles`)
  <https://learn.microsoft.com/en-us/defender-endpoint/command-line-arguments-microsoft-defender-antivirus>
  · SANS, *Uncovering Windows Defender Real-time Protection History with DHParser*
  <https://www.sans.org/blog/uncovering-windows-defender-real-time-protection-history-with-dhparser>
  · DHParser <https://github.com/jklepsercyber/defender-detectionhistory-parser>
  · Huntress, *Defender Exclusions* <https://www.huntress.com/blog/you-can-run-but-you-cant-hide-defender-exclusions>
- **Web logs**: 🔴 **IIS default fields, incl. the Feb 2026 bytes change**
  <https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/sitedefaults/logfile/>
  · IIS log storage (no built-in deletion)
  <https://learn.microsoft.com/en-us/iis/manage/provisioning-and-managing-iis/managing-iis-log-file-storage>
  · Apache log files <https://httpd.apache.org/docs/2.4/logs.html>
  · Apache on Windows (`\Apache24` as the documented default)
  <https://httpd.apache.org/docs/2.4/platform/windows.html>
- Companion notes: `windows-network-analysis.md` §2.8 (RDP source IP, live side) ·
  `diskrupt.md` §4 (scenario framing, the counter-example)
- Tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` — **needs a block G for the
  PowerShell three-state finding, the pwsh 7 channel split, Defender 5013 and the IIS defaults.**
