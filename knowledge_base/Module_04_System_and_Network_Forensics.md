# Module 04 — System & Network Forensics

| | |
|---|---|
| **INE source** | unit 6 — *Windows Forensics* (429 pp) · unit 7 — *Network Forensics* (455 pp) |
| **Feeds sessions** | `S5` · `S6` |
| **Source text** | [`_source_text/INE_Unit_06_Windows_Forensics.md`](_source_text/INE_Unit_06_Windows_Forensics.md) · [`_source_text/INE_Unit_07_Network_Forensics.md`](_source_text/INE_Unit_07_Network_Forensics.md) |
| **Instructor delivery** | [`instructor/Session_04_Practical_Windows_Forensics.md`](instructor/Session_04_Practical_Windows_Forensics.md) · [`instructor/Session_05_Practical_Windows_Forensics_part_2.md`](instructor/Session_05_Practical_Windows_Forensics_part_2.md) · [`instructor/Session_06_Network_Forensics.md`](instructor/Session_06_Network_Forensics.md) |

> Condensed reference, our words, from INE's eCDFP courseware. Not published.
> Page cites `[U6 p128–148]` point into the source-text file, which is OCR — check any exact
> string on the source page before putting it in front of students.

## 0 · What this module is for

After this module a student can take a dead Windows image and answer, artifact by artifact, *what
ran, what was opened, what was plugged in, what was deleted and what was still there yesterday* —
and can take a packet capture, a flow record set and a pile of device logs and say what the network
half of the same incident looked like. It is the practical heart of the course: S1–S3 taught how to
acquire an image and read a file system, and this module is where those images finally get
interrogated for human activity. It is also where the course's central discipline is drilled hardest,
because Windows execution artifacts are the place students most reliably overclaim: half of §2A
exists to teach the difference between *this file was on the disk* and *this file ran*. S6 then repeats
the same discipline against the wire, where the limiting question is not "what did the packet say"
but "what could this capture point ever have seen".

Neither unit covers Linux, macOS or mobile forensics, so nothing was skipped on that ground.

## 1 · Core concepts

### Windows registry (as a file system, not a settings dialog)
- **Definition** — a set of hierarchical binary databases (hives) holding keys, subkeys and values, used by Windows to store system, application and per-user configuration.
- **Why it exists** — Windows needed one transactional, permission-controlled store for settings instead of thousands of scattered INI files; that centralisation is exactly what makes it a forensic goldmine.
- **Where it shows up** — as files on disk: `%SystemRoot%\System32\config\{SYSTEM, SOFTWARE, SAM, SECURITY, DEFAULT, BCD}` and, per user, `NTUSER.DAT` in the profile root plus `USRCLASS.DAT`. `HKLM\HARDWARE` and `HKLM\SYSTEM\Clone` are volatile and exist only in a running system's memory.
- **Example** — a hive file begins with the four-byte ASCII signature `regf` at offset `0x0`, followed by version numbers and the root cell offset; every key carries a last-write FILETIME, and no value ever does.
- **In the case (D19)** — the SYSTEM and NTUSER.DAT hives from EVI-SRC01 supply the timezone that every other timestamp in the incident timeline is normalised against.
`[U6 p159–195]`

### Key last-write time (the only registry timestamp)
- **Definition** — a FILETIME stored on each key/subkey recording when that key was last modified.
- **Why it exists** — the hive format tracks change at cell granularity for recovery purposes, not for us; value names, types and data carry no timestamp of their own.
- **Where it shows up** — in every registry parser's "last write" column, and as the *only* time source for keys such as `Run`, `USBSTOR` device subkeys and ShellBags.
- **Example** — if a subkey holds ten values and one is rewritten, the subkey's last-write time moves; you learn *something changed here then*, never *which value changed*.
- **In the case (D19)** — the `Run` key's last-write time brackets when persistence was installed, but it cannot single out the attacker's value from the legitimate ones already present.
`[U6 p183]`

### FILETIME, Unix 32-bit, and the UTC offset problem
- **Definition** — FILETIME is an 8-byte count of 100-nanosecond intervals since 1601-01-01 UTC; Windows also stores some values as 4-byte Unix epoch seconds.
- **Why it exists** — two eras of Microsoft API design; the examiner has to know which decoder to point at which value or the date lands centuries away.
- **Where it shows up** — FILETIME throughout NTFS and the registry; Unix 32-bit in `SOFTWARE\Microsoft\Windows NT\CurrentVersion\InstallDate` on Windows 10.
- **Example** — decoding an 8-byte little-endian FILETIME with a Unix decoder yields nonsense; INE demonstrates the choice explicitly with DCode's *Decode Format* dropdown.
- **In the case (D19)** — every artifact time in the S5 timeline is converted to UTC first and displayed in the host's local zone second, with both stated in the report.
`[U6 p180–185]`

### Presence vs execution (the module's spine)
- **Definition** — the distinction between an artifact proving a file *existed at a path with a given size and metadata* and one proving *the OS actually created a process from it*.
- **Why it exists** — Windows generates metadata about executables for compatibility, indexing and UI reasons long before anyone runs them; several artifacts students treat as execution evidence are really cataloguing evidence.
- **Where it shows up** — Prefetch and UserAssist sit on the execution side; ShimCache and Amcache sit on the presence side; the classic misread is treating a ShimCache row as a run.
- **Example** — ShimCache is populated on metadata or path change *regardless of whether the file executed*, so it can legitimately list a binary that never ran once [U6 p153].
- **In the case (D19)** — `lockit.exe` (the ransomware tooling that was staged but never fired) appears in ShimCache and Amcache and in no Prefetch file; that gap is the finding, not a collection failure.
`[U6 p149–158]`

### Evidence of absence
- **Definition** — using a counter or list that survives deletion to show that content once existed at a location now empty.
- **Why it exists** — Windows caches for the user's convenience persist after the user's data is gone; the cache outlives its subject.
- **Where it shows up** — UserAssist run counts, ShellBags for removed directories, Thumbs.db/thumbcache for deleted pictures, `$I` records for emptied bins.
- **Example** — INE's illustration: a `Documents` folder that is empty now but whose UserAssist entry shows 33 launches implies content that has since gone [U6 p278].
- **In the case (D19)** — the staging folder `…\AppData\Local\Temp\stage\` is gone from the live file system but still has a ShellBag entry with an MFT record number.
`[U6 p276–278, p312–329]`

### System artifacts vs user artifacts
- **Definition** — INE's top-level split: system artifacts record what the machine did in response to a stimulus; user artifacts record what a named human did or touched.
- **Why it exists** — attribution. A system artifact places an event on the host; a user artifact places it inside one profile's SID.
- **Where it shows up** — SYSTEM/SOFTWARE hives, Prefetch and setupapi logs on the system side; NTUSER.DAT, USRCLASS.DAT, LNK, jump lists and the per-SID Recycle Bin on the user side.
- **Example** — Prefetch tells you `updater.exe` ran on this host; only UserAssist, jump lists or LNK files tell you it ran under a particular profile.
- **In the case (D19)** — the report separates "on EVI-SRC01" claims from "under the compromised user profile" claims, and the second set always cites a user-hive artifact.
`[U6 p9–10]`

### MRU (most-recently-used) lists
- **Definition** — ordered lists Windows keeps of the last N items a user touched in some UI, usually with an `MRUListEx` ordering value.
- **Why it exists** — to prepopulate File→Open menus and jump lists; ordering matters more to Windows than timestamps, which is why most MRU entries have no individual time.
- **Where it shows up** — `ComDlg32\OpenSavePidlMRU`, `RunMRU`, `RecentDocs`, `Terminal Server Client\Default`, ShellBags `MRUListEx`.
- **Example** — in ShellBags the `MRUListEx` entries are 4 bytes each and shift right as new bags open, so the leftmost entry is the most recent [U6 p322–323].
- **In the case (D19)** — the RDP client MRU gives the ordered list of hosts the attacker connected to, but only the key's single last-write time.
`[U6 p289–305]`

### SID, RID and profile mapping
- **Definition** — every account gets a Security Identifier; its trailing Relative Identifier distinguishes accounts within a domain or machine, and RID 500 is always the built-in Administrator.
- **Why it exists** — Windows names things by SID internally and by display name only in the UI, so every per-user artifact directory is a SID that has to be resolved before it means anything.
- **Where it shows up** — `$Recycle.Bin\<SID>\`, `HKU\<SID>`, and the mapping table at `SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>\ProfileImagePath`.
- **Example** — SAM stores user subkeys under a hex RID (`\SAM\Domains\Account\Users\<hex>`); converting the hex to decimal gives the RID that ties back to the SID.
- **In the case (D19)** — the deleted staging archive is found under one SID's bin, and `ProfileImagePath` is what converts that SID into the named user in the report.
`[U6 p188–189, p262–269]`

### Volume Shadow Copy as a second timeline
- **Definition** — a block-level, point-in-time snapshot service that stores only the blocks changed since the snapshot, presented as a full mirror of the volume when mounted.
- **Why it exists** — to let backups and "Restore previous versions" run while applications keep writing; the side effect is that deleted or tampered files survive inside snapshots.
- **Where it shows up** — snapshots on the volume, enumerable with `vssadmin list shadows`; retention is capped (by default 5 % of the volume on Windows 7) and old snapshots are dropped as new ones are made.
- **Example** — a registry hive, log or file the attacker deleted on Tuesday can still be read out of Monday's snapshot, giving you two versions of the same artifact to diff.
- **In the case (D19)** — the pre-cleanup contents of the staging folder are recovered from a snapshot taken before the attacker deleted it.
`[U6 p42–66]`

### Network evidence tiers: packets, flow, logs
- **Definition** — three tiers with decreasing fidelity and increasing retention: full packet capture (content), flow records (who talked to whom, when, how much), device and service logs (interpreted events).
- **Why it exists** — nobody can store full packets for long. Flow keeps only header-derived summaries, which INE quantifies: about 30 MB of flow record for 8 GB of packets.
- **Where it shows up** — pcap from a tap or SPAN port; NetFlow/IPFIX/sFlow at routers; DHCP, DNS, proxy and web-server logs at services.
- **Example** — a beacon's *timing and volume* survive in flow after the pcap has rolled; a beacon's *payload* only ever exists in the pcap, and only if it was not encrypted.
- **In the case (D19)** — the C2 channel is first spotted as a flow pattern to `203.0.113.45:443` and only then confirmed against the short pcap window that still exists.
`[U7 p281–308, p309–316]`

### Capture point determines the evidence ceiling
- **Definition** — what a capture can contain is fixed by where the sensor sits and what the medium and switching fabric deliver to it.
- **Why it exists** — switches forward frames only to the destination port, so promiscuous mode alone sees nothing on a switched segment; hubs and wireless broadcast, so they see everything.
- **Where it shows up** — SPAN/port-mirror configuration, taps on copper and fibre, wireless monitor mode, and the sensor-placement trade-off (too high in the hierarchy overloads you, too low misses the traffic).
- **Example** — an investigator handed a capture from an access-layer port cannot claim "the host contacted no other server"; they can only claim what crossed that port.
- **In the case (D19)** — the S6 capture is taken at the egress gateway, so internal RDP lateral movement is *absent by design* and has to come from host artifacts instead.
`[U7 p98–104, p341–368]`

### Encapsulation and what encryption actually hides
- **Definition** — each layer wraps the layer above it (segment/datagram → packet → frame), so encryption at one layer leaves everything below it in clear.
- **Why it exists** — layered design; it also means the *layer* at which crypto is applied decides how much forensic value survives.
- **Where it shows up** — TLS encrypts the application payload, leaving TCP/IP/Ethernet headers readable; IPsec ESP encapsulates the whole packet, leaving only the data-link header.
- **Example** — from a TLS session you still get the five-tuple, the byte counts, the timing pattern, the SNI/certificate exchange at the start, and nothing of the HTTP inside.
- **In the case (D19)** — the C2 is HTTPS, so the case rests on flow timing, DNS resolution and the certificate exchange, not on request bodies.
`[U7 p86–92, p148–171, p350–351]`

### Flow record ecosystem (sensor → collector → aggregator → analyzer)
- **Definition** — the four roles in a statistical flow deployment: the device that emits records, the server that stores them, the node that unifies multiple collectors, and the tool that queries them.
- **Why it exists** — enterprises need one queryable history of network conversations without storing payloads; the same infrastructure is what an investigator inherits after the fact.
- **Where it shows up** — Cisco NetFlow (v5 is the common IPv4-only version; v9 is template-based; v10 is IPFIX), and sFlow as the sampling-based alternative.
- **Example** — flow answers "did this workstation ever talk to that host, how often, and how much did it send" for months back, which no pcap retention policy will.
- **In the case (D19)** — flow is what shows the exfiltration volume leaving the workstation *before* the USB copy, distinguishing staged-and-sent from staged-only.
`[U7 p293–308]`

### OSCAR (the network investigation method)
- **Definition** — Obtain information, Strategise, Collect evidence, Analyse, Report — INE's network-side variant of the general forensic method taught in Module 01.
- **Why it exists** — network evidence is distributed and volatile, so the collection order has to be planned rather than improvised; strategy is a named step precisely because you will not get a second chance at a CAM table.
- **Where it shows up** — in the S6 lab flow and in the report structure (executive summary plus technical narrative).
- **Example** — "Strategise" is where you decide that the router's routing table and the switch's CAM table are collected first because both live in RAM and vanish on reboot.
- **In the case (D19)** — the same numbered method governs both sessions so the disk and network narratives can be merged into one timeline.
`[U7 p330–340]`

## 2 · Artifacts  (R10 six-box, one table per artifact)

### 2A · Windows artifacts

#### Registry hive files
| | |
|---|---|
| **What it is** | The on-disk binary databases behind `HKLM` and `HKU`: system-wide hives plus one `NTUSER.DAT` and one `USRCLASS.DAT` per profile. |
| **Where it lives** | `%SystemRoot%\System32\config\` → `SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, `DEFAULT`, `BCD`. Per user: `<profile>\NTUSER.DAT` and `USRCLASS.DAT` (Vista+ under `AppData\Local\Microsoft\Windows`, ⚠ verify against source page — INE lists USRCLASS.DAT in the hive table [U6 p167] without giving its path). Each file starts with `regf` at offset `0x0`. `HKLM\HARDWARE` and `HKLM\SYSTEM\Clone` exist only in memory. |
| **What it proves** | That a given configuration state, account, device record or user preference was written into the hive, with a last-write time per key. |
| **What it does NOT prove** | It does not prove *who* made a change or *when a particular value* was written — only keys carry timestamps, values never do, so a key rewritten once shows one time for everything under it. A hive recovered from a dead image also does not reflect volatile keys (`HARDWARE`, `SYSTEM\Clone`, `LogonUI\SessionData`) that only exist while the machine runs, so their absence is normal and proves nothing about tampering. |
| **How to parse it** | Registry Explorer / RECmd (Eric Zimmerman) — the tool INE uses throughout; also RegRipper, python-registry, AccessData Registry Viewer, EnCase. Never load a subject hive into live `regedit`. |
| **Anti-forensics / false positive** | Hives can be edited offline; transaction logs (`.LOG1`/`.LOG2`) may hold pending writes that a naive parser ignores, so a "clean" hive can be stale. Deleted keys and unallocated cells still hold recoverable records that a raw `regedit` view will not show. |
`[U6 p159–195]`

#### ControlSet and the `Select` key
| | |
|---|---|
| **What it is** | Numbered copies of the system configuration branch; `Select` records which one the running system used. |
| **Where it lives** | `HKLM\SYSTEM\ControlSet001`, `ControlSet002`, …, and `HKLM\SYSTEM\Select` with values `Current` and `LastKnownGood` (both REG_DWORD). On a live system `CurrentControlSet` is the alias for the set named by `Current`. |
| **What it proves** | Which control set the system was actually booting from, so that every other SYSTEM-hive path (`Enum\USBSTOR`, `Control\TimeZoneInformation`, `Services`) is read out of the right branch. |
| **What it does NOT prove** | It does not prove that the other control sets are stale or irrelevant — a second set can hold an *earlier* configuration that is itself evidence, for example a service or firewall setting the attacker changed. Reading only `ControlSet001` because it is first alphabetically is a real and common error; the `Select\Current` value, not the ordering, decides. |
| **How to parse it** | Registry Explorer on the SYSTEM hive; read `Select\Current` first, then substitute that number wherever this module writes `ControlSet00#`. |
| **Anti-forensics / false positive** | Multiple control sets exist because settings changed or a boot failed, not because anyone hid anything; treating a second set as suspicious in itself is a false positive. |
`[U6 p197–201]`

