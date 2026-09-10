# P05 — Acquisition · build log

**Topics** `T08` Imaging Scope & Formats (33 min) · `T09` Imaging Tools — FTK Imager & dc3dd (112 min)
**Page** `docs/page-05/index.html` — 31 screens, 5 part dividers
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **5** — `F1` three scopes · `F2` what each format carries · `F3` three sizes for one disk · `F4` DCO before HPA · `F5` the loop `verified` covers |
| SIMSCREENs | **2** — `ss-t09a` FTK Imager acquisition (6 steps) · `ss-t09b` dc3dd and an independent check (5 steps) |
| Lifecycle stage | **1 · ACQUIRE** — same stage as `P04`, and the page says why: `P04` took the volatile half, this takes the disk |

## The two sentences the page turns on

1. **`verified` describes a write-then-read round trip inside one tool.** The source is never read a
   second time, so the word says nothing about the disk, nothing about the write blocker, and nothing
   about whether the right device was selected. An image of the wrong disk verifies perfectly.
2. **One disk can report three different sizes.** INE's own worked example: `IDENTIFY_DEVICE`
   100,000,000 · `READ_NATIVE_MAX` 156,301,488 · DCO 625,142,447. Image the first number in good
   faith and a fully verified forensic image covers **16% of the drive**, with nothing anywhere
   saying so.

And the operational consequence of (2): **the DCO check comes before the HPA check.** A DCO lowers
the native maximum that `hdparm -N` measures against, so the wrong order reports *"HPA is disabled"*
on a disk that is hiding capacity.

## Evidence position

`EVS-02` and `EVS-04` are ⛔ PENDING. `T09` is therefore taught against **a device the student owns**
— a USB they can inspect afterwards.

This is not only a workaround. For an acquisition exercise, **knowing ground truth is worth more
than realism**: it is the only way a student can tell the tool's mistake from their own. Case 02a
ends with `sha256sum` on the *source device*, which is practical on 16 GB and not on 4 TB — so the
student learns what they are giving up before they are in a situation where they must give it up.
When `EVS-02` lands it becomes the second exercise, not the first.

## Tool currency — what the check found

| Claim | Finding |
|---|---|
| FTK Imager, published by AccessData, 4.x | **Now Exterro, current free line 8.3, with a separate paid FTK Imager Pro** |
| `dc3dd` | still packaged in Kali at **7.3.1** — stable rather than abandoned; the course's choice stands |
| HPA/DCO detection | `hdparm --dco-identify` → `Real max sectors:` · `hdparm -N` → `max sectors = A/B` |

## Gates

- `density_gate.py` — **ALL PASS**
- `render_gate.js` — **zero findings**, 5 widths
- Fixed during the build: four tables starved their Arabic at 1100 px (`D105`) — a 4-column table
  became 2 columns, two 3-column tables became 2, and one became a single column. **A table with
  Arabic in every cell does not survive more than two columns below 1200 px** — that is now the
  working rule.
- One build-time `check_widths()` catch before any render pass.

## Open

- `EVS-02` / `EVS-04` acquisition (Phases C, D)
- The rest of the 11-document package
