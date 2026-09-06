---
room: Windows Network Analysis
url: https://tryhackme.com/room/windowsnetworkanalysis
module: Windows Endpoint Investigation
feeds: **S6** — `S6-02` (network artifacts on the host) and `S6-05` (live triage).
       Also **S2** (order of volatility, live vs dead acquisition) and **S5** (SRUM is an
       execution/usage artifact).
       🔴 **Carries a licensing change that affects our whole KAPE story — see §3 #8.**
difficulty / time: Medium · 45 min · 6 tasks · Premium · 5,079 completions · 113 recommends
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 6 tasks read in full. 0 sections NOT READ.
              ⚠️ Two section headings in Task 3 ("Viewing Named-Pipes", "Querying WinRM Sessions")
              carry explanatory prose and **no command** — the room promises and does not deliver.
              That is the room's content, not a gap in this extraction.
---

## 1. What the room teaches

**Live network triage on a Windows host, using only what is already installed.** The framing is
correct and it is the one thing no other room in the path says:

> *"Often in the initial stages of an incident, you may not be able to install all of your fancy
> tooling. It's essential to know how to work with the Operating System to capture the evidence you
> need."*

Four groups of artifacts: **SRUM** and the **Windows Firewall log** (historical) · a **PowerShell
triage set** (`Get-NetTCPConnection`, `Get-NetUDPEndpoint`, `Get-DnsClientCache`,
`Get-SmbConnection`, `qwinsta`, the hosts file) · **`pktmon`** and **`netstat`** (built-in) · then a
two-machine practical against a live C2 agent.

**🟢🟢 SRUM is the find.** `C:\Windows\System32\sru\SRUDB.dat` records **bytes sent and bytes
received, per application, per user, per hour, for roughly 30–60 days.** Nothing else on a Windows
host answers *"how much data left, through what, and when"* without a packet capture. **We had no
artifact for exfiltration volume. Now we do.** It also belongs in S5 as an execution artifact.

**🔴 But the room is live response taught without a single word about the observer effect.** Every
command in it runs on the evidence system: `pktmon start -c` writes a 512 MB circular ETL into the
system directory; `netstat -a -o > netstat.txt` writes a file to the suspect host; `netstat` without
`-n` makes the compromised host issue DNS queries; and each PowerShell invocation adds prefetch,
process-creation and PowerShell-history artifacts. **No order of volatility, no RFC 3227, no
"document what you touched."** After room 15 taught hashing and then invalidated the hash, this is
the same failure in the other direction: **the method is sound and the handling discipline is
absent.**

## 2. Artifacts — one 6-box block each

### 2.1 SRUM — the System Resource Usage Monitor database

- **What it is** — Windows' own per-application resource accounting: network bytes, energy, process
  and service activity, push notifications.
- **Where it lives** — **`C:\Windows\System32\sru\SRUDB.dat`**, an **ESE (Extensible Storage Engine
  / JET Blue)** database — the same engine as Active Directory, Exchange and Windows Search.
  Providers are registered under
  `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SRUM\Extensions`.
- **What it proves** — 🟢🟢 **bytes sent and received, attributed to an application and a user.**
  The Network Data Usage Monitor table `{973F5D5C-1D90-4944-BE8E-24B94231A174}` carries
  `TimeStamp`, `AppId`, `UserId`, `InterfaceLuid`, `L2ProfileId`, **`BytesSent`**, **`BytesRecvd`**;
  `SruDbIdMapTable` resolves `AppId` to a string and `UserId` to a **SID**. Other tables:
  `{DD6636C4-…}` network connectivity · `{D10CA2FE-…FA89}` application resource usage ·
  `{5C8CF1C7-…}` app timeline · `{FEE4E14F-…}` energy usage · `{D10CA2FE-…FA86}` push notifications.
- **What it does NOT prove** — 🔴 **five limits, none of which the room states.**
  1. **It is hourly and bucketed** — *"an hourly, bucketed count of how many bytes were sent and
     received"*. **You cannot time a transfer from SRUM**, only the hour it fell in.
  2. **The last ~hour is missing.** SRUM is two-tier: a **Tier1 in-memory store updated every 60
     seconds** and a **Tier2 on-disk database updated every hour** (and at shutdown). ⚠️ On
     Windows 10 2004 and later, *"SRUDB.dat is not always written on shutdown"*. **Up to an hour of
     data exists only in memory** — which makes SRUM an argument for capturing RAM first.
  3. **VPN and proxy attribution is wrong by design.** When traffic goes over a VPN, *"bytes
     in/out will be associated with the VPN process/service"*, not the originating application.
  4. **No destination.** SRUM records volume and process. **It does not record who the bytes went
     to.** Pair it with `netscan`, the firewall log, or NetFlow.
  5. **Retention varies by table** — 60 days for network and application usage, **7 days** for App
     Timeline, and five years for the long-term (`}LT`) tables.
- **How to parse it** — the file is **locked on a live system** and usually **dirty** when copied.
  Repair before parsing: `esentutl.exe /r sru /i` then `esentutl.exe /p SRUDB.dat`. Then either:
  - **`SrumECmd`** (Eric Zimmerman) — `SrumECmd.exe -f SRUDB.dat -r SOFTWARE --csv <out>`,
    current version **2026.5.0**, CSV output, **and it is what KAPE's `!EZParser` actually runs**;
  - or **`srum-dump` v3.2** (Mark Baggett) — **rewritten in 2025**, JSON-driven, XLSX or CSV.
  🔴 **The `SRUM_TEMPLATE.xlsx` the room tells students to supply no longer exists** — see §3 #6.
  The **SOFTWARE hive** is needed to resolve interface and profile IDs; KAPE's `SRUM.tkape` target
  collects it for exactly that reason.
