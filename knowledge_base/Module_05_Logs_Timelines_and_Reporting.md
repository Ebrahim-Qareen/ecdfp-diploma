# Module 05 — Logs, Timelines & Reporting

| | |
|---|---|
| **INE source** | unit 8 — *Log Analysis* (121 pp) · unit 9 — *Timeline Analysis* (53 pp) · unit 10 — *Reporting* (63 pp) |
| **Feeds sessions** | `S1` (the report template) · `S6` |
| **Source text** | [`_source_text/INE_Unit_08_Log_Analysis.md`](_source_text/INE_Unit_08_Log_Analysis.md) · [`_source_text/INE_Unit_09_Timeline_Analysis.md`](_source_text/INE_Unit_09_Timeline_Analysis.md) · [`_source_text/INE_Unit_10_Reporting.md`](_source_text/INE_Unit_10_Reporting.md) |
| **Instructor delivery** | [`instructor/Session_07_Log_and_Timeline_Analysis.md`](instructor/Session_07_Log_and_Timeline_Analysis.md) · [`instructor/Session_08_Reporting_and_CTF.md`](instructor/Session_08_Reporting_and_CTF.md) |

> Condensed reference, our words, from INE's eCDFP courseware. Not published.
> Page cites `[U8 p83–106]` point into the source-text file, which is OCR — check any exact
> string on the source page before putting it in front of students.
> `⚠` marks a value or command that is **not in the INE text** (or that the OCR left uncertain)
> and must be verified against the source page, the vendor documentation, or the lab build
> before it goes in front of a student.

---

## 0 · What this module is for

After this module a student can take a set of Windows event logs and a disk image, produce one
normalised timeline in a single time base, defend which rows are facts and which are inferences,
and hand in a report whose findings a second examiner could re-derive without asking them a
question. It is the only module that touches every other one: it consumes the acquisition record
from S1, the file-system times from S2–S3, the Windows artifacts from S4–S5 and the network
evidence from S6, and turns them into one chronology plus one deliverable. It is also the module
that closes the loop back to session 1 — the report template graded in all six sessions is defined
here, on the fixed four-criterion rubric (**Integrity · Method · Findings · Separation**) that never
changes across the course.

> **Scope line — Linux.** Unit 8 spends §8.3 (pp 21–52) on `cat`, `grep`, `cut` and `awk`, §8.4 on
> Apache under Linux, and §8.6 on syslog from network devices. **Linux host forensics is out of
> scope for this course and is not written up here** — no `/var/log` triage, no journald, no Linux
> account or file-system artifacts, no `/etc/passwd` walkthrough. What *is* in scope, and is
> written up: those same shell tools used **against exported Windows evidence** — a
> `wevtutil` / `Get-WinEvent` text or CSV export, an IIS W3C log, a plaso CSV — where
> `grep | cut | awk | sort | uniq -c` remains the fastest way to count, slice and pivot a few
> hundred thousand lines. §3 lists them in that role only. Web-server logs (Apache and IIS) stay in
> because they are an examinable *log format*, not a Linux host artifact.

---

## 1 · Core concepts

### Log message
- **Definition** — a record a system, device or application writes in response to a stimulus, carrying at minimum a time, a source and a description. `[U8 p8–9]`
- **Why it exists** — logging began as a troubleshooting aid, not a forensic control; its evidentiary value was discovered afterwards. That origin explains almost every weakness in this module: retention is sized for operations, not for investigations, and defaults are tuned to keep disks small. `[U8 p5]`
- **Where it shows up** — text files an editor can open (Apache, IIS, syslog) and proprietary binary containers that need a parser (Windows `.evtx`). `[U8 p12]`
- **Example** — a firewall writes an ACL deny; a disk subsystem writes a hardware failure; Windows writes 4624 when credentials are accepted. `[U8 p9]`
- **In the case (D19)** — the same second of the incident is written down three times: by the endpoint (event log), by the perimeter (syslog / firewall) and by the file system (MACB). Three independent writers of one moment is what makes the timeline defensible.
`[U8 p4–15]`

### Filtering and normalization
- **Definition** — *filtering* includes or excludes messages by content; *normalization* converts differently-formatted messages into one common format. `[U8 p15]`
- **Why it exists** — you cannot compare a `.evtx` record, an IIS W3C row and a syslog line until they share a field structure and a time base. Normalization is what a super-timeline tool does for you; filtering is what you do afterwards.
- **Where it shows up** — plaso's `l2tcsv` output is a normalization product; every `psort` query and every Event Viewer filter is a filtering product.
- **Example** — 4624 (FILETIME/UTC), an Apache line (local time with a `+0800` offset) and a syslog line (no year, no zone) all become one UTC-ordered CSV row set.
- **In the case (D19)** — the master timeline is the normalized set; each session's working view is a filtered copy. **Never filter the master.** Filtering deletes context; a row you filtered out at session 3 is the row you needed at session 6.
`[U8 p15]`

### Windows event log channel (`.evtx` and legacy `.evt`)
- **Definition** — a per-purpose binary log container written by the Windows Event Log service. INE names four: Application, Security, Hardware and System. `[U8 p85]` ⚠ the standard Event Viewer tree shows **Application, Security, Setup, System** plus *Forwarded Events* and hundreds of `Applications and Services Logs` channels — "Hardware Events" is one of the latter, not a peer of the big three. The screenshots on `[U8 p87, p97]` show the standard tree, so the p85 list is loose.
- **Why it exists** — Windows separates audit records from operational records so that security auditing can be secured, sized and cleared independently of application noise.
- **Where it shows up** — Vista and later: `%SystemRoot%\System32\winevt\Logs\*.evtx`. XP and Server 2003: `%SystemRoot%\System32\config\*.evt`. Neither is a text file. `[U8 p91–92]`
- **Example** — `Security.evtx` holds 4624/4625/4720/1102; `System.evtx` holds 7045 and 104.
- **In the case (D19)** — the persistence step (service install) is in *System*, the lateral-movement step (RDP logon) is in *Security*, and the anti-forensics step (clear) is in *Security* on the second host. A student who only opens Security misses half the incident.
`[U8 p84–97]`

### Audit policy — the silence problem
- **Definition** — the administrator-set policy that decides which event categories are written at all. Windows logs comparatively little by default and server editions log more than desktop editions. `[U8 p99–100]`
- **Why it exists** — INE is explicit that logging everything is not the right answer: it makes analysis slower and harder, so somebody chose a subset. `[U8 p100]`
- **Where it shows up** — as *absence*. An event category that was never enabled produces exactly the same empty result as an event that never happened.
- **Example** — no 4688 process-creation records on a workstation almost always means command-line/process auditing was off, not that no process ran.
- **In the case (D19)** — the initial document-execution step leaves no process-creation record; it has to be reconstructed from prefetch, the ShimCache/AmCache set from S4–S5 and the file-system times. Say so in the report's limitations section rather than leaving a hole.
`[U8 p99–101]`

### Timeline and super-timeline
- **Definition** — a timeline lists events from a system in chronological order irrespective of type, location or application, so that sequence supplies the context a single event lacks. A *super-timeline* is the "automatically gather everything" variant. `[U9 p5, p18]`
- **Why it exists** — INE's own example makes the case: accessing a network service, enabling Remote Desktop and creating a user are each an ordinary administrative act; in that order, minutes apart, they are an intrusion. `[U9 p6–8]`
- **Where it shows up** — two approaches, and the course teaches both. **(1) Super-timeline:** collect everything, then reduce (plaso/log2timeline). **(2) Targeted, "the Carvey approach":** decide the question first, then run one tool per artifact class — event logs, registry, prefetch, LNK, file-system metadata. `[U9 p17–20]`
- **Example** — a super-timeline of one workstation image routinely exceeds a million rows; INE warns that even an idle machine generates events (schedulers, file-system checks) which will appear in your output. `[U9 p11, p15]`
- **In the case (D19)** — one image, `EVI-SRC01`, one master super-timeline. The targeted approach is used inside it: the super-timeline finds the window, the targeted tools explain what is in it.
`[U9 p4–20]`

### Temporal proximity
- **Definition** — closeness in time; the working assumption that events clustered tightly around one moment are more likely to be related, and that a time corroborated by several independent artifacts is more likely to be the true time. `[U9 p22–23]`
- **Why it exists** — because timestamps can be altered. INE's argument is explicitly about confidence: *"Because times may be altered, multiple references to a particular time will increase the confidence in that time."* `[U9 p23]`
- **Where it shows up** — as the pivot technique. Anchor on one event you trust, take a window around it, and read everything in the window regardless of source.
- **Example** — a `.lnk` write, a prefetch execution and a 4624 within eleven seconds of each other, from three different parsers, is a corroborated moment; the same three timestamps spread over three days is not a story, it is coincidence.
- **In the case (D19)** — the anchor is the first C2 callout seen in the S6 capture. The window around it contains the document open, the child-process artifacts and the first outbound connection.
`[U9 p21–23]`

### Timestamps, time zone and clock skew — read this before building anything
- **Definition** — a timestamp is a *number in a representation*, plus a *reference frame* (UTC or local), plus the *accuracy of the clock that produced it*. All three have to be known before two timestamps may be compared.
- **Why it exists** — Windows uses several representations at once, some UTC and some local, in the same image. `[U9 p25–26]`

| Representation | Epoch / unit | Frame | Typical home |
|---|---|---|---|
| 64-bit `FILETIME` | 100-nanosecond intervals since 1601-01-01 | **UTC** | file-system times, EVTX `SystemTime`, many registry values `[U9 p25]` |
| 32-bit Unix time | seconds since 1970-01-01 | **UTC** | browser and application data, TLN, many tool outputs `[U9 p25]` |
| String-based | as written in the text | **local** | text logs — Apache, syslog, database logs `[U9 p26]` |
| `SYSTEMTIME` | packed struct fields | **local** | some registry entries and some XP times `[U9 p26]` |

