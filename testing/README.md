# testing/ — the Part 9 verification gate

Nothing is reviewed and nothing is published until this passes. Zero findings, or the work does
not move.

## The four checks

| Check | Script | Runs on |
|---|---|---|
| Render — 1400 / 1100 / 900 / 700 / 480 px | `testing/render_gate.js` | Node + Playwright/Chromium |
| Credentials · PII · evidence bytes · stage directions | `tools\precommit_scan.ps1` | Windows PowerShell |
| Local refs + external hosts | `tools\check_links.ps1` | Windows PowerShell |
| **Research-note structure + credential leak** | **`testing/verify_note.py`** | **python3, from `Resources/THM`** |

```
node testing\render_gate.js docs\session-01\index.html
powershell -ExecutionPolicy Bypass -File tools\precommit_scan.ps1
powershell -ExecutionPolicy Bypass -File tools\check_links.ps1
```

```
python3 ../../testing/verify_note.py <note>.md '{"finding":"exact phrase that must appear"}'
```

The first three exit **0 on clean, 1 on findings**, so they can gate a script or a CI step.
`check_links.ps1 -SkipExternal` skips DNS for an offline classroom machine.

## The two traps, encoded as guards

Part 9 records two mistakes this project has already paid for. Both are now enforced by the
harness rather than by memory:

1. **The Playwright option key is `viewport`, not `viewportSize`.** `viewportSize` is silently
   ignored — the suite passes at one default width while claiming to have tested five.
   `contextOptions()` asserts the spelling and aborts the run if it ever drifts.
2. **`url#pN` on an already-loaded document does not re-run the page script.** Every page under
   test gets its own full `page.goto()` with the hash in the URL. There is no hash assignment on
   a live document anywhere in the harness.

## What the render gate asserts

- Zero document-level horizontal overflow at every width
- Zero elements wider than the viewport outside a designated scroll container
- Zero SVG geometry or text escaping its `viewBox`
- Every `[data-node]` has **exactly one** matching `[data-detail]`, and no orphan panels
- Zero console errors and zero failed requests (a missing asset fails the gate)
- `.page` count matches `.page-list` entry count, and exactly one page is visible
- `.page-layout > * { min-width: 0 }` is actually in effect — the load-bearing rule

## The note checker — `verify_note.py` (D39)

Runs on every file in `Resources/THM`. Asserts: exactly nine `## N.` sections; a `### 2.N` block for
every artifact; **all six boxes present on every block, in equal counts**; and **no credential-shaped
string anywhere in the note**. The optional second argument is a JSON dict of phrases that must
appear verbatim — pass the note's own headline findings, and it catches a finding you meant to record
and didn't.

🔴🔴 **Never run a copy from `/tmp`.** On 2026-08-29 a stale `/tmp/verify.py` was found owned by
another user and unwritable, so a heredoc write failed silently and the *old* script ran, reporting
PASS. That old script used a **literal password blocklist**, which made the checker itself a
credential store — in a repo that is **PUBLIC (D22)**. **The credential check is pattern-based on
purpose**: patterns generalise to rooms not yet seen, and they store no secret.

### Proving the note checker can fail

Same principle as the render gate. Re-run both controls on any change to the `CRED` list:

| Control | Result, 2026-08-29 |
|---|---|
| 7 synthetic leak shapes (user/password pair · labelled · space-separated · api key · bearer · WLAN PSK · private key) | **7/7 caught** |
| All 33 real notes | **0 false positives** |

⚠️ **Build the fixtures with obviously synthetic values, outside the repo, and delete them after the
run.** Four false-positive modes have been seen, and **all four were in the assertion string, never
in the note**: a phrase split across a line wrap; a case mismatch; markdown emphasis inside the
phrase; and a blockquote marker on a wrapped line. The first and last are normalised away by the
script; the other two are the caller's job. **Always grep the note before changing it in response to
a MISSING result.**

## Proving the gate can fail

A gate that only ever passes proves nothing — that is the `viewportSize` trap restated. The
harness was mutation-tested on 2026-08-28 against eight injected defects and caught all eight:

| Mutant | Caught by |
|---|---|
| `.page-layout > * { min-width: 0 }` deleted | load-bearing CSS missing |
| `.table-wrap` loses its scroll container | element wider than viewport |
| a `data-node` loses its `data-detail` | pairing |
| two `data-detail` panels for one node | pairing |
| SVG text pushed outside the `viewBox` | SVG outside viewBox |
| a referenced JS file removed | console error + failed request |
| sidebar carries one more entry than pages | page count vs sidebar |
| option key changed to `viewportSize` | **run aborted** |

**Three checks added 2026-09-08 (`D105` · `D106` · `D107`), mutation-tested the same day — 6 of 7
injected defects caught, and the seventh is a non-defect (see below):**

| Injected defect | Caught by |
|---|---|
| the cell-wide `text-wrap:nowrap` on a first table column | Arabic in a starved container (D105) |
| `.ar` to a full-width right-aligned block | Arabic not under its English (D108) |
| `.ss-mask` bleed restored, so the spotlight leaves the pointer | SIMSCREEN pointer off its window (D107) |
| `place()` stops dividing by the holder's `zoom` | SIMSCREEN pointer off its window (D107) |
| the IntersectionObserver re-place removed (`D103`) | SIMSCREEN pointer off its window (D107) |
| the SIMSCREEN container queries removed | **nothing — and correctly so** |

That last row is not a hole in the gate. The container queries exist for a band that no longer
occurs on these five widths, because the sidebar now collapses at 1099 px rather than 899 px
(`D105`) and the 900 px page is full width. Removing the rule produces no overflow, so there is
nothing to catch. It is kept as a safety net for a narrower container, not deleted.

**The `.ar` check asserts the PAINTED TEXT, not the box.** Its first version compared box edges —
and a full-width right-aligned `.ar` starts its *box* at exactly the same place as a `fit-content`
one, so the check passed the very layout it exists to reject. Only the glyphs differ, and only on a
block that fits on **one line**; a wrapping block fills the column either way. The check also has
to add the parent's **border** to its padding, or every `.note` reads as 3 px adrift.

**The two SIMSCREEN assertions are behavioural, not structural.** The pointer must land on the
element the step *declares* it points at (`root.dataset.ssTarget`, published by `place()`), and
the spotlight must indicate the same place as the pointer (`root.dataset.ssSpot`). An earlier
version only checked "the ring is somewhere inside the window" — it passed a 30 px offset and a
`z x z` error, which is how both shipped.

`precommit_scan.ps1` and `check_links.ps1` were tested the same way against a deliberately dirty
tree and caught all of it: a password assignment, an AWS key, a real email address, a routable
private IP, an `.E01`, a bare `SYSTEM` hive, an instructor stage direction, a broken local
reference and a dead external host.

**Re-run the mutation test after any change to the harness.** A harness that stops catching
mutants has stopped being a gate.

## Scratch

The throwaway page used to exercise the gate is built **outside the project tree** and is never
committed (R3 — the device mount cannot delete, so anything created inside the tree is permanent).
