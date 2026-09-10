# P03 · Student guide — Data at byte level

Topics `T04` and `T05` · 117 minutes. Everything on the page, in order, so you can work through it
again alone.

---

## The one sentence

> **The name of a file is a label someone typed. The bytes are the file.**

`P02` proved your copy equals its source. This page asks the next question: identical to **what**?

---

## 1 · Hex is a way of reading, not a topic

One byte holds a value from 0 to 255. Two hex digits express it exactly: `00` to `FF`.

```bash
xxd -l 16 q3_summary.pdf
00000000: 2550 4446 2d31 2e34 0a25 e2e3 cfd3 0a31  %PDF-1.4.%......1
```

Two panes, **one set of bytes**. Left: the numbers. Right: the ones that happen to be printable
characters. Nothing is converted between them.

---

## 2 · The first bytes are the file's own claim

Most formats begin with a fixed byte pattern &mdash; a **signature**, or magic number.

| Bytes | Format | Read as |
|---|---|---|
| `25 50 44 46` | PDF | `%PDF` |
| `89 50 4E 47 0D 0A 1A 0A` | PNG | |
| `FF D8 FF` | JPEG | |
| `50 4B 03 04` | ZIP &mdash; **and `.docx`, `.xlsx`, `.pptx`, `.odt`, `.jar`, `.apk`** | `PK` |

> **Learn the last row properly.** A Word document *is* a ZIP archive with a particular structure
> inside it. When you meet OOXML later, you should already expect `50 4B`.

Windows picks a program by **extension**. Unix-like systems read the **signature**. Two different
answers to the same question, and only one of them lives inside the file.

---

## 3 · What a rename actually changes

Renaming rewrites a **name string** &mdash; in the directory index, and in the file's `$FILE_NAME`
attribute. It does **not** read, move or rewrite the clusters holding the content.

That is the mechanism behind everything on this page:

> **The header survives a rename because the header is content. The extension is not.**

Which is why a keyword search for `*.jpg` will not find every JPEG on a disk, and why signature
analysis exists at all.

---

## 4 · The limits &mdash; read these before you write anything

Signature analysis is **better evidence than the extension**. It is not certainty.

- **Four bytes are trivially forged.** Writing `FF D8 FF` at offset 0 takes a moment.
- **Many formats have no signature at all** &mdash; plain text, CSV, many logs. A *missing* match
  establishes nothing.
- **A mismatch is not an action.** You observe a state. You did not observe anyone renaming
  anything.
- **A mismatch is certainly not a motive.** *&ldquo;Renamed to hide it&rdquo;* is a story you added.

The correct sentence has this shape:

> `thumbnail.png` begins `FF D8 FF E0`, which matches the JPEG signature and not the PNG signature
> its extension implies.

---

## 5 · Endianness &mdash; pattern versus value

The order a **multi-byte value** is stored in.

- **Little-endian** puts the least significant byte first. x86, Windows and NTFS are little-endian.
- **Big-endian** puts the most significant first. Many network protocol fields use it.

The bytes `00 10 00 00` read little-endian are the value `0x00001000` &mdash; **4096**. Read
big-endian they are `0x00100000` &mdash; **1 048 576**. Same four bytes, and a factor of 256 between
the two answers.

> **The distinction people trip over:** a signature like `FF D8` is a **pattern**, read left to
> right. A field like a timestamp or a size is a **value**, and its byte order matters. Ask yourself
> which you are looking at before you read a number off a hex dump.

**Encodings**, briefly: ASCII, then UTF-8, then UTF-16LE. Windows internals are full of UTF-16LE,
which is why a plain string search for `svchost` can miss it entirely.

---

## 6 · Metadata, and what it is worth

**EXIF** is metadata a camera writes into an image &mdash; make, model, software, timestamps,
sometimes GPS. Every piece of software that touches the file afterwards can rewrite it.

### The two timestamps

| Field | Records |
|---|---|
| `DateTimeOriginal` | when the **shutter fired**. Written once, by the camera |
| `ModifyDate` / `DateTime` | when the file was **last written**. Rewritten by whatever touched it |

So when they disagree, that is not evidence of tampering &mdash; it is the **expected** state of any
image that has been edited. It tells you the file was written to on that later date, and the
`Software` field usually tells you by what.

### The rule for GPS

> The file **records** coordinates. That is your finding.
>
> *The photograph was taken there* is an interpretation, and it needs the device clock to have been
> right, the location service to have been on and correct, and the file to be unedited since.

### And the case that matters most

Sometimes `exiftool` returns a name, a size, a type &mdash; and nothing else.

**That is a result.** Write it:

> The file contains no EXIF metadata block. The absence is consistent with a camera that writes
> none, with software that stripped it, or with re-encoding; which of these applies cannot be
> determined from the file alone.

> The commonest mistake in this topic is reporting an empty result as *&ldquo;the tool did not work&rdquo;*.
> It worked. **An absence is frequently the finding.**

---

## 7 · Integrity and identity are different properties

`P02` gave you integrity: **the bytes did not change**.

This page gives you identity: **the file is what it claims to be**.

They are independent, and a single file can demonstrate it: one that verifies perfectly against
both manifests, is named `.txt`, and begins `89 50 4E 47`. Integrity intact. Identity wrong.

---

## 8 · The sentence to keep

For any file whose verification fails, when you hold no clean copy:

> The file does not match the recorded digest. **The nature of the change cannot be determined from
> this package.**

Say the first part. Say the second part. Stop.
