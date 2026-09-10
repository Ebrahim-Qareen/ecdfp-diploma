# eCDFP — PAGE BUILD PROMPT (`P04`–`P14`)

**Paste this whole file as the first message of a new session, then name the page.**
It is written to be self-sufficient: everything below was learned the expensive way on
`P01`–`P03`, and a page built to it should need **no visual round trips**.

Repository root: `E:\Work\ITgate\ECDFP_Course`.
Reference pages, all three approved: `docs/page-01/index.html` · `page-02` · `page-03`.

---

## 0 · Who this is for, in one paragraph

Ebrahim Mohamed teaches the eCDFP digital-forensics diploma at ITGate Academy. His students read
English unevenly, so every page is **bilingual**: English on top, an Arabic **explanation** under it.
They sit an English exam and work in English tools, so **every technical term stays in English even
inside the Arabic**. They learn from **pictures**, not paragraphs — his exact words were *"I do not
want material that looks like a newspaper."* And they must never get lost: a page is a **numbered
deck with named parts**, not an essay.

**Report back in Egyptian Arabic, short.** The detail belongs in the files, not in the chat.
One page at a time. Never start the next page until he has said the current one is good.

---

## 1 · Read these before writing anything

| Order | File | Why |
|---|---|---|
| 1 | `00_INSTRUCTIONS.md` **Part 9** | the frozen page contract — the list a page is checked against |
| 2 | `design/page_structure.md` | the page shape, the title rules, the lifecycle table |
| 3 | `DECISIONS.md` — last 30 rows | why things are the way they are; **do not re-decide any of them** |
| 4 | `design/topic_map.md` | which topics this page owns, and their minutes |
| 5 | `design/evidence_sets.md` | whether this page's evidence exists and is verified |
| 6 | `docs/page-03/index.html` | the closest model — read the markup, not just the render |

**A page may not be built on invented findings.** That is the rule, and it is the one failure this
whole project exists to prevent. But `⛔ PENDING` evidence does **not** automatically stop the page —
split the topic by *what actually needs a corpus* first (`D127`):

- **procedure** — an order of collection, a tool run, a workflow, a decision under time pressure —
  needs a machine and a tool, not evidence. Build it at full depth.
- **investigation** — reading an artifact and stating what it proves — needs the corpus. That part
  waits, or routes to a vetted public hands-on (`design/practice_platforms.md`), and the page
  **says so on the References screen**.

**And one part of the split is a hard line, not a trade-off.** `P07` teaches malicious documents and
executables; it does **not** generate a maldoc, a macro, or any sample to teach against, and does not
substitute one. It did not need to: format structure and evidential limits are the half of that topic
that transfers to every future file, and they are teachable on a benign document and a published
benign binary. **Never build the hostile artifact — build the reader.**

On `P04` that split recovered **45 of 60 minutes** at full quality. Applying the blunt rule would
have deferred the whole page for weeks. What you may never do is write a finding you did not measure.

---

## 2 · The shape of a page — fixed, not a choice

```
01  Cover
02  Where we are          <- lifecycle figure dg-lc-pNN, this page's stage marked
03  What you will be able to do
04  ── PART 1 — <plain name of the first half> ────────────  (divider screen)
05..  teaching screens
NN  ── LAB TIME ──────────────────────────────────────────  (divider screen)
      the guided lab
NN  ── ON YOUR OWN ───────────────────────────────────────  (divider screen)
      exercises · knowledge check
NN  ── PART 2 — <plain name of the second half> ──────────  (divider screen)
NN..  teaching screens
NN  ── REPORT STAGE ──────────────────────────────────────  (divider screen)
      the report sections this page advances
NN  Summary  ·  Homework  ·  References and what comes next
```

**Five dividers is the working density** (`P01` 26 screens/5 · `P02` 25/5 · `P03` 31/5).
A divider carries: kicker · bilingual `<h2>` · rule · bilingual lede · **screen count and minutes**,
so the student sees the size of what they are entering.

`is-part` goes on the **divider's** sidebar entry and on nothing else. The gate asserts
`divider screens == is-part entries` — `P01` and `P02` once had it on content screens, so the
sidebar announced a part and then opened a lesson.

### The lifecycle marker must MOVE

