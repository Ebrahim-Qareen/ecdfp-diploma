---
room: Volatility Essentials
url: https://tryhackme.com/room/volatilityessentials
module: Memory Analysis (Section 6 of Advanced Endpoint Investigations)
feeds: S6 — **`S6-10` Volatility 3 in the capstone (direct hit)** + the Volatility homework
       track (Part 4). Also `S2-03` (format table) and `S6-04` (the bulk_extractor pivot).
       **Changes our `EVS-03` acquisition plan — see §3.**
difficulty / time: Medium · 60 min · 8 tasks
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

Volatility 3 as a working tool: its three-layer architecture (memory layers → symbol tables →
plugins), then roughly fifteen plugins applied across two cases — a banking trojan masquerading as
an Adobe document, and a ransomware post-incident analysis.

It is correct on the thing most Volatility material gets wrong: it states plainly that v3
**"abandoned static OS profiling in favour of dynamic symbol resolution"** and that
**"OS profiles have been deprecated… now we have the individual information plugins"** — i.e.
`windows.info` replaces `imageinfo`. That matches our currency finding exactly, and makes this room
safe to build `S6-10` on where a v2-era source would not be.

Its real strength is **pairing plugins by evasion**: `pslist` and `psscan` are taught together,
because the second exists to catch what the first misses. That pairing is the lesson, not the
commands.

## 2. Artifacts — one 6-box block each

### 2.1 Active process list (`pslist`)

- **What it is** — the processes Windows itself is tracking.
- **Where it lives** — the kernel's **doubly-linked list of `_EPROCESS` structures** — the same
  source Task Manager reads.
- **What it proves** — which processes the OS considered active at capture, with PIDs, parent PIDs
  and exit times.
- **What it does NOT prove** — 🔴 **that this is every process.** A rootkit that **unlinks** its
  `_EPROCESS` entry disappears from `pslist` entirely while continuing to run. The room states this
  as the reason `psscan` exists. Absence from `pslist` is therefore never evidence of absence.
- **How to parse it** — `python3 vol.py -f <image> windows.pslist`
- **Anti-forensics / false-positive caveat** — Direct Kernel Object Manipulation (DKOM) unlinking
  is the named technique. `pslist` is the **fast, trustworthy-when-positive** view: what it shows
  is real, what it omits is unknown.

### 2.2 Unlinked processes (`psscan`)

- **What it is** — processes found by scanning memory for structures that *look like* `_EPROCESS`,
  rather than by following the list.
- **Where it lives** — anywhere in the memory image; pool-tag/structure scanning, not list walking.
- **What it proves** — processes **hidden by unlinking**, and often terminated processes whose
  structures have not yet been overwritten.
- **What it does NOT prove** — 🔴 **the room states the caveat and it is the important one:
  structure scanning "can also result in false positives; therefore, we must be careful."** A byte
  pattern that resembles an `_EPROCESS` is not a process. `psscan` output must be corroborated, not
  reported.
- **How to parse it** — `windows.psscan`
- **Anti-forensics / false-positive caveat** — 🟢 **the diff is the technique**: entries in
  `psscan` but not `pslist` are the hunting ground. Teach the pair, never either alone.

### 2.3 Process hierarchy (`pstree`)

- **What it is** — the same data as `pslist`, arranged by parent PID.
- **Where it lives** — same `_EPROCESS` list.
- **What it proves** — **lineage**, which is where the story lives: `winword.exe` spawning
  `cmd.exe` spawning `powershell.exe` is a narrative that a flat list hides. The room's Case 001
  questions turn on exactly this — find the Adobe process, then its parent, then that parent's PID.
- **What it does NOT prove** — a parent PID is **recorded at creation and not maintained**. If the
  parent exited, the PID may have been reused by an unrelated process, producing a false lineage.
  And it inherits every `pslist` blind spot (§2.1) because it uses the same source.
- **How to parse it** — `windows.pstree`
- **Anti-forensics / false-positive caveat** — parent-PID spoofing is a documented technique; a
  plausible tree is not a verified one.

### 2.4 Handles — files, registry keys, threads

- **What it is** — the objects a process has open.
- **Where it lives** — per-process handle tables in memory.
- **What it proves** — which **files, registry keys, mutexes and events** a process was holding at
  capture. Mutex and **KeyedEvent** names are frequently malware-family fingerprints — the room's
  question asks for one by name.
