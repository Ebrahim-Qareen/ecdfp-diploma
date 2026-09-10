# P02 · Report stage — Sections 4 and 5

Topic `T03` · **4 minutes** · your report for case `ITG-2026-014` is already open from `P01`.

You filled **Section 1 Case identification** and **Section 3 Authorisation & scope** on the last
page. Now you fill the two sections that **rubric criterion 1 (Integrity)** grades.

---

## Section 4 — Chain of custody

Transcribe from `custody_form_EVI-SRC01.txt`. Your report's Section 4 is a **summary with a
pointer**, not a copy of the form — the form itself is an exhibit.

Include:

| Field | From |
|---|---|
| Exhibit reference | `ITG-2026-014-A1` |
| What it is | internal 3.5in SATA disk removed from `EVI-SRC01` |
| Number of transfers, and whether any is unaccounted for | the transfer table |
| Where it is stored, and whether access is logged | the storage line |
| Seal state at each transfer | the declaration |
| Where the source hash was recorded | **the notebook, separately from both the exhibit and the image** |

**One line you must include, in these words or your own:**

> The chain of custody for this exhibit contains no unaccounted transfer, and the seal was recorded
> as intact at each one.

If that sentence is not true of your exhibit, say what is true instead. A gap that is stated is a
limitation. A gap that is hidden is the end of the exhibit.

---

## Section 5 — Evidence received

One row per item, and for `P02` you have five: the four `EVS-01` documents and the exhibit they
describe.

| Column | Rule |
|---|---|
| Item | the file or exhibit name, exactly |
| Size | bytes, from the file system |
| **MD5** | **required** |
| **SHA-256** | **required** |
| Received from | a named person or a named process |
| Received when | date and time, **UTC** |
| Verified? | `OK`, or the result you actually got |

### The two rules that are not negotiable

**1 · Both digests. Always.** MD5 and SHA-1 are broken for collision resistance (`[U2 p145]`).
Recording both means a challenge to one function does not take the exhibit with it. One digest is a
single point of failure you chose.

**2 · The hash lives somewhere the exhibit does not.** (`[U2 p144]`) A hash file sitting next to
the image protects nothing: anyone who can change one can change the other. `EVS-01`'s custody form
models the right habit — *"recorded in the examiner's notebook, page 41, stored separately from the
exhibit and separately from the image."*

---

## The row that will be graded hardest

The row for `EVI-SRC01_acquisition_log.txt`, because it did not verify.

Write the `Verified?` cell as what happened, not as a conclusion:

> `FAILED` — computed SHA-256 does not match the manifest value. Difference located by inspection:
> one timestamp field, `09:14:02` vs `09:14:03`. Cause not established. Referred to the set owner.

**Read that back.** It states a measurement, states what inspection added, and stops at the edge of
what is known. It does not say *tampered*, *altered by*, or *someone*.

That sentence is the whole of `P02` in one line. If you can write it, the page has done its job.

---

## Still empty on purpose

**Section 2 Executive summary**, **Section 9 Interpretation** and **Section 11 Conclusions** stay
empty (`D85`). You are two pages into a fourteen-page course. A summary written now would be a
conclusion you then go looking for evidence to support.
