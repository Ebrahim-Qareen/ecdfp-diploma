# P01 · Student guide — Foundations and the deliverable

Everything on this page, in your own time. **Terms stay in English** — they are the words the exam,
the tools and the job all use.
<span class="ar">كل اللي في الصفحة دي، براحتك. **المصطلحات بالإنجليزي** — دي الكلمات اللي الامتحان و الأدوات و الشغل بيستخدموها.</span>

---

## T01 · Foundations & Forensic Principles

### What digital forensics is

Recover, preserve and interpret digital evidence **so that it survives challenge**. The last part is
the whole job. Anyone can find the file; the question is whether what you say about it holds up when
someone whose job is to break it starts asking.
<span class="ar">تسترجع و تحافظ و تفسّر الدليل الرقمي **بحيث يصمد قدام الاعتراض**. الجزء الأخير ده هو الشغلانة كلها. أي حد يقدر يلاقي الملف؛ السؤال هو هل كلامك عنه هيصمد لما حد شغلانته يكسّره يبدأ يسأل.</span>

### The evidence life cycle

**acquisition → analysis → presentation**

The three words are not the lesson. **The lesson is that each phase can destroy the next.**
<span class="ar">التلات كلمات مش الدرس. **الدرس إن كل مرحلة تقدر تدمّر اللي بعدها.**</span>

| Phase | How it destroys the next |
|---|---|
| Acquisition | you open a file "just to read it" — the timestamp changes, and analysis now works on corrupted data |
| Analysis | you record a conclusion without the artifact it rests on — presentation has nothing to show |
| Presentation | you state more than the evidence supports — the whole examination is discredited, including the parts that were right |

> ⚠️ The classic example — double-clicking a file changes its last-access time — **has aged.**
> Modern Windows disables last-access updates by default. The lesson holds; that particular effect
> often does not. You will meet more of this: the courseware is a decade old in places, and knowing
> which parts have aged is part of being good at this.
> <span class="ar">المثال الكلاسيكي — إن الدبل كليك بيغيّر آخر وقت وصول — **بقى قديم.** ويندوز الحديث بيقفل التحديث ده افتراضياً. الدرس صح؛ التأثير ده تحديداً غالباً لأ. هتقابل ده كتير: المنهج قديم في حتت، و إنك تعرف إيه اللي قدم ده جزء من إنك تبقى شاطر في الشغلانة.</span>

### The three principles

| | |
|---|---|
| **Minimal footprint** | change as little as possible, and record everything you did change |
| **Always work on a copy** | the original is evidence; your working copy is where you work |
| **Repeatable and reproducible** | both, always |

**Repeatable** = same lab, same tools, same result.
**Reproducible** = **different** lab or tools, same result.
<span class="ar">**Repeatable** = نفس المعمل و نفس الأدوات و نفس النتيجة. **Reproducible** = معمل أو أدوات **مختلفة** و نفس النتيجة.</span>

INE requires both, and the distinction is examinable. It is also why *"I used the GUI and clicked
around"* is not a method — nobody, including you next month, can repeat it.
<span class="ar">و ده كمان سبب إن "استخدمت الواجهة و دوّست هنا و هنا" مش منهج — محدش، و لا انت الشهر الجاي، يقدر يعيدها.</span>

### What you may not claim

This is the first appearance of the rule the whole course is built on.

| You may write | You may not write |
|---|---|
| the artifact recorded X at time T | the user did X |
| the file was not present in the collected set | the file was never on the machine |
| the process was running at collection time | the process was running at the time of compromise |

**Artifacts record accounts, processes and devices. They do not record people.**
<span class="ar">**الآثار بتسجّل حسابات و عمليات و أجهزة. مش بتسجّل بني آدمين.**</span>

### What makes evidence defensible

| Test | Means | Who owns it |
|---|---|---|
| **Relevant** | proves or disproves a hypothesis in *this* case | the lawyer |
| **Reliable** | authentic (chain of custody) + objective (a fact, not an opinion) | 🔴 **you** own authenticity |
| **Competent** | obtained legally, no protected confidentiality breached | the lawyer |

**Only authenticity is yours.** Everything else is somebody else's problem — and pretending
otherwise is how analysts end up giving legal opinions they are not qualified to give.
<span class="ar">**الـ authenticity بس هي بتاعتك.** الباقي مشكلة ناس تانية — و إنك تدّعي العكس هو اللي بيخلي المحللين يدّوا آراء قانونية مش مؤهلين ليها.</span>

