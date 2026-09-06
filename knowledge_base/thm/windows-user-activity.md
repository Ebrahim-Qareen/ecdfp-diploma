---
room: Windows User Activity Analysis
url: https://tryhackme.com/room/windowsuseractivity
module: Windows Endpoint Investigation (Section 3 of Advanced Endpoint Investigations)
feeds: S5 — `S5-04` shellbags · `S5-07` LNK/jumplists · enriches `S5-01` registry structure.
       Also exposes a large gap: six user-activity registry keys with no row in our map.
difficulty / time: Medium · 60 min · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

Where Windows records what a *user did* — as opposed to what *ran* (room 1) or what *accounts
exist* (room 2). Eleven artifacts across three families: user-activity registry keys, ShellBags,
and the Recent/JumpList shortcut stores.

The strongest room of the three so far, and the closest to eCDFP's actual centre. Its case is an
**insider**, not an intruder: a departing employee accessed documents over a weekend, ran tools
from a network share, and wiped traces. That framing forces every artifact to answer *intent*
questions rather than *how did they get in* questions.

Its unifying claim, stated plainly at the end: Windows keeps these records to improve user
experience, not for forensics — the evidentiary value is a side effect. That is a good line to
teach with.

## 2. Artifacts — one 6-box block each

### 2.1 Registry hive files and their mapped keys

- **What it is** — the on-disk files that make up the registry.
- **Where it lives** — `%SystemRoot%\System32\config` for the machine hives, with per-user hives
  in the profile. The room's mapping table:

  | hive file | mapped key | holds |
  |---|---|---|
  | `SAM` | `HKLM\SAM` | local account and security policy data |
  | `SECURITY` | `HKLM\SECURITY` | authentication and permissions config |
  | `SYSTEM` | `HKLM\SYSTEM` | hardware, drivers, startup |
  | `SOFTWARE` | `HKLM\SOFTWARE` | installed software, system-wide settings |
  | `DEFAULT` | `HKU\.DEFAULT` | template for new user profiles |
  | `NTUSER.DAT` | `HKCU` | per-user settings — **`%USERPROFILE%\NTUSER.dat`** |
  | `USRCLASS.DAT` | `HKCU\Software\Classes` | per-user class data — **`%USERPROFILE%\AppData\Local\Microsoft\Windows\UsrClass.dat`** |

- **What it proves** — where every other registry artifact in this note physically lives, and
  which file you must acquire to get it. `HKCU` is not a file; `NTUSER.DAT` is.
- **What it does NOT prove** — nothing on its own. This is the map, not the evidence.
- **How to parse it** — `regedit` (Win+R) for the live system; **Registry Explorer** for offline
  *and* live hive inspection. The room runs Registry Explorer as administrator and notes a 1–2
  minute load.
- **Anti-forensics / false-positive caveat** — see the transaction-log block below; a hive read
  without its logs can be stale.

### 2.2 Dirty hives and transaction logs

- **What it is** — a hive is "dirty" when it was not closed cleanly; transaction logs hold the
  changes not yet folded in.
- **Where it lives** — alongside the hives in `C:\Windows\System32\config`, named
  `SYSTEM.LOG1`, `SYSTEM.LOG2`, and so on. **They are hidden** — the room uses `dir /a` to reveal
  them.
- **What it proves** — that recent registry changes may exist *outside* the hive file you
  acquired. Windows uses the logs to roll back or replay after an unclean shutdown.
- **What it does NOT prove** — the logs are not an audit trail of who changed what. They are a
  crash-consistency mechanism, not a history you can attribute.
- **How to parse it** — ⚠️ **the room never says.** It teaches that dirty hives matter, that the
  logs must be carried alongside the hive "for an accurate investigation", and then stops.
  **See §3 — the tool is `RLA`, and the room does not name it.**
- **Anti-forensics / false-positive caveat** — this *is* the caveat, and it is the most important
  acquisition lesson in the room: **acquire the `.LOG1`/`.LOG2` files with every hive.** A hive
  parsed without its pending transactions can show an investigator a value that has already been
  superseded — a wrong answer that looks exactly like a right one.

