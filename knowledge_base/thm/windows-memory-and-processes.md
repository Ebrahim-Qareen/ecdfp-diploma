---
room: Windows Memory & Processes
url: https://tryhackme.com/room/windowsmemoryandprocs
module: Memory Analysis — **first of a three-room set** (Processes → User Activity → Network)
feeds: S6 — **`S6-10` Volatility 3 in the capstone (direct hit)** and **`S6-09` capstone shape**.
       Also `S1` (the MITRE-mapping discipline + the hashing defects) and the Volatility
       homework track (Part 4).
       **Carries three currency corrections that reach back into S5 — see §3.**
difficulty / time: Medium · 75 min · 9 tasks · Premium · 3,015 completions
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 9 tasks read in full. 0 sections NOT READ. Task 2 network map and Task 1 hero
              image viewed directly in Chrome (§7).
---

## 1. What the room teaches

Two halves that do not usually appear together.

**First**, the kernel structures — `_EPROCESS`, `_ETHREAD`, PEB, TEB — and, crucially, **which
Volatility plugin reads which field of which structure**. Twelve rooms in, this is the first one
that answers *"where does this number actually come from?"* instead of treating the tool as an
oracle. That mapping is the room's real contribution and it is exactly what our 6-box
"where it lives" box exists to force.

**Second**, a complete triage workflow on a 4-plus-GB Windows memory image: verify the hash →
`pslist` → **difference against a known-good baseline** → `pstree` to link the survivors →
`psscan`/`psxview` for hidden processes → `dlllist` for on-disk paths → `dumpfiles` to extract the
executables → assemble a kill chain.

Two things make it worth more than its question quality suggests:

1. **🟢 Baseline differencing.** The room teaches comparing a process list against a captured
   baseline with `comm`, and then — unprompted — **names its own false positives**: processes that
   simply were not running when the baseline was taken, and names truncated by the 15-byte
   `ImageFileName` field. A room that tells you why its own technique lies is rare.
2. **🟢 It admits what it could not determine.** Task 8 has a section headed
   **"Attack Phases Not Accounted For"**, which says of `updater.exe`: *"you can only speculate…
   An educated guess would be…"* — and leaves it unplaced. Twelve rooms in, **this is the first
   room that ships an unresolved artifact on purpose.** See §6; this is D7/D20 material.

Against that, the room carries **one wrong MITRE mapping, three deprecated plugin names, one wrong
structure size, and four internal inconsistencies in its own scenario.** All are listed below, and
most of them are more useful to us as teaching material than the room's correct parts.

## 2. Artifacts — one 6-box block each

### 2.1 `_EPROCESS` — the kernel's process object

- **What it is** — the kernel-mode structure that *is* the process, as far as Windows is concerned.
- **Where it lives** — kernel space, one per process; reachable by walking `ActiveProcessLinks` or
  by scanning for the structure signature.
- **What it proves** — PID (`UniqueProcessId`), parent PID (`InheritedFromUniqueProcessId`), short
  image name (`ImageFileName`), `CreateTime`, `ExitTime`, the thread list head, the handle table,
  the VAD root and the security token.
- **What it does NOT prove** — 🔴 **the full image name.** `ImageFileName` is a fixed
  **15-byte** field and in practice only **14 printable characters survive**. `fontdrvhost.exe`
  appears as `fontdrvhost.ex`; `windows-update.exe` appears as `windows-update`. Any conclusion
  drawn from a truncated name is a conclusion about a truncated name. It also does not prove the
  path — that comes from the PEB or `dlllist`, not from here.
- **How to parse it** — `windows.pslist` / `windows.psscan` / `windows.pstree` / `windows.getsids`
  / `windows.handles` / `windows.dlllist` / `windows.cmdline` / `windows.envars`, all of which the
  room correctly attributes to this structure.
- **Anti-forensics / false-positive caveat** — 🔴 `ActiveProcessLinks` is a *doubly-linked list a
  driver can edit*. DKOM unlinking removes the process from every list-walking plugin while the
  `_EPROCESS` itself remains in memory. That is the whole reason `psscan` exists.
  ⚠️ **The room's prose says this field "can only accommodate 16 bytes." That is wrong for
  Windows 7 and later** — see §3.

### 2.2 `_ETHREAD` — the kernel's thread object

- **What it is** — one per thread; linked back to its process through the `_EPROCESS`
  `ThreadListHead`.
- **Where it lives** — kernel space.
- **What it proves** — `Cid` (thread + process IDs), thread `CreateTime` and `ExitTime`,
  `StartAddress` (kernel entry point) and **`Win32StartAddress` (the user-mode entry point)**,
  `ThreadState` and `WaitReason`.
- **What it does NOT prove** — 🔴 **that the code at `Win32StartAddress` is what it claims to be.**
  A hollowed or injected thread has a perfectly ordinary-looking start address inside a region
  whose contents were replaced. The address tells you *where*, never *what*.
- **How to parse it** — `windows.threads` (the room lists `threads`, `ldrmodules`, `apihooks` and
  `malfind`; see §3 — one of those four does not exist in Volatility 3 at all).
