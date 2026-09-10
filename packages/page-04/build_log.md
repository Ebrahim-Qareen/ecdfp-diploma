# P04 — Volatile evidence · build log

**Topics** `T06` Live Response — Order of Volatility (25 min) · `T07` Memory Forensics — Acquire and Analyse (35 min)
**Page** `docs/page-04/index.html` — 29 screens, 5 part dividers
**Built** 2026-09-09

## What is on the page

| | |
|---|---|
| Screens | 29 (Cover · Where we are · Objectives · PART 1 6 · LAB 1 · ON YOUR OWN 3 · PART 2 7 · REPORT 1 · Summary · Homework · References) |
| Stepped figures | **6** — `P04-F1` order of volatility · `F2` the collector's footprint · `F3` smear not snapshot · `F4` Volatility 2→3 · `F5` four plugins · `F6` where the image lands |
| SIMSCREENs | **2** — `ss-t06` collect in order (6 steps) · `ss-t07` acquire memory (5 steps) |
| Arabic blocks | 222 |
| Lifecycle stage | **1 · ACQUIRE** |

## Evidence position — read this before teaching it

`EVS-03` (memory capture of `FIN-WKS-07`) and `EVS-09` (triage collection) are **⛔ PENDING** —
they need `labs/vm_notes/staging_plan.md` Phases C and D.

**What that did and did not block.** `T06` and the acquisition half of `T07` are *procedure*: they
need a running machine and a tool, not a corpus, and they are built at full depth. Only the
**15-minute Volatility investigation** needs an image, and that is routed to the free
**TryHackMe Volatility room** (already the vetted spine in `design/practice_platforms.md`) as
homework item 3.

**No memory image could be obtained in the build environment** — the network policy refused the
public corpora hosts, and the local VM could not fetch a browser engine either. So rather than
invent Volatility output, the page teaches **what each plugin establishes and what none of them do**,
with syntax verified against current tool documentation. Nothing on the page claims to be a
measurement that was not made.

**When `EVS-03` lands:** the investigation moves onto the diploma's own case, homework item 3 is
replaced, and the References screen's evidence note comes off.

## Facts verified against primary sources during the build

| Claim on the page | Source |
|---|---|
| the seven-tier order, and *"minimise changes to the data as you are collecting it"* | RFC 3227 §2.1 and §2.2, Brezinski & Killalea, February 2002 |
| WinPmem mini writes **RAW only**; the AFF4 imager was not carried to the new driver; write support disabled in signed binaries; Win7–Win10 | Velocidex WinPmem documentation |
| Volatility 3 has **no profiles** — a JSON **ISF** symbol table, often built from Microsoft PDBs | Volatility 3 documentation |
| malware plugins moved namespace (`windows.malfind` → `windows.malware.malfind`), old names deprecated | Volatility 3 release notes, 2.26.2 |
| **DumpIt is now Magnet DumpIt for Windows** — Comae was acquired | Magnet Forensics |
| memory is a *smear, not a snapshot*; *"running your forensic tool will change part of the memory"* | INE eCDFP M1, via `knowledge_base/Module_01` |

## The currency correction this page makes

Our courseware teaches `imageinfo` and `--profile=Win7SP0x64`. **Neither exists in the current
release line.** The page teaches this as the rule rather than as a version note: *RFC 3227 is from
2002 and is still exact; a command line from 2019 is already wrong.* **Principles age well and
procedures do not.**

Same shape as `D112` on `P02` — a respected source is imprecise in one place, and telling which is
the skill.

## Gates

- `density_gate.py` — **ALL PASS** (2,4xx words, worst screen 229, 0 screens with no visual)
- `render_gate.js` — **zero findings**, 5 widths, including the `D124` one-right-edge check
- Fixed during the build: 3 three-column tables starved their Arabic at 1100 px (`D105`) — two were
  folded to two columns, one had its cell Arabic shortened to names rather than sentences.
- `check_widths()` caught one SVG `<text>` overrun before any render pass.

## Open

- `EVS-03` / `EVS-09` acquisition (Phases C, D)
- The 11-document package: this log plus `guided_lab.md` and `report_stage.md` are written; the
  student-facing documents follow the page and are not yet split out.
