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
| **D1** | **6 sessions × 4 h = 24 h.** Locked. *(Extended by `D70` — see Part 4.)* | Fixed slot. Everything else is sized to fit it, not the reverse. |
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
- **Student path:** CCNA → MCSA → Linux Administration → SOC → CEH → eCIR → **eCDFP**.
  This is the **seventh** course in the ITGate diploma track.
  Assume they already have: networking (CCNA) · Windows and Active Directory (MCSA) · Linux
  administration · SIEM and alert triage (SOC) · attacker mindset and tooling (CEH) · incident
  response and log analysis (eCIR).
  **Link to it. Never re-teach it (`D72`).**

### The dual framing (`D72`) — DF as a skill *and* as a job

The course is built on **two axes at once**, and every session carries both:

| Axis | The question it answers | Who it is for |
|---|---|---|
| **DF as a SOC skill** | *"I am a SOC analyst — what does this artifact let me say that a SIEM alert cannot?"* | every student, from day one |
| **DF as a profession** | *"An examiner produces a signed, defensible deliverable. What is the standard?"* | the student who may specialise later |

**The continuity story — and it is literal (`D73`).** In eCIR the students worked **web, network and
email attacks**. The carry-through case (`D19`) therefore fixes its entry vector as a **phishing
email carrying the malicious document**, with an **HTTP C2 channel**. Two of eCIR's three attack
families are then the same evidence, seen from the other side:

| eCIR taught | eCDFP proves it, on disk |
|---|---|
| email attack analysis | the phishing message and its attachment, recovered in `S6-07` (email forensics) |
| network attack analysis | the C2 beacon, in the `EVS-08` pcap and the host's own artifacts (`S6`) |
| web attack analysis | the HTTP delivery and staging traffic, plus browser artifacts (`S6-07`) |

*You contained it — now you prove it.* Same person, next phase of the same job. Stated once, in
`S1`, and closed in `S6` when the last session recovers the first artifact of the story.

**Three mechanisms, and no more — the linkage is deliberately light:**

| Level | Element | Size cap |
|---|---|---|
| **Course** | One reference page: *DF capability → what it gives a SOC analyst → what an examiner must produce.* Built once, linked from every session | ~12 rows |
| **Session** | **Opening bridge** — *"In eCIR you did ___ on this incident. Today you prove ___."* Exactly one per session | ≤ 3 lines |
| **Session** | **Closing "what you can now sign"** — the deliverable this session makes them able to produce, and the SOC action it unlocks | ≤ 4 lines |
| **Topic** | A one-line `SOC` chip, **only** where the analyst's use genuinely differs from the examiner's | 1 line |

**Anti-bloat rules — these are the enforcement, not decoration:**

- **Linking is allowed; re-teaching is not.** A bridge *names* what they already know and moves on.
  The moment it starts explaining that thing again, it is a defect.
- **The `SOC` chip is selective.** If the line would only repeat the artifact's *what it proves* box,
  it is not written. A forced link on every topic is noise, and noise is what makes students skip
  the real ones.
- **`R10`'s six-box artifact template is unchanged.** The dual framing never becomes a seventh box.
- Depth stays **overwhelmingly on DF itself**. The linkage is the frame around the material, never a
  share of its minutes.
- **Class:** ~5 students, offline classroom, every student at the keyboard every session.
- **Language:** written material is **bilingual by design** — simplest possible English, with an
  Egyptian-Arabic explanation line under it. See *The bilingual layer* (`D76`) below.

### The bilingual layer (`D76`) — English line, Egyptian explanation under it

Not every student reads English well, and the certificate content is English. So the material
carries **both, in place**: the English line, and directly under it a short Egyptian-Arabic
explanation of what it means.

**The seven rules. These are what stop it becoming noise:**

1. **Explanation, never literal translation (`D104`).** The Arabic answers *what does this mean, and
   why does it matter* — it does **not** follow the English sentence. A line that mirrors the English
   word order is a defect, however accurate it is. **Test:** cover the English. Does the Arabic stand
   on its own and teach the idea? If not, rewrite it.
2. **Technical terms stay in English, inside the Arabic line (`D122`).** Never invent or borrow an
   Arabic equivalent — the student sits an English exam and works in English tools, so a translated
   term teaches a word they will never see again. The form is `الـ hash`, `الـ bytes`, `bits`.
   **Banned, with what to write instead:**

   | Do not write | Write |
   |---|---|
   | `البصمة` · `بصمة` | `الـ hash` — or `الـ signature` when it means magic bytes |
   | `البايتات` · `بايت` | `الـ bytes` · `byte` |
   | `بتات` · `البتات` | `bits` |
   | `الترويسة` | `الـ header` |
   | `الوقائع` | `الـ findings` |
   | `الاستنتاج` | `الـ interpretation` |
   | `الحرز` | `الـ exhibit` |
   | `الأثر` · `الآثار` | `الـ artifact` · `الـ artifacts` |
   | `بيان البصمات` | `الـ manifest` |
   | `البيانات الوصفية` | `الـ metadata` |
   | `سلسلة الحيازة` | `الـ chain of custody` |
   | `مانع الكتابة` | `الـ write blocker` |
   | `المنطقة المحمية` | `الـ HPA` |
   | `الحاوية` | `الـ container` |
   | `العناقيد` · `المجموعات` | `الـ clusters` |
   | `الهيكس` · `الست عشري` | `الـ hex` |
   | `النزاهة` · `الهوية` | `الـ integrity` · `الـ identity` |
   | `الاستحواذ` | `الـ acquisition` |
   | `الوسيط` | `الـ media` |

   **This applies to every Arabic string in the file, not only `<span class="ar">`** — the SIMSCREEN
   and `Dgm` caption strings live in `<script>` and ship to the student exactly the same way. About
   60 violations hid there through a sweep that only matched the span.

   **Two mechanical traps when fixing these:** match **whole words** with an Arabic-letter lookaround
   — a substring replace turns `تُثبت` into `تُثbit` — and **re-read every changed sentence for
   agreement**, because swapping the noun strands its adjective (`الـ hash الرقمية`) and kills duals
   (`البصمتان` has no English carrier; write `القيمتان`). `density_gate.py` fails the build on any
   banned term.

   **And the table above is a list of STEMS, not a list of forms (`D132`).** Arabic attaches its
   particles to the front of the word — `و` `ف` `ب` `ك` `ل` `ال`, and `ل` + `ال` **contracts to** `لل`
   — and its suffixes to the back, where a final `ة` becomes `ت` (`بصمة` → `بصمتها`). So `للترويسة`
   and `بصمتي` are the same violation as the bare word, and a gate that matched only the listed forms
   **passed eight pages that each still contained one**. The gate now splits the table in two:

   | Class | Terms | Matching |
   |---|---|---|
   | **STEMMED** — never anything but the technical term | `بصمة` `بايت` `بتات` `ترويسة` `الهيكس` | prefixes **and** suffixes, including `ة`→`ت` |
   | **LITERAL** — also an ordinary Arabic word | everything else in the table | the exact definite form only |

   The split is deliberate: `أثر` is the banned translation of *artifact* **and** the ordinary word
   for *effect*, so matching it loosely reports *its effect is long* as a terminology break. The
   LITERAL class therefore **will miss an indefinite technical use** — `أي حرز` for *any exhibit* is
   a real violation the gate cannot see. That is the accepted cost of a gate nobody learns to ignore,
   and it is why the terminology pass is **a reading pass as well as a gate run**.
