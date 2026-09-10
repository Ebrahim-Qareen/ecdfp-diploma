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

---

## 16 · Re-cut under `D58`, 2026-09-06

Instructor review of the built S2 page found that **order of volatility was taught in this session
*and* in S2 — 35 minutes for one idea** — and that S1+S2 together held 46 % of the course's pure
lecture time, so a student first met hex at hour 9 of 24. `D58` re-cut the roadmap. Sections 1–15
above describe the session **as first built** and are left as the record of that build.

### What changed in this package

| | Before | After |
|---|---|---|
| `S1-01` mandate | 15 min, 2 pages | **10 min**, merged to 1 page |
| `S1-02` principles | 20 min, 2 pages — included order of volatility | **10 min**, 1 page. **Volatility removed — `S2-01` owns it** |
| `S1-03` defensible evidence | 12 min | **10 min** |
| `S1-05` toolkit | 20 min, 2 pages | **15 min**, merged to 1 page |
| — | — | 🔴 **`S1-09` NEW — Inside a file: hex, magic bytes, 22 min, hands-on** |
| Case 01 | `S1-09` | renumbered **`S1-10`** |
| Ritual | `S1-10` | renumbered **`S1-11`** |
| Objective **O1** | *sequence a collection by order of volatility* | ***identify a file from its first bytes; the name is not evidence*** |
| Quiz **Q5** | the wiper / volatility scenario | a hex-signature finding-vs-interpretation question |
| Figure `S1-F4` | order-of-volatility ladder | **removed with its page** |
| Figure — | — | 🔴 **`S1-F13` NEW** — the name vs the bytes, with the four signatures |
| Page count | 26 | **24** |
| Break | minute 92 | minute **70** (still after `S1-05`, so the snapshot runs through it) |

### Verified after the re-cut, by re-parsing the written page

| Check | Result |
|---|---|
| Block minutes | **205** (10+10+10+25+15+18+12+8+22+60+15) ✅ |
| Pages = sidebar entries, ids `p1..p24` with no gaps | ✅ |
| `data-node` / `data-detail` parity | ✅ |
| 12 figures, all `role="img"` with `<title>` first | ✅ |
| No S1 page **teaches** order of volatility | ✅ — the only hits left are the INE syllabus-mapping table (which describes what Unit 2 *contains*), the `D58` note, and the S2 bridge |
| `S1-F4` gone; `S1-F13` present | ✅ |
| Zero nested anchors, no inline style or script | ✅ |
| **Part 9 render gate** | ✅ **PASS, zero findings** — 24 pages × 5 widths |

⚠️ The gate first reported 360 findings, all `ERR_FILE_NOT_FOUND` for `img/*.jpg`. That was the
container sandbox missing the five photographs, **not the page**. Staging them gave a clean pass —
the seventh time in this project a checker was wrong rather than the content.

### Open, carried into the next pass

