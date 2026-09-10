# thm/ — TryHackMe room notes

**33 rooms from TryHackMe's *Advanced Endpoint Investigations* path, plus one module-arc
analysis.** Extracted 2026-08-28/29 by `ecdfp-web-extract` through the logged-in Chrome session
(`D34` — premium rooms return a marketing shell to `WebFetch`, so the browser tools are used
directly). Moved here from `Resources/THM/` on 2026-08-29 so they are tracked rather than sitting
in a gitignored folder.

These are **course-design intelligence, not walkthroughs.** Each note asks what the room teaches,
what its artifacts do *not* prove, whether its tools and paths are still current in 2026, what the
room gets wrong, and what we should do differently. Solutions are deliberately not recorded.

Not published (Part 2). See [`../README.md`](../README.md) for the wider knowledge base.

---

## 1 · What is here

| | |
|---|---|
| Room notes | **32**, one per room, `<room-slug>.md` |
| Module analysis | **1** — [`honeynet-collapse-module.md`](honeynet-collapse-module.md), the six-room arc read as a single design |
| Artifacts documented | **252**, every one on the R10 six-box template |
| Tool-currency reference | [`_TOOL_CURRENCY_2026-08-28.md`](_TOOL_CURRENCY_2026-08-28.md) — **186 KB, blocks A–Q.** Project-wide, not THM-specific |
| Access | 29 premium, 3 free (`forensicimaging`, `memoryanalysisintroduction`, `winincidentsurface`) |

**Read `_TOOL_CURRENCY_2026-08-28.md` before running any currency check.** Every tool version,
artifact path and deprecation verified during the extraction is already in it. Cite its items as
**"block R5"**, never bare `R5` — bare `R1`–`R8` always means a project hard rule (`D42`).

---

## 2 · The mapping — room → eCDFP session

Grouped by the THM module each room belongs to. The **Feeds** column is the note's own
`feeds:` frontmatter, condensed; open the note for the reasoning.

### File System Analysis → `S4`

| Room | Feeds | Difficulty · time | Artifacts |
|---|---|---|---:|
| [MBR and GPT Analysis](mbr-and-gpt-analysis.md) | `S4-04` MBR · `S4-05` GPT — both direct hits. **Task 5 is essentially our `S4-10` Case 04, already designed, including the proof step** | Medium · 80 min | 8 |
| [FAT32 Analysis](fat32-analysis.md) | `S4-06` FAT (direct, far deeper than the row allows) · `S4-03` slack · `S4-09` carving. Gives the MITRE mapping pattern and **a Tier 1 evidence route we had not considered** | Hard · 90 min | 7 |
| [NTFS Analysis](ntfs-analysis.md) | `S4-07` NTFS · `S4-08` MFTECmd/Timeline Explorer — both direct hits. Carries the **MFT column reference** and the **USN reason-code table** our rows only gesture at | Medium · 90 min | 8 |
| [EXT Analysis](ext-analysis.md) | `T14` ext (new PART 4 on P09, D167) — superblock at byte 1024, `s_log_block_size`, inodes, the five timestamps and `ctime` as the one a user cannot set, content recovery by `strings -t d` → block → `dd`. Extracted 2026-09-10 through the logged-in Chrome session; premium room, read in full | Medium · 60 min | 7 |
| [File Carving](file-carving.md) | `S4-09` carving (direct) · `S4-03` slack. **Most serious safety finding of the batch — CVE-2022-4510** | Medium · 90 min | 6 |
| [Diskrupt](diskrupt.md) · *challenge* | **`S4` capstone, already built.** Its four prerequisites are our four S4 teaching rows and its question chain is our session in order | Hard · 120 min | 8 |

### Windows Endpoint Investigation → `S5`

