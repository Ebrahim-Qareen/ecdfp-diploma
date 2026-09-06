# eCDFP Diploma — Project

**ITGate Academy · INE eCDFP (Certified Digital Forensics Professional)**
Owner: Ebrahim Mohamed · Root: `E:\Work\ITgate\ECDFP_Course` · Phase 0 complete, 2026-08-28

> This is the entry document. It is the **only** entry document, and it must be **true** (R5).
> Nothing here is duplicated from `00_INSTRUCTIONS.md` — that file is the full reference; this one
> is the current state. Every decision behind these choices is a dated row in `DECISIONS.md`.

---

## §1 — What this is

A practical, instructor-led digital forensics diploma, published as a static site on GitHub Pages,
plus a local forensics lab and evidence-based investigation cases.

| | |
|---|---|
| **Course** | eCDFP — INE Certified Digital Forensics Professional |
| **Shape** | 6 sessions × 4 hours = **24 hours** (D1, locked) |
| **Class** | ~5 students, offline classroom, every student at the keyboard every session |
| **Language** | All written material in professional simple English. Arabic is spoken explanation only. |
| **Live site** | `https://ebrahim-qareen.github.io/ecdfp-diploma/` |
| **Repo** | `Ebrahim-Qareen/ecdfp-diploma` · Pages = `main` / `/docs` (D5) |

**Student path:** SOC Analyst → CEH → eCIR → **eCDFP**. This is the *fourth* course. Students already
have CCNA, Windows, Linux, AD, attacker tooling (CEH), and incident response and triage (eCIR).
**Never re-teach any of it.**

**The exam sets the teaching target.**

| Domain | Weight |
|---|---|
| Fundamentals of Digital Forensics | **33 %** |
| Digital Forensics Tools & Techniques | **27 %** |
| Preservation of Evidence | **20 %** |
| Storage Device Fundamentals | **20 %** |

Format: 24 hours · 30 MCQs (15 theory + 15 scenario, answered against a live VPN lab).
**Consequence:** students must be fast and correct with tools on evidence under time pressure, not
essay-fluent. Every session produces **timed tool repetitions**. No session is theory-only.

**The INE spine** — INE wins wherever any other source disagrees:
M1 Data Acquisition · M2 Data Representation & File Examination · M3 Disks and File Systems ·
M4 System & Network Forensics · M5 Logs, Timelines & Reporting.

---

## §2 — Folder map

**This map lists only folders that exist (R5).** A folder is created on first use, and this map is
updated in the same commit as the change. Folders scheduled for later phases are listed underneath,
unbuilt, so nobody invents a different name for them later.

### Exists now

```
ECDFP_Course/
├── 00_INSTRUCTIONS.md      the full reference — Parts 0-13 (D13)
├── ECDFP_CLAUDE_SETUP.md   how to drive the build from Claude — phase prompts
├── PROJECT.md              this file — entry doc, rules, folder map, status
├── DECISIONS.md            append-only:  | Date | ID | Decision | Why |
├── README.md               public repo readme (D22)
├── .gitignore              from Part 9
│
├── Resources/              RAW SOURCE — gitignored, read-only, NEVER copied (R6)
│   ├── INE_eCDFP/              official INE material
│   └── Instructor/             your own decks
│
├── design/                 planning only — ALL of it exists before Session 1 (D10)
│   ├── design_system.md        colours · page model · components · diagram rules
│   ├── practice_platforms.md   verified external DFIR practice (links only)
│   ├── coverage_matrix.md      ★LOCKED  exam domain % → session → module → lab → case
│   ├── topic_map.md            topic → session · minutes · hands-on? · evidence needed
│   ├── scope_decisions.md      in/out of scope · instructor brief · locked format
│   └── evidence_sets.md        every EVS- set: tier · licence · size · MD5 · SHA-256 (D54)
│
├── knowledge_base/         REFERENCE — condensed from Resources/. Never published.
│   ├── README.md               index · the 10-unit → 5-module → S1-S6 map · method · provenance
│   ├── Module_01..05_*.md      one condensed file per INE module (M1-M5)
│   ├── instructor/             one delivery note per instructor session (8) + README
│   ├── thm/                    32 TryHackMe room notes + module analysis + tool-currency ref
│   └── _source_text/           GITIGNORED — verbatim OCR, 19 files, page/slide-marked
│
├── packages/               INSTRUCTOR — the 9 markdown documents per session. NEVER served.
│   └── session-01/             session_plan · instructor_guide · student_guide · guided_lab
│                               student_activity · quiz · homework · report_template · build_log
│
├── tools/                  scaffold.ps1 · precommit_scan.ps1 · check_links.ps1
├── testing/                render_gate.js · README.md   (the Part 9 gate)
├── scripts/                code only, no prose — make_evs01.py (D54) ·
│                           gen_session_record.py — the CoC records (D55)
│
└── docs/                   * THE SITE — GitHub Pages root, self-contained, no build step (D5)
    ├── .nojekyll
    ├── index.html              platform home — hero · legend · 6 session cards · tile hubs (D46)
    │                           + #records — one Case-records tile per session (D55)
    ├── roadmap.html            topic_map.md published — anchored #s1..#s6
    ├── session-01/             brief.html (syllabus, D48) · index.html = THE TEACHING PAGE
    │                           26 pages · 12 inline-SVG figures · report_template.md · img/
    │                           record.html = THE CHAIN-OF-CUSTODY RECORD (D55)
    ├── session-02..06/         brief.html + record.html — index.html arrives with each session
    ├── lab/index.html          topology · the 3 VMs · #before · #snapshots
    ├── cases/index.html        the six investigations + the carry-through incident
    ├── resources/              evidence.html · report.html · references.html
    └── assets/     css/ecdfp.css (session layer · §14 platform · §18 record)
                    js/{session,quiz,homework,task-creator}.js — session pages only
                    js/record.js — the CoC record engine, record.html only (D55)
                    base_template.html · img/itgate-logo.jpg (D49)
```

