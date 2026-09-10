# Session 1 — Session Plan

**eCDFP Diploma · ITGate Academy**
**Forensic Foundations, Evidence Integrity & Chain of Custody**

| | |
|---|---|
| **Session** | 1 of 6 |
| **Slot** | 240 min · 220 teaching · **205 topic minutes** + 15 break (`D15` / `D23`) |
| **INE source** | Module 1 intro — units 1–2 · Module 5 §2 (the report template) |
| **Primary domains** | Fundamentals of Digital Forensics · Preservation of Evidence |
| **Delivery** | integrated theory → demo → hands-on, closing with one blocked investigation hour |
| **Students** | ~5, offline classroom, **every student at a keyboard** (`D16`) |
| **Evidence set** | `EVS-01` — ✅ **verified 2026-08-30**. See §6 |
| **Case** | Case 01 — verify four files against a signed manifest, find the tampered one |

---

## 1 · Where this session sits

eCDFP is the **seventh** course in the track:

> CCNA → MCSA → Linux Administration → SOC → CEH → eCIR → **eCDFP**

Students arrive holding hashing, MD5/SHA-256, the chain-of-custody *concept* (eCIR S5),
Volatility, Wireshark and its filter set (eCIR S8), tcpdump, event logs, 4624, 1102, Sysmon,
MITRE ATT&CK and the IR lifecycle. **None of it is re-taught. It is referenced and the session
moves on.**

What is new is not a tool. It is a standard of proof:

| They can already do | This session is about |
|---|---|
| decide *"is this bad?"* | decide *"can I defend this in front of someone whose job is to break it?"* |
| detect | **evidence** |

That sentence opens the session.

**The other opening line:** this is the most important session in the diploma and it needs **no
forensic software at all** — `Get-FileHash`, `sha256sum`, and a text editor. Everything after it
needs software, and none of that software rescues a student who skipped this.

---

## 2 · Objectives

By the end of this session a student can:

| # | Objective | Blocks |
|---|---|---|
| **O1** | **Identify** a file from its first bytes, and **state** why its name is not evidence of what it is | `S1-09` |
| **O2** | **Verify** a file set against a signed manifest, and **report** a mismatch as a finding rather than a conclusion | `S1-06` · `S1-10` |
| **O3** | **Separate** findings from interpretation in writing, using the fixed course report template | `S1-04` |
| **O4** | **Complete** a chain-of-custody record for one exhibit, and **identify** the gap that breaks one | `S1-07` · `S1-11` |
| **O5** | **State** the proof trail that evidences a write blocker was used — and why the image itself cannot | `S1-08` |

Every quiz question and every homework criterion maps to one of these five.

---

## 3 · Time table

| # | Block | Type | Min | Cumulative |
|---|---|---|--:|--:|
| `S1-01` | What digital forensics is — mandate, evidence lifecycle, what you may not claim | theory | 10 | 10 |
| `S1-02` | Forensic principles — minimal footprint, repeatability, work on a copy | theory | 10 | 20 |
| `S1-03` | What makes evidence defensible — relevant · reliable · competent | theory | 10 | 30 |
| — | **Knowledge check 1** | check | *(within blocks)* | 30 |
| `S1-04` | **The fixed report template — findings vs interpretation (`D7`)** | theory + guided | **25** | 55 |
| `S1-05` | Analyst toolkit install and the `CLEAN-TOOLS` snapshot | guided lab | 15 | 70 |
| — | **BREAK** — the snapshot completes while the room is out | break | *15* | *85* |
| `S1-06` | Cryptographic hashing — what a hash proves and what it does not | theory + demo | 18 | 88 |
| `S1-07` | Chain of custody — the form and the discipline | theory + guided | 12 | 100 |
| `S1-08` | **Write blocking — and how to prove one was used** | theory | 8 | 108 |
| `S1-09` | 🔴 **Inside a file — hex, magic bytes, and why renaming changes nothing** | theory + micro-lab | **22** | 130 |
| `S1-10` | **[INVESTIGATION]** Case 01 — the tampered file | activity | **60** | 190 |
| — | **Knowledge check 2** | check | *(within `S1-10`)* | 190 |
| `S1-11` | **[RITUAL]** Hash-verify + chain-of-custody close | ritual | 15 | **205** |

