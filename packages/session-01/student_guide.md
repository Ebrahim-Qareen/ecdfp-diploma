# Session 1 — Student Guide

**Forensic Foundations, Evidence Integrity & Chain of Custody**

---

## What changes today

You can already decide whether something is bad. From today you work to a different standard:
**can you defend it in front of someone whose job is to break it?**

That is the difference between detection and evidence, and it is what the rest of this diploma is
built on.

This session needs **no forensic software**. Two built-in commands and a text editor. Everything
after it needs software, and none of that software repairs work that was unsound at the start.

---

## 1 · What digital forensics is

**The mandate:** recover, preserve and interpret artifacts from digital devices so the result
survives challenge as evidence.

**The evidence life cycle:** `acquisition → analysis → presentation`

The order is not administrative. **Each phase can destroy the one after it.** Opening a file "just
to read it" can update its last-access time — acquisition has failed and analysis inherits a
corrupted timestamp.

> On current Windows builds last-access updates are disabled by default, so this specific effect
> often does not occur. The principle still holds: any action on evidence is a change until you
> can show it was not.

### What you may not claim

| ✅ You may write | ❌ You may not write |
|---|---|
| the artifact recorded X at time T | the user did X |
| the file was not present in the collected set | the file was never on the machine |
| the process was running at collection time | the process was running at the time of compromise |

### Why this course is Windows-weighted

Linux equivalents of the Windows artifacts are weaker in every case that matters: there is no
`USBSTOR` equivalent at all, login records get deleted outright, `.bash_history` carries no
timestamps and a command prefixed with a space is silently omitted from it, and no Autopsy module
parses Linux persistence artifacts.

Reading down the Linux column is itself the argument for concentrating on Windows.
Linux and macOS forensics are out of scope for this diploma — decided, not overlooked.

---

## 2 · Forensic principles

### Order of volatility — collect the most fragile first

| # | Store | Survives |
|--:|---|---|
| 1 | CPU registers and cache | nanoseconds |
| 2 | RAM — processes, connections, sessions, clipboard | until power loss |
| 3 | Network state | seconds to minutes |
| 4 | Temporary and paging areas | until overwritten |
| 5 | Disk | power loss |
| 6 | Remote logs | retention policy |
| 7 | Removable and archival media | years |

Collection takes time. Every minute spent on the disk is a minute RAM is being overwritten.

**The rule has an exception, and knowing it is the point.** If a wiper is actively running,
pulling power is correct — you lose RAM deliberately to save the disk. A rule you can only recite
is a rule you cannot apply.

### Minimal footprint

Touch as little as possible, and record everything you touch.

### Repeatable and reproducible — both are required

| | Meaning |
|---|---|
| **Repeatable** | same lab, same tools, same result |
| **Reproducible** | **different** lab or tools, same result |

This is why *"I used the GUI and clicked around"* is not a method. If another analyst cannot
follow your steps and reach your result, you have an anecdote.

### Always work on a copy

Hash the original, shelve it, work on a copy under a different filename. Working on the original
is a defect, not a shortcut.

---

## 3 · What makes evidence defensible

| Test | Means |
|---|---|
| **Relevant** | proves or disproves a hypothesis in *this* case |
| **Reliable** | **authentic** (proven by the chain of custody) and **objective** (a fact, not an opinion) |
| **Competent** | obtained legally, without breaching protected confidentiality |

**Of these, the examiner owns authenticity.** Relevance and competence are legal questions.

A video that convicts the suspect is thrown out because the warrant covered text files only:
perfect forensics, inadmissible evidence. Separating the three tests is what lets you see that
the forensics was not the failure.

---

## 4 · Findings and interpretation — the core of this course

Everything you write for the rest of this diploma is graded on this. Three categories, not two.

| | Border | Contains |
|---|---|---|
| **FINDING** | **solid** | only what the artifact literally says — artifact named, exact path given |
| **INTERPRETATION** | **dashed** | your reasoning, citing the findings it rests on |
| **CANNOT PROVE** | **dotted** | what this evidence cannot show, however it is read |

**The test for a finding:** if it needs the word *because*, it is not a finding.

**The border style carries the meaning, not just the colour.** A solid line is something you
observed. A dashed line is something you reasoned to.

### A worked triple

> **FINDING** — the FTK Imager log for `EVI-SRC01.E01` reads `MD5 checksum: <value> : verified`
> and `SHA1 checksum: <value> : verified`, with acquisition start and finish timestamps.

> **INTERPRETATION** — the image was written and read back without corruption, so the file on the
> destination drive is very probably a faithful copy of whatever the tool read from the source.

> **CANNOT PROVE** — that the **source** is unaltered. The tool hashed its own read and its own
> write-back; it never re-read the drive. It cannot show that a write blocker was in the path,
> that the physical device selected was the one on the custody form, or that the read covered the
> whole medium.

**Read the log again with one question: which lines describe the source?** Almost none of them do.