- **Anti-forensics / false-positive caveat** — 🟢 the room supplies the single best thread
  heuristic in twelve rooms: **an active process with zero threads is suspicious, because every
  live process has at least one**; and **a process absent from `pslist` that still has live threads
  is suspicious in the opposite direction.** Both are cheap, both are checkable, both belong in
  `S6-10`.

### 2.3 PEB — the Process Environment Block

- **What it is** — the process's own view of itself, in **user space**.
- **Where it lives** — user-mode address space; `_EPROCESS.Peb` points to it, and the TEB carries a
  redundant pointer back to it.
- **What it proves** — `ImageBaseAddress`, the loader data `Ldr` (the DLL list), and
  `ProcessParameters` — which is where the **full command line, the image path and the environment
  variables** actually live.
- **What it does NOT prove** — 🔴🔴 **anything, if the process chose to lie.** The PEB is
  writable by the process that owns it. PEB masquerading — rewriting `ProcessParameters` so the
  command line and image path read as something benign — is a known technique with its own
  Volatility plugin (`windows.malware.pebmasquerade`). **A command line recovered from the PEB is
  the process's claim about itself, not the kernel's record of it.** The room never says this.
- **How to parse it** — `windows.cmdline`, `windows.envars`, `windows.dlllist`,
  `windows.malware.ldrmodules`.
- **Anti-forensics / false-positive caveat** — 🔴 kernel-side (`_EPROCESS`) and user-side (PEB)
  answers to *"what is this process?"* can disagree, and **the disagreement is the finding**.
  Teach the two as a pair, exactly as `pslist`/`psscan` are taught as a pair.

### 2.4 TEB — the Thread Environment Block

- **What it is** — per-thread user-space state.
- **Where it lives** — user-mode address space; `_ETHREAD.Teb` points to it.
- **What it proves** — `ClientId`, `ThreadLocalStoragePointer`, `LastErrorValue`, and the thread's
  **`StackBase`/`StackLimit`** — the bounds that let you carve a single thread's stack out of a
  full dump.
- **What it does NOT prove** — 🔴 stack bounds give you the region, not its meaning; and a thread
  running injected code has an entirely normal TEB.
- **How to parse it** — `windows.threads`, `windows.malware.malfind`.
- **Anti-forensics / false-positive caveat** — the TEB is user-writable like the PEB; same rule.

### 2.5 Parent–child lineage (`windows.pstree`)

- **What it is** — the process list re-drawn as a hierarchy from PID/PPID.
- **Where it lives** — derived; `InheritedFromUniqueProcessId` in each `_EPROCESS`.
- **What it proves** — **who launched what.** In this image it produces the whole chain in one
  view: `explorer.exe` → `WINWORD.EXE` → `pdfupdater.exe` → `windows-update` → `updater.exe` →
  `cmd.exe` → `powershell.exe`.
- **What it does NOT prove** — 🔴🔴 **that the parent still exists, or ever did what it appears to
  have done.** PPID is a *number copied at creation*; it is not a live reference. If the parent
  exits, the PID can be **reused** and the tree will re-root the child under an unrelated process.
  **Parent PID spoofing** (`PROC_THREAD_ATTRIBUTE_PARENT_PROCESS`) lets a process choose its own
  parent outright. A tree is a hypothesis about lineage, not a record of it.
- **How to parse it** — `windows.pstree`; the room's `cut -d$'\t' -f1,2,3 processtree.txt` to strip
  it down to PID/PPID/name is a good habit worth copying.
- **Anti-forensics / false-positive caveat** — 🟢 **corroborate lineage with time.** The room's own
  table does this without naming it: every child's `CreateTime` is at or after its parent's, and
  the 92-second gap between `windows-update.exe` (07:13:05) and `updater.exe` (07:13:56) is itself
  evidence. **A child older than its parent means PID reuse or spoofing.** Make that check
  explicit in our material; the room leaves it implicit.

### 2.6 Cross-view process detection (`windows.malware.psxview`)

- **What it is** — five independent ways of finding a process, run at once and cross-tabulated:
  `pslist`, `psscan`, `thrdscan`, `csrss`, plus the exit time.
- **Where it lives** — five different sources: the active-process linked list, raw structure
  scanning, thread objects, the CSRSS handle table.
- **What it proves** — 🟢 **disagreement between detection methods.** A process visible to four
  techniques and invisible to the fifth is where you look.
- **What it does NOT prove** — 🔴 **that a `False` under `pslist` means hiding.** The room's own
  run returns ten `pslist=False` rows and every one is benign — `svchost.exe`, `sihost.exe`,
  `ctfmon.exe`, `taskhostw.exe`, `vmtoolsd.exe` — because terminated processes legitimately leave
  scannable structures behind. **`psxview` produces leads at a fairly high false-positive rate;
  it does not produce findings.** To the room's credit it says so: *"you can never be 100% sure."*