### Not built yet — created on first use

| Folder | Arrives in | Holds |
|---|---|---|
| `labs/` | Phase 3 | `lab_design.md` (ONE) · `setup_guide.md` (ONE) · `vm_notes/` (gitignored) |
| `evidence/` | Phase 3 | **PRIVATE, gitignored** — `acquisitions/` · `manifests/` · `staging_scripts/` |
| `cases/case-NN-<name>/` | Phase 4 | investigation cases. `answer_key.md` is always a **separate, gitignored** file. |
| `docs/session-NN/index.html` | Phase 4 | the teaching page. **S1 built 2026-08-30**; `brief.html` sits beside it (D48) |
| `docs/session-NN/assets/img/` · `report_template.md` | Phase 4 | per-session figures and the report template |
| `docs/cheatsheets/` `docs/review/` | Phase 4 | cheat-sheet hub (anchored `#sNN`) and the milestone review |
| `docs/resources/labs.html` `glossary.html` · `docs/lab/setup.html` | Phase 3–4 | practice labs, glossary, the full lab build guide |

**Why `packages/` is separate from `docs/session-NN/`:** instructor guides and answer keys must never
be served publicly. `docs/` is the public site; `packages/` is yours. Different artifacts, not two copies.

---

## §3 — Standing rules (R1–R12)

| # | Rule |
|---|---|
| **R1** | **No versioned files.** Never `_v2`, `_new`, `_final`, or a dated copy. Edit in place, log one line in `DECISIONS.md`. |
| **R2** | **One copy of the project, one path** — `E:\Work\ITgate\ECDFP_Course`. If it ever moves, delete the old path the same day. |
| **R3** | **Delete, don't archive.** Scratch files, zips and staging folders are **never created inside the project tree** — the device mount cannot delete, so litter is permanent. Build scratch outside, copy only the finished file in. |
| **R4** | **Strict folder separation.** planning (`design/`) · reference (`knowledge_base/`) · published (`docs/`) · instructor (`packages/`) · cases (`cases/`) · lab (`labs/`) · code (`scripts/`) · QA (`testing/`). Never mix two in one folder. |
| **R5** | **`PROJECT.md` is the only entry doc and it must be true.** Its folder map lists only folders that exist. |
| **R6** | **Reuse `Resources/` as-is.** Never copy a source file elsewhere. One intake pass per source; re-running updates the existing file. |
| **R7** | **One session at a time**, fully approved before the next starts. |
| **R8** | **No secrets, ever.** No passwords, keys, tokens or internal IPs in any file, including `labs/vm_notes/`. Placeholders only. |
| **R9** | **Forensic integrity (non-negotiable).** No real personal data — evidence is a published research corpus, a purpose-built DFIR challenge image, or one we generated; never a real device, case or colleague's machine. **Never commit evidence bytes** — the repo carries the manifest (source · licence · size · MD5 + SHA-256), not the bytes; large images go offline via classroom USB or the academy share. **Hash before and after, always** — every lab teaches hash → verify → work on a copy; working on an original image is a defect, not a shortcut. Every case states its provenance, licence and sourcing tier; a source whose licence or origin cannot be established is not used. |
| **R10** | **Every artifact taught uses the 6-box template:** what it is · where it lives (exact path) · what it proves · **what it does NOT prove** · how to parse it (tool + command) · one anti-forensics / false-positive caveat. |
| **R11** | **Publishing is CLI-first, but the environment wins.** `git push` has no credentials here. Commit on the mount if you like; the push happens through **GitHub Desktop**. Do not browser-automate the push. |
| **R12** | **One skill, one responsibility.** Don't create a skill for a one-off task; don't extend a skill past its one job. |