- **Where it goes wrong — the four failures, in the order students hit them:**
  1. **Display ≠ storage.** EVTX stores its times as UTC `FILETIME`; Event Viewer renders them in *the viewing machine's* time zone. A screenshot taken on the examiner's laptop is stamped with the examiner's zone, not the evidence's. ⚠ not stated in the INE OCR — verify once in the lab and then teach it as a rule.
  2. **Self-describing vs not.** An Apache line carries its offset in the bracket (`[16/Oct/2017:13:31:03 +0800]`), so it can be converted with no outside knowledge `[U8 p60–61]`. IIS W3C rows and classic syslog lines carry no zone at all — IIS defaults to GMT/UTC, syslog carries neither a year nor a zone. INE's phrasing on `[U8 p78]` — *"the console uses the GMT time zone unless it was told to use the local time zone"* — blurs this: the **"Use local time for file naming and rollover"** checkbox `[U8 p79]` changes file *naming and rollover*, not the timestamps written inside the rows. ⚠ verify against the IIS build in the lab before teaching either reading.
  3. **The evidence machine's zone is a fact you must recover, not assume.** INE says only *"if you don't know what time zone the system was using, you must check the Windows Registry for that"* `[U9 p46]` and never names the key. It is `HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation` (`TimeZoneKeyName`, `Bias`, `DaylightBias`, `ActiveTimeBias`), with `ActiveTimeBias` the minutes to **add to local time to obtain UTC**. ⚠ key path and bias direction are our addition — verify on the image before use. Note also that the registry gives the zone *at the last write*, and a machine that travelled or was re-zoned mid-incident had a different offset earlier.
  4. **Daylight saving.** Handing a tool a fixed numeric offset (`-05:00`) is wrong for half the year. Hand it a zone *name* (`America/New_York`) so the tool applies the transition itself.
- **Clock skew** — the evidence host's real-time clock may simply be wrong. The only place INE gives you to record it is the sample report's BIOS examination block: *date accurate / time accurate / offset from correct time / what was used as a time reference* `[U10 p59]`. That block is the skew record. Capture it at acquisition, because after the machine is powered down it cannot be recovered.
- **Rule for this course (put it on the S1 handout and enforce it in every session):**
  > Every timestamp in a report, a timeline and a finding is written **`YYYY-MM-DD HH:MM:SS UTC`**.
  > A local time may appear only in parentheses after it. The evidence host's time zone and its
  > measured clock skew are stated **once**, in Method, and applied to every converted value.
  > Two date formats in one report is a defect `[U10 p28]`; two time bases in one timeline is a
  > wrong answer.
- **In the case (D19)** — two hosts, two clocks. `WKSTN-07` and `SRV-FILE01` are correlated only after each host's skew is stated and applied; an uncorrected 90-second skew is enough to put the RDP logon *before* the credential theft that enabled it and invert the whole story.
`[U9 p24–27]` · `[U10 p28, p59]` · `[U8 p78–79]`

### MACB
- **Definition** — the four file times a timeline carries per file: **M**odified, **A**ccessed, **C**hanged (metadata/MFT-entry modified), **B**orn (created). `[U9 p27]`
- **Why it exists** — one file contributes up to four rows to a timeline, and which of the four fired tells you what kind of touch it was.
- **Where it shows up** — INE's mapping `[U9 p27]`:

  | | M | A | C | B |
  |---|---|---|---|---|
  | **FAT** | Written | Accessed | *not available* | File created |
  | **NTFS** | File modified | Accessed | MFT entry modified | File created |

- **Example** — a mactime row rendered `...a.b` means only Accessed and Born fired at that instant: a file that appeared and was read, not written.
- **Caution** — the instructor deck writes the acronym as "MCAB" and orders it *modified / changed / accessed / birth* (Session 7 pt 2, slide 15). The tools emit **MACB**; teach the tool order or students misread every row.
- **Timestomping** — the deck adds the `$STANDARD_INFORMATION` vs `$FILE_NAME` comparison (slides 16–19) as the timestomp test, stating the rule as *"$STD_INFO > $FILE_NAME"*. This is **not in units 8–10**, and the direction is contestable: the common backdating case makes `$STANDARD_INFORMATION` *earlier* than `$FILE_NAME`. Teach it as *"a significant divergence in either direction between the two attribute sets is the signal"*, and leave the MFT mechanics to the file-systems module. ⚠ record the disagreement; do not pick a side in front of students.
`[U9 p27]`

### The report — the only deliverable, and the findings/interpretation split
- **Definition** — the written product of the investigation. INE is blunt: security work is usually non-functional, so the report is the only thing the client receives and therefore the only thing your work is judged by. `[U10 p4–5]`
- **Why it exists** — *"without the proper analysis and reasoning an evidence is nothing but a meaningless piece of data"* `[U10 p17]`. A list of artifacts is not a report; a narrative with no artifacts is not evidence.
- **Where the split lives** — INE's structure separates **Analysis** (`[U10 p35]`) from **Crime reconstruction** (`[U10 p36]`) and warns off absolute terms — *avoid "we are sure", "we are certain"*, because the analysis is the investigator's interpretation and not absolute truth `[U10 p18]`. That is the findings-vs-interpretation split, but INE never names it. **We name it, and we grade it** (rubric criterion *Separation*).
- **Example** — "The Security log contains one 1102 record at 22:14:07 UTC" is a finding. "The attacker cleared the log to hide the RDP session" is an interpretation. They go in different sections, and the second cites the first by number.
- **The hard rule the instructor adds** — *you are not the judge*: never write "in my opinion Mr X committed this crime". Present method and evidence; the decision is not yours (Session 8, slide 30).
- **In the case (D19)** — six sessions produce findings `F-01…`; the final report's interpretation section is the first place they are joined into a story, and each interpretation names the findings it rests on.
`[U10 p4–5, p17–18, p35–36]`

---

## 2 · Artifacts

### Windows Security event log — `Security.evtx`
| | |
|---|---|
| **What it is** | The audit channel: authentication, logon/logoff, privilege use, account and group management, object access. Binary EVTX written by the Event Log service; the highest-value single file in a Windows intrusion case. |
| **Where it lives** | `%SystemRoot%\System32\winevt\Logs\Security.evtx` (Vista+); `%SystemRoot%\System32\config\SecEvent.Evt` (XP / 2003) `[U8 p91–92]`. The live path is read from `HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Security` → `File`, and can be repointed `[U8 p93–95]`. |
| **What it proves** | That the audit subsystem recorded a specific event at the record's own UTC time, with the account name and SID, logon type, logon ID, and — where the schema carries them — the source workstation name and IP. Also that the record sits at a given position (`EventRecordID`) in the channel's sequence. |
| **What it does NOT prove** | It does not prove a human did anything. A 4624 records that credentials were *accepted*, not who typed them, and the OS itself generates service (type 5) and network (type 3) logons continuously with no user present. It equally does not prove the negative: a missing event may mean the category was never audited `[U8 p100]`, the log rolled over at `MaxSize` `[U8 p95]`, the file was repointed, or the record was destroyed — all four produce identical silence, and only one of them means "it did not happen". |
| **How to parse it** | Event Viewer → *Filter Current Log* → Event IDs `[U8 p96, p105–106]`; DeepBlueCLI `.\DeepBlue.ps1 .\security.evtx` (instructor deck, slides 32–33); ⚠ offline CLI `wevtutil qe Security.evtx /lf:true /f:text` or PowerShell `Get-WinEvent -Path .\Security.evtx -FilterHashtable @{Id=4624}` — not in the INE OCR, verify flags in the lab build. |
| **Anti-forensics / false positive** | Clearing (1102) empties the channel in one action; `MaxSize` + *overwrite as needed* retention destroys history with no operator involvement `[U8 p95]`; disabling an audit category stops recording without touching the file; repointing `File` in the registry sends new records somewhere else. False positive: a noisy scheduled task or backup agent produces thousands of type-5 4624s that look like brute-force volume until you read the logon type. |
`[U8 p89–106]`

### Windows System event log — `System.evtx`
| | |
|---|---|
| **What it is** | The channel for events about the operating system and its components — drivers, services, the Service Control Manager, the Event Log service itself, DNS client, resource exhaustion. `[U8 p86]` |
| **Where it lives** | `%SystemRoot%\System32\winevt\Logs\System.evtx` (Vista+); `%SystemRoot%\System32\config\SysEvent.Evt` (XP / 2003) `[U8 p91–92]`. |
| **What it proves** | That a system-level component reported a condition at the recorded UTC time — a service was installed (7045), the log file was cleared (104), a DNS lookup failed (1014), the system diagnosed low virtual memory (2004) `[U8 p86–88]`. |
| **What it does NOT prove** | A System-channel record describes what a component *reported*, not what a user intended, and almost none of these events carry an initiating user. 7045 says a service was registered — it does not say the service ever started, or that its binary is malicious. A 1014 DNS failure does not prove the queried name was attacker infrastructure; it proves resolution failed, which happens constantly on any laptop that moves between networks. |
| **How to parse it** | Event Viewer, same route as Security; DeepBlueCLI accepts the System log as well; ⚠ `Get-WinEvent -Path .\System.evtx -FilterHashtable @{Id=7045}` — not in the INE OCR. |
| **Anti-forensics / false positive** | Cleared independently of Security (its own 104 record); rolls over on its own `MaxSize`. False positive: legitimate software installers create services constantly — a 7045 is only interesting once you look at the image path and the name. |
`[U8 p84–88, p91–97]`

### Windows Application event log — `Application.evtx`
| | |
|---|---|
| **What it is** | The channel applications write to: crashes, error reporting, installer messages, and the application-whitelisting and application-crash categories INE lists as forensically essential. `[U8 p85, p101]` |
| **Where it lives** | `%SystemRoot%\System32\winevt\Logs\Application.evtx`; the registry entry that defines it is the one shown in INE's screenshot — `HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Application`, `File = %SystemRoot%\system32\winevt\Logs\Application.evtx` `[U8 p94–95]`. |
| **What it proves** | That an application reported a condition at that time under that source name — most usefully, that a process crashed, or that an installer ran. Crash records place a *named binary executing* at a moment even when process auditing was off. |
| **What it does NOT prove** | The source name in the record is a string the writing application chose; anything running with the right privileges can write a record claiming to be any source, so this channel authenticates nothing. A crash record proves the process existed at that instant, not what it did, not who started it, and not that the crash was caused by the incident. |
| **How to parse it** | Event Viewer; same offline tooling as the other channels. |
| **Anti-forensics / false positive** | Highest-volume of the three classic channels, so it rolls over fastest — on a busy workstation the Application log may cover days where Security covers months. False positive: routine application errors dominate; the signal is a crash of a process that should never have been running. |
`[U8 p85, p94–95, p101]`