- **What it does NOT prove** — an open handle proves *access*, not *action*: a held file handle
  does not show a read, a write or the content. Handles closed before capture are simply gone.
- **How to parse it** — `windows.handles`
- **Anti-forensics / false-positive caveat** — the room states none. Legitimate software holds
  thousands of handles; **this artifact is only useful once you have a process to scope it to.**

### 2.5 Network connections (`netstat`, `netscan`)

- **What it is** — network state recovered from memory.
- **Where it lives** — kernel network structures. Two plugins, two techniques:
  `windows.netstat` walks memory structures with a network connection; **`windows.netscan`** uses
  **pool scanning** and recovers **active *and closed*** TCP/UDP connections with PIDs, local and
  remote ports and IPs.
- **What it proves** — who was talking to whom, and — via `netscan`'s closed connections — **traffic
  that had already ended before capture**, which is often the C2 evidence.
- **What it does NOT prove** — a connection in memory does not prove data was transferred or what
  it contained. A remote IP is an endpoint, not an attacker — and `netscan`'s pool scanning carries
  the same false-positive risk as `psscan`.
- **How to parse it** — `windows.netstat` / `windows.netscan`
  ⚠️ **the room's own warning is worth carrying: `netstat` "can be very unstable, particularly
  around old Windows builds."**
- **Anti-forensics / false-positive caveat** — 🟢 **the room supplies the best cross-tool tip in the
  batch: when Volatility cannot recover the connections, run `bulk_extractor` against the memory
  image to carve a PCAP out of it.** bulk_extractor is **already on our FOR-WS01/FOR-LNX01 list
  (Part 6)**, so this costs nothing to adopt and gives `S6-05` a host-side route to C2 evidence
  when the network capture is missing.

### 2.6 Loaded DLLs (`dlllist`)

- **What it is** — the modules each process has loaded.
- **Where it lives** — per-process module lists in memory.
- **What it proves** — which DLLs a process loaded and **from where**. The room's question —
  *how many DLLs used by the Adobe process are outside `system32`* — is the technique in one line:
  **load path is the anomaly**, not the DLL count.
- **What it does NOT prove** — that a DLL was malicious or that its code ran. Reflectively-loaded
  and manually-mapped modules **do not appear here at all**, which is precisely what sophisticated
  in-memory malware does.
- **How to parse it** — `windows.dlllist`
- **Anti-forensics / false-positive caveat** — as above: absence from `dlllist` is the expected
  result for the injection techniques `malfind` exists to catch. The two are complementary.

### 2.7 Injected code (`malfind`, `vadinfo`)

- **What it is** — memory regions that look like injected code.
- **Where it lives** — process heaps and virtual address descriptors (VADs).
- **What it proves** — the room explains the detection logic exactly right: it finds regions where
  the **executable bit is set (RWE or RX)** and/or there is **no memory-mapped file on disk** —
  i.e. **fileless malware**. Output gives PID, offset, and hex/ASCII/disassembly of the region.
  🟢 **An `MZ` header in the injected region indicates a Windows executable**; without one you are
  looking at shellcode and the analysis is different.
- **What it does NOT prove** — 🔴 **RWE memory is not inherently malicious.** JIT compilers
  (.NET, Java, browsers) legitimately allocate executable-writable memory constantly. `malfind` is
  a *lead generator*; every hit needs the header check and corroboration.
- **How to parse it** — 🔴 **`windows.malware.malfind`, NOT `windows.malfind`** — see §3.
  `windows.vadinfo` for the detailed VAD walk.
- **Anti-forensics / false-positive caveat** — the false-positive rate is the caveat, and the room
  does not state it. Ours to add.

### 2.8 Kernel structures — SSDT, modules, drivers

- **What it is** — the kernel-level view, where rootkits operate.
- **Where it lives** — three plugins, three sources:
  **`windows.ssdt`** — the System Service Descriptor Table, which resolves system-call addresses
  (`NtCreateFile` and friends) · **`windows.modules`** — loaded drivers and kernel modules from the
  linked list · **`windows.driverscan`** — raw scan for `DRIVER_OBJECT` structures **unlinked** from
  that list.
- **What it proves** — SSDT entries redirected to malicious handlers; loaded drivers with their base
  address, size and path; and drivers hidden from `modules`.
