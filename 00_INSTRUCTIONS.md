# eCDFP Diploma — Project Instructions

**ITGate Academy · INE eCDFP (Digital Forensics Professional)**
Version 1.0 · 2026-08-28 · Owner: Ebrahim Mohamed

> **What this file is.** The single source of truth for the eCDFP project.
> It replaces `ECDFP_Project_Blueprint.md` and the earlier `ECDFP_PROJECT_INSTRUCTIONS.md` — delete both.
> Built from the working parts of the **CEH** build (flat folders, decision log, skills, outline gate)
> and the **eCIR** build (evidence policy, case files, hashes, HTML engine), with every known failure fixed.

---

## PART 0 — Locked decisions (from the design session, 2026-08-28)

Record all of these as rows D1–D10 in `DECISIONS.md` on day one. Reopen only with a new dated row.

| ID | Decision | Why |
|---|---|---|
| **D1** | **6 sessions × 4 h = 24 h.** Locked. | Fixed slot. Everything else is sized to fit it, not the reverse. |
| **D2** | **Hybrid folder model** — flat CEH names + a private `evidence/` folder (the eCIR piece). | Flat is easier to work in; evidence needs a private home that git never sees. |
| **D3** | **Evidence = own lab VM (primary) + public corpora (secondary) + synthesis where valid.** | You cannot fake `.evtx`, E01, memory dumps or hives. Decide once, not per session. |
| **D4** | **6 custom skills**, namespaced `ecdfp-`. Existing `ceh-web-research` and `ceh-chrome-extract` are reused, not duplicated. | One skill, one job. Six is the smallest set that covers the whole build. |
| **D5** | **Site root is `docs/` from day one.** Repo `Ebrahim-Qareen/ecdfp-diploma`, Pages = `main` / `/docs`. | CEH lost two publish rounds renaming `sessions/` → `docs/`. |
| **D6** | **Theme copied from eCIR, not shared.** eCDFP owns `docs/assets/css/ecdfp.css`. | Separate repos. The two sites can diverge without breaking each other. |
| **D7** | **The forensic report template is fixed from Session 1** and required in every session. | Findings-vs-interpretation is the professional skill the course exists to teach. |
| **D8** | **One carry-through case** across all 6 sessions — one incident, acquired in S2, analysed deeper each session. | Fixes CEH's missing continuity at design time instead of mid-course. |
| **D9** | **Outline gate** — a page-by-page outline is approved before any HTML exists. | CEH Session 1 was rebuilt 3× without it; Session 2 was built once with it. |
| **D10** | **Design system ships before Session 1**, not inside it. | Same root cause as D9. Phase 1 is doubled on purpose. |

---

## PART 1 — Identity

- **Course:** eCDFP — INE Certified Digital Forensics Professional, ITGate Academy.
- **Root (one copy, one path):** `E:\Work\ITgate\ECDFP_Course`
- **Live site:** `https://ebrahim-qareen.github.io/ecdfp-diploma/`
- **Student path:** SOC Analyst → CEH → eCIR → **eCDFP**. This is the *fourth* course.
  Assume they already have: attacker mindset and tooling (CEH), incident response, triage and log analysis (eCIR),
  CCNA, Windows, Linux, AD. **Never re-teach any of it.**
- **Class:** ~5 students, offline classroom, every student at the keyboard every session.
- **Language:** all written material in professional simple English. Arabic is spoken explanation only.

### The exam — this sets the teaching target

| Domain | Weight | Meaning |
|---|---|---|
| Fundamentals of Digital Forensics | **33 %** | Windows artifact analysis, evidence of execution, report structure |
| Digital Forensics Tools & Techniques | **27 %** | correct tool use, network analysis, log & timeline tools |
| Preservation of Evidence | **20 %** | collection methodology, integrity, chain of custody |
| Storage Device Fundamentals | **20 %** | physical device characteristics + logical storage structures |

**Format:** 24 hours · 30 MCQs (15 theory + 15 scenario, answered against a live VPN lab).
**Consequence:** students must be **fast and correct with tools on evidence under time pressure**, not essay-fluent.
Every session must produce timed tool repetitions. No session is theory-only.

### INE module map (the spine — INE wins where any source disagrees)

