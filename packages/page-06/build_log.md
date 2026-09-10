# P06 — Hidden information · build log

**Topic** `T10` Hidden Data & Image Forensics (80 min)
**Page** `docs/page-06/index.html` — 26 screens, 5 part dividers
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **4** — `F1` one JPEG left to right · `F2` four timestamps on one photo · `F3` one bit, one pixel · `F4` the four checks in cost order |
| SIMSCREEN | **1** — `ss-t10`, the seven EVS-10 files in one pass (6 steps) |
| Real image | `assets/img/evs10-thumbnail-pair.png` — the redacted image beside its unredacted EXIF thumbnail |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | **`EVS-10` — Tier 3, verified, and the first page with no evidence blocker at all** |

## Every number on the page was measured, not recalled

`EVS-10` was regenerated from `scripts/make_evs10.py` and read before a word was written:

| Measurement | Value |
|---|---|
| `office_floor3.jpg` — `DateTimeOriginal` | `2026:08:24 09:14:02` |
| — `DateTime` (last software write) | `2026:08:31 16:40:05` — **seven days later** |
| — file mtime | `2026:09:02` — **two days later again**, and not in the photo at all |
| — `Software` | `MRG ImageTool 2.4` |
| — GPS | `30°2'27.60"N 31°14'13.20"E` |
| `team_photo.jpg` — ZIP local header | offset **10,296**, member `handover.txt` |
| `holiday_snap.jpg` | 156 B, `50 4B 03 04`, member `inventory.csv` |
| `meeting_notes.txt` | `89 50 4E 47` — a PNG |
| `receipt_scan.png` vs its clean twin | **190 of 76,800 pixels differ — R:0 G:0 B:190** |
| — recovered payload | `MRG-INTERNAL: staged archive is customer_export.7z` |
| `invoice_batch.jpg` — main image | 600 × 400, **redacted** |
| — EXIF thumbnail | **1,735 bytes, 160 × 107, NOT redacted** |

The thumbnail pair was rendered and **looked at** before the claim was written on the page. The
black box is on the main image and absent from the thumbnail.

## The three things this page teaches that `T04` could not

1. **`team_photo.jpg` passes the signature check.** It really is a JPEG. A file can be exactly what
   it claims and still be carrying something else — and only reading past `FF D9` finds it.
2. **Channel asymmetry is the LSB signal.** 190 pixels, all blue, red and green untouched. A
   photograph's noise is spread across all three channels; a payload is not. This is what you use
   when you do *not* have the clean twin, which is always.
3. **Redaction by drawing on pixels does not reach the EXIF thumbnail.** Ordinary editor behaviour,
   not a trick — which is why redaction means exporting a new file.

## Report discipline

The page ends on the split that `P01` set up: **Section 7 takes what another examiner could
reproduce from the bytes; Section 9 takes what you assess from it, with a confidence and a named
alternative.** The Case 03 exercise is six sentences to sort, and the one that matters is
*"no hidden data is present in the remaining files"* — **not supported**, and the easiest of the six
to write by accident.

## Gates

- `density_gate.py` — **ALL PASS**
- `render_gate.js` — **zero findings**, 5 widths
- Fixed during the build: three tables starved their Arabic at 1100 px — the `D129` two-column rule
  applied again, plus one case where the fix was to **drop** Arabic that added nothing (a
  two-word deliverable column).

## Open

- Nothing. This page has no evidence dependency.