**Totals — checked against `topic_map.md`, not estimated:**

| | Min |
|---|--:|
| Integrated chunks (`S1-01` … `S1-08`) | **130** |
| Break | 15 |
| Blocked investigation (`S1-09`) | **60** |
| Hash-verify + chain-of-custody close (`S1-10`) | **15** |
| **Teaching total** | **220** |
| Slot | 240 |
| **Slack** | **20** |

**Hands-on: 160 min of 205 (78 %)** — `S1-04` through `S1-11`.

**Why the break is at minute 70 and not at the midpoint.** `S1-05` ends by starting the
`CLEAN-TOOLS` snapshot, which takes real wall-clock time. The machine works through the break.

---

## 4 · Prerequisites

**Pre-course task, issued before the session:**

- **TryHackMe — Intro to Digital Forensics** (`introdigitalforensics`) · free · ~90 min.
  Covers `S1-01`, `S1-02` and part of `S1-07`, so the session opens on shared vocabulary instead
  of definitions.
  ⚠️ **Assign it with its defect named** (`D47`): its hashing task is thin and will not prepare
  a student for `S1-06`. Say so in the assignment text.

**Before students arrive:**

| | Who | What |
|---|---|---|
| 1 | student | `FOR-WS01` imported and booting — clean Windows base VM, no forensic tooling (`D17`) |
| 2 | student | `EVS-01` downloaded **and its hash verified** (`D18`). A mismatch is a finding, not an inconvenience |
| 3 | instructor | fallback USB set prepared and re-verified |
| 4 | instructor | tool installers staged locally — the classroom is offline |

---

## 5 · Tools

**No forensic software is installed for this session's own teaching.** The tool set is installed
in `S1-05` because sessions 2–6 need it, not because session 1 does.

| Tool | Version | Role | Note |
|---|---|---|---|
| `Get-FileHash` / `sha256sum` | OS built-in | 🟢🟢 **CORE** | the whole of `S1-06` |
| `md5sum` / `Get-FileHash -Algorithm MD5` | OS built-in | ⚠️ **MENTION** | **a lookup key, explicitly not an integrity control** |
| A text editor + a manifest | — | 🟢🟢 **CORE** | the chain of custody is a document, not a tool — that is the lesson |

**Installed in `S1-05` for later sessions** (`D49`): FTK Imager 8.3 · Autopsy 4.23.1 ·
Wireshark 4.6.8 · Volatility 3 2.28.2 + symbol pack · ExifTool 13.59 · HxD 2.5.0.0 ·
OSFMount 3.3.1000 · Arsenal Image Mounter 3.13.368 · TestDisk **7.2 stable** ·
RegRipper **3.0 only** · Get-ZimmermanTools · NetworkMiner 3.1 · plaso · CyberChef offline copy.

**Three tools are named and deliberately not shipped** — this is taught as a finding, not skipped:

| Tool | Why not |
|---|---|
| RegRipper **4.0** | licence bars *"vendor training"* and *"any distribution"*. ITGate is paid training. Stay on 3.0 |
| 010 Editor | commercial, 30-day evaluation, **no free tier**. HxD does everything this course needs |
| Xiao Steganography | **no living vendor** — every copy is a third-party mirror dating to 2010 or earlier |

⚠️ **Re-verify every version above on the build date** — forensic tooling rots fast.
Versions here were confirmed 2026-08-29; Volatility re-verified 2026-09-06.

---

## 6 · Evidence

**`EVS-01` — ✅ verified 2026-08-30.** Generated by `scripts/make_evs01.py`, hashes computed from
the generated files and published in `design/evidence_sets.md`. Part 8 step 0 is satisfied.

**Tier 1 — generated in our own lab.** Four plain-text documents, **6 144 B total**, produced by a
deterministic generator (fixed seed, fixed base date) so a student's copy is diffable against ours.

