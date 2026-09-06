# session_01_outline.md — S1 page-by-page outline

**Part 8 step 2 · the OUTLINE GATE (`D9`).** Nothing in `packages/session-01/` or
`docs/session-01/index.html` exists until this is approved.

**Built against `design/topic_map.md`, the ratified map** — not `design/session_map.md`, which is
still marked *"proposal, not yet ratified"* and contradicts `D1` and `D38`. Decision taken
2026-08-29: S1 is the **10-topic / 205-minute** shape.

---

## 1 · The blocks — 10 topics, 205 min

| ID | Block | Min | Domain | Hands-on | Pages |
|---|---|--:|:-:|:-:|---|
| `S1-01` | What digital forensics is — the mandate, the evidence lifecycle, what an investigator may not claim | 15 | `F` | No | 5–6 |
| `S1-02` | Forensic principles — order of volatility, minimal footprint, repeatability, always work on a copy | 20 | `F` | No | 7–8 |
| `S1-03` | What makes evidence defensible — relevance, authenticity, integrity | 12 | `F` | No | 9 |
| `S1-04` | **The fixed forensic report template — findings vs interpretation (`D7`)** | **25** | `F` | Yes | 11–13 |
| `S1-05` | Analyst toolkit install and the `CLEAN-TOOLS` snapshot | 20 | `T` | Yes | 14–15 |
| `S1-06` | Cryptographic hashing — MD5, SHA-256, what a hash proves and what it does not | 18 | `T` | Yes | 17–18 |
| `S1-07` | Chain of custody — the form and the discipline | 12 | `P` | Yes | 19 |
| `S1-08` | **Write blocking — hardware vs software, and how to prove one was used** | 8 | `P` | Yes | 20 |
| `S1-09` | **[INVESTIGATION]** Case 01 — verify 4 files against a signed manifest, find the tampered one | **60** | `P` | Yes | 21–22 |
| `S1-10` | **[RITUAL]** Hash-verify + chain-of-custody close | 15 | `P` | Yes | 24 |
| | **Total** | **205** | | **158 min hands-on** | |

**Shape check (`D15` / `D23`)** — integrated `S1-01`…`S1-08` = **130** · break **15** ·
investigation **60** · ritual **15** = **220** teaching, inside a 240 slot. Exact, not approximate.

**Where the break falls.** After `S1-05`, at minute 92. The `CLEAN-TOOLS` snapshot is started at the
end of `S1-05` and completes during the break — the machine works while the room does not. Second
half is 38 min teaching + 60 investigation + 15 ritual.

**Two blocks the earlier draft brief put in S1 are `S2`, and are not built here:** physical vs
logical acquisition (`S2-04`) and image formats E01/raw/AD1 (`S2-05`). The FTK Imager verification
log screenshot goes with them.

---

## 2 · Page-by-page — 26 pages, Tier A

Tier A is nominally ~22 pages. S1 runs 26 because `S1-04` earns three pages and the investigation
earns two. Recorded as a deliberate deviation in `build_log.md`.

