# scope_decisions.md — eCDFP Diploma

**Phase 1, part A.** The Part 12 interview, answered 2026-08-28.
Every answer below is also a dated row in `DECISIONS.md` (D15–D22). This file is the *reasoning*;
`DECISIONS.md` is the *record*. Reopen anything here only with a new dated row.

Format and audience are not open questions — Part 1 and D1 already fixed them:
6 × 4 h = 24 h · ~5 students · offline classroom · every student at a keyboard · written material in
simple professional English, Arabic spoken only · fourth course after SOC → CEH → eCIR.

---

## 1 — Locked format

### Delivery (Q1, Q2)

**Q1 — Integrated theory→hands-on chunks, with one blocked lab hour to close.** (D15)

Roughly the first three hours run in the eCIR/CEH rhythm — theory → instructor demo → guided
hands-on → knowledge check, repeated — and the session closes with one uninterrupted hour of
independent investigation on the same evidence.

Why: the exam is 15 scenario questions answered against a live VPN lab under time pressure, so no
session can be theory-only and students need the keyboard roughly every 25 minutes. But a forensic
investigation has a *long* shape that 20-minute chunks cannot teach — you cannot practise working
an image end to end in fragments. The closing hour is where the arc in R10 (acquire → verify →
analyse → interpret → document) actually gets rehearsed.

**Consequence for the page shapes.** Tier A already fits: pages 5–11 are the integrated chunks,
page 12 is the break, and pages 15–17 (independent practice → investigation → knowledge check 2)
become the blocked hour. Tier B (S4, S5) is a catalogue of micro-pages, so its closing hour is the
**last chapter**, run as one continuous investigation rather than as more micro-pages.

**Time shape per session (≤ 220 min of the 240):**

| Block | Minutes |
|---|---|
| Integrated chunks (theory · demo · guided hands-on · checks) | ~130 |
| Break | 15 |
| Blocked independent investigation | 60 |
| Hash-verify + chain-of-custody closing ritual (Part 4, every session) | 15 |
| **Total** | **220** |

**Q2 — Individual work at the keyboard; paired peer-review of the forensic report.** (D16)

Every student acquires, verifies and analyses alone. Pairing exists for exactly one purpose:
reading someone else's report and marking where a *finding* has drifted into an *interpretation*.
With ~5 students that is two pairs and one trio.

Why: the exam is individual, keyboard time is the scarce resource, and shared investigations hide
who can actually drive the tools. But the findings-vs-interpretation distinction (D7) is far easier
to see in someone else's writing than in your own — reviewing is the cheapest way to teach it.

---

## 2 — Lab and evidence

**Q3 — Pre-built Windows base VM; students install the tool set and snapshot `CLEAN-TOOLS` in S1.** (D17)

You distribute FOR-WS01 as a clean, activated, patched Windows 10/11 VM with no forensic tooling.
The S1 guided lab is the tool install and the snapshot.

Why: Part 4's S1 line ("build FOR-WS01, install tool set, snapshot CLEAN-TOOLS") is preserved where
it teaches something and dropped where it does not. Installing Windows teaches nothing about
forensics and would eat most of S1's four hours; installing the analyst tool set teaches students
what is in the kit and where each tool lives, which they need from S2 onward. The snapshot is the
lesson in itself — a known-good baseline you can always return to.

**Follow-through:** `labs/setup_guide.md` (Phase 3) still documents the full build from scratch, so
a student can rebuild the workstation at home or at work. It is reference, not class time.

**Q4 — Students pre-download evidence before class. Instructor holds a fallback USB set.** (D18)

Each session's evidence package is published ahead of time with its MD5 + SHA-256; students download
and verify it before they arrive. Prepared USB drives sit in the room for anyone who arrives without
the image or with a failed hash.

Why: this is the one answer the instructions explicitly flag as the biggest logistics risk, and the
risk is real — one student without the image blocks that session's lab. The fallback USB set removes
the single point of failure without adding a class-day network dependency. It also turns a logistics
chore into the course's first lesson: **verify the hash before you start work**, every session, and
a mismatch is a finding, not an inconvenience.

**Operational rules that follow:**

- Evidence for session N is published no later than the end of session N−1.
- The published package always carries both hashes; students verify *before* class, not in class.
- The fallback USB set is prepared once and re-verified before each session it is needed for.
- No evidence bytes ever enter the repo (R9). The site carries the manifest and the hashes only.

