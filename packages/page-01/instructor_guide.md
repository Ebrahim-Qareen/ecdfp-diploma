# P01 · Instructor guide — Foundations and the deliverable

**70 topic minutes** · `T01` Foundations & Forensic Principles (45) · `T02` The Forensic Report (25)
**Evidence required: none.** This is the only page in the course that needs no evidence set.

Internal document. Not bilingual (`D76`) — your Arabic is `instructor_script_ar.md`.

---

## 0 · Pre-class checklist

| ☐ | |
|:-:|---|
| ☐ | `docs/page-01/index.html` open on the projector; the SIMSCREEN plays and pauses |
| ☐ | `FOR-WS01` powered on, at the `CLEAN-BASE` snapshot — **not** `CLEAN-TOOLS`; taking it is the lab |
| ☐ | Every student's machine can reach the tool set and a terminal |
| ☐ | `design/report_template.md` printed or open — students need it in front of them for `T02` |
| ☐ | The six may/may-not statement cards and the five scenario cards printed (`student_activity.md`) |

---

## 1 · The two sentences this page turns on

Say these in the first five minutes, in these words.

> **1.** *"You already know how to decide whether something is bad. This course is about whether you
> can defend that in front of someone whose job is to break it."*

> **2.** *"This is the most important page in the diploma, and it needs no forensic software at all.
> Everything after it does — and none of it will save you if you skip this."*

Then show the page shape so the room knows the rhythm.

---

## `T01` — Foundations & Forensic Principles · 45 min

### Bridge + theory · 14 min

**The bridge is to the track, not to a previous topic** — this is the first topic in the course.

> *"In eCIR you worked web, network and email attacks. You contained an incident and you were right.
> Nobody asked you to prove it. This course is the part where somebody does."*

**6 min — the mandate and the life cycle.** Recover · preserve · interpret, so it survives
challenge. Life cycle **acquisition → analysis → presentation**. The point is not the three words:
**each phase can destroy the next.** Walk `P01-F2`'s companion figure and make them name the failure
at each stage.

The worked example: an examiner who double-clicks a file "just to read it" has updated its
last-access time — acquisition failed and analysis inherits a corrupted timestamp.

⚠️ **Say honestly that this specific example has aged.** Modern Windows disables last-access updates
by default. The *lesson* holds; the *effect* often does not. This is the students' first taste of
"the courseware is a decade old", and hearing it from you first buys credibility for the rest of the
diploma.

**8 min — the principles.** Minimal footprint · always work on a copy · **repeatable vs
reproducible**.

| | Meaning |
|---|---|
| **Repeatable** | same lab, same tools, same result |
| **Reproducible** | **different** lab or tools, same result |

INE requires both and the distinction is examinable. This is why *"I used the GUI and clicked
around"* is not a method. **Say that sentence out loud.**

⚠️ **Order of volatility is not taught here.** `T06` owns it and teaches it at the moment the
collection decision is actually made. One clause in passing is enough if a student raises it.

⚠️ **Linux and macOS are no longer "out of scope" (`D81`).** If the cross-platform question comes
up: the *taught* course is Windows-weighted because the exam and the casework are; Linux, macOS and
mobile are **built units in the self-study track** at `docs/beyond/`. Say where they are. Do not
call them out of scope — that answer is now wrong.

### Guided practice · 15 min — `SIMSCREEN T01-1`

Verify the tool set, then take the `CLEAN-TOOLS` snapshot. Instructor drives; **students follow on
their own machine.**

**The key step is the snapshot, and it is the last one.** Say why, in these words:

> *"Every case you run this year starts from this snapshot. If you take it after you have already
> touched a case, you can never again say what state your tools were in."*

Two things students get wrong here:

1. They **check the tools after using them**, not before trusting them. A binary is not yours until
   you have hashed it and know what that hash means.
2. They name the snapshot something like `test` or `snap1`. It is `CLEAN-TOOLS`, exactly, because
   `labs/setup_guide.md` and every later page refer to it by that name.

🔴 **The honest point you must make here, and it is the best moment in the page to make it.**
`TOOLS.sha256` is **our** baseline, generated at the snapshot. It proves a tool has not changed
since then. It does **not** prove the binary is what the vendor shipped — nobody in this lab checked
a vendor signature.

Say it, and then say why it matters:

> *"So write 'checked against the lab baseline', not 'verified against the vendor'. The second one
> is stronger and it is false. Writing the weaker sentence that is true is the entire job."*

**Quiz Q7 asks the ideal version** — a hash matching a vendor's published value, which proves
byte-identity with what the vendor published. **The lab is the weaker real case.** A student who can
say what the difference is has understood `T03` a page early.

### Independent · 12 min — they judge, you do not tell

**(a) 4 min — the sort.** Six statements, sorted *may write / may not write*. Do not pre-teach the
answer; the table below is what they should arrive at.

| You may write | You may not write |
|---|---|
| the artifact recorded X at time T | the user did X |
| the file was not present in the collected set | the file was never on the machine |
| the process was running at collection time | the process was running at the time of compromise |

**Take the answers before you confirm anything.** The wrong answers are the lesson: almost every
student writes *"the user did X"* first time, because it is what a SIEM alert says.

