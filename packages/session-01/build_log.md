# Session 1 — Build Log

**Built 2026-08-30.** Instructor-facing. Never served.

---

## 1 · What was built

| # | File | Bytes | State |
|--:|---|--:|---|
| 1 | `session_plan.md` | 10,994 | complete |
| 2 | `instructor_guide.md` | 24,373 | complete |
| 3 | `student_guide.md` | 17,592 | complete |
| 4 | `guided_lab.md` | 11,137 | complete |
| 5 | `student_activity.md` | 6,543 | complete |
| 6 | `quiz.md` | 10,830 | complete |
| 7 | `homework.md` | 6,418 | complete |
| 8 | `report_template.md` | 7,600 | complete · copied to `docs/session-01/` |
| 9 | `build_log.md` | 14,951 | this file |

Also: `design/session_01_outline.md` (the D9 gate artifact) ·
`docs/session-01/index.html` and its twelve figures ·
`docs/session-01/img/` (five credited photographs, five pending captures).

`packages/` **did not exist before this build.** Created here — `PROJECT.md` §2 must be updated in
the same commit (`D11`).

---

## 2 · The decision that shaped everything: which session map

🔴 **The build brief was written against `design/session_map.md`, which is not ratified.**

That file says of itself *"Status: proposal, not yet ratified"*, and it contradicts **`D1`**
(6 × 4 h, locked) and **`D38`** (Linux out of scope). `coverage_matrix.md` is `★ LOCKED` at six
sessions. Nothing in `DECISIONS.md` supersedes either row.

**Decision taken 2026-08-30: S1 is built against `design/topic_map.md`, the ratified map.**

| | topic_map.md (built) | session_map.md (rejected) |
|---|---|---|
| Blocks | **10** | 13 |
| Topic minutes | **205** | 201 |
| Investigation | **60** | 45 |
| Physical vs logical acquisition | `S2-04` | S1 block 10 |
| Image formats E01/raw/AD1 | `S2-05` | S1 block 11 |
| Windows/Linux roadmap | not a row (`D38`) | S1 block 8, 10 min |

**The deciding factor was the investigation length.** `D15` and `D23` both name **60 minutes** of
blocked investigation explicitly. The proposal's 45 breaks the one number two locked decisions
agree on.

**Consequence:** three blocks in the brief were not built. Two are S2 topics and one is covered by
`D38` as a figure inside `S1-01` at zero session minutes — which is how it was built.

---

## 3 · What was verified, and how

Re-parsed from the written files, never from build-time variables.

| Check | Method | Result |
|---|---|---|
| Block minutes total 205 | regex-parsed the `session_plan.md` time table and summed it | ✅ **205** across 10 rows |
| Session shape matches `D15`/`D23` | computed from the parsed rows | ✅ **130 integrated + 15 break + 60 investigation + 15 ritual = 220** |
| Hands-on minutes | summed the hands-on rows | ✅ **158** — matches `topic_map.md`'s own block-check line |
| Outline per-page minutes reconcile to block totals | parsed both tables in `session_01_outline.md` and diffed | ✅ zero mismatches |
| Quiz structure | parsed question and answer-key headers | ✅ 10 questions · 6 MCQ · 4 short · 10 key entries · all 5 objectives mapped |
| Stage directions in student-facing files | pattern scan across 5 files | ✅ **CLEAN** — see §4 |
| Photograph integrity | `sha256sum -c` against Ebrahim's `SHA256SUMS.txt` | ✅ **5 of 5 OK** |
| `data-node` ↔ `data-detail` pairing | parsed the rendered HTML | ✅ **51 nodes / 51 details / 51 unique** — no orphans, no duplicates |
| **Part 9 render gate** | `testing/render_gate.js`, real headless Chromium | ✅ **PASS — zero findings.** 26 pages × 5 widths (1400/1100/900/700/480) = **130 page loads**, each a fresh `goto` per page (trap 2), option key `viewport` (trap 1) |
| Zero horizontal overflow · zero SVG outside `viewBox` · zero console errors · zero failed requests · page count = sidebar count | same run | ✅ all clean at every width |
| `role="img"` + `<title>` first child + `.svg-wrap` parent | parsed the HTML | ✅ **12/12** |
| No inline CSS or JS, no external script hosts, no diagram library | parsed the HTML | ✅ `<style>` 0 · inline `<script>` 0 · external script hosts 0 |
| Credentials · real PII · non-documentation IPs | pattern scan of the page | ✅ **0 / 0 / 0** — and 0 e-mail addresses |
| Every local `href`/`src` resolves | checked against the real tree | ✅ **9/9** |
| Every image carries alt text saying what to notice | parsed the HTML | ✅ 3/3, each containing an explicit *“Notice…”* clause |
| `R10` six boxes, box 4 not the shortest | parsed each `.artifact` | ✅ **3 artifacts, all six-box, box 4 the longest in each** |
| `EVS-01` marked `unverified` | parsed the HTML | ✅ named 9×, `unverified` stated, all digests `TBD` |
| External links | `NSRL` fetched and its quoted sentence confirmed verbatim | ✅ the NSRL page states *“Cryptographic hash values (MD5 and SHA-1) of the file's content. These uniquely identify the file even if, for example, it has been renamed.”* — which is what `S1-F8` cites. 6 remaining links listed in §12 for `tools\check_links.ps1` |

