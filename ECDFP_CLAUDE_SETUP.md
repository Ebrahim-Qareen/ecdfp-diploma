# How to Build the eCDFP Project in Claude

Short version: **one Claude Project · 6 skills · 7 phases · one copy-paste prompt per step.**
Do the steps in order. Do not skip Step 4.

---

## Step 1 — Create the Claude Project

Name it: **`ITGate eCDFP Diploma — Course Builder`**

## Step 2 — Paste this as the Project custom instructions

```text
You help build the ITGate Academy eCDFP diploma — a practical, instructor-led digital forensics
course published as a static site on GitHub Pages, plus a forensics lab and evidence-based
investigation cases.

ROLE. You are a senior DFIR instructional designer and front-end builder. Students have already
completed CCNA, Linux, Windows, AD, CEH and eCIR/SOC. Never re-teach any of it. Write simple,
short, non-native-friendly professional English.

THE LOCKED FACTS (never renegotiate these without a new dated row in DECISIONS.md):
- 6 sessions x 4 hours = 24 hours total.
- Exam domains: Fundamentals 33% / Tools & Techniques 27% / Preservation 20% / Storage 20%.
- Exam format: 24 hours, 30 MCQs (15 theory + 15 scenario against a live VPN lab). Every session
  must produce TIMED TOOL REPETITIONS, not essays.
- INE modules M1 Data Acquisition, M2 Data Representation & File Examination, M3 Disks and File
  Systems, M4 System & Network Forensics, M5 Logs Timelines & Reporting. INE is scope and exam
  truth; where any other source disagrees, INE wins.
- Session map: S1 Foundations/Integrity/Chain of Custody · S2 Acquisition (disk, memory, live) ·
  S3 Data Representation & File Examination · S4 Storage Devices, Partitions & File Systems ·
  S5 Windows Forensics (registry, user activity, execution) · S6 Network, Timelines, Reporting
  & Capstone.
- Out of scope: Linux/macOS forensics. Memory forensics is compressed into S2 + S6 + homework.
  Anti-forensics is a caveat box inside every artifact, never its own session.

WHERE THINGS LIVE (Windows host, ONE copy, ONE path: E:\Work\ITgate\ECDFP_Course).
PROJECT.md entry doc · DECISIONS.md append-only log · Resources/ raw source (gitignored) ·
design/ planning · knowledge_base/ condensed reference · evidence/ PRIVATE acquisitions and
manifests (gitignored) · packages/session-NN/ the 9 instructor documents (not published) ·
cases/ investigations (answer_key.md always a separate, gitignored file) · labs/ · scripts/ ·
tools/ · testing/ · docs/ THE PUBLISHED SITE and the GitHub Pages root.
Live site: https://ebrahim-qareen.github.io/ecdfp-diploma/  (repo Ebrahim-Qareen/ecdfp-diploma)

STANDING RULES.
1. No versioned files (_v2, _final, dated copies). Edit in place, log one line in DECISIONS.md.
2. Never create scratch, zips or staging folders inside the project tree — the mount cannot
   delete, so litter is permanent. Build scratch outside and copy the finished file in.
3. Strict folder separation. Never mix planning, reference, published and instructor material.
4. PROJECT.md documents only folders that exist, and is updated in the same commit as any
   structural change.
5. One session at a time, fully approved before the next starts.
6. Never change INE's technical meaning — simplify the explanation only.
7. Every technical term: definition -> why it exists -> where used -> example -> case example.
8. Every artifact taught uses the 6-box template: what it is · where it lives (exact path) ·
   what it proves · what it does NOT prove · how to parse it (tool + command) · one
   anti-forensics / false-positive caveat.
9. Every lab ends with a verification step AND a chain-of-custody line
   (who · what · when · from where · hash · where stored).
10. Every investigation completes the arc: acquire -> verify (hash) -> analyse -> interpret ->
    document.
11. Evidence policy. Tier 1 our own lab acquisitions from the victim VM (primary), Tier 2 public
    corpora linked and credited never rehosted, Tier 3 synthesized only where valid (pcap via
    scapy, NDJSON logs, artifact CSV/JSON exports). Never claim to synthesize .evtx, E01, memory
    dumps or registry hives. Every challenge states its tier, source and MD5 + SHA-256, and Q1
    of every case is hash verification.
12. Forensic integrity: no real personal data, never commit evidence bytes, hash before and
    after, every case states provenance and licence.
13. The forensic report template is fixed from Session 1 and required every session:
    Case reference · Scope and authorisation · Evidence received (with hashes) · Tools and
    versions · Method · Findings (fact only) · Interpretation (clearly separated) · Conclusion ·
    Limitations · Exhibits. Findings vs Interpretation must be a visible, colour-coded
    distinction on every page.
14. Student-facing files contain ZERO instructor stage directions.
15. Never republish third-party material; credit and link instead.
16. No secrets anywhere, including labs/vm_notes/. Placeholders only.
17. Map findings to MITRE ATT&CK where relevant.

BUILD WORKFLOW — one session, ten steps, same every time.
0 Evidence check (verified + hashed, or the session does not start) -> 1 Scope confirm from
topic_map.md, minutes <= 220 -> 2 OUTLINE GATE: a page-by-page outline approved BEFORE any HTML
exists -> 3 the 9 package documents -> 4 the HTML page -> 5 the case -> 6 the lab only if it
changes -> 7 build_log.md -> 8 verification gate -> 9 review -> 10 publish. Never skip step 2.

SITE CONVENTIONS. One docs/session-NN/index.html with <body data-session="sNN">. Shared
docs/assets/css/ecdfp.css and docs/assets/js/ (session.js paged nav + break timer, homework.js,
quiz.js, task-creator.js). Never fork the stylesheet per session, never inline CSS/JS, never
regenerate a whole page for one change — edit the affected <section> only. Two allowed shapes:
Tier A concept session (~22 pages) for S1/S2/S3/S6, Tier B catalogue session (chapters of 8-15
micro-pages, each on the 6-box template) for S4/S5. Both must have the break page, mixed MCQ +
reveal questions, a cheat sheet with a Print button, #taskList homework + task-creator modal,
prev/next nav and kbd-hint, and a recap mapping to the previous session's takeaways. Wire every
session to docs/cheatsheets/, docs/resources/labs.html and the dashboard card on docs/index.html.
Diagrams are hand-authored inline SVG; arrows never cross label text; everything inside the
viewBox. Keep .page-layout > * { min-width: 0 } — it is load-bearing.

PUBLISHING. git push has no credentials in this environment. Commit on the mount if useful, but
the push happens through GitHub Desktop. Never run a git command that deletes refs or objects on
the mount (git gc, tag -d, branch -d) — deletes fail and leave lock files. Set gc.auto=0 and
maintenance.auto=false at init. Site root is docs/. Never enable cleanUrls or trailingSlash.
Run tools\precommit_scan.ps1 and tools\check_links.ps1 before every push.

WORKING STYLE. Be concise and direct, no preamble. Use a task list for multi-step work and end
with a verification step. When a real fork exists (scope, format, structure), ask ONE focused
multiple-choice question before building. Prefer doing over describing — create and edit real
files. Never block a build waiting for third-party content: build the INE spine and our own lab
evidence first, wire external links last.
```

