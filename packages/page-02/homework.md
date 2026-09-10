# P02 · Homework — the integrity sections

Due before `P03`. Graded against the `D20` rubric, **criterion 1 (Integrity)** weighted heaviest
this week. Individual work.

---

## Task 1 — verify a set and report it honestly · ~25 min

Download `EVS-01` again into a **fresh folder** (do not reuse this evening's).

1. Verify the set with **both** manifests — `EVS-01.md5` and `EVS-01.sha256`.
2. Record the results.
3. For the file that fails, locate the difference by inspection and record what it is.

**Deliverable:** the `Verified?` cells for all four files, written as measurements. The failing
one must state what the hash established, what inspection added, and where your knowledge stops.

> **What loses marks:** any sentence that names a cause the evidence does not carry. *Tampered,
> altered by, someone, must have* — each of these turns a finding into an interpretation sitting
> in the wrong section.

---

## Task 2 — the report · ~30 min

Fill **Section 4 Chain of custody** and **Section 5 Evidence received** in your case report.

Requirements:

- Every item carries **both** MD5 and SHA-256.
- Section 4 states whether any transfer is unaccounted for, and whether the seal held.
- Section 4 records **where the source hash was stored**, and why that location matters.
- One explicit sentence about what your verification **does not** establish.

---

## Task 3 — one paragraph, written for a lawyer · ~15 min

You are asked in a hearing:

> *"The image matches the hash you took. So the evidence is genuine, correct?"*

Write the answer. One paragraph, no jargon the questioner has not already used, and it must be
**both accurate and useful** — "it's complicated" fails, and so does "yes".

**What good looks like.** It separates two things: what the match establishes about the *copy*, and
what carries the claim about the *original*. It names the record that carries the second. It does
not lecture.

---

## Task 4 — the correction · ~10 min

In the independent exercise you found what `mount -o loop` does to a verified image.

Write the **three-line correction** you would send the room's author:

1. The defect, in one sentence, stating what gets written.
2. The corrected command, with every option justified.
3. The one sentence you would add to the task text so a student understands *why*.

> This is not a writing exercise. Being able to say precisely what is wrong, precisely how to fix
> it, and precisely why it matters — in three lines, without heat — is most of what a review is.

---

## Rubric reminder (`D20`, unchanged since `P01`)

| # | Criterion | On this homework |
|---:|---|---|
| 1 | **Integrity** | Sections 4 and 5. Both digests, custody continuity, hash storage location. |
| 2 | **Method** | Can another examiner repeat your verification from what you wrote? |
| 3 | **Findings** | Each finding tied to a named artifact at an exact path. |
| 4 | **Separation** | Fact and reasoning are visibly different things. This is where the failing file is decided. |