**Q5 — The carry-through incident (D8): one intrusion chain, staged on EVI-SRC01.** (D19)

> **The story.** A finance-department user at a fictional company opens a malicious document
> received by email. Malware executes and establishes persistence, beacons to an external C2 server,
> and the operator then uses harvested credentials over RDP to reach a second host. Data is collected
> and staged in a temporary folder, archived, and copied to a USB mass-storage device. Tooling
> consistent with a ransomware precursor is dropped and staged but **never fires** — the intrusion is
> caught first. EVI-SRC01 is powered down and imaged in S2.

One incident. One EVI-SRC01 image. One timeline. Every session cuts into the same evidence at a
deeper level, which is exactly what D8 asks for.

**Why this chain and not a smaller one:** each session needs first-class evidence of its own topic,
and no single-stage story provides all of it. Mapped:

| Session | What this incident gives it |
|---|---|
| **S2** Acquisition | the powered-down host and its volatile state — disk image, memory capture, KAPE triage. The case is born here. |
| **S3** Data representation & file examination | the malicious document itself — header vs extension, embedded objects, metadata, EXIF on the staged files |
| **S4** Storage & file systems | the staging folder's deleted files, `$MFT` records, slack space, the archive, the USB volume's partition structure |
| **S5** Windows forensics | persistence in the registry, USB device history, shellbags, prefetch and amcache for execution, LNK and jumplists for file access, recycle bin |
| **S6** Network, timelines, reporting | the C2 beacon pcap, RDP session traffic, memory analysis, and the plaso super-timeline that ties all of the above into one narrative |

**ATT&CK spine** (mapped properly in `topic_map.md` during part B): Initial Access via
spearphishing attachment · Execution · Persistence · Credential Access · Lateral Movement over
RDP · Collection and staging · Exfiltration over physical medium · Impact staged but not executed.

**Cost, accepted:** this is more staging work on EVI-SRC01 in Phase 3 than a single-stage story
would be, and Phase 3 is already the critical path. Mitigated by reusing the eCIR attack scripts
(Part 5) and by scripting the whole compromise into `evidence/staging_scripts/` so it is repeatable
rather than hand-driven.

**Constraints on the story (R8, R9):** fictional company, fictional users, no real personal data, no
real IPs beyond documentation ranges, no real malware sample — a benign purpose-built binary that
produces the same artifacts. Every credential in the story is a placeholder.

---

## 3 — Assessment

**Q6 — The forensic report is graded every session against one fixed 4-criterion rubric.** (D20)

The same rubric from S1 to S6, published to students in S1 and never changed:

| # | Criterion | What earns the mark |
|---|---|---|
| 1 | **Integrity** | hashes recorded before and after · verified against the manifest · chain of custody complete (who · what · when · from where · hash · where stored) |
| 2 | **Method** | reproducible by another analyst · every tool named with its version · steps in the order performed |
| 3 | **Findings** | fact only · every finding tied to one named artifact at an exact path · nothing asserted the evidence does not show |
| 4 | **Separation** | interpretation kept visibly distinct from findings · limitations stated · at least one honest "this evidence cannot show X" |

Why one fixed rubric rather than a growing one: students see the same target six times, and the
session-over-session comparison is the only way to prove report writing is actually improving.
A moving target destroys that signal. Criterion 4 is deliberately the one the course is *about*.

**Q7 — Capstone confirmed. Investigation in class in S6; the report is take-home.** (D21)

S6's blocked hour becomes the full capstone investigation against image + memory + pcap, in the room
where you can unblock people. The written forensic report is completed afterwards and submitted.

Why: a proper report cannot be written well in the last 45 minutes of a four-hour session, and
squeezing it would compromise the single deliverable that the whole course is built to produce.
Keeping the writing outside the session also protects the 220-minute ceiling.

---

## 4 — Delivery / repo

**Q8 — Public repo.** (D22)

`Ebrahim-Qareen/ecdfp-diploma` is public, Pages = `main` / `/docs`.

Why: GitHub Pages publishes from private repositories only on Pro, Team or Enterprise — on Free it
is public repositories only. Public also means students open a URL with no account and no access
grant, and the site stands as a visible ITGate portfolio piece.

