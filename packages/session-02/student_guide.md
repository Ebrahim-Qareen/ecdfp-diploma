# Session 2 — Student Guide

**Acquisition: Disk, Memory &amp; Live Response**

---

## What changes today

Session 1 was about what has to be true **before** analysis starts, and it ended with you reading the
first bytes of a file. Today you **make** the evidence.

Everything you examine in Sessions 3 to 6 comes from the images made in this session. If the
acquisition is wrong, no later analysis repairs it. That is why acquisition is a **decision**, not a
button.

| # | By the end you can |
|---|---|
| **O1** | sequence a collection on a running host by order of volatility, and state what each delay destroys |
| **O2** | capture memory from a live host, and state why the result is a smear rather than a snapshot |
| **O3** | choose physical or logical acquisition, name what each forfeits, and identify a file from its bytes |
| **O4** | create an image as E01 and as raw, and state what `verified` covers and what it does not |
| **O5** | acquire and verify the suspect USB, and write the result as a finding separated from interpretation |

---

## 1 · Live response, and the order of volatility

**Live response is collecting volatile data from a machine that is still running.** There is a
paradox at the centre of it: to preserve a running machine you must touch it, and every command
changes it. There is no clean option — only a **recorded** one.

Collection is also not free. Data stores decay at very different rates:

| # | Store | Survives |
|--:|---|---|
| 1 | CPU registers and cache | nanoseconds |
| 2 | RAM | until power is lost |
| 3 | Network state — connections, ARP, routing | seconds to minutes |
| 4 | Running processes | until reboot |
| 5 | Disk | power loss |
| 6 | Central logs | until they rotate |
| 7 | Archival media | months to years |

That ordering is the **order of volatility**: collect the most perishable first, the most durable
last. **While you collect RAM, network state is decaying. While you image the disk, both are gone.**
The order you choose is a decision about what you accept losing.

### The five rules

1. Run the collector from **external media**. Never install it on the evidence host.
2. Write output to **external media**. Never to the evidence disk — you would overwrite the
   unallocated space Session 4 needs.
3. Record **every command and its time**, as you run it.
4. Isolate the network **before** collecting, and record when.
5. Prefer one tool that does several things over many separate commands — fewer footprints.

---

## 2 · The collector — it has a name

**BriMor Labs Live Response Collection.** You run `Windows_Live_Response.bat` as administrator, from
your own external media, and choose a menu option:

| Option | What it takes |
|---|---|
| **Triage** | fastest, smallest — key artifacts only |
| **Memory Dump** | RAM only |
| **Complete** | memory **and** triage |
| `Secure-` variants | the same, compressed and password-protected |

It is a wrapper: it runs many small utilities and files their output in one structure.

```
FIN-WKS-07_2026-09-02_1412\
├── ForensicImages\
│   ├── Memory\                    the RAM capture
│   └── DiskImage\                 a disk image, if you asked for one
├── LiveResponseData\
│   ├── BasicInfo\                 host identity
│   ├── NetworkInfo\               connections, ARP, routing, DNS cache
│   ├── PersistenceMechanisms\     autoruns
│   ├── UserInfo\                  logged-on users, sessions
│   └── CopiedFiles\event logs\Logs\*.evtx
├── <hostname>_hashes.csv          one hash per collected file
└── Processing_Details.txt         every command, with start and finish times
```

**Two of those files are a record of *your own conduct*, not the host's state.**
`Processing_Details.txt` is your method section, written as you worked — ISO/IEC 27037 requires that
a third party can reconstruct what you did, and on a live host that is only possible from a
contemporaneous command record. The hash list proves the collected files have not changed **since**
collection.

### 🟢 Velociraptor — the one to use on a paid engagement

Apache 2.0 licensed, and it builds a **standalone offline collector** you carry on a USB stick: one
`.exe`, no server needed.

⚠️ **This matters commercially.** KAPE is free for classroom use but **not available for commercial
use since 1 January 2026** — that is, on a third-party network or as part of a paid engagement.
Velociraptor carries no such restriction.

### What a clean report does *not* prove

A collector asks the operating system what is running and writes down the answer. If the operating
system has been subverted, the answer is the one the attacker chose. A clean live-response report is
evidence of **what the host said about itself**, and nothing more. That is why memory is captured
too: the image can be examined later with tools that do not have to trust the OS.

---

## 3 · Memory acquisition

Memory holds what exists nowhere else: running processes, open network connections, injected code,
loaded drivers, and data that is only ever decrypted in RAM. Power off and it is gone.

Free tools: **WinPmem**, **DumpIt**, or FTK Imager's `File > Capture Memory`.

### A capture is a smear, not a snapshot

The tool reads memory from low addresses to high, and it takes minutes. **The machine keeps running
the whole time.** So the top of the dump was read at one moment and the bottom at a later one.

| This becomes unreliable | This is unaffected |
|---|---|
| a claim that two structures were consistent **with each other** at one instant | an artifact you find — it really was there |
| counts that must add up exactly | strings, injected code and connections recovered intact |

**Write it this way:** *the capture ran from 14:12 to 14:19 UTC; findings describe the state during
that window, not at a single instant.*

