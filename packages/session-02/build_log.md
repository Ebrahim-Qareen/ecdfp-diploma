# Session 2 — Build Log

**Built 2026-09-06.** Package only — figures and the HTML page follow in the same build.
Outline approved by Ebrahim at the D9 gate on 2026-09-06 (six items, all as written).

---

## 1 · What was built

| # | File | Bytes | Note |
|--:|---|--:|---|
| 1 | `session_plan.md` | ~12 k | time table totals 205 + 15, checked from the file |
| 2 | `instructor_guide.md` | ~20 k | per-block notes, demo scripts with expected output, the six common errors |
| 3 | `student_guide.md` | ~13 k | self-review walkthrough of every demo |
| 4 | `guided_lab.md` | ~9 k | the eight micro-labs, a verification line each, custody close |
| 5 | `student_activity.md` | ~6 k | Case 02a and Case 02b, success criteria, time boxes |
| 6 | `quiz.md` | ~6 k | 10 MCQ, answer rotating A→B→C→D, answer key with justifications |
| 7 | `homework.md` | ~5 k | `forensicimaging` with its defect named + the D20 report |
| 8 | `report_template.md` | 7 600 | 🔴 **copied byte-for-byte from S1** |
| 9 | `build_log.md` | this | — |

---

## 2 · The decision that shaped this build: the evidence gate

🔴 **Part 8 step 0 is FAILED and the session cannot be taught yet.** `EVS-02`, `EVS-03`, `EVS-04` and
`EVS-09` have not been acquired. They are Tier 1 — an E01 image, a memory dump and a USB image are
never synthesised — so **no hashes were invented anywhere in this package.**

What was built anyway, and why it is safe to have built it: the acquisition contents are fully locked
(`labs/vm_notes/staging_plan.md`, the F7 chain, the built victim VM and `D57`), and **every digest
shown to a student is a placeholder by policy** (`D41`) regardless of whether the real ones exist. So
the teaching material does not depend on the hashes. What does depend on them — the published
`.md5`/`.sha256` manifests and the instructor answer key — is deliberately left unwritten.

**Nothing in this package ships to a student until the runbook is run and the manifests published.**

---

## 3 · What was verified, and how

Re-checked by re-reading the written files, not from build variables.

