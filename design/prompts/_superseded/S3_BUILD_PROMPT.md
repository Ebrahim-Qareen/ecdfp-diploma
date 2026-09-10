# BUILD PROMPT — Session 3 · Data Representation, Hidden Information & File Examination

**Read `design/prompts/SHARED_RULES.md` first. Everything in it is binding.**
Project root: `E:\Work\ITgate\ECDFP_Course`. Output: `docs/session-03/index.html`.

This is the **densest visual session in the course**. Every single block is something you can put
on screen as bytes, pixels or structure — there is almost no abstract theory in it. If any page
here reads as prose, you have built it wrong.

---

## 1 · The spine

> **A file's name is a claim. Its bytes are the evidence. What is the file really, and what is
> hiding inside it?**

**The hook (page 4).** Twelve files were exported from the suspect's workstation. The export log
lists them by name and the investigator before you accepted that list.

- **five of the twelve names are lying**
- **two files have a valid header and a broken body**
- one image carries a hidden payload; its clean twin sits beside it
- one "redacted" scan is **not** redacted — its EXIF thumbnail outlived the redaction

The claim on trial: *"the export list tells us what was taken."* Blame the conclusion, never a person.

---

## 2 · ✅ Evidence — TWO SETS ARE BUILT AND VERIFIED. USE THE REAL VALUES.

Unlike Session 2, this session is **not** blocked. Read `design/evidence_sets.md` and use the
published SHA-256 values verbatim — **never invent a hash**.

### `EVS-05` — 12 files whose extensions are unreliable ✅ verified 2026-09-06
Generator `scripts/make_evs05.py`. 12 892 B total.

| File | Claims | Actually is | First 4 bytes |
|---|---|---|---|
| `q3_summary.pdf` · `floorplan.png` · `badge_photo.jpg` · `archive_2026.zip` · `readme.txt` | — | honest | — |
| `invoice_scan.jpg` | JPEG | **PDF** | `25 50 44 46` |
| `meeting_notes.txt` | text | **PNG** | `89 50 4E 47` |
| `holiday_snap.jpg` | JPEG | **ZIP** | `50 4B 03 04` |
| **`policy_v2.docx`** | ZIP *(a .docx **is** a ZIP)* | **PNG** | `89 50 4E 47` |
| `thumbnail.png` | PNG | **JPEG** | `FF D8 FF E0` |
| `scan_partial.png` | PNG | PNG, **truncated** | valid header, dead body |
| `export_partial.jpg` | JPEG | JPEG, **truncated** | valid header, dead body |

🟢 **`policy_v2.docx` is the best file in the whole course — build a page moment around it.** A
student who learned *"a .docx is really a ZIP"* will confidently predict `50 4B 03 04` and be
**wrong**. It punishes pattern-matching and rewards looking. Make them predict out loud first.

🟢 **The two truncated files are the second lesson:** a valid signature does **not** mean a valid
file. Header and integrity are different questions — that is the bridge back to `S1-06` hashing.

### `EVS-10` — the hidden-information image set ✅ verified 2026-09-06
Generator `scripts/make_evs10.py`. 46 402 B, 7 files.

| # | File | The lesson it carries |
|--:|---|---|
| 1 | `office_floor3.jpg` | EXIF GPS + **three disagreeing timestamps** — `DateTimeOriginal` 2026:08:24 ≠ `DateTime` 2026:08:31 ≠ mtime 2026:09:02 |
| 2 | `receipt_scan.png` | LSB payload in the **blue channel** |
| 3 | `receipt_scan_clean.png` | the same image **without** the payload — **diff the two** |
| 4 | `team_photo.jpg` | a valid JPEG **and** a valid ZIP — a polyglot |
| 5 | `meeting_notes.txt` | is really a PNG |
| 6 | `holiday_snap.jpg` | is really a ZIP |
| 7 | `invoice_batch.jpg` | main image redacted; **the EXIF thumbnail is not** |

🟢 **Files 2 and 3 are a gift** — the clean twin means students *see* the noise instead of being
told about it. Build the whole stego block on that diff.

### ⛔ `EVS-06` does not exist — and this is your one real constraint

`EVS-06` (the malicious document and the executable it drops) has **no section in
`evidence_sets.md`**, because it was to be carved out of `EVS-02`, which is not yet acquired.
It is needed by `S3-04`, `S3-05` and the page-17 investigation.

