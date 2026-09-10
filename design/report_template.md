# Forensic Report — Template

**eCDFP Diploma · ITGate Academy** · the fixed structure (`D7` · `D85`).
Canonical source. The student-facing copy is `docs/report/`.

**You write ONE report for the whole course**, on the carry-through case, and it grows as topics
complete. Not one per session. It is graded at every session against the same four criteria — seeing
the same target repeatedly is the only way to prove your report writing is improving.

**The sections fill in learning order, not report order.** You will write §8 long before §3, and
that is correct: it is how real casework runs. The belief that a report is written front to back is
what makes people leave it to the end.

**Findings versus interpretation is the whole course in one line.** §8 and §9 are separate sections,
not two headings on one page, and the boundary between them is what criterion 4 grades.

---

## The rubric — four criteria, unchanged

The wording has never changed and does not change here; only the section numbers it points at were
re-pointed when the template went from ten sections to twelve (`D99`).

| # | Criterion | Full marks | Owned by |
|--:|---|---|:-:|
| 1 | **Integrity** | hashes recorded before and after · verified against the manifest · chain of custody complete: who · what · when · from where · hash · where stored | §4 · §5 |
| 2 | **Method** | reproducible by another analyst · every tool named with its version · steps in the order performed | §6 · §7 |
| 3 | **Findings** | fact only · each finding tied to one named artifact at an exact path · nothing asserted the evidence does not show | §8 |
| 4 | **Separation** | interpretation visibly distinct from findings · limitations stated · at least one honest *"this evidence cannot show X"* | §9 · §10 |

---

## Which topic fills which section

| # | Section | Filled by |
|--:|---|---|
| 1 | Case identification | `T01` |
| 2 | Executive summary | `T25` — **written last** |
| 3 | Authorisation & scope | `T01` |
| 4 | Chain of custody | `T03`, then every session close |
| 5 | Evidence inventory + hashes | `T03`, growing with each new exhibit |
| 6 | Tools and method | **every topic** adds the tool it used |
| 7 | Acquisition details | `T06`·`T07` memory · `T08`·`T09` disk |
| 8 | Findings | `T04` → `T23` |
| 9 | Interpretation | `T25` |
| 10 | Limitations | every topic adds its line |
| 11 | Conclusions | `T25` |
| 12 | Appendices | `T24` |

---

## 1 · Case identification

| Field | |
|---|---|
| Case ID | |
| Requesting party | |
| Examiner name and role | |
| Report version | |
| Date issued (UTC) | |
| Classification / handling | |

---

## 2 · Executive summary

**Written last, read first.** Half a page, for a reader who will not read the rest — a manager, a
lawyer, a client.

State, in this order:

- who asked, and what question the examination was asked to answer
- what was examined — exhibits, in one line
- **what was found**, in two to four sentences of plain language, no artifact names
- what it means at the top level, marked as interpretation
- **the single most important limitation**, stated here and not buried in §10

> Write it after §11, never before. A summary written first becomes the conclusion you then go
> looking for evidence to support — which is the failure mode this whole course exists to prevent.

---

## 3 · Authorisation & scope

What you were asked to determine, and under what authority.

State explicitly:

- the questions the examination was asked to answer
- **what was outside scope**, and on whose instruction
- any authorisation limit that constrained what you could examine

> A case arrives with a scope and an objective, not just with evidence. An examination that silently
> exceeds its scope produces evidence that may be inadmissible however good the work was.

---

## 4 · Chain of custody

One line per transfer, per exhibit. **No transfer without two signatures.**

| Who released | Who received | Exhibit | When (UTC) | From where | Purpose | Hash re-verified | Signatures |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**A gap is declared, not hidden.** If an exhibit was unaccounted for between two times, that fact
goes in this table with the times either side of it. A gap you state is a weakness; a gap the other
side finds is the end of the exhibit.

> This is its own section, not a line in an appendix. SWGDE 18-F-002 sets the minimum: a unique
> identifier, the date and time, and every transfer identifying each person taking possession by
> name and signature.

---

## 5 · Evidence inventory and hashes

One row per exhibit. **Both hash algorithms, every time.**

| Exhibit ID | Description | Size | MD5 | SHA-256 | Received from | When (UTC) | Custody ref |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Also record, per exhibit:**

| | |
|---|---|
| Hash **at acquisition** | as supplied |
| Hash **re-verified at analysis** | computed by you, with the command used |
| Result | match / mismatch — **a mismatch is recorded here, not omitted** |

> SHA-256 is the value you defend. MD5 is recorded alongside it as a lookup key, and never as the
> integrity control.

---

## 6 · Tools and method

**Tools — a tool without a version is not a method.**

| Tool | Version | Used for |
|---|---|---|
| | | |

**Method — what you did, in the order you did it**, in enough detail that another analyst reaches
the same result without asking you a question.