- **Anti-forensics / false-positive caveat** — 🟢 **SRUM is a volume artifact, and volume is the
  question exfiltration cases turn on.** But it is also **quietly deletable** — it is one file, and
  an attacker with SYSTEM can stop the service and remove it. ⚠️ **Volume Shadow Copies preserve
  historical SRUM state** and are the way to get more than the retention window. 🔴 **And the room's
  own practical proves the false-positive risk**: it asks students to identify *"another process
  that has sent a large amount of bytes, indicating data exfil"* — **a large byte count is a lead.
  Backup agents, updaters, cloud sync and video calls all top that chart on a normal day.**

### 2.2 The Windows Firewall log

- **What it is** — a W3C-style text log of packets the firewall allowed or dropped.
- **Where it lives** — **`%windir%\System32\LogFiles\Firewall\pfirewall.log`**, with one prior
  generation as `pfirewall.log.old`. ⚠️ **Configured and stored per profile** (Domain / Private /
  Public) — a host can be logging on one profile and blind on another.
- **What it proves** — a 5-tuple with a verdict and a direction. Fields:
  `date time action protocol src-ip dst-ip src-port dst-port size tcpflags tcpsyn tcpack tcpwin
  icmptype icmpcode info path`, where **`path` is the direction** — `SEND`, `RECEIVE`, `FORWARD`
  or `UNKNOWN`.
