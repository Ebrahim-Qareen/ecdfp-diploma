---
room: Compromised Windows Analysis
url: https://tryhackme.com/room/compromisedwindowsanalysis
module: Windows Endpoint Investigation (Section 3 of Advanced Endpoint Investigations)
feeds: S5 — whole-session model + the D19 carry-through case. Touches S5-05, S5-06, S5-07, and S6-06.
difficulty / time: Easy · 75 min (as stated by the room — note the PATH is rated hard; this room is not)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 9 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

Root-cause analysis of one compromised Windows workstation by chaining four execution/access
artifacts plus two event-log sources into a single timeline. The real skill is **pivoting on
timestamps**: a time from one artifact becomes the filter for the next. It teaches the artifacts
in the order an investigator would actually reach for them (persistence spotted first because it
is what the user noticed), not in textbook order. Tool work is entirely Eric Zimmerman CLI
parsers feeding CSVs into Timeline Explorer.

It is a **guided walkthrough, not a challenge** — every answer is reached by following stated
steps. Its value to us is the *shape of the investigation*, not its difficulty.

## 2. Artifacts — one 6-box block each

### 2.1 Scheduled Tasks

- **What it is** — Windows' built-in mechanism for running a program on a time interval or
  trigger. Attackers use it for persistence.
- **Where it lives** — `C:\Windows\System32\Tasks` (one XML file per task). Also readable through
  the Task Scheduler GUI.
- **What it proves** — that a task exists, what it is configured to run, and its creation time.
  In this case the creation time is the pivot the whole rest of the investigation hangs on.
- **What it does NOT prove** — that the task ever fired, or that it succeeded. Configuration is
  not execution. It also does not prove *who* created it; the task file carries an author field,
  which is attacker-controlled text. Confirming execution needs a second artifact (prefetch,
  event logs).
- **How to parse it** — the room uses the GUI (Task Scheduler) and direct directory inspection.
  It does **not** teach a CLI parser for this artifact.
- **Anti-forensics / false-positive caveat** — the room states none. Ours to add: tasks are
  trivially deleted, the folder is writable by admin, and legitimate software creates
  minute-interval tasks constantly. A one-minute interval is suspicious in context, not by itself.

### 2.2 LNK files (Recent Items)

- **What it is** — shortcut files Windows creates automatically when a file is opened, recording
  metadata about the target.
- **Where it lives** — `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent`
  ⚠️ the room's prose writes this as `...\Windows\Recent Items`, but its own LECmd command uses
  `...\Windows\Recent`. **The command is right, the prose is wrong.** See §6 note.
- **What it proves** — that a file was accessed, and — critically — that it *existed*, with its
  target-created and LNK-created timestamps, **even after the target file is deleted**. That is
  the point of the task: the RAR file is gone from the disk but the LNK survives it.
- **What it does NOT prove** — that the file was executed, or that its contents were used. It
  proves an open/access event, nothing about what followed. It also does not prove the file is
  still on the system — in this case it demonstrably is not.
- **How to parse it** —
  `.\LECmd.exe -d "C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent" --csv <outdir> --csvf Parsed-LNK.csv`
  then open the CSV in Timeline Explorer. Key columns: Target Created, Source Created.
- **Anti-forensics / false-positive caveat** — the room states none. LNKs are deletable, and
  "Recent" can be disabled by policy. Also: a LNK can be *planted*, and its timestamps are file
  timestamps like any other.

### 2.3 Prefetch

- **What it is** — Windows performance-optimisation files recording that a program ran and how.
- **Where it lives** — `C:\Windows\Prefetch`
- **What it proves** — **execution**. Executable name, run count, last-run time, and the source
  timestamps that place the run in the timeline.
- **What it does NOT prove** — who ran it, or with what privileges, or what it did once running.
  It also does not prove the file is still present. And absence of a prefetch entry does not
  prove non-execution — see caveat.
- **How to parse it** —
  `.\PECmd.exe -d "C:\Windows\Prefetch" --csv <outdir> --csvf Prefetch-Parsed.csv`
- **Anti-forensics / false-positive caveat** — **the room states this one explicitly and it is a
  good one: prefetch is not enabled by default on Windows Server.** So on a server, an empty
  Prefetch folder is expected, not evidence of cleaning. Prefetch files are also individually
  deletable, and the folder is capped (older entries roll off).

### 2.4 Amcache

- **What it is** — a registry hive holding application compatibility metadata about programs seen
  on the system.
