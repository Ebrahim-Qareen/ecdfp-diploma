# Session 2 — gate report (Part 8 step 0 + brief §13 steps 1–2)

**Run 2026-09-06.** Nothing has been built. This file records the evidence gate result and every
contradiction found between `design/session_02_build_prompt.md` and the repository as it stands.

---

## 1 · The evidence gate — ⛔ FAIL. Session 2 cannot start.

`ecdfp-evidence` called. `design/evidence_sets.md` (last written 2026-08-30) and the filesystem agree:

| Set | Needed by | Status |
|---|---|---|
| `EVS-01` — Case 01 seizure package | S1 | ✅ **verified 2026-08-30** (`D54`), Tier 1 |
| `EVS-02` — `EVI-SRC01` disk image, E01 **and** raw | `S2-05` `S2-06` | ⛔ **not started** |
| `EVS-03` — memory capture from `EVI-SRC01` | `S2-03`, and `S6-10` later | ⛔ not started |
| `EVS-04` — the suspect USB image | `S2-08` `S2-09` `S2-10` | ⛔ not started |
| `EVS-09` — triage collection set | `S2-07` | ⛔ not started |

`evidence/` does not exist on disk at all. `scripts/` holds `make_evs01.py` only.
Four of the ten blocks cannot be written until these exist, because the outline depends on what the
evidence actually contains. **No theory pages are being built meanwhile** (brief §4).

### 🔴 But the brief's reason is out of date, and that changes the decision

The brief (§4 and §14 item 4) says Tier 1 is blocked because `labs/` does not exist and `FOR-WS01`
has never been built. **That has not been true since 2026-09-04.**

| Brief says | Reality on disk, 2026-09-06 |
|---|---|
| `labs/` does not exist | `labs/` exists: `setup_guide.md`, `kali_setup.md`, `kali_setup.sh`, `vm_notes/` |
| `FOR-WS01` unbuilt | **Built and verified 2026-09-04.** `verify_tools.ps1` 25/25 PASS, snapshot `CLEAN-TOOLS` |
| — | **`EVI-SRC01` victim built 2026-09-05.** Win 10 Pro, host `FIN-WKS-07`, snapshot `VICTIM-CLEAN` with VSS restore point, LibreOffice, 7-Zip and seeded benign data |
| — | **Kali tooled 2026-09-06:** `plaso 20260119`, `dc3dd 7.3.1`, Sleuth Kit 4.14.0, foremost, bulk_extractor, tcpdump |
| `D40`'s `F7` unsettled (§14 item 5) | **`F7` LOCKED 2026-09-06** — six numbered stages across named hosts, in `labs/vm_notes/staging_plan.md`. Still needs the SVG and a dated `DECISIONS.md` row |

**So Tier 1 is available, not blocked.** The only thing standing between here and `EVS-02/03/04/09`
is that **staging Phases C and D of `labs/vm_notes/staging_plan.md` were deferred by the instructor.**

---

## 2 · 🔴 Two case-narrative contradictions that must be settled *before* staging

These are not build details. Phase B3 sets file and log times on the victim VM; once the machine is
staged, changing either answer means re-staging.

### 2.1 The case dates collide

| Source | Date |
|---|---|
| `EVS-01` / `scripts/make_evs01.py` — case `ITG-2026-014` | seizure **2026-03-03**, acquisition of `EVI-SRC01` **2026-03-04 09:14 UTC** |
| `F7`, locked 2026-09-06 | attack window **24–26 Aug 2026**, discovered ~1 week later |

Same host, same case, two timelines eight weeks apart. `EVS-01` is already **published and verified**
and its SHA-256 values are the manifest students check against — retiming it means regenerating it
and reissuing the hashes.

### 2.2 S1 says no memory was captured; S2 is built on capturing memory

`EVS-01`'s exhibit inventory, item `ITG-2026-014-A3`, records that the first responder's notes
**"record that no memory capture was taken"**, and the seizure package has the host powered down.

The brief §10 says: *"live response first where the host is still running, then memory, then the
disk"*, and `EVS-03` is defined as *a memory capture from `EVI-SRC01`*. Both cannot be true of the
same machine in the same case.

Three ways out, all Ebrahim's call:

1. **Keep S1 as written and make it the lesson.** The responder lost volatile data — which is
   exactly what `S2-01` (order of volatility) and `S2-02` teach. `S2-02`/`S2-03` then run on the
   **student's own VM** (the §8 micro-lab table already says "their own VM" / "their own RAM"), and
   `EVS-03` is dropped or re-scoped to a lab capture that is not part of the case. ⚠️ `S6-10` needs
   `EVS-03` for Volatility in the capstone — check that first.