- **What it does NOT prove** — 🟢 **the room makes the single best interpretive point in the whole
  batch: "Hooks are not inherently malicious; antivirus and debugging tools also use them
  legitimately. The analyst's responsibility is to identify whether the presence of a hook aligns
  with expected system behaviour or represents malicious interference."** That is findings-vs-
  interpretation (D7) stated as well as any textbook. A hook is an observation; malice is a
  conclusion requiring a baseline.
- **How to parse it** — `windows.ssdt` · `windows.modules` · `windows.driverscan`
- **Anti-forensics / false-positive caveat** — the same list-vs-scan pairing as §2.1/§2.2, one level
  down: `modules` walks a list a rootkit can unlink from; `driverscan` finds what it hid. The room
  adds **`windows.modscan`** as a third option that evades both.

## 3. Tools and commands

| plugin | command | what it gives |
|---|---|---|
| `windows.info` | `python3 vol.py -f <image> windows.info` | kernel base, DTB, symbols, build, **capture time** |
| `windows.pslist` | … `windows.pslist` | active process list |
| `windows.psscan` | … `windows.psscan` | unlinked / terminated processes |
| `windows.pstree` | … `windows.pstree` | process hierarchy |
| `windows.handles` | … `windows.handles` | file/registry/thread handles |
| `windows.netstat` | … `windows.netstat` | connections (⚠️ unstable on old builds) |
| `windows.netscan` | … `windows.netscan` | active **and closed** TCP/UDP + PIDs |
| `windows.dlllist` | … `windows.dlllist` | loaded DLLs and paths |
| **`windows.malware.malfind`** | … `windows.malware.malfind` | injected code regions ⚠️ **room uses the old name** |
| `windows.vadinfo` | … `windows.vadinfo` | virtual address descriptors |
| `windows.ssdt` | … `windows.ssdt` | system-call table, hook detection |
| `windows.modules` | … `windows.modules` | loaded kernel modules |
| `windows.driverscan` | … `windows.driverscan` | unlinked `DRIVER_OBJECT`s |

Room's "worth knowing" list: `windows.callbacks` · `windows.driverirp` · `windows.modscan` ·
`windows.moddump` · `windows.memmap` · `yarascan`.

Dependencies the room names: Python 3.6+, plus `pefile`, `capstone` and `yara-python` for PE
parsing, disassembly and YARA rules.

### CURRENCY CHECK — cross-referenced to `_TOOL_CURRENCY_2026-08-28.md` block D

| item | result |
|---|---|
| 🔴 **the room uses `windows.malfind`** | Renamed to **`windows.malware.malfind`**. The old path is a deprecation shim with `removal_date="2026-06-07"` — **already passed**. It still runs and emits a `FutureWarning`; it dies at the next release. **`S6-10` and the homework track must use the new name.** |
| 🔴 **room runs Volatility 2.26.2**; current is **2.28.0** (30 Apr 2026) | Two minor versions behind. Nothing else in the room is affected, but pin **2.28.0** in our lab and re-verify the plugin names against the installed build. |
| ✅ **the room is correct that profiles are gone** | *"OS profiles have been deprecated… now we have the individual information plugins"* — matches our finding. Safe to build on; a v2-era source would not be. |
| ✅ `python3 vol.py` is right **for this install method** | The room clones the repo, so `vol.py` exists. **A `pip install volatility3` provides `vol` and no `vol.py`.** Pick one for our lab and write every command to match. |
| 🔴🔴 **the `.vmem` metadata warning — this changes our `EVS-03` plan** | The room's own output: *"No metadata file found alongside VMEM file. **A VMSS or VMSN file may be required to correctly process a VMEM file. These should be placed in the same directory with the same file name.**"* See §4 — our VMware snapshot route must capture **both files, same basename, same directory**. |
| ⚠️ **the two memory rooms disagree on hypervisor formats** | This room: Hyper-V → `.bin`, VirtualBox → `.sav` ("a partial memory file"). Room 10 (Memory Acquisition): Hyper-V → **`.vmrs`**, VirtualBox → **`.elf`** via `VBoxManage debugvm dumpvmcore`. **Room 10 is the better guidance** — `.vmrs` is the modern Hyper-V runtime-state file and `.elf` is a proper core dump, whereas `.sav` is a saved-state file the room itself calls partial. **Teach room 10's methods.** Both rooms agree VMware → `.vmem`. |
| ⚠️ stale cross-reference | The room's conclusion says *"In the next room, Memory Acquisition, we will cover memory acquisition"* — but the path lists **Memory Acquisition before Volatility Essentials**. Harmless, but it means the room text predates the current path ordering. |
| Room's version claims | ✅ **first room in eleven to state a tool version** — `Volatility 3 Framework 2.26.2` appears in its own terminal output. Credit where due. |

