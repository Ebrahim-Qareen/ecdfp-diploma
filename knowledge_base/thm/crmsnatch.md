---
room: CRM Snatch
url: https://tryhackme.com/room/crmsnatch
module: **Honeynet Collapse — stage 4 of 6.** *"Investigate the fourth, Disk part of the Honeynet
        Collapse!"* Challenge room (Priority 2). Target `SRV-CRM-01` (172.16.2.9, **CORE**).
feeds: 🟢🟢 **The most in-scope room of the module.** Disk image + EZ Tools = our `S4`/`S5`/`S6`
       working shape exactly. Feeds `S6-06`, `S5-08`, `S3-03`, `S6-09` and the D19 exfiltration leg.
       🔴🔴 **Two question-design defects that together settle a rule**: Q5's answer is a **password**
       and Q6's answer is **PII from the exfiltrated customer data** (§4).
       ⚠️ **A chaining inference I drew here was REFUTED by stage 6 and is corrected in §5.2** —
       recorded rather than quietly fixed, because the mistake is instructive.
difficulty / time: **Hard** · 60 min · 2 tasks · 7 questions (6 scored + 1 "Let's go!") · Premium ·
                   1,246 completions · 31 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, scenario, lab paths, tips and all question stems.
              0 sections NOT READ.
              🔴 **Room ships a plaintext RDP password in the task body — not reproduced (R8).**
              Sixth Priority-2 room to do so. ⚠️ **That password is literally one of the strings
              hardcoded in the stale `/tmp/verify.py` blocklist found on the device** — see §5.5;
              it is the sharpest possible argument for **D39**.
              🔴🔴 **Q5's expected answer is a password and Q6's is a person's email address taken
              from exfiltrated customer data.** Neither reproduced; neither obtainable here.
              ⚠️ **Answers NOT READ** — lab machine not started. §2 reconstructed from the 6 scored
              questions and the scenario paragraph, as for rooms 18–25.
---

## 1. What the room teaches

**The complete collection-to-exfiltration leg, worked from a disk image — which is exactly the shape
our S4–S6 sessions have, and the first room in the module where that is true.**

The scenario paragraph is unusually dense and every clause is an artifact:

> *"The latest customer export was grabbed, hidden inside a password-protected archive, and quietly
> transferred to the external buckets. In the process, event logs were wiped, and shadow copies were
> deleted on the way out."*

**Collection → staging → archive → cloud exfiltration → anti-forensics, in one sentence**, and the
room then asks the student to *"unravel the timeline, expose the masqueraded tools, and prove the
exfiltration."* 🟢🟢 **"Prove the exfiltration" is the right verb** and the room earns it: the
proof does not come from watching traffic, it comes from the **tool's own configuration file left on
disk** (§2.5).

🟢🟢 **The cover story is again the delivery mechanism, and it is better than stage 2's.**

> *"Hey Alex, did you finish patching the Odoo server? Can you have a look at the nightly exports on
> SRV-CRM-01? Finance says yesterday's customer CSV file vanished from the share. ~ Matthew"*

**The missing file is the attack, and it is dispatched as a helpdesk ticket.** Finance noticed the
*symptom* of the exfiltration and reported it as an IT fault; Matthew — whose credentials were stolen
in stage 2 and who was the investigator in stage 3 — sends someone to look at it. ⚠️ **The room says
outright that the attacker "used the distraction to complete the snatch."** **The detection worked
and the routing destroyed it**, which is a more interesting failure than "nobody noticed."

**What it gets right that the earlier rooms did not:**

- 🟢🟢 **It is a disk image, offline, with tools provided** — `.\Image\*` and `.\EZTools\*` on the
  Desktop. **No live-system defect** (§5.5), and it matches `S4`/`S5` exactly.
- 🟢 **"Expose the masqueraded tools"** makes T1036.005 an explicit objective rather than a tip.
- 🟢 **The anti-forensics is in the scenario, not hidden** — the student knows logs were wiped and
  shadow copies deleted, so the exercise is *working around destroyed evidence*, which is the real
  job. **That is the single best framing decision in the module.**

**What it gets wrong:**

- 🔴🔴 **Q5 asks for a password and Q6 asks for a person's email address from the stolen customer
  data.** §4. Room 24 gave us the rule *"no question may have a credential as its answer"*; **this
  room shows the rule was too narrow.**
- 🔴 **Q2 is built on a weaker artifact than it appears.** *"For how many seconds did the attacker
  maintain their PowerShell session active?"* is answered from engine-lifecycle events **400/403** —
  which bracket an **engine instance, not a session**, and *"cannot be strictly correlated to a logon
  session."* §2.2. **A number of seconds is exactly the kind of answer that hides an assumption.**
- ⚠️ **Task 1's heading in this room reads "Initial Access Pot"** — stage 1's title, left in by
  copy-paste. Trivial, but it is the visible seam of the template (§5.1) and worth one line in our
  own review checklist.

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 6 scored questions plus the scenario paragraph. Mapping: Q1 → 2.1 ·
Q2 → 2.2 · Q3 → 2.3 · Q4 → 2.4 · Q5 → 2.5 · *"password-protected archive"* → 2.6 ·
*"event logs were wiped"* → 2.7 · *"shadow copies were deleted"* → 2.8. **Q6 is not an artifact
question and is handled in §4.**

### 2.1 The remote session, from a disk image

- **What it is** — Q1: *"Which domain account was used to initiate the remote session onto the
  host?"*
- **Where it lives** — the same channels as room 24 §2.1 — `TerminalServices-LocalSessionManager/
  Operational` 21/22/23/24/25 (**on by default**), `RemoteConnectionManager` 1149, Security
  4624 LogonType 10 — 🔴 **but this time they are `.evtx` files inside an image**, parsed offline
  with `EvtxECmd`, not read live. **Registry corroboration** survives independently: profile
  creation under `HKLM\…\ProfileList`, and the user's `NTUSER.DAT` existing at all.
- **What it proves** — that a session was established for that account at that time.
- **What it does NOT prove** — 🔴🔴 **that the account's owner did it — and here the module has
  already told us he did not.** These are **Matthew's stolen credentials** from stage 2. **The
  strongest possible demonstration that authentication is not attribution**, delivered by the same
  module three rooms apart, and it is free to use.
  🔴🔴 **And the logs were wiped** (§2.7). **So the honest first question is not "who logged in" but
  "is this channel complete?"** — a wiped Security log with an intact `LocalSessionManager` channel
  gives a partial answer whose gaps must be stated. ⚠️ **Q1 presumes the record survived**; on this
  host that is a finding to establish, not an assumption.
  ⚠️ 1149 is not authentication and fires before it (**G6**); `Source Network Address = LOCAL` must
  be filtered.
- **How to parse it** — `EvtxECmd` over the image's `\Windows\System32\winevt\Logs\`, into Timeline
  Explorer. 🟢 **Cross-check the event record IDs for gaps** — a wiped-then-restarted log begins at
  RecordID 1, and a **discontinuity is evidence of clearing even if 1102 itself was removed**.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the disk image is what makes this survivable.**
  Registry hives, `$MFT` and profile directories are not cleared by `wevtutil cl`, so **an attacker
  who wipes event logs has removed one source and left four.** That asymmetry is the reason S4 comes
  before S6 in our map (**D25**) and it is worth stating explicitly here.

