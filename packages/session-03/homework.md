# Session 3 — Homework

**Hidden Information: Metadata, Steganography & Malicious Files**

---

## Part 1 — Strip your own metadata, then prove it is gone

Take one photograph of your own. Do not use case evidence.

1. Record everything ExifTool reports about it: `exiftool -a -G1 yourphoto.jpg`
2. Strip it: `exiftool -all= yourphoto.jpg`
3. Run step 1 again and compare.

**Answer these three:**

| # | Question |
|--:|---|
| 1 | Which blocks disappeared, and which survived? |
| 2 | Did the file's **size** change? Did its **pixels** change? How did you check? |
| 3 | You receive a photograph with no EXIF at all. Write the one-sentence finding that describes it — **without** claiming anyone stripped it. |

⚠️ **Question 3 is the point of the exercise.** Absent metadata has many causes: a screenshot, a social
platform that strips on upload, an export, a format that never carried it. *"The metadata was
removed"* is an interpretation, and usually an unsupported one.

---

## Part 2 — The forensic report

Write up **Case 03** using `report_template.md`. It has not changed since Session 1 and will not.

### Scope

Only what you did in `S3-07`: the file identification sweep, the recovered payload, and the appended
archive.

### Length

Two to three pages. Criterion 3 rewards findings tied to named artifacts, not volume.

### The rubric — unchanged, all four criteria

| # | Criterion | What earns the mark |
|---|---|---|
| 1 | **Integrity** | both sets verified against their manifests · you worked on a copy |
| 2 | **Method** | every tool named **with its version** · offsets as numbers · steps reproducible |
| 3 | **Findings** | fact only · each tied to one named artifact at an exact path |
| 4 | **Separation** | interpretation visibly distinct · at least one honest *"this evidence cannot show X"* |

### Before you submit — check yourself

| ☐ | |
|:-:|---|
| ☐ | Every date names **which clock** it came from |
| ☐ | Every offset is a number, not "near the end" |
| ☐ | Your steganography result names the tool, its version, **and its limit** |
| ☐ | The phrase *"the image is clean"* appears **nowhere** |
| ☐ | No finding claims a **person** did anything |
| ☐ | Every tool named with its version — ExifTool **13.59**, not "ExifTool" |

---

## Optional — practice, with its defect named (`D47`)

Public steganography challenges are plentiful, and most are built as puzzles: **the payload is always
there and always findable.**

⚠️ **That is the opposite of casework, and the habit it teaches is wrong.** A puzzle trains you to keep
digging until you find something. Real evidence is mostly negative, and the skill being graded is
writing an honest negative result.

Use them for tool practice — `zsteg`, Stegsolve, `binwalk` all reward repetition. Do not let them
teach you what a negative result means.

---

## Peer review

Pairs, once, on the report only (`D16`). Read your partner's report and mark every place a **finding**
has drifted into an **interpretation**. You are not marking whether they are right — only whether the
sentence belongs where it is.

---

## Before Session 4

| ☐ | |
|:-:|---|
| ☐ | Session 4's evidence downloaded **and hashes verified** (`D18`) |
| ☐ | `FOR-WS01` back on a clean snapshot |
| ☐ | Your custody line from this session closed on the record page |
| ☐ | Part 2 report submitted |

Session 4 goes underneath the file system: *"Everything today was inside a file. Next week we look at
what is left when the file is gone."*
