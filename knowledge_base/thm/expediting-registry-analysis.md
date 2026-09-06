---
room: Expediting Registry Analysis
url: https://tryhackme.com/room/expregistryforensics
module: Windows Endpoint Investigation (Section 3 of Advanced Endpoint Investigations)
feeds: S2 — `S2-04` physical vs logical · `S2-06` FTK Imager · `S2-07` KAPE triage.
       S5 — `S5-01` registry structure (RECmd/RegRipper/Registry Explorer), `S5-02` system config.
       The single most useful room of the four so far for **S2**, not S5.
difficulty / time: Medium · **120 min** (longest in the batch) · **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 8 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

**Method and tooling, deliberately not artifacts.** The room says so explicitly up front: it will
not re-cover which artifacts exist or where — it assumes that — and instead teaches how to
*acquire* registry data and how to *parse it fast* during an incident.

Four acquisition/analysis paths, compared honestly: FTK Imager (granular, manual, slow), KAPE
(automated, scalable, delegable), Registry Explorer + RECmd (EZ parsing), RegRipper (plugin
aggregation). The room's real argument is that **no single tool is sufficient** — you learn several
so you can cover one tool's blind spots with another, and so you can fall back to first principles
when two tools disagree.

That last point is stated outright and is the best sentence in any of the four rooms:
knowing the basics matters *because* tool output can be unreliable or contradictory. That is our
`S1`/`S2` integrity argument, made by a third party.

## 2. Artifacts — one 6-box block each

This room touches fewer artifacts than room 3 because its subject is process. Five appear.

### 2.1 System identity — ComputerName and the control set

- **What it is** — the keys that answer "which machine is this evidence from?"
- **Where it lives**
  `SYSTEM\ControlSet001\Control\ComputerName\ComputerName` — the machine name
  `SYSTEM\Select\Current` — which control set is the live one
  `SYSTEM\Select\LastKnownGood` — the last-known-good control set
- **What it proves** — the identity of the acquired system, and **which `ControlSetNNN` your other
  findings should be read from**. That second part is the one people skip.
- **What it does NOT prove** — that the name is unique, honest or unchanged. A computer name is
  user-settable and is not an identifier of record — it cannot substitute for a serial number,
  disk hash or chain-of-custody entry. Nor does the current control set tell you which set was
  active at the time of the incident, only at the time of the last boot.
- **How to parse it** — Registry Explorer's **Available bookmarks** tab surfaces ComputerName and
  TimeZone directly; `SYSTEM\Select\Current` must be navigated to manually. Or RECmd.
- **Anti-forensics / false-positive caveat** — the room states none. Ours: reading
  `CurrentControlSet` on a *cold* hive is a classic error — that key does not exist on disk, it is
  synthesised at boot. Offline you must resolve `Select\Current` yourself. **The room's live-vs-cold
  discussion (§5) makes exactly this point and it is worth teaching hard.**

### 2.2 TimeZoneInformation

- **What it is** — the system's configured time zone.
- **Where it lives** — `SYSTEM\CurrentControlSet\Control\TimeZoneInformation`
  (the room asks specifically for `TimeZoneKeyName`)
- **What it proves** — the offset needed to interpret every local timestamp on the system.
- **What it does NOT prove** — what the time zone was *at the time of the events*. It is current
  configuration, not history — a machine moved or reconfigured mid-incident will mislead. It also
  says nothing about clock accuracy or drift.
- **How to parse it** — Registry Explorer bookmarks, or RECmd.
- **Anti-forensics / false-positive caveat** — the room states none. This is the artifact that
  silently corrupts an entire timeline if skipped, which is why it belongs at the *start* of an
  examination, not the end.

### 2.3 Network history — interfaces, known networks, adapters

- **What it is** — the record of networks this system has joined.
- **Where it lives**
  `SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces` — interface configuration
  and, via the `!EZParser` output, three CSVs: **KnownNetworks**, **NetworkAdapters**, **NetworkSetup**
- **What it proves** — per the room's KnownNetworks output: network name, network type,
  **first connection date, last connection date**, DNS suffix, and the **gateway's MAC address**.
  First/last-seen dates make this a genuine timeline artifact, and the gateway MAC is the closest
  thing to a physical-location fingerprint in the registry.
- **What it does NOT prove** — that the system transmitted anything, or what. It proves association
  with a network, not activity over it. A gateway MAC can be spoofed and is not unique in the way a
  serial number is.