- **How to parse it** — `windows.malware.psxview`; the room's
  `awk 'NR==3 || $4 == "False"' psxview.txt` filter is a neat way to read only the anomalies.
  There is also a `--physical-offsets` flag the room never mentions, which swaps column 1 to
  `Offset(Physical)`.
- **Anti-forensics / false-positive caveat** — 🔴 **the room's plugin name is deprecated.** It runs
  `windows.psxview`; the canonical name is **`windows.malware.psxview`** and the old path is a
  rename shim with `removal_date="2026-06-07"` — **already past**. See §3.

### 2.7 Module path and load time (`windows.dlllist`)

- **What it is** — the main executable and every loaded DLL, with **full on-disk path** and load
  timestamp.
- **Where it lives** — the PEB loader data (`Ldr`).
- **What it proves** — 🟢 **this is where the path finally appears**, and the path is what turns
  three innocuous-sounding names into an incident: `C:\Users\operator\pdfupdater.exe`,
  `C:\Users\operator\Downloads\updater.exe`, and
  `…\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\windows-update.exe`.
- **What it does NOT prove** — 🔴 the path is read from the **PEB**, so §2.3's caveat applies in
  full: a masquerading process reports a path of its choosing. Corroborate against the VAD
  (`windows.vadinfo`) or the file object before treating a path as fact.
- **How to parse it** — `windows.dlllist --pid <PID>`; columns `PID Process Base Size Name Path
  LoadCount LoadTime File output`. Also accepts `--offset`, `--base`, `--name`, `--ignore-case`,
  `--dump`.