2. **Retime and rewrite `EVS-01`** so the host was found running and memory *was* captured.
   Cost: regenerate `EVS-01`, reissue both manifests, update `D54` and the S1 package.
3. **Split the case:** `EVI-SRC01` was powered down (S1), and a *second* still-running host supplies
   the live-response and memory evidence. Cost: a fourth VM, and it weakens the one-image `D19` spine.

---

## 3 · `FOR-LNX01` does not exist in the built lab

`S2-07` is *"`dc3dd` on `FOR-LNX01`"* in the brief §5, in `design/topic_map.md` line 80, in
`00_INSTRUCTIONS.md` Part 6, and already published on `docs/roadmap.html` and
`docs/session-02/brief.html`.

The lab that was actually built has **no `FOR-LNX01`**. The instructor's existing **Kali** VM is the
Linux machine, and `dc3dd 7.3.1` is installed there.

⚠️ And `F7` makes that same Kali host the **receiving end of the lateral movement and exfiltration**,
declared *not examined* as a stated limitation (`D38`). Using the compromised host as the analyst's
acquisition workstation in `S2-07` is a contradiction students will spot.

Options: rename `FOR-LNX01` → Kali across the map, brief pages and Part 6 and accept the dual role
with a stated limitation; or run `S2-07` from a clean Kali snapshot taken before staging; or move
`dc3dd` onto a small dedicated Linux VM.

---

## 4 · Smaller items confirmed, no decision needed

| | |
|---|---|
| `ecdfp-case` still **not installed** — 7 of 8 skills (`ListSkills` shows intake, evidence, session-package, session-html, publish, pdf-extract, web-extract) | S2 has **two** investigations (`S2-08`, `S2-09`) and no skill behind `cases/case-02*` |
| `D51`–`D55` all present in `DECISIONS.md` (lines 67–71) | brief §2 correct |
| S2's 10 rows in `design/topic_map.md` match the brief §5 exactly; minutes total **205** (130 + 60 + 15) | ✅ |
| `docs/session-02/brief.html` and `record.html` exist and must not be overwritten | ✅ confirmed |
| `scripts/gen_session_record.py` already carries S2 step data | ✅ confirmed |
| `Resources/LABS/thm-free-labs.md` and `cyberdefenders-free-labs.md` exist | ✅ |
| `DECISIONS.md` duplicate rows `D45`–`D50` (six pairs) | cite by date **and** subject |

---

## 5 · The decision this report is waiting on

**A — Tier 1 (recommended).** Run staging Phases C and D per `labs/vm_notes/staging_plan.md`:
stage the compromise on `EVI-SRC01`, capture memory and triage (`EVS-03`, `EVS-09`), power down and
image the disk E01 + raw (`EVS-02`), image the suspect USB (`EVS-04`), then hash, verify and write
manifests through `ecdfp-evidence`. This is the plan already locked, and it is also the origin of
every artifact in S3–S6 (`D19`), so it is the critical path for four more sessions, not just this one.

**B — Tier 2 (NIST CFReDS, `D36`).** Link a public image set, never rehosted. S2 gets built now, but
`S2-06`, `S2-08` and `S2-09` stop being the case: the images are not `EVI-SRC01`, so the carry-through
chain breaks exactly where the brief §10 says the course depends on it. CFReDS also does not supply a
memory capture matched to its disk images.

**C — Defer S2 and build a different session.** No session S3–S6 has evidence either, so this only
moves the block.

---

## 6 · Decisions taken 2026-09-06 (Ebrahim, via the build session)

| Fork | Choice | Logged |
|---|---|---|
| Evidence tier | **Tier 1 — run the acquisition** per `labs/vm_notes/acquisition_runbook.md` | `D57` |
| S1 timeline / memory | **Keep S1 byte-for-byte; make the volatile-data loss the lesson.** Memory IS captured from the incident host so `EVS-03` survives for S6 | `D57` |
| `FOR-LNX01` | **Clean Kali snapshot** for `S2-07`; rename `FOR-LNX01` → Kali across the map/pages | `D56` |

**Consequence:** the outline (`design/session_02_outline.md`) is written and awaiting approval (D9). The
package/figures/page build starts once (a) the outline is approved and (b) the acquisition runbook has been
run and the real `EVS-02/03/04/09` hashes pasted into `evidence_sets.md`. Until then Part 8 step 0 stays
FAILED and no student-facing S2 material ships.
