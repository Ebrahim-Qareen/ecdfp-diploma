---
room: Blizzard
url: https://tryhackme.com/room/blizzard
module: Windows Endpoint Investigation — **challenge room, three machines** (Priority 2)
feeds: **S5 / S6 capstone structure** — 🟢🟢 **it investigates in REVERSE order across three hosts,
       which nothing else in the path does and which our `S6-09` should copy.**
       🔴🔴 **AND IT SETTLES THE BROWSER-FORENSICS DECISION — see §8.**
difficulty / time: Medium · 90 min · 3 tasks · **3 lab machines** · Premium · 2,274 completions
                   · 53 recommends · carries a **Badge**
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 3 tasks read in full. 0 sections NOT READ.
              🔴 Room ships plaintext RDP credentials in all three tasks — **deliberately not
              reproduced here (R8)**.
              Priority-2 room: extracted for **scenario shape and question design**. §2 is
              reconstructed from the 15 questions, which is the only artifact evidence exposed.
---

## 1. What the room teaches

**How an incident response actually runs: backwards.**

Three tasks, three separate machines, and the task titles are the method:

| task | title | machine | position in the attack |
|---|---|---|---|
| 1 | **Analysing the Impact** | `HS-SQL-01`, the database server | **last** — the alert |
| 2 | **Backtracking the Pivot Point** | an IT employee's workstation | middle — lateral movement |
| 3 | **Discovering the Root Cause** | another user's workstation | **first** — initial access |

🟢🟢 **Every other room in this path — and our own `S6-09` design — runs forward from initial
access. Real incident response does not.** You get an alert about the *end* of the attack and work
backwards to the beginning, and each machine's findings tell you which machine to look at next.
**Task 1's answer ("the attacker accessed this machine from another internal machine") is Task 2's
starting point; Task 2's answer ("what file did the attacker leverage… provide the password") is
what explains Task 1.**

That is the single most valuable structural idea in twenty rooms, and it costs nothing to adopt.

**🔴🔴 And it makes the browser-forensics question unavoidable.** Three of Task 3's five questions
are browser artifacts — the phishing URL, the phishing site's title, and the first-access timestamp
"in UTC". Task 2 requires browser downloads. **A room already on our Priority 2 list cannot be used
at all without browser forensics**, and this is the twentieth room to raise it. **§8 closes it.**

The scenario also does two things right that no other room does. It **explains why the evidence is
thin** rather than just clearing the logs — *"Since the security controls are still being
established, alerts have only come from servers, and only network-level events are being audited,
it's essential to manually investigate both servers and workstations to connect the dots"* — and it
**supplies environmental context that constrains the hypothesis space**: *"the infected database
server is set up for internal access only and is not yet linked to other systems, as it is still in
the setup phase. This information could help narrow down potential sources of the threat."* **That
is what a real IT team gives you, and using it is a skill.**

## 2. Artifacts — one 6-box block each

Reconstructed from the fifteen questions; the room exposes no walkthrough.

### 2.1 Chromium browsing history

- **What it is** — the record of pages loaded, in a SQLite database.
- **Where it lives** — **Chrome**: `%LOCALAPPDATA%\Google\Chrome\User Data\<profile>\History`.
  **Edge**: `%LOCALAPPDATA%\Microsoft\Edge\User Data\<profile>\History`. ⚠️ **`<profile>` is not
  always `Default`** — `Profile 1`, `Profile 2`, `Guest Profile` and `System Profile` are separate
  databases. **Examining only `Default` is an incomplete examination.** Tables that matter: `urls`,
  `visits`, `downloads`, `downloads_url_chains`, `keyword_search_terms`.
- **What it proves** — which URLs this profile has records for, with visit counts and times, and —
  through `visits.from_visit` and `visits.opener_visit` — **the chain that led to each one.**
  Task 3's *"URL of the malicious phishing link"*, *"title of the phishing website"* and *"when did
  the victim first access the phishing website"* all come from here.
- **What it does NOT prove** — 🔴🔴 **three separate things, and all three are gradable questions.**
  1. **That a human clicked.** `visits.transition` packs a **core type** in the low byte and
     **qualifier flags** above it. Deliberate: `TYPED(1)`, `GENERATED(5)`, `FORM_SUBMIT(7)`,
     `AUTO_BOOKMARK(2)`. Automatic: `AUTO_SUBFRAME(3)`, `AUTO_TOPLEVEL(6)`, `RELOAD(8)`, and
     anything carrying **`SERVER_REDIRECT (0x80000000)`** or **`CLIENT_REDIRECT (0x40000000)`**.
     🟢 **A `LINK` transition carrying `SERVER_REDIRECT` means the user clicked something else and
     was carried here** — which is exactly what a phishing redirect chain looks like.
  2. **That the visit happened on this machine.** `VisitSource` includes `SOURCE_SYNCED` (from
     another device), `SOURCE_EXTENSION`, three `*_IMPORTED` values, and — new and very much a 2026
     problem — **`SOURCE_ACTOR`, "Added by the GLIC actor"**. ⚠️ **Agentic browsing writes history
     rows no human generated.** The `originator_cache_guid` / `originator_visit_id` columns are how
     you tell.
  3. **That absence means non-visit.** InPrivate/Incognito writes **no** `visits` row at all — but
     *"Chrome retains bookmarks that you save and files that you download when you exit Incognito"*,
     **so look outside the profile.** Add profile switching (above) and deliberate clearing.
- **How to parse it** — **the timestamp is microseconds since 1601-01-01 UTC** (the Chromium/WebKit
  epoch): `datetime(value/1000000 - 11644473600, 'unixepoch')`.
  🔴 **Same epoch as Windows `FILETIME`, different unit — FILETIME is 100-ns intervals, Chromium is
  microseconds, a factor of 10. This is the number one conversion error students make.**
  Firefox `places.sqlite` uses **microseconds since 1970 UTC** — same unit, different epoch.
  🟢 **And this is why the room says "in UTC" on this question and not on the others: the browser
  value *is* UTC on disk, so "in UTC" means "do not apply a timezone."** Event logs are also stored
  UTC but every viewer renders them in local time. **Storage timezone and display timezone are
  different questions and you must say which you are reporting.**