3. **Professional written Arabic (`D104`), and PLAIN (`D128`)** — Modern Standard, clear and direct,
   the register of a textbook rather than a conversation. **Not** heavy Egyptian colloquial: `اللي` ·
   `مش` · `عشان` · `دلوقتي` · `كده` · `بتاع` · `يبقى` do not belong in written material. The spoken
   Egyptian lives in `instructor_script_ar.md`, where it is the instructor's own voice.

   **But MSA is not licence to write literary Arabic.** The failure that actually happened is the
   opposite of colloquial: ornate, archaic phrasing that a working analyst has to stop and decode.
   **The test is not *is this correct Arabic*. It is *does a reader get it at normal speed, once*.**

   | Do not write | Write | Why |
   |---|---|---|
   | `لطخة لا لقطة` | `صورة على مدى دقائق، لا لحظة واحدة` | say the mechanism, not a metaphor |
   | `إذ` · `بيد أن` · `ثمّة` · `فحسب` | `فـ` · `لكن` · `هناك` · `فقط` | literary connectors slow a technical line down |
   | `تُعمّر` · `يتلاشى` · `ينبع` | `تبقى صحيحة` · `يختفي` · `يقوم على` | a common verb beats an elegant one |
   | `اللاتماثل` · `ماهيته` | `الفرق` · `ما هو` | an abstract noun where a plain word works |
   | `مقرونة بثقة زائدة` | `لكن بثقة أكبر مما تستحق` | unpack the compression |
   | `قابلاً للطرح لاحقًا` | `تستطيع لاحقًا فصله عن أثر المهاجم` | say the action, not its abstraction |

   **Short sentences. One idea each. A common word over a fine one.** If the English says it in a
   plain sentence, the Arabic says it in a plain sentence.
4. **Every explanatory element carries one — not just paragraphs.** Table cells, list items, box
   bodies and worked examples. A student who cannot read the English cell cannot read the table.
5. **Roughly the length of the English, and no longer.** An explanation may need a clause the
   English did not, but a paragraph where the English had a sentence means the English is too
   complicated — simplify the English instead.
6. **If the Arabic adds nothing, delete it.** A restatement of an already-simple line is noise, and
   noise trains students to skip the Arabic that does matter.
7. **Visually secondary and visibly attached** — smaller, muted, correct RTL. It sits *under* its
   English, never beside it, never replacing it.
8. **The Arabic sits DIRECTLY UNDER its English, in one box that fits both (`D108`, supersedes
   `D106`).** `.ar` is `width:fit-content` with **physical** `margin-left:0; margin-right:auto`, so
   its box starts where the English starts. Never `width:auto` right-aligned — on a wide column
   that puts the explanation at the far right, level with nothing, and a reader looking for the
   Arabic looks at **the line above**, not at a column edge. `margin-inline-end` cannot express
   this: it resolves against the element's own direction, and `.ar` is `rtl`, so *inline-end* means
   LEFT. The margins are physical on purpose.
8a. **No measure cap on a caption or a box body.** `.ss-cap p` had `max-width:78ch`, which used
   half the SIMSCREEN frame and pushed the Arabic onto a third line for nothing.
9. **Arabic always wraps (`D105`).** `.ar` is `white-space:normal` everywhere, so it can never
   inherit a `nowrap` written for the label it sits under. A first table column keeps its **label**
   unbreakable — `> b`, `> code`, above 700 px — never the whole cell: a cell-wide `nowrap` puts
   the English *and* its Arabic on one unbreakable line, which sets a huge max-content width and
   starves every other column. The symptom shows up in the **second** column.

**How the cost is absorbed (`D78`) — by measurement and type, never by cutting content:**

- **`density_gate.py` counts English text only.** The Arabic layer is excluded by its class. It
  restates; it does not add concepts, so counting it would fail a page for a feature we required.
  The existing limits are unchanged: **4000 total visible words · 180 average per page · 250 worst
  page.**
- **Two new gate checks replace what that exclusion gives up:** every teaching block carries its
  Arabic line, and **no Arabic line is longer than the English it sits under** — `D76` rule 4,
  machine-checked instead of trusted.
- ~~The type scale drops one step~~ — **cancelled by `D92`.** The English body keeps its size;
  legibility on a projector outranks page height, and height is absorbed by longer pages instead.
  **Only the Arabic line is smaller** — roughly `0.85em` of its English, muted. **Floor: nothing
  renders below 12 px at any breakpoint.** Below that it stops being a reading aid.
- **Longer pages, and more pages per session, are accepted — not a defect.** Material size is not a
  constraint on this course; readability is.

**Where it applies:**

| Surface | Bilingual? | Note |
|---|:-:|---|
| `docs/page-NN/index.html` | **Yes** | every teaching block — this is the reference surface |
| `student_guide.md` | **Yes** | same rules |
| `guided_lab.md` | **Yes** | every step |
| `quiz.md` · `homework.md` | **Yes** | question **stems** only. Answer options stay English |
| `report_template.md` | **Guidance only** | the fill-in guidance may be bilingual; **the report the student writes is English** |
| `instructor_guide.md` · `report_stage.md` · `build_log.md` | **No** | internal. The instructor's Arabic is `instructor_script_ar.md` (`D77`) |

### The instructor delivery script (`D77`) — required in every package

`packages/page-NN/instructor_script_ar.md` is **mandatory for every page**, in Egyptian
Arabic. It is not the `instructor_guide` and never repeats it: the guide is *what the session
contains*, the script is **what you say and do, in order, on the day**. Fixed sections:

| # | Section | What it must give the instructor |
|---|---|---|
| 1 | **قبل ما تدخل القاعة** | pre-class checklist — evidence staged, VM at baseline, tools tested |
| 2 | **خريطة السيشن** | the four blocks (`D71`) on the clock, and the one sentence that opens and closes each |
| 3 | **صفحة صفحة** | per page: what you say · **how it links to the page before** · **how it links to the lab** · the terms on that page and how to answer if a student asks |
| 4 | **اللاب خطوة بخطوة** | every step: what you type or click · the output to expect · what to say while it runs · what commonly goes wrong |
| 5 | **من العملي للتقرير** | how what was just done becomes report lines — which section, what wording, and where the finding/interpretation line falls |
| 6 | **لو حصل** | the questions students actually ask, and the honest answer |

**Style: short, simple, direct.** Terms stay English. It tells the instructor what to *do*, never
what a topic *is* — that is the guide's job.

### The exam — this sets the teaching target