| Module | Content |
|---|---|
| **M1 · Data Acquisition** | FTK Imager, suspect USB, volatile + non-volatile acquisition |
| **M2 · Data Representation & File Examination** | file structure, header analysis, EXIF, metadata extraction |
| **M3 · Disks and File Systems** | WinHex disk recovery (MBR/GPT), FAT, NTFS, carving, deleted files, slack space |
| **M4 · System & Network Forensics** | registry, `.lnk`, thumbcache, VSS, jumplists, recycle bin, shellbags · Wireshark, network carving, tcpdump |
| **M5 · Logs, Timelines & Reporting** | log analysis, timeline creation, investigation documentation |

---

## PART 2 — Folder map (hybrid · D2)

A folder is created **on first use**, and `PROJECT.md` is updated in the same commit.

```
ECDFP_Course/
├── PROJECT.md              entry doc — rules + folder map + status table. Nothing duplicated.
├── DECISIONS.md            append-only:  | Date | ID | Decision | Why |
├── README.md               public repo readme
├── .gitignore
│
├── Resources/              RAW SOURCE — gitignored, read-only, NEVER copied
│   ├── INE_eCDFP/              official INE material
│   └── Instructor/             your own decks
│
├── design/                 planning only — ALL of it exists before Session 1
│   ├── coverage_matrix.md      ★LOCKED  exam domain % → session → module → lab → case
│   ├── topic_map.md            topic → session · minutes · hands-on? · evidence needed
│   ├── scope_decisions.md      in/out of scope · instructor brief · locked format
│   ├── design_system.md        colours · page model · components · diagram rules
│   ├── evidence_sets.md        every evidence set: source · licence · size · SHA-256 · session
│   └── practice_platforms.md   verified external DFIR practice (links only)
│
├── knowledge_base/         one condensed file per INE module. Never published.
│   └── Module_0N_<name>.md
│
├── evidence/               PRIVATE — gitignored, never published, never committed
│   ├── acquisitions/           acquisition logs (who · what · when · tool · hash)
│   ├── manifests/              <case>.md : file · MD5 · SHA-256 · size · source tier
│   └── staging_scripts/        how EVI-SRC01 was compromised before imaging
│
├── packages/session-NN/    INSTRUCTOR PACKAGE — 9 markdown docs, NOT published
│
├── cases/case-NN-<name>/   investigation cases
│   ├── brief.md  evidence_manifest.md  environment.md  tasks.md
│   └── answer_key.md           SEPARATE file — never inside docs/
│
├── labs/                   lab_design.md (ONE) · setup_guide.md (ONE) · vm_notes/
├── scripts/                code only, no prose (generators, hash/verify helpers)
├── tools/                  precommit_scan.ps1 · check_links.ps1
├── testing/                the verification harness (Part 9)
│
└── docs/                   ★ THE SITE — GitHub Pages root, self-contained, no build step
    ├── .nojekyll   index.html            course dashboard, one card per session
    ├── assets/css/ecdfp.css              ONE stylesheet, never forked per session
    ├── assets/js/  session.js · homework.js · quiz.js · task-creator.js
    ├── assets/img/                       our own SVGs
    ├── assets/base_template.html         the empty session skeleton
    ├── session-NN/index.html + assets/img/ + report_template.md
    ├── cases/index.html                  student-facing case files (no answer keys)
    ├── cheatsheets/index.html            all sessions, anchored #sNN
    ├── resources/labs.html               all practice labs, anchored #sNN
    └── review/index.html                 milestone review + quiz banks
```

**Why `packages/` is separate from `docs/session-NN/`:** instructor guides and answer keys must never be
served publicly. `docs/` is the public site; `packages/` is yours. Different artifacts, not two copies.

---

## PART 3 — Standing rules (R1–R12)

**R1 — No versioned files.** Never `_v2`, `_new`, `_final`, or a dated copy. Edit in place, log one line in `DECISIONS.md`.

**R2 — One copy of the project, one path.** `E:\Work\ITgate\ECDFP_Course`. If it ever moves, delete the old path the same day.

**R3 — Delete, don't archive, don't gitignore-as-a-substitute.** Scratch files, zips and staging folders are **never created inside the project tree** — the device mount cannot delete, so litter is permanent. Build scratch outside, copy only the finished file in.

**R4 — Strict folder separation.** planning (`design/`) · reference (`knowledge_base/`) · published (`docs/`) · instructor (`packages/`) · cases (`cases/`) · lab (`labs/`) · code (`scripts/`) · QA (`testing/`). Never mix two in one folder.

