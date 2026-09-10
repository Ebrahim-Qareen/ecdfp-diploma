# Session 3 — Instructor Guide

**Hidden Information: Metadata, Steganography & Malicious Files** · 205 topic min + 15 break

---

## 0 · Pre-class checklist

| ☐ | Item |
|:-:|---|
| ☐ | `EVS-05` and `EVS-10` published with **both** digests (`D18`) — both are **verified**, so this session is not blocked |
| ☐ | ⛔ `EVS-06` still pending. Have a **locally created macro-enabled document** ready as the stand-in for `S3-05` and `S3-08` |
| ☐ | ExifTool, `binwalk`, `zsteg`, Stegsolve, `oledump.py`/`olevba`, HxD on every machine |
| ☐ | Session 2's record open — the session opens by checking what was closed |
| ☐ | Versions on the board |

---

## 1 · The sentence the session turns on

> *"A photograph places a **device**, never a **person**."*

Say it early, and use it every time a student's finding drifts. **This is the session where criterion 4
is most often lost**, because GPS and timestamps feel like proof in a way that a hash never does.

---

## 2 · Per-block teaching notes

### `S3-01` — Endianness and encodings · 15 min

The only theory-only block in the session; keep it tight.

Draw `0A 0B 0C 0D` once and read it both ways: `168 496 141` big-endian, `218 893 066` little-endian.
**Same bytes, two answers, 50 million apart.** x86 is little-endian, so most Windows structures are —
and that is why a timestamp looks backwards in a raw hex view.

Encodings in one line: `41` is `A` in ASCII and UTF-8; in UTF-16LE it is `41 00`, so text read with the
wrong decoder shows a null between every letter. **Not corruption — the wrong decoder.**

**The habit to instil:** the specification decides, never what looks plausible, and never a tool's
silent default. State which you used.

---

### `S3-02` — Metadata and EXIF · 25 min

Four blocks: camera, timestamps, GPS, thumbnail. Walk the figure, then go straight to the clocks.

🔴 **The four clocks are the point of the block.** Three live inside the file, one outside it. Copying
to a USB stick rewrites the mtime and leaves the EXIF alone — **that asymmetry is what makes internal
and external metadata answer different questions.**

**The correction to make immediately, every time:** a student who writes *"the photo was taken on
2026-08-31"* has read `DateTime` (last modified), not `DateTimeOriginal`. There is no *"the date"*.

**Micro-labs 1 and 2 · 10 min.** Read every block; then line the four clocks up and write the gaps.

---

### `S3-03` — Steganography · 25 min · 🔴 new

**Open by separating it from encryption:** encryption makes a message unreadable **and obvious**;
steganography makes it **unremarkable**. The goal is that nobody looks.

**Then LSB, concretely.** Blue 180 → 181. Invisible. 1 bit per channel per pixel.
🔴 **Format constraint, and it is operationally useful:** LSB needs lossless — PNG, BMP, TIFF, WAV. It
**does not survive JPEG**. So a lone PNG among JPEGs is where to spend the first ten minutes. Say
clearly that this is **triage, not a finding**.

**Spend most of the block on detection, not embedding.** Students find embedding fun and it teaches
them nothing an examiner needs.

| Method | Note |
|---|---|
| size vs content | cheapest, weakest |
| **view the bit plane** | 🟢 the one to learn — noise vs structure, often visible |
| statistical tests | chi-square / RS, report as *an indication* with the tool named |
| known-tool signatures | and **check the host** for an installed stego tool — often stronger than analysing the picture (that is S5) |

🔴 **The sentence to drill:** *absence of a detection is not absence of a payload.*

**Micro-lab 3 · 8 min.** `zsteg` on the payload file and on the clean twin, then both bit planes in
Stegsolve. The clean twin is in the set precisely so a negative result has something to look like.

---

### `S3-04` — Embedded and appended data · 20 min · 🔴 new

Cruder than stego, far more common. `[JPEG ... FF D9][ZIP ...]`.

**Why both readers are satisfied** — and this is the satisfying part to teach: an image decoder reads
forward and stops at `FF D9`; **a ZIP reader does the opposite**, seeking to the end and reading the
central directory backwards. Two readers with opposite habits, one file that pleases both.