### 2.3 TypedPaths

- **What it is** — paths typed into the File Explorer address bar or the Run dialogue.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths` (in `NTUSER.DAT`)
- **What it proves** — that a user typed a specific path, which reveals what they were *looking
  for* rather than what they found. The room's own investigative note is the useful part: a path
  into a `tmp` directory that does not exist on a normal C: drive is itself the anomaly.
- **What it does NOT prove** — that the path existed, that it was reached, or that anything there
  was opened. Typing is intent, not access. It also does not prove *which* user session typed it
  beyond the profile the hive belongs to.
- **How to parse it** — Registry Editor live, or Registry Explorer against `NTUSER.DAT`.
- **Anti-forensics / false-positive caveat** — the room states none. The key is user-writable and
  clearable from the Explorer UI.

### 2.4 WordWheelQuery

- **What it is** — terms typed into File Explorer's search box.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery`
- **What it proves** — what the user searched their own machine for, in order. In the room's case
  the most recent search is for a disk-cleaning/evidence-removal tool — search terms as a
  statement of intent.
- **What it does NOT prove** — that anything was found, opened, or acted on. A search term is the
  purest example in this room of intent without action.
  🔴🔴 **AND, AS OF 2026-08-29, IT MAY NOT EXIST AT ALL. The key is no longer populated on
  Windows 11 23H2 and later.** A SANS instructor's finding, published Oct 2024: *"in Windows 11 23H2
  the WordWheelQuery value is no longer populated"* — because *"searches are basically conducted as
  you type rather than on pressing enter"*, with the shell querying the search index directly rather
  than recording a submitted term. **13cubed's Registry Cheat Sheet v2.0 now bounds the artifact
  explicitly: *"Explorer search history (Windows 11 22H2 / Server 2022 and earlier)."***
  ⚠️ **So an empty key on a modern host means nothing.** It is not *"the user did not search"* and
  not *"the user cleared it"* — **the artifact is simply not written any more.** 24H2/25H2 not
  separately tested; both sources stop at 23H2.
- **How to parse it** — ⚠️ **Registry Editor shows it as unreadable hex.** Registry Explorer
  decodes it, and carries a **bookmark** for the key. The room makes this contrast explicitly and
  it is a good teaching moment: the raw view and the parsed view of the same key.
  Values are numbered, one **UTF-16LE** term each, with **`MRUListEx`** giving the order as 4-byte
  little-endian indices, most recent first.
  🟢 **The successor is `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths`**,
  which records a search as a `search-ms:` URI carrying both the term and the folder it ran against
  — ⚠️ **but `TypedPaths` holds only ONE timestamp for the whole key, so an individual search
  cannot be dated.**
  ➕ **And the terms themselves moved into the Windows Search index, which changed format in
  Windows 11**: Vista→Win10 used one ESE database
  (`%PROGRAMDATA%\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb`); **Windows 11 splits it
  into three SQLite databases — `Windows.db`, `Windows-gather.db`, `Windows-usn.db`.** That is a
  new and unexploited S5 artifact and it is where the evidence went.
- **Anti-forensics / false-positive caveat** — the room states none. 🟢🟢 **Ours must, and it is
  now the best currency lesson in the project:** the rule is not *"check WordWheelQuery"*, it is
  **"know the OS build before you interpret an absence."** Put the two versions of the same 13cubed
  cheat-sheet row side by side on a slide.
  🔴 **Lab-build consequence:** if `FOR-WS01`/`EVI-SRC01` are Windows 11 23H2+, **this artifact
  cannot be staged at all** and the search-terms exercise must be rebuilt on `TypedPaths` plus the
  SQLite search index. **Decide the lab OS version before the image is built.**
  ⚠️ Related: **`ActivitiesCache.db` (Windows Timeline) is deprecated** — *"no longer being
  actively maintained, its database remains for now"*. Mention as legacy; do not build on it.
  Sources: <https://thinkdfir.com/2024/10/31/windows11-wordwheelquery-woes/> ·
  <https://cdn.13cubed.com/downloads/windows_registry_cheat_sheet.pdf> ·
  <https://securelist.com/forensic-artifacts-in-windows-11/117680/>
  Full context: `diskfiltration.md` §2.3 and §3 #4–6.