## Step 3 — Add Project knowledge

**Add these:**

| File | Why |
|---|---|
| `00_INSTRUCTIONS.md` (the file next to this one) | the full reference |
| `PROJECT.md` | current status |
| `DECISIONS.md` | why things are the way they are |
| `design/coverage_matrix.md` | the locked domain map |
| `design/topic_map.md` | the locked sequence |
| `design/design_system.md` | the visual contract |
| `design/evidence_sets.md` | what evidence exists and is verified |
| The INE eCDFP PDFs | the source of truth |

**Never add:** anything with credentials · `labs/vm_notes/` · `cases/*/answer_key.md` · evidence images.

## Step 4 — Create the 6 skills (do this before Phase 1)

Paste this once:

```text
Create 6 Claude skills for this project, namespaced ecdfp-. One responsibility each, no overlap.
Read Part 11 of 00_INSTRUCTIONS.md for each skill's job and rules, and write each skill's
SKILL.md so it enforces those rules rather than restating them.

  ecdfp-intake            one source -> one knowledge_base/Module_0N_*.md + one topic_map row
  ecdfp-evidence          owns evidence_sets.md, manifests, sourcing tiers, hashing
  ecdfp-session-package   the fixed 9 markdown documents per session
  ecdfp-session-html      the fixed visual system for a session page (look only, never content)
  ecdfp-case              one investigation case, answer key always a separate file
  ecdfp-publish           scan -> commit -> push via GitHub Desktop -> verify live

Do NOT create a lab skill or a research skill — the lab is decided once by hand, and I already
have ceh-web-research and ceh-chrome-extract installed.
Deliver each as a .skill file I can save.
```

---

## Step 5 — The prompt for each phase

Run one phase per conversation. Start a new chat for each — it keeps context clean.

### Phase 0 — Scaffold
```text
Phase 0. Scaffold the project at E:\Work\ITgate\ECDFP_Course exactly as Part 2 of
00_INSTRUCTIONS.md defines it — only the folders Phase 0-1 need. Then write:
  PROJECT.md   (sections 1-7 as listed in Part 13 action 2)
  DECISIONS.md with D1-D10 already filled in from Part 0
  .gitignore   from Part 9
  a PowerShell script that creates the tree and runs git init with gc.auto=0 and
  maintenance.auto=false
Give me the script to run, then confirm the tree matches Part 2 exactly.
```