| # | Page | Tag | Block · min | Hands-on | Figure | Shot | Check for understanding |
|--:|---|---|---|:-:|---|:-:|---|
| 1 | Cover — *Forensic Foundations, Evidence Integrity & Chain of Custody* | `cover` | — | — | — | — | — |
| 2 | How this session works — the finding / interpretation / cannot-prove / CoC components, live | `frame` | — | — | **S1-F12** | — | — |
| 3 | Objectives, and the rubric you are graded on from today | `frame` | — | — | — | — | — |
| 4 | Case hook — the seizure. Nothing has been analysed yet | `hook` | — | — | **S1-F10** | — | — |
| 5 | The mandate, and the evidence lifecycle | `theory` | `S1-01` · 8 | — | **S1-F2** | — | reveal: *name the phase that destroys the next one* |
| 6 | What an investigator may not claim — and why this course is Windows-weighted | `theory` | `S1-01` · 7 | — | **S1-F3** | — | reveal: *read down the Linux column — what is it an argument for?* |
| 7 | Order of volatility — and the case where the rule inverts | `theory` | `S1-02` · 10 | — | **S1-F4** | — | mcq: *which do you collect first, and what does it cost* |
| 8 | Minimal footprint · repeatable vs reproducible · always work on a copy | `theory` | `S1-02` · 10 | — | — | — | reveal: *repeatable or reproducible?* ×3 |
| 9 | Defensible evidence — relevant · reliable · competent | `theory` | `S1-03` · 12 | — | — | — | mcq: *the warrant covered text files; the video convicts. Admissible?* |
| 10 | **Knowledge check 1** — `S1-01` … `S1-03` | `check` | — | — | — | — | 4 questions, mcq + reveal |
| 11 | **Finding · Interpretation · Cannot prove** — one artifact, three sentences | `theory` | `S1-04` · 9 | — | **S1-F1** ★ | — | mcq: *classify each of three sentences* |
| 12 | The fixed report template — thirteen sections, four rubric criteria | `theory` | `S1-04` · 8 | — | **S1-F5** | — | reveal: *which section owns criterion 4?* |
| 13 | Writing `F-01` and `I-01` — the two line formats, and the banned words | `guided` | `S1-04` · 8 | **Yes** | — | — | **task:** rewrite three contaminated findings |
| 14 | Lab setup — the kit, its versions, and the three tools that cannot ship | `setup` | `S1-05` · 6 | — | **S1-F6** | — | reveal: *why is RegRipper pinned at 3.0?* |
| 15 | Guided hands-on — install · verify · snapshot `CLEAN-TOOLS` | `guided` | `S1-05` · 14 | **Yes** | — | **1** | verification line + CoC line |
| 16 | **Break — 15 minutes.** The snapshot finishes while you are out | `break` | — | — | — | — | `data-timer="15"` |
| 17 | What a hash proves — and the three outcomes | `theory` | `S1-06` · 8 | **Yes** | **S1-F7** | **2** | mcq: *the hashes match. What may you write?* |
| 18 | Two different questions — lookup vs integrity. And a published room getting it wrong | `theory` | `S1-06` · 10 | **Yes** | **S1-F8** | **3** | reveal: *find the error in this 2025 room* |
| 19 | Chain of custody — the form, the discipline, and the hop that is missing | `theory` | `S1-07` · 12 | **Yes** | **S1-F9** | **4** | mcq: *which hop fails, and what does that let the other side argue?* |
| 20 | Write blocking — and how you prove you used one | `theory` | `S1-08` · 8 | **Yes** | **S1-F11** | — | reveal: *name the four parts of the proof trail* |
| 21 | Case 01 — the brief, the evidence, the questions | `case` | `S1-09` · 10 | **Yes** | — | **5** | Q1 is always hash verification |
| 22 | Case 01 — the investigation, and writing it up as a finding | `case` | `S1-09` · 50 | **Yes** | — | — | six questions, one answerable only *"cannot prove"* |
| 23 | **Knowledge check 2** — `S1-04` … `S1-09` | `check` | — | — | — | — | 5 questions; 3 are *finding or interpretation?* |
| 24 | The closing ritual — hash-verify and chain-of-custody close | `ritual` | `S1-10` · 15 | **Yes** | — | — | every student signs one custody line |
| 25 | Summary, cheat sheet and takeaways (Print) | `summary` | — | — | — | — | — |
| 26 | Homework, the report, additional practice and references | `close` | — | — | — | — | `#taskList` + task-creator |

**Break page is 16, not 12** — the Tier A default assumes an even split; S1's break sits at minute
92 of 205 because the snapshot has to run through it.

---

## 3 · The twelve figures — renumbered `S1-Fn`

**Renumbered on purpose.** `D40` reserves the bare `F7` for the carry-through topology map drawn
once and reused on every session page, and `D38` reserves `F1` for the cross-platform table. Bare
`Fn` is now the project-wide namespace; per-session figures carry the session prefix.