| Page | Stage |
|---|---|
| `P01` | none — a band under all five (it is the map, not a place on it) |
| `P02` | 2 · PRESERVE |
| `P03` | 3 · ANALYSE |
| `P04`–`P05` | 1 · ACQUIRE — live response and imaging are acquisition |
| `P06`–`P13` | 3 · ANALYSE |
| `P14` | 4 · VALIDATE → 5 · PRESENT |

Two pages claiming the same stage empties the device of its only job. `P03` shipped saying *stage 2*
because a nice sentence justified it. **A "you are here" that does not move is decoration.**

### Titles

Descriptive, never editorial. ***What are magic bytes?*** not ***A hash proves less than you think***.
Question form for a concept, noun form for a thing, verb form for a procedure. Numbered when
sequential (`#1`…`#4`). **If you cannot guess what is on the screen from its title alone, the title
is wrong.** The insight goes in the body, the finding box or the figure caption — all three exist
and all three are better places for it.

### The definition rule

**Never use a term on screen before the screen that defines it.** `P03` opened hex on screen 3
having defined neither a byte nor how a computer stores anything. Order for anything new:
**what it is → how it works → how it is abused → what it does NOT establish → how you use it.**

---

## 3 · The bilingual layer — where most of the mistakes were

1. **Explanation, never translation.** Cover the English: does the Arabic teach the idea on its own?
   If it mirrors the English word order it is a defect however accurate it is.
2. **Every technical term in English inside the Arabic.** `الـ hash` · `الـ bytes` · `bits` ·
   `الـ header` · `الـ metadata` · `الـ chain of custody` · `الـ write blocker` · `الـ manifest` ·
   `الـ exhibit` · `الـ artifact` · `الـ findings` · `الـ interpretation` · `الـ container` ·
   `الـ clusters` · `الـ hex` · `الـ integrity` · `الـ identity` · `الـ acquisition`.
   **The full banned/allowed table is `00_INSTRUCTIONS.md` D76 rule 2.**
   **This includes `<script>`** — the SIMSCREEN and `Dgm` caption strings ship to the student
   exactly like body text, and ~60 violations hid there through a sweep that only matched
   `<span class="ar">`.
3. **Professional written Arabic (MSA).** No `اللي` `مش` `عشان` `دلوقتي` `كده` `بتاع`. Spoken
   Egyptian lives in `instructor_script_ar.md`, which is the instructor's own voice.
4. **Every explanatory element carries one** — table cells, list items, box bodies, worked examples.
   A student who cannot read the English cell cannot read the table.
5. **Roughly the length of the English.** If the Arabic needs a paragraph where the English had a
   sentence, the English is too complicated — simplify the English.
6. It sits **directly under its English, in one box that fits both**.

> **When you swap a term, re-read the sentence.** `البصمة الرقمية` → `الـ hash الرقمية` strands a
> feminine adjective on an English masculine noun, and `فتتطابق البصمتان` has a dual ending nothing
> can carry (write `فتتطابق القيمتان`). Match **whole words** with an Arabic-letter lookaround — a
> substring replace turns `تُثبت` into `تُثbit`.

---

## 4 · Visual contract — this is the part he cares about most

**Nearly every screen carries a visual.** Figures that stop after screen 5 is precisely the failure
this rule exists to prevent, and he has called it out by name.

| Use | For |
|---|---|
| **stepped diagram** (`dgm.js`) | any mechanism. The whole structure is on screen from frame one; stepping changes only what is **lit**; the caption **changes with the step**. Controls are SIMSCREEN's bar, so the student learns one interaction. Not SMIL. |
| **SIMSCREEN** | a procedure the student will repeat — a recreated Windows UI walkthrough, DOM only |
| **real photograph** | physical objects — write blocker, evidence bag, drive internals. Register every one in `design/image_sources.md` with its licence line. |
| **`.cmp` reveal figure** | comparison, one row at a time |
| **table** | a set of parallel facts |

**A picture must earn its place.** Two HDD photographs were removed from `P01` because the page was
about the forensic method, not about disks — *"what does the hard disk have to do with the topic?"*
An image that is merely interesting is decoration.