**Why public is safe here.** What is published is *teaching material*, never evidence. The
separation is already structural, not a matter of care:

- `Resources/`, `evidence/`, `labs/vm_notes/` and `cases/*/answer_key.md` are gitignored (Part 9).
- `packages/` — the 9 instructor documents — is never served and never linked from `docs/`.
- Every push runs `tools\precommit_scan.ps1` (credentials) and the PII scan before it is allowed.
- R9 forbids committing evidence bytes at all; the repo carries manifests and hashes only.

**Consequence:** because the repo is public, the credential and PII scans stop being hygiene and
become a release gate. A finding blocks the push — it does not get waived.

---

## 5 — In scope / out of scope

### In scope

Windows forensics end to end, on the INE spine: acquisition (disk, memory, live) · data
representation and file examination · storage devices, partitions and file systems · registry, user
activity and evidence of execution · network forensics · timelines · and the forensic report.

### Out of scope — decided, not overlooked

| Excluded | Why | Where a student goes instead |
|---|---|---|
| **Linux / macOS forensics** | eCDFP is Windows-weighted and 24 hours does not stretch. State this to students explicitly in S1. | `design/practice_platforms.md` (Phase 1, part B) |
| **Anything already taught** | CCNA, Windows, Linux, AD, attacker tooling (CEH), incident response and triage (eCIR). Never re-taught. | their earlier courses |
| **Cloud and mobile forensics** | not on the exam, no lab budget | out of course |
| **Malware reverse engineering** | the course examines *artifacts of execution*, not the binary | out of course |
| **Legal procedure by jurisdiction** | chain of custody is taught as method, not as law | out of course |

### Accepted costs of 24 hours (Part 4 — conscious, not accidental)

| Cost | Mitigation |
|---|---|
| **Memory forensics is compressed** into S2 (acquisition) + S6 (analysis in the capstone) — no session of its own | Volatility 3 runs as a **homework track**, with a graded homework case in S5 and S6 |
| **Anti-forensics is not a session** | mandatory caveat box inside every artifact (R10) — timestomping, wiping, log clearing, encryption. The carry-through incident includes real anti-forensic behaviour so the caveats are not hypothetical. |
| **Storage Device Fundamentals is 1.2 pp under exam weight** (18.8 % class vs 20 % exam) | WinHex / hex practice is the homework in both S3 and S4 |
| **A report cannot be written in class** | Q7 — capstone report is take-home |

---

## 6 — Instructor brief

- Teach to the exam's shape: **fast and correct with tools on evidence under time pressure.**
  Every session produces timed tool repetitions. No session is theory-only.
- Never re-teach CCNA, Windows, Linux, AD, CEH or eCIR content. Reference it and move on.
- Every technical term gets: definition → why it exists → where it is used → example → case example.
- Every artifact gets the 6-box template (R10), including **what it does NOT prove** and one
  anti-forensics or false-positive caveat.
- Every lab ends with a verification step and a chain-of-custody line.
- **Findings vs Interpretation is the course.** Colour-coded on every page, criterion 4 of the
  rubric, and the thing you correct hardest in peer review.
- Where INE and any other source disagree, INE wins. Simplify the explanation, never the meaning.
- Student-facing files contain zero instructor stage directions (Part 11, enforced by the
  Part 9 stage-direction scan). R1–R12 are the standing rules; there is no R13 or R14.

---

## 7 — Open gaps

**The register.** Phase 2's exit gate is *every topic in the map has a source; gaps are listed here,
not hidden.* This section is that list. It is the **only** place a gap is declared; the per-module
detail stays in each `knowledge_base/Module_0N_*.md` §7, which this table cites rather than copies.

Audited 2026-08-29 against `design/topic_map.md` (built 28 Aug), `DECISIONS.md` D35–D44, and all
five knowledge-base modules. **No minutes were moved** — the budget stays exactly as `topic_map.md`
and D23/D24/D26 define it, and every row below is a decision still to be taken (D50).

**Classes.** `decided` — a decision names it, no topic row carries it yet · `case` — the
carry-through incident (D19) or a case question needs evidence no topic teaches · `source` — a topic
in the map has no INE source and must be researched or removed.

