# Session 2 — Instructor Guide

**Acquisition: Disk, Memory & Live Response** · 205 topic min + 15 break

---

## 0 · Pre-class checklist

| ☐ | Item |
|:-:|---|
| ☐ | `EVS-02` · `EVS-03` · `EVS-04` · `EVS-09` acquired, hashed and published with **both** digests (`D18`). ⛔ **If this is not done, the session does not run** — Part 8 step 0 |
| ☐ | Fallback USB evidence set prepared and re-verified this morning |
| ☐ | Kali rolled back to the **clean pre-staging snapshot** (`D56`) — `S2-07` must not run on the compromised host |
| ☐ | Every student's `FOR-WS01` restored to `CLEAN-TOOLS` |
| ☐ | A ~100 MB scratch volume per student, for micro-labs 4, 5, 6 and 7 |
| ☐ | ~20 GB free per student — images are made in class |
| ☐ | FTK Imager 8.3 confirmed on each machine (**not** the paid Pro build) |
| ☐ | Write blocker present, or the software equivalent demonstrated |
| ☐ | Session 1's record page open — the session **opens** with it |
| ☐ | Versions re-verified today and written on the board |

---

## 1 · The two sentences the session turns on

**Open with this:**

> *"Everything you did in Session 1 was preparation. Nothing has been acquired yet.
> Session 2 is where the evidence is created — and every session after this one works on the
> images you make today."*

**Close every block with the second one:**

> *"`verified` means the tool checked its own output. It never re-read the source."*

That second sentence is the `D7` lesson of this session and it is the one students most reliably get
wrong. It appears in `S2-05`, is proved in `S2-06`, and is examined in the quiz.

---

## 2 · Per-block teaching notes

### `S2-01` — Order of volatility in practice · 15 min

**The move:** S1 taught the *list*. Today it is a **race against a clock**.

Draw the seven stores and start a timer on them:

| # | Store | Gone in |
|--:|---|---|
| 1 | CPU registers and cache | nanoseconds |
| 2 | RAM | on power loss |
| 3 | Network state — connections, ARP, routing | seconds to minutes |
| 4 | Running processes | on reboot |
| 5 | Disk | survives |
| 6 | Remote and centralised logs | log rotation |
| 7 | Archival media | months to years |

**The point to land:** collection is not free. *While you collect RAM, network state is decaying.
While you image the disk, both are already gone.* Order is a choice about what you are willing to
lose.

🔴 **The Case 01 contrast — use it, it is why the case exists.** Session 1's first responder received
`EVI-SRC01` powered down and recorded that **no memory capture was taken**. Everything in stores 1 to 4
was destroyed before the examiner touched it. Ask the room what questions can now never be answered:
running processes, open network connections, injected code, anything decrypted only in memory.

**Micro-lab 1 · 7 min.** Give a scenario — a running host, a suspect at the desk, one hour. Students
write the collection order and one line per step saying what that step costs. Check: the order matches
and each cost is named.

---

### `S2-02` — Live response · 25 min · 🔴 new

**The paradox to state plainly:** to preserve what is on a running machine, you must touch it — and
every command you run changes it. There is no clean option. There is only a **recorded** one.

**What the OS tells you is not what is true.** A live collector asks the operating system for the
process list. If the operating system has been subverted, it answers with the list the attacker wants
you to see. Show the two columns: what the collector reports, and what is actually running.

> **What catches it:** compare the live answer against the memory image later. `pslist` walks the
> same structures the OS uses; `psscan` scans memory for process objects directly. **Run both and
> diff them** — that is `S6-10`, and today is where the reason for it is planted.

**Minimal footprint rules — these are the graded habits:**

1. Run the collector from **external media**, never install it on the evidence host.
2. Write output to **external media**, never to the evidence disk.
3. Record **every command and its time**, as you go.
4. Isolate the network **before** collecting, and record when.
5. Prefer one tool that does many things over many separate commands — fewer footprints.

**The output tree** — this is the shape students must recognise:

```
FIN-WKS-07_2026-09-02_1412\
├── ForensicImages\
│   └── Memory\                    the raw memory capture
├── LiveResponseData\
│   ├── ProcessInfo\               process list, DLLs, handles
│   ├── NetworkInfo\               connections, ARP, routing, DNS cache
│   ├── UserInfo\                  logged-on users, sessions
│   └── SystemInfo\                uptime, patches, services, scheduled tasks
├── <hostname>_hashes.csv          one hash per collected file
└── Processing_Details.txt         every command, its start and finish time
```

