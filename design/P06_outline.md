# P06 outline — Hidden information

**OUTLINE GATE (`D9`).** Page `P06` · **80 topic minutes** · one topic, `T10` Hidden Data & Image
Forensics. Evidence **`EVS-10`** and **`EVS-05`** — both verified `2026-09-06`, both regenerated and
re-read for this build. Design frozen by `D109`; diagrams stepped per `D115`.

**This page asks for three decisions** (Section 8). It invents nothing locally.

Sources: `knowledge_base/Module_02_Data_Representation_and_File_Examination.md` §1 *Data hiding
locations* `[U3 p107–126]` and §2 *File trailer and data past the end* `[U3 p4, p61, p149]` ·
`knowledge_base/Module_04_System_and_Network_Forensics.md` §2A *Thumbcache and Thumbs.db*
(`6.3.2`) · `design/tools_by_session.md` S3.

---

## 0 · Evidence gate — PASS

`EVS-10` was regenerated on a **third independent machine** for this build. All seven SHA-256 values
are byte-identical to the manifest in `design/evidence_sets.md`. `EVS-05` is verified and unchanged.

Every number on this page below is a **measurement taken from those files**, not an illustration.

### What was measured, and where it lands

| Reading | Value | Screen |
|---|---|---|
| `invoice_batch.jpg` EXIF thumbnail | offset **266**, length **1735 bytes**, image **160 × 107** | 11 · 12 |
| its main image | **600 × 400**, redaction rectangle `[180,150 – 470,250]` = **29 391 px** blacked | 12 |
| the same region **in the thumbnail** | **2 184 px**, of which **0** are redacted | 12 |
| `receipt_scan.png` LSB payload | `MRG-INTERNAL: staged archive is customer_export.7z` — **50 chars = 400 bits** | 15 · 16 |
| stego twin vs clean twin | **190 of 76 800 px differ = 0.247 %**, **blue channel only**, every delta **±1** | 17 |
| the two twins' file sizes | clean **2 970 B** · stego **3 231 B** — the hidden copy is **261 B LARGER** | 17 |
| `team_photo.jpg` | **10 476 B**. JPEG `FF D9` at **10 294** · ZIP local header at **10 296** · central directory **10 396** · EOCD **10 454** | 19 · 20 |
| its appended entry | `handover.txt`, **58 B**, stored (not compressed) | 20 |
| `file team_photo.jpg` | reports **JPEG only** — the ZIP is invisible to it | 20 |
| `unzip -l team_photo.jpg` | `warning: 10296 extra bytes at beginning or within zipfile` — **the warning is the finding** | 20 |

> **The sharpest reading on the page is the size one.** A student expects a file carrying a hidden
> message to be the same size — the pixels only changed by ±1. It is **8.8 % bigger**, because LSB
> noise destroys the flat runs that PNG compresses. The picture is identical and the *file* is not.

> **The second sharpest is the shortfall.** 50 characters is 400 bits, but only **190** pixels moved.
> Roughly half the LSBs already held the bit that was written. A student who predicts 400 has
> understood the encoding and not the medium.

---

## 1 · The one sentence this page installs

**A file shows you one thing and stores several. What a viewer draws is not what the file contains.**

`P03` taught that the bytes are the file, not the name. `P06` is the next turn of the same screw: you
have now read the bytes the *format* declares — and the format is not obliged to declare all of them.

---

## 2 · Where this sits against `P03` — no screen is a repeat

`P03` already spent 117 minutes on `EVS-05` and `EVS-10`. Everything below is checked against it.

| `P03` taught | `P06` does NOT re-teach | `P06` adds |
|---|---|---|
| magic bytes; the 12-file signature sweep; the 5 liars | the sweep, the table, the `policy_v2.docx` trap | the sweep returns **only as Case 03 warm-up**, done by the student, not shown |
| `office_floor3.jpg` — GPS and two disagreeing timestamps | EXIF timestamps, GPS | — |
| `team_photo.jpg` — **no EXIF block; the absence is finding F-04** | that finding | **the same file is also a valid ZIP.** P03's finding stays true and was never the whole file |
| `invoice_batch.jpg` — used once, as an EXIF exercise question | its timestamps | **its EXIF thumbnail, which survived the redaction** |
| — | — | `receipt_scan.png` / `receipt_scan_clean.png` — **untouched by every earlier page** |

