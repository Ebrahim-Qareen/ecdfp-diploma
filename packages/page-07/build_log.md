# P07 — Malicious files · build log

**Topic** `T11` Malicious Documents & Executables (75 min)
**Page** `docs/page-07/index.html` — 27 screens, 5 part dividers
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **5** — `F1` two document families · `F2` five parts of a .docx · `F3` follow the pointer · `F4` the entropy scale · `F5` imports as capability |
| SIMSCREEN | **1** — `ss-t11`, one document and one binary, without running either (6 steps) |
| Lifecycle stage | **3 · ANALYSE** |

## The scope decision, stated plainly

**This page contains no malicious sample and no macro source, and that is deliberate.**

`T11` has three parts. Parts 1 and 2 — document structure and executable structure, 50 of the
75 minutes — are **format analysis**: they need a document and a binary, not malware. Part 3, the
carry-through malicious document, needs `EVS-06`, which is not acquired.

Part 3 is **not substituted**. Building a working maldoc to teach against is not something this
project will do, and it is not necessary: the half of the topic that transfers to every future file
is the structural half, and that is built here in full. The investigation runs when `EVS-06` exists,
in a lab VM, never on a classroom machine.

## Every number on the page was measured

Two artifacts, both benign, both read before writing:

**`handover_notes.docx`** — authored for this page. 3,111 bytes, `50 4B 03 04`, five parts:
`[Content_Types].xml` 674 · `_rels/.rels` 593 · `word/document.xml` **257** · `docProps/core.xml` 688
· `docProps/app.xml` 337. The visible text is the smallest part, and there is no `vbaProject.bin`.

**`_imagingmorph.cp312-win_amd64.pyd`** from published Pillow 12.3.0 — 12,288 bytes:

| Field | Measured |
|---|---|
| `e_lfanew` | **0x110**, and `50 45 00 00` is at that offset |
| Machine | 0x8664 AMD64 · 6 sections · DLL bit set |
| `TimeDateStamp` | 1782900552 → **2026-07-01 10:09:12 UTC** |
| Magic / ImageBase / Subsystem | 0x020B PE32+ · 0x180000000 · 2 (GUI) |
| Section entropy | `.text` **5.99** · `.rdata` 4.20 · `.data` 1.14 · `.reloc` **0.88** |
| Imports | 30 functions across 4 libraries — **no socket, registry, process or file-enumeration API** |

**And a measured entropy scale**, which is what makes `F4` worth having:
zeroes **0.00** · this PE whole-file **5.08** · English text 5.43 · `.text` **5.99** ·
the same PE compressed **7.96** · random bytes **7.95**.

## The three sentences the page turns on

1. **A macro's presence proves code is present** — and not that it ran, that macros were enabled,
   that the user clicked Enable Content, or that the code is hostile. And the reverse fails too:
   the second delivery path needs no macro at all.
2. **Compressed reads 7.96 and random reads 7.95.** Entropy cannot tell them apart, and certainly
   cannot tell either from malice. It is a reason to look, never a finding.
3. **A short import table is a louder signal than a long one** — two functions means the capability
   is resolved at run time, where a static reader cannot see it.

Summary line: **every over-claim in malware triage is one adjective past the evidence.**

## Gates

- `density_gate.py` — **ALL PASS**
- `render_gate.js` — **zero findings**, 5 widths
- Fixed during the build: two starved cells, both fixed by **deleting** Arabic rather than
  restructuring — a tool name (`oledump.py`) and a four-word claim need no gloss (`D76` r6).

## Open

- `EVS-06` for the part-3 investigation. Everything else on this page is complete.