- **Where it lives** — `C:\Windows\appcompat\Programs\Amcache.hve`
- **What it proves** — richer file identity than prefetch: **full path** and **SHA1 hash** of the
  binary, plus a last-write timestamp for the file key. The hash is what makes attribution and
  threat-intel lookup possible after the binary is deleted.
- **What it does NOT prove** — that the program executed. Amcache records *presence/awareness* of
  a binary, not a run. The room does not make this distinction, and it is exactly the distinction
  our `S5-06` row is built around — treat the room as an example of the misreading, not a source
  for it. The `File Key Last Write Timestamp` is a registry write time, not an execution time.
- **How to parse it** —
  `.\AmcacheParser.exe -f "C:\Windows\appcompat\Programs\Amcache.hve" --csv <outdir> --csvf Amcache_Parsed.csv`
  ⚠️ this command omits `-i`; see §3 currency note.
- **Anti-forensics / false-positive caveat** — the room states a good operational one: **Amcache
  refreshes on restart**, which is why the room ships a pre-parsed CSV captured during the attack
  session rather than having students parse it live. That is a real acquisition-order lesson:
  reboot the evidence host and you lose this.

### 2.5 ShimCache / AppCompatCache

- **What it is** — another application-compatibility record of binaries the system has seen.
- **Where it lives** — **room does not state.**
- **What it proves** — the room says only that it "gives information on an executable".
- **What it does NOT prove** — **room does not state.**
- **How to parse it** — **room does not state.** No tool or command given.
- **Anti-forensics / false-positive caveat** — the room gives one comparative point:
  **shorter retention than Amcache.**

> This block is deliberately thin. The room mentions ShimCache in a single closing note and
> teaches nothing about it. Filling the empty boxes from general knowledge is exactly what this
> extraction forbids — `ecdfp-intake` should source `S5-06` from INE, not from here.

### 2.6 Event log — RDP logon

- **What it is** — Terminal Services connection logging.
- **Where it lives** — Event Viewer →
  `Applications and Services Logs → Microsoft → Windows → TerminalServices-RemoteConnectionManager → Operational`
  **Event ID 1149.**
- **What it proves** — that a successful RDP authentication occurred, and the source IP of the
  connecting system. It places the intrusion at a time before the payload appears on disk.
- **What it does NOT prove** — that the account owner performed it, or that the source IP is the
  attacker's true origin rather than a pivot or proxy. EID 1149 also fires on successful *user
  authentication* to the RD gateway/host — it is not by itself proof of what the session then did.
- **How to parse it** — the room uses the Event Viewer GUI only. No CLI parser taught.
- **Anti-forensics / false-positive caveat** — the room states none. Event logs are clearable, and
  this specific channel is small and rolls over.

### 2.7 Event log — Windows Defender disabled

- **What it is** — Defender's operational logging.
- **Where it lives** — Event Viewer →
  `Applications and Services Logs → Microsoft → Windows → Windows Defender → Operational`
  **Event ID 5001.**
- **What it proves** — that Defender protection was turned off, and when. Corroborates the user's
  own report — a nice example of victim statement matched to artifact.
- **What it does NOT prove** — who disabled it, or by what mechanism (GUI, policy, registry,
  tooling). It is a state-change record, not an attribution record.
- **How to parse it** — Event Viewer GUI. No CLI parser taught.
- **Anti-forensics / false-positive caveat** — the room states none. Note the room's own timeline
  table then mislabels this step as "Turned Off Firewall" — see §6.

## 3. Tools and commands

| tool | version the room uses | exact command | what it outputs |
|---|---|---|---|
| Timeline Explorer | not stated | GUI — drag-and-drop a CSV onto it | sortable/filterable grid of the CSV |
| LECmd | not stated | `.\LECmd.exe -d <RecentDir> --csvf Parsed-LNK.csv --csv <outdir>` | one CSV of parsed LNKs |
| PECmd | not stated | `.\PECmd.exe -d "C:\Windows\Prefetch" --csv <outdir> --csvf Prefetch-Parsed.csv` | one CSV of parsed prefetch |
| AmcacheParser | not stated | `.\AmcacheParser.exe -f "...\Amcache.hve" --csv <outdir> --csvf Amcache_Parsed.csv` | CSV(s) of Amcache entries |
| Task Scheduler | n/a (built-in GUI) | — | scheduled task list |
| Event Viewer | n/a (built-in GUI) | — | event log channels |

### CURRENCY CHECK — run 2026-08-28

