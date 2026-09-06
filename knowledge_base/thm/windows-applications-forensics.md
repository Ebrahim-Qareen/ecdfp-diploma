---
room: Windows Applications Forensics
url: https://tryhackme.com/room/windowsapplications
module: Windows Endpoint Investigation (Section 3 of Advanced Endpoint Investigations)
feeds: PARTIALLY. Part 1 maps this to `S5-05` prefetch and `S5-06` amcache/shimcache —
       **WRONG, the room contains neither.** Real fit: closes room 1's scheduled-tasks gap,
       adds services, and opens a browser-forensics question our map has never answered.
       Teams and OneDrive are OUT (cloud, excluded in scope_decisions).
difficulty / time: Medium · 60 min · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 11 tasks read in full. 0 sections NOT READ.
  (Note: 72 KB body exceeded the page-text limit at 50 KB; the remainder was recovered by
   removing already-read task nodes from the DOM and re-reading. Nothing was skipped.)
---

## 1. What the room teaches

**Live triage of installed applications** — hunting outliers in scheduled tasks, services,
browsers and Office apps on a running machine, before the disk and memory images arrive. Its
framing is explicitly *incomplete visibility*: the SIEM is half-built, the images are still
downloading, go look at the host now.

Eleven tasks in three families: persistence (scheduled tasks, services), browsers (Firefox,
Chrome, Edge), and Microsoft 365 apps (Outlook, Teams, OneDrive). Every family is taught
**twice** — once through logs/GUI and once through PowerShell — which is a deliberate and good
choice, because the log path depends on audit policy being enabled and the manual path does not.

The largest room of the five and the most operationally realistic. It is also the room whose
scope overlaps ours the least cleanly — see §8.

## 2. Artifacts — one 6-box block each

### 2.1 Scheduled task creation events

- **What it is** — the audit record of a scheduled task being created or changed.
- **Where it lives** — Security log. **Event ID 4698** created · **Event ID 4702** updated.
- **What it proves** — timestamp, **the user who created it**, the command to be executed, the
  execution interval, and the user context it runs as. That is attribution the on-disk XML
  cannot give you.
- **What it does NOT prove** — ⚠️ **the room states the limit that matters and it is the whole
  reason Task 3 exists: these events only exist if advanced audit policy for scheduled-task
  events was enabled.** No 4698 is *not* evidence that no task was created. Nor does the event
  prove the task ever ran.
- **How to parse it** — `eventvwr.msc` filtered by ID; or `wevtutil.exe`; or PowerShell
  `Get-WinEvent` / `Get-EventLog`.
- **Anti-forensics / false-positive caveat** — the room supplies a genuinely useful triage
  heuristic set instead of a single caveat: judge a task by **command**, **creating user**
  (only admins normally create tasks), **execution context** (privileged = suspicious),
  **trigger interval**, and **comparison to a fleet baseline** — a real deployment appears on
  many machines, an implant on one.

### 2.2 Service installation events

- **What it is** — the audit record of a new service being installed.
- **Where it lives** — **Event ID 7045** in the **System** channel · **Event ID 4697** in the
  **Security** channel. Two channels, two IDs, same event class — worth teaching as a pair.
- **What it proves** — timestamp, creating user, **the service binary**, the **start type**, and
  the execution context.
- **What it does NOT prove** — same audit-policy dependency as 4698, and the same silence
  problem: absence is not absence. It also does not prove the service ever started.
- **How to parse it**
  `Get-WinEvent -FilterHashTable @{LogName='System';ID='7045'} | fl`
  `Get-WinEvent -FilterHashTable @{LogName='Security';ID='4697'} | fl`
- **Anti-forensics / false-positive caveat** — the room's own point is sharp: **services are
  expected to run service binaries**, so a one-liner command in a service's image path is a
  glaring anomaly visible without any tooling.

### 2.3 Scheduled tasks on disk

- **What it is** — the task definitions themselves.
- **Where it lives** — `C:\Windows\System32\Tasks`, mirroring the task's logical location as
  subdirectories (a task at `\Microsoft\Office` is the file
  `C:\Windows\System32\Tasks\Microsoft\Office\<task name>`). Each file is **XML**.