### A false positive worth recording

The first stage-direction scan flagged five lines in `homework.md` on the pattern `the room`.
**All five were false positives** — they refer to the *TryHackMe room*, not to the classroom. The
pattern was narrowed to the actual stage-direction phrasings (`ask the room`, `have the class`,
`what to listen for`, `on the board`, `expect them to`, …) and re-run.

> This is the fourth instance in this project of a checker being wrong rather than the content.

**And two more in the same build, both the same shape:**

- A `style="[^"]*"` scan reported 2 inline styles. Both were the tail of `font-style="italic"` — a
  substring match, not an inline style. (The 3 that *were* real, on the figure play controls, were
  removed into one shared `.svg-play` rule.)
- The content gate reported `../index.html` unresolved. It is resolved — the container copy of the
  tree simply had no `docs/index.html` in it. Re-run against the real tree: **9/9 OK.**

> **Read what the checker actually says before believing it.** Six instances now.

---

## 4 · Rules honoured, and where

| Rule | Where it bites in S1 |
|---|---|
| **`D7`** findings vs interpretation visible on every page | `S1-04` is 25 min and three pages; figure `S1-F1`; three quiz questions; `student_activity.md` Activity 1; the report template's §6/§7 split is a **section boundary**, not a heading colour |
| **`D20`** the four-criterion rubric, unchanged | published in `session_plan.md` §8, `report_template.md`, `homework.md`, `student_activity.md` — same four criteria, same wording |
| **`R10`** six-box artifact template | applied to the chain-of-custody form, the write blocker + proof trail, and `StorageDevicePolicies\WriteProtect` on the page. **Box 4 (*what it does NOT prove*) is the longest box in all three** |
| **`R9`** no evidence bytes | `EVS-01` is a specification and two manifests. No bytes anywhere |
| **`D16`** individual at the keyboard | Case 01 is solo; pairing appears once, on report peer-review only |
| **`D41`** no secret or PII as an answer | all six Case 01 questions and all ten quiz questions ask *which* / *what does this show*, never *what is the value* |
| **`D47`** external labs assigned with the defect named | `introdigitalforensics` (thin hashing task) · `caseb4dm755` (no recommend count, tool advice unverified) · `introtocoldsystemforensics` (🔴 **shown, never assigned**) |
| **`D48`** licence checked one version ahead | RegRipper 4.0, 010 Editor and Xiao Steganography are named in `S1-05` **as findings**, not omitted |
| **Part 11** zero stage directions in student-facing files | scanned, clean |

---

## 5 · Reconciliations — where two sources disagreed

### 5.1 The report template has two versions in the corpus

| Source | Sections |
|---|--:|
| `00_INSTRUCTIONS.md` Part 8 | **10** |
| `knowledge_base/Module_05` §2 | 13 |

**Resolved in favour of Part 8** — it is the project's single source of truth, and the
`ecdfp-session-package` skill restates its ten-section list as the fixed template.
`Module_05` §2's detail was used to fill each of the ten sections (rubric ownership per section,
the `F-07`/`I-03` line formats, the banned-word list, *write it as you go*).

