# Session 1 — Homework

**Forensic Foundations, Evidence Integrity & Chain of Custody**
**Due: before Session 2 begins.**

Two parts. Part 1 is practical and external. Part 2 is the report, and it is the part that is
graded against the rubric you will see in every session of this diploma.

---

## Part 1 — Digital Forensics Case B4DM755

**TryHackMe · `caseb4dm755` · free · ~120 minutes**
<https://tryhackme.com/room/caseb4dm755>

**Why this room and not another.** It presents evidence preservation, disk imaging and artefact
analysis as **work that has to survive a courtroom**. That framing is exactly what `S1-07`
teaches, and it is rare — most rooms treat evidence handling as a step to get past on the way to
the answer. It also rehearses the whole `acquire → verify → analyse → document` arc once, before
Session 2 does it properly with real tools.

⚠️ **Known defect, stated so you can work around it.** The room has 24,209 completions and **no
recommend count is displayed**, so there is no community signal on its quality. **Treat its tool
advice as unverified until you have read it.** If it recommends a hash algorithm, check that
recommendation against what you learned today before you accept it.

### What to hand in for Part 1

Not the room's answers. **One page**, containing:

| # | |
|--:|---|
| 1 | Three **findings** from the room, in the `F-01` format, each naming its artifact and exact path |
| 2 | One **interpretation** drawn from at least two of them, with a confidence and one alternative you could not exclude |
| 3 | One **limitation** — something the room's evidence cannot show |
| 4 | One paragraph: **did the room's integrity advice match this session's standard?** If not, say precisely where it differs |

Item 4 is not a trick. It may match. Either answer is acceptable; only an unexamined answer is not.

---

## Part 2 — The forensic report

**This is the deliverable the whole diploma is built to produce.** You will hand in a version of
this document every session, growing, against a rubric that never changes.

### Scope

Write sections **4, 5, 6, 7 and 9** of the report template for **Case 01**, the manifest
verification you carried out in class.

| § | Section | What it must contain |
|--:|---|---|
| **4** | Evidence and integrity | one row per file: exhibit ID, description, who supplied it and when (UTC), hash algorithm and value at receipt, hash re-verified at analysis, custody reference |
| **5** | Examination environment and method | the working copy used, the platform, **every tool with its version**, the order of your steps, and the time basis you worked in |
| **6** | Findings | numbered `F-01`, `F-02`, … Each one observable fact, past tense, one named artifact, exact path, UTC timestamp |
| **7** | Interpretation | numbered `I-01`, … Each citing the findings it rests on, with a confidence, and one alternative considered |
| **9** | Limitations and what was not done | everything not examined and **why**; anything the evidence cannot show |

Plus **one signed chain-of-custody line**.

### Length

There is no minimum. A precise page beats a padded five. If a sentence does not carry a fact, a
citation or a stated limit, remove it.

### The rubric — all four criteria, every session, unchanged

| # | Criterion | Full marks |
|--:|---|---|
| 1 | **Integrity** | hashes recorded before and after · verified against the manifest · custody complete: who · what · when · from where · hash · where stored |
| 2 | **Method** | another analyst could reproduce your result from §5 alone · every tool named with its version · steps in the order performed |
| 3 | **Findings** | fact only · every finding tied to one named artifact at an exact path · nothing asserted that the evidence does not show |
| 4 | **Separation** | interpretation kept visibly distinct from findings · limitations stated · **at least one honest "this evidence cannot show X"** |

**Criterion 4 is the one this course is about.** It is also the one most reports lose marks on,
every session, for the same three reasons:

| The loss | What it looks like |
|---|---|
| **Motive in a finding** | *"altered to hide"*, *"deliberately"*, *"to avoid detection"* |
| **A person in a finding** | *"the user copied"* when the artifact records an account, not a human |
| **No limitation at all** | a report that states no limit reads as one that did not look for any |

### Before you submit — check yourself

| ☐ | |
|:-:|---|
| ☐ | Every finding survives the *because* test — if it needs the word, it is not a finding |
| ☐ | No banned word appears in §6: *clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious · unauthorised* |
| ☐ | Every interpretation cites a finding **by number** |
| ☐ | Every interpretation names an alternative and says why it was rejected or could not be excluded |
| ☐ | §9 exists and is not empty |
| ☐ | One date format throughout. One term per concept throughout |
| ☐ | Every tool in §5 carries a version |
| ☐ | No sentence assigns guilt |
| ☐ | The custody line is signed and records the mismatch |

---

## Optional — 40 minutes, if you want the *why*

**TryHackMe · IR Philosophy and Ethics · `irphilosophyethics`** · free
<https://tryhackme.com/room/irphilosophyethics>

Proportionality, the analyst's obligations, and the boundary between investigating and
interfering. It is philosophy rather than procedure — there is no artifact in it — but it is the
right thing to read if today's material left you asking *why do we do it this way?*

⚠️ Its framing is incident-response shaped and sometimes assumes a live network, which is not what
this course is teaching. Take the reasoning, not the operational assumptions.

---

## Peer review

Bring your report to Session 2. You will swap with one other person and mark **their** §6 and §7
for one thing only: **where has a finding drifted into an interpretation?**

That is the only shared work in this course, and it exists because the drift is far easier to see
in someone else's writing than in your own.

---

## Before Session 2

| ☐ | |
|:-:|---|
| ☐ | `EVS-02` downloaded and **its hash verified** — a mismatch is a finding, bring it |
| ☐ | `FOR-WS01` reverts cleanly to `CLEAN-TOOLS` |
| ☐ | Report printed or on a USB stick, ready to hand to a partner |