> A video that convicts the suspect is thrown out because the warrant covered text files only.
> Perfect forensics, inadmissible evidence. **Whose failure is that?** Nobody's forensics — and that
> is exactly why the three tests are separated.
> <span class="ar">فيديو بيدين المتهم بيتشال لأن الإذن كان بيغطي ملفات نصية بس. تحليل جنائي ممتاز، و دليل مرفوض. **غلطة مين؟** مش غلطة التحليل الجنائي — و ده بالظبط سبب إن التلات اختبارات منفصلين.</span>

### The `CLEAN-TOOLS` snapshot

Your analyst workstation gets a snapshot taken **after** the tools are installed and hash-verified,
and **before** any case data touches it. Everything you do this year starts from there.
<span class="ar">جهاز التحليل بتاعك بياخد سناب شوت **بعد** ما الأدوات تتثبت و يتحقق من الهاش بتاعها، و **قبل** ما أي بيانات قضية تلمسه. كل اللي هتعمله السنة دي بيبدأ من هناك.</span>

Take it late and *"my tools were clean"* becomes something you believe rather than something you can
show. See `guided_lab.md`.

---

## T02 · The Forensic Report

### One report, twelve sections, filled out of order

You write **one** report for this whole course, on one case, and it grows as you learn. Not one per
session.
<span class="ar">بتكتب **تقرير واحد** للكورس كله، على قضية واحدة، و بيكبر مع اللي بتتعلمه. مش واحد كل سيشن.</span>

**The sections fill in learning order, not report order.** You will write §8 Findings long before
you finish §3 Scope, and that is correct — it is how real casework runs. Believing a report is
written front to back is what makes people leave it to the end.
<span class="ar">**الأقسام بتتملا بترتيب التعلم، مش ترتيب التقرير.** هتكتب قسم ٨ قبل ما تخلص قسم ٣ بكتير، و ده صح — كده الشغل الحقيقي بيمشي. الاعتقاد إن التقرير بيتكتب من الأول للآخر هو اللي بيخلي الناس تسيبه للنهاية.</span>

The full template is in `docs/report/`. Three sections are written **last**: §2 Executive summary,
§9 Interpretation, §11 Conclusions.

### Finding · Interpretation · Cannot prove

| | | Border on the page |
|---|---|---|
| **FINDING** | fact only, tied to one named artifact at an exact path, with a UTC time | **solid** |
| **INTERPRETATION** | what it means — with a confidence and at least one alternative | **dashed** |
| **CANNOT PROVE** | what this evidence does not show | **dotted** |

**The test for a finding: if it needs the word *because*, it is not a finding.**
<span class="ar">**اختبار الـ finding: لو محتاج كلمة "لأن"، يبقى مش finding.**</span>

The border style is not decoration — solid means *observed*, dashed means *reasoned*. You will see
the same three borders on every page of this course.

### The two formats, from memory

> **F-07** — `System.evtx` on `FIN-WKS-07`, record 41 992, Event ID 7045, `2026-08-25 09:12:55 UTC`:
> a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

> **I-03** — The service in **F-07** is assessed, with **high** confidence, to be attacker
> persistence: the name imitates a Microsoft component, the binary sits in a user-writable temp
> directory, and it was installed 41 seconds after the execution in **F-05**. Considered and not
> excluded: a legitimate third-party installer using a misleading name — no installer entry was
> found in `Application.evtx`, but that log covers only 6 days (**F-02**).

### Banned in Findings

> *clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
> unauthorised*

Every one of them is an interpretation wearing a finding's clothes.
<span class="ar">كل واحدة فيهم interpretation لابسة هدوم finding.</span>

**And never name a person as the actor.**

---

## Key terms

| Term | |
|---|---|
| **Digital forensics** | recovering, preserving and interpreting digital evidence so it survives challenge |
| **Repeatable** | same lab, same tools, same result |
| **Reproducible** | different lab or tools, same result |
| **Authenticity** | that the evidence is what you say it is, and has not changed — **the examiner's responsibility** |
| **Admissibility** | whether a court will accept the evidence: relevant + reliable + competent |
| **Finding** | one observable fact tied to one named artifact |
| **Interpretation** | what a finding means, with a confidence and an alternative |
| **`CLEAN-TOOLS`** | the snapshot of your workstation taken after tools are verified and before any case data |