**Why `Processing_Details.txt` is the important file.** ISO/IEC 27037 asks that a qualified third
party can reconstruct what you did. On a live host that is only possible if every command and its time
were recorded while you ran them. The hash list proves the collected files did not change afterwards;
the details file proves what you did to get them.

**Micro-lab 2 · 12 min.** WATCH: run the collector once. DO: each student runs it on their own VM.
CHECK: the output tree exists and the per-file hash list has an entry for every collected file.
WHY: *this proves the files have not changed since collection. It does not prove the operating system
told the truth when it listed them.*

---

### `S2-03` — Memory acquisition · 20 min · 🔴 new

**Why memory comes first:** it holds what exists nowhere else — running processes, open network
connections, injected code, loaded drivers, and data that is only ever decrypted in RAM. Power off and
it is gone. There is no second chance and no partial recovery.

🔴 **The key idea of the block: a memory capture is a smear, not a snapshot.**

The capture tool reads memory from low addresses to high, and it takes time — minutes on a large host.
**The system keeps running the whole time.** So the top of the dump was read at one moment and the
bottom at a later one. A process that existed when the read started may be gone by the time the read
reaches its pages.

| What the smear makes unreliable | What it does **not** affect |
|---|---|
| a claim that two structures were consistent **with each other** at one instant | the presence of an artifact you find — it was really there |
| page-level counts that must add up exactly | strings, injected code and connections that are recovered intact |
| "the process table proves the exact state at 14:12" | "this process was present during the capture window" |

**Say the sentence students should write:** *"the capture ran from 14:12 to 14:19 UTC; findings
describe the state during that window, not at a single instant."*

**What blocks a capture — and what you actually see:**

| Blocker | What you see | The way round |
|---|---|---|
| Driver signing enforcement | the tool's driver refuses to load | use a signed acquisition tool |
| Secure Boot | driver load blocked at boot level | signed tool, or document that capture was not possible |
| A hypervisor | the guest sees only its own memory | capture at the host, or take the VM's memory file |
| An anti-cheat or EDR driver | the tool is blocked or the host crashes | coordinate with the vendor; record the attempt and the refusal |

⚠️ **A failed capture is a finding.** Record the tool, the version, the error and the time. "We could
not capture memory because Secure Boot blocked the driver" is a defensible sentence. Silence is not.

**Sizes:** the dump is roughly the size of physical RAM. A 16 GB host gives a ~16 GB file. If it is
dramatically smaller, the capture did not complete — check before you power down, because after that
there is nothing to re-run.

**Micro-lab 3 · 8 min.** WATCH: capture memory, note the elapsed time out loud. DO: each student
captures their own VM's RAM. CHECK: dump size is about equal to the VM's assigned RAM, and they wrote
down **start and finish** times. WHY: *the two times define the window your findings describe.*

---

### `S2-04` — Physical vs logical acquisition · 20 min

One disk, drawn once, with two envelopes over it.

| | **Physical** | **Logical** |
|---|---|---|
| Reaches | every sector on the device | allocated files only, as the file system presents them |
| Includes | slack space, unallocated space, deleted file remnants, HPA/DCO, partition gaps | the files you can see, and their metadata |
| Misses | nothing on the device | everything not currently allocated to a file |
| Size | the full device size | the size of the selected data |
| Use when | you can take the whole device, and the case may need deleted data | the device is huge, encrypted at rest, or legal scope is narrow |

🔴 **Tie it forward, by name:** `S4` recovers deleted staging files from **unallocated space** and
parses the `$MFT`. A logical acquisition taken today would make that session impossible. **The
acquisition decision made in S2 sets the ceiling on every later session.**

**The four methods:**

| Method | What it produces | Forfeits |
|---|---|---|
| **Disk-to-image** | one or more image files from the source device | nothing — this is the default |
| **Disk-to-disk (clone)** | a second physical disk, sector for sector | no compression, no metadata, no embedded hash; needs a disk as big as the source |
| **Sparse** | selected portions of the device | everything outside the selection |
| **Logical** | selected files as a container | slack, unallocated, deleted data |

**Micro-lab 4 · 8 min.** WATCH: image the 100 MB scratch volume physically, then logically. DO: both.
CHECK: the two output files differ in size — and the student can say **why** (the physical image
includes free space; the logical one holds only the files). WHY: *the size difference is the evidence
you did not collect.*

---

### `S2-05` — Image formats · 15 min · 🔴 new

