---
room: Windows Memory & Network
url: https://tryhackme.com/room/windowsmemoryandnetwork
module: Memory Analysis — **third and last of the three-room set** (Processes → User Activity → **Network**)
feeds: S6 — **`S6-04` network evidence**, **`S6-10` Volatility**, **`S6-09` capstone (closes the chain)**.
       Also **S1** (the strongest findings-vs-interpretation material in the whole path) and the
       ATT&CK-mapping discipline.
       **Carries a deprecated ATT&CK technique and three mis-mappings — see §3.**
difficulty / time: Medium · 60 min · 8 tasks · Premium · 2,382 completions
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ. Same image, host, scenario and network
              map as rooms 12–13 (transcribed in room 12's note, not repeated here).
---

## 1. What the room teaches

The network third of the same investigation, and the room that finally names the malware: it finds
the C2, proves code injection, matches Meterpreter with YARA, recovers the PowerShell payload out
of a process dump, and closes with an ATT&CK table for the whole three-room chain.

The technical spine is strong — `windows.netscan` → `windows.malfind` → `windows.vadyarascan` →
`windows.memmap --dump` → `strings`. Five plugins, each answering a question the previous one
raised, ending in a complete attack narrative.

**And it is the most instructive room in the path for the wrong reasons.** It contains, in one
place, the three classic over-conclusions our rubric exists to penalise:

1. **A YARA match reported as identification.** Five weak patterns hit the minimum threshold of a
   rule whose two most distinctive patterns did **not** match — and the room writes *"confirming
   the presence of a Meterpreter session."*
2. **A TCP socket reported as a protocol.** PowerShell holds a raw TCP connection open to port 22
   and the room maps it to **T1021.004 SSH — Lateral Movement**. Nothing authenticated. Nothing
   negotiated. `Start-Sleep 1` in a loop.
3. **🔴🔴 A string in a memory dump reported as an event.** The room greps a process dump, finds
   `[!] HttpSendRequestA failed.`, and concludes *"the process tried a POST connection, but it
   seemed to fail."* The **same output also contains `[+] Hosts file exfiltrated to http://`** —
   the success message. Both are in the binary's static string table. **`strings` shows what a
   program *can* print, never what it *did* print.**

Finding 3 is the single best teaching artifact in fourteen rooms. **`S1` should open with it.**

## 2. Artifacts — one 6-box block each

### 2.1 Socket objects in the pool (`windows.netscan`)

- **What it is** — every TCP and UDP endpoint object still recoverable from kernel memory,
  **including connections that have already closed**.
- **Where it lives** — kernel pool memory, found by **pool-tag scanning** for `TCP_ENDPOINT` and
  `UDP_ENDPOINT` objects, then mapped back to owning `_EPROCESS`.
- **What it proves** — the whole network picture in one command:

  | proto | local | remote | state | PID / owner | created |
  |---|---|---|---|---|---|
  | TCPv4 | `192.168.1.192:55985` | `10.0.0.129:8081` | ESTABLISHED | 10032 `updater.exe` | — |
  | TCPv4 | `0.0.0.0:4443` | — | **LISTENING** | 10084 `windows-update` | 07:13:05 |
  | TCPv4 | `192.168.1.192:4443` | `10.0.0.129:47982` | ESTABLISHED | 10084 `windows-update` | 07:13:35 |
  | TCPv4 | `192.168.1.192:55987` | `192.168.0.30:22` | ESTABLISHED | 6984 `powershell.exe` | 07:15:15 |

  🟢 **Two C2 channels in opposite directions** — `updater.exe` dials **out** to 8081 (reverse),
  while `windows-update.exe` **listens** on 4443 and takes an inbound connection from the same
  attacker host (bind). The room notes the listener but never draws the reverse-vs-bind
  distinction. **We do — it is the difference between egress filtering and ingress filtering as a
  control.**
- **What it does NOT prove** — 🔴 **that a connection carried the protocol its port implies.**
  Port 22 is a *number*, not SSH. Port 8081 is not HTTP. See §2.4. It also does not prove **when**
  a connection ended — there is a `Created` column and no closed time — nor **how much data
  crossed**, nor **what was sent**. ⚠️ Pool scanning also produces **false positives**: a byte
  pattern resembling an endpoint object is not an endpoint.
- **How to parse it** — `vol -f <image> windows.netscan > netscan.txt`, then
  `grep LISTENING` / `grep <process>`. Columns: `Offset · Proto · LocalAddr · LocalPort ·
  ForeignAddr · ForeignPort · State · PID · Owner · Created`. Both this and `windows.netstat` are
  current in 2.28.0 and **share the identical ten-column set**; the difference is the method.
- **Anti-forensics / false-positive caveat** — 🟢 **run both and diff.** `netscan` **scans pools**
  (finds closed and terminated sockets, some false positives); `netstat` **walks live tracking
  structures** in `tcpip.sys` (fewer results, higher confidence). ⚠️ **`netstat` fails outright
  without tcpip symbols** — its source raises *"Unable to locate symbols for the memory image's
  tcpip module"* — and its debug log is a catalogue of partial-parse conditions. **In an
  air-gapped lab, `netstat` is the one that breaks.** The room's *"try also running
  `windows.netstat`"* is good advice with the failure mode omitted.

### 2.2 Injected memory regions (`windows.malware.malfind`)

- **What it is** — memory regions whose permissions and contents do not match how legitimate code
  gets loaded.
- **Where it lives** — the process's **VAD tree**; the plugin looks for private, committed regions
  marked `PAGE_EXECUTE_READWRITE` with no mapped file behind them.
- **What it proves** — one region in `updater.exe`, `0x1a0000`–`0x1d1fff`, tag `VadS`,
  `PAGE_EXECUTE_READWRITE`, `PrivateMemory 1`, **note `MZ header`**. The first bytes are
  `4d 5a 41 52 55 48 89 e5` — 🟢 **`MZAR`, the classic Metasploit reflective-loader stub, where
  the `MZ` DOS signature is *also valid x64 instructions*** (`dec ebp; pop rdx; push r10; push
  rbp; mov rbp, rsp`). A PE header that executes is not an accident.
- **What it does NOT prove** — 🔴🔴 **that the region is malicious.** `PAGE_EXECUTE_READWRITE`
  private memory is exactly what a **JIT compiler** produces — .NET, Java, JavaScript engines,
  and every browser tab on the machine. `malfind` output is a **candidate list**, and the room
  never says so. It also does not prove **who** injected it — a region inside `updater.exe` could
  have been written by a different process entirely.
- **How to parse it** — 🔴 **`windows.malware.malfind --pid <PID>`.** The room uses the old
  `windows.malfind`, which is a rename shim with `removal_date="2026-06-07"` — **already past**.
  It survives in 2.28.0 only because that release shipped on 30 Apr 2026; **the next release can
  drop it.** Columns include `Notes` (populated from the `b"MZ" → "MZ header"` mapping) and a
  `Disasm` column the room does not mention but which is where the real reading happens.
- **Anti-forensics / false-positive caveat** — 🟢 **the two-part rule**: executable **and** no
  mapped file **and** a recognisable header. Any one alone is noise. Room 11 already framed this
  as *"same signature, different meaning"*; this room supplies the positive case to sit beside it.

### 2.3 A YARA hit inside a process (`windows.vadyarascan`)

- **What it is** — a rule scan restricted to one process's VAD-mapped user-space regions.
- **Where it lives** — per-process VAD regions, so **every hit is attributed to a named process**.
- **What it proves** — five matches inside PID 10032, all within `0x140004104`–`0x14000414a` — a
  **70-byte window**. 🟢 **The tight clustering is the real signal** and the room does not mention
  it: five independent patterns landing in seventy bytes is far stronger than five scattered hits.
- **What it does NOT prove** — 🔴🔴 **that this is Meterpreter.** The rule's condition is
  `5 of them` and **exactly five matched — the bare minimum.** More importantly, **the two most
  distinctive patterns did not match**: `$s1 = { fce8 8?00 0000 60 }` (the canonical Metasploit
  shellcode prologue) and `$s2 = { 648b ??30 }` (the PEB fetch) are **both absent**. The rule
  passed on its five *weakest* strings — one of which, **`$s4 = "ws2_"`, is a fragment of
  `ws2_32.dll`, present in an enormous number of entirely benign binaries.** The room writes
  *"confirming the presence of a Meterpreter session."* **A YARA match is a pattern match. It is a
  lead, and the strength of the lead is a property of the rule, not of the tool.**
- **How to parse it** — `windows.vadyarascan --pid <PID> --yara-file <rule>`.
  ⚠️ **Flag currency:** valid options in 2.28.0 are `--pid`, `--yara-file`, **`--yara-string`**,
  `--yara-compiled-file`, `--insensitive`, `--wide`, `--max-size`. **`--yara-rules` was renamed to
  `--yara-string`** — material written against the old name will fail. Contrast with plain
  `yarascan`, which sweeps the **kernel layer**, has **no `--pid`**, and returns four columns with
  **no process attribution**. For finding injected code in a known PID, `vadyarascan` is the
  correct choice and the room picks right.
- **Anti-forensics / false-positive caveat** — 🔴 **report the rule, the threshold and which
  strings matched — never just "YARA matched".** Our version of this exercise gives students the
  rule and the five hits and asks: *what would raise your confidence?* (Answer: `$s1`/`$s2`
  matching; a second independent rule; the disassembly at the region; C2 traffic consistent with
  the framework.) 🟢 The room hands us a **calibration exercise for free.**

### 2.4 The PowerShell payload, recovered from a process dump

- **What it is** — the actual command PowerShell was running, carved out of its own memory.
- **Where it lives** — the full process memory image written by `windows.memmap --pid 6984 --dump`
  to `pid.6984.dmp`, then `strings … | grep 192.168.0.30`.
- **What it proves** — the exact one-liner, **twice**:
  `$client=New-Object Net.Sockets.TcpClient; $client.Connect("192.168.0.30",22); while($client.Connected){Start-Sleep 1}`
- **What it does NOT prove** — 🔴🔴 **SSH, authentication, or lateral movement.** Read what the
  code does: it opens a **raw TCP socket** to port 22 and **sleeps in a loop while it stays open**.
  There is no SSH client, no key exchange, no credential, and **nothing is ever sent or received**.
  This is a **connectivity check or a keep-alive**, and the honest finding is
  *"a TCP connection to 192.168.0.30:22 was established and held open by PID 6984 at 07:15:15."*
  🔴 **The room maps it to `T1021.004 — Remote Services: SSH`, Lateral Movement.** That is an
  interpretation presented as a finding, and it is doubly wrong: **Windows is not even a listed
  platform for T1021.004** (ESXi, Linux, macOS only). ⚠️ Two matches in the dump are also not two
  executions — the same string routinely appears in several buffers.
- **How to parse it** — `windows.memmap --pid <PID> --dump` → `pid.<PID>.dmp` → `strings | grep`.
  ⚠️ `memmap`'s `--pid` takes **a single PID**, not a list (unlike `malfind`/`vadyarascan`).
  `-o` is honoured; **re-running in the same directory appends a counter rather than overwriting**,
  so a second run silently produces a different filename.
- **Anti-forensics / false-positive caveat** — 🟢 **`strings` on a process dump is an
  unstructured, unordered, undated view.** It gives you candidate text and no context: no idea
  which memory region, whether it is a literal or runtime-generated, or when it got there.
  **Follow every `strings` hit back to its region** — `vadyarascan` on the same string will tell
  you whether it lives in the mapped image (a literal) or in a private heap allocation
  (runtime data). The distinction is the whole of §2.5.

### 2.5 🔴🔴 The exfiltration strings — capability, not occurrence

- **What it is** — the string table of `windows-update.exe`, surfaced from `pid.10084.dmp`.
- **Where it lives** — the mapped PE image inside the process dump. The Windows loader maps a
  binary's **entire** `.rdata`/string section into the address space regardless of which code
  paths ever run; `windows.memmap --dump` writes out every mapped segment.
- **What it proves** — 🟢 **capability, precisely and usefully**: the binary contains a WinINet
  HTTP POST routine (`InternetOpenA` / `InternetConnectA` / `HttpOpenRequestA` /
  `HttpSendRequestA`), a `Content-Type: application/x-www-form-urlencoded` header, a component
  named **`Exfiltrator`**, the target path
  **`C:\Windows\System32\drivers\etc\hosts`**, and the domains **`attacker.thm`**,
  **`external-attacker.thm`** and `http://attacker.thm/updater.exe`. That is a complete,
  defensible finding about **what this binary is built to do.**
- **What it does NOT prove** — 🔴🔴 **that any of it happened.** The room's own grep output
  contains, side by side:

  ```
  [!] InternetOpenA failed.          [!] HttpOpenRequestA failed.
  [!] InternetConnectA failed.       [!] HttpSendRequestA failed.
  [+] Hosts file exfiltrated to http://
  ```

  **Those are mutually exclusive outcomes on any single run, and all of them are present.** The
  room reads the failure strings and concludes *"it seemed to fail"*; a student reading two lines
  lower would conclude it succeeded. **Both are wrong for the same reason: this is the format-string
  table, not a log.** `strings` is a byte-pattern extractor with no model of execution — GNU
  `strings` "prints the printable character sequences… followed by an unprintable character", and
  nothing more. **Presence of a message establishes that the program can emit it. Nothing else.**
- **How to parse it** — the strings themselves are fine; the **conclusion** is what must change.
  What would actually settle whether the POST happened:
  - **`windows.netscan`** for an outbound connection from PID 10084 to the C2 on the HTTP port,
    in any state including CLOSED — the pool scan recovers terminated sockets.
  - **`windows.handles` / `windows.dlllist`** for an open `wininet.dll` handle and WinINet cache
    or cookie files under the user profile.
  - **`windows.vadyarascan --pid 10084 --yara-string "…"`** to check whether the string appears in
    a **private heap allocation** (runtime-formatted, with data interpolated) or only in the mapped
    image (a literal). **A formatted instance is evidence; the template is not.**
  - **Console output** — `windows.consoles` / `windows.cmdscan` for a screen buffer containing the
    message as actually printed.
  - **The `Disasm` column at the call site** — showing the failure string is referenced from a
    conditional branch proves it is a template.
  - **Ground truth off the host** — PCAP, proxy or firewall logs, **Sysmon Event ID 3**, NetFlow.
    **Bytes on the wire is the only thing that decides a transfer succeeded.**
- **Anti-forensics / false-positive caveat** — 🟢 **the sentence to teach**:
  *presence of a string in a memory dump establishes **capability**, never **occurrence**;
  telling "the program can say this" from "the program said this" is the discipline.*

### 2.6 The listening port as an artifact (bind vs reverse C2)

- **What it is** — `windows-update.exe` (PID 10084) bound to `0.0.0.0:4443` and accepting an
  inbound connection from `10.0.0.129:47982`.
- **Where it lives** — the same pool endpoint objects as §2.1, `State = LISTENING` plus a second
  `ESTABLISHED` row for the accepted connection.
- **What it proves** — 🟢 **the direction of control.** `updater.exe` reaches **out** (reverse
  shell, defeats inbound firewall rules); `windows-update.exe` **waits** (bind shell, requires the
  attacker to reach in). **One incident, both patterns** — and it means egress filtering alone
  would not have stopped this.
- **What it does NOT prove** — 🔴 **that a listening socket is malicious.** The same output shows
  `System` on 445 and 139, `svchost.exe` on 3389, 49671 and 5040 — all legitimate. **The finding is
  not "a process is listening", it is "a process with no business listening is listening on a
  non-standard port from a user-profile path."** Three facts, and the room's own reasoning uses all
  three even though it states only the last.
- **How to parse it** — `cat netscan.txt | grep LISTENING`, then subtract the known-good set —
  **which is the baseline-differencing method from room 12 applied to ports instead of processes.**
- **Anti-forensics / false-positive caveat** — ⚠️ **the room calls `10.0.0.129` "an external
  network".** `10.0.0.0/8` is **RFC 1918 private space**, and it is not on the room's own network
  map (whose internet edge is `10.10.8.6`). It is external *to the described subnets*; it is not a
  public address. **Say "outside the documented network ranges", not "external"** — the difference
  matters when you are deciding whether to call an ISP or walk down the hall.

### 2.7 The host's own IP address

- **What it is** — `192.168.1.192`, the local address on every connection in §2.1.
- **Where it lives** — the `LocalAddr` column of the endpoint objects.
- **What it proves** — 🔴🔴 **it identifies the host, and it contradicts the case file.** Room 12's
  network map lists the USER LAN as `192.168.1.0/24` with **`WIN-012` at `192.168.1.192`**. The
  scenario page calls the compromised host **`WIN-001`**. **The memory says the host is WIN-012.**
  Room 12 flagged that WIN-001 was missing from the network diagram; **this is why — it was never
  missing, it was mislabelled.**
- **What it does NOT prove** — ⚠️ **that the map is right and the case file wrong** — only that
  they disagree. Resolving it needs the map's provenance and date, and an ARP or DHCP record. 🟢
  **That is the correct answer to the question, and it is a much better exercise than picking a
  side.**
- **How to parse it** — read `LocalAddr` in `netscan`; corroborate with
  `windows.registry.printkey` on the TCP/IP interfaces key, or the hostname from `windows.info`.
- **Anti-forensics / false-positive caveat** — a memory image can hold **stale** addresses from
  before a DHCP renewal, and a multi-homed host has several. **Never take one `LocalAddr` as the
  host's identity without corroboration** — which is exactly the discipline this contradiction
  teaches.

### 2.8 The lateral-movement target

- **What it is** — `192.168.0.30`, the destination of the PowerShell TCP connection.
- **Where it lives** — `ForeignAddr` on the PID 6984 endpoint, and as a literal in `pid.6984.dmp`.
- **What it proves** — 🟢 **the target is `FS-01`, the Linux file server on the SERVER LAN**, per
  room 12's network map (`192.168.0.0/24` — FS-01 `.30`, AD-01 `.31`, DB-01 `.32`). **Port 22 on a
  Linux file server is a coherent destination**, which is what makes the room's SSH reading
  tempting.
- **What it does NOT prove** — 🔴 **that anything moved.** See §2.4: the socket opened and was held
  open. **Coherent and proven are different words.** Nor does it prove the attacker knew what
  `192.168.0.30` was — the address may have come from a scan, the hosts file (which the exfil
  routine targets), or an ARP cache.
- **How to parse it** — cross-reference `netscan` `ForeignAddr` against the network map, then
  **pivot to the target host** — a second image or its `auth.log` is what would settle whether an
  SSH session ever authenticated.
- **Anti-forensics / false-positive caveat** — 🟢 **this is the natural end of a memory
  investigation and the natural start of the next one.** The honest closing line of a report on
  this image is *"PID 6984 opened and held a TCP connection to FS-01:22; determining whether a
  session was established requires evidence from FS-01."* **No room in this path ever writes a
  sentence like that. Ours will.**

## 3. Tools and commands

| step | command as the room writes it | what it gives |
|---|---|---|
| connections | `vol -f <image> windows.netscan > netscan.txt` | all TCP/UDP endpoints, incl. closed |
| listeners | `cat netscan.txt \| grep LISTENING` | bound ports by process |
| sanity check | `vol -f <image> windows.netstat` | live tracking structures — fewer, higher confidence |
| injection | `vol -f <image> windows.malfind --pid 10032` ⚠️ deprecated name | RWX private regions + hexdump + disasm |
| YARA | `vol -f <image> windows.vadyarascan --pid 10032 --yara-file meterpreter.yar` | per-process rule hits |
| process dump | `vol -f <image> windows.memmap --pid 6984 --dump` → `pid.6984.dmp` | full process memory |
| strings | `strings pid.6984.dmp \| grep "192.168.0.30"` | recovered payload text |
| context grep | `strings pid.10084.dmp \| grep "POST" -C 8` | ⚠️ **string table, not a log — §2.5** |

### CURRENCY CHECK — verified 2026-08-28 against Volatility 3 **v2.28.0** and ATT&CK **v19.2**

| # | item | result |
|---|---|---|
| 1 | 🔴 **room runs Volatility `2.26.0`** | Current **2.28.0** (30 Apr 2026). ⚠️ **Three-room set, three inconsistencies:** room 12 = `2.26.2` + alias `vol3` (git clone, `python3 vol.py`); rooms 13 and 14 = `2.26.0` + `vol` (pip entry point). **Pin one build and one invocation for our lab and write every command to match.** |
| 2 | 🔴 **`windows.malfind` is a deprecated alias — third memory room in a row to use it** | Canonical **`windows.malware.malfind`**. The shim is `PluginRenameClass … removal_date="2026-06-07"` — **already past**, surviving in 2.28.0 only because that release predates the date. **The next release can remove it.** |
| 3 | ✅ **`windows.vadyarascan` exists and is current** | `plugins/windows/vadyarascan.py`, `_version = (1,1,4)`, **not deprecated**. Attributes every hit to a named process. Plain `yarascan` scans the **kernel layer**, has **no `--pid`**, and returns four columns with **no process attribution** — `vadyarascan` is the right choice for a known PID. |
| 4 | 🔴 **`--yara-rules` no longer exists** | Renamed to **`--yara-string`**. Valid flags in 2.28.0: `--pid`, `--yara-file`, `--yara-string`, `--yara-compiled-file`, `--insensitive`, `--wide`, `--max-size`. The room uses `--yara-file`, which is fine — **but any of our material written against `--yara-rules` will fail.** |
| 5 | ✅ **`windows.memmap`** | Current. `--pid` is a **single int, not a list**; `--dump` writes `pid.<PID>.dmp` (literal `f"pid.{pid}.dmp"`). Global `-o` is honoured. ⚠️ **Re-running in the same directory appends a counter instead of overwriting** — a second run silently produces a different filename, which will confuse students mid-lab. |
| 6 | ✅ **`windows.netscan` and `windows.netstat`** | Both current, **neither deprecated**, and they share the **identical ten-column set**. `netscan` uses `poolscanner` (pool tags — recovers closed sockets, some false positives); `netstat` uses `pdbutil` + `modules` and walks `tcpip.sys` tracking structures. 🔴 **`netstat` hard-fails without tcpip symbols** (*"Unable to locate symbols for the memory image's tcpip module"*) — **relevant to our air-gapped lab.** Note: the only deprecation inside `netstat` is an internal helper (`create_tcpip_symbol_table`), **not the plugin.** |
| 7 | ✅ `windows.pslist`, `windows.cmdline` | Current, not deprecated. |
| 8 | 🔴🔴 **`T1043 — Commonly Used Port` is DEPRECATED** | The room's ATT&CK table cites it. ATT&CK's own page: *"This technique has been deprecated. Please use Non-Standard Port where appropriate."* **Deprecated in ATT&CK v7, July 2020 — five years before this room was written.** Replacement: **T1571 Non-Standard Port** (C2). ⚠️ And the logic inverted: T1043 flagged *common* ports; **T1571 flags uncommon protocol/port pairings.** Ports 8081 and 4443 fit T1571 and would never have fit T1043. **Both the ID and the reasoning are stale.** |
| 9 | 🔴🔴 **`T1055.002` is NOT "Reflective DLL Injection"** | T1055.002 is **Process Injection: Portable Executable Injection** (tactics **Stealth**, Privilege Escalation). The correct technique for reflective loading is **T1620 — Reflective Code Loading** (tactic **Stealth**), whose description is written for exactly this case: *"allocating then executing payloads directly within the memory of the process, vice creating a thread or process backed by a file path on disk."* T1055.001 is **Dynamic-link Library Injection** — a different mechanism (a DLL on disk via `LoadLibrary`), a poor fit here. 🔴 **And the room files it under "Command & Control".** Neither T1620 nor any T1055 sub-technique sits under C2. **Wrong name, wrong ID, wrong tactic.** |
| 10 | 🔴 **`T1021.004 SSH` is not supported by the evidence** | The artifact is a raw `Net.Sockets.TcpClient` connect to port 22 held open by `Start-Sleep`. No SSH. ⚠️ **And Windows is not a listed platform for T1021.004** (ESXi, Linux, macOS). See §2.4. |
| 11 | 🔴 **`T1140 Deobfuscate/Decode` is mis-justified** | The ID and name are right and its tactic is now **Stealth**, but the room's rationale — *"downloaded payload with no arguments to evade detection"* — describes **neither obfuscation nor its reversal**. "No command-line arguments" is **an absence of an artifact, not an adversary behaviour**, and has no ATT&CK entry. Defensible instead: **T1105 Ingress Tool Transfer** for the download, **T1059.005** for the macro. **Claim T1140 only if you can point at an actual decode step.** |
| 12 | ⚠️ **`T1547.001` — right ID, half a name** | The room prints *"T1547.001 - Startup Folder"*. The full name is **Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder**. There is **no ATT&CK technique called "Startup Folder"**. 🟢 **But note: room 14 gets this technique RIGHT where room 12 got it WRONG** (room 12 used T1037.005, a macOS technique). **Two rooms in one set, same artifact, contradictory mappings.** That contradiction is itself a teaching exercise. |
| 13 | ⚠️ **`T1041` is defensible but not the best fit** | The binary builds its **own** WinINet handle to POST the hosts file over cleartext `http://`. **T1048.003 — Exfiltration Over Alternative Protocol: Exfiltration Over Unencrypted Non-C2 Protocol** is the better mapping, since it is a separate unencrypted request rather than reuse of an established C2 channel. T1041 fits only if the POST rides the existing channel. |
| 14 | ✅ **correct rows in the room's table** | **T1566.001** Spearphishing Attachment · **T1059.005** Visual Basic · **T1059.001** PowerShell · **T1071.001** Application Layer Protocol: Web Protocols. All four verified. |
| 15 | ⚠️ **"Defense Evasion" appears in the room's table** | **TA0005 was renamed to "Stealth" in ATT&CK v19**; the residue became **TA0112 Defense Impairment**. Already logged as a repo-wide item in room 13 §3 #16 and **already back-propagated** to `fat32-analysis.md`. |
| 16 | ➕ **there is no ATT&CK ID for a bind shell** | Enterprise ATT&CK does **not** distinguish bind from reverse shells. For the 4443 listener, **T1571 Non-Standard Port** is the defensible mapping (its own procedure examples are written in listener terms — *"binds and listens on port 1058"*). **T1095 Non-Application Layer Protocol** applies if the channel is raw TCP rather than an application protocol; **T1205 Traffic Signaling** only for a dormant listener woken by a magic packet. **Say so explicitly in our material** — students hunt for a bind-shell ID and there isn't one. |

### 🟢 Our corrected ATT&CK chain for the whole three-room incident

| tactic | ID | name | evidence |
|---|---|---|---|
| Initial Access | **T1566.001** | Phishing: Spearphishing Attachment | `cv-resume-test.docm` |
| Execution | **T1204.002** | User Execution: Malicious File | UserAssist / session context |
| Execution | **T1059.005** | Command and Scripting Interpreter: Visual Basic | recovered VBA (room 13) |
| Command and Control | **T1105** | Ingress Tool Transfer | `MSXML2.XMLHTTP` + `ADODB.Stream` |
| Stealth | **T1564.003** | Hide Artifacts: Hidden Window | `Shell filePath, vbHide` |
| Persistence | **T1137.001** | Office Application Startup: Office Template Macros | macro in `Normal.dotm` ← **rooms miss this** |
| Persistence | **T1547.001** | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | `…\Startup\windows-update.exe` |
| **Stealth** | **T1620** | **Reflective Code Loading** | `malfind` RWX + `MZAR` stub ← **replaces the room's T1055.002/C2** |
| Command and Control | **T1571** | **Non-Standard Port** | 8081 outbound, 4443 listening ← **replaces deprecated T1043** |
| Command and Control | **T1071.001** | Application Layer Protocol: Web Protocols | WinINet POST routine |
| Execution | **T1059.001** | Command and Scripting Interpreter: PowerShell | PID 6984 |
| Exfiltration | **T1048.003** | Exfiltration Over Unencrypted Non-C2 Protocol | hosts-file POST — ⚠️ **capability only, §2.5** |
| ~~Lateral Movement~~ | — | **not established** | TCP socket to `:22` only — §2.4 |

**Two rows carry a limit rather than a claim.** That is the table our students should learn to
write, and it is the difference between our material and the room's.

## 4. Evidence used

- **The same image as rooms 12 and 13** — `THM-WIN-001_071528_07052025.mem`, MD5
  `78535fc49ab54fed57919255709ae650`, on an Ubuntu lab VM at `/home/ubuntu`.
- 🟢 **New in this room: pre-computed outputs.** Task 4 notes *"you can access the same output in
  the already existing file `netscan-saved.txt`. There are also some other commands that have been
  pre-saved to save time."* A sensible accommodation for a slow plugin on a big image — **and a
  pattern we should copy**, since `netscan` on a 4 GB image is minutes of dead classroom time.
  **Pre-compute the slow outputs, hand them out, and let students run one live to see the cost.**
- **Not downloadable. No licence offered. Not reusable.** Nothing for `ecdfp-evidence`.

### 🟢 The fourth documentation inconsistency is now RESOLVED — and it is the best of the four

Room 12 flagged that the compromised host `WIN-001` does not appear on the network map, whose USER
LAN runs `WIN-012`…`WIN-019`. **Room 14 supplies the missing fact: the host's own IP is
`192.168.1.192`, which that map labels `WIN-012`.**

So the host was never missing from the diagram — **the case file gives it a different name than
the network documentation does.** Both artifacts are internally consistent; they disagree with each
other, and nothing in any of the three rooms notices.

Combined with the acquisition-time resolution from room 13, **all four of room 12's inconsistencies
are now adjudicable from evidence**:

| # | the disagreement | what the evidence says |
|---|---|---|
| 1 | narrative "May 5th" vs artifacts 2025-05-07 | **artifacts** — every timestamp in three rooms agrees |
| 2 | case file `.dmp` vs every command `.mem` | **unresolved** — a naming slip, no artifact decides it |
| 3 | filename `071528` vs narrative "07:45 CET" | **filename** — FTK Imager launched 07:15:28 (room 13) |
| 4 | host `WIN-001` vs map `WIN-012` | **the IP is `192.168.1.192`** — the map's label matches |

🟢🟢 **This is now a complete, self-contained exercise and it is the best one the three rooms
produced.** Hand students the case file, the network map and the three plugin outputs, and ask them
to **adjudicate each contradiction and state which are undecidable.** It needs no lab machine, no
image and no tooling; it exercises D7 and D20 criterion 4 directly; and **row 2 has no answer**,
which is the point. **Build it.**

## 5. Lab design worth reusing

1. **🟢🟢 Five tools, one escalating question.** `netscan` finds a connection → `cmdline` shows no
   arguments → `malfind` finds injected code → `vadyarascan` tests a hypothesis → `memmap` +
   `strings` recovers the payload. **Every step is motivated by the previous result, never by a
   syllabus.** This is the best-sequenced task in fourteen rooms and it is the shape `S6-09` should
   take end to end.
2. **🟢 "No arguments" read as a signal, not a null result.** *"This is common for binaries that
   serve as droppers or loaders, especially those that use in-memory injection or reflective
   loading."* An empty field interpreted as evidence — a genuinely good instinct, and the one
   place the room reasons better than its material.
3. **🟢 Pre-computed slow outputs.** See §4. Copy it.
4. **🟢 A YARA rule printed in full, with its condition.** The rule is on the page — `5 of them` —
   so the threshold is auditable. **The room shows its working and then misreads it, which makes it
   more useful to us than a rule that simply worked.** See §2.3.
5. **⚠️ `grep -C 8` for context.** Small, good habit, explicitly taught. Keep it — **and pair it
   with the §2.5 warning about what the surrounding lines actually are.**
6. **🔴 The ATT&CK table is the room's headline and it is 4-of-10 wrong.** But it is the right
   *format* — tactic · technique · detail · **the plugin that produced it**. 🟢 **Keep the columns,
   fix the rows, and use the original as a marking exercise:** hand students the room's table and
   the corrected one and ask them to find the four errors. That exercise teaches ATT&CK currency,
   platform checking, and the deprecation lifecycle in one pass.

### ✅ No safety defect in this room

Nothing is executed; the malware is only read. The `memmap --dump` output lands in the working
directory like room 12's `dumpfiles`, but here it is a **memory dump**, not an extracted PE — it
cannot be double-clicked into running. **Rooms 10, 11 and 14 are clean; the five defects are
concentrated in rooms 6, 8, 9, 12 and 13** (table in room 13 §5).

⚠️ **One thing our version must add that the room omits:** the recovered artifacts include **live
C2 infrastructure** — `10.0.0.129`, `attacker.thm`, `external-attacker.thm`,
`http://attacker.thm/updater.exe`. In a real engagement these are **not to be resolved, fetched or
scanned from the analysis network**, because doing so tips off the operator and can burn the
investigation. The room redacts the URL for puzzle reasons and never states the rule. **Ours does.**

## 6. Question patterns

**16 questions across 8 tasks** — the most of any room in the set, and the split is stark.

**🔴 Nine are single-value lookups from one file.** *"What is the remote source port number…"* ·
*"Which internal IP address received a connection on port 22?"* · *"What is the exact timestamp…"* ·
*"What is the local port used…"* · *"What is the protocol used in the connection from
192.168.1.192:55985 to 10.0.0.129:8081?"* · *"What port was windows-update.exe listening on?"* —
six of them read the **same `netscan.txt`**. A student who runs one command answers half the room.

**🟢 Three are good.**
- *"What is the order in which the potential malicious processes established outbound
  connections?"* — **requires sorting by the `Created` column and reasoning about sequence.** The
  best question in the room.
- *"What is the virtual memory address space of the suspicious injected region in updater.exe?"* —
  requires running `malfind`, reading the VAD columns and knowing which of them is the answer.
- *"What is the first 2-byte signature found in the shellcode?"* (`4d 5a`) — small, but it makes
  the student read a hexdump and connect `MZ` to a PE header.

**🔴 One is actively harmful.** *"What is the protocol used in the connection from
192.168.1.192:55985 to 10.0.0.129:8081?"* The intended answer is read off the `Proto` column —
**TCPv4** — which is fine. But sitting three questions from *"which internal IP received a
connection on port 22"* and next to an ATT&CK table that maps that port to **SSH**, it trains
exactly the reflex we are trying to break: **port number → protocol name.** 🟢 **Our version asks
the same question and then asks the follow-up the room never does:** *"and what protocol was
carried over it?"* → **cannot be determined from `netscan`.**

**🔴 Fourteenth room, still no question whose answer is "cannot be determined"** — and this room
had the richest crop of candidates in the entire path:

| the room could have asked | correct answer |
|---|---|
| *"Did the HTTP POST exfiltration succeed?"* | **Cannot be determined.** The dump contains both the success and the failure strings; `strings` shows the format-string table, not a log (§2.5). |
| *"Did the attacker move laterally to 192.168.0.30?"* | **Not established.** A TCP socket to port 22 was opened and held. No authentication, no protocol, no data (§2.4). |
| *"Is the injected region in `updater.exe` malicious?"* | **A lead, not a finding** — RWX private memory is also what every JIT produces; the `MZ` header and the YARA cluster raise confidence, they do not settle it (§2.2). |
| *"Is this Meterpreter?"* | **The rule matched at its exact threshold on its five weakest strings, and the two distinctive patterns did not match** (§2.3). |
| *"What is this host's name?"* | **The case file and the network map disagree** (§2.7, §4). |

**Five ready-made questions, all answerable from evidence already on screen, none asked.** 🟢 **The
room has effectively written our assessment for us — we ask the questions it left on the table.**

**And the room's own summary commits the errors its questions avoid**: *"confirming the presence of
a Meterpreter session"*, *"suggesting lateral movement"* hardened by Task 7 into
*"Lateral Movement — T1021.004 SSH"*, and *"it seemed to fail"*. 🟢 **Task 7's five-line attack
chain plus its ten-row ATT&CK table is a finished D20 criterion-4 marking exercise** — hand it over
and ask which lines the evidence supports, which are interpretation, and which are wrong.

## 7. Figures we would need to draw

Figures present in the room: **none.** Task 2 repeats room 12's network map; everything else is
terminal output, one YARA rule and one ATT&CK table. **Three rooms, one continuous investigation,
and not a single conceptual diagram between them.**

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **capability vs occurrence** | one process box split in two: **mapped image** (`.rdata`) holding *every* message the binary can print — success and failure side by side, both shaded neutral — and **private heap** holding one *formatted* string with runtime data interpolated, accented; caption *"strings finds both. Only one is evidence."* | **highest** — this is the `S1` opener |
| 2 | **two C2 directions in one incident** | the host in the middle; `updater.exe` arrow **outbound** to `10.0.0.129:8081` labelled *reverse — defeats ingress filtering*; `windows-update.exe` **inbound** from `10.0.0.129:47982` to `:4443` labelled *bind — defeats egress filtering*; caption *"one attacker, both directions — neither control alone would have stopped this"* | **highest** |
| 3 | **port number is not a protocol** | one `netscan` row magnified, `ForeignPort 22` circled, with two branches: *"SSH session"* struck through and *"a TCP socket was opened and held"* accented; below, the actual PowerShell one-liner with `Start-Sleep 1` highlighted | **high** — the room's own trap |
| 4 | **the YARA rule as a confidence instrument** | the seven strings listed, `$s1` and `$s2` greyed with *"the distinctive ones — did not match"*, `$s3`–`$s7` accented with their offsets showing all five inside a 70-byte window, and the condition `5 of them` boxed with *"threshold met exactly"*; caption *"a match is a property of the rule"* | **high** |
| 5 | **`malfind`'s two-part test** | reuse room 11's figure 3 (RWX + no mapped file) and **add the positive case**: the `MZAR` bytes shown twice — once as a DOS header, once as the x64 instructions they also are | medium |
| 6 | **the corrected ATT&CK chain** | the §3 table as a left-to-right kill chain, with the room's four wrong cells shown struck through beside their replacements (T1043→T1571, T1055.002→T1620, T1021.004→*not established*, T1140→T1105), and the **two limit rows drawn as open ends rather than arrows** | **high** — the marking exercise made visual |
| 7 | **the four contradictions, adjudicated** | four rows: claim · counter-claim · the artifact that decides · verdict — with **row 2 (`.dmp` vs `.mem`) ending in a question mark**, deliberately | medium |

Figures 1, 2 and 6 are the ones that carry the course's argument. Never their images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct

Mapped to `S6`. Correct — and this room lands on **`S6-04`** as much as `S6-10`, which Part 1 does
not say. **Amend Part 1's row for this slug to name both.**

### Rows this strengthens

- **`S6-04`** network evidence — 🟢 **this room supplies the host-side half of the row.** Rooms 1–11
  gave us network evidence from the wire; this gives it from RAM: `netscan` recovers **closed**
  sockets a PCAP never saw and a live `netstat` would have missed, and attributes each to a PID.
  Combined with room 11's `bulk_extractor`-carves-PCAP-from-memory pivot, `S6-04` now has **two
  independent host-side routes to network evidence.** Fully sourced.
- **`S6-10`** — `netscan`/`netstat`, `malfind`, `vadyarascan`, `memmap`. The three memory rooms
  together now over-supply this 15-minute row several times over.
- **`S6-09` capstone** — 🟢 **the five-tool escalation (§5.1) is the capstone's structure**, and
  §2.8's closing sentence (*"determining whether a session was established requires evidence from
  FS-01"*) is **how the capstone report should end**: a finding, a limit, and a next step.
- **`S1`** — 🟢🟢 **three contributions, and they are the strongest in the path:**
  1. the **capability-vs-occurrence** exercise (§2.5) — the opener;
  2. the **contradiction-adjudication** exercise (§4) — now complete across three rooms;
  3. the **ATT&CK marking exercise** (§5.6) — the room's ten-row table against our corrected one.
- **The ATT&CK discipline generally** — this room alone yields: a technique **deprecated five years
  before the room was written**, a technique cited under **the wrong name and the wrong tactic**, a
  technique cited **outside its platform**, and a technique with **a justification that does not
  describe it**. **Four distinct failure modes, one table.** That is a lesson we could not have
  designed better ourselves.

### Four things `S6-04` / `S6-10` must do differently

1. **Use `windows.malware.malfind`, and `--yara-string` not `--yara-rules`.**
2. **Never let a port number stand in for a protocol.** Teach the `netscan` row as
   *"a TCP connection to port N"*, full stop.
3. **Report YARA matches with the rule, the threshold and which strings hit** — never "YARA
   matched".
4. **Teach `strings` output as capability.** Occurrence needs a socket, a handle, a heap-resident
   formatted instance, console output, or evidence off the host.

### Minutes

Everything here is **correction**, **exercise material** for rows that already exist (`S1`,
`S6-09`), or **figures**. `S6-04` and `S6-10` are now over-supplied, not under-supplied.

**No new rows. S6 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **The S5 overdraft has now been carried unresolved across nine rooms. It needs a structural
re-split, and no further room extraction will change the number.**

### Out of scope

Malware analysis of the Meterpreter payload — correctly deferred. Analysis of `FS-01` — explicitly
out of scope and correctly flagged as requiring separate evidence. **No scope conflict.**

### Still unresolved

**Browser forensics** — fourteenth room, still no `DECISIONS.md` row. **Decide it.**

## 9. Links

- Room: <https://tryhackme.com/room/windowsmemoryandnetwork>
- The set, in order: `windowsmemoryandprocs` → `windowsmemoryanduseractivity` → **this room**.
  One image, one host, one timeline. **Read the three notes together.**
- Room's stated prerequisites: Volatility · **Yara** · Windows Memory & Processes ·
  Windows Memory & User Activity.
- Volatility 3 docs: <https://volatility3.readthedocs.io/en/stable/> (**`/stable/`, not `/latest/`**)
- ATT&CK corrections:
  **T1043 (deprecated)** <https://attack.mitre.org/techniques/T1043/> →
  **T1571** <https://attack.mitre.org/techniques/T1571/> ·
  **T1620 Reflective Code Loading** <https://attack.mitre.org/techniques/T1620/> ·
  T1055.002 <https://attack.mitre.org/techniques/T1055/002/> ·
  T1021.004 <https://attack.mitre.org/techniques/T1021/004/> ·
  T1048.003 <https://attack.mitre.org/techniques/T1048/003/> ·
  T1140 <https://attack.mitre.org/techniques/T1140/> ·
  **TA0005 Stealth** <https://attack.mitre.org/tactics/TA0005/> ·
  **TA0112 Defense Impairment** <https://attack.mitre.org/tactics/TA0112/> ·
  v7 deprecation notes <https://attack.mitre.org/resources/updates/updates-july-2020/>
- `strings` semantics (the §2.5 argument): GNU binutils
  <https://sourceware.org/binutils/docs/binutils/strings.html> · PE format / section mapping
  <https://learn.microsoft.com/en-us/windows/win32/debug/pe-format>
- Full memory-tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block D**
- Companion notes: `windows-memory-and-processes.md` (scenario, network map, the four
  inconsistencies) · `windows-memory-and-user-activity.md` (the ATT&CK v19 tactic rename, UserAssist
  corrections, T1137.001)