| # | Figure | Page | Mechanism / comparison / consequence it shows | `data-node` interaction |
|---|---|:-:|---|---|
| **S1-F1** | 🔴 **Finding · Interpretation · Cannot prove** | 11 | One artifact, three branches: what it *states* · what an analyst *concludes* · what it **cannot** reach. Solid / dashed / dotted borders carry the meaning without colour | 3 nodes → the worked triple from `Module_01` §4 behind each |
| **S1-F2** | The evidence lifecycle | 5 | seize → acquire → verify → analyse → interpret → document → present, with the destructive coupling drawn: each phase can destroy the next | 7 nodes → what goes wrong at that stage, and which session teaches it |
| **S1-F3** | Cross-platform artifact equivalence | 6 | Windows artifact ↔ its Linux counterpart, five rows, every Linux cell visibly weaker — no `USBSTOR`, login records deleted, `.bash_history` undated | 5 nodes → the specific weakness, from `thm/exfilnode.md` |
| **S1-F4** | Order of volatility as a ladder | 7 | Seven rungs with survival windows, registers → archival media | 7 nodes → **what you destroy by collecting the rung below first** |
| **S1-F5** | The report template against the `D20` rubric | 12 | Thirteen sections down one side, four criteria down the other, lines joining section to criterion — showing three sections carry Integrity and three carry Separation | 4 nodes (criteria) → what full marks look like |
| **S1-F6** | Snapshot lineage | 14 | `CLEAN-BASE` → `CLEAN-TOOLS` → per-case working state, with the arrow back to each | 3 nodes → what a roll-back to that point costs you |
| **S1-F7** | What a hash proves | 17 | file → function → digest, then match · mismatch · collision — three outcomes, three different sentences | 3 nodes → **the sentence you may write, and the sentence you may not** |
| **S1-F8** | Two different questions | 18 | A fork: *"seen this file before?"* → lookup, MD5 acceptable · *"is this unaltered?"* → SHA-2/3 only. `introtocoldsystemforensics` marked on the wrong branch, named | 2 nodes → NSRL on one, CERT/CC VU#836068 + NIST SHA-1 retirement on the other |
| **S1-F9** | Chain of custody as a transfer timeline | 19 | Five hops, each carrying who · when · why · hash. **Hop 3 is deliberately broken** | 5 nodes → the entry that must exist; hop 3 → what the gap lets the other side argue |
| **S1-F10** | The `D19` case, six stages | 4 | The intrusion chain, S1's slice lit and the rest dimmed. ⚠ **Provisional** — `D40`'s prerequisite (D19 as numbered stages across *named hosts*) is still open, so this ships as a stage strip, not a topology | 6 nodes → which session cuts in there |
| **S1-F11** | Write blocking — the data path | 20 | Two paths side by side: unprotected (writes reach the media) and blocked, with hardware inline vs software driver drawn at the point each intercepts | 2 nodes → **the proof trail: before/after source hash · tool log · photograph · custody line** |
| **S1-F12** | The shape of a session | 2 | 240 slot → 220 teaching → 130 integrated · 15 break · 60 investigation · 15 ritual. Real numbers | 4 nodes → what happens in that segment |

**Dropped as decorative or out of scope**, recorded here so the decision is visible:
physical vs logical acquisition (`S2-04`) · image container anatomy (`S2-05`) · any figure for
`S1-03`, where a three-column table states the test more compactly than a diagram can.

---

## 4 · Screenshots — five, all `CAPTURE PENDING`

Ebrahim captures these on `FOR-WS01`. **Until the files land, each slot renders as an empty
bordered placeholder carrying its caption and its alt text — no `<img>` element and therefore no
unresolved `src`**, so the Part 9 link check passes on an imageless page. Swapping a placeholder
for the real `<img>` is a one-line edit per shot.

| # | File | Shows | Page | What the reader must notice (becomes the alt text) |
|--:|---|---|:-:|---|
| 1 | `img/clean-tools-snapshot.png` | The `CLEAN-TOOLS` snapshot in the hypervisor's snapshot manager | 15 | that there is a named point you can always return to, taken *before* any evidence is touched |
| 2 | `img/get-filehash-sha256.png` | `Get-FileHash -Algorithm SHA256` in PowerShell, with the version banner | 17 | the algorithm is stated explicitly — the default is not SHA-256 on every host |
| 3 | `img/sha256sum-check-failed.png` | 🔴 `sha256sum -c` over four files — three `OK`, one `FAILED` | 18 | **the mismatch being caught.** The single most important image in the session |
| 4 | `img/custody-form-completed.png` | The completed chain-of-custody form | 19 | it is a document, not a tool output — no software produced it |
| 5 | `img/manifest-in-editor.png` | The signed manifest open in a text editor | 21 | a manifest is a text file and nothing more |

Each capture is specified command-by-command in `packages/session-01/build_log.md` §Screenshots:
exact command, tool version, window to frame, what must be legible, what must not be on screen.
**No screenshot comes from TryHackMe, CyberDefenders, INE or the instructor decks** — the repo is
public (`D22`) and the decks carry a real Windows SID and a personal email address.

---

## 5 · `EVS-01` — specified, not faked

`design/evidence_sets.md` does not exist and `ecdfp-evidence` owns it. This is the **specification**
the session is written against; every hash reads `TBD` and every mention says `unverified` until
that skill generates the set and publishes the manifest.