**R5 — `PROJECT.md` is the only entry doc and it must be true.** Its folder map lists only folders that exist.

**R6 — Reuse `Resources/` as-is.** Never copy a source file elsewhere. One intake pass per source; re-running updates the existing file.

**R7 — One session at a time**, fully approved before the next starts.

**R8 — No secrets, ever.** No passwords, keys, tokens or internal IPs in any file, including `labs/vm_notes/`. Placeholders only.

**R9 — Forensic integrity (non-negotiable):**
- **No real personal data.** Evidence is a published research corpus, a purpose-built DFIR challenge image, or an image we generated. Never a real device, never a real case, never a student's or colleague's machine.
- **Never commit evidence bytes.** No image, memory dump, hive or raw pcap in the repo. The repo carries the **manifest** — source, licence, size, MD5 + SHA-256 — not the bytes. Large images are distributed offline (classroom USB / academy share).
- **Hash before and after, always.** Every lab teaches hash → verify → work on a copy. Working on an original image is a defect, not a shortcut.
- **Every case states its provenance, licence and sourcing tier.** A source whose licence or origin cannot be established is not used.

**R10 — Every artifact taught uses the 6-box template:** what it is · where it lives (exact path) · what it proves · **what it does NOT prove** · how to parse it (tool + command) · one anti-forensics / false-positive caveat.

**R11 — Publishing is CLI-first, but the environment wins.** `git push` has no credentials here. Commit on the mount if you like; the push happens through **GitHub Desktop** on the machine. Do not browser-automate the push.

**R12 — One skill, one responsibility.** Don't create a skill for a one-off task; don't extend a skill past its one job.

---

## PART 4 — The locked roadmap · 6 × 4 h = 24 h (D1)

| # | Session | INE | Primary domain | Lab / evidence | Case file |
|---|---|---|---|---|---|
| **S1** | **Forensic Foundations, Evidence Integrity & Chain of Custody** | M1 intro | Fundamentals + Preservation | build **FOR-WS01**, install tool set, snapshot `CLEAN-TOOLS`, hashing + CoC form + write-blocking | verify 4 files against a manifest — find the tampered one |
| **S2** | **Acquisition — Disk, Memory & Live Response** | M1 | Preservation + Storage | FTK Imager · `dc3dd` · order of volatility · memory capture · KAPE triage · E01 vs raw vs AD1. **Image EVI-SRC01 → the carry-through case is born** | suspect USB: acquire, verify, document |
| **S3** | **Data Representation & File Examination** | M2 | Fundamentals | hex, magic bytes, headers/footers, EXIF, metadata, malicious documents, file signature vs extension | 12 renamed / corrupted files — identify each by header |
| **S4** | **Storage Devices, Partitions & File Systems** | M3 | Storage | HDD/SSD internals · sectors, clusters, slack · MBR vs GPT · FAT vs NTFS · `$MFT` · ADS · carving · deleted data | wiped partition table — recover it and prove the recovery |
| **S5** | **Windows Forensics — Registry, User Activity & Execution** | M4 | Fundamentals | hives · RegRipper · Registry Explorer · USB history · shellbags · prefetch · amcache · LNK · jumplists · recycle bin · VSS | which USB, which user, which program ran, when, how many times |
| **S6** | **Network Forensics, Timelines, Reporting & Capstone** | M4 + M5 | Tools & Techniques | Wireshark · tcpdump · network file carving · plaso super-timeline · report structure | **full capstone:** image + memory + pcap → written forensic report |

### Domain coverage matrix (verified — put this in `design/coverage_matrix.md`)

| Domain | Class hours | Class % | Exam % | Δ |
|---|---|---|---|---|
| Fundamentals of Digital Forensics | 8.00 | 33.3 % | 33 % | +0.3 |
| Digital Forensics Tools & Techniques | 6.50 | 27.1 % | 27 % | +0.1 |
| Preservation of Evidence | 5.00 | 20.8 % | 20 % | +0.8 |
| Storage Device Fundamentals | 4.50 | 18.8 % | 20 % | −1.2 |
| **Total** | **24.00** | **100 %** | **100 %** | — |

Per-session split (hours): every session reserves **0.25 h** for the hash-verify + chain-of-custody closing ritual (Preservation), and **0.75 h** minimum of timed tool reps (Tools & Techniques).