**`team_photo.jpg` is the payoff of the page.** Students met it three pages ago, ran `exiftool` on it,
got nothing, and correctly recorded an absence. P06 shows that the file they closed had 180 bytes
after its end. Nothing they wrote was wrong — they had answered the question they asked.

---

## 3 · Scope, and one honest note about the source

`T10` = 80 min, domain **Tools & Techniques 68 / Fundamentals 12**, prerequisites `T05` · `T09`.

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory (image forensics)** | 7 | Bridge from `T05`: *you read what the file says about itself. Now: what does it keep that it never shows you?* The anatomy of an image file (2) · the EXIF thumbnail as a second copy (2) · ThumbCache, the copies outside the file (2) · what a photograph cannot establish (1). |
| **Guided practice** | 5 | `SIMSCREEN T10-1` — extract the thumbnail from `invoice_batch.jpg` and put it beside the picture. **Key step: the `-b` flag** — without it ExifTool prints a description of the thumbnail instead of the thumbnail. |
| **Theory (hidden data)** | 21 | Three places data hides (3) · LSB steganography, what it is and how a message becomes bits (7) · detecting it with and without a reference copy (6) · data past the trailer, and the polyglot (5). |
| **Guided practice** | 12 | `SIMSCREEN T10-2` — HxD on `team_photo.jpg`: search hex `50 4B 03 04`, read the offset off the status bar, compare it to the file length. **Key step: reading the offset**, because "near the end" is not a finding. |
| **Independent — CASE 03** | 27 | Twelve renamed/corrupted files and one hidden payload. `EVS-05` + `EVS-10`. |
| **Report stage** | 8 | **Section 8 Findings** — the first entries that are *measurements of concealment*; **Section 10 Limitations** — this page produces more limitation rows than any page so far, and that is the point. |

**Theory 28 / 80 = 35 %.** Hands-on 52 / 80 = 65 %.

> ⚠ **INE does not teach steganography.** `Module_02` records it: unit 3 *"names steganography and
> covert channels in network protocols and explicitly defers them"* `[U3 p123]`. The appended-data
> half **is** INE's — it opens the unit with a PNG carrying a hidden ZIP `[U3 p4]` and covers the
> trailer at `[U3 p61, p149]`. So the LSB block is **ours, under `D81`** (scope goes beyond the
> certificate), and the outline says so rather than implying INE backs it. If `D81` is not meant to
> stretch this far, cut screens 15–18 to one and the page becomes 68 minutes.

---

## 4 · The screens — 30, five dividers

| # | Title | Tag | Min | Hands-on | Figure | Evidence |
|--:|---|---|--:|:-:|---|---|
| 1 | Cover | — | — | | — | — |
| 2 | Where we are | — | — | | `dg-lc-p06` lifecycle | — |
| 3 | What you will be able to do | — | — | | — | — |
| **4** | **PART 1 — What a picture carries besides the picture** | divider | **7** | | 4 screens | |
| 5 | What is inside an image file? | theory | 2 | | `P06-D1` · pattern 1·5 | `invoice_batch.jpg` |
| 6 | What is an EXIF thumbnail? | theory | 2 | | `P06-D2` · pattern 1·2 | `invoice_batch.jpg` |
| 7 | ThumbCache — the copies Windows keeps | theory | 2 | | `P06-D3` · pattern 1·4 | ⚠ concept only |
| 8 | What a photograph does not prove | limits | 1 | | `P06-D4` · `.cmp` reveal | — |
| **9** | **LAB TIME** | divider | **5** | | 3 screens | |
| 10 | Lab objectives | lab | — | ✓ | — | — |
| 11 | Extracting the thumbnail | lab | 3 | ✓ | **`SIMSCREEN T10-1`** | `invoice_batch.jpg` |
| 12 | The thumbnail against the picture | finding | 2 | ✓ | `P06-D5` · pattern 2·6 | 29 391 px / 2 184 px |
| **13** | **PART 2 — Data hidden inside and behind a file** | divider | **33** | | 8 screens | |
| 14 | Three places data hides | theory | 3 | | `P06-D6` · pattern 2·3 | — |
| 15 | What is LSB steganography? | theory | 4 | | `P06-D7` · pattern 1·6 | `receipt_scan.png` |
| 16 | How a message becomes bits | theory | 3 | | `P06-D8` · pattern 5 | 400 bits |
| 17 | Detecting it — with a reference copy | finding | 4 | ✓ | `P06-D9` · pattern 2·6 | 190 / 76 800 · 261 B |
| 18 | Detecting it — without one | limits | 2 | | `P06-D10` · `.cmp` reveal | — |
| 19 | What is data past the end of a file? | theory | 3 | | `P06-D11` · pattern 1·5 | `team_photo.jpg` |
| 20 | What is a polyglot? | theory | 2 | | `P06-D12` · pattern 2 | `file` vs `unzip -l` |
| 21 | Finding it in a hex editor | lab | 12 | ✓ | **`SIMSCREEN T10-2`** | offset **10 296** |
| **22** | **ON YOUR OWN** | divider | **27** | | 3 screens | |
| 23 | Case 03 — the brief | case | — | ✓ | exhibit table | `EVS-05` · `EVS-10` |
| 24 | Case 03 — what a good answer looks like | case | — | | `P06-D13` · F/I/L encoding | — |
| 25 | Knowledge check | quiz | — | ✓ | MCQ component | — |
| **26** | **REPORT STAGE** | divider | **8** | | 4 screens | |
| 27 | Section 8 — findings | report | 3 | | `P06-D14` · pattern 5 | — |
| 28 | Section 10 — limitations | report | 3 | | `P06-D15` · pattern 5 | — |
| 29 | Summary — what you can now state | — | 2 | | — | — |
| 30 | Cheat sheet and homework | — | — | | — | — |

