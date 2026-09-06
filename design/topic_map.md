# topic_map.md — eCDFP Diploma

**One row per topic.** Built 2026-08-28 from `coverage_matrix.md` (the locked Part 4 roadmap) and
`scope_decisions.md` (the Part 12 answers). Measured against the matrix, not the reverse — where the
two disagree, the matrix is right and this file is wrong.

**The budget (D15 · D23).** Every session is 240 min of slot and **220 min of teaching**: 15 min break plus
**205 min of topic time**, split 130 integrated · 60 blocked investigation · 15 hash-verify and
chain-of-custody close. Every session below totals **exactly 205 + 15 = 220**. Nothing overflows, so
nothing was re-split (D26).

**Rule.** If a session ever exceeds 220, it is re-split *here* and the instructor is told. Overflow is
never carried into the build (Part 8 step 1).

**Domain codes:** `F` Fundamentals · `T` Tools & Techniques · `P` Preservation · `S` Storage.

---

## Evidence sets referenced

Provisional IDs. `design/evidence_sets.md` (Phase 3, `ecdfp-evidence`) owns the final IDs, licences,
sizes and hashes, and is the only file that may declare a set **verified**. A session cannot start
until every set it names here is verified and hashed (Part 8 step 0).

| ID | Set | Tier | Sessions |
|---|---|---|---|
| `EVS-01` | Integrity starter set — 4 files + signed manifest, one tampered | 3 · synthesized | S1 |
| `EVS-02` | **EVI-SRC01 disk image (E01)** — the carry-through incident | 1 · own lab | S2 · S3 · S4 · S5 · S6 |
| `EVS-03` | EVI-SRC01 memory dump | 1 · own lab | S2 · S6 |
| `EVS-04` | Suspect USB image — the exfiltration medium | 1 · own lab | S2 · S4 · S5 |
| `EVS-05` | File-type identification set — 12 renamed / corrupted files | 3 · synthesized | S3 |
| `EVS-06` | The malicious document, extracted from EVS-02 | 1 · own lab | S3 |
| `EVS-07` | Wiped-partition-table image | 1 · own lab | S4 |
| `EVS-08` | C2 beacon + RDP session pcap | 3 · scapy, fixed seed | S6 |
| `EVS-09` | KAPE triage collection from EVI-SRC01 | 1 · own lab | S2 |

---

## S1 — Forensic Foundations, Evidence Integrity & Chain of Custody

`Tier A` · INE **M1 intro** · 10 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S1-01` | What digital forensics is — the mandate, the evidence lifecycle, and what an investigator may not claim | M1 intro | — | 1 | No | 15 | `F` | — |
| `S1-02` | Forensic principles — order of volatility, minimal footprint, repeatability, always work on a copy | M1 intro | S1-01 | 1 | No | 20 | `F` | — |
| `S1-03` | What makes evidence defensible — relevance, authenticity, integrity | M1 intro | S1-02 | 1 | No | 12 | `F` | — |
| `S1-04` | The fixed forensic report template — findings vs interpretation (D7) | M5 | S1-03 | 1 | Yes | 25 | `F` | EVS-01 |
| `S1-05` | Analyst toolkit install and the `CLEAN-TOOLS` snapshot | M1 | pre-built base VM (D17) | 1 | Yes | 20 | `T` | — |
| `S1-06` | Cryptographic hashing for evidence — MD5, SHA-256, what a hash proves and what it does not | M1 | S1-02 | 1 | Yes | 18 | `T` | EVS-01 |
| `S1-07` | Chain of custody — the form and the discipline | M1 | S1-06 | 1 | Yes | 12 | `P` | EVS-01 |
| `S1-08` | Write blocking — hardware vs software, and how to prove one was used | M1 | S1-07 | 1 | Yes | 8 | `P` | — |
| `S1-09` | **[INVESTIGATION]** Case 01 — verify 4 files against a signed manifest, find the tampered one | M1 | S1-06 · S1-07 | 1 | Yes | 60 | `P` | EVS-01 |
| `S1-10` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 1 | Yes | 15 | `P` | EVS-01 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 158 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Fundamentals | 72 | 77 | -5 |
| Tools | 38 | 38 | +0 |
| Preservation | 95 | 90 | +5 |

---

## S2 — Acquisition — Disk, Memory & Live Response

`Tier A` · INE **M1** · 10 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S2-01` | Order of volatility in practice — the collection sequence, and what you destroy by getting it wrong | M1 | S1-02 | 2 | No | 15 | `P` | — |
| `S2-02` | Live response — volatile data collection on a running host | M1 | S2-01 | 2 | Yes | 25 | `P` | EVI-SRC01 live |
| `S2-03` | Memory acquisition — why it comes first, the tools, and the pitfalls | M1 | S2-02 | 2 | Yes | 20 | `P` | EVS-03 |
| `S2-04` | Physical vs logical acquisition — what each captures and what each misses | M1 | S1-02 | 2 | No | 20 | `S` | — |
| `S2-05` | Image formats — E01 vs raw (dd) vs AD1, compression, embedded verification | M1 | S2-04 | 2 | No | 15 | `S` | EVS-02 |
| `S2-06` | FTK Imager — correct use and verification. **Instructor demo: imaging EVI-SRC01** | M1 | S2-05 · S1-06 | 2 | Yes | 20 | `T` | EVS-02 |
| `S2-07` | `dc3dd` on Kali (clean snapshot) and KAPE targeted triage | M1 | S2-06 | 2 | Yes | 15 | `T` | EVS-09 |
| `S2-08` | **[INVESTIGATION]** Case 02a — acquire and verify the suspect USB | M1 | S2-06 | 2 | Yes | 35 | `P` | EVS-04 |
| `S2-09` | **[INVESTIGATION]** Case 02b — examine the acquired image's partition and file-system structure | M1 · M3 | S2-08 | 2 | Yes | 25 | `S` | EVS-04 |
| `S2-10` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 2 | Yes | 15 | `P` | EVS-04 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 155 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Tools | 35 | 38 | -3 |
| Preservation | 110 | 115 | -5 |
| Storage | 60 | 51 | +9 |