| item | result |
|---|---|
| EZ tools current version | **2026.5.0** for all of LECmd, PECmd, AmcacheParser, Timeline Explorer (also MFTECmd, RECmd) — source: ericzimmerman.github.io |
| Runtime | .NET 4.7.2+ **or** .NET 9+ depending on which build you take. Matters for our offline FOR-WS01 image (D17/D29 — nothing fetches at runtime, so the runtime must be baked into `CLEAN-TOOLS`). |
| `PECmd -d / -f / --csv / --csvf` | **all still valid.** `-d` recursive directory, `-f` single file, mutually exclusive. |
| `LECmd -d / -f / --csv / --csvf` | **all still valid.** Also supports `--json`, `--xml`, `--html`, `-q`, `-r`. |
| `AmcacheParser -f / --csv / --csvf` | **all still valid.** |
| ⚠️ **`AmcacheParser -i`** | **the room's command omits it.** `-i` includes file entries for Programs entries. Without it the run exports only *unassociated* file entries, and AmcacheParser writes **multiple CSVs per run**, not one. The room's `--csvf Amcache_Parsed.csv` therefore does not produce a single tidy file the way the LECmd/PECmd commands do. **Teach `-i` and teach that the output is a set of CSVs.** |
| Room's version claims | the room states **no version for any tool**, so nothing it shows can be trusted to match what a student installs. Our material must state versions. |

**Nothing the room shows is broken by tool drift.** The one real defect is the missing `-i`, which
is a completeness bug, not a dead flag.

## 4. Evidence used

- A THM-hosted **lab VM** (Windows, reached by split-screen browser or RDP over VPN), plus a
  second attacker machine / AttackBox.
- **Size: not stated. Not downloadable. No licence offered.**
- The room publishes RDP credentials for its own lab VM inline. **Deliberately not recorded here
  (R8 — no credentials in any project file), and they are useless to us anyway.**
- **NOT reusable as an eCDFP evidence set.** Nothing to flag for `ecdfp-evidence`: there is no
  image, no dump, no hash, and no licence. This room contributes *design*, not evidence.
- The one acquisition lesson worth carrying: the room had to **pre-parse Amcache and ship the CSV**
  because Amcache refreshes on reboot. That is a Tier-1 staging constraint for our own
  EVI-SRC01 acquisition (D19) — capture Amcache before any restart.

## 5. Lab design worth reusing

The structure is strong and maps almost one-to-one onto our `guided_lab.md` shape:

1. **The scenario supplies the first pivot, not the tooling.** The user reports "a prompt every
   minute" → that *sends* you to Scheduled Tasks. Students are never told "now open Task
   Scheduler" out of nowhere. Our labs should open with the reported symptom, not the artifact.
2. **Each task ends with a timestamp that becomes the next task's filter.** Task created at T →
   look at LNKs just before T → RAR accessed at T−2min → look at prefetch just after → executable
   ran → Amcache for its path and hash → event logs around the whole window. This is the single
   most reusable idea in the room.
3. **One tool per artifact, always the same pattern**: `cd` to the tool directory → run the parser
   with `--csv` → drag the CSV into Timeline Explorer. Repetition of the same motion five times
   is exactly the "timed tool repetitions" the eCDFP exam rewards.
4. **The final task asks students to rebuild the timeline table themselves** rather than showing
   it filled in. The room lists the activity rows and leaves the times blank. That is a good
   cheap assessment and it is essentially our report's Method + Findings sections in miniature.
5. **Deleted-artifact reasoning is the spine.** Both the RAR and the executable are gone from
   disk. Every artifact used is one that survives deletion. Worth stealing wholesale for `S5-08`.

What we should **not** copy: the room hands over every step, so nobody has to decide what to look
at. Our `student_activity.md` must remove the pivots and make the student find them.

## 6. Question patterns

15 questions across 9 tasks. Distribution: T1 ×1, T2 ×1 (a "you are good to go" gate), T3 ×1
(tool-name recall), T4 ×2, T5 ×2, T6 ×3, T7 ×2, T8 ×2, T9 ×1 (completion gate).

- **Almost every real question is answerable from exactly ONE named artifact**, which matches our
  case rule precisely. Task name → Scheduled Tasks. RAR name and creation time → LNK. Executable
  name, run count, last run → prefetch. Full path, SHA1 → Amcache. Defender-off time, attacker IP
  → event logs.
- **Timestamp answers specify their format in the question** (`YYYY-MM-DD HH:MM:SS`, and one in
  12-hour AM/PM). Worth copying — it removes a whole class of wrong-but-right answers. Note the
  room is inconsistent about which format it wants, which is itself a small lesson in why a report
  should state its time format and timezone once, up front.
- **Not a single question has "this cannot be determined" as its answer.** Every question has a
  findable string. **This is the room's biggest weakness against our design**, because D20
  criterion 4 and R10's sixth box are precisely about knowing what an artifact cannot show. Our
  version of this case must add at least one such question — the obvious candidate is asking what
  the Amcache entry proves about execution.

