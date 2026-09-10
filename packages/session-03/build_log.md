# Session 3 — Build Log

**Built 2026-09-06** under `D58`, immediately after the S1 re-cut and the S2 rebuild.
This session did not exist in this form before today.

---

## 1 · Why this session was rebuilt from the map up

The instructor reviewed the first S2 build and rejected it. One complaint was that students spent two
sessions on acquisition before reaching anything they found interesting, and that **steganography,
hidden data in photographs and file-type-by-hex were what he actually wanted to teach**.

Measured, not asserted: the old S3 was *"Data Representation & File Examination"* — five blocks of
which two (magic bytes, signature vs extension) have now moved **earlier**, to `S1-09` and `S2-06`.
**Steganography had zero rows in the ratified map**, despite `binwalk` (37 mentions), `zsteg`,
`stegsolve` and `steghide` sitting in the knowledge base.

`D58` rebuilt S3 as **Hidden Information**, and it is now the session with the **highest hands-on
ratio in the course: 180 of 205 minutes (88 %)**.

---

## 2 · What was built

| # | File | Bytes |
|--:|---|--:|
| 1 | `session_plan.md` | ~9 k |
| 2 | `instructor_guide.md` | ~8.5 k |
| 3 | `student_guide.md` | ~7.5 k |
| 4 | `guided_lab.md` | ~5 k · **six micro-labs** |
| 5 | `student_activity.md` | ~4.6 k · Case 03 + Case 03b |
| 6 | `quiz.md` | 10 MCQ, key split out |
| 7 | `quiz_answer_key.md` | **gitignored** (`D22`) |
| 8 | `report_template.md` | 🔴 **copied byte-for-byte from S1** |
| 9 | `build_log.md` | this |

Plus `docs/session-03/index.html` — **22 pages, 12 figures, 86 KB**.

---

## 3 · The blocks

| Block | Min | New? |
|---|--:|:-:|
| `S3-01` endianness and encodings | 15 | — |
| `S3-02` metadata and EXIF, the four clocks | 25 | deepened |
| `S3-03` **steganography, and how you detect it** | 25 | 🔴 **new** |
| `S3-04` **embedded and appended data, polyglots** | 20 | 🔴 **new** |
| `S3-05` malicious document structure | 25 | — |
| `S3-06` **image forensics, the thumbnail that outlived the edit** | 20 | 🔴 **new** |
| `S3-07` **[INVESTIGATION]** Case 03 | 35 | — |
| `S3-08` **[INVESTIGATION]** the carry-through document | 25 | — |
| `S3-09` **[RITUAL]** | 15 | — |
| | **205** | |

---

## 4 · Evidence — and why this session is not blocked

🟢 **`EVS-05` and `EVS-10` were generated and verified for this session.** Both are Tier 3 and
legitimately so: they are **images and documents we author**, not forensic containers. The Tier 3 bar
forbids fabricating `.evtx`, E01/AD1/raw, memory dumps and registry hives. It does not forbid making
a PNG.

| Set | Verified how |
|---|---|
| `EVS-05` — 12 files, 5 lying extensions, 2 truncated | regenerated to a second path and diffed **byte-identical**; a signature sniffer finds **exactly 5** mismatches, matching the answer key |
| `EVS-10` — EXIF/GPS, LSB payload **and clean twin**, polyglot, thumbnail | **13 of 13 assertions passed** — LSB decodes to the expected string, the clean twin decodes to nothing, the polyglot opens as **both** an image and a ZIP, the thumbnail differs across **290 of 290** sampled pixels in the redacted region. Regenerated **on a second machine** (the lab VM) — all 7 SHA-256 identical |

**So a student's regenerated copy is diffable against the instructor's**, on either machine.

⛔ **`EVS-06` is the exception.** The carry-through document comes out of the `EVS-02` disk image, and
**that acquisition has not run**. `S3-05` and `S3-08` therefore run on a locally created
macro-enabled stand-in. **The material says so plainly** rather than implying the case document is in
hand — in the session plan, the instructor guide, the student activity and on the page itself.

---

## 5 · Verified, by re-parsing the written files

