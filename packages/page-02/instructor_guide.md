# P02 · Instructor guide — Evidence integrity

Page `P02` · topic `T03` · **38 topic minutes** · evidence `EVS-01` (Tier 1, verified).
Design frozen by `D109`. Outline approved: `design/P02_outline.md`.

Source: `knowledge_base/Module_01_Data_Acquisition.md` sections 1 and 2 ·
`knowledge_base/instructor/Session_01` · `knowledge_base/thm/forensic-imaging.md`.

---

## 0 · Pre-class checklist

- [ ] `EVS-01` unzipped on every student machine at `C:\Forensics\Cases\ITG-2026-014\EVS-01\`.
- [ ] **Do not tell them one file will fail.** The whole lab turns on that surprise.
- [ ] `Get-FileHash` available (built in, PowerShell 4+). No install.
- [ ] The two INE slides ready to show side by side: `[U2 p143]` and `[U2 p144]`.
- [ ] Your own `CLEAN-TOOLS` snapshot from `P01` restored, so you demo from a known state —
      and **say that out loud**, because it is `P01`'s lesson being used, not repeated.

---

## 1 · The one sentence this page turns on

> **A matching hash proves the copy equals the source as read at that moment — and nothing else.**

Everything else on the page is a consequence. Students arrive believing a hash "proves the evidence
was not tampered with"; most have said it in an interview. **INE's own slide says it too**
(`[U2 p143]`), and corrects itself one slide later (`[U2 p144]`).

**Show them both slides.** Not to score a point off INE — to make the real point: *a respected
source stated it loosely, and you still have to be able to say what is actually true.* A student who
never sees an authority be imprecise learns to trust authorities instead of evidence, which is the
opposite of this course.

---

## `T03` — Evidence Integrity · 38 min

### Bridge + theory · 13 min

**Bridge (2 min).** *"Last page you signed that your platform was in a known state. You can name
the snapshot. Now the evidence arrives — and you cannot snapshot someone else's disk. So what can
you actually prove about it?"*

**What a hash is (5 min).** One-way, fixed-length, avalanche. Do the demo live, do not describe it:

```powershell
"H" | Set-Content -NoNewline t.txt ; Get-FileHash t.txt -Algorithm SHA256
"h" | Set-Content -NoNewline t.txt ; Get-FileHash t.txt -Algorithm SHA256
```

One bit of difference, two digests with nothing in common. **Never quote a digest from a slide** —
the INE deck's are truncated by OCR (`[U2 p146–150]`), and a value on a page is not a value you
computed. Generate it in front of them.

**The four not-proves (5 min).** These are the substance. Do **not** lecture all four — state them,
one line each, and let the independent exercise do the teaching:

| # | A matching hash does not prove | The one-line reason |
|---|---|---|
| 1 | the acquisition was **complete** | an HPA excluded from the read is excluded from *both* hashes, so they match perfectly |
| 2 | a mismatch means **tampering** | a failing sector, a cable fault, or an SSD's own garbage collection between two reads all mismatch with nobody at fault |
| 3 | **authenticity or provenance** | it says the copy equals the source; it says nothing about *which drive this is* or where it came from |
| 4 | anything, **if the attacker held both** | someone with the disk and the hash file simply recomputes. `[U2 p144]` — INE's own correction |

**Where authenticity actually lives (3 min).** Not in the image. In two records: the **chain of
custody**, and the **write-block proof trail**. Both are documents you write; neither can be
recovered later if you did not write them at the time.

> **The line to land here:** an image taken on a write blocker and an image taken without one are
> **byte-identical**. There is no field in the file. So "I used a write blocker" is a claim that
> lives or dies entirely on your paperwork.

---

### Guided practice · 12 min — `SIMSCREEN T03-1`

Full steps in `guided_lab.md`. Run it with them, on your machine, projected.

**The lab has one surprise and you must not spoil it.** They verify four files. Three say `OK`.
One says `FAILED`. Watch the room — someone will say *"it's been tampered with."*

**That is the moment the page exists for.** Do not correct it immediately. Ask: *"What did the
command actually compare?"* Walk them to: **the file differs from what the manifest recorded. That
is all I know.** Not what changed. Not when. Not why. Not by whom.

Then open the file and diff it against the manifest's expectations. The difference is **one
second** in a timestamp: `09:14:02` → `09:14:03`.

Land it hard:

> **A one-second edit and a total file replacement produce the same `FAILED` line.**
> The hash tells you *that* something differs. It never tells you *how much*.

---

### Independent · 9 min — they judge, you do not tell

**(a) The five-scenario sort · 4 min.** Five one-line scenarios, each with a hash result, sorted
into three buckets: *integrity intact · integrity broken · cannot tell from this*. Full text in
`student_activity.md`.

The bucket that matters is the third. Most students will not use it at all on the first pass —
that is the finding, and it is worth naming to the room: *"Four of you used 'cannot tell' zero
times. In a report, that bucket is where honesty lives."*

**(b) The defect hunt · 5 min.** Show TryHackMe's **Forensic Imaging** room, Task 4 and Task 5, one
after the other. Task 4 computes an MD5 and confirms it matches. Task 5 runs:

```bash
sudo mount -o loop example1.img /mnt/example1
```

Ask one question: **"What just happened to the hash you verified on the previous page?"**

A read-write `ext4` mount writes to the image: mount count, mount time and `s_last_mounted` go
into the superblock; `relatime` updates the atime of every file older than a day the moment the
directory is listed; and a dirty image has its journal replayed. **The verified hash is now
wrong, and the room never re-checks it.** 18,481 people have completed that room.

The correct command, and the one they will use for the rest of the course:

```bash
sudo mount -o ro,loop,noload example1.img /mnt/example1
```

> **Say this plainly:** the room is not bad. Its Task 2 audit trail — seven bash settings plus
> session recording with `script` — is the best thing in fourteen rooms we reviewed, and nothing
> else teaches an examiner to log *themselves*. A source can be worth using and wrong in one place.
> Being able to tell which is which is the skill.

---

### Report stage · 4 min

`report_stage.md` has the student-facing text. They fill **Section 4 Chain of custody** and
**Section 5 Evidence received** for `EVI-SRC01`, transcribing from the `EVS-01` forms.

Two things to insist on:

1. **Both digests, always.** MD5 *and* SHA-256. MD5 and SHA-1 are broken for collision resistance
   (`[U2 p145]`); recording both means a challenge to one does not sink the exhibit.
2. **The hash goes somewhere the exhibit is not.** `[U2 p144]`. The `EVS-01` custody form models
   it: *"value recorded in the examiner's notebook, page 41, stored separately from the exhibit and
   separately from the image."* If the hash travels with the disk, it protects nothing.

These are the two sections rubric **criterion 1 (Integrity)** grades. Say so.

---

## Where students reliably go wrong on this page

| What they do | What to say |
|---|---|
| Read `FAILED` as "tampered" | *"What did the command compare? Say only that."* |
| Read `OK` as "this is the suspect's disk" | It equals what the manifest recorded. Provenance is the custody form's job, not the hash's. |
| Record one digest | Both. Always. `[U2 p145]`. |
| Store the hash beside the image | Then anyone who can edit the image can edit the hash. `[U2 p144]`. |
| Say "I used a write blocker" and stop | Where is it written? Which make, model, serial? Photograph? The image cannot tell anyone. |
| Trust FTK Imager's `verified` line | That is the tool checking its own write-then-read round trip. It never re-read the source. The `EVS-01` acquisition log states this explicitly — make them read that note aloud. |
| Set `WriteProtect` and not reboot | Windows writes to the evidence, and the report says "software write blocked". Always demonstrate the block on a scratch stick first. |

---

## If you are running short

Cut in this order:

1. The `WriteProtect` registry screen (screen 11 static) — mention it, move on.
2. The five-scenario sort drops from five scenarios to three (keep #2 and #4 — they are the two
   "cannot tell" cases).
3. **Never cut the `FAILED` beat or the report stage.** Those are the page.

---

## Bridge to `P03`

*"You can now prove a copy equals its source. `P03` asks a harder question: the copy is identical —
but what is actually **in** it? A file says it is a `.jpg`. Who says?"*
