# BUILD PROMPT — Session 1 · Foundations, Evidence Integrity & Chain of Custody

**Read `design/prompts/SHARED_RULES.md` first. Everything in it is binding.**
Project root: `E:\Work\ITgate\ECDFP_Course`. Output: `docs/session-01/index.html`.

A version of this page already exists and **passes both gates** (2,902 words, 131/page, zero
pages without a visual, render-clean at five widths). Your job is to **raise the visual quality
to the ceiling** — animate the mechanisms, sharpen the diagrams, tighten the type — **without
losing a single gate**. Re-measure after every change.

---

## 1 · The spine — one question drives the whole session

> **You have been handed evidence. How do you know it is real?**

Every block answers part of it. Case 01 is that question with a right answer. **If a block does
not serve that question, it does not belong on the page.**

**The hook (page 4).** Four files arrive with a signed manifest. The acquisition log says
`verified`. One file has been altered by **a single character** since the manifest was signed.
The claim on trial: *"the log says it verified, so the evidence is fine."*

Evidence set **`EVS-01`** — verified and published in `docs/session-01/`. Four plain-text files,
`EVS-01.sha256` and `EVS-01.md5`. `sha256sum -c` gives **3 × OK, 1 × FAILED**. Use the real values.

---

## 2 · The blocks — 130 taught + 60 investigation + 15 close

Teaching order. The `S1-NN` label is a stable ID, **not** the sequence.

| Page | Block | ID | Min | The visual this block IS | Practical inside the block |
|--:|---|---|--:|---|---|
| 5 | What digital forensics is — lifecycle, and what you may **not** claim | `S1-01` | 10 | lifecycle, 5 stages, S1's two lit | read one claim, say if it is allowed |
| 6 | Three principles — minimal footprint · repeatability · work on a copy | `S1-02` | 10 | 3 wrong/right pairs, red vs green | "which principle does this break?" ×3 |
| 7 | What makes evidence defensible | `S1-03` | 10 | table: *they ask* → *what answers it* → *artifact* | match 4 challenges to 4 artifacts |
| 9 | Toolkit **verify** + `CLEAN-TOOLS` snapshot ⚠️ *install is pre-work* | `S1-05` | 15 | `.gui-row` snapshot tree | take the snapshot, record the tree |
| 8,10 | Hashing — what it proves, what it does **not** | `S1-06` | 18 | **ANIMATE:** avalanche · `.gui` `sha256sum -c` | run it, write the failing filename down |
| 13 | Chain of custody — the form and the discipline | `S1-07` | 12 | custody timeline with **one unsigned gap** · `.gui-row` form | fill one entry for your own copy |
| 14 | Write blocking — and how you **prove** one was used | `S1-08` | 8 | **ANIMATE:** a write reaching the media vs being dropped | read the blocker log, extract the 4 fields |
| 15 | **The fixed report template — findings vs interpretation** | `S1-04` | 25 | `.finding`/`.interpretation`/`.limitation` on **one** fact · 10-section `.gui-row` | write all three about the failing hash |
| 16 | Inside a file — hex, magic bytes, why a rename changes nothing | `S1-09` | 22 | **ANIMATE:** extension flips, header bytes do not · magic-byte table | `xxd -l 16` on all four `EVS-01` files |
| 17 | **Case 01** — investigation | `S1-10` | 60 | brief + exhibit table, **no prose** | the whole thing |
| — | Hash-verify + custody close | `S1-11` | 15 | `.coc` | re-hash, sign, store read-only |

**Why the report template sits at page 15 and not earlier:** the student has already produced a
real finding by hand at page 10. You teach the form **after** they have made the thing the form
holds. Do not move it earlier.

---

## 3 · The four animations to build (`D51` — click-to-play, no autoplay, no loop)

1. **Avalanche (p8).** Two inputs differing by one character. On play, the second digest scrambles
   character by character into something unrelated to the first. Caption: *not "slightly
   different" — unrelated.*
2. **Write blocker (p14).** A write travels the path. On play it reaches the media on one route
   and is **visibly dropped** at the blocker on the other. Cross-fade a red shape in; do not
   animate `fill` to a `var()`.
3. **The rename (p16).** The filename label flips `.jpg` → `.txt` while the 16 header bytes below
   stay frozen. This is the whole lesson in one motion.
4. **The custody gap (p13).** Signed handovers light green left to right; the unaccounted 15 hours
   stays dark and the dashed box closes around it.

Each: `<g class="svg-play" role="button" tabindex="0">` with a visible ▶ label, and every
`<animate>` / `<set>` bound `begin="thatId.click"`. Nothing moves on load.

---

## 4 · What to take from the previous instructor's material

Source: `knowledge_base/instructor/Session_01_Introduction_and_Acquisition.md`.

**Take:**
- His **continuous acquisition lab** shape — image → verify → RAM → logical → mount → triage. It
  is the best thing in his S1. It belongs to Session 2, but S1's lab should feel like the same
  hands.
- His **evidence-lifecycle "we are here" marker.** Six of his eight decks open with it — his best
  structural habit. Keep it as the page-5 diagram.
- **Slide 30 of his session 8:** *"Don't say 'in my opinion Mr X has committed this crime. You are
  not the judge.'"* Move it into **page 15**, the report block, where it shapes the template from
  day one instead of arriving in the last session.

**Fix, do not copy:**
- ❌ **"Triage = three images"** (his slide 35) — wrong. Triage is a targeted subset, not three images.
- ❌ He lists `dd` and HashCalc in a lab agenda and **demonstrates neither**. Six such phantom labs
  exist in his decks. **Never build from his lab-agenda slides — build from what he actually ran.**
- ❌ He sets challenges and **ships no answer key**, in any session. Every challenge you build has
  a key, in-repo.

---

## 5 · What Session 2 will need from you

S2 opens on a **running** machine and teaches live response, memory capture and imaging. It
inherits and must not re-explain:

- hashing and `sha256sum -c` — **owned by you, p8**
- chain of custody — **owned by you, p13**
- write blocking — **owned by you, p14**
- the report template and the rubric — **owned by you, p15**
- hex and magic bytes — **owned by you, p16** (S2 uses it on a real image at its p15)

**Do not teach order of volatility.** It belongs to S2, taught once and operationally. Your page
must not contain the phrase.

Your page-22 "next session" line must set S2's hook: *the machine is still running.*

---

## 6 · Done means

```
python3 scripts/density_gate.py docs/session-01/index.html     → ALL PASS
node testing/render_gate.js docs/session-01/index.html         → zero findings, 5 widths
```
Plus, stated as numbers: total words, worst page, pages without a visual, animations built, and
that **no animation autoplays**. Then list what you changed and what you left alone.