| Domain | Weight | Meaning |
|---|---|---|
| Fundamentals of Digital Forensics | **33 %** | Windows artifact analysis, evidence of execution, report structure |
| Digital Forensics Tools & Techniques | **27 %** | correct tool use, network analysis, log & timeline tools |
| Preservation of Evidence | **20 %** | collection methodology, integrity, chain of custody |
| Storage Device Fundamentals | **20 %** | physical device characteristics + logical storage structures |

**INE exam format (for reference):** 24 hours · 30 MCQs (15 theory + 15 scenario, answered against
a live VPN lab).

**The academy does not provide the INE exam (`D74`).** A student who wants the certificate sits it
themselves. What ITGate promises is **the certificate's full content, taught to exam-ready depth**.

**The academy's own final exam is MCQ-only, run by ITGate, and is out of scope for this build
(`D75`).** It is not designed, written, or stored in this repo, and nothing in the course is shaped
around it. **The assessment of record is the forensic report on the `D20` rubric, every session**,
plus the per-session quiz.

`D74` changes three things:

- **Coverage of every INE section stays mandatory.** It is the whole promise — *same content* is
  what is being sold. Nothing here loosens `topic_map.md`'s obligation to place every section.
- **`D24`'s domain tolerance relaxes from ≤ 1.0 pp to ≤ 2.0 pp**, and it is now a **health check,
  not a gate**. The weights still describe a student who could sit INE tomorrow, so they stay the
  design target — but they no longer justify trimming the two things the job and the academy grade.
- **A deliberate lean toward Preservation and Reporting is allowed** inside that ±2.0 pp, because
  the assessment of record is the forensic report (`D20`), not a multiple-choice paper.

**Consequence, unchanged:** students must be **fast and correct with tools on evidence under time
pressure**, not essay-fluent. Every session produces timed tool repetitions. No session is
theory-only.

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
├── packages/page-NN/       INSTRUCTOR PACKAGE — 11 markdown docs, NOT published
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
    ├── page-NN/index.html + assets/img/     (14 pages, D84/D86)
    ├── beyond/         SELF-STUDY TRACK — own index, M01-M14 (D83)
    ├── cases/index.html                  student-facing case files (no answer keys)
    ├── cheatsheets/index.html            all sessions, anchored #sNN
    ├── resources/labs.html               all practice labs, anchored #sNN
    └── review/index.html                 milestone review + quiz banks
