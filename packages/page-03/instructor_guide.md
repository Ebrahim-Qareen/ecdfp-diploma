# P03 · Instructor guide — Data at byte level

Page `P03` · topics `T04` (82 min) + `T05` (35 min) · **117 topic minutes**.
Evidence `EVS-05` · `EVS-01` · `EVS-10` · case `CASE-01B`. Outline: `design/P03_outline.md`.
Design frozen by `D109`; diagrams stepped per `D115`.

---

## 0 · Pre-class checklist

- [ ] `EVS-05` and `EVS-10` generated and unzipped on every machine. **They were never generated
      before this page was built** — run `scripts/make_evs05.py` and `scripts/make_evs10.py`.
      `make_evs10.py` needs `piexif`.
- [ ] `CASE-01B` unzipped, **manifests included**.
- [ ] `xxd`, `file` and `exiftool` present. Windows fallback: `Format-Hex -Count 8`.
- [ ] Restore `CLEAN-TOOLS`. Say it out loud — third page running, third time it pays.
- [ ] **Do not pre-announce which files lie.** Five of the twelve do. Let them find it.

---

## 1 · The one sentence

> **The name of a file is a label someone typed. The bytes are the file.**

`P02` ended with a copy proven identical to its source. `T04` opens by asking the obvious next
question and letting it land: *identical to **what**, exactly?*

---

## `T04` — Inside a File · 82 min

### Bridge + theory · 20 min

**Bridge (3 min).** *"You can now prove your copy equals the source. Fine. Open it — what is it?
A file called `holiday_snap.jpg`. Is it a photograph?"*

**Hex (6 min).** Not a topic in its own right — a way of reading bytes. One byte, two hex digits,
values `00`–`FF`. Show `xxd -l 16` on anything and read the two panes: bytes on the left, the
printable interpretation on the right. **Both panes are the same bytes.** That is the whole idea,
and `FIG P03-D1` is built on it.

**Magic bytes (8 min).** The signature table, and the four that matter today:

| Bytes | Format |
|---|---|
| `25 50 44 46` | PDF — literally `%PDF` |
| `89 50 4E 47 0D 0A 1A 0A` | PNG |
| `FF D8 FF` | JPEG |
| `50 4B 03 04` | ZIP — and therefore `.docx`, `.xlsx`, `.odt`, `.jar`, `.apk` |

> **Say the last one properly.** A `.docx` *is* a ZIP. When they meet OOXML later they should
> already expect `50 4B`.

**What a rename changes (6 min).** Renaming rewrites a name string in the directory index and the
`$FILE_NAME` attribute. **It does not read, move or rewrite the clusters holding the content.** That
is the mechanism behind the entire lesson: the header survives because the header **is content**,
and the extension is not. `FIG P03-D2` walks it.

> INE asserts the outcome and never explains the mechanism. Say that you are adding it, and that
> they will meet clusters properly in `P08`.

---

### Guided practice · 18 min — `SIMSCREEN T04-1`

Full steps in `guided_lab.md`. Read one file's first bytes, then sweep all twelve.

**The key step is `thumbnail.png` returning `FF D8 FF E0`.** Stop there. Ask what they now know:

- The file's first bytes match the **JPEG** signature. That is all.
- **Not** "the file is a JPEG" — a signature is four bytes agreeing with a table, and four bytes are
  trivially forged.
- **Not** "someone renamed it to hide something" — that is motive, and there is none in evidence.

Then the sweep: **five of twelve disagree with their extension.** Real values, read from the set:

| Name says | First bytes say |
|---|---|
| `thumbnail.png` | `FF D8 FF E0` — JPEG |
| `holiday_snap.jpg` | `50 4B 03 04` — ZIP |
| `invoice_scan.jpg` | `25 50 44 46` — PDF |
| `meeting_notes.txt` | `89 50 4E 47` — PNG |
| `policy_v2.docx` | `89 50 4E 47` — PNG |

> **`policy_v2.docx` is the interesting one.** A `.docx` should be a ZIP — so its extension is
> wrong **twice over**, and a student who has understood the `50 4B` point will notice.

---

### Independent — `CASE-01B` · 40 min

The verification challenge, individually, at the keyboard. Brief in `student_activity.md`.

**Every result below was run against the real package during the build.** Do not paraphrase from
memory in class — project the terminal.

| Step | What they find |
|---|---|
| 1 | 2 files fail **both** manifests. **`policy_extract.txt` passes SHA-256 and fails MD5** — so one of the two manifests is itself wrong, which is a different problem from a changed file |
| 2 | `missing_statement.txt` is in the manifest, not in the folder. `extra_notes.txt` is in the folder, not in the manifest. **Opposite problems** |
| 3 | `photo_evidence.txt` passes both manifests and is a **PNG** — integrity intact, identity wrong |
| 4 | `access_log_excerpt.txt` fails, and `cat -A` shows one line with **trailing whitespace** where no other line has any |
| 5 | `duplicate_a.txt` and `duplicate_b.txt` share a digest — the same content twice under two names |

