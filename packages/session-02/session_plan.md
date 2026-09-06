# Session 2 — Session Plan

**eCDFP Diploma · ITGate Academy**
**Acquisition: Disk, Memory & Live Response**

| | |
|---|---|
| **Session** | 2 of 6 |
| **Slot** | 240 min · 220 teaching · **205 topic minutes** + 15 break (`D15` / `D23`) |
| **INE source** | Module 1 — units 1–2 (acquisition) |
| **Primary domains** | Preservation of Evidence · Techniques of Digital Forensics |
| **Delivery** | integrated theory → demo → **micro-lab after every block**, closing with one blocked investigation hour |
| **Students** | ~5, offline classroom, **every student at a keyboard** (`D16`) |
| **Evidence sets** | `EVS-02` · `EVS-03` · `EVS-04` · `EVS-09` — ⛔ **PENDING acquisition.** See §6 |
| **Case** | Case 02a — acquire and verify the suspect USB · Case 02b — examine its structure |

---

## 1 · Where this session sits

**Session 2 is where the evidence is created.** Every artifact examined in Sessions 3 to 6 is made
here. Say that out loud in the room — it is the reason the acquisition has to be right.

Session 1 ended with the host seized, the evidence verified and the custody record open. Its closing
sentence is this session's opening question:

> *"Everything you just did was preparation. Nothing has been acquired yet."*

| Session 1 taught | Session 2 teaches |
|---|---|
| what must be true **before** analysis starts | how the evidence is **made** |
| verify a set someone else acquired | acquire it yourself, and prove what you did |

**What is new, and what is not.** Students met hashing, Volatility and the chain-of-custody concept in
eCIR and in S1. None of it is re-taught — it is referenced and the session moves on. The four new
blocks are `S2-02` (live response), `S2-03` (memory acquisition), `S2-05` (image formats) and `S2-07`
(`dc3dd` and targeted triage). **Those four carry the session.**

**The one idea the session turns on:** acquisition is a **decision**, not a button. No free lab on any
platform teaches it that way (`D46`), which is why `S2-01`–`S2-05` and `S2-09` are ours alone.

---

## 2 · Objectives

By the end of this session a student can:

| # | Objective | Blocks |
|---|---|---|
| **O1** | **Sequence** a collection on a running host by order of volatility, and **state** what each delay destroys | `S2-01` · `S2-02` |
| **O2** | **Capture** memory from a live host, and **state** why the result is a smear rather than a snapshot | `S2-03` |
| **O3** | **Choose** physical or logical acquisition for a stated goal, and **name** the evidence each one forfeits | `S2-04` · `S2-07` |
| **O4** | **Create** an image as E01 and as raw, and **state** exactly what `verified` covers and what it does not | `S2-05` · `S2-06` |
| **O5** | **Acquire and verify** the suspect USB, and **write** the result as a finding separated from interpretation | `S2-08` · `S2-09` · `S2-10` |

Every quiz question and every homework criterion maps to one of these five.

---

## 3 · Time table

| # | Block | Type | Min | Cumulative |
|---|---|---|--:|--:|
| `S2-01` | Order of volatility **in practice** — the sequence, and what getting it wrong destroys | theory + micro-lab | 15 | 15 |
| `S2-02` | **Live response** — volatile collection on a running host | theory + guided | 25 | 40 |
| `S2-03` | **Memory acquisition** — why it comes first, the tools, the pitfalls | theory + guided | 20 | 60 |
| — | **Knowledge check 1** | check | *(within blocks)* | 60 |
| `S2-04` | Physical vs logical acquisition — what each captures and what each misses | theory + micro-lab | 20 | 80 |
| `S2-05` | **Image formats** — E01 vs raw (`dd`) vs AD1, compression, embedded verification | theory + micro-lab | 15 | 95 |
| — | **BREAK** — imaging runs while the room is out | break | *15* | *110* |
| — | **Knowledge check 2** | check | *(within blocks)* | 95 |
| `S2-06` | **FTK Imager** — correct use and verification · *demo: imaging `FIN-WKS-07`* | demo + guided | 20 | 115 |
| `S2-07` | `dc3dd` on the clean Kali snapshot, and KAPE targeted triage | theory + guided | 15 | 130 |
| `S2-08` | **[INVESTIGATION]** Case 02a — acquire and verify the suspect USB | activity | **35** | 165 |
| `S2-09` | **[INVESTIGATION]** Case 02b — examine the image's partition and file-system structure | activity | **25** | 190 |
| — | **Knowledge check 3** | check | *(within `S2-09`)* | 190 |
| `S2-10` | **[RITUAL]** Hash-verify + chain-of-custody close | ritual | 15 | **205** |