| Check | Result |
|---|---|
| **Part 9 render gate** | ✅ **PASS, zero findings** — 22 pages × 5 widths |
| Blocks / minutes | 9 blocks, **205** = 130 integrated + 60 investigation + 15 ritual ✅ |
| Figures | **12**, and **every one of the 12 teaching pages carries one** ✅ |
| `data-node` / `data-detail` parity | ✅ |
| Every SVG `role="img"`, `<title>` first, `.svg-wrap` parent | ✅ |
| Micro-labs | **6**, each with all four parts ✅ |
| Stage directions in student-facing files | **0** ✅ |
| Quiz | 10 MCQ, rotation **A B C D A B C D A B** ✅ |
| Answer key published? | **No** — split into a gitignored file ✅ |
| Report template | byte-identical to S1's ✅ |
| Repetition of S1/S2-owned ideas | **0** occurrences of volatility, `verified`, or write-blocking in the student guide ✅ |

---

## 6 · Decisions honoured

| Rule | Where |
|---|---|
| `D7` findings vs interpretation | `S3-06`'s closing figure, Case 03 Q7, quiz Q9 · Q10 |
| `D20` rubric unchanged | `homework.md`, `report_template.md` byte-identical |
| `D41` no secret or personal data as an answer | both sets carry **no IP addresses at all** and a fictional payload |
| `D47` external practice with its defect named | `homework.md` — stego puzzles teach the wrong habit about negative results |
| `D52` all questions MCQ | `quiz.md` |
| `D58` one idea, one owner | volatility, `verified` and write-blocking appear **nowhere** in this session |
| `R9` no evidence bytes | generators + manifests only |

---

## 7 · Still open

| # | Item | Blocks? |
|--:|---|---|
| 1 | ⛔ **`EVS-06`** — needs the S2 acquisition to run | **`S3-05` and `S3-08`** run on a stand-in until then |
| 2 | `docs/session-03/brief.html` still describes the **old** session ("Data Representation & File Examination") and its old block list | No — the dashboard card and the teaching page are both correct |
| 3 | `roadmap.html` still lists the old S3 topic rows | No |
| 4 | `cases/case-03-*/` — `ecdfp-case` is **still not installed** (7 of 8 skills). Case content sits in `student_activity.md`, as S1 and S2 do | No, but it is now the third session working around it |
| 5 | The `S3-01` block has no micro-lab — it is the only theory-only block in the session. Deliberate, but it is the first thing to give one if the block ever grows | No |
| 6 | Stegsolve is named but not version-bound — it is distributed as a bare `.jar` with no clear versioning | Minor; state the source instead |

**An empty "still open" would be wrong.** Item 1 is the only one that changes what can be taught.


---

## Rebuild — the `D61` density pass (2026-09-06)

Built from `design/prompts/SHARED_RULES.md` + `S3_BUILD_PROMPT.md`. Rebuilt, not patched.

### Before → after

| | before | after | limit |
|---|--:|--:|--:|
| total visible words | **5 620** | **3 119** | ≤ 4 000 |
| average per page | **255** | **141** | ≤ 180 |
| worst single page | **487** | **220** | ≤ 250 |
| pages with no visual | 2 | **0** | 0 |
| pages with 4+ consecutive `<p>` | **11** | **0** | 0 |
| concept ownership | ✗ `finding` re-explained on p15 ×4 | **PASS** | — |
| figures | 12 | 7, of which **4 animate** | — |

### Every value on the page is real, and was measured

`EVS-05` and `EVS-10` both regenerated from their scripts and **verified against the published
manifests** — 12/12 and 7/7 `OK`. Then the actual tools were run and their output used verbatim:

| Claim on the page | How it was obtained |
|---|---|
| the three timestamps, nine days apart | `exiftool -s -G` — `DateTimeOriginal` 2026:08:24 09:14:02, `ModifyDate` 2026:08:31 16:40:05, `FileModifyDate` 2026:09:02 |
| GPS 30°2′27.60″N 31°14′13.20″E | `exiftool` Composite `GPSPosition` — resolves to a real city, which is the exercise |
| the surviving thumbnail, 160×107, 1 735 B | `exiftool -b -ThumbnailImage`, against a 600×400 main image |
| **190 of 76 800 pixels differ, all blue, every delta exactly 1** | pixel-by-pixel diff of `receipt_scan.png` against `receipt_scan_clean.png` |
| the polyglot's ZIP at offset **10 296** of 10 476, holding `handover.txt` 58 B | `unzip -l team_photo.jpg` plus a byte search for `PK\x03\x04` |
| endianness: `4D 5A 90 00` → 9 460 301 vs 1 297 780 736 | computed; the two differ by 137× |
| the six `.docm` parts and their sizes | `unzip -l` on the sample the shipped generator produces |
| `vbaProject.bin` begins `d0 cf 11 e0` | read from the extracted part |
| PE format, sections, imports incl. `GetSystemDirectoryA` | `objdump -f`, `-h`, `-p` on the compiled sample |

