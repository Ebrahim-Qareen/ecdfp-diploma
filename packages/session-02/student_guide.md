# Session 2 — Student Guide

**Acquisition: Disk, Memory & Live Response**

---

## What changes today

Session 1 was about what has to be true **before** analysis starts. Today you make the evidence
yourself.

Everything you examine in Sessions 3 to 6 comes from the images made in this session. If the
acquisition is wrong, no later analysis can repair it. That is why acquisition is a **decision**, not
a button.

By the end of the session you can:

- **O1** — sequence a collection on a running host by order of volatility, and state what each delay destroys
- **O2** — capture memory from a live host, and state why the result is a smear rather than a snapshot
- **O3** — choose physical or logical acquisition for a stated goal, and name the evidence each one forfeits
- **O4** — create an image as E01 and as raw, and state exactly what `verified` covers and what it does not
- **O5** — acquire and verify the suspect USB, and write the result as a finding separated from interpretation

---

## 1 · Order of volatility, in practice

In Session 1 you learned the list. Today it is a race.

| # | Store | How long it survives |
|--:|---|---|
| 1 | CPU registers and cache | nanoseconds |
| 2 | RAM | until power is lost |
| 3 | Network state — connections, ARP, routing | seconds to minutes |
| 4 | Running processes | until reboot |
| 5 | Disk | survives power loss |
| 6 | Remote and centralised logs | until they rotate |
| 7 | Archival media | months to years |

**Collection is not free.** While you collect RAM, network state is decaying. While you image the
disk, both are already gone. The order you choose is a decision about what you accept losing.

### The example from Case 01

In Session 1 the host was received **powered down**, and the responder's notes record that **no memory
capture was taken**. Everything in stores 1 to 4 was destroyed before the examiner saw the machine.

These questions can now never be answered for that host:

- what was running
- what network connections were open
- whether code was injected into a running process
- anything that was only ever decrypted in memory

That loss is the reason this session exists.

---

## 2 · Live response

**Live response is collecting volatile data from a machine that is still running.**

There is a paradox at the centre of it: to preserve what is on a running machine, you must touch it —
and every command you run changes it. There is no clean option. There is only a **recorded** one.

### What the operating system reports is not always what is true

A live collector asks the operating system for the process list. If the operating system has been
subverted, it answers with the list the attacker wants you to see. The report can look perfectly
normal while three processes are hidden.

This is why memory is captured as well: the memory image can be examined later with tools that do not
have to trust the operating system's answer.

### The five rules

1. Run the collector from **external media**. Never install it on the evidence host.
2. Write output to **external media**. Never to the evidence disk.
3. Record **every command and its time**, as you run it.
4. Isolate the network **before** collecting, and record when you did.
5. Prefer one tool that does several things over many separate commands — fewer footprints.

### The output tree

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

**`Processing_Details.txt` is the most important file in that tree.** A qualified third party must be
able to reconstruct what you did. On a live host that is only possible if every command and its time
were recorded while you ran them.

**What the hash list proves:** the collected files have not changed since collection.
**What it does not prove:** that the operating system told the truth when it listed them.

---

## 3 · Memory acquisition

Memory holds what exists nowhere else: running processes, open network connections, injected code,
loaded drivers, and data that is only ever decrypted in RAM. Power off and it is gone. There is no
second chance.

### A memory capture is a smear, not a snapshot

The capture tool reads memory from low addresses to high, and it takes time — minutes on a large host.
**The machine keeps running the whole time.** So the top of the dump was read at one moment and the
bottom at a later one. A process that existed when the read started may be gone by the time the read
reaches its pages.

| This makes unreliable | This is unaffected |
|---|---|
| a claim that two structures were consistent **with each other** at one instant | an artifact you find — it really was there |
| counts that must add up exactly | strings, injected code and connections recovered intact |
| "the process table proves the exact state at 14:12" | "this process was present during the capture window" |

**Write it this way:**
> *The capture ran from 14:12 to 14:19 UTC. Findings describe the state during that window, not at a
> single instant.*

### What can block a capture

| Blocker | What you see | What to do |
|---|---|---|
| Driver signing enforcement | the tool's driver refuses to load | use a signed acquisition tool |
| Secure Boot | driver load blocked at boot level | use a signed tool, or record that capture was not possible |
| A hypervisor | the guest sees only its own memory | capture at the host, or take the VM's memory file |
| An anti-cheat or EDR driver | the tool is blocked, or the host crashes | record the attempt and the refusal |

**A failed capture is a finding.** Record the tool, its version, the exact error and the time.
*"Memory capture was attempted at 14:05 UTC with `<tool> <version>` and failed because the driver was
blocked by Secure Boot"* is a defensible sentence. Silence is not.

### Self-review — check your own capture

The dump should be roughly the size of physical RAM. A 16 GB host gives a file of about 16 GB. If it
is much smaller, the capture did not finish — check **before** the machine is powered down, because
after that there is nothing left to re-run.

---

## 4 · Physical and logical acquisition

