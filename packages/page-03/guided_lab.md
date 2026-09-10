# P03 · Guided lab — read the bytes, then read the metadata

Topics `T04` (18 min) + `T05` (10 min) · evidence `EVS-05`, `EVS-10` · workstation `FOR-WS01`.
Every step has a **verification line**. Do not move on without it.

---

## Part A — the signature sweep · `T04`

### Step 0 — known state

Restore `CLEAN-TOOLS`. **Verify:** the snapshot manager shows it as current.

### Step 1 — look at one file the slow way

```bash
cd ~/Cases/ITG-2026-014/EVS-05
xxd -l 16 q3_summary.pdf
```

**Verify:** you see two panes. Left: `2550 4446 2d31 2e34 ...`. Right: `%PDF-1.4`.

> **Both panes are the same bytes.** The left shows them as numbers, the right shows the ones that
> happen to be printable characters. Nothing is being converted &mdash; you are looking at one thing
> two ways.

### Step 2 — the first four bytes are the claim

```bash
xxd -l 4 q3_summary.pdf
```

**Verify:** `2550 4446`. That is `%PDF`. The file's own first bytes say what format it is.

Now the same file through a tool that reads signatures rather than names:

```bash
file q3_summary.pdf
```

**Verify:** `PDF document, version 1.4`. Name and bytes agree. Nothing to see &mdash; yet.

### Step 3 🔑 — a file whose bytes disagree with its name

```bash
xxd -l 4 thumbnail.png
```

**Verify:** `ffd8 ffe0`.

**Stop. Write down what you now know, in one sentence.**

The honest sentence:

> The first four bytes of `thumbnail.png` match the **JPEG** signature, not the PNG signature.

Now notice what is **not** in that sentence:

| Not established | Why not |
|---|---|
| "the file is a JPEG" | four bytes agreeing with a table is good evidence, not proof &mdash; and four bytes are trivially forged |
| "someone renamed it" | you have no evidence of an action, only of a state |
| "someone renamed it **to hide something**" | that is motive, and nothing here carries motive |

### Step 4 — sweep the whole set

```bash
file *
```

**Verify:** twelve results. **Five disagree with their extension:**

```
thumbnail.png       JPEG image data
holiday_snap.jpg    Zip archive data
invoice_scan.jpg    PDF document
meeting_notes.txt   PNG image data
policy_v2.docx      PNG image data
```

> **Look hard at `policy_v2.docx`.** A `.docx` is a ZIP container &mdash; it should begin `50 4B 03 04`.
> This one begins `89 50 4E 47`. Its extension is wrong **twice over**: it is not a Word document,
> and it is not even the container a Word document lives in.

### Step 5 — prove the rename does not touch the bytes

```bash
cp readme.txt /tmp/rename_test.jpg
xxd -l 8 /tmp/rename_test.jpg
```

**Verify:** the first bytes are unchanged &mdash; still the text file's bytes, now under a `.jpg` name.

> Renaming rewrites a **name string** in the directory index. It does not read, move or rewrite the
> clusters holding the content. That is the whole mechanism: **the header survives because the header
> is content, and the extension is not.**

---

## Part B — the metadata read · `T05`

### Step 6 — what a photograph says about itself

```bash
cd ~/Cases/ITG-2026-014/EVS-10
exiftool office_floor3.jpg
```

**Verify:** you see `Make`, `Model`, `Software`, two date fields, and a GPS block.

### Step 7 — the location claim

**Verify:**

```
GPS Latitude    30 deg  2' 27.60" N
GPS Longitude   31 deg 14' 13.20" E
```

> **Write it as a claim, not a fact.** The correct finding is *the file records GPS coordinates of
> 30&deg;2&prime;27.60&Prime;N 31&deg;14&prime;13.20&Prime;E*. Not *the photograph was taken there*.
> EXIF is ordinary editable data.

### Step 8 🔑 — two timestamps that disagree

```bash
exiftool -DateTimeOriginal -ModifyDate -Software office_floor3.jpg
```

**Verify:**

```
Date/Time Original  : 2026:08:24 09:14:02
Modify Date         : 2026:08:31 16:40:05
Software            : MRG ImageTool 2.4
```

**Seven days apart.** Before calling that suspicious, ask what each field records:

| Field | Records |
|---|---|
| `DateTimeOriginal` | when the **shutter fired** &mdash; written once, by the camera |
| `ModifyDate` (`DateTime`) | when the file was **last written** &mdash; rewritten by whatever touched it |

> So the disagreement is not evidence of tampering. It is evidence that **software wrote to this
> file on 31 August**, and the `Software` field names it. Two fields disagreeing is what you would
> **expect** from any edited image.

### Step 9 — the empty result

```bash
exiftool team_photo.jpg
```

**Verify:** the output has a file name, a size and a type &mdash; and **no EXIF block at all**.

**This is a finding. Write it:**

> `team_photo.jpg` contains no EXIF metadata. The absence is consistent with a camera that writes
> none, with software that stripped it, or with re-encoding. Which of these applies **cannot be
> determined from the file alone**.

> **An empty result is a result.** The commonest mistake in this lab is reporting it as *"the tool
> did not work"*. It worked perfectly. It told you there is nothing there.

### Step 10 — one more, for contrast

```bash
exiftool -GPSLatitude -GPSLongitude invoice_batch.jpg
```

**Verify:** no GPS fields returned, though the file **does** carry other EXIF.

> Three images, three different states: full EXIF with GPS &middot; EXIF without GPS &middot; no EXIF at
> all. Only one of the three is *"the camera recorded a location"*, and none of the three is
> *"the photograph was taken at that location"*.

---

## Chain of custody — the line this lab produces

```
[YYYY-MM-DD HH:MM UTC]  EVS-05 and EVS-10 examined by [your name] on FOR-WS01
                        (state: CLEAN-TOOLS snapshot). Read only; no file modified.
                        EVS-05: signature sweep, `file` over 12 files.
                        5 of 12 carry a signature that disagrees with the extension.
                        EVS-10: EXIF read over 3 images with exiftool.
                        1 with GPS, 1 without GPS, 1 with no EXIF block.
                        No conclusion drawn as to cause.
```

**Verify:** your line records what you ran and what it returned. If it contains the word *hidden*,
*disguised* or *altered*, delete that word and read it again.
