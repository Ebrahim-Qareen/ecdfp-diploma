# Session 2 — Homework

**Acquisition: Disk, Memory & Live Response**
Two parts. Part 1 is practical. Part 2 is the forensic report, and it is graded on the same four
criteria as every other session.

---

## Part 1 — TryHackMe: Forensic Imaging

**Room:** `forensicimaging` · free · ~45 min.

It covers imaging concepts and the vocabulary of image formats. It is short, clean and correct enough
to be worth your time.

⚠️ **Its defect, so you are not caught by it.** The room does **not** cover write blocking as a
**separate control**. It treats imaging as the whole of acquisition. In practice the distinction
matters more than the room implies — and note that **NIST CFTT has never tested a Linux software write
blocker**, so "I used a software blocker on Linux" is a claim you cannot support the way you can
support a tested hardware one.

Work through the room, then answer these three questions in your own words:

| # | Question |
|--:|---|
| 1 | The room images a device. At which point in its process should a write blocker have been recorded, and why does the order matter? |
| 2 | The room uses a single image format. Name one thing that format gives you and one thing it does not. |
| 3 | Give one sentence the room states that you would **not** write in a report, and say why. |

### What to hand in for Part 1

- Your three answers, one short paragraph each.
- A screenshot of the room completed is not required. The answers are the deliverable.

---

## Part 2 — The forensic report

Write a report on **Case 02a** — the acquisition and verification of the suspect USB device.

Use `report_template.md`. It has not changed since Session 1 and it will not change for the rest of
the course.

### Scope

Cover only what you did in `S2-08`:

- the acquisition decision you made, and why
- the write blocker, and when it was recorded
- the image you produced, its format, and both digests
- the verification result, stated precisely
- what your evidence cannot show

### Length

Two to three pages. A longer report is not a better one. Criterion 3 rewards findings tied to named
artifacts, not volume.

### The rubric — all four criteria, every session, unchanged

| # | Criterion | What earns the mark |
|---|---|---|
| 1 | **Integrity** | hashes before and after · verified against the published manifest · custody complete |
| 2 | **Method** | reproducible by another analyst · every tool named **with its version** · steps in order |
| 3 | **Findings** | fact only · each tied to one named artifact at an exact path |
| 4 | **Separation** | interpretation visibly distinct · limitations stated · at least one honest *"this evidence cannot show X"* |

### Before you submit — check yourself

| ☐ | |
|:-:|---|
| ☐ | Every tool named with its version — FTK Imager **8.3**, not "FTK Imager" |
| ☐ | Both digests given for every artifact |
| ☐ | No finding contains the words *stole*, *deliberately*, *tried to*, or *guilty* |
| ☐ | At least one limitation, written honestly |
| ☐ | The sentence *"the image is verified, so the device was untampered"* appears **nowhere** |
| ☐ | Every claim about a person is in the Interpretation section, not the Findings section |
| ☐ | The report reads the same if someone else runs your steps |

---

## Optional background — 30 minutes, if the subject is new to you

**TryHackMe:** `memoryanalysisintroduction` · free.

It gives vocabulary to someone who has never met memory forensics.

⚠️ **It is optional and it is not assigned, because it has two defects you would have to unlearn.**
It cites a **retired ATT&CK ID beside the live one for the same behaviour, in the same task**. And it
lists **RAMMap** as a capture tool — Microsoft describes RAMMap as a physical memory *usage analysis*
utility, and **it writes no dump at all**. If you read the room, read it knowing both.

**KAPE** was shown in class as an example only. The TryHackMe `kape` room is good on targets and
modules, but it does **not** mention the licence position: KAPE is no longer available for commercial
use as of 1 January 2026. Classroom use is educational; your future paid engagements are not. Use the
free alternatives shown in `S2-07` for real work.

---

## Peer review

Pairs, once, on the report only (`D16`). Read your partner's report and mark every place where a
**finding** has drifted into an **interpretation**. Hand back one marked copy.

You are not marking whether they are right. You are marking whether the sentence belongs where it is.

---

## Before Session 3

| ☐ | |
|:-:|---|
| ☐ | Session 3's evidence downloaded **and its hashes verified** (`D18`) |
| ☐ | `FOR-WS01` back on a clean snapshot |
| ☐ | Your custody line from this session closed on the record page |
| ☐ | Part 2 report submitted |

Session 3 opens the images you made today: *"You have the evidence now. What is actually inside it?"*
