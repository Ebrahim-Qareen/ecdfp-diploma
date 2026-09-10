# P14 — Timelines and the final report · build log  (the capstone)

**Topics** `T24` Logs & Super-Timelines (45) · `T25` Final Report & Capstone (40) — **85 minutes**
**Page** `docs/page-14/index.html` — 21 screens, 6 part dividers — shape v2 (`D136`)
**Built** 2026-09-09 — **the diploma is complete: 14 of 14 pages live**

| | |
|---|---|
| Stepped figures | **4** — `F1` five sources → one axis · `F2` normalise then pivot · `F3` catching a liar · `F4` the twelve-section report |
| SIMSCREEN | **1** — `ss-t24`, plaso: build, normalise, pivot, read the incident |
| Lifecycle stage | **4·VALIDATE + 5·PRESENT** — the only page that sits at two, because the timeline IS validation and the report IS present |
| Evidence | `EVS-09` — one coherent incident timeline, Tier 3, consistent with EVS-08/12/13/14 |

## Why this page is different

Every other page taught an artifact. This one teaches the **two acts that turn thirteen piles of findings into a
case**: merging them onto one clock (the super-timeline) and writing them down (the report). Nothing here is new
evidence — it is the **discipline** every page rehearsed, applied to all of them at once.

## The timeline is a real, coherent incident

`EVS-09` is not a fresh corpus — it is an eleven-row plaso-style super-timeline whose every row is drawn from the
**same artifact types** the diploma already read, referencing the **same evidence** (the C2 `sync-check.net`, the
IP `185.220.101.7` from `EVS-08`; the host and Mountain timezone from `EVS-12`). So a student can trace any row
back to the page that taught its artifact. The incident:

phish (12:20) → **click (12:24:03) → execution + Run-key persistence in the same second (12:24:07) → first beacon
(12:24:20)** → pass-the-hash logon (12:26:29) → DNS + HTTP exfil (12:28–12:30) → Recycle-Bin cleanup (12:31) →
System and Security logs cleared (12:34–12:35).

The pedagogical peaks: **causation lives in the order** (a chain no single source shows), and **the nine rows
above the log-clears survived because they live off the event logs** — the timeline reconstructs the window the
attacker tried to erase. `F3` generalises it: a timestomp is caught because `$STANDARD_INFORMATION` and
`$FILE_NAME` disagree; faking one artifact does not fake the others. That is stage-4 VALIDATE at full scale.

## The report, and the one rule

`T25` assembles the twelve-section report every page's report-stage was feeding. The page is explicit that only
**three** sections are forensics — **7 Findings, 8 Timeline, 10 Limitations** — and that the whole diploma
collapses to one writing rule, stated in the final key-takeaway:

> **State the claim in the verb the evidence supports, cite the artifact, give your confidence, and name the
> limit — never one adjective past the bytes.**

The capstone exercise is writing Section 7 and Section 10 for `EVS-09`, and the **assessment is a peer review**
whose single question is *"is any claim one adjective past its evidence?"* — the one habit the diploma exists to
build.

## Real tools

`EVS-09` is built by `scripts/make_evs09.py` (deterministic, byte-reproducible) and the SIMSCREEN shows real
plaso/psort `l2tcsv` layout. Event counts are what a real image yields; the eleven pivoted rows are the real
timeline, read verbatim.

## Gates

```
python3 scripts/density_gate.py docs/page-14/index.html      ALL PASS
node testing/render_gate.js docs/page-14/index.html          PASS — zero findings
```

**All 14 pages pass both gates. The homepage and roadmap show 14 of 14 live, zero planned.**
