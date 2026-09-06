# evidence_sets.md — eCDFP Diploma

**Owned by `ecdfp-evidence`.** No other skill assigns an `EVS-` ID or marks a set verified.
Part 8 step 0: **a session whose evidence set is not verified and hashed does not start.**

**`R9` — the repo carries the manifest, never the bytes.** No image, dump, hive or raw pcap is
committed. Generators write outside the project tree; the mount cannot delete (Part 10), so a
stray file inside it is permanent.

---

## Sourcing tiers

| Tier | What | Rule |
|:-:|---|---|
| **1** | Our own lab acquisitions | primary. One `EVI-SRC01` image feeds S2–S6 at increasing depth (`D19`) |
| **2** | Public corpora — NIST CFReDS, Digital Corpora, published challenges | **linked and credited, never rehosted** (`D22`). Licence checked before use |
| **3** | Synthesized | narrow: pcap, syslog/NDJSON/web logs, artifact **exports** (CSV/JSON). 🔴 **Never** `.evtx`, E01/AD1/raw, memory dump or registry hive — a fabricated hive is a lie about what a forensic artifact looks like |

---

## The sets

### `EVS-01` — Session 1 · the manifest set

| Field | Value |
|---|---|
| **Name** | EVS-01 — Case 01 seizure package |
| **Tier** | **1** — generated in our own lab |
| **Source** | `scripts/make_evs01.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no third-party material, no external corpus |
| **Format** | 4 × UTF-8 plain text (LF), 2 × checksum manifest |
| **Size** | 6 144 B total · 587–2 303 B per file |
| **Contains** | a first responder's contemporaneous notes · an imaging tool's acquisition and verification log · a completed chain-of-custody record · a three-row exhibit inventory |
| **Session** | S1 (`S1-06`, `S1-07`, `S1-09`, `S1-10`) |
| **Date verified** | **2026-08-30** — hashes computed from the generated files, not copied from anywhere |

**🔴 One file is deliberately altered after the manifest is computed.** That is the exercise.

| # | File | Bytes | State as distributed |
|--:|---|--:|---|
| 1 | `seizure_notes.txt` | 2 303 | clean |
| 2 | `EVI-SRC01_acquisition_log.txt` | 1 340 | 🔴 **altered — one character** |
| 3 | `custody_form_EVI-SRC01.txt` | 1 914 | clean |
| 4 | `evidence_inventory.csv` | 587 | clean |

**The alteration:** `Acquisition started : 2026-03-04 09:14:0` **`2`** ` UTC` → `…09:14:0` **`3`** ` UTC`.
One character. Invisible to the eye, total to the digest.

**Why that file.** It is the file whose *content is the integrity claim* — the one containing the
word `verified`. The catch lands exactly where students reliably fail: *"verified" means the tool
checked its own output.*

#### Manifest — SHA-256 (the values students verify against)

```
ee62e8b1396c7c3d4d3349817dc02cc67fc9fe733eba522090e300665c7a81a1  seizure_notes.txt
f05bfee856c578d50af2302f0bd09f4260e8f8b7617f9162340458cb457171d7  EVI-SRC01_acquisition_log.txt
bb8ea1983fa7a64e738ba7f52fdd905467e0a9db3a0abd1acc0d3746bfcc0adc  custody_form_EVI-SRC01.txt
acc6c87547f0661f739670ef35dd2cfee5290ff4457c3b3d2119b209eb9a29ee  evidence_inventory.csv
```

#### Manifest — MD5 (recorded as a lookup key, never as the integrity control)

```
5127e6d1609da0e140d9483d2198852e  seizure_notes.txt
c9dfb4b8c20095c9f739359b43812515  EVI-SRC01_acquisition_log.txt
a3f69f666078c94d84351ee656e42001  custody_form_EVI-SRC01.txt
11a85407fa5b9cdd2950b1ae71e55838  evidence_inventory.csv
```

#### 🔴 Answer key — instructor only

The digest the **distributed** (altered) file actually computes to:

| Algorithm | Value |
|---|---|
| SHA-256 | `7eda34b36f53700bb3e0c4cd85c6c026b4c67982d7f7c2375fa8540af4bfb3c6` |
| MD5 | `2f3858969b36fc4f06efad19a5e973b1` |

A correct `F-01` quotes **that** value against the manifest's
`f05bfee8…`, names both, and stops there.

#### Verified by running it

```
$ sha256sum -c EVS-01.sha256
seizure_notes.txt: OK
EVI-SRC01_acquisition_log.txt: FAILED
custody_form_EVI-SRC01.txt: OK
evidence_inventory.csv: OK
sha256sum: WARNING: 1 computed checksum did NOT match
```

`md5sum -c EVS-01.md5` gives the same three OK and the same one FAILED.
Regenerated to a second path and diffed: **byte-identical** — the generator is deterministic
(fixed seed `20260304`, fixed base date `2026-03-04`), so a student's copy is diffable against
the instructor's.

#### What it deliberately does not contain

No real personal data · no real company · no real malware · no credential of any kind · no IP
address at all. The narrative carries the case without any of it, which is what `D41` requires:
**no question in this set has a secret or a person's data as its answer.**

#### Distribution

Published by the end of the session before (`D18`) with **both** hashes. Students verify before
class; a mismatch is a finding, not an inconvenience. The instructor holds a prepared fallback
USB set, re-verified before each session that needs it.

Regenerate with:

```
python3 scripts/make_evs01.py --out <a path OUTSIDE the repo>/EVS-01
```

---

### Session 2 sets — design LOCKED, manifests PENDING acquisition

**Status 2026-09-06.** The staging + acquisition (`labs/vm_notes/acquisition_runbook.md`, Phases C-D of
`staging_plan.md`) has not been run yet, so **no real hashes exist and none are invented** (Tier 1 rule:
E01, memory dump and USB image are never synthesised). Each set below is fully specified; the instructor
runs the runbook, then the two hashes per artifact are pasted in and the row is marked **verified** with the
date the check was actually run. **Part 8 step 0 stays FAILED for S2 until that happens.**

Source host for all four: exhibit **`EVI-SRC01`** = Windows host **`FIN-WKS-07`** (the built victim VM,
Meridian Retail Group / `l.bennett`). Attack window **24-26 Aug 2026**, acquired ~1 week later (`D57`).

| ID | Tier | Source | Format | Contains | Session | MD5 / SHA-256 | Verified |
|---|:-:|---|---|---|---|---|---|
| `EVS-02` | **1** | our lab — image of `FIN-WKS-07` system disk after power-down, on a write blocker | **E01** (compressed, per-chunk CRC + embedded hash) **and** raw `dd` | full system disk: OS, `l.bennett` profile, persistence, `$MFT`, USBSTOR history, cleared event logs, one timestomp | `S2-05` `S2-06` `S2-09` (and S3-S6) | ⛔ PENDING | ⛔ |
| `EVS-03` | **1** | our lab — live memory capture of `FIN-WKS-07` **before** power-down | raw memory image (`.raw`/`.mem`) + tool log | running processes, network connections, injected code, the C2 beacon in memory | `S2-03` · `S6-09` · `S6-10` | ⛔ PENDING | ⛔ |
| `EVS-04` | **1** | our lab — image of the suspect USB device | **E01** + raw | the staged `customer_export` archive, exfil artefacts, USB volume + file-system structure | `S2-08` `S2-09` `S2-10` | ⛔ PENDING | ⛔ |
| `EVS-09` | **1** | our lab — targeted triage collection from `FIN-WKS-07` (live) | KAPE/triage output tree + per-file hash list | key artefacts only (registry hives, event logs, prefetch, `$MFT`) as a triage set, not a full image | `S2-07` | ⛔ PENDING | ⛔ |

**Reconciliation with `topic_map.md`:** the map's provisional `EVS-05`..`EVS-09` are unchanged; `EVS-09`
is bound here to the S2 triage set. No IDs moved.

**Licence / IP notes for the S2 sets:** all Tier 1, ours, no third-party material. Fictional company and
users, documentation IPs only, no real malware, no real credentials (`D19`, `D41`, `R8`/`R9`). The USB
`customer_export` is benign decoy content seeded on the victim's Data drive (`seed_victim.ps1`).

---

### Reference — original placeholder table (superseded by the block above)

### Not yet built

| ID | Session | What it needs to be | Status |
|---|:-:|---|---|
| `EVS-02` | S2 | `EVI-SRC01` disk image (E01 + raw) | ⛔ **not started** — blocks S2 (Part 8 step 0) |
| `EVS-03` | S2 | memory capture from `EVI-SRC01` | ⛔ not started |
| `EVS-04` | S2 | the suspect USB device image | ⛔ not started |
| `EVS-05`–`EVS-09` | S3–S6 | provisional IDs in `topic_map.md`; reconcile here when built | ⛔ not started |

⚠️ **`EVS-02` is the critical path.** S2 cannot begin without it, and it is a real acquisition
from a real staged host — not a text file.

⚠️ **The Drive `Cases/` folder is not a source until its provenance is established.** Six
folders whose contents were never enumerated; if they are copies of public corpora, `D22` says
link and credit, never rehost.