```

**Why `packages/` is separate from `docs/page-NN/`:** instructor guides and answer keys must never be
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

## PART 4 — The locked roadmap · 6 × 4 h = 24 h (D1 · extended by D70)

**The 24 hours is the design target, not a hard ceiling (`D70`).** Ebrahim owns the slot, so **up to
two extra sessions may be added during the build — maximum 8 × 4 h = 32 h**. They are a relief valve,
never planned space:

- Every session is still designed to fit **220 teaching minutes** inside the six. An extra session is
  opened **only** when a named session breaks that ceiling and re-splitting inside the six cannot fix it.
- Whatever moves out must be **one coherent block** — its own title, its own case. Never leftovers
  swept into a spare slot.
- The call is made **no later than the S5 build**, so the schedule is fixed before students are told.
- Adding a session **re-runs the `D24` domain reconciliation**. It is not a free four hours.

### The unit of material is the TOPIC, not the session (`D79`)

The course is an **ordered chain of topics**. A session is a **container**: on the day, the
instructor takes as many topics as fit the clock. This is what makes the roadmap safe — **no session
can be overloaded, because no session owns its content.**

**Every topic is a complete, self-contained unit, in this order:**

| Part | What it does |
|---|---|
| **1 · Bridge + theory** | opens with **the link to the topic before it** — what we established, what it left open. Then the concept. Students follow demos on their own keyboard |
| **2 · Guided practice** | instructor-led, step by step. Each step opens with the theory it applies |
| **3 · Independent** | the student applies it alone, on the carry-through case |
| **4 · Report stage** | what this topic contributes to the report — **written now, not later** |

- **Theory is the smaller part: ≤ 35 % of the topic's minutes**; practice and report ≥ 65 %.
  (`D71`'s proportion, moved down to the topic.)
- **Topic order is a strict dependency chain, machine-verified (`D80`).**
- **The report is built in stages, one per topic**, so the student ends holding a report of the
  shape a professional examiner produces — not a summary written at the end.

**The session container** — same totals, new internal logic:

- **205 topic minutes + 15 break = 220**, inside a 240-minute slot.
- **The break falls at a topic boundary, inside the first two hours. Never mid-topic.**
- **The last 15 minutes are the session's integrity close** — hash-verify and chain-of-custody
  sign-off. This stays a *session* ritual, not a topic part.
- A second break is the instructor's call at delivery time and is not budgeted in the material.

**This supersedes `D71`'s A / B1 / B2 / C session layout.** What `D71` keeps: theory light and
practice heavy · the report written during the practical, not after · students at their own keyboard
during demos · the break inside the first two hours · the second break unbudgeted.

**Topic IDs are `T01`…`Tnn`, sequential in teaching order and session-independent.** The `SN-NN`
labels are retired: an ID that names a session cannot survive a course whose sessions are decided on
the day.

### Topic ordering is proved, not judged (`D80`)

A topic in the wrong place leaves a gap the student never recovers from, so the order is not a
matter of editorial judgement:

- Every topic declares its **prerequisites** — the topics whose result it uses. `topic_map.md`
  already carries the column; it becomes load-bearing.
- The chain is **topologically sorted and verified by a script**: no topic before one it depends on ·
  no cycles · no prerequisite that does not exist · every topic reachable from the start.
- **Evidence is a prerequisite too.** A topic cannot appear before the point at which the evidence
  it needs has been acquired.
- **This is a gate, not a warning. A failing order does not ship.**

### Scope goes beyond the certificate (`D81`)

The course teaches **Linux forensics and mobile forensics**, which the eCDFP syllabus does not
cover. This **reverses `D38`** (Linux declared out of scope) and the earlier exclusion of mobile.

- **They are additions, never replacements.** Every INE section stays covered — `D74`'s *same
  content* promise is untouched.
- **They sit OUTSIDE the `D24` domain reconciliation.** The exam-weight check is computed on
  INE-mapped topics only. Folding roughly four hours of non-exam material into percentages that
  describe a different thing would make the check meaningless.
- **They are labelled `beyond certificate` on the site and in the material**, so a student
  preparing for INE knows exactly what is and is not on that exam.
- **Evidence consequence — this is the hard part.** Linux is **Tier 1**: a Linux victim VM joins
  the lab (a fourth VM). **Mobile cannot be Tier 1** — `R9` forbids real personal data and a real
  handset cannot be imaged for teaching. Mobile is **Tier 2 only**: a purpose-built public research
  image, linked and never rehosted. If no such image can be licensed, **the topic is cut rather
  than faked.**

### Two content tiers: TAUGHT and SELF-STUDY (`D82`)

`D81`'s extensions are **not taught in class**. The material carries two tiers, and the difference
is absolute:

| | **Taught** | **Self-study** |
|---|---|---|
| Where | the session containers | on the site, outside any session |
| Minutes | budgeted — counts against the 190 min/session | **none. It never competes for class time** |
| Instructor script (`D77`) | required | not written |
| Guided-lab timing, session placement | required | not applicable |
| Evidence | Tier 1 preferred | **Tier 2 only** — linked public corpora, never rehosted |
| Domain reconciliation (`D24`) | counted | excluded |

**The taught course therefore stays at 1140 topic minutes ÷ 190 = exactly 6 sessions.** `D81`'s
"7 × 4 h" line is wrong and is corrected here: **extension content never grows the taught course.**

**The one rule that makes this safe: a self-study topic ships complete, or it does not ship.**
Same `R10` six-box standard, the same findings-vs-interpretation discipline, real licensed evidence
links, and an answer key for anything it sets. **No stubs. No "coming soon" tiles.** The previous
instructor's material announced six labs it never built — a self-study tier is exactly where that
failure comes back, so the bar is the same as taught material, only the timing is not.

**The two tiers are physically separate (`D83`).** The self-study tier is its own section of the
material and its own area of the site — reached *after* the taught course, never mixed into it:

| | Taught | Self-study |
|---|---|---|
| Map | `design/topic_map.md` — **INE eCDFP topics only** | `design/beyond_map.md` |
| Material | `packages/topic-NN/` | `packages/beyond/mNN-<slug>/` |
| Site | `docs/topic-NN/` | `docs/beyond/` with its own index |
| Entry point | the roadmap | the site nav, and the end of the roadmap |

- **`topic_map.md` never carries a self-study row.** Our taught material is organised strictly by
  the INE eCDFP syllabus; a topic that is not in that syllabus is not in that map.
- **No session page links into `beyond/`**, and no `beyond/` module is a prerequisite of anything
  taught. The dependency chain (`D80`) covers the taught tier only.
- All twelve modules of the catalogue are in scope: Linux (×2) · Mobile (×2) · macOS · VM forensics ·
  Cloud · Database · Encryption · Anti-forensics detection · Advanced memory · Enterprise DFIR at
  scale · Legal & expert testimony · Malware triage for examiners.

### The map (`D84`) — 25 taught topics on 14 pages

**Locked 2026-09-08.** `design/topic_map.md` carries the rows; this is the structure it must emit.
A **page** holds one or two topics; **each topic keeps its own bridge, theory, guided practice,
independent work and report stage** (`D79`) even when it shares a page. Two topics share a page only
where they are genuinely the same stage of the work — never to fill space.

| Page | Topics (min) | Page min | Why they share a page |
|---|---|---:|---|
| **P01** | `T01` Foundations & Forensic Principles (45) · `T02` The Forensic Report (25) | 70 | what the work is, and what it produces |
| **P02** | `T03` Evidence Integrity — Hashing, Chain of Custody, Write Blocking (38) | 38 | alone — the single discipline the course turns on |
| **P03** | `T04` Inside a File — Hex, Magic Bytes & Signatures (82) · `T05` Data Representation & Metadata (35) | 117 | both are data at byte level; Case 01 is `T04`'s investigation |
| **P04** | `T06` Live Response — Order of Volatility (25) · `T07` Memory Forensics — Acquire and Analyse (35) | 60 | volatile evidence, collected then read |
| **P05** | `T08` Imaging Scope & Formats (33) · `T09` Imaging Tools — FTK Imager & dc3dd (112) | 145 | choose the format, then make the image and test what it contains |
| **P06** | `T10` Hidden Data & Image Forensics (80) | 80 | alone |
| **P07** | `T11` Malicious Documents & Executables (75) | 75 | alone |
| **P08** | `T12` Storage Internals & Slack (45) · `T13` Partitioning — MBR & GPT (68) | 113 | the physical disk, and how it is divided |
| **P09** | `T14` File Systems — FAT & NTFS (52) · `T15` Carving & Deleted Data (25) | 77 | the file system, and what survives deletion |
| **P10** | `T16` Registry Structure & System Configuration (28) · `T17` USB & Device History (35) | 63 | learn the hive, then read the first artifacts from it |
| **P11** | `T18` Evidence of Execution (40) · `T19` User Activity — Shellbags, Recycle Bin, VSS (38) | 78 | what ran, and what the user touched |
| **P12** | `T20` Windows Event Logs (49) | 49 | alone |
| **P13** | `T21` Network Evidence & Traffic Analysis (42) · `T22` C2 & Attack Patterns in Traffic (28) · `T23` Internet & Email Artifacts (20) | 90 | network and internet activity, from the wire and from the host |
| **P14** | `T24` Logs & Super-Timelines (45) · `T25` Final Report & Capstone (40) | 85 | build the timeline, then write from it |

**`T01`…`T25` are sequential in teaching order** (`D79`). A topic never changes its number.

**Totals: 25 topics · 14 pages · 1140 topic minutes.** Pages run 38–145 min, average 81.
`1140 ÷ 190` per session packs into **7 sessions = 28 h** once topic sizes and the fixed
order are respected (`D98`) — `D70`'s valve, inside its ceiling of eight.
Average page **81 min**, so roughly **2–3 pages a session**. The instructor decides on the day.

**The six 15-minute hash-verify / chain-of-custody rows are NOT topics.** They are the session's
integrity close (`D79`) — 15 min × 6 = 90 min, budgeted per session, never in the topic map.

**The self-study catalogue (`D83`) — 14 units, no minutes, `docs/beyond/`:**

`M01`–`M02` Linux (filesystem · logs and user activity) · `M03`–`M04` Mobile (acquisition and its
limits · Android and iOS artifacts) · `M05` macOS · `M06` Virtual machine forensics ·
`M07` Cloud · `M08` Database · `M09` Encryption · `M10` Anti-forensics detection ·
`M11` Advanced memory · `M12` Enterprise DFIR at scale · `M13` Legal and expert testimony ·
`M14` Malware triage for examiners.

> **The pre-`D79` session roadmap table has been removed.** It described a structure the course no
> longer has. `design/topic_map.md` is the live map; the table above is the structure it emits.

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
                    which evidence · WHICH SIMSCREENS, and the key step of each) approved BEFORE
                    any HTML exists.
3. Package          the 11 markdown documents  ->  packages/page-NN/
4. Page             docs/page-NN/index.html from the shared system, SIMSCREENs built
                    from the shared kit — steps taken from guided_lab.md (D96)
5. Case             cases/case-NN-*/ if the session ends in a full investigation
6. Lab              touch labs/ only if this session changes the lab. Most do not.
7. build_log.md     what was built · what was verified · what is open
8. Verify           Part 9 gate. Must pass before review.
9. Review           you approve.
10. Publish         then — and only then — the next session starts.
```

**Step 2 saves the most time.** It is the difference between CEH Session 1 (rebuilt 3×) and Session 2 (built once).

### The build prompt (`D125`)

**`design/prompts/PAGE_BUILD_PROMPT.md` is the single prompt for `P04`–`P14`.** Paste it as the
first message of a new session and name the page. It carries the page shape, the bilingual rules
with the term table, the visual contract, the evidence rule, the gate commands, the traps already
paid for, and a per-page table of what is buildable now and what is blocked on evidence.