**Totals: 7 + 5 + 33 + 27 + 8 = 80 min.** 30 screens · **5 dividers** · `is-part` on those five only.
Teaching screens carrying a figure: **21 of 21.**

---

## 5 · The figures

Fifteen stepped figures (`dgm.js`, `D115`) and two `SIMSCREEN`s. **No photographs on this page** —
`D93` requires that a picture earn its place, and a photograph of a camera or a disk would be exactly
the decoration two HDD images were removed from `P01` for being.

| Figure | Pattern | Shows | Steps |
|---|---|---|--:|
| `dg-lc-p06` | — | lifecycle, **3 · ANALYSE**, plus the analysis ladder (Section 8, decision 1) | 5 |
| `P06-D1` | 1 · 5 | **The anatomy of one JPEG** — `FF D8` · APP1/EXIF · IFD0 tags · **IFD1 = the thumbnail at offset 266, 1735 B** · pixel data · `FF D9`. Real offsets from `invoice_batch.jpg` | 6 |
| `P06-D2` | 1 · 2 | **One shutter press, two pictures** — 600 × 400 and 160 × 107 side by side, both written at the same moment, into the same file | 4 |
| `P06-D3` | 1 · 4 | **Where the other copies live** — the file · Explorer's `thumbcache_<size>.db` per user · the pre-Vista per-folder `Thumbs.db`. Steps walk *delete the picture → the cached copy is still there* | 4 |
| `P06-D4` | `.cmp` | **Four things a photograph does not establish** — who pressed the shutter · whether the clock was right · whether it was resaved · whether an absent field was removed or never written | 4 rows |
| `P06-D5` | 2 · 6 | **The redaction, twice** — main image with the black rectangle over 29 391 px, thumbnail with 0 of the corresponding 2 184 px covered | 3 |
| `P06-D6` | 2 · 3 | **Three places data hides** — in the pixel values · after the trailer · in a slot the format provides (EXIF comment, ZIP comment, ADS). One row lights at a time | 3 |
| `P06-D7` | 1 · 6 | **One pixel, one bit** — blue byte `58` → `59`, shown as `00111010` → `00111011`, with the rendered colour swatch beside it, visibly unchanged | 4 |
| `P06-D8` | 5 | **`M` becomes eight pixels** — `0x4D` = `01001101` accumulating across eight blue channels | 8 |
| `P06-D9` | 2 · 6 | **The two twins** — 76 800 px, 190 lit; and the size counter running `2 970 → 3 231` | 4 |
| `P06-D10` | `.cmp` | **What you can say without a clean copy** — three rows of claim vs what the evidence carries; the third resolves to *cannot be determined* | 3 rows |
| `P06-D11` | 1 · 5 | **The byte map of `team_photo.jpg`** — `0 … 10 294` JPEG, `FF D9`, then `10 296 … 10 476` ZIP. The whole bar is on screen from frame one; stepping lights each region | 5 |
| `P06-D12` | 2 | **Three tools, three answers** — `file` says JPEG · `exiftool` says JPEG · `unzip -l` says *10296 extra bytes* and lists `handover.txt` | 3 |
| `P06-D13` | 1 · 3 | **One observation, three sentences** — the same measurement written as a finding, as an interpretation, and as a limitation (`D7` colour encoding) | 3 |
| `P06-D14` | 5 | **Section 8 growing** — the report's twelve sections, 8 gaining its concealment rows | 3 |
| `P06-D15` | 5 | **Section 10 growing** — and why this page contributes more to it than any page before | 3 |
| **`SIMSCREEN T10-1`** | 11 | `exiftool -b -ThumbnailImage invoice_batch.jpg > thumb.jpg`, then open it. **Key step: `-b`** | 5 |
| **`SIMSCREEN T10-2`** | 11 | HxD → Search → Hex-values `50 4B 03 04` → read offset `10296` from the status bar → compare with the file length. **Key step: reading the offset as a number** | 6 |

