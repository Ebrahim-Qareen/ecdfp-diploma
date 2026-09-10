# P09 — File systems · build log

**Topics** `T14` File Systems — FAT & NTFS (52 min) · `T15` Carving & Deleted Data (25 min) — **77 minutes**
**Page** `docs/page-09/index.html` — 29 screens, 6 part dividers
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **6** — `F1` the three FAT structures · `F2` what a delete changes · `F3` an MFT record · `F4` two data streams · `F5` carving across a fragment · `F6` six objects, three outcomes |
| SIMSCREEN | **2** — `ss-t14` reading a deleted file out of the `$MFT` (5 steps) · `ss-t15` Case 05, carving a volume with no file system (5 steps) |
| Rendered result | **1** — `carve_compare.png`, the fragmented photograph as carved beside the original |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | `EVS-11` — three images, **built for this page**, 49 assertions passed |

## The page this was supposed to be, and the page it is

`P09` was marked **⛔ blocked** on `EVS-02` in every planning document. It is not blocked, and the `D127`
split is why: `T14` and `T15` need **a file system to read**, not *the suspect's* file system. A FAT volume
and an NTFS volume that we build ourselves teach every structural fact in both topics, and they teach them
better, because **we know the ground truth and can hash against it**.

`EVS-02` is still needed — for `P10`'s registry hives and `P11`'s execution artifacts, where the content of a
real system is the point. It was never needed here.

## Every number on the page was measured

**NTFS — `EVS-11-ntfs.dd`, four records:**

| Record | File | `$DATA` | The lesson |
|--:|---|---|---|
| 64 | `notes.txt` | **resident, 290 B** | the file occupies **no cluster anywhere** — the record *is* the file |
| 65 | `report.bin` | **non-resident, 204,800 B** | the record holds only a run list |
| 66 | `budget.csv` | **34 B unnamed + 41 B named `notes`** | the listing size counts one stream of two |
| 67 | `old_plan.txt` | **resident, 212 B** — flags `0x00`, links 0, seq 2 | **deleted, and its full content is still readable at `0x14D78`** |

Record 67 is the page's centrepiece. A resident file's content lives inside the record that deletion marks
free, so **deleting a small NTFS file does not remove it from anywhere** — it clears a flag in the same
1,024 bytes that hold the text.

**FAT — `EVS-11-fat.dd`:**

The deleted entry still reads `E5 4C 44 5F 49 4E 7E 31 50 44 46` — **ten of eleven name bytes**, size
**1,583**, first cluster **19**. That cluster is marked free and still begins `25 50 44 46`. **A FAT delete
changed five bytes and left the document alone.**

`whiteboard.jpg` occupies **two runs, (20, 9) and (38, 10)**, with nine clusters of `logs.txt` between them.
`mtools` will not fragment a file — it allocates from a next-free hint — so the file was **written into the
FAT by hand**, chain and directory entry both. The chain walks correctly and reassembles to the original
SHA-256, which is how we know the hand-written file is a real file and not a prop.

**Carving — `EVS-11-carve.dd`:** the same volume with both FAT copies and the root directory zeroed —
**86,016 of 41,943,040 bytes, 0.2051%** — data area byte-identical.

| Carved | Result |
|---|---|
| `site_photo.jpg`, `badge_scan.png`, `exports.zip` | **exact** — hash matches |
| `handover.pdf`, `old_invoice.pdf` | **one byte short** each: the files end `%%EOF\n` and the footer rule stops at `%%EOF` |
| `whiteboard.jpg` | **112,253 bytes instead of 75,389** — exactly **+36,864**, nine clusters of the log file |

Two results are worth more than the rest. **The deleted invoice was carved** — the carver found it because it
never consulted the file system, so "deleted" meant nothing to it. And the fragmented photograph **still opens
as an 800×500 JPEG**, with a band of log data across the middle. `carve_compare.png` shows it, because a
student who sees that image does not need the argument.

## What changed outside this page

**`scripts/make_evs11.py` is new**, and reproducible where it honestly can be. Two builds of the FAT and carve
images are byte-identical; the NTFS image differs in **344 bytes of 67,108,864** because `mkntfs` writes a
journal and index entries carrying timestamps. **Those are not pinned on purpose**: forging a `$LogFile` that
does not match what happened is a worse thing to give a forensics student than an unstable hash. The manifest
carries the four MFT records the page reads instead, and those are stable. See `D135`.

**`.photo.wide` is new (`D134`).** `figure.photo img` is a fixed 560 px, which is right for a photograph of a
write blocker and wrong for a 3:1 comparison. `P06` has been shipping two comparison figures at that width
since it was built, and it took building `P09` to notice.

**A fabricated pair of hashes was caught before it shipped.** Writing this set's manifest entry, two SHA-256
values were completed from the 16-character prefixes printed by the build rather than copied from
`EVS-11.sha256`. They were corrected and then **every 64-hex string in both the `EVS-07` and `EVS-11`
sections was checked mechanically against the real manifests**. See `D135`.

## Gates

```
python3 scripts/density_gate.py docs/page-09/index.html      ALL PASS
node testing/render_gate.js docs/page-09/index.html          PASS — zero findings
```

Nine pages now pass both.