| | **Physical** | **Logical** |
|---|---|---|
| Reaches | every sector on the device | allocated files only |
| Includes | slack space, unallocated space, deleted remnants, HPA/DCO, partition gaps | the files you can see, and their metadata |
| Misses | nothing on the device | everything not currently allocated to a file |
| Size | the full device size | the size of the selected data |
| Choose when | you can take the whole device, and the case may need deleted data | the device is very large, or legal scope is narrow |

**This decision sets a ceiling on every later session.** In Session 4 you recover deleted staging files
from **unallocated space** and parse the `$MFT`. A logical acquisition taken today would make that
impossible — the data simply would not be in your image.

### The four methods

| Method | Produces | Forfeits |
|---|---|---|
| **Disk-to-image** | one or more image files from the source | nothing — this is the default |
| **Disk-to-disk (clone)** | a second physical disk, sector for sector | compression, metadata and an embedded hash; needs a disk as large as the source |
| **Sparse** | selected portions of the device | everything outside the selection |
| **Logical** | selected files in a container | slack, unallocated space, deleted data |

---

## 5 · Image formats

| | **raw (`dd`)** | **E01 (EWF)** | **AD1** |
|---|---|---|---|
| Contents | bytes, nothing else | bytes plus structure | selected files only |
| Metadata | none | case number, examiner, notes, times | container metadata |
| Compression | no | yes | yes |
| Built-in integrity | none | **per-chunk CRC + embedded image hash** | container hash |
| Read by | everything | most forensic tools | AccessData tools — Autopsy **cannot** open AD1 |

**E01 is the default** because it carries its own verification and its own case metadata, so the image
describes itself. **Raw still matters** because every tool reads it, and several Linux utilities used
later in this course want a raw device.

🔴 **The catch, and it is the point of the next section.** E01's embedded hash verifies **the image
against itself**. It proves the container is internally intact. It does **not** re-read the source
device, and it does not prove the image still matches the original drive.

---

## 6 · What `verified` covers — and what it does not

This is the most important idea in the session.

When FTK Imager finishes and its log says `verified`, here is what happened:

| The tool **did** | The tool **did not** |
|---|---|
| hash the data as it wrote the image | re-read the source drive |
| read the image back and hash it again | prove the image matches the original **now** |
| prove the two match — the write was clean | prove nothing was altered before you arrived |

**A sentence you may write:**
> *`F-02` — The acquisition log for `EVS-02` records the image hash as `<value>` and the read-back
> verification as `verified` (FTK Imager 8.3, 2026-09-02 15:02 UTC).*

**A sentence you may not write:**
> ~~*The image is verified, so the disk was not tampered with.*~~

The second sentence is an interpretation, and it is not supported. Verification covers the copy. It
says nothing about the history of the original.

### Self-review — read your own verification log

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

Ask yourself the three questions: which data was hashed first? Which data was hashed second? Was the
source drive read a second time? The answer to the third is **no** — and that is the whole lesson.

---

## 7 · `dd`, `dc3dd` and targeted triage

| | `dd` | `dc3dd` **7.3.1** | KAPE |
|---|:-:|:-:|:-:|
| Hashes while imaging | ✗ | ✅ | ✅ (per file) |
| Writes a log | ✗ | ✅ | ✅ |
| Handles read errors well | ✗ | ✅ | n/a |
| Scope | whole device | whole device | **selected artifacts only** |

The command you run:

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

The log ends with the hash:

```
   204800 sectors in
   204800 sectors out
   [sha256] <placeholder-sha256>
```

**Why this matters:** the log is proof that the hash was computed **at acquisition time**, not
afterwards. Plain `dd` gives you neither a hash nor a log, so you must hash the source and the image
in separate steps and record them by hand — and if they disagree, nothing tells you where the read
failed.

### Targeted triage

Triage collects the artifacts that answer the question instead of the whole disk. It is used when the
disk is very large, the system cannot be taken offline, or time is short.

⚠️ **KAPE licence.** KAPE's FAQ states it is **no longer available for commercial use** as of
1 January 2026 — that is, on a third-party network or as part of a paid engagement. **Classroom and
educational use remain free.** In paid work, use the free alternatives: the EZ Tools underneath KAPE
are separately free, and a target set is only a list of file paths that a script can collect.

**What triage forfeits:** unallocated space, slack, deleted files, and anything not on the target
list. **You cannot later answer a question about data you chose not to collect.** Triage trades
completeness for speed, and that trade has to be recorded.

---

## 8 · The acquisition decision, in one path

Work down it and record the answer at each step:

1. **Is the host running?** → yes: capture volatile data first (live response, then memory), then power down and image.
   → no: do not power it on. Image the disk.
2. **Is the data encrypted at rest?** → yes: a powered-down image may be unreadable. Capture while the volume is unlocked, or capture the key material in memory.
3. **Is time short, or is the device too large to image?** → consider targeted triage, and record exactly what you chose not to collect.
4. **Which method?** → physical unless a stated reason forces logical. Record the reason.

Every answer is written down. The decision is part of the evidence.

---

## 9 · Before you leave

- Your images are made and verified.
- Both digests are recorded for every artifact.
- Your custody line is filled and the session's steps are closed on the record page.
- You can say, in one sentence, what `verified` does not cover.