**Two more that live in Part 10 and cost real time when forgotten:**

- Never run a git command that **deletes** refs or objects on the mount (`git gc`, `git tag -d`,
  `git branch -d`). Deletes fail with `Operation not permitted` and leave a `.lock` behind.
  `gc.auto=0` and `maintenance.auto=false` are set at init to stop git doing it on its own (D14).
- Never enable `cleanUrls` or `trailingSlash`. Session pages use directory-relative asset paths;
  clean URLs shift the relative base and break every image on every session page.

---

## §4 — The skills (D4, extended by D33)

Namespaced `ecdfp-` so they never collide with the installed `ceh-` and `ecir-` sets.
Full rules per skill: Part 11 of `00_INSTRUCTIONS.md`.

| Skill | One job | Status |
|---|---|---|
| `ecdfp-intake` | one source → one condensed `knowledge_base/Module_0N_*.md` + one `topic_map.md` row. Extract with `pdftotext -layout` first, never read raw pages. Never copy verbatim. Stop if provenance is unclear. | ☑ delivered |
| `ecdfp-evidence` | owns `design/evidence_sets.md`, `evidence/manifests/` and the Tier 1/2/3 declaration. Verify download **and** hash before any session is built on it. No licence, no use. | ☑ delivered |
| `ecdfp-session-package` | the fixed 9 markdown documents per session. Terminology identical across all nine. Student-facing files carry zero instructor stage directions. | ☑ delivered |
| `ecdfp-session-html` | the fixed visual + interaction system for a session page — **look only, never content**. Starts from `base_template.html`. Never invents a colour, never inlines CSS/JS, never forks the stylesheet, edits the affected `<section>` only. | ☑ delivered |
| `ecdfp-case` | one investigation case in `cases/case-NN-<name>/`. Never a tool the course has not taught. Answer key always a separate file. Generator code in `scripts/`. | ☑ delivered |
| `ecdfp-publish` | reviewed material → live site. Credential + PII scan of the diff **first**. Explicit `git add <paths>`, never `-A`. Push via GitHub Desktop. Confirm the live URL updated. | ☑ delivered |
| `ecdfp-pdf-extract` | PDF / deck / transcript → clean working text. Provenance check, density check, no scratch in the tree. **Extraction only** — hands off to `ecdfp-intake` (D33). | ☑ delivered |
| `ecdfp-web-extract` | a web page → a forensics-shaped note. WebFetch first, browser only when blocked. **Mandatory tool currency check.** Extraction only — hands off to `ecdfp-intake` or `ecdfp-evidence` (D33). | ☑ delivered |

**Paid platforms (D34):** `ecdfp-web-extract` goes straight to the Chrome browser tools; `WebFetch` is not tried first.

**Reused as-is, not rebuilt:** `ceh-web-research` (gap-filling + the mandatory **tool currency check** —
forensic tooling rots fast) and `ceh-chrome-extract` (pages `WebFetch` cannot reach).
**Not a skill:** the lab. Decided once (Part 6), maintained by hand in `labs/lab_design.md`.

---

## §5 — Roadmap

### The 6 sessions (Part 4 — locked, D1)

