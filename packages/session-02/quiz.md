# Session 2 — Quiz

**Acquisition: Disk, Memory & Live Response**
10 questions · all multiple choice (`D52`) · one mark each · 15 minutes

Every question maps to a numbered objective:

| # | Objective |
|---|---|
| **O1** | Sequence a collection on a running host by order of volatility, and state what each delay destroys |
| **O2** | Capture memory from a live host, and state why the result is a smear rather than a snapshot |
| **O3** | Choose physical or logical acquisition for a stated goal, and name the evidence each one forfeits |
| **O4** | Create an image as E01 and as raw, and state exactly what `verified` covers and what it does not |
| **O5** | Acquire and verify the suspect USB, and write the result as a finding separated from interpretation |

---

## Q1 · MCQ · O1

You reach a workstation that is still running and unlocked. Which do you collect **first**?

- **A.** The contents of RAM
- **B.** The system disk
- **C.** The centralised server logs
- **D.** The archival backup tapes

---

## Q2 · MCQ · O1

A first responder powers a running host down before any capture is taken. Which question can **no
longer** be answered for that host?

- **A.** What files were stored on the disk
- **B.** Which network connections were open
- **C.** When the operating system was installed
- **D.** What the disk's serial number is

---

## Q3 · MCQ · O4

FTK Imager finishes an acquisition and its log reports `verified`. What has the tool **not** done?

- **A.** Hashed the data as it wrote the image
- **B.** Read the image back and hashed it a second time
- **C.** Re-read the source drive and compared it against the image
- **D.** Written both digests into the log

---

## Q4 · MCQ · O2

Why is a memory capture described as a **smear** rather than a snapshot?

- **A.** Compression discards pages during the write
- **B.** The tool deliberately skips kernel memory
- **C.** The dump is hashed only after it has been written
- **D.** The machine keeps running while memory is read, so different regions are read at different moments

---

## Q5 · MCQ · O3

A file named `policy_v2.docx` is opened in a hex editor. Its first four bytes are `89 50 4E 47`.

**What is it?**

- **A.** A PNG image carrying a `.docx` extension.
- **B.** A DOCX, which is a ZIP — those are the expected bytes.
- **C.** A corrupted DOCX whose header was damaged.
- **D.** An OLE compound document.

---

## Q6 · MCQ · O5

*"The USB image verified successfully against its published manifest."*
Is that a finding, an interpretation, a limitation, or a conclusion?

- **A.** An interpretation
- **B.** A finding
- **C.** A limitation
- **D.** A conclusion

---

## Q7 · MCQ · O5

*"The suspect copied company data to the USB device."*
Is that a finding, an interpretation, a limitation, or a verified fact?

- **A.** A finding
- **B.** A limitation
- **C.** An interpretation
- **D.** A verified fact

---

## Q8 · MCQ · O5

*"This image cannot show who physically attached the device to the workstation."*
Is that a finding, an interpretation, a conclusion, or a limitation?

- **A.** A finding
- **B.** An interpretation
- **C.** A conclusion
- **D.** A limitation

---

## Q9 · MCQ · O3

What does `dc3dd` give you that plain `dd` does not?

- **A.** A hash computed during imaging, and a log of the run
- **B.** A smaller output file
- **C.** The ability to image a running host safely
- **D.** Automatic partition recovery

---

## Q10 · MCQ · O3

You collect a targeted triage set instead of imaging the whole disk. Which question can you **no
longer** answer later?

- **A.** Which event logs existed on the host
- **B.** What was in the disk's unallocated space
- **C.** What the hostname was
- **D.** Which user accounts existed

---

# Answer key

**Instructor copy only - not in this repository.**

The ten answers with their justifications live in `quiz_answer_key.md`
in this folder on the instructor machine. It is gitignored, because this
repository is public (D22) and a published answer key is not an answer key.