### Legacy `.evt` event logs (Windows XP / Server 2003)
| | |
|---|---|
| **What it is** | The pre-Vista event log format and numbering scheme — a different binary container *and* a different ID space from EVTX. `[U8 p91, p98–99]` |
| **Where it lives** | `%SystemRoot%\System32\config\*.Evt` (`AppEvent.Evt`, `SecEvent.Evt`, `SysEvent.Evt`) `[U8 p91]`. |
| **What it proves** | The same class of facts as EVTX, under old IDs. The conversion INE teaches: many XP security IDs map to the Vista+ ID by **adding 4096** — 528→4624, 529→4625, 624→4720, 632→4728, 636→4732, 680→4776 `[U8 p99, p102]`. |
| **What it does NOT prove** | The +4096 rule is a mapping aid, not an equivalence: INE states plainly that the two systems are **not fully compatible**, because Windows 7/8 introduced events that never existed on XP `[U8 p99]`. So a Vista+ ID with no XP counterpart cannot be "converted backwards", and the absence of an event on an XP box may simply mean that event did not exist in that OS. Nor does the rule extend beyond the Security channel — see the caution on `2949 → 7045` below. |
| **How to parse it** | Event Viewer on a matching OS; Harlan Carvey's `evtparse` for `.evt` and `evtxparse` for `.evtx` `[U9 p49]`; LogParser `[U9 p49]`. |
| **Anti-forensics / false positive** | ⚠ `2949 → 7045` in INE's table `[U8 p102]` is arithmetically consistent with +4096 but 7045 is a *System*-channel Service Control Manager event, not a Security event, and the +4096 shift is a Security-channel phenomenon. Treat the `2949` value as unverified. False positive: opening an `.evt` on a modern Windows without the matching message DLLs renders descriptions as "the description for Event ID … cannot be found" — the record is fine, the renderer is not. |
`[U8 p91, p98–99, p102]`

### Log clearing — event ID 1102 (Security) / 104 (System) / legacy 517
| | |
|---|---|
| **What it is** | The record the Event Log service writes when a log is cleared. **1102** — "the audit log was cleared" — is written into the *Security* channel as the first record of the now-empty log; **104** — "the *&lt;channel&gt;* log file was cleared" — is the equivalent for other channels and names the channel that was cleared; **517** is the pre-Vista Security analogue. ⚠ **None of these three IDs appear in INE's event-ID table** `[U8 p102]`, which lists "Clearing Event Logs" only as an essential *category* `[U8 p101]`. Verify all three against Microsoft's documentation before handing out. |
| **Where it lives** | Inside the channel that was cleared — 1102 in `Security.evtx`, 104 in the affected channel's `.evtx` — as its lowest surviving `EventRecordID`. |
| **What it proves** | That *that channel* on *that host* was cleared, at the record's UTC time, in a session whose account name, domain and logon ID the record carries. Nothing more, and nothing about any other channel: clearing Security does not touch System, Setup, PowerShell/Operational or any `Applications and Services` channel. |
| **What it does NOT prove** | **It does not prove wrongdoing.** Administrators, imaging and build pipelines, and some management tooling clear logs routinely; a 1102 during a maintenance window is normal. **It does not prove who.** The named account is the account whose token was used — impersonation, a stolen token or a service started by the intruder all put someone else's name in the field. **It does not prove the history is gone.** Records may survive in Volume Shadow Copies, in a `ForwardedEvents` collector or SIEM `[U8 p87, p97]`, in backups, or unallocated on disk. **And it does not prove what was destroyed** — you cannot characterise records you never saw. |
| **What its ABSENCE does not prove** | **No 1102 is not evidence that nothing was removed.** Records can vanish with no clear record at all: (a) normal rollover once the channel hits `MaxSize` under *overwrite as needed* `[U8 p95]`; (b) the category was never audited `[U8 p100]`; (c) the file was deleted or replaced offline, with Windows not running, so no service existed to write a record; (d) individual records stripped by a tool that edits the EVTX file directly; (e) the channel disabled or its `File` value repointed in the registry `[U8 p93–95]`. Treat "no 1102" as *consistent with* both an untouched log and a carefully-emptied one. |
| **How to parse it** | Filter the channel for 1102/104 in Event Viewer `[U8 p105–106]`; DeepBlueCLI flags log clearing among its detections (instructor deck, slides 32–33). Then corroborate: ⚠ compare the **earliest surviving `EventRecordID` and its timestamp against the channel's `MaxSize`/`Retention` values** — a channel far below its size limit that nevertheless starts yesterday was emptied, not rolled; and look for **gaps in the record-number sequence**, which is monotonic within a channel, so a jump means records left without a rollover. Both checks are our addition, not INE's — verify. |
| **Anti-forensics / false positive** | This *is* the anti-forensic signal, and the sophisticated version is not to clear at all — stopping the service, repointing `File`, or disabling auditing removes future records and writes no 1102. False positive: a genuine administrative clear, and re-imaged or template-built hosts whose logs legitimately begin at build time. |
`[U8 p95, p100–102]` · ⚠ IDs not in the INE OCR

### Logon and authentication events — 4624 / 4625 / 4648 / 4672
| | |
|---|---|
| **What it is** | The Security-channel account-usage set: **4624** successful logon, **4625** failed logon, **4648** logon using explicit credentials, **4672** special privileges assigned to a new logon. INE's table gives 528→4624 and 529→4625 `[U8 p102]`; 4648 and 4672 appear in INE's and the instructor's screenshots `[U8 p90]`, instructor slides 21, 32. |
| **Where it lives** | `Security.evtx`. In a 4624, the fields that matter are `TargetUserName`, `TargetDomainName`, `LogonType`, `LogonID`, `WorkstationName`, `IpAddress` and `ProcessName`. |
| **What it proves** | That credentials for the named account were accepted (or rejected) by *this* host at that UTC time, by the mechanism the logon type names. The logon ID is the join key: everything that session did later carries the same logon ID. |
| **What it does NOT prove** | The logon type is the whole meaning and students ignore it. ⚠ **Logon types — not in the INE OCR, standard Microsoft values, verify:** 2 interactive (console), 3 network (SMB/share), 4 batch, 5 service, 7 unlock, 8 network cleartext, 9 new credentials (`runas /netonly`), **10 RemoteInteractive (RDP)**, 11 cached interactive. A 4624 does not prove presence at a keyboard unless the type says so; a wall of 4625s does not prove a human brute-forcing, because an expired service password produces the same wall at machine speed; and `IpAddress` is the address that presented the credentials, which behind a jump host or NAT is the jump host. 4672 does not prove privilege was *used* — only that it was granted to the session. |
| **How to parse it** | Event Viewer filter on Event IDs `4624` (instructor slides 30–31); DeepBlueCLI summarises patterns such as repeated admin logons for one account (slide 32); ⚠ `Get-WinEvent -Path .\Security.evtx -FilterHashtable @{Id=4624} \| Where-Object {$_.Properties[8].Value -eq 10}` — not in INE, verify property index against the build. |
| **Anti-forensics / false positive** | Volume is the cover: a normal workstation produces thousands of type-5 and type-3 4624s a day, so a single malicious type-10 hides in plain sight unless you filter by type first. Pass-the-hash and token theft produce a legitimate-looking 4624 for an account whose owner did nothing. |
`[U8 p89–90, p102]` · logon-type table ⚠ not from INE

### Service installation — event ID 7045
| | |
|---|---|
| **What it is** | The System-channel record written by the Service Control Manager when a service is installed. INE lists it as `2949 / 7045 Service Creation` `[U8 p102]` and names "Software and Service Installation" as an essential category `[U8 p101]`. |
| **Where it lives** | `System.evtx`. Carries the service name, the image path, the service type and the start type. |
| **What it proves** | That a service by that name, pointing at that binary path, with that start type, was registered on the host at that UTC time. It is one of the strongest persistence indicators available when process auditing is off, because it survives reboots and names the file. |
| **What it does NOT prove** | Installation is not execution — 7045 does not show the service ever started or did anything; that needs the SCM start/stop records, prefetch, or the binary's own artifacts. It does not prove the binary is malicious: the name and path are attacker-chosen strings and a service named `WinDefendUpd` in a user temp folder is *suspicious*, which is an interpretation, not a finding. ⚠ Whether the installing account appears in the record varies by build — verify against the record's XML in the lab rather than asserting it. |
| **How to parse it** | Event Viewer filter on `7045` in System; ⚠ `Get-WinEvent -Path .\System.evtx -FilterHashtable @{Id=7045}` — not in INE. |
| **Anti-forensics / false positive** | Legitimate installers register services all day; the discriminators are image path (user-writable directories, `AppData`, `Temp`, `ProgramData`), a random or lookalike service name, and `auto start`. Attackers who use a scheduled task, a Run key or WMI persistence instead leave **no 7045 at all** — its absence says nothing about persistence in general. |
`[U8 p101–102]`

### Account and group change events — 4720 / 4728 / 4732 / 4776
| | |
|---|---|
| **What it is** | The account-management set: **4720** a user account was created, **4732** a member was added to a **local** group, **4728** a member was added to a **global** group, **4776** credential validation by the authenticating computer. INE's mapping: 624→4720, 636→4732, 632→4728, 680→4776 `[U8 p102]`. |
| **Where it lives** | `Security.evtx` — on the machine where the change happened: a local account on the workstation, a domain account on the domain controller. |
| **What it proves** | That the account or group membership changed at that UTC time, naming both the subject (who did it) and the target (what changed), including the target SID. DeepBlueCLI surfaces exactly this pair — "New User Created" and "User added to local Administrators group" — with the target SID (instructor slide 33). |
| **What it does NOT prove** | These records prove a change was *made*, never that it was unauthorised — help-desk account creation looks identical to attacker account creation, and only context (hour, subject account, proximity to other events) separates them. 4732 tells you a member was added to a local group; **it does not by itself tell you the group was Administrators** — read the group name in the record rather than assuming. ⚠ INE labels 4776 "Successful Account Authentication" `[U8 p102]`; 4776 is written for *attempted* validation and appears for failures too, carrying an error code — the "successful" label is imprecise, verify. |
| **How to parse it** | Event Viewer filter on the ID set; DeepBlueCLI (slide 33) for a summarised pass. |
| **Anti-forensics / false positive** | If the intruder uses an existing account rather than creating one, none of these fire — a clean account-management history is not a clean host. Local-vs-domain confusion is the standard false positive: a 4720 on a workstation is a *local* account and will never appear on the domain controller. |
`[U8 p101–102]`

