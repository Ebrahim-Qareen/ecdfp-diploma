# BUILD PROMPT — Session 2 · Acquisition: Disk, Memory & Live Response

**Read `design/prompts/SHARED_RULES.md` first. Everything in it is binding.**
Project root: `E:\Work\ITgate\ECDFP_Course`. Output: `docs/session-02/index.html`.

⚠️ **A page exists at that path and it is the OLD build. It fails the density gate on six checks**
(7,163 words, 298/page, worst 590, 15 pages with four-plus paragraph runs, "hash" re-explained on
three separate pages). **Rebuild it, do not patch it.** Run the gate on the current file first so
you see the baseline you are replacing.

---

## 1 · The spine

> **The machine is still running. What do you take, in what order, and how do you prove
> afterwards that you did not change it?**

**The hook (page 4).** `FIN-WKS-07` is found powered on, a user still logged in. The clock is
running and every second costs volatile evidence. Session 1's Case 01 was a *cold* seizure where
memory was never captured — **use that as the cautionary contrast**, in one clause, not a lecture.

**Order of volatility is taught HERE, once, operationally** — as the reason for a collection
sequence, never as a list to memorise. Session 1 does not contain it.

---

## 2 · ⛔ Evidence gate — read before you plan the labs

`EVS-02` (disk image), `EVS-03` (memory), `EVS-04` (suspect USB) and `EVS-09` (triage set) are
**not yet acquired** (`design/evidence_sets.md`). Part 8 step 0 says a session does not start
without verified evidence.

**Therefore:** build pages **1–9 and 11–15** in full now. For pages **10, 16 and 17** build the
complete structure, steps and verification lines, and mark each evidence-dependent value with a
visible `.caveat` placeholder. **Do not invent hashes, file sizes or tool output for evidence that
does not exist yet.** Say clearly in your report which pages are provisional.

---

## 3 · The blocks — 130 taught + 60 investigation + 15 close

Teaching order. The `S2-NN` label is a stable ID, **not** the sequence.

| Page | Block | ID | Min | The visual this block IS | Practical inside the block |
|--:|---|---|--:|---|---|
| 5 | **Live response in order of volatility** | `S2-01` | 15 | **ANIMATE:** volatility ladder draining — RAM/net first, disk last | order 6 evidence types against the clock |
| 6 | The collector, **named** | `S2-01` | 10 | `.gui` BriMor `Windows_Live_Response.bat` menu + real output tree | run Triage, read the output tree |
| 7 | Memory acquisition — WinPmem · DumpIt · pitfalls | `S2-02` | 20 | what lives **only** in RAM · `.gui` WinPmem run | capture, then check the dump completed |
| 8 | Acquisition scope and image formats | `S2-03` | 25 | table physical vs logical · **E01 / raw / AD1** layout, embedded hash shown | pick the right format for 3 scenarios |
| 9 | 🆕 **HPA and DCO — storage hidden from acquisition** | `S2-07` | 8 | true sector count vs what the OS reports, hidden area shaded · `.gui` `hdparm -N` | read two sector counts, spot the gap |
| 10 | **FTK Imager end to end** | `S2-04` | 20 | numbered steps, verification line each · `.gui` verify dialog | image, then verify |
| 13 | `dc3dd` + targeted triage | `S2-05` | 12 | `.gui` `dc3dd hash=sha256` and its log | run it, compare its hash to FTK's |
| 14 | **What `verified` does and does not cover** | `S2-04` | — | **ANIMATE:** source → read → write → hash; the tick lands on **one link only** | say which link is unproven |
| 15 | Signature vs extension — on the image **you** just made | `S2-06` | 20 | annotated hex of a file pulled from the student's own image | `xxd` three files, one is lying |
| 16 | Independent practice | `S2-06` | — | task list ⛔ needs `EVS-02` | — |
| 17 | **Case 02a/02b** | `S2-08` `S2-09` | 60 | brief + exhibit table ⛔ needs `EVS-04` | acquire, verify, **verify completeness** |
| — | Hash-verify + custody close | `S2-10` | 15 | `.coc` | re-hash, sign, store read-only |