| | Fundamentals | Tools | Preservation | Storage |
|---|---|---|---|---|
| S1 | 1.50 | 0.75 | 1.75 | — |
| S2 | — | 0.75 | 2.25 | 1.00 |
| S3 | 2.50 | 0.75 | 0.25 | 0.50 |
| S4 | — | 0.75 | 0.25 | 3.00 |
| S5 | 3.00 | 0.75 | 0.25 | — |
| S6 | 1.00 | 2.75 | 0.25 | — |

### What 24 hours costs you — accept this consciously

- **Memory forensics is compressed** into S2 (acquisition) + S6 (analysis in the capstone). It does not get its own session. Mitigation: Volatility 3 is a **homework track**, with a graded homework case in S5 and S6.
- **Linux / macOS forensics is out of scope.** Recorded in `scope_decisions.md`. eCDFP is Windows-weighted; say so to students explicitly.
- **Anti-forensics is not a session.** It is a mandatory caveat box inside every artifact (R10) — timestomping, wiping, log clearing, encryption.
- **Storage is 1.2 pp under weight.** Mitigation: WinHex / hex practice is the homework in both S3 and S4.

**Ordering rule — do not reorder without a decision row:** integrity before acquisition · acquisition before analysis · storage before file systems · file systems before Windows artifacts · timelines and reporting last, because a timeline needs every earlier artifact to mean anything.

---

## PART 5 — Evidence policy (D3) — the biggest risk in the project

You **cannot** synthesize valid `.evtx`, E01/AD1 images, memory dumps or registry hives — and eCDFP is made of exactly those. Every published challenge states **its tier, its source and its hashes**.

**Tier 1 — our own lab evidence (primary).** Stage a compromise on **EVI-SRC01**, then acquire it properly. One image feeds many sessions: the same E01 yields registry hives (S5), prefetch/LNK/jumplists (S5), `$MFT` and deleted files (S4), partitions (S4). Reuse the eCIR attack scripts to stage the intrusion. Publish the **hashes and the acquisition log** on the site; distribute the image **offline**.

**Tier 2 — public corpora (linked and credited, never rehosted).** NIST CFReDS, Digital Corpora, public DFIR challenge images. Check the licence before use. Same rule as eCIR's THM rule: never republish someone else's material on our public site.

**Tier 3 — synthesized, where synthesis is actually valid:**

| Artifact | Synthesizable? | How |
|---|---|---|
| PCAP | ✅ | scapy generator, fixed seed |
| NDJSON / syslog / web logs | ✅ | the eCIR generator pattern |
| Artifact **exports** (MFT CSV, prefetch CSV, registry-parse CSV, JSON timelines) | ✅ | teaches analysis of parsed output — ideal for quizzes and homework |
| `.evtx` · E01 / raw image · memory dump · registry hives | ❌ | Tier 1 or Tier 2 only |

**Generator rule (fixes a real eCIR bug):** generators resolve output relative to `__file__`, accept `--out`, use a fixed `random.seed()` and a fixed base timestamp, and **print an MD5 + SHA-256 manifest** you paste straight into the case file.

---

## PART 6 — The lab (decide once, build once)

The eCIR SOC lab does **not** transfer. Do not rebuild it, do not extend it, leave it running for eCIR.
eCDFP needs an **analyst workstation with an evidence source** — 3 local VMs. No cloud. No firewall. No SIEM.

| VM | Spec | Job |
|---|---|---|
| **FOR-WS01** — Windows 10/11 analyst workstation | 4 vCPU · 8 GB · 120 GB · snapshot per session | where all analysis happens |
| **EVI-SRC01** — Windows 10 victim | 2 vCPU · 4 GB · 60 GB | gets compromised, then imaged — the **evidence factory** |
| **Kali** — the instructor's existing Kali VM (D56) | 2 vCPU · 4 GB · 60 GB | `dd`/`dc3dd`, Sleuthkit, plaso, foremost, bulk_extractor, tcpdump |

**Host requirement:** ≥ 250 GB free. State this in the student setup guide up front.
**Hypervisor:** one only — VMware Workstation. Record it.
**Evidence store:** a separate virtual disk or host folder, mounted **read-only**, outside the project tree.