The old `S1`/`S2`/`S3` prompts and `SHARED_RULES.md` moved to `design/prompts/_superseded/` — they
target `docs/session-NN/`, which no longer exists, and rules that later rows reversed.

### The package (`D86`) — one folder per PAGE, `packages/page-NN/`

**Fourteen folders, one per page of the `D84` map.** Inside every document, **each topic gets its
own clearly marked section** — sharing a folder never merges two topics (`D79`).

`session_plan.md` is **removed**: sessions are composed on the day, so a per-session plan cannot be
written in advance. It is replaced by **one** file, `design/delivery_planner.md` — every topic with
its minutes, its page, its prerequisites and its evidence — which the instructor reads to build a
day.

| # | Document | Must contain |
|---|---|---|
| 1 | `instructor_guide.md` | per topic: teaching notes · common misconceptions · the exact demo script with expected output · the bridge into the next topic |
| 2 | `student_guide.md` | **bilingual (`D76`)** — notes matching the page · a self-review walkthrough of each demo · key terms |
| 3 | `guided_lab.md` | **bilingual** — per topic: objective · environment · numbered steps, each with an **expected result** and a **verification line** · common mistakes |
| 4 | `student_activity.md` | the independent task on the carry-through case · success criteria · time box |
| 5 | `quiz.md` | 8–10 questions, MCQ + short scenario, each mapped to an objective. **Stems bilingual, options English** |
| 6 | `quiz_answer_key.md` | every answer with a one-line justification |
| 7 | `homework.md` | one practical task **plus the report stage it feeds** |
| 8 | `homework_answer_key.md` | required — `D60`: every challenge ships a key |
| 9 | `report_stage.md` | **`D85` rule 3** — which report section(s) each topic on this page fills, and a worked example of a good entry into each |
| 10 | `instructor_script_ar.md` | **`D77`** — the six-section Egyptian-Arabic delivery script |
| 11 | `build_log.md` | what was built · what was verified · what is still open |

**All eleven are required. A package with ten is incomplete.**

Site pages follow the same unit: **`docs/page-NN/`**.

### The forensic report (`D7` · `D85`) — ONE report, twelve sections, filled out of order

**The student writes one report for the whole course, on the carry-through case, and it grows as
topics are learned.** Not one report per session. `D20`'s four criteria grade that one growing
document at every session.

| # | Section | Filled by |
|---|---|---|
| 1 | Case identification | `T01` |
| 2 | Executive summary | `T25` — **written last** |
| 3 | Authorisation & scope | `T02` |
| 4 | Chain of custody | `T03`, then every session close |
| 5 | Evidence inventory + hashes | `T03`, growing with each new item |
| 6 | Tools & methods, with versions | **every topic** adds the tool it used |
| 7 | Acquisition details | `T06`·`T07` memory · `T08`·`T09` disk |
| 8 | **Findings — fact only, each tied to a named artifact** | `T04` → `T23` |
| 9 | **Interpretation — separate** | `T25` |
| 10 | **Limitations & what could not be determined** | every topic adds its line |
| 11 | Conclusions | `T25` |
| 12 | Appendices — raw output · hashes · timeline | `T24` |

**Four rules (`D85`):**

1. **Sections fill in learning order, not report order.** A student may write section 8 long before
   section 3, and that is correct — it is how real casework runs. Say this to students out loud;
   the belief that a report is written front to back is what makes people leave it to the end.
2. **A complete worked model report ships on the report page from day one**, fully written to
   professional standard, so the student can see the destination before starting. **It is written
   on a DIFFERENT case from the student's carry-through case** — a model on the same case is an
   answer key.
3. **Every topic's report stage (`D79` part 4) names the exact section it fills and shows what a
   good entry into that section looks like.** A topic that does not say which section it feeds has
   not finished.
4. **`T25` is the assembly, taught as its own skill** — reorder into report order, write the
   executive summary, interpretation, limitations and conclusions last, and verify no section is
   empty. Assembling a report is a skill; it is not clerical work that happens by itself.

A **section tracker** on the report page shows what is filled and what is still empty. It exists
precisely because the sections fill out of order.

The `D7` template, unchanged:

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

### Page shape (`D88` · `D101`) — a DECK OF SCREENS, composed from its topics

**Replaces the old Tier A / Tier B session shapes.** A page is not a fixed page-count any more; it
is its topics — but it is **not one long scroll** either.

🔴 **A page is a deck of screens, one idea per screen (`D101`).** `.page-layout` → `.sidebar`
(`.page-list`) + `.main` (`.page` sections) + `.page-nav`, driven by `docs/assets/js/session.js`:
prev/next buttons, ← → Home End keys, `#pN` deep links, and a live counter. **Only one screen is
visible at a time.** Twenty-ish screens per page is normal.

**The rule that decides where a screen ends: one idea.** If a screen carries two things the student
could be asked about separately, it is two screens. A screen that scrolls has already failed.

```
1   Cover — the page, and what it lets you prove
2   How this page works · objectives
3   Recap — what the previous page established (the bridge into this one)

    ── repeated for EACH topic on the page ──
    Tn · Bridge            the link from the topic before it
    Tn · Theory            concept · artifacts on R10's six boxes · SOC chip where it is real
    Tn · Guided lab        numbered steps, each opening with the theory it applies
    Tn · Independent       the student alone, on the carry-through case
    Tn · Report stage      which report section this fills, and a good entry into it
    Tn · Knowledge check   mixed .q.mcq + <details> reveal
    ── end ──

N-2 Cheat sheet (Print button) · what you can now sign
N-1 Homework + the report sections it feeds
N   References — INE module and lesson only
```

- **No break page.** The break falls at a topic boundary chosen on the day (`D79`), so it cannot be
  baked into one page. The 15-minute timer lives in the page furniture and the instructor triggers
  it wherever the seam falls.
- **The old Tier B catalogue shape survives as a within-topic pattern**, not a second page type: a
  topic made of many small uniform artifacts (registry, Windows artifacts) lays its theory out as a
  uniform six-box catalogue. That is a layout choice inside a topic, not a different kind of page.
- **At least one question per page has the correct answer "this artifact cannot prove that."**
  Stricter than `D60`'s one-per-session, and it is the thing no THM room does.
- Every page keeps: prev/next nav + `kbd-hint` · the cheat sheet with a Print button ·
  `#taskList` homework + task-creator modal · bilingual throughout (`D76`).

### Typography and layout (`D92`) — read from the back of the room

The page is read on a projector by a student who is not sitting at it. Every rule below follows from
that one fact.

1. **Body text is sized for the room, not the laptop.** **`D78`'s instruction to drop the English
   type one step is cancelled** — it was there to absorb the bilingual layer's height, and the height
   is now absorbed by longer pages instead, which is already accepted. Only the **Arabic** line is
   smaller.
2. **Title above body, clearly.** The topic title is visibly larger than its text — the reader must
   be able to tell what they are looking at from across the room, before reading a word.