### Defects found in the room — keep these, they are teaching material

1. **Wrong path in prose.** Task 5 text says `...\Microsoft\Windows\Recent Items`; the LECmd
   command in the same task uses `...\Microsoft\Windows\Recent`. The command is correct.
2. **Timeline row mislabelled.** Task 9's table lists "Turned Off Firewall", but Task 8
   established **Defender** was disabled (EID 5001). Defender ≠ firewall, and the distinction
   matters in a report.
3. **Amcache command incomplete** — missing `-i` (see §3).

All three are usable in class as "verify the source" exercises rather than as errors to hide.

## 7. Figures we would need to draw

The room carries 18 images. Most are screenshots of tool output — i.e. the answers — and are
worthless to us as well as un-reusable. Three concepts are worth our own inline SVG:

| room figure showed | our SVG spec (one line) |
|---|---|
| the pivot chain across tasks (implicit — never actually drawn) | **Draw this: a left-to-right timeline rail with five stacked pins — RDP logon → Defender off → RAR dropped → RAR opened → payload executed → task created — each pin labelled with the artifact that proves it. This is the diagram the room needed and does not have.** |
| Task Scheduler GUI showing the malicious task | a two-box comparison: `C:\Windows\System32\Tasks\<name>` XML on disk vs the same task as the GUI renders it, arrow between, caption "same fact, two views" |
| Timeline Explorer grid of parsed CSV | a stylised 4-column grid with one row highlighted and the pivot column called out, showing filter-then-pivot rather than any real data |

Never their images (D22). All three follow D28/D29 — no webfonts, our accent meanings.

## 8. Fit against our material

**Rows this strengthens (all already in `design/topic_map.md`):**

- `S5-05` prefetch — the room's command and column set are directly usable; its Server caveat is
  the best anti-forensics line in the whole room.
- `S5-06` amcache/shimcache — strengthens the *tooling*, but see the warning in §2.4: the room
  blurs presence vs execution, which is the exact misreading this row exists to correct. Use the
  command, not the framing.
- `S5-07` LNK files — the "target deleted, LNK survives" demonstration is better than anything we
  had planned.
- `S6-06` Windows event logs — supplies two concrete, high-value event IDs (1149 RDP, 5001
  Defender) tied to a story.
- **The whole-session model**: this room is a working proof that D19's chain can be taught as one
  continuous investigation, which is what S5's Tier B closing chapter is meant to be.

**GAP — our map has no scheduled-tasks row.**

`S5-01`…`S5-10` cover registry, system config, USB, shellbags, prefetch, amcache/shimcache, LNK,
recycle bin/VSS, the case and the ritual. **Persistence via scheduled tasks appears nowhere**,
despite D19's chain explicitly containing "malware execution **and persistence**". A student
following our S5 as written could not answer the first real question in this room.

Proposed row — `ecdfp-intake` decides, this skill only proposes:

> `S5-06b` · Scheduled tasks and Run keys — persistence that survives reboot ·
> M4 · prereq `S5-01` · S5 · hands-on Yes · **15 min** · `F` · EVS-02

**MINUTE RULE (D26).** S5 totals exactly 220 and must stay there, so 15 minutes must come from a
named row. Two candidates, in order of preference:

1. **`S5-08` 25 → 10 min.** Recycle bin + VSS is currently doing two artifacts in one row and is
   the least connected to the D19 chain. Cost: VSS gets thin, and `scope_decisions` already flags
   VSS/"Volume Shadow Copies" as terminology the exam uses.
2. **`S5-04` 15 → 0, folded into `S5-01`.** Shellbags as a sub-topic of registry structure. Cost:
   shellbags is a named exam artifact and deserves its own row.

Recommendation: option 1. But this is a topic-map decision, not an extraction one.

**Out of scope:** nothing. The room is Windows-only throughout.

## 9. Links

- Room: <https://tryhackme.com/room/compromisedwindowsanalysis>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 3, Windows
  Endpoint Investigation)
- Prerequisites the room names — **both outside this path**, so we do not get them from the
  extraction plan: "Windows Forensics 1" and "Windows Forensics 2".
- Eric Zimmerman's tools (version + download): <https://ericzimmerman.github.io/>
- `AmcacheParser`: <https://github.com/EricZimmerman/AmcacheParser>
- `PECmd`: <https://github.com/EricZimmerman/PECmd>
- `LECmd`: <https://github.com/EricZimmerman/LECmd>

END OF NOTE.