⚠️ **A size mismatch was caught this way.** The first `.gui` said 1 626 B / 3 530 B, from a scratch
build. The **shipped** generator produces 1 627 B / 3 532 B, because its `document.xml` differs by
two bytes. The page now states what `scripts/make_s3_sample.py` actually produces. A number on a
page has to come from the artifact that ships, not from a build that happened to be open.

### The four animations (`D51`)

| Figure | Page | The mechanism |
|---|:-:|---|
| `S3-F2` endianness | 5 | two read-order arrows sweep in opposite directions and two very different numbers resolve underneath |
| `S3-F4` the surviving thumbnail | 7 | a redaction blacks out the main image while the embedded thumbnail beside it stays sharp |
| `S3-F5` LSB | 8 | the low bit of blue flips, the swatch does not change, and the real diff count lands |
| `S3-F6` the document unzipping | 13 | one `.docm` opens into six parts, staggered, with `vbaProject.bin` in the alert colour |

Same contract as S1 and S2: one full-length `<animate>` per element, all `begin="<control>.click"`,
nothing autoplays or loops, no `fill` animated to a `var()`.

🟡 **One deliberate departure from `SHARED_RULES` §5 ("never invent a colour").** `S3-F5`'s two
swatches are painted `#603E3B` and `#603E3A` — the **actual pixel values** from the two evidence
files. They are data, not design: the entire point is that the reader cannot tell them apart, and a
token colour would destroy the lesson. Nothing else on the page uses a non-token colour.

### ⛔ `EVS-06` — one provisional page, and a sample that does not pretend to be it

`EVS-06` has no section in `design/evidence_sets.md` because it was to be carved from `EVS-02`.

- **Page 17** (`S3-08`, the carry-through document) keeps its full structure, five steps and
  verification line, with a visible `.caveat`. **No filename, size, digest or tool output on it.**
- **Pages 13 and 14 are complete**, taught on a Tier 3 sample authored for the course:
  `scripts/make_s3_sample.py`. Page 13 carries its own `.caveat` saying so.

⚠️ **The sample carries no `EVS-` id, deliberately.** Only the `ecdfp-evidence` skill assigns those
and owns the tier declaration. If the sample becomes permanent it must be declared there first.

🔴 **The `.docm` contains no executable macro code.** It carries the real OLE/CFB signature and a
real embedded object, which is everything the block teaches — *where* the macro lives and *what
container it is*. Shipping runnable VBA would add nothing to the lesson. The PE is a hello-world
compiled only to be read; the generator skips it with a message where no mingw cross-compiler
exists, rather than shipping a binary in a public repo.

### Scope held

Images run as one complete thread (EXIF → thumbnail → hidden data) before documents and
executables start. `policy_v2.docx` gets its own page moment and its own quiz item, and the student
is told to **predict before looking**. The two truncated files carry the header-vs-integrity
lesson. The "cannot be determined" question is the timestamp conflict, as the prompt specified.
S1's "the extension is a label" is used, never re-taught. Recycle Bin, TestDisk and carving are
left to S4, referenced in one clause. Xiao Steganography is named only as the thing not used.

### Gates

```
python3 scripts/density_gate.py docs/session-03/index.html   ALL PASS  (numbers above)
node testing/render_gate.js docs/session-03/index.html       PASS — zero findings, 5 widths
node anim_s3.js                                              PASS — 0 failures
node audit.js docs/session-03/index.html                     PASS — 0 findings
```

⚠️ **One intermediate failure, and it was the gate being right.** The magic-byte quick-reference
table on page 19 was written without a `.table-wrap`, and the render gate caught it overflowing the
viewport at 900px. Wrapped; re-run clean.

🔴 **And one mistake worth recording.** The S3 generator was derived from S2's, and the output path
lives in the tail of that script — which the derivation did not rewrite. **The first S3 build wrote
S3's content over `docs/session-02/index.html`.** It was caught immediately because the density gate
reported S2's old figure and MCQ counts, and it cost nothing to repair: re-running S2's own
generator restored the file to the exact verified hash `00267a4f…`. **That the pages are generated,
not hand-edited, is what made a destructive mistake a thirty-second fix.** The S3 generator now
asserts that no `session-02` path appears anywhere in it.