| # | Session | INE | Primary domain | Case file |
|---|---|---|---|---|
| **S1** | Forensic Foundations, Evidence Integrity & Chain of Custody | M1 intro | Fundamentals + Preservation | verify 4 files against a manifest — find the tampered one |
| **S2** | Acquisition — Disk, Memory & Live Response | M1 | Preservation + Storage | suspect USB: acquire, verify, document · **the carry-through case is born** (D8) |
| **S3** | Data Representation & File Examination | M2 | Fundamentals | 12 renamed / corrupted files — identify each by header |
| **S4** | Storage Devices, Partitions & File Systems | M3 | Storage | wiped partition table — recover it and prove the recovery |
| **S5** | Windows Forensics — Registry, User Activity & Execution | M4 | Fundamentals | which USB, which user, which program ran, when, how many times |
| **S6** | Network Forensics, Timelines, Reporting & Capstone | M4 + M5 | Tools & Techniques | **full capstone:** image + memory + pcap → written forensic report |

**Ordering rule — do not reorder without a decision row:** integrity before acquisition · acquisition
before analysis · storage before file systems · file systems before Windows artifacts · timelines and
reporting last, because a timeline needs every earlier artifact to mean anything.

**Page shape:** Tier A concept session (~22 pages) for S1/S2/S3/S6 · Tier B catalogue session
(chapters of 8–15 micro-pages, each on the 6-box template) for S4/S5.

**Session shape (D15/D23):** 130 min integrated theory→hands-on chunks · 60 min blocked independent
investigation · 15 min hash-verify + chain-of-custody close = **205 min of topic time**, plus the
15 min break = **220 min** taught inside a 240 min slot. All six sessions total exactly 220 (D26).

**The carry-through incident (D8/D19):** malicious document → malware execution and persistence →
C2 beacon → RDP lateral movement → collection and staging → **exfiltration to USB**, ransomware
tooling staged but never fired. Staged on EVI-SRC01, imaged in S2, cut deeper every session.

### The 7 phases (Part 7)

| Phase | What | Gate to leave it | Status |
|---|---|---|---|
| **0** | Scaffold the tree, `PROJECT.md`, `DECISIONS.md` (D1–D10), `.gitignore`, `git init` with `gc.auto=0` + `maintenance.auto=false`. Create the 6 `ecdfp-` skills. | Structure matches Part 2 exactly | ☑ **complete** 2026-08-28 |
| **1** | `scope_decisions.md` → `coverage_matrix.md` → `topic_map.md` with minutes + evidence. **And** `design_system.md` + `ecdfp.css` + `session.js` + `base_template.html` + `docs/index.html`. | Topic map fits every slot; one real page renders and passes the Part 9 gate | ☑ **complete** — gate passed 2026-08-28 |
| **2** | `knowledge_base/` — all 5 INE modules condensed from `Resources/`; gaps researched and tagged | Every topic in the map has a source; gaps listed in `scope_decisions.md`, not hidden | ◪ modules ☑ 2026-08-29 · **gap register ☑** `scope_decisions.md` §7, 20 rows (D50). Still open: a topic-by-topic source attestation, and closing the 20 |
| **3** | `labs/lab_design.md` + `setup_guide.md`, VMs built, **first staged compromise + acquisition done**, `evidence_sets.md` hash-verified | A student can build FOR-WS01 from the guide; every S1–S6 evidence set is verified | ☐ |
| **4** | Sessions, **one at a time** (§6) | Each session reviewed and approved before the next starts | ☐ |
| **5** | `testing/` full pass | Zero findings | ☐ |
| **6** | Publish | Live URL serves the new material | ☐ |

**Phase 1 is doubled on purpose (D9/D10).** The design system ships before the first session exists.
**Phase 3 is the critical path.** Start building the VMs in parallel with Phase 2, not after it.

### The lab (Part 6 — decide once, build once)

Three local VMs, VMware Workstation only, no cloud, no SIEM. **Host requirement: ≥ 250 GB free.**

| VM | Spec | Job |
|---|---|---|
| **FOR-WS01** — Win 10/11 analyst workstation | 4 vCPU · 8 GB · 120 GB · snapshot per session | where all analysis happens |
| **EVI-SRC01** — Win 10 victim | 2 vCPU · 4 GB · 60 GB | gets compromised, then imaged — the **evidence factory** |
| **Kali** — the instructor's existing Kali VM (D56) | 2 vCPU · 4 GB · 60 GB | `dd`/`dc3dd`, Sleuthkit, plaso, foremost, bulk_extractor, tcpdump |

---

## §6 — How one session gets built (Part 8)

