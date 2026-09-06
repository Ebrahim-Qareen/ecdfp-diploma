# session_02_outline.md — S2 page-by-page outline (D9 gate — approve before any HTML)

**Session 2 — Acquisition: Disk, Memory & Live Response.** 10 blocks · 205 topic min · 15 break = 220,
inside a 240 slot (`D23`). Continues the running case; reuses the finished design system; inherits the
S1 record. Nothing here is built yet — this is the outline to approve.

> 🔴 **The evidence gate (Part 8 step 0) is FAILED.** `EVS-02/03/04/09` do not exist. The path is
> **Tier 1 — run the acquisition** (`labs/vm_notes/acquisition_runbook.md`). This outline can be reviewed
> **in parallel** with that run; the package/figures/page are built once both the outline is approved and
> the real hashes are back. Student-facing examples use placeholder digests regardless (`D41`).

---

## 1 · Blocks — 10 topics, 205 min (from `topic_map.md`, ratified)

| # | Block | Min | Hands-on | New |
|---|---|--:|:-:|:-:|
| `S2-01` | Order of volatility **in practice** — the sequence, and what getting it wrong destroys | 15 | ML | — |
| `S2-02` | **Live response** — volatile collection on a running host | 25 | ML | 🔴 |
| `S2-03` | **Memory acquisition** — why first, the tools, the pitfalls | 20 | ML | 🔴 |
| `S2-04` | Physical vs logical — what each captures and misses | 20 | ML | — |
| `S2-05` | Image formats — E01 vs raw vs AD1, compression, embedded verification | 15 | ML | 🔴 |
| `S2-06` | **FTK Imager** — correct use + verification · *demo: imaging FIN-WKS-07* | 20 | ML | — |
| `S2-07` | `dc3dd` on clean Kali, and KAPE targeted triage | 15 | ML | 🔴 |
| `S2-08` | **[INVESTIGATION]** Case 02a — acquire and verify the suspect USB | 35 | Yes | — |
| `S2-09` | **[INVESTIGATION]** Case 02b — examine the image's partition & file-system structure | 25 | Yes | — |
| `S2-10` | **[RITUAL]** hash-verify + chain-of-custody close | 15 | ML | — |

Shape (`D15`/`D23`): integrated 130 · break 15 · investigation 60 · ritual 15 = 220. Break after
`S2-05`, at **minute 95** — start `S2-06`'s FTK demo before the break if the imaging run allows.

---

## 2 · Page-by-page — 29 pages