### 2.2 PowerShell engine lifecycle — a duration that is not a session

- **What it is** — Q2: *"For how many seconds did the attacker maintain their PowerShell session
  active?"*
- **Where it lives** — the **classic `Windows PowerShell` channel**: **400** *"Engine state is
  changed from None to Available"*, **403** *"Engine state is changed from Available to Stopped"*,
  and **600** provider lifecycle (*"Provider … is Started"* — a `WSMan` provider indicates remoting).
  🟢 **On by default**, and Microsoft says why: *"By default, only the following event types are
  enabled: `$LogEngineLifecycleEvent`, `$LogEngineHealthEvent`, `$LogProviderLifecycleEvent`,
  `$LogProviderHealthEvent`."* ⚠️ **4103/4104 live in `Microsoft-Windows-PowerShell/Operational` and
  module/script-block logging is off by default there** — see **G1** for the three-state nuance.
- **What it proves** — that a PowerShell **engine instance** started and stopped at those times.
- **What it does NOT prove** — 🔴🔴🔴 **that it was one session, or the attacker's session.**
  *"This event cannot be strictly correlated to a logon session."* **Every host that loads the
  PowerShell engine emits its own 400/403 pair** — `powershell.exe`, the ISE, and **any .NET or COM
  application hosting `System.Management.Automation`.** So one RDP session with three console
  launches yields **three pairs**, and a long-lived non-interactive host **inflates the span**.
  🔴 **Subtracting the first 400 from the last 403 is therefore a plausible-looking wrong answer**,
  and it is the answer a student under time pressure will produce.
  🟢 **The correct method:** pin the pair by **`RunspaceId`**, corroborate with
  **`HostApplication`/`HostName`** (`ConsoleHost` = local, `ServerRemoteHost` = remote), and bracket
  against the RDP logon/logoff (**4624 type 10 / 4634**) from §2.1. ⚠️ **And even then it is a
  duration of *engine availability*, not of attacker activity** — an idle console counts.
- **How to parse it** — `EvtxECmd` over `Windows PowerShell.evtx`; sort by `RunspaceId`; join to
  §2.1's session.
- **Anti-forensics / false-positive caveat** — 🔴 **the channel is small and was a wipe target**
  (§2.7). 🟢🟢 **But the engine-lifecycle channel being on by default is the reason anything survives
  at all**, and it is the best example in the corpus of **G4**'s point: *the classic PowerShell
  channel is the best default-on artifact*. ⚠️ **On PowerShell 7 it is not this channel at all** —
  `PowerShellCore/Operational`, under a different policy key (**G2**).

### 2.3 The C2 address, recovered from what PowerShell recorded

- **What it is** — Q3: *"What was the attacker's C2 IP address used for staging and exfiltration?"*
- **Where it lives** — in descending order of likelihood on a real host:
  **`ConsoleHost_history.txt`** (PSReadLine — on by default, per-host, lossy, **G3**);
  **4104 script blocks** (on for *suspicious* blocks even when "Not Configured" — **G1**);
  **4103 pipeline/module logging** (off by default); **`rclone.conf`** itself (§2.5, which names the
  remote rather than an IP); **`$UsnJrnl`/`$MFT`** for the tool and staging paths; and
  **`Terminal Server Client` / firewall or DNS caches** where they survive.
- **What it proves** — that a string resembling an address appears in a command that was typed or
  logged on this host.
- **What it does NOT prove** — 🔴🔴 **that a connection was made to it, or that data left.** A
  command line is an *intention*; the network evidence is not on this disk. ⚠️ **And "C2" is an
  interpretation** — *"used for staging and exfiltration"* is the room asserting a role the artifact
  does not carry. 🔴 An IP in a script is equally consistent with a failed attempt, a typo, or a
  decoy.
  🔴🔴 **Absence proves nothing** — the wipe (§2.7) plus 4103/4104 being off by default plus
  `HISTCONTROL`-equivalent gaps mean **"no C2 address found" is the expected result on a
  well-cleaned host**, not evidence of no C2.
- **How to parse it** — read `ConsoleHost_history.txt` from each user profile in the image;
  `EvtxECmd` over the PowerShell channels; `grep` the `rclone.conf` and any batch/PS1 files;
  `MFTECmd` for recently created scripts in temp paths.
- **Anti-forensics / false-positive caveat** — 🟢 **PSReadLine is the one that usually survives a
  log wipe**, because `wevtutil cl` clears **event logs** and `ConsoleHost_history.txt` is **a text
  file in the user profile**. 🟢🟢 **That asymmetry is the lesson: the attacker's cleanup targeted a
  log subsystem, not the filesystem** — and it is why §2.1's *"one source removed, four left"* holds
  here too.

### 2.4 rclone — the "well-known tool", and what it leaves

- **What it is** — Q4: *"Which well-known tool was used to exfiltrate the collected data?"* Given Q5
  names **Mega**, the tool is **rclone**. ⚠️ **Not confirmed without running the lab**, but the
  evidence is strong: rclone is ATT&CK software **S1040**, and **T1567.002 names the exact
  combination** — *"Rclone can exfiltrate data to cloud storage services such as Dropbox, Google
  Drive, Amazon S3, and MEGA."*
