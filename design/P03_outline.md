# P03 outline — Data at byte level

**OUTLINE GATE (`D9`).** Page `P03` · **117 topic minutes** · topics `T04` (82) + `T05` (35).
Evidence **`EVS-05`** · **`EVS-01`** · **`EVS-10`** — all three verified.
Design frozen by `D109`; diagrams stepped per `D115`. This page decides nothing new.

Sources: `knowledge_base/Module_02_Data_Representation_and_File_Examination.md` ·
`Module_01` (Case 01) · `knowledge_base/instructor/Session_02` ·
`knowledge_base/thm/` (file-carving, autopsy).

---

## The one sentence this page installs

**The name of a file is a label someone typed. The bytes are the file.**

`P02` taught that a copy equals its source. `P03` asks the harder question: the copy is identical —
but what is actually *in* it? A file says it is a `.jpg`. **Who says?**

---

## The evidence, generated and read before writing a word

`EVS-05` and `EVS-10` had **never been generated** — only their scripts existed. Both were run and
their real bytes read, so every value on this page is a measurement, not an illustration (`D94`).

**`EVS-05` — 12 files, and 5 of them lie.** Read from the real magic bytes:

| The name says | The first bytes say | |
|---|---|:-:|
| `thumbnail.png` | `FF D8 FF E0` — **JPEG** | ✗ |
| `holiday_snap.jpg` | `50 4B 03 04` — **ZIP** | ✗ |
| `invoice_scan.jpg` | `25 50 44 46` — **PDF** | ✗ |
| `meeting_notes.txt` | `89 50 4E 47` — **PNG** | ✗ |
| `policy_v2.docx` | `89 50 4E 47` — **PNG** | ✗ |
| the other seven | agree with their extension | ✓ |

**`EVS-10` — the EXIF set.** Also real:

- `office_floor3.jpg` — GPS present (30&deg;2&prime;27.6&Prime;N 31&deg;14&prime;13.2&Prime;E), and
  **`DateTimeOriginal` 2026-08-24 09:14:02 against `DateTime` 2026-08-31 16:40:05** — a week apart.
- `team_photo.jpg` — **no EXIF at all.** The absence is the finding.
- `invoice_batch.jpg` — EXIF present, **no GPS**.

> **The continuity worth noticing:** `09:14:02` is the same timestamp `EVS-01` was seeded to break in
> `P02`. Same case, same hour, three pages apart. Nobody planned that across sessions — it is what
> having one case running through the whole diploma buys.

---

## `T04` — Inside a File · 82 min

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory** | 20 | Bridge from `T03`: *your copy is identical to the source. Identical to **what**?* Then: hex as a way of reading bytes (6) · magic bytes and the signature table (8) · why renaming changes nothing, and what actually does change (6). |
| **Guided practice** | 18 | `SIMSCREEN T04-1` — a signature sweep across `EVS-05`: read the first four bytes of one file, meet a mismatch, then sweep all twelve. **Key step: `thumbnail.png` returning `FF D8 FF E0`** — the moment the extension stops being evidence. |
| **Independent &mdash; CASE 01** | 40 | The `CASE-01B` verification challenge, cut to 40 min. A package from another examiner, two manifests, and the covering line *"Verified before sending."* `sha256sum -c` does not finish it. |
| **Report stage** | 4 | **Section 6 Tools and method** — first real rows: what was run, on what, with which version. |

**Theory 20 / 82 = 24 %.**

## `T05` — Data Representation & Metadata · 35 min

| `D79` part | Min | Content |
|---|---:|---|
| **Bridge + theory** | 12 | Bridge from `T04`: *you can now say what a file is. Now: what does it say about itself?* Endianness and encodings (6) · what EXIF is and where it comes from (6). |
| **Guided practice** | 10 | `SIMSCREEN T05-1` — read `office_floor3.jpg`'s EXIF: GPS, then the two timestamps a week apart. **Key step: the disagreement**, and what each of the two actually records. |
| **Independent** | 9 | Three images from `EVS-10`, three questions: where was it taken · when · and for `team_photo.jpg`, **why the empty result is itself a finding**. |
| **Report stage** | 4 | **Section 8 Findings** — the first entries, each tied to a named file at an exact path. |

**Theory 12 / 35 = 34 %.** Page total **32 / 117 = 27 %**, inside `D79`'s ceiling.

---

## Screens (~22) and figures

Every teaching screen carries a figure (`D94` pattern 1, `D115` stepped) — not the first five only.

| Figure | Pattern | Shows |
|---|---|---|
| `P03-D1` | 1 · 6 | **The same 8 bytes read three ways** — as hex, as ASCII, as a signature. One row of bytes, three interpretations stacked. |
| `P03-D2` | 2 · 3 | **Rename does nothing.** Two panes: the directory entry changes, the bytes do not move. |
| `P03-D3` | 1 · 5 | **The signature table as a lookup**, walked against a real file that disagrees with its name. |
| `P03-D4` | 2 | **Five liars out of twelve** — the real `EVS-05` sweep result, name against magic. |
| `P03-D5` | 1 · 6 | **Endianness** — the same four bytes, two orders, two very different numbers. |
| `P03-D6` | 1 · 5 | **Where EXIF comes from** — camera writes, software rewrites, and which field each one touches. |
| `P03-D7` | 1 · 4 | **Two timestamps, one week apart** — what `DateTimeOriginal` records and what `DateTime` records. |
| `P03-D8` | 5 · 8 | **Section 6 and Section 8** joining the report — 6 of 12 after three pages. |
| `SIMSCREEN T04-1` | 11 | the signature sweep · key step: `thumbnail.png` |
| `SIMSCREEN T05-1` | 11 | the EXIF read · key step: the timestamp disagreement |

---

## The three things this page must not let slide

1. **A signature is not proof of type either.** It is the first four bytes agreeing with a table —
   trivially forged, and absent from formats that have no magic number. `T04` teaches it as
   *better evidence than the extension*, never as certainty.
2. **EXIF is written by software and is trivially editable.** GPS in a photograph is a **claim by
   the camera**, not a fact about the world. This is criterion 4 territory and the quiz tests it.
3. **`team_photo.jpg` has no EXIF, and that is a finding, not a failed step.** Students reliably
   report an empty result as *"the tool did not work"*. It is the single most valuable moment in
   `T05`.