### Event log configuration key — `…\Services\EventLog\<Channel>`
| | |
|---|---|
| **What it is** | The registry subkey that defines each classic channel: where its file is, how big it may get, and what happens when it is full. `[U8 p93–95]` |
| **Where it lives** | `HKLM\SYSTEM\CurrentControlSet\Services\EventLog\<Channel>` — e.g. `…\EventLog\Application`. Values visible in INE's screenshot `[U8 p95]`: `File` (REG_EXPAND_SZ, `%SystemRoot%\system32\winevt\Logs\Application.evtx`), `MaxSize` (REG_DWORD `0x01400000` = 20 971 520 bytes = 20 MB), `Retention` (`0x00000000`), `AutoBackupLogFiles` (`0`), `RestrictGuestAccess` (`1`), `PrimaryModule`, `DisplayNameFile`, `DisplayNameID`. ⚠ the newer `Microsoft-Windows-*` channels are configured under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WINEVT\Channels\<Channel>` instead — not in INE, verify. |
| **What it proves** | The configuration of each channel as of the hive's last write: the file's real location, the size ceiling, and the retention behaviour that explains how much history could possibly have survived. This is the key that turns "the log only goes back three days" from a mystery into a calculation. |
| **What it does NOT prove** | It shows the *current* configuration, not the configuration in force when the events of interest were written. A `MaxSize` raised last week says nothing about last month's retention, and an attacker who repointed `File`, collected clean logs and put the value back leaves only the key's LastWrite time as a trace. A dead image shows the last state written before shutdown — nothing about the state during the incident. |
| **How to parse it** | Load the `SYSTEM` hive from the image in a registry viewer and read the subkey per channel; INE demonstrates it in `regedit` on a live host `[U8 p95]`. |
| **Anti-forensics / false positive** | Repointing `File` is a quiet way to stop evidence accumulating in the expected place; shrinking `MaxSize` forces rollover to destroy history without any clear event. False positive: enterprise GPO commonly relocates or resizes logs for entirely legitimate reasons — check the domain policy before calling it tampering. |
`[U8 p93–95]`

### IIS log — W3C extended log file format
| | |
|---|---|
| **What it is** | Microsoft IIS's request log. IIS is on by default in the Windows NT family from NT 4.0 onward, though absent from some editions and not active by default in all of them; INE notes that logging is usually enabled but not always `[U8 p71–72]`. The format is W3C extended — a self-describing text file whose field set the administrator chooses `[U8 p76, p81]`. |
| **Where it lives** | Configured in the IIS management console → *Logging*, which sets one-file-per-server or per-site plus the directory `[U8 p77–78]`. ⚠ the modern default is `%SystemDrive%\inetpub\logs\LogFiles\W3SVC<site-id>\` — **not stated in the INE OCR**, verify on the lab build. Rollover is by schedule or maximum file size, or disabled entirely `[U8 p79]`. |
| **What it proves** | For each logged request: the date and time (GMT/UTC by default `[U8 p78]`), the server IP and port, the method, the URI stem and query, the client IP, the user agent, the referer, and the status/substatus/win32-status and time-taken — as far as the enabled field set goes. The header block makes the file self-parsing: `#Software:`, `#Version:`, `#Date:`, and `#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken` `[U8 p82]` (the OCR mangles `cs-method`). |
| **What it does NOT prove** | A field that is not in `#Fields:` was never *recorded* — that is an administrator's configuration decision `[U8 p81]`, not evidence that the thing did not happen, and students read a missing `cs-username` column as "anonymous" when it may simply be off. `sc-status 200` is the HTTP outcome, never the security outcome: a blocked, sanitised or failed attack can all return 200. `c-ip` is the immediate peer, so behind a load balancer or CDN every request appears to come from the balancer. And the user agent is a client-supplied string, so it identifies nothing. |
| **How to parse it** | Any text tool, because the header names the columns — `grep`/`cut`/`awk` on an export, or LogParser `[U9 p49]`, which speaks W3C natively. Read `#Fields:` first, every time: column positions differ between servers. |
| **Anti-forensics / false positive** | Logging can be turned off per site, fields removed, or rollover set to *do not create new log files* `[U8 p79]` so one file grows and is trivially truncated. ⚠ the *"Use local time for file naming and rollover"* option `[U8 p79]` affects naming and rollover, and INE's `[U8 p78]` wording invites the misreading that it re-bases the row timestamps — verify against the lab build before teaching either reading. |
`[U8 p71–82]`

### Apache access log — combined log format
| | |
|---|---|
| **What it is** | The request log of the Apache HTTP server — a plain-text line per request, one of the two web log formats the course examines. INE: free, open source, cross-platform, ~92 % of copies running on Linux `[U8 p57–58]`. |
| **Where it lives** | ⚠ INE's prose gives `/var/www/apache2/logs` `[U8 p59]`, but **INE's own screenshot two pages later shows a shell prompt of `root@debian:/var/log/apache2#`** `[U8 p67]`, and the instructor's demo screenshots show the same path (Session 7 pt 1, slides 43–44) — `/var/log/apache2` is the Debian/Ubuntu default. **Record the disagreement — do not silently pick one.** INE also notes Apache logs are found in the Apache directory on Windows `[U8 p59]`, which is the case where this artifact is squarely in scope for a Windows examination. |
| **What it proves** | Per line: client IP, timestamp **with an explicit UTC offset**, request line (method, path, query, protocol), status code and response size, then two quoted client-supplied strings. Example `[U8 p60–62]`: `10.108.5.170 - - [16/Oct/2017:13:31:03 +0800] "GET /application/example.php?name=Parameter HTTP/1.1" 200 898 "http://10.100.0.28/" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) …"`. |
| **What it does NOT prove** | ⚠ **INE misreads the tail of the line.** `[U8 p62]` describes the two trailing quoted fields as *"the webserver's IP address (the requested host) and the user-agent"*. In combined log format they are **Referer** and **User-Agent**; the referer in INE's sample merely happens to contain the server's own URL. Teach the correct field list, and note INE's wording so a student meeting it on the exam recognises it. Beyond that: a log entry proves a request *arrived* and what the server *answered* — not that the attack worked (a 200 on an injection string is an HTTP result, not a database result `[U8 p66]`), not who sent it (referer and user agent are attacker-controlled and trivially forged), and not the true client address behind a proxy unless `X-Forwarded-For` is being logged. |
| **How to parse it** | Text tools against an export — `cat access.log \| grep script` for XSS payloads, `grep` for SQL keywords, `AND`/`OR` or `%27` (URL-encoded single quote) for SQLi, `../` plus `/etc/passwd` for traversal, `nc -lvp … -e /bin/bash` for command injection `[U8 p64–68]`; the instructor demonstrates exactly this against a deliberately vulnerable app (slides 43–44). |
| **Anti-forensics / false positive** | `mod_log_forensic` gives a richer record — two lines per request, one after headers are received and one at normal logging time `[U8 p69–70]` — but it is off unless someone enabled it. False positive: keyword grepping is noisy. A URL containing `or` matches every request with "or" in a word; a `<script>` string in a query may be a scanner, a bug bounty, or a user pasting text. A match is a *lead*, not a finding. |
`[U8 p54–70]`

### Syslog record
| | |
|---|---|
| **What it is** | A logging standard that separates the software generating a message, the system storing it, and the software analysing it. Each message carries a **facility** (what produced it) and a **severity**. `[U8 p111, p113]` |
| **Where it lives** | On a collector — INE's small-network model is one log server receiving from router, switch, firewall and application servers `[U8 p17–18]`; the enterprise model puts a per-segment aggregator/collector in front of a central server `[U8 p19–20]`. Sources are network devices and clients `[U8 p112]`. |
| **What it proves** | That the collector received a message claiming a given facility, severity, origin and text at the time it recorded. **Facility codes** `[U8 p114]`: 0 kernel, 1 user, 2 mail, 3 system services (daemons), 4 authentication. **Severity** `[U8 p115]` and instructor slide 26: 0 Emergency, 1 Alert, 2 Critical, 3 Error, 4 Warning, 5 Notice, 6 Informational, 7 Debug — numerically lower is more severe. Setting a level sends that level **and every more-severe level**: level 4 sends 0–4 `[U8 p116]`. |
| **What it does NOT prove** | Classic syslog is unauthenticated and normally rides UDP, so a record proves only that *something* sent a packet the collector accepted: anything on the network can forge a message with any source, facility and text. Delivery is not guaranteed either — an absent message may have been dropped in transit or filtered by the configured severity threshold, so a gap is not evidence of a gap in events. And the classic BSD header carries **no year and no time zone**, so the collector's own clock and zone become part of the evidence. |
| **How to parse it** | Text tools on the collector's files; the device end is configured, on Cisco, with `logging 192.168.1.1` / `logging trap debugging` / `logging on` `[U8 p117]`. |
| **Anti-forensics / false positive** | Raising the trap level silently removes whole classes of message from the record. Flooding the collector with forged low-severity noise pushes real events out of retention. False positive: a device rebooting produces an interface-state storm that looks like an outage everywhere. |
`[U8 p108–117]`

### TSK body file
| | |
|---|---|
| **What it is** | The Sleuth Kit's intermediate, pipe-delimited representation of file-system metadata — one line per file, carrying all four times — from which a timeline is generated. `[U9 p30, p41]` |
| **Where it lives** | A file you create; it does not exist on the evidence. Field order `[U9 p30]`: `MD5\|name\|inode\|mode_as_string\|UID\|GID\|size\|atime\|mtime\|ctime\|crtime`. |
| **What it proves** | What the file system's metadata structures say about each entry at imaging time: name, metadata address, size, and the four times as stored. |
| **What it does NOT prove** | A body file is a *reading* of the file system, not the file system — it proves what the parser extracted from the metadata, and if the parser skipped a structure the line simply is not there. It carries **no `$FILE_NAME` attribute set**, so it cannot be used to test for timestomping. Entries marked `(deleted-realloc)` mean the metadata has been reused, so the name and the times on that line may belong to different files entirely — INE's own sample output is full of them `[U9 p42]`. And an MD5 column is empty unless you asked for hashing. |
| **How to parse it** | ⚠ `fls -r -m "/" <image>  > bodyfile` — INE says only *"you can use `fls` to first create a Bodyfile format"* `[U9 p41]` and shows no command; the flags here are the standard TSK invocation, verify against `fls -h` in the lab. Then feed it to `mactime`. |
| **Anti-forensics / false positive** | Inherits everything done to the file system: timestomping, wiping and anti-forensic tools are invisible at this layer. False positive: bulk file operations (an update, an AV scan, an install) rewrite thousands of times at once and dominate any window they land in. |
`[U9 p30, p41–42]`