**The two to press hardest on:**

**Step 1's split result.** Most will report "one file failed". Ask which manifest. A file that
passes one algorithm and fails the other **cannot have changed** — a changed file fails both. So the
finding is about the *manifest*, not the file. This is the sharpest moment on the page.

**Step 2's asymmetry.** Ask which is more serious. The missing file is worse: something the sender
listed is not here, and you cannot examine it. The extra file is a documentation gap. Both go in the
report; only one blocks the examination.

> **What they must not write.** For a failing file you can prove **that** it changed. You hold no
> clean copy, so you cannot say **what** changed. *"The timestamp was altered from X to Y"* is an
> invention. The correct sentence is in `report_stage.md`, and it is the point of the exercise.

---

### Report stage · 4 min

**Section 6 Tools and method** — the first real rows. Tool, version, what it was run on, what it
produced. If another examiner cannot repeat it from that table, it is not a method.

---

## `T05` — Data Representation & Metadata · 35 min

### Bridge + theory · 12 min

**Bridge (2 min).** *"You can say what a file is. Now: what does it say about **itself**?"*

**Endianness (6 min).** The order a multi-byte **value** is stored in. `00 10 00 00` little-endian
is `0x00001000`, not `0x00100000`. `FIG P03-D5` shows the same four bytes read both ways.

> **The distinction they trip over, so say it explicitly:** a signature like `FF D8` is a byte
> **pattern**, read left to right. A field like a PE `TimeDateStamp` is a **value**, and its byte
> order matters. Pattern versus value. INE never defines endianness at all; you are adding it
> because nothing in `P08`'s PE tables can be read without it.

**Encodings (2 min).** ASCII, then UTF-8 and UTF-16LE. Windows internals are full of UTF-16LE —
which is why a string search for `svchost` misses it unless the tool knows.

**EXIF (2 min).** Metadata the camera writes, and that **every piece of software afterwards can
rewrite**. `FIG P03-D6`.

---

### Guided practice · 10 min — `SIMSCREEN T05-1`

`office_floor3.jpg` from `EVS-10`. Real values:

```
GPSLatitude       30 deg  2' 27.60" N
GPSLongitude      31 deg 14' 13.20" E
DateTimeOriginal  2026:08:24 09:14:02
DateTime          2026:08:31 16:40:05
Software          MRG ImageTool 2.4
```

**The key step is the two timestamps.** They are a week apart, and they record different events:

- `DateTimeOriginal` — when the **shutter fired**, written by the camera.
- `DateTime` — when the file was **last modified**, rewritten by whatever touched it.

So the disagreement is not evidence of tampering. It is evidence that **software opened this file on
31 August** — and `Software: MRG ImageTool 2.4` names it.

> **Then take it away from them.** Every one of those fields is ordinary editable data. GPS in a
> photograph is a **claim by the camera**, not a fact about the world. It is excellent lead
> material and it is not proof of location.

---

### Independent · 9 min

Three images, three questions (`student_activity.md`). The one that matters is `team_photo.jpg`:
**it has no EXIF at all.**

Students reliably report an empty result as *"the tool did not work"*. It is a finding:

> `team_photo.jpg` contains no EXIF block. The absence is consistent with a camera that writes none,
> with software that stripped it, or with a file that was re-encoded. **Which of these applies
> cannot be determined from the file alone.**

That sentence is worth more than the two images that do have GPS.

---

### Report stage · 4 min

**Section 8 Findings** — first entries. Each tied to a named file at an exact path, each stating a
measurement. This is where `T04` and `T05` become the report.

---

## Where students reliably go wrong on this page

| What they do | What to say |
|---|---|
| "The file is a JPEG" | Its first bytes match the JPEG signature. Four bytes are trivially forged. |
| "Someone renamed it to hide it" | That is motive. Where is it in evidence? |
| Report "one file failed" in Case 01 | Which manifest? A file that passes one and fails the other did not change. |
| "The timestamp was altered from X to Y" | You have no clean copy. You can prove *that* it differs, not *what* differs. |
| "The photo was taken at these coordinates" | The camera **recorded** those coordinates. Both are editable. |
| "exiftool returned nothing, it did not work" | It worked. There is no EXIF. **Write that down.** |

---

## If you are running short

1. Endianness drops to the one-line pattern-versus-value distinction.
2. Case 01 drops steps 4 and 5 — keep 1, 2 and 3.
3. **Never cut Case 01 step 1, or `team_photo.jpg`.** Those are the page.

---

## Bridge to `P04`

*"Everything so far has been a file sitting still on a disk. `P04` goes somewhere the file is not:
memory, where the evidence disappears the moment the power does."*
