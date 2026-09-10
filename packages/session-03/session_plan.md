# Session 3 — Session Plan

**eCDFP Diploma · ITGate Academy**
**Hidden Information: Metadata, Steganography & Malicious Files**

| | |
|---|---|
| **Session** | 3 of 6 |
| **Slot** | 240 min · 220 teaching · **205 topic minutes** + 15 break (`D15` / `D23`) |
| **INE source** | Module 2 |
| **Primary domains** | Fundamentals of Digital Forensics · Digital Forensics Tools & Techniques |
| **Delivery** | integrated theory → demo → **micro-lab after every block**, closing with one blocked investigation hour |
| **Students** | ~5, offline classroom, **every student at a keyboard** (`D16`) |
| **Evidence** | `EVS-05` ✅ **verified** · `EVS-10` ✅ **verified** · `EVS-06` ⛔ pending. See §6 |
| **Case** | Case 03 — 12 files, five that lie, one hidden payload · Case 03b — the carry-through document |

---

## 1 · Where this session sits

**This is the session students have been waiting for**, and it is deliberately placed early
(`D58`). Sessions 1 and 2 were about being allowed to look. Today you actually look.

| Session 1 gave you | Session 2 gave you | Today |
|---|---|---|
| hex, magic bytes, a hash | verified images, a signature sweep | what is **inside** that nobody meant you to see |

**The one idea the session turns on:** metadata and hidden data are *evidence about a file*, and
they are the easiest place in the whole course to overreach. A GPS tag feels like proof of a person.
It is not. **Criterion 4 of the rubric bites harder today than in any other session.**

---

## 2 · Objectives

| # | Objective | Blocks |
|---|---|---|
| **O1** | **Read** a value out of a structure knowing its endianness and encoding | `S3-01` |
| **O2** | **Extract** metadata from an image and **state** which of its four clocks a date came from | `S3-02` |
| **O3** | **Detect** hidden data — LSB payloads and appended files — and **state** the limit of a negative result | `S3-03` · `S3-04` |
| **O4** | **Locate** a macro inside both OLE and OOXML containers | `S3-05` |
| **O5** | **Separate** what a photograph shows from what it cannot prove, in writing | `S3-06` · `S3-07` |

---

## 3 · Time table

| # | Block | Type | Min | Cumulative |
|---|---|---|--:|--:|
| `S3-01` | How data is represented — endianness and character encodings | theory | 15 | 15 |
| `S3-02` | **Metadata and EXIF** — GPS, the four clocks, and how far to trust them | theory + 2 micro-labs | 25 | 40 |
| — | **Knowledge check 1** | check | *(within blocks)* | 40 |
| `S3-03` | 🔴 **Steganography** — LSB, and how you actually **detect** it | theory + micro-lab | 25 | 65 |
| `S3-04` | 🔴 **Embedded and appended data** — polyglots, `binwalk` | theory + micro-lab | 20 | 85 |
| — | **Knowledge check 2** | check | *(within blocks)* | 85 |
| — | **BREAK** | break | *15* | *100* |
| `S3-05` | Malicious document structure — OLE vs OOXML, where a macro lives | theory + micro-lab | 25 | 110 |
| `S3-06` | 🔴 **Image forensics** — the thumbnail that outlived the edit, and what a photo cannot prove | theory + micro-lab | 20 | 130 |
| `S3-07` | **[INVESTIGATION]** Case 03 — 12 files, five that lie, one hidden payload | activity | **35** | 165 |
| `S3-08` | **[INVESTIGATION]** The carry-through document | activity | **25** | 190 |
| — | **Knowledge check 3** | check | *(within `S3-08`)* | 190 |
| `S3-09` | **[RITUAL]** Hash-verify + chain-of-custody close | ritual | 15 | **205** |

| | Min |
|---|--:|
| Integrated (`S3-01` … `S3-06`) | **130** |
| Break | 15 |
| Blocked investigation (`S3-07` + `S3-08`) | **60** |
| Ritual (`S3-09`) | **15** |
| **Teaching total** | **220** · slot 240 · slack 20 |

**Hands-on: 180 min of 205 (88 %)** — the highest of any session so far. Only `S3-01` is theory-only.

---

## 4 · Prerequisites