| Room | Feeds | Difficulty · time | Artifacts |
|---|---|---|---:|
| [Compromised Windows Analysis](compromised-windows-analysis.md) | Whole-session model for `S5` + the `D19` carry-through. Touches `S5-05`, `S5-06`, `S5-07`, `S6-06` | Easy · 75 min | 7 |
| [Windows User Account Forensics](windows-user-account-forensics.md) | ⚠️ Part 1 mapped this to `S5-02` — **wrong.** Real fit is a missing S5 row plus `S6-06`; ~half the room is out of scope | Medium · 60 min | 6 |
| [Windows User Activity Analysis](windows-user-activity.md) | `S5-04` shellbags · `S5-07` LNK/jumplists · enriches `S5-01`. **Exposes six user-activity registry keys with no row in our map** | Medium · 60 min | 12 |
| [Expediting Registry Analysis](expediting-registry-analysis.md) | `S2-04` · `S2-06` FTK Imager · `S2-07` KAPE triage · `S5-01` · `S5-02`. **More useful for `S2` than `S5`** | Medium · 120 min | 5 |
| [Windows Applications Forensics](windows-applications-forensics.md) | ⚠️ Part 1 mapped this to `S5-05`/`S5-06` — **wrong, the room contains neither.** Closes the scheduled-tasks gap, adds services, opens the browser-forensics question (→ `D35`) | Medium · 60 min | 11 |
| [Windows Network Analysis](windows-network-analysis.md) | `S6-02` host network artifacts · `S6-05` live triage · `S2` volatility order · `S5` SRUM. **Carries the KAPE licence change (→ `D37`)** | Medium · 45 min | 8 |
| [Logless Hunt](logless-hunt.md) · *hybrid* | `S5-08` event logs beyond Security · `S6-01` · `S6-07`. **Its scenario states the `D7` error out loud — the best opening for the whole diploma** | Medium · 90 min | 8 |
| [Blizzard](blizzard.md) · *challenge, 3 machines* | **`S6-09` capstone structure — it investigates in REVERSE order across three hosts**, which nothing else in the path does. Settled the browser-forensics decision (`D35`) | Medium · 90 min | 8 |

### Disk Image Analysis → `S2` · `S4`

| Room | Feeds | Difficulty · time | Artifacts |
|---|---|---|---:|
| [Forensic Imaging](forensic-imaging.md) · *free* | **`S2` core acquisition** — `S2-06` imaging, `S2-02` write-blocking, `S2-04` hashing, `S2-07` mounting. Also a sixth safety defect, the worst found | Easy · 45 min | 8 |
| [Autopsy](autopsy.md) | `S2-08` Autopsy walkthrough · `S4` tool reps · `S6-06` · `S3`. **Solved our Tier 2 evidence problem (→ `D36`)** | Easy · 60 min | 8 |
| [Intro to Cold System Forensics](intro-to-cold-system-forensics.md) · *P3* | `S1-02/03/06/07`, `S2-01/04` — **vocabulary and framing, not technique.** ⚠️ Three factual errors, including recommending MD5/SHA-1 for evidence integrity | Info · 60 min | 8 |
| [DiskFiltration](diskfiltration.md) · *challenge* | `S4`/`S5`/`S6` insider-exfiltration case + a question-design idea worth copying | Hard · 120 min | 8 |

### Memory Analysis → `S2-03` · `S6-10` + the Volatility homework track

| Room | Feeds | Difficulty · time | Artifacts |
|---|---|---|---:|
| [Memory Analysis Introduction](memory-analysis-introduction.md) · *free, P3* | `S2-03` and `S6-10` as vocabulary only. ⚠️ **Cites a dead ATT&CK ID and the live one for the same behaviour, in the same task** | Info · 45 min | 8 |
| [Memory Acquisition](memory-acquisition.md) | **`S2-03` direct hit** · `S2-01` · `S2-02` · `S2-04`. Reveals a fourth Tier 1 evidence route and **a lab-blocking Volatility 3 problem** affecting `S6-10` | Easy · 60 min | 6 |
| [Volatility Essentials](volatility-essentials.md) | **`S6-10` direct hit** + homework track · `S2-03` · `S6-04`. **Changes our `EVS-03` acquisition plan** | Medium · 60 min | 8 |
| [Windows Memory & Processes](windows-memory-and-processes.md) | `S6-10` direct · `S6-09` shape · `S1` MITRE discipline. **Three currency corrections reaching back into `S5`** | Medium · 75 min | 8 |
| [Windows Memory & User Activity](windows-memory-and-user-activity.md) | `S6-10` · `S6-09` · `S5` (**corrects our understanding of UserAssist**) · `S1`. One course-wide ATT&CK currency break | Medium · 60 min | 8 |
| [Windows Memory & Network](windows-memory-and-network.md) | `S6-04` · `S6-10` · `S6-09`. **The strongest findings-vs-interpretation material in the whole path.** Carries a deprecated ATT&CK technique and three mis-mappings | Medium · 60 min | 8 |
| [Supplemental Memory](supplemental-memory.md) · *module capstone, P3* | `S6-09` · `S6-10` · `S2-03`. **First room in 32 to publish an acquisition hash — and it is MD5 only.** Supplies three reusable lateral-movement lineage signatures | Medium · 60 min | 8 |

