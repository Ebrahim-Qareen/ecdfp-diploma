# P03 · Build log — Data at byte level

Built 2026-09-09. Topics `T04` (82 min) + `T05` (35 min) = **117 min**.
Evidence `EVS-05` · `EVS-01` · `EVS-10` · case `CASE-01B`.

---

## The thing that had to happen first

**`EVS-05` and `EVS-10` had never been generated.** Only `scripts/make_evs05.py` and
`make_evs10.py` existed; no bytes did. `make_evs10.py` also needs `piexif`, which was not installed.

Both were generated and **read** before a word of this page was written, because `D94` requires a
finding to be real. Everything quoted on the page is a measurement:

**`EVS-05` — 5 of 12 files carry a signature that disagrees with their extension:**

| Name | First bytes | Actually |
|---|---|---|
| `thumbnail.png` | `FF D8 FF E0` | JPEG |
| `holiday_snap.jpg` | `50 4B 03 04` | ZIP |
| `invoice_scan.jpg` | `25 50 44 46` | PDF |
| `meeting_notes.txt` | `89 50 4E 47` | PNG |
| `policy_v2.docx` | `89 50 4E 47` | PNG &mdash; wrong **twice**, since a `.docx` should be a ZIP |

**`EVS-10` — three images, three metadata states:**

- `office_floor3.jpg` &mdash; GPS `30&deg;2&prime;27.60&Prime;N 31&deg;14&prime;13.20&Prime;E`,
  `DateTimeOriginal 2026:08:24 09:14:02`, `DateTime 2026:08:31 16:40:05`, `Software MRG ImageTool 2.4`
- `invoice_batch.jpg` &mdash; EXIF present, **no GPS**
- `team_photo.jpg` &mdash; **no EXIF at all**

**`CASE-01B` — every step run against the real package:**

| Step | Result |
|---|---|
| 1 | `incident_timeline.txt` and `access_log_excerpt.txt` fail both manifests. **`policy_extract.txt` passes SHA-256 and fails MD5** |
| 2 | `missing_statement.txt` in the manifest, not in the folder. `extra_notes.txt` in the folder, not in the manifest |
| 3 | `photo_evidence.txt` passes both and begins `89 50 4E 47` &mdash; a PNG |
| 4 | `access_log_excerpt.txt` line 5 carries **trailing whitespace** where no other line does |
| 5 | `duplicate_a.txt` and `duplicate_b.txt` share digest `5826bb9c…9ca9a0` |

---

## The best thing on this page, and it was already in the repo

**`policy_extract.txt` passing one manifest and failing the other.**

A file whose content changed fails **both** algorithms. A split result is therefore *logically
incompatible* with a changed file, and the finding is about a **manifest**, not the file.

That is a genuine piece of reasoning &mdash; not a fact to memorise &mdash; and it sits in a case
file written weeks ago for a different session. It is now the sharpest moment in `T04`, the
hardest-graded homework entry, and quiz Q5.

The second best is `team_photo.jpg` having no EXIF, because students report an empty result as
*"the tool did not work"*. Naming an absence precisely, without inventing a reason for it, is worth
more than either image that does carry GPS.

---

## What was built

| # | File | Lines |
|---:|---|---:|
| 1 | `instructor_guide.md` | 222 |
| 2 | `student_guide.md` | 157 |
| 3 | `guided_lab.md` | 193 |
| 4 | `student_activity.md` | 124 |
| 5 | `quiz.md` | 127 (12 questions, 7 objectives) |
| 6 | `quiz_answer_key.md` | 38 |
| 7 | `homework.md` | 76 |
| 8 | `homework_answer_key.md` | 85 |
| 9 | `report_stage.md` | 83 |
| 10 | `instructor_script_ar.md` | 194 |
| 11 | `build_log.md` | this |

**Budget.** `T04` 20+18+40+4 = 82. `T05` 12+10+9+4 = 35. Theory **32 / 117 = 27 %**, inside
`D79`'s 35 % ceiling.

---

## Two things added that INE does not cover

Both are flagged as gaps in the knowledge base and both are load-bearing later:

1. **Endianness.** INE unit 3 never defines it, and nothing in `P08`'s PE tables can be read without
   it. Taught as **pattern versus value**: a signature is read left to right, a numeric field is not.
2. **What a rename actually changes.** INE asserts the outcome and never explains the mechanism. It
   is taught here because it *is* the mechanism of the whole topic &mdash; the header survives
   because the header is content.

---

## What is still open

- [x] **The HTML page is built.** 22 screens &middot; 9 stepped figures &middot; 2 SIMSCREENs &middot;
      107 Arabic blocks. `density_gate.py` ALL PASS, `render_gate.js` zero findings at five widths,
      all 9 diagrams stepping with a changing caption, and **9/9 SIMSCREEN pointers on target**.
      Two gate findings were fixed rather than argued with: the summary screen carried 280 words
      (split into takeaways + a reference screen, which is better teaching anyway), and the
      `T05` bridge had no figure (`FIG P03-D9`, the three questions, now sits there).
- [ ] `EVS-05` and `EVS-10` are generated **in this container**, not on `FOR-WS01`. The lab needs
      them staged onto the student machines and their manifests re-verified there.
- [ ] `design/evidence_sets.md` should record that both sets are now materialised, with the real
      digests. Currently it describes them as specified, not built.
- [ ] Nobody has taught this page. The 27 % theory figure is a plan.