3. **No stacked sentences.** A prose block is **never narrower than 45 characters**; the target
   measure is **65–80**. Anything narrower than 45ch carries labels and short phrases only, never
   sentences. A sentence broken into a narrow tower is a layout defect, not a style.
4. **The middle is for the topic and its explanation.** Notes, caveats, asides and `SOC` chips sit in
   a **side rail** — they never interrupt the main column's reading flow.
5. **Blocks are placed, not centred by default.** The page is a grid: content may sit left or right,
   with its own space. A stack of centred cards is not the layout.
6. **The reader can always feel the move from one point to the next** — each part of a topic
   (`D79`) carries a visible position marker, and the transition between points is stated, not
   implied by whitespace.

**The Arabic line (`D76` · `D92`):**

- **In the same box as its English**, directly after it. Never a separate box, never a parallel
  column.
- **A clear gap above it** — the two must not read as one block glued together.
- **`dir="rtl"`, right-aligned**, smaller than its English and muted.
- **Full width of its container (`D106`)**, so its start edge is in the same place on every block.

### Images (`D93`) — real, sourced, attributed

**The material uses real images. This is a requirement, not a preference.**

| Source | Use | Attribution |
|---|---|---|
| **Our own lab capture** — FTK Imager on our evidence, Registry Explorer on our hive, Wireshark on our pcap | **Preferred wherever equally good** — it shows the student *their own case* | none needed |
| `Resources/Instructor` | Freely — it is the previous ITGate instructor's own work, not third-party courseware | internal credit |
| **THM · INE · vendor · web** | Yes, for teaching | **a visible source line under every image** — small, muted: *Source: TryMe Hack Me — room name* / *Source: INE eCDFP, Module N* |
| **Tool logos** | **The official logo. Never a substitute or a redrawn one** | vendor name where it is not obvious |

- **Every image is registered** in `design/image_sources.md`: file · what it shows · source · URL or
  document · date captured. An image with no row is not published.
- **Sizing (`D92`):** an image is never so small it must be squinted at, never so large it pushes the
  explanation off the screen. It sits in the grid like any other block, with its own space.
- **`R9` is unchanged and overrides everything here:** never an image containing real personal data,
  real credentials, a real case, or a real person's device.

### The diagram system (`D94`) — the state machine, not the slideshow

**Nearly everything gets a visual.** A teaching block that is prose only is the exception and has to
earn it. The student should be able to follow a page by its figures and read the text for the
detail — not the other way round.

**Ten patterns. Every figure is built from these, not invented fresh:**

| # | Pattern | Use it for |
|---|---|---|
| 1 | **Whole system on screen from frame one** — the structure never appears or disappears, only its **state** changes | everything. This is the rule the other nine sit on |
| 2 | **Parallel rows, identical layout** — one row per variant, so the *difference* is the only thing that moves | MD5 vs SHA-256 · E01 vs raw vs AD1 · FAT vs NTFS · logical vs filesystem vs physical acquisition · **Prefetch vs Amcache vs ShimCache** |
| 3 | **Spotlight walk** — one row lights (border glow, tinted fill), the rest dim, and **a one-line plain explanation fades in inside the lit row** | any comparison |
| 4 | **Step counter / status banner** — `Stage 3 / 6`, with the accent colour of the current stage | the `D87` attack chain · an acquisition sequence · a tool's workflow |
| 5 | **Accumulation** — coloured chips stacking to show structure being built | sector → cluster → slack · an `$MFT` record field by field · a custody form gaining signatures · **the report filling section by section (`D85`)** |
| 6 | **Live values** — numbers changing in place as the state advances | a hash changing when one byte changes · run counts · sector offsets |
| 7 | **Real chrome** — a real window frame, a real prompt, the real font | tool windows, terminals, browsers |
| 8 | **Changing caption** — one plain-language line under the figure that changes with the step and states the takeaway | every animated figure |
| 9 | **One colour per concept, held for the whole course** | each artifact type, each acquisition format, each attack stage |
| 10 | **Dark ground, subtle grid, zero decorative motion** | everything. Nothing bounces, nothing spins |
| **11** | **`SIMSCREEN`** — a recreated screen, walked step by step (`D95`) | **the standard visual for theory.** Any procedure the student will carry out on a machine |

**Animation has two modes now — `D51` is extended:**

| Mode | When | Control |
|---|---|---|
| **Looping (no button)** | a **comparison or a cycle** with no beginning or end — the spotlight walk, the request counter | runs on its own, respects `prefers-reduced-motion` |
| **Click to play** | a **mechanism with a story** — a beginning, a middle, an end | the existing `.svg-play` control (`D51`) |

`D51`'s SMIL rules are unchanged for click-to-play figures: one full-length `<animate>` per element
with computed `keyTimes`, never `fill="freeze"` at staggered offsets; never animate `fill` through a
`var()`; `stroke-width` ≥ 1.5 and text ≥ 12 units.

**Fabrication — the line, precisely (`D94` · `D95`):**

- A **recreated interface** — a dialog's layout, its buttons, its menus — is a *diagram of a UI* and
  is allowed. `SIMSCREEN` is built entirely this way.
- A **finding** — a hash, an artifact value, a path, a timestamp, a command's output presented as
  something our case shows — **must be real**. Until the lab produces it, the figure carries a
  visible provisional line and is replaced the moment the evidence exists.
- Never a *stylised approximation of real output* passed off as the real thing. That is both the
  cartoon look and an integrity failure.

### `SIMSCREEN` (`D95`) — the named component

**The standard visual for theory.** A procedure the student is about to perform, shown as a screen
being operated: every screen **built from scratch in HTML/CSS, never a screenshot**.

| Layer | What it uses |
|---|---|
| **Theory** | `SIMSCREEN` — recreated screens. *"This is what is about to happen."* |
| **Practical** | **real screenshots**, captured by the instructor on `FOR-WS01` against our own evidence |

**Anatomy — fixed, so every one is the same:**

- A **step list**. One step = **one action on one screen**.
- **Animated cursor** travelling to the target · **pulsing ring** on it · **spotlight** dimming the
  rest of the window.
- **Bilingual caption** per step (`D76`) — what to do, and the reason it matters.
- **Step counter, dots, `PREV` / `PAUSE` / `NEXT`.** It auto-plays and loops; the instructor pauses
  on any step and talks over it.
- **Exactly one step may be marked `key`** — it renders amber, and it is the decision the whole
  procedure turns on. If nothing on the screen matters more than the rest, the procedure is not
  worth a `SIMSCREEN`.
- Targets are resolved from the DOM at runtime, so a hotspot can never drift from its element.

**Invocation: “simscreen for `<topic>`”.** The component is generated from a steps array; only the
recreated screens and the step captions change.

### `SIMSCREEN` is shipped infrastructure (`D96`)

There will be many of these, and they must all be this good or better. That is only achievable if
each one is **assembled from a kit rather than built from scratch**:

| File | What it holds |
|---|---|
| `docs/assets/js/simscreen.js` | the engine — step advance, cursor, ring, spotlight, caption swap, counter, dots, `PREV`/`PAUSE`/`NEXT`, DOM hotspot resolution, reduced-motion |
| `docs/assets/css/simscreen.css` | the shell — stage, holder, mask, ring, cursor, caption, controls |
| `docs/assets/css/win-ui.css` | **the recreated-interface library** — title bar · menu bar · dropdown menu · fieldset + legend · radio · checkbox · text field · list box · buttons (default / disabled) · combo · progress bar · status bar · Start menu · Explorer pane · terminal · hex pane. Each matched to real Windows metrics, not approximated |

A page then supplies **only** its screens (markup built from the library) and its steps array.

**The step list is not written twice.** A `SIMSCREEN`'s steps **are** the steps of
`guided_lab.md` — theory shows the procedure, the practical performs it, and they cannot drift
because they are one list.

**Every procedure a student will perform gets a `SIMSCREEN`.** It is named in the outline gate
(`D9`) and recorded in `build_log.md`.

**The quality bar — ten checks, and a `SIMSCREEN` does not ship until all ten pass:**

1. Every screen is DOM. **Zero images.**
2. Windows metrics are correct, not approximated — control sizes, fonts, colours, spacing.
3. **One action per step.** A step doing two things is split into two.
4. **Exactly one `key` step.** None qualifying means the procedure does not need a `SIMSCREEN`.
5. Every caption gives the **reason**, not just the action.
6. Bilingual, and the Arabic is **shorter** than the English (`D76` rule 4).
7. Hotspots resolved from the DOM, never hard-coded coordinates — **and no offset constant that
   compensates for a CSS value in another file (`D107`).** `.ss-mask` is `inset:0`, so `place()`
   writes the holder's own coordinates unmodified.
7a. **Narrow screens use `zoom`, not `transform:scale` (`D107`)** — `scale` shrinks the pixels but
   keeps the old box, so the window still overflows the stage and leaves dead space under itself.
   `place()` recovers the factor as `rect.width / offsetWidth` and divides by it, because
   `getBoundingClientRect()` is zoomed and `style.left` is not.
8. Auto-play, pause, prev/next and `prefers-reduced-motion` all verified.
9. Any value that is a **finding** carries the provisional line until the lab produces it (`D95`).
10. The step list matches `guided_lab.md` **one for one**.

### Pre-work and the depth rule (`D89`)

**Pre-work** is declared per page, in the package and on the page, and is **only ever one of three
things**:

1. **Recall** from a course earlier in the track (`D72` — link, never re-teach).
2. **Evidence download + hash verification** before class (`D18`).
3. **Tool installation** (`D17`).

**Pre-work is never new examinable material.** If a page's pre-work would have to teach something
new, that content moves into the page instead. Every pre-work item states its **time** and a
one-line **"how you know you did it"** check.

**The depth rule — how much a topic gets, and what is cut when a page overflows.** Breadth is fixed:
every INE section is covered (`D74`). *Depth* is allocated by three tests, in order:

| | Test |
|---|---|
| 1 | Does it appear in the **carry-through case** (`D87`)? |
| 2 | Does it produce a **line in the report** (`D85`)? |
| 3 | Is it a **known misread** — the ShimCache presence-vs-execution class of error? |

Three out of three earns full depth. Zero out of three earns a mention and a reference — covered,
not taught.

**Cut first, in this order:** history and background · tool or vendor comparisons that change no
decision · anything with no artifact behind it.

**Never cut, whatever the overflow:** `R10`'s *what it does NOT prove* box · the report stage · the
answer key · the bridge into the topic.

### The site under the new map (`D90`)

| Path | State |
|---|---|
| `docs/page-01/` … `docs/page-14/` | **replaces** `docs/session-01..06/`. `index.html` only |
| `brief.html` × 6 | **removed.** A per-session brief cannot exist for a session composed on the day |
| `record.html` × 6 | **becomes one** `docs/record.html` — the cumulative chain-of-custody record (`D55`) was always cumulative; six copies of it were an artefact of the session layout |
| `docs/report/` | **new** — the report page: the twelve sections, the **complete worked model report on a different case** (`D85`), and the **section tracker** |
| `docs/beyond/` | **new** — the self-study track, own index, `M01`–`M14` (`D83`) |
| `docs/roadmap.html` | regenerated from `topic_map.md`: **14 pages, 25 topics, the dependency chain** — not six sessions |
| `docs/cases/` · `docs/lab/` · `docs/resources/` | unchanged in purpose; links repointed to `page-NN` |

**Nothing is deleted until its replacement exists and passes the Part 9 gate.** The device mount
cannot delete (`R3`), so superseded files are moved to `_to_delete/` and removed in Explorer.

### The evidence gate moves to the page (`D91`)

Part 8 step 0 was per session. It is now **per page**: *a page is not built until every evidence set
its topics name is verified in `design/evidence_sets.md`.* Nothing else changes — `ecdfp-evidence`
still owns the IDs and is still the only thing that may mark a set verified.

**The six cases keep their numbers and bind to topics, not sessions:**

| Case | Bound to | What it is |
|---|---|---|
| **Case 01** | `T03` | verify four files against a signed manifest, find the tampered one |
| **Case 02** | `T09` | acquire and verify the suspect USB, then prove the acquisition is complete |
| **Case 03** | `T10` | twelve renamed / corrupted files and one hidden payload |
| **Case 04** | `T13` | wiped partition table — recover it and prove the recovery |
| **Case 05** | `T20` | which USB, which user, which program ran, when, how many times |
| **Case 06** | released at the end of the **fifth session**, debriefed in `T25` | the graded take-home capstone (`D59`) |

**Case 06's release point is now a session event, not a topic** — sessions are composed on the day,
so it is released at whatever topic boundary ends session five. The instructor is told this in
`delivery_planner.md`.

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

### The frozen page contract (`D109`) — check every page against this list

`P01` is the reference page. Its look is **approved and closed**; `P02`–`P14` inherit it and no page
re-decides it. A page that wants something this list does not have is a **new decision row in
`DECISIONS.md` first**, never a local invention.