**FOR-WS01 tool set** (install once, snapshot as `CLEAN-TOOLS`):
FTK Imager · Autopsy · WinHex or HxD · Arsenal Image Mounter · **Eric Zimmerman suite** (MFTECmd, PECmd, LECmd, JLECmd, SBECmd, RECmd, RBCmd, AmcacheParser, Registry Explorer, Timeline Explorer) · RegRipper · KAPE · Volatility 3 · bulk_extractor · PhotoRec/TestDisk · Wireshark + NetworkMiner · ExifTool · plaso/log2timeline.

Every tool on the eCDFP exam is on this list, and none of them need a network.

---

## PART 7 — Build roadmap (phases)

| Phase | What | Gate to leave it |
|---|---|---|
| **0** | Scaffold the tree, `PROJECT.md`, `DECISIONS.md` (with D1–D10), `.gitignore`, `git init` with `gc.auto=0` and `maintenance.auto=false`. Create the 6 `ecdfp-` skills. | Structure matches Part 2 exactly |
| **1** | `scope_decisions.md` (Part 12 interview) → `coverage_matrix.md` (already locked, Part 4) → `topic_map.md` with minutes + evidence columns. **And** `design_system.md` + `ecdfp.css` + `session.js` + `base_template.html` + `docs/index.html`. | Topic map fits every slot; one real page renders and passes the Part 9 gate |
| **2** | `knowledge_base/` — all 5 INE modules condensed from `Resources/`; gaps filled by research and tagged | Every topic in the map has a source; gaps listed in `scope_decisions.md`, not hidden |
| **3** | `labs/lab_design.md` + `setup_guide.md`, VMs built, **first staged compromise + acquisition done**, `evidence_sets.md` populated and hash-verified | A student can build FOR-WS01 from the guide; every S1–S6 evidence set is verified |
| **4** | Sessions, **one at a time** (Part 8) | Each session reviewed and approved before the next starts |
| **5** | `testing/` full pass | Zero findings |
| **6** | Publish | Live URL serves the new material |

**Phase 1 is doubled on purpose (D9/D10).** The design system ships before the first session exists.
**Phase 3 is the critical path.** Start building the VMs in parallel with Phase 2, not after it.

---

## PART 8 — How one session gets built

```
0. Evidence check   evidence_sets.md has this session's set, verified + hashed.
                    Not verified → the session does not start.
1. Scope confirm    topics from topic_map.md only. Minutes total ≤ 240 − 20. No expansion.
2. OUTLINE GATE ★   page-by-page outline (title · tag · minutes · hands-on? · which diagram ·
                    which evidence) approved BEFORE any HTML exists.
3. Package          the 9 markdown documents  →  packages/session-NN/
4. Page             docs/session-NN/index.html from the shared system
5. Case             cases/case-NN-*/ if the session ends in a full investigation
6. Lab              touch labs/ only if this session changes the lab. Most do not.
7. build_log.md     what was built · what was verified · what is open
8. Verify           Part 9 gate. Must pass before review.
9. Review           you approve.
10. Publish         then — and only then — the next session starts.
```

**Step 2 saves the most time.** It is the difference between CEH Session 1 (rebuilt 3×) and Session 2 (built once).

### The 9 documents in `packages/session-NN/`

| # | Document | Must contain |
|---|---|---|
| 1 | `session_plan.md` | number · title · domain reference · 3–5 action-verb objectives · time table (theory / demo / guided lab / activity / quiz) totalling **≤ 240 min** · prerequisites · evidence set + tools required |
| 2 | `instructor_guide.md` | pre-class checklist (evidence staged and hash-verified, tools installed, VM at baseline) · per-topic teaching notes + common misconceptions · exact demo script with expected output · one-line bridge to next session |
| 3 | `student_guide.md` | simplified notes matching the page · self-review walkthrough of each demo · key-terms list |
| 4 | `guided_lab.md` | objective · environment · numbered steps, each with an **expected result** and a **verification line** · common mistakes · **chain-of-custody line at the end** |
| 5 | `student_activity.md` | a less-guided task on the same evidence · success criteria · time box |
| 6 | `quiz.md` | 8–10 questions, MCQ + short scenario, each mapped to an objective · answer key · one-line justifications |
| 7 | `homework.md` | one practical task **plus the forensic report** · 3–4 criterion rubric |
| 8 | `report_template.md` | the fixed report structure (below) — also copied to `docs/session-NN/` for students |
| 9 | `build_log.md` | what was built · what was verified · what is still open |

### The forensic report template (D7) — fixed from Session 1, required every session