#### TimeZoneInformation
| | |
|---|---|
| **What it is** | The host's timezone and daylight-saving configuration — the key that makes every other local timestamp interpretable. |
| **Where it lives** | `SYSTEM\ControlSet00#\Control\TimeZoneInformation`. Values: `Bias` (minutes offset from UTC), `ActiveTimeBias` (offset currently in force), `StandardBias`, `DaylightBias`, `StandardName` / `DaylightName` (pointers of the form `@tzres.dll,-NNN`), `TimeZoneKeyName`, `DynamicDaylightTimeDisabled` (0 = auto-adjust on, 1 = off). `StandardStart` / `DaylightStart` encode year/month/week/day/hour as a binary structure — year `00 00` means "every year". |
| **What it proves** | The offset that must be applied to convert local-time artifacts on this host to UTC, and whether the machine was auto-adjusting for DST. |
| **What it does NOT prove** | It does not prove the offset that applied *at the time of the incident* — this key holds the current setting with a single last-write time, so a timezone changed after the events silently mis-dates everything before it. It also says nothing about whether the clock itself was correct; a machine in the right timezone with a two-hour clock skew produces perfectly consistent, perfectly wrong times. |
| **How to parse it** | Registry Explorer (it decodes `tzres.dll` string IDs); cross-check the ID against a published `tzres.dll` string list. Record the offset on the front page of the timeline. |
| **Anti-forensics / false positive** | Changing the timezone or the clock is trivial and leaves only this key's last-write time behind. Compare against timestamps of known-UTC sources (event records, network logs, NTFS `$STANDARD_INFORMATION`) to detect skew. |
`[U6 p202–210]`