### mactime timeline
| | |
|---|---|
| **What it is** | The human-readable, time-ordered rendering of a body file — one row per *time value*, so a single file can produce up to four rows. `[U9 p42]` |
| **Where it lives** | Output you create: `mactime -b bodyfile.csv -d > timeline.csv` `[U9 p42]`. Columns in INE's sample: `Date, Size, Type, Mode, UID, GID, Meta, File Name`, with `Type` the MACB flag string. |
| **What it proves** | That the named metadata entry carried that time value in that MACB position. The flag string is the payload: `..c.` is a metadata change only; `.a.b` is accessed and born; `m...` is a content modification alone. |
| **What it does NOT prove** | Order in this file is order of *stored numbers*, so anything that changed a stored number moves the row and it still looks authoritative. Rows dated **1970** or **1601** are null timestamps, not events — INE's own sample output opens with a block of "Sun May 10 1970" and "Wed May 23 1970" rows `[U9 p42]` that a student will read as 1970 activity. And a mactime timeline contains **only file-system metadata**: no event logs, no registry, no browser history, so its silence about an action means nothing at all. |
| **How to parse it** | Read it in a spreadsheet or a timeline viewer; ⚠ `mactime -z <TZ>` sets the output zone — not shown in the INE OCR, verify. Sort and slice with `grep`/`awk` on the exported CSV. |
| **Anti-forensics / false positive** | Same exposure as the body file. False positive: the `Accessed` time is the least reliable of the four on modern Windows, because last-access updates are commonly disabled — do not build a "the file was opened" story on it without a second artifact. |
`[U9 p42]`

### plaso / log2timeline super-timeline
| | |
|---|---|
| **What it is** | The "gather everything" timeline: a framework that runs many parsers across an image and normalises every timestamp it finds into one ordered set. Originally Kristinn Gudjonsson's Perl `log2timeline`, rewritten in Python as **plaso**. `[U9 p18, p38, p43]` |
| **Where it lives** | Output you create. INE's Perl syntax `[U9 p43]`: `log2timeline -z <timezone> -f <plugin> -r -w <output-file> <mountpoint>/` — `-z` the *source machine's* zone, `-f` plugin or plugin file, `-w` output, `-r` recursive. Examples `[U9 p44, p46]`: `log2timeline -f exif,mft,pdf -o csv -r -w log2time.body /mnt/mountpoint` and `log2timeline -z UTC -f ntuser -w timeline.csv -r "C:\Documents and Settings\<user>"`; a `win7` plugin set applies all Windows 7 plugins `[U9 p45]`, and a custom `.lst` file can hold a plugin list `[U9 p47]`. The output columns in INE's sample `[U9 p48]`: `date, time, timezone, MACB, source, sourcetype, type, user, host, short, desc, version, filename, inode, notes, format, extra`. |
| **What it proves** | That a named parser, reading a named file at a named offset, reported an event of a given type at a given normalised time. The `source`/`sourcetype`/`format` columns are the provenance of every row and are the reason a super-timeline row can be cited in a report at all. |
| **What it does NOT prove** | **A timeline row is a rendering, not an artifact.** It proves what a parser reported, not what the disk holds, and the CSV's confident ordering hides three different failures: a timestomped source lands in the wrong place and looks normal; a skewed or wrongly-zoned host shifts wholesale against every other source; and a missing row may mean "no such event", "no parser for that artifact" or "the parser failed and said nothing". Never cite a super-timeline row as a finding without naming the underlying artifact it came from. |
| **How to parse it** | ⚠ **current plaso — not in INE, verify flags against the installed version:** `log2timeline.py --storage-file case.plaso EVI-SRC01.E01` to build; `pinfo.py case.plaso` to see which parsers actually ran; `psort.py -o l2tcsv -w window.csv case.plaso "date > '2026-03-05 00:00:00' AND date < '2026-03-06 00:00:00'"` to slice; `psteal.py` for a one-shot collect-and-output. Then `grep`/`awk`/`sort`/`uniq -c` the CSV to pivot. |
| **Anti-forensics / false positive** | An idle machine still generates events — schedulers, file-system checks `[U9 p11]` — so noise is the default state, and INE warns that multi-system cases multiply both sources and systems `[U9 p14–15]`. Any artifact class the intruder wiped simply produces no rows, with no marker where they would have been. |
`[U9 p18, p38, p43–48]`

### FTK Imager directory listing export
| | |
|---|---|
| **What it is** | A CSV of every entry in a mounted image, exported straight from FTK Imager — the lightest way to get a file-level timeline with no framework at all. `[U9 p39–40]` |
| **Where it lives** | *Evidence item → Export Directory Listing* `[U9 p39]`. Columns in INE's sample `[U9 p40]`: `Filename, Full Path, Size (bytes), Created, Modified, Accessed, Is Deleted`, with times rendered in **UTC** to microsecond precision. |
| **What it proves** | The name, full path, size, three times and deleted state of every entry the tool enumerated, including `[unallocated space]`, `[orphan]` and NTFS metafiles such as `$MFT`, `$LogFile` and `$BadClus`. |
| **What it does NOT prove** | Three time columns is not four: there is **no MFT-entry-modified column and no `$FILE_NAME` attribute set**, so this export cannot test for timestomping and cannot distinguish a metadata change from a content change. ⚠ which attribute the columns are read from is not stated by INE — verify in the lab build before describing them to students. Deleted-entry rows depend entirely on the tool recovering the metadata entry, so "not listed" never means "never existed". |
| **How to parse it** | Open the CSV in a spreadsheet or Timeline Explorer; sort by the time column of interest; ⚠ note that a spreadsheet will silently reformat these timestamps on import — set the column to text first. |
| **Anti-forensics / false positive** | Same file-system exposure as any metadata listing. False positive: sorting a directory listing by `Created` and reading the top as "the first thing that happened" ignores that most of those rows are OS install artifacts from the build date. |
`[U9 p39–40]`

### TLN five-field timeline
| | |
|---|---|
| **What it is** | The pipe-delimited timeline format used by Harlan Carvey's tools, designed to be trivially parsable and mergeable. `[U9 p50]` |
| **Where it lives** | Output you create, from the WFAT/CLI toolset — `regtime`, `evtparse`/`evtxparse`, `pref`, `lnk`, `jl` `[U9 p49]`. Fields: `Time \| Source \| System \| User \| Description` `[U9 p50]`. |
| **What it proves** | Five things per row, and deliberately no more: when, which artifact class it came from, which host, which user, and a free-text description. The `System` field is what makes multi-host merging possible; the `User` field is what makes per-user filtering possible. |
| **What it does NOT prove** | INE says it directly: **user and description are relatively free-form** `[U9 p50]` — they are whatever the producing tool wrote, so they are not a controlled vocabulary and cannot be relied on for automated correlation across tools. The format also carries no offset, no record number and no hash, so a TLN row on its own cannot be traced back to the exact byte range it came from; you must keep the source artifact. ⚠ the OCR never states the time representation — Carvey's tools normally use Unix epoch seconds, verify before converting. |
| **How to parse it** | Any text tool; the point of the format is that `awk -F'\|'` handles it. Merge multiple hosts by concatenating and sorting on field 1. |
| **Anti-forensics / false positive** | Inherits whatever the per-artifact tool was blind to. False positive: because the description is free text, two tools describing the same event differently will appear as two events after a merge — de-duplicate on time plus system before counting. |
`[U9 p49–50]`

---

### The fixed course report template (S1 handout → graded every session)

*Not an artifact — the deliverable.* This is the section-by-section master an instructor hands out in
session 1 and grades against in all six sessions. It follows INE's report structure `[U10 p30–45]`
and the "good report" criteria `[U10 p47–51]`, reorganised so that each of the four rubric
criteria has a section that owns it. **The rubric never changes: Integrity · Method · Findings ·
Separation.**

| # | Section | Must contain | Owns rubric criterion |
|---|---|---|---|
| 0 | **Cover page** | Case ID, client/requesting party, examiner name and role, report version and date, classification/handling marking. `[U10 p30]` | Integrity |
| 1 | **Table of contents** | Section list with page numbers; plus list of tables and figures. `[U10 p31, p44]` | — |
| 2 | **Executive summary** | ≤ 1 page, non-technical, no jargon: what was asked, what was found, what it means for a decision. Written last, read first — INE calls it the hardest and most important part, and the part a senior non-technical manager reads. `[U10 p32]` | Separation *(no new facts here)* |
| 3 | **Objective and scope** | The client's request and the questions the examination was asked to answer, plus what was explicitly **out** of scope. A case arrives with a scope and an objective, not just evidence (instructor slide 25). | Method |
| 4 | **Evidence and integrity** | One row per exhibit: exhibit ID, description, source host/location, who acquired it and when (UTC), acquisition tool + version, write-blocker/asset tag, hash algorithm and value **at acquisition**, hash **re-verified at analysis**, and the chain-of-custody reference. INE requires serial number, hash value and the acquiring investigator's name/ID plus chain-of-custody data. `[U10 p34, p57–58]` | **Integrity** |
| 5 | **Examination environment and method** | Working copy used (never the original), examination platform, every tool with its **version**, the order in which steps were performed, and the **time basis**: evidence host time zone, how it was determined, measured clock skew and reference used `[U10 p59]`. INE: the analysis section must name the tools, and must be clear and consistent or the report may be refused in court `[U10 p35]`. | **Method** |
| 6 | **Findings** | Numbered `F-01, F-02, …`. Each finding is **one observable fact**, in the past tense, tied to **one named artifact** with its exact location, and a UTC timestamp. No adjectives, no motive, no "suspicious". If it needs the word *because*, it is not a finding. | **Findings** |
| 7 | **Interpretation / analysis** | Numbered `I-01, I-02, …`. Each interpretation states the inference, **cites the finding numbers it rests on**, gives a confidence level, and names at least one alternative explanation that was considered and why it was rejected or could not be excluded. No absolute terms — INE: avoid "we are sure", "we are certain" `[U10 p18]`. | **Separation** |
| 8 | **Timeline / reconstruction** | The events in the order the examiner believes they occurred `[U10 p36]`, one row per step, every time in UTC, every row citing the finding IDs behind it. Multi-host rows state which host's clock and which skew correction. | Separation |
| 9 | **Limitations and what was not done** | Everything not examined and **why**, especially technical reasons `[U10 p24]`; data that did not exist or could not be recovered; artifacts whose absence is explained by policy or retention rather than by non-occurrence. INE notes there is usually no dedicated section for this — **in this course there is, and it is graded.** | **Separation** |
| 10 | **Conclusions** | Answers to the questions in §3 and nothing else. Never a verdict — *you are not the judge*; do not write "in my opinion Mr X committed this crime" (instructor slide 30). `[U10 p37]` | Separation |
| 11 | **Appendices** | Bulky material: full tool output, hash lists, log extracts, witness statements `[U10 p45]`; glossary of acronyms and technical terms `[U10 p43]`; references, checked and current `[U10 p12, p42]`. | Integrity |
| 12 | **Approvals** | Author and approver, signed/digitally signed. `[U10 p60]` | Integrity |

**Optional sections, by client type** — law-enforcement work adds chain-of-custody and evidence-handling
detail `[U10 p38]`; incident work may add a first-responder list ordered by time of arrival with 2–3 lines
of first impressions `[U10 p39–40]`, and a witnesses section with brief statements `[U10 p41]`.

