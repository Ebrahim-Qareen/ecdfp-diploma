# CASE-01B — Verification Challenge

**Case:** ITG-2026-014 · **Exhibit:** EVI-SRC02, USB mass storage device
**Time:** 45 minutes · **You may use:** anything from Session 1

---

## The situation

A package arrived from another examiner. It contains a folder of files and two
manifests — one MD5, one SHA-256. The covering email said only:

> "Verified before sending. Ready for your report."

You have no clean copy of anything. You have the package and the two manifests.

**Your job:** decide what you can state about this package, and what you cannot.

---

## Rules

1. `sha256sum -c` alone will **not** finish this. Run it, then keep going.
2. Every claim in your report must be backed by output you can show.
3. If you cannot determine something, that is a **finding**, not a gap. Write it
   in section 9 of the report template.

---

## Step 1 — Verify against both manifests

```bash
cd CASE-01B
sha256sum -c CASE-01B.sha256
md5sum -c CASE-01B.md5
```

Record the result for **every** file under both algorithms. Do not summarise yet.

> One file behaves differently under the two manifests. Note which, and note
> that the difference itself is the finding.

## Step 2 — Compare the manifest to the folder

The manifest is a list. The folder is a list. They are not the same list.

```bash
awk '{print $NF}' CASE-01B.sha256 | sort > /tmp/manifest.txt
ls | grep -v '^CASE-01B' | sort > /tmp/disk.txt

echo "--- in the manifest, not in the folder:" ; comm -23 /tmp/manifest.txt /tmp/disk.txt
echo "--- in the folder, not in the manifest:" ; comm -13 /tmp/manifest.txt /tmp/disk.txt
```

Two files are involved and they are **opposite problems**. Name both and say
which is more serious for the case, and why.

## Step 3 — Check identity, not only integrity

A passing hash proves the bytes did not change. It does not prove the file is
what its name says.

```bash
file *
xxd -l 8 photo_evidence.txt
```

One file passes both manifests and is still wrong. Explain the difference
between **integrity** and **identity** using it.

## Step 4 — The file that looks correct

One file fails both manifests but opens looking completely normal. Find the
difference without a clean copy.

```bash
cat -A access_log_excerpt.txt
```

*(`cat -A` marks line ends with `$` and makes trailing whitespace visible.)*

What tells you which line is wrong, given that you have nothing to compare against?

## Step 5 — Two names, one digest

`duplicate_a.txt` and `duplicate_b.txt` both pass. Look at their digests.
What does that tell you about the package, and is it a problem?

---

## What you must NOT claim

For a file whose hash fails, you can prove **that** it changed. You cannot state
**what** changed, because you hold no clean copy to compare against.

Writing "the timestamp was altered from X to Y" is an invention. Writing
"the file does not match the recorded digest; the nature of the change cannot
be determined from this package" is a finding.

This distinction is the point of the exercise.

---

## Deliverable

Fill `report_template.md`:

| Section | What goes in it |
|---|---|
| 4 | What you received and what you did — written while you can still see it |
| 6 | Findings — every file, every result, differing or not |
| 9 | **Limitations** — what this package cannot tell you, and why |

Section 9 is where most of the marks are.