```
Case reference
Scope and authorisation
Evidence received          (file · size · MD5 · SHA-256 · received from · when)
Tools and versions used
Method                     (what you did, in order, reproducibly)
Findings                   (FACT ONLY — what the artifact says)
Interpretation             (what it means — clearly separated from Findings)
Conclusion
Limitations                (what this evidence cannot show)
Exhibits
```

**Findings vs Interpretation is the whole course in one line.** Make it a visible, colour-coded distinction on every page.

### Session page — two official shapes

**Tier A — concept session (~22 pages).** Use for S1, S2, S3, S6.

```
1 Cover · 2 How this session works · 3 Objectives · 4 Case hook (a real investigation)
5–7 Theory A/B/C · 8 Instructor demo · 9 Lab setup · 10 Guided hands-on · 11 Knowledge check 1
12 BREAK (timer-card data-timer="15") · 13–14 Theory D/E · 15 Independent practice
16 Investigation / case file · 17 Knowledge check 2 · 18 Summary + cheat sheet · 19 Takeaways
20 Homework + report · 21 Additional practice · 22 References (INE module + lesson only)
```

**Tier B — catalogue session (chapters of 8–15 micro-pages).** Use for S4, S5 — many artifacts, each small and uniform, every one on the **6-box template (R10)**.

Both shapes must have: the break page · mixed `.q.mcq` + `<details>` reveal questions · a cheat sheet with a Print button · `#taskList` homework + task-creator modal · prev/next nav + `kbd-hint` · a recap that maps to the previous session's takeaways.

### Investigation case file (`cases/case-NN-*/`)

1. **Brief** — the scenario, the questions to answer, scope and authorisation framing.
2. **Evidence manifest** — every file · source · tier · size · MD5 · SHA-256 · acquired when/with what.
3. **Environment** — which VM and which snapshot to start from.
4. **Investigator tasks** — numbered, using only techniques taught by that session or earlier.
5. **Expected findings** — what right looks like at each step.
6. **Artifact → conclusion mapping** — which artifact supports which conclusion. Plus MITRE ATT&CK chips.
7. **Answer key** — a **separate file**, never in the student brief, naming exact tool · command · artifact path.

**Question rules:** **Q1 is always hash verification.** Every other question is answerable from **one named artifact** — no guessing, no outside knowledge. At least one question per case has the correct answer **"this artifact cannot prove that."**

---

## PART 9 — The verification gate

Nothing is reviewed and nothing is published until this passes. Lives in `testing/`.

**Render checks** — headless browser at **1400 / 1100 / 900 / 700 / 480 px**:

- [ ] Zero document-level horizontal overflow at every width
- [ ] Zero elements wider than the viewport outside a designated scroll container
- [ ] Zero SVG text escaping its `viewBox`
- [ ] Every `data-node` has exactly one matching `data-detail`; clicking each opens exactly one panel
- [ ] Zero console errors (image placeholders excepted, each listed as an open item)
- [ ] Page count matches sidebar entry count
- [ ] Every external link host resolves

> **Two traps, both already paid for.** The option key is `viewport`, **not** `viewportSize` — `viewportSize` is silently ignored and the whole suite passes while proving nothing. And navigating to `url#pN` on an already-loaded document does not re-run the page script — reload per page under test.

> **The load-bearing CSS rule:** `.page-layout > * { min-width: 0 }`. Without it one wide nested table forces the whole page wider than the viewport instead of scrolling inside its own wrapper. Do not delete it.

**Content checks:**

- [ ] **Credential / secret scan** of the diff — `tools\precommit_scan.ps1` → CLEAN
- [ ] **PII scan** — no real names, emails, phones, addresses or identifiers in any artifact, screenshot or example output
- [ ] **No evidence bytes committed** — no image, memory dump, hive or raw pcap in the repo
- [ ] **Hash check** — every hash quoted in a lab, case brief or manifest matches the real file
- [ ] **Link check** — `tools\check_links.ps1`: every `href`, `src`, `download` resolves
- [ ] **Time check** — the session plan's minutes total ≤ 240
- [ ] **Stage-direction scan** — no instructor-only phrasing ("ask the room", "what to listen for") in any student-facing file
- [ ] **Currency check** — every tool version and command shown was confirmed current during the build

### `.gitignore`