```
0. Evidence check   evidence_sets.md has this session's set, verified + hashed.
                    Not verified -> the session does not start.
1. Scope confirm    topics from topic_map.md only. Minutes total <= 220. No expansion.
2. OUTLINE GATE *   page-by-page outline (title · tag · minutes · hands-on? · which diagram ·
                    which evidence) approved BEFORE any HTML exists.
3. Package          the 9 markdown documents  ->  packages/session-NN/
4. Page             docs/session-NN/index.html from the shared system
5. Case             cases/case-NN-*/ if the session ends in a full investigation
6. Lab              touch labs/ only if this session changes the lab. Most do not.
7. build_log.md     what was built · what was verified · what is still open
8. Verify           Part 9 gate. Must pass before review.
9. Review           you approve.
10. Publish         then — and only then — the next session starts.
```

**Step 2 saves the most time.** It is the difference between CEH Session 1 (rebuilt 3×) and
Session 2 (built once).

**The 9 documents in `packages/session-NN/`:** `session_plan.md` · `instructor_guide.md` ·
`student_guide.md` · `guided_lab.md` · `student_activity.md` · `quiz.md` · `homework.md` ·
`report_template.md` · `build_log.md`.

**The forensic report template (D7)** — fixed from Session 1, required every session:

```
Case reference · Scope and authorisation · Evidence received (file · size · MD5 · SHA-256 ·
received from · when) · Tools and versions used · Method · Findings (FACT ONLY) ·
Interpretation (clearly separated) · Conclusion · Limitations · Exhibits
```

**Findings vs Interpretation is the whole course in one line.** It is a visible, colour-coded
distinction on every page, and its colour pair is a required token in `design_system.md`.

**Case question rules:** **Q1 is always hash verification.** Every other question is answerable from
**one named artifact** — no guessing, no outside knowledge. At least one question per case has the
correct answer **"this artifact cannot prove that."**

**The Part 9 verification gate** (renders at 1400/1100/900/700/480 — the option key is `viewport`,
**not** `viewportSize` — plus credential scan · PII scan · no-evidence-bytes · hash check · link
check · time check · stage-direction scan · currency check) must pass before review, every time.
The load-bearing CSS rule is `.page-layout > * { min-width: 0 }`. Do not delete it.

**Publish flow:** `tools\precommit_scan.ps1` CLEAN → `tools\check_links.ps1` CLEAN →
GitHub Desktop commit to `main` → push → Pages redeploys (~1 min) → open the live URL and check it →
update the §7 status table + `DECISIONS.md`.

---

## §7 — Status

**Phase 0 complete: 2026-08-28.** Next: Phase 0 skills, then Phase 1.

### Sessions

| Session | Scope | Package (9 docs) | Page | Case | Evidence | Gate | Published |
|---|---|---|---|---|---|---|---|
| S1 Foundations & Chain of Custody | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| S2 Acquisition | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| S3 Data Representation | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| S4 Storage & File Systems | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| S5 Windows Forensics | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| S6 Network, Timelines & Capstone | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

### Foundations

