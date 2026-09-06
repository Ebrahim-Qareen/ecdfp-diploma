# coverage_matrix.md — eCDFP Diploma

**★ LOCKED.** Transcribed from Part 4 of `00_INSTRUCTIONS.md`. This file is not a plan — it is the
locked roadmap. Nothing here changes without a new dated row in `DECISIONS.md`.

`topic_map.md` is measured against this file. Where the two disagree, this one is right and the
topic map is wrong.

---

## 1 — The locked roadmap · 6 × 4 h = 24 h (D1)

| # | Session | INE | Primary domain | Lab / evidence | Case file |
|---|---|---|---|---|---|
| **S1** | **Forensic Foundations, Evidence Integrity & Chain of Custody** | M1 intro | Fundamentals + Preservation | build **FOR-WS01**, install tool set, snapshot `CLEAN-TOOLS`, hashing + CoC form + write-blocking | verify 4 files against a manifest — find the tampered one |
| **S2** | **Acquisition — Disk, Memory & Live Response** | M1 | Preservation + Storage | FTK Imager · `dc3dd` · order of volatility · memory capture · KAPE triage · E01 vs raw vs AD1. **Image EVI-SRC01 → the carry-through case is born** | suspect USB: acquire, verify, document |
| **S3** | **Data Representation & File Examination** | M2 | Fundamentals | hex, magic bytes, headers/footers, EXIF, metadata, malicious documents, file signature vs extension | 12 renamed / corrupted files — identify each by header |
| **S4** | **Storage Devices, Partitions & File Systems** | M3 | Storage | HDD/SSD internals · sectors, clusters, slack · MBR vs GPT · FAT vs NTFS · `$MFT` · ADS · carving · deleted data | wiped partition table — recover it and prove the recovery |
| **S5** | **Windows Forensics — Registry, User Activity & Execution** | M4 | Fundamentals | hives · RegRipper · Registry Explorer · USB history · shellbags · prefetch · amcache · LNK · jumplists · recycle bin · VSS | which USB, which user, which program ran, when, how many times |
| **S6** | **Network Forensics, Timelines, Reporting & Capstone** | M4 + M5 | Tools & Techniques | Wireshark · tcpdump · network file carving · plaso super-timeline · report structure | **full capstone:** image + memory + pcap → written forensic report |

---

## 2 — Domain coverage matrix (verified)

| Domain | Class hours | Class % | Exam % | Δ |
|---|---|---|---|---|
| Fundamentals of Digital Forensics | 8.00 | 33.3 % | 33 % | +0.3 |
| Digital Forensics Tools & Techniques | 6.50 | 27.1 % | 27 % | +0.1 |
| Preservation of Evidence | 5.00 | 20.8 % | 20 % | +0.8 |
| Storage Device Fundamentals | 4.50 | 18.8 % | 20 % | −1.2 |
| **Total** | **24.00** | **100 %** | **100 %** | — |

---

## 3 — Per-session domain split (hours)

Every session reserves **0.25 h** for the hash-verify + chain-of-custody closing ritual
(Preservation), and **0.75 h** minimum of timed tool repetitions (Tools & Techniques).

| | Fundamentals | Tools | Preservation | Storage | Total |
|---|---|---|---|---|---|
| **S1** | 1.50 | 0.75 | 1.75 | — | 4.00 |
| **S2** | — | 0.75 | 2.25 | 1.00 | 4.00 |
| **S3** | 2.50 | 0.75 | 0.25 | 0.50 | 4.00 |
| **S4** | — | 0.75 | 0.25 | 3.00 | 4.00 |
| **S5** | 3.00 | 0.75 | 0.25 | — | 4.00 |
| **S6** | 1.00 | 2.75 | 0.25 | — | 4.00 |
| **Total** | **8.00** | **6.50** | **5.00** | **4.50** | **24.00** |

### How this maps onto real teaching minutes

The split above allocates the **full 4-hour slot** (240 min). The teaching budget is **220 min**
(D15), of which 15 min is the break — so **205 min per session is topic time**, and each session
carries ~20 min of slack. `topic_map.md` is built against the 205, and its domain proportions are
reconciled against the percentages in §2 — not against the raw hours, which include the break.

**Scaled per-session targets (205 min of topic time):**

| | Fundamentals | Tools | Preservation | Storage |
|---|---|---|---|---|
| **S1** | 77 | 38 | 90 | — |
| **S2** | — | 38 | 115 | 51 |
| **S3** | 128 | 38 | 13 | 26 |
| **S4** | — | 38 | 13 | 154 |
| **S5** | 154 | 38 | 13 | — |
| **S6** | 51 | 141 | 13 | — |

---

## 4 — What 24 hours costs you — accepted consciously

- **Memory forensics is compressed** into S2 (acquisition) + S6 (analysis in the capstone). It does
  not get its own session. **Mitigation:** Volatility 3 is a **homework track**, with a graded
  homework case in S5 and S6.
- **Linux / macOS forensics is out of scope.** Recorded in `scope_decisions.md`. eCDFP is
  Windows-weighted; say so to students explicitly.
- **Anti-forensics is not a session.** It is a mandatory caveat box inside every artifact (R10) —
  timestomping, wiping, log clearing, encryption.
- **Storage is 1.2 pp under weight.** **Mitigation:** WinHex / hex practice is the homework in both
  S3 and S4.

---

## 5 — Ordering rule

**Do not reorder without a decision row.**

```
integrity  ->  acquisition  ->  analysis
storage    ->  file systems ->  Windows artifacts
timelines and reporting LAST
```

A timeline needs every earlier artifact to mean anything. That is why S6 is last and why nothing
moves ahead of it.
