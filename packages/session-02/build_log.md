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