⚠️ **`Module_05` §2's extra sections are not lost, only unranked:** executive summary, table of
contents, timeline/reconstruction, approvals. If S6's final report needs them, that is a template
change and therefore a `DECISIONS.md` row, not a quiet edit.

### 5.2 `tools_by_session.md` is written against the six-session map

Its §2 has six session tables and cites topic IDs `S1-06` / `S1-07`. **S1's tool substance is
unaffected** — the three-row S1 table is correct as written.

### 5.3 The prerequisite stack

`scope_decisions.md` §1 says *"fourth course after SOC → CEH → eCIR"*. The build brief says
**seventh**, after CCNA → MCSA → Linux Administration → SOC → CEH → eCIR.

**Built against seven** — it is a statement of fact about this cohort, not a scope decision, and
it only ever *raises* the assumed baseline. ⚠️ `scope_decisions.md` §1 should be corrected.

---

## 6 · What was cut, and why

| Cut | Reason |
|---|---|
| Figure: physical vs logical acquisition | `S2-04`. Not an S1 topic on the ratified map |
| Figure: image container anatomy (E01/raw/AD1) | `S2-05`. Same |
| Screenshot: FTK Imager `.txt` verification log | belongs with image formats — moved to S2. **Six shots became five** |
| Any figure for `S1-03` | a three-column table states relevant/reliable/competent more compactly than a diagram. **A diagram that re-labels the bullets beside it has failed** |
| `red-stealer` as a 15-minute demo | `S1-06` is 18 minutes total. Reduced to **5 minutes and two questions**; the full lab moved to additional practice |
| The write-protect registry demo (set → fail to reboot → write → reboot → fail) | needs more than `S1-08`'s 8 minutes. Described in one sentence; the full demo is S2's |

---

## 7 · OCR strings resolved before they reached a student

The knowledge base is OCR-derived and carries 100+ `⚠ verify against source page` markers. Those
touching S1:

| String | Source state | Resolved to | How |
|---|---|---|---|
| Order-of-volatility ladder | `[U2 p14]` is a graphic; **only the two ends survived OCR** | full 7-rung ladder taught (registers → archival) | reconstructed from outside the source. **Flagged in the instructor guide so nobody slides the source page** |
| `StorageDevicePolicies` path | OCR shows only the `CurrentControlSet\Control` fragment; screenshot shows `0x00000000` while prose says change "from 0" | `HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` → `REG_DWORD` `WriteProtect` = `1` | target value was implied, never printed. Stated explicitly |
| Both demo SHA-512 digests | truncated (`a545de…`, `34a593…`) | **not used** | every digest in S1 is generated live. `Get-FileHash`/`sha256sum` replace INE's `sha512sum` so the digest matches what students run |
| `Get-FileHash MDS` (instructor deck, slide 57) | `MDS` is OCR for `MD5`; prompt reads `IPS F:\>` for `PS F:\>` | **not used** | the deck's every digest resolves differently across three slides. Regenerated, never transcribed |
| FTK Imager acquisition dates | OCR renders 2017 as **2027** | **not used in S1** | S2 concern |

---

## 8 · The figures — twelve, and the animation decision

Renumbered **`S1-F1` … `S1-F12`**. `D40` reserves bare `F7` for the carry-through topology map and
`D38` reserves bare `F1` for the cross-platform table; bare `Fn` is now the project-wide namespace
and per-session figures carry the session prefix.

### ⚠️ Proposed decision row — figure-level animation

**Requested by Ebrahim 2026-08-30: animated, three-dimensional figures.**

`design_system.md` §5 is locked on *"hand-authored inline SVG only, no image files for diagrams,
no diagram libraries"*, and §8 rule 7 says *"animations only on section entrance. Nothing
decorative, nothing looping."* **A GIF breaks both.**

**Built as:** animated **inline SVG**, isometric where depth carries meaning, each driven by an
explicit **play / replay control** rather than an autoloop.