```gitignore
Resources/
evidence/
labs/vm_notes/
cases/*/answer_key.md
*CREDENTIALS*
*.local.md
*.E01
*.AD1
*.dd
*.raw
*.mem
*.vmem
*.dmp
NTUSER.DAT
SYSTEM
SOFTWARE
SAM
SECURITY
```

---

## PART 10 — Environment & publishing: what actually works here

Measured behaviour of this exact setup. Encode it at Phase 0 rather than rediscovering it.

- **At `git init`:** set `gc.auto = 0` and `maintenance.auto = false`. Git's automatic maintenance is the source of `gc.lock` / `maintenance.lock` on this mount.
- **On the device mount: writes work, deletes do not.** `git config`, index writes, ref writes and `git commit` succeed. Anything that *removes* a file fails with `Operation not permitted` and leaves a `.lock` behind — `git tag -d`, `git branch -d`, `git gc`, packed-refs rewrites. **Never run a git command that deletes refs or objects on the mount.** To clear a stuck lock, rename it into `_to_delete/` and remove it manually. `mv` *within* the mount works; `mv` *out of* it does not.
- **`git push` has no credentials here.** No helper, no `gh`, no token. Commit on the mount if you like; **push through GitHub Desktop**. Do not browser-automate the push.
- **Site root is `docs/` from day one.** GitHub Pages: source `main` / `/docs`. If you also use Vercel: **Root Directory = `docs`**, and do not add a repo-root `vercel.json`.
- **Never enable `cleanUrls` or `trailingSlash`.** Session pages use directory-relative asset paths; clean URLs shift the relative base and break every image on every session page.
- **Anything linked from `docs/index.html` must live inside `docs/`.** Files in `packages/`, `design/`, `labs/` are outside the served root and will 404 — link those as GitHub blob URLs, or don't link them at all.
- **Verify a site-root change without deploying:** serve `docs/` locally (`python3 -m http.server`) and request `/`, `/session-NN/index.html` and the asset paths.
- **Scratch never goes in the project tree** (R3) — deletes fail, so scratch is permanent.

### Publish flow

```
1. tools\precommit_scan.ps1      → must print CLEAN
2. tools\check_links.ps1         → must print CLEAN
3. GitHub Desktop → summary → Commit to main → Push origin
4. Pages redeploys in ~1 min → open the live URL and check it
5. Update PROJECT.md status table + DECISIONS.md + the Delivery Log
```

---

## PART 11 — The 6 skills (D4)

Namespaced `ecdfp-` so they never collide with the installed `ceh-` and `ecir-` sets.

| Skill | One job | Key rules |
|---|---|---|
| **`ecdfp-intake`** | one source (PDF, deck, transcript, page) → one condensed `knowledge_base/Module_0N_*.md` + one `topic_map.md` row | Extract text locally first (`pdftotext -layout`, `pdfinfo`) — never spend model tokens reading raw pages. One file per **module**, not per source — merge, never duplicate. Never copy verbatim. **If the source is watermarked, leaked, or its provenance cannot be established: stop and say so before extracting.** |
| **`ecdfp-evidence`** | owns `design/evidence_sets.md`, `evidence/manifests/`, and the sourcing tiers | For every set record: name · source URL · publisher · licence · format · size · MD5 · SHA-256 · what it contains · which session · date verified. **Verify the download and the hash before any session is built on it.** No licence, no use. Never commit the bytes. Re-verify anything older than ~3 months before the session that needs it. Owns the Tier 1/2/3 declaration on every challenge. |
| **`ecdfp-session-package`** | the fixed 9 markdown documents per session | Every deliverable maps to the approved scope. Terminology identical across all nine. **Student-facing files contain zero instructor stage directions.** The forensic report template is included every session. Edit in place for revisions. |
| **`ecdfp-session-html`** | the fixed visual + interaction system for a session page. Look only, never content | Start from `docs/assets/base_template.html`. Never invent a colour, font or layout pattern. Never inline CSS/JS. Never fork the stylesheet per session. Edit the affected `<section>` only — never regenerate a whole page for one change. Requires `design_system.md` + `ecdfp.css` + `session.js` + `base_template.html` to exist first. |
| **`ecdfp-case`** | one investigation case in `cases/case-NN-<name>/` | The 7-part structure in Part 8. Never introduce a tool the course has not taught. Never reuse one evidence set as the answer for two cases. Generator code goes in `scripts/`, not inline. No real PII, no real company, no real case. Answer key is always a separate file. |
| **`ecdfp-publish`** | reviewed material → live site | Credential + PII scan of the diff **first**. Explicit `git add <paths>`, never `git add -A`. One commit per logical change. **Never commit an evidence image.** Push via GitHub Desktop (R11). Confirm the live URL updated before reporting it published. |