🔴 **This is why `S1-09` insisted on the end marker as well as the signature.** A signature says where
a file begins; the terminator says where it should stop — and therefore whether anything follows.

`binwalk` wins because it scans **every signature at every offset** rather than trusting the first.

⚠️ Legitimate appends exist (thumbnails, colour profiles). **The offset is the finding; intent is not.**

**Micro-lab 4 · 8 min.**

---

### `S3-05` — Malicious document structure · 25 min

**OLE** is a small filesystem inside a file; macro at `Macros/VBA/Module1`.
**OOXML** is a ZIP of XML; macro at `word/vbaProject.bin` — **which is itself an OLE file**. So the
macro is OLE either way; only the digging differs.

🔴 **The extension trap:** `.docx` is defined macro-free, `.docm` is macro-enabled — but renaming a
`.docm` to `.docx` **removes nothing**. The check that works is unzipping and looking for the part.
**Presence of `word/vbaProject.bin` is the finding.** What the macro does is a separate step.

**Micro-lab 5 · 8 min.** ⛔ On the stand-in document until `EVS-06` exists. Say so — do not pretend
the case document is in hand.

**The limitation to state:** a document being opened is not evidence of intent, and a macro executing
is not evidence anyone chose to run it knowingly.

---

### `S3-06` — Image forensics · 20 min · 🔴 new

**The thumbnail that outlived the edit.** Extract it, put it beside the main image, and let the room
see the redacted content reappear. It lands better than any explanation.

```
exiftool -b -ThumbnailImage invoice_batch.jpg > thumb.jpg
```

⚠️ **State the honest limit immediately:** many editors update the thumbnail correctly, so a
**matching** thumbnail proves nothing. This technique finds a failure, not a rule.

**Then close the block on the `D7` figure** — the same photograph as a finding, an interpretation and
a limitation. **This is the highest-value eight minutes in the session.** Do not run over `S3-05` and
lose it.

---

### `S3-07` — Case 03 · 35 min · blocked investigation

Individual at the keyboard. Hand out the brief, name the `policy_v2.docx` trap **in advance** (it is
in the student brief deliberately), then stay quiet.

**Watch for:** a student who predicts `50 4B 03 04` for the `.docx` because they learned the rule.
That is the whole point of the file — it punishes pattern-matching and rewards looking.

---

### `S3-08` — The carry-through document · 25 min · blocked investigation

Type → container → structure → content, in that order. ⛔ Runs on the stand-in until `EVS-06` exists.

---

### `S3-09` — The closing ritual · 15 min

Identical in shape to `S1-11` and `S2-09`, and it stays identical.

---

## 3 · Where students reliably go wrong — the six

| # | Error | Correction |
|--:|---|---|
| 1 | Reading `DateTime` and calling it the date of the photograph | three clocks inside, one outside. Name which one |
| 2 | *"The GPS proves the suspect was there"* | it places a **device**, never a person |
| 3 | *"`zsteg` found nothing, so it is clean"* | a negative test is not proof of absence |
| 4 | Looking at the picture to spot steganography | the one method guaranteed not to work — view the bit plane |
| 5 | Predicting `.docx` is a ZIP instead of checking | `policy_v2.docx` in `EVS-05` is a PNG |
| 6 | *"The image was tampered with"* from a resave | cropping and converting update `DateTime` legitimately |

---

## 4 · If you are running short

Cut in this order and record it in `build_log.md`:

1. **`S3-01` encodings half** — keep endianness, drop UTF-16. Saves ~5 min.
2. **Micro-lab 4** — demonstrate the polyglot once instead of each student doing it. Saves ~6 min.
3. **`S3-05` OLE half** — teach OOXML fully, name OLE and move on. Saves ~8 min.

🔴 **Never cut:** `S3-06`'s closing `D7` figure, the investigation hour, or the ritual.

---

## 5 · Bridge to Session 4

Everything today was **inside a file**. S4 goes underneath the file system — sectors, clusters and
slack, MBR and GPT, FAT and NTFS — and recovers the staging archive deleted before the exfiltration.

Closing line: *"Everything today was inside a file. Next week we look at what is left when the file is gone."*