| | GIF | Animated inline SVG |
|---|---|---|
| Size | ~2 MB | ~8 KB |
| Projector / zoom | raster, blurs | vector, sharp at any scale |
| Dark theme | baked-in background | uses the CSS tokens |
| §5 | ❌ image file | ✅ inline SVG |
| §8.7 *nothing looping* | ❌ loops unattended | ✅ nothing moves until clicked |

**Proposed row, for confirmation:**

> **`D51`** — **A figure may animate when the animation shows a mechanism over time**, and only
> behind an explicit play/replay control. Autoplay and looping remain forbidden. Animation is
> hand-authored inline SVG (SMIL or CSS); no GIF, no video, no diagram library.
> *Why:* §8.7's intent is that nothing moves while an instructor is talking over the page. A
> click-to-play animation satisfies that intent while letting a figure show change over time,
> which is the one thing a static diagram cannot do.

**Not yet appended to `DECISIONS.md`** — awaiting confirmation.

---

## 9 · Images

**Five photographs, all sourced from Wikimedia Commons by Ebrahim, credited in
`docs/session-01/img/IMAGE-CREDITS.md`, and hash-verified on receipt: 5 of 5 `OK`.**

| File | Licence | Used in |
|---|---|---|
| `write-blocker-inline.jpg` | public domain (ErrantX) | `S1-08` |
| `write-blocker-ports.jpg` | public domain (ErrantX) | `S1-08` |
| `evidence-bag-sealed.jpg` | public domain (ErrantX) | `S1-07` |
| `hdd-open-inner-view.jpg` | CC BY-SA 3.0 (Eric Gaba) | ⏸ **held for S4** |
| `hdd-head-platter-detail.jpg` | CC BY-SA 3.0 (Eric Gaba) | ⏸ **held for S4** |

The two CC BY-SA files **must** carry their attribution line in the page caption. The public-domain
three are credited as good practice.

### Rejected

| File | Why |
|---|---|
| `Screenshot_1.png` | a frame from a copyrighted YouTube video (Branch Education). The repo is public (`D22`). Moved to `Resources/img_pending_licence/` (gitignored) |
| `Mobiles.jpg` | byte-duplicate of `evidence-bag-sealed.jpg` (`R1`). Moved to `_to_delete/` — the mount cannot delete, so Ebrahim removes it in Explorer |

🔴 **A request to cut GIFs from that video was declined.** Copyrighted third-party footage cannot
be rehosted in a public repo, whatever the framing. The mechanism it shows is HDD internals, which
is **S4** content, and is being built as an animated inline SVG instead.

### An error made and corrected in this build

The five photographs were moved out of `docs/` on a suspected licence problem **before
`IMAGE-CREDITS.md` — sitting in the same folder — had been read.** The licence work was already
complete and correct. All five were restored and re-verified against their recorded hashes.

> **Read the folder before acting on the folder.** The credits file was one `cat` away.

---

## 10 · Still open — honest list

| # | Open | Owner | Blocks |
|--:|---|---|---|
| 1 | ~~`design/evidence_sets.md` does not exist; `EVS-01` unverified~~ | — | ✅ **CLOSED 2026-08-30 (`D54`).** Built, verified by running it, and published. **Part 8 step 0 now passes.** See §14 |
| 2 | `cases/case-01-manifest/` — the 7-part case file and its **separate** answer key | `ecdfp-case` — **not installed** (7 of 8 skills) | Part 8 step 5. Case 01 currently lives inside `student_activity.md` |
| 3 | Five screenshots not captured | Ebrahim, on `FOR-WS01` | slots carry caption + alt text and **no `<img>` element**, so the link check passes meanwhile. **Less urgent than it was** — five `.gui` panels (`D53`) now carry the same content as styled text, including the real `sha256sum -c` output |
| 4 | `labs/` does not exist — `FOR-WS01` unbuilt | Part 6, by hand | the five captures, and Lab A step A1 |
| 5 | `D40`'s `F7` topology — `D19` expressed as numbered stages across **named hosts** | a decision row | `S1-F10` ships as a provisional stage strip |
| 6 | `DECISIONS.md` carries **duplicate rows `D45`–`D50`** — ⚠️ **a second `D50` was added by a parallel session while this build ran**, so it is now six pairs, not five — two blocks, same IDs, different content, both dated 2026-08-29 | a renumbering decision | nothing here; every citation in this package names the row by date **and** subject |
| 7 | ~~`D51` figure-animation row not appended~~ | — | ✅ **CLOSED 2026-08-30** — `D51`–`D54` appended. Append-only verified: 0 lines removed |
| 8 | The two sample forensic reports in the training Drive have never been opened | `ecdfp-pdf-extract` | nothing — `Module_05` §2 carried `S1-04`. Would still improve it |
| 9 | ~~`PROJECT.md` §2 does not list `packages/`~~ | — | ✅ **closed 2026-08-30** — tree updated, `packages/` and `docs/session-01/index.html` added, status rows appended. Diff verified: 4 lines removed, all intentional replacements |
| 10 | `scope_decisions.md` §1 says "fourth course"; it is the seventh | a correction | §5.3 |

