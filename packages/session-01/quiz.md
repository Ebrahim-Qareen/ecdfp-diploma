# Session 1 — Quiz

**Forensic Foundations, Evidence Integrity & Chain of Custody**
**10 questions · all multiple choice · no score kept**

**Instructor-facing — this file contains the answer key.** Only the question text is published to
the session page.

| Objective | Questions |
|---|---|
| **O1** sequence a collection by order of volatility | 5 |
| **O2** verify against a manifest; report a mismatch as a finding | 1 · 6 · 10 |
| **O3** separate findings from interpretation | 2 · 3 · 4 · 9 |
| **O4** complete a chain-of-custody record; identify the gap | 8 |
| **O5** state the proof trail for a write blocker | 7 |

⚠️ **All ten are multiple choice** (`D52`), which supersedes `design_system.md` §4.2's
mixed-format rule. The cost is real and worth naming: MCQ tests **recognition**, free recall tests
**production**, and writing a clean finding is a producing skill. It is covered instead by
`student_activity.md` Activity 1 and by the report itself, which is where it is graded.

Four questions sit on `S1-04`, which is where the weight belongs.

---

## Q1 · MCQ · O2

You image a suspect drive. The source hash taken before imaging and the image hash taken
afterwards are identical.

**Which of the following has been established?**

- **A** — The image is a faithful copy of the data that was read from the source.
- **B** — The drive in your hand is the drive described on the chain-of-custody form.
- **C** — The entire physical medium was captured.
- **D** — The data on the source was unaltered before you arrived.

---

## Q2 · MCQ · O3

> *"`EVI-SRC01_acquisition_log.txt` computes to SHA-256 `a91f…`, which does not match the value
> `4c02…` recorded for that filename in `EVS-01.sha256`."*

**Finding, interpretation, or limitation?**

- **A** — Finding
- **B** — Interpretation
- **C** — Limitation
- **D** — None of these: it is a conclusion

---

## Q3 · MCQ · O3

> *"The acquisition log was altered after the manifest was produced, most likely to conceal the
> true acquisition time."*

**Finding, interpretation, or neither?**

- **A** — Finding
- **B** — A sound interpretation
- **C** — An interpretation that fails the standard, because it asserts motive
- **D** — Limitation

---

## Q4 · MCQ · O3

> *"The user obviously plugged in the USB drive at 14:22 and copied the finance data to it."*

**Which rewrite is acceptable as a finding?**

- **A** — *"The user plugged in the USB drive at 14:22 and copied the finance data to it."*
- **B** — *"`setupapi.dev.log` on `EVI-SRC01`, line 4 119, records the first installation of a USB mass-storage device with serial `<serial>` at `2026-03-03 14:22:07 UTC`."*
- **C** — *"A USB device was connected at 14:22, suggesting the user was preparing to exfiltrate data."*
- **D** — *"At 14:22 the finance user's account was used to copy data to removable media, indicating intent."*

---

## Q5 · MCQ · O1

You arrive at a running workstation. A process you do not recognise is writing continuously to
disk, and the file names suggest a wiper is running.

**What do you do first?**

- **A** — Capture RAM, because RAM is the most volatile store.
- **B** — Pull the power, accepting the loss of RAM.
- **C** — Run a live-response collector, then decide.
- **D** — Image the disk while the machine is running.

---

## Q6 · MCQ · O2

A widely-used and well-rated 2025 training room states:

> *"Hashing: Using cryptographic hash functions such as MD5 and SHA-1 to create unique data
> fingerprints and verify that it has not been altered."*

**What exactly is wrong with it?**

- **A** — Nothing. MD5 and SHA-1 still produce unique fingerprints.
- **B** — Both are broken for **collision** resistance, which is the property *"has not been altered"* depends on — and SHA-256 is not mentioned at all.
- **C** — MD5 and SHA-1 are too slow for large evidence files.
- **D** — Hash functions should never be used to check integrity; only digital signatures should.

---

## Q7 · MCQ · O5

You imaged a drive through a hardware write blocker. A defence examiner asks you to prove the
blocker was in the path.

**Which single item is the strongest technical evidence available to you?**

- **A** — The image file, which shows no modification.
- **B** — The source hash taken before the imaging run and again after it, both matching.
- **C** — The imager's verification log reading `verified`.
- **D** — The `StorageDevicePolicies\WriteProtect` value set to `1` on your workstation.

---

## Q8 · MCQ · O4

A chain-of-custody record shows this sequence for one exhibit:

| # | When (UTC) | From | To | Hash recorded |
|--:|---|---|---|---|
| 1 | 09:14 | first responder | evidence store | yes |
| 2 | 11:02 | evidence store | examiner A | yes |
| 3 | *(no entry)* | — | — | — |
| 4 | 16:47 | examiner B | evidence store | yes |

**What can the other side argue as a result?**

- **A** — Nothing. Every row present is complete and carries a hash.
- **B** — That the recorded hash values must be wrong.
- **C** — That for 5 h 45 m the exhibit's handling is unaccounted for, so substitution or alteration cannot be excluded.
- **D** — That examiner A should be called as a witness.

---

## Q9 · MCQ · O3

You hold a manifest and four files. One file's digest does not match the manifest.

**Which question can this evidence, on its own, not answer?**

- **A** — Which file's content differs from the content recorded in the manifest.
- **B** — Whether the other three files match their recorded values.
- **C** — Whether the file was altered before or after it was handed to you.
- **D** — What algorithm was used to produce the recorded values.

---

## Q10 · MCQ · O2

**MD5 is right for one question and wrong for another. Which pairing is correct?**

- **A** — Right for *"is this file unaltered?"*; wrong for *"have we seen this file before?"*
- **B** — Right for *"have we seen this file before?"*; wrong for *"is this file unaltered?"*
- **C** — Wrong for both — MD5 has no remaining forensic use.
- **D** — Right for both, provided the file is under 4 GB.

---

# Answer key

**Instructor copy only - not in this repository.**

The ten answers with their justifications live in `quiz_answer_key.md`
in this folder on the instructor machine. It is gitignored, because this
repository is public (D22) and a published answer key is not an answer key.
