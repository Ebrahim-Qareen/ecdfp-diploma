# P02 outline — Evidence integrity

**OUTLINE GATE (`D9`). Approved before any document or HTML exists.**
Page `P02` · **38 topic minutes** · topic `T03` · evidence **`EVS-01`** (Tier 1, verified, ours).
Design frozen by `D109` — this page inherits `P01`'s look and decides nothing new.

Sources: `knowledge_base/Module_01_Data_Acquisition.md` §1 (hashing · CoC · write blocking) and §2
(acquisition hash set · FTK Imager log · CoC form · write blocker proof trail ·
`StorageDevicePolicies\WriteProtect`) · `knowledge_base/instructor/Session_01` ·
`knowledge_base/thm/forensic-imaging.md` · `knowledge_base/thm/intro-to-cold-system-forensics.md`.

---

## The one sentence this page exists to install

**A matching hash proves the copy equals the source as read at that moment — and nothing else.**
Everything on the page is a consequence of that sentence: what a match does not cover, what a
mismatch does not mean, and why the two things that *do* carry authenticity — the chain of custody
and the write-block proof trail — live entirely **outside** the image file.

This is `D7`'s core lesson (finding vs interpretation) applied to the one artifact students already
believe they understand. Most arrive certain a hash "proves the evidence wasn't tampered with".
INE's own slides say exactly that at `[U2 p143]` and correct it at `[U2 p144]`. **We teach the
correction, and we show them the slide that got it wrong** — that is the moment the lesson lands.

---

## `T03` — Evidence Integrity · 38 min

Map parts: hashing (18) · chain of custody (12) · write blocking (8).

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory** | 13 | Bridge from `T01`: *you signed that your platform was in a known state. Now you have to prove the evidence is too.* Then: what a hash is and the one thing it proves (5) · the four things it does **not** (5) · CoC and the write-block trail as the two records that carry what the hash cannot (3). |
| **Guided practice** | 12 | `SIMSCREEN T03-1` — verify `EVS-01` on `FOR-WS01`: `Get-FileHash` and `sha256sum -c`, both MD5 and SHA-256, **and the set contains one deliberately failing file**. The key step is not the command; it is the line `EVI-SRC01_acquisition_log.txt: FAILED` and the question *what does this actually tell me?* |
| **Independent** | 9 | **Two judgement exercises, no lecture.** (a) 4 min — five one-line scenarios, each with a hash result, sorted into *integrity intact · integrity broken · cannot tell from this*. (b) 5 min — **the THM defect hunt**: the student is shown Task 4 (verify the MD5, it matches) and Task 5 (`sudo mount -o loop …`) of the Forensic Imaging room and asked what just happened to the hash they verified. |
| **Report stage** | 4 | Fill **Section 4 Chain of custody** and **Section 5 Evidence received** for `EVI-SRC01` from the `EVS-01` forms — the first two sections graded by rubric criterion 1. Record **both** MD5 and SHA-256 (`[U2 p145]`: never one). |

**Theory 13 / 38 = 34 %** — inside `D79`'s 35 % ceiling.

**How the budget works.** The four not-proves are the substance of the topic, and every one of them
is a *judgement*, so they are taught by making the student judge (independent part (a)) rather than
by listing them. The write-blocking 8 minutes are not a separate block: a write blocker exists to
make two source hashes match across an imaging run, so it is taught as **the thing that makes the
before-hash and the after-hash comparable** — inside the hashing story, where it belongs.

---

## Screens (~15, `D101` — one idea each)

| # | Screen | Carries |
|---:|---|---|
| 1 | Cover | `T03` · 38 min · what you will be able to sign at the end |
| 2 | Bridge from `T01` | the platform was known; the evidence is not yet |
| 3 | What a hash is | one-way, fixed length, avalanche — the live one-letter demo (`[U2 p146–150]`) |
| 4 | The one thing a match proves | `FIG P02-F1` row 1 — *these two byte streams are identical* |
| 5 | Not proof 1 — **completeness** | an HPA excluded from both reads matches perfectly |
| 6 | Not proof 2 — **a mismatch is not tampering** | failing sector · cable fault · SSD garbage collection |
| 7 | Not proof 3 — **authenticity and provenance** | the hash says nothing about which drive this is |
| 8 | Not proof 4 — **the attacker who holds both** | disk + hash = recompute. INE `[U2 p143]` vs `[U2 p144]`, shown side by side |
| 9 | So where does authenticity live? | it is not in the file — it is in two records |
| 10 | Chain of custody | INE's six fields · signed tape across the seal · the two-signature rule |
| 11 | The write blocker | hardware vs software; INE is blunt that software is a fallback, not an equal |
| 12 | `FIG P02-F2` | **the image is byte-identical either way** — so the proof trail is four places outside it |
| 13 | `SIMSCREEN T03-1` | verify `EVS-01`, meet the `FAILED` line |
| 14 | Independent (a) + (b) | the five-scenario sort, then the THM defect hunt |
| 15 | Knowledge check | one MCQ + one reveal question |
| 16 | Report stage | Section 4 and Section 5, both digests |
| 17 | Summary + cheat sheet + homework | what you can now sign |

---

## Figures

| ID | Pattern (`D94`) | What it shows — and why a table would not do |
|---|---|---|
| `P02-F1` | **parallel rows + spotlight**, 4 rows | *match · match-but-incomplete · mismatch-without-misconduct · match-that-proves-nothing*. Each row is the **same** green "hashes match" result with a different truth underneath it. The point is that the result line is identical in all four — which a table of four bullet points cannot say, because a table implies four different-looking cases. |
| `P02-F2` | **accumulation**, 4 steps | The four places the write-block proof lives — blocker display/log · photograph of the rig with serials legible · the CoC line naming make/model/serial · contemporaneous notes — accumulating **around an image file that never changes**. The image is the constant; the evidence of care is everything stacked beside it. |
| `SIMSCREEN T03-1` | **11 steps** | `Get-FileHash` → `sha256sum -c` → the `FAILED` line → open the file → find the one changed byte → re-hash → record both digests. **Key step: the `FAILED` line** — the whole component exists for the beat where the student wants to say *tampering* and has to say *I cannot tell yet*. |

No second SIMSCREEN. The `WriteProtect` registry procedure is four clicks and the decision is not on
the screen — `D96` rule 4. It ships as a static `.wu` regedit screen on screen 11 with the failure
mode called out: **set it, forget the reboot, plug in evidence, Windows writes.**

---

## `EVS-01` — why this set, and the one thing to be careful about

`EVS-01` already ships a **deliberately failing checksum** (`EVI-SRC01_acquisition_log.txt: FAILED`,
three others OK). That is the single most valuable thing on the page and it is already built and
verified — no acquisition needed, which is why `P02` is buildable while `P04`–`P14` are not.

**Careful:** the failure is *seeded by us*, so the honest lab answer is **"the file differs from the
manifest — I cannot tell why from the hash alone"**, not "someone tampered with it". The guided lab
must end by opening the file and finding the change, because *that* is the step a hash cannot do.

---

## Open questions for approval

1. **The INE side-by-side on screen 8** — we show a course we sell content from getting a slide
   wrong, then getting it right one slide later. It is the strongest teaching moment on the page.
   Ship it, or teach the correction without naming INE?
2. **The THM defect hunt** — same question, on a free public room with 18,481 completions.
   Recommended: ship both. A student who never sees a respected source be wrong learns to trust
   sources instead of evidence, which is the opposite of this course.