| # | Item | |
|--:|---|---|
| 1 | ~~`guided_lab.md` and `student_activity.md` lack the `S1-09` micro-lab~~ | ✅ **CLOSED** — `guided_lab.md` gained **Lab C** (5 steps: read the bytes, build the 12-row table, prove renaming changes nothing, write it as a finding, state what it cannot show); `student_activity.md` gained **Activity 2** and Case 01 renumbered to Activity 3 |
| 2 | ~~The hex micro-lab has no evidence set~~ | ✅ **CLOSED** — **`EVS-05` generated and verified** (`scripts/make_evs05.py`): 12 files, **exactly 5 lying extensions**, 2 truncated. Deterministic, regenerated and diffed byte-identical |
| 3 | ~~`homework.md` assigns against the old objective numbering~~ | ✅ **CLOSED** — gained **Part 1b**, ten minutes on the student's own machine, ending on *name one innocent reason an extension might not match* |
| 4 | 🔴 **S1 has 6 teaching pages with no figure** | Open. S1 predates the every-teaching-page-a-figure standard that S2 (16 figures / 24 pages) and S3 (12 / 22) now meet, so S1 now looks thinner than the sessions after it |
| 5 | The `verified` lesson is taught here **and** in `S2-04` | Open, and **deliberate** — S1 reads it in a log it was *handed* (`EVS-01`'s tampered file **is** that log; it is the whole of Case 01), S2 in a log the student *produced*. Documented as the one exception to `D58`'s ownership rule in `topic_map.md` |


---

## Pass 5 — the `D51` animation and visual-quality pass (2026-09-06)

Brief: `design/prompts/SHARED_RULES.md` + `design/prompts/S1_BUILD_PROMPT.md`.
The page already passed both gates (2,902 words / 131 per page / render-clean). The job was to
raise the visual ceiling **without losing a gate**, so every change was re-measured.

### The four animations (`D51` — click to play, no autoplay, no loop)

| # | Figure | Page | The mechanism it shows that a static picture cannot |
|--:|---|:-:|---|
| 1 | **`S1-F4` the avalanche** | 8 | Digest B is `????` at rest. On play it resolves in four staggered groups through two scramble frames into a digest with **nothing** in common with A. Readout flips `? of 64` → **`0 of 64` characters shared** |
| 2 | **`S1-F5` the custody gap** | 13 | Four handovers light green left to right; the fifteen-hour link stays dark, takes a red ring, and a dashed box **grows outward from it** |
| 3 | **`S1-F6` the write blocker** | 14 | Three beats: an unprotected write **reaches the disk** (MODIFIED); a second is **dropped at the software gate**; the gate is then shown **switched off** and a third write is still **dropped by the inline device** (UNCHANGED). Defence in depth, and which layer cannot be turned off |
| 4 | **`S1-F7` the rename** | 16 | Icon and `.jpg` → `.txt` cross-fade while the sixteen header bytes below **do not move**; a green frame closes on them and `16 of 16 bytes identical` appears |

**Implementation contract, and why it is built this way.** Hand-authored inline SVG + SMIL only.
Every animated element carries **one** `<animate>` spanning the whole timeline with computed
`keyTimes`, all bound `begin="<controlId>.click"` — *not* a set of short animations at staggered
`begin` offsets. ⚠️ **That choice is load-bearing:** short offset animations with `fill="freeze"`
hold their frozen value across a restart, so **Replay would land on the finished state without ever
replaying**. One full-length animation per element resets cleanly on every click. Keyframes were
computed from a seconds-based storyboard by a generator, never typed by hand. `D51`'s `var()` trap
was avoided throughout: nothing animates `fill`; state changes are opacity cross-fades of a second
shape, and travel is `animateTransform type="translate"`.

`docs/assets/js/session.js` gained a `.svg-play` keyboard handler. An SVG `<g>` has no `.click()`
method, so Enter/Space dispatches a real `MouseEvent` — without it the controls were focusable but
not operable. No JS is inlined and no animation is JS-driven.

### Three content defects fixed on the way through

1. 🔴 **The page named four EVS-01 files that do not exist.** `case_notes.txt`,
   `interview_summary.txt` and `exhibit_photo.jpg` appeared in the p8 `sha256sum -c` panel and the
   p17 exhibit table. The manifest, `design/evidence_sets.md`, `record.html` and every file in this
   package agree the real four are `seizure_notes.txt` · `EVI-SRC01_acquisition_log.txt` ·
   `custody_form_EVI-SRC01.txt` · `evidence_inventory.csv`. Corrected in both places.
2. 🔴 **p16 taught magic bytes on a JPEG that is not in the set,** then told students to run `xxd`
   on all four EVS-01 files — which are text and CSV. `topic_map.md` binds `S1-09` to **`EVS-05`**.
   p16 now uses real EVS-05 files and their real bytes: `badge_photo.jpg` → `ff d8 ff e0` in the
   figure, `holiday_snap.jpg` → `50 4b 03 04` in the `.gui` (it claims JPEG and is a ZIP).
   EVS-05 was regenerated from `scripts/make_evs05.py` and **verifies byte-identical** against the
   published manifest, so every byte on the page is reproducible by a student.
3. The avalanche now uses **real digests**: `printf 'Verify......: verified' | sha256sum` →
   `e424dbf7…`, and the same string with a capital V → `b25a56c9…`. The command is printed in the
   figure so the room can reproduce it.

### Visual defects found by rendering and looking, not by the gate

| Where | Defect | Fix |
|---|---|---|
| `S1-F5` p13 | The dashed gap box **crossed the `17:05 → 08:30` label** — `design_system.md` §5 forbids it | Box extended to enclose the label instead of cutting it |
| `S1-F6` p14 | Each stopped packet **covered the thing that stopped it** (the ✕, the interface box) | Interface moved left, three stop distances re-cut so every packet halts clear |
| `S1-F6` p14 | Two labels at **font-size 11** — §5 requires ≥ 12 | Raised to 12. ⚠️ My first checker asserted `≥ 11`, so it passed. The bar was set to what was built instead of to the rule |
| `S1-F7` p16 | The verify frame **clipped the ASCII row** | Panel deepened, ASCII moved down, frame re-cut |
| `S1-F4` p8 | The revealed line left a **hole mid-figure** at rest | Reveal slot moved to the last row |
| `S1-F3` p6 (pre-existing) | Captions sat **on the box borders** in all six boxes | Boxes shortened 86 → 64, captions moved below them |

### 🔴 The one that mattered most — `D64`

Screenshotting p16 at **480px** showed the content crushed into a narrow strip with the heading
clipped. Cause: `ecdfp.css` section 16 re-declares `.page-layout`'s columns and `--sidebar-w`
*after* section 15's media queries, at equal specificity, cancelling them — so the grid resolved to
**`300px 140px`** at 480px on **every session page in the course**. The render gate said PASS
throughout, because nothing overflowed. Fixed at the source as `ecdfp.css` §16.0 and logged as
`D64`. Re-verified: 480 and 700 single column with the sidebar above main, 900 back to 210px.

### Gate results — the numbers, not "looks good"

```
python3 scripts/density_gate.py docs/session-01/index.html     ALL PASS
    total visible words     3029   limit 4000
    average words / page     137   limit 180
    worst single page        222   limit 250      (p16)
    pages with NO visual       0   limit 0
    runs of 4+ <p>             0   limit 0
    pages == sidebar entries  22 / 22
    every svg titled           7 svg / 7 <title>
    mcq contract               6 mcq / 6 feedback / 6 correct

node testing/render_gate.js docs           RENDER GATE: PASS — zero findings
    session-01 (22) · session-02 (24) · session-03 (22) · record · brief · hub · roadmap
    at 1400 / 1100 / 900 / 700 / 480
```

**Animation behaviour, asserted under Playwright — 42 checks, 0 failures:**
56 SMIL elements, **every** `begin` ends `.click`, **zero** `repeatCount`/`repeatDur`; for each of
the four figures — nothing moves after a full duration idle on load, click plays it, **replay
resets every hidden element to 0 and completes**, the control is focusable and Enter plays it;
4 controls all `role="button" tabindex="0"` with an aria-label and a visible ▶ label; all 7 figures
`role="group"` + `svg role="img"` + `<title>` first child + `<figcaption>`; min stroke-width 1.5,
min font-size 12.

Because nothing autoplays, `prefers-reduced-motion` needs no special handling: a reduced-motion
user simply never presses play.

### Left alone, deliberately

- **`S1-F1` (p2) and `S1-F2` (p5) stay static.** `D51` allows animation only where it shows a
  mechanism over time; a time budget and a lifecycle chain are states, not mechanisms.
- **Order of volatility is still absent from the page** — it is S2's, per the prompt.
- Page count, block order, minutes, question set and all prose are unchanged.

### Open

| # | Item |
|--:|---|
| 6 | `.page .svg-wrap svg { width: 100% }` (§19.2) makes every figure **shrink** on a phone instead of scrolling inside its wrapper — at 480px a 1120-unit viewBox renders 12-unit text at about 5px. The wrapper is already an `overflow-x: auto` scroll container, so a `min-width` on the svg would make figures scroll and stay legible. Affects all 26 figures in three sessions, so it is a `design_system.md` decision, not a page edit |
| 7 | The four animations exist only in S1. S2's write-blocking and hashing pages inherit these figures by reference (`S1-06`, `S1-08`) and should not rebuild them |


---

## Pass 6 — the review pass (2026-09-06)

Triggered by screenshots of live rendering faults. **Every one of these passed the density gate,
the render gate and the animation suite.** Two of them were in the shared stylesheet and affected
all six sessions.

### Layout

| # | Defect | Cause | Fix |
|--:|---|---|---|
| 1 | 🔴 `<code>` and `<strong>` inside a `.steps` item wrapped **one character per line** (`FOR-WS01` → F/O/R/-/W/S/0/1); rows grew 51px → **252px** | `.steps > li` was `display: grid` with a 32px number column, so every child *element* became its own grid item | `ecdfp.css` §16.4 rewritten — the item is a block, the number an absolutely positioned marker (`D65`) |
| 2 | 🔴 The connector line ran **straight through the `interface` label** in both `S1-F6` lanes | one `<line>` spanning the whole lane, painted *after* the boxes | split into two segments that stop at the box edges |
| 3 | An inline chip split at its hyphen — `CLEAN-` + `TOOLS` — each half drawing its own bordered chip | a hyphen is a normal break opportunity | `ecdfp.css` §16.6, `white-space: nowrap` on inline `<code>`, breaking again under 700px (`D65`) |
| 4 | The p9 verification line, 86 characters, overflowed at 1100 and 900px once (3) landed | a command that long was an inline chip | moved to `<pre><code>` — **found by the render gate, which was right** |
| 5 | The four play controls sat 12 units from the figure edge and read as jammed against the panel | — | moved to end 32 units in |

### Content — three more fabricated artifacts, all published and checkable

| # | Was | Is |
|--:|---|---|
| 6 | p4's acquisition-log `.gui` invented every field, an examiner (`M. Fahmy`) and an MD5 (`9f2b41c8…`) | the **real lines** from `EVI-SRC01_acquisition_log.txt`, including its `(computed over the written image)` verification wording |
| 7 | p15 finding: computed `e07a4419…`, recorded `3b1f8c02…`; p13 custody entry `3b1f8c02…` | the **real** digests — computed `7eda34b3…`, recorded `f05bfee8…` |
| 8 | `S1-F4` demonstrated the avalanche on `Verify......: verified`, a line that exists in no file | **the real tamper.** `make_evs01.py` changes exactly one character of the acquisition log, `09:14:02` → `09:14:03`. The figure now hashes those two strings, prints the `printf … \| sha256sum` that reproduces them, and the session coheres end to end: the hook shows the line, the avalanche shows why one character in it changes everything, Case 01 has them find it |
| 9 | p22 carried the phrase *order of volatility* | removed — `S1_BUILD_PROMPT` §5 reserves it for S2 |

### The new checker — and its own negative test

`audit.js` adds what neither existing gate measures:

1. **per-character wrapping** — any inline element far taller than it is wide holding short text;
2. **a stroke crossing label text** inside any SVG (`design_system.md` §5), by sampling every
   straight `<line>`/`<path>` against every visible `<text>` bounding box;
3. any leaf element under 40px wide holding more than 8 characters.

⚠️ **Check 2 needed document order to be honest.** Its first version flagged `WRITE` on the moving
packet — the lane line passes under an opaque packet painted *after* it, which is a packet on a
wire, not a line over a label. It now ignores a text covered by a filled shape that comes later in
document order. **That relaxation was then negative-tested**: the original unbroken lane line was
reintroduced and the audit reported `stroke crosses text "interface"`, then passed again once
restored. A checker that was loosened without a failing case proving it still bites is a checker
that lies — the ninth instance of the standing lesson in this project.

### Gates after the pass

```
python3 scripts/density_gate.py docs/session-01/index.html     ALL PASS
    3079 words · 139 / page · worst 238 (p16, limit 250) · 0 pages without a
    visual · 0 runs of 4+ <p> · 22/22 sidebar · 7 svg / 7 <title> · 6 mcq

node testing/render_gate.js docs        RENDER GATE: PASS — zero findings
node anim_check.js                      ANIMATION CHECK: PASS — 0 failures (42 checks)
node audit.js  S1 / S2 / S3             LAYOUT AUDIT: PASS — 0 findings (22 / 24 / 22 pages)
```

Device and container SHA-256 match — `01c788e4…` index, `bdcc4455…` css, `0545a343…` js — so the
gates ran on exactly the files that ship.


---

## Pass 7 — the polish pass, and one page-breaking bug (2026-09-06)

Six presentation faults reported from live screenshots, plus homework labs. One of the six led to
a defect that had been silently destroying content on every built session page.

### 🔴 The one that mattered — `D66`, the disappearing homework

`<ul id="taskList" data-task-counter>` put the counter attribute **on the list itself**, and
`homework.js` writes `counter.textContent = '0 / 5'` — which replaced all five `<li>` children with
that string. **S1, S2 and S3 all rendered an empty homework section.** The pre-written tasks also
had no checkboxes (only student-added ones did), so the counter could never leave zero anyway.

**Why no gate saw it:** the density gate reads the *source*, where the items are present; the
render gate checks overflow and console errors, not whether content survived a script. Fixed in the
markup on all three pages and hardened in the shared script.

### The six presentation fixes

| # | Reported | Cause | Fix |
|--:|---|---|---|
| 1 | p22 "looks bad", large dead area | `.split` is `1fr + 380px`; the left column held three short bullets | rebuilt on `.vs` — two equal bordered panels, plus a `.gui` making the S2 hook concrete |
| 2 | no space under the `S1-F7` closing line | the text sat 12 units off the viewBox floor, so the figure had no bottom margin | viewBox deepened; same correction applied to `S1-F4` and `S1-F6` |
| 3 | play label not centred in its pill | the pill was a fixed 208 units with a left-anchored label, so shorter labels left trailing space | `play()` now sizes the pill to its own label and centres the ▶ + text pair; all four still end at the same x |
| 4 | break timer had no frame and no button | it was a bare `<p>` | `ecdfp.css` §16.7 frames it; **Pause / Resume / Reset** added to `session.js`. Also suppressed the `h2` left rule inside the centred card, which was leaving a stray cyan mark |
| 5 | the avalanche result did not read as a result | — | the second digest now sits in a red-bordered panel that fades in with the outcome, and the readout is larger |
| 6 | `SESSION 1 LIVES HERE` not centred | it was centred, but on a 418-unit bar holding a 174-unit label, so it read as floating | now a chip that hugs its label, sitting on a bracket that spans exactly Preserve → Acquire |

### 🔴 And a false claim I had introduced

The avalanche readout said **"0 of 64 characters shared."** It is **4** — positions 41, 46, 58, 63.

Worse than wrong, it taught the opposite of the lesson. A hex digit is one of 16 values, so two
independent digests agree at about 64 ÷ 16 = **4** positions. Zero is not what a good hash looks
like; **about 4 is**, because that is what independence looks like. A student who counted would
have found 4 and concluded the figure was broken. Now reads
**"4 of 64 positions match — chance alone predicts 4"**, and homework Lab 2 makes them derive it.

### Homework labs added

`homework.md` **Part 1c**, three labs on evidence students already hold, with
`homework_answer_key.md` (gitignored, instructor-only) and a compact `.steps` summary on p21:

1. **Prove the tamper** (`EVS-01`) — run the manifest check, then answer *what can you prove and
   what can you not?* 🔴 The trap is that the altered character **cannot** be identified: they hold
   the altered copy and a manifest, not a clean copy. "One character was changed" is true and
   unsupported, and the key marks it down for exactly that.
2. **Your own avalanche** — count matching positions and say why it is ~4, not 0.
3. **Header, not extension** (`EVS-05`) — five of twelve lie; `policy_v2.docx` is the trap (a real
   `.docx` *is* a ZIP, this one is a PNG), and the two `*_partial` files are the reverse trap —
   correct signature, truncated body.

### Gates

```
density_gate.py  docs/session-01/index.html      ALL PASS
    3231 words · 146 / page · worst 245 (limit 250) · 0 pages without a visual
render_gate.js   docs                            PASS — zero findings
anim_check.js                                    PASS — 0 failures
audit.js         S1 / S2 / S3                    PASS — 0 findings
```

⚠️ **Two intermediate failures, both correct, both fixed in the page rather than the checker:**
swapping `.split` for `.vs` on p22 dropped it below the "every page carries a visual" line, because
`.vs` is not on the gate's visual list — resolved by giving p22 a real `.gui`, **not** by editing
the gate; and the new labs tripped `D58` hash-ownership on p21 at ×4 — resolved by rewording the
labs to *use* SHA-256 rather than re-explain hashing.

⚠️ Also: `anim_check.js` failed 5 checks after this pass. All five were **stale expectations in the
test** — the SMIL count rose 56 → 57 with the result panel, and the payoff string changed. Updated
to the new values, not relaxed.

### Not mine, and still open

`docs/session-02` and `docs/session-03` **fail the density gate** — total words, average, worst
page, pages with no visual, consecutive `<p>` runs, and a concept-ownership breach each. Confirmed
pre-existing: `git show HEAD:docs/session-02/index.html` fails identically, and S3 is untracked and
has never been gated. Neither has had a `D61` pass. Out of scope here; flagged for their own build.


---

## Pass 8 — publishing Case 01, the report template, and a page to write it (2026-09-06)

### What was actually missing

`D18` requires students to verify the evidence **before** class, and `D54` had left
`make_evs01.py` writing outside the tree — so **there was no published route to `EVS-01` at all.**
The page linked neither the evidence nor the report template. Confirmed before changing anything:
`grep 'href="EVS-01' docs/session-01/index.html` returned nothing.

### `R9` — checked, not assumed

`R9` says *"Never commit evidence bytes. No **image, memory dump, hive or raw pcap** in the repo"*,
and `.gitignore`'s "Evidence byte formats (R9)" block lists exactly those extensions — `.E01 .dd
.raw .mem .dmp .pcap .vhd`. `EVS-01` is **6 144 B of UTF-8 text we wrote ourselves**: Tier 1, no
personal data, no credential, no IP address at all (`D54`, `R8`, `D41`). It is not in the class the
rule prohibits, and it was already fully derivable from the public repo because
`scripts/make_evs01.py` is committed and deterministic. Published as `D67`.

### Published

| Path | | |
|---|--:|---|
| `docs/session-01/EVS-01.zip` | 4 177 B | all six files, one level, so `sha256sum -c` runs in place |
| `docs/session-01/EVS-01/` | 6 740 B | the four case files plus both manifests, loose |
| `docs/session-01/report_template.md` | 7 600 B | copied from `packages/`, served beside the evidence |

**Verified after publishing, against the served copies, not the generator's:**
`sha256sum -c` → 3 `OK`, 1 `FAILED` (`EVI-SRC01_acquisition_log.txt`); `md5sum -c` the same; and
the two manifests inside the set are byte-identical to the ones already at `docs/session-01/`.
`git check-ignore` confirms all four paths will actually commit. Every `href` on the page was
resolved against the filesystem — zero broken. Links carry `download`, which works because GitHub
Pages serves them same-origin.

### New page 22 — *Write the report*

Sits between Homework and References; References moved to p23 and the sidebar was regenerated from
document order, so ids and entries cannot drift. A ten-row table maps each report section to what
the session already produced (case reference from the acquisition log, both hashes from the
manifest check, the commands from the method, and so on), beside the two download links and the
four-criterion rubric reminder.

### 🔴 Noted, not fixed — Case 01's answer is already public

`scripts/make_evs01.py` is committed and states the alteration in clear at lines 155–156
(`TAMPER_FROM` / `TAMPER_TO`), and `design/evidence_sets.md` states it in prose. **This predates
this pass** — publishing the evidence adds no disclosure. The generator cannot omit the tamper and
still generate the set, so the options are to accept it or gitignore the script; that is a call for
the course owner, not a silent change here.

**The exercise survives it.** Homework Lab 1 grades what a student can *prove* from the manifest,
and its key marks "one character was changed" **down** as unsupported — they hold the altered copy
and a manifest, not a clean copy — whether or not they read the generator.

### Gates

```
density_gate.py   ALL PASS   3410 words · 148 / page · worst 245 (limit 250)
                             23 pages == 23 sidebar entries
render_gate.js    PASS       zero findings, 23 pages × 5 widths
anim_check.js     PASS       0 failures
audit.js          PASS       0 findings
```