| Item | Status |
|---|---|
| Folder tree (Phase 0–1 subset) | ☑ 2026-08-28 |
| `PROJECT.md` · `DECISIONS.md` · `.gitignore` | ☑ 2026-08-28 |
| `git init` + `gc.auto=0` + `maintenance.auto=false` | ☑ 2026-08-28 · branch `main` |
| GitHub repo `ecdfp-diploma`, Pages = `main` / `/docs`, `.nojekyll` committed | ◪ 2026-09-06 · **first commit `59ba164` on `main`** — 167 files, 5.0 MB, `.nojekyll` included · remote and Pages still to be created (push via GitHub Desktop) |
| The 8 `ecdfp-` skills (D4 + D33) | ◪ 2026-08-28 · all 8 delivered as .skill files; **7 saved and enabled** — `ecdfp-case` still to save. Verify with `ListSkills` keyword `ecdfp`, never from this row. |
| `design/scope_decisions.md` (Part 12 interview) | ☑ 2026-08-28 |
| `design/coverage_matrix.md` | ☑ 2026-08-28 |
| `design/topic_map.md` | ☑ 2026-08-28 · 62 topics · every session 220 min |
| `design/design_system.md` + `ecdfp.css` + `session.js` + `base_template.html` + `docs/index.html` | ☑ 2026-08-28 |
| `docs/` platform — hub layer (D45–D49) | ☑ 2026-08-29 · 13 pages · `ecdfp.css` §14 replaced · 946 content checks + 663 render checks clean |
| `design/scope_decisions.md` §7 — the gap register (D50) | ☑ 2026-08-29 · 20 rows · `decided` 4 · `case` 6 · `source` 10 · published on `roadmap.html#open`, every session brief and `references.html` |
| `knowledge_base/` Modules 01–05 | ☑ 2026-08-29 · 5 modules · 111 artifacts on the R10 six-box template · 8 instructor notes · `_source_text/` = all 2,218 INE pages (OCR) + 380 slides |
| `knowledge_base/thm/` | ☑ 2026-08-29 · 32 room notes + module analysis · 252 artifacts · all pass `testing/verify_note.py` · moved in from `Resources/THM/` — **delete the originals in Explorer (R6)** |
| `packages/session-01/` — the 9 documents | ☑ 2026-08-30 · 110 KB · time table sums to 205 · stage-direction scan clean |
| `docs/session-01/index.html` — the teaching page | ☑ 2026-08-30 · 26 pages · 12 inline-SVG figures · 51 data-node/data-detail pairs · render gate PASS at 1400/1100/900/700/480 |
| `docs/session-NN/record.html` — the Chain-of-Custody records (D55) | ☑ 2026-09-04 · **all 6 sessions** · `scripts/gen_session_record.py` + `assets/js/record.js` + `ecdfp.css` §18 · structure follows **SWGDE 18-Q-002** (report content), **SWGDE 18-F-002** (custody minimum) and **ISO/IEC 27037** (phases) · cumulative, one shared key `ecdfp-case-file`; custody log + disposition are case-level · gate PASS 6 pages × 6 widths force-expanded + carry-forward, cumulative export, clear-scope |
| `labs/lab_design.md` + `setup_guide.md` | ☐ |
| FOR-WS01 built + `CLEAN-TOOLS` snapshot | ☐ |
| EVI-SRC01 built + staged compromise + first acquisition | ☐ |
| `design/evidence_sets.md` populated and hash-verified | ☐ |
| `tools\precommit_scan.ps1` + `tools\check_links.ps1` | ☑ 2026-08-28 · mutation-tested |
| `testing/` harness | ☑ 2026-08-28 · 8/8 mutants caught |

### Delivery log

| Date | What shipped | Commit |
|---|---|---|
| 2026-08-28 | Phase 0 — tree, `PROJECT.md`, `DECISIONS.md` (D1–D14), `.gitignore`, `tools\scaffold.ps1` | `59ba164` |
| 2026-08-28 | Phase 1 part A — `design/scope_decisions.md`, `DECISIONS.md` D15–D22 (Part 12 interview) | `59ba164` |
| 2026-08-28 | Phase 1 part B — `design/coverage_matrix.md`, `design/topic_map.md`, `DECISIONS.md` D23–D26 | `59ba164` |
| 2026-08-28 | Phase 1 part C — `design_system.md`, `ecdfp.css`, 4 JS files, `base_template.html`, `docs/index.html`, `testing/` gate, 2 scan scripts, D27–D32. **Part 9 gate passed.** | `59ba164` |
| 2026-08-29 | Platform (hub layer) — `docs/index.html` rebuilt, `roadmap.html`, 6 × `session-NN/brief.html`, `lab/`, `cases/`, `resources/{evidence,report,references}.html`, `ecdfp.css` §14, `itgate-logo.jpg`, `design_system.md` §9, D45–D49 | `59ba164` |
| 2026-08-29 | Roadmap audit — `scope_decisions.md` §7 gap register (20 rows), D50, and the register rendered on `roadmap.html#open`, all six briefs and `references.html`. **No minutes moved.** | `59ba164` |
| 2026-09-04 | Chain-of-Custody records — `scripts/gen_session_record.py`, `docs/assets/js/record.js`, `ecdfp.css` §18, 6 × `docs/session-NN/record.html`, the `#records` hub section, a **Deliverable** section in all six briefs, and the pinned sidebar CTA on the S1 teaching page. D55. | `59ba164` |
| 2026-09-06 | **Repository review and first commit.** Release gate re-run tree-wide (155 files / 47,297 lines — no credentials, no evidence bytes, 226 PII candidates all false positives). Four broken `session-NN/index.html` links in the S3–S6 records repointed to the brief per D48 and `gen_session_record.py` taught to choose the target; quiz answer keys split into gitignored `quiz_answer_key.md`; `.gitignore` rewritten with anchored top-level paths, the 78 GB VM/ISO set and working scratch excluded. Stale `.git/index.lock` from 2026-08-28 removed — it is why the repo had zero commits. | `59ba164` |