### 2.5 RecentDocs

- **What it is** — a list of recently opened documents.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs`
- **What it proves** — which files, documents and folders were opened on this machine under this
  profile, and their ordering.
- **What it does NOT prove** — that the file's *contents* were read, copied or exfiltrated, or
  that the file still exists. It records an open event and nothing about what followed.
- **How to parse it** — same pattern: hex and unreadable in Registry Editor, readable in Registry
  Explorer.
- **Anti-forensics / false-positive caveat** — the room states none.

### 2.6 ComDlg32 → LastVisitedMRU

- **What it is** — the folders most recently visited through a common Open/Save dialogue.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU`
- **What it proves** — navigation history *within application dialogues* — where the user browsed
  to, reconstructing movement through the file system.
- **What it does NOT prove** — that any file in those folders was opened or saved. This key is
  about the folder, not the file.
- **How to parse it** — Registry Explorer.
- **Anti-forensics / false-positive caveat** — the room states none.

### 2.7 ComDlg32 → OpenSavePidlMRU

- **What it is** — the files most recently opened or saved through a common dialogue.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU`
- **What it proves** — *which* file was last opened from where, and which was last saved to
  where. That save side is the distinguishing value: it is one of the few artifacts here that
  evidences file **creation by the user**, not just access.
- **What it does NOT prove** — that the saved file is still present, or what it contained. Nor
  does it cover files opened by double-click rather than through a dialogue — a real coverage
  limit the room does not mention.
- **How to parse it** — Registry Explorer.
- **Anti-forensics / false-positive caveat** — the room states none.

### 2.8 UserAssist

- **What it is** — a record of GUI-launched program usage.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`
  Two GUIDs the room names explicitly, and they are worth memorising:
  - `{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}` — **executable file execution** (raw `.exe` launches)
  - `{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}` — **shortcut (`.LNK`) file execution**
  ⚠️ **CORRECTED 2026-08-28** (room 13): the room glossed `{CEBFF5CD-…}` as "interactions with files
  and folders". The documented meaning is *executable file execution*. Value names are **ROT13-encoded**
  — still ROT13 on Windows 10/11; only the Windows 7 *beta* ever used a Vigenère cipher.
- **What it proves** — four things, per the room: **program name · execution count · last executed
  · focus time.** Execution count and focus time make this the richest execution artifact in the
  room — richer than prefetch on the human-behaviour axis.
- **What it does NOT prove** — **it only sees GUI launches.** Anything run from a command line, a
  script, a service or a scheduled task does not appear. An empty UserAssist is not evidence that
  nothing ran — a distinction that matters enormously next to room 1's scheduled-task persistence.
  It also does not prove what the program did.
  ⚠️ **THREE LIMITS ADDED 2026-08-28** (room 13, where the same artifact appears from memory):
  1. **No command-line arguments are recorded** — you get the program, never how it was invoked.
  2. **One timestamp, last run only.** A count of 33 gives you 33 events and exactly one time;
     earlier executions are unrecoverable.
  3. **The count is an interaction tally, not an execution count.** On Windows 10+, *"jump to file
     location"* from the Start Menu increments the run count with **nothing executed**; a non-zero
     count with zero focus time can be a failed launch or a mere shortcut click.
- **How to parse it** — Registry Explorer against `NTUSER.DAT`; `windows.registry.userassist` when
  working from memory. ⚠️ **The `+5` run-count offset is Windows XP only** — Volatility's source
  carries a `CountStartingAtFive` field on the pre-Win7 path and applies **no adjustment** for
  Windows 7 and later. **Do not subtract 5 from a modern count.**