---

## S3 — Data Representation & File Examination

`Tier A` · INE **M2** · 10 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S3-01` | How data is represented — bits, bytes, hex, endianness, character encodings | M2 | — | 3 | No | 20 | `F` | — |
| `S3-02` | File structure — headers, footers, magic bytes | M2 | S3-01 | 3 | Yes | 20 | `F` | EVS-05 |
| `S3-03` | File signature vs extension — the mismatch, and what it actually proves | M2 | S3-02 | 3 | Yes | 20 | `F` | EVS-05 |
| `S3-04` | Metadata and EXIF — what it records and how far to trust it | M2 | S3-02 | 3 | Yes | 20 | `F` | EVS-05 |
| `S3-05` | Malicious document structure — OLE and OOXML, embedded objects, macro storage | M2 | S3-04 | 3 | Yes | 25 | `F` | EVS-06 |
| `S3-06` | How a file sits on disk — clusters, and why a header survives a rename | M2 · M3 | S3-02 | 3 | No | 15 | `S` | — |
| `S3-07` | Hex and metadata tooling — HxD/WinHex, ExifTool, TrID | M2 | S3-03 | 3 | Yes | 10 | `T` | EVS-05 |
| `S3-08` | **[INVESTIGATION]** Case 03 — 12 renamed/corrupted files, identify each by header | M2 | S3-03 · S3-07 | 3 | Yes | 35 | `T` | EVS-05 |
| `S3-09` | **[INVESTIGATION]** The carry-through malicious document — structure, embedded objects, metadata | M2 | S3-05 | 3 | Yes | 25 | `F` | EVS-06 |
| `S3-10` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 3 | Yes | 15 | `P` | EVS-06 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 170 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Fundamentals | 130 | 128 | +2 |
| Tools | 45 | 38 | +7 |
| Preservation | 15 | 13 | +2 |
| Storage | 15 | 26 | -11 |

---

## S4 — Storage Devices, Partitions & File Systems

`Tier B` · INE **M3** · 11 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S4-01` | HDD internals — platters, heads, sectors, CHS and LBA | M3 | — | 4 | No | 12 | `S` | — |
| `S4-02` | SSD internals — NAND, wear levelling, TRIM and what it destroys | M3 | S4-01 | 4 | No | 18 | `S` | — |
| `S4-03` | Sectors, clusters and slack — file slack vs volume slack | M3 | S4-01 | 4 | Yes | 20 | `S` | EVS-02 |
| `S4-04` | MBR partitioning — structure, partition table, boot record | M3 | S4-03 | 4 | Yes | 18 | `S` | EVS-07 |
| `S4-05` | GPT partitioning — header, entries, protective MBR | M3 | S4-04 | 4 | Yes | 15 | `S` | EVS-07 |
| `S4-06` | FAT — FAT table, directory entries, and what deletion actually does | M3 | S4-03 | 4 | Yes | 17 | `S` | EVS-04 |
| `S4-07` | NTFS — `$MFT`, resident vs non-resident, ADS, `$LogFile` and `$UsnJrnl` | M3 | S4-06 | 4 | Yes | 20 | `S` | EVS-02 |
| `S4-08` | MFTECmd and Timeline Explorer — parsing `$MFT` to CSV | M3 | S4-07 | 4 | Yes | 10 | `T` | EVS-02 |
| `S4-09` | **[INVESTIGATION]** File carving — PhotoRec/foremost, and carving the staged archive | M3 | S4-07 | 4 | Yes | 25 | `T` | EVS-02 |
| `S4-10` | **[INVESTIGATION]** Case 04 — wiped partition table, recover it and prove the recovery | M3 | S4-05 | 4 | Yes | 35 | `S` | EVS-07 |
| `S4-11` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 4 | Yes | 15 | `P` | EVS-07 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 175 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Tools | 35 | 38 | -3 |
| Preservation | 15 | 13 | +2 |
| Storage | 155 | 154 | +1 |