- **What it proves** — everything the Task Scheduler GUI shows: trigger, action and arguments,
  run-as context, highest-privileges flag, and the **Settings** block. Plus the file's own
  **created and last-modified timestamps**, which the room uses well — **a mismatch between them
  suggests a legitimate task was later modified to carry a malicious command.**
- **What it does NOT prove** — execution. Configuration only. And the XML's author field is
  attacker-controllable text.
- **How to parse it** — `taskschd.msc` GUI (start from **Active Tasks**, sorted by next run
  time); Notepad on the XML; or PowerShell:
  - `Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"}`
  - `schtasks.exe /query /fo CSV | findstr /V Disabled`
  - sorted with context:
    `Get-ScheduledTask | Where-Object {$_.Date -ne $null -and $_.State -ne "Disabled"} | Sort-Object Date | select Date,TaskName,Author,State,TaskPath | ft`
  - per-task detail: `(Get-ScheduledTask -TaskName <name>).Actions` / `.Triggers` / `.Principal`
    (parenthesised because a property is being read)
- **Anti-forensics / false-positive caveat** — **the best content in the room.** Four Settings
  fields that exist for admins and are abused by attackers:
  - *Run task as soon as possible after a missed start* — fires even if the machine was off
  - *Restart on failure* — survives a failed first attempt
  - *Stop after a specific time* — goes quiet after the payload lands
  - **Auto-delete after expiry — the task removes itself, taking the evidence with it**
  Also: naming. Threat actors name implants after real installed software (the room's example
  imitates a Microsoft Office service task), so name plausibility is not evidence of legitimacy.
  And binary *location* (Temp, AppData) is a hint, never a verdict — the room says so explicitly.

### 2.4 Services in the registry

- **What it is** — the configuration of every installed service.
- **Where it lives** — `HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>`
- **What it proves** — image path, start type, and user context. Via the key's **Last Write
  Time**, an approximate change time.
- **What it does NOT prove** — ⚠️ **the room is admirably careful here: the registry holds no
  service creation date.** Last Write Time may be treated as a creation date *only* if the
  service has not been modified since — an assumption, and the room labels it as one. This is a
  textbook findings-vs-interpretation moment and we should lift it directly.
- **How to parse it** — `services.msc` (sort by Status + Startup Type); Registry Editor; Task
  Manager's Services tab to map service → PID → child processes; or PowerShell with
  `Get-Service` + `Get-WmiObject Win32_Service` for image path and `StartName`, joined to a
  `Get-RegWriteTime` helper script for the key's last write time.
- **Anti-forensics / false-positive caveat** — two, both stated:
  - Filtering to **Running + Automatic** is fast but **misses services deliberately left Disabled
    or Manual and triggered by another implant.** The room says to sweep all services eventually.
  - Also check **stopped** Automatic services — a service binary that injects and exits leaves a
    stopped service behind.
  - The **Recovery** tab can run a *different* program on failure than the one shown on General.

### 2.5 Firefox browsing artifacts