### The two line formats — write these from memory

> **F-07** — `System.evtx` on `WKSTN-07`, record 41 992, Event ID 7045,
> `2026-03-03 09:12:55 UTC`: a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

> **I-03** — The service in **F-07** is assessed, with high confidence, to be attacker
> persistence: its name imitates a Microsoft component, its binary sits in a user-writable temp
> directory, and it was installed 41 seconds after the document execution in **F-05**.
> Considered and not excluded: a legitimate third-party installer using a misleading name — no
> corresponding installer entry was found in `Application.evtx`, but the log covers only 6 days
> (**F-02**).

An interpretation is acceptable when it does three things: **cites finding numbers**, **states a
confidence**, and **names an alternative** it considered and could not exclude.

### Banned in the Findings section

*clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
unauthorised*

Each is an interpretation wearing a finding's clothes.

**Banned everywhere:** two date formats in one report · two terms for one thing · sentences of
25–30 words · jargon with no glossary entry · **any sentence assigning guilt.**

> **You are not the judge.** Never write "in my opinion Mr X committed this crime." Present method
> and evidence. The decision is not yours.

### A limitation is worth marks

Criterion 4 awards marks for stating what your evidence cannot show. A report with no stated
limitation is a report that nobody senior believes.

---

## 5 · The analyst toolkit and the `CLEAN-TOOLS` snapshot

`FOR-WS01` arrives as a clean Windows VM with no forensic tooling. You install the kit and take a
snapshot named exactly `CLEAN-TOOLS`.

**The snapshot is the lesson.** It is a known-good baseline you can always return to. Later
sessions refer to it by name.

### Three tools this course names and does not distribute

| Tool | Why not |
|---|---|
| **RegRipper 4.0** | its licence permits personal and academic use only, and bars inclusion in vendor training or any distribution. This is paid training, so the course stays on **RegRipper 3.0** (MIT) |
| **010 Editor** | commercial software with a 30-day evaluation and no free tier. **HxD** is free for commercial use and does everything this course needs |
| **Xiao Steganography** | no working vendor site exists; every available copy is a third-party mirror dating to 2010 or earlier |

**This is a finding, not an oversight.** RegRipper 4.0 has new plugins and MITRE ATT&CK mappings —
a capability declined on licence grounds and recorded as a decision.

Check a tool's licence for the version you use **and the version one ahead**. Licences change
between releases, and three tools in this course have been caught by exactly that.

---

## 6 · Cryptographic hashing — what it proves, and what it does not

A hash is a one-way function producing a fixed-length digest. Any change, however small, changes
the digest completely.

### Self-review — run this yourself

```powershell
"Evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

Expected: a 64-hex-character digest and the file path.

Now change one capital letter:

```powershell
"evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

Expected: a completely different digest.

The Linux equivalent:

```bash
sha256sum evidence.txt
```

> **Generate digests yourself. Never copy one from a slide or a document** — a transcribed digest
> is a digest you cannot defend.

**What that demonstrates:** the file changed. **Not** who changed it, **not** when, and **not**
whether the original was ever genuine.

### Two different questions

| Question | Answer with | Why |
|---|---|---|
| *"Have we seen this exact file before?"* | MD5 is acceptable | **preimage** resistance still holds. NIST's own NSRL ships MD5 and SHA-1 hash sets precisely for this, to eliminate known files from an investigation |
| *"Is this file unaltered?"* | **SHA-2 / SHA-3 only** | **collision** resistance is broken for MD5 and for SHA-1 |

The same agency publishes MD5 hash sets for forensics and excludes MD5 from approved
cryptography — because these are different problems.

**Course standard: record MD5 *and* SHA-256 for every artifact. SHA-256 is what you defend; MD5 is
a secondary lookup key.** A chain of custody signed against an MD5 is a chain whose integrity
claim can be forged.

### What a hash does not prove — four things

1. **Not authenticity, not provenance.** A match says the copy equals the source *as read at that
   moment*. It says nothing about where the source came from, who owned the data, or whether it
   was already altered before you arrived.
2. **Not completeness.** A hidden area of the disk excluded from the read is excluded from both
   hashes — and they match perfectly.
3. **A mismatch is not proof of tampering.** A failing sector, a cable fault, or an SSD's own
   background garbage collection between two reads all produce mismatches with nobody doing
   anything wrong.
4. **Not protection, if stored alongside the evidence.** Someone holding both the data and the
   hash alters the data and recomputes the hash. **Store the hash securely and separately.**

### Sources worth reading

- CERT/CC **VU#836068** — *MD5 vulnerable to collision attacks*
  <https://www.kb.cert.org/vuls/id/836068>
- NIST — *NIST retires SHA-1 cryptographic algorithm*
  <https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm>
- NIST **NSRL** — why MD5 hash sets are still published
  <https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl/about-nsrl/nsrl>

---

## 7 · Chain of custody