### Honeynet Collapse — one incident across six rooms → `D19` / `D40`

Read [`honeynet-collapse-module.md`](honeynet-collapse-module.md) **first**: it analyses the arc
as a single design — how state carries between rooms, what each is allowed to assume, how the
difficulty ramps. That analysis is why these six were extracted, and it produced `D40` and `D41`.

| Stage | Room | Target | Feeds | Scope |
|---:|---|---|---|---|
| 1 | [Initial Access Pot](initialaccesspot.md) | `SRV-DMZ` (Linux) | **`S1-06` hashing gets its best content here** — MD5-for-lookup vs SHA-256-for-integrity. ⚠️ **Repo-wide ATT&CK correction: T1562 revoked** | ⚠️ Linux — `D38` |
| 2 | [Elevating Movement](elevatingmovement.md) | `SRV-IT-QA` (DMZ) | `S5-05`/`S5-06` execution · `S6-06` · `S5-01` · `S6-09`. **Amcache SHA-1 covers only the first ~30 MB** | ✅ in scope |
| 3 | [Lost in RAMslation](lostinramslation.md) | `SRV-DMZ-GW` | `S2-03` · `S6-10` + memory homework. **Memory recovers the command line the disk never recorded — then undercuts it** | ✅ in scope |
| 4 | [CRM Snatch](crmsnatch.md) | `SRV-CRM-01` (CORE) | **Most in-scope room of the module.** `S6-06` · `S5-08` · `S3-03` · `S6-09` + the `D19` exfiltration leg | ✅ in scope |
| 5 | [Shock and Silence](shockandsilence.md) | `DC-01` (CORE) | **Most `S4`-relevant room in the extraction** — `$MFT`, ADS, `$LogFile`, `$UsnJrnl`, `S4-08`, `S2-04/05`, `S6-09` | ✅ in scope |
| 6 | [The Last Trial](thelasttrial.md) | Remote macOS laptop | Supplies the third column of the `D38` contrast table; *enforcement lives in the running OS, not in the data* | ⚠️ macOS — `D38` |

### Priority 3 — context only

[`windows-incident-surface.md`](windows-incident-surface.md) (*free*) is the exception in this
group: **the strongest source found for `S2-02` live response**, and it carries **safety defect
#11, the most destructive in the corpus** — opening PowerShell out of order wipes every event log
on the evidence machine. The other three (`memory-analysis-introduction`,
`intro-to-cold-system-forensics`, `supplemental-memory`) are listed in their modules above.

---

## 3 · Note format — nine fixed sections

Every room note carries these, and `testing/verify_note.py` (`D39`) enforces the structure:

| § | Section |
|---|---|
| 1 | What the room teaches |
| 2 | **Artifacts — one six-box block each** (`### 2.N`, same R10 template as the module files) |
| 3 | Tools and commands — with the 2026 currency check |
| 4 | Evidence used |
| 5 | Fit against our material |
| 6 | Question patterns |
| 7 | Lab design worth reusing |
| 8 | Figures we would need to draw |
| 9 | Links |

**Verification status: all 33 notes pass** — nine sections present, six-box counts matching the
artifact-block count exactly, zero credential or PII leaks. Re-run any time with:

```bash
cd knowledge_base/thm
for f in *.md; do python3 ../../testing/verify_note.py "$f"; done
```