- **Anti-forensics / false-positive caveat** — 🟢🟢 **cleared history is often still there.**
  SQLite's `secure_delete` is **off by default**, and freelist leaf pages are deliberately never
  read or written — so deleted rows persist as intact record bytes in freelist pages and intra-page
  freeblocks until reused. ⚠️ **Chromium's History database does not use WAL by default**
  (`kHistoryDatabaseWriteAheadLogging` is disabled), so expect `History-journal` rather than
  `History-wal` — **but the flag is field-togglable and WAL is sticky once set, so collect
  `History`, `History-journal`, `History-wal` and `History-shm` and see which exist.**

### 2.2 Browser downloads

- **What it is** — the record of files the browser fetched to disk.
- **Where it lives** — the `downloads` and `downloads_url_chains` tables in the same `History`
  database.
- **What it proves** — 🟢 **far more than "a file was downloaded".** `target_path` · `referrer` ·
  `tab_url` · `start_time` / `end_time` · `received_bytes` / `total_bytes` · `mime_type` and
  `original_mime_type` · `danger_type` · **`hash` (raw SHA-256 of the contents)** · **`opened`** ·
  `last_access_time` · `by_ext_id` / `by_ext_name` (if an extension started it).
  🟢🟢 **`downloads_url_chains` is the one to teach**: `chain_index = 0` is the URL that was
  requested, the highest index is the URL that actually served the bytes. **"The link looked like X
  but delivered from Y" is proved right here** — and that is precisely Task 2's payload question.
- **What it does NOT prove** — 🔴 **that the download finished, or that anyone opened it.** Those
  are separate fields and separate claims:
  **completed** → `state` (schema comment: `1=complete, 4=interrupted`), `received_bytes ==
  total_bytes`, non-zero `end_time`, a populated `hash`, and `current_path == target_path` (they
  differ while a `.crdownload` is in flight).
  **opened** → `opened = 1`, which is a **much stronger and quite separate claim** — it proves
  subsequent user interaction. Task 2 asks *"when did the victim open the malicious payload"*, and
  **that is a different field from the one that proves it arrived.**
  ⚠️ **Validate the `state` mapping empirically** — Chromium's in-memory enum
  (`IN_PROGRESS=0, COMPLETE=1, CANCELLED=2, INTERRUPTED=3`) does **not** match the on-disk values,
  which go through a separate conversion.
- **How to parse it** — **Hindsight** (`obsidianforensics`), current **v2026.06 (8 Jul 2026)** —
  🟢 **it now parses Firefox as well as Chromium.** Or read the SQLite directly. Autopsy's
  **Recent Activity** module parses five browsers natively (IE, Edge, Chromium, Firefox, Safari).
  ⚠️ **Eric Zimmerman ships no browser parser** — `SQLECmd` is the indirect route, and only if a
  community map exists.
- **Anti-forensics / false-positive caveat** — 🟢 **the `hash` field is the bridge to the disk.**
  A populated SHA-256 lets you match the download record against a file still present, a file in a
  quarantine store, or a hash in threat intel — **even if the file itself has been deleted.**
  ⚠️ And a `danger_type` that fired means the browser warned the user, which the user then
  overrode: **that is user-intent evidence, and no room in the path teaches it.**

### 2.3 The local email store