**What to do — do NOT stall the session:**
1. Build pages 13 and 14 in full, teaching **structure**, on a **Tier 3 sample you author**: a
   `.docm` with a visible macro and one embedded object, and a small **benign** PE you compile.
   The Tier 3 bar forbids fabricating `.evtx`, E01/AD1/raw, memory dumps and registry hives — it
   does not forbid authoring a document or compiling a hello-world binary. `EVS-10`'s own header
   makes exactly this argument; follow it.
2. Page 17's investigation keeps its full structure, steps and verification lines, with every
   value that must come from the real carry-through artefact marked in a visible `.caveat`.
3. **Never invent a hash, a size or tool output for `EVS-06`.**
4. Say plainly in your report which pages are provisional.

---

## 3 · The blocks — 130 taught + 60 investigation + 15 close

Teaching order. **The image thread runs first and completely, then the document/executable
thread.** Do not interleave them — that was a defect corrected on 2026-09-06.

| Page | Block | ID | Min | The visual this block IS | Practical inside the block |
|--:|---|---|--:|---|---|
| 5 | How data is represented — endianness, encodings | `S3-01` | 10 | **ANIMATE:** the same 4 bytes read little- vs big-endian giving two different numbers | convert one value both ways, by hand |
| 6 | **Metadata and EXIF** — GPS, and timestamps that disagree | `S3-02` | 25 | `.gui` `exiftool office_floor3.jpg` · a 3-row timeline of the three conflicting dates | run exiftool, state which date you trust and **why** |
| 7 | **Image forensics** — ThumbCache, the thumbnail that outlived the edit | `S3-06` | 12 | **ANIMATE:** main image redacts, embedded thumbnail stays | extract the thumbnail from `invoice_batch.jpg` |
| 8,10 | **Hidden data** — LSB stego · embedded & appended files · polyglots · **detection** | `S3-03` | 33 | **ANIMATE:** LSB — the low bit flips, the pixel does not visibly change · `.gui` `binwalk team_photo.jpg` | diff files 2 and 3; carve the ZIP out of the polyglot |
| 13 | **Malicious document structure** — OLE vs OOXML, embedded objects, macros | `S3-04` | 25 | **ANIMATE:** a `.docx` unzipping into its parts, `vbaProject.bin` lighting up | rename to `.zip`, unzip, find the macro |
| 14 | 🆕 **Executable analysis** — PE headers, imports, sections, resources, strings | `S3-05` | 25 | PE layout map (DOS stub → PE hdr → sections) · `.gui` `strings` + import list | read 3 imports, say what the binary can do |
| 16 | **Case 03** — 12 files, one hidden payload | `S3-07` | 35 | brief + exhibit table, **no prose** | identify all 12 by bytes; find the payload |
| 17 | The carry-through malicious document | `S3-08` | 25 | ⛔ needs `EVS-06` | structure → embedded object → macro |
| — | Hash-verify + custody close | `S3-09` | 15 | `.coc` | re-hash, sign, store read-only |

**Why this order.** EXIF → thumbnails → hidden data is **one continuous thread about images**, and
`invoice_batch.jpg` is the hinge: its EXIF *is* metadata (block 6) and its surviving thumbnail *is*
image forensics (block 7). Documents and executables are a second thread, and `S3-05` reads the
binary that `S3-04`'s document drops. Two threads, each finished before the next starts.

---

## 4 · The four animations (`D51` — click-to-play, no autoplay, no loop)

1. **Endianness (p5).** Four bytes sit in a row. On play, read-order arrows sweep left-to-right
   and right-to-left, and two different decimal values resolve underneath. One picture kills a
   topic that is otherwise pure hand-waving.
2. **The surviving thumbnail (p7).** The main image visibly blurs/blacks out under a redaction
   box while the small embedded thumbnail beside it **stays sharp**. Caption: *the redaction
   edited the picture, not the file.*
3. **LSB (p8).** Zoom to one pixel. On play its **lowest bit** flips 0→1 while the rendered colour
   swatch beside it does not perceptibly change; a payload bit counter ticks up. Then the diff view
   of files 2 and 3 reveals the noise pattern.
4. **The document unzipping (p13).** A `.docx` opens into its OOXML parts;
   `word/vbaProject.bin` cross-fades to the alert colour and the tree settles.

Cross-fade shapes for colour change — **SMIL cannot interpolate `var()`**; animating `fill` to a
token renders **white**.

---

## 5 · What Sessions 1 and 2 own — name it, never re-explain it