- **How to parse it** — KAPE `!EZParser` → CSV, then **EZViewer** (the room notes the lab VM has no
  Office, so EZViewer opens the CSVs). Or Registry Explorer bookmarks.
- **Anti-forensics / false-positive caveat** — the room states none.

### 2.4 SAM account data (as RegRipper renders it)

- **What it is** — local account records, aggregated by a parser rather than read key by key.
- **Where it lives** — `SAM` hive; keys such as
  `SAM\Domains\Account\Users\Names\<username>` and `SAM\Domains\Builtin\Aliases\Names\<group>`
- **What it proves** — RegRipper's SAM output surfaces, per account: **last login date, password
  reset date, login count, RID**, and further down, **group membership**. This is the material
  room 2 described but gave no tool for — **room 4 supplies what room 2 was missing.**
- **What it does NOT prove** — a login count is not a session log; a password-reset date does not
  say who reset it or how. And crucially — see the caveat — an *absent* field may mean the data is
  absent, or may mean no plugin exists to read it.
- **How to parse it** — RegRipper `rr.exe` (GUI): set Hive File, set Report File, click Rip.
  One hive at a time. Or RECmd `--sk` / `--kn` for targeted lookups.
- **Anti-forensics / false-positive caveat** — **the room states the best tool caveat in the whole
  batch, and it belongs verbatim in our material as a principle: a RegRipper plugin may run when
  the key is absent, and a key may be present when no plugin exists to read it.** Therefore
  *"RegRipper did not report it"* is never *"it is not there."* That is criterion-4 thinking about
  a tool rather than an artifact, and we should teach it that way.

### 2.5 Registry transaction logs — the corrected picture

- **What it is** — pending registry changes not yet written into the hive file.
- **Where it lives** — `C:\Windows\System32\config`, as `HIVE.LOG1`, `HIVE.LOG2`, plus backup files.
  Hidden — room 3 uses `dir /a` to reveal them.
- **What it proves** — that the hive you acquired may not be the hive as it stood. The room is
  emphatic: extract the transaction logs **with** the hives, or accept incomplete data.
- **What it does NOT prove** — attribution. The logs are a crash-consistency mechanism, not an
  audit trail.
- **How to parse it** — ✅ **this room answers the question room 3 left open:**
  | tool | handles transaction logs? |
  |---|---|
  | **Registry Explorer** | **Yes, natively.** Prompts on load, asks which `.LOG1`/`.LOG2` to merge, writes a `HIVE_clean` copy, offers to fall back to the dirty hive if the clean one fails to load. |
  | **KAPE `!EZParser`** | **Yes, automatically** — the room calls this out as a major advantage of the KAPE route. |
  | **RegRipper** | **No.** Its own interface warns of this. Clean the hive first. |
  | **RLA (`rla.exe`)** | the standalone pre-processor for tools that cannot — named by RegRipper's own README. |
- **Anti-forensics / false-positive caveat** — a hive parsed dirty can return a **superseded value
  that looks exactly like a correct answer**. There is no error, no warning, no visible failure —
  which makes this the most dangerous quiet defect in registry forensics and a first-rate example
  for D7.

## 3. Tools and commands