- **Anti-forensics / false-positive caveat** — ⚠️ a DLL **outside `C:\Windows\System32\`** is the
  room 11 heuristic and it belongs here too; it is a lead, and signed-but-relocated Microsoft DLLs
  and legitimate side-by-side assemblies both trip it.

### 2.8 Dumped section objects (`windows.dumpfiles`)

- **What it is** — the file-backed memory of a process, written out as files.
- **Where it lives** — `_FILE_OBJECT` section pointers reachable from the process handle table.
- **What it proves** — 🟢 **the actual bytes**: here, two macro-enabled Word documents
  (`cv-resume-test.docm`, `Normal.dotm`) recovered from `WINWORD.EXE`, and the PE images of all
  three suspicious executables. This is the step that turns "suspicious name" into "artifact you
  can hand a malware analyst".
- **What it does NOT prove** — 🔴🔴 **that what you dumped is complete or executable.** Memory
  holds only the **resident** pages; paged-out sections are simply absent, so a dumped PE is
  routinely a partial file. It also does not prove maliciousness — `Normal.dotm` is the default
  Word template and is present in every Word process on earth. **Two `.docm`/`.dotm` files came
  out; exactly one of them is interesting, and the room never distinguishes them.**
- **How to parse it** — `windows.dumpfiles --pid <PID>` (also `--virtaddr`, `--physaddr`,
  `--filter`, `--ignore-case`). Output goes to the **current working directory** by default;
  the global `-o/--output-dir` overrides it and is **not required**. Filenames are
  `file.<file_obj_offset>.<memory_obj_offset>.<CacheType>.<basename>.<ext>` where the cache type
  and extension pair up:

  | cache type | extension | contents |
  |---|---|---|
  | `ImageSectionObject` | `.img` | mapped executable image — `.exe`, `.dll`, injected PE |
  | `DataSectionObject` | `.dat` | mapped data — configs, documents, unpacked payloads |
  | `SharedCacheMap` | `.vacb` | cached file data from the Windows cache manager |

- **Anti-forensics / false-positive caveat** — 🔴 **`.img` files are live malware with the
  extension filed off.** See §5 — the room dumps them into the analyst's home directory with no
  containment instruction whatsoever. Also: the room tells students to identify types with `file`
  because *"all the dumped files have the extension `.img` appended"* — that is only true of the
  `ImageSectionObject` set, and the advice to trust `file` over the extension is right for the
  wrong reason.

## 3. Tools and commands

| plugin / command | as the room writes it | what it gives |
|---|---|---|
| hash check | `md5sum <image> > newhash.txt` then `diff acquisitionhash.txt newhash.txt` | integrity verification — **see the defect below** |
| `windows.pslist` | `vol3 -f <image> windows.pslist > pslist.txt` | active processes |
| `windows.pstree` | `vol3 -f <image> windows.pstree > processtree.txt` | parent–child hierarchy |
| `windows.psscan` | `vol3 -f <image> windows.psscan > psscan.txt` | all process objects incl. terminated/unlinked |
| **`windows.malware.psxview`** | `vol3 -f <image> windows.psxview > psxview.txt` ⚠️ deprecated name | five-technique cross-view |
| `windows.dlllist` | `vol3 -f <image> windows.dlllist --pid <PID> > <PID>_dlllist.txt` | paths + load times |
| `windows.dumpfiles` | `vol3 -f ../<image> windows.dumpfiles --pid <PID>` | extract file-backed memory |

Supporting shell the room actually teaches — all of it worth keeping:

| command | purpose |
|---|---|
| `awk 'NR>3{print $2}' baseline.txt \| sort \| uniq > baseline_procs.txt` | strip a Task Manager export to a sorted unique name list |
| `awk 'NR>3{print $3}' pslist.txt \| sort \| uniq > current_procs.txt` | same for Volatility output (**note the different column index** — the two files have different layouts) |
| `comm -13 a.txt b.txt` | lines unique to **b** — "what is running now that was not in the baseline" |
| `comm -23 a.txt b.txt` | lines unique to **a** — "what `psscan` found that `pslist` missed" |
| `awk 'NR==3 \|\| $4=="False"' psxview.txt` | keep the header, show only rows failing the `pslist` test |
| `cut -d$'\t' -f1,2,3 processtree.txt` | reduce the tree to PID / PPID / name |
| `ls <dir> \| grep -E ".docm\|.dotm" -i` | filter a dump directory by document type |
| `file <dumped>` | identify a dumped file by content, not extension |
| `strings <dumped>` | first-pass IOC sweep of an extracted binary |

The alias the room's VM ships: `vol3` = `python3 vol.py`.

### CURRENCY CHECK — verified 2026-08-28, feeds `_TOOL_CURRENCY_2026-08-28.md` block D

| # | item | result |
|---|---|---|
| 1 | Volatility 3 release | ✅ **2.28.0, released 30 Apr 2026** is current. ⚠️ Do **not** cite 2.28.2 — that is the `develop` branch version, there is no such release tag, and ReadTheDocs `/en/latest/` shows it. Pin `/en/stable/`. |
| 2 | 🔴 **room runs 2.26.2** (25 Sep 2025) | Two minor versions behind — same finding as room 11. Both memory rooms are stale by the same amount. |
| 3 | 🔴 **`windows.psxview` is a deprecated alias** | Canonical name is **`windows.malware.psxview`** (`plugins/windows/malware/psxview.py`). The old path is a `PluginRenameClass` shim with `removal_date="2026-06-07"` — **already passed**. Columns are unchanged: `Offset(Virtual) Name PID pslist psscan thrdscan csrss Exit Time`. Undocumented extra flag: `--physical-offsets`. |
| 4 | 🔴 **`ldrmodules` is also deprecated** | Room's Task 3 lists it as a plugin. Canonical: **`windows.malware.ldrmodules`**, same `removal_date="2026-06-07"`. |
| 5 | 🔴🔴 **`apihooks` does not exist in Volatility 3 at all** | The room lists it in Task 3 as one of the plugins reading `_ETHREAD`. It is **Volatility 2 only and was never ported** — there is no `apihooks.py` anywhere under `plugins/windows/`, and no entry in the docs index. Open request: issue #686. **A student who types it gets an unknown-plugin error and will assume they broke something.** Our slides must not repeat this list unedited. |
| 6 | ✅ the other nine plugin names in Task 3 | `pslist`, `pstree`, `psscan`, `getsids`, `handles`, `dlllist`, `cmdline`, `envars`, `threads` all exist under `windows.*` and none is deprecated. `malfind` → `windows.malware.malfind` (already recorded, room 11). |
| 7 | 🔴🔴 **NEW — a second deprecation wave lands 25 Sep 2026** | `windows.amcache`, `windows.cachedump`, `windows.hashdump`, `windows.lsadump`, `windows.scheduled_tasks` → **`windows.registry.*`**, `removal_date="2026-09-25"`. **That is four weeks from now and it hits the S5 registry/account material, not this room.** Verified on `windows/amcache.py`: `replacement_class=amcache.Amcache, removal_date="2026-09-25"`. **Action: check rooms 2/3/4 notes and any S5 slide that names these plugins.** |
| 8 | ⚠️ deprecation shims still ship | Both 2026-06-07 shims are present in the **v2.28.0 tag** and on `develop`. So old names still run today and emit a `FutureWarning`. They die at the next release. **Teach the new names; mention the warning so students recognise it.** |
| 9 | ✅ `windows.dumpfiles` flags | `--pid`, `--virtaddr`, `--physaddr`, `--filter`, `--ignore-case`. **`-o` is a global CLI option, not a plugin flag, and is optional** — it defaults to `os.getcwd()`. The room's `mkdir 5252 && cd 5252` is therefore a legitimate way to isolate output, just an implicit one. |
| 10 | ⚠️ dumpfiles filename convention | The room implies `ImageSectionObject`/`DataSectionObject`/`SharedCacheMap` are prefixes. They are not — every name begins `file.` and the cache type is the **fourth** dot-separated field. Extensions pair strictly: `.img` / `.dat` / `.vacb`. Corrected in §2.8. |
| 11 | ✅ `windows.dlllist` | Current; still emits `Path` and `LoadTime`. Full column set in §2.7. |
| 12 | 🔴 **`_EPROCESS.ImageFileName` is 15 bytes, not 16** | The room's own code block says `UCHAR ImageFileName[15]` — correct. Its prose says *"this field can only accommodate 16 bytes"* — **wrong for Windows 7 and later.** It was `[16]` up to and including Vista and has been `[15]` since 6.1. Sources: Vergilius (Win7 SP1 and Win11 24H2 both `[15]`), Geoff Chappell (`0x10` for 3.50–6.0, `0x0F` for 6.1+), NirSoft (Vista `[16]`). **In practice 14 printable characters survive** — every truncation in the room's own output (`fontdrvhost.ex`, `smartscreen.ex`, `vm3dservice.ex`, `windows-update`) is exactly 14. State it as: *15-byte field, 14 characters in practice.* |
| 13 | 🔴🔴 **the room's MITRE mapping for Startup-folder persistence is wrong** | It calls `…\Start Menu\Programs\Startup\windows-update.exe` **"Boot or Logon Initialization Scripts: Startup Items"**. That is **T1037.005, and it is macOS-only** — the deprecated `/Library/StartupItems` mechanism. The correct mapping is **T1547.001 — Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder**, whose description names this exact path verbatim. The two parents are near-twins and are the classic ATT&CK confusion: **T1037 Initialization Scripts** vs **T1547 Autostart Execution**. Validated against **ATT&CK Enterprise v19.2** (v19 released 2026-04-28; v19.2 point release 2026-08-06). |
| 14 | ✅ the room's other MITRE IDs | **T1059.005** Visual Basic ✅ · **T1059.007** JavaScript ✅ (but see below) · **T1566** Phishing ✅ · **TA0011** Command and Control ✅. |
| 15 | ⚠️ T1059.007 justification overreaches | The ID and name are right, but the current T1059.007 page covers JScript, JXA and Node.js and **does not mention PDF-embedded JavaScript**. There is no PDF-specific technique in ATT&CK. Phrase it as *"JavaScript execution, whatever the host container, maps to T1059.007"* rather than *"ATT&CK says JS-in-PDF is T1059.007."* |
| 16 | ➕ IDs the room should have used and did not | **T1566.001** Phishing: Spearphishing Attachment (the `.docm` CV) · **T1204.002** User Execution: Malicious File (the victim double-clicking it) · **T1055.001** Process Injection: **Dynamic-link Library Injection** (the room says "DLL injection" — that is the colloquial name) · **T1055.012** Process Hollowing. The honest chain for this incident is **T1566.001 → T1204.002 → T1059.005 → T1547.001**. |

**Net: the room is a good workflow wrapped around a plugin list that will not run as printed and a
persistence mapping that points at the wrong operating system.** Both are fixable in one slide, and
fixing them in front of students is better teaching than never showing the error.

## 4. Evidence used

- **`THM-WIN-001_071528_07052025.mem`** — full memory dump of a Windows 10 22H2 (10.0.19045) host,
  on an Ubuntu Desktop analysis VM at `/home/ubuntu`. MD5 supplied as
  `78535fc49ab54fed57919255709ae650`.
- A **baseline** process export at `~/baseline/baseline.txt`, taken from Task Manager.
- **Not downloadable. No licence offered. Not reusable.** Nothing to flag for `ecdfp-evidence`.

### 🔴 Four internal inconsistencies in the room's own evidence documentation

These are not nitpicks — the room is teaching chain of custody and its own paperwork does not
survive a read. **Together they make the best "audit this case file" exercise we have found.**

| # | the room says | but |
|---|---|---|
| 1 | *"On May 5th, 2025, at 07:30 CET"* the incident was escalated | every timestamp in every artifact is **2025-05-07**, and the filename encodes `07052025`. **The narrative date and the evidence date disagree by two days.** |
| 2 | dump name is **`THM-WIN-001_071528_07052025.dmp`** | every command in every task operates on **`.mem`**. The file named in the case record is not the file that was analysed. |
| 3 | filename timestamp is **`071528`** (07:15:28) | the scenario says the dump was taken at **07:45 CET**, and the malicious chain runs 07:13:04 → 07:14:39. **07:15:28 is consistent with the artifacts and inconsistent with the narrative.** |
| 4 | host is **`WIN-001`** on the USER LAN | the network map's USER LAN contains **WIN-012 through WIN-019** and nothing else. **The compromised host does not appear on the network diagram of the network it was compromised on.** |

🟢 **Use this.** Hand students the scenario page and the artifact tables and ask them to list every
place the case file contradicts the evidence. It is a pure D7 exercise — findings versus the story
someone wrote around them — and it needs no lab machine, no image and no tooling. Candidate for
`S1` or as the warm-up to `S6-09`.

### 🔴 The hash verification does not verify anything

Three separate defects stacked:

1. **`diff acquisitionhash.txt newhash.txt` compares `md5sum` output files, and `md5sum` prints
   `<hash>  <filename>`.** The two files were produced from different filenames (`.dmp` at
   acquisition, `.mem` at analysis — defect 2 above), so **the diff reports a difference even when
   the hashes match.** The correct forms are `md5sum -c acquisitionhash.txt`, or comparing only the
   first field.
2. **The room tells students not to run it**: *"You don't need to enter the command. We have
   already pre-calculated the hash for you."* So no student in this room ever verifies an image.
   The one habit that must be muscle memory is the one step they are told to skip.
3. **MD5 only.** No SHA-256 anywhere, and no acknowledgement that MD5 is collision-broken and
   retained only for legacy tool compatibility. Our **R9** requires both.

**Our version:** students run the hash themselves, on both algorithms, with `sha256sum -c`, and are
shown what a genuine mismatch looks like — because being handed a clean image and told the hash is
fine teaches nothing about what to do when it is not.

### The network map (viewed in Chrome, Task 2)

Not reusable as an image (D22) but the **topology shape** is a good reference for our own
carry-through incident (D19):

```
INTERNET ──(10.10.8.6)── FW-01 ─┬─ DMZ Internal 192.168.10.0/24
                                │     WEB-01 192.168.10.1 · DNS-01 192.168.10.2
                                ├─ USER LAN   192.168.1.0/24
                                │     WIN-012 .192 … WIN-019 .199  (8 workstations)
                                └─ SERVER LAN 192.168.0.0/24
                                      FS-01 .30 (Linux) · AD-01 .31 · DB-01 .32