| The page must | Decision |
|---|---|
| be a **deck of screens**, one idea each, driven by `session.js` | `D101` |
| carry the Arabic as **explanation in professional written Arabic**, never a translation | `D104` |
| put the Arabic **directly under its English, in one box that fits both** | `D108` |
| encode **FINDING / INTERPRETATION / CANNOT PROVE** three ways — colour, border style, chip | `D27` |
| use **SIMSCREEN** for procedure and real screenshots for the lab | `D95` · `D96` |
| use `D94`'s reveal figures for comparison, never a static wall | `D94` |
| make every diagram a **stepped state machine** via `dgm.js` &mdash; structure on screen from frame one, caption changes with the step, controls identical to SIMSCREEN | `D115` |
| put a figure on **every teaching screen**, not only the first few &mdash; figures that stop after screen 5 is the failure pattern 1 exists to prevent | `D94` · `D115` |
| carry **real photographs and hand-authored mechanism diagrams** &mdash; a visual on most screens, every photo registered in `design/image_sources.md` with its licence line | `D93` · `D113` |
| write the word **Section**, never the `§` glyph | `D104` |
| end on a **report stage** that advances the twelve-section report | `D85` · `D86` |
| open on **`Where we are`** carrying the lifecycle figure `dg-lc-pNN`, with the stage marked &mdash; **and the stage must differ from the pages either side of it** | `D123` |
| divide into **named PARTS with divider screens** &mdash; `PART 1` · `PART 2` · `LAB TIME` · `ON YOUR OWN` · `REPORT STAGE`, each giving its screen count and minutes | `D119` · `D123` |
| put `is-part` on the **divider's** sidebar entry and on nothing else | `D123` |
| give every screen a **plain descriptive title** that can be found in a sidebar &mdash; never an editorial headline | `D119` · `D120` |
| write every **technical term in English inside the Arabic line**, in `<script>` captions as well as in the body | `D76` r2 · `D122` |
| treat the banned table as **stems** &mdash; Arabic glues `و ف ب ك ل ال` to the front and `لل` is `ل`+`ال` | `D132` |
| let **every block in the flow share one right edge** &mdash; no per-element `max-width` inside `.page` | `D124` |

**Run both gates, in this order:**

```
python3 scripts/density_gate.py docs/page-NN/index.html     -> ALL PASS
node    testing/render_gate.js docs/page-NN/index.html      -> zero findings, 5 widths
node    testing/render_gate.js docs/index.html docs/roadmap.html   -> the site too
```

**What the two gates now assert, beyond the word counts.** Each of these was a defect that shipped
once, and each is here so it cannot ship twice:

| Check | Gate | What it caught |
|---|---|---|
| no translated technical term, **anywhere in the file** | density | ~460 violations of `D76` r2, about 60 of them inside `<script>` caption strings the first sweep never looked at (`D122`) |
| the same check, matching **stems with prefixes and suffixes** | density | 14 more violations across all eight built pages &mdash; `للترويسة`, `بصمتها`, `البصمتان` &mdash; every one of them on a page the previous version of this check had already passed (`D132`) |
| the Arabic names the **same** technical term as its English | density | ten `P03` blocks saying *hash* under English about *signatures* (`D126`) |
| **no join between Arabic and Latin script** in either order | density | `partitionان` &mdash; an Arabic dual ending on an English noun &mdash; which passed both gates and was caught by eye; and `hashاته` on `P06` (`D133`) |
| `divider screens == is-part sidebar entries` | density | a sidebar announcing a part and then opening a lesson (`D123`) |
| every teaching block carries Arabic · no Arabic beyond 2.2&times; its English · no colloquial | density | `D78` · `D104` |
| **one right edge** &mdash; every flow child of the active screen ends within 2 px | render | 1476 / 1298 / 1086 px on one screen (`D124`) |
| the Arabic box starts where its English starts | render | `D108` |
| SIMSCREEN pointer on its declared target, and spotlight agreeing with pointer **as computed** | render | `D107` · `D121` |
| no SVG `<text>` outside its own `viewBox` | render + build-time `check_widths()` | five overruns in two days (`D116`) |

**A truncated hash is not a hash.** Builds print a 16-character prefix; the manifest file holds all 64. **Copy the file.** Completing a hash from the printed prefix produced two fabricated SHA-256 values in a draft of `design/evidence_sets.md` (`D135`), and in a project whose whole claim is that the numbers are measured, a fabricated hash is the one error that discredits every other number on the page. After writing any manifest section, re-read every 64-hex string in it against the manifest file.

**A gate that only ever passes proves nothing.** Before trusting a new check, break the page on
purpose and confirm the check fails. Three of the gate's own rules were wrong on first contact
(`D110`, `D113`) and a wrong gate is worse than no gate, because the honest fix looks like moving
the goalposts.

**Run the gate on the SITE pages, not only the topic pages (`D111`).** `docs/index.html` shipped as
**one complete document plus six appended copies** of its pages grid, each after a closing
`</html>`, because the generator appended where it should have inserted. It went unseen for weeks:
a browser paints the first document correctly and parses the rest into the body below the fold. The
most-visited page in the project was the least verified one. Structural minimum for any site page:
`<html>` and `<body>` appear **exactly once**, `body.innerHTML` contains no `</html>`, zero page
errors.

`density_gate.py` counts **what is on screen** (`D110`): the Arabic layer, SIMSCREEN chrome, `<svg>`
labels and the hidden rows of a reveal figure are all excluded, because none of them is prose the
student reads at once. **A word limit that counts diagram labels pushes the author toward worse
diagrams** (`D113`) &mdash; if the gate ever fights the design system again, the gate is the bug. It also enforces the three bilingual checks — Arabic present on every teaching block, Arabic
not beyond 2.2× its English, **zero Egyptian colloquial** in student-facing Arabic.

**Render checks** — headless browser at **1400 / 1100 / 900 / 700 / 480 px**:

- [ ] Zero document-level horizontal overflow at every width
- [ ] Zero elements wider than the viewport outside a designated scroll container
- [ ] Zero SVG text escaping its `viewBox`
- [ ] Every `data-node` has exactly one matching `data-detail`; clicking each opens exactly one panel
- [ ] Zero console errors (image placeholders excepted, each listed as an open item)
- [ ] Page count matches sidebar entry count
- [ ] **Every landmark heading appears exactly once** on a site page (`D116`) &mdash; counting
      `<html>` tags is the symptom, not the property; `docs/index.html` passed that count while
      carrying two *"The fourteen pages"* sections
- [ ] **Every diagram steps**: one control bar, at least two steps, and the caption text changes
      between the first step and the last (`D115`)
- [ ] **`check_widths()` passes** before the build &mdash; every SVG `<text>` fits its `viewBox`
- [ ] **Arabic sits under its English** — single-line blocks start within 3 px of the English (`D108`)
- [ ] **No Arabic in a starved container** — a wrapping `.ar` never has under 260 px above 700 px (`D105`)
- [ ] **Every SIMSCREEN pointer lands on the element its step declares**, and the spotlight agrees
      with the pointer to within 6 px (`D107`) — "inside the window" is not the check; it passed a
      30 px offset for the life of the component
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
- **Verify a site-root change without deploying:** serve `docs/` locally (`python3 -m http.server`) and request `/`, `/page-NN/index.html` and the asset paths.
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
| **`ecdfp-session-package`** | the fixed **11** markdown documents per **page** (`D86`) | Every deliverable maps to the approved scope. Terminology identical across all eleven. **Student-facing files contain zero instructor stage directions.** The forensic report template is included every session. Edit in place for revisions. |
| **`ecdfp-session-html`** | the fixed visual + interaction system for a **page** (`D88`). Look only, never content | Start from `docs/assets/base_template.html`. Never invent a colour, font or layout pattern. Never inline CSS/JS. Never fork the stylesheet per session. Edit the affected `<section>` only — never regenerate a whole page for one change. Requires `design_system.md` + `ecdfp.css` + `session.js` + `base_template.html` to exist first. |
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