| | **raw (`dd`)** | **E01 (EWF)** | **AD1** |
|---|---|---|---|
| Contents | bytes, and nothing else | bytes plus structure | selected files only |
| Metadata | none | case number, examiner, notes, acquisition times | logical container metadata |
| Compression | no | yes | yes |
| Integrity | none built in | **per-chunk CRC + embedded image hash** | container hash |
| Segments | one large file (or split by hand) | split automatically | container |
| Read by | everything | most forensic tools | AccessData tools ⚠️ **Autopsy cannot open AD1** |

**Why E01 is the default here:** it carries its own verification and its own case metadata, so the
image is self-describing. **Why raw still matters:** every tool on earth reads it, and some tools —
including several Linux utilities the course uses later — want a raw device.

🔴 **The catch, and it is the whole point of the next block:** E01's embedded hash verifies **the image
against itself**. It proves the container is internally intact. It does **not** re-read the source
device and does not prove the image still matches the original drive.

**Micro-lab 5 · 7 min.** WATCH: create the same scratch volume as E01 and as raw. DO: both.
CHECK: the E01 is smaller (compression); `ewfverify` passes on it; the raw file has **no embedded hash
to verify at all** — its integrity depends entirely on a manifest you keep separately.
WHY: *format is a decision about what verification you will be able to do later.*

---

### `S2-06` — FTK Imager, and what `verified` covers · 20 min · ★ the `D7` block

**Version:** FTK Imager **8.3**, free edition. 🔴 Not *FTK Imager Pro*, which is paid.

**Demo — imaging `FIN-WKS-07`, end to end.** Narrate every step; students watch, then repeat on their
scratch volume.

1. Engage the write blocker. **Record it before connecting the source** — a blocker written down
   afterwards proves nothing, because the write you are ruling out would already have happened.
2. `File > Create Disk Image` → source `Physical Drive`.
3. Select the source device. **Read the size and model aloud and match them to the exhibit record.**
4. Destination: `E01`, evidence-item fields filled — case number, examiner, description.
5. Compression on. Segment size default.
6. 🔴 **`Verify images after they are created` — ticked.** This is the checkbox the block is about.
7. Start. It takes real time — this is why the demo starts before the break.

**The verification log — read it out loud, line by line:**

```
[Computed Hashes]
 MD5 checksum    : <placeholder-md5>
 SHA1 checksum   : <placeholder-sha1>

Image Verification Results:
 Verification started: 2026-09-02 14:41:07
 Verification finished: 2026-09-02 15:02:55
 MD5 checksum    : <placeholder-md5>   : verified
 SHA1 checksum   : <placeholder-sha1>  : verified
```

🔴 **Now the question the whole session builds to:** *what did the tool actually check?*

| The tool **did** | The tool **did not** |
|---|---|
| hash the data as it wrote the image | re-read the source drive |
| read the image back and hash it again | prove the image matches the original **now** |
| prove the two match — the write was clean | prove nothing was altered before you arrived |

**The sentence a student may write:**
> *`F-02` — The acquisition log for `EVS-02` records the image hash as `<value>` and the read-back
> verification as `verified` (FTK Imager 8.3, 2026-09-02 15:02 UTC).*

**The sentence a student may not write:**
> ~~*The image is verified, so the disk was not tampered with.*~~ That is an interpretation, and an
> unsupported one. Verification covers the copy, not the history of the original.

**Micro-lab 6 · 10 min.** DO: each student images their scratch volume with verification ticked.
CHECK: the `.txt` log shows both digests and the word `verified`.
WHY: *it proves the copy is faithful. It says nothing about the source's history.*

---

### `S2-07` — `dc3dd` and targeted triage · 15 min · 🔴 new

**Three tools, three jobs.** Compare them on four axes: hashes on the fly? · writes a log? · handles
read errors? · scope.

| | `dd` | `dc3dd` **7.3.1** | KAPE |
|---|:-:|:-:|:-:|
| Hashes while imaging | ✗ | ✅ | ✅ (per collected file) |
| Writes a log | ✗ | ✅ | ✅ |
| Handles read errors well | ✗ | ✅ | n/a |
| Scope | whole device | whole device | **selected artifacts only** |

**The `dc3dd` command students run:**

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

**Expected tail of the log:**

```
   204800 sectors in
   204800 sectors out
   [sha256] <placeholder-sha256>
```

**The catch to state:** `dd` produces no hash and no log. If you image with plain `dd` you must hash
the source and the image yourself, in separate steps, and record them by hand — and if the two do not
match you have no log to tell you where the read failed.

**KAPE — targeted triage.** Collect the artifacts that answer the question, not the whole disk. Used
when the disk is huge, the system cannot be taken offline, or time is short.