```

Three segments behind one firewall, a Linux file server beside a Windows DC and DB — a small,
legible shape a student can hold in their head. **We draw our own with our own hostnames**, and
ours will include the host that was actually compromised.

## 5. Lab design worth reusing

1. **🟢🟢 The running findings table.** Every task ends with **"Analysis Notes and Next Steps"** and
   a table that **grows by one column each time**: Task 4 gives name/PID/timestamp; Task 5 adds
   PPID; Task 7 adds path and dumped files; Task 8 restates the whole thing as the kill chain. The
   student watches one artifact record accumulate across a whole investigation. **This is the best
   single structural idea in twelve rooms and it is exactly our case-notes discipline made
   visible.** Adopt it wholesale for `S6-09` and the carry-through incident.
2. **🟢🟢 Baseline differencing, with its own false positives named.** `comm -13 baseline current`
   reduces ~90 processes to 14, and the room then tells you **why some of the 14 are noise**:
   processes not running when the baseline was captured, and names truncated by the 15-byte field.
   It even tells you where to get a legitimate-updater shortlist (the task scheduler).
   **A triage technique taught together with its error modes.** Rare, and directly reusable.
3. **🟢 Structure → plugin mapping.** Task 3 lists, per structure, which plugins read it. Turning a
   tool into a set of field reads is the difference between a student who runs `pslist` and one who
   knows `pslist` cannot show them a path. **Build our EPROCESS/ETHREAD/PEB/TEB figure around this
   mapping** (§7).
4. **🟢 The `CreateProcess()` sequence as forensics, not OS theory.** Six steps ending in *"the
   process is created but is still suspended… the primary thread is resumed."* That suspended
   window is where hollowing happens; the room never says so, and one sentence from us turns a dry
   sequence into the reason process hollowing works.
5. **🟢 Named typosquat examples.** `scvhost.exe` / `explorere.exe` / `lsasss.exe`, and the
   masquerade set `dockerupdater.exe` / `defenderAV.exe` / `pdfupdateservice.exe`. Concrete,
   memorable, and the incident's own three names follow the same pattern.
6. **⚠️ Weak but salvageable: the `svchost.exe` verification checklist** (image path · loaded DLLs ·
   active threads · zero threads · exit time · dump and analyse). Good list, but the room says
   *"you will explore some of these checks later on"* and then does not. **We finish it.**

### 🔴 Safety defect — dumped malware with no containment

`windows.dumpfiles --pid 3392` writes a live second-stage PE (`pdfupdater.exe.img`) into the
analyst's home directory on a networked VM, and the room follows with `strings` and `file`. There
is **no instruction to disarm the extension, no isolated directory outside the user profile, no
mention of AV/EDR quarantining the dump mid-write, and no warning against double-clicking it.**

To the room's credit, Task 8's *"collect these artifacts, hash them, and then pass them to the
threat hunter or malware analyst"* is the right closing instruction. But hashing comes after
extraction, and nothing covers the interval.

**This is the fourth safety defect across twelve rooms, and it is the first in the memory block**
(rooms 10 and 11 were clean). It joins the S4 set:

| room | defect |
|---|---|
| 6 · FAT32 | paste-recovered PowerShell into a live shell |
| 8 · File Carving | `binwalk -e` with no isolation (CVE-2022-4510) |
| 9 · MBR/GPT | edit and save the evidence image in place |
| **12 · Memory & Processes** | **dump live malware to the home directory, no containment** |

All four are *"the instruction is technically correct and operationally unsafe"* — which is the
exact shape of the `S1` handling exercise. **Four is enough to build the exercise; stop collecting
and start writing it.**

## 6. Question patterns

**~11 questions across 9 tasks**, and the quality splits hard.

**🔴 Six of them are `grep`.** *"What is the PID of the csrss.exe process that has 12 threads?
You can use the pslist.txt file to find the answer."* · *"What is the Offset(V) of the process with
PID 5672?"* · *"What is the number of processes that have 0 Threads?"* · *"What is the PPID of
services.exe (PID 664)?"* · *"What is the ImageFileName of the process with PID 7788?"* The task
literally names the file to look in. **These test file navigation, not analysis**, and a student
can answer every one without understanding a single thing the room taught. Do not copy this shape.

**🟢 Two are genuinely good.**
- *"What is the path of the process with PID 7788?"* followed by *"Dump the process with PID 7788.
  What is the name of the dumped file that represents the executable?"* — **the second requires
  running the tool, choosing the right one of three cache types, and knowing that
  `ImageSectionObject`/`.img` is the executable and `DataSectionObject`/`.dat` is not.** That is
  procedure plus comprehension, and it has one defensible answer. This is our target shape.

**⚠️ Two are structure recall** (*"what field keeps track of all active processes?"* →
`ActiveProcessLinks`; *"what field stores the PID?"* → `UniqueProcessId`). Fine as a knowledge
check; not an investigation.

**⚠️ One is a lookup on the wrong source** — *"What is the ID assigned to the MITRE Tactic Command
and Control?"* (`TA0011`). The answer is correct, but it is a documentation lookup dressed as
analysis, and it sits three paragraphs below the room's **incorrect** T1037.005 mapping.

### 🟢🟢 The finding that matters: the room ships an unresolved artifact

Twelve rooms in, **this is the first room whose prose refuses to over-conclude**, and it does so
consistently:

> *"Now, you can only speculate about the attacker's technique…"*
> *"This needs to be confirmed by analyzing the user's activity on the system."*
> *"…likely downloads and launches a second-stage malware… Further analysis of the macro files
> should confirm this."*
> *"**Attack Phases Not Accounted For** — there is still one executable that you couldn't place in
> any of the above phases. For now, you can only speculate about what the `updater.exe` process
> does. **An educated guess would be**…"*

That last section is the thing. The room reaches the end of its investigation with an artifact it
**cannot classify**, says so under its own heading, offers four candidate tactics, and **does not
pick one**. It is the closest any room in this path comes to a "this cannot be determined"
position, and it arrives in the prose rather than the questions.

**🔴 But there is still no question with that answer** — twelve for twelve. The room writes the
right conclusion and then never asks the student to reach it. **That gap is our differentiator,
stated precisely:** our version turns *"Attack Phases Not Accounted For"* into a graded question —
*"What tactic does `updater.exe` serve? State your answer or state what evidence you would need."*
— and D20 criterion 4 rewards the student who declines to guess.

## 7. Figures we would need to draw

Figures actually present in the room, viewed in Chrome:

| # | task | what it is | reusable? |
|---|---|---|---|
| 1 | T1 | a stylised Volatility "machine" on a conveyor turning folders into binary | **decorative only.** Ignore. |
| 2 | T2 | TryHatMe company logo | irrelevant |
| 3 | T2 | **the network map** (transcribed in §4) | **concept yes, image no** (D22) |

Everything else in the room is terminal output or an ASCII tree. **The structural content of Task 3
is delivered entirely in prose and C structs with no diagram at all** — which is where our biggest
win is.

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **the four structures and who reads what** | a vertical split — **kernel space** above (`_EPROCESS` box, `_ETHREAD` box, arrow `ThreadListHead` between them) and **user space** below (PEB box, TEB box, dashed arrows `Peb` and `Teb` crossing the boundary, plus TEB's redundant back-pointer to PEB); each box lists its 4–5 forensically useful fields, and **a plugin name is anchored to the specific field it reads**; the kernel/user boundary drawn as the trust line, captioned *"below the line, the process describes itself"* | **highest** |
| 2 | **`CreateProcess()` and the hollowing window** | the six steps as a horizontal sequence, with step 5 (*"created but still suspended"*) drawn as a **gap** and annotated *"this is the window process hollowing writes into"*; step 6 resumes | **high** |
| 3 | **three views of one process list** | three overlapping sets — `pslist` (list walk), `psscan` (structure scan), `thrdscan`/`csrss` — with one process in the scan-only intersection labelled *unlinked → investigate* and **ten processes also in the scan-only region shaded grey and labelled *terminated → benign***, captioned *"psxview produces leads, not findings"* | **high** — this is the D7 figure for memory |
| 4 | **the incident's process tree** | the `WINWORD.EXE → pdfupdater → windows-update → updater → cmd → powershell` chain as a tree, each node carrying **path + timestamp**, with the two nodes whose *path* is the tell (`C:\Users\operator\…`, `…\Startup\…`) accented, and the 92-second gap between `windows-update` and `updater` marked on the edge | medium |
| 5 | **baseline differencing** | two columns of process names funnelling through a `comm -13` gate into a shortlist of 14, then a second gate labelled *"false positives: not-running-at-baseline · name truncated at 14 chars"* reducing to 3 | medium |
| 6 | **the MITRE correction** | side-by-side: **T1037 Boot or Logon Initialization Scripts → .005 Startup Items 🍎 macOS** vs **T1547 Boot or Logon Autostart Execution → .001 Registry Run Keys / Startup Folder 🪟 Windows**, with the Startup path under the correct one; captioned *"two techniques, near-identical names, different operating systems"* | **high** — reusable far beyond this room |

Figure 1 is the one that changes how students read every subsequent memory plugin. Figure 6 is the
one they will still be using in five years. Never their images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct

Mapped to `S6` / `S6-10`. Correct — and this is the first of the three-room memory set, so rooms 13
(User Activity) and 14 (Network) will land in the same place.

### Rows this strengthens

- **`S6-10`** *"Volatility 3 in the capstone — processes, network connections, injected code"*,
  15 min **[INVESTIGATION]**. Rooms 11 and 12 together now over-supply this row: room 11 gives the
  plugin catalogue and the evasion pairings, room 12 gives the **workflow order** and the
  structure→plugin mapping. **Fully sourced, twice over.**
- **`S6-09`** capstone. The running findings table (§5.1) is the **format** our capstone worksheet
  should take, and the four documentation inconsistencies (§4) are the **audit exercise** that
  should precede it.
- **`S1`** — two contributions, both unplanned: the evidence-documentation audit (§4) and the
  fourth safety defect completing the handling exercise (§5).
- **Volatility homework track (Part 4)** — the shell pipeline in §3 (`awk`/`comm`/`cut`/`file`/
  `strings`) is a self-contained take-home that needs no memory image at all; students can practise
  the differencing method on `ps` output from their own machine.

### Three things `S6-10` must do differently from the room

1. **Use `windows.malware.psxview` and `windows.malware.ldrmodules`**, and **delete `apihooks`
   from the plugin list entirely** — it does not exist in v3.
2. **Map Startup-folder persistence to T1547.001**, and use the room's error as the worked example
   of why you check ATT&CK's platform field before citing a sub-technique.
3. **Say that PPID is a copied number, not a live reference.** The room builds its entire
   conclusion on the process tree and never mentions PID reuse or parent spoofing. A student who
   learns lineage from this room will over-trust it.

### 🔴 Action item outside this room

Currency finding **#7** — the `windows.registry.*` rename wave with `removal_date="2026-09-25"` —
does **not** affect this room but does affect **`windows.amcache`, `windows.hashdump`,
`windows.lsadump`, `windows.cachedump`, `windows.scheduled_tasks`**. Those are S5 plugins.
**✅ CHECKED 2026-08-28 — clean.** A grep across all twelve room notes returns **zero** hits
outside this file: the S5 rooms teach the registry through **Registry Explorer, RECmd, RegRipper
and KAPE**, never through Volatility plugins, so no existing note or S5 slide names any of the five.
**No back-propagation needed.** Re-check only if S5 later gains a memory-derived registry step.

### Minutes

`S6-10` is 15 min against the room's 75. As with room 11, `S6-10` is *applied* Volatility inside the
capstone, not a from-scratch teaching row; the workflow content belongs to `S6-09` (which already
exists) and the homework track. The structure figure (§7 #1) is a **slide**, not a new row.

**No new rows. S6 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).

### Out of scope

Malware analysis proper — the room correctly stops at *"hand it to the malware analyst"* every
time. Macro/OLE analysis of the `.docm` is deferred to a later room. Network artifacts are deferred
to room 14. **No scope conflict.**

### Still unresolved

**Browser forensics** has no `DECISIONS.md` row — neither taught nor declined. Room 12 touches it
only in passing (eight `msedge.exe` children under `explorer.exe` in the process tree, never
examined). **Twelfth room, still open.**

## 9. Links

- Room: <https://tryhackme.com/room/windowsmemoryandprocs>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations>
- Room's stated prerequisites: **Volatility** (= Volatility Essentials, room 11 — extracted) and
  the **Windows Fundamentals** module (not in this path).
- Next two in the set: **Windows Memory & User Activity** and **Windows Memory & Network** —
  rooms 13 and 14. Same scenario, same image, same host. **Extract them in order; the findings
  table carries forward.**
- Volatility 3: <https://github.com/volatilityfoundation/volatility3> — docs at
  <https://volatility3.readthedocs.io/en/stable/> (**use `/stable/`, not `/latest/`**)
- ATT&CK: T1547.001 <https://attack.mitre.org/techniques/T1547/001/> ·
  T1037.005 <https://attack.mitre.org/techniques/T1037/005/> (the macOS one the room cited) ·
  T1566.001 <https://attack.mitre.org/techniques/T1566/001/> ·
  T1204.002 <https://attack.mitre.org/techniques/T1204/002/> ·
  T1055.001 / T1055.012 <https://attack.mitre.org/techniques/T1055/>
- `_EPROCESS` field reference: <https://vergiliusproject.com/kernels/x64/windows-11/24h2/_EPROCESS>
  and Geoff Chappell's `EPROCESS` study (version-by-version field sizes)
- Full memory-tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block D**