Both `SIMSCREEN` step lists **are** `guided_lab.md`'s steps (`D96` rule 10) — one list, written once.

---

## 6 · Case 03 · 27 min

Bound to `T10` by `00_INSTRUCTIONS.md` Part 8. A **draft already exists** in the superseded
`packages/session-03/student_activity.md` and is good; it is carried forward with four changes.

**Kept:** the brief, the scope/authorisation framing, the named-in-advance `policy_v2.docx` trap,
Q1 hash verification, and Q7 as a limitation.

**Changed:**

1. **Time box 35 → 27 min**, because `D84` gives `T10` 80 minutes and the report stage is inside them.
2. **Q5 gets a method, not a wish.** The old Q5 said *recover the message and state the method*. The
   FOR-WS01 tool set has **no steganography tool** — `tools_by_session.md` §1.3 dropped Xiao and
   installed no replacement. Q5 now reads: *diff the two twins, state how many pixels differ, in
   which channel, and by how much; then extract the message with the supplied 6-line Python script.*
   Python 3 is installed by `scripts/install/00_bootstrap.ps1`, so this is derivable.
   **The honesty rule from `CASE-01B` is the reason** — never ask for what the student cannot derive.
3. **Q6 keeps the offset requirement** and it is now derivable two independent ways: HxD search, or
   the `unzip -l` warning. Both were run; both give `10296`.
4. **A new Q8, and it is the one that separates the class:** *`P03` recorded that `team_photo.jpg`
   has no EXIF block. Is that finding still correct?* The answer is **yes** — and a student who says
   "no, it was hiding something" has confused *the file has no EXIF* with *the file has nothing else*.

**Q7 stays exactly as written.** Nothing in a file's bytes records a person.

Answer key ships as `cases/case-03-hidden/answer_key.md` — gitignored by `/cases/*/answer_key.md`.

---

## 7 · The four things this page must not let slide

1. **A polyglot is not a broken file.** Both readers are correct. `team_photo.jpg` is a valid JPEG
   *and* a valid ZIP, and neither tool is malfunctioning when it reports only what it parses.
2. **"I found no hidden data" is a statement about a method, not about a file.** The only honest
   form is *"no appended data past the trailer, and no LSB anomaly against the reference copy."*
   Students will write the short version; the rubric's criterion 4 is where it costs them.
3. **A recovered thumbnail proves an image existed, not where it lived or that anyone looked at it.**
   `Module_04` is explicit: the modern thumbcache stores no original path, and the shell populates it
   as soon as a folder is viewed. This is the page's strongest criterion-4 trap.
4. **Concealment is not intent.** Every measurement here says *something is hidden*. None of them
   says *someone hid it deliberately*, and the difference is section 8 against section 9.

---

## 8 · Three decisions this page needs — none of them invented here

### `D126?` · The lifecycle marker cannot move for eight pages, so it needs a second axis

**The collision.** Part 9's contract says the `Where we are` stage *"must differ from the pages either
side of it"* (`D123`) — and `PAGE_BUILD_PROMPT.md` §2 assigns **3 · ANALYSE to `P06` through `P13`**.
Eight consecutive pages, one stage. `P06` differs from `P05` (ACQUIRE) and cannot differ from `P07`.

