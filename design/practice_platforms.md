# practice_platforms.md — eCDFP Diploma

External DFIR practice students can use between sessions. **Links only.**

**Rules for this file.** Never republish anyone else's material on our site — credit and link
(Part 5, Tier 2: public corpora are linked and credited, never rehosted). Every entry states what it is good for and which session it follows. Nothing here is
required: the graded work is the session homework and the forensic report (D20).

> 🟢🟢 **PARTIALLY VERIFIED 2026-08-29.** The two guided-lab platforms have been enumerated and
> their labs opened individually — **28 labs verified across TryHackMe and CyberDefenders**, each
> probed on its own page under **D45**. They now have their own catalogues, which supersede the
> single-line rows below:
>
> - **`Resources/LABS/thm-free-labs.md`** — 15 free rooms, control-tested tier probe, plus the
>   10 premium rooms worth the instructor's voucher.
> - **`Resources/LABS/cyberdefenders-free-labs.md`** — 13 free labs from 82 free of 255, plus 2
>   rejected after reading them.
>
> ⚠️ **The evidence-corpus, tool-practice and reading rows below are STILL UNVERIFIED.** NIST
> CFReDS, Digital Corpora, the Honeynet Project, Eric Zimmerman's sample data, the Volatility
> Foundation images, the Wireshark captures and the SANS posters have **not** been opened, confirmed
> live, or licence-checked in this pass. **Those rows remain a worklist.**
>
> 🔴 **Licence and classroom-use terms have not been checked for either lab platform** — including
> whether screen-sharing a premium TryHackMe room in a paid class is permitted. **Check before
> session 1.**
>
> **D30 still applies to this file as a whole:** do not link it from `docs/` until the remaining
> rows are verified too.

---

## Evidence corpora — free, citable, licence-checked before use

| Source | Good for | After |
|---|---|---|
| NIST CFReDS | reference images with known ground truth — file carving, deleted data, hashing | S1 · S3 · S4 |
| Digital Corpora | realistic disk and memory images, scenario-based | S2 · S4 · S5 |
| The Honeynet Project challenges | network + memory forensics with published solutions | S6 |

## Tool practice

| Source | Good for | After |
|---|---|---|
| Eric Zimmerman's tools + his sample data | MFTECmd, PECmd, LECmd, Registry Explorer, Timeline Explorer | S4 · S5 |
| Volatility Foundation sample images | memory analysis — the homework track (Part 4) | S5 · S6 |
| Wireshark sample captures | display filters, follow stream, export objects | S6 |

## Guided rooms and labs — 🟢 VERIFIED, see the catalogues

**D46: CyberDefenders is the students' platform; TryHackMe is the instructor's.**

| Source | Good for | After | Verified |
|---|---|---|---|
| **CyberDefenders** — free (Community) labs | full multi-source investigations; **the only free cover we have for `S3`** | S1 · S3 · S4 · S5 · S6 | 🟢 **13 of 82 free labs opened individually** — `Resources/LABS/cyberdefenders-free-labs.md` |
| **TryHackMe** — free rooms | guided repetition; **Volatility Essentials + Windows Forensics 1 are the two spines** | S1 · S2 · S4 · S5 · S6 | 🟢 **15 rooms probed individually** — `Resources/LABS/thm-free-labs.md` |
| TryHackMe — premium rooms | ⚠️ **instructor demonstration only, never assigned** — students have no subscription | S2–S6 | 🟢 tier verified; ⚠️ **classroom licence NOT checked** |

🔴🔴 **Neither platform teaches acquisition.** Every CyberDefenders lab starts from an image someone
else made; TryHackMe's only room that treats acquisition as a judgement is premium. **`S2-01`–`S2-05`
and `S2-09` have no external practice and stay entirely ours.**

## Reading — method, not tooling

| Source | Good for |
|---|---|
| SANS DFIR posters and cheat sheets | artifact location reference — pairs with the 6-box template |
| Vendor documentation for each taught tool | confirming the command shown is still current |

---

## What to practise, by session

| After | Practise |
|---|---|
| **S1** | hash a file, alter one byte, hash again. Write the two-line finding. |
| **S2** | image a small USB, verify, document the chain of custody. |
| **S3** | rename 10 files, identify each by header alone. |
| **S4** | carve deleted files from a sample image and prove the recovery. |
| **S5** | answer "which USB, which user, which program, when" on a sample image. |
| **S6** | build a super-timeline and write the full report against the rubric. |

**The pattern that matters more than any platform:** acquire → verify → analyse → interpret →
document. A practice exercise that skips the hash or skips the write-up is not practice for this
exam.