**Totals — checked against `topic_map.md`, not estimated:**

| | Min |
|---|--:|
| Integrated chunks (`S2-01` … `S2-07`) | **130** |
| Break | 15 |
| Blocked investigation (`S2-08` + `S2-09`) | **60** |
| Hash-verify + chain-of-custody close (`S2-10`) | **15** |
| **Teaching total** | **220** |
| Slot | 240 |
| **Slack** | **20** |

**Hands-on: 155 min of 205 (76 %)** — `S2-02`, `S2-03`, `S2-06` … `S2-10` per `topic_map.md`.
Micro-labs 1, 4 and 5 add short practice inside the three theory blocks on top of that.

**Why the break is at minute 95.** It falls after `S2-05`, so `S2-06`'s FTK Imager demo gets an
uninterrupted run. Imaging takes real wall-clock time — **start it before the break if the hardware
allows** and let the machine work while the room is out.

---

## 4 · Prerequisites

**Before students arrive:**

| | Who | What |
|---|---|---|
| 1 | student | `FOR-WS01` restored to the `CLEAN-TOOLS` snapshot taken in S1 (`D17`) |
| 2 | student | this session's evidence downloaded **and its hash verified** (`D18`). A mismatch is a finding, not an inconvenience |
| 3 | student | ~20 GB free disk space — images are made in class |
| 4 | instructor | fallback USB evidence set prepared and re-verified |
| 5 | instructor | Kali rolled back to the **clean pre-staging snapshot** (`D56`) |
| 6 | instructor | a small scratch volume (~100 MB) per student for the micro-labs |

**No pre-course room is assigned for this session.** `D46`: no free lab on any platform teaches
acquisition as a decision, so there is nothing worth assigning that would not have to be corrected in
class. External practice is issued as homework instead, each with its defect named (`D47`).

---

## 5 · Tools

⚠️ **Re-verify every version on the build date** — forensic tooling rots fast. The versions below were
confirmed **2026-09-06**.

| Tool | Version | Role | Note |
|---|---|---|---|
| **FTK Imager** | **8.3** (Exterro, free) | 🟢🟢 **CORE** | `S2-06`. 🔴 **Not** the paid *FTK Imager Pro* — do not download that one by mistake |
| **`dc3dd`** | **7.3.1** (Kali) | 🟢🟢 **CORE** | `S2-07`. Hashes on the fly and writes a log — which plain `dd` never does |
| **KAPE** | core **1.3.0.2** · KapeFiles current | 🟢 **SUPPORTING** | `S2-07` targeted triage. 🔴 **Licence: free for education, barred for commercial use since 2026-01-01.** State that in class and pair every step with a free alternative (`D37`) |
| **OSFMount** | **3.3.1000** | 🟢 **SUPPORTING** | mounting an image read-only. Free, commercial use allowed, redistributable |
| **Arsenal Image Mounter** | **3.13.368** | 🟢 **SUPPORTING** | Free Mode covers what this session needs; BitLocker and VM launch are paid tiers |
| **Volatility 3** | **2.28.2** | ⚠️ **MENTION** | named here as *what the memory image is for*; analysis is `S6-10`. Ship the symbol pack — first run downloads symbols and **fails on an air-gapped lab** (`D2`) |
| `dd` / `dcfldd` | OS | ⚠️ **MENTION** | `dd` is no longer the recommendation for damaged media |
| `ewfverify` / `ewfinfo` | libewf | 🟢 **SUPPORTING** | proves an E01's embedded hash independently of the tool that wrote it |

**Hosts** (`D56`): analyst workstation **`FOR-WS01`** · Linux acquisition host **Kali**, run from the
**clean pre-staging snapshot**. There is no `FOR-LNX01`.

---

## 6 · Evidence