| tool | version the room uses | exact command / action | what it outputs |
|---|---|---|---|
| FTK Imager | **not stated** | `File > Add Evidence Item` → **Logical Drive** (live) or **Image File** (cold); then navigate and **Export Files** | selected hives, transaction logs, backups |
| FTK Imager | **not stated** | `Obtain Protected Files` | protected/locked registry files — **incomplete, see below** |
| KAPE (GUI) | **not stated** | `gkape.exe` → tick *Use Target Options* → set Target source / destination → pick `KapeTriage` or `RegistryHives` → *Execute!* | triage collection preserving directory structure + 3 log files |
| KAPE (batch) | **not stated** | `_kape.cli` file beside `kape.exe`, run as admin | same, unattended |
| KAPE (+modules) | **not stated** | add module options → `!EZParser` module | parsed CSVs per artifact category |
| Registry Explorer | **not stated** | `File > Load hive`; accept the transaction-log prompt; use **Available bookmarks** | decoded keys; `HIVE_clean` output |
| RECmd | **2.0.0.0** (shown in the room's own output) | `RECmd.exe -f <hive> --sk <string>` | key-name search hits |
| RECmd | **2.0.0.0** | `RECmd.exe -f <hive> --kn <keypath>` | key detail: last write time, subkey/value counts, values |
| RECmd | **2.0.0.0** | batch mode from a YAML file | normalised CSVs grouped by the batch file's `Category` |
| RegRipper | **not stated** | `rr.exe` (GUI): Hive File + Report File → **Rip!** | long text report + an execution log |
| RegRipper | **not stated** | `rip.exe` | single-plugin CLI runs |
| EZViewer | **not stated** | opens the CSVs (the lab VM has no Office) | CSV view |

**On the room's `_kape.cli` example:** it demonstrates `--tsource`, `--tdest`, `--target`,
`--vhdx`, and SFTP upload switches (`--scs` server, `--scp` port, `--scu` user, `--scpw` password).
⚠️ **The room's example embeds a plaintext SCP password. It is deliberately not reproduced here
(R8), and our material must never show one either** — that example is a bad habit printed in a
teaching resource, and it is worth calling out in class as exactly that.

### CURRENCY CHECK — run 2026-08-28

| item | result |
|---|---|
| **RECmd** — three different version numbers in play | the room's own output shows **2.0.0.0**; the GitHub README documents **1.6.0.0**; ericzimmerman.github.io ships **2026.5.0**. **The GitHub README is stale — do not source version claims from it.** Use the download page. |
| `RECmd -f` | ✅ current — "Hive to search" |
| `RECmd --sk` | ✅ current — "Search for `<string>` in key names" |
| `RECmd --kn` | ✅ current — "Display details for key name. Includes subkeys and values" |
| `RECmd --bn` | ✅ current — batch mode from a supplied file; **requires `--csv`**. The room describes batch mode but never names the switch — **add `--bn` when we teach it.** |
| RECmd output/search extras the room omits | `--csv`/`--csvf`, `--json`/`--jsonf`, `--regex`, `--Base64`, and **`--recover` (defaults to TRUE)** for deleted keys/values. The room mentions the capabilities in prose but gives no switches. |
| **RegRipper 3.0** | `rr.exe` (GUI) and `rip.exe` (CLI) both current. No version number published beyond "3.0". |
| **RegRipper + transaction logs** | ✅ **confirmed from its own README**: it does **not** process them, and recommends `yarp` + `registryFlush.py` **or Eric Zimmerman's `rla.exe`**. Independent confirmation of §2.5. |
| **Registry Explorer / EZ suite** | **2026.5.0**, .NET 9 (verified in the room-3 pass). |
| 🔴 **FTK Imager has changed materially** | current free build is **FTK Imager 8.3**, and Exterro now also ships a separate **FTK Imager Pro** line (8.2 SP1 / 8.2.0.26). **Our `S2-06` teaches FTK Imager — we must pin which product and which version, and confirm the free build still does everything the lab needs.** The room states no version at all. |
| ⚠️ **KAPE — NOT VERIFIED in this pass** | version, licence and switch list could not be confirmed from a primary source: the Kroll product URL 404s, the official KapeDocs site is a JavaScript MDwiki that renders no readable text, and the raw markdown path returns 404. **Three attempts, then stopped.** The KAPE switches above are recorded **as the room gave them** and are unverified. Verify before teaching `S2-07`. |
| Room's version claims | **none stated for any tool** — fourth room running. |

## 4. Evidence used

- A THM lab VM carrying the artifacts, with FTK Imager, KAPE, EZTools, RegRipper and EZViewer
  pre-installed, plus a second artifact set in a `James` folder for Task 7.
- **Size: not stated. Not downloadable. No licence offered. Not reusable.**
- Lab credentials published inline again. **Deliberately not recorded here (R8).**
- ✅ **One downloadable asset — flag for `ecdfp-evidence` as a *document*, not evidence:** Task 4
  attaches a **Registry Forensics cheat sheet** for download. Not an evidence set, and we must not
  redistribute it (D22, Part 5 Tier 2 — link, never rehost). Worth noting only because Part 8
  requires a cheat sheet with a Print button on every session page, and **we must author our own**;
  this one is a reference point for scope, not a source to copy.

## 5. Lab design worth reusing

**The strongest section of any room so far, and it is mostly S2 material, not S5.**

1. **Live vs cold acquisition, argued rather than defined.** The room gives the trade-off properly:
   - *Live* — hives are locked and need special tools; configuration is already resolved in memory
     (you know which control set is active); **but your tool leaves traces and can overwrite the very
     program-execution keys you came for.** The room's own example is perfect: running FTK Imager to
     collect evidence writes an entry into the execution-tracking keys. Chosen when time matters.
   - *Cold* — disk removed behind a **write blocker**, imaged, **hashed**, analysed on a copy so the
     result is reproducible and the original provably untampered. Slower, minimal impact,
     **the right choice when the result may go to court.**
   **This is `S2-01`/`S2-04` and the D20 integrity criterion in one page, and it is better framed
   than most textbooks.** Take it.
2. **The tool-trace paradox as a teaching moment.** "The act of collecting changes the thing you
   are collecting" is the single most useful idea for a forensics student and this room delivers it
   with a concrete, checkable example. Build a micro-page on it.
3. **`Obtain Protected Files` is a trap, and the room says so.** It does **not** collect every hive —
   notably it misses **Amcache**, so program-execution evidence is lost — and it exists to serve a
   SAM-focused workflow. **A one-click button that silently gives you an incomplete collection is a
   perfect guided-lab failure to stage deliberately**, then recover from with the manual export.
4. **Granular vs automated, with honest costs on both sides.** FTK Imager = precision, needs
   expertise, slow, human error. KAPE = fast, scalable, **delegable to a sysadmin who is not a
   forensic examiner**, preserves directory structure and metadata. That delegation argument is a
   real-world consideration our students will meet and never see in a textbook.
5. **The escalation arc across the room** — manual export → automated collection → GUI parsing →
   CLI parsing → one-command collect-and-parse. Each step is the previous one made faster, and the
   student feels the speed-up. That is a genuinely good pedagogical spine for `S2-07`.
6. **Task 7 is a real practical challenge** — a second, un-walked artifact set with four questions
   and "use the tools of your own choice". First room in the batch to actually stop holding hands.
   **This is the shape our `student_activity.md` should take** (Part 8 doc 5).

What **not** to copy: the plaintext SCP password in the batch-file example (§3).

## 6. Question patterns

21 answer inputs across 8 tasks; several are "I have completed…" gates, so roughly **17 real
questions** — the most of any room so far.

- **Two genuinely different question types appear here, and the room is better for it:**
  - *Conceptual* — "when we collect from a disk image, what type of acquisition is that?",
    "is speed an advantage of FTK Imager collection? Y/N". These test the trade-off reasoning of
    Task 2 rather than a lookup. **We should copy this**: our sessions currently plan artifact
    lookups almost exclusively.
  - *Constructive* — "what will the contents of a `_kape.cli` file be if you want to collect from
    C: to D: using the RegistryHives target?" The student must **compose a command**, not find a
    string. That is the closest thing in four rooms to a timed tool repetition on paper, and it is
    exactly right for an exam with 15 scenario questions against a live lab.
- **Single-artifact discipline holds** for the lookup questions: ComputerName, TimeZoneKeyName,
  LastKnownGood, RID, password reset date, group membership, gateway MAC, first/last connection.
- **Task 7's four questions are unguided** — name the system, find the non-administrator account in
  the Administrators group, find the VPN-connected network, find the registered organisation.
- **Still zero "this cannot be determined" answers** — fourth room, same omission. And again this
  room hands us the material for one: given RegRipper's plugin caveat (§2.4), *"RegRipper's report
  does not mention X — can you conclude X did not happen?"* Answer: no.

## 7. Figures we would need to draw

38 images, overwhelmingly GUI screenshots of FTK Imager, KAPE and RegRipper — i.e. click-path
documentation and answers. Three concepts deserve our own inline SVG:

| room figure showed | our SVG spec (one line) |
|---|---|
| live vs cold acquisition (prose only, never drawn) | a two-column comparison: running system → tool leaves traces → fast; powered-down disk → write blocker → image → hash → copy → analysis, with a "reproducible / court-ready" tag on the cold path only |
| the KAPE collect-then-parse pipeline (several disjoint screenshots) | one left-to-right pipeline: source → **target** (`RegistryHives` / `KapeTriage`) → structured collection → **module** (`!EZParser`) → CSVs by category, with "transaction logs merged here" annotated at the module step |
| which tool handles transaction logs (never drawn; the room's key insight) | a four-row capability matrix — Registry Explorer ✓ / KAPE `!EZParser` ✓ / RegRipper ✗ / `rla.exe` = the fix — captioned "the same hive, four different answers" |

The third is the most valuable diagram to come out of any of the four rooms. Never their images (D22).

## 8. Fit against our material

### 🟢 This room's main value is S2, not S5 — Part 1 has it filed under the wrong session

Part 1 lists this room under **Windows / S5 / `S5-01` RECmd RegRipper**. That is true but is the
smaller half. Tasks 2, 3 and 6 are **acquisition**, which is S2:

- **`S2-04`** physical vs logical acquisition — the live/cold argument is better than what we planned
- **`S2-06`** FTK Imager, correct use and verification — the room gives the exact click path for both
  live (Logical Drive) and cold (Image File) collection, **plus the `Obtain Protected Files` trap**
- **`S2-07`** `dc3dd` and **KAPE targeted triage** — Tasks 3 and 6 are effectively this row's lab
- **`S2-01`** order of volatility — the tool-trace paradox reinforces it

**Recommend Part 1's Feeds column for this room be corrected to `S2` · `S5`.**

### Rows this strengthens

- **`S5-01`** registry structure — RECmd, Registry Explorer, RegRipper, and the transaction-log
  capability matrix. This is the row's tooling, settled.
- **`S5-02`** system configuration — ComputerName, control set, **TimeZoneInformation**, network
  interfaces. Direct hit; the room's questions map almost one-to-one onto the row as written.
  ✅ **`S5-02` is the one S5 row that needed no expansion.**

### ✅ Partially closes room 2's gap

Room 2 described SAM contents and **taught no parser**. This room supplies two — RegRipper's SAM
output (last login, password reset, login count, RID, group membership) and RECmd's targeted
lookups. The proposed `S5-02b` row from room 2 now has its tooling.

### 🔴 S5 MINUTE CRISIS — status after four rooms

| from | proposed | minutes |
|---|---|---|
| room 1 | `S5-06b` scheduled tasks / persistence | 15 |
| room 2 | `S5-02b` local accounts and the SAM | 15 |
| room 3 | `S5-04b` user-activity registry keys | 25 |
| room 3 | `S5-01` enrichment (dirty hives, transaction logs, tool matrix) | ~5 |
| room 4 | *(none — its additions land in S2, and `S5-01`'s enrichment is already counted)* | 0 |
| | **total demanded on S5** | **60** |

**Room 4 adds nothing further to the S5 overdraft** — a useful data point. It suggests the crisis is
concentrated in the artifact-catalogue rooms (1–3), not the tooling rooms, and that the remaining
S5 room (Windows Applications Forensics) is the last real risk to S5's budget.

**New pressure on S2, however:** the live/cold material and the KAPE collect-and-parse pipeline are
richer than `S2-04`/`S2-07` currently allow. S2 also totals exactly 220. This should be assessed
in the same deliberate pass as S5 — **not** absorbed room by room.

### Out of scope

Nothing. Entirely Windows, entirely on-topic. Note the room explicitly declines to re-teach
artifacts, which is the same discipline our `scope_decisions.md` applies to CCNA/Windows/AD/CEH —
a useful precedent to cite.

## 9. Links

- Room: <https://tryhackme.com/room/expregistryforensics>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 3)
- Room's stated prerequisites: SOC Level 1 and SOC Level 2 paths, **Windows Forensics 1**, and the
  **KAPE** room — none of which are in this path.
- RECmd (switches verified here): <https://github.com/EricZimmerman/RECmd>
  ⚠️ README version is stale (1.6.0.0) against the 2026.5.0 download.
- RegRipper 3.0 (transaction-log limitation confirmed): <https://github.com/keydet89/RegRipper3.0>
- EZ tools downloads (2026.5.0): <https://ericzimmerman.github.io/>
- FTK Imager downloads — **8.3 free, plus a separate FTK Imager Pro line**:
  <https://www.exterro.com/ftk-downloads>
- KAPE — **no working primary source found this pass.** The Kroll service URL 404s and
  <https://ericzimmerman.github.io/KapeDocs/> is a JS-only MDwiki that returns no readable text.
  Retry from <https://www.kroll.com/en/publications/cyber/kroll-artifact-parser-extractor-kape>
  or <https://aboutdfir.com/toolsandartifacts/windows/kape/> before teaching `S2-07`.

END OF NOTE.