## 4. Evidence used

- Two memory images on an Ubuntu lab VM under `~/Desktop/Investigations/`:
  **`Investigation-1.vmem`** (Windows guest from VMware; banking trojan case, suspicious IP given)
  and **`Investigation-2.raw`** (ransomware case).
- Volatility pre-installed at `~/Desktop/volatility3`.
- **Not downloadable. No licence offered. Not reusable.**
- **Nothing to flag for `ecdfp-evidence` from the room itself.**

### 🔴 But it amends the `EVS-03` route proposed from room 10 — read this before staging

Room 10 established that snapshotting our VMware EVI-SRC01 gives Tier 1 memory with no acquisition
tool on the guest. **This room shows the trap in that plan.** Volatility warns:

> *No metadata file found alongside VMEM file. A VMSS or VMSN file may be required to correctly
> process a VMEM file. These should be placed in the same directory with the same file name.*

**So `EVS-03` is not one file, it is a pair.** Staging requirements:

1. Capture **`<name>.vmem` AND `<name>.vmss`/`.vmsn` together** — identical basename, same directory.
2. **Hash both**, and list both in the manifest — the metadata file is part of the evidence set.
3. **Distribute both.** A student handed only the `.vmem` gets a warning and possibly degraded
   results, which will read to them as their mistake.
4. Verify the pair parses **offline** on `CLEAN-TOOLS` before the session, since Volatility also
   needs its symbols pre-staged (block D2).

This is exactly the kind of detail that silently ruins a session, and we would not have caught it
from room 10 alone.

## 5. Lab design worth reusing

1. **🟢 Teach plugins in evasion pairs, not alphabetically.** `pslist` → *"malware unlinks itself"* →
   `psscan`. `modules` → *"drivers can be unlinked too"* → `driverscan` → `modscan`. **The second
   plugin's existence is the lesson about the first plugin's limits.** This is the single most
   reusable idea in the room and it maps straight onto our 6-box "what it does NOT prove".
2. **🟢 One hunting rule stated with its false-positive built in.** The hook passage — *"Hooks are
   not inherently malicious; antivirus and debugging tools also use them legitimately"* — is D7 in
   two sentences. **Quote the sentiment in `S6-10`.**
3. **🟢 Two cases with different shapes.** Case 001 is guided with a starting IOC handed over
   (a suspicious IP); Case 002 is post-incident with no lead at all. Same tool, two investigative
   postures. Good model for `S6-09` (capstone) vs `S6-10`.
4. **🟢 A concrete anomaly heuristic per plugin**, not just a command: DLLs **outside `system32`**;
   an **`MZ` header** in an injected region; **RWE/RX with no mapped file**. Students get a
   decision rule they can apply to unfamiliar output.
5. **🟢 The cross-tool fallback** (§2.5): when `netstat` fails, carve a PCAP with `bulk_extractor`.
   Teaches that a tool's failure is a routing decision, not a dead end.

**No safety defect in this room** — second clean room in a row after Memory Acquisition. Nothing is
executed, nothing is written back to evidence.

## 6. Question patterns

~15 questions across 8 tasks.

- **🟢 Case 001 is a proper pivot chain** and it is single-artifact throughout: build version and
  capture time (`windows.info`) → Adobe process path (`pslist`/`pstree`) → its parent → the
  parent's PID → DLLs outside `system32` (`dlllist`) → the KeyedEvent name (`handles`) → processes
  with an `MZ` header in injected memory (`malfind`). **Each answer comes from one named plugin**,
  which is our case rule exactly.
- **`windows.info` for the acquisition time** is a small, excellent habit: the first question of a
  memory investigation should establish *when the frame was taken*, and the room makes it the first
  question. Adopt it.
- **🔴 One question type we must NOT copy.** Case 002 asks *"From our current information, what
  malware is present on the system?"* — that is **threat-intelligence inference, not artifact
  analysis**, and it cannot be answered from a named artifact. It also invites students to name a
  family from a filename, which is precisely the finding/interpretation collapse D20 criterion 4
  penalises. **Our version asks what the artifact shows, then asks separately what it would take to
  attribute it.**