Include:

- the working copy used, and confirmation the original was not worked on
- the examination platform
- each step in sequence, with the command or action
- the **time basis**: the evidence host's time zone, how it was determined, and any measured clock
  skew

> **Repeatable** means same lab, same tools, same result. **Reproducible** means different lab or
> tools, same result. Both are required. *"I used the GUI and clicked around"* is neither.

---

## 7 · Acquisition details

How each exhibit came to exist. Separate from §6 because acquisition is the one step that cannot be
repeated — if it was done wrong, nothing below it can be fixed by doing the analysis better.

Per exhibit:

| | |
|---|---|
| Acquisition tool and version | |
| Method | physical / logical / filesystem / live |
| Format | E01 · raw · AD1 · memory image |
| Write protection | hardware blocker make and model, engaged **before** the source was connected — or the explicit statement that the source was read-only and why no blocker was required |
| Source identification | make · model · **serial**, never the drive letter |
| Hash before and after, and the verification result | |
| Acquired by · when (UTC) · where | |
| **Deviations** | anything that did not go to plan, and what was done about it |

> A source is identified by its serial, not its drive letter. A drive letter is assigned by Windows
> and means nothing in a report.

---

## 8 · Findings

**Fact only.** Numbered `F-01`, `F-02`, …

Each finding is **one observable fact**, in the past tense, tied to **one named artifact** with its
exact location and a UTC timestamp.

**The test:** if it needs the word *because*, it is not a finding.

**Format:**

> **F-07** — `System.evtx` on `FIN-WKS-07`, record 41 992, Event ID 7045,
> `2026-08-25 09:12:55 UTC`: a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

**Banned in this section:**

> *clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
> unauthorised*

Every one of them is an interpretation wearing a finding's clothes.

**Also banned here:** naming a person as the actor. Artifacts record accounts, processes and
devices. They do not record people.

---

## 9 · Interpretation

**What it means.** Numbered `I-01`, `I-02`, …

Each interpretation must do three things:

1. **cite the finding numbers it rests on**
2. **state a confidence** — high, moderate, low
3. **name at least one alternative explanation**, and say why it was rejected or could not be
   excluded

**Format:**

> **I-03** — The service in **F-07** is assessed, with high confidence, to be attacker persistence:
> its name imitates a Microsoft component, its binary sits in a user-writable temp directory, and it
> was installed 41 seconds after the document execution in **F-05**. Considered and not excluded: a
> legitimate third-party installer using a misleading name — no corresponding installer entry was
> found in `Application.evtx`, but the log covers only 6 days (**F-02**).

**No absolute terms.** Not *"we are sure"*, not *"we are certain"*. The analysis is your
interpretation, not absolute truth, and writing it as truth is what gets a report taken apart.

---

## 10 · Limitations and what could not be determined

Everything not examined, and **why** — especially the technical reasons.

Cover:

- data that did not exist, or could not be recovered
- artifacts whose absence is explained by **policy or retention** rather than by the event not
  happening
- anything outside the authorisation in §3
- systems that were part of the incident but **not examined**, and on whose instruction
- at least one honest **"this evidence cannot show X"**

> Most reports have no section like this. **This one does, and it is graded.** A report that states
> no limitation reads as a report that did not look for one.

---

## 11 · Conclusions

Answers to the questions in §3, and nothing else.

**No new facts appear here.** If it is not in §8, it does not belong in §11.

> **You are not the judge.** Never write *"in my opinion Mr X committed this crime."* Present method
> and evidence. The decision is not yours.

---

## 12 · Appendices

Bulky supporting material, referenced from the sections above and never inline:

- full tool output
- hash lists and manifests
- log extracts and the super-timeline
- glossary of acronyms and technical terms used
- references, checked and current

---

## Write it as you go

Reporting is not a stage that begins when analysis ends. **The report starts when the investigation
starts and is updated as it progresses.** Reconstructing your own work into a report afterwards is
how mistakes get in — and in this course you hand in the same growing document every session, not a
new one.

---

## Before you submit

| ☐ | |
|:-:|---|
| ☐ | Every finding survives the *because* test |
| ☐ | No banned word appears in §8 |
| ☐ | No person is named as an actor in §8 |
| ☐ | Every interpretation cites a finding by number |
| ☐ | Every interpretation states a confidence and names an alternative |
| ☐ | §10 exists and is not empty |
| ☐ | Every tool in §6 carries a version |
| ☐ | Both MD5 and SHA-256 are recorded for every exhibit |
| ☐ | §4 has no undeclared gap |
| ☐ | §7 identifies every source by serial, not drive letter |
| ☐ | §2 was written **after** §11 |
| ☐ | One date format throughout; one term per concept throughout |
| ☐ | No sentence assigns guilt |