**An empty "still open" on a first build is almost always wrong.** This one has ten, and item 1 is
the one that stops the session being taught.

---

## 11 · Bridge to Session 2

S2 inherits: the `CLEAN-TOOLS` snapshot · the report template unchanged · the rubric unchanged ·
the custody discipline · and `EVS-01` re-verified at the top of the session.

It also inherits the two blocks cut from this brief — **physical vs logical acquisition
(`S2-04`)** and **image formats (`S2-05`)** — plus the FTK Imager verification-log screenshot and
the full write-protect registry demo.


---

## 12 · External links, for `tools\check_links.ps1`

One was fetched and its quoted content confirmed (§3). The rest are listed rather than probed —
link checking on Windows is `check_links.ps1`'s job and it runs at publish time.

| Link | Where it is used |
|---|---|
| `https://www.kb.cert.org/vuls/id/836068` | `S1-06` · `S1-F8` — MD5 collision resistance |
| `https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm` | `S1-06` · `S1-F8` — SHA-1 retirement |
| `https://www.nist.gov/itl/csd/.../nsrl` | `S1-F8` — ✅ **fetched and confirmed 2026-08-30** |
| `https://cyberdefenders.org/blueteam-ctf-challenges/red-stealer/` | `S1-06` demo · additional practice |
| `https://tryhackme.com/room/introdigitalforensics` | pre-course task |
| `https://tryhackme.com/room/caseb4dm755` | homework |
| `https://tryhackme.com/room/irphilosophyethics` | optional homework |

`introtocoldsystemforensics` is named in the material and **deliberately not linked** — it is shown
on screen with the correction attached and must never be one click away from an unsupervised
student (`D47`).

---

## 13 · The figures as built

| # | Figure | Nodes | Animated | Notes |
|---|---|:-:|:-:|---|
| `S1-F1` | Finding · Interpretation · Cannot prove | 3 | — | 🔴 the course in one figure. The **connector line style matches the panel border style**, so the claim type is encoded twice |
| `S1-F2` | The evidence lifecycle | 7 | — | the mechanism is the red/green band: errors before `verify` are permanent, after it repeatable |
| `S1-F3` | Cross-platform artifact equivalence | 5 | — | strength bars, not a table — three Linux bars are zero |
| `S1-F4` | Order of volatility | 7 | ▶ | bars drain in proportion to survival time |
| `S1-F5` | Report template ↔ `D20` rubric | 4 | — | shows the imbalance: Findings has one section, Separation has three |
| `S1-F6` | Snapshot lineage | 3 | — | isometric |
| `S1-F7` | What a hash proves | 3 | ▶ | the avalanche: one letter changes, every hex digit changes |
| `S1-F8` | Lookup vs integrity | 2 | — | the wrong room marked on the wrong branch, named |
| `S1-F9` | Chain of custody as a timeline | 5 | — | hop 3 is deliberately absent |
| `S1-F10` | The `D19` case, six stages | 6 | — | ⚠ provisional — `D40`'s host map is open |
| `S1-F11` | Write blocking, two paths | 2 | ▶ | isometric. The write reaches the media above and is dropped below |
| `S1-F12` | The shape of a session | 4 | — | drawn to scale |

**Three animate, all behind a click, none loops.** Implemented as SMIL `begin="<id>.click"` — no
JavaScript, no library, nothing moves while an instructor is talking over the page.