| ID | Class | Item | Sessions | Detail | Status |
|---|---|---|---|---|---|
| `GAP-01` | `decided` | Browser forensics — Chromium `History`, transition types, WebView2 convergence | S5 · S6 · slide in S2/S4 | D35 | open — no topic row |
| `GAP-02` | `decided` | Cross-platform artifact-equivalence figure `F1` | S1 | D38 | open — one figure, zero minutes |
| `GAP-03` | `decided` | Carry-through topology figure `F7` and the given-context blocks | S1–S6 | D40 | blocked — D19 must first be expressed as six numbered stages across named hosts |
| `GAP-04` | `decided` | Detection-as-structure worked example (PsExec `-r`) | S5 · S6 | D44 | open |
| `GAP-05` | `case` | Persistence artifacts — autostart keys (Run/RunOnce, AppInit_DLLs) and the Services key | S5 | `Module_04` §2A | open — D19 stage 2 is persistence and no topic teaches the artifact |
| `GAP-06` | `case` | USB and removable-media event IDs | S5 · S6 | `Module_05` §7.5 | open — D19 **ends** in exfiltration to USB |
| `GAP-07` | `case` | Sysmon, process-creation auditing (4688) and PowerShell script-block logging | S6 | `Module_05` §7.1–3 | open — the execution chain rests on these |
| `GAP-08` | `case` | RDP session channels (`TerminalServices-LocalSessionManager`) | S5 · S6 | `Module_05` §7.4 | open — D19's lateral movement needs more than 4624 type 10 |
| `GAP-09` | `case` | SAM accounts and `ProfileList` — SID to username | S5 | `Module_04` §2A | open — Case 05 asks *which user* and no topic maps a SID to a name |
| `GAP-10` | `case` | UserAssist | S5 | `Module_04` §2A | open — sits beside Prefetch/ShimCache/Amcache in the source, absent from the map |
| `GAP-11` | `source` | Beaconing intervals and jitter | S6 | `Module_04` §7.1 | open — named in `S6-05`, absent from unit 7 |
| `GAP-12` | `source` | TLS fingerprinting (JA3 / JA3S) | S6 | `Module_04` §7.2 | open — named in `S6-05`, absent from unit 7 |
| `GAP-13` | `source` | DNS anomaly detection | S6 | `Module_04` §7.3 | open — unit 7 mentions tunnelling once and gives no method |
| `GAP-14` | `source` | NetworkMiner | S6 | `Module_04` §7.4 | open — `S6-04` requires it; unit 7 teaches other carvers |
| `GAP-15` | `source` | Wireshark *Export Objects* | S6 | `Module_04` §7.6 | open — named in `S6-02`, not in unit 7 |
| `GAP-16` | `source` | KAPE and Timeline Explorer | S2 · S4 | `Module_01` §7 G6 · `Module_03` §7.2 | open — used by `S2-07` and `S4-08`, absent from the units |
| `GAP-17` | `source` | Windows 10/11 artifact changes — `ActivitiesCache.db`, SRUM, USB `Properties` sub-IDs | S5 | `Module_04` §7.7 | open — unit 6 stops at Windows 8.1 |
| `GAP-18` | `source` | Modern plaso workflow (`log2timeline.py` → `psort.py`) | S6 | `Module_05` §7.12 | open — the units teach the retired Perl tool |
| `GAP-19` | `source` | NTFS deletion mechanics — in-use flag, `$Bitmap` release, index entry removal | S4 | `Module_03` §7.3 | open — FAT deletion is taught, NTFS deletion is not |
| `GAP-20` | `source` | TRIM, garbage collection and wear levelling | S4 | `Module_03` §7.1 | open — `S4-02`'s central "what you cannot recover" fact |

### 7.1 — What this register does not repeat

The five module §7 sections hold **129 recorded items** in total (`Module_01` 25 tagged `G1`–`G25`,
`Module_02` 14, `Module_03` 15, `Module_04` 37, `Module_05` 38). Most are **cautions** (OCR damage,
dated tooling) or **source errors** to correct in delivery, not gaps in the course. The 20 rows above
are the subset that touches a topic row, a case question or a standing decision. The rest stay where
they are, cited per module, and are read at build time by `ecdfp-session-package`.

### 7.2 — The rule, unchanged

A topic with no source is a gap, and a gap is either researched with `ecdfp-web-extract` (with the
tool-currency check) or removed from the map. It is never quietly taught from memory.
**A gap is closed by a dated `DECISIONS.md` row, not by deleting its line here.**
