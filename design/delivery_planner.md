# delivery_planner.md — how a session gets built on the day

**GENERATED from `design/topic_map.md` — never hand-edit.** Regenerated 2026-09-08.

`D79` made the session a **container**: the topic is the unit, and you decide on the day how many
topics the clock allows. This file is what you read to make that decision. `D86` replaced six
per-session plans with this one file, because a plan for a session composed that morning cannot be
written in advance.

---

## The clock

| | Minutes |
|---|---:|
| Slot | 240 |
| Teaching | 220 |
| Break — **at a topic boundary, inside the first two hours, never mid-topic** | 15 |
| Integrity close — hash-verify + chain-of-custody sign-off, **every session** | 15 |
| **Topics** | **190** |
| Unallocated slack | 20 |

**Hard ceiling 210 topic minutes** (190 + the slack). Above that, move a topic to the next day.
A second break is your call and is not budgeted.

---

## Every topic, in order

Take them **in this order**. It is dependency-verified (`D80`) and `scripts/order_gate.py` refuses
any other sequence.

| ID | Topic | Page | Min | Needs first | Evidence |
|---|---|:-:|---:|---|---|
| **`T01`** | Foundations & Forensic Principles | `P01` | 45 | — | — |
| **`T02`** | The Forensic Report | `P01` | 25 | `T01` | — |
| **`T03`** | Evidence Integrity — Hashing, Chain of Custody, Write Blocking | `P02` | 38 | `T01` | `EVS-01` |
| **`T04`** | Inside a File — Hex, Magic Bytes & Signatures | `P03` | 82 | `T03` | `EVS-05` · `EVS-01` |
| **`T05`** | Data Representation & Metadata | `P03` | 35 | `T04` | `EVS-10` |
| **`T06`** | Live Response — Order of Volatility | `P04` | 25 | `T01` | — |
| **`T07`** | Memory Forensics — Acquire and Analyse | `P04` | 35 | `T06` | `EVS-03` |
| **`T08`** | Imaging Scope & Formats | `P05` | 33 | `T07` | — |
| **`T09`** | Imaging Tools — FTK Imager & dc3dd | `P05` | 112 | `T03` · `T04` · `T08` | `EVS-02` · `EVS-09` · `EVS-05` · `EVS-04` |
| **`T10`** | Hidden Data & Image Forensics | `P06` | 80 | `T05` · `T09` | `EVS-10` · `EVS-05` |
| **`T11`** | Malicious Documents & Executables | `P07` | 75 | `T05` · `T10` | `EVS-06` |
| **`T12`** | Storage Internals & Slack | `P08` | 45 | — | `EVS-02` |
| **`T13`** | Partitioning — MBR & GPT | `P08` | 68 | `T12` | `EVS-02` · `EVS-07` |
| **`T14`** | File Systems — FAT & NTFS | `P09` | 52 | `T12` | `EVS-11` ✅ built |
| **`T15`** | Carving & Deleted Data | `P09` | 25 | `T12` | `EVS-11` ✅ built |
| **`T16`** | Registry Structure & System Configuration | `P10` | 28 | `T14` | `EVS-02` |
| **`T17`** | USB & Device History | `P10` | 35 | `T16` | `EVS-02` · `EVS-04` |
| **`T18`** | Evidence of Execution | `P11` | 40 | `T16` | `EVS-02` |
| **`T19`** | User Activity — Shellbags, Recycle Bin, VSS | `P11` | 38 | `T16` · `T17` | `EVS-02` |
| **`T20`** | Windows Event Logs | `P12` | 49 | `T16` · `T17` · `T18` | `EVS-02` · `EVS-04` |
| **`T21`** | Network Evidence & Traffic Analysis | `P13` | 42 | — | `EVS-08` |
| **`T22`** | C2 & Attack Patterns in Traffic | `P13` | 28 | `T21` | `EVS-08` |
| **`T23`** | Internet & Email Artifacts | `P13` | 20 | `T16` | `EVS-02` |
| **`T24`** | Logs & Super-Timelines | `P14` | 45 | `T14` · `T20` | `EVS-02` · `EVS-08` |
| **`T25`** | Final Report & Capstone | `P14` | 40 | `T02` | `EVS-02` |

---

## Suggested composition — **7 sessions**

Balanced so no day runs over. **A suggestion, not a schedule** — recompose freely, the only rules
are the order above and the 210-minute ceiling.

| Session | Topics | Topic min | Load |
|---|---|---:|---|
| **S1** | `T01` · `T02` · `T03` | 108 | **light — room for deeper lab time** |
| **S2** | `T04` · `T05` · `T06` · `T07` | 177 | comfortable |
| **S3** | `T08` · `T09` | 145 | **light — room for deeper lab time** |
| **S4** | `T10` · `T11` | 155 | comfortable |
| **S5** | `T12` · `T13` · `T14` · `T15` | 190 | full |
| **S6** | `T16` · `T17` · `T18` · `T19` · `T20` | 190 | full |
| **S7** | `T21` · `T22` · `T23` · `T24` · `T25` | 175 | comfortable |
| | | **1140** | |

**Why 7 and not 6.** `1140 ÷ 190 = 6.0` only with perfect packing. Topics are indivisible and the
order is fixed, so the real answer is **7 × 4 h = 28 hours** (`D98`) — which is what `D70`'s
valve exists for, and is inside its ceiling of eight.

---

## Before a session

1. **Evidence** — every set the day's topics name is `verified` in `design/evidence_sets.md`.
   Not verified → that topic does not run (`D91`).
2. **Order** — `python3 scripts/order_gate.py` passes.
3. **Break** — pick the topic boundary it falls on, inside the first two hours. Write it on the board.
4. **Case 06** — released at the close of the **fifth session** as a graded take-home (`D59`),
   debriefed in `T25`. This is a calendar event, not a topic.
5. **The report** — every student's single growing report (`D85`) is open from `T01` to the end.