**The two line formats students must be able to write from memory:**

> **F-07** — `System.evtx` on `WKSTN-07`, record 41 992, Event ID 7045, `2026-03-03 09:12:55 UTC`:
> a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

> **I-03** — The service in **F-07** is assessed, with high confidence, to be attacker persistence:
> its name imitates a Microsoft component, its binary sits in a user-writable temp directory, and it
> was installed 41 seconds after the document execution in **F-05**. Considered and not excluded:
> a legitimate third-party installer using a misleading name — no corresponding installer entry was
> found in `Application.evtx`, but the log covers only 6 days (**F-02**).

**Banned in the Findings section:** "clearly", "obviously", "we are sure", "we are certain", "proves that",
"the attacker", "malicious", "unauthorised" — every one of them is an interpretation wearing a finding's
clothes. **Banned everywhere:** two date formats in one report `[U10 p28]`, two terms for one thing
`[U10 p26]`, sentences of 25–30 words `[U10 p23]`, jargon without a glossary entry `[U10 p25]`, and any
sentence assigning guilt.

**Write it as you go.** INE is emphatic: reporting is not a stage that starts when analysis ends, and
reverse-engineering your own work into a report afterwards is how mistakes get in. The report starts
when the investigation starts and is updated as it progresses `[U10 p14–15]`. In this course that means
each session hands in the *same growing document*, not a new one.

---

## 3 · Tools

| Tool | What it is for | Command / entry point | Output | Caveat |
|---|---|---|---|---|
| Event Viewer | Reading and filtering `.evtx` / `.evt` on a live or mounted system | `eventvwr.msc`, or type "event" in the start menu `[U8 p96]`; *Filter Current Log* → level, time, source, Event IDs, keyword, user `[U8 p105–106]` | On-screen records, XML view, filtered save | Renders times in the **viewing** machine's time zone, so screenshots carry the examiner's zone; needs matching message DLLs or descriptions render as "cannot be found" |
| DeepBlueCLI | Fast triage pass over a `.evtx` for known bad patterns | `.\DeepBlue.ps1 .\security.evtx` (instructor slides 32–33) | Date / log / EventID / message / results per detection | PowerShell execution policy prompt on first run; detections are heuristics — every hit needs the underlying record read before it becomes a finding |
| `wevtutil` | Offline query and export of event channels | ⚠ `wevtutil qe Security.evtx /lf:true /f:text`, `wevtutil epl <channel> <file>` — not in the INE OCR | Text / XML / exported `.evtx` | ⚠ verify flags on the lab build; `wevtutil cl` **clears** a log — never demo it on evidence |
| PowerShell `Get-WinEvent` | Scripted filtering of a channel or a file | ⚠ `Get-WinEvent -Path .\Security.evtx -FilterHashtable @{Id=4624}` — not in the INE OCR | Objects, pipeable to CSV | ⚠ property indexes differ per event schema; verify before scripting a logon-type filter |
| LogParser | SQL-style querying of Windows event logs and W3C logs | Named in Carvey's tool list `[U9 p49]` | Table / CSV | Legacy Microsoft tool; still the fastest path for W3C logs, but unsupported |
| Carvey WFAT / CLI tools | Targeted per-artifact timelines in TLN format | `regtime`, `evtparse`, `evtxparse`, `pref`, `lnk`, `jl` `[U9 p49]`; full list at `github.com/keydet89/Tools` | TLN — `Time\|Source\|System\|User\|Description` `[U9 p50]` | ⚠ INE's other link, `code.google.com/p/winforensicaanalysis` `[U9 p38]`, is dead — Google Code closed in 2016 |
| Sleuth Kit `fls` | Extract file-system metadata to a body file | ⚠ `fls -r -m "/" <image> > bodyfile` — INE names the tool but shows no command `[U9 p41]` | Body file `[U9 p30]` | File-system metadata only; no `$FILE_NAME` set, so no timestomp test |
| Sleuth Kit `mactime` | Render a body file as a time-ordered timeline | `mactime -b bodyfile.csv -d > timeline.csv` `[U9 p42]` | CSV: Date, Size, Type(MACB), Mode, UID, GID, Meta, File Name | 1970/1601 rows are null times, not events; `(deleted-realloc)` rows pair a name with reused metadata |
| log2timeline (Perl) | INE's super-timeline builder | `log2timeline -z <tz> -f <plugin> -r -w <out> <mountpoint>/` `[U9 p43]` | CSV / body file | **Superseded.** Teach the syntax because the exam uses it; run plaso in the lab |
| plaso | Current super-timeline framework | ⚠ `log2timeline.py --storage-file case.plaso <image>`; `pinfo.py case.plaso`; `psort.py -o l2tcsv -w out.csv case.plaso "<filter>"`; `psteal.py` — not in INE, verify against the installed version | `.plaso` storage file → `l2tcsv` / dynamic CSV `[U9 p48]` | Hours on a full image; always record which parsers ran (`pinfo.py`) so absence can be explained |
| Timeline Explorer (TLE) | Viewing, sorting, filtering and tagging any timeline CSV | Eric Zimmerman's tooling `[U9 p32, p38]` | Interactive grid | INE notes it imposes **no** structure — the structure is whatever the producing tool wrote `[U9 p32]` |
| FTK Imager | Quick file-level listing without a framework | *Export Directory Listing* `[U9 p39]` | CSV: Filename, Full Path, Size, Created, Modified, Accessed, Is Deleted `[U9 p40]` | Three times only; no MFT-entry-modified column |
| Excel / spreadsheet | Reviewing and colour-coding a timeline | Import the CSV; the SANS colorized super-timeline template is in INE's references `[U9 p53]` | Coloured, filtered sheet | Silently reformats timestamps on import — set time columns to text first; row limits on very large timelines |
| `grep` / `cut` / `awk` / `sort` / `uniq` | **Against exported Windows evidence only** — counting, slicing and pivoting text logs | `cat f.txt \| grep report \| cut -d" " -f5` `[U8 p32–38]`; `awk -F":" '{print $1}'` with `NR` ranges, `printf` formatting and `BEGIN` headers `[U8 p39–52]` | Filtered text | Useless directly against `.evtx` — it is a **binary** format `[U8 p92]`; export to text or CSV first |
| Autopsy | Generating a report from a case | Report generation demonstrated in INE's lab `[U10 p61]` | HTML / Excel / CSV report | A tool-generated report is an appendix, never the report — it contains no interpretation and no limitations |

---

## 4 · Findings vs interpretation — worked from this module

> **FINDING** — `Security.evtx` on `SRV-FILE01` contains 4 118 records; the lowest surviving
> `EventRecordID` is 1, an Event ID **1102** at `2026-03-05 22:14:07 UTC`, with
> `SubjectUserName = svc_backup`. No record precedes it. The channel's `MaxSize` is 20 971 520
> bytes and the file is 3.1 MB.
> **INTERPRETATION** — the Security channel was cleared at that time using a token for
> `svc_backup`; because the file is far below its size ceiling, ordinary rollover does not explain the
> missing history, so the loss is attributed to the clearing action. Assessed as anti-forensic
> activity rather than administration, with moderate confidence, because the account was created
> two days earlier (**F-04**) and the clear fell outside any maintenance window (**F-11**).
> **CANNOT PROVE** — that the person who created `svc_backup` performed the clear (a token can be
> stolen or impersonated); that what was destroyed related to this incident; or that the history is
> unrecoverable — Volume Shadow Copies, the forwarded-events collector, backups and unallocated
> space are all untested until they are tested.

> **FINDING** — `Security.evtx` on `SRV-FILE01`, Event ID **4624**, `LogonType 10`,
> `TargetUserName = svc_backup`, `IpAddress = 192.0.2.37`, `2026-03-05 21:02:44 UTC`.
> **INTERPRETATION** — a Remote Desktop session to `SRV-FILE01` was authenticated for that account
> from the address recorded for `WKSTN-07` (**F-01**), which is consistent with lateral movement
> from the first compromised host.
> **CANNOT PROVE** — that a human was at a keyboard. Type 10 records that a RemoteInteractive logon
> was *authenticated*, not that anything was typed; it does not prove the source host was `WKSTN-07`
> rather than another machine holding that address at that moment; and it says nothing whatsoever
> about what happened inside the session, which needs that session's own artifacts.

> **FINDING** — the super-timeline row for the staged archive's creation reads
> `2026-03-05 17:41:09 UTC`; the examiner's Event Viewer screenshot of the corresponding record
> reads `12:41:09`.
> **INTERPRETATION** — the five-hour difference is the examination workstation's display zone
> (UTC−05:00) applied by Event Viewer at render time; the two records describe one event and no gap
> exists.
> **CANNOT PROVE** — that the evidence host's clock was correct. A display-offset explanation says
> nothing about skew between the evidence machine's real-time clock and true time; that is
> established only by the reference recorded at acquisition `[U10 p59]`, and if it was not recorded
> then, it cannot be recovered now — which is a limitations-section sentence, not a finding.

> **FINDING** — no Event ID **4688** records exist in `Security.evtx` on `WKSTN-07` for any date;
> the audit configuration recovered from the image does not enable process-creation auditing.
> **INTERPRETATION** — process creation could not have been recorded on this host, so the execution
> chain must be reconstructed from prefetch, application-compatibility artifacts and file-system
> times instead.
> **CANNOT PROVE** — that no processes were created. An absence produced by policy is not an absence
> of the event `[U8 p100]`. Any report sentence of the form "there is no evidence that X ran" must
> be written as "process execution was not audited on this host, so execution of X can be neither
> confirmed nor excluded from this channel".

> **FINDING** — the IIS W3C log records `cs-uri-stem /app/item.aspx`,
> `cs-uri-query id=7'+or+1%3d1--`, `c-ip 203.0.113.45`, `sc-status 200`, `time-taken 412`,
> `2026-03-01 08:19:33 UTC`.
> **INTERPRETATION** — an SQL-injection attempt was made against that parameter and the application
> returned a normal page.
> **CANNOT PROVE** — that the injection succeeded. `200` is the HTTP outcome, not the database
> outcome `[U8 p66]`: a successful injection, a sanitised input and a generic error page all return
> 200. Nor does `c-ip` identify a person — behind a proxy or CDN it is the proxy, and the user-agent
> string on the same row is attacker-controlled.