🔴 **Licence — say this in class, do not let a student find out mid-engagement** (`D37`):
KAPE's own FAQ states it is **no longer available for commercial use** as of 1 January 2026 — that is,
on a third-party network or as part of a paid engagement. **Classroom and educational use remain
free.** So it is taught for the concepts, and **every KAPE step is paired with a free alternative**:
the EZ Tools underneath it are separately free, and a target set is only a list of file paths that
`robocopy` or a short script can collect.

⚠️ Also correct a common claim: the KAPE core binary is **1.3.0.2 (Dec 2022)**, but **KapeFiles ships
by commit and is current**. "KAPE is stale" is wrong and should not be taught.

**What triage forfeits — the part that matters:** unallocated space, slack, deleted files, and
anything not on the target list. **You cannot later answer a question about data you chose not to
collect.** Triage is a decision to trade completeness for speed, and the decision has to be recorded.

**Micro-lab 7 · 7 min.** On the **clean Kali snapshot** (`D56`). DO: run the `dc3dd` command above on
the scratch volume. CHECK: the log file contains the SHA-256 — which plain `dd` never produces.
WHY: *the log is the proof the hash was computed at acquisition time, not afterwards.*

---

### `S2-08` — Case 02a · 35 min · blocked investigation

Individual at the keyboard (`D16`). The brief, the evidence and the questions are in
`student_activity.md`. **Q1 is always hash verification.**

**Run it like this:** hand out the brief, give the acquisition decision tree once, then stay quiet.
Answer questions with questions. The block is about students making the acquisition decision
themselves — the thing no external lab teaches (`D46`).

**The decision tree they apply:** is the host running? → is the data encrypted? → is time short? →
which method, and what does it forfeit?

**Watch for the two failures:** a student who images without recording the write blocker first, and a
student who writes *"the USB was used to steal data"* as a finding. The second is the `D7` error and
it costs marks under criterion 4.

---

### `S2-09` — Case 02b · 25 min · blocked investigation

Examine the acquired image's **structure** — partition table, partition type, file system, volume
size, and whether the sizes reconcile.

**The lesson buried in it:** an unallocated gap between partitions, or a partition smaller than the
device, is a *finding* worth writing. What it means is an *interpretation*, and often the honest
answer is *"this evidence cannot show why the gap is there."* One question in the set is answerable
only that way — that is deliberate.

Tools: OSFMount 3.3.1000 or Arsenal Image Mounter 3.13.368, mounted **read-only**.

---

### `S2-10` — The closing ritual · 15 min

Identical in shape to `S1-10`, and it must stay identical — that is what makes six sessions one
document.

1. Re-verify the evidence hashes against the published manifest.
2. Each student completes **one custody line** on their own record.
3. Close the session's steps on `docs/session-02/record.html`.

**Micro-lab 8.** DO: fill one custody line. CHECK: the record page shows the step closed.
WHY: *the record is the deliverable that carries forward; a session that does not close it leaves the
chain broken.*

⚠️ The custody-transfer log and the disposition are **case-level** — rendered once, never cleared with
a session. Do not let a student "reset" the page to tidy it.

---

## 3 · Where students reliably go wrong — the six

| # | The error | The correction |
|--:|---|---|
| 1 | Reading `verified` as *"the evidence is untampered"* | the tool checked its own output; it never re-read the source |
| 2 | Powering the host down to "preserve" it | that destroys stores 1–4. Preservation on a live host means **capture first** |
| 3 | Writing collector output to the evidence disk | it overwrites unallocated space — the space `S4` needs |
| 4 | Treating a memory dump as an instant snapshot | it is a smear across the capture window; say the window |
| 5 | Choosing logical acquisition because it is faster | it forfeits deleted data and caps every later session |
| 6 | Recording the write blocker after connecting the source | written afterwards it proves nothing |

---

## 4 · If you are running short

Cut in this order, and record the cut in `build_log.md`:

1. **Micro-lab 4** (`S2-04`) — the size difference can be shown once by you instead of by everyone. Saves ~6 min.
2. **`S2-05` to the table only** — drop the AD1 discussion, keep E01 vs raw. Saves ~5 min.
3. **Micro-lab 1** (`S2-01`) — do it as a room discussion rather than written. Saves ~5 min.

🔴 **Never cut:** `S2-06`'s verification log reading (it is the `D7` lesson), the investigation hour,
or the closing ritual. If time is truly gone, shorten `S2-09` and keep `S2-10` whole.

---

## 5 · Bridge to Session 3

The images exist and are verified. **S3 opens them** — data representation, file signatures versus
extensions, metadata, and the malicious document that began the intrusion.

Closing line: *"You have the evidence now. What is actually inside it?"*