**(b) 8 min — five scenarios: admissible or not, and whose failure is it?** This is where INE's
three-part test is taught. Do not lecture the table first; they meet it through the scenarios.

| Test | Means | Who owns it |
|---|---|---|
| **Relevant** | proves or disproves a hypothesis in *this* case | the lawyer |
| **Reliable** | authentic (chain of custody) + objective (a fact, not an opinion) | 🔴 **you** own authenticity |
| **Competent** | obtained legally, no protected confidentiality breached | the lawyer |

**The scenario that lands:** a video that convicts the suspect is thrown out because the warrant
covered text files only. Perfect forensics, inadmissible evidence. *Whose failure?* — the answer is
**nobody's forensics**, and that is the point of separating the three tests.

**Of the three, only authenticity is yours.** Everything else is somebody else's problem, and
pretending otherwise is how analysts end up giving legal opinions they are not qualified to give.

### Report stage · 4 min

They open **the** report — one document, for the whole course (`D85`). Fill:

- **§1 Case identification** — case ID, examiner, date, version
- **§3 Authorisation & scope** — the questions this examination must answer, and **what is out of
  scope**

Say the rule that governs the rest of the course: **the sections fill in learning order, not report
order.** They will write §8 long before they finish §3, and that is correct.

---

## `T02` — The Forensic Report · 25 min · 🔴 the point of the diploma

### Bridge + theory · 8 min

**Bridge from `T01`:**

> *"You just decided which of those five scenarios would survive. This is the document where you
> have to prove it — and it is the only thing anyone outside this room will ever see."*

Walk the **twelve sections** (`P01-F3`) — but do not read them out. Show the figure filling **out of
order**, because that is the single idea in this block that changes behaviour.

Then the split, which is the course in one line:

| | | |
|---|---|---|
| **FINDING** | fact only, tied to one named artifact at an exact path | solid border |
| **INTERPRETATION** | what it means, with a confidence and an alternative | dashed border |
| **CANNOT PROVE** | what this evidence does not show | dotted border |

**The test for a finding: if it needs the word *because*, it is not a finding.**

### Guided practice · 10 min — work one triple live, on the board

Take one artifact line and build all three in front of them. Use this one:

> `System.evtx`, record 41 992, Event ID 7045, `2026-08-25 09:12:55 UTC`, service `WinDefendUpd`,
> image path `C:\Users\<user>\AppData\Local\Temp\svchost.exe`, start type auto.

Write the finding first, in the fixed format. Then ask the room for the interpretation — and
**refuse the first version**, because it will not carry a confidence or an alternative. Then write
the *cannot prove* line: this does not show who installed it, or that it ever ran.

**The two formats they must write from memory:**

- **F-nn** — `<artifact>` at `<exact path>`, `<UTC timestamp>`: `<one observable fact, past tense>`
- **I-nn** — `<claim>` is assessed with `<confidence>` confidence, resting on **F-xx**, **F-yy**.
  Considered and not excluded: `<alternative>`, because `<reason>`.

**Banned in Findings**, and say why each one is banned:

> *clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
> unauthorised*

Every one is an interpretation wearing a finding's clothes. **Also banned: naming a person.**
Artifacts record accounts, processes and devices. They do not record people.

### Independent · 5 min

Each student writes their **own** triple from a second supplied artifact line, then swaps with a
neighbour and marks it against criteria 3 and 4 of the rubric. **This is the only pairing in the
page** (`D16`) — the investigation is always individual.

### Report stage · 2 min

Mark **§2 Executive summary**, **§9 Interpretation** and **§11 Conclusions** as *written last*
(`D85`). Say why §2 is written last:

> *"A summary written first becomes the conclusion you then go looking for evidence to support.
> That is the failure this whole course exists to prevent."*

---

## Where students reliably go wrong on this page

1. **They write interpretation in the Findings section** and cannot see it. The *because* test is
   the fix, and it has to be applied out loud the first three times.
2. **They name a person.** "The user opened the document." Correct it every single time on this
   page; by `P04` it should have stopped.
3. **They think the report is written at the end.** The whole point of §2-written-last is that
   everything else is written *as you go*.
4. **They skip §10 Limitations** because it feels like admitting failure. It is graded, and a report
   with no limitation reads as a report that did not look for one.
5. **They verify the tools after installing them.** Backwards, and it is the habit `T03` is about to
   formalise.
6. **They ask whether Linux is covered.** It is — in the self-study track. Answer it in one line and
   move on.

---

## If you are running short

Cut **in this order**, and nothing else:

1. The life-cycle worked example (keep the principle, drop the aged illustration).
2. The second scenario in the independent sort — four is enough.
3. The `T02` peer-swap; keep the writing, drop the exchange.

**Never cut:** the may/may-not sort · the live triple on the board · the report opening. Those three
are the page.

---

## Bridge to `P02`

> *"You now know what has to be true for evidence to survive, and what the document that carries it
> looks like. You have not touched a single piece of evidence. Next page: proving that a file is
> exactly what it was when you got it — and the four things a hash cannot tell you."*
