# P03 · Quiz — Data at byte level

Topics `T04` and `T05`. Twelve questions. Answer key: `quiz_answer_key.md`.

**Objectives**
1. Read a file's first bytes and say what they establish.
2. State the limits of signature analysis.
3. Explain what a rename does and does not change.
4. Read a verification result that differs between two algorithms.
5. Separate integrity from identity.
6. Read EXIF as a claim rather than a fact.
7. Report an absence as a finding.

---

**Q1 · obj 1.** `xxd -l 4 report.docx` returns `89 50 4E 47`. What is established?

- a) The file is a PNG image.
- b) The file's first four bytes match the PNG signature and not the ZIP signature a `.docx` requires.
- c) Someone renamed a PNG to hide it.
- d) The file is corrupt.

---

**Q2 · obj 2.** Why is a matching signature *evidence* rather than *proof* of file type?

- a) Signature tables are incomplete.
- b) Four bytes are trivially forged, and some formats have no magic number at all.
- c) `file` is unreliable on Windows.
- d) Signatures change between versions of a format.

---

**Q3 · obj 3.** A JPEG is renamed from `photo.jpg` to `report.docx`. What changed on disk?

- a) The first bytes were rewritten to `50 4B 03 04`.
- b) The file was re-encoded into the new format.
- c) A name string in the directory index and the `$FILE_NAME` attribute. The clusters holding the content were not read, moved or rewritten.
- d) Nothing &mdash; a rename is not a write.

---

**Q4 · obj 1.** Which of these is a ZIP container in ordinary use?

- a) `.pdf`
- b) `.docx`
- c) `.rtf`
- d) `.csv`

---

**Q5 · obj 4.** A file **passes** verification against the SHA-256 manifest and **fails** against the MD5 manifest. What follows?

- a) The file was altered; MD5 detected it and SHA-256 missed it.
- b) The file was altered; SHA-256 detected it and MD5 missed it.
- c) The file cannot have changed &mdash; a changed file fails both. One of the two manifests is incorrect.
- d) MD5 is broken, so the MD5 result should be ignored.

---

**Q6 · obj 4.** In the same package, one file is listed in the manifest but absent from the folder, and another is present in the folder but absent from the manifest. Which is more serious for the examination, and why?

- a) The extra file &mdash; unlisted content is always suspicious.
- b) The missing file &mdash; something the sender recorded is not available to examine, and its absence cannot be resolved from this package.
- c) They are equally serious.
- d) Neither &mdash; manifests routinely drift.

---

**Q7 · obj 5.** A file verifies against both manifests and begins `89 50 4E 47`, but is named `.txt`. State it correctly.

- a) Integrity failed.
- b) Integrity is intact; identity does not match the name.
- c) The manifest is wrong.
- d) The file is corrupt but recoverable.

---

**Q8 · obj 1, 4.** You hold a package and no clean copy. A file fails verification. Which sentence belongs in Findings?

- a) The file was modified after the manifest was created.
- b) The timestamp inside the file was altered.
- c) The file does not match the recorded digest; the nature of the change cannot be determined from this package.
- d) The sender tampered with the file before sending it.

---

**Q9 · obj 6.** A photograph's EXIF carries GPS coordinates. What is the finding?

- a) The photograph was taken at those coordinates.
- b) The file records GPS coordinates of that value.
- c) The camera was at those coordinates when the shutter fired.
- d) The photographer was at those coordinates.

---

**Q10 · obj 6.** `DateTimeOriginal` reads `2026:08:24 09:14:02` and `ModifyDate` reads `2026:08:31 16:40:05`. What does the seven-day difference indicate?

- a) The timestamps were tampered with.
- b) The camera clock was wrong.
- c) The file was written to on 31 August &mdash; which is what these two fields are supposed to show when an image has been edited.
- d) The photograph was taken twice.

---

**Q11 · obj 7.** `exiftool` on an image returns a file name, size and type and no EXIF block. What do you write?

- a) The tool failed to parse the image.
- b) The image has no metadata, so there is nothing to report.
- c) The file contains no EXIF block; the absence is consistent with a camera that writes none, with software that stripped it, or with re-encoding, and cannot be resolved from the file alone.
- d) The metadata was deliberately removed.

---

**Q12 · obj 6.** Two files carry the same SHA-256 digest under different names. What does that establish?

- a) A hash collision has been found.
- b) They hold identical content &mdash; the package contains the same file twice under two names.
- c) One is a shortcut to the other.
- d) The manifest was generated incorrectly.

---

> **Q5 and Q8 are the two that separate the class.** Both punish the instinct to name a cause. Q5
> asks you to reason from *which check disagreed*; Q8 asks you to stop at the edge of what a failing
> hash carries. Getting the byte questions right and these two wrong means the mechanics landed and
> the discipline did not.