### What can block it

| Blocker | What you see | What to do |
|---|---|---|
| Driver signing | the tool's driver refuses to load | use a signed acquisition tool |
| Secure Boot | blocked below the OS | signed tool, or record that capture was impossible |
| A hypervisor | the guest sees only its own memory | capture at the host, or take the VM memory file |
| Anti-cheat / EDR driver | blocked, or the host crashes | coordinate with the vendor; record the refusal |

**A failed capture is a finding.** Record the tool, its version, the exact error and the time.

### Check your own capture

The dump should be roughly the size of physical RAM. If it is much smaller the capture did not
finish — check **before** power-down, because afterwards there is nothing left to re-run.

---

## 4 · Acquisition scope, and image formats

| | **Physical** | **Logical** |
|---|---|---|
| Reaches | every sector on the device | allocated files only |
| Includes | slack, unallocated space, deleted remnants, HPA/DCO | the files you can see, and their metadata |
| Choose when | you can take the whole device | the device is enormous, or scope is narrow |

**This decision caps every later session.** Session 4 recovers deleted staging files from
**unallocated space**. A logical image taken today makes that impossible — the data is simply not in
your evidence.

### The four methods

| Method | Forfeits |
|---|---|
| **Disk-to-image** | nothing — the default |
| **Disk-to-disk (clone)** | compression, metadata, embedded hash; needs a disk as large as the source |
| **Sparse** | everything outside the selection |
| **Logical** | slack, unallocated space, deleted data |

### The three containers

| | **raw (`dd`)** | **E01 (EWF)** | **AD1** |
|---|---|---|---|
| Contents | bytes, nothing else | bytes plus structure | selected files only |
| Metadata | none | case, examiner, times | container metadata |
| Compression | no | yes | yes |
| Built-in integrity | **none** | per-chunk CRC + embedded hash | container hash |
| Read by | everything | most forensic tools | AccessData tools — **Autopsy cannot open AD1** |

🔴 **The catch:** E01's embedded hash verifies **the image against itself**. It does not re-read the
source device.

---

## 5 · What `verified` covers — and what it does not

This is the most important idea in the session.

| The tool **did** | The tool **did not** |
|---|---|
| hash the data as it wrote the image | re-read the source drive |
| read the image back and hash it again | prove the image matches the original **now** |
| prove the two match — the write was clean | prove nothing was altered before you arrived |

**You may write:** *`F-02` — the acquisition log records the image hash as `<value>` and the read-back
verification as `verified` (FTK Imager 8.3).*

**You may not write:** ~~the image is verified, so the disk was not tampered with.~~

Verification covers the copy. The history of the original is the chain of custody's job.

---

## 6 · `dc3dd` and targeted triage

| | `dd` | `dc3dd` **7.3.1** | triage |
|---|:-:|:-:|:-:|
| Hashes while imaging | ✗ | ✅ | ✅ per file |
| Writes a log | ✗ | ✅ | ✅ |
| Handles read errors | ✗ | ✅ | n/a |
| Scope | whole device | whole device | **selected artifacts only** |

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

The log ends with the hash — proof it was computed **at acquisition time**, not afterwards. Plain
`dd` gives you neither, so you must hash the source and image separately and record them by hand.

**What triage forfeits:** unallocated space, slack, deleted files, and anything not on the target
list. **You cannot answer a question about data you chose not to collect** — so record what you left.

---

## 7 · Signature vs extension, on what you acquired

In Session 1 you read the first bytes of a single file. Now you run that across a whole image,
because the first thing an examiner asks of a file set is *are these files what they claim to be?*

| Type | Signature | Note |
|---|---|---|
| JPEG | `FF D8 FF` | ends `FF D9` — Session 3 finds things after that |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | the `89` catches a 7-bit transfer |
| ZIP / DOCX | `50 4B 03 04` | ASCII `PK`. A `.docx` **is** a ZIP of XML |
| OLE (legacy `.doc`) | `D0 CF 11 E0 A1 B1 1A E1` | a macro lives somewhere different from OOXML |

**When the name and the bytes disagree, the bytes win.**

**Finding:** *the file at `\Users\l.bennett\holiday_snap.jpg` begins `50 4B 03 04`, the ZIP signature.*
**Interpretation:** *the file is a ZIP archive carrying a `.jpg` extension.*
**Cannot prove:** *that it was renamed deliberately, or by whom.*

---

## 8 · The acquisition decision, in one path

1. **Is the host running?** → yes: volatile data first, then power down and image. → no: do not power it on.
2. **Is the data encrypted at rest?** → a powered-down image may be unreadable. Capture while unlocked.
3. **Is time short, or the device too large?** → consider triage, and record what you did not collect.
4. **Which method?** → physical unless a stated reason forces otherwise. Record the reason.

Every answer is written down. **The decision is part of the evidence.**

---

## 9 · Before you leave

- Images made and verified, both digests recorded.
- Start **and** finish times recorded for the memory capture.
- Your custody line filled and the session's steps closed on the record page.
- You can say in one sentence what `verified` does not cover.