### Two scope rules you must not break

1. **HPA/DCO comes BEFORE the imaging tools** (page 9, before page 10). The student must know
   hidden storage exists *before* they image, so they know to check. Teaching it afterwards is
   backwards and was a defect we corrected.
2. **Case 02b is acquisition VERIFICATION, not file-system analysis.** It asks: is the volume
   present, what is the sector count, what file-system type does the tool report. ⛔ **It must not
   ask the student to interpret MBR, GPT, FAT or `$MFT` structures — those are Session 4** and the
   student has not met them. This was a real forward-dependency error; do not reintroduce it.

---

## 4 · The three animations to build (`D51` — click-to-play, no autoplay, no loop)

1. **The volatility ladder (p5).** On play, the rungs drain top-down at visibly different rates —
   CPU/RAM gone in seconds, network state in minutes, disk persisting. The animation *is* the
   argument for the collection order. Show a half-life beside each rung.
2. **The verification chain (p14).** Source → read → write → hash. On play the tick travels and
   **stops on the write-and-read-back link**, leaving the source link visibly unproven. This is
   the single most misunderstood idea in the session; the motion is what fixes it.
3. **The hidden area (p9).** The reported disk shrinks to the OS-visible size while the true
   extent stays outlined — the shaded gap is HPA/DCO.

Cross-fade shapes for colour change; **SMIL cannot interpolate `var()`**.

---

## 5 · What Session 1 already owns — name it, never re-explain it

| Idea | Owned by | What you may do |
|---|---|---|
| hashing, `sha256sum -c` | `S1-06` | use it; one clause of reminder at most |
| chain of custody | `S1-07` | fill the form; do not re-teach the fields |
| write blocking | `S1-08` | apply it to the source disk; do not re-explain hardware vs software |
| the report template + rubric | `S1-04` | reference it; do not restate the ten sections |
| hex and magic bytes | `S1-09` | **apply** it at your page 15 on a real image |

✅ **One deliberate exception.** The word `verified` is taught twice **on purpose** — S1 reads it
in a log it was *handed*, you read it in a log the student *produced*. They are different lessons.
Say so explicitly. Everything else that overlaps is a defect.

🔴 **The old page's worst failure was here:** *"memory comes first"* appeared in **six** places and
*"`verified` checks the tool's own output"* in **eight**. One idea, said once, then used.

---

## 6 · What to take from the previous instructor's material

Source: `knowledge_base/instructor/Session_01_Introduction_and_Acquisition.md`.

**Take — his acquisition lab is the best thing he built:** image → verify → RAM → logical/AD1 →
mount → triage as one continuous run, including his **three-tool mount comparison** where
Arsenal's *"write original"* option sits on screen as a selectable choice. That single screen
teaches write-protection better than a paragraph does.

**Fix:**
- ❌ The old build said *"run the live-response collector"* and **never named a tool.** Name
  **BriMor Labs Live Response Collection** (`Windows_Live_Response.bat`, menu: Triage / Memory /
  Complete) and give **Velociraptor** (Apache 2.0) as the free-for-commercial-use alternative.
- ❌ His *"triage = three images"* is wrong. Triage is a targeted subset.
- ❌ `dd` and HashCalc appear in his lab agenda and are never demonstrated.

---

## 7 · What Session 3 will need from you

S3 is *Data Representation, Hidden Information & File Examination* — EXIF, steganography,
polyglots, malicious documents, PE analysis. It inherits your **signature-vs-extension** block and
builds on it. End page 22 by pointing at it: *the file is not what its name says — now find what
is hidden inside it.*

---

## 8 · Done means

```
python3 scripts/density_gate.py docs/session-02/index.html     → ALL PASS
node testing/render_gate.js docs/session-02/index.html         → zero findings, 5 widths
```
Report as numbers: words before → after, worst page, pages without a visual, animations built, and
**which pages are provisional pending evidence acquisition**.