- **Where it lives** — the binary (often **renamed** — this is the room's *"masqueraded tools"*),
  its config at **`%APPDATA%\rclone\rclone.conf`** (§2.5), plus the usual execution artifacts:
  **Prefetch**, **Amcache** (with block **L2**'s caveats), **ShimCache**, `$MFT`/`$UsnJrnl`.
  ⚠️ **rclone writes no log by default** — *"`--log-file` … This is not active by default."*
- **What it proves** — that a data-transfer utility was present and, with Prefetch, that it ran.
- **What it does NOT prove** — 🔴🔴 **that anything was transferred, or what.** rclone is a
  general-purpose sync tool with entirely legitimate uses; **presence is not exfiltration.** The
  proof chain is: the binary (present) → Prefetch (ran) → `rclone.conf` (a remote was configured) →
  the command line (§2.3, *what* was copied) → **and only network or provider-side evidence shows
  bytes leaving.** **Four of those five are on this disk; the fifth is not.**
  🔴 **A renamed binary defeats name-based hunting entirely** — which is the room's own point. The
  discriminators are **Amcache/`$MFT` size and hash**, the **Authenticode publisher**, and the
  **`rclone.conf` sitting beside it**, not the filename. ⚠️ **And per block L2, Amcache's SHA-1 is
  truncated at ~30 MB and carries a `0000` prefix** — strip it, and check the size before trusting a
  negative lookup.
- **How to parse it** — `PECmd` (Prefetch), `AmcacheParser`, `MFTECmd`; then read `rclone.conf`.
  🟢 Command-line flags worth grepping for in history or script blocks: `copy`, `sync`,
  `--transfers` (*"Number of file transfers to run in parallel (default 4)"*), `--config`,
  `--no-check-certificate` (*"Do not verify the server SSL certificate (insecure)"*), `--log-file`.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **rclone is a genuinely dual-use tool and that is
  the teaching point.** MITRE: *"Rclone has been used in a number of ransomware campaigns, including
  those associated with the Conti and DarkSide Ransomware-as-a-Service operations."* The DFIR Report
  documents the identical shape — RDP intrusion, then *"Rclone was utilized on multiple file servers
  to facilitate the exfiltration of data."* **The finding is never "rclone is present"; it is
  "rclone is present, configured to a remote nobody in this organisation owns, and ran once."**

### 2.5 `rclone.conf` — the exfiltration proof, and a password that is not encrypted

- **What it is** — Q5: *"What is the obscured password to the attacker-controlled Mega?"*
  🔴 **The value is a credential and is not reproduced (R8); the question shape is the defect (§4).**
  **The artifact, however, is excellent.**
- **Where it lives** — **`%APPDATA%\rclone\rclone.conf`** on Windows — rclone's docs give the search
  order and note the Windows case resolves to `%APPDATA%/rclone/rclone.conf`; on Unix
  `$XDG_CONFIG_HOME/rclone/rclone.conf` or `~/.config/rclone/rclone.conf`. ⚠️ `--config` can point
  anywhere, so **grep the image for the section header form rather than trusting the default path.**
- **What it proves** — 🟢🟢 **the destination, and that is the exfiltration proof the room promises.**
  A section carries the **remote name**, **`type`** (e.g. `mega`), **`user`**, and **`pass`**. rclone's
  own Mega walkthrough shows exactly this shape: `type: mega` / `user: you@example.com` /
  `pass: *** ENCRYPTED ***`. **An attacker-controlled account name and provider, written by the tool
  itself, on the victim's disk.**
- **What it does NOT prove** — 🔴🔴🔴 **that the "obscured" password is protected — it is not, and
  rclone says so in as many words.** *"In the rclone config file, human-readable passwords are
  obscured. Obscuring them is done by encrypting them and writing them out in base64."* And then the
  warning that matters: ***"This is not a secure way of encrypting these passwords as rclone can
  decrypt them - it is to prevent 'eyedropping'."*** **`rclone reveal` reverses it** — ⚠️ and note
  the command has **no documentation page** (a 404 on rclone.org), which is itself worth telling
  students: *an undocumented command is not a hidden one.*
  🔴 **The `*** ENCRYPTED ***` display string is actively misleading** — it is what rclone *prints*,
  not what the file contains, and it is not encryption.
  🔴 **Worse, rclone warns that obscuring is not even applied uniformly:** *"Many equally important
  things (like access tokens) are not obscured in the config file."* **So an OAuth token for a cloud
  remote may sit in the file in cleartext** — which is a bigger finding than the password and the
  room does not ask about it.
  ⚠️ **Real config encryption exists and would defeat all of this** — `rclone config encryption set`,
  *"Set or change the config file encryption password"*. **An encrypted `rclone.conf` is a different
  investigation**, and a student should be able to tell the two apart on sight.
  🔴🔴 **And possessing the credential does not authorise using it.** Logging in to the attacker's
  Mega account to see what was uploaded is **unauthorised access to a third-party service**, however
  satisfying. **This is a handling rule, not a technique**, and the room does not state it.
- **How to parse it** — read the file; record the remote name, type and user **as findings**; place
  the secret **in the restricted appendix by reference (path, offset, timestamp), never by value**
  — the same rule as §4.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **this block is the best "obfuscation is not
  encryption" example in the whole corpus**, and it beats the usual base64 slide because **the tool's
  own documentation says so.** ⚠️ It pairs directly with block **K7** (MD5 for lookup, not integrity)
  and **L2** (Amcache's hash as identification, not integrity): **three separate cases of a value
  that looks cryptographic and is not.** That is a slide.

### 2.6 The password-protected archive — what survives without the password

- **What it is** — *"hidden inside a password-protected archive"*. Not a question, and **that is the
  omission** — the room states the archive and never asks the one thing that makes it interesting.
- **Where it lives** — the archive on disk (or its `$MFT`/`$UsnJrnl` traces if deleted), plus the
  archiving tool's execution artifacts. ATT&CK **T1560.001 Archive via Utility** (Collection).
- **What it proves** — 🟢🟢 **far more than students expect. On a default password-protected archive
  the file names, sizes, timestamps and CRC32 values are all readable without the password.**
  - **ZIP:** encryption (ZipCrypto or AES/AE-x) covers **data only**; the central directory keeps
    names, sizes and CRCs. Hiding them requires **Central Directory Encryption**, APPNOTE bit 13 —
    *"Set when encrypting the Central Directory to indicate selected data values in the Local Header
    are masked to hide their actual values."*
  - **7-Zip:** *"Enables or disables archive header encryption. The default mode is he=off."*
  - **WinRAR:** *"If you set 'Encrypt file names' option, WinRAR will encrypt not only file data, but
    all other sensitive archive areas like file names, sizes, attributes, comments and other
    blocks"*, and *"Without a password it is impossible to view even the list of files in archive
    encrypted with this option."* — **opt-in, therefore off by default.**
  **So the examiner can prove *which customer export was staged* without cracking anything**, which
  is the whole point of the exfiltration question.
- **What it does NOT prove** — 🔴 **the contents.** Names and CRCs are metadata: a file named
  `customers_2026-08-26.csv` proves a name, not a payload. 🟢 **But a CRC32 is a comparison key** —
  if the original export still exists on the share or in a backup, **matching CRCs tie the archived
  item to the known file without ever opening the archive.** ⚠️ CRC32 is a 32-bit checksum, so
  treat a match as strong corroboration, not identity.
  🔴 **And header encryption changes the answer completely** — with `-mhe=on` or WinRAR's option, the
  archive is opaque and **the finding becomes "an encrypted archive of unknown contents was staged",
  which is still a finding.**
- **How to parse it** — `7z l archive.7z` (listing works without the password on a default archive);
  `MFTECmd` for creation time and size; compare CRCs against known files. **Do not attempt to crack
  it** unless the engagement authorises it.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the failure mode here is giving up too early.**
  A student who sees a password prompt concludes the evidence is unavailable; **the correct move is
  to list the archive first.** ⚠️ **That instinct — "try to enumerate before you try to decrypt" —
  generalises to encrypted containers, protected Office documents and locked databases**, and it
  belongs in `S3` beside file-signature analysis.

### 2.7 Event log wiping — and the gaps it cannot fill

- **What it is** — *"event logs were wiped"*. ATT&CK 🔴 **`T1685.005` Clear Windows Event Logs**,
  tactic **Defense Impairment (TA0112)** — *"Adversaries may clear Windows Event Logs to hide the
  activity of an intrusion."* **This is the first room in the corpus that actually needs the
  post-v19 ID** (block **K1**): it is **no longer `T1070.001`.**
- **Where it lives** — **Security 1102** (*audit log cleared*) and **System 104** (*log file
  cleared*), which are written **into the newly cleared log**; the tool's own execution artifacts
  (`wevtutil.exe` in Prefetch/Amcache); and 🟢 **the structural traces the clearing cannot remove.**
- **What it proves** — that a log was cleared, and by which account, if 1102/104 survived.
- **What it does NOT prove** — 🔴🔴 **what was in the log.** Clearing is destruction, not
  concealment — the content is gone. 🔴 **And absence of 1102/104 does not mean no clearing:** a
  second clear removes the first clear's record. ⚠️ **Selective deletion is different from clearing**
  and does not raise 1102 at all.
  🟢🟢 **What survives is the shape of the hole, and this is the method worth teaching:**
  **record-ID discontinuity** (a cleared log restarts at 1 — a channel whose earliest record is 1 on
  a server with months of uptime is a finding *in itself*), **file size and creation time of the
  `.evtx`**, and **cross-channel disagreement** — `LocalSessionManager` still holding sessions the
  Security log no longer mentions. **Three independent tells, none of which the attacker touched.**
- **How to parse it** — `EvtxECmd` over every channel in `\Windows\System32\winevt\Logs\`; sort by
  record ID and by earliest timestamp per channel; `MFTECmd` for the `.evtx` file timestamps.
  🟢 **Then pivot to the artifacts that are not event logs at all** — registry, `$MFT`, `$UsnJrnl`,
  Prefetch, `ConsoleHost_history.txt` (§2.3).
- **Anti-forensics / false-positive caveat** — 🟢🟢 **this is why S4 precedes S6 in our map (D25),
  and the room demonstrates it better than an argument could.** The attacker destroyed the timeline
  source and left the file system intact. ⚠️ **Legitimate clearing happens** — a rebuilt server, a
  misconfigured SIEM forwarder, an administrator "tidying up" — so **1102 is a lead, not a verdict**,
  and its account and timestamp must be checked against change records.

### 2.8 Shadow copy deletion — the artifact that mostly does not exist

- **What it is** — *"shadow copies were deleted on the way out"*. ATT&CK **T1490 Inhibit System
  Recovery**, tactic **Impact** — MITRE names the command: *"vssadmin.exe can be used to delete all
  volume shadow copies on a system - vssadmin.exe delete shadows /all /quiet."*
- **Where it lives** — 🔴🔴 **there is no dedicated event ID for it.** Detection in practice is
  **process-creation based**: Elastic's rule matches `process.name : "vssadmin.exe"` with
  `process.args : ("delete", "resize")` and `process.args : "shadows*"`. **So the artifact is Security
  4688 with command-line auditing, or Sysmon 1** — 🔴 **and block L1 established that both are off by
  default.** Fallbacks: **Prefetch / Amcache / ShimCache for `vssadmin.exe` or `wmic.exe`**, and
  4104 if script-block logging caught it.
- **What it proves** — with those artifacts, that the deletion tool ran.
- **What it does NOT prove** — 🔴🔴🔴 **two beliefs I held going in were wrong, and the research
  refuted both. Recording them because they are widely repeated:**
  1. **Application event 524 is NOT a shadow-copy artifact.** It is provider
     `Microsoft-Windows-Backup` and means *"The system catalog was deleted"* — **backup-catalog
     deletion (`wbadmin delete catalog`), not VSS.** ⚠️ And even for that, JPCERT warns *"the
     above-mentioned content may also occur in normal operation."*
  2. **`volsnap` event 25 is NOT an attacker indicator.** Its text is *"The shadow copies of volume
     %2 were aborted because the diff area file could not grow in time"* — **a capacity/IO
     condition.** A ransomware playbook that lists it as an IOC is wrong.
  ⚠️ **Registry or `System Volume Information` remnants of deleted shadow copies: NOT VERIFIED.**
  No primary source found. **Do not teach it as fact.**
  🔴 **So the honest position is uncomfortable and correct: on a default host, shadow copy deletion
  may leave nothing but execution evidence for the tool** — and if command-line auditing was off,
  not even the arguments. **"Shadow copies are gone" is often established by their absence plus
  `vssadmin.exe` in Prefetch, and nothing stronger.**
- **How to parse it** — `PECmd`/`AmcacheParser` for `vssadmin.exe`, `wmic.exe`, `powershell.exe`;
  `EvtxECmd` for 4688/4104 if present; check whether any shadow copies remain.
  ⚠️ **On PowerShell 7 the command differs** — `Get-WmiObject`/`Remove-WmiObject` are **removed in
  PowerShell 6/7** (**F5**), so expect `Get-CimInstance Win32_ShadowCopy | Remove-CimInstance`, logged
  to `PowerShellCore/Operational` (**G2**), not the classic channel.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the teaching value is the negative result.**
  This is the clearest case in the corpus where **the correct professional answer is "the deletion is
  inferred from the absence of shadow copies and the execution of `vssadmin.exe`; no direct record of
  the deletion exists on this host, because process command-line auditing was not enabled."**
  **Finding, method, and stated limitation — D20 criteria 2, 3 and 4 in one paragraph.**

## 3. Tools and commands

The room supplies the tools rather than naming commands: *"All the resources you need are on the
user's Desktop"*, with `.\Image\*` and `.\EZTools\*`.

| purpose | command | note |
|---|---|---|
| remote session (Q1) | `EvtxECmd` → Timeline Explorer; 4624 t10 + LSM 21/22 | 🔴 check for a wipe first — §2.7 |
| PowerShell duration (Q2) | `EvtxECmd` over `Windows PowerShell.evtx`; 400 / 403 / 600 | 🔴🔴 engine ≠ session — #2 |
| C2 address (Q3) | read `ConsoleHost_history.txt`; `EvtxECmd` 4104 | 🟢 survives a log wipe — §2.3 |
| the tool (Q4) | `PECmd`, `AmcacheParser`, `MFTECmd` | 🔴 renamed binary — match on hash/size, not name |
| the config (Q5) | read `%APPDATA%\rclone\rclone.conf` | 🔴🔴 "obscured" ≠ encrypted — #1 |
| the archive | `7z l archive.7z` | 🟢🟢 **lists without the password** — #4 |
| log wiping | `EvtxECmd` all channels; sort by record ID | 🟢 discontinuity is the tell — §2.7 |
| shadow copies | `PECmd` for `vssadmin.exe` | 🔴🔴 **no dedicated event ID** — #3 |

⚠️ **EZ Tools GUI are .NET 9 only** as of `2026.5.0` (**I10**) — the `CLEAN-TOOLS` snapshot (**D17**)
must include it. Third room to confirm this.

### CURRENCY CHECK

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"the **obscured** password to the attacker-controlled Mega"* | 🟢🟢 **Correct word, and rclone's own docs make it the best "obfuscation is not encryption" example we have.** *"In the rclone config file, human-readable passwords are obscured. Obscuring them is done by encrypting them and writing them out in base64."* Then the warning: ***"This is not a secure way of encrypting these passwords as rclone can decrypt them - it is to prevent 'eyedropping'."*** **`rclone reveal` reverses it** — ⚠️ and that command **has no documentation page** (404 on rclone.org); it is undocumented, not hidden. 🔴 **The `*** ENCRYPTED ***` string rclone prints is not what the file contains and is actively misleading.** 🔴 **And obscuring is not applied uniformly:** *"Many equally important things (like access tokens) are not obscured in the config file"* — **an OAuth token may sit in cleartext, which is a bigger finding than the password.** ⚠️ Real protection exists — `rclone config encryption set`, *"Set or change the config file encryption password"* — **an encrypted `rclone.conf` is a different investigation.** Config path: `%APPDATA%/rclone/rclone.conf` on Windows; `$XDG_CONFIG_HOME/rclone/rclone.conf` or `~/.config/rclone/rclone.conf` on Unix. **No log by default** — *"`--log-file` … This is not active by default."* | [rclone obscure](https://rclone.org/commands/rclone_obscure/) · [rclone docs](https://rclone.org/docs/) · [rclone flags](https://rclone.org/flags/) · [rclone mega](https://rclone.org/mega/) · [config encryption](https://rclone.org/commands/rclone_config_encryption_set/) |
| 2 | Q2: *"For how many seconds did the attacker maintain their PowerShell session active?"* | 🔴🔴 **The artifact brackets an ENGINE INSTANCE, not a session.** IDs confirmed in the classic `Windows PowerShell` channel: **400** *"Engine state is changed from None to Available"*, **403** *"Engine state is changed from Available to Stopped"*, **600** provider lifecycle. 🟢 **On by default** — Microsoft: *"By default, only the following event types are enabled: `$LogEngineLifecycleEvent`, `$LogEngineHealthEvent`, `$LogProviderLifecycleEvent`, `$LogProviderHealthEvent`."* 🔴 **But *"this event cannot be strictly correlated to a logon session"*** — every host loading the engine emits its own pair, including the ISE and **any .NET/COM app hosting `System.Management.Automation`**, so one RDP session with three console launches gives **three pairs**. **Last-403 minus first-400 is a plausible-looking wrong answer.** 🟢 Pin by **`RunspaceId`**, corroborate `HostApplication`/`HostName` (`ConsoleHost` local, `ServerRemoteHost` remote), bracket against 4624 t10 / 4634. ⚠️ **4103/4104 are in `Microsoft-Windows-PowerShell/Operational` and module/script-block logging is off by default there** (see **G1** for the three-state nuance). | [MS about_EventLogs](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_eventlogs?view=powershell-5.1) · [Elastic winlogbeat PowerShell module](https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-module-powershell.html) · [qazeer, PowerShell activity](https://notes.qazeer.io/dfir/windows/ttps_analysis/powershell_activity) |
| 3 | *"shadow copies were deleted"* | 🔴🔴 **No dedicated event ID exists, and TWO widely repeated IOCs are wrong.** Detection is process-creation based — Elastic's rule matches `process.name : "vssadmin.exe"` with `process.args : ("delete", "resize")` and `process.args : "shadows*"` — **so the artifact is 4688 with command-line auditing, or Sysmon 1, both off by default (L1).** ❌ **Application event 524 is NOT a shadow-copy artifact** — provider `Microsoft-Windows-Backup`, *"The system catalog was deleted"*, i.e. **backup-catalog** deletion; JPCERT adds that it *"may also occur in normal operation."* ❌ **`volsnap` event 25 is NOT an attacker indicator** — *"The shadow copies of volume %2 were aborted because the diff area file could not grow in time"*, a capacity condition. ⚠️ **Registry / `System Volume Information` remnants: NOT VERIFIED — do not teach.** **T1490 Inhibit System Recovery, tactic Impact**, names the command: *"vssadmin.exe delete shadows /all /quiet"*. ⚠️ On PowerShell 7, `Get-WmiObject`/`Remove-WmiObject` are **removed** (**F5**) — expect `Get-CimInstance … \| Remove-CimInstance` in `PowerShellCore/Operational` (**G2**). | [Elastic VSS rule](https://www.elastic.co/guide/en/security/8.19/volume-shadow-copy-deleted-or-resized-via-vssadmin.html) · [JPCERT](https://blogs.jpcert.or.jp/en/2024/09/windows.html) · [MS volsnap events](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/dd364930(v=ws.10)) · [T1490](https://attack.mitre.org/techniques/T1490/) |
| 4 | *"hidden inside a password-protected archive"* | 🟢🟢 **"Hidden" overstates it — on a default archive the file names, sizes, timestamps and CRC32s are readable without the password.** **ZIP:** encryption covers data only; hiding the central directory needs **Central Directory Encryption**, APPNOTE **bit 13** — *"Set when encrypting the Central Directory to indicate selected data values in the Local Header are masked to hide their actual values."* **7-Zip:** *"Enables or disables archive header encryption. **The default mode is he=off**."* **WinRAR:** *"If you set 'Encrypt file names' option, WinRAR will encrypt not only file data, but all other sensitive archive areas like file names, sizes, attributes, comments and other blocks"* — opt-in. 🟢 **So the staged customer export can be identified without cracking anything**, and a **CRC32 match against the original** ties the archived item to a known file. ⚠️ CRC32 is 32-bit — strong corroboration, not identity. **T1560.001 Archive via Utility, tactic Collection.** | [ZIP APPNOTE 6.3.9](https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.9.TXT) · [7-Zip method docs](https://documentation.help/7-Zip/method.htm) · [WinRAR archive password](https://documentation.help/WinRAR/HELPArcPassword.htm) · [T1560.001](https://attack.mitre.org/techniques/T1560/001/) |
| 5 | *"Which **well-known tool** was used to exfiltrate"* | 🟢 **rclone, and it is well-known for exactly this.** ATT&CK software **S1040**: *"Rclone has been used in a number of ransomware campaigns, including those associated with the Conti and DarkSide Ransomware-as-a-Service operations."* **T1567.002 names the combination outright** — *"Rclone can exfiltrate data to cloud storage services such as Dropbox, Google Drive, Amazon S3, and MEGA."* The DFIR Report documents the identical shape (RDP intrusion → *"Rclone was utilized on multiple file servers to facilitate the exfiltration of data"*). ⚠️ **Tool identity is NOT CONFIRMED for this room** without running the lab — inferred from Q5's mention of Mega. 🔴 **And it is genuinely dual-use: presence is not exfiltration.** | [ATT&CK S1040](https://attack.mitre.org/software/S1040/) · [T1567.002](https://attack.mitre.org/techniques/T1567/002/) · [The DFIR Report, Jun 2025](https://thedfirreport.com/2025/06/30/hide-your-rdp-password-spray-leads-to-ransomhub-deployment/) |
| 6 | ATT&CK for this chain | ✅ **All confirmed, and this is the first room that actually needs the post-v19 log-clearing ID.** **T1685.005 Disable or Modify Tools: Clear Windows Event Logs**, tactic **Defense Impairment (TA0112)** — *"Adversaries may clear Windows Event Logs to hide the activity of an intrusion"* — **not `T1070.001`** (block **K1**). Also: **T1567.002** Exfiltration to Cloud Storage → Exfiltration · **T1560.001** → Collection · **T1490** → Impact · **T1074.001** Local Data Staging → Collection · **T1059.001** PowerShell → Execution · **T1021.001** RDP → Lateral Movement · **T1036.005 Match Legitimate *Resource* Name or Location** → **Stealth** (renamed — block **M5**). ⚠️ **Version date: cite "v19.2", not a date** (block **L7**). | [T1685.005](https://attack.mitre.org/techniques/T1685/005/) · [T1490](https://attack.mitre.org/techniques/T1490/) · [T1036.005](https://attack.mitre.org/techniques/T1036/005/) |

### NOT VERIFIED — carried forward honestly

- **That the tool is rclone.** Inferred from Q5's "Mega"; not confirmed without running the lab.
  §2.4 is written so the artifact reasoning holds regardless of which sync tool it is.
- **Registry or `System Volume Information` remnants of deleted shadow copies** — no primary source.
  **Do not teach.**
- **Whether this room's lab enabled command-line auditing.** If not, Q3's C2 address must come from
  PSReadLine or 4104, not 4688 — and the room does not say.
- **ATT&CK v19.2's release date** — carried from block **L7**; cite the version only.

## 4. Evidence used

**A forensic disk snapshot plus a tool kit, both on the Desktop of an RDP-accessible analysis VM:**
`.\Image\*` and `.\EZTools\*`.

🟢🟢 **This is the first room in the module whose evidence shape matches ours** — an image, analysed
offline, with EZ Tools. **It is what `S4` and `S5` look like.**

- **Downloadable?** ⚠️ **No** — inside the lab VM. **Reusable?** 🔴 **No.**
- **`ecdfp-evidence` action: none.** 🔴 **Fifth room running with no evidence set.** `EVS-10` remains
  unallocated. ⚠️ **The whole module is live-VM-only, confirmed for the fifth time.** **Our Windows
  intrusion image must be staged on `EVI-SRC01` (D19) or sourced from CFReDS (D36) — extraction will
  not supply one.**

### 🔴🔴 Two question-design defects, and together they settle a rule

Room 24 gave us *"no eCDFP question may have a credential as its answer."* **This room shows that
rule was too narrow, in two directions:**

**Q5 — *"What is the obscured password to the attacker-controlled Mega?"*** A password, submitted as
a graded answer. **Second room in the module**, so it is a house pattern rather than an oversight.
⚠️ **And it is a password to a live-service account**, which makes the temptation concrete: a student
who recovers it can log in and look. **That is unauthorised access to a third-party service**, and
the room says nothing about it (§2.5).

**Q6 — *"What is Lucas's email address found in the exfiltrated data?"*** 🔴🔴 **This is worse, and
it is a different category.** The student is asked to open **stolen customer data** and report **a
named individual's personal information** as the answer. In a real engagement the exfiltrated data
set is the most sensitive material in the case — **its contents are the victim's, not the analyst's,
and an answer key containing a data subject's email is a breach of the thing you were hired to
protect.** **D22 makes this ours to care about**: the repo is public and the PII scan is a release
gate, not hygiene.

**The generalised rule, replacing room 24's:**

> **No eCDFP question may have a secret or a data subject's personal information as its answer.**
> Ask *which* account, *which* remote, *which* record — never the value. Ask **"how many customer
> records were in the staged export, and how do you know?"**, never **"what is a customer's email
> address?"** Secrets and PII enter the record **by reference only** — path, offset, timestamp,
> record count — in the restricted appendix.

🟢🟢 **And the replacement questions are strictly better forensics.** *"How many records were in the
export, and what is your evidence?"* exercises §2.6's archive-listing technique, the CRC comparison,
and a stated limitation. *"What is Lucas's email?"* exercises `Ctrl+F`.

⚠️ **One nuance worth keeping:** the module needs Lucas's presence in the exfiltrated data, because
that is how stage 6 targets him (§5.2). **The narrative requirement is real; the question is what is
wrong.** Our version establishes the same fact as *"the export contains records for N employees,
including the lead developer"* — same plot, no PII in the answer key.

### 🔴 The credential in the stale checker — a coincidence that argues for D39

The room's published RDP password is **verbatim one of the literal strings hardcoded in the
`/tmp/verify.py` blocklist** discovered on the device during room 22's verification (**D39**).

**That is the whole argument for D39 in one observation:** the old checker was not a pattern set, it
was **a list of real room passwords** — which means it was itself a credential store, it could not
generalise to a room nobody had seen yet, and **had it ever been committed to a public repo (D22) it
would have been the leak it was meant to prevent.** ✅ The current checker is pattern-based, tested
7/7 with 0 false positives, and lives in `testing/verify_note.py`.

### Critique of the scenario brief

🟢🟢 **The best-constructed brief in the module.** The exfiltration is delivered as a helpdesk ticket
about a missing file — *"Finance says yesterday's customer CSV file vanished from the share"* —
and the room states plainly that *"the attacker … used the distraction to complete the snatch."*

**Detection worked. Routing destroyed it.** Finance observed the *symptom of an exfiltration* and it
became a ticket about a file share. 🟢 **Use this verbatim in `S1`**: it is a better argument for
incident triage than any alert-fatigue slide, and it pairs with room 25's *"the logs looked normal"*
and room 24's *"unstable after we replaced the motherboard"* — **three rooms, three ways an
organisation explains away its own evidence.**

⚠️ **One flaw, and it is the module's habit:** the brief narrates the entire attack before the
student looks — archive, transfer, log wipe, shadow copies. 🟢 **More defensible here than in room
22**, because the objective is explicitly *"prove the exfiltration"*, i.e. **evidence for a stated
claim** (room 21's model). **But our version must mark such text as *given context*, not findings.**

## 5. Lab design worth reusing

### 5.1 🟢🟢 Anti-forensics stated in the brief, not hidden in the evidence

The scenario tells the student **up front** that logs were wiped and shadow copies deleted. **That is
the single best design decision in the module**, and it inverts the usual challenge-room instinct.

**Why it is right:** the exercise stops being *"can you find the log entry"* and becomes ***"the log
entry does not exist — now what?"*** — which is the actual job. It forces the pivot to registry,
`$MFT`, Prefetch and PSReadLine (§2.3, §2.7), and it makes a **negative finding** the expected
deliverable rather than a failure.

🟢🟢 **Adopt for `S6-09`.** Our capstone brief should state the anti-forensic actions and grade the
student on **what they establish anyway, and what they correctly report as unrecoverable.** ⚠️ That
requires the D20 rubric to reward a stated limitation as much as a finding — **which criterion 4
already does.** This is the exercise that makes criterion 4 pay.

### 5.2 ⚠️ CORRECTED — an inference I drew here, and stage 6 refuted

**What I wrote when this room was extracted, and it was wrong:**

Q6 asks for **Lucas's** email address **in the exfiltrated data**, and **Lucas Rivera (Lead
Developer) is stage ⑥** on the module map (room 23 §7) — from which I concluded that *stage 4's loot
is stage 6's targeting*, i.e. the stolen customer export supplied the contact details used to reach
the developer in the final room.

🔴🔴 **Stage 6 says the opposite, in its own words:** *"amidst this primary attack, another critical
compromise took place, this time on a macOS system. Lucas … unintentionally became a victim of a
**different** compromise"*, and — flatly — ***"Not every attack is targeted. Sometimes, your
curiosity makes you fall into a trap."*** **Lucas is compromised by a trojanised "free AI tool"
he found himself. The two intrusions are presented as unrelated.**

🟢🟢 **Recording the error rather than deleting it, because it is the most useful thing in this
section.** The inference was *plausible* — a name appears in stolen data at stage 4 and that same
person is compromised at stage 6 — and it was built on **proximity plus a shared name**, with no
artifact connecting them. **That is exactly the failure mode `shockandsilence.md` §2.8 warns about**
(*"the most dangerous artifact here is the plausible story"*), and I committed it **one room before
writing that warning.**

**What survives the correction, and it is still worth adopting:**

- ⚠️ **The coincidence is real and an investigator must resolve it, not assume it either way.** Two
  compromises, one organisation, one week, and a person who appears in both. **"Related" and
  "unrelated" are both hypotheses; the module asserts the second, and in a real case the assertion
  would need evidence.** 🟢🟢 **That is a better exercise than the chaining device I imagined** —
  give students two incidents and a shared name, and grade them on whether they claim a link.
- 🟢 **`S6-09` should still contain one artifact whose significance is revealed a session later**,
  recorded when found rather than when understood. **The design idea stands; my evidence for it did
  not.**

⚠️ **Take the structure, not the question** — §4.

### 5.3 🟢 Disk image plus tools, on the Desktop

*"All the resources you need are on the user's Desktop"*, `.\Image\*` and `.\EZTools\*`. 🟢 **Copy
this exactly** for our lab hand-outs: evidence and tools in named, predictable paths, and no setup
step between the student and the investigation. ⚠️ **Add what it omits: the image's hash, and a
verify-before-you-start ritual** (**D18**) — the room supplies neither (§4 of `lostinramslation.md`
made the same point about the memory dump).

### 5.4 ⚠️ The template seam is visible

Task 1's heading in this room reads **"Initial Access Pot"** — stage 1's title, left in by
copy-paste. Trivial in itself; 🟢 **worth one line in our review checklist**, because we are
deliberately building six sessions from one template (§5.1 of `initialaccesspot.md`) and **this is
precisely the error that pattern produces.**

### 5.5 🟢 Safety and handling defects

**None new.** Offline analysis of a disk image with supplied tools — **the correct working pattern**,
and the second room running without a defect after three that had them.

🟢🟢 **Rooms 25 and 26 together are the counter-example to block L8's pattern.** Rooms 22, 23 and 24
had students act on the live system; **25 hands over a captured memory image and 26 a captured disk
image.** ⚠️ **The difference is not the room authors' care — it is the stage.** Stages 1–2 are live
response by nature; stages 3–4 are post-incident analysis. **That is worth teaching directly: the
correct handling rule depends on where in the incident you are standing**, and the module walks
through both.

**Running total: 10 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24. Four endanger the analyst's
machine; six endanger the evidence. Unchanged for two rooms.**

## 6. Question patterns

**Six scored questions tracing collection → staging → exfiltration**, with the anti-forensics stated
rather than asked. 🟢 **The set is well ordered** and each answer narrows the next.

**⚠️ No answer formats specified at all** — including on Q2, which asks for **a number of seconds**
and is the question most in need of one. 🔴 **And no timezone**, on a room whose whole objective is
*"unravel the timeline"*.

**🔴🔴 Q5 and Q6 are the two defects that settle our rule** — a password and a data subject's email
address as graded answers. Full argument in §4. **The rule is now: no secret and no PII as an
answer.**

**⚠️ Stems assert conclusions, again** — *"the **attacker's C2** IP address used for staging and
exfiltration"* · *"the **attacker-controlled** Mega"* · *"the well-known tool used **to exfiltrate**
the collected data"*. **Ninth room running.** 🟢 **Mildly more defensible here** than elsewhere,
because the objective is explicitly *prove the stated claim* (room 21's published-chain model).

**🔴 Twenty-sixth room, no "cannot be determined" question** — and this room is the richest source in
the corpus, because **its scenario destroyed two evidence sources on purpose:**

| the room could have asked | correct answer |
|---|---|
| *"Security 1102 is absent. Were the logs cleared?"* | 🔴🔴 **Cannot be determined from its absence** — a second clear removes the first clear's record, and selective deletion never raises 1102. 🟢 **But three structural tells survive:** record-ID discontinuity (a cleared channel restarts at 1), the `.evtx` file's own timestamps, and cross-channel disagreement. |
| *"For how many seconds was the attacker's PowerShell session active?"* — **the room's own Q2** | 🔴🔴 **Not answerable as asked.** 400/403 bracket an **engine instance**; *"this event cannot be strictly correlated to a logon session."* Three console launches give three pairs. **The defensible answer is a bounded range tied to a `RunspaceId`, with the assumption stated.** |
| *"`vssadmin.exe` is in Prefetch. Did the attacker delete the shadow copies?"* | ⚠️ **Not established.** Prefetch proves execution, **not arguments** (**L1**). Without 4688 + command-line auditing or 4104, *delete* versus *list* is unrecoverable. |
| *"Application event 524 is present. Were shadow copies deleted?"* | 🔴🔴 **No — wrong artifact entirely.** 524 is `Microsoft-Windows-Backup`, *"The system catalog was deleted"* — **backup-catalog deletion**. **A trap question that catches a genuinely widespread misconception**, including one I held before this pass. |
| *"The archive is password-protected. What was staged?"* | 🟢🟢 **Determinable without the password** — names, sizes, timestamps and CRC32 are readable on a default ZIP/7z/RAR. **The best row here, because the intuitive answer ("nothing, it's encrypted") is wrong.** |
| *"`rclone.conf` gives the Mega account. Was the data uploaded?"* | 🔴🔴 **Not proven.** The config proves a remote was **configured**; Prefetch proves rclone **ran**; **bytes leaving needs network or provider-side evidence, which is not on this disk.** |
| *"No C2 address appears in any log. Was there no C2?"* | 🔴🔴 **No.** 4103/4104 are off by default, the logs were wiped, and PSReadLine is lossy. **On a well-cleaned host, "not found" is the expected result.** |
| *"The obscured password decodes to X. Is the Mega account the attacker's?"* | ⚠️ **Not established by the credential** — the account being *attacker-controlled* comes from context. 🔴 **And do not test it by logging in** — that is unauthorised access to a third-party service (§2.5). |

🟢🟢 **Eight, and three of them attack the room's own questions.** ⚠️ **The pattern from room 25
holds and strengthens: in rooms 24, 25 and 26 the "cannot be determined" answer is repeatedly the
*correct* answer to a question the room actually asks.** **This is no longer a suggested improvement
to question design — it is a correctness finding about the existing questions**, and the course
rationale should say so in those words.

## 7. Figures

**No room-specific figure.** ⚠️ Images were **not enumerated** for this room — rooms 23–25
established that the module reuses one topology SVG and decorative assets, and the DOM query was not
re-run. **Recorded as not-checked rather than claimed decorative.**

🔴 **Seventh room running with no conceptual figure**, on a room covering archives, cloud
exfiltration, log wiping and shadow copies.

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F23 | **Obfuscation is not encryption** | Three panels, one row each: `rclone.conf`'s obscured `pass` → `rclone reveal` → plaintext; an MD5 hash → *"lookup, not integrity"* (**K7**); an Amcache `FileId` → *"first 30 MB only"* (**L2**). Caption: **"three values that look cryptographic and are not."** | **🔴 P1** | §2.5 — and it consolidates three separate findings into one slide instead of three. |
| F24 | **What survives a password-protected archive** | An archive drawn in two layers: the **central directory / header** shaded *"readable — names, sizes, timestamps, CRC32"*, the **data** shaded *"encrypted"*. Beside it the same archive with `-mhe=on`, both layers dark. | **🔴 P1** | §2.6 — corrects the intuitive wrong answer, and teaches *enumerate before you decrypt*. |
| F25 | **The shape of a cleared log** | Two `.evtx` channels side by side on a time axis: Security starting at **record ID 1** two days into a six-month uptime, LocalSessionManager continuous across the same span, with the disagreement circled. | **🔴 P1** | §2.7 — the three structural tells the attacker cannot remove; serves `S6-06` directly. |
| F26 | **Engine instance ≠ session** | One RDP session bar, with **three** 400/403 pairs inside it from three hosts (`ConsoleHost`, ISE, a .NET app), and a red bracket labelled *"last 403 − first 400 = wrong answer"*. | **🟢 P2** | §2.2 — the specific wrong answer a student under time pressure will give. |
| F27 | **One source removed, four left** | The host as five artifact stores — event logs, registry, `$MFT`/`$UsnJrnl`, Prefetch/Amcache, user profile files. Event logs struck through; the other four intact, with arrows showing which question each still answers. | **🔴 P1** | §2.1 and §2.7, and it is the visual argument for **D25**'s ordering (file systems before timelines). |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 4"* — correct, and it is the module's most useful room for us.

**It is the only stage whose working shape is ours**: a disk image, offline, with EZ Tools. Amend the
Part 1 row to say so, and to note that **its two question-design defects produced the strongest
process rule of the whole extraction** (§4).

### Rows this strengthens

- **`S6-06`** (*"Windows event logs for the timeline — what survives, what is cleared, what is never
  written"*) — 🟢🟢 **the row's title is this room's scenario.** Add §2.7's three structural tells,
  figures **F25** and **F27**, and 🔴 **the corrected ID: log clearing is `T1685.005`, not
  `T1070.001`** (**K1**). **First row in the map that actually needs that correction.**
- **`S5-08`** (*"Recycle bin and Volume Shadow Copies — deleted files and previous versions"*) —
  🔴🔴 **needs the negative result from §2.8**: there is **no dedicated event ID** for shadow copy
  deletion, and **both event 524 and volsnap 25 are wrong answers** widely repeated. **This is a
  correction to what the row would otherwise have taught.**
- **`S3-03`** (*"File signature vs extension — the mismatch, and what it actually proves"*) —
  🟢🟢 §2.6's archive listing belongs beside it as *"enumerate before you decrypt"*, and §2.4's
  renamed-binary discrimination (hash and publisher, not filename) is the same lesson.
- **`S1-06`** (hashing) — 🟢 figure **F23** consolidates `rclone obscure`, MD5-for-lookup (**K7**) and
  Amcache's truncated SHA-1 (**L2**) into one slide: **three values that look cryptographic and are
  not.**
- **`S6-09`** (capstone) — 🟢🟢 §5.1's *anti-forensics stated in the brief* and §5.2's
  *artifact-revealed-later* chaining. **Both are structural, both cost nothing.**
- **`S1-04`** (report template) — §2.8's worked paragraph: finding, method and stated limitation in
  three sentences.
- **`S1`** — the third scenario in a row of an organisation explaining away its own evidence (§4).

### Back-propagation

🟢 **None.** Every ID this room uses was checked: **T1685.005** is new to the repo and correct per
block **K1**; **T1490**, **T1567.002**, **T1560.001**, **T1074.001**, **T1059.001** appear nowhere
yet; **T1036.005** appears nowhere (block **M5**); **T1021.001** only in `elevatingmovement.md`,
already correct. ✅ **`T1070.001` is not used anywhere in the repo** — re-checked, because this is the
first room where it would have been the tempting choice.

⚠️ **One thing to watch rather than fix:** block **K1** and this note both give ATT&CK v19.2 a date;
**L7** says cite the version only. **Consistent across notes; nothing to patch.**

### Minutes

**Net zero in rows.** Everything lands in `S6-06`, `S5-08`, `S3-03`, `S1-06`, `S6-09`, `S1-04`.
**No new rows.**

⚠️ **But `S5-08` gains a correction that changes its content**, and **`S6-06` gains three figures and
an ID change** — so the row-overload watch from room 25 now covers **`S5-06`, `S5-08` and `S6-06`.**
🔴 **Three rows, four consecutive rooms, no row count change.** **The S5 re-split must size rows, not
count them** — restated for the third time, with a longer list each time.

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-first room carrying the S5 overdraft.**

### Out of scope

Odoo administration, Mega's service internals, rclone operation as a tool, and archive password
cracking. ⚠️ **One item sits on the line and should be in:** **the handling rule from §2.5** — that
recovering an attacker's credential does not authorise using it. **It is one sentence in `S1-03`
(what makes evidence defensible) and it is the kind of thing students get wrong enthusiastically.**

### Still unresolved

- **S5 re-split** — twenty-first room; now a **three-row overload list** (`S5-06`, `S5-08`, `S6-06`).
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- **No Windows intrusion image in the Priority-2 set** — fifth confirmation. `EVS-10` unallocated.
- **D19 has no per-session host map** — still gating figure **F7**; §5.2 now adds a second
  requirement: **one artifact whose significance is revealed a session later.**
- **Volatility symbol pre-population on `CLEAN-TOOLS`** (**D2**) — still not done.
- **`ecdfp-case` skill** not installed.
- ⚠️ **`knowledge_base/` exists (corrected in room 25) but no room note has been intaken into it.**

## 9. Links

**Room** — <https://tryhackme.com/room/crmsnatch>
**Module** — Honeynet Collapse, stage 4 of 6. Previous: <https://tryhackme.com/room/lostinramslation>.
Next: <https://tryhackme.com/room/shockandsilence>.
**Companion notes** — `lostinramslation.md` (stage 3) · `elevatingmovement.md` (stage 2 — Matthew's
stolen credentials, used here) · `initialaccesspot.md` (the module map; Lucas is stage ⑥) ·
`windows-network-analysis.md` and `logless-hunt.md` (log-wiping and timeline material) ·
`honeynet-collapse-module.md` (the arc, after stage 6) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **G1–G4**, **I10**, **K1**, **L1**, **L2**, and new block **N**.

**Citations from §3, by finding:**

- #1 rclone — `rclone obscure` <https://rclone.org/commands/rclone_obscure/> ·
  docs and config paths <https://rclone.org/docs/> · flags <https://rclone.org/flags/> ·
  Mega remote <https://rclone.org/mega/> ·
  config encryption <https://rclone.org/commands/rclone_config_encryption_set/>
- #2 PowerShell lifecycle — MS `about_EventLogs`
  <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_eventlogs?view=powershell-5.1> ·
  Elastic winlogbeat PowerShell module
  <https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-module-powershell.html> ·
  qazeer, PowerShell activity
  <https://notes.qazeer.io/dfir/windows/ttps_analysis/powershell_activity>
- #3 shadow copies — Elastic VSS rule
  <https://www.elastic.co/guide/en/security/8.19/volume-shadow-copy-deleted-or-resized-via-vssadmin.html> ·
  JPCERT, Windows event logs <https://blogs.jpcert.or.jp/en/2024/09/windows.html> ·
  MS volsnap events
  <https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/dd364930(v=ws.10)> ·
  T1490 <https://attack.mitre.org/techniques/T1490/>
- #4 archives — ZIP APPNOTE 6.3.9
  <https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.9.TXT> ·
  7-Zip method docs <https://documentation.help/7-Zip/method.htm> ·
  WinRAR archive password <https://documentation.help/WinRAR/HELPArcPassword.htm> ·
  T1560.001 <https://attack.mitre.org/techniques/T1560/001/>
- #5 rclone as tradecraft — ATT&CK S1040 <https://attack.mitre.org/software/S1040/> ·
  T1567.002 <https://attack.mitre.org/techniques/T1567/002/> ·
  The DFIR Report
  <https://thedfirreport.com/2025/06/30/hide-your-rdp-password-spray-leads-to-ransomhub-deployment/>
- #6 ATT&CK — T1685.005 <https://attack.mitre.org/techniques/T1685/005/> ·
  T1074.001 <https://attack.mitre.org/techniques/T1074/001/> ·
  T1059.001 <https://attack.mitre.org/techniques/T1059/001/> ·
  T1036.005 <https://attack.mitre.org/techniques/T1036/005/>