⚠ **One implementation note worth keeping:** SMIL cannot interpolate a CSS `var()`, so animating
`fill` from `var(--text-secondary)` to `var(--accent-red)` renders white, not red. Cross-fade a
second shape instead — the tokens are preserved and the animation is correct.

**Two defects were caught by looking at the rendered figures**, not by any checker:
`S1-F4` left its survival labels stranded in space once the bars drained (fixed: a fixed
right-aligned column), and `S1-F11` printed its sub-labels across the isometric edges (fixed:
sub-labels moved below each slab). **Both are the exact flaw that made the reference GIF unusable.**


---

## 14 · Second pass, 2026-08-30 — five changes on request

| # | Asked for | Done |
|--:|---|---|
| 1 | every question multiple choice | 12 in-page reveals converted → **23 MCQ**; `quiz.md` 6 MCQ + 4 short → **10 MCQ**. `D52` logged, and `design_system.md` §4.2's mixed-format rule struck through rather than deleted |
| 2 | bigger titles, content filling more of the page | `h1` → 3.1 rem, `h2` → 1.9 rem **with a cyan left rule**, `h3` → 1.22 rem · `--content-max` 1000 → **1320 px** · `--sidebar-w` 260 → 240 |
| 3 | more colour on the important parts | page kicker as a cyan state pill · `mark`/`.key` amber inline highlight · inline `<code>` on a cyan tint · tables as rules with a mono uppercase header and a row hover |
| 4 | a small visual beside the content, GUI view | **`.split`** + **`.gui`** — five panels: the snapshot tree, `Get-FileHash` before/after, `sha256sum -c` with its real 3 `OK` / 1 `FAILED`, the custody form as a field list, and the closing custody line |
| 5 | check the labs | see §15 |

All of it is in `ecdfp.css` **section 15** and documented in `design_system.md` §2, §4.4, §4.5 and
§7. Nothing was inlined and the stylesheet was not forked (`D53`).

**Re-verified after the change — the gates were re-run, not assumed:**

| | |
|---|---|
| Part 9 render gate | ✅ **PASS, zero findings** — 26 pages × 5 widths, again |
| Structure | 26 pages = 26 sidebar entries · 12 figures · **51 `data-node` / 51 `data-detail`** · 0 inline `<style>` · 0 inline `<script>` |
| `TBD` placeholders remaining in the package | **0** |

---

## 15 · The labs — what is actually available

🔴 **The Drive folder that would supply lab evidence is not on disk.**
`Resources/DRIVE/` holds **only `drive-inventory.md`**.

| Came down from the Drive | Did not |
|---|---|
| 8 lecture PDFs (Sessions 1–8) | 🔴 **`Cases/`** — the six evidence-set folders |
| 10 INE unit PDFs | `Digital forensics reports/` — the two sample reports |
| | `Tools/` · `cheatsheets/RegRipper-plugins.csv` |

`Resources/Instructor/Lectures PDF/` is an **empty folder** — the zip beside it was never extracted.

⚠️ And even when it arrives, `Cases/` is **not a usable source until its provenance is
established**. Six folders whose contents have never been enumerated; if they are copies of public
corpora, `D22` says link and credit, never rehost.

**So S1's lab depends on none of it, and should not.** The three sources it does use:

| Source | Tier | Role |
|---|:-:|---|
| **`EVS-01`** — ours, generated, verified | **1** | the 60-minute investigation. Built this pass (`D54`) |
| **CyberDefenders `red-stealer`** | 2 | shown in `S1-06` as a hash-as-lookup-key demo. Linked, never rehosted |
| **TryHackMe** `introdigitalforensics` (pre-course) · `caseb4dm755` (homework) · `irphilosophyethics` (optional) | 2 | linked, each with its known defect named in the assignment text (`D47`) |
| **TryHackMe `introtocoldsystemforensics`** | 2 | 🔴 **shown on screen only, never assigned, never linked from the page** — it recommends MD5/SHA-1 for integrity |

**What is still missing is `EVS-02`, and it is the critical path.** S2 needs a real disk image of a
real staged host — not a text file, and not something the Drive can supply. Part 8 step 0 will fail
for S2 exactly as it did for S1.
