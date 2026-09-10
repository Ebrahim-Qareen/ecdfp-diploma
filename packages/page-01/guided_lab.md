# P01 · Guided lab — verify the toolkit, then seal it

**`T01` guided practice · 15 min · instructor drives, you follow on your own machine.**

**These six steps are also `SIMSCREEN T01-1` on the page** (`D96`). One list. If a step changes
here, it changes there — there is only one of it.

> **Environment.** `FOR-WS01`, at the `CLEAN-BASE` snapshot. The tool set is already installed —
> installation was pre-work (`D89`). What is not done is the part that matters.
> **البيئة:** `FOR-WS01` على سناب شوت `CLEAN-BASE`. الأدوات متثبتة خلاص — التثبيت كان pre-work. اللي لسه ما اتعملش هو الجزء المهم.

---

## Why this lab exists

You are about to spend a year saying *"my tools were clean and my method was reproducible."*
This lab is the only fifteen minutes in which that sentence becomes true.
<span class="ar">هتقضي سنة و انت بتقول "أدواتي كانت نضيفة و منهجي قابل للتكرار". الربع ساعة دي هي الوقت الوحيد اللي بتخلي الجملة دي حقيقية.</span>

---

## Step 1 — find the tool set and its manifest

Open `C:\Forensics\Tools\` in Explorer. Alongside the binaries there is **`TOOLS.sha256`** — the
SHA-256 of every tool, taken at the moment the `CLEAN-TOOLS` snapshot was made.
<span class="ar">افتح `C:\Forensics\Tools\` في الإكسبلورر. جنب البرامج هتلاقي **`TOOLS.sha256`** — الـ SHA-256 لكل أداة، متاخد في اللحظة اللي سناب شوت `CLEAN-TOOLS` اتعمل فيها.</span>

> ⚠️ **Read the header of that file before you use it.** It is the **lab's baseline**, not a vendor
> manifest. It proves a tool has **not changed since the baseline**. It does **not** prove the binary
> is what the vendor shipped — nobody here verified that. Hold on to the difference; `T03` is
> entirely about it.
> <span class="ar">**اقرا أول الملف قبل ما تستخدمه.** ده **الأساس بتاع المعمل**، مش manifest من الشركة. بيثبت إن الأداة **ما اتغيرتش عن الأساس**. **مش** بيثبت إن الملف هو اللي الشركة طرحته — محدش هنا تحقق من ده. خلي بالك من الفرق؛ `T03` كله عنه.</span>

| | |
|---|---|
| **Expected result** | the folder lists the tools **and** `TOOLS.sha256` |
| **Verify** | open it: a comment header, then one `<digest>  <relative path>` line per binary |

---

## Step 2 — compute the hash of a tool you are about to trust

Pick **any line** from `TOOLS.sha256` and hash that file yourself:

```powershell
Get-FileHash 'C:\Forensics\Tools\<the relative path from the manifest>' -Algorithm SHA256
```

<span class="ar">احسب الهاش بنفسك للأداة اللي هتعتمد عليها. متفترضش إنها سليمة — اثبتها.</span>

| | |
|---|---|
| **Expected result** | a 64-character hex digest |
| **Verify** | the `Algorithm` column says `SHA256`. If it says `MD5`, you ran the wrong command |

**Common mistake.** Students run this *after* they have already used the tool on evidence. A tool
you have already trusted is a tool you cannot un-trust.
<span class="ar">الغلطة الشائعة: الطالب بيعمل ده **بعد** ما يكون استخدم الأداة على دليل. الأداة اللي وثقت فيها خلاص مش هتقدر ترجع في كلامك.</span>

---

## Step 3 — compare it against the published value

```powershell
Select-String -Path 'C:\Forensics\Tools\TOOLS.sha256' -Pattern '<the file name>'
```

Compare the two digests. **Read the first eight and the last eight characters** — a digest that
differs in the middle differs, and eyeballing the whole string is how mismatches get missed.
<span class="ar">قارن الاتنين. **اقرا أول ٨ حروف و آخر ٨** — لو مختلفين في النص يبقوا مختلفين، و البص على السلسلة كلها بالعين هو اللي بيخلي الاختلاف يعدي.</span>

| | |
|---|---|
| **Expected result** | the two digests are identical |
| **Verify** | say the result out loud: *match* or *mismatch*. A mismatch is a finding, not an inconvenience |

---

## Step 4 — open the snapshot menu

In VMware Workstation, with `FOR-WS01` selected: **VM → Snapshot → Take Snapshot…**
<span class="ar">في VMware Workstation و `FOR-WS01` مختارة: **VM → Snapshot → Take Snapshot…**</span>

| | |
|---|---|
| **Expected result** | the Take Snapshot dialog opens |
| **Verify** | the title bar of the dialog names **`FOR-WS01`** and not another VM |

---

## Step 5 🔑 — name it exactly `CLEAN-TOOLS`

| Field | Value |
|---|---|
| Name | `CLEAN-TOOLS` |
| Description | `tool set installed and hash-verified · no case data · <YYYY-MM-DD> UTC` |

<span class="ar">الاسم `CLEAN-TOOLS` بالظبط. مش `test` و لا `snap1` — `labs/setup_guide.md` و كل صفحة جاية بتشاور عليه بالاسم ده.</span>

**This is the step the whole lab exists for.**

> Every case you run this year starts from this snapshot. Take it **before** any case data touches
> the machine and you can always return to a state you can describe. Take it after, and you can
> never again say what state your tools were in — and *"my tools were clean"* becomes something you
> believe rather than something you can show.
>
> <span class="ar">كل قضية هتشتغلها السنة دي بتبدأ من السناب شوت ده. خده **قبل** ما أي بيانات قضية تلمس الجهاز، و ساعتها تقدر ترجع في أي وقت لحالة تعرف توصفها. خده بعدها، و عمرك ما هتقدر تقول أدواتك كانت في أنهي حالة — و "أدواتي كانت نضيفة" تبقى حاجة بتصدقها، مش حاجة بتثبتها.</span>

| | |
|---|---|
| **Expected result** | the dialog closes and the snapshot is written |
| **Verify** | **Step 6.** Do not assume it worked |

---

## Step 6 — confirm the lineage

**VM → Snapshot → Snapshot Manager.**
<span class="ar">**VM → Snapshot → Snapshot Manager.**</span>

| | |
|---|---|
| **Expected result** | `CLEAN-BASE → CLEAN-TOOLS`, with **You Are Here** on `CLEAN-TOOLS` |
| **Verify** | two snapshots, in that order. One snapshot means step 5 replaced the base instead of branching from it — stop and tell the instructor |

---

## Chain of custody — the line this lab produces

Nothing here touches evidence, so there is no custody transfer. What there **is**, is the first line
of §6 of your report:

> **Tools.** `<tool>` `<version>` — SHA-256 checked against the lab baseline manifest
> (`TOOLS.sha256`, generated at the `CLEAN-TOOLS` snapshot), `<YYYY-MM-DD hh:mm>` UTC.
> Examination platform `FOR-WS01`, snapshot `CLEAN-TOOLS`.

**Write what you actually did, not what sounds stronger.** *"Verified against the vendor"* would be
the first false sentence in your report, and it would be false on page one.
<span class="ar">**اكتب اللي عملته فعلاً، مش اللي شكله أقوى.** «تم التحقق مقابل الشركة» هتبقى أول جملة كذب في تقريرك — و في الصفحة الأولى.</span>

<span class="ar">مفيش نقل حيازة هنا لأننا ما لمسناش دليل. اللي في هو **أول سطر في قسم ٦** في تقريرك — الأداة و إصدارها و إن الهاش اتحقق منه، و منصة الفحص و السناب شوت.</span>

**Write it now, in the report, before you close the lab.** A tool without a version is not a method.