| | Who | What |
|---|---|---|
| 1 | student | `FOR-WS01` on `CLEAN-TOOLS`; HxD, ExifTool, `binwalk`, `zsteg`, Stegsolve, `oledump`/`olevba` installed |
| 2 | student | `EVS-05` and `EVS-10` downloaded **and hashes verified** (`D18`) |
| 3 | instructor | a locally created macro-enabled document as the `EVS-06` stand-in (see §6) |
| 4 | instructor | fallback USB set re-verified |

---

## 5 · Tools

⚠️ Versions confirmed **2026-09-06**.

| Tool | Role | Note |
|---|---|---|
| **ExifTool 13.59** | 🟢🟢 CORE | metadata for `S3-02`, `S3-06`. `-b -ThumbnailImage` extracts the embedded preview |
| **HxD 2.5.0.0** | 🟢🟢 CORE | `S3-01`. Free for commercial use. ⚠️ Last updated 2021 — stable, say so rather than be caught out |
| **`binwalk`** | 🟢🟢 CORE | `S3-04`. Scans for every signature at every offset |
| **`zsteg`** | 🟢 SUPPORTING | LSB detection in PNG/BMP only |
| **Stegsolve** | 🟢 SUPPORTING | bit-plane browser — the visual method that actually works |
| **`oledump.py` / `olevba`** | 🟢🟢 CORE | `S3-05`. List streams, then read the macro |
| **`file` / TrID** | 🟢 SUPPORTING | signature identification, carried over from `S2-06` |
| ~~010 Editor~~ | 🔴 DROP | paid, 30-day trial, no free tier — HxD does everything needed |
| ~~Xiao Steganography~~ | 🔴 DROP | **no living vendor**; every copy is a 2010-era mirror. `zsteg`/Stegsolve/`binwalk` replace it |

---

## 6 · Evidence

| Set | What | For | Status |
|---|---|---|---|
| `EVS-05` | 12 files whose extensions are unreliable — 5 lie, 2 are truncated | `S3-07` | ✅ **verified 2026-09-06** |
| `EVS-10` | EXIF/GPS + 4 clocks · LSB stego **and its clean twin** · a JPEG/ZIP polyglot · a thumbnail that outlived a redaction | `S3-02` `S3-03` `S3-04` `S3-06` `S3-07` | ✅ **verified 2026-09-06** |
| `EVS-06` | the carry-through malicious document, extracted from `EVS-02` | `S3-05` `S3-08` | ⛔ **pending** — needs the S2 acquisition |

🟢 **Five of the six blocks are fully unblocked.** Both Tier 3 sets are generated by
`scripts/make_evs05.py` and `scripts/make_evs10.py`, deterministic and cross-verified on two
machines, so a student's regenerated copy is diffable against the instructor's.

⛔ **`S3-05` and `S3-08` need `EVS-06`**, which comes out of the `EVS-02` disk image. Until the
acquisition runbook is run, teach the **structure and method** on a locally created macro-enabled
document and say plainly that the case document is not yet available.

**Constraints (`R8`, `R9`, `D41`):** fictional company and users · no real personal data · no real
malware · **no IP addresses at all in these sets** · no question has a secret or a person's data as
its answer · no evidence bytes in the repo.

---

## 7 · The carry-through case (`D19`)

**Stage 1 is lit.** `l.bennett` opened a document that arrived by email. Today it is taken apart —
real type, container, macro location, references — and the photographs from the same host are
examined, because the exfiltration in stage 6 used one of them.

---

## 8 · Assessment

| What | When | Against |
|---|---|---|
| Knowledge check 1 | after `S3-02` | O1 · O2 |
| Knowledge check 2 | after `S3-04` | O3 |
| Knowledge check 3 | after `S3-08` | O5 |
| `quiz.md` — 10 MCQ | end of session | all five |
| Case 03 write-up | in `S3-07` | O3 · O5 |
| Homework report | take-home | the `D20` rubric, unchanged |

**The rubric is unchanged and never changes** (`D20`): Integrity · Method · Findings · Separation.

---

## 9 · Bridge to Session 4

S3 ends having read what files say about themselves. **S4 goes underneath the file system** —
sectors, clusters and slack, MBR and GPT, FAT and NTFS — and recovers the staging archive that was
deleted before the exfiltration.

Closing line: *"Everything today was inside a file. Next week we look at what is left when the file is gone."*
