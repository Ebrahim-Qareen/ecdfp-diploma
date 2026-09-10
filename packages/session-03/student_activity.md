# Session 3 — Student Activity

**Two investigations, 60 minutes, individual at the keyboard.**
Case 03 — twelve files and a hidden payload · 35 min
Case 03b — the carry-through document · 25 min

---

## Case 03 — twelve files, and one of them is hiding something

**Time box: 35 minutes.**

### Brief

A folder was recovered from the suspect USB device imaged in Session 2. It contains twelve files.
Some are what they claim to be. Some are not. One image carries a hidden message and another has an
archive bolted onto the end of it.

**Your job: identify every file by its bytes, and recover what is hidden.**

### Scope and authorisation

You are authorised to examine `EVS-05` and `EVS-10`, mounted or copied read-only, and to extract
hidden content from them. You are **not** authorised to draw conclusions about who created, renamed
or hid anything.

### Evidence

| Set | Contents | Status |
|---|---|---|
| `EVS-05` | 12 files whose extensions are unreliable | ✅ verified |
| `EVS-10` | EXIF/GPS, an LSB payload and its clean twin, a polyglot, a thumbnail | ✅ verified |

⚠️ **Verify both against their published manifests before you begin.** Then work on a copy.

### The trap, named in advance

One file is called `policy_v2.docx`. A real `.docx` **is** a ZIP, so if you predict `50 4B 03 04` you
will be wrong. **Look, do not predict.**

### The questions

| # | Question |
|--:|---|
| **Q1** | Verify both sets against their manifests. State both results. |
| **Q2** | For all 12 files in `EVS-05`: name, extension, first four bytes, and the type those bytes indicate. |
| **Q3** | Which files' signatures disagree with their extensions? Give the count. |
| **Q4** | Two files have a valid signature and still will not open. What is wrong with them, and how do you know? |
| **Q5** | One image in `EVS-10` carries a hidden message. Recover it, and state the **method** you used to find it. |
| **Q6** | One image has an appended archive. Give the **offset** as a number and the name of the appended file. |
| **Q7** | Can you establish **who** hid the message? Answer honestly. |

⚠️ **Q7 is answerable only as a limitation.** Nothing in a file's bytes records a person — they record
a device, a program and a sequence of edits.

### Deliverable

```
F-01  <fact only, tied to one named artifact at an exact path>
I-01  <interpretation, clearly separated, with its basis>
L-01  <limitation — what this evidence cannot show>
```

### Success criteria

| ☐ | |
|:-:|---|
| ☐ | Q1 answered with an explicit pass or fail for **both** sets |
| ☐ | All 12 files listed with their first four bytes |
| ☐ | The offset in Q6 given as a **number**, not "near the end" |
| ☐ | Q5 names the tool **and its version** |
| ☐ | Q7 answered as a limitation, not guessed |
| ☐ | At least one honest *"this evidence cannot show X"* |

### Two things that will cost you marks

1. *"The user hid the message to conceal the theft."* Two interpretations stacked on one observation.
2. *"The other images are clean."* You tested them with one method. Say which, and what it does not cover.

---

## Case 03b — the carry-through document

**Time box: 25 minutes.**

### Brief

The document `l.bennett` opened, recovered from the `EVS-02` image. Take it apart in the order you
learned today: **type, then container, then structure, then content.**

⛔ **Evidence status.** `EVS-06` is extracted from the `EVS-02` disk image and **that acquisition has
not run yet**. Until it does, this case runs on a locally created macro-enabled document. The method
is identical; only the case relevance is deferred.

### The questions

| # | Question |
|--:|---|
| **Q1** | What is the file's real type, by signature? Does the extension agree? |
| **Q2** | Which container format is it — OLE or OOXML? How do you know **from the bytes**? |
| **Q3** | Give the exact path of the macro part inside the container, and its size. |
| **Q4** | List the external references the macro contains. Quote them verbatim. |
| **Q5** | State one thing this document proves, and one thing it cannot. |

### Success criteria

| ☐ | |
|:-:|---|
| ☐ | Q2 answered from the signature, not the extension |
| ☐ | Q3 gives a full path inside the container and a size in bytes |
| ☐ | Q4 quotes references verbatim, without interpreting them |
| ☐ | Q5's limitation is real — *a document being opened is not evidence of intent* |

### If you finish early

Rename the document's extension and confirm the macro part is still there. Then write the one-sentence
finding that proves renaming removed nothing.