| # | Page | Tag | Block · min | Hands-on | Figure | Check for understanding |
|--:|---|---|---|:-:|---|---|
| 1 | Cover — *Acquisition: Disk, Memory & Live Response* | `cover` | — | — | — | — |
| 2 | How this session works — finding / interpretation / limitation / CoC, live | `frame` | — | — | **S2-F14** (reuse S1-F12) | — |
| 3 | **Open with the record** — what you already recorded in S1, objectives, the unchanged rubric | `frame` | — | — | — | reveal: *which S1 custody line is still open?* |
| 4 | Case hook — the incident to acquire. Session 2 is where the evidence is **created** | `hook` | — | — | **S2-F12** (D19, stage 0 lit) | — |
| 5 | Order of volatility **in practice** — the collection job against the clock | `theory` | `S2-01` · 8 | — | **S2-F1** ▶ | mcq: *you start at the disk. What is already gone?* |
| 6 | Micro-lab 1 — write the collection order for a given scenario | `guided` | `S2-01` · 7 | **ML1** | — | check: order matches + can say what each step costs |
| 7 | Live response — what the OS **reports** vs what is **true** | `theory` | `S2-02` · 13 | — | **S2-F2** ▶ | mcq: *the report looks clean. What could still be hidden?* |
| 8 | The live-response collector and its output tree — run it | `guided` | `S2-02` · 12 | **ML2** | **S2-F3** | check: output tree exists + per-file hash list complete |
| 9 | **Knowledge check 1** — `S2-01` · `S2-02` | `check` | — | — | — | 3 mcq |
| 10 | Memory acquisition — why it comes first, and the **smear** | `theory` | `S2-03` · 12 | — | **S2-F4** ▶ ★ | mcq: *top and bottom of the dump are from different moments. What is now unreliable?* |
| 11 | What blocks a memory capture — and capture your own RAM | `guided` | `S2-03` · 8 | **ML3** | **S2-F5** | check: dump size ≈ RAM + start **and** finish times recorded |
| 12 | Physical vs logical — two envelopes over one disk | `theory` | `S2-04` · 12 | — | **S2-F6** | mcq: *which reaches unallocated space, and which later session needs it?* |
| 13 | The four acquisition methods — and image a small volume both ways | `guided` | `S2-04` · 8 | **ML4** | **S2-F7** | check: the two files differ in size + can say why |
| 14 | Image formats — E01 vs raw vs AD1, container anatomy | `theory` | `S2-05` · 8 | — | **S2-F8** | reveal: *what does each container's verification actually verify?* |
| 15 | Make the same image as E01 and as raw | `guided` | `S2-05` · 7 | **ML5** | — | check: E01 smaller · `ewfverify` passes · raw has no embedded hash |
| 16 | **Knowledge check 2** — `S2-03` · `S2-04` · `S2-05` | `check` | — | — | — | 3 mcq |
| 17 | **Break — 15 minutes.** Imaging runs while you are out | `break` | — | — | — | `data-timer="15"` |
| 18 | FTK Imager — correct use, and what `verified` **does not** cover | `theory` | `S2-06` · 10 | — | **S2-F9** ▶ ★ | mcq: *the log says verified. What has the tool NOT checked?* |
| 19 | Instructor demo — imaging `FIN-WKS-07` end to end; then image the test volume | `guided` | `S2-06` · 10 | **ML6** | — | check: the `.txt` log shows both digests and `verified` |
| 20 | `dd` · `dc3dd` · KAPE — three jobs, three tools (and KAPE's licence) | `theory` | `S2-07` · 8 | — | **S2-F10** · **S2-F11** | mcq: *which tool records a hash as it images, and which never does?* |
| 21 | `dc3dd` with `hash=` and `log=` on the clean Kali snapshot | `guided` | `S2-07` · 7 | **ML7** | — | check: the log contains the hash — which plain `dd` never produces |
| 22 | **Case 02a** — the brief, and the acquisition decision tree | `case` | `S2-08` · 12 | **Yes** | **S2-F13** | Q1 is always hash verification |
| 23 | **Case 02a** — acquire and verify the suspect USB, write it up | `case` | `S2-08` · 23 | **Yes** | — | finding vs interpretation on every claim |
| 24 | **Case 02b** — the brief: examine the acquired image's structure | `case` | `S2-09` · 8 | **Yes** | — | — |
| 25 | **Case 02b** — partitions, file systems, what the structure proves and does not | `case` | `S2-09` · 17 | **Yes** | — | one question answerable only *"cannot prove"* |
| 26 | **Knowledge check 3** — `S2-06` … `S2-09` | `check` | — | — | — | 4 mcq; ≥2 *finding or interpretation?* |
| 27 | The closing ritual — hash-verify, chain-of-custody close, and fill a custody line | `ritual` | `S2-10` · 15 | **ML8** | — | every student signs one custody line; links `record.html` |
| 28 | Summary, cheat sheet, takeaways (Print) | `summary` | — | — | — | — |
| 29 | Homework, the report, additional practice, open items, references | `close` | — | — | — | `#taskList` + task-creator |

Visible-word budget ≈ 240/page. Break page is **17**, at minute 95 (after `S2-05`).

---

## 3 · The fourteen figures — every block has one, and more of them move

Inline SVG only · `role="img"` + `<title>` first · `.svg-wrap` · exactly one `[data-detail]` per
`[data-node]` · animation behind an explicit play control, no autoplay/loop/JS (`D51`). **6 of 14 animate**
(S1 did 5 of 12).

| # | Figure | Block | Anim | Shows |
|---|---|:-:|:-:|---|
| **S2-F1** | Collection sequence against the clock | `S2-01` | ▶ | 7 stores; a collection job moves down while lower stores decay. Click a store → what starting lower cost you |
| **S2-F2** | Live response — OS report vs truth | `S2-02` | ▶ | two columns; a rootkit hides 3 processes, report still clean. Click → the artifact that catches it |
| **S2-F3** | The live-response output tree | `S2-02` | — | `<HOST>_<date>_<time>\` → ForensicImages + LiveResponseData + hash list + Processing_Details.txt. Click a branch → what it holds / cannot |
| **S2-F4** ★ | Memory capture is a smear | `S2-03` | ▶ | capture head moves down a live map as processes change; top ≠ bottom in time. Click → what it makes unreliable, and what it does not |
| **S2-F5** | What blocks a memory capture | `S2-03` | — | driver signing · Secure Boot · hypervisor · anti-cheat driver. Click → the real error + the way round |
| **S2-F6** | Physical vs logical — two envelopes over one disk | `S2-04` | — | slack/unallocated/HPA-DCO vs allocated files. Click a region → what is lost, which session needs it |
| **S2-F7** | The four acquisition methods | `S2-04` | — | disk-to-image · clone · sparse · logical. Click → when right, and the evidence it forfeits |
| **S2-F8** | Image container anatomy | `S2-05` | — | E01 (header·segments·CRC·embedded hash·metadata) vs raw vs AD1. Click → what its verification verifies |
| **S2-F9** ★ | What `verified` covers, and what it does not | `S2-06` | ▶ | the `D7` figure of the session, sequel to S1-F1. Tool hashes what it writes then reads back, never re-reads source. Click → the sentence you may write |
| **S2-F10** | `dd` · `dc3dd` · KAPE — three tools | `S2-07` | — | 4 axes: hashes on the fly? · log? · read errors? · scope. Click → one command + one catch |
| **S2-F11** | Targeted triage — take vs leave | `S2-07` | — | disk with the triage target set over it. Click → what it collects + the question it can no longer answer |
| **S2-F12** | The D19 case — S2's slice lit | hook | — | the 6 stages from S1-F10, **stage 0 (seizure+acquisition) lit**, rest dim. Built from the locked **F7** |
| **S2-F13** | The acquisition decision tree | `S2-08` | ▶? | running? → encrypted? → time short? → which method. The thing **no free lab teaches** (`D46`) |
| **S2-F14** | The shape of a session | opening | — | reuse S1-F12 unchanged |

---

## 4 · The eight micro-labs (WATCH · DO · CHECK · WHY) — new in S2

Rendered with existing components: command in `<pre><code>`, expected output in a `.gui` panel in a
`.split`, the check as a `.lab-box` line, the *does-not-prove* as a `.limitation`. **Every micro-lab uses
`EVS-02/03/04` or a scratch volume the student makes — never the original evidence, never an unverified set.**

| ML | Block | WATCH (instructor) | DO (student) | CHECK |
|---|---|---|---|---|
| 1 | `S2-01` | list host contents in volatility order | write the order for a scenario | order matches + costs named |
| 2 | `S2-02` | run the live-response collector | run it on their own VM | output tree + full per-file hash list |
| 3 | `S2-03` | capture RAM, note elapsed time | capture their own RAM | dump ≈ RAM · start **and** finish times |
| 4 | `S2-04` | image a 100 MB volume physically then logically | do both | two files differ in size — and why |
| 5 | `S2-05` | create the image as E01 and as raw | do both | E01 smaller · `ewfverify` passes · raw has no embedded hash |
| 6 | `S2-06` | FTK Imager end to end, verification ticked | image the supplied test volume | `.txt` log shows both digests + `verified` |
| 7 | `S2-07` | `dc3dd` with `hash=` and `log=` (clean Kali) | same on the test volume | log contains the hash `dd` never produces |
| 8 | `S2-10` | fill one custody line on the record | fill their own | the record page shows the step closed |

---

## 5 · Assessment
- **`quiz.md`** — 10, all MCQ (`D52`), correct answer rotating A→B→C→D. ≥3 *finding or interpretation?*;
  ≥1 on what `verified` does **not** cover.
- **In-page** knowledge checks 1–3, all MCQ.
- **`report_template.md`** — **copied byte-for-byte from S1** (`D20`, never changes).
- **`homework.md`** — external labs each assigned with its known defect named (`D47`); THM/CyberDefenders
  from `Resources/LABS/`. No lab teaches acquisition-as-a-decision (`D46`) — that stays ours.

---

## 6 · Tool currency — re-verified on the build date 2026-09-06 (brief §12)

| Tool | Bind to | Note |
|---|---|---|
| FTK Imager | **8.3** (Exterro, free) | ✅ current · **not** the paid "FTK Imager Pro" |
| Volatility 3 | **2.28.2** | 🔺 **brief says 2.28.0 — stale.** 2.28.2 released 2026-08-19. Used in acquisition context; symbol pack ships (`D2`) |
| OSFMount | **3.3.1000** | ✅ current · redistributable |
| Arsenal Image Mounter | **3.13.368** | ✅ current · Free Mode |
| `dc3dd` | **7.3.1** (Kali) | dormant, not dead (`A6`) |
| KAPE | core **1.3.0.2** / KapeFiles current | educational use free; **commercial use barred since 2026-01-01** — state it in class, pair every step with a free alt (`D37`) |

---

## 7 · Reconciliations to apply **on approval** (not yet done)

1. **`FOR-LNX01` → Kali** (`D56`) in: `topic_map.md` row `S2-07`, `00_INSTRUCTIONS.md` Part 6,
   `docs/lab/index.html`, `docs/lab/setup.html`, `docs/roadmap.html`, `docs/session-02/brief.html`,
   `tools_by_session.md`. `S2-07` runs `dc3dd` from a **clean pre-staging Kali snapshot**.
2. **Volatility 3 2.28.0 → 2.28.2** in `tools_by_session.md` (S2 and S6 rows) and anywhere a command is bound.
3. **Case framing (`D57`, confirm):** Case 01 (`EVS-01`, powered-down, no memory, March) = standalone
   integrity/custody warm-up, kept byte-for-byte, used as S2's cautionary contrast. The **D19 incident**
   (`EVI-SRC01` / `FIN-WKS-07`, found running, Aug window) = the graded carry-through case S2 acquires and
   S3–S6 analyse. Memory **is** captured → `EVS-03` survives for `S6-09`/`S6-10`.

---

## 8 · What this outline does NOT cover / owners
- Real digests for `EVS-02/03/04/09` — produced by `acquisition_runbook.md`, owned by `ecdfp-evidence`.
- `cases/case-02a`, `case-02b` answer keys — `ecdfp-case` is **not installed** (7 of 8 skills). Case
  content lives in `student_activity.md` for now, as S1's Case 01 did.
- The **F7 SVG** (drives `S2-F12`) — drawn at figure-build time from the locked F7 in `staging_plan.md`;
  add a dated `DECISIONS.md` row formalising F7 then.

## 9 · Deliverables this outline authorises (after approval + hashes)
`packages/session-02/` nine docs · 14 inline-SVG figures · `docs/session-02/index.html` · regenerate
`docs/session-02/record.html` · the exit gate (brief §13, 15 checks).
