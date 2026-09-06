# Instructor Session 07 — Log and Timeline Analysis (delivered in two parts)

| | |
|---|---|
| **Deck** | `Resources/Instructor/session 7 part 1.pdf` — 47 slides, 31 screenshots · `Resources/Instructor/session 7 part 2.pdf` — 21 slides, 13 screenshots |
| **INE material covered** | units 8–9 — see [`Module_05_Logs_Timelines_and_Reporting.md`](../Module_05_Logs_Timelines_and_Reporting.md) |
| **Feeds eCDFP session** | `S6` |
| **Source text** | [`../_source_text/Instructor_Session_07_part1_Log_Timeline_Analysis_part_1.md`](../_source_text/Instructor_Session_07_part1_Log_Timeline_Analysis_part_1.md) · [`../_source_text/Instructor_Session_07_part2_Log_Timeline_Analysis_part_2.md`](../_source_text/Instructor_Session_07_part2_Log_Timeline_Analysis_part_2.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

Slide ranges below are labelled `pt1 s…` (session 7 part 1, 47 slides) and `pt2 s…` (session 7
part 2, 21 slides) so the two decks stay distinguishable.

## 0 · Shape of the session

One session, two decks. **Part 1 is log analysis**: the first three-fifths is lecture (`pt1 s3–27`
— what a log is, message types and formats, where logs live, filtering and normalization, central
logging, web logs, Windows event logs, syslog), then a slide that literally reads "Lab time"
(`pt1 s28`) after which the deck is screen work to the end — Event Viewer, DeepBlueCLI, an IIS
build-out, a shell pipeline, and four investigations against a running vulnerable host.
**Part 2 is timeline analysis and is almost entirely lecture**: sequence-beats-single-event,
the two collection approaches, temporal proximity, time formats, MACB and the two NTFS attribute
sets, with exactly one tool screenshot at the very end (`pt2 s20`). Part 2 runs **no timeline
tool at all** — no plaso, no `fls`/`mactime`, no Timeline Explorer — which is the single largest
gap in the pair (§5).

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| `pt1 s1–2` | Title; 8-session course outline; standing announcement of the closing CTF challenge | `admin` |
| `pt1 s3` | Section title — "Session 7: Log analysis" | `admin` |
| `pt1 s4–8` | Why logs matter; what a log and a log message are; stimuli differ by source | `concept` |
| `pt1 s9–13` | Message types; text log formats; database transaction logs; locating logs; filtering and normalization | `concept` |
| `pt1 s14` | Central logging interface — log server fed by router, switch, firewall, application server | `concept` |
| `pt1 s15–19` | Web logs; Apache combined-format entry walked field by field; `mod_log_forensic` | `concept` |
| `pt1 s20–23` | Windows event logs; Security channel in Event Viewer; the EventLog registry key; legacy/modern event ID table | `concept` |
| `pt1 s24–27` | Syslog: origin (facility) codes, severity codes, Cisco device configuration | `concept` |
| `pt1 s28` | "Lab time" divider | `admin` |
| `pt1 s29–31` | Event Viewer: launch, *Filter Current Log* on `4624`, read one record | `demo` |
| `pt1 s32–33` | DeepBlueCLI triage of a Security log | `demo` |
| `pt1 s34–37` | IIS: enable the Windows feature, IIS Manager, open a W3C log, field-selection dialog | `demo` |
| `pt1 s38–41` | Shell text processing — `cat` → `grep` → `cut` over saved scan output | `demo` |
| `pt1 s42` | Apache log location restated | `concept` |
| `pt1 s43` | Investigating XSS in an Apache access log | `demo` |
| `pt1 s44` | Investigating SQL injection in the same log | `demo` |
| `pt1 s45` | Investigating an "RCE exploit" — evidence shown is an FTP daemon log | `demo` |
| `pt1 s46` | Checking the host time zone to establish current date/time (no screenshot) | `concept` |
| `pt1 s47` | Relational database transaction logs — PostgreSQL | `demo` |
| `pt2 s1–3` | Title; course outline; section title — "Session 7: Timeline analysis" | `admin` |
| `pt2 s4–6` | Individually-normal events become an intrusion in sequence; what belongs in a timeline | `concept` |
| `pt2 s7–10` | Two approaches — gather everything (super timeline) vs gather specific events (the Carvey approach) | `concept` |
| `pt2 s11–12` | Temporal proximity; repeated references to a time raise confidence in it | `concept` |
| `pt2 s13` | Time formats — 64-bit FILETIME and 32-bit Unix time | `concept` |
| `pt2 s14–16` | Timestamps in NTFS and FAT; the MCAB mnemonic; stored in `$STANDARD_INFORMATION` and `$FILE_NAME` | `concept` |
| `pt2 s17–18` | Windows time-rules matrices — which operation changes which time, per attribute set | `concept` |
| `pt2 s19` | Detecting a timestomp attack from the two attribute sets | `concept` |
| `pt2 s20` | FTK Imager — Export Directory Listing | `demo` |
| `pt2 s21` | Close | `admin` |

## 2 · Labs and demos — what was actually run

### Event Viewer — filter the Security channel on 4624 · `pt1 s29–31`
**Tools:** Windows Event Viewer, opened from the Start-menu search box. The deck never shows
`eventvwr.msc` or any command line.
**Evidence used:** the **live** Security channel on the presenter's own workstation — 30,234 events
in the earlier screenshot (`pt1 s21`), 34,058 in the lab screenshot (`pt1 s31`). On the course lab
this must become a supplied `.evtx`, not a live machine (§6).
**Steps as demonstrated:**
1. Type `event viewer` into the Start-menu search box and open the result (`pt1 s29`).
2. *Filter Current Log* on the Security log, Event ID box filled with `4624` (`pt1 s30`). The
   dialog's own hint text is legible on the slide and is worth reading aloud, because it is the
   whole filter syntax: `Enter ID numbers and/or ID ranges separated by commas. To exclude
   criteria, type a minus sign first. For example 1,3,5-99,-76`. Other filter axes visible: level
   (Critical / Error / Warning / Information / Verbose), *Logged* time range, by log, by source,
   task category, keywords, user, computer.
3. Open one filtered record in the detail pane (`pt1 s31`).
   **What the output showed:** `An account was successfully logged on`, `Security ID: SYSTEM`,
   `Logon Type: 5`, `Restricted Admin Mode: -`, `Source: Microsoft Windows security`,
   `Event ID: 4624`, `Task Category: Logon`, `Level: Information`,
   `Keywords: Audit Success`, `User: N/A`, `OpCode: Info`, `Logged: 12/2/2024 1:35:30 AM`.
   The Account Name, Account Domain and Computer fields are the presenter's own and are **not**
   reproduced here — see §6.
**What this lab teaches:** the Event Viewer filter is the cheapest possible pivot from 30,000
events to the handful that answer a question — and the displayed time is the *viewing* machine's
local time, which is why §1 of the module insists on UTC.

### DeepBlueCLI triage of a Security log · `pt1 s32–33`
**Tools:** Windows PowerShell; **DeepBlueCLI**, run from an unpacked `DeepBlueCLI-master` folder.
The deck cites no download URL anywhere (§5).
**Evidence used:** `security.evtx` sitting in the same folder as the script.
⚠ exported from a live machine — regenerate on the course lab (§6).
**Steps as demonstrated:**
1. From the DeepBlueCLI folder (presenter's local path generalised to
   `<deepbluecli-folder>`):
```
.\DeepBlue.ps1 .\security.evtx
```
`⚠ OCR — verify`
2. PowerShell's execution-policy warning appears; the presenter answers `R`:
```
[D] Do not run [R] Run once [S] Suspend [?] Help (default is "D"): R
```
**What the output showed (`pt1 s32`):** one detection block —
`Log : Security`, `EventID : 4672`, `Message : Multiple admin logons for one account`,
`Results : Username: <account>` with `User SID Access Count: 52`, dated `10/30/2024 4:56:30 PM`.
**The username printed in this screenshot is the presenter's personal email address; it is
omitted here and the slide must be regenerated before reuse (§6).**
**What the output showed (`pt1 s33`):** two further blocks — `EventID : 4732`,
`Message : User added to local Administrators group`, and `EventID : 4720`,
`Message : New User Created`, naming `IEUser` and a `S-1-5-21-<...>-1000` SID, both dated
`10/23/2013`. Every block carries empty `Command :` and `Decoded :` fields — DeepBlueCLI's slots
for a recovered command line and its decoded form; empty means these detections were not
command-based.
⚠ **Provenance mismatch:** `pt1 s32` is dated 2024 and names a live account; `pt1 s33` is dated
2013 and names `IEUser`, so the two screenshots are **not** the same evidence file. The deck never
says which log `pt1 s33` came from — recover it before reusing either slide.
**What this lab teaches:** a triage tool turns 34,000 records into three named leads in one
command — and each of those leads is a heuristic that must be opened in Event Viewer before it
becomes a finding.

### IIS — enable logging, find the log, read the W3C header · `pt1 s34–37`
**Tools:** *Turn Windows features on or off*; IIS Manager; Notepad.
**Evidence used:** the presenter's own IIS instance; the sample log shown is dated 2017-10-22 and
matches INE's own screenshot set.
**Steps as demonstrated:**
1. Windows Features → *Internet Information Services* → *FTP Server* (FTP Extensibility, FTP
   Service), *Web Management Tools* (IIS 6 Management Compatibility, IIS Management Scripts and
   Tools, IIS Management Service), *World Wide Web Services* (`pt1 s34`). ⚠ OCR mangles most of
   these labels — verify against the slide.
2. IIS Manager home pane (`pt1 s35`) — the feature icons are where *Logging* is configured. ⚠ the
   OCR of this screenshot is largely destroyed; the connections pane also carries the presenter's
   machine name, which is omitted here (§6).
3. Open the log file in Notepad (`pt1 s36`). File name as printed: `ec17102206` — ⚠ OCR;
   the IIS default naming is `u_exYYMMDD.log`, so this is *likely intended* `u_ex171022.log`.
   **What the output showed** — the self-describing W3C header block plus request rows:
```
#Software: Microsoft Internet Information Services 10.0
#Version: 1.0
#Date: 2017-10-22 06:44:24
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken
```
   `⚠ OCR — verify`: the leading `#` on each header line is missing from the OCR and `cs-method`
   is printed `cs-methpd`; the form above is the *likely intended* standard header. Three rows
   follow, all from `127.0.0.1` on `2017-10-22`: `GET /`, `GET /iisstart.png` and `GET /test`.
   ⚠ the port column reads `88`; `80` is the likely intended value — verify.
4. *W3C Logging Fields* dialog (`pt1 s37`) — the administrator ticks which fields are recorded:
   Date, Time, Client IP Address (`c-ip`), User Name (`cs-username`), Service Name (`s-sitename`),
   Server Name (`s-computername`), Server IP Address (`s-ip`), Server Port (`s-port`), Method
   (`cs-method`), URI Stem (`cs-uri-stem`), URI Query (`cs-uri-query`), Protocol Status
   (`sc-status`), Protocol Substatus (`sc-substatus`).
**What this lab teaches:** the IIS field set is an administrator's choice, so a column that is not
in `#Fields:` was never *recorded* — which is a configuration fact, never evidence that the thing
did not happen.

### Shell pipeline — `cat` → `grep` → `cut` · `pt1 s38–41`
**Tools:** a Linux shell.
**Evidence used:** `scanresult.txt`, the saved output of an `nmap 7.01` sweep dated 2017-10-20
finding four live hosts on a `192.168.153.0/24` lab range with VMware MAC prefixes.
**Steps as demonstrated:**
1. Show the whole file:
```
cat scanresult.txt
```
2. Keep only the report lines:
```
cat scanresult.txt | grep report
```
   **Output showed** four `Nmap scan report for <ip>` lines.
3. Reduce to bare addresses:
```
cat scanresult.txt | grep report | cut -d"" -f5
```
   `⚠ OCR — verify`: **as printed** the delimiter argument is empty (`-d""`); **likely intended**
   `cut -d" " -f5`. **Output showed** the four IP addresses alone, which is what a single-space
   delimiter and field 5 produce.
4. `pt1 s41` is a fourth "Linux basics" slide carrying **no screenshot**. A further step (INE's
   `awk` material) was either spoken or skipped — it is demonstrated visually at best and must be
   recovered from the slide.
**What this lab teaches:** the pivot from "a file I cannot read" to "a list I can count" is three
processes long, and it is the same three against an exported `.evtx` or a plaso CSV.

### Apache access log — investigating XSS · `pt1 s43`
**Tools:** a shell on the web host; the log is read from its `/var/log/apache2` directory (visible
in the prompt).
**Evidence used:** `access.log` from a deliberately vulnerable web application. ⚠ the OCR renders
the app directory as `duwa` / `dywa`; **likely intended `dvwa`** — verify.
**Steps as demonstrated:** **no command is visible on this slide** — the screenshot shows only the
tail of the file and the shell prompt. The step is demonstrated visually and the command must be
recovered from the slide.
**What the output showed:** requests dated `02/Dec/2024` from `192.168.153.128` against
`192.168.153.129`, walking the reflected-XSS page and the security-level page, including:
```
"GET /dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%281%29%3C%2Fscript%3E HTTP/1.1" 200 4374
```
`⚠ OCR — verify`: the percent-encodings are badly mangled in the source (`z3E`, `~3C`, `23C`) and
`dvwa` is reconstructed; the line above is the *likely intended* form of what is on the slide.
The injected request returns **`200`** — per Module 05, an HTTP outcome, never a security outcome.
**What this lab teaches:** an XSS attempt is visible in a web log as a payload inside the query
string, and the status code tells you nothing about whether it worked.

### Apache access log — investigating SQL injection · `pt1 s44`
**Tools:** same shell, same file.
**Steps as demonstrated:**
1. Filter the log for the keyword:
```
cat access.log | grep or
```
`⚠ OCR — verify`
**What the output showed:** a single matching request dated `02/Dec/2024 07:36:05 -0500`:
```
"GET /dvwa/vulnerabilities/sqli/?id=%27+or+1%3D1%23&Submit=Submit HTTP/1.1" 200 4650
```
`⚠ OCR — verify`. **As printed** the query is
`/2id=72? sor +173D1+723&Submit=Submit` (and `tor` in the second pass of the same line);
**likely intended** the form above, decoding to `id=' or 1=1#`. This reconstruction is ours, not
the deck's — check the slide before teaching it.
**What this lab teaches:** the grep-for-a-keyword pass is how you find an injection attempt in a
log you cannot read line by line — and `grep or` also matches every URL containing the letters
"or", so a hit is a lead and not a finding.

### FTP daemon log — slide titled "Investigating RCE exploit" · `pt1 s45`
**Tools:** a shell in the host's `/var/log` directory.
**Evidence used:** a vsftpd log. ⚠ the file name is not visible on the slide.
**Steps as demonstrated:** **no command is visible** — output only. Demonstrated visually; recover
the command from the slide.
**What the output showed:** `CONNECT: Client "192.168.183.1"` lines dated `Tue Nov 12 2024`, then
`CONNECT` plus `[ftp] OK LOGIN: Client "192.168.183.135", anon password "<value>"` lines dated
`Thu Nov 21 2024`, and a final `CONNECT: Client "192.168.153.128"` dated `Mon Dec 2 2024`. Each
line carries the daemon PID. The anonymous-login password is a client-supplied string and is
generalised here.
⚠ **The slide title and the evidence do not match** — the title says RCE, the screenshot is
anonymous FTP logins from two different lab subnets (`192.168.183.x` and `192.168.153.x`). The RCE
step is not in this screenshot; recover it from the slide or retitle it.
**What this lab teaches:** a service log records connections and authentications with per-process
identifiers, and a client-supplied credential string is content, not identity.

### PostgreSQL transaction log · `pt1 s47`
**Tools:** a shell in the database host's PostgreSQL log directory.
**Evidence used:** `postgresql-8.3-main.log.1`.
**Steps as demonstrated:**
1. Show the head of the rotated log:
```
head postgresql-8.3-main.log.1
```
`⚠ OCR — verify`: **as printed** `postgresq1-8.3-main.log.1` (digit one substituted for `l`);
the prompt's host name is likewise OCR'd with `n` for `m`.
**What the output showed:** startup and recovery records, all stamped **`EST`**, not UTC —
`could not load root certificate file "root.crt": no SSL error reported`;
`DETAIL: Will not verify client certificates.`;
`database system was interrupted: last known up at <time>`;
`database system was not properly shut down: automatic recovery in progress`;
`record with zero length at 0/4406F0`; `redo is not required`;
`autovacuum launcher started`; `database system is ready to accept connections`;
`incomplete startup packet`.
**What this lab teaches:** a database writes its own timeline, including an unclean shutdown and
the recovery that followed it — and it writes it in the host's local zone, which is precisely the
normalisation problem part 2 goes on to describe.

### FTK Imager — Export Directory Listing · `pt2 s20`
**Tools:** FTK Imager; a spreadsheet to view the CSV.
**Evidence used:** an NTFS `System Reserved` partition (the Windows 7-era boot volume), entries
dated `2013-Mar-13`.
**Steps as demonstrated:** **no menu path is shown** — the slide is a screenshot of the resulting
CSV already open in a spreadsheet. The export is FTK Imager's *Export Directory Listing*
(Module 05 §2); the step is demonstrated visually and the route must be recovered from the slide.
**What the output showed:** columns `Filename`, `Full Path`, `Size (bytes)`, `Created`,
`Modified`, `Accessed`, `Is Deleted`, with times to microsecond precision and explicitly marked
`UTC`. Rows include `[unallocated space]`, `[orphan]`, `$MFT`, `$MFTMirr`, `$LogFile`, `$BadClus`,
`$AttrDef`, `$Bitmap`, `$Boot`, `$I30`, `Boot\`, `Boot\zh-HK\` and
`System Volume Information\tracking.log`.
**What this lab teaches:** three time columns is not four — this export has no MFT-entry-modified
column and no `$FILE_NAME` set, so it **cannot** perform the timestomp test the previous slide
(`pt2 s19`) has just taught. That gap, not the export, is the lesson.

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| Event log configuration key | `HKLM\SYSTEM\CurrentControlSet\Services\eventlog` (`pt1 s22`, printed lower-case) | "Events directory"; "its path can be modified and alterd" [sic] | [M05 §2 — Event log configuration key](../Module_05_Logs_Timelines_and_Reporting.md) |
| `File` value | `%SystemRoot%\system32\winevt\Logs\Application.evtx` (REG_EXPAND_SZ) | where the Application channel is stored | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| `DisplayNameFile` value | `%SystemRoot%\system32\wevtapi.dll` (REG_EXPAND_SZ) | shown in the same key, not explained | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| `MaxSize` / `Retention` / `AutoBackupLogFiles` / `RestrictGuestAccess` | `0x01400000` (20 MB) / `0x00000000` / `0x00000000` / `0x00000001` (`pt1 s22`) | shown, not used — the retention arithmetic is never done | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| Windows event IDs (legacy/modern) | `528`/`4624`, `529`/`4625`, `680`/`4776`, `624`/`4720`, `636`/`4732`, `632`/`4728`, `2949`/`7045` (`pt1 s23`) | successful login, failed login, account authentication, new user, added to local group, added to global group, service creation | [M05 §5](../Module_05_Logs_Timelines_and_Reporting.md) |
| Security channel | Event Viewer → Windows Logs → Security (`pt1 s21`, `s29–31`) | "logs events related to security processes such as login attempts" | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| `security.evtx` + DeepBlueCLI | `<deepbluecli-folder>\DeepBlue.ps1` and `<deepbluecli-folder>\security.evtx` (`pt1 s32`) | triage of a Security log | [M05 §3](../Module_05_Logs_Timelines_and_Reporting.md) |
| Apache log directory (as claimed) | `/var/www/apache2/logs` (`pt1 s17`, `s42`) | "Log file located at" | [M05 §2 — Apache access log](../Module_05_Logs_Timelines_and_Reporting.md) — **contradicted by the deck's own screenshots**, §6 |
| Apache access log (as shown) | `/var/log/apache2/access.log` (prompt, `pt1 s43–44`) | XSS and SQLi investigation | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| `mod_log_forensic` | Apache module (`pt1 s19`) | "generate more logging data" | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| FTP daemon log | `/var/log/` (`pt1 s45`; file name not visible) | connection and anonymous-login record | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| PostgreSQL log | `/var/log/postgresql/postgresql-8.3-main.log.1` (`pt1 s47`) | "transaction logs contains all transaction and queries ... can be used to rebuild the database" (`pt1 s11`) | [M05 §1](../Module_05_Logs_Timelines_and_Reporting.md) |
| IIS W3C log | opened in Notepad; **directory never shown** (`pt1 s36`) | W3C extended format, admin-selected fields | [M05 §2 — IIS log](../Module_05_Logs_Timelines_and_Reporting.md) |
| Syslog facility codes | `0` kernel, `1` user, `2` mail, `3` system services (daemons), `4` authentication (`pt1 s25`) | message origin | [M05 §2 — Syslog record](../Module_05_Logs_Timelines_and_Reporting.md) |
| Syslog severity codes | `0` Emergency … `7` Debug (`pt1 s26`) | message severity | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| Cisco syslog configuration | `logging 192.168.1.1` / `logging trap debugging` / `logging on` (`pt1 s27`) | enable syslog to a collector at a severity level | [M05 §2](../Module_05_Logs_Timelines_and_Reporting.md) |
| NTFS timestamp attributes | `$Standard_info` and `$FILE_NAME` (`pt2 s16`, as printed) | where MACB times are stored | [M03 §2 — `$STANDARD_INFORMATION` / `$FILE_NAME`](../Module_03_Disks_and_File_Systems.md) |
| Timestomp indicator | "If time in `$STD_INFO` > Time in `$FILE_NAME`" (`pt2 s19`) | detecting a timestomp attack | [M05 §1](../Module_05_Logs_Timelines_and_Reporting.md) — **direction disputed**, §6 |

## 4 · What this deck adds beyond the INE material

- **DeepBlueCLI** (`pt1 s32–33`). Not mentioned anywhere in units 8–10. It is the deck's single
  biggest contribution: one command turns a 34,000-record Security log into three named detections
  (`4672` repeated admin logons, `4732` group addition, `4720` user creation) with the target SID
  attached. Already carried into Module 05 §3 as a tool row.
- **A live IIS build-out**, not just IIS screenshots (`pt1 s34–37`). Turning the feature on and
  then opening the field-selection dialog makes "which fields exist is an administrator's decision"
  a thing students watched happen rather than a sentence they read.
- **Four end-to-end investigations against a running vulnerable host with 2024-dated evidence**
  (`pt1 s43–45`, `s47`): XSS, SQLi, anonymous FTP, and a database recovery sequence. INE's
  attack-string material is a list of things to grep for; this is the walk-through.
- **Timestomp detection** (`pt2 s16–19`). The `$STANDARD_INFORMATION` vs `$FILE_NAME` comparison
  does not appear in units 8–10 at all. Its stated *direction* is contestable — §6.
- **The Windows time-rules matrices** (`pt2 s17–18`) — an operation-by-operation table (rename,
  local move, volume move, copy, access, modify, creation, deletion) against each attribute set.
  INE has nothing equivalent, and this is the most reusable single page in part 2.
- **A PostgreSQL log read as evidence** (`pt1 s47`) — INE names database transaction logs as a
  category and shows none; the deck shows one, with an unclean shutdown visible in it.
- The **MCAB mnemonic** (`pt2 s15`) as a teaching device — with the caveat in §6 about the letter
  order.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted (INE covers it; the deck does not):**
- **The entire super-timeline toolchain.** No `log2timeline`, no plaso, no `-z`/`-f`/`-r`/`-w`
  switches, no body file, no `fls`, no `mactime`, no TLN format, no Timeline Explorer. Part 2
  teaches timeline theory and then never builds a timeline. This is the biggest hole in the pair.
- The six timeline components, the `source` field values (FILE, EVT/EVTX, REG, PRE, LNK), and the
  system/user fields.
- XP `.evt` vs Vista+ `.evtx` storage locations, and the XP-to-Vista event ID conversion
  (`+4096`, and the fact that the two schemes are not fully compatible).
- INE's seven forensically-essential event categories, and the audit-policy point that Windows
  logs comparatively little unless configured to.
- **Log clearing** — event IDs `1102`/`104`/`517` appear nowhere in either deck, despite an
  Event Viewer demo sitting right next to the topic.
- `awk` (INE spends a dozen pages on it); `pt1 s41` is a bare slide with no screenshot.
- FAT vs NTFS MACB field mapping in detail, and the string-based and SYSTEMTIME formats — the deck
  gives only 64-bit FILETIME and 32-bit Unix time.
- Retention arithmetic from `MaxSize` — the values are on screen at `pt1 s22` and are never used.
- Logon types, which the deck's own `4624` demo depends on (`pt1 s31` shows type 5 and does not
  say what 5 means).

**Resources cited on the slides** — recorded verbatim, `unverified`, not vouched for:
- `http://windowsir.blogspot.com/` — Harlan Carvey's blog, cited at `pt2 s9` alongside a
  recommendation of his books. `unverified`
- `https://aka.ms/PSWindows` — appears only inside the PowerShell banner in the `pt1 s32`
  screenshot, not as a citation. `unverified`
- `https://nmap.org` — appears only inside nmap's own banner in the `pt1 s38` screenshot, not as a
  citation. `unverified`
- **DeepBlueCLI has no URL on any slide.** It is run from a folder named `DeepBlueCLI-master`,
  which implies a downloaded repository archive, but the deck never says from where.

## 6 · Cautions before reuse

**Screenshots containing the presenter's personal data — regenerate on the course lab before any
of these goes on a new slide:**
- **`pt1 s32`** — the DeepBlueCLI result block prints the presenter's **personal email address**
  as the detected username, and the PowerShell prompt shows the presenter's **local working path**
  on a `D:` drive. Both are omitted from this file. This is the worst offender in either deck.
- **`pt1 s31`** — the Event Viewer detail pane shows the presenter's Windows **account name** and
  **computer name**.
- **`pt1 s33`** — the continuation of the same DeepBlueCLI run; it carries a full user SID and
  belongs to the same re-shoot even though no presenter identifier survived the OCR.
- **`pt1 s35`** — the IIS Manager connections pane shows the presenter's **machine name**.
- **`pt1 s29–30`** are live captures of the presenter's desktop and Event Viewer. Nothing personal
  survived the OCR, but re-shoot them with `pt1 s31` so the demo sequence stays consistent.
- **Checked the rest of both decks.** `pt1 s43–45` and `s47` show only stock lab accounts on a
  deliberately vulnerable VM and RFC1918 lab addressing (`192.168.153.x`, `192.168.183.x`) — no
  presenter identifiers. `pt1 s21` and `s36` are INE-sourced sample data. **Part 2 contains no
  personal data at all.**

**Content that is wrong or disputed:**
- **`pt2 s19`'s timestomp rule is the wrong way round for the common case.** The deck states
  `$STD_INFO > $FILE_NAME`; backdating — the usual attack — makes `$STANDARD_INFORMATION`
  *earlier* than `$FILE_NAME`. This material is instructor-added and is in neither unit 8 nor 9.
  Module 05 §1 and §7 already record the disagreement; **INE is the course's truth**, and what to
  teach is Module 05's wording: a significant divergence **in either direction** between the two
  attribute sets is the signal, and the finding is "an inconsistency exists", never "the file was
  timestomped".
- **`pt1 s17`/`s42`'s Apache path is contradicted by the deck's own screenshots.** The slides say
  `/var/www/apache2/logs`; the prompts at `pt1 s43–44` read `/var/log/apache2`. INE prints the same
  wrong path, and Module 05 §2 records the disagreement. Teach `/var/log/apache2` on Debian/Ubuntu
  and show students both.
- **`pt2 s15` uses `MCAB`, not `MACB`.** Every tool output column, INE and Module 05 use MACB.
  Reordering the letters for a mnemonic in front of students who will next read a `mactime` `Type`
  column is a needless trap — use MACB.
- **`pt1 s31`'s demonstrated `4624` is a logon type 5 (service) record.** If the sequence is
  reused, pick a type 2, 3 or 10 record instead, or the "who logged on" lesson lands on a service
  account and the deck never defines the types (§5).

**Tools and versions that have moved on** (the decks date from early 2025):
- DeepBlueCLI is run from an unpacked `-master` archive with no version recorded. Pin a release,
  record its version and hash in the lab build, and re-run the capture.
- The vulnerable web host, `vsftpd` and **PostgreSQL 8.3** are Metasploitable-era software. Fine as
  *evidence*, misleading as a demonstration of current log formats — say so when using them.
- `nmap 7.01` (`pt1 s38`) and the IIS `10.0` sample header (`pt1 s36`) are both old; confirm what
  the rebuilt lab actually ships before quoting version strings.
- The Apache and IIS sample entries are dated 2017 and are INE's, not the presenter's; only the
  live captures (`pt1 s31–33`, `s43–45`, `s47`) are from 2024.

**OCR that could not be resolved and matters:**
- **`pt2 s17–18` — the two Windows time-rules matrices are the most valuable slides in part 2 and
  the OCR of both is destroyed.** Do not transcribe them from the source text. Re-derive the tables
  from the original reference before they go in front of students.
- `pt1 s40` — the `cut` delimiter is printed empty (`-d""`).
- `pt1 s44` — the SQL injection query string; the decoded form in §2 is our reconstruction.
- `pt1 s43` — the XSS percent-encodings, and the vulnerable app's directory name.
- `pt1 s36` — the IIS log file name and the `s-port` value (`88` printed, `80` likely).
- `pt1 s34–35` — the Windows Features list and the IIS Manager icon set.
- `pt2 s20` — the FTK Imager listing is a screenshot of a spreadsheet; only the column headers and
  a minority of rows are legible.
- `pt1 s14` — the central-logging diagram is a picture; only the node labels survive.

**What the S6 compression costs.** As delivered this was a full session of lecture plus five
distinct demos in part 1, and a second deck for timelines. In the rebuilt six-session course all of
it shares one 4-hour S6 with network forensics, reporting and the capstone. The realistic split:
keep the Event Viewer filter and a **regenerated** DeepBlueCLI run as the only live log demos, plus
the three-command shell pipeline; move IIS, the XSS/SQLi/FTP/PostgreSQL walk-throughs to homework
against pre-supplied logs. The unavoidable cost is on the timeline side — part 2 already ran no
timeline tool, and S6 has less time than part 2 had, so the plaso work that INE requires and this
deck never demonstrated has to be pre-built before class (Module 05 §6) or it will not happen at
all.