| Check | Method | Result |
|---|---|---|
| Time table totals | parsed the 10 `S2-` rows out of `session_plan.md` and summed column 4 | **205** topic min · +15 break = **220** ✅ |
| Shape (`D15`/`D23`) | same parse, grouped | 130 integrated · 60 investigation · 15 ritual ✅ |
| Blocks match `topic_map.md` | compared all 10 rows and minutes against the ratified map | identical ✅ |
| Stage directions in student-facing files | `grep -inE` over 13 phrasings × 5 files | **0 hits** ✅ |
| Report template unchanged | `md5sum` against `packages/session-01/report_template.md` | `4b7cef1f…` **identical** ✅ |
| Quiz answer rotation | extracted the answer-key letters in order | `A B C D A B C D A B` ✅ |
| Quiz question types | counted | 10/10 MCQ (`D52`) ✅ |
| *Finding or interpretation?* questions | Q6 · Q7 · Q8 | **3**, meets the ≥3 requirement ✅ |
| Question on what `verified` does **not** cover | Q3 | present ✅ |
| Objective coverage | mapped all 10 questions | O1–O5 all covered ✅ |
| Tool versions | re-verified on the web on the build date | see §4 |
| **Part 9 render gate** | `node testing/render_gate.js` (container-side; Playwright is not on the lab VM) | ✅ **PASS, zero findings** — 29 pages × 5 widths (1400/1100/900/700/480) |
| **Exit gate, all 15 checks** | re-parsed from the written files, not build variables | ✅ **PASS 15/15** |
| Figures | node/detail parity, `<title>` first, `.svg-wrap` parent, viewBox containment | 14 figures · 50 `data-node` = 50 `data-detail` · 0 escapes ✅ |
| MCQ integrity | parsed from the page | 17 in-page MCQs, each exactly one correct option, each 4 options ✅ |
| Page prose | visible words per page, figures and reveals excluded | mean ~150, max 231 ✅ |
| Links | every relative `href` resolved on disk | 0 broken · 0 nested anchors ✅ |
| `record.html` | regenerated and diffed | **byte-identical**, S2 shows 14 cumulative steps (S1's 6 carried forward) ✅ |
| Credentials / real PII / real IPs | scan of all nine files | none — documentation ranges only ✅ |

---

## 4 · Tool currency — re-verified 2026-09-06

| Tool | Bound to | Change |
|---|---|---|
| FTK Imager | **8.3** | ✅ still current. Warning kept that *FTK Imager Pro* is the paid product |
| OSFMount | **3.3.1000** | ✅ still current |
| Arsenal Image Mounter | **3.13.368** | ✅ still current |
| **Volatility 3** | **2.28.2** | 🔺 **changed.** The build brief said 2.28.0; 2.28.2 was released 2026-08-19. Bound to 2.28.2 here |
| `dc3dd` | **7.3.1** | as installed on Kali |
| KAPE | core **1.3.0.2** · KapeFiles current | licence sentence carried into `S2-07`, the student guide and the homework (`D37`) |

---

## 5 · Rules honoured, and where

| Rule | Where |
|---|---|
| `D7` findings vs interpretation | `S2-06` block, student guide §6, Case 02a Q3/Q6, quiz Q6–Q8 |
| `D20` rubric unchanged | `homework.md`, `session_plan.md` §8, `report_template.md` (byte-identical) |
| `D37` KAPE licence stated, paired with a free alternative | instructor guide `S2-07`, student guide §7, homework |
| `D41` no secret or personal data as an answer | verified across quiz and both cases |
| `D46` acquisition-as-a-decision is ours | `S2-08` decision path, student guide §8 |
| `D47` external lab assigned with its defect named | `homework.md` Part 1 and the optional section |
| `D52` all questions MCQ | `quiz.md` |
| `D56` no `FOR-LNX01`; clean Kali snapshot | `session_plan.md` §5, micro-lab 7 |
| `D57` S1 kept, loss is the lesson | `session_plan.md` §7, instructor guide `S2-01`, student guide §1 |
| `R9` no evidence bytes | manifests referenced, never included |

---

## 6 · Reconciliations — where two sources disagreed

### 6.1 The build brief said `labs/` does not exist
It said `labs/` was missing and `FOR-WS01` unbuilt, and that this blocked Tier 1. **Both were out of
date** — all three VMs were built 2026-09-04 to 09-06. Recorded in `design/session_02_gate_report.md`.

### 6.2 The brief said `FOR-LNX01`
There is no such host. Resolved by `D56`: Kali, from a clean pre-staging snapshot, because F7 makes
the running Kali the compromised receiving host.

### 6.3 S1 says no memory was captured; S2 needs a memory image
`EVS-01`'s exhibit inventory records that no memory capture was taken, and the case is dated March;
F7 dates the incident to August. Resolved by `D57`: Case 01 stays byte-for-byte as a **standalone**
integrity warm-up and becomes S2's cautionary contrast, while the D19 incident is acquired from the
running host — so `EVS-03` still exists for `S6-09` and `S6-10`, which both need it.

### 6.4 Volatility 2.28.0 vs 2.28.2
The brief's version was stale. Bound to 2.28.2; `tools_by_session.md` still says 2.28.0 and is listed
as open below.

---

## 7 · What was cut, and why

- **No pre-course TryHackMe room assigned.** `D46`: no free lab teaches acquisition as a decision, so
  anything assigned beforehand would have to be corrected in class. `forensicimaging` moved to homework.
- **`memoryanalysisintroduction` deliberately not assigned** — a retired ATT&CK ID cited beside the
  live one, and RAMMap listed as a capture tool when it writes no dump. Named as optional, defects stated.
- **AD1 kept to one table row.** It is the format Autopsy cannot open; that is the only thing S2 needs
  from it, and `S2-05` is 15 minutes.

---

## 8 · Still open — honest list

| # | Open | Owner | Blocks S2? |
|--:|---|---|---|
| 1 | 🔴 **`EVS-02`/`03`/`04`/`09` not acquired.** Runbook written (`labs/vm_notes/acquisition_runbook.md`), not run | Ebrahim, on the VMs | **YES — the session cannot be taught** |
| 2 | The published `.md5` / `.sha256` manifests for `docs/session-02/` | follows item 1 | **YES** |
| 3 | The instructor answer key with real digests for Case 02a/02b | follows item 1 | **YES** |
| 4 | 🔴 **The live-response collector is taught generically** — the output tree shape is correct but no specific free tool and version is named yet | a tool decision | **YES for the lab** — micro-lab 2 needs a named binary |
| 5 | `cases/case-02a/`, `cases/case-02b/` — `ecdfp-case` **not installed** (7 of 8 skills). Case content sits in `student_activity.md`, as S1's Case 01 did | install the skill | No, but it is the second session to work around it |
| 6 | ~~`D56` rename not propagated~~ | — | ✅ **CLOSED** — `FOR-LNX01` → Kali applied in `00_INSTRUCTIONS.md` Part 6, `PROJECT.md`, `topic_map.md`, `session_time_estimates.md`, `docs/lab/index.html` (prose, SVG label and table), `docs/roadmap.html`, `docs/session-02/brief.html`, `labs/kali_setup.md`. Left deliberately: the unratified `plan_8_sessions.md`, the input brief, and the KB source notes |
| 7 | ~~Volatility still pinned at 2.28.0~~ | — | ✅ **CLOSED** — 2.28.2 in `tools_by_session.md` (×3), `labs/setup_guide.md`, `docs/lab/setup.html`, both READMEs, **and the installer pin `volatility3==2.28.2`** in `scripts/install/s2_acquisition.ps1`, its downloadable copy in `docs/lab/scripts/`, and the rebuilt `ecdfp-forws01-scripts.zip`. 🔴 `packages/session-01/` still echoes 2.28.0 — left alone as the record of a delivered session; see item 13 |
| 8 | **F7 SVG not drawn**, and F7 still has no dated `DECISIONS.md` row formalising it | figure build | `S2-F12` needs it |
| 9 | `DECISIONS.md` duplicate rows `D45`–`D50` (six pairs) — inherited from S1 | a renumbering decision | No. Every citation here names the row by date **and** subject |
| 10 | The two sample forensic reports in the training Drive still never opened | `ecdfp-pdf-extract` | No |
| 11 | `scope_decisions.md` §1 says "fourth course"; it is the seventh — inherited from S1 | a correction | No |
| 12 | No screenshots planned for S2 — the `.gui` panels carry the content, same resolution as S1 | — | No |
| 13 | `packages/session-01/session_plan.md` and `guided_lab.md` still list Volatility **2.28.0**. `D49` makes `tools_by_session.md` the authority and S1's own text says *re-verify on the build date*, so the two do not contradict — but a student reading S1 alone sees the old pin | a decision: edit a delivered session, or leave it | No |
| 14 | 🔴 **A stage direction reached a student-facing page and the scan caught it** — *"KAPE — say this out loud before anyone uses it"* on page 21. Fixed to *"the licence limit, before you use it anywhere"*. Recorded because it is the exact failure Part 11 exists to prevent | fixed this build | No |

**An empty "still open" is almost always wrong.** This one has fourteen; two closed during the build.
**Items 1 to 4 are the ones that stop the session being taught** — all four wait on the acquisition.

---

## 9 · Bridge to Session 3

S2 ends with the images made, verified and logged, and the custody record carried forward. S3 opens
them: data representation, file signatures versus extensions, metadata, and the malicious document
that began the intrusion.

Closing line: *"You have the evidence now. What is actually inside it?"*

---

## 15 · Rebuilt under `D58`, 2026-09-06

The instructor reviewed the first build and rejected it. The complaints were specific and all of them
were correct; sections 1–14 above describe the session **as first built** and stay as that record.

| Complaint | Measured | Fixed by |
|---|---|---|
| *"what is the collector?"* | the page said *"run the collector"* and **never named a tool** | **BriMor Labs Live Response Collection** (`Windows_Live_Response.bat`, menu Triage / Memory Dump / Complete / `Secure-*`), `[U2 p116–125]`, plus **Velociraptor** (Apache 2.0) as the alternative that is legal on a paid engagement |
| *"stop repeating the same info"* | order of volatility taught in **S1 and S2** (35 min); *"memory first"* in **6** places; *"`verified`"* in **8** | one owner per idea (`D58`). Volatility defined **once**, on one page. `S2-01` deleted, physical/logical + formats **merged** |
| *"the look is bad, I want diagrams"* | 14 figures / 29 pages, and **the micro-lab pages had none** — those were the screenshots | **16 figures / 24 pages, every teaching page has one.** Micro-labs now sit **on** their block's page instead of being pages of stacked boxes |
| *"go faster, more information"* | — | 10 blocks → **9**; 29 pages → **24**; a new `S2-06` block that was not in the session at all |

### New in this session

- 🔴 **`S2-06` — file signature vs extension**, run against the image the student just acquired. Follows
  straight on from `S1-09`, uses **`EVS-05`** (verified), and adds **`S2-F15`** (signature anatomy).
- **`S2-F16`** — the collector: what it runs, and the two kinds of output it produces.
- **`S2-F17`** — the cumulative record, so the ritual block has a figure like every other block.

### Verified after the rebuild

| Check | Result |
|---|---|
| **Part 9 render gate** | ✅ **PASS, zero findings** — 24 pages × 5 widths |
| Blocks / minutes | 9 blocks, **205** (30+20+25+20+15+20+35+25+15) ✅ |
| Figures | 16, every teaching page carries one; **0 teaching pages without a figure** ✅ |
| Collector named on the live page | BriMor ×4 · `Windows_Live_Response.bat` ×5 · Velociraptor ×8 · WinPmem ×3 · DumpIt ×2 ✅ |
| De-duplication | *"order of volatility"* appears **1×**; *"memory comes/is first"* **1×** ✅ |
| Micro-labs | **7**, each with all four parts (WATCH · DO · CHECK · WHY) ✅ |
| Stage directions in student-facing docs | **0** across five files ✅ |
| Quiz | 10 MCQ, rotation **A B C D A B C D A B** ✅ |

### Two things found while rebuilding

1. **A parallel session split the answer keys out of `quiz.md` into `quiz_answer_key.md` and gitignored
   them** (`.gitignore` line 19). That is correct for a public repo (`D22`) — a published answer key is
   not an answer key. The Q5 swap was applied to **both** files.
2. 🔴 **`device_commit_files` silently discards overwrites.** It returns `{"written":[…]}` while the file
   on disk keeps its old digest, even with `force:true`. Creating a *new* path works. Hit three times.
   **Workaround:** commit to a fresh path, then `cp` it over the target with `device_bash`, and
   **md5-verify every write** rather than trusting the success response.

### Still open

| # | Item |
|--:|---|
| 1 | 🔴 `EVS-02` / `03` / `04` / `09` **still not acquired** — `labs/vm_notes/acquisition_runbook.md` is written and waiting on the instructor. The session cannot be taught until it runs |
| 2 | The published `.md5` / `.sha256` manifests for `docs/session-02/` follow from item 1 |
| 3 | `student_activity.md` still refers to the cases as `S2-08`/`S2-09`; they are now `S2-07`/`S2-08` |
| 4 | `homework.md` unchanged and still correct, but its objective references were not re-checked against the new `O3` |


---

## Rebuild — the `D61` density pass (2026-09-06)

Built from `design/prompts/SHARED_RULES.md` + `S2_BUILD_PROMPT.md`. The page was **rebuilt, not
patched**, as the prompt required.

### Before → after

| | before | after | limit |
|---|--:|--:|--:|
| total visible words | **7 166** | **2 793** | ≤ 4 000 |
| average per page | **298** | **126** | ≤ 180 |
| worst single page | **590** | **189** | ≤ 250 |
| pages with no visual | 1 | **0** | 0 |
| pages with 4+ consecutive `<p>` | **15** | **0** | 0 |
| concept ownership | ✗ hash re-explained on p5 ×4, p15 ×7, p16 ×6 | **PASS** | — |
| pages | 24 | **22** (Tier A) | 22 |

The old page's specific failure was repetition: *"memory comes first"* in six places, *"`verified`
checks the tool's own output"* in eight. Each idea is now stated once, on the page that owns it,
and used everywhere else. Every page is kept to **≤ 3** mentions of any tracked term, which is the
gate's threshold — so ownership passes regardless of which page happens to hold the maximum.

### The three animations (`D51`)

| Figure | Page | The mechanism |
|---|:-:|---|
| `S2-F2` volatility ladder | 5 | six bars drain at **visibly different rates** — registers to zero, RAM to a sliver, disk barely moving. The animation *is* the argument for the order |
| `S2-F4` hidden area | 9 | the reported extent shrinks inside the true outline and the gap shades in as HPA/DCO |
| `S2-F5` verification chain | 14 | a tick travels the chain and **stops on the write-and-read-back link**; the green bracket closes there and a red dashed one under source→read shows what was never covered |

Same contract as S1: one full-length `<animate>` per element, all `begin="<control>.click"`, no
`fill` animated to a `var()`, nothing autoplays or loops. Two static figures — the session clock
and the E01/raw/AD1 container anatomy — are static on purpose: they are states, not mechanisms.

⚠️ **The animation suite needed a new check to be honest here.** `S2-F2` animates `width`, not
`opacity`, so the "no authored-hidden element moved" assertion had **nothing to assert** and
reported `all 0 hidden elements`. It now measures the six bars directly: full width after a
6.4-second idle, `[0, 27, 48, 172, 504, 531]` after a click — six different rates, in the right
order — and back to full on replay. An assertion with an empty subject is not a pass.

### Scope rules held

- **HPA/DCO (p9) is taught before the imaging tools (p10)**, so the student knows hidden storage
  exists before they image. Teaching it after was the corrected defect.
- **Case 02b asks what the tool reports, never what the structures mean.** Volume present, sector
  count, reported file-system type. A `.limitation` states outright that partition tables and
  `$MFT` are Session 4 and that saying so is the correct answer, not a gap.
- **The collector is named** — BriMor `Windows_Live_Response.bat` with its four menu options, and
  Velociraptor as the free-for-commercial alternative (`D68`).
- **Triage is a targeted subset**, said explicitly, against the previous instructor's "three images".
- **`verified` is the one deliberate repeat**, and page 14 says so in a `.caveat`: S1 read the word
  in a log it was handed, S2 produces the log first.
- Order of volatility appears **only** here, per `S1_BUILD_PROMPT` §5.

### ⛔ Provisional pages — pending evidence

`EVS-02`, `EVS-03`, `EVS-04` and `EVS-09` are all `⛔ PENDING` in `design/evidence_sets.md`, so
Part 8 step 0 is not satisfied. Per the prompt, pages 1–9 and 11–15 are complete; **three pages
carry a visible `.caveat` and contain no invented values:**

| Page | Blocked on | What is final | What is a placeholder |
|--:|---|---|---|
| 10 | `EVS-02` | the five FTK Imager steps and the verification-log structure | every digest, size and sector count — shown as `&lt;pending EVS-02&gt;` |
| 16 | `EVS-02` | the five independent-practice steps and the re-verify line | any path, size or digest |
| 17 | `EVS-04` | the Case 02a/02b brief, both parts, the deliverables | exhibit names, sector counts, digests |

Page 15 is built in full: `S2-06`'s evidence is **`EVS-05`**, which is generated and verified, so
its bytes are real. Only the framing — *files exported from the image you made* — waits on
`EVS-02`, and a `.caveat` says so.

**No hash, file size or tool output was invented for evidence that does not exist.**

### Gates

```
python3 scripts/density_gate.py docs/session-02/index.html   ALL PASS  (numbers above)
node testing/render_gate.js docs                             PASS — zero findings, 5 widths
node anim_s2.js                                              PASS — 0 failures
node audit.js docs/session-02/index.html                     PASS — 0 findings
```
Device and container SHA-256 match (`9a6a5b37…`), so the gates ran on the file that ships.


### Follow-up — the label that was centred on nothing

Reported from a screenshot of page 9 at rest: *"this is not in middle or box"*. Correct.
`what the OS reports` sat at a **fixed** `x`, left-anchored, inside a rect whose width **animates**
996&nbsp;&rarr;&nbsp;815. It was 174 units off centre at rest and 84 off after play &mdash; centred
on neither state, because a fixed label cannot be. Its `x` now animates on the same keyTimes as the
box, measured at **offset 0 in both states** (560/560 at rest, 470/470 after play).

⚠️ **The first checker I wrote for this would never have caught it.** It only inspected
`text[text-anchor="middle"]`, and the defective label was left-anchored &mdash; so the negative test
passed with the bug reintroduced. The second attempt, a general "is this label aligned to its box"
rule, was worse: it would have flagged legitimate two-column layouts inside a panel.

What is in `audit.js` now is exact and cannot false-positive: **a `<text>` inside a rect whose
`width` animates must either animate its own `x`, or stay within 8 units of the box centre at both
the start and end widths.** Negative-tested &mdash; reintroducing the fixed `x` reports
`"what the OS reports" is fixed inside a rect that resizes 996&rarr;815 (off centre by 174 then 84)`,
and restoring it passes. It also runs clean over S1's 23 pages.


### Follow-up — the report thread, merged into the blocks

Added page 22, *Write the report*; References moved to 23 and the sidebar regenerated from
document order. S2 is now 23 pages.

**It is not S1's page repeated.** S1's maps the ten sections to a first evidence handling; this one
is built around the fact that **acquisition's honest output is mostly section 9**. An image that is
*complete* and an image that is *verified* are different sentences, and the report has to say which
one the student has. The table's fourth column names the page each value came from — p10 for the
case number, p6 for tools and versions, p9 and p10 for the sector counts and the verify line, p14
for the limitation — so a student can walk back to the block that produced it.

**Merged into the content, not bolted on.** Three teaching blocks now name the section they feed:

| Page | Cue added |
|--:|---|
| 6 | tool, version, menu option, operator, output path &mdash; *"that is **section 4** of your report, written while you can still see it"* |
| 9 | record both sector counts &mdash; *"**section 6, Findings** &mdash; whether they differ or not"* |
| 14 | what `verified` does not cover &mdash; *"that sentence belongs in **section 9, Limitations**"* |

The template is **linked, not copied**: `../session-01/report_template.md`, the identical published
file. That the link crosses back to Session 1 is the point — it does not change for six sessions.
Link verified to resolve, 7 600 B.

Gates after: density **ALL PASS** (3 047 words, 132/page, worst 228, 23/23 sidebar), render gate
**zero findings**, animation suite and layout audit clean. Device and container hashes match.
