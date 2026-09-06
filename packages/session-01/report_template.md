# Forensic Report — Template

**eCDFP Diploma · ITGate Academy**

**This template is fixed from Session 1 and does not change.** You submit a version of it every
session, and it is graded every session against the same four criteria. That is deliberate: seeing
the same target six times is the only way to prove your report writing is improving.

**Findings versus interpretation is the whole course in one line.** Sections 6 and 7 are separate
sections, not two headings on one page, and the boundary between them is what criterion 4 grades.

---

## The rubric — four criteria, unchanged all six sessions

| # | Criterion | Full marks | Owned by |
|--:|---|---|:-:|
| 1 | **Integrity** | hashes recorded before and after · verified against the manifest · chain of custody complete: who · what · when · from where · hash · where stored | §3 · §10 |
| 2 | **Method** | reproducible by another analyst · every tool named with its version · steps in the order performed | §4 · §5 |
| 3 | **Findings** | fact only · each finding tied to one named artifact at an exact path · nothing asserted the evidence does not show | §6 |
| 4 | **Separation** | interpretation visibly distinct from findings · limitations stated · at least one honest *"this evidence cannot show X"* | §7 · §9 |

---

## 1 · Case reference

| Field | |
|---|---|
| Case ID | |
| Requesting party | |
| Examiner name and role | |
| Report version | |
| Date issued (UTC) | |
| Classification / handling | |

---

## 2 · Scope and authorisation

What you were asked to determine, and under what authority.

State explicitly:

- the questions the examination was asked to answer
- **what was outside scope**, and on whose instruction
- any authorisation limit that constrained what you could examine

> A case arrives with a scope and an objective, not just with evidence. An examination that
> silently exceeds its scope produces evidence that may be inadmissible however good the work was.

---

## 3 · Evidence received

One row per exhibit. **Both hash algorithms, every time.**

| Exhibit ID | Description | Size | MD5 | SHA-256 | Received from | When (UTC) | Custody ref |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Also record:**

| | |
|---|---|
| Hash **at acquisition** | as supplied |
| Hash **re-verified at analysis** | computed by you, with the command used |
| Result | match / mismatch — **a mismatch is recorded here, not omitted** |

> SHA-256 is the value you defend. MD5 is recorded alongside it as a lookup key, and never as the
> integrity control.

---

## 4 · Tools and versions used

| Tool | Version | Used for |
|---|---|---|
| | | |

**A tool without a version is not a method.** A command is only correct against a stated version,
and the reader has to be able to reproduce your result on the same build.

---

## 5 · Method

What you did, in the order you did it, in enough detail that another analyst reaches the same
result without asking you a question.

Include:

- the working copy used, and confirmation the original was not worked on
- the examination platform
- each step in sequence, with the command or action
- the **time basis**: the evidence host's time zone, how it was determined, and any measured clock
  skew

> **Repeatable** means same lab, same tools, same result. **Reproducible** means different lab or
> tools, same result. Both are required. *"I used the GUI and clicked around"* is neither.

---

## 6 · Findings

**Fact only.** Numbered `F-01`, `F-02`, …

Each finding is **one observable fact**, in the past tense, tied to **one named artifact** with its
exact location and a UTC timestamp.

**The test:** if it needs the word *because*, it is not a finding.

**Format:**

> **F-07** — `System.evtx` on `WKSTN-07`, record 41 992, Event ID 7045,
> `2026-03-03 09:12:55 UTC`: a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

**Banned in this section:**

> *clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
> unauthorised*

Every one of them is an interpretation wearing a finding's clothes.

**Also banned here:** naming a person as the actor. Artifacts record accounts, processes and
devices. They do not record people.

---

## 7 · Interpretation

**What it means.** Numbered `I-01`, `I-02`, …

Each interpretation must do three things:

1. **cite the finding numbers it rests on**
2. **state a confidence** — high, moderate, low
3. **name at least one alternative explanation**, and say why it was rejected or could not be
   excluded

**Format:**

> **I-03** — The service in **F-07** is assessed, with high confidence, to be attacker
> persistence: its name imitates a Microsoft component, its binary sits in a user-writable temp
> directory, and it was installed 41 seconds after the document execution in **F-05**.
> Considered and not excluded: a legitimate third-party installer using a misleading name — no
> corresponding installer entry was found in `Application.evtx`, but the log covers only 6 days
> (**F-02**).

**No absolute terms.** Not *"we are sure"*, not *"we are certain"*. The analysis is your
interpretation, not absolute truth, and writing it as truth is what gets a report taken apart.

---

## 8 · Conclusion

Answers to the questions in §2, and nothing else.

**No new facts appear here.** If it is not in §6, it does not belong in §8.

> **You are not the judge.** Never write *"in my opinion Mr X committed this crime."* Present
> method and evidence. The decision is not yours.

---

## 9 · Limitations

Everything not examined, and **why** — especially the technical reasons.

Cover:

- data that did not exist, or could not be recovered
- artifacts whose absence is explained by **policy or retention** rather than by the event not
  happening
- anything outside the authorisation in §2
- at least one honest **"this evidence cannot show X"**

> Most reports have no section like this. **This one does, and it is graded.** A report that states
> no limitation reads as a report that did not look for one.

---

## 10 · Exhibits

Bulky supporting material, referenced from the sections above and never inline:

- full tool output
- hash lists and manifests
- log extracts
- the chain-of-custody record for each exhibit
- glossary of acronyms and technical terms used
- references, checked and current

### Chain-of-custody line

One line per transfer, per exhibit. No transfer without two signatures.

| Who | What | When (UTC) | From where | Hash | Where stored | Signature |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## Write it as you go

Reporting is not a stage that begins when analysis ends. **The report starts when the
investigation starts and is updated as it progresses.** Reconstructing your own work into a report
afterwards is how mistakes get in — and in this course you hand in the same growing document each
session, not a new one.

---

## Before you submit

| ☐ | |
|:-:|---|
| ☐ | Every finding survives the *because* test |
| ☐ | No banned word appears in §6 |
| ☐ | No person is named as an actor in §6 |
| ☐ | Every interpretation cites a finding by number |
| ☐ | Every interpretation states a confidence and names an alternative |
| ☐ | §9 exists and is not empty |
| ☐ | Every tool in §4 carries a version |
| ☐ | Both MD5 and SHA-256 are recorded for every exhibit |
| ☐ | One date format throughout; one term per concept throughout |
| ☐ | No sentence assigns guilt |