**Proposed.** `dg-lc-pNN` keeps the five stages and gains **one row underneath, inside ANALYSE**: the
analysis ladder — **file → disk → operating system → network → timeline** — with the page's rung
marked. `P06` sits on **file**; `P08`–`P09` on **disk**; `P10`–`P12` on **operating system**; `P13` on
**network**; `P14` on **timeline**. The marker then moves on every page, which is the only thing
`D123` actually wanted.

**Cost of not doing it:** eight pages whose orientation figure is identical, i.e. decoration.

### `D127?` · `EVS-05` and `EVS-10` have no published download route

**The gap.** `D18` requires students to pre-download each set and verify its hashes before class.
`D67` published `EVS-01` at `docs/session-01/` and settled that `R9` prohibits evidence **bytes** —
*image, memory dump, hive, raw pcap* — which is exactly the `.gitignore` byte-format list. **`.jpg`
and `.png` are not on it.** But `P03` shipped without publishing either set, and `docs/page-03/`
contains only `index.html`. **Two pages now depend on files students cannot get.**

**Proposed.** Publish both at **`docs/evidence/EVS-05/`** and **`docs/evidence/EVS-10/`** — keyed by
set, not by page, because two pages share them — each with its `.zip`, both manifests, and a link
from `P03`, `P06` and `docs/resources/evidence.html`. Tier 3, ours, 59 KB total, no PII, no
credential, no IP address (`D41`, `R8`).

### `D128?` · The superseded `session-NN` tree is still shipping

`docs/session-01/`, `session-02/`, `session-03/` and `packages/session-01..03/` are the pre-`D84`
build. `PAGE_BUILD_PROMPT.md` §10 says *the folder holds one current version of everything*, and
`docs/session-03/index.html` currently publishes a **Case 03 that P06 is about to replace** — two
live answers to the same case. The mount cannot delete. **Proposed:** Ebrahim removes the six folders
in Explorer, and `docs/session-01/`'s `EVS-01`, `CASE-01B` and `report_template.md` move to
`docs/evidence/` and `docs/page-02/` first, since `D67` made them live links.

---

## 9 · Currency check (Part 9) — done for this build, 2026-09-09

| Tool | Pinned | Checked against the vendor today | |
|---|---|---|:-:|
| **ExifTool** | 13.59.0 | `exiftool.org/history.html` — **13.59, released 2026-05-27, still latest** | ✅ |
| **HxD** | 2.5.0.0 | `mh-nexus.de/en/hxd/` — **2.5.0.0, 2021-02-11, still current** | ✅ |
| Python 3 | installed by `00_bootstrap.ps1` | used for the LSB diff and extraction | ✅ |
| 7-Zip | installed by `00_bootstrap.ps1` | second route to the appended archive | ✅ |
| Steganography tool | **none** | `tools_by_session.md` §1.3 dropped Xiao; nothing replaced it | ⚠ see Case 03 change 2 |

**`P06` requires no new tool install.** Everything it teaches runs on the `CLEAN-TOOLS` snapshot.

---

## 10 · Open items carried into `build_log.md`

- `check_widths()` is required by Part 9 before any SVG ships and **has no implementation in the
  repo** — it is named in `00_INSTRUCTIONS.md`, `DECISIONS.md` and the build prompt only. It will be
  written into `scripts/` as part of this build and broken on purpose to prove it fails.
- `density_gate.py` enforces a rule it calls **`D126`** (*the Arabic must name the same technical term
  as its English*). `DECISIONS.md` ends at `D125` and has no such row. The check is right and the row
  is missing; the ID above is proposed as `D126` only if that gap is filled first.
- **`docs/resources/evidence.html` is stale by three sets.** It still prints `EVS-01` and `EVS-05` as
  `unverified · unverified · Phase 3`, and **has no `EVS-10` row at all** — while
  `design/evidence_sets.md` carries full, dated manifests for all three. `D26` requires the published
  table to say `unverified` **until** `evidence_sets.md` marks a set verified; it has, and the page
  did not follow. Regenerating it belongs with decision 2.
- `docs/page-03/index.html` contains **no external links at all** — only its own `#pN` anchors. So
  nothing is broken; the gap is that a page which names two evidence sets offers no route to either.