**Tier 1 — generated in our own lab.** Four plain-text files, ~2–8 KB each, deterministic from a
generator script so the set is reproducible and any student's copy is diffable against ours.

| # | File | What it is |
|--:|---|---|
| 1 | `seizure_notes.txt` | the first responder's contemporaneous notes at the desk |
| 2 | `EVI-SRC01_acquisition_log.txt` | 🔴 **the tampered file** — the imager's own log |
| 3 | `custody_form_EVI-SRC01.txt` | the completed chain-of-custody record |
| 4 | `evidence_inventory.csv` | the three exhibits, one row each |
| — | `EVS-01.sha256` · `EVS-01.md5` | the signed manifest, both algorithms (`D18`) |

**Why the acquisition log is the file that was altered.** It is the file whose *content is the
integrity claim*. One character of one timestamp is changed — invisible to the eye, fatal to the
digest. The lesson lands exactly where `Module_01` §6 says students fail: *"verified" means the tool
checked its own output*, and a log is documentation of an acquisition, not evidence of one.

**Constraints on the content (`R8`, `R9`, `D41`):** fictional company and users, no real personal
data, documentation IP ranges only (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`), no
credential anywhere, and **no question in the case has a secret or a person's data as its answer**.
No evidence bytes enter the repo — the manifest and the hashes only.

---

## 6 · Assessment

**`quiz.md` — 10 questions**, mixed `.q.mcq` and `<details>` reveal, each mapped to an objective.
Four are `S1-04` — the block is the point of the diploma and the quiz has to weight it:

- **≥ 3** present an artifact and ask *"finding or interpretation?"*
- **≥ 1** asks what a hash match does **not** prove
- **≥ 1** has the correct answer *"this artifact cannot prove that"*
- **1** is the `introtocoldsystemforensics` sentence, quoted, asking what is wrong with it

**`homework.md`** — the graded practical plus the report, on the fixed `D20` rubric:

| What | Source | Why this one |
|---|---|---|
| **THM — Digital Forensics Case B4DM755** (`caseb4dm755`, free, ~120 min) | linked, never rehosted | evidence framed as work that has to survive a courtroom — that framing *is* `S1-07`, and it is rare. The S1 → S2 bridge |
| **The report**, sections 4 · 5 · 6 · 7 · 9 for Case 01 | ours | first pass at the template. Graded on all four criteria; criterion 4 is where everyone loses marks |
| *Optional, 40 min* — THM `irphilosophyethics` | linked | the *why*, for anyone who asks |

**Pre-course task, issued before S1:** THM **Intro to Digital Forensics** (`introdigitalforensics`,
free, ~90 min). Covers `S1-01`, `S1-02` and part of `S1-07`, so S1 opens on shared vocabulary rather
than definitions. ⚠ Its hashing task is thin — the assignment text says so, and students still get
`S1-06` from us.

**`D47` is honoured on every external link:** each is assigned with its known defect named in the
assignment text.

---

## 7 · What this outline does not cover, and who owns it

| Open | Owner | Blocks what |
|---|---|---|
| `design/evidence_sets.md` does not exist; `EVS-01` unverified, no hashes | `ecdfp-evidence` | Part 8 step 0. The guided lab and Case 01 print `TBD` until it runs |
| `cases/case-01-manifest/` — the 7-part case file and its separate answer key | `ecdfp-case` — **not installed** (7 of 8) | Part 8 step 5. Case 01 ships inside `student_activity.md` for now |
| `D40`'s `F7` topology — `D19` as six numbered stages across *named hosts* | a decision row | `S1-F10` is a provisional stage strip until then |
| `labs/` does not exist — `FOR-WS01` unbuilt | Part 6, by hand | the five screenshots, and `S1-05`'s step 1 |
| The two sample forensic reports in the training Drive, never opened | `ecdfp-pdf-extract` | nothing — `Module_05` §2 carries `S1-04`. Would improve it |
| `DECISIONS.md` has duplicate rows `D45`–`D49` | a renumbering decision | nothing here; cited precisely by date + subject instead |

---

## 8 · Deliverables this outline authorises

```
packages/session-01/     session_plan · instructor_guide · student_guide · guided_lab
                         student_activity · quiz · homework · report_template · build_log
docs/session-01/index.html    26 pages, 12 inline-SVG figures, 5 pending shot slots
docs/session-01/img/          empty until the captures land
docs/session-01/report_template.md   the student copy (Part 8)
```

`packages/` does not exist yet. Creating it updates `PROJECT.md` §2 in the same commit (`D11`).