- **One question is genuinely well-formed in the opposite direction**: *"what plugin could be used
  to identify all files loaded from the malware working directory?"* — it tests tool selection
  rather than recall, which is what an exam with scenario questions actually needs.
- **Still no explicit "cannot be determined" answer** — eleventh room. Candidates here are
  unusually strong because the room states the limits itself:
  *"`pslist` shows no such process — does that prove it was not running?"* → **no** (§2.1) ·
  *"`malfind` flagged this RWE region — is it malicious?"* → **cannot be determined without the
  header check and a baseline** (§2.7) · *"`windows.ssdt` shows a hook — is it a rootkit?"* →
  **no** (§2.8, the room's own words).

## 7. Figures we would need to draw

The room is almost entirely terminal output; no conceptual diagrams. Three are needed:

| what is needed | our SVG spec (one line) |
|---|---|
| list-walking vs pool-scanning | one memory strip with an `_EPROCESS` chain drawn as linked boxes, **one box unlinked and floating free** — `pslist` traces the arrows and misses it, `psscan` sweeps the whole strip and finds it plus two false hits shaded grey; captioned "the diff is the hunt" |
| Volatility 3's three layers | a stack — raw image → **memory layers** (address translation) → **symbol tables** (structure interpretation) → **plugins** — with the symbol-table box annotated **"fetched from Microsoft's symbol server — pre-stage this for an offline lab"** (block D2) |
| what `malfind` actually looks for | a VAD region with two flags drawn as switches — **executable bit set** and **no mapped file on disk** — and beside it a legitimate JIT region with the same switches, captioned "same signature, different meaning" |

The third is the one that stops students reading `malfind` output as a verdict. Never their images
(D22).

## 8. Fit against our material

### ✅ Part 1's mapping is correct

Mapped to `S6` / `S6-10` + the Volatility homework track. Correct.

### Rows this strengthens

- **`S6-10`** *"Volatility 3 in the capstone — processes, network connections, injected code"*,
  15 min **[INVESTIGATION]**. The room covers all three named areas and supplies the plugin set,
  the anomaly heuristics and the evasion pairings. **Fully sourced.**
- **The Volatility homework track (Part 4)** — the room's plugin catalogue plus its "worth knowing"
  list is the natural spine for take-home work.
- **`S6-04`** network file carving — the `bulk_extractor`-on-a-memory-image pivot (§2.5) is a
  genuine addition: it gives `S6-04` a **host-side** route to network evidence.
- **`S2-03`** — the acquisition-tool and hypervisor-format tables, with room 10's corrections.

### Two things `S6-10` must do differently from the room

1. **Use `windows.malware.malfind`.** The room's name is deprecated past its removal date.
2. **State the false-positive rate on `psscan`, `netscan` and `malfind`.** The room names it for
   `psscan` only. All three are structure-scanning or heuristic plugins and all three generate
   leads rather than findings — which is the entire point of teaching them inside a course whose
   rubric grades findings-vs-interpretation.

### Minutes

`S6-10` is 15 min against the room's 60 — but `S6-10` is explicitly *"Volatility 3 **in the
capstone**"*, i.e. applied, not taught from scratch. The room's teaching content is the homework
track's job, and Part 4 already establishes that pattern. **No new rows. S6 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).

### Out of scope

`linux.info` is mentioned once in passing; macOS is mentioned only in the closing reading note.
Neither is taught. **No scope conflict** — the room is Windows throughout in practice.

## 9. Links

- Room: <https://tryhackme.com/room/volatilityessentials>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 6)
- Room's stated prerequisites: **Memory Analysis Introduction** (Priority 3, not yet extracted) and
  **Core Windows Processes** (not in this path — but a genuinely useful prerequisite, since every
  anomaly heuristic in §2 depends on knowing what normal looks like).
- Volatility 3: <https://github.com/volatilityfoundation/volatility3>
- The room again recommends ***The Art of Memory Forensics*** — same reference as room 10; worth
  listing once in `practice_platforms.md` (link and credit, never rehost — D22).
- Full memory-tool currency, including the `windows.malware.malfind` rename and the offline-symbols
  problem: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block D**

END OF NOTE.