**Reused as-is, not rebuilt:** `ceh-web-research` (gap-filling + the mandatory tool **currency check** — forensic tooling rots fast; confirm the current major version and that the command shown still exists before teaching it) and `ceh-chrome-extract` (pages `WebFetch` cannot reach).

**Not a skill:** the lab. It is decided once (Part 6) and maintained by hand in `labs/lab_design.md`.

---

## PART 12 — Phase 1 interview (answer these, record in `scope_decisions.md`)

Format and students are already answered by Part 1 and D1. These are still open:

**Delivery**
1. Integrated theory→hands-on chunks (the eCIR/CEH model), or blocked theory then blocked lab?
2. Pairs/teams — used at all, and if so fixed from Session 1?

**Lab and evidence**
3. Do students build FOR-WS01 themselves, or is a pre-built image provided?
4. **Evidence hosting — the single biggest logistics risk.** Does each student download images, or does the academy pre-stage them on USB / a share? Multi-GB downloads on class day do not work.
5. What is the carry-through incident (D8)? Decide the story before S2 acquires it.

**Assessment**
6. Is the forensic report graded, and against which rubric?
7. Capstone: full investigation with a written report in S6 — confirmed?

**Delivery / repo**
8. Public or private repo?

---

## PART 13 — First 10 actions

1. Create `E:\Work\ITgate\ECDFP_Course` and the Part 2 tree — only the folders Phase 0–1 need.
2. Write `PROJECT.md` (§1 what this is · §2 folder map · §3 rules R1–R12 · §4 skill table · §5 roadmap · §6 session workflow · §7 status table) and `DECISIONS.md` with **D1–D10 already filled in**.
3. `.gitignore` from Part 9. `git init`, then `git config gc.auto 0` and `git config maintenance.auto false`.
4. Create the GitHub repo `ecdfp-diploma`, Pages = `main` / `/docs`, confirm `.nojekyll` is committed.
5. Copy `itgate.css` and the four JS files from the eCIR repo into `docs/assets/`; rename the stylesheet `ecdfp.css` (D6).
6. Write `design/coverage_matrix.md` from Part 4 — it is already locked, just transcribe it.
7. Run the Part 12 interview and write `design/scope_decisions.md`.
8. Write `design/design_system.md` + `docs/assets/base_template.html` + `docs/index.html`. **Render one throwaway page and run the Part 9 gate on it before Session 1 exists.**
9. Build **FOR-WS01** and **EVI-SRC01**, snapshot both clean, run the first staged compromise + acquisition, and populate `design/evidence_sets.md`. **Start this in parallel with step 8 — it is the critical path.**
10. Build **Session 1** through the Part 8 workflow, wire the hubs, publish, open the live URL.

---

## Appendix — eCIR / CEH → eCDFP quick reference

| eCIR / CEH | eCDFP |
|---|---|
| Numbered folders + `_archive\` | Flat names + private `evidence/` (D2) |
| `attacks/` — CTF attack challenges | `cases/` — investigation cases; the deliverable is a **finding**, not a shell |
| Cloud SOC lab (Wazuh, TheHive, Shuffle) | 3 local VMs: analyst workstation + victim + Linux (Part 6) |
| Splunk + SPL | FTK Imager · Autopsy · WinHex · EZ tools · RegRipper · KAPE · Volatility · Wireshark · plaso |
| NDJSON datasets → Splunk index | Evidence packages → forensic tools, distributed offline |
| Hidden instructor **SPL** | Hidden instructor **tool · command · artifact path** |
| Kill-chain continuity target | **One carry-through case**, acquired in S2 (D8) |
| Lab report | **Forensic report — findings separated from interpretation** (D7) |
| Authorisation to attack | **Chain of custody, integrity and PII** (R9) |
| MITRE ATT&CK mapping | MITRE ATT&CK mapping *(unchanged)* |
| repo `ecir-diploma` / `ceh-diploma` | repo `ecdfp-diploma` |

---

*Keep this file at `E:\Work\ITgate\ECDFP_Course\00_INSTRUCTIONS.md`.
Update it whenever a standing rule changes, and log the change in `DECISIONS.md`.*