| # | File | Bytes | State as distributed |
|--:|---|--:|---|
| 1 | `seizure_notes.txt` | 2 303 | clean |
| 2 | `EVI-SRC01_acquisition_log.txt` | 1 340 | 🔴 **altered — one character** |
| 3 | `custody_form_EVI-SRC01.txt` | 1 914 | clean |
| 4 | `evidence_inventory.csv` | 587 | clean |
| — | `EVS-01.sha256` · `EVS-01.md5` | — | the manifests, published in `docs/session-01/` |

**The alteration:** `Acquisition started : 2026-03-04 09:14:0`**`2`**` UTC` → `…09:14:0`**`3`**` UTC`.
One character. Verified by running it: `sha256sum -c` gives **3 OK, 1 FAILED**, and `md5sum -c`
gives the same.

🔴 **Instructor only — the digest the distributed file actually computes to:**
SHA-256 `7eda34b36f53700bb3e0c4cd85c6c026b4c67982d7f7c2375fa8540af4bfb3c6` · MD5 `2f3858969b36fc4f06efad19a5e973b1`.
A correct `F-01` quotes that against the manifest's `f05bfee8…`.

**Why the acquisition log is the file that was altered.** It is the file whose *content is the
integrity claim* — the one containing the word `verified`. The catch lands exactly where students
reliably fail: *"verified" means the tool checked its own output*, and a log is documentation of an
acquisition, not evidence of one.

**Constraints (`R8`, `R9`, `D41`):** fictional company and users · no real personal data ·
documentation IP ranges only (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) · no
credential anywhere · **no question has a secret or a person's data as its answer** · no evidence
bytes in the repo — manifest and hashes only.

---

## 7 · The carry-through case (`D19`)

One intrusion chain runs through all six sessions:

> A finance-department user at a fictional company opens a malicious document received by email.
> Malware executes and establishes persistence, beacons to an external C2 server, and the operator
> uses harvested credentials over RDP to reach a second host. Data is collected, staged, archived
> and copied to a USB device. Ransomware tooling is staged but **never fires** — the intrusion is
> caught first. The host is powered down and imaged in Session 2.

**Session 1's slice:** the host has been seized and **nothing has been analysed yet.** S1 is
about *what has to be true before analysis is allowed to start.*

---

## 8 · Assessment

| What | When | Against |
|---|---|---|
| Knowledge check 1 | after `S1-03` | O3 |
| Knowledge check 2 | after `S1-10` | O1 · O2 · O5 |
| `quiz.md` — 10 questions | end of session | all five objectives |
| Case 01 write-up | in `S1-10` | O2 · O3 |
| Homework report | take-home | the `D20` rubric, all four criteria |

**The rubric is published today and never changes** (`D20`):

| # | Criterion |
|---|---|
| 1 | **Integrity** — hashes before and after · verified against the manifest · custody complete |
| 2 | **Method** — reproducible by another analyst · every tool named with its version · steps in order |
| 3 | **Findings** — fact only · each tied to one named artifact at an exact path |
| 4 | **Separation** — interpretation visibly distinct · limitations stated · at least one honest *"this evidence cannot show X"* |

Criterion 4 is the one the course exists to teach. Students see the same target six times, which
is the only way to prove report writing is improving.

**Peer review** (`D16`): pairs, once, on the report only — reading someone else's writing and
marking where a *finding* has drifted into an *interpretation*. ~5 students = two pairs and a trio.

---

## 8.5 · Re-cut under `D58` (2026-09-06)

**Order of volatility was removed from this session.** It was taught here *and* in S2 — 35 minutes for
one idea. `S2-01` now owns it and teaches it operationally, where the decision is actually made.
The theory blocks were trimmed to 10 minutes each and the recovered time went into a new hands-on
block, **`S1-09` — hex and magic bytes**, so students open a file and read its real type on day one
instead of at hour 9. Blocks after it renumbered: Case 01 is now `S1-10`, the ritual `S1-11`.

---

## 9 · Bridge to Session 2

S1 ends with the host seized, the evidence verified and the custody record open.
**S2 opens by acquiring it** — live response, memory capture, then FTK Imager against
`EVI-SRC01`, and the carry-through case is born.

The closing sentence of S1 is the opening question of S2:
*"Everything you just did was preparation. Nothing has been acquired yet."*