- **What it does NOT prove** — 🔴🔴 **almost certainly nothing at all, because logging is OFF by
  default.** Microsoft: *"No logging occurs until you set one of following two options"* — and the
  two options, **Log dropped packets** and **Log successful connections**, are **independent and
  both default to No**. 🟢 **The room says to check first** (*"Before proceeding, check if logging
  is enabled"*), which is the right instinct and is the single most important sentence in the task.
  Beyond that: **no payload · no process name · no PID · no user or SID · and nothing from before
  logging was turned on.** ⚠️ **Default max size is 4,096 KB** (settable to 32,767 KB), so a busy
  host overwrites its own history in hours.
- **How to parse it** — `Get-Content …\pfirewall.log`; for real work, import to a spreadsheet or a
  log tool on the **analyst's** machine, not the suspect's.
- **Anti-forensics / false-positive caveat** — 🔴 **the common configuration logs drops only**, so
  **successful C2 is absent even on a host that is "logging".** 🟢 **This is the cleanest
  "absence is not evidence of absence" artifact in the whole path** — three independent reasons the
  log can be empty while traffic flowed: logging off, allowed-connections not logged, and rollover.
  **Use it in `S1`.**

### 2.3 Active TCP connections and their processes (`Get-NetTCPConnection`)

- **What it is** — the live TCP connection table, joined to the owning process.
- **Where it lives** — kernel TCP state, exposed through the **NetTCPIP** module.
- **What it proves** — 🟢 the room's headline one-liner is genuinely good: it joins
  `LocalAddress`, `LocalPort`, `RemoteAddress`, `RemotePort`, `State`, the **process name** and the
  **full command line**, sorted by remote address. **Command line is the part that matters** —
  a process name alone tells you nothing.
- **What it does NOT prove** — 🔴 **that the connection is what its port implies** (the room's own
  practical asks *"a popular port for reverse shells is currently active — what is the port
  number?"*, training exactly the reflex room 14 got wrong). It also does not prove **duration** —
  `CreationTime` is the connection's start, and a closed connection is simply gone. ⚠️ **And the
  process is the current owner of the socket**, not necessarily what opened it.
- **How to parse it** — 🔴 **the room's one-liner will not run on PowerShell 7.** It uses
  `Get-WmiObject`, which was superseded in PowerShell 3.0 and **removed outright in PowerShell 6/7**
  (*"The following WMI v1 cmdlets were removed from PowerShell: … Get-WmiObject …"*). Correct form:

  ```powershell
  Get-NetTCPConnection | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,
    @{n='Process'; e={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}},
    @{n='CmdLine'; e={(Get-CimInstance Win32_Process -Filter "ProcessId = $($_.OwningProcess)").CommandLine}} |
    Sort-Object RemoteAddress -Descending | Format-Table -Wrap -AutoSize
  ```

  ⚠️ Better still for a real host: pull `Get-CimInstance Win32_Process` **once** and join on
  `ProcessId` — the room's version fires one WMI query per connection.
- **Anti-forensics / false-positive caveat** — 🟢 **`Get-NetTCPConnection` never resolves names**,
  which makes it structurally safer than `netstat` on a compromised host (§2.6). ⚠️ It shows only
  **currently open** sockets — for closed and terminated ones you need memory (`windows.netscan`,
  room 14) or the firewall log.

### 2.4 The DNS client cache (`Get-DnsClientCache`)

- **What it is** — the host's in-memory record of recent name resolutions.
- **Where it lives** — memory only, held by the **DNS Client (`Dnscache`) service**. Never written
  to disk.
- **What it proves** — 🟢 **which domains this host resolved recently.** The room's own output is
  the finding: `attacker.thm  A  Success … 10.10.182.37`. The `TimeToLive` column is the
  **remaining** lifetime in seconds, so **original TTL minus observed TTL ≈ seconds since the
  lookup** — a rough age estimate that most students never realise is there.
- **What it does NOT prove** — 🔴🔴 **that the host connected to the name, or that a missing name
  was never resolved.** A resolution is not a connection. And the cache is destroyed by: a reboot ·
  `ipconfig /flushdns` / `Clear-DnsClientCache` · **TTL expiry** · restarting or **stopping the
  Dnscache service**. ⚠️ **An attacker who stops `Dnscache` erases this artifact entirely and
  leaves nothing to collect** — and a stopped service is itself the finding.
- **How to parse it** — `Get-DnsClientCache`. 🟢 **Collect it FIRST**, before any command that
  resolves names — see §2.6.
- **Anti-forensics / false-positive caveat** — 🔴 **the responder pollutes it.** Every
  name-resolving command the examiner runs writes new entries into the very cache they are about to
  collect. **This is the observer effect in its most concrete form and it is a two-line
  demonstration.**

### 2.5 The hosts file

- **What it is** — a static name-to-address override consulted **before** DNS.
- **Where it lives** — `C:\Windows\System32\Drivers\etc\hosts`.
- **What it proves** — 🟢 **redirection**. The room's example is `192.168.0.200  attacker.thm`, and
  its explanation of why this matters is the best writing in the room: an attacker can point a
  legitimate domain at their own server *"whilst all the user will see is the correct URL"* —
  the mechanism behind a long line of banking trojans and credential-harvesting attacks.
- **What it does NOT prove** — 🔴 **who wrote the entry, or when.** The file has one mtime for the
  whole file; individual lines are undated and unattributed. Corroborate with the **USN journal**,
  **Amcache/Prefetch** for whatever edited it, or a **VSS copy** of the previous version. ⚠️ **And
  entries do not prove use** — an override only matters if something resolved that name afterwards
  (which the DNS cache, §2.4, may or may not still show).
- **How to parse it** — `Get-Content C:\Windows\System32\Drivers\etc\hosts`. **Read the whole file,
  not the tail** — the room's `gc -tail 4` would miss an entry planted at the top, and attackers
  pad with blank lines precisely so the interesting line scrolls out of a casual look.
- **Anti-forensics / false-positive caveat** — 🟢 **a shadow-copy diff of `hosts` is a
  five-second, high-yield check** and nothing in the path teaches it. ⚠️ Note the file is also
  legitimately edited by developers, ad-blockers and licence tools — **a non-empty hosts file is
  normal.**

### 2.6 `netstat` — and the two flags that matter

- **What it is** — the classic connection lister, still present on every Windows host.
- **Where it lives** — `%SystemRoot%\System32\netstat.exe`.
- **What it proves** — with `-a -o` you get every connection and listening port **with a PID**;
  with `-b` you get the **executable** responsible.
- **What it does NOT prove** — 🔴 **`-b` frequently fails and the failure looks like data.**
  Microsoft: *"this option can be time-consuming and **will fail unless you have sufficient
  permissions**."* The `Can not obtain ownership information` lines throughout the room's own
  output are the symptom — usually an unelevated shell, and sometimes protected/System processes
  (PID 4) even when elevated. **A student reading that output will assume those connections have no
  owner.**
- **How to parse it** — 🔴🔴 **`netstat -anob`, and the `-n` is not optional on a compromised
  host.** Microsoft: without `-n`, *"no attempt is made to determine names"* is precisely what you
  lose — meaning **the evidence host issues DNS and reverse-lookup queries at the moment of
  collection.** Three consequences:
  1. **It contaminates the evidence** — new entries in the DNS cache (§2.4) and new rows in SRUM's
     network tables (§2.1), both of which you are about to collect.
  2. **It can tip off the adversary** — reverse lookups of attacker infrastructure are observable
     from their side.
  3. **It hangs** on unreachable DNS, turning a one-second command into minutes — on top of `-b`
     already being slow.
  🔴 **The room never uses `-n` and never mentions it.**
- **Anti-forensics / false-positive caveat** — ⚠️ `netstat -a -o > netstat.txt` **writes a file to
  the suspect host.** Redirect to removable media or a mapped share, and **record that you did**.

### 2.7 `pktmon` — the built-in packet capture

- **What it is** — Microsoft's in-box packet sniffer, hooked into **NDIS**.
- **Where it lives** — `pktmon.exe`, present since **Windows 10 1809** and documented from
  **build 19041 (2004)**; current on Windows 10, Windows 11, Server 2016/2019/2022/2025.
- **What it proves** — packets, with the component of the network stack each was seen at, and —
  uniquely — **which packets were dropped and why**. Verbs: `filter · list · start · stop ·
  status · unload · counters · reset · etl2txt · etl2pcap · hex2pkt · help`. ⚠️ **The room's list
  is missing `status`, `unload` and `hex2pkt`, and lists `comp`, which is a parameter of `start`,
  not a verb.**
- **What it does NOT prove** — 🔴🔴 **three hard limits, none of them in the room.**
  1. **Loopback traffic is invisible** — *"PktMon cannot … trace loopback traffic, since the Windows
     loopback implementation does not use NDIS."* **Local proxies, C2 relays and `127.0.0.1` pivots
     do not appear.**
  2. **Packets are truncated to 128 bytes by default** (`--pkt-size`); set `--pkt-size 0` for full
     packets or payload analysis is silently ruined.
  3. **`etl2pcap` throws away what pktmon is for** — *"all information about the packet drop
     reports and packet flow through the networking stack is lost in pcapng format output."*
     Dropped packets are **not included by default** (`--drop-only` is a second pass), and captures
     from **802.11 links convert incorrectly** and are mis-decoded by Wireshark.
  ⚠️ And it sits below TLS, so application payloads remain encrypted.
- **How to parse it** — `pktmon start -c` (`--capture` is the same flag), `pktmon stop`,
  `pktmon etl2pcap`. **Requires elevation.**
- **Anti-forensics / false-positive caveat** — 🔴🔴 **it writes to the evidence system.** The
  defaults are **`PktMon.etl`, circular, 512 MB** — into the **current working directory**, which
  from an elevated prompt is `System32`. ⚠️ **The room's "768 MB memory" figure is not in
  Microsoft's documentation and is contradicted by it** — the memory-mode buffer is governed by
  `--file-size`, i.e. 512 MB. **Half a gigabyte written into the system directory of a host under
  investigation is a decision, and it must be a documented one.**

### 2.8 Remote-session artifacts (`qwinsta`, `Get-SmbConnection`)

- **What it is** — who is connected to this host, and what it is connected to.
- **Where it lives** — `qwinsta` reads the Terminal Services session table; `Get-SmbConnection`
  (SmbShare module) reads the SMB client's connection list.
- **What it proves** — `qwinsta` gives **SESSIONNAME · USERNAME · ID · STATE · TYPE · DEVICE** —
  the room's output showing `rdp-tcp#2  Attacker  2  Active` is a live RDP session with a username.
  `Get-SmbConnection` gives **ServerName · ShareName · UserName · Credential · Dialect ·
  NumOpens** — outbound SMB, with the dialect (`3.1.1`) and the credential in use.
- **What it does NOT prove** — 🔴 **`qwinsta` does not show the source IP, and the room says it
  does.** Its documented columns contain no address field of any kind. The room's claim that it
  *"will show the user status, as well as source of the connection"* is **wrong**, and a student
  will look for a column that does not exist.
- **How to parse it** — for the **RDP source address**, go to the event logs:
  - **Event ID 1149** in **`Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational`**
    — source IP in `Param3`, username in `Param1`. ⚠️ **Critical caveat**: *"this event does not
    indicate a successfully authenticated RDP session has taken place, only that the channel has
    been established"* — **1149 without a matching 4624 is a failed or abandoned attempt**, and that
    pattern is the brute-force indicator.
  - **Security 4624, LogonType 10** — the authenticated logon, with *Source Network Address*.
  - **4778 / 4779** — session reconnected / disconnected.
  - **`Microsoft-Windows-TerminalServices-LocalSessionManager/Operational`** IDs **21** (logon),
    **22** (shell start), **23** (logoff), **24** (disconnect), **25** (reconnect) — the session
    lifecycle that neither 1149 nor 4624 gives you.
- **Anti-forensics / false-positive caveat** — 🔴 **both cmdlets show only what is live right now.**
  A disconnected session, a closed SMB connection and a logged-off RDP user are all invisible.
  **The event log is the historical record; these two are the snapshot.** ⚠️ And if the examiner is
  themselves connected over RDP, **their own session is in the `qwinsta` output** — the
  responder-footprint problem from room 13, in a different tool.

## 3. Tools and commands

| artifact | command as the room writes it | our verdict |
|---|---|---|
| SRUM collection | KAPE `--module SRUMDump --target SRUM` | 🔴 **no such module** — it is `SrumECmd` (§3 #7) |
| SRUM parsing | `srum-dump` + `SRUM_TEMPLATE.xlsx` | 🔴 **template no longer exists** (§3 #6) |
| firewall log | `gc C:\Windows\System32\LogFiles\Firewall\pfirewall.log \| more` | ✅ path correct; ⚠️ **off by default** |
| TCP + process + cmdline | `Get-NetTCPConnection … Get-WmiObject Win32_Process …` | 🔴 **`Get-WmiObject` removed in PS 6/7** |
| UDP endpoints | `Get-NetUDPEndpoint \| select local*,creationtime,remote*` | ✅ ⚠️ UDP endpoints have no remote address |
| unique remote IPs | `(Get-NetTCPConnection).remoteaddress \| Sort-Object -Unique` | 🟢 clean, safe, exportable |
| drill into one IP | `Get-NetTCPConnection -remoteaddress <ip> \| select state,creationtime,localport,remoteport` | 🟢 good |
| DNS cache | `Get-DnsClientCache \| ? Entry -NotMatch "…"` | ✅ — **collect this first** |
| hosts file | `gc -tail 4 "…\etc\hosts"` | ⚠️ **read the whole file**, not the tail |
| RDP sessions | `qwinsta` | ✅ — 🔴 but it shows **no source IP** (§2.8) |
| SMB connections | `Get-SmbConnection` | ✅ |
| packet capture | `pktmon start -c` … `pktmon etl2pcap` | ⚠️ writes 512 MB to the evidence host |
| connections | `netstat -a`, `-b`, `-o`, `-p`, `> netstat.txt` | 🔴 **`-n` missing and it matters** |

### CURRENCY CHECK — verified 2026-08-28

| # | item | result |
|---|---|---|
| 1 | 🔴🔴 **`Get-WmiObject` is REMOVED in PowerShell 6/7** | Superseded in PowerShell **3.0**; Microsoft lists it under *"Cmdlets removed from PowerShell"*: *"The following WMI v1 cmdlets were removed from PowerShell: Register-WmiEvent, Set-WmiInstance, Invoke-WmiMethod, **Get-WmiObject**, Remove-WmiObject."* **The room's headline one-liner fails on PowerShell 7.** Replacement: `Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $($_.OwningProcess)"`. Corrected one-liner in §2.3. |
| 2 | ✅ the four Net/DNS/SMB cmdlets are current | `Get-NetTCPConnection` and `Get-NetUDPEndpoint` (**NetTCPIP**), `Get-DnsClientCache` (**DnsClient**), `Get-SmbConnection` (**SmbShare**). All documented against Server 2025, none deprecated, and **all three modules are "Natively Compatible" with PowerShell 7** — no compatibility shim. Both NetTCPIP cmdlets expose `OwningProcess`, which is the join key. |
| 3 | 🔴 **SRUM retention: the room's "30 to 60 days" is loose, and per-table** | Best-sourced default is **60 days** for Network Data Usage, Network Connectivity and Application Resource Usage; **7 days** for App Timeline; **5 years** for long-term (`}LT`) tables. Other reputable sources say 30. **Teach it as "roughly 30–60 days, varies by table", never as a hard number.** |
| 4 | 🔴 **SRUM's registry staging is a legacy claim** | It was true on Windows 8/8.1 (staged under `…\CurrentVersion\SRUM`). On Windows 10/11 *"SRUM no longer uses the registry to store temporarily database records"* — the registry holds table names only. **The Tier1 store is in memory.** ⚠️ **Our material must not repeat the "check the registry for the last hour" advice** that circulates widely; **the last hour is in RAM**, which is a fresh argument for memory-first acquisition. ⚠️ Also: from **Windows 10 2004 onward, SRUDB.dat is not always written on shutdown.** |
| 5 | ⚠️ **SRUM retention registry values — NOT VERIFIED, likely fabricated** | `SruDbIdleRetentionPeriod` and `SruDbRolloverTimeSpan` circulate in DFIR write-ups. Exact-phrase searches return **nothing**, and no Microsoft or research source documents any registry value that sets SRUM retention. **Do not put these value names in our material.** The only documented SRUM key is the **provider registration** key, which does not control retention. |
| 6 | 🔴 **`srum-dump` was rewritten — the XLSX template is gone** | Current **v3.2 (Jun 2025)**; v3.0 announced in SANS ISC, **27 Apr 2025**. **Version 3 IS the rewrite** — there is no "srum-dump2". Inputs are now **SRUDB.dat (required)** and the **SOFTWARE hive (optional, "provides useful additional context")**; configuration is `srum_dump_config.json` and output is selectable XLSX **or CSV**. **`SRUM_TEMPLATE.xlsx` survives only in stale forks.** The room's instruction to supply a template is obsolete. |
| 7 | 🔴 **KAPE has no `SRUMDump` module — it has `SrumECmd`** | `Modules/Apps/SRUMDump.mkape` **404s** and no such file is findable. What exists: **`Modules/EZTools/SrumECmd.mkape`** (Category `SRUMDatabase`, `-d %sourceDirectory% --csv %destinationDirectory%`), and it is one of the 15 processors inside **`!EZParser.mkape`**. Target **`Targets/Windows/SRUM.tkape`** collects `C:\Windows\System32\SRU\` recursively **plus the SOFTWARE hive and its `.LOG*` transaction files** — precisely because SrumECmd wants `-r`. **`SrumECmd` current version 2026.5.0**, CSV output. |
| 8 | 🔴🔴 **KAPE IS NO LONGER FREE FOR COMMERCIAL USE — and this is a course-wide decision** | Official KAPE FAQ: *"KAPE is free for any local, state, federal or international government agency. KAPE is also free for educational, research, and internal company use."* and **"As of January 1, 2026 KAPE IS NO LONGER AVAILABLE for commercial use (i.e. when used on a third-party network and/or as part of a paid engagement)."** ✅ **Our classroom use is educational and remains free.** 🔴 **But our students are working analysts.** Anyone doing paid client work or third-party IR **cannot use KAPE for it as of 1 Jan 2026**, and we teach KAPE across S4 and S5. **This must be stated in the session, not discovered by a student on an engagement.** ⚠️ There is also **no stable direct download URL** — it is behind a form on Kroll's product page, which is why our earlier attempts 404'd. |
| 9 | ⚠️ **KAPE core is 1.3.0.2, released 22 Dec 2022 — the room's version is current** | **This closes a NOT VERIFIED item that failed three previous attempts.** (Route, for the record: `github.com/*/tree/*` and `/commits/*` are robots-disallowed and `api.github.com` 403s; the MDwiki renders client-side only. The way in is `raw.githubusercontent.com/EricZimmerman/KapeDocs/master/navigation.md`, which lists every page path verbatim — including `Pages/0.-Changelog.md`.) 🟢 **Important nuance: "KAPE is stale" is wrong.** The **core binary** has not moved since 2022; **KapeFiles (targets and modules) ships by commit and is updated continuously** — its releases page says *"There aren't any releases here."* |
| 10 | ✅ **SRUDB.dat is locked on a live host, and usually dirty when copied** | Confirmed. srum-dump's own README: *"If selecting `C:\Windows\System32\sru\srudb.dat` on a live system, administrative privileges are required."* **Expect a dirty database** — SrumECmd's README: *"This almost always means the database is dirty and must be repaired"*, fixed with `esentutl.exe /r sru /i` then `esentutl.exe /p SRUDB.dat`. 🟢 **Teach the repair step** — students will otherwise think the acquisition failed. ⚠️ **VSS preserves historical SRUM state** and is how you exceed the retention window. |
| 11 | ⚠️ **`pktmon` verb list corrections** | Current verbs: `filter · list · start · stop · **status** · **unload** · counters · reset · etl2txt · etl2pcap · **hex2pkt** · help`. **The room is missing `status`, `unload` and `hex2pkt`, and lists `comp`, which is a `start` parameter, not a verb.** `-c` and `--capture` are the same flag; both are current. |
| 12 | 🔴 **`pktmon` defaults: 512 MB confirmed, "768 MB memory" is not documented** | Microsoft: `--file-name` default `PktMon.etl` · `--file-size` default **512 MB** · `--log-mode` default **circular** · **`--pkt-size` default 128 bytes** (packets are truncated!) · `--flags` default `0x012`. **Memory mode's buffer is governed by `--file-size`, i.e. 512 MB — the 768 MB figure appears nowhere in current documentation.** ⚠️ Microsoft documents only the **file name**, not a directory — it lands in the **cwd**, which from an elevated prompt is `System32`. Elevation is required (confirmed by third-party sources; **Microsoft Learn does not state it**). |
| 13 | 🔴🔴 **`pktmon` cannot see loopback** | *"PktMon cannot … trace loopback traffic, since the Windows loopback implementation does not use NDIS."* **Local proxies, C2 relays and `127.0.0.1` pivots are invisible.** And **`etl2pcap` discards the drop reports and stack-component attribution** — *"all information about the packet drop reports and packet flow through the networking stack is lost in pcapng format output"* — which are the two things pktmon is uniquely good at. **802.11 captures convert incorrectly** and Wireshark mis-decodes them. |
| 14 | 🔴 **Windows Firewall logging is DISABLED by default** | *"No logging occurs until you set one of following two options"* — **Log dropped packets** and **Log successful connections**, both independently defaulting to **No**, **per profile**. Default path `%windir%\system32\logfiles\firewall\pfirewall.log`; **default max size 4,096 KB** (settable to 32,767 KB). ✅ The room's `#Fields:` line and the `path` = SEND/RECEIVE/FORWARD/UNKNOWN direction field are **current and correct**. |
| 15 | 🔴 **`qwinsta` shows no source IP** | Documented columns are **SESSIONNAME · USERNAME · ID · STATE · TYPE · DEVICE** — no address field. The room's claim is wrong. RDP source IP comes from **Event 1149** (`…TerminalServices-RemoteConnectionManager/Operational`, `Param3`), **4624 LogonType 10**, and **4778/4779**; session lifecycle from **`…TerminalServices-LocalSessionManager/Operational`** IDs 21–25. ⚠️ **1149 fires on channel establishment, not authentication** — *"this event does not indicate a successfully authenticated RDP session has taken place"* — so **1149 without a matching 4624 is the brute-force pattern.** |
| 16 | 🔴 **`netstat -n` is missing from the room and it matters** | Without `-n`, *"no attempt is made to determine names"* is what you forfeit — **the evidence host issues DNS and reverse lookups at collection time**, contaminating the DNS cache and SRUM's network tables, potentially tipping off the operator, and hanging on unreachable DNS. **Teach `netstat -anob`.** ⚠️ `-b` *"can be time-consuming and will fail unless you have sufficient permissions"* — which is what the room's own `Can not obtain ownership information` lines are. 🟢 **`Get-NetTCPConnection` never resolves names**, so the PowerShell path avoids this structurally. |
| 17 | ⚠️ two sections promise a command and give none | Task 3's **"Viewing Named-Pipes"** (*"This task will show you how to list network-based Named-pipes"*) and **"Querying WinRM Sessions"** both have explanatory prose and **no command**. For our material: named pipes are `Get-ChildItem \\.\pipe\` (or `pipelist.exe`), and WinRM sessions are `Get-WSManInstance -ResourceURI shell -Enumerate` / `Get-PSSession`. **Verify both on a live host before teaching them** — not verified this pass. |

## 4. Evidence used

- **Two live Windows VMs**, deployed across **two different rooms** — an "Analyst" host in this room
  and a "C2" host in a companion room (*Windows Network Analysis C2*) — connected in real time, with
  a status page on port 5000 on each confirming readiness. **The evidence is a running infection,
  not an image.**
- Screenshots and transcripts throughout come from **the author's own workstation** (`CMNatic`'s
  desktop, a `192.168.0.0/24` home network, real Outlook and Edge connections to Microsoft and
  Akamai ranges). ⚠️ **Not reusable and not something we would ship** — but a useful reminder that
  demo output is a real host's data.
- **Nothing downloadable. Nothing to flag for `ecdfp-evidence`** — no image, no corpus.

### 🟢 What is reusable is the *architecture*, not the evidence

**A live two-host lab where one machine attacks the other in real time** is a genuinely good design
and it is the only room in seventeen that does it. Students see connection state **change** between
two runs of the same command — the room even says *"If nothing sticks out, wait a few minutes and
run the command again."* **That sentence teaches something a disk image never can: live evidence
moves.**

We can reproduce it cheaply on our own infrastructure — `EVI-SRC01` plus a second small VM with a
scripted beacon — and it costs no evidence-production effort at all, because **the evidence is
generated by the lab rather than shipped with it**.

⚠️ **But it cannot be our primary S6 lab**, for two reasons: it requires two VMs per student
simultaneously, and **nothing is reproducible** — every student's `netstat` output differs, so
there is no single defensible answer key. **Use it as a demonstration, keep the assessment on a
fixed image.**

### 🔴 The handling gap this room leaves us to fill

Every artifact in §2 is collected **from a running suspect host**, and the room never once mentions:

- **order of volatility** (RFC 3227) — SRUM's Tier1 store and the DNS cache are **memory-resident**
  and die on reboot, while the firewall log and `pfirewall.log.old` do not. **Collection order is a
  decision with consequences and the room implies none exists.**
- **the examiner's footprint** — PowerShell history, prefetch, process creation, `pktmon`'s 512 MB
  ETL, `netstat.txt` on the suspect's disk, DNS-cache pollution from unresolved-name lookups, and
  the examiner's own RDP session appearing in `qwinsta`.
- **documenting what you touched** — which is exactly the audit-trail material room 15 supplied
  (`script`, `history -a`, save every command's output) and which **belongs in front of this room's
  content, not beside it.**

🟢 **Rooms 15 and 17 fit together as one `S2` narrative**: room 15 teaches you to log yourself
before you touch anything; room 17 gives you the things to touch. **Sequence them.**

## 5. Lab design worth reusing

1. **🟢🟢 The framing sentence.** *"Often in the initial stages of an incident, you may not be able
   to install all of your fancy tooling."* **That is the entire justification for `S6-05` and no
   other room states it.** Open with it.
2. **🟢🟢 SRUM.** A new first-rank artifact for us — the only host-side answer to *"how much data
   left, through what?"* — with a real parser, a KAPE target, and CSV output.
3. **🟢 Run it twice.** *"If nothing sticks out, wait a few minutes and run the command again."*
   Live evidence changes; a snapshot is a sample. **One sentence, real lesson.**
4. **🟢 The hosts-file explanation.** The best prose in the room, and it connects a trivial text
   file to banking trojans and credential harvesting in three sentences. **Keep it.**
5. **🟢 `(Get-NetTCPConnection).remoteaddress | Sort-Object -Unique`.** A clean, safe, exportable
   one-liner that produces exactly the artifact you want to hand to threat intel. 🟢 **And the room
   says why**: *"The `-Unique` filter … is important because IP addresses can make multiple
   connections (i.e. a browser)."*
6. **🟢 Command "cheatsheet" tables** for `pktmon` and `netstat` — the right format for a live-response
   room, and the right thing to give students as a one-page handout. **Ours will be correct** (§3).
7. **⚠️ Two-host live lab** — excellent as a demonstration, unusable as an assessment (§4).
8. **🔴 Do NOT reuse: the practical's framing of port 4444.** *"A popular port for reverse shells is
   currently active. What is the port number?"* trains port-number-implies-badness — the same
   reflex room 14 got wrong with port 22. **Our version asks what the connection proves, then asks
   what protocol it carried.** (Answer: not determinable from a connection table.)

### ✅ No safety defect — but the largest *handling* gap in seventeen rooms

Nothing here endangers the analyst, and nothing corrupts a stored image. But **the entire room
operates on live evidence with no acquisition discipline at all** (§4). It is a different category
from the six defects logged so far — those were single bad instructions; **this is a missing
chapter.**

**Defect tally unchanged at six** (rooms 6, 8, 9, 12, 13, 15 — table in `forensic-imaging.md` §5).
**Add this room to `S1` as the "what did the responder change?" case**, alongside room 13's FTK
Imager footprint.

## 6. Question patterns

**13 questions across 6 tasks.**

**⚠️ Eight are recall from the text** — *"What is the full name of the Windows feature that tracks
the last 30 to 60 days…"* · *"What is the full path to the directory that Windows will output
Firewall logs to?"* · *"What cmdlet can be used to display active TCP connections?"* · *"…the DNS
cache?"* · *"What command can be used to list all active RDP sessions?"* · *"What netstat flag…
executable?"* · *"…TCP connections and the associated process ID?"* · *"What special character can
we use to save the output of netstat to a text file?"* **A student can answer every one of these
without opening a VM.**

**🟢 The five practical questions are real work**, and they are well chosen because **each needs a
different tool**: a listening port (`Get-NetTCPConnection`) · the process behind the C2 connection
(the process/cmdline join) · the planted hosts-file domain (`gc hosts`) · **the exfiltration
process by byte volume (SRUM)** · the anomalous SMB share (`Get-SmbConnection`). **Five artifacts,
five tools, one incident.** That is the right shape and it is what `S6-05` should look like.

**🔴 Seventeenth room, still no question whose answer is "cannot be determined."** And this room's
artifacts make the candidates unusually good, because **every one of them has an "absent" state
that means nothing**:

| the room could have asked | correct answer |
|---|---|
| *"`pfirewall.log` is empty. Was there no blocked traffic?"* | **Cannot be determined** — logging is **off by default**, drops and allows are separately configurable, it is per-profile, and it rolls over at 4 MB. **Three reasons for an empty log, none of them "no traffic."** |
| *"SRUM shows this process sent 4 GB. Is that exfiltration?"* | **A lead.** Backup agents, updaters, cloud sync and video calls all look like this. And **if a VPN is in use the bytes are attributed to the VPN client**, not the real sender. |
| *"The DNS cache has no entry for `evil.com`. Was it never resolved?"* | **No** — TTL expiry, a reboot, `ipconfig /flushdns`, or a **stopped `Dnscache` service** all erase it. |
| *"`netstat -b` says 'Can not obtain ownership information'. Does that connection have no owner?"* | **No** — it means insufficient privilege, or a protected process. **The tool failed; it did not report a finding.** |
| *"`pktmon` captured nothing from the local proxy. Was there no traffic?"* | **No** — **pktmon cannot see loopback.** |
| *"`qwinsta` shows one RDP session. Is that the only one there has been?"* | **No** — it is a snapshot. History lives in **1149 / 4624 / 21–25**. |

**Six, all arising from the room's own commands, none asked.** 🟢 **This is the richest set of
"cannot be determined" candidates in the whole path**, because live-response tools fail *silently
and in a way that looks like a negative result* — which is precisely the distinction D20 criterion
4 grades. **`S6-05`'s assessment writes itself from this table.**

## 7. Figures we would need to draw

Figures present in the room: screenshots of terminal output and of the srum-dump GUI. **No
conceptual diagrams.**

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **SRUM's two tiers** | a clock strip: **Tier1 in memory, updated every 60 s** · **Tier2 = `SRUDB.dat`, written hourly and at shutdown** · the last partial hour drawn as a shaded gap labelled **"exists only in RAM — capture memory first"**, plus a footnote that since Win10 2004 the shutdown write is not guaranteed | **highest** |
| 2 | **six ways an artifact is absent** | one column per artifact — firewall log · DNS cache · SRUM · `netstat -b` · pktmon · qwinsta — each with its "absent" states listed beneath, over one caption: **"none of these means 'it did not happen'"** | **highest** — this is the `S6-05` assessment slide |
| 3 | **the responder's footprint on a live host** | the suspect host with the examiner's writes drawn landing on it: PowerShell history · prefetch · process creation · `PktMon.etl` 512 MB in System32 · `netstat.txt` · **DNS-cache pollution from name resolution** · the examiner's own `qwinsta` row; caption *"every command is an edit"* | **high** |
| 4 | **order of volatility for this artifact set** | the seven artifacts ranked by lifetime — SRUM Tier1 and DNS cache (minutes–hours, RAM) → live connections (seconds) → SRUM Tier2 (60 days) → firewall log (until rollover) → hosts file (until edited) → event logs — with a collection order arrowed through them | **high** |
| 5 | **where the RDP source IP actually is** | `qwinsta` output with a struck-through "source IP?" column, arrowed across to **1149 (`Param3`)**, **4624 LogonType 10**, **4778/4779** and **LocalSessionManager 21–25**, annotated *"1149 = channel established, not authenticated"* | **high** — corrects a room error and teaches the log set |
| 6 | **pktmon's blind spot** | the NDIS stack drawn as a layer cake with the capture hook marked, **loopback drawn as a bypass arrow that never crosses it**, and TLS above the hook; caption *"below the crypto, above nothing local"* | medium |
| 7 | **SRUM attribution under a VPN** | app → VPN client → NIC, with the SRUM byte counter attached to the **VPN client** and the real app greyed; caption *"SRUM tells you which process moved bytes, not which process wanted to"* | medium |

Figures 1 and 2 carry the session. Never their images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct

Mapped to **S6** / `S6-02` and `S6-05`. Correct. ➕ **Add `S2`** — the live-vs-dead and
order-of-volatility material (§4) is S2's, not S6's, and this room is where the need for it becomes
concrete.

### Rows this strengthens

- **`S6-02`** host network artifacts — 🟢 **SRUM is the addition.** Together with room 14's
  `windows.netscan` (memory) and the firewall log (disk), `S6-02` now has **three independent
  host-side sources of network evidence, with three different lifetimes and three different failure
  modes.** That contrast *is* the row.
- **`S6-05`** live triage — the PowerShell set, corrected for `Get-CimInstance`, is the row's
  content, and the six-artifact practical (§6) is its shape.
- **`S5`** — 🟢 **SRUM is also an execution artifact** (Application Resource Usage, App Timeline).
  It belongs beside Prefetch, Amcache and UserAssist in the S5 execution-evidence set, and unlike
  all three it carries **volume**. ⚠️ **Check whether `windows-user-activity.md` and
  `windows-applications-forensics.md` mention SRUM at all** — I do not believe they do.
- **`S1`** — the "what did the responder change?" case (§5), pairing with room 13's FTK Imager
  footprint. Two rooms, same lesson, different tools.
- **`S2`** — order of volatility; and the audit-trail material from room 15 sequenced **before**
  this room's commands.

### Four things `S6-05` must do differently from the room

1. **Use `Get-CimInstance`, not `Get-WmiObject`** — the room's headline one-liner does not run on
   PowerShell 7.
2. **`netstat -anob`** — and say why `-n` is not optional on a compromised host.
3. **Collect in volatility order, and log the collection** — DNS cache before anything that
   resolves names; memory before rebooting anything that holds SRUM Tier1.
4. **Teach every tool with its silent-failure mode** (§6). `Can not obtain ownership information`,
   an empty firewall log and a missing DNS entry are **tool states, not findings.**

### 🔴 One decision this room forces — KAPE licensing

**KAPE is no longer available for commercial use as of 1 January 2026.** Educational use — ours —
remains free. **But our students are practising analysts**, and we teach KAPE in S4 and S5.

Three options, and we must pick one:
- **(a)** keep teaching KAPE, and state the licence limit explicitly in the session;
- **(b)** teach KAPE for the concepts and **pair every KAPE step with a free alternative** for
  paid work (`SrumECmd` and the other EZ Tools run standalone; the targets are just file lists);
- **(c)** drop KAPE.

**Recommendation: (b).** KAPE's targets and modules are the best teaching artifact for
*"what do I collect and why"*, the EZ Tools underneath it are separately free, and (b) is the only
option that leaves students able to do the work on Monday. **This needs a `DECISIONS.md` row.**

### Minutes

`S6-02` and `S6-05` both already exist. SRUM is **new content inside `S6-02`**, and it displaces
material rather than adding to it — the firewall log and SRUM together are one artifact-comparison
slide, not two rows. The order-of-volatility content belongs in **`S2`**, where an acquisition row
already exists.

**No new rows. S6 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Twelfth room carrying the S5 overdraft.** ⚠️ **And SRUM's S5 claim will make it worse, not
better** — another reason the re-split cannot keep waiting.

### Out of scope

Packet analysis proper (Wireshark, PCAP) — correctly out; this is host-side. Sysmon and EDR
telemetry — not mentioned, and arguably should be in `S6-02` as the modern answer to the firewall
log's limits. **No scope conflict.**

### Still unresolved

**Browser forensics** — seventeenth room, still no `DECISIONS.md` row.

## 9. Links

- Room: <https://tryhackme.com/room/windowsnetworkanalysis> ·
  companion C2 room referenced in Task 5 (*Windows Network Analysis C2*) — **not extracted; it is a
  VM host with no teaching content.**
- Room's stated prerequisites: Windows Fundamentals · Investigating Windows · Introductory
  Networking · Hacking with PowerShell.
- **SRUM**: format spec (libyal esedb-kb)
  <https://github.com/libyal/esedb-kb/blob/main/documentation/System%20Resource%20Usage%20Monitor%20(SRUM).asciidoc>
  · table GUIDs and tiering (WithSecure chainsaw wiki)
  <https://github.com/WithSecureLabs/chainsaw/wiki/SRUM-Analysis>
  · <https://github.com/Psmths/windows-forensic-artifacts/blob/main/execution/srum-db.md>
- **SrumECmd** <https://github.com/EricZimmerman/Srum> · EZ Tools
  <https://ericzimmerman.github.io/> (current CLI version **2026.5.0**)
- **srum-dump v3** <https://github.com/MarkBaggett/srum-dump> · announcement
  <https://isc.sans.edu/diary/31896>
- **KAPE**: 🔴 **licensing FAQ**
  <https://raw.githubusercontent.com/EricZimmerman/KapeDocs/master/Pages/50-Frequently-asked-questions.md>
  · changelog (**1.3.0.2, 22 Dec 2022**)
  <https://raw.githubusercontent.com/EricZimmerman/KapeDocs/master/Pages/0.-Changelog.md>
  · download (form-gated)
  <https://www.kroll.com/en/services/cyber/incident-response-recovery/kroll-artifact-parser-and-extractor-kape>
  · `SRUM.tkape` and `SrumECmd.mkape` in <https://github.com/EricZimmerman/KapeFiles>
- **pktmon** <https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon>
  · `start` flags and defaults
  <https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-start>
  · `etl2pcap` losses
  <https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-etl2pcap>
  · loopback limitation <https://gary-nebbett.blogspot.com/2021/05/pktmon.html>
- **`Get-WmiObject` removal**
  <https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell>
  · `Get-CimInstance` <https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance>
  · PS7 module compatibility <https://learn.microsoft.com/en-us/powershell/windows/module-compatibility>
- **Firewall logging defaults**
  <https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-the-windows-firewall-log>
  · field reference
  <https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc758040(v=ws.10)>
- **RDP source IP**: Event 1149
  <https://psmths.gitbook.io/windows-forensics/artifacts-by-type/event-log-artifacts/terminalservices-remoteconnectionmanager/terminal-services-remote-1149>
  · <https://woshub.com/rdp-connection-logs-forensics-windows/>
- **netstat** <https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat>
- Tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` — **needs a block F for SRUM, KAPE
  licensing and pktmon; see §8.**