Read the checker's output rather than testing for a word: it prints a report
(`ARTIFACTS` / `6-BOX` / `SECTIONS` / `BYTES`), and only the lines `6-box mismatch`,
`sections:`, `CREDENTIAL LEAK` or `MISSING` are failures. A naive `grep OK` reports all 33 as
failing.

---

## 4 · What this extraction decided

Ten decisions in `DECISIONS.md` came out of these rooms. They are the reason the extraction was
worth its cost:

| | Decision |
|---|---|
| `D35` | **Browser forensics is IN scope**, at a fixed boundary — settled by Blizzard |
| `D36` | **NIST CFReDS is the Tier 2 evidence anchor** (Data Leakage Case: NTFS · exFAT · FAT32 · UDF, E01 and raw, published hashes) — from Autopsy |
| `D37` | **KAPE taught for concepts, every step paired with a free standalone alternative** — its licence changed 1 Jan 2026 |
| `D38` | **Linux/macOS stay OUT of scope**; three things taken from ExfilNode instead at zero session minutes |
| `D40` | **The six-session carry-through gets five structural devices** from the Honeynet Collapse arc |
| `D41` | **No question's answer may be a secret or a data subject's PII** — ask *which* account, never the value. Two rooms broke this |
| `D42` | Currency-block items are cited as **"block R5"**, never bare `R5` |
| `D43` | A completion-count curve is a difficulty signal **only within one access tier** |
| `D44` | **Detection signatures are taught as structures, never strings** — and one taught signature is broken on the following slide |
| `D39` | The note checker lives at `testing/verify_note.py`, never in `/tmp` |

---

## 5 · Cautions

- **Three rooms are out of scope by `D38`** — `initialaccesspot` (Linux), `exfilnode` (Linux),
  `thelasttrial` (macOS). Their notes are kept because each contributes something at zero session
  cost, chiefly the cross-platform contrast table (figure `F1`) that lands in `S1`. **Do not
  build a lab from them.**
- **Two Part-1 mappings were wrong** and the notes say so: `windows-user-account-forensics` was
  mapped to `S5-02`, and `windows-applications-forensics` to `S5-05`/`S5-06` — that room contains
  neither prefetch nor amcache. Trust the note's §5, not the original worklist.
- **Eleven safety defects** were found across the corpus. Two are serious enough to name here:
  **CVE-2022-4510** (file-carving room) and the **PowerShell-order event-log wipe**
  (`windows-incident-surface` §5.4). Both must be handled before either technique is demonstrated
  to students.
- **The rooms' ATT&CK mappings are unreliable** — revoked IDs, moved sub-techniques and outright
  mis-mappings appear in rooms authored as recently as 2025. Block `K1` of the currency file
  covers this; re-check every ID before it reaches a slide.
- **These notes describe premium TryHackMe content.** They are our own analysis in our own words
  and hold no room solutions, but `knowledge_base/` is never published (Part 2) and should stay
  that way.
- **A duplicate currently exists.** These 34 files were copied from `Resources/THM/`, which the
  device mount cannot delete. Remove the originals from Windows Explorer so `R1`/`R6` hold —
  keep `_EXTRACTION_PROMPT.md` and `_HANDOFF_PROMPT.md`, which stay there as process record.
- **No `DECISIONS.md` row logs this move.** It should get one before the next commit.

---

## 6 · Next

1. **Fold the corrections into the module files.** Several notes correct
   [`../Module_04_System_and_Network_Forensics.md`](../Module_04_System_and_Network_Forensics.md)
   directly — UserAssist semantics, the Amcache 30 MB limit, the ATT&CK currency breaks. `ecdfp-intake`
   owns that merge.
2. **Propose the missing `topic_map.md` rows** these rooms justify — six user-activity registry
   keys with no row, scheduled tasks, services, browser forensics under `D35`.
3. **Take the ready-made case designs.** Diskrupt is an `S4` capstone already built; MBR/GPT Task 5
   is `S4-10` including the proof step; Blizzard's reverse-order three-host structure is the
   `S6-09` shape.
4. **Route `D36`'s NIST CFReDS Data Leakage Case through `ecdfp-evidence`** — it is the Tier 2
   anchor and still needs its `EVS-` IDs and hashes recorded.