**Diagrams must be CORRECT.** Two on `P02` were not: one drew three inputs converging on one box
with a single arrow to three unconnected outputs, so you could not tell which digest came from
which input; another ran its caption under the `verified` pill and pointed the red arrow **into**
it, reading as the exact opposite of the lesson. Trace every arrow and ask what a student would
conclude from it.

**Run `check_widths()` before shipping any SVG.** Five `<text>` lines shipped wider than their own
`viewBox` in two days, each costing a full render round trip.

**One right edge (`D124`).** Never put a `max-width` on anything inside `.page`. The column is the
measure; every block fills it. Three "correct" `ch` caps produced 1476 / 1298 / 1086 px on one
screen, which is what *"empty space on the right"* looks like. The render gate now fails on a 2 px
spread.

---

## 5 · Evidence

Every finding on a page must be a **measurement**, from a set that is verified and hashed. Generate
the evidence and read it **before** writing a word. On `P03` this produced the sharpest moment on
the page — `CASE-01B`'s `policy_extract.txt` **passes SHA-256 and fails MD5**, and a file whose
content changed would fail *both*, so the finding is logically about a manifest, not a changed file.
That was reasoning, not recall, and it was already in the repo unnoticed.

Tiers: **1** our own lab · **2** public corpora · **3** synthesized. State the tier.

---

## 6 · Order of work

```
0  Evidence check      verified + hashed, or stop
1  Scope confirm       topics from topic_map.md only, minutes as mapped, no expansion
2  OUTLINE GATE  ★     screen-by-screen outline — title · tag · minutes · hands-on? · which
                       figure · which evidence · which SIMSCREENs and the key step of each.
                       APPROVED BY EBRAHIM BEFORE ANY HTML EXISTS.
3  Package             the 11 markdown documents -> packages/page-NN/
4  Page                docs/page-NN/index.html, built from the frozen system
5  Case                cases/case-NN-*/ if the page ends in a full investigation
6  build_log.md        what was built · what was verified · what is open
7  Gates               both, below. Fix and re-run until clean.
8  Report              short, in Egyptian Arabic
```

**Step 2 saves the most time in the project.** Research first, always: gather every fact, figure and
evidence reading **before** opening any output-format skill or writing markup.

---

## 7 · The gates

```
python3 scripts/density_gate.py docs/page-NN/index.html    -> ALL PASS
node    testing/render_gate.js docs/page-NN/index.html     -> zero findings at 5 widths
node    testing/render_gate.js docs/index.html docs/roadmap.html
```

`render_gate.js` needs Playwright + Chromium. If the local machine cannot download Chromium, stage
the three CSS files, the JS folder, the photos and the page into the cloud workspace and run it there.

**A gate that only passes proves nothing.** Break the page on purpose and confirm the check fails
before trusting a new one. Three of this gate's own rules were wrong on first contact, and a wrong
gate is worse than none — the honest fix looks like moving the goalposts.

---

## 8 · Traps already paid for — do not re-discover these