| Idea | Owned by | What you may do |
|---|---|---|
| hex reading, magic bytes, "renaming changes nothing" | **`S1-09`** | **use it hard**; do not re-teach what a magic byte is |
| the magic-byte reference table | `S1-09` cheat sheet | reprint it in your cheat sheet only |
| signature vs extension as a sweep | **`S2-06`** | you go **deeper**: the *subtle* mismatch (`policy_v2.docx`) and the *damaged* file |
| hashing / `sha256sum -c` | `S1-06` | verify `EVS-05` and `EVS-10` at the start; one clause |
| chain of custody, write blocking, the report template | `S1-07/08/04` | apply, never restate |
| order of volatility, imaging, `verified` | `S2` | not this session at all |

🔴 **The specific trap here:** S1 and S2 both already taught "the extension is a label". If your
page explains that again, you have burned 10 minutes. Your job is the **next** layer — *the file is
not what it says, AND something is hidden inside it that no extension check will ever find.*

---

## 6 · The previous instructor's Session 2 deck — what to take, what to fix

Source: `knowledge_base/instructor/Session_02_Data_Representation_and_File_Examination.md`.
This was one of his **stronger** decks. Read it properly.

**Take:**
- **His EXIF-GPS challenge** (slide 20) — a photo, find the city. Rebuild it on `office_floor3.jpg`,
  which has GPS *and* the three-timestamp conflict, so one exercise now teaches two things.
- **His HxD raw-view signature walkthrough** (slides 21–23) — the manual read before the tool.
  Keep the shape; regenerate the screens (see PII below).
- **The Gary Kessler signature table** as a named, citable reference students keep.
- **His identify-the-extension challenge** (slide 24) — this is exactly `EVS-05`, now with hashes
  and a generator instead of a shared-drive link.

**Fix — these are not optional:**
- 🔴 **PII in his screenshots.** Slides 21, 22, 25–32 leak his own profile path, working tree,
  physical drive models, an FTK case path and **a real Windows SID**. **Never reuse those images.**
  Every screen in your page is a `.gui` panel or a screen regenerated on the course lab.
- 🔴 **Two graded tasks depended on Google Drive links** (slides 20, 24) — single points of failure,
  probably already dead. Both are replaced by `EVS-05`/`EVS-10`, in-repo and hashed.
- 🔴 **He used Xiao Steganography** (slides 33–36) — **no vendor, no licence**. This is why stego
  was dropped from the roadmap once already. Use `steghide`, `zsteg`, `stegsolve`, `binwalk`.
- ❌ **His Recycle Bin `$I`/`$R`, TestDisk partition repair and PhotoRec carving belong to S4 now.**
  Do not pull them into S3 — that is where the ~40 minutes for the malicious-document block came
  from. Reference forward in one clause at most.
- ❌ **He taught no malicious-document structure at all.** INE covers it across ~120 pages
  (`3.7.1` DOCX, `3.7.3` PDF, `3.7.4` EXE). **Pages 13 and 14 are the largest single gap in his
  material and the reason this session was re-cut. Build them properly.**

---

## 7 · Questions — the "cannot be determined" one is chosen for you

Exactly one per session (`D60`). For S3 it is the timestamp conflict on `office_floor3.jpg`:

> *Three timestamps disagree. Which one records when the photograph was actually taken?*
> **Cannot be determined from this file alone.** `DateTimeOriginal` is what the camera wrote and is
> the best candidate, but EXIF is user-writable, `DateTime` records a later edit, and mtime records
> a copy. Naming `DateTimeOriginal` as *proof* is the wrong answer; naming it as the **best
> available indicator, with its limitation stated**, is the right one.

That question is the whole session's thesis in one item. Put it in Knowledge check 2.

---

## 8 · What Session 4 will need from you

S4 is *Storage Devices, Partitions & File Systems* — sectors, clusters, slack, MBR, GPT, FAT, NTFS,
`$MFT`, and **carving**. It inherits from you:
- **file signatures**, which is what carving searches for — say explicitly that carving is
  "signature matching across unallocated space", so S4 opens on ground you prepared
- **the truncated files** — S4 explains *why* a file can be half there

End page 22 pointing at it: *you have read files. Now find the ones that were deleted.*

---

## 9 · Done means

```
python3 scripts/density_gate.py docs/session-03/index.html     → ALL PASS
node testing/render_gate.js docs/session-03/index.html         → zero findings, 5 widths
```
Report as numbers: total words, worst page, pages without a visual, animations built, **that no
animation autoplays**, and **which pages are provisional pending `EVS-06`**.