- **What it is** — Firefox's per-profile metadata stores.
- **Where it lives** — `%APPDATA%\Mozilla\Firefox\Profiles\<profile>` where the profile
  directory matches `[a-z0-9]{8}\.default.*`
  | file | contents |
  |---|---|
  | `places.sqlite` | history and bookmarks |
  | `logins.json` + `key4.db` | saved credentials |
  | `cookies.sqlite` | cookies |
  | `extensions.json` / `extensions\` | extensions |
  | `favicons.sqlite` | favicon metadata — evidence a site was loaded |
  | `sessionstore-backups\` | sessions and tabs (`jsonlz4`) |
  | `formhistory.sqlite` | data typed into web forms |
- **What it proves** — from `moz_places`: URL, title, **visit count**, last visit date (epoch —
  must be converted), and a **`typed` flag distinguishing a URL the user typed from one they
  arrived at by click or redirect**. Joining `moz_places.id` to `moz_historyvisits` gives *every*
  visit, not just the last, plus a `visit_type` (1 link · 2 typed · 3 bookmark · 4 embed ·
  5 permanent redirect · 6 temporary redirect · 7 download · 8 framed link · 9 reload).
  `moz_annos` carries download metadata including where the file was saved.
- **What it does NOT prove** — that the user *intended* to visit. `visit_type` 4/5/6/8 are
  machine-driven: embedded content, redirects and frames land in history without a human
  choosing them. **Treating any history row as a deliberate visit is the classic browser-forensics
  error, and the `typed` flag plus `visit_type` are exactly what separate the two.** History also
  does not prove what the page contained, or that it was read.
- **How to parse it** — DB Browser for SQLite, with SQL against the tables above.
- **Anti-forensics / false-positive caveat** — the room states none directly, but gives a strong
  positive technique: **cookie–site mismatch as MITM/phishing evidence.** It cites Microsoft's
  own documented Entra session cookies (`ESTSAUTH` transient, `ESTSAUTHPERSISTENT` persistent) and
  notes that finding O365 session cookies scoped to *some other* domain suggests an
  adversary-in-the-middle proxy (evilginx2-style). That is a genuinely advanced, teachable idea.

### 2.6 Chrome browsing artifacts

- **What it is** — Chrome's per-profile metadata stores.
- **Where it lives** — `%LOCALAPPDATA%\Google\Chrome\User Data\Default`
  | file | contents |
  |---|---|
  | `History` | history **and downloads** (SQLite) |
  | `Login Data` | saved credentials (SQLite) |
  | `Extensions\` | extension code and manifests |
  | `Cache\` | cached response bodies |
  | `Sessions\` | sessions and tabs |
  | `Bookmarks` | JSON |
  | `Web Data` | web-form input (SQLite) |
- **What it proves** — the same classes as Firefox; the room's point is that **the artifacts are
  equivalent and only the schema differs**, so the Firefox method transfers.
- **What it does NOT prove** — same limits as Firefox: presence in history is not intent, and
  saved credentials prove storage, not use.
- **How to parse it** — DB Browser for SQLite.
- **Anti-forensics / false-positive caveat** — the room states none here.

### 2.7 Browser extensions

- **What it is** — installed browser extension code.
- **Where it lives** — `...\Chrome\User Data\Default\Extensions\<extension id>\<version>\`
  Key file: **`manifest.json`**, which declares `background.service_worker` and
  `content_scripts.js` plus the `matches` patterns.
- **What it proves** — exactly what the extension is permitted to do and what code runs.
  `matches: ["*://*/*"]` means it injects into **every** site. The room's worked example is a
  keystroke harvester whose `script.js` hooks `document.onkeydown`, buffers keys, and `POST`s
  them to a remote URL on a `setInterval` timer, with a second `POST` leaking the current URL.
- **What it does NOT prove** — that the extension ever ran, or that data actually reached the
  remote host. Static code review shows capability; network or host evidence shows use.
- **How to parse it** — read `manifest.json`, then source-review the files named in `background`
  and `content_scripts`. No tool required.
- **Anti-forensics / false-positive caveat** — the room says it plainly: **its sample is
  unobfuscated and real ones usually are not.** Deobfuscation is a separate skill and out of the
  room's scope — and, for us, out of the course's (`scope_decisions`: no malware RE).

### 2.8 Edge cache

- **What it is** — cached response bodies and their metadata.
- **Where it lives** — `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default` (Chromium-based, so the
  Chrome layout applies).
- **What it proves** — per cached entry: **Last Accessed**, the **URL of the cached file**, the
  **site that loaded it**, and the **content type**.
- **What it does NOT prove** — ⚠️ **the room is explicit and correct: cache is supporting
  evidence only.** It shows a resource was fetched, not which page the user was on, not what they
  did there. It must be corroborated with history or cookies. This is the cleanest
  "cannot-prove" statement in the whole room.
- **How to parse it** — **ChromeCacheView** (NirSoft), pointed at the Edge cache directory — the
  room notes it defaults to Chrome's and must be redirected.
- **Anti-forensics / false-positive caveat** — the room states none beyond the above.

### 2.9 Outlook mailbox and attachment cache

- **What it is** — the local mail store and the cache of attachments opened from it.
- **Where it lives**
  `%LOCALAPPDATA%\Microsoft\Outlook\<user_email@domain>.ost` — the offline mail store
  `%LOCALAPPDATA%\Microsoft\Windows\INetCache\Content.Outlook\<random>\` — attachment cache
- **What it proves** — the OST holds mail as of the **last successful synchronisation**: folders
  (Inbox, Sent, Deleted, Junk), attachments (the paperclip column), links, and **headers** via
  the Properties view — `Date`, `From`, `Received` (the hop path), `X-Mailer`.
  The `Content.Outlook` cache proves something stronger and more specific: **that the user
  actually opened an attachment from within the client**, not merely received it.
- **What it does NOT prove** — the OST is a *synced copy*, so anything changed server-side after
  the last sync is absent, and anything deleted server-side may still be present. Headers are
  attacker-supplied except for the receiving hops. And ⚠️ **the room states a crucial volatility
  limit: `Content.Outlook` is cleared when the Outlook client exits** — its contents are a
  live-system artifact only.
- **How to parse it** — **XstReader** for the OST (navigate `Root - Mailbox > IPM_SUBTREE`);
  PowerShell to find the directories across profiles, e.g.
  `ls C:\Users\ | foreach {ls "C:\Users\$_\AppData\Local\Microsoft\Outlook\" 2>$null | findstr Directory}`
- **Anti-forensics / false-positive caveat** — the volatility of `Content.Outlook` is the caveat:
  **shut the client down and the evidence of opening is gone.** That is an order-of-volatility
  lesson (`S2-01`) landing inside an application artifact.

### 2.10 Microsoft Teams message store

- **What it is** — the local IndexedDB/LevelDB store behind the Teams client.
- **Where it lives** — 🔴 **the room's path is for CLASSIC Teams only and is now obsolete.**
  - Teams **1.x** (classic, what the room teaches):
    `%APPDATA%\Microsoft\Teams\IndexedDB\https_teams.microsoft.com_0.indexeddb.leveldb\`
  - Teams **2.x** (new client):
    `%LOCALAPPDATA%\Packages\MicrosoftTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\EBWebView\Default\IndexedDB\<url>`
  See §3 — this is the most serious currency defect found across all five rooms.
- **What it proves** — after parsing, records typed by `record_type`:
  *contact* → `displayName`, `email`, `mri` (unique id), `userPrincipalName`
  *message* → `conversationId` (thread key), `composetime`/`createdTime`, `content`,
  `creator` (an MRI, resolvable via the contact records), `isFromMe` (direction),
  and `properties`, which carries edit times and **file attachment details**
  (`fileName`, `fileInfo.fileUrl`, `fileType`).
- **What it does NOT prove** — that an attachment was downloaded, opened or executed. The room is
  good on this: it tells you to pivot from the attachment name to Downloads/Desktop/Documents and
  then to execution artifacts. Chat content is also user-supplied text — it evidences a claim,
  not a fact.
- **How to parse it** — `ms_teams_parser.exe -f <...\.indexeddb.leveldb\> -o output.json`
  (the standalone binary of the **Forensics.im / forensicsim** Autopsy plugin), then PowerShell
  over the JSON: build an MRI → `userPrincipalName` hashtable from the contact records, group
  messages by `conversationId`, sort by `createdTime`, and print sender/direction/content, with a
  branch that walks `properties.files` for attachments.
- **Anti-forensics / false-positive caveat** — the room states none. Ours: **the client version
  determines the path**, and getting it wrong produces a confident "no Teams artifacts found".

### 2.11 OneDrive sync logs

- **What it is** — the local record of OneDrive synchronisation.
- **Where it lives** — `%LOCALAPPDATA%\Microsoft\OneDrive\logs\`, with `Business*` and `Personal`
  subdirectories (enterprise licensing means `Business` is the usual one).
  - `SyncEngine.odl` — every operation performed, with per-file information. `.odlgz` are the
    compressed rotations.
  - `SyncDiagnostics.log` — plain text; sync progress, bytes up/down, file counts.
- **What it proves** — per file: `name`, `lastChange`, `status` (cloud-only vs local), `size`.
  For the OneDrive root: **the associated OneDrive/SharePoint link and its local path** — which is
  how you spot *a personal or foreign tenant folder synced onto a corporate machine*, i.e.
  **exfiltration by sync**. Also a list of **deleted files with deletion dates and locations**.
- **What it does NOT prove** — that a file's contents left the machine, or who initiated the sync.
  A sync relationship is not proof of transfer, and the ODL is a client-side log — the server side
  is where the transfer is actually evidenced.
- **How to parse it** — `SyncDiagnostics.log` is readable as text. `SyncEngine.odl` needs
  **OneDriveExplorer**, run as administrator, `File > Live system` to harvest every user profile.
- **Anti-forensics / false-positive caveat** — the room states none.

## 3. Tools and commands

| tool | version the room uses | exact command / action | what it outputs |
|---|---|---|---|
| Event Viewer | n/a | `eventvwr.msc` → Security → filter 4698 / 4702 | task create/update events |
| PowerShell | n/a | `Get-WinEvent -FilterHashTable @{LogName='System';ID='7045'} \| fl` | service install events |
| PowerShell | n/a | `Get-WinEvent -FilterHashTable @{LogName='Security';ID='4697'} \| fl` | service install events |
| Task Scheduler | n/a | `taskschd.msc` → Active Tasks | enabled tasks, sorted by next run |
| PowerShell | n/a | `Get-ScheduledTask \| Where-Object {$_.State -ne "Disabled"}` | enabled tasks |
| `schtasks.exe` | n/a | `schtasks.exe /query /fo CSV \| findstr /V Disabled` | tasks as CSV, disabled removed |
| PowerShell | n/a | `(Get-ScheduledTask -TaskName <n>).Actions` / `.Triggers` / `.Principal` | command, trigger, run-as |
| Services / Task Mgr | n/a | `services.msc`; Task Manager → Services tab | services, start type, PID mapping |
| PowerShell + helper | n/a | `Import-Module C:\Tools\Get-RegWriteTime.ps1` then `Get-Item HKLM:\SYSTEM\CurrentControlSet\Services\<n> \| Get-RegWriteTime` | service key last write time |
| DB Browser for SQLite | **not stated** | SQL over `places.sqlite`, `cookies.sqlite`, Chrome `History` | history, visits, cookies, downloads |
| ChromeCacheView | **not stated** | GUI, repointed at the Edge cache directory | cache entries + metadata |
| XstReader | **not stated** | GUI, open the `.ost` | mailbox tree, messages, headers |
| `ms_teams_parser.exe` | **not stated** | `-f <...indexeddb.leveldb\> -o output.json` | Teams records as JSON |
| OneDriveExplorer | **not stated** | run as admin → `File > Live system` | parsed ODL, per-file properties |

### CURRENCY CHECK — run 2026-08-28

| item | result |
|---|---|
| 🔴🔴 **Microsoft Teams path — the room teaches a location that no longer exists** | The room uses **classic Teams 1.x**: `%APPDATA%\Microsoft\Teams\IndexedDB\https_teams.microsoft.com_0.indexeddb.leveldb\`. The **new Teams 2.x client stores elsewhere entirely**: `%LOCALAPPDATA%\Packages\MicrosoftTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\EBWebView\Default\IndexedDB\<url>` — a packaged (MSIX) app using an Edge **WebView2** container. **Confirmed from the parser author's own write-up.** A student following this room on a current enterprise workstation finds nothing and may conclude Teams was not used. **If we teach Teams at all, teach both paths and how to tell which client is installed.** |
| **forensicsim / `ms_teams_parser`** | latest release **v0.8.5, 7 July 2024**; the project states it handles both Teams 1.x and 2.x (tested against 1.4.x and 2.0). ⚠️ Two years old as of this check, against a client that has since moved to a WebView2 architecture — **re-test before relying on it.** |
| **OneDriveExplorer** | live-system mode confirmed; parses `.odl`, `.odlsent`, `.odlgz`, `.aold`, plus `<UserCid>.dat` and SQLite. **Version number not published in the README — not confirmed this pass.** |
| **XstReader · ChromeCacheView · DB Browser for SQLite · `Get-RegWriteTime.ps1`** | **NOT VERIFIED this pass.** No versions stated by the room and not independently checked. Verify before any of these enters student material. |
| Event IDs 4698 / 4702 / 7045 / 4697 | consistent with the event-ID sets in rooms 2 and 3; no conflicts found. |
| Firefox `visit_type` enumeration (1–9) | as the room gives it; **not independently verified** against current Mozilla source. |
| PowerShell / `schtasks` / `services.msc` | built-in, unversioned. Commands are ordinary and current in form. |
| ⚠️ transcription hazard in the room | several PowerShell snippets render the `-ne` operator with an **en dash** (`—ne`) rather than a hyphen. Copy-pasted as shown, **they will not run.** Worth flagging to students as a lesson in never trusting a pasted command. |
| Room's version claims | **none stated for any tool** — fifth room running. |

## 4. Evidence used

- A THM lab VM (live "compromised machine") plus an attacker machine / AttackBox, with XstReader,
  ChromeCacheView, DB Browser for SQLite, `ms_teams_parser.exe`, OneDriveExplorer and
  `Get-RegWriteTime.ps1` pre-staged in `C:\Tools\` and on the Desktop.
- **Size: not stated. Not downloadable. No licence offered. Not reusable.**
- Lab credentials published inline again. **Deliberately not recorded here (R8).**
- **Nothing to flag for `ecdfp-evidence`.**
- ✅ One handling practice worth copying verbatim into our own case briefs: the room opens with a
  **warning not to interact with the artifacts** — do not visit the URLs, resolve the domains, or
  pull the malicious binaries off the machine. Our cases use fictional infrastructure (D19), but
  **teaching the reflex is still right**, and it costs one line.

## 5. Lab design worth reusing

1. **Every artifact family is taught twice — logs first, then manual.** And the *reason* is
   stated: log-based analysis only works if the audit policy was enabled, so the manual path is
   the fallback, not an alternative. **This is the single most transferable structure in the
   room.** It builds the habit of asking "what if this source is missing?", which is criterion-4
   thinking applied to method rather than to an artifact.
2. **GUI → structure → command line, in that order, per artifact.** Task Scheduler GUI → the XML
   on disk → `Get-ScheduledTask`. The student sees the same fact three ways and learns that the
   GUI is a *view*, not the evidence. Same arc for services: `services.msc` → registry key →
   PowerShell. Excellent for Tier B micro-pages.
3. **The scripts build up incrementally.** The Teams analysis starts with a contact hashtable,
   then adds conversation grouping, then adds attachment parsing — each snippet a superset of the
   last. That is how to teach scripting to mixed-level students without losing the slower half.
4. **Three users share one workstation.** A small scenario decision with large consequences: every
   artifact must be attributed to a *profile*, so "which user" is a live question throughout
   rather than an afterthought. **Directly relevant to `S5-09`, whose case asks exactly that.**
5. **A stated triage heuristic, not just a location.** For both tasks and services: command,
   creating user, execution context, trigger interval, fleet baseline. Students are given a
   *decision procedure*, not a fact to look up. Our micro-pages should carry one of these per
   artifact family.

What **not** to copy: the room never leaves the live machine, so nothing is hashed, nothing is
acquired, and no chain of custody exists. For us that is a violated standing rule (R9/D20), and it
is the gap our version must close — **acquire, verify, then analyse the copy.**

## 6. Question patterns

18 answer inputs across 11 tasks; T1 and T11 are gates, so **16 real questions**:
T2 ×3, T3 ×2, T4 ×2, T5 ×3, T6 ×1, T7 ×0, T8 ×1, T9 ×2, T10 ×1.

- **The strongest question design of the five rooms**, because several questions are explicitly
  *paired to force a method contrast*. T2 asks what the logs reveal; T3 then asks
  **"aside from the scheduled tasks from Windows Event Logs, what does the *second* malicious
  scheduled task execute?"** — i.e. the one the logs never captured. T4 does the same for
  services. **The question itself teaches that the log-based sweep was incomplete.** That is a
  question pattern we should steal wholesale.
- **Defanged-URL format is requested explicitly** (`format: defanged URL`). Small, and correct —
  it builds a safe-handling habit into the answer format. **Adopt this in our cases.**
- **Timestamp formats are specified per question** (`MM/DD/YYYY HH:MM:SS`) and one asks for a
  **timezone-normalised** answer ("in the UTC timezone"). That is better than rooms 1–4 and
  reinforces why `S5-02`'s TimeZoneInformation row matters.
- **Cross-artifact correlation is required but never over-reached**: the Teams question chain goes
  attachment name → the URL inside it; the Firefox chain goes phishing URL → access time → the
  O365 cookie found on the wrong domain.
- **Still zero "this cannot be determined" answers** — fifth room, same omission, and by now this
  is clearly a platform-wide pattern rather than a per-room oversight. **Our cases are
  differentiated by exactly this.** This room hands us three candidates: the Edge cache
  ("can you determine which page the user was on?" — no), the service Last Write Time ("is this
  the creation date?" — no, only if never modified), and the missing 4698 ("does the absence of a
  creation event prove no task was created?" — no).

## 7. Figures we would need to draw

57 images — the most of any room — and overwhelmingly GUI screenshots and command output, i.e.
click paths and answers. Four concepts deserve our own inline SVG:

| room figure showed | our SVG spec (one line) |
|---|---|
| the log-vs-manual duality (structural, never drawn) | two parallel lanes for one artifact — "audit policy ON → event ID" above, "audit policy OFF → on-disk/registry/PowerShell" below — converging on the same finding, captioned "the second lane is not optional" |
| a scheduled task's Settings tab (screenshot) | four labelled switches — run-if-missed · restart-on-failure · stop-after · **auto-delete** — each annotated with the attacker benefit, with auto-delete flagged as the evidence-destroying one |
| Firefox `moz_places` → `moz_historyvisits` join (two table screenshots) | a two-table join diagram keyed on `place_id`, with the `visit_type` legend beside it and types 4/5/6/8 tinted as "not a deliberate visit" |
| the Teams path change (not in the room at all — it predates it) | a before/after path diagram: Teams 1.x `%APPDATA%\...\Teams\IndexedDB` vs Teams 2.x `%LOCALAPPDATA%\Packages\MicrosoftTeams_...\EBWebView\...`, captioned "same evidence, different client, different disk" |

The last one is ours entirely — it is the correction, not the room. Never their images (D22).

## 8. Fit against our material

### 🔴 Part 1's mapping for this room is WRONG

Part 1 lists this room as feeding **`S5-05` prefetch** and **`S5-06` amcache/shimcache**.
**The room mentions neither artifact anywhere.** It is scheduled tasks, services, browsers and
Microsoft 365 apps. The Feeds column must be corrected. That is now **three of five rooms
mis-mapped** in Part 1 (this one, room 2, and room 4's session) — the Part 1 table was built from
room titles, not room contents, and should be treated as provisional until each room is extracted.

### ✅ Closes room 1's scheduled-tasks gap, and adds services

This room supersedes room 1 as the source for the proposed persistence row. Room 1 gave the
location and a GUI walk; this room gives **both audit event IDs, the XML structure, the
created-vs-modified mismatch tell, the full PowerShell enumeration, and the four abused Settings
fields** — plus services as a parallel persistence mechanism our map also lacks.

Revised proposal, superseding room 1's `S5-06b`:

> `S5-06b` · Persistence artifacts — scheduled tasks (`C:\Windows\System32\Tasks`, EID 4698/4702)
> and services (`HKLM\SYSTEM\CurrentControlSet\Services`, EID 7045/4697): where they live, what
> the Settings/Recovery fields let an attacker do, and why the log sweep is never sufficient ·
> M4 · prereq `S5-01` · S5 · hands-on Yes · **20 min** (was 15) · `F` · EVS-02

### 🔴 UNANSWERED SCOPE QUESTION — browser forensics is nowhere in the course

Grepped the entire `topic_map.md` for browser, Chrome, Firefox, Edge, email, Outlook, Teams,
OneDrive, cloud, SQLite, service. **Zero matches.** Not a single row.

`scope_decisions.md` excludes **cloud and mobile forensics** (line 194) — which cleanly disposes
of **Teams and OneDrive**, and arguably of the Outlook OST's server-synced nature. But **browser
forensics is local Windows artifact analysis and is not excluded by anything.** It simply was
never decided either way.

That is a genuine hole in the design, not a minutes problem:

- **The case for including it** — INE M4 is "System & Network Forensics"; browsers are where
  user-targeted attacks land; D19's chain begins with a **malicious document delivered to a user**,
  and browser history is the natural artifact for "how did it arrive"; and `S6-05`'s C2 work has
  an obvious host-side counterpart in browsing history.
- **The case against** — 24 hours does not stretch, S5 is already 60 minutes overdrawn, and
  browser forensics is a large topic that is poorly served by a 15-minute row.

**This needs a `DECISIONS.md` row either way.** If included, it is a new row (~20 min) and S5
cannot host it. If excluded, `scope_decisions.md` must say so explicitly and
`practice_platforms.md` should point students at this room — because right now the course neither
teaches it nor declines it, which is the one state R5's discipline forbids.

### 🔴 S5 MINUTE CRISIS — final tally, all five S5 rooms extracted

| from | proposed | minutes |
|---|---|---|
| rooms 1 + 5 | `S5-06b` persistence — scheduled tasks **and services** | 20 |
| room 2 | `S5-02b` local accounts and the SAM | 15 |
| room 3 | `S5-04b` user-activity registry keys | 25 |
| room 3 | `S5-01` enrichment (dirty hives, transaction logs, tool matrix) | ~5 |
| room 5 | *browser forensics — scope undecided, not counted* | (0–20) |
| | **total demanded on S5** | **65**, before any browser decision |

**All five Priority-1 S5 rooms are now extracted. The number is final at 65 minutes** on a session
whose entire integrated block is 130. This is a re-split, not an adjustment. The four options
recorded in the room-3 note stand; the new information is that (a) the demand has stopped growing,
(b) services must join scheduled tasks in the persistence row, and (c) a browser decision could
add 20 more.

### Out of scope — the Microsoft 365 half of the room

| room content | verdict |
|---|---|
| Scheduled tasks, services (Tasks 2–4) | **IN** — the `S5-06b` proposal |
| Browser artifacts (Tasks 5–7) | **UNDECIDED** — needs a `DECISIONS.md` row, see above |
| Outlook OST + `Content.Outlook` (Task 8) | **borderline** — the OST is local, but it is a synced copy of a cloud mailbox. The `Content.Outlook` volatility lesson is worth one line in `S2-01` regardless. |
| Microsoft Teams (Task 9) | **OUT** — cloud app, excluded by `scope_decisions` line 194. Also the room's path is obsolete (§3). |
| Microsoft OneDrive (Task 10) | **OUT** — cloud storage, same exclusion. Note the *concept* (exfiltration by syncing to a personal tenant) is a good one and could be a caveat line in D19's exfiltration step without teaching the artifact. |

## 9. Links

- Room: <https://tryhackme.com/room/windowsapplications>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 3)
- Room's stated prerequisites: Intro to Endpoint Security, Windows Event Logs, the DFIR module,
  **Windows Incident Surface** (Priority 3 in our Part 1 list).
- forensicsim / Forensics.im parser: <https://github.com/lxndrblz/forensicsim> (v0.8.5, Jul 2024)
- **Teams 1.x vs 2.x artifact paths** — the correction in §3:
  <https://forensics.im/blog/parsing-microsoft-teams-indexeddb/>
- OneDriveExplorer: <https://github.com/Beercow/OneDriveExplorer>
- Microsoft Entra session cookie reference (`ESTSAUTH` / `ESTSAUTHPERSISTENT`) — cited by the room
  from Microsoft's own documentation; worth keeping for the cookie-mismatch technique.

END OF NOTE.