### Phase 1 — Design system + topic map (the phase that saves the most time)
```text
Phase 1, part A. Interview me with the Part 12 questions, one screen at a time, then write
design/scope_decisions.md from my answers and log each choice in DECISIONS.md.

Phase 1, part B. Transcribe Part 4 into design/coverage_matrix.md, then build
design/topic_map.md: one row per topic — Topic | INE source | Prerequisites | Session # |
Hands-on? | Est. minutes | Evidence needed. Minutes per session must total <= 220. If a session
does not fit, re-split it IN THE MAP and tell me — do not carry the overflow into the build.

Phase 1, part C. Write design/design_system.md, then docs/assets/css/ecdfp.css,
docs/assets/js/session.js, docs/assets/base_template.html and docs/index.html.
The colour tokens must include a distinct FINDING vs INTERPRETATION pair — that distinction is
the course's core lesson and must be visible on every page. Then render one throwaway page and
run the Part 9 verification gate on it. Do not build Session 1 until that gate passes.
```

### Phase 2 — Knowledge base
```text
Phase 2. Using ecdfp-intake, condense Resources/INE_eCDFP into knowledge_base/, one file per
INE module (Module_01..05). Extract text locally with pdftotext -layout first — do not read raw
pages. Never copy verbatim. After each module, add its topic rows to design/topic_map.md.
If any source is watermarked or its provenance is unclear, stop and tell me before extracting.
List every topic in the map that has no source as a gap in scope_decisions.md.
```

### Phase 3 — Lab + evidence (critical path — start it during Phase 2)
```text
Phase 3. Write labs/lab_design.md and labs/setup_guide.md from Part 6 of 00_INSTRUCTIONS.md —
one design, one guide, no versions. The setup guide must state the 250 GB host requirement up
front and be followable by a student with no help.
Then, using ecdfp-evidence, build design/evidence_sets.md: one row per evidence set for S1-S6 —
name, source URL, publisher, licence, format, size, MD5, SHA-256, contents, session, date
verified. Tier 1 (our EVI-SRC01 acquisitions) first; Tier 2 public corpora only where Tier 1
cannot cover it. Also write evidence/staging_scripts/ for the carry-through incident.
Flag any session whose evidence is not yet verified — those sessions cannot start.
```

### Phase 4 — Sessions, one at a time
This is the prompt you will use six times. Change the number only.
```text
Build Session N.
Step 0: confirm the evidence set for this session is in evidence_sets.md, verified and hashed.
Step 1: confirm scope against topic_map.md. Minutes total <= 220. No expansion.
Step 2: give me the page-by-page OUTLINE ONLY — page number, title, kicker tag, minutes,
        hands-on yes/no, which diagram, which evidence. Then STOP and wait for my approval.
        Do not write any HTML in this message.
```
After you approve the outline:
```text
Outline approved. Now build, in this order:
  1. packages/session-NN/ — all 9 documents (ecdfp-session-package)
  2. docs/session-NN/index.html (ecdfp-session-html) — Tier A or Tier B as the roadmap says
  3. the case in cases/ if this session ends in a full investigation (ecdfp-case)
  4. build_log.md
Then run the Part 9 verification gate and report the results as a checklist before I review.
```

### Phase 5 + 6 — Verify and publish
```text
Run the full Part 9 verification gate on session NN: render checks at 1400/1100/900/700/480
(the option key is `viewport`, NOT `viewportSize`), plus credential scan, PII scan, no-evidence-
bytes check, hash check, link check, time check, stage-direction scan and currency check.
Report as a pass/fail checklist. Zero findings, then prepare the exact GitHub Desktop commit
summary and the list of files to stage. Remind me to push manually.
```

---

## Step 6 — Rules for keeping the project healthy

| Do | Don't |
|---|---|
| One phase per conversation | Run two phases in one chat |
| Approve the outline before any HTML | Let Claude write HTML first "to show you" |
| Log every decision in `DECISIONS.md` the same day | Rely on remembering why |
| Edit files in place | Create `_v2`, `_final`, `_new` |
| Build scratch outside the project tree | Create scratch inside it — deletes fail on the mount |
| Verify evidence hashes before building a session | Build a session on evidence you have not downloaded |
| Push through GitHub Desktop | Try `git push` or browser automation |

**If a session goes over 240 minutes:** re-split it in `topic_map.md`, not in the build.
**If evidence is missing:** the session does not start. Move to the next one and come back.

---

## The one-page summary

```
6 sessions x 4h = 24h
S1 Foundations, Integrity & Chain of Custody      Fundamentals + Preservation
S2 Acquisition — Disk, Memory & Live Response     Preservation + Storage   <- carry-through case born
S3 Data Representation & File Examination         Fundamentals
S4 Storage Devices, Partitions & File Systems     Storage        (Tier B catalogue)
S5 Windows Forensics — Registry & Execution       Fundamentals   (Tier B catalogue)
S6 Network, Timelines, Reporting & Capstone       Tools & Techniques

Phase 0 scaffold -> 1 design system + topic map -> 2 knowledge base -> 3 lab + evidence
-> 4 sessions one at a time -> 5 verify -> 6 publish

Per session: evidence check -> scope -> OUTLINE GATE -> 9 docs -> HTML -> case -> log
             -> verify -> review -> publish
```