⛔ **Part 8 step 0 is NOT yet satisfied.** The four sets are specified and the acquisition is planned,
but they have not been acquired, so **no real hashes exist and none have been invented**.

| Set | What | For | Status |
|---|---|---|---|
| `EVS-02` | `FIN-WKS-07` system disk image — **E01 and raw** | `S2-05` `S2-06` `S2-09` | ⛔ PENDING |
| `EVS-03` | live **memory capture** from `FIN-WKS-07` | `S2-03` · later `S6-09` `S6-10` | ⛔ PENDING |
| `EVS-04` | the **suspect USB** image — E01 and raw | `S2-08` `S2-09` `S2-10` | ⛔ PENDING |
| `EVS-09` | **targeted triage** collection set | `S2-07` | ⛔ PENDING |

**Tier 1 — our own lab.** An E01 image, a memory dump and a USB image are Tier 1 or Tier 2 only. They
are **never synthesised**: a fabricated image is a lie told to students about what a forensic artifact
looks like. The acquisition is run from `labs/vm_notes/acquisition_runbook.md`; the resulting MD5 and
SHA-256 pairs are then written into `design/evidence_sets.md` and published as `.md5` / `.sha256`
manifests in `docs/session-02/`, exactly as `EVS-01` was.

**Every digest shown to students in this session is a placeholder** (`D41`). Real digests live in the
instructor answer key only.

**Micro-lab evidence.** Every micro-lab uses a **scratch volume the student makes**, their own VM, or
their own RAM — never the original evidence and never an unverified set.

**Constraints (`R8`, `R9`, `D41`):** fictional company and users · no real personal data · documentation
IP ranges only (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) · no credential anywhere · no
question has a secret or a person's data as its answer · **no evidence bytes in the repo** — manifests
and hashes only.

---

## 7 · The carry-through case (`D19`)

**Session 2's slice: the evidence is created.** The incident host is the finance workstation — exhibit
**`EVI-SRC01`**, Windows computer name **`FIN-WKS-07`**, used by `l.bennett` at the fictional Meridian
Retail Group. The attack window is **24–26 Aug 2026**; it is discovered about a week later.

> The host is reached **still running**. Live response collects volatile data first, then memory is
> captured, then the machine is powered down and the disk imaged. The suspect USB device is imaged
> too. **From this session on, every later session works on the images made here.**

**Two cases, deliberately separate** (`D57`):

| | Case 01 (Session 1) | The D19 incident (Sessions 2–6) |
|---|---|---|
| Purpose | standalone integrity and custody warm-up | the graded carry-through investigation |
| State as received | powered down, **no memory captured** | **found running** |
| Role in S2 | the **cautionary contrast** — what a cold power-down destroys | the acquisition done properly |

That contrast is the teaching point of `S2-01`. Case 01's first responder lost every byte of volatile
data. `S2-01` and `S2-02` are about not repeating it.

---

## 8 · Assessment

| What | When | Against |
|---|---|---|
| Knowledge check 1 | after `S2-02` | O1 |
| Knowledge check 2 | after `S2-05` | O2 · O3 · O4 |
| Knowledge check 3 | after `S2-09` | O4 · O5 |
| `quiz.md` — 10 questions, all MCQ | end of session | all five objectives |
| Case 02a / 02b write-up | in `S2-08` · `S2-09` | O5 |
| Homework report | take-home | the `D20` rubric, all four criteria |

**The rubric is unchanged from Session 1 and never changes** (`D20`):

| # | Criterion |
|---|---|
| 1 | **Integrity** — hashes before and after · verified against the manifest · custody complete |
| 2 | **Method** — reproducible by another analyst · every tool named with its version · steps in order |
| 3 | **Findings** — fact only · each tied to one named artifact at an exact path |
| 4 | **Separation** — interpretation visibly distinct · limitations stated · at least one honest *"this evidence cannot show X"* |

**Peer review** (`D16`): pairs, once, on the report only. ~5 students = two pairs and a trio.

---

## 9 · Bridge to Session 3

S2 ends with the images made, verified and logged, and the custody record carried forward.
**S3 opens the images** — data representation, file signatures and the malicious document that started
the intrusion.

The closing sentence of S2 is the opening question of S3:
*"You have the evidence now. What is actually inside it?"*
