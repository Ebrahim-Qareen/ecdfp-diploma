# P03 · Independent work

`T04` &mdash; **CASE-01B**, 40 minutes. `T05` &mdash; three images, 9 minutes. Individual, at your keyboard.

---

## CASE-01B &mdash; the verification challenge · 40 min

**Case** ITG-2026-014 · **Exhibit** EVI-SRC02, USB mass storage.

A package arrived from another examiner: a folder of files and two manifests, one MD5 and one
SHA-256. The covering email said only:

> *"Verified before sending. Ready for your report."*

You have **no clean copy of anything**. You have the package and the two manifests.

**Your job: decide what you can state about this package, and what you cannot.**

### Rules

1. `sha256sum -c` alone will not finish this. Run it, then keep going.
2. Every claim must be backed by output you can show.
3. If you cannot determine something, that is a **finding**, not a gap.

### Step 1 — verify against **both** manifests

```bash
cd CASE-01B
sha256sum -c CASE-01B.sha256
md5sum -c CASE-01B.md5
```

Record the result for **every** file under **both** algorithms. Do not summarise yet.

> One file behaves **differently under the two manifests**. Note which, and think about what that
> difference can and cannot mean. It is not the same kind of problem as a file that fails both.

### Step 2 — compare the manifest to the folder

The manifest is a list. The folder is a list. They are not the same list.

```bash
awk '{print $NF}' CASE-01B.sha256 | sort > /tmp/manifest.txt
ls | grep -v '^CASE-01B' | sort > /tmp/disk.txt
comm -23 /tmp/manifest.txt /tmp/disk.txt    # in the manifest, not in the folder
comm -13 /tmp/manifest.txt /tmp/disk.txt    # in the folder, not in the manifest
```

Two files are involved and they are **opposite problems**. Name both, and say **which is more
serious for the examination**, and why.

### Step 3 — check identity, not only integrity

A passing hash proves the bytes did not change. It does not prove the file is what its name says.

```bash
file *
xxd -l 8 photo_evidence.txt
```

One file **passes both manifests and is still wrong**. Use it to explain the difference between
integrity and identity in two sentences.

### Step 4 — the file that looks normal

One file fails both manifests but opens looking completely ordinary. Find the difference **without a
clean copy**.

```bash
cat -A access_log_excerpt.txt
```

*(`cat -A` marks line ends with `$`, so trailing whitespace becomes visible.)*

What tells you which line is anomalous, given that you have nothing to compare against?

### Step 5 — two names, one digest

`duplicate_a.txt` and `duplicate_b.txt` both pass. Compare their digests. What does that tell you
about the package, and is it a problem?

---

### What you must NOT claim

For a file whose hash fails you can prove **that** it changed. You **cannot** state what changed,
because you hold no clean copy to compare against.

> *"The timestamp was altered from X to Y"* &mdash; an invention.
>
> *"The file does not match the recorded digest; the nature of the change cannot be determined from
> this package"* &mdash; a finding.

**This distinction is the whole point of the exercise**, and it is what criterion 4 grades.

### Deliverable

Section 8 of your report, with one entry per issue found. Each entry names the file, states the
measurement, and stops where your knowledge stops.

---

## `T05` &mdash; three images, three questions · 9 min

From `EVS-10`. One tool: `exiftool`.

| # | File | The question |
|---:|---|---|
| 1 | `office_floor3.jpg` | **Where** does this file say it was taken, and how confident can you be in that? |
| 2 | `invoice_batch.jpg` | **When** was it taken, and when was it last written? What accounts for the difference? |
| 3 | `team_photo.jpg` | **What** does its metadata tell you? |

### Success criteria

- For image 1 you wrote a **claim about the file**, not a fact about the world.
- For image 2 you named which field records which event, rather than calling the difference
  suspicious.
- For image 3 you wrote a finding. **An empty result is a result** &mdash; if your answer is
  *"the tool did not work"*, run it again on image 1 and compare.

> Image 3 is worth more than the two with GPS. Anyone can read a coordinate off a photograph.
> Reporting an absence precisely, without inventing a reason for it, is the skill this course is
> actually teaching.
