# P03 · Report stage — Sections 6 and 8

Your report for `ITG-2026-014` has been open since `P01`. Sections 1, 3, 4 and 5 are done.
Today you open the two that carry the examination itself.

---

## Section 6 — Tools and method · after `T04`

One row per tool, per use. The test is blunt:

> **Could another examiner repeat exactly what you did, from this table alone?**

| Column | Rule |
|---|---|
| Tool | the name as the tool reports it, not as you remember it |
| Version | run `--version`. &ldquo;latest&rdquo; is not a version |
| Run on | the exact path, and the exhibit it belongs to |
| Purpose | one line: what question you were answering |
| Output | where the output is filed |

**Rows you can write today:**

- `sha256sum` / `md5sum` &mdash; verification of `EVS-01`, `EVS-05` and `CASE-01B` against their manifests.
- `file` &mdash; signature identification across `EVS-05` and the `CASE-01B` package.
- `xxd` &mdash; first-bytes read on named files.
- `exiftool` &mdash; metadata read on three `EVS-10` images.

> **The line most people forget:** the *read-only* statement. If nothing you ran modified an exhibit,
> say so here, because later you will want to have said it.

---

## Section 8 — Findings · after `T05`

The first real entries. Every finding obeys three rules, and rule 3 is the one that gets graded:

1. **Named artifact, exact path.** Not &ldquo;a file in the package&rdquo;.
2. **A measurement**, in the form the tool produced it.
3. **It stops where your knowledge stops.**

### The four entries this page produces

**From the signature sweep:**

> **F-01** &mdash; `EVS-05/thumbnail.png` begins `FF D8 FF E0`, which matches the JPEG signature and
> not the PNG signature its extension implies. Five of the twelve files in `EVS-05` carry a
> signature that disagrees with their extension.

**From Case 01, and this is the one that separates the class:**

> **F-02** &mdash; `CASE-01B/policy_extract.txt` **passes** verification against the SHA-256 manifest
> and **fails** against the MD5 manifest. A file whose content changed would fail both. The
> discrepancy therefore concerns one of the two manifests, not the file. Which manifest is incorrect
> cannot be determined from this package.

> **F-03** &mdash; `CASE-01B/photo_evidence.txt` verifies against both manifests and begins
> `89 50 4E 47` &mdash; a PNG. Its integrity is intact and its identity does not match its name.

**From the metadata read:**

> **F-04** &mdash; `EVS-10/team_photo.jpg` contains no EXIF metadata block. The absence is consistent
> with a camera that writes none, with software that removed it, or with re-encoding; which of these
> applies cannot be determined from the file alone.

### Read them back

Every one names a file and a path, states what the tool returned, and **ends before the reason**.
None contains *hidden*, *disguised*, *altered by*, or *someone*.

> **The sentence that fails criterion 4** is the tempting one: *&ldquo;`thumbnail.png` was renamed to
> disguise a JPEG.&rdquo;* You have a byte pattern. You do not have an action, and you certainly do not
> have an intention.

---

## Still empty on purpose

**Section 9 Interpretation** is where the reasons go &mdash; and it stays closed until you have enough
findings to reason across. **Sections 2 and 11** are written last (`D85`).

**Six of twelve sections** are now written, and you have not analysed a disk, a memory capture or a
log. That is the argument for writing as you go, made in numbers.