| Trap | The lesson |
|---|---|
| `margin-inline-end` on `.ar` | resolves against the **element's own** direction; `.ar` is `rtl`, so *inline-end* means LEFT. Margins on `.ar` are **physical** on purpose. |
| `width:max-content` on a figure | resolves to the caption's **unwrapped** width (1306 px at a 480 px viewport) and `max-width:100%` cannot clamp it. Use `fit-content`. |
| `ch` for a shared width | resolves against each element's own font-size. Equal numbers, unequal pixels. A shared edge must be a shared **pixel** value on the column. |
| `transform:scale` for shrinking a window | shrinks the pixels, keeps the box. Use `zoom` — then divide by `rect.width / offsetWidth` in any hotspot maths. |
| a magic number compensating for a value in another file | the `+30` in `simscreen.js` answering `inset:-30px` in CSS moved the spotlight 30 px off at **every** width for weeks. |
| `nowrap` on a whole first table cell | swallows the Arabic too, sets a huge max-content width and starves every other column. Mark the **label** (`> b`, `> code`), never the cell. The symptom appears in the **second** column. |
| a generator that appends instead of inserts | `docs/index.html` shipped as one document plus **six** appended copies. Browsers paint the first and hide the rest below the fold. |
| verifying the symptom you were just looking at | after fixing that, it was checked by counting `<html>` tags — and the duplicate section survived. **Assert the property that matters, not the one you were staring at.** |
| timing a race in a gate | two attempts to wait for an animating ring before the correct fix: compare the two numbers `place()` **computed**, not a rendered frame. A flaky gate teaches you to re-run until it passes. |
| a limit that fights the design system | the density gate counted SVG `<text>` as prose, so a well-labelled diagram broke the word cap — pushing the author toward **worse** diagrams. |
| a regex over nested HTML for a containment check | `re.finditer` scans forward from the end of each match, so an outer `<div>` **swallows every row inside it** and they are never examined — silently, with no error. The `D126` check passed a deliberately broken page because of this. |
| trusting a gate you just wrote | **mutation-test it: break the page on purpose and confirm it fails.** This costs thirty seconds and it is the only reason `D126` was caught. The rule applies to the check you are writing right now, not only to inherited ones. |
| a table with Arabic in 3+ columns | below 1200 px each cell gets ~200 px and every Arabic line wraps to two. **Two columns is the limit** for a bilingual table — fold the third into the second as a sentence (`D129`). |
| copying a build script for the next page | `sed 's/p04/p05/'` does not match `page-04`, so the output path stayed on the previous page and **overwrote it**. Check the `<title>` of what you just wrote, every time. |
| a term with two meanings | `بصمة` is *signature* and *hash*. A one-to-one term map silently mistranslated ten blocks. When the English says X and the Arabic says Y, **the pair is the defect** — neither side is wrong alone (`D126`). |
| a banned-word list written as **forms** | Arabic glues `و ف ب ك ل ال` to the front of a word and `ل`+`ال` contracts to `لل`, so `للترويسة` slipped past a gate that had **already passed the page**. Ban **stems**, and match prefixes and suffixes — including `ة`→`ت` in `بصمتها` (`D132`). |
| loosening that match on **every** term | `أثر` is the banned translation of *artifact* **and** the ordinary word for *effect*. Split the list: stems that are only ever technical get loose matching; words that are also normal Arabic match their exact definite form only (`D132`). |
| an evidence generator that is not **deterministic** | `mkfs.fat` takes the volume serial from the clock, `mcopy` stamps the current time, FAT stores **local** time, `mkfs.fat` also stamps the **volume-label** entry, and `sgdisk` invents GUIDs the CRC32s then cover. Two builds differed in **two bytes** — enough to make the manifest a lie. **Build the set twice into two paths and `cmp` them** before publishing a hash (`D133`). |
| a backslash in a SIMSCREEN/figure caption | `EXAMPLE\user01` becomes `\u` in the inline script &mdash; an invalid Unicode escape that kills every figure on the page. The shared `fig()`/`simscreen()` builders now escape backslashes; if you write a new caption builder, **escape `\` before the quote** (`D139`). |
| an Arabic ending glued to an English word | `partitionان` &mdash; the dual ending on an English noun &mdash; **passed both gates** and was found by looking at a screenshot. Same shape as `D122`'s `تُثbit` in the other direction. The house style always puts a space between the scripts; the gate now fails on any join (`D133`). |
| **completing a truncated hash from memory** | a build prints `8d5d754731e7d5b0...` and the manifest holds the other 48 characters. **Copy the manifest file. Never finish the string.** Two fabricated SHA-256 values reached a draft of `evidence_sets.md` this way; in a project whose whole claim is that the numbers are measured, this is the one error worth more than all the others (`D135`). |
| a class name treated as a category | `figure.photo` is on the ragged-edge exclusion list because a photograph has a natural size. A 3:1 rendered comparison wearing the same class inherited the exclusion **and a 560 px cap**, and shipped squeezed on two `P06` figures. **Every entry on an exclusion list is a claim about a category** (`D134`). |
| hard-coding a layout the volume decides | the fragmented file's clusters were hard-coded and **silently overwrote the deleted file placed there a moment earlier**, removing the artifact the whole carving lesson depends on. Compute the layout from the volume and assert it afterwards (`D135`). |
| pinning a timestamp that is evidence | making `mkntfs` reproducible means forging a `$LogFile` that does not match what happened. **Name the irreproducibility and fingerprint the part that is stable** instead (`D135`). |
| quoting a spec number you did not recompute | the GPT header and array CRC32 on `P08` changed the moment the GUIDs were pinned. **Every number on a page is re-read from the evidence after any change to the generator.** |

**And the meta-lesson, which cost the most:** three separate complaints about *"empty space on the
right"* got three separate fixes, because each time the element he pointed at was treated as the
bug instead of the rule that produced it. **When he points at something, ask what produced it.**

---

## 9 · The remaining pages

| Page | Topics | Min | Evidence | Status |
|---|---|---|---|---|
| ~~P04~~ | `T06` Live Response — Order of Volatility (25) · `T07` Memory Forensics (35) | 60 | `EVS-03` memory, `EVS-09` triage | ✅ **BUILT** — see `D127` for how the blocked evidence was handled |
| ~~P05~~ | `T08` Imaging Scope & Formats (33) · `T09` FTK Imager & dc3dd (112) | 145 | `EVS-02`, `EVS-04` | ✅ **BUILT** — taught on a device the student owns (`D129`) |
| ~~P06~~ | `T10` Hidden Data & Image Forensics (80) | 80 | `EVS-10` ✅ ready | ✅ **BUILT** — every number measured from the regenerated set (`D130`) |
| ~~P07~~ | `T11` Malicious Documents & Executables (75) | 75 | `EVS-06` | ✅ **BUILT** — structure only, no sample generated (`D131`) |
| ~~P08~~ | `T12` Storage Internals & Slack (45) · `T13` MBR & GPT (68) | 113 | `EVS-07` ✅ ready | ✅ **BUILT** — every number read out of four generated, reproducible disk images (`D133`) |
| ~~P09~~ | `T14` FAT & NTFS (52) · `T15` Carving & Deleted Data (25) | 77 | `EVS-11` ✅ ready | ✅ **BUILT** — it was marked blocked in every planning document and was not; the `D127` split is why (`D135`) |
| **P10** | `T16` Registry Structure (28) · `T17` USB & Device History (35) | 63 | `EVS-02`, `EVS-04` | ⛔ blocked |
| ~~P11~~ | `T18` Evidence of Execution (40) · `T19` Shellbags, Recycle Bin, VSS (38) | 78 | `EVS-13` ✅ ready | ✅ **BUILT** — Tier 2 corpus; Amcache & VSS taught here, run in `P14` (`D138`) |
| ~~P12~~ | `T20` Windows Event Logs (49) | 49 | `EVS-14` ✅ ready | ✅ **BUILT** — six real attack .evtx, Tier 2; every finding mapped to MITRE (`D140`) |
| ~~P13~~ | `T21` Network Evidence (42) · `T22` C2 in Traffic (28) · `T23` Internet & Email (20) | 90 | `EVS-08` ✅ ready | ✅ **BUILT** — one synthesized capture carries the whole intrusion; Tier 3, byte-reproducible (`D141`) |
| ~~P14~~ | `T24` Logs & Super-Timelines (45) · `T25` Final Report & Capstone (40) | 85 | `EVS-09` ✅ ready | ✅ **BUILT** — the capstone; diploma complete, 14/14 (`D142`) |

**Next buildable without evidence:** none — `P07`–`P14` all need `EVS-02`/`EVS-04`/`EVS-06`/`EVS-08`.
Apply the `D127` split first (procedure vs investigation) before declaring any of them blocked.

**Unblocking is `labs/vm_notes/staging_plan.md` Phases C and D** — stage the compromise on
`FIN-WKS-07`, then acquire. Until those run, `P06` is the page to build.

`P08` still owes the two HDD photographs a home: they were pulled from `P01` as off-topic and held
for `T12` Storage Internals, where they are the subject rather than decoration.

---

## 10 · Every decision gets a row

A page that wants something the frozen contract does not have is **a new row in `DECISIONS.md`
first**, never a local invention. Row format: date · ID · **what was decided** (bold, with the
measurement that justifies it) · **why it is worth recording** (what it cost, and what would have
caught it earlier). Then update `00_INSTRUCTIONS.md` so the next page inherits it.

Delete anything the rebuild superseded. The folder holds one current version of everything.