- **Anti-forensics / false-positive caveat** — the room states none. **Ours must**: UserAssist is
  trivially deletable by the user and is a standard anti-forensics target, and combined with the
  GUI-only limit it is **corroborating evidence only** — it strengthens a timeline built elsewhere
  and can never carry one alone. 🟢 Also worth teaching alongside it: the **live hive in memory can
  be newer than the seized `NTUSER.DAT`**, because Windows lazy-flushes hives (reconciliation after
  ~1 h idle, at unload, or at shutdown) — the same mechanism as the room-4 transaction-log matrix,
  seen from the other end.

### 2.9 RunMRU

- **What it is** — commands typed into the Run dialogue.
- **Where it lives**
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`
- **What it proves** — the commands a user typed, **and their order**. The room explains the
  ordering mechanism precisely: an `MRUList`-style value such as `dcba` gives the sequence, with
  the first letter the most recent. That ordering is what turns a list into a timeline.
- **What it does NOT prove** — that the command succeeded, or that the target existed. It records
  what was typed and accepted by the dialogue, not the outcome.
- **How to parse it** — Registry Editor is sufficient here; the values are readable.
- **Anti-forensics / false-positive caveat** — the room states none. The key is user-clearable.

### 2.10 ShellBags

- **What it is** — stored per-folder Explorer view preferences, which incidentally record that a
  folder was opened.
- **Where it lives** — primarily `USRCLASS.DAT`
  (`%USERPROFILE%\AppData\Local\Microsoft\Windows\UsrClass.dat`), mapped at
  `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell`.
  Also `NTUSER.DAT` (`%USERPROFILE%\NTUSER.dat`).
- **What it proves** — the room's list: folder view settings (icons/list/details) · folder paths
  **including external devices and network shares** · timestamps for created / last accessed ·
  user preferences such as window size and sort order · **folders that have since been deleted** ·
  external-drive and network-location access history.
  In the case it establishes that the suspect reached two network shares and browsed confidential
  directories.
- **What it does NOT prove** — that any *file* inside the folder was opened, copied or read.
  ShellBags is a folder-level artifact throughout. It also does not prove the folder still exists
  — which is exactly why it is valuable, and exactly why it must not be over-read.
- **How to parse it** — **ShellBags Explorer**, using *Load active registry* for the live system,
  or pointed at offline `UsrClass.dat`.
- **Anti-forensics / false-positive caveat** — the room gives one that we must carry: **the
  structure and content of shellbags vary by Windows version.** A parser's interpretation is
  version-dependent, so the Windows build must be recorded in the report alongside any shellbag
  finding.

### 2.11 LNK files (Recent)

- **What it is** — shortcut files Windows creates when a file is accessed.
- **Where it lives** — the room gives two paths and, unlike room 1, gets them right:
  `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent` and `%USERPROFILE%\Recent`
  ✅ **This confirms room 1's prose error** — room 1 wrote "Recent Items"; the correct folder is
  `Recent`.
- **What it proves** — the room's list: name of the file accessed · when · the **target path** it
  was accessed from · **network share name** · whether it came from the hard drive · file size.
  The network-share field is the one doing the work in this case.
- **What it does NOT prove** — execution, or that the file is still present. Same limit as room 1.
- **How to parse it** — `LECmd.exe` from the EZ tools folder. ⚠️ **the room gives no command
  line at all here** — it says to use the tool and shows output. Room 1 supplies the actual
  syntax; use that.
- **Anti-forensics / false-positive caveat** — the room states none.

### 2.12 JumpLists

- **What it is** — per-application recent-item lists surfaced in the Taskbar and Start Menu.
- **Where it lives** — two stores:
  `%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations` — maintained by Windows per app
  `%APPDATA%\Microsoft\Windows\Recent\CustomDestinations` — items an app adds itself
  **Filenames are hashed AppIDs**, so the file name does not reveal the application. The room
  frames the hashing as integrity-preserving; the practical point is that a parser is required.
- **What it proves** — recently accessed files **per application**, when, absolute target path,
  documents opened from a network share, and **how many times** each was accessed.
- **What it does NOT prove** — that the file was modified or exfiltrated, or that it still
  exists. Also, JumpLists only cover applications that participate in the feature.
- **How to parse it** — **JumpList Explorer**, which decodes the AppID to an application name.
  The room walks its four panes: loaded files → items per application → per-item metadata →
  AppID/application identity.
- **Anti-forensics / false-positive caveat** — the room states none.

## 3. Tools and commands

| tool | version the room uses | exact command | what it outputs |
|---|---|---|---|
| `regedit` | n/a (built-in) | Win+R → `regedit` | live registry; **hex/undecoded for several keys** |
| Registry Explorer | **not stated** | GUI, run as administrator; live or offline hive; has bookmarks | decoded key values |
| `cmd` | n/a | `dir /a` | reveals hidden transaction logs in `config` |
| ShellBags Explorer | **not stated** | GUI → *Load active registry*, or open offline `UsrClass.dat` | folder access tree with timestamps |
| `LECmd.exe` | **not stated** | ⚠️ **no command line given in this room** | parsed LNK detail |
| JumpList Explorer | **not stated** | GUI, from the EZ tools folder | per-app recent items + AppID resolution |
| FTK Imager | **not stated** | — (mentioned as available for offline extraction) | acquired artifacts |

### CURRENCY CHECK — run 2026-08-28

| item | result |
|---|---|
| Registry Explorer · ShellBags Explorer · JumpList Explorer · LECmd · Timeline Explorer | **all present and all at 2026.5.0**, all listed as **.NET 9** builds (ericzimmerman.github.io). Consistent with rooms 1–2. |
| .NET 9 requirement | matters for `CLEAN-TOOLS` (D17). FOR-WS01 is offline (D29) — the runtime must be baked into the snapshot, not fetched at first run. |
| `LECmd` flags | verified in the room-1 note (`-d`, `-f`, `--csv`, `--csvf` all current). This room supplies no command to check. |
| 🔴 **the tool this room needed and never names** | **The room teaches dirty hives and transaction logs as a concept, tells you to carry the logs, and then never tells you what to do with them.** **CORRECTED 2026-08-28 after extracting room 4** (`expregistryforensics`), which demonstrates the real picture: **Registry Explorer *does* integrate transaction logs natively** — it prompts on load, asks which `.LOG1`/`.LOG2` to merge, and writes a `HIVE_clean` copy. **RegRipper does not**, and its own README names `rla.exe` (or Maxim Suhanov's `yarp` + `registryFlush.py`) as the fix. **KAPE's `!EZParser` module integrates them automatically.** So `RLA` is the pre-processor for tools that cannot do it themselves, not the only path. **Our `S5-01` must teach the capability matrix, not just the concept.** |
| Room's version claims | **none stated for any tool** — third room running. |

## 4. Evidence used

- A THM lab machine holding **artifacts extracted from the suspect host** (registry hives,
  prefetch, LNK files, JumpLists), with the EZ tools on the Desktop. A second attacker machine /
  AttackBox is offered for connectivity.
- **Size: not stated. Not downloadable. No licence offered. Not reusable.**
- Lab credentials are published inline again. **Deliberately not recorded here (R8).**
- **Nothing to flag for `ecdfp-evidence`.**
- One genuinely good practice worth copying into our own lab notes, stated by the room: it is
  investigating a *live* machine, and it says plainly that **artifacts should be extracted before
  analysis to avoid unintentional tampering**, naming FTK Imager for the job. That is our `S2-06`
  and the D18/D20 integrity criterion restated by a third party — useful corroboration for class.

## 5. Lab design worth reusing

The best of the three rooms so far, and closest to our Tier B catalogue shape.

1. **The insider framing changes every question.** No intrusion, no malware — the suspect was
   authorised to be at the keyboard. So no artifact can answer "was this allowed?"; every artifact
   answers "what did they touch, and in what order?" That is a far better vehicle for
   findings-vs-interpretation (D7/D20) than an intrusion case, because the *facts* are mundane and
   only the *interpretation* is incriminating. **Strong candidate to inform our `S5-09` case.**
2. **Same artifact, two views.** Show the key raw in Registry Editor (hex, unreadable), then the
   same key in Registry Explorer (decoded). Repeated for WordWheelQuery and RecentDocs. This
   teaches that a parser is an interpretation layer — which sets up the "tool disagreement"
   discussions we want, and justifies recording tool + version in the report.
3. **A time-boxed window as the case's spine** — "what happened in those 36 hours". A bounded
   window forces filtering rather than browsing, which is the actual skill.
4. **Artifact-per-micro-page ordering.** Eleven artifacts, each with location → forensic value →
   worked look → question. That is exactly the Tier B micro-page rhythm (Part 8), independently
   arrived at. Good confirmation that our S5 shape is right.

What **not** to copy: every question is answered by clicking a GUI. There is no CLI, no parsing to
CSV, no timeline construction. For an exam rewarding **timed tool repetitions**, GUI clicking is
the wrong motion. Room 1's parse-to-CSV-then-pivot-in-Timeline-Explorer loop is the better model;
this room's *artifact coverage* is the better content. **Take content from here, motion from
room 1.**

## 6. Question patterns

17 answer inputs across 8 tasks; T1 and T8 are "continue" gates, so **15 real questions**:
T2 ×1 (count tools in a folder — an orientation gate), T3 ×2, T4 ×5, T5 ×2, T6 ×2, T7 ×3.

- **Every substantive question is answerable from exactly ONE named artifact**, and the room is
  disciplined about naming which. Best-in-class on our single-artifact rule: TypedPaths → the tmp
  path; WordWheelQuery → the last search term; OpenSavePidlMRU → where the last text file was
  saved; UserAssist → which keylogger ran five times and which wiper ran; ShellBags → the network
  share IP and sub-folder; LNK → last document and the share path; JumpList → the tmp path for
  `code.txt`, an IE URL, and an access time.
- **Question 3 in Task 3 is a nice non-obvious one**: the *current size in KB* of the SAM hive.
  It forces the student to actually locate the file on disk rather than read about it.
- **Still zero "this cannot be determined" answers.** Third room, same omission. And this room is
  the one where it would bite hardest — a student who reads ShellBags as proof that files were
  *read*, or UserAssist as proof that nothing else ran, has made exactly the error our rubric
  criterion 4 exists to catch. Our version must add at least two such questions; §2.8 and §2.10
  hand us both.

## 7. Figures we would need to draw

41 images — by far the most of any room so far, and almost all are screenshots of Registry Editor
and EZ tool panes, i.e. the answers. Three concepts deserve our own inline SVG:

| room figure showed | our SVG spec (one line) |
|---|---|
| the hive-file → mapped-key relationship (given only as a table) | a two-column mapping diagram: files on disk in `System32\config` and the profile on the left, mounted `HK*` keys on the right, arrows between — captioned "you acquire the left, you read the right" |
| WordWheelQuery raw hex vs decoded (two separate screenshots) | a side-by-side pair, same key, garbage bytes left / decoded terms right, arrow labelled "Registry Explorer" — the parser-as-interpretation-layer point |
| the user-activity key family (never drawn; scattered across Task 4) | one `NTUSER.DAT` block fanning out to six labelled subkeys — TypedPaths, WordWheelQuery, RecentDocs, ComDlg32, UserAssist, RunMRU — each tagged with the one question it answers |

The third is the diagram this room needed and does not have. Never their images (D22).

## 8. Fit against our material

### Rows this strengthens

- **`S5-04` shellbags** — direct hit and materially better than planned. Adds the deleted-folder
  property, network-share and external-drive coverage, and the version-dependence caveat.
- **`S5-07` LNK files and jumplists** — direct hit. Supplies both JumpList stores, the hashed-AppID
  problem, and the correct `Recent` path (confirming room 1's prose error).
- **`S5-01` registry structure** — the hive→key mapping table is exactly this row's content.
  **And it should grow**: dirty hives, transaction logs, and **RLA** are not in the row text and
  are a genuine acquisition-integrity issue, not a nicety. Recommend enriching `S5-01` in place
  rather than adding a row.
- **`S2-06` FTK Imager** — corroborates the extract-before-analysis discipline.

### 🔴 GAP — no row anywhere for the user-activity registry keys

Task 4 covers **six** artifacts: TypedPaths · WordWheelQuery · RecentDocs · ComDlg32
(LastVisitedMRU + OpenSavePidlMRU) · UserAssist · RunMRU. Our S5 has:

`S5-01` registry structure · `S5-02` system config (timezone/network/mounted devices) ·
`S5-03` USB · `S5-04` shellbags · `S5-05` prefetch · `S5-06` amcache/shimcache ·
`S5-07` LNK/jumplists · `S5-08` recycle bin/VSS · `S5-09` case · `S5-10` ritual.

**None of the six appear.** UserAssist in particular is a first-rank execution artifact — it
carries run count *and* focus time, and it is the artifact that distinguishes GUI-launched from
script-launched execution. Its absence beside `S5-05` prefetch and `S5-06` amcache is a real hole
in the execution story.

Proposed row — `ecdfp-intake` decides:

> `S5-04b` · User-activity registry keys — TypedPaths, WordWheelQuery, RecentDocs, ComDlg32
> (LastVisited/OpenSave MRU), UserAssist, RunMRU · M4 · prereq `S5-01` · S5 · hands-on Yes ·
> **25 min** · `F` · EVS-02

### 🔴🔴 S5 MINUTE CRISIS — three rooms in, the arithmetic no longer works

S5 totals exactly **220** (D26) with zero slack. Demands so far:

| from | proposed row | minutes |
|---|---|---|
| room 1 · Compromised Windows Analysis | `S5-06b` scheduled tasks / persistence | 15 |
| room 2 · Windows User Account Forensics | `S5-02b` local accounts and the SAM | 15 |
| room 3 · this room | `S5-04b` user-activity registry keys | 25 |
| room 3 · this room | `S5-01` enrichment (dirty hives, transaction logs, RLA) | ~5 |
| | **total demanded** | **60** |

**Sixty minutes cannot be found inside a 220-minute session by trimming rows.** S5's entire
integrated block is 130 minutes; this is asking for nearly half of it again. And **two Priority-1
S5 rooms remain unextracted** — Expediting Registry Analysis and Windows Applications Forensics —
both of which will add more.

This is no longer a "take minutes from a named row" problem. Options, for `ecdfp-intake` and a
`DECISIONS.md` row:

1. **Move artifacts out of S5.** `S5-08` recycle bin/VSS and parts of the execution family could
   sit in S6 alongside timeline work, or become the Volatility-style homework track Part 4 already
   established as a pattern.
2. **Re-split S5 across the S4/S5 boundary.** `S5-01` registry structure already depends on
   `S4-07`; some file-system-adjacent material could move down.
3. **Demote the weakest current rows to reference-only** (cheat sheet + homework, not class time).
4. **Accept narrower coverage** and state it explicitly in `scope_decisions.md` as a known gap.

**Do not resolve this per-room.** Finish the remaining S5 extractions, then take one deliberate
pass. D26 permits re-splitting in the map and forbids carrying overflow into the build — this is
that situation, and it is now large enough to need a decision, not an adjustment.

### Dependency note for the extraction order

This room names **Expediting Registry Analysis** (Priority 1, room 4 in our list) as its own
prerequisite. Our Part 1 order puts this room *before* it. Not a defect — our notes are for
instructors, not learners — but if anyone runs these rooms hands-on, reverse the two.

### Out of scope

Nothing. Entirely Windows, entirely single-host, entirely on-topic. The most in-scope room of the
three.

## 9. Links

- Room: <https://tryhackme.com/room/windowsuseractivity>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 3)
- Room's stated prerequisites: Windows Forensics 1, Windows Forensics 2, **Expediting Registry
  Analysis** (the last is Priority 1 in our Part 1 list).
- Room's onward pointers: Windows User Account Forensics (extracted — room 2), Windows
  Applications Forensics (Priority 1, not yet extracted), "Secret Recipe" (**not in this path**).
- Eric Zimmerman's tools, all at 2026.5.0: <https://ericzimmerman.github.io/>
  — includes **RLA** for replaying transaction logs into dirty hives.

END OF NOTE.