- **What it is** — the mailbox, cached on the workstation.
- **Where it lives** — 🔴🔴 **and this is a live currency problem.**
  **Classic Outlook**: `.ost` at `%LOCALAPPDATA%\Microsoft\Outlook\<address>.ost`; `.pst` under
  `Documents\Outlook Files\`. **Supported until at least 2029** and still overwhelmingly common.
  **New Outlook (`olk.exe`) does NOT use an OST at all.** Its local cache lives at
  **`%LOCALAPPDATA%\Microsoft\Olk\EBWebView\`** — 🟢 **which is a WebView2 (Chromium) profile
  directory**, with `data_0`…`data_3` and `index` files in the Chromium disk-cache format.
  **If the host runs new Outlook, stop looking for an OST and apply §2.1's technique instead.**
- **What it proves** — the messages this profile synced: Task 2's *"when did the attacker send the
  malicious email"*, Task 3's *"when did the victim receive the malicious phishing message"* and
  *"what is the display name of the attacker"*.
- **What it does NOT prove** — 🔴🔴 **two things, and the second is the important one.**
  1. **Internet headers may simply not exist.** `PidTagTransportMessageHeaders` is only required
     *"for outgoing messages with recipients who have an SMTP address type, and for incoming
     messages from a sender who has an SMTP address type"*. **An internal Exchange-to-Exchange
     message never traverses SMTP, so it may carry no `Received:` chain at all.** ⚠️ **Absent
     headers are the expected state for an internal message — do not let a student build a
     spoliation argument on it.** And where present, the property is a *copy* made at delivery,
     truncated at the first blank line — **not the wire.**
  2. 🔴🔴 **A sent message does NOT prove the account owner sent it — and this is Microsoft's own
     documentation, not an inference.** On the **Send As** permission: *"Allows the delegate to send
     messages as if they came directly from the mailbox or group. **There's no indication that the
     message was sent by the delegate.**"* **A legitimately configured permission produces a sent
     item indistinguishable from one the owner sent** — no compromise required. Add OAuth-token and
     session-cookie theft (AiTM), which produce the same result. 🟢 **The room's whole Task 3 premise
     is "the sender's O365 account was compromised", and this is the artifact-level reason you
     cannot conclude that from the mailbox alone.**
- **How to parse it** — **XstReader v1.14 (Jan 2025)** — free, C#, reads `.ost` directly with no
  Outlook installed, and now has command-line export. Or **`pffexport`** from `libpff`
  (Debian/Ubuntu `pff-tools`) — ⚠️ upstream is marked *alpha*, latest release **20231205** — whose
  **`-m recovered` mode recovers deleted items from PST/OST slack**, which is the free equivalent of
  a commercial suite. Autopsy has an email module over the same library.
- **Anti-forensics / false-positive caveat** — 🔴 **the authoritative record is server-side, not on
  the workstation.** Establishing who actually sent a message needs the **Unified Audit Log**
  (`Send` / `SendAs` / `SendOnBehalf`), **sign-in logs** (IP, device, MFA state), **message tracking
  logs**, and the **delegate/permission history** — none of which is on the endpoint. 🟢 **Check
  `PidTagSentRepresenting*` against `PidTagSender*`: where they diverge, a delegate is recorded.**

### 2.4 Remote logon to the server

- **What it is** — the trace of the attacker reaching `HS-SQL-01` from inside the network.
- **Where it lives** — with only *"network-level events being audited"*, the candidates are
  Security **4624** (with its LogonType), the **TerminalServices-LocalSessionManager/Operational**
  channel (21/22/24/25), and **RemoteConnectionManager 1149**.
- **What it proves** — Task 1's opening question: *"When did the attacker access this machine from
  another internal machine?"* — **and the phrasing is careful**: it asks *when*, from *another
  internal machine*, without asserting which protocol.
- **What it does NOT prove** — 🔴 **which host, without corroboration.** A source IP is an address
  at a moment; mapping it to a workstation needs DHCP or ARP evidence, and **that is exactly what
  makes Task 2 a genuine pivot rather than a hint.** ⚠️ **And LogonType matters**: type 10 is
  RemoteInteractive (RDP), type 3 is Network (SMB, WMI, WinRM) — **different techniques, different
  follow-on artifacts.**
- **How to parse it** — `EvtxECmd` over the Security and TerminalServices channels; filter
  LocalSessionManager 21/24/25 and **exclude `Source Network Address = LOCAL`** or you will
  over-count.
- **Anti-forensics / false-positive caveat** — ⚠️ **1149 fires before 21 and is not
  authentication** — *"a client launched RDP and reached the login prompt before entering any
  credentials"*. **1149 with no matching 21 is scanning or failed credentials.**
  (Same finding as `logless-hunt.md` §2.5 and `windows-network-analysis.md` §2.8 — **three rooms,
  one figure.**)

### 2.5 Execution evidence for the exfiltration binary

- **What it is** — proof that a specific program ran, and when.
- **Where it lives** — **Prefetch** (`C:\Windows\Prefetch\*.pf`), **Amcache**
  (`C:\Windows\AppCompat\Programs\Amcache.hve`), **ShimCache** (in `SYSTEM`), and — 🟢 **on a
  server, prefetch is frequently disabled**, which is worth saying before students go looking.
- **What it proves** — Task 1's *"full file path of the binary used by the attacker to exfiltrate
  data"*.
- **What it does NOT prove** — 🔴 **that it did what its name suggests, or that it succeeded.**
  The question asserts *"used… to exfiltrate data"*; execution artifacts prove **execution**.
  ⚠️ **And each of the three sources means something different**: Prefetch proves execution with a
  run count and up to eight timestamps; **ShimCache proves the file was *present and enumerated*,
  not necessarily executed**; Amcache records presence with a **SHA-1**. **Reporting "it ran"
  from a ShimCache entry is a classic and gradable error.**
- **How to parse it** — `PECmd` (Prefetch), `AmcacheParser`, `AppCompatCacheParser`.
- **Anti-forensics / false-positive caveat** — 🟢 **Amcache's SHA-1 is the pivot**: it survives
  deletion of the binary and gives you a value for threat intel and for matching against §2.2's
  download `hash`. **Two independent artifacts, one hash — that is a corroborated finding.**

### 2.6 Registry Run-key persistence

- **What it is** — an autostart entry.
- **Where it lives** — Task 1 asks for *"the registry **value name**"*, so this is a Run-key-shaped
  artifact: `…\CurrentVersion\Run` / `RunOnce` in `NTUSER.DAT` or `SOFTWARE`.
- **What it proves** — that a command is configured to execute at logon or boot.
  **ATT&CK T1547.001 — Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder.**
- **What it does NOT prove** — 🔴 **that it ever ran.** A Run key is a *configuration*; execution
  needs Prefetch, Amcache or a matching process-creation event. ⚠️ **And the value's own timestamp
  does not exist** — registry timestamps are **per key, not per value**, so the key's LastWrite
  gives you the time of the *most recent* change to *any* value under it. **"When was this value
  created?" is usually not answerable from the hive alone**, which is why Task 1 asks for the value
  *name* here and asks for a *timestamp* only about the second implant (§2.7).
- **How to parse it** — `RECmd` with the autoruns batch, or Registry Explorer; corroborate the key's
  LastWrite against the transaction logs (`.LOG1`/`.LOG2` — room 4's matrix).
- **Anti-forensics / false-positive caveat** — 🟢 **the Run key is the noisiest, best-known
  persistence location, which is why an attacker who uses it usually has a second, quieter one** —
  and the room's next question is exactly that.

### 2.7 The second, non-registry implant

- **What it is** — Task 1: *"Aside from the registry implant, another persistent implant is stored
  within the machine. When did the attacker implant the alternative backdoor?"*
- **Where it lives** — the candidates, in the order we would teach them: a **scheduled task**
  (XML in `C:\Windows\System32\Tasks` + `TaskCache` registry) · a **service** · a **Startup folder**
  shortcut · **WMI event subscription** · a **DLL search-order hijack**.
- **What it proves** — 🟢🟢 **that finding one persistence mechanism is not finding persistence.**
  The room's design makes this a graded fact rather than advice, and **that is the best question in
  the room.**
- **What it does NOT prove** — 🔴 **that there is not a third.** ⚠️ And if it is a scheduled task,
  the **`SD`-deletion technique** (`logless-hunt.md` §2.6) makes a task invisible to `schtasks`,
  Autoruns and the GUI **while it still runs** — so *"I enumerated the tasks and found nothing"* is
  not an answer. **Diff `TaskCache\Tree` against `System32\Tasks`.**
- **How to parse it** — Autoruns for the sweep, then the specific parser per mechanism. 🟢 **The
  question asks for a creation *timestamp*, which is answerable here (the task XML carries a `Date`,
  a service has a key LastWrite, a Startup shortcut has filesystem MACB) where it was not for the
  Run value (§2.6) — a nice illustration that different persistence mechanisms are differently
  datable.**
- **Anti-forensics / false-positive caveat** — 🟢 **teach the sweep, not the location.** A student
  who memorises "check Run keys" fails this question; one who runs an autoruns-class enumeration
  and then validates each hit does not.

### 2.8 A plaintext credential file

- **What it is** — Task 2: *"What file did the attacker leverage to gain access to the database
  server? Provide the password found in the file."*
- **Where it lives** — an IT employee's workstation. In practice: a `.txt`/`.xlsx`/`.kdbx`-adjacent
  notes file, a script with an embedded credential, a saved RDP `.rdp` file, or an unencrypted
  password export.
- **What it proves** — 🟢🟢 **the mechanism of the pivot, and it is the most realistic detail in the
  room.** The attacker did not exploit the database server; they read a file on an admin's
  workstation. **That is how lateral movement usually happens**, and it explains Task 1's
  "access from another internal machine" without any exploit at all.
- **What it does NOT prove** — 🔴 **that this file is where the credential came from.** The same
  password may exist in a password manager, a wiki, a ticket or another host. **Corroborate with
  file-access artifacts** — was it opened, and when, relative to the logon in §2.4? ⚠️ **And a
  credential in a file does not prove it was valid at the time of use.**
- **How to parse it** — file-system search plus **LNK, JumpLists, RecentDocs and ShellBags** to
  prove *access*, not just existence.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **and here is the handling problem the room
  creates: the question asks the student to write a real password into an answer box.**
  **Our version does not.** The finding is *"a plaintext credential for the SQL service account was
  stored at `<path>` and accessed at `<time>`"* — **the path and the access time are the evidence;
  the secret itself belongs in a restricted appendix, not in a report body, a slide, or an answer
  field (R8).** 🟢 **That is a one-line handling lesson this room hands us for free by getting it
  wrong.**

## 3. Tools and commands

The room names no tools — *"Standalone tools in the `C:\Tools` directory"* and *"Tools prepared as
desktop shortcuts"* — which, like Diskrupt, makes **tool selection part of the assessment**. The set
the fifteen questions actually require:

| artifact | tool | note |
|---|---|---|
| browser history + downloads | **Hindsight** · Autopsy *Recent Activity* · raw SQLite | ⚠️ **no EZ Tool exists** |
| browser SQLite by hand | DB Browser for SQLite **3.13.0** | ⚠️ will **not** surface freelist records |
| deleted browser rows | a carving-aware SQLite parser | `secure_delete` is off by default — §2.1 |
| OST / PST | **XstReader v1.14** · `pffexport -m recovered` | ⚠️ **new Outlook has no OST** — §2.3 |
| Teams chat | `forensicsim` **v0.8.5 (Jul 2024)** | ⚠️ stale — teach the method, not the tool |
| logons | `EvtxECmd` | exclude `LOCAL` — §2.4 |
| execution | `PECmd` · `AmcacheParser` · `AppCompatCacheParser` | three artifacts, three meanings |
| registry | `RECmd` · Registry Explorer | value timestamps do not exist — §2.6 |
| persistence sweep | Autoruns | ⚠️ blind to `SD`-deleted tasks |
| file access | `LECmd` · `JLECmd` · ShellBags Explorer | proves *access*, not existence |

KAPE targets, with the names corrected — ⚠️ **they are under `Targets/Browsers/`, not
`Targets/Apps/`, and the Edge one is `EdgeChromium.tkape`, not `Edge.tkape`**:
`Chrome.tkape` · `EdgeChromium.tkape` · `BrowserCache.tkape`.

### CURRENCY CHECK — verified 2026-08-29

| # | item | result |
|---|---|---|
| 1 | 🔴 **Chromium timestamps: same epoch as FILETIME, different unit** | Microseconds since **1601-01-01 UTC**; FILETIME is **100-ns intervals** — **a factor of 10**. `datetime(v/1000000 - 11644473600, 'unixepoch')`. Firefox is microseconds since **1970** UTC. **The #1 student conversion error.** Chromium's own header: *"an absolute point in coordinated universal time (UTC)"* — **not localised on write**, which is why "in UTC" means "apply no timezone". |
| 2 | 🟢🟢 **`transition` distinguishes a click from a redirect** | Core type in the low byte (`0xFF`), qualifiers above (`0xFFFFFF00`). **`IS_REDIRECT_MASK = 0xC0000000`** covers `SERVER_REDIRECT (0x80000000)` and `CLIENT_REDIRECT (0x40000000)`. **`CHAIN_END` without `CHAIN_START` is the landing URL of a chain; `CHAIN_START` without `CHAIN_END` is a hop the user never saw rendered.** `visits.from_visit` / `opener_visit` rebuild the chain rather than inferring it. |
| 3 | 🔴🔴 **NEW — a history row may not be from this machine or from a human** | `VisitSource`: `SOURCE_SYNCED` (another device), `SOURCE_EXTENSION`, `SOURCE_{FIREFOX,IE,SAFARI}_IMPORTED`, `SOURCE_OS_MIGRATION_IMPORTED`, and **`SOURCE_ACTOR` — "Added by the GLIC actor"**. ⚠️ **Agentic browsing writes history rows no human generated**, and this is new enough that no course covers it. `originator_cache_guid` / `originator_visit_id` are the tell. **This belongs on a slide.** |
| 4 | 🟢🟢 **cleared history is usually still on disk** | SQLite `secure_delete` is **off by default**, and freelist leaf pages are deliberately never read or written *"in order to reduce disk I/O"* — so deleted records persist intact until the pages are reused. ⚠️ **DB Browser for SQLite will not show them** — it reads the b-tree, not the freelist. |
| 5 | ⚠️ **Chromium History does NOT use WAL by default** | `kHistoryDatabaseWriteAheadLogging` is `FEATURE_DISABLED_BY_DEFAULT`. **Expect `History-journal`, not `History-wal`** — but the flag is field-togglable and **WAL is persistent once set** (*"If a process sets WAL mode, then closes and reopens the database, the database will come back in WAL mode"*). **Collect `History`, `-journal`, `-wal` and `-shm`; check which exist rather than assuming.** |
| 6 | ⚠️ **`downloads.state` — do not trust the enum** | The on-disk schema comment says `1=complete, 4=interrupted`; the in-memory enum is `IN_PROGRESS=0, COMPLETE=1, CANCELLED=2, INTERRUPTED=3`. **They differ** — history persists through a separate conversion. **Validate empirically or use a parser.** 🟢 Corroborate completion with `received_bytes == total_bytes`, non-zero `end_time`, a populated **`hash` (raw SHA-256 of contents)**, and `current_path == target_path`. |
| 7 | 🟢 **`downloads_url_chains` proves the redirect** | `chain_index = 0` is what was requested; the highest index is what served the bytes. **"The link looked like X but delivered from Y" is a single query.** |
| 8 | 🔴🔴 **new Outlook does NOT use an OST** | Classic Outlook (and OST) is *"supported until at least 2029"* and remains the enterprise norm — **the OST lesson is current.** But new Outlook (`olk.exe`) caches to **`%LOCALAPPDATA%\Microsoft\Olk\EBWebView\`**, a **WebView2 (Chromium) profile** with `data_0`…`data_3` + `index` in Chromium disk-cache format. ⚠️ **Path is observation-derived, not Microsoft-documented — teach it as such.** **Add a second lesson: if `olk.exe` is running, stop looking for an OST.** |
| 9 | 🔴 **new Teams moved, and is also WebView2** | Classic: `%APPDATA%\Microsoft\Teams\IndexedDB\*.leveldb`. **New: `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\EBWebView\Default\IndexedDB\`.** Three changes: **Roaming → Local**, into an **MSIX package container** (roaming-profile assumptions break), and **Electron → WebView2**. 🟢 **The storage tech is unchanged — still IndexedDB over LevelDB — so the parsing technique survives; only the path moved.** ⚠️ `forensicsim` v0.8.5 (Jul 2024) is two years stale and validated only to Teams 2.0 v48 — **teach the method and validate against data you generated yourself.** |
| 10 | 🟢🟢 **THE CONVERGENCE — and it is the argument that settles §8** | **New Outlook and new Teams both store their local evidence in `EBWebView\Default\` — a Chromium profile directory.** Browser forensics is no longer one artifact family; **it is the substrate for browsing, email and chat on a modern Windows endpoint.** Declining to teach it does not remove one topic, it removes three. |
| 11 | 🔴 **"a sent message proves the owner sent it" is false, per Microsoft** | On **Send As**: *"Allows the delegate to send messages as if they came directly from the mailbox or group. **There's no indication that the message was sent by the delegate.**"* **A legitimately configured permission produces an indistinguishable sent item** — no compromise needed. Add AiTM token/cookie theft. 🟢 **Check `PidTagSentRepresenting*` vs `PidTagSender*` — divergence records a delegate.** Authority is server-side: Unified Audit Log, sign-in logs, message tracking. |
| 12 | ⚠️ **internal email may carry no internet headers** | `PidTagTransportMessageHeaders` is required only *"for outgoing messages with recipients who have an SMTP address type, and for incoming messages from a sender who has an SMTP address type"*. **Exchange-to-Exchange internal mail may have no `Received:` chain at all — absent headers are the expected state, not evidence of tampering.** Where present it is *"a copy of the beginning of the message stream"*, truncated at the first blank line. |
| 13 | ✅ **tooling, current** | **Hindsight v2026.06 (8 Jul 2026)** — 🟢 **now parses Firefox**, plus service-worker data. **XstReader v1.14 (Jan 2025)** — free, C#, reads `.ost` with no Outlook, command-line export. **`libpff`/`pffexport`** — alpha, latest **20231205**; 🟢 **`-m recovered` recovers deleted PST/OST items.** **DB Browser 3.13.0 (Aug 2024)** — fine for schemas, useless for recovery. **Autopsy Recent Activity** parses IE, Edge, Chromium, Firefox, Safari. ⚠️ **Eric Zimmerman ships no browser parser** — `SQLECmd` only via a community map. |
| 14 | ➕ **Edge Collections — a user-intent artifact with no Chrome equivalent** | `…\Edge\User Data\<profile>\Collections\collectionsSQLite`. Captures **deliberately saved URLs, images and typed notes** — 🟢 **user-curated intent that survives history clearing.** Worth one slide. |
| 15 | ⚠️ **`WebCacheV01.dat` — collect it, but do not promise it** | IE11 is retired; **IE mode is supported "through at least 2029"**. KAPE still collects `…\AppData\Local\Microsoft\Windows\WebCache\`. **But no current source confirms it is still meaningfully populated on a Windows 11 host** — the fullest Microsoft reference dates to Windows 8. **Validate on our own Win11 image before teaching it as live.** |
| 16 | 🟢 **defanging has a citable source** | **IETF Internet-Draft `draft-grimminck-safe-ioc-sharing-12`** (Active, last revised 2026-06-10, intended status Informational): *"Replace 'http' and 'https' schemes with 'hxxp' and 'hxxps'"* · *"Replace every period ('.') in domain names and IP addresses with '[.]'"* · *"Replace the '@' character … with '[@]'"* · *"Using encoded characters (such as %2e for '.') SHOULD be avoided."* ⚠️ **A draft is not an RFC** — cite it as a convention with a source. 🟢 **The rationale is the teaching point** — SANS ISC: clicking a live IOC *"could not only affect the security of the user/computer but it could also leak data or **pollute statistics**"*, i.e. **it contaminates the telemetry the investigation depends on and can tip off the adversary.** ➕ **Teach refanging as a deliberate, logged step.** |

## 4. Evidence used

- **Three live Windows VMs**, one per task, each reached over RDP, each pre-loaded with a completed
  stage of one intrusion. Tools staged in `C:\Tools` and as desktop shortcuts.
- **Not downloadable. No image. Nothing for `ecdfp-evidence`.**
- 🔴 Plaintext RDP credentials in all three tasks. Not reproduced (**R8**).

### 🟢🟢 The scenario is the best-constructed in the path, and here is why

| element | what it does |
|---|---|
| **an alert with a timestamp, a name, a description and a host** | a realistic starting artifact, not "investigate this box" |
| *"only network-level events are being audited"* | **explains why the evidence is thin** without clearing logs — better than room 19's premise and far better than "the attacker deleted everything" |
| *"the database server is … not yet linked to other systems, as it is still in the setup phase"* | **environmental context that constrains the hypothesis space** — what a real IT team gives you, and using it is a skill |
| **a named threat group** (Midnight Blizzard, healthcare) | ⚠️ **double-edged** — see below |
| **an investigation guide per task** | *"Determine any unusual login attempts… Note any suspicious binaries… Look for typical persistence mechanisms"* — **a playbook, not a hint list.** The student is told *what classes of thing to look for*, never *where*. |

⚠️ **The one element to handle carefully is the named threat group.** Attributing to "Midnight
Blizzard" in the brief risks the room-18 problem in a different costume: a student who begins with
an actor in mind will read ambiguous artifacts as that actor's TTPs. 🟢 **Our version keeps the
sector context and the alert, and puts attribution where it belongs — as a question the evidence may
or may not support at the end, not a premise at the start.**

### 🟢 `EVS-08` — the three-machine chain, and it is buildable

We already have the pieces from `EVS-05`/`EVS-06`/`EVS-07`. What this adds is **the chain**:

| machine | what we stage | already have? |
|---|---|---|
| **W1** — patient zero | a phishing email in a mailbox · browser history with a redirect chain to a credential-harvest page · the download | ➕ **new: browser + email** |
| **W2** — the pivot | the received internal phish · the payload download and its `opened=1` · an implant with a C2 domain · **a plaintext credential file** | ➕ partly new |
| **S1** — the target | a network logon from W2 · an exfil binary with execution artifacts · a Run-key implant **and** a second one | ✅ mostly `EVS-07` |

🟢 **And the chain is what makes it gradable in reverse**: each machine's answer is the next
machine's question, so a student who guesses on machine 1 cannot proceed. **That is a much better
assessment property than a flat question list.**

## 5. Lab design worth reusing

1. **🟢🟢 Investigate backwards.** Impact → Pivot → Root Cause. **Nothing else in the path does
   this, and it is how the job actually works.** `S6-09` should be restructured around it.
2. **🟢🟢 One machine per stage, with the pivot as the deliverable.** The answer that ends Task 1 is
   the reason Task 2 exists. **Chain the tasks by evidence, not by syllabus order.**
3. **🟢 Explain why the evidence is thin.** *"security controls are still being established… only
   network-level events are being audited."* **More realistic than cleared logs and it teaches
   students that log coverage is a finding about the organisation.**
4. **🟢 Give environmental context that constrains, not context that hints.** The "internal access
   only, still in setup" line narrows the source of the intrusion without naming it.
5. **🟢 A per-task investigation guide framed as a playbook.** *"Determine any unusual emails or
   chats to cover the social engineering attack vectors."* **Names the objective, never the
   artifact.** This is the right level and we should copy the wording style.
6. **🟢 Ask for defanged IOCs.** *"(format: defanged)"*, twice. **A handling convention, assessed** —
   and no other room in the path does it. §3 #16 gives us the citation and the rationale.
7. **🟢 Specify UTC only where the artifact is UTC-native.** *"(format: MM/DD/YYYY HH:MM:SS in
   UTC)"* on the browser question, local elsewhere. **Deliberate, correct, and worth explaining to
   students rather than just following.**
8. **⚠️ Consistent answer formats given up front** — `MM/DD/YYYY HH:MM:SS`, `defanged`. Same
   strength as room 19, same contrast with room 18.
9. **🔴 Do NOT reuse: asking a student to type a recovered password into an answer field** (§2.8).
10. **⚠️ Handle the named threat actor differently** (§4).

### ✅ No safety defect — one handling gap

Read-only investigation of prepared hosts. The gap is §2.8: **the room asks for a plaintext
credential as an answer.** Our version asks for the path and the access time and puts the secret in
a restricted appendix (**R8**). ⚠️ Standard live-response note applies: **the student is on the box
over RDP, so their own session and tooling generate artifacts in the channels they are examining.**

**Defect tally unchanged at seven** (rooms 6, 8, 9, 12, 13, 15, 18).

## 6. Question patterns

**15 questions, 5 per task, and the design is deliberate.**

**🟢🟢 Each task's five questions walk one machine from entry to exit.** Task 2 is the clearest:
*when was the malicious email sent* (arrival) → *when did the victim open the payload* (execution) →
*when was the implant created* (persistence) → *what domain does it contact* (C2) → *what file did
the attacker leverage to reach the server* (**the pivot out**). **Arrival → execution → persistence
→ C2 → pivot.** That is a reusable per-host template and it is better than room 19's
orient/lead/artifact/classify because **it ends by handing you the next machine.**

**🟢 Nine of the fifteen are timestamps**, all in a stated format. **That is a timeline exercise
disguised as a question list** — and assembling the nine answers in order reconstructs the whole
intrusion across three hosts. 🟢 **Set that as the deliverable explicitly**: our version asks for the
timeline as the artifact, with the individual answers as its evidence.

**🟢 Two questions ask for defanged output** and one specifies UTC (§5).

**⚠️ But most stems embed their conclusion** — *"the binary used by the attacker **to exfiltrate
data**"* · *"the **malicious** email"* · *"the **malicious** persistent implant"* · *"the domain
accessed by the **malicious** implant"*. **The student is told what everything is and asked only
where.**

**🔴 Twentieth room, no question whose answer is "cannot be determined"** — and the reverse-order
structure makes the omission unusually costly, because **every pivot in this room is exactly the
kind of inference that needs qualifying:**

| the room could have asked | correct answer |
|---|---|
| *"The victim's browser history shows the phishing URL. Did they click the link in the email?"* | **Not from the history row alone** — check `transition` for `SERVER_REDIRECT`/`CLIENT_REDIRECT` and walk `from_visit`. A `LINK` transition carrying a redirect flag means they clicked **something else**. |
| *"There is no history entry for the payload URL. Was it never visited?"* | **Cannot be determined** — InPrivate writes no visit row, other profiles have separate databases, and cleared rows may still be in the freelist. |
| *"Sent Items shows the phishing message. Did this user send it?"* | 🟢🟢 **No — and Microsoft says so.** **Send As** produces a sent item with *"no indication that the message was sent by the delegate."* **Authority is the Unified Audit Log, not the mailbox.** |
| *"The download record exists. Was the file executed?"* | **Different artifact.** `opened=1` proves user interaction; execution needs Prefetch or Amcache. |
| *"ShimCache lists the exfil binary. Did it run?"* | **No** — ShimCache proves presence and enumeration. |
| *"You found a Run key. Is that the persistence?"* | 🟢 **The room already knows the answer is no** — it asks for a second implant. **But it never asks "how would you know you had found them all?"** — and an `SD`-deleted scheduled task is invisible to the obvious sweep. |
| *"The password is in this file. Is that how the attacker got it?"* | **Not established** — the same credential may exist elsewhere; corroborate with file-access artifacts. |

**Seven, and six of them are the joins the room's own structure depends on.** 🟢🟢 **A reverse-order
investigation is built entirely out of inferences from one host to the next — which makes it the
best possible vehicle for D20 criterion 4, and the room grades none of them.** Ours does.

## 7. Figures we would need to draw

Figures present in the room: **none** — a scenario table and three question lists.

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **the reverse-order investigation** | three hosts left to right in *attack* order (W1 → W2 → S1) with the **attack arrows forward** above and the **investigation arrows backward** below, numbered ③②①, and each backward arrow labelled with the artifact that made the pivot possible; caption *"you start at the alert and work outwards"* | **highest** |
| 2 | **the phishing redirect chain, from the `visits` table** | four rows of a `visits` table with their `transition` values decoded beside them — `LINK\|CHAIN_START` → `SERVER_REDIRECT` → `SERVER_REDIRECT` → `LINK\|CHAIN_END` — over the caption *"one click, four rows; only the first and last were ever seen by the user"* | **highest** |
| 3 | **what a history row does not prove** | one `visits` row with three arrows out — **"a human clicked?" → check `transition`** · **"on this machine? → check `VisitSource`"** (with `SOURCE_SYNCED` and **`SOURCE_ACTOR — agentic browsing`** called out) · **"absent means never? → Incognito, other profiles, freelist"** | **highest** |
| 4 | **the Chromium epoch trap** | one 64-bit value shown twice — divided by 10⁷ as a FILETIME and by 10⁶ as a Chromium value — landing on **two dates decades apart**; caption *"same epoch, different unit"* | **high** |
| 5 | **`downloads` — four separate claims** | the row's fields grouped into four boxes: **it was requested** (`chain_index 0`, `tab_url`, `referrer`) · **it arrived** (`state`, bytes, `end_time`, `hash`) · **it came from somewhere else** (highest `chain_index`) · **someone opened it** (`opened`, `last_access_time`); caption *"four fields, four different findings"* | **high** |
| 6 | 🟢🟢 **the WebView2 convergence** | three application icons — **Edge**, **new Outlook (`olk.exe`)**, **new Teams** — all three arrowed down into one `EBWebView\Default\` box containing `IndexedDB` · `Local Storage\leveldb` · `Cache`; caption *"browsing, email and chat are now one artifact family"* | **highest** — **this is the slide that justifies the §8 decision** |
| 7 | **who sent this message?** | a Sent Items entry with three possible authors above it — **the owner** · **a Send As delegate** ("no indication") · **a stolen session token** — and the three server-side sources below that can tell them apart; caption *"the mailbox cannot answer this"* | **high** |
| 8 | **execution evidence is three different claims** | Prefetch / Amcache / ShimCache as three columns against what each actually proves — **ran (with count and times)** · **present, with a SHA-1** · **present and enumerated** — with the ShimCache column flagged *"not execution"* | medium — reusable across S5 |

Figure 6 is the one that changes the course's scope. Never their images (**D22**).

## 8. 🔴🔴 THE DECISION: browser forensics is in scope

**Twenty rooms have raised this. It has to stop being an open item, and this room closes it.**

### The evidence for

1. **It is unavoidable in the material we have already committed to.** Three of Task 3's five
   questions here are browser artifacts. Room 16 (Autopsy) asks two web-history questions and
   **extracts browser artifacts by default** in an ingest module we are teaching. Rooms 12–14's
   image is full of `msedge.exe` processes. **We are already teaching it by accident.**
2. 🟢🟢 **It is no longer one artifact family — it is three.** §3 #10: **new Outlook and new Teams
   both store their local evidence in a WebView2 (`EBWebView\Default\`) Chromium profile.**
   Declining browser forensics does not remove one topic; it removes **browsing, email and chat**
   on a modern Windows endpoint.
3. **Phishing is the most common initial-access vector our students will actually see**, and the
   browser is where its evidence is.
4. **It is cheap.** One SQLite database, one timestamp conversion, one transition-flag decode.
   The concepts (§2.1) are the same "what it does NOT prove" discipline we teach everywhere else.

### The scope, stated tightly

**IN** — Chromium `History` (`urls`, `visits`, `downloads`, `downloads_url_chains`) · the
Chromium/WebKit timestamp · `transition` core types and redirect qualifiers · `VisitSource` ·
profile enumeration · Incognito's evidentiary meaning · deleted-row survival in freelist pages ·
downloads as four separate claims · **the WebView2 convergence (Outlook/Teams)** · defanging as a
handling convention.

**OUT** — cache reconstruction · cookie and session-token analysis beyond "it exists" · Safari ·
mobile browsers · browser extension reverse-engineering · password-store decryption
(🔴 **explicitly out — R8**).

**WHERE** — 🟢 **it is not a new session.** It lands as: a block inside **`S5`** (browser as a
user-activity artifact, beside LNK/JumpLists/ShellBags/UserAssist) · a **`S6-09`** capstone
requirement (phishing → redirect → download) · and one slide in **`S2`/`S4`** (Autopsy's Recent
Activity module already produces it).

**TOOLS** — **Hindsight v2026.06** as the primary (now covers Firefox too) · Autopsy Recent Activity
for the GUI path · raw SQLite for the teaching moment. ⚠️ **Say out loud that Eric Zimmerman ships
no browser parser** — students trained on EZ Tools will look for one.

### 🔴 Action

**Write a `DECISIONS.md` row** recording: browser forensics **IN**, at the scope above, sited in S5
and S6-09, justified by the WebView2 convergence and by rooms 12–14, 16 and 20. **This has been the
longest-standing open item in the project and it is now decided by evidence rather than deferred
again.**

⚠️ **And it has a minutes consequence**, which is the honest part: **S5 is already 65 minutes
overdrawn** and this adds to it. **The browser block is a further argument that S5 needs a
structural re-split, not that browser forensics should be dropped.**

## 9. Fit against our material

### ⚠️ Part 1 under-rates this room too

Listed as *"S5/S6 case"*. **It is the capstone structure**, plus the room that forces the browser
decision, plus the best-constructed scenario in the path. **Amend to:** *S6-09 capstone structure
(reverse-order, three-host chain); forces the browser-forensics decision; scenario-design model.*

### Rows this strengthens

- **`S6-09` capstone** — 🟢🟢 **restructure it around reverse-order investigation across three
  hosts** (§5.1–5.2). This is the single biggest structural change any room has suggested.
- **`S5`** — the browser block (§8), the email/chat block (§2.3), and the credential-file pivot
  (§2.8) as a realistic lateral-movement mechanism.
- **`S5-05` / `S5-06`** — §2.5's three-way distinction (Prefetch = ran · Amcache = present with a
  hash · ShimCache = present and enumerated) is a correction worth checking against
  `windows-applications-forensics.md`.
- **`S1`** — §2.8's handling lesson (**do not put a recovered secret in a report body or an answer
  field**), and §2.3's *"a sent message does not prove the owner sent it"*, which is a
  finding-versus-interpretation case with a **Microsoft citation**.
- **`ecdfp-evidence`** — **`EVS-08`**, the three-machine chain (§4).
- **Question-writing guidance** — the per-host template *arrival → execution → persistence → C2 →
  pivot*, and **the timeline as the deliverable** rather than fifteen loose answers.

### Five things our version must do differently

1. **Do not name the threat actor in the brief** — make attribution a question at the end (§4).
2. **Do not ask for a recovered password as an answer** — path and access time instead (§2.8).
3. **Ask the pivot questions as pivots** — *"what would you need to confirm this?"* — because a
   reverse-order investigation is made of inferences (§6).
4. **Teach the browser artifact with its three limits**, not as a lookup (§2.1).
5. **Cover the WebView2 convergence** — if the host runs new Outlook or new Teams, the technique is
   browser forensics (§3 #8–10).

### Minutes

Structural, not additive: §5.1–5.2 **restructure** `S6-09` rather than extending it, and §8's
browser block **displaces** existing S5 content. ⚠️ **But it does add to S5**, and honestly so.

**No new rows. S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Fifteenth room carrying the S5 overdraft — and the third in a row to add S5 material.**
**The re-split is now blocking, not deferred.**

### Out of scope

Exploitation, phishing-kit analysis, O365/Entra-side investigation (the room correctly stops at the
endpoint and says the O365 compromise is what it is *trying to explain*). ⚠️ **Note for `S6`**: the
authoritative answer to Task 3's underlying question lives in the **Unified Audit Log and sign-in
logs**, not on any of the three workstations — **worth one slide saying so.**

### Still unresolved

**S5 re-split** — fifteenth room, now blocking.
**S4 capstone weighting** — from room 18.
~~**Browser forensics**~~ — 🟢 **decided in §8.**

## 10. Links

- Room: <https://tryhackme.com/room/blizzard>
- Room's stated prerequisites, all six extracted: Windows Forensics 1 (≈ `compromised-windows-analysis`)
  · `expediting-registry-analysis` · `windows-network-analysis` · `windows-user-activity` ·
  `windows-user-account-forensics` · `windows-applications-forensics`.
- **Chromium**: user data dir
  <https://chromium.googlesource.com/chromium/src/+/master/docs/user_data_dir.md> ·
  the UTC/epoch statement <https://chromium.googlesource.com/chromium/src/+/HEAD/base/time/time.h> ·
  **downloads schema**
  <https://chromium.googlesource.com/chromium/src/+/HEAD/components/history/core/browser/download_database.cc> ·
  **PageTransition types and qualifiers**
  <https://chromium.googlesource.com/chromium/src/+/HEAD/ui/base/page_transition_types.h> ·
  **`VisitSource` incl. `SOURCE_ACTOR`**
  <https://chromium.googlesource.com/chromium/src/+/HEAD/components/history/core/browser/history_types.h>
- **SQLite**: freelist and freeblocks <https://sqlite.org/fileformat2.html> ·
  `secure_delete` default off <https://sqlite.org/pragma.html> ·
  WAL is persistent <https://sqlite.org/wal.html>
- **Firefox**: profile paths <https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data>
  · `places.sqlite` schema <https://searchfox.org/mozilla-central/source/toolkit/components/places/nsPlacesTables.h>
- **Outlook**: classic supported to 2029
  <https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/guide-product-availability>
  · 🔴 **new Outlook has no OST** <https://office365itpros.com/2024/10/10/offline-access-new-outlook/>
  · `PidTagTransportMessageHeaders`
  <https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxomsg/28f67517-0f35-4b87-a78d-8d5029141db0>
  · 🔴 **Send As leaves "no indication"**
  <https://learn.microsoft.com/en-us/exchange/recipients-in-exchange-online/manage-permissions-for-recipients>
- **Teams**: new-vs-classic local paths
  <https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-administration/clear-teams-cache>
  · IndexedDB parsing <https://forensics.im/blog/parsing-microsoft-teams-indexeddb/> ·
  `forensicsim` <https://github.com/lxndrblz/forensicsim>
- **Tools**: Hindsight <https://github.com/obsidianforensics/hindsight/releases/latest> ·
  XstReader <https://github.com/Dijji/XstReader/releases> ·
  libpff <https://github.com/libyal/libpff> ·
  Autopsy Recent Activity <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/recent_activity_page.html> ·
  BrowsingHistoryView <https://www.nirsoft.net/utils/browsing_history_view.html>
- **Defanging**: IETF draft <https://datatracker.ietf.org/doc/draft-grimminck-safe-ioc-sharing/> ·
  SANS ISC, *Defang all the things!* <https://isc.sans.edu/diary/22744>
- Companion notes: `logless-hunt.md` (RDP events, persistence, the same 1149 finding) ·
  `diskrupt.md` §4 (scenario framing, the counter-example on naming a suspect) ·
  `autopsy.md` §4 (CFReDS, the real-image evidence route)
- Tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` — **needs a block H for browser,
  email and chat artifacts; see §3.**
