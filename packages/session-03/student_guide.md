# Session 3 — Student Guide

**Hidden Information: Metadata, Steganography & Malicious Files**

---

## What changes today

Session 1 gave you hex and magic bytes. Session 2 gave you verified images. Today you stop asking
*what is this file?* and start asking **what is inside it that nobody meant you to see?**

⚠️ **This is the session where it is easiest to overreach.** A GPS tag feels like proof that a person
was somewhere. It is not. Criterion 4 of the rubric — separating what you found from what it means —
matters more today than anywhere else in the course.

---

## 1 · Endianness and encodings

Reading a file's *type* needs the first bytes. Reading anything else out of a structure — an offset,
a length, a timestamp — needs to know **which way round the number is stored**.

| | Bytes on disk | Read as |
|---|---|---|
| **Big-endian** | `0A 0B 0C 0D` | `0x0A0B0C0D` = 168 496 141 |
| **Little-endian** | `0A 0B 0C 0D` | `0x0D0C0B0A` = 218 893 066 |

Same four bytes, two answers, 50 million apart. **The format specification decides which is right.**

- Network protocols and some file formats are big-endian ("network byte order").
- **x86 is little-endian**, so most Windows structures are. This is why a timestamp looks backwards
  in a raw hex view — it is not corrupt, you are reading it the wrong way.

**Encodings are the same problem.** `41` is `A` in ASCII and UTF-8. In UTF-16LE, `A` is `41 00` — so
text read with the wrong decoder shows a null between every letter.

---

## 2 · Metadata and EXIF

A JPEG carries blocks of metadata alongside the picture:

| Block | Holds | Careful |
|---|---|---|
| **Camera** | Make, Model, Software | `Software` shows the file was *processed*, not *what changed* |
| **Timestamps** | DateTimeOriginal · DateTimeDigitized · DateTime | three clocks, and they can all disagree |
| **GPS** | latitude, longitude, date stamp | records what the **device** stored |
| **Thumbnail** | a second, smaller copy of the image | sometimes not updated when the image is edited |

### The four clocks

| Clock | Meaning | Lives |
|---|---|---|
| `DateTimeOriginal` | the shutter fired | inside the file |
| `DateTimeDigitized` | became a file | inside the file |
| `DateTime` | last modified | inside the file |
| file system **mtime** | last touched by the file system | **outside** the file |

**Copying a file to a USB stick rewrites the mtime and leaves all three EXIF values alone.** That
asymmetry is useful: internal metadata travels with the file, external metadata describes the journey.

🔴 **There is no "the date" of a photograph. A finding names which clock it read.**

---

## 3 · Steganography

Steganography is not encryption. Encryption makes a message unreadable **and obvious**.
Steganography makes it **unremarkable** — the goal is that nobody looks.

### How LSB works

Change the least significant bit of a colour channel. Blue 180 becomes 181. The eye cannot resolve a
one-step change, so the picture looks identical.

- **Capacity:** 1 bit per channel per pixel — about 23 KB in a 320×240 image using all three channels.
- 🔴 **Format constraint:** LSB needs a **lossless** format — PNG, BMP, TIFF, WAV. **It does not
  survive JPEG**, because re-encoding discards exactly the low-order detail the message lives in.

🟢 **Use that operationally:** in a folder of mostly JPEGs, a lone PNG is where to spend your first
ten minutes. That is not a finding — it is triage.

### How you detect it

| Method | How | Cost |
|---|---|---|
| File size vs content | a simple graphic that is far too big | cheap, weak |
| **View the LSB plane** | `zsteg`, or Stegsolve's plane browser | cheap, **strong** |
| Statistical tests | chi-square, RS analysis on the bit distribution | stronger, needs a tool |
| Known-tool signatures | `steghide`, OpenStego leave recognisable structure | strongest when it hits |

🟢 **The one to learn is the bit plane.** A natural photograph's low bit is sensor noise and looks
like static. A payload has **structure** — blocks, edges, a band that stops abruptly where the
message ended. You can often see it.

🔴 **Absence of a detection is not absence of a payload.** Write it as: *`zsteg <version>` reported no
LSB payload; this does not exclude other methods.*

---

## 4 · Files inside files

Cruder than steganography and far more common: the second file is **appended**, past the point the
first reader stops looking.

```
[ FF D8 FF ... JPEG image data ... FF D9 ][ 50 4B 03 04 ... ZIP ... ]
                  image ends here ^        ^ archive starts here
```

**Why both readers are satisfied:** an image decoder reads forward and stops at `FF D9`. A ZIP reader
does the **opposite** — it seeks to the end of the file and reads the central directory backwards, so
leading data does not bother it.

```
$ binwalk team_photo.jpg
0         0x0      JPEG image data
10327     0x2857   Zip archive data, name: handover.txt
```

`binwalk` finds it because it scans for **every** signature at **every** offset, instead of trusting
the first one.

⚠️ Some formats append thumbnails and colour profiles legitimately. **The offset is the finding; the
intent is not.**

---

## 5 · Where a macro lives

| | **OLE** (`.doc`, `.xls`) | **OOXML** (`.docx`, `.docm`) |
|---|---|---|
| Signature | `D0 CF 11 E0 A1 B1 1A E1` | `50 4B 03 04` — it is a ZIP |
| Structure | a small filesystem of streams | a ZIP of XML parts |
| Macro at | `Macros/VBA/Module1` | `word/vbaProject.bin` — **itself an OLE file** |
| Read with | `oledump.py`, then `olevba` | unzip first, then the same tools |

🔴 **`.docx` is defined as macro-free; `.docm` is the macro-enabled one. But the extension is a
label — renaming a `.docm` to `.docx` removes nothing.** The check that works: unzip it and look for
`word/vbaProject.bin`. **The presence of that part is the finding.** What the macro does is a
separate question.

---

## 6 · Image forensics — the thumbnail

Cameras embed a small preview so galleries render quickly. **Some editors update it; some do not.**

When they do not, the thumbnail is a picture of the file **before the edit**:

```
exiftool -b -ThumbnailImage invoice_batch.jpg > thumb.jpg
```

**Finding:** the EXIF thumbnail differs from the main image in the region at (180,150)-(470,250).
**Interpretation:** the main image was modified after the thumbnail was generated.
**Cannot prove:** who modified it, when, or why.

⚠️ **And the honest limit:** plenty of editors update the thumbnail correctly, so a **matching**
thumbnail proves nothing at all.

---

## 7 · What a photograph cannot prove

| You may write | You may not write |
|---|---|
| EXIF `GPSLatitude` records `<value>` | the suspect was at the warehouse |
| the device recorded those coordinates | the photo was taken at 09:14 |
| `DateTimeOriginal` is `<value>` | the image was tampered with |
| the EXIF thumbnail differs from the main image | the metadata proves the file is authentic |

**A photograph places a device, never a person.** Phones are shared, lent and stolen. Camera clocks
are routinely wrong and the base EXIF spec has no timezone field.

---

## 8 · Before you leave

- Both evidence sets verified against their manifests.
- You can name which clock any date you quote came from.
- You can state, in one sentence, what a negative steganography result means.
- Your custody line is filled and the session's steps are closed.
