# Session 1 — Student Activity

**Forensic Foundations, Evidence Integrity & Chain of Custody**

Two activities. The first is short and written. The second is the session's investigation.

You work **alone at the keyboard**. Pairing happens once, at the end, and only for reading each
other's report.

---

## Activity 1 — Clean up three contaminated findings

**Time box: 8 minutes.**

Each sentence below is offered as a *finding*. None of them is one. Rewrite each as up to three
separate entries: a **finding**, an **interpretation**, and — where the sentence claims something
no evidence could reach — a **limitation**.

Use the two line formats from the report template. Number them `F-01`, `I-01`, and so on.

### 1

> *"The acquisition log was clearly modified by the attacker to hide the real acquisition time."*

### 2

> *"The USB device was plugged in by the finance user at 14:22, proving they carried out the
> exfiltration."*

### 3

> *"No malware was found on the system, so the host is clean."*

### Success criteria

| ☐ | |
|:-:|---|
| ☐ | No finding contains a verb of inference — no *suggests*, *indicates*, *was likely*, *proves* |
| ☐ | No finding names a person as the actor |
| ☐ | Every interpretation cites at least one finding by number |
| ☐ | Every interpretation names one alternative explanation |
| ☐ | Sentence 3 produces a **limitation**, not just a finding and an interpretation |
| ☐ | None of the banned words appears in any finding |

> **Sentence 3 is the one most people get wrong.** *"No malware was found"* and *"the host is
> clean"* are not the same claim, and the gap between them is a limitation.

---

## Activity 2 — Case 01: the tampered file

**Time box: 60 minutes.** Suggested split: 10 verify · 20 examine · 25 write · 5 custody.

### Brief

A finance-department workstation at a fictional company has been seized following a suspected
intrusion. The host has been powered down. **Nothing has been analysed yet.**

You have been handed the seizure package — four documents and a signed manifest — by the first
responder. Your job today is not to investigate the intrusion. Your job is to establish **whether
what you were handed is what you were told you were handed**, and to document that to a standard
that survives challenge.

### Scope and authorisation

You are authorised to examine the four documents in `EVS-01` and their manifests, and nothing
else. You are not authorised to access the workstation, its image, or any network resource.
Anything outside that scope is out of scope, and saying so is part of the deliverable.

### Evidence

✅ **`EVS-01`, verified 2026-08-30.** Four documents and two manifests, 6 144 B in total.
**Verify before you start.** One file will not match — that is the exercise.

| # | File | Bytes | MD5 recorded in the manifest |
|--:|---|--:|---|
| 1 | `seizure_notes.txt` | 2 303 | `5127e6d1609da0e140d9483d2198852e` |
| 2 | `EVI-SRC01_acquisition_log.txt` | 1 340 | `c9dfb4b8c20095c9f739359b43812515` |
| 3 | `custody_form_EVI-SRC01.txt` | 1 914 | `a3f69f666078c94d84351ee656e42001` |
| 4 | `evidence_inventory.csv` | 587 | `11a85407fa5b9cdd2950b1ae71e55838` |

Full SHA-256 values are in `EVS-01.sha256`. **That is the file you check against** — MD5 is shown
here only because it fits on a page.

### Environment

`FOR-WS01`, started from the `CLEAN-TOOLS` snapshot you took in Lab A.

### The questions

Answer all six. **Each answer must name the artifact it rests on and give its exact path.**

| # | Question |
|--:|---|
| **1** | Verify all four files against the signed manifest. State the command you used, its version, and the result for each file. |
| **2** | One file does not verify. Name it, and write the mismatch as a **finding** — with both the computed and the recorded digest. |
| **3** | At what date, time and **time zone** was the host seized? Name the artifact and the exact line you are reading. |
| **4** | `evidence_inventory.csv` lists three exhibits. Which one does `EVI-SRC01_acquisition_log.txt` describe, and how do you know it is that one and not another? |
| **5** | The acquisition log contains the word `verified`. **State precisely what was verified against what.** Then state what that word does **not** cover. |
| **6** | Was the file that failed verification altered **before** or **after** it was handed to you? |

> **Question 5 is the one this case exists for.** Read the log line by line and mark which lines
> describe the *source drive* and which describe the *image file*. The answer to "what was
> verified" follows from that, and it is narrower than the word suggests.

> **Question 6 has a correct answer, and it is not a date.** If you find yourself reasoning
> towards a guess, that feeling is the answer.

### Deliverable

Sections **4, 5, 6, 7 and 9** of the report template:

| § | Section |
|--:|---|
| 4 | Evidence and integrity |
| 5 | Examination environment and method |
| 6 | Findings — numbered `F-01`, `F-02`, … |
| 7 | Interpretation — numbered `I-01`, `I-02`, … |
| 9 | Limitations and what was not done |

Plus **one signed chain-of-custody line**.

### Success criteria

Graded on the same four criteria as every session in this diploma.

| # | Criterion | What earns the mark here |
|--:|---|---|
| 1 | **Integrity** | all four files hashed · checked against the manifest · both algorithms recorded · the mismatch written onto the custody form, not only into your notes |
| 2 | **Method** | another analyst could repeat your check from your §5 alone · every command carries its tool version · steps in the order you performed them |
| 3 | **Findings** | every finding is one fact · tied to one named artifact at an exact path · no verb of inference · no person named as an actor |
| 4 | **Separation** | interpretations in their own section, each citing finding numbers, each with a confidence and one alternative considered · **at least one limitation stated** · question 6 answered honestly |

### Two things that will cost you marks

**Motive in a finding.** *"altered to hide"*, *"deliberately"*, *"to avoid detection"* — none of
these is observable in a digest.

**A missing limitation.** A report that states no limitation reads as a report that did not look
for one. This case has at least three.

### If you finish early

Do not start question 7 — there isn't one. Instead:

- Re-read your own findings and mark every word that is doing interpretive work.
- Swap reports with the person next to you and mark **theirs**. Drift from finding to
  interpretation is far easier to see in someone else's writing than in your own — which is the
  only reason pairing exists in this course.
