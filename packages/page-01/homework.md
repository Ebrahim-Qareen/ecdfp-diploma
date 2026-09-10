# P01 · Homework

**One practical task, and the report sections it feeds.** Due before `P02`.
<span class="ar">تكليف عملي واحد، و أقسام التقرير اللي بيغذيها. التسليم قبل `P02`.</span>

---

## Task — verify a tool you actually use, and write it up

Pick **any two tools** from `C:\Forensics\Tools\`. For each:

1. Compute its SHA-256.
2. Find its line in `TOOLS.sha256` — the lab baseline, **not** a vendor manifest.
3. Record both, and the result.
4. Record the tool's **version** — from the binary's properties or its `--version` output, not from
   the folder name.

<span class="ar">اختار **أي أداتين** من `C:\Forensics\Tools\`. لكل واحدة: احسب الـ SHA-256 · هات القيمة المنشورة من `TOOLS.sha256` · سجّل الاتنين و النتيجة · و سجّل **إصدار** الأداة من خصائص الملف أو من `--version`، مش من اسم الفولدر.</span>

---

## What goes in the report

| Section | What you add |
|---|---|
| **§1 Case identification** | complete it — case ID, your name and role, version 0.1, today's date in UTC |
| **§3 Authorisation & scope** | the three questions this examination will answer, and **one thing that is out of scope** |
| **§6 Tools and method** | one row per tool: name · **version** · what it is used for. Plus one line naming your examination platform and the `CLEAN-TOOLS` snapshot |

**§6 is the one that gets marked.** A tool without a version is not a method.
<span class="ar">**قسم ٦ هو اللي بيتصحح.** أداة من غير إصدار مش منهج.</span>

---

## Written part — one triple, on paper

From the artifact line below, write **F-01**, **I-01**, and one **cannot prove** line.

> `Prefetch\RCLONE.EXE-A1B2C3D4.pf` on `FIN-WKS-07`: run count **3**, last run
> `2026-08-25 21:14:07 UTC`, first run `2026-08-24 23:07:44 UTC`, volume serial `8C4A-19F2`.

<span class="ar">من سطر الأثر ده اكتب **F-01** و **I-01** و سطر **cannot prove** واحد.</span>

---

## Rubric — the four criteria, unchanged all course (`D20`)

| # | Criterion | Full marks here |
|--:|---|---|
| 1 | **Integrity** | both hashes recorded per tool, and the result stated — including a mismatch if you find one |
| 2 | **Method** | every tool carries a version; the platform and snapshot are named |
| 3 | **Findings** | F-01 is one fact, tied to the named artifact at its exact path, past tense, no banned word |
| 4 | **Separation** | I-01 cites F-01, states a confidence, names an alternative — and the cannot-prove line is real, not decorative |

**A perfect F-01 with a decorative cannot-prove line loses criterion 4.** The limitation is the part
most reports do not have, and it is the part this course grades hardest.
<span class="ar">**F-01 ممتاز مع سطر cannot-prove شكلي بيخسّرك المعيار الرابع.** الحد ده هو اللي معظم التقارير مفيهاش، و هو اللي الكورس بيحاسب عليه بأقصى صرامة.</span>