The unbroken, contemporaneous record of who held an exhibit, when, and what they did to it — from
seizure to case close.

**Minimum fields:** what the evidence is · how it was acquired · when · by whom · where stored ·
and **every subsequent action**.

**Physical controls are part of it:** antistatic bag, padding, sealed container, **tape signed and
written across the seal** so re-opening is visible, and controlled temperature and humidity.

**No software produces a chain of custody.** It is a document and a set of physical controls. That
is the lesson.

### How to read one

Check three things:

1. no unexplained time gaps
2. no transfer without two signatures
3. hash values recorded at seizure that still match today

### The asymmetry

An unbroken chain does not by itself win admissibility. **A single unexplained gap is enough to
lose it**, because the other side only has to raise the *possibility* of substitution or
alteration.

### What it does not prove

That the **data** is genuine. A wiper that ran before seizure leaves the custody record perfect
and the evidence gutted.

The commonest real failure is not malice. It is two identical drives from the same office, both
unlabelled. After that, no form can say which desk each came from.

---

## 8 · Write blocking, and how you prove you used one

A write blocker filters write commands out of the path before they reach the media. Hardware: an
inline dock. Software: a forensic boot disc, or a Windows registry policy.

It matters because **attaching a disk to a running Windows machine is itself a write** — Windows
touches the volume, updates journal state, and can mount and modify without being asked.

### The problem this block exists for

**An image taken on a write blocker and an image taken without one are byte-identical.** Nothing
in the image records that you used one. The fact lives only in your documentation, and it cannot
be recovered afterwards if you did not write it down.

### The proof trail — four parts

| # | Part | Why it counts |
|--:|---|---|
| 1 | **Source hash before and after the imaging run** | the actual technical proof — two matching source hashes across the run |
| 2 | The blocker's own display or log | the device attesting to its own state |
| 3 | A photograph of the connected rig, serials legible | taken **before** disconnecting anything |
| 4 | The custody line naming blocker make, model, serial and firmware | written at the time, not reconstructed |

### And the honest limit

> Two identical source hashes are **consistent with** an effective write block. They do not
> **prove** a blocker was used — they are equally consistent with a correctly-set software policy,
> or with a system that simply did not touch the volume. The blocker is evidenced by the
> photograph, the serial on the form, and contemporaneous notes.

### The software fallback, and its classic failure

`HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` → `REG_DWORD` `WriteProtect` = `1`.

This value sits in the **examiner's** registry, not the evidence's. Finding it set proves something
about the analysis workstation and **nothing at all about how any particular exhibit was handled**.
It is not per-device and not timestamped. It also covers only devices enumerated as USB mass
storage — not a SATA disk on an internal port, and not a drive in a dock that presents as a fixed
disk.

> **The classic false positive:** set the value, fail to reboot, plug the evidence in, and report
> "software write blocked". Windows will write to it happily.
> **Demonstrate the block on a scratch stick before touching evidence. Never assume it.**

A blocker also protects only the path it is in. It does not stop the same source being mounted
read-write on another port, does not protect other exhibits on the bench, and cannot undo damage
already done — a machine booted once before you arrived has its altered state preserved perfectly.

---

## 9 · The closing ritual

Every session ends the same way, all six:

1. **Re-hash** every evidence file against the manifest.
2. **Write one custody line:** who · what · when · from where · hash · where stored.
3. **Sign it.**

This is the habit the exam tests, not a formality.

---

## Key terms

| Term | Definition |
|---|---|
| **Acquisition** | producing a forensic copy of evidence media |
| **Admissibility** | whether evidence may be heard: relevant · reliable · competent |
| **Authenticity** | that the evidence is what it is claimed to be — proven by the chain of custody |
| **Chain of custody** | the contemporaneous record of possession and handling of one exhibit |
| **Collision resistance** | that two different inputs cannot feasibly be made to produce the same digest. **Broken for MD5 and SHA-1** |
| **Commingling** | mixing evidence from different sources so the origin of a byte can no longer be established |
| **Exculpatory** | evidence that contradicts the hypothesis |
| **Finding** | a single observable fact, tied to one named artifact at an exact path |
| **Forensic soundness** | the process preserved the evidence's meaning, and can be shown to have done so |
| **Inculpatory** | evidence that supports the hypothesis |
| **Integrity** | that the data has not changed — what a hash shows |
| **Interpretation** | reasoning drawn from findings, citing them, with a confidence and an alternative |
| **Limitation** | what the evidence cannot show, however it is read |
| **Order of volatility** | collect from the most fragile store first |
| **Preimage resistance** | that an input cannot feasibly be recovered from a digest. **Still holds for MD5** — which is why lookup survives |
| **Provenance** | where the evidence came from |
| **Repeatable** | same lab, same tools, same result |
| **Reproducible** | different lab or tools, same result |
| **Write blocker** | hardware or software that filters write commands before they reach the media |
