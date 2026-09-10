# P03 · Homework — identity, and what metadata is worth

Due before `P04`. Graded on the `D20` rubric; **criterion 3 (Findings)** weighted heaviest this
week, because this is the first page that produces real findings. Individual.

---

## Task 1 — finish Case 01 · ~35 min

Complete any `CASE-01B` steps you did not reach in class, and write **Section 8** of your report
with one entry per issue.

Minimum: five entries covering the two files that fail both manifests, the file that passes one and
fails the other, the missing file, the extra file, the misnamed file, and the duplicate pair.

**What loses marks:** any entry that names a cause. You hold no clean copy.

---

## Task 2 — a signature sweep of your own machine · ~20 min

Pick a folder of your own with at least thirty files. Sweep it:

```bash
file * | grep -v -i -E 'directory|empty'
```

**Deliverable:** how many files carry a signature that disagrees with their extension, and for
**one** of them, an explanation of why the disagreement is completely innocent.

> Almost every machine has some. Office temporary files, browser cache entries, downloads saved
> with the wrong suffix. **The point is calibration:** a mismatch is common, and treating every
> mismatch as suspicious is how an examiner produces a report nobody trusts.

---

## Task 3 — read your own photographs · ~15 min

Run `exiftool` on three photographs from your own phone or camera. Report, for each:

1. Is there a GPS block?
2. Do `DateTimeOriginal` and `ModifyDate` agree?
3. What does the `Software` field say, if anything?

Then one paragraph: **what would you be able to establish about your own movements** from these
three files alone, and what would you not?

> This one is not busywork. Understanding what your own photographs disclose is how you calibrate
> what a suspect's disclose &mdash; and how you avoid overstating it.

---

## Task 4 — the sentence, again · ~10 min

You are asked in a hearing:

> *&ldquo;The photograph's metadata places the defendant's camera at that address on the 24th. That's
> conclusive, isn't it?&rdquo;*

Write the answer. One paragraph. It must be accurate **and** useful &mdash; &ldquo;metadata can be edited&rdquo; on
its own is accurate and useless, because it leaves the questioner with nothing.

**What good looks like:** it says what the file records, says what would have to be true for that
record to reflect reality, names what could corroborate it, and does not pretend the evidence is
worthless.

---

## Rubric reminder (`D20`)

| # | Criterion | On this homework |
|---:|---|---|
| 1 | **Integrity** | Section 6 records what you ran, on what, with which version. |
| 2 | **Method** | Can another examiner repeat your sweep and reach your numbers? |
| 3 | **Findings** | Each tied to a named artifact at an exact path. **Heaviest this week.** |
| 4 | **Separation** | Task 4 is criterion 4 in a single paragraph. |
