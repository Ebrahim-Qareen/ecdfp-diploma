# Session 3 — Quiz

**Hidden Information: Metadata, Steganography & Malicious Files**
**10 questions · all multiple choice (`D52`) · no score kept**

| Objective | Questions |
|---|---|
| **O1** read a value knowing its endianness and encoding | 1 |
| **O2** extract metadata; name which clock a date came from | 2 · 3 |
| **O3** detect hidden data; state the limit of a negative result | 4 · 5 · 6 |
| **O4** locate a macro in OLE and OOXML | 7 · 8 |
| **O5** separate what a photo shows from what it cannot prove | 9 · 10 |

---

## Q1 · MCQ · O1

A 4-byte value reads `D2 02 96 49` in a hex editor, in a structure from an x86 Windows image.

**What is the value?**

- **A.** `0x499602D2`, because x86 is little-endian.
- **B.** `0xD2029649`, reading left to right.
- **C.** Whichever the hex editor is configured to show.
- **D.** Both are equally valid readings.

---

## Q2 · MCQ · O2

A photograph's EXIF `DateTimeOriginal` is `2026:08:24`, its `DateTime` is `2026:08:31`.

**Which sentence belongs in Findings?**

- **A.** The photograph was taken on 2026:08:31.
- **B.** EXIF `DateTimeOriginal` is 2026:08:24 and EXIF `DateTime` is 2026:08:31.
- **C.** The image was tampered with seven days after it was taken.
- **D.** The camera clock was set incorrectly.

---

## Q3 · MCQ · O2

You copy a photograph from a disk image onto a USB stick. **Which timestamp changes?**

- **A.** EXIF `DateTimeOriginal`.
- **B.** EXIF `DateTimeDigitized`.
- **C.** The file system mtime.
- **D.** All four.

---

## Q4 · MCQ · O3

**Why does LSB steganography not survive being saved as a JPEG?**

- **A.** JPEG strips all metadata.
- **B.** JPEG images are too small to hold a payload.
- **C.** JPEG uses a different colour space.
- **D.** JPEG is lossy, and re-encoding discards the low-order detail the message lives in.

---

## Q5 · MCQ · O3

`zsteg` reports no payload in an image. **What do you write?**

- **A.** `zsteg <version>` reported no LSB payload; this does not exclude other methods.
- **B.** The image contains no hidden data.
- **C.** The image is clean.
- **D.** The image is encrypted.

---

## Q6 · MCQ · O3

A JPEG opens correctly in a viewer **and** unzips to reveal a text file.

**What is the finding?**

- **A.** The image was edited to conceal an archive.
- **B.** The file contains a ZIP archive beginning at offset `0x2857`, after the JPEG end-of-image marker.
- **C.** The file is corrupt.
- **D.** The file has two extensions.

---

## Q7 · MCQ · O4

In a `.docm` file, **where does the macro live?**

- **A.** In `word/document.xml`, as XML.
- **B.** In the file's EXIF metadata.
- **C.** In `word/vbaProject.bin`, which is itself an OLE compound file.
- **D.** In `[Content_Types].xml`.

---

## Q8 · MCQ · O4

Someone renames a `.docm` file to `.docx`. **What happens to the macro?**

- **A.** It is removed, because `.docx` is macro-free by definition.
- **B.** It is disabled but still present in the XML.
- **C.** It is converted to a script.
- **D.** Nothing — renaming changes a label, and `word/vbaProject.bin` is still there.

---

## Q9 · MCQ · O5

A photograph's EXIF carries GPS coordinates and a timestamp.

**What can you NOT conclude?**

- **A.** That a particular person was at those coordinates at that time.
- **B.** That the device recorded those coordinates.
- **C.** That the EXIF GPS block contains those values.
- **D.** That `DateTimeOriginal` holds that value.

---

## Q10 · MCQ · O5

*"The EXIF thumbnail differs from the main image in the region at (180,150)-(470,250)."*

**What kind of statement is that?**

- **A.** An interpretation.
- **B.** A finding.
- **C.** A limitation.
- **D.** A conclusion.

---

# Answer key

**Instructor copy only - not in this repository.**

The ten answers with their justifications live in `quiz_answer_key.md` in this folder on the
instructor machine. It is gitignored, because this repository is public (`D22`) and a published
answer key is not an answer key.