> **FINDING** — a mactime row reads
> `Sun May 10 1970 16:04:53,0,..c.,r/rrwxrwxrwx,0,0,15999-126-1,"C:/Users/<user>/AppData/Local/Microsoft/Feeds Cache/…"`
> (⚠ reproduced from INE's screenshot `[U9 p42]`, whose mode string and path are OCR-garbled — the
> date and the MACB flags are the point, not the exact characters).
> **INTERPRETATION** — the 1970 date is a **null timestamp**, not an event: only the metadata-change
> flag fired and the stored value is at or near the epoch, so the row carries no usable time and is
> excluded from the reconstruction.
> **CANNOT PROVE** — that the file was created, touched or modified in 1970, and equally not that it
> was never touched. The row proves only that the parser read a zero-or-near-zero value out of that
> metadata field; the real activity time, if any, has to come from another artifact.

---

## 5 · Exam-relevant points

- **Log lifecycle vocabulary:** *filtering* = include/exclude by content; *normalization* = convert differently-formatted messages to a common format `[U8 p15]`. To analyse a log you must know **where it is stored, its format, and its structure** `[U8 p14]`.
- **Logging infrastructure:** small network = one log server everything reports to `[U8 p17]`; large network = per-segment **aggregator/collector** feeding a central server `[U8 p19]`.
- **Event log storage:** XP / Server 2003 → `*.evt` in `system32\config`; Vista and later → `*.evtx` in `system32\winevt\Logs`; **not text files — proprietary binary** `[U8 p91–92]`.
- **Relocation:** each log's path lives under `HKLM\SYSTEM\CurrentControlSet\Services\EventLog\<Channel>` and can be changed `[U8 p93–94]`.
- **ID numbering:** XP and Vista+ use different numbers (logoff = **551** on XP, **4647** on Vista+); many XP IDs convert by **+4096**, but the two schemes are **not fully compatible** because Vista+ added new events `[U8 p98–99]`.
- **The ID table to memorise** `[U8 p102]`: 528/**4624** successful login · 529/**4625** failed login · 680/**4776** account authentication · 624/**4720** new user created · 636/**4732** member added to a local group · 632/**4728** member added to a global group · 2949/**7045** service creation.
- **Server editions log more events than desktop installations** `[U8 p99]`; Windows logs comparatively little unless told otherwise, and logging *everything* is explicitly the wrong answer `[U8 p100]`.
- **The seven forensically-essential event categories** `[U8 p101]`: application whitelisting · application crashes · **clearing event logs** · software and service installation · account usage · external media detection · lateral movement detection.
- **Event Viewer filtering** is by level, time, log, source, Event ID (ranges and negations, e.g. `1,3,5-99,-76`), task category, keyword, user and computer `[U8 p105–106]`.
- **Web logs:** Apache ≈ 92 % on Linux `[U8 p58]`; `mod_log_forensic` writes **two lines per request** — one after headers are received, one at normal logging time `[U8 p69–70]`. IIS uses **W3C extended log file format**, fields selectable by the administrator, header block `#Software / #Version / #Date / #Fields` `[U8 p76, p81–82]`; rollover by schedule or size, or disabled `[U8 p79]`; console defaults to **GMT** `[U8 p78]`.
- **Attack strings to grep:** `<script>` for XSS `[U8 p64]`; SQL keywords, `AND`/`OR`, single quotes (URL-encoded **`%27`**) for SQLi `[U8 p66]`; `nc -lvp <port> -e /bin/bash` for command injection; repeated `../` plus `/etc/passwd` for traversal `[U8 p68]`.
- **Syslog:** separates message *generation*, *storage* and *analysis* `[U8 p111]`; every message carries a **facility** (origin) and a **severity** `[U8 p111, p113]`. Facilities 0–4: kernel, user, mail, daemons, auth `[U8 p114]`. Severities 0–7: Emergency, Alert, Critical, Error, Warning, Notice, Informational, Debug `[U8 p115]`. **Setting level N sends 0 through N** `[U8 p116]`. Cisco: `logging <ip>` / `logging trap debugging` / `logging on` `[U8 p117]`.
- **Timeline rationale:** events that are individually ordinary (access a service → enable RDP → add a user) become an intrusion **in sequence** `[U9 p6–8]`. Even an idle system generates events `[U9 p11]`.
- **Two approaches** `[U9 p17–20]`: automatically gather everything (**super timeline**) vs gather specific event types (**the Carvey approach**, objective-driven, one tool per artifact class).
- **Temporal proximity** = closeness in time; because times may be altered, **multiple references to a time increase confidence in it** `[U9 p22–23]`.
- **Time formats** `[U9 p25–26]`: 64-bit **FILETIME** = 100-ns intervals since **1601-01-01**, UTC · 32-bit **Unix** = seconds since **1970-01-01**, UTC · **string-based** = local · **SYSTEMTIME** = local, used in some registry entries and some XP times.
- **MACB by file system** `[U9 p27]`: FAT — Written / Accessed / *n-a* / File created; NTFS — File modified / Accessed / MFT entry modified / File created.
- **Six timeline components** `[U9 p29]`: timestamp, source, source type, type, MACB, description. **Source field values** `[U9 p33]`: FILE, EVT/EVTX, REG, PRE, LNK. **System field**: name, host, IP, MAC `[U9 p34]`. **User field**: user, SID; users are often tied to registry entries `[U9 p35]`.
- **Body file structure** `[U9 p30]`: `MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime`. **TLN**: `Time | Source | System | User | Description`, pipe-delimited, five fields, user and description free-form `[U9 p50]`.
- **log2timeline switches** `[U9 p43]`: `-z` source time zone · `-f` plugin/plugin file · `-w` output file · `-r` recursive. If you do not know the zone, **check the registry** `[U9 p46]`.
- **Report structure order** `[U10 p30–37]`: cover/title → table of contents → executive summary → objective → evidence (serial, hash, acquirer, chain of custody) → analysis (tools named) → crime reconstruction → conclusion; then references `[U10 p42]`, glossary of acronyms `[U10 p43]`, list of tables and figures `[U10 p44]`, appendices for bulky material `[U10 p45]`.
- **What makes a report good** `[U10 p47–51]`: it helps decision-makers decide; **one report serves every audience** — needing separate versions for management and IT means something is wrong; the higher the ratio of evidence-supported claims to assumptions, the more reliable it is in court; and it must be understandable across backgrounds, which is why figures, charts and statistics are recommended.
- **Report style rules** `[U10 p18, p22–28]`: past tense · no absolute terms ("we are sure", "we are certain") · no jargon · consistent terminology, formatting and **date/time format** · avoid 25–30-word sentences · **document what you did not do and why**.
- **Reporting is continuous, not a final stage** — never reverse-engineer the work into a report afterwards `[U10 p14–15]`; check that references are current, because a claim true in 2016 may be false in 2017 `[U10 p12–13]`.
- **The sample report** `[U10 p54–60]` is a US government form: case information, involved persons, summary, evidence submitted, **software utilised (licensed and validated)**, per-item examination, **hash of original evidence** (MD5/SHA1) taken through a hardware write blocker before anything else, forensic imaging with image-vs-original hash comparison, malware scan, drive geometry, **BIOS date/time examination with the offset and the time reference used**, examination of files, evidence disposition, examiner's conclusion, attachments, approvals.

---

## 6 · Teaching notes

**Demo live (S6, in this order):**
1. **The time-zone demo, first, before any tool.** Open the same `Security.evtx` in Event Viewer on two machines set to different zones and show the same record with two different times. Then open the record's XML and show the stored `SystemTime` is UTC in both. Nothing else in this module lands until students have seen this.
2. `grep` an `.evtx` directly and get nothing useful — then export and grep the export. Fifteen seconds, and it permanently kills "I searched the log and it wasn't there" `[U8 p92]`.
3. Event Viewer → *Filter Current Log* → `4624`, then read the **logon type** field aloud for each hit and sort them into "human" and "machine" (instructor slides 30–31).
4. DeepBlueCLI over a supplied `security.evtx` (instructor slides 32–33) — then immediately open one of its hits in Event Viewer, so that "the tool said so" never becomes a finding.
5. `fls` → `mactime` on a small image, and point at the 1970 rows in the output `[U9 p42]`.
6. `psort.py` slicing a pre-built `.plaso` down to a one-hour window around a known anchor — build the full timeline *before* class, it takes hours.
7. The rewrite exercise: hand out five badly-written sentences, have the room split each into `F-nn` and `I-nn`.

**Leave to homework:** the full `log2timeline.py` run on `EVI-SRC01`; the `awk`/`printf` formatting
material from `[U8 p39–52]` (students can read it — it is a shell tutorial, not forensics); writing
`F-01…F-05` from a supplied `.evtx`; the syslog facility/severity tables.

**Where students reliably go wrong:**
- **Time zone, every single cohort.** They screenshot Event Viewer on the examination workstation and report the displayed time as the evidence time. Enforce the UTC rule from §1 in every session's marking, not just S6.
- **Treating a super-timeline row as evidence.** The CSV looks authoritative, so it gets cited directly. Require every finding to name the *underlying artifact*, with the timeline row as the pointer that found it.
- **"The log was cleared, so they're guilty."** Work through the 1102 table in §2 line by line; then ask what the *absence* of 1102 would have proved. The correct answer — nothing — is the one they never volunteer.
- **Confusing "not recorded" with "did not happen."** Make them phrase every negative finding as a statement about the *recording*, never about the world.
- **Building the timeline first and asking the question afterwards.** A four-million-row timeline with no anchor is unusable. Teach anchor → window → widen, using temporal proximity `[U9 p22]` as the justification.
- **Filtering the master timeline.** Filtered views are working copies; the master is never edited.
- **Grepping for keywords and calling the hits findings.** `grep or` matches every URL containing the letters "or". A match is a lead.
- **Report: pasting tool output under a heading called "Findings".** Tool output goes in an appendix; a finding is a sentence a human wrote that cites it.
- **Report: absolute language and verdicts.** "We are certain" and "in my opinion the suspect is guilty" both cost marks — INE bans the first `[U10 p18]`, the instructor bans the second (slide 30).
- **Report: writing it at the end.** They will try. INE's warning about reverse-engineering the work into a report `[U10 p14–15]` is the argument; requiring the *same* document to grow across all six sessions is the enforcement.
- **Two date formats in one document.** Mark it down every time `[U10 p28]`.

**Marking shortcut for the four criteria:** Integrity → is there a hash at acquisition *and* a
re-verification? Method → could a second examiner repeat this with the tool versions named? Findings →
pick any finding at random: does it name one artifact and contain no inference? Separation → does the
limitations section exist and say something real, and does every interpretation cite finding numbers?

---

## 7 · Gaps, cautions and disagreements

**Topics the course needs that units 8–10 do not cover** (each becomes a gap row):

1. **Sysmon** — no mention anywhere. The `Microsoft-Windows-Sysmon/Operational` channel (process creation with hashes and command lines, network connections, file creation, registry changes) is how a modern examiner reconstructs D19's execution and beacon steps. Needs its own source.
2. **Process-creation auditing (4688) and command-line logging** — absent from INE's ID table, yet it is the single most useful Security event for an execution chain.
3. **PowerShell logging** — script-block (4104), module and transcription logging, and the legacy `Windows PowerShell` channel. Not covered; increasingly the only record of what an intruder actually ran.
4. **RDP-specific channels** — `TerminalServices-LocalSessionManager/Operational` and `RemoteConnectionManager`. S5's lateral-movement story needs session start/reconnect/disconnect records, not just 4624 type 10.
5. **USB and removable-media events** — INE names "external media detection" as an essential category `[U8 p101]` and then never gives an event ID or a registry key for it. D19 **ends in exfiltration to USB**, so this gap sits directly on the course's climax.
6. **EVTX internals and record recovery** — no coverage of the file's chunk/record structure, of carving event records from unallocated space, or of recovering records after a clear. This is what turns 1102 from a dead end into a lead.
7. **Log-clearing event IDs themselves** — 1102 / 104 / 517 are *not in INE's tables*; only the category name appears `[U8 p101]`. We supply them; they need a citable source of their own.
8. **Logon types** — the 2/3/5/10 table is not in the OCR, yet no 4624 can be interpreted without it.
9. **Retention arithmetic** — `MaxSize` and `Retention` are shown in a screenshot `[U8 p95]` but never used to reason about how far back a log can possibly reach. That calculation is the honest answer to "why does the log start on Tuesday".
10. **Clock-skew procedure** — beyond the sample report's BIOS checkbox `[U10 p59]`, there is no method for measuring, recording or applying skew, and nothing at all on correlating two hosts with two different skews.
11. **The time-zone registry key** — INE says "check the Windows Registry" `[U9 p46]` and never names it. Also nothing on Windows Time/NTP evidence or DST transitions.
12. **Modern plaso** — the whole of `[U9 p43–47]` teaches the retired Perl `log2timeline`. The current workflow (`log2timeline.py` → `.plaso` storage file → `psort.py`/`psteal.py`, `pinfo.py` for parser provenance) is absent.
13. **Timeline reduction technique** — INE says the timeline will be huge and you must "figure out a duration to focus on" `[U9 p15]` and then gives no method: no filtering strategy, no known-good noise reduction, no worked pivot.
14. **Timeline Explorer in practice** — named `[U9 p32, p38]` with no workflow: no tagging, no bookmarking, no multi-file correlation.
15. **A worked report** — `[U10 p52–60]` is a blank US-government form, not a completed report. There is no example of a well-written finding, and the findings-vs-interpretation split is implied by the section order but never named or taught.
16. **Report integrity mechanics** — nothing on exhibit numbering schemes, on hashing the report itself, or on how chain-of-custody documentation is structured beyond "include it" `[U10 p34]`.
17. **Testimony and admissibility** — court attendance is mentioned once as a time cost `[U10 p11]`; nothing on expert-witness standards, on how a report is challenged, or on what makes an analysis section survive cross-examination beyond "clear and consistent" `[U10 p35]`.
18. **Anti-forensics generally** — apart from log clearing being named as a category, units 8–10 cover none of it. Timestomping appears only in the instructor deck (Session 7 pt 2, slides 16–19), not in the INE units.
19. **SIEM / centralised analysis** — the infrastructure diagrams `[U8 p17–20]` stop at "logs go to a server". No query workflow, no correlation, no discussion of the collector as an evidence source that survives a local clear.
20. **Correlating web and network evidence** — units 7 and 8 never meet: no worked example joining an IIS/Apache row to a packet capture, which is exactly the join S6 needs.

**Dated or dead material:**

21. The NSA reference `www.iad.gov/iad/library/reports/spotting-the-adversary-with-windows-event-log-monitoring.cfm` `[U8 p103]` — **iad.gov no longer serves this**; the guidance moved to NSA's own site and has been superseded. Replace the link before it appears on a slide.
22. `code.google.com/p/winforensicaanalysis/downloads/list` `[U9 p38]` — **Google Code shut down in 2016**. Carvey's tools are at `github.com/keydet89/Tools`, which INE also cites `[U9 p49]`.
23. The Perl `log2timeline` syntax `[U9 p43–47]` — superseded by plaso (see gap 12). Teach INE's syntax for the exam; run plaso in the lab and say which is which.
24. INE's "no known remote exploits on Windows 7 … a vulnerability was discovered earlier this year" `[U10 p13]` dates the unit to roughly 2017. Use it as INE intends — a lesson about stale references — but do not repeat the claim as current.
25. The IIS screenshots are IIS 10 on a Windows 10 desktop and the Event Viewer screenshots are Windows 7/8-era; menu paths shift on Server 2019/2022 and Windows 11. Re-shoot before use.

**Disagreements and source defects — record these, do not silently correct them:**

26. **Apache log path — INE contradicts itself.** The prose on `[U8 p59]` says `/var/www/apache2/logs`; the screenshot on `[U8 p67]` shows INE's own shell sitting in `/var/log/apache2`, and the instructor's demo agrees (slides 43–44). `/var/log/apache2` is the Debian/Ubuntu reality. Show both; INE's prose is what an exam question would echo.
27. **Apache field misread.** INE `[U8 p62]` calls the second-to-last quoted field "the webserver's IP address (the requested host)". In combined log format it is the **Referer**; the sample's referer merely contains the server URL. Correct in teaching, flag as INE's wording.
28. **Body file vs plaso structure.** `[U9 p30]` and `[U9 p31]` give the **identical** field string for the Sleuth Kit body file and for log2timeline output. That cannot both be right — the plaso sample on `[U9 p48]` clearly shows `date, time, timezone, MACB, source, sourcetype, type, user, host, short, desc, version, filename, inode, notes, format, extra`. Treat `[U9 p31]` as a slide error.
29. **`2949 → 7045`.** `[U8 p102]` The arithmetic fits +4096, but 7045 is a *System*-channel Service Control Manager event and the +4096 shift is a Security-channel phenomenon. Treat `2949` as unverified; do not put it on a quiz.
30. **`4776` labelled "Successful Account Authentication".** `[U8 p102]` 4776 is written for credential-validation *attempts* and appears with an error code on failure. The label is imprecise.
31. **"Four separate files: Applications, Security, Hardware and System."** `[U8 p85]` The standard Windows Logs set is Application, Security, **Setup**, System (plus Forwarded Events) — and INE's own screenshots `[U8 p87, p97]` show exactly that, with "Hardware Events" sitting under *Applications and Services Logs*. Use the screenshots.
32. **IIS local-time wording.** `[U8 p78]` — "the console uses the GMT time zone unless it was told to use the local time zone" — reads as if a setting re-bases the row timestamps, while the option shown on `[U8 p79]` is explicitly *"Use local time for file naming and rollover"*. Verify against the lab build; this one produces wrong timelines.
33. **MACB vs "MCAB".** The instructor deck (Session 7 pt 2, slide 15) uses "MCAB" ordered modified/changed/accessed/birth. Tools emit **MACB**. Teach the tool order.
34. **Timestomp direction.** The deck's rule (slide 19) is *"$STD_INFO > $FILE_NAME"*; the common backdating case produces `$STANDARD_INFORMATION` **earlier** than `$FILE_NAME`. Teach "significant divergence in either direction", and note that this material is instructor-added — it is not in units 8–10.

**OCR the machine left unusable:**

35. `[U8 p104]` — the "Vista and above Events" table lost its right-hand column almost entirely ("Windows Update installed 0 and 9", "Hotpatching Error", "Kernel Filter Driver", "Printing Activities" with blank IDs). **Do not reconstruct these IDs from memory** — pull the page.
36. `[U8 p115]` — the severity table OCR drops severities 0, 1 and 3; the instructor deck (slide 26) has the complete 0–7 list and is used above.
37. `[U8 p10]`, `[U8 p18]`, `[U8 p20]`, `[U9 p37]`, `[U10 p2]` — diagram/title pages with no recoverable text. Nothing lost that matters, but they are why some page ranges below cite fewer pages than they span.
38. Instructor screenshots contain the presenter's own account name, email address, machine name and local working paths (Session 7 pt 1, slides 32–33). **None of it is carried into this file, and none of it goes on a slide** — regenerate those screenshots on the lab build before the session.

---

## 8 · Section index → source pages

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `8.1` | Introduction | 3–15 | §1 *Log message*, *Filtering and normalization*; §5 |
| `8.2` | Logging Infrastructure | 16–20 | §2 *Syslog record* (where it lives); §5; §7 gap 19 |
| `8.3` | Using Linux Tools for Log Analysis | 21–52 | §3 (`grep`/`cut`/`awk` row) and §0 scope line — **tools only**; Linux host forensics out of scope |
| `8.4` | Web Logs | 53–82 | §2 *IIS log*, *Apache access log*; §5; §7 items 26–27, 32 |
| `8.5` | Windows Events | 83–106 | §1 *Windows event log channel*, *Audit policy*; §2 (nine event-log artifacts); §5; §6 |
| `8.6` | Syslog | 107–121 | §2 *Syslog record*; §5 |
| `9.1` | Introduction | 3–11 | §1 *Timeline and super-timeline*; §6 |
| `9.2` | Event Types | 12–15 | §1 *Timeline and super-timeline*; §7 gap 13 |
| `9.3` | Approaches | 16–20 | §1 *Timeline and super-timeline* (two approaches); §5 |
| `9.4` | Temporal Proximity | 21–23 | §1 *Temporal proximity*; §6 |
| `9.5` | Timestamp Types | 24–27 | §1 *Timestamps, time zone and clock skew*; §1 *MACB*; §5 |
| `9.6` | Timeline Fields | 28–36 | §2 *TSK body file*, *TLN five-field timeline*; §5; §7 item 28 |
| `9.7` | Creating Timelines | 37–53 | §2 *mactime*, *plaso super-timeline*, *FTK Imager directory listing*; §3; §7 items 12, 22–23 |
| `10.1` | Introduction | 3–8 | §1 *The report — the only deliverable* |
| `10.2` | Tips on Reporting | 9–20 | §2 report template (§§2, 5, 7, 9 of the template); §5; §6 |
| `10.3` | How to Write a Report | 21–28 | §2 report template (banned-phrase list, "write it as you go"); §5 |
| `10.4` | Report Structure | 29–45 | §2 report template (the whole section table); §5 |
| `10.5` | What is a Good Report? | 46–51 | §2 report template (rubric mapping); §5; §6 marking shortcut |
| `10.6` | Report Samples | 52–63 | §2 report template §§4–5 and 12; §1 *Timestamps* (BIOS skew block); §7 gap 15 |