---

## S5 — Windows Forensics — Registry, User Activity & Execution

`Tier B` · INE **M4** · 10 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S5-01` | Registry structure — hives, keys, values, and where the hives live on disk | M4 | S4-07 | 5 | No | 20 | `F` | EVS-02 |
| `S5-02` | System configuration artifacts — timezone, network, mounted devices | M4 | S5-01 | 5 | Yes | 15 | `F` | EVS-02 |
| `S5-03` | USB device history — USBSTOR, MountedDevices, `setupapi.dev.log` | M4 | S5-02 | 5 | Yes | 20 | `F` | EVS-02 · EVS-04 |
| `S5-04` | Shellbags — folder access that survives deletion | M4 | S5-01 | 5 | Yes | 15 | `F` | EVS-02 |
| `S5-05` | Prefetch — evidence of execution, run count, first and last run | M4 | S5-01 | 5 | Yes | 20 | `F` | EVS-02 |
| `S5-06` | Amcache and ShimCache — presence vs execution, and the classic misreading | M4 | S5-05 | 5 | Yes | 20 | `F` | EVS-02 |
| `S5-07` | LNK files and jumplists — file access, origin volume, and what they prove | M4 | S5-03 | 5 | Yes | 20 | `F` | EVS-02 |
| `S5-08` | **[INVESTIGATION]** Recycle bin (`$I`/`$R`) and Volume Shadow Copies (VSS) — deleted files and previous versions | M4 | S5-07 | 5 | Yes | 25 | `F` | EVS-02 |
| `S5-09` | **[INVESTIGATION]** Case 05 — which USB, which user, which program ran, when, how many times | M4 | S5-03 · S5-05 · S5-07 | 5 | Yes | 35 | `T` | EVS-02 · EVS-04 |
| `S5-10` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 5 | Yes | 15 | `P` | EVS-02 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 185 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Fundamentals | 155 | 154 | +1 |
| Tools | 35 | 38 | -3 |
| Preservation | 15 | 13 | +2 |

---

## S6 — Network Forensics, Timelines, Reporting & Capstone

`Tier A` · INE **M4 + M5** · 11 topics · **205 + 15 break = 220 min**

| ID | Topic | INE source | Prerequisites | Session # | Hands-on? | Est. minutes | Domain | Evidence needed |
|---|---|---|---|---|---|---:|:-:|---|
| `S6-01` | Network evidence sources — pcap, flow, logs, and what each can and cannot prove | M4 | — | 6 | No | 10 | `F` | — |
| `S6-02` | Wireshark for investigators — display filters, follow stream, export objects | M4 | S6-01 | 6 | Yes | 25 | `T` | EVS-08 |
| `S6-03` | `tcpdump` and capture methodology — capture filters, ring buffers, what you lose | M4 | S6-02 | 6 | Yes | 10 | `T` | EVS-08 |
| `S6-04` | Network file carving — NetworkMiner, extracting transferred files | M4 | S6-02 | 6 | Yes | 14 | `T` | EVS-08 |
| `S6-05` | Identifying C2 traffic — beaconing intervals, DNS anomalies, TLS fingerprints | M4 | S6-04 | 6 | Yes | 16 | `T` | EVS-08 |
| `S6-06` | Windows event logs for the timeline — what survives, what is cleared, what is never written | M5 | S5-01 | 6 | Yes | 14 | `F` | EVS-02 |
| `S6-07` | Super-timelines with plaso/log2timeline — build, filter, pivot | M5 | S6-06 · S4-08 | 6 | Yes | 23 | `T` | EVS-02 |
| `S6-08` | The final forensic report — assembling six sessions of findings, with the D20 rubric applied | M5 | S1-04 | 6 | No | 18 | `F` | — |
| `S6-09` | **[INVESTIGATION]** Capstone — full investigation across image + memory + pcap | M4 · M5 | S1–S5 (all) | 6 | Yes | 45 | `T` | EVS-02 · EVS-03 · EVS-08 |
| `S6-10` | **[INVESTIGATION]** Volatility 3 in the capstone — processes, network connections, injected code | M4 | S2-03 | 6 | Yes | 15 | `T` | EVS-03 |
| `S6-11` | **[RITUAL]** Hash-verify + chain-of-custody close | M1 | S1-07 | 6 | Yes | 15 | `P` | EVS-02 |

**Block check** — integrated 130 · investigation 60 · ritual 15 · break 15 = **220 min** (ceiling 220) · hands-on 177 min

**Domain check** vs the scaled target in `coverage_matrix.md` §3:

| Domain | This map | Target | Δ |
|---|---:|---:|---:|
| Fundamentals | 42 | 51 | -9 |
| Tools | 148 | 141 | +7 |
| Preservation | 15 | 13 | +2 |

---

## Reconciliation — the whole course

| Domain | Minutes | This map | `coverage_matrix.md` | Δ | Exam | Δ |
|---|---:|---:|---:|---:|---:|---:|
| Fundamentals of Digital Forensics | 399 | 32.4 % | 33.3 % | -0.9 | 33 % | -0.6 |
| Digital Forensics Tools & Techniques | 336 | 27.3 % | 27.1 % | +0.2 | 27 % | +0.3 |
| Preservation of Evidence | 265 | 21.5 % | 20.8 % | +0.7 | 20 % | +1.5 |
| Storage Device Fundamentals | 230 | 18.7 % | 18.8 % | -0.1 | 20 % | -1.3 |
| **Total** | **1230** | **100 %** | **100 %** | — | **100 %** | — |

Every domain lands within **0.9 pp** of the locked matrix, inside the 1.0 pp tolerance set by D24. The two visible gaps against the *exam*
weights are the ones Part 4 already declared and mitigated:

- **Storage −1.3 pp.** Part 4 accepts −1.2 and mitigates with WinHex / hex practice as homework in
  both S3 and S4. Unchanged here.
- **Preservation +1.5 pp.** Every session spends 15 min on the hash-verify and chain-of-custody
  close (90 min across the course), and S1–S2 are preservation sessions by design. Over-weighting
  the one habit the whole course depends on is deliberate.

---

## Sequencing check

Every prerequisite is satisfied by a topic earlier in this file, and the Part 4 ordering rule holds:

```
integrity (S1) -> acquisition (S2) -> analysis (S3)
storage (S4)   -> file systems (S4) -> Windows artifacts (S5)
timelines and reporting LAST (S6)
```

Three cross-session dependencies are load-bearing and must not be broken by any re-split (D25):

| Depends | On | Why |
|---|---|---|
| `S5-01` registry structure | `S4-07` NTFS `$MFT` | hives are files; you cannot locate or carve them without the file system |
| `S6-07` plaso super-timeline | `S6-06` event logs · `S4-08` `$MFT` parsing | a super-timeline is only meaningful once its inputs are understood |
| `S6-09` capstone | S1–S5, all | the capstone is the whole arc — it introduces no new technique |

---

## Open items for Phase 2

| Item | Blocks | Status |
|---|---|---|
| INE PDFs not yet in `Resources/INE_eCDFP/` | intake, and confirming every topic's INE lesson reference | open |
| Topic-level INE lesson numbers (this map cites modules only) | precision of the References page in each session | open — filled during Phase 2 intake |
| Every `EVS-*` set above is **unverified** | Part 8 step 0 for every session | open — Phase 3 |

**Rule (Phase 2 exit gate).** Any topic with no INE source after intake is a **gap**: it is either
researched with `ceh-web-research` including the tool currency check, or removed from this map. It is
never quietly taught from memory. Gaps are listed in `scope_decisions.md` §7, not hidden here.