#### System identity and lifecycle keys (computer name, product, shutdown)
| | |
|---|---|
| **What it is** | The keys that name the host, describe the installed OS and record the last clean shutdown. |
| **Where it lives** | Name: `SYSTEM\ControlSet00#\Control\ComputerName\ComputerName` (Unicode). Product: `SOFTWARE\Microsoft\Windows NT\CurrentVersion` → `InstallDate` (Unix 32-bit), `ProductName`, `RegisteredOwner`, `RegisteredOrganization`, `SystemRoot`. Shutdown: `HKLM\SYSTEM\ControlSet001\Control\Windows\ShutdownTime` (FILETIME). |
| **What it proves** | That the image belongs to a host of a given NetBIOS name and OS build, installed at a given date, and last shut down cleanly at a given time. |
| **What it does NOT prove** | `ShutdownTime` does not prove the machine was off from then until seizure — it records the last *graceful* shutdown, so a crash, a hard power-off or a still-running machine leaves a stale value that a student will read as "the machine was untouched after this". `InstallDate` likewise dates the OS install, not the hardware, and is reset by an in-place upgrade or reimage. `RegisteredOwner` is free text typed at install and identifies nobody. |
| **How to parse it** | Registry Explorer; decode `InstallDate` as Unix 32-bit and `ShutdownTime` as FILETIME (DCode or the parser's built-in decoder). |
| **Anti-forensics / false positive** | All are plain writable values; a renamed machine keeps evidence of the old name in other artifacts (jump lists, network profiles, File History config `PCName`). |
`[U6 p211–213, p245]`

#### Network configuration and network history keys
| | |
|---|---|
| **What it is** | The per-interface TCP/IP configuration plus the list of every network the host has joined. |
| **Where it lives** | Interfaces: `SYSTEM\ControlSet00#\Services\Tcpip\Parameters\Interfaces\{GUID}\` → `DhcpIPAddress`, `DhcpServer`, `DhcpNameServer`, `DhcpDefaultGateway`, `DhcpSubnetMaskOpt`, `LeaseObtainedTime`, `LeaseTerminatesTime` (the last two REG_DWORD Unix times). History: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\` → `Nla\Cache`, `Signatures\Managed`, `Signatures\Unmanaged`, `Profiles\{GUID}`. Network type codes are given only partially by INE (`2` broadband `0x17`, `3` wireless `0x47`) — ⚠ verify against source page. |
| **What it proves** | Which IP addresses, DNS servers and gateways this host used, and which named networks (SSIDs, domains) it has attached to, with first/last-connected times in the profile keys. |
| **What it does NOT prove** | The DHCP values are the *current or last* lease only, so they do not prove which address the host held during the incident — that has to come from DHCP server logs or flow. Network profiles prove attachment to a network with a given name, not physical location: an SSID can be cloned anywhere, and a "Managed" signature only means the host was domain-joined at that moment. |
| **How to parse it** | Registry Explorer or RegRipper on SYSTEM and SOFTWARE; correlate profile GUIDs to firewall profile decisions. |
| **Anti-forensics / false positive** | A static reconfiguration overwrites the DHCP values; a VPN or virtual adapter creates additional interface GUIDs that look like extra networks. |
`[U6 p218–220, p238–244]`

#### Services key
| | |
|---|---|
| **What it is** | The registry definition of every Windows service and kernel driver, including its executable and start type. |
| **Where it lives** | `SYSTEM\ControlSet00#\Services\<ServiceName>\` (INE's slides render this as `\Service\` — ⚠ verify against source page; the live key is `Services`). Values of interest: `ImagePath`, `ServiceDll`, `DisplayName`, `ObjectName` (the account it runs as), `Type`, `DependOnService`, and `Start`: `0` = boot, `1` = system, `2` = automatic, `3` = manual, `4` = disabled. |
| **What it proves** | That a service by that name was configured to run a specific binary or DLL under a specific account, and the key's last-write time brackets when that definition was created or changed. |
| **What it does NOT prove** | A service definition is not a service execution — `Start = 2` proves intent to run at boot, not that the machine ever booted afterwards or that the binary launched successfully. Nor does a service running as `LocalSystem` prove privilege escalation happened here; most legitimate services do. And the last-write time covers the whole subkey, so an attacker who only altered `ImagePath` leaves the same evidence as one who created the service outright. |
| **How to parse it** | RegRipper's service plugins or Registry Explorer; sort by last-write time and by `ImagePath` outside `%SystemRoot%\System32`. |
| **Anti-forensics / false positive** | Service names are freely chosen and are routinely made to resemble real Windows services; `svchost.exe` in `ImagePath` with an unusual `-k` group or a `ServiceDll` pointing outside System32 is the pattern to teach. |
`[U6 p214–217]`

#### Autostart keys (Run/RunOnce, AppInit_DLLs and friends)
| | |
|---|---|
| **What it is** | The registry locations Windows consults to launch code automatically at boot or logon. |
| **Where it lives** | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` and `\RunOnce`; the same under `HKLM\SOFTWARE\Wow6432Node\...` for 32-bit on 64-bit; the same two under `HKCU`. Explorer hooks at `HKCU\Software\Classes\*\ShellEx\ContextMenuHandlers` (INE's OCR reads `SehllEx` — ⚠ verify). `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs`, gated by `LoadAppInit_DLLs` (should be `0x0`) and `RequireSignedAppInit_DLLs` (`0x1`; on by default from Server 2008 R2). Non-registry siblings: the Startup folder and scheduled tasks. |
| **What it proves** | That a command line or DLL path was registered for automatic loading, and roughly when (key last-write). `AppInit_DLLs` in particular proves a DLL was set to load into every user-mode process linked against `user32.dll`. |
| **What it does NOT prove** | Registration is not execution: a `Run` value proves the entry was written, not that the referenced file existed, was reachable or ever launched — and `AppInit_DLLs` may be globally disabled by `LoadAppInit_DLLs = 0` or blocked by the signing requirement, so its presence alone proves nothing loaded. There is also no authoritative Microsoft list of autostart locations, so an empty `Run` key does not prove the absence of persistence; it proves only that one of dozens of mechanisms was unused. |
| **How to parse it** | Offline: RegRipper / Registry Explorer across HKLM and every NTUSER.DAT. Live triage: Sysinternals **Autoruns**, which enumerates far more locations than the registry alone. |
| **Anti-forensics / false positive** | Legitimate software fills these keys; the discriminator is the target path and signature, not the presence of an entry. `RunOnce` values self-delete after firing, so the evidence of a one-shot payload may be gone. |
`[U6 p226–230, p246–249]`

#### Evidence-affecting configuration keys
| | |
|---|---|
| **What it is** | The keys that change whether *other* evidence is generated at all — the ones to read before concluding anything from an absence. |
| **Where it lives** | Last-access updates: `SYSTEM\ControlSet###\Control\FileSystem\NtfsDisableLastAccess` (`1` = not updated, `0` = updated). Prefetch: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters\EnablePrefetcher` (`0` off, `1` applications only, `2` boot only). Recycle Bin bypass: `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\Volume\{GUID}\NukeOnDelete` (`1` = bypass) and `MaxCapacity`. Firewall: `SYSTEM\ControlSet###\Services\SharedAccess\Parameters\FirewallPolicy\{Standard,Public,Domain}Profile\EnableFirewall` (`0` off, `1` on). UAC: `SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA` (`0` disabled, `1` enabled). RDP: `SYSTEM\ControlSet###\Control\Terminal Server\fDenyTSConnections` (`1` = RDP disabled). |
| **What it proves** | The host's evidence-generation posture: whether last-access times, prefetch files and Recycle Bin records could exist, and whether inbound RDP and the firewall were on. |
| **What it does NOT prove** | These are *current* settings with one last-write time each, so they do not prove the posture that applied during the incident — an attacker who disabled prefetching, then a defender who re-enabled it, leave a key that reads "enabled". Equally, `fDenyTSConnections = 0` proves RDP was permitted, never that anyone connected; and `EnableFirewall = 1` does not prove traffic was blocked, because rule subkeys and per-application exceptions decide that. |
| **How to parse it** | Registry Explorer / RegRipper; read these keys *first* in every Windows examination and record them alongside the timezone. |
| **Anti-forensics / false positive** | These are the classic anti-forensic switches. `EnablePrefetcher = 0` is also the *normal* state on Windows Server and on SSD-backed systems, so a zero is not by itself evidence of tampering. |
`[U6 p137–139, p223–225, p231–237, p251–254, p273–275]`

#### SAM accounts and ProfileList
| | |
|---|---|
| **What it is** | The local account database and the SID-to-profile-path mapping that turns SIDs into names. |
| **Where it lives** | `SAM\SAM\Domains\Account\Users\<hex RID>\` with per-user values including `UserPasswordHint` (Unicode) and `UserTile`; domain accounts appear under `SAM\Domains\Names` without an RID. The mapping lives in `SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>\ProfileImagePath`. RID 500 is the built-in Administrator on every Windows install since NT. `UserTile` holds a bitmap: 4-byte size at offset 12, bitmap data from offset 16 beginning `BM`. |
| **What it proves** | Which local accounts existed, their RIDs and group membership, created/last-login/last-password-change/expiry times as decoded by a registry viewer, and which profile directory belongs to which SID. |
| **What it does NOT prove** | A `LastLoginTime` in SAM is a *local* interactive-login record and does not prove a human sat at the keyboard — service logons, `runas`, and remote sessions all touch accounts, and domain logons are not recorded here at all. Account creation time proves when the account object appeared, not who created it. A populated password hint proves the hint text, not the password, and must never be reproduced verbatim in a report. |
| **How to parse it** | Registry Explorer decodes the SAM `F`/`V` structures directly (INE notes AccessData's viewer needs a full licence for the same job); RegRipper `samparse`. |
| **Anti-forensics / false positive** | Accounts can be created and deleted; a deleted account leaves an orphaned `ProfileList` entry and profile directory, which is itself a useful finding. |
`[U6 p187–189, p262–272]`

#### LogonUI last-logged-on user
| | |
|---|---|
| **What it is** | The value the logon screen uses to prefill the last user, plus a volatile per-session list of who is currently signed in. |
| **Where it lives** | `SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\` → `LastLoggedOnUser`, `LastLoggedOnSAMUser`, `LastLoggedOnUserSID`. Volatile: `...\LogonUI\SessionData\<#>\LastLoggedOnSamUser`, created only while a session is live and **deleted on shutdown or power loss**. |
| **What it proves** | Which account was most recently presented at the interactive logon UI on this host. |
| **What it does NOT prove** | It records the *last* interactive user only — it proves nothing about who was logged on during the incident, and it is overwritten by every subsequent logon, including one by a responder who touched the machine before imaging. Absence of `SessionData` subkeys is the normal state of any dead image and is not evidence that nobody was logged in. |
| **How to parse it** | Registry Explorer on SOFTWARE; treat `SessionData` as memory-only evidence that must be captured live if it matters. |
| **Anti-forensics / false positive** | Fast user switching creates one session subkey per switched-to session, so a count of subkeys on a live box is not a count of distinct users. |
`[U6 p255–261]`

#### USBSTOR
| | |
|---|---|
| **What it is** | The enumeration record Windows writes for every USB mass-storage device that has been attached. |
| **Where it lives** | `HKLM\SYSTEM\ControlSet00#\Enum\USBSTOR\Disk&Ven_<vendor>&Prod_<product>&Rev_<rev>\<serial>&0\`. Under the serial subkey, `ParentIdPrefix` links to `MountedDevices`, and a `Properties\{83da6326-…}` GUID subkey holds install/connect/remove FILETIMEs (INE truncates this GUID and does not give the property sub-IDs — ⚠ verify against source page). |
| **What it proves** | That a device with that vendor, product, revision and serial was enumerated by this host at least once, with the subkey last-write and the `Properties` timestamps bracketing installation and use. |
| **What it does NOT prove** | It does not prove that any file moved. USBSTOR records *attachment and driver installation*, not read or write activity, so a student who calls a USBSTOR entry "evidence of exfiltration" has proved only that a stick was plugged in. It also does not prove *which user* attached it — USBSTOR is a system-wide key, and only `MountPoints2` in a user hive puts a profile behind it. Nor does it prove the device is still in existence, or that the serial is genuine: if the device reports none, Windows generates one (a second character of `&` in the serial marks a generated value). |
| **How to parse it** | Registry Explorer or RegRipper `usbstor`; USBDeview and USBDeviceForensics roll USBSTOR, `MountedDevices` and the setupapi log into one view. |
| **Anti-forensics / false positive** | Serials can be spoofed in firmware; a USB device that is not mass storage (printer, phone in MTP mode) will not appear under USBSTOR at all — check `Windows Portable Devices` and `Enum\USB` too. Deleting the key removes the record but leaves `setupapi.dev.log` and `MountPoints2`. |
`[U6 p330–338, p349–353]`

#### MountedDevices (and Windows Portable Devices)
| | |
|---|---|
| **What it is** | The map from drive letters and volume GUIDs to the underlying device, i.e. what letter a given stick received. |
| **Where it lives** | `HKLM\SYSTEM\MountedDevices`, with values named `\DosDevices\D:`, `\DosDevices\E:`, … whose Unicode data contains strings such as `\??\USBSTOR#Disk&Ven_SanDisk&Prod_Ultra_USB_3.0&Rev_1.00#<serial>`. Drive letters and volume names also appear under `SOFTWARE\Microsoft\Windows Portable Devices\Devices`, and disk-class GUIDs under `SYSTEM\CurrentControlSet\Control\DeviceClasses\{53f56307-b6bf-11d0-94f2-…}`. |
| **What it proves** | Which drive letter a specific device (matched by the serial already found in USBSTOR) was mounted as, letting you connect a letter seen in LNK files, ShellBags or jump lists to a physical device. |
| **What it does NOT prove** | It shows the *most recent* binding of each letter, not a history — a letter reused by three different sticks retains only the last one, so an old LNK pointing at `E:\` cannot be tied to the device currently in `\DosDevices\E:` without independent corroboration. The key also has a single last-write time for the whole set, so it dates nothing individually. |
| **How to parse it** | Registry Explorer (read the value data as Unicode); RegRipper `mountdev`. Match on the serial substring, not on the letter. |
| **Anti-forensics / false positive** | Letters are also assigned to fixed disks, VHDs, network shares and virtual CD images, so a `\DosDevices\` entry is not by itself a removable device. |
`[U6 p339–342, p353]`

#### MountPoints2 (user-side device attachment)
| | |
|---|---|
| **What it is** | The per-user record of volumes mounted while that user was logged on. |
| **Where it lives** | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2\` — subkeys named by volume GUID (and by `##<host>#<share>` for network mappings). |
| **What it proves** | That the volume with that GUID was present during that user's session; the subkey last-write time is the closest thing to "this user had this device attached at this time". |
| **What it does NOT prove** | It does not prove the user copied, opened or even saw anything on the volume — mounting is automatic, and a device attached while the profile happened to be loaded is recorded whether or not the human noticed. It also has no run-count or history: one subkey, one last-write time, so repeated attachments over months collapse into the single most recent moment. |
| **How to parse it** | Registry Explorer or RegRipper `mp2` on each `NTUSER.DAT`; join the GUID to `MountedDevices` and thence to a USBSTOR serial. |
| **Anti-forensics / false positive** | Deleting the profile's `MountPoints2` subkeys is trivial and leaves the system-wide USBSTOR record intact — a mismatch between the two is itself worth reporting. |
`[U6 p351–352]`

#### setupapi.dev.log
| | |
|---|---|
| **What it is** | A plain-text log of device driver installation written the first time each device is attached. |
| **Where it lives** | Vista and later: `C:\Windows\INF\setupapi.dev.log` (siblings: `setupapi.offline.log`, `setupapi.setup.log`, `setupapi.upgrade.log`); Windows XP: `C:\Windows\setupapi.log`. Also `C:\Windows\setupact.log` and `setup.err.log` for installation-time actions and errors. |
| **What it proves** | The **first** installation of a specific device instance — the log line carries the full device instance ID (vendor, product, revision, serial) and a local timestamp for driver install. |
| **What it does NOT prove** | It records first installation only, so it does not prove the last time the device was used, how often, or by whom — a device attached daily for a year still appears once. Because the timestamps are written in *local* time, comparing them with UTC registry FILETIMEs without converting produces a false sequence of events. And it says nothing about data transfer. |
| **How to parse it** | It is plain text: `grep`/`findstr` for `USBSTOR` or for the serial found in the registry. No special tool needed, which is exactly why it is the best corroboration for a registry-only USB claim. |
| **Anti-forensics / false positive** | The file is user-writable by an administrator and can be truncated or edited; it also rolls over, so an old device may have aged out of the current file. |
`[U6 p343–347, p350]`

#### ShellBags
| | |
|---|---|
| **What it is** | Registry structures recording the view, icon, position and size settings of folders browsed in Windows Explorer — and therefore a record of the folders themselves. |
| **Where it lives** | `NTUSER.DAT`: `HKCU\Software\Microsoft\Windows\Shell\Bags`, `…\Shell\BagMRU`, `…\ShellNoRoam\Bags`, `…\ShellNoRoam\BagMRU`. `USRCLASS.DAT`: `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU` and `…\Shell\Bags`. Each bag holds binary shell-item data with ANSI/Unicode names, embedded dates, and MFT entry plus sequence numbers; `MRUListEx` orders siblings in 4-byte entries, most recent leftmost. |
| **What it proves** | That a folder — local, removable, UNC path, Control Panel item or the interior of a compressed archive — was opened in Explorer under that user profile, and that it existed at that path with that MFT record number. |
| **What it does NOT prove** | It proves *navigation*, not *content handling*: a bag for a folder does not prove any file inside it was opened, copied or exfiltrated, and students routinely make that leap. The embedded dates come from the shell item at the time the bag was written, so they date the folder, not the visit; and a bag surviving for a folder that no longer exists proves prior existence, not deletion by anyone in particular. Absence of a bag is also weak: folders reached by typing a path, by a command line, or by an application's own dialog may never create one. |
| **How to parse it** | **ShellBags Explorer** (GUI) or **SBECmd** (CLI) — both ingest `NTUSER.DAT` and `USRCLASS.DAT`, deduplicate across hives, and rebuild the tree. RegRipper `shellbags` as a cross-check. |
| **Anti-forensics / false positive** | Bags are created by any Explorer traversal including one by a responder on a live machine, so post-seizure browsing pollutes the artifact. Some entries are created by the shell for locations the user never opened (Control Panel categories, virtual folders). |
`[U6 p312–329]`

#### Prefetch (`.pf`)
| | |
|---|---|
| **What it is** | A cache manager trace of the files and DLLs an executable touched at startup, written to speed up later launches — and, incidentally, the cleanest evidence-of-execution artifact on Windows. |
| **Where it lives** | `%SystemRoot%\Prefetch\`, named `<EXENAME>-<8-hex-hash>.pf` where the hash derives from the path the binary launched from. Also present: `NTOSBOOT-B00DFAAD.pf` (boot trace, always this name) and `Layout.ini` (defragmenter data). Limit: 128 files on Vista/7, 1024 on Windows 8/8.1/10. The cache manager traces the first **10 seconds** of a normal application start, and the first **2 minutes** of boot for `NTOSBOOT`. |
| **What it proves** | That an executable of that name, launched from that path, ran on this system at least once — even if the binary itself has since been deleted. Internally: a **run counter**, the **last run time**, and the full paths (including volume) of every file loaded in that first 10-second window, which pins down where the executable resided on disk. File-system creation time of the `.pf` indicates the **first** run; last-modified indicates the **most recent** one. |
| **What it does NOT prove** | The run count and last-run time are the two most misread values in the course. The **run count is not a count of user launches** — a program restarted by a service, a scheduled task, a crash-restart loop or an installer increments it identically, and on modern Windows a single `.pf` records only a bounded set of recent run times, so a count of 92 does not mean 92 human decisions. The **last-run time is not the moment of the malicious act**: it is the *most recent* execution, so a binary that ran ten times shows only the tenth, and any legitimate later run (including one triggered by an analyst on a live host) overwrites the evidentiary one. The last-run timestamp inside the file also sits roughly **10 seconds earlier** than the file's last-modified time, because the trace is written after the fact — so quoting the `.pf` file's modified time as "the execution time" is off by that delay. Prefetch proves nothing about *who* ran the program (it is system-wide, not per user), nothing about the program's behaviour or success, and — critically — **absence of a `.pf` does not prove a program never ran**: prefetching is commonly disabled on Servers and SSD-backed systems, the directory rolls at 128/1024 entries, and `.pf` files are trivially deleted. Two different paths produce two separate `.pf` files for the same executable name, so one file never accounts for all executions of that name. |
| **How to parse it** | **PECmd** (Eric Zimmerman) — `PECmd.exe -d C:\Windows\Prefetch --csv <out>` for a directory, `-f <file.pf>` for one; it exposes every retained run time, not just the last. Also WinPrefetchView (NirSoft), TZWorks and Redwolf prefetch parsers. Always read `EnablePrefetcher` before interpreting an empty directory. |
| **Anti-forensics / false positive** | Deleting `.pf` files is the simplest anti-forensic act there is and leaves the directory looking merely tidy. A `.pf` whose loaded-file list points into `C:\Users\<user>\` or `…\AppData\Local\Temp\` is far more suspicious than the same executable name from `System32` — INE's own example contrasts `C:\Users\<user>\svchost.exe` with `C:\Windows\System32\svchost.exe`. Conversely, a legitimate program that happens to load an attacker DLL appears entirely normal at the name level. |
`[U6 p128–148]`

#### ShimCache / Application Compatibility Cache
| | |
|---|---|
| **What it is** | A kernel-maintained cache the Application Compatibility Infrastructure uses to decide quickly whether a binary needs a compatibility shim. It is a *lookup index of executables Windows has considered*, not an execution log. |
| **Where it lives** | Windows XP: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatibility\AppCompatCache`. Vista and later: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache\AppCompatCache` (INE's OCR renders "Session Manager" without the space in places — ⚠ verify against source page). Held in kernel memory and **serialised to the registry only at shutdown or restart**. Capacity: 1,024 entries on Windows 7 / Server 2008, 512 on earlier versions. |
| **What it proves** | That the OS *catalogued* an executable at a given full path, recording the file's `$STANDARD_INFORMATION` last-modified date and (on some versions) its size — and the entry's position in the cache gives a relative recency ordering. It survives deletion of the binary and covers far more files than Prefetch, which is why it is the standard fallback on Servers where prefetching is off. |
| **What it does NOT prove** | **This is the classic misread and the single most important box in this knowledge base: a ShimCache entry does not prove the program ran.** Windows adds an executable to the cache when its file metadata or path changes and when the shell merely enumerates it — INE states this outright: entries can exist for "executable files that never actually ran on a system". A student who reports "ShimCache shows the ransomware executed" has, in the general case, reported nothing more than "a file with that name existed at that path and Windows looked at it". Four further limits: (1) the timestamp in a ShimCache row is the **file's** last-modified time, **not** an execution time — it can predate the intrusion by years and is fully attacker-controllable by timestomping; (2) the ordering is relative recency of *insertion*, so it lets you say "this was catalogued after that", never "this happened at 14:07"; (3) it is written to the registry only at shutdown, so on a machine that has not cleanly restarted since the incident the on-disk copy is stale and the real cache is in RAM; (4) the per-entry execution flag that some Windows versions expose is version-dependent and is **not** available or trustworthy on all builds — INE's slide listing "whether the file actually ran on the system" among the decoded fields overstates this badly, and treating that flag as authoritative on modern Windows is exactly the error the course is trying to prevent. Finally, absence proves nothing: the cache holds at most 512–1,024 entries and rolls. |
| **How to parse it** | **AppCompatCacheParser** (Eric Zimmerman) against the extracted SYSTEM hive, or RegRipper `appcompatcache`. For a live or memory-only system, the Volatility **ShimCacheMem** plugin (Fred House, Claudiu Teodorescu, Andrew Davis — 2015 Volatility plugin contest winner) reads the cache out of kernel memory and defeats the shutdown-only limitation. |
| **Anti-forensics / false positive** | Timestomping the binary changes the value ShimCache stores, because it copies the file's own metadata. Renaming or moving the binary produces a *new* entry, so one attacker tool can occupy several rows under different paths. Entries for files in `\Temp`, `\ProgramData` and user profile paths are the triage signal; entries for System32 binaries are noise. Always pair with Prefetch, Amcache, UserAssist or event data before saying "ran". |
`[U6 p149–158]`

#### Amcache.hve (and RecentFileCache.bcf)
| | |
|---|---|
| **What it is** | A separate registry hive recording programs and binaries the compatibility infrastructure has seen, with richer per-file metadata than ShimCache. |
| **Where it lives** | `%SystemRoot%\AppCompat\Programs\Amcache.hve`. On Windows 7 the predecessor file is `RecentFileCache.bcf` in the same directory; installing update KB2952664 replaces it with `Amcache.hve`. From Windows 8 onward `Amcache.hve` is standard. |
| **What it proves** | That a binary with a given full path, size and — importantly — **SHA-1 hash** was present and catalogued on the system, together with entries for installed applications. The hash is what makes Amcache uniquely valuable: it lets you tie a deleted file to a known sample without the file. |
| **What it does NOT prove** | Amcache sits on the **presence** side of the presence/execution line, exactly like ShimCache: an entry means the binary was seen and inventoried, not that a process was created from it. The timestamps it carries describe the *file* (compilation, last-modified, first-seen-by-the-cataloguer) rather than an execution moment, so quoting an Amcache time as "when the malware ran" is unsupported. Because the cataloguing is opportunistic, the absence of an entry does not mean a program was never on the disk, and the presence of one for a file in a user's Downloads folder proves download or copy, not intent to run. INE's coverage is thin here — it introduces Amcache only as ShimCache's successor and does not describe its key structure or the hash field, so anything beyond "presence plus hash" must be verified outside the course material. |
| **How to parse it** | **AmcacheParser** (Eric Zimmerman) — `AmcacheParser.exe -f C:\Windows\AppCompat\Programs\Amcache.hve --csv <out>`; also loadable directly in Registry Explorer as a hive. |
| **Anti-forensics / false positive** | The hive is a file and can be deleted; it is also large and noisy — thousands of legitimate entries mean the artifact is only useful when driven by an IOC (a hash, a path, a time window). Its per-entry timestamps are file-derived and therefore timestompable. |
`[U6 p155]`

#### UserAssist
| | |
|---|---|
| **What it is** | Per-user counters Windows keeps of programs and shortcuts launched through the Explorer shell, used to tailor the Start menu. |
| **Where it lives** | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count\`. Value names are **ROT13-encoded**; the value data holds a run counter, a last-executed FILETIME and a focus-time figure. Distinct GUIDs separate executables from shortcuts; some entries use folder GUIDs in place of program names (`ProgramFilesX64` `6D809377-…`, `Desktop` `B4BFCC3A-…`, `Documents` `FDD39AD0-…`, `Downloads` `374DE290-…`, `UserProfiles` `0762D272-…`). |
| **What it proves** | That a specific user account launched a program *through the shell* — double-click, Start menu, desktop shortcut — how many times, when it was last launched, and how long it held focus. Because it is per user, it is the artifact that attaches execution to a profile. |
| **What it does NOT prove** | UserAssist only sees **GUI, shell-initiated** launches, so it does not prove a program never ran: anything started from a command line, a script, a service, a scheduled task or another process is invisible here, and that covers most attacker tooling. It equally does not prove the user understood or intended what they launched — a shortcut that silently chains to a payload is recorded as one clean user launch. The run counter is per profile, not per host, and entries persist after the program is uninstalled, so a non-zero count is evidence of past activity, not present installation. |
| **How to parse it** | RegRipper `userassist` or Registry Explorer (both ROT13-decode automatically); the standalone UserAssist utility used in INE's browser section does the same job. |
| **Anti-forensics / false positive** | Trivially deleted from the user hive. Counters also reflect responder activity if a live profile was used after the incident. The ROT13 encoding is obfuscation for tidiness, not security, and confuses students the first time they see a raw key. |
`[U6 p276–284]`

#### LNK (shortcut) files
| | |
|---|---|
| **What it is** | A Windows shell data object pointing at another object, created automatically whenever a file is opened as well as manually by users and installers. |
| **Where it lives** | Auto-created ones in `%USERPROFILE%\Recent` (modern: `…\AppData\Roaming\Microsoft\Windows\Recent`) and `%USERPROFILE%\Application Data\Microsoft\Office\Recent`. Anywhere else on the disk for user-made shortcuts. The format has a fixed signature, so LNKs can be carved from unallocated space. |
| **What it proves** | A rich metadata set about the **target at the time of access**: target path, target size when last accessed, target's own MAC timestamps captured into the LNK, the **volume serial number and label** of the volume the target lived on, network share name, the host's MAC address (not always present), file attributes, and distributed-link-tracking data. The LNK's own file-system timestamps add a second layer: creation time indicates the **first** time the target was opened, last-modified indicates the **most recent** time. When the two sets match, INE's reading is that the target was opened exactly once from that location. |
| **What it does NOT prove** | An LNK proves *access*, not *authorship, possession or viewing*: it is created by opening a file, and an automated preview, a thumbnail generation or an application's own recent-files handling can produce one without a human reading anything. It does not prove the target file still exists, nor that it exists on this machine — a volume serial pointing at removable media proves the file was on *some* volume with that serial, which is only a device identification once you have that device or its registry record. There is a documented exception where the metadata is simply absent: a file created and first saved from inside an Office application (INE cites Office 2003 and 2007) produces a `Recent`-folder LNK with **no embedded target dates**, so drawing conclusions from missing dates is unsafe. Finally, INE's slide claiming "the absolute path to the file is **not** stored in the lnk file" contradicts its own LECmd output two slides later, which prints both a local path and an absolute path — see §7. |
| **How to parse it** | **LECmd** (Eric Zimmerman): `LECmd.exe -f "<path>\file.lnk"`, or across a directory `LECmd.exe -d "<dir>" --csv <out> --html <out> --xml <out> -q`. Also ExifTool, TZWorks' LNK parser, or a hex editor if you know the structure. |
| **Anti-forensics / false positive** | An LNK can be weaponised — INE closes the section warning that a shortcut can be configured to run malicious code, which is exactly the initial-access vector students should expect. LNKs are also easy to delete individually, and deleting one silently removes the matching `RecentDocs` value. |
`[U6 p11–26]`

#### Jump Lists
| | |
|---|---|
| **What it is** | The per-application recent/pinned item lists behind the Windows 7+ taskbar right-click menu, stored as compound files containing embedded LNK-format entries. |
| **Where it lives** | `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\<AppID>.automaticDestinations-ms` (OS-created) and `…\Recent\CustomDestinations\<AppID>.customDestinations-ms` (created when a user pins an item — INE's path for this one omits `\Roaming`, ⚠ verify against source page). `AppID` is a 16-hex-digit application identifier set by the app or the OS at runtime. Related: pinned taskbar items in `…\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar`, and the registry values `Favorites`/`FavoritesResolve` under `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband`. The displayed item count defaults to 10 and can be raised to 60. |
| **What it proves** | Which files a **specific application** opened for a **specific user** who logged on interactively, with per-entry LNK-grade metadata. Two high-value cases: the Explorer jump list recovers recently accessed directories, and the **Remote Desktop jump list gives a list of recent RDP connections**, which is prime evidence when reconstructing lateral movement from a compromised host. |
| **What it does NOT prove** | Jump lists are an interactive-logon artifact, so their absence does not mean an application was unused — remote, service and non-interactive execution produce none. An entry proves the application registered a document as recent, not that the user read, edited or exfiltrated it. Pinned entries in `customDestinations-ms` reflect a *deliberate* pin that may be months old and say nothing about recent use. The `AppID` identifies the application build, not the binary on this disk, so mapping an unknown AppID from a published table is an inference, not a match. Counts are capped and roll, so old activity silently disappears. |
| **How to parse it** | **JLECmd** (Eric Zimmerman) across the `AutomaticDestinations`/`CustomDestinations` directories; it resolves known AppIDs and expands the embedded LNK structures. |
| **Anti-forensics / false positive** | Deleting the `.automaticDestinations-ms` file removes the whole application's history at once, which is far quieter than deleting individual LNKs. INE also gives conflicting hives for the `Start_JumpListItems` setting (HKLM on one slide, HKCU on another) — see §7. |
`[U6 p67–89]`

#### RecentDocs
| | |
|---|---|
| **What it is** | A per-user registry list of recently opened files of any extension, used to populate application File menus. |
| **Where it lives** | `HKEY_USERS\{SID}\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs`, with per-extension subkeys and an `MRUListEx` ordering value. |
| **What it proves** | That files with those names were opened under that profile, in a known order, and that the corresponding LNK files existed in the user's `Recent` folder — the two artifacts mirror each other. |
| **What it does NOT prove** | Filenames only: `RecentDocs` records a name, not a path or a volume, so it cannot show where a file lived or whether two identically named files are the same file. It has no per-entry timestamps — only the key's last-write, which dates the most recent addition and nothing else. And it is tightly coupled to the `Recent` folder: **deleting an LNK automatically deletes the matching `RecentDocs` value**, so a sparse list is as consistent with tidy-up as with light use. |
| **How to parse it** | RegRipper `recentdocs` or Registry Explorer; always parse the `Recent` folder LNKs alongside it, because each supplies what the other lacks. |
| **Anti-forensics / false positive** | Because it mirrors the LNK folder, a user or tool that clears "recent items" wipes both at once, leaving matching gaps that look like inactivity. |
`[U6 p295–296]`

#### Explorer Open/Save and Run MRUs (ComDlg32, RunMRU)
| | |
|---|---|
| **What it is** | Registry MRU lists tracking the common file-dialog and Start→Run interfaces. |
| **Where it lives** | `HKEY_USERS\{SID}\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\` → `OpenSavePidlMRU` (files chosen in Open/Save As dialogs, value name `0` = most recent), `LastVisitedPidlMRU` (which **application** last used the dialog and in which directory), `CIDSizeMRU` (dialog size/position per application, Vista+). Start→Run history at `…\Explorer\RunMRU`. |
| **What it proves** | Which files a user selected through a file dialog, which applications opened those dialogs and in which folder, and which commands were typed into the Run box. `LastVisitedPidlMRU` is the artifact that names the *application* — INE's worked example reads the most recently used application straight out of it. |
| **What it does NOT prove** | Selecting a file in an Open dialog is not the same as opening it successfully, and saving through a Save As dialog does not prove the write completed. `RunMRU` proves a string was typed and accepted, not that the command executed or succeeded — a typo'd command sits in the list identically to a working one. Neither key timestamps individual entries; only the ordinal position and the key's single last-write survive, so "third in the list" is an ordering claim, never a time claim. |
| **How to parse it** | RegRipper (`comdlg32`, `runmru`) or Registry Explorer, which decodes the PIDL structures into readable paths. |
| **Anti-forensics / false positive** | Applications that use their own file dialogs bypass `ComDlg32` entirely, so an empty list is weak evidence. Entries persist after the referenced files are deleted. |
`[U6 p291–294, p301–305]`

#### Terminal Server Client MRU (RDP client history)
| | |
|---|---|
| **What it is** | The Remote Desktop Connection client's history of hosts this user connected *out* to. |
| **Where it lives** | `HKEY_USERS\{SID}\Software\Microsoft\Terminal Server Client\Default\` with values `MRU0`, `MRU1`, … (`MRU0` = most recent), and `…\Terminal Server Client\Servers\<address>\` holding a subkey per tracked address with per-connection configuration such as the username hint. |
| **What it proves** | That an RDP session was **successfully established** from this host to each listed address or hostname under that user profile — INE is explicit that Windows adds an entry only on a successful connection. That makes it a primary artifact for reconstructing attempted and achieved lateral movement outward from a compromised machine. |
| **What it does NOT prove** | It is outbound only, so it proves nothing about who connected *to* this machine — students routinely cite it as evidence of an inbound intrusion, which it can never be. It is per user and per host, capped and ordered, with no per-entry timestamps: `MRU0` proves "most recent of those recorded", not "at 03:12 on Tuesday". Nor does it prove what was done inside the session, or that the account named in the `Servers` subkey is the account that authenticated. |
| **How to parse it** | RegRipper `tsclient` / Registry Explorer on each `NTUSER.DAT`; corroborate with the Remote Desktop jump list, with `bitmapcache` files, and with authentication records on the *destination* host. |
| **Anti-forensics / false positive** | Cleared by any user with a few clicks. Failed connection attempts leave nothing, so an absent entry does not disprove an attempt. |
`[U6 p297–300]`

#### Recycle Bin ($I / $R, and legacy INFO2)
| | |
|---|---|
| **What it is** | The per-user staging area for deleted files, with separate metadata and content records. |
| **Where it lives** | Vista and later: `<volume>\$Recycle.Bin\<SID>\` containing matched pairs — `$I<6-character ID>.<ext>` (metadata: original full path and name, original size, deletion date/time in UTC) and `$R<6-character ID>.<ext>` (the renamed content; the **R** holds the **raw** file). Windows XP / Server 2003: `<volume>\Recycler\<SID>\` with files renamed `D<DriveLetter><Index#>.<ext>` — INE's slide text garbles which character is fixed (⚠ verify against source page) — and a hidden `INFO2` index recording physical size, UTC deletion time, and original name and path. Both directories are hidden, per-volume, and NTFS-permissioned so users cannot see each other's deletions. |
| **What it proves** | That a specific file was deleted via Explorer from a specific original path by a specific SID at a specific UTC time, and — where the `$R`/`DC` file survives — recovers the content in full. Deleted **directories** behave differently: their contents keep their original names and, under the legacy scheme, are not tracked in `INFO2`. |
| **What it does NOT prove** | An empty or missing Recycle Bin does not prove nothing was deleted: `Shift+Delete` bypasses it entirely, the bin can be emptied, `NukeOnDelete` can disable it per volume, and Windows does **not** enable it at all for devices classified as removable storage — so an exfiltration USB will simply have no bin. The deletion timestamp records the move into the bin, not when the file was created, last used, or finally purged. And the presence of a file in the bin proves an Explorer-mediated delete, not intent to destroy evidence — routine tidying looks identical. |
| **How to parse it** | **rifiuti2** (parses both `INFO2` and `$I` records), `recbin.exe` (Harlan Carvey) — `recbin -f <INFO2 or $I file>`, with `-c` for CSV and `-t` for TLN timeline output — plus Autopsy, EnCase and FTK, or the `RecycleDump.py` script. |
| **Anti-forensics / false positive** | The **root** of `$Recycle.Bin` should contain no files at all, which makes it an attractive hiding place that few users ever inspect; INE (citing Harlan Carvey) adds that any persistence mechanism pointing at an executable or DLL inside the Recycle Bin should be treated as suspicious. A `$R` file can be replaced while its `$I` metadata stays plausible. |
`[U6 p102–127]`

#### Volume Shadow Copies
| | |
|---|---|
| **What it is** | Block-level, point-in-time snapshots of a volume created by the Volume Shadow Copy Service, exposed to users as "Restore previous versions". |
| **Where it lives** | In the `System Volume Information` structures on each protected volume; enumerable by ID and creation time. Introduced in Server 2003 (limited in XP for NT Backup), comprehensive from Vista/7. Default space cap on Windows 7 is 5 % of the volume; when the cap or count is reached, the oldest snapshots are deleted. |
| **What it proves** | The state of files, registry hives and logs at each snapshot time — recovering material an attacker deleted or altered afterwards, and giving a second copy of key artifacts to diff against the live one. Snapshots are created on service-pack installs, Windows updates, driver installs, daily scheduled tasks, and on manual request by users or applications. |
| **What it does NOT prove** | A snapshot proves what the volume looked like **at that instant**, and nothing about the interval between snapshots — a file created and deleted between two snapshots leaves no trace here at all, so "not in any VSC" is not evidence of absence. Because VSS is block-level, a mounted snapshot *looks* like a complete volume even though only changed blocks are stored; students read that as "a full backup existed", which it never was. Snapshot creation times date the snapshot, not any file inside it. And the absence of snapshots proves only that VSS was off, capped out, or cleared — a very common attacker action that is itself a finding. |
| **How to parse it** | `vssadmin list shadows /for=C:` to enumerate, then mount (Microsoft's `vssadmin` + `mklink`); NirSoft **ShadowCopyView**; **libvshadow** for offline images; ShadowExplorer; VSC Toolset. For an image, mount the snapshot read-only and run the same registry/prefetch parsers against it. |
| **Anti-forensics / false positive** | Deleting shadow copies is a standard pre-ransomware step, so an empty list is a signal, not a dead end. INE warns explicitly that snapshots on a **live** system may still contain live malware — mount them in an isolated environment. |
`[U6 p42–57]`

#### File History (Windows 8+)
| | |
|---|---|
| **What it is** | The file-level, user-scoped backup mechanism introduced in Windows 8, running alongside (not replacing) VSS. |
| **Where it lives** | Configuration XML: `%USERPROFILE%\AppData\Local\Microsoft\Windows\FileHistory\Configuration\`. Local staging cache: `…\FileHistory\Data`. Backups themselves live on the configured target (removable media or a network share). By default it saves hourly, caps the offline cache at 5 % of disk, and keeps versions forever. |
| **What it proves** | From the configuration file alone: which directories the user selected for backup, the user ID, the **PC name**, the retention policy, the backup frequency, and where the backups are stored — volume path, drive type and drive letter. From the data: previous versions of user files, and the NTFS USN journal is what drives change detection. |
| **What it does NOT prove** | Coverage is narrow and fixed: it backs up Libraries, Desktop, Contacts and Favorites only, so the absence of a file in File History says nothing — most of the disk was never eligible. Nor does the configuration prove backups actually ran or completed; it records intent and target, and a target that was absent (`TargetAbsenceTime`) simply queues data in the local cache. It is not a system-state backup, so it cannot recover registry hives the way a shadow copy can. |
| **How to parse it** | Read the configuration XML directly; the target catalogues are ESE databases (`Catalog1.edb`, `Catalog2.edb`) on the backup target. Treat the target volume as a separate piece of evidence to acquire. |
| **Anti-forensics / false positive** | Because the target is usually external, the most valuable half of this artifact is frequently not in the seized image at all — the configuration file is then a *pointer to evidence you do not yet have*, which is exactly its investigative use. |
`[U6 p57–66]`

#### Thumbcache and Thumbs.db
| | |
|---|---|
| **What it is** | Cached thumbnail images Explorer generates for picture and document views. |
| **Where it lives** | Before Vista: a hidden `Thumbs.db` in **each** directory containing the images. Vista and later: consolidated per user at `%USERPROFILE%\AppData\Local\Microsoft\Windows\Explorer\` as `thumbcache_<size>.db` — one database per view size (`thumbcache_32.db`, `thumbcache_256.db`, …). |
| **What it proves** | That an image or document with that visual content was present in a viewed folder — recoverable even after the original file, or the entire folder, has been deleted. Legacy `Thumbs.db` additionally carries the source file name and last-modification date. |
| **What it does NOT prove** | The modern thumbcache does **not store the original file path**, so a recovered thumbnail proves an image existed on the system, not where it lived or which user's folder it came from; the mapping has to be rebuilt separately. It does not prove a human looked at the image — thumbnails are generated by the shell as soon as a folder is viewed in a thumbnail layout, so a folder browsed once populates the cache for everything in it. Nor does it prove current possession, which is precisely why it is powerful *and* why the inference must be stated carefully. |
| **How to parse it** | Thumbcache Viewer (`thumbcacheviewer.github.io`) for `thumbcache_*.db`, Thumbs Viewer (`thumbsviewer.github.io`) for `Thumbs.db`. To recover paths: run the viewer on the live system so it maps entries, or map offline against the Windows Search ESE database `Windows.edb` in `C:\ProgramData\Microsoft\Search\Data\Applications\Windows` — INE gives the command as `esentutil.exe /p Windows.edb` (⚠ verify against source page: the Microsoft binary is `esentutl.exe`, and `/p` is the repair switch). Offline mapping requires an OS of the same or newer version than the one that generated the database. |
| **Anti-forensics / false positive** | Users delete `Thumbs.db` believing it is junk; the consolidated cache is harder to notice and survives folder deletion, which is the whole forensic point. Thumbnails can persist for images that were only ever previewed from removable media. |
`[U6 p27–41]`

#### Windows Search history (search charm)
| | |
|---|---|
| **What it is** | The per-user MRU of terms typed into the Windows 8/8.1 search charm, including the "Search Everywhere" option that spans local files and the internet. |
| **Where it lives** | An MRU list in `NTUSER.DAT` under a `SearchHistory` key; entries are also written to disk as individual LNK files. (INE cites `WordWheelQuery` under `…\CurrentVersion\Explorer\` only in its reference list — ⚠ verify against source page before teaching that path.) |
| **What it proves** | That a specific keyword was searched by that user on that machine, and — from the key's last-modified timestamp — **the first time** that keyword was searched. |
| **What it does NOT prove** | The timestamp is the *first* search only and, INE states explicitly, **does not update on repeat searches** — so a student reading it as "when the user last searched for this" has the meaning exactly backwards. It also does not prove the search returned results, that the user opened anything found, or that the term relates to content on this machine (Search Everywhere reaches the internet). Selecting the "Settings" or "Apps" category does not add the term to the MRU at all, so absence is not evidence the user never searched. |
| **How to parse it** | Registry Explorer / RegRipper on `NTUSER.DAT`, plus the associated LNK files via LECmd. |
| **Anti-forensics / false positive** | Clearing search history removes the MRU; the version-specificity is severe — this is a Windows 8/8.1-era artifact and its layout differs on Windows 10/11 (see §7). |
`[U6 p96–101]`

#### Libraries (`.library-ms`)
| | |
|---|---|
| **What it is** | XML definitions of the folder sets Windows presents as Documents, Music, Pictures, Videos — plus any custom library the user creates. |
| **Where it lives** | `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Libraries\`, one `.library-ms` XML file per library. |
| **What it proves** | Which physical directories — including network and removable locations — a user aggregated under each library name, and, by extension, which locations that user treated as a working set. |
| **What it does NOT prove** | A library is a view, not a container: an entry proves a folder was *included*, not that any file in it was opened, copied or even still exists. Because users can create custom libraries, checking only the four default ones is a real collection gap — INE flags this directly — so an examination limited to the defaults proves nothing about the user's actual working set. The XML has no per-entry timestamps. |
| **How to parse it** | Any XML/text viewer, or a forensic suite that renders `.library-ms` natively; read them as pointers to *other* locations that must then be acquired. |
| **Anti-forensics / false positive** | Libraries look like ordinary folders in Explorer, so responders sometimes acquire the library rather than its targets and believe they have collected the data. |
`[U6 p90–95]`

#### Internet Explorer history and typed URLs
| | |
|---|---|
| **What it is** | IE's split artifact set: registry-resident typed URLs, autocomplete and preferences, plus file-system-resident cache, cookies, bookmarks and history database. |
| **Where it lives** | Registry: `HKCU\Software\Microsoft\Internet Explorer\TypedURLs` (`url1` = most recent) with matching `TypedURLsTime` FILETIMEs; autocomplete form data in `IntelliForms\Storage1` / `Storage2`; browser preferences under `…\Internet Explorer\Main`. Files: cache in `%USERPROFILE%\AppData\Local\Microsoft\Windows\Temporary Internet Files\`; bookmarks (`Favorites`) as plain-text `.url` files in `%USERPROFILE%\Favorites`; cookies in `…\AppData\Roaming\Microsoft\Windows\Cookies` (and `\Low`). History: `index.dat` for IE ≤ 9 (multiple files, per function and per time range); from IE 10 an ESE database — `WebCacheV01.dat` / `V16` / `V24` — in `…\AppData\Local\Microsoft\Windows\WebCache`. |
| **What it proves** | Requested URLs with last-accessed, file-modified and expiry times; which URLs were **typed** rather than followed (a deliberate-navigation signal); cached copies of retrieved content; and cookies proving contact with a domain. |
| **What it does NOT prove** | A history record proves a request was issued by the browser process, not that a human chose to visit — advertisements, redirects, prefetching, iframes and malware in the browser all generate identical entries, so "the user visited this site" is an inference that needs corroboration. `TypedURLs` is a partial exception but includes autocomplete-completed entries. Cache content proves data was retrieved, not read. Absence proves little: history can be cleared while cookies survive, which INE turns into a technique — a cookie for a domain with no matching history entry still shows the site was reached. |
| **How to parse it** | `pasco.exe` for `index.dat`; NirSoft's ESE Database View / IE cache, history and cookie viewers; Web Historian; libmsiecf and libesedb. A dirty ESE database must be repaired with `esentutl` before some tools will read it, and the file is usually locked during live acquisition. |
| **Anti-forensics / false positive** | InPrivate browsing suppresses most of this. Cross-check the browser actually used — INE warns against assuming the corporate standard browser is the one that ran, and recommends confirming from Prefetch and UserAssist first. |
`[U6 p360–392]` · `[U7 p376–406]`

#### Chrome and Firefox data stores
| | |
|---|---|
| **What it is** | SQLite-backed history, cookie, cache and credential stores for the two dominant non-Microsoft browsers. |
| **Where it lives** | Chrome: `\Users\<user>\AppData\Local\Google\Chrome\User Data\Default`. Firefox: `\Users\<user>\AppData\Roaming\Mozilla\Firefox\Profiles\<random>.default` — note INE gives `AppData\Local\Mozilla\…` on one slide and `AppData\Roaming\Mozilla\…` on another (⚠ verify; Roaming holds the profile, Local holds cache). Firefox's `places.sqlite` holds `moz_places`, `moz_historyvisits`, `moz_bookmarks`, `moz_keywords`, `moz_inputhistory`, `moz_hosts`; cookies live in `cookies.sqlite`. INE's paths are stated for Windows 7 and change on later releases. |
| **What it proves** | Visited URLs with visit counts and timestamps, bookmarks, typed-input history, downloads, and cookies establishing contact with a domain. Stored credentials can be recovered where the browser retained them. |
| **What it does NOT prove** | The same request-vs-intent limit as IE applies, with an added trap: a `visit_count` is a count of navigations by the browser, not by the human, and background tabs, restored sessions and redirects inflate it. Deleted history rows frequently remain in SQLite free pages, so a clean `moz_places` table does not prove clean browsing; conversely, recovering a row from free space does not tell you when it was deleted. Some stores are encrypted (SQLCipher) or OS-protected, so failure to read them is not evidence of absence. |
| **How to parse it** | DB Browser for SQLite for direct table work; NirSoft BrowsingHistoryView and Mandiant RedLine to view IE, Firefox, Chrome and Safari history in one pane; WebBrowserPassView for stored credentials. Always work on a copy — opening a live SQLite file writes to it. |
| **Anti-forensics / false positive** | Multiple profiles and multiple installed browsers are the norm; INE's guidance is to determine which browsers ran (Prefetch, UserAssist) before deciding which stores matter, and to cross-check findings between at least two locations. |
`[U7 p376–414]`

#### Skype local data store
| | |
|---|---|
| **What it is** | The desktop Skype client's local SQLite databases and support files — taught in the unit primarily as a worked method for approaching an *unfamiliar* application, not for Skype's own sake. |
| **Where it lives** | Vista and later: `C:\Users\<user>\AppData\Roaming\Skype\<skype-id>\`. XP: `C:\Documents and Settings\<user>\Application Data\Skype\<skype-id>\`. Inside: SQLite databases holding text messages, call logs (metadata and duration, never audio) and transfer records; a `chatsync` directory of `.dat` conversation files; `shared.xml` at the Skype root and `config.xml` in the ID directory. |
| **What it proves** | That an account with that Skype ID was configured on this machine, and — from the databases — that specific messages, calls and file transfers occurred between named accounts at recorded times. |
| **What it does NOT prove** | It records the **account**, never the person: possession of a machine with a signed-in ID does not prove who typed. Call rows prove a call was placed and its duration, not what was said, because no audio is stored. What appears in the directory depends entirely on what the user did with the account, so an absent `chatsync` folder means no chats were synced to this device — not that none occurred. And the whole artifact is version-bound: modern Skype builds do not necessarily keep this layout (see §7). |
| **How to parse it** | Free: Skyperious (searches the machine for profiles, browses and exports, runs raw SQL), SkypeLogView, Skype Log Viewer, SkypeFreak, Skype Xtractor. `.dat` files under `chatsync` yield readable content to `strings` or `bstrings.exe`. Commercial: SkypeAlyzer, Skype Extractor, Paraben E3:Internet Chat. |
| **Anti-forensics / false positive** | The transferable lesson is INE's method for an undocumented application: image a clean system, install and exercise the application, image again, and diff — then hunt for its storage format (here, SQLite files under `AppData`). Apply that, not the Skype paths, when the application is unknown or malicious. |
`[U6 p393–417]`

### 2B · Network evidence

#### Full packet capture (pcap)
| | |
|---|---|
| **What it is** | A byte-for-byte record of frames observed at one capture point, with per-frame timestamps. |
| **Where it lives** | On disk as a capture file written by tcpdump, dumpcap or a sensor appliance; in Wireshark's case buffered in **RAM** until the user saves, which is why INE warns Wireshark is unsuitable for long captures and tcpdump is the tool for sustained collection to disk. |
| **What it proves** | Everything that crossed that interface within the capture window: the five-tuple, timing to microseconds, byte counts, protocol headers at every layer, and — where unencrypted — full application payload including credentials, commands and transferred files. |
| **What it does NOT prove** | A pcap is bounded by *where* and *when* it was taken, and both bounds are routinely forgotten. It cannot prove a host "did not communicate" with anything — it proves only that nothing crossed this interface during this window, and a switched network delivers almost nothing to an un-mirrored port. It does not prove a packet's claimed source: source IPs and MACs are forgeable, so an IP in a capture identifies an address, not a machine and certainly not a person. It does not prove content when TLS or IPsec is in use, and it does not prove that a session completed — a capture that starts mid-stream shows no handshake, which is a capture artifact rather than an anomaly. |
| **How to parse it** | Wireshark for interactive dissection and Follow Stream; **tshark** where there is no GUI; capture with `tcpdump -i <iface> -w <file.pcap> <bpf-expression>`. Apply a Berkeley Packet Filter at capture time to control volume. |
| **Anti-forensics / false positive** | Encryption, tunnelling and non-standard ports defeat naive protocol assumptions — INE notes explicitly that a well-known application may be configured on a non-standard port, so "port 8080 therefore not HTTP" is unsound reasoning in both directions. Capture files can also be edited; hash them on collection. |
`[U7 p107–110, p272–283, p341–351, p369–374]`

#### Flow records (NetFlow / IPFIX / sFlow)
| | |
|---|---|
| **What it is** | Header-derived summaries of network conversations, emitted by routers and switches and stored centrally. |
| **Where it lives** | Emitted by a **sensor** (typically a gateway router), stored on a **collector**, unified across collectors by an **aggregator**, queried by an **analyzer**. Formats: Cisco NetFlow (v5 is the common IPv4-only version; v9 is template-based; v10 is IPFIX) and sFlow. Roughly 30 MB of flow records for 8 GB of packets. |
| **What it proves** | Who talked to whom, on which ports, when, for how long and with how much data — over a retention window far longer than any pcap. That makes it the evidence of choice for identifying infected hosts by pattern, confirming or excluding data exfiltration by volume, and profiling a user's habitual destinations. |
| **What it does NOT prove** | Flow has **no payload**, so it can never prove what was said, which file moved, or that a transfer was malicious — a 4 GB upload to a cloud host looks identical whether it is a backup or an exfiltration. It also cannot prove absence of communication, because it only sees flows crossing the sensor: INE's sensor-placement problem cuts both ways, and a sensor low in the hierarchy misses evidence while one at the root drowns in it. Some deployments (notably sFlow) **sample**, so an absent flow may simply not have been sampled, and flow timestamps carry the sensor's clock, not the endpoints'. |
| **How to parse it** | The collector's own analyzer; export to CSV and pivot on source, destination, port, byte count and time. Correlate the flow window with the pcap window and with host artifacts. |
| **Anti-forensics / false positive** | NAT and proxying collapse many hosts into one flow source; long-lived sessions are split across records; and an attacker who keeps volumes low and destinations popular is invisible to volume-based analysis. |
`[U7 p293–308, p363]`

#### DNS traffic and DNS server logs
| | |
|---|---|
| **What it is** | The name-resolution record: query and response packets on the wire, plus the resolver's own logs. |
| **Where it lives** | UDP and TCP port 53 in capture (Wireshark display filter `dns`); server-side in DNS query logs. Header fields to read: transaction **ID** (maps query to response), **QR** (query/response), **opcode**, **TC** (truncated), **RD** (recursion desired), **RA** (recursion available), **RCODE**, and the question/answer/authority/additional counts. Record types: `A`, `AAAA`, `CNAME`, `PTR`, `TXT`, `NS`, `MX`. Names are capped at 253 characters. |
| **What it proves** | That a host asked to resolve a specific name at a specific time and what answer it received — INE's point being that **any** device connecting to a remote machine by name must issue a DNS request, so resolver logs are a near-complete index of intended destinations. |
| **What it does NOT prove** | A query proves a lookup, not a connection: resolution frequently happens for names nothing ever connects to (prefetching, link previews, security products, typos), so "resolved therefore visited" is unsupported. It does not prove intent or user awareness — most resolutions are made by software. It does not identify the requesting *user*, only the resolver client address, and a caching resolver hides the original asker entirely. Conversely, absence of a query does not prove no connection: cached entries, hard-coded IPs, hosts-file entries and non-standard resolvers all bypass the logged path. INE flags that record types (notably `TXT`) can be used to smuggle data out of a protected network, but the unit does not describe how to detect that (see §7). |
| **How to parse it** | Wireshark `dns` filter and packet detail; on the server, the resolver's query log. Correlate a suspicious name's first-ever resolution time against host artifacts. |
| **Anti-forensics / false positive** | Encrypted DNS (DoH/DoT) removes port-53 visibility entirely; fast-flux and domain generation produce large numbers of short-lived names; a rogue DNS server on the segment can return forged answers, so an answer in a capture is what the client was *told*, not the truth. |
`[U7 p191–211, p367, p426–428]`

#### DHCP traffic and lease data
| | |
|---|---|
| **What it is** | The address-assignment exchange (DORA: Discover, Offer, Request, Ack) and the server-side lease database. |
| **Where it lives** | UDP ports 67 (server) and 68 (client); Wireshark labels it *Bootstrap Protocol* and the capture filter is `bootp`. Key fields: transaction ID, client MAC, `ciaddr`/`yiaddr`, and options — `(53)` message type, `(61)` client identifier, `(50)` requested address, `(12)` host name, `(60)` vendor class, `(55)` parameter request list, `(54)` server identifier, `(51)` lease time, `(1)` subnet mask, `(3)` router, `(6)` DNS, `(15)` domain name. |
| **What it proves** | Which **MAC address** held which IP address over which lease period, plus the client's self-reported host name and vendor class — the join that turns an IP address seen in a flow or log into a specific network interface. |
| **What it does NOT prove** | An IP-to-MAC mapping is not an IP-to-person mapping, and it is not even a stable IP-to-machine mapping: leases expire and are reissued, so the same address belongs to different hosts at different times and every claim must carry a time window. The host name and vendor class in options `(12)` and `(60)` are **client-supplied strings** and are freely spoofable, as is the MAC itself. And a rogue DHCP server on the segment can hand out configuration that never appears in the legitimate server's logs. |
| **How to parse it** | Wireshark with the `bootp` filter, reading the options block; on the server, the lease file or DHCP log. Always record the lease start and end alongside the address. |
| **Anti-forensics / false positive** | MAC randomisation on modern clients breaks the join outright. DHCP starvation (many Discovers from non-existent MACs) and rogue DHCP servers are the two attacks that poison this evidence — DHCP snooping on the switch is the control that prevents the second. |
`[U7 p212–238, p365–366, p419–425]`

#### HTTP request and response
| | |
|---|---|
| **What it is** | The plaintext application-layer exchange behind unencrypted web traffic — self-describing, so no decoder is required. |
| **Where it lives** | TCP port 80 by default, but any port an administrator chose; also visible through a web proxy (Burp Suite) placed between browser and server. Request fields of forensic value: method (`GET` puts parameters in the URL, `POST` puts them in the body), `Host`, `User-Agent`, `Cookie`, `Referer`. Response: status line plus headers; status classes 1xx informational, 2xx success (200), 3xx redirect (302), 4xx client error (403, 404), 5xx server error. |
| **What it proves** | The exact resource requested, the parameters supplied, the client software as it identified itself, session identity via cookies, the referring page, and the server's answer including any content returned. |
| **What it does NOT prove** | `User-Agent` and `Referer` are client-controlled strings and prove only what the client *claimed*, so building attribution on a browser version string is unsound. A `200` proves the server returned a resource, not that a human viewed it. `GET` parameters in a URL are as exposed as `POST` parameters — INE's point is that the two are equally insecure, so the presence of credentials in a body rather than a URL proves nothing about protection. And a cookie identifies a session, not a person; a stolen cookie replayed by an attacker is indistinguishable at this layer from the legitimate user. |
| **How to parse it** | Wireshark `http` filter plus **Follow HTTP Stream**; tshark for bulk extraction; a proxy for live interception. Server-side, the equivalent evidence is in access logs and proxy logs. |
| **Anti-forensics / false positive** | HTTPS removes all of it. Non-standard ports break port-based filters, so filter on protocol dissection rather than port where possible. |
`[U7 p114–139, p117–119, p379]`

#### TLS handshake and certificate
| | |
|---|---|
| **What it is** | The negotiation that precedes an encrypted session — and, for the investigator, the last clear-text window into it. |
| **Where it lives** | At the start of every TLS session, before the record layer takes over. Phases: handshake (client nonce → server nonce plus certificate → client-generated pre-master key encrypted to the server's public key → both sides derive a master key and from it four sub-keys) and record layer (two keys per direction for authenticated encryption, plus per-packet sequence numbers to defeat replay). Certificates carry the server public key plus metadata about the key and its owner, validated against a CA public key embedded in the client. |
| **What it proves** | That an encrypted session was established between two endpoints at a given time, with a specific certificate presented — subject, issuer, validity dates and key details — plus the session's timing and volume. Certificate anomalies (self-signed, mismatched subject, absurd validity, unknown issuer) are visible without any decryption. |
| **What it does NOT prove** | It proves nothing about the content, and students overreach in the other direction too: a **valid certificate does not prove the endpoint is legitimate** — certificates are cheap and an attacker's C2 server can present a perfectly valid one. Conversely a self-signed certificate is common in legitimate internal services, so it is a lead, not a finding. TLS also does not hide the five-tuple, packet sizes or timing, so "it was encrypted, therefore nothing can be determined" is equally wrong. Whether an intercepted certificate is the *server's own* cannot be determined from the capture alone — that is precisely the substitution attack the CA hierarchy exists to prevent. INE explicitly defers decryption techniques to a later course. |
| **How to parse it** | Wireshark's TLS dissector — read the `Client Hello`/`Server Hello` and the certificate chain; export the certificate for inspection. INE's own lab frames this as "analysing encrypted traffic based on certificate information only". |
| **Anti-forensics / false positive** | Certificate details can be made to mimic a well-known service. Note also a factual error in the source at `[U7 p144]` — it describes the receiver decrypting with its *public* key; the private key is what decrypts (see §7). |
`[U7 p141–171, p453]`

#### SMTP session and email headers
| | |
|---|---|
| **What it is** | The mail-submission conversation on the wire, and the header block that survives inside the delivered message. |
| **Where it lives** | On the wire as a text exchange — server banner, `EHLO`/`HELO`, `AUTH LOGIN` (username and password each **Base64-encoded, not encrypted**), `MAIL FROM`, `RCPT TO`, `DATA`, and per-command numeric responses (`250`, `235`, `354`, `221`). In the message: `Return-Path`, a stack of `Received:` lines, `Message-ID`, `X-Mailer`, `Date`, `From`, `To`, `Subject`, `Content-Type`, and authentication results (SPF, DKIM) added by the receiving side. |
| **What it proves** | The submission path: which client software (`X-Mailer`, `User-Agent`) sent the message, from which host, authenticating as which mailbox, to which recipients, at which times — and the `Received:` chain records each relay hop, read from the bottom upward. Base64 in an unencrypted capture yields the submitting credentials outright. |
| **What it does NOT prove** | `From`, `To` and `Subject` are trivially forged — INE demonstrates a public fake-mailer doing exactly that — so a message's apparent sender proves nothing on its own. `Received:` headers can also be fabricated by the sender; only the hops added by servers *you* trust (typically the last ones, nearest the recipient) carry weight, and the earliest lines are the most suspect. A `Message-ID` is locally significant to the generating server and is not a global proof of anything. SPF/DKIM `PASS` proves the sending domain authorised that server, not that the human named in `From` wrote the message. |
| **How to parse it** | Wireshark **Follow TCP Stream** on the SMTP conversation; Base64-decode `AUTH` exchanges. For a delivered message, use the client's "show original" view and read the `Received:` chain bottom-up, checking each hop's plausibility. |
| **Anti-forensics / false positive** | An open or misconfigured server allows manual message injection and `VRFY`-based user enumeration. Modern submission is normally on TLS, which removes the on-the-wire half entirely and leaves only the header analysis. |
`[U7 p172–190, p317–329]`

#### ARP traffic and ARP cache
| | |
|---|---|
| **What it is** | The IP-to-MAC resolution exchange on a local segment, and the client-side cache of its results. |
| **Where it lives** | Broadcast request, unicast reply, on the local broadcast domain only; cached per host and readable with `arp -a`. |
| **What it proves** | Which MAC address claimed a given IP address on the segment at a given time — the mapping every frame on the LAN depends on. |
| **What it does NOT prove** | ARP has **no authentication**, so a reply proves only what some device asserted, never who actually holds the address; a cache entry is therefore a claim, not a fact. The cache is volatile and short-lived, so its contents describe the last few minutes, not the incident. And two MACs claiming one IP is the *signature* of poisoning rather than proof of it — a duplicate can also arise from a misconfigured device or a failover pair. |
| **How to parse it** | Wireshark `arp` filter, watching for one IP mapping to changing MACs or for unsolicited replies; `arp -a` on a live host, captured before anything else because it will not survive. |
| **Anti-forensics / false positive** | ARP poisoning is the classic man-in-the-middle on a switched LAN and lets the attacker intercept, analyse and sometimes modify traffic. Related switch-layer attacks — MAC flooding to overflow the CAM table and force the switch to broadcast, and port stealing — leave similar signatures. |
`[U7 p253–269, p446–452]`

#### ICMP traffic
| | |
|---|---|
| **What it is** | The control and error messaging protocol carried inside IP packets, split into error messages and query messages. |
| **Where it lives** | Encapsulated in the IP data field; Wireshark filter `icmp`. Type 8 is echo request, type 0 is echo reply; other query types cover timestamp, address-mask and router solicitation/advertisement, while error types cover destination unreachable, time exceeded and parameter problem. Each echo packet carries a sequence number and a **data section filled with padding by default**. |
| **What it proves** | Reachability testing and path discovery (ping, traceroute), and — from error messages — that a port or host was unreachable, which is how a closed UDP port announces itself (ICMP destination port unreachable). Request and reply are correlated by sequence number, and Wireshark computes the response time. |
| **What it does NOT prove** | A successful ping proves a host responded to ICMP, not that any service on it was running, and a failed ping proves only that ICMP was blocked or unanswered — firewalls drop it routinely, so "no reply therefore host down" is unsupported. More importantly, an ICMP packet being "just a ping" is an assumption, not a finding: INE's point is that many exfiltration tools ride ICMP, and because the data section is expected to contain filler, **payload in an echo packet does not look anomalous to a casual reviewer**. Examining that padding is the step students skip. |
| **How to parse it** | Wireshark `icmp` filter; open the Data section of echo packets and inspect the bytes rather than trusting that they are the default pattern. Compare payload length and content against the OS's normal ping. |
| **Anti-forensics / false positive** | Oversized, variable or high-entropy ICMP payloads and asymmetric request/reply volumes are the tells; conversely, legitimate monitoring systems generate large steady ICMP volumes that resemble a covert channel in flow data alone. |
`[U7 p78–79, p239–252]`

#### Switch evidence (CAM table, SPAN/mirror, VLAN and port security)
| | |
|---|---|
| **What it is** | The layer-2 forwarding state and configuration of the switch a host is attached to. |
| **Where it lives** | The **CAM** (content addressable memory) table maps each learned MAC address to a physical port; alongside it sit VLAN assignments and port-security tables. Capture capability comes from a **SPAN port** (a hardware copy of every frame crossing the switch) or **port mirroring** (an OS feature copying specified source ports to a destination port). All of it lives in the device's RAM and running configuration. |
| **What it proves** | Which MAC address was seen on which physical port — the join that **physically locates a device** in a building — plus which segments were bridged and what capture coverage was actually configured. |
| **What it does NOT prove** | The CAM table is a live cache, not a history: it shows what the switch has learned recently and proves nothing about last week, and entries age out. It is also stored in RAM, so a crash, a power failure, or the table simply filling up destroys it — INE notes some switches clear the table on memory exhaustion, which is exactly what a MAC-flooding attack forces. A MAC-to-port mapping identifies an interface, not a machine or a user, and MACs are spoofable. Finally, an existing SPAN configuration does not prove the captures you were given came from it. |
| **How to parse it** | Read from the device CLI during live response, before anything is rebooted; treat it as the most volatile network evidence in the room and collect it first. |
| **Anti-forensics / false positive** | MAC flooding turns the switch into a hub and simultaneously destroys the table's evidentiary value. Unmanaged switches have no SPAN, no mirroring and no readable table at all. |
`[U7 p101–103, p355–361, p364]`

#### Router evidence (routing table, ACLs, configuration)
| | |
|---|---|
| **What it is** | The layer-3 forwarding state, access control configuration and export settings of the gateway. |
| **Where it lives** | Routing table (static entries plus those learned dynamically via routing protocols), access control lists, and the export configuration that sends flow records to a collector. Routing tables live in RAM. |
| **What it proves** | The path a packet would have taken between networks, which traffic the device was configured to permit or deny, and where its logs and flow records were being sent — which is how you discover evidence sources you did not know existed. |
| **What it does NOT prove** | A routing table shows the paths available **now**, not the path a specific historical packet took; reconstructing that requires flow or capture, not configuration. An ACL proves what was configured, not what was enforced — order, interface direction and implicit rules decide the effect, and a permissive ACL does not prove traffic occurred. Like the CAM table, the routing table is RAM-resident and is lost on crash or power failure. |
| **How to parse it** | Capture the running configuration and routing table from the CLI during live response; follow the logging and flow-export lines to the collectors they name. |
| **Anti-forensics / false positive** | Seizing a router is operationally far harder than seizing a disk — INE makes the business-continuity point directly — so in practice this evidence is collected live, under time pressure, from a device that must keep running. |
`[U7 p104–106, p362–364]`

#### Files carved from network traffic
| | |
|---|---|
| **What it is** | Application-layer content reassembled out of a stream and written back out as a file. |
| **Where it lives** | Distributed across the packets of one flow; the file only exists once the flow has been identified and the payload bytes concatenated in sequence. |
| **What it proves** | That a specific file — matched by its signature and, once carved, by its hash — traversed the capture point between two endpoints at a given time, in a given direction. This is the strongest single link between a network event and a host artifact, because the carved file's hash can be compared against a file found on disk. |
| **What it does NOT prove** | Carving proves transfer past the sensor, not that the transfer completed at the far end, that the file was written to disk, or that anyone opened it. A partially captured flow yields a truncated file whose hash matches nothing, and treating that mismatch as "a different file" is a common error. Carving also cannot recover anything from an encrypted stream, so failure to carve is not evidence that no file moved. Direction must be read from the flow, not assumed — an uploaded and a downloaded file look the same once carved out of context. |
| **How to parse it** | Manually: identify the flow (Wireshark **Follow TCP/HTTP Stream**), locate the file signature, export the byte range. Automatically: `xplico` or `tcpxtract` against the pcap. The course's own S6 lab adds **NetworkMiner** for the same job (not in the INE units — see §7). |
| **Anti-forensics / false positive** | Compression, chunked encoding and multi-part transfers break naive signature carving; a file split across two flows will not reassemble. Always record the flow's five-tuple and time window with the carved file so the provenance survives into the report. |
`[U7 p285–292]`

#### Web-server, proxy and service access logs
| | |
|---|---|
| **What it is** | Server-side records of requests received, kept independently of the client and of the network sensor. |
| **Where it lives** | Web-server access logs and proxy logs on the serving side; equivalently, DHCP and DNS logs already covered above. INE's framing is that a web case usually requires examining **both** ends. |
| **What it proves** | That a request arrived at the server from a given source address at a given time, what was requested and what status was returned — surviving long after any capture has rolled and independent of anything on the client. |
| **What it does NOT prove** | The source address in a log is the address the server saw, which behind NAT, a proxy or a VPN is not the client's address at all; treating it as the endpoint is the standard mistake. Logs record requests, not humans, and are subject to the same intent problem as browser history. They are also written by the target of the investigation in intrusion cases, so an attacker with server access can edit or truncate them — an absence in a log is only as trustworthy as the host that wrote it. Clock skew between the log host and other sources is routine and must be measured, not assumed. |
| **How to parse it** | Text processing (`grep`, awk, or a log analyser); align to UTC before merging with host artifacts. Cross-check a sample of log lines against capture or flow to establish the log's reliability before relying on it. |
| **Anti-forensics / false positive** | Log rotation quietly destroys the window you need; proxy logs frequently hold the only record of internal-to-external requests once TLS hides the content. |
`[U7 p310, p367, p379]`

## 3 · Tools

| Tool | What it is for | Command / entry point | Output | Caveat |
|---|---|---|---|---|
| Registry Explorer / RECmd | Browsing and parsing registry hives offline; INE's tool of choice throughout the unit | GUI: load hive. CLI: `RECmd.exe -f <hive> --bn <batch>` | Decoded keys, values, last-write times, deleted-record recovery | Load a copy; dirty hives need transaction logs replayed |
| RegRipper | Plugin-driven registry triage | `rip.exe -r <hive> -f <profile>` | Text report per plugin | Plugin coverage varies by Windows version |
| PECmd | Prefetch parsing | `PECmd.exe -d C:\Windows\Prefetch --csv <out>` or `-f <file.pf>` | Run count, all retained run times, loaded-file list | Empty output may mean prefetching disabled, not "nothing ran" |
| AppCompatCacheParser | ShimCache extraction from a SYSTEM hive | `AppCompatCacheParser.exe -f <SYSTEM> --csv <out>` | Ordered entries with path and file-modified time | Entries are presence, not execution — see §2A |
| AmcacheParser | Amcache hive parsing | `AmcacheParser.exe -f <Amcache.hve> --csv <out>` | Paths, sizes, SHA-1 hashes, install records | Not taught in depth by INE; verify field meanings |
| LECmd | LNK parsing | `LECmd.exe -f <file.lnk>` / `-d <dir> --csv <out> -q` | Target path, volume serial and label, embedded MAC times | Office-created LNKs may carry no embedded dates |
| JLECmd | Jump list parsing | `JLECmd.exe -d <AutomaticDestinations dir> --csv <out>` | Per-application recent/pinned entries with LNK metadata | AppID mapping to application is an inference |
| ShellBags Explorer / SBECmd | ShellBag reconstruction | GUI, or `SBECmd.exe -d <hive dir> --csv <out>` | Rebuilt folder tree with timestamps and MFT numbers | Ingests NTUSER.DAT and USRCLASS.DAT; deduplicates |
| WinPrefetchView | Quick prefetch view (NirSoft) | GUI | Created/modified time, run counter, loaded files | Live-system oriented; PECmd exposes more run times |
| USBDeview | USB device history (NirSoft) | GUI, can query remotely | Device name, type, serial, date added, VID/PID | Live-oriented; corroborate with setupapi.dev.log |
| USBDeviceForensics | Aggregated USB registry extraction (Woanware) | GUI | Consolidated device/timestamp report | INE recommends reading its bundled `help.pdf` |
| rifiuti2 | Recycle Bin parsing | CLI against `INFO2` or `$I` files | Original path, size, UTC deletion time | Handles both legacy and modern layouts |
| recbin.exe | Recycle Bin parsing with timeline output (Harlan Carvey) | `recbin.exe -f <INFO2 or $I>`; `-c` CSV, `-t` TLN, `-s` system, `-u` user | STDOUT records or TLN timeline rows | Older tool; verify flags against the source page |
| vssadmin | Enumerating shadow copies | `vssadmin list shadows /for=C:` | Snapshot IDs and creation times | Administrative; pair with `mklink` to mount |
| ShadowCopyView / ShadowExplorer / libvshadow | Browsing and extracting from snapshots | GUI / library | Files as they were at snapshot time | Snapshots on live systems may still hold live malware |
| Thumbcache Viewer / Thumbs Viewer | Extracting cached thumbnails | GUI | Recovered images, entry sizes, modified times | Original path not stored; map separately |
| esentutl | Repairing or handling ESE databases (`Windows.edb`, `WebCacheV01.dat`) | `esentutl /p <db>` (INE prints `Esentutil.exe /p Windows.edb` — ⚠ verify) | Repaired database | `/p` is a repair operation — work on a copy only |
| DCode | Decoding timestamps of many formats | GUI: pick format, paste value | Human-readable date/time | Choosing the wrong format silently yields a plausible wrong date |
| Autoruns (Sysinternals) | Enumerating autostart locations far beyond `Run` | GUI on a live system | Every ASEP with signature status | Live-response tool; has no offline-image mode |
| bstrings / `strings` | Pulling readable text from binary blobs (e.g. Skype `chatsync` `.dat`) | `bstrings.exe -f <file>` | Extracted strings | Blunt instrument; loses structure and context |
| Autopsy / EnCase / FTK | Suite-level parsing of most artifacts in this module | GUI ingest modules | Consolidated artifact views | Convenient but opaque — verify a sample by hand |
| Wireshark | Interactive packet dissection, Follow Stream, custom dissectors | GUI; display filters (`http`, `dns`, `icmp`, `arp`, `bootp`) | Decoded packets, reassembled streams, exported objects | Buffers in RAM — unsuitable for long captures |
| tshark | Wireshark's engine without a GUI | `tshark -r <file.pcap> -Y '<display filter>'` | Same dissection, text or field output | Same filter language; scriptable |
| tcpdump | Sustained capture written straight to disk | `tcpdump -i <iface> -w <file.pcap> <bpf>` | pcap file | Pre-installed on Linux; use BPF to control volume |
| Berkeley Packet Filter (BPF) | Kernel-level capture filtering | Expression passed to tcpdump/dumpcap or Wireshark's capture-filter box | Only matching frames reach userspace | A capture filter discards non-matching traffic permanently |
| xplico / tcpxtract | Automated file carving from pcap | CLI against a capture file | Reconstructed files | Struggles with chunked, compressed or split transfers |
| NetworkMiner | Host-centric pcap parsing and file/credential extraction | GUI: open pcap | Hosts, sessions, extracted files and images | **Not in the INE units** — added by the course for S6 |
| Burp Suite | Intercepting proxy for HTTP | Configure browser proxy; Intercept tab | Live request/response with modify, forward, drop | Interception is an active technique — lab use only |
| Snort | Signature-based intrusion detection over traffic | Named only in INE's lab list | Alerts | Coverage in the unit is a lab reference, not teaching |
| pasco | Parsing IE `index.dat` | `pasco.exe index.dat` | Tab-delimited URL, modified and access times | IE ≤ 9 only; IE 10+ uses ESE |
| DB Browser for SQLite | Reading Chrome/Firefox/Skype SQLite stores | GUI, or Execute SQL tab | Table contents, custom queries | Some stores are SQLCipher-encrypted |
| BrowsingHistoryView / RedLine | Multi-browser history in one view | GUI | IE, Firefox, Chrome, Safari history combined | Confirm which browser actually ran before trusting scope |
| Skyperious / SkypeLogView | Skype database analysis | GUI | Messages, calls, transfers, exports, raw SQL | Version-bound to the local-SQLite era of Skype |
| KAPE | Targeted collection of these artifacts from a live or mounted system | Course tool, used in S5 | Collected artifact set plus module output | **Not in the INE units** — added by the course |
| Timeline Explorer | Reviewing and filtering the CSV output of the EZ tools | Course tool, used in S5 | Sortable, filterable artifact timeline | **Not in the INE units** — added by the course |

## 4 · Findings vs interpretation — worked from this module

> **FINDING** — The ShimCache entry `SYSVOL\ProgramData\lockit.exe` is present in the SYSTEM hive from EVI-SRC01, carrying a file-modified timestamp of 2026-03-11 09:14 UTC. No prefetch file `LOCKIT.EXE-*.pf` exists, and no UserAssist entry names it.
> **INTERPRETATION** — A binary of that name was written to `C:\ProgramData\` and catalogued by the compatibility infrastructure; the absence of both an execution artifact and a shell-launch record is consistent with tooling that was staged but never run.
> **CANNOT PROVE** — That `lockit.exe` executed. ShimCache is populated on metadata or path change regardless of execution, so the entry alone supports *presence at a path*, nothing more. It equally cannot prove the binary **never** ran: prefetching may have been disabled, the `.pf` may have rolled or been deleted, and non-shell execution leaves no UserAssist record. The safe claim is "no evidence of execution was found", not "it did not execute".

> **FINDING** — `PECmd` reports `UPDATER.EXE-4A1C9F02.pf` with a run count of 6, a first-run (file creation) time of 2026-03-09 21:47 UTC, a last-run time of 2026-03-11 06:22 UTC, and a loaded-file list including `C:\Users\<user>\AppData\Local\Temp\updater.exe`.
> **INTERPRETATION** — An executable at that user-writable Temp path was launched at least six times over roughly 33 hours, the most recent launch being on the morning of 11 March; the path is consistent with attacker tooling rather than an installed application.
> **CANNOT PROVE** — That a human launched it six times, or that anything happened *at* 06:22. The counter increments for service, scheduled-task, installer and crash-restart launches identically, and the last-run time is only the most recent of the six — the four intermediate runs are not individually dated by this artifact. Prefetch is system-wide, so it cannot attribute any of the six to a user profile.

> **FINDING** — `USBSTOR` contains `Disk&Ven_SanDisk&Prod_Ultra_USB_3.0&Rev_1.00\<serial>&0`; `MountedDevices` binds `\DosDevices\E:` to that serial; `setupapi.dev.log` shows the device's driver installation at 2026-03-11 07:02 (local); and `MountPoints2` in the compromised profile holds the matching volume GUID.
> **INTERPRETATION** — A removable device with that serial was first attached to EVI-SRC01 on the morning of 11 March, received drive letter `E:`, and was present while that user's profile was loaded — the sequence expected of the exfiltration step in this incident.
> **CANNOT PROVE** — That any file was copied to it. None of these four artifacts records read or write activity; together they prove attachment, letter assignment and profile-time presence only. The setupapi entry is a *first* installation, so it cannot show how long or how often the device stayed connected, and its local-time stamp must be converted before it is sequenced against the UTC registry values.

> **FINDING** — `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\Invoice_Q3.lnk` names target `E:\Invoice_Q3.docm`, records a target size of 74,240 bytes, a volume serial matching the device above, and LNK creation and modification times that differ by 41 hours.
> **INTERPRETATION** — A document by that name was opened from a volume with that serial, first at the LNK's creation time and most recently 41 hours later; the differing timestamps indicate access on at least two separate occasions rather than a single open.
> **CANNOT PROVE** — That the user read the document, that its content was what the filename suggests, or that the file still exists anywhere. The LNK records *access*, and access can be produced by a preview handler or an application's recent-file logic. The volume serial identifies a volume, not the physical device in evidence, until the registry join is made explicitly.

> **FINDING** — DNS traffic in the S6 capture shows 41 `A` queries for `cdn-sync.example` from the workstation between 08:00 and 12:00 UTC, each answered with `203.0.113.45`, and matching TLS sessions to `203.0.113.45:443` with a self-signed certificate whose subject does not match the queried name.
> **INTERPRETATION** — The host resolved and connected to a single external address at a rate and regularity inconsistent with user-driven browsing, using TLS with a certificate that fails basic validation — a pattern consistent with automated command-and-control rather than human activity.
> **CANNOT PROVE** — That this is C2, that data was exfiltrated over it, or what was sent. The capture shows resolution, connection and encryption; the payload is unavailable, so "exfiltration" is unsupported from the network side alone. A self-signed certificate is a lead, not a finding — legitimate internal and embedded services use them constantly. The regular interval is likewise suggestive, not probative: software updaters and telemetry produce identical timing signatures.

> **FINDING** — `$Recycle.Bin\<SID>\$IA1B2C3.7z` records original path `C:\Users\<user>\AppData\Local\Temp\stage\arch.7z`, original size 218,443,776 bytes, and deletion time 2026-03-11 07:41 UTC; the matching `$R` file is present and recoverable.
> **INTERPRETATION** — An archive of that size was assembled in a Temp staging directory and deleted through Explorer by that SID shortly after the USB device was attached — consistent with staging followed by clean-up.
> **CANNOT PROVE** — That the archive was copied to the USB device, or that deletion was an attempt to destroy evidence. The `$I` record proves an Explorer-mediated delete by that SID at that time and recovers the content; it says nothing about prior copy operations, and routine clean-up produces the same record. Note also what the absence of a bin on the USB device would prove: nothing, because Windows does not enable the Recycle Bin for removable storage.

> **FINDING** — `Terminal Server Client\Default\MRU0` in the compromised profile holds `198.51.100.20`, with a matching subkey under `…\Servers\198.51.100.20\`; the key's last-write time is 2026-03-10 22:15 UTC.
> **INTERPRETATION** — An RDP session was successfully established from this host to that address under this profile, most recently around that time — consistent with outbound lateral movement to the file server.
> **CANNOT PROVE** — That the intrusion arrived *via* RDP into this machine; the key is outbound only. It also cannot date the individual connections — `MRU0` is an ordering, and the single last-write time covers the whole key — nor prove what was done inside the session, nor that the person at this keyboard was the account holder. Confirmation has to come from authentication and session evidence on `198.51.100.20`.

## 5 · Exam-relevant points

- **Prefetch:** path `%SystemRoot%\Prefetch`; naming `NAME-<8 hex>.pf`; hash derives from the launch path, so the same binary from two paths yields two files; limits 128 (Vista/7) and 1024 (8/8.1/10); cache manager traces 10 s of application start, 2 min of boot; `NTOSBOOT-B00DFAAD.pf` is the boot trace; `.pf` creation = first run, modification = last run; last-run time inside the file sits ~10 s before the file's modified time; `EnablePrefetcher` values 0/1/2.
- **ShimCache:** stored in the SYSTEM hive under `Session Manager\AppCompatCache`; kernel-resident and written **only at shutdown**; 1,024 entries on Win7/2008, 512 earlier; the timestamp is the file's last-modified time; entries can exist for files that never executed; ShimCacheMem (Volatility) reads it from memory.
- **Amcache:** `%SystemRoot%\AppCompat\Programs\Amcache.hve`; Win7 predecessor `RecentFileCache.bcf`; KB2952664 introduces Amcache on Win7; carries SHA-1 hashes.
- **Registry:** hive signature `regf` at offset `0x0`; only keys carry a last-write time; FILETIME is 8 bytes of 100-ns intervals since 1601-01-01 UTC; `InstallDate` on Win10 is Unix 32-bit; hive file locations; `Select\Current` names the live ControlSet; the four root keys HKCR, HKCU, HKLM, HKU (plus HKCC).
- **Timezone:** `SYSTEM\ControlSet00#\Control\TimeZoneInformation`; `Bias` vs `ActiveTimeBias`; `DynamicDaylightTimeDisabled` 0/1; names resolve through `tzres.dll` string IDs.
- **USB chain:** `Enum\USBSTOR` → serial subkey (`&` as second character means Windows generated it) → `ParentIdPrefix` → `HKLM\SYSTEM\MountedDevices\\DosDevices\<letter>` → user-side `MountPoints2` → `setupapi.dev.log` (Vista+ in `C:\Windows\INF`, XP `setupapi.log` in `C:\Windows`). Know which of these gives first install, which gives per-user presence, and that none gives file transfer.
- **Recycle Bin:** XP `\Recycler\<SID>\` with `INFO2`; Vista+ `\$Recycle.Bin\<SID>\` with `$I` (metadata, UTC deletion time, original path and size) and `$R` (**R = raw content**); no Recycle Bin for removable storage by default; `Shift+Delete` bypasses; `NukeOnDelete = 1` disables.
- **ShellBags:** four NTUSER.DAT paths and two USRCLASS.DAT paths; `MRUListEx` 4-byte entries with most recent leftmost; bags carry MFT entry and sequence numbers.
- **LNK / jump lists:** `Recent` and Office `Recent` folders; jump lists in `Recent\AutomaticDestinations` (OS) and `Recent\CustomDestinations` (user-pinned); AppID is 16 hex digits; default 10 items, max 60; RDP jump list for lateral movement.
- **VSS:** first in Server 2003, comprehensive from Vista/7; block-level; 5 % default cap on Win7; `vssadmin list shadows /for=C:`; File History is file-level, Win8+, hourly, Libraries/Desktop/Contacts/Favorites only, driven by the USN journal.
- **UserAssist:** `NTUSER.DAT\…\Explorer\UserAssist\{GUID}\Count`; ROT13 value names; run count, last-executed FILETIME, focus time; GUI launches only.
- **TCP/IP:** three-way handshake SYN → SYN/ACK → ACK; four-way teardown FIN/ACK/FIN/ACK; `RST` for a closed TCP port; ICMP destination-port-unreachable for a closed UDP port; port ranges 0–1023 well known, 1024–49151 registered, 49152–65535 dynamic; encapsulation naming segment (TCP) / datagram (UDP) → packet → frame; unicast, multicast (class D), broadcast (last address in the network).
- **Protocol specifics:** DNS on TCP **and** UDP 53, record types A/AAAA/CNAME/PTR/TXT/NS/MX, names ≤ 253 characters; DHCP DORA on UDP 67/68, Wireshark filter `bootp`, options 53/50/51/54/55/61; ICMP type 8 request and type 0 reply; HTTP status classes 1xx–5xx; SMTP `HELO`/`EHLO`, `MAIL FROM`, `RCPT TO`, `DATA`, `VRFY`, with `AUTH LOGIN` credentials merely Base64-encoded.
- **TLS:** handshake protocol then record layer; nonces, certificate, pre-master key, master key, four derived keys; MAC over the exchanged messages; sequence numbers defeat replay; SSLv3 became TLS 1.0 at the IETF.
- **Network forensics:** OSCAR = Obtain, Strategise, Collect, Analyse, Report; flow roles sensor → collector → aggregator → analyzer; NetFlow v5 common and IPv4-only, v9 template-based, v10 = IPFIX, sFlow the IETF-adopted alternative; ~30 MB of flow per 8 GB of packets; SPAN vs port mirroring; promiscuous mode suffices on a hub and not on a switch; BPF filters at capture time; TLS leaves headers readable while IPsec ESP leaves only the data-link header.
- **Attacks to recognise from traffic:** DHCP starvation (many Discovers from non-existent MACs; countered by port security and DHCP rate limiting), rogue DHCP (countered by DHCP snooping), rogue DNS, SYN flood, full-connect vs half-open (SYN/stealth) vs zombie/idle scanning, TCP session hijacking (desynchronise then inject), MAC flooding, ARP poisoning.

## 6 · Teaching notes

**Lead S5 with the presence-vs-execution frame, not with a tool.** Put the three-column board up before opening any parser: *proves execution* (Prefetch, UserAssist), *proves presence* (ShimCache, Amcache), *proves access* (LNK, jump lists, ShellBags, RecentDocs). Every artifact taught that day gets placed in a column out loud. The single most common failure in student reports is a ShimCache row written up as an execution — INE itself calls the cache "a great alternative" to Prefetch on Servers, which is true for *coverage* and dangerously misleading about *meaning*, and students take the shortcut. Make them state the column before they state the conclusion.

**Demo the misread deliberately.** The strongest ten minutes in S5 is showing `lockit.exe` in the ShimCache output, asking the room what it proves, taking the wrong answer, then showing the empty Prefetch directory search for the same name and asking again. Do the same in reverse with `updater.exe`: run count 6, last run 06:22 — ask "what happened at 06:22?" and let someone answer "the malware ran", then establish that six runs produced one timestamp and that 06:22 is the *last* of them. Both demos take minutes and stick for the rest of the course.

**Demo live:** loading a SYSTEM hive in Registry Explorer and reading `Select\Current` before anything else; PECmd against a real `Prefetch` directory with the output in Timeline Explorer; the full USB join from `USBSTOR` serial through `MountedDevices` to `MountPoints2` and `setupapi.dev.log`, on screen, in that order — it is four artifacts and it is the clearest illustration in the course of why single-artifact conclusions fail. On the network side: a `Follow HTTP Stream` on a plaintext session, then the same host over TLS so the room sees exactly what disappears and what remains.

**Leave to homework:** the exhaustive registry-key catalogue (§2A's configuration keys), Thumbcache path mapping via `Windows.edb`, the Skype walk-through, and the browser-store tables. These are lookup material, not comprehension material, and they consume session time that belongs to the execution artifacts.

**Where students reliably go wrong:**
- Reading `ControlSet001` because it sorts first, instead of the set named by `Select\Current`.
- Treating a key's last-write time as the timestamp of a specific value.
- Quoting local-time `setupapi.dev.log` entries in a UTC timeline without conversion.
- Saying "the USB was used to exfiltrate" from registry evidence that only shows attachment.
- Reading the Windows Search history timestamp as the *last* search when it records the *first*.
- Concluding "the program never ran" from an empty Prefetch directory without checking `EnablePrefetcher`.
- Citing the RDP client MRU as evidence of an inbound connection.
- On the network side: claiming a host "did not communicate" from a capture taken at one interface; treating a DNS query as a visit; treating a valid certificate as proof of a legitimate endpoint; and assuming port 80 means HTTP and port 8080 does not.

**Assessment hook.** Every §2 table's *does NOT prove* box is a ready-made exam question, and the graded report rubric maps directly onto §4's three-line structure. Require students to write findings and interpretations as separate labelled sentences from the very first lab of S5; by S6 they should be flagging their own overreach without prompting.

**Sequencing note.** S5 and S6 are one arc, not two topics: the S6 capture is taken at the gateway precisely so that the RDP lateral movement is *missing* from it, forcing the class to go back to host artifacts. Say that out loud at the start of S6 rather than letting students discover it as a failure.

## 7 · Gaps, cautions and disagreements

**Topics the course needs that these units do NOT cover** (gap rows):

1. **Beaconing analysis** — the topic map asks S6 to teach C2 identification by beacon interval and jitter. Unit 7 gets as far as statistical flow analysis identifying "infected machines" by pattern `[U7 p296]` but never names beaconing, never defines an interval or jitter, and gives no detection method. Must be built from outside the units.
2. **TLS fingerprinting (JA3/JA3S and successors)** — named in the topic map, entirely absent from unit 7, which stops at reading certificate metadata `[U7 p453]`.
3. **DNS anomaly detection** — unit 7 states that records can be used to smuggle data out `[U7 p195]` and then never returns to it. No DNS tunnelling indicators, no entropy or query-length heuristics, no NXDOMAIN or DGA discussion.
4. **NetworkMiner** — required by the topic map for S6 file carving; unit 7 teaches carving with Wireshark, xplico and tcpxtract only. The tool is in the course's own instructor material but not in the source.
5. **Modern IDS/NSM stack** — Zeek, Suricata and modern Snort rule-writing are absent; Snort appears only as a lab title on a slide `[U7 p453]`.
6. **Wireshark "Export Objects"** — the topic map names it explicitly for S6; unit 7 describes manual byte-range export and automated tools but never this menu.
7. **Windows 10/11 artifact changes** — the OS version table in unit 6 stops at Windows 8.1 `[U6 p6]`. Nothing covers Win10/11-specific behaviour: the Windows Timeline/`ActivitiesCache.db`, `SRUM`, the Win8+ USB `Properties` sub-IDs for last-arrival and last-removal, or `AppCompatCache` format changes after Win8 (INE's own reference list points at a blog post on Win10 AppCompatCache changes but the slides do not teach it).
8. **Amcache in depth** — introduced in one slide `[U6 p155]` as ShimCache's successor. No key structure, no hash field, no explanation of what each timestamp means. Given how heavily S5 leans on the presence-vs-execution pair, this needs building out.
9. **Volume Shadow Copy destruction as an attacker action** — the unit teaches VSS as a recovery resource but never covers `vssadmin delete shadows` as a pre-ransomware step or how to evidence it.
10. **`$MFT`, `$LogFile` and `$UsnJrnl` as corroboration** — referenced only in passing (ShellBags carry MFT entry numbers; File History uses the USN journal) and taught in the file-system module, but S5 needs the cross-reference explicitly.
11. **Chromium-era browser forensics** — unit 6 devotes 33 pages to Internet Explorer (EOL) and unit 7 gives Chrome and Firefox roughly a dozen slides with Windows 7 paths. Edge/Chromium, profile handling, and modern cache formats are absent.
12. **Anti-forensics as a topic** — scattered warnings exist (Recycle Bin root hiding, LNK weaponisation, prefetch disabling) but there is no consolidated treatment of timestomping, log clearing or artifact deletion detection.

**Places where the material is dated:**

13. Tool set: INE teaches Eric Zimmerman's tools by their older names and does not mention **KAPE** or **Timeline Explorer**, which the course's own S5 uses as the collection and review layer. AccessData Registry Viewer and several NirSoft/Woanware utilities are still cited with live URLs that may no longer resolve.
14. `libvshadow` and `python-registry` are cited at Google Code addresses `[U6 p52, p376]`, which have not existed for years; both now live on GitHub.
15. Skype coverage assumes the local-SQLite desktop client `[U6 p393–417]`; modern Skype builds do not necessarily use that layout, so the section's value is now the *method* (image, install, exercise, re-image, diff) rather than the paths.
16. `index.dat` and IE's ESE `WebCache` are legacy; the ESE handling technique still transfers to `Windows.edb` and other ESE stores.
17. The Windows Search charm artifact `[U6 p96–101]` is a Windows 8/8.1 feature; its Win10/11 equivalent differs.
18. Unit 7's TLS discussion stops at TLS 1.2-era mechanics and defers all decryption to "the advanced Network forensics course" `[U7 p171]`; TLS 1.3, encrypted SNI/ECH and encrypted DNS all change what a modern capture yields.

**Factual errors in the source — INE wins on technical meaning for this course, but these should not be repeated to students:**

19. `[U7 p144]` states that the receiver "uses its **public** key to decrypt that data" in asymmetric encryption. The private key decrypts. Teach the correct mechanism and note the slide error.
20. `[U7 p82]` states the MAC address is 48 bits of which "the first **32** bits are called the OUI" and "the other **32** bits" are the NIC ID. The split is 24 + 24. The arithmetic in the slide is self-contradictory.
21. `[U7 p218]` states "the client IP address is the IP address offered by the DHCP server". In the DHCP header, `ciaddr` is the client's *current* address and `yiaddr` ("your IP address") is the offered one; the slide conflates them.
22. `[U7 p438]` describes the half-open (SYN/stealth) scan as terminating "immediately after receiving the **ACK** message". It is the SYN-ACK that is received and then reset.
23. `[U7 p160]` writes "OSCP" for **OCSP** (Online Certificate Status Protocol).
24. `[U7 p92]` gives unicast as "0.0.0.0 to 223.255.255.255", which sweeps in reserved and loopback space; and `[U7 p84]` says the MAC address "is used to identify the path which leads out of the network (the gateway)", which is true only for off-net destinations — on-net delivery uses the destination host's own MAC.

**Internal contradictions within the INE material:**

25. **LNK absolute path.** `[U6 p15]` states "the absolute path to the file is **not** stored in the lnk file". The LECmd output on `[U6 p24]` prints both `Local path: C:\…` and `Absolute path: My Computer\C:\…`. The slides contradict each other; teach the tool output and flag the claim.
26. **Jump list item-count key.** `[U6 p72]` places `Start_JumpListItems` under `HKLM\Software\…\Explorer\Advanced`; `[U6 p86]` places it under `HKCU\Software\…\Explorer\Advanced`. HKCU is the per-user setting; verify before teaching.
27. **Firefox profile path.** `[U7 p400]` gives `AppData\Local\Mozilla\Firefox\Profiles\`; `[U7 p412]` gives `AppData\Roaming\Mozilla\Firefox\Profiles\`. Roaming holds the profile and `places.sqlite`; Local holds cache.
28. **ShimCache execution flag.** `[U6 p151]` lists "whether the file actually ran on the system" among the decoded fields, while `[U6 p153]` states the cache records files "regardless of whether the file has executed". Both are on the same artifact three slides apart. The reconciliation — that an execution flag exists on some Windows versions and is neither present nor reliable on all — is not made anywhere in the unit, and this is the single most consequential ambiguity in the source. Teach `p153` as the rule and `p151` as a version-specific exception that must be verified per build.

**OCR uncertainty that matters** (each marked `⚠ verify against source page` in §2):

29. The Recycle Bin legacy naming convention `[U6 p110–111]`: the slide says "C is a fixed character" and then uses `C` as the drive letter in the `DC1.txt` example. The fixed character is `D`; the OCR has lost it.
30. USB timestamp property GUID `[U6 p350]`: truncated to `{83da632`. The full GUID and its property sub-IDs (install, last arrival, last removal) are not recoverable from the OCR.
31. `AppCompatCache` key path spacing `[U6 p154]`: "Session Manager" appears with and without its space across the two version paths.
32. Services key `[U6 p214, p216]`: rendered `\Service\` singular; the live key is `Services`.
33. Explorer context-menu hook `[U6 p227]`: rendered `SehllEx`; the key is `ShellEx`.
34. CustomDestinations path `[U6 p77]`: given as `%USERPROFILE%\AppData\Microsoft\Windows\Recent\CustomDestinations`, missing `\Roaming`.
35. ESE tool name `[U6 p40]`: printed `Esentutil.exe`; the Microsoft binary is `esentutl.exe`, and `/p` is a repair switch that must never be run against original evidence.
36. Network type codes `[U6 p244]`: the table survives only as two rows (`2` broadband `0x17`, `3` wireless `0x47`); the wired value is missing.
37. Unit 7's section numbering in the source Contents is itself corrupt — `7.9.9 DHCP`, `7.9.6 ICMP`, `7.5.7 ARP`, `7.9.1 HTTP` (which actually covers Berkeley Packet Filter and web/browser forensics, not HTTP) and `7.1.1 NETWORK ATTACKS` are out of sequence, and `7.4 NETWORKING DEVICES` appears twice at pages 4 and 96–110. §8 reproduces the numbering as the source has it; do not cite these section numbers to students as though they were meaningful.

**Scope note:** these units contain no Linux, macOS or mobile forensics, so nothing was excluded on out-of-scope grounds. Windows **Event Logs**, **timeline construction** and **reporting** are deliberately absent from this module because units 8, 9 and 10 own them; that is a module boundary, not a gap.

## 8 · Section index → source pages

**Unit 6 — Windows Forensics**

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `6.1` | Introduction | 4–8 | §0; §7 (version table dated) |
| `6.2` | User and System Artifacts | 9–10 | §1 · System artifacts vs user artifacts |
| `6.3.1` | LNK Files | 11–26 | §2A · LNK (shortcut) files |
| `6.3.2` | ThumbCache | 27–41 | §2A · Thumbcache and Thumbs.db |
| `6.3.3` | Volume Shadow Copy | 42–66 | §2A · Volume Shadow Copies; §2A · File History |
| `6.3.4` | JumpLists | 67–89 | §2A · Jump Lists |
| `6.3.5` | Libraries | 90–95 | §2A · Libraries (`.library-ms`) |
| `6.3.6` | Windows Search History | 96–101 | §2A · Windows Search history |
| `6.3` | Windows Recycle Bin | 102–127 | §2A · Recycle Bin ($I / $R, and legacy INFO2) |
| `6.4.1` | Prefetch Files | 128–148 | §2A · Prefetch (`.pf`); §4; §5 |
| `6.4.2` | Application Compatibility Cache | 149–158 | §2A · ShimCache; §2A · Amcache.hve; §1 · Presence vs execution |
| `6.5` | Windows Registry | 159–195 | §1 · Windows registry, Key last-write time, FILETIME; §2A · Registry hive files |
| `6.5.1` | Registry Artifacts | 196–243 | §2A · ControlSet, TimeZoneInformation, System identity, Network configuration, Services, Autostart, Evidence-affecting keys |
| `6.5.1.1` | Registry Artifacts | 244–244 | §2A · Network configuration and network history keys (partial — OCR incomplete, §7 item 36) |
| `6.5.1` | Registry Artifacts | 245–249 | §2A · System identity and lifecycle keys; §2A · Autostart keys (AppInit_DLLs) |
| `6.5.2` | User Hives | 250–311 | §2A · SAM accounts, LogonUI, UserAssist, RecentDocs, ComDlg32/RunMRU, Terminal Server Client MRU, Evidence-affecting keys, Internet Explorer |
| `6.6` | ShellBags | 312–329 | §2A · ShellBags |
| `6.7` | USB Forensics | 330–359 | §2A · USBSTOR, MountedDevices, MountPoints2, setupapi.dev.log; §4 |
| `6.8` | Browser Forensics | 360–368 | §2A · Internet Explorer history and typed URLs |
| `6.8.1` | Internet Explorer | 369–392 | §2A · Internet Explorer history and typed URLs |
| `6.9` | Skype Forensics | 393–429 | §2A · Skype local data store (method only); §7 item 15 |

**Unit 7 — Network Forensics**

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `7.4` | NETWORKING DEVICES | 4–4 | — divider slide |
| `7.1` | INTRODUCTION | 5–17 | §0; §1 · Network evidence tiers |
| `7.2` | TCP/IP PROTOCOL SUITE | 18–25 | §1 · Encapsulation; §5 |
| `7.2.1` | SERVER-CLIENT MODEL | 26–28 | §5 (assumed background) |
| `7.2.2` | Protocol METADATA | 29–31 | §1 · Encapsulation and what encryption hides |
| `7.2.3` | APPLICATION LAYER | 32–34 | §5 (assumed background) |
| `7.2.4` | TRANSPORT LAYER | 35–45 | §5 (port ranges, non-standard ports); §2B · Full packet capture |
| `7.2.5` | TRANSMISSION CONTROL PROTOCOL | 46–57 | §5 (handshake, teardown, RST) |
| `7.2.6` | USER DATAGRAM PROTOCOL | 58–62 | §5 (connectionless, ICMP port unreachable) |
| `7.2.7` | INTERNET LAYER | 63–79 | §5; §7 items 20, 24 |
| `7.2.8` | DATA-LINK LAYER | 80–85 | §2B · Switch evidence; §7 items 20, 24 |
| `7.2.9` | ENCAPSULATION | 86–92 | §1 · Encapsulation and what encryption hides |
| `7.3` | CLASSES OF TRAFFIC | 93–95 | §5 (unicast/multicast/broadcast) |
| `7.4` | NETWORKING DEVICES | 96–110 | §1 · Capture point determines the evidence ceiling; §2B · Switch evidence, Router evidence, Full packet capture |
| `7.5` | NETWORK PRoTocoLs NAP | 111–114 | §2B · HTTP request and response (intro slides) |
| `7.5.1` | HTTP | 115–140 | §2B · HTTP request and response |
| `7.5.2.1` | CRYPTOGRAPHY | 141–147 | §2B · TLS handshake and certificate; §7 item 19 |
| `7.5.2.2` | SSL/TLS | 148–190 | §2B · TLS handshake and certificate; §2B · SMTP session and email headers |
| `7.5.4` | DNS sip | 191–211 | §2B · DNS traffic and DNS server logs |
| `7.9.9` | DHCP | 212–238 | §2B · DHCP traffic and lease data; §7 item 21 |
| `7.9.6` | ICMP | 239–252 | §2B · ICMP traffic |
| `7.5.7` | ARP | 253–269 | §2B · ARP traffic and ARP cache |
| `7.6` | NETWORK FORENSICS | 270–271 | — divider slide |
| `7.6.1` | PROTOCOL ANALYSIS | 272–280 | §2B · Full packet capture; §3 (Wireshark, tshark) |
| `7.6.2` | FLOW ANALYSIS | 281–284 | §1 · Network evidence tiers; §2B · Files carved from network traffic |
| `7.6.3` | FILE CARVING & DATA EXTRACTION | 285–292 | §2B · Files carved from network traffic |
| `7.6.4` | STATISTICAL FLOW ANALYSIS | 293–308 | §1 · Flow record ecosystem; §2B · Flow records; §7 item 1 |
| `7.6.5` | NETWORK FORENSICS | 309–316 | §1 · Network evidence tiers; §2B · Web-server, proxy and service access logs |
| `7.7` | EMAIL FORENSICS | 317–329 | §2B · SMTP session and email headers |
| `7.8` | OSCAR | 330–340 | §1 · OSCAR |
| `7.9` | NETWORK EVIDENCE ACQUISITION | 341–368 | §1 · Capture point; §2B · Full packet capture, Switch evidence, Router evidence, DHCP, DNS |
| `7.9.1` | HTTP | 369–415 | §2B · Full packet capture (BPF); §2A · Internet Explorer history; §2A · Chrome and Firefox data stores |
| `7.1.1` | NETWORK ATTACKS | 416–455 | §5 (attacks to recognise); §2B · DHCP, ARP, Switch evidence; §7 item 22 |
