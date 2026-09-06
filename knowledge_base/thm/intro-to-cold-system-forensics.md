---
room: Intro to Cold System Forensics
url: https://tryhackme.com/room/introtocoldsystemforensics
module: Disk Image Analysis — **walkthrough room**, concept-only. **Priority 3.**
       🟢 Task 6 names the module's other rooms — *"Forensic Imaging, Autopsy, DiskFiltration,
       ExfilNode"* — **confirming that rooms 16, 21 and 22 belong to this module.**
feeds: `S1-02`, `S1-03`, `S1-06`, `S1-07`, `S2-01`, `S2-04`. **Vocabulary and framing, not technique.**
       🔴🔴 **Three factual errors our material must not inherit — including a recommendation to use
       MD5 and SHA-1 for evidence integrity** (§3 #1), which contradicts `S1-06` directly.
difficulty / time: Info-level walkthrough · 60 min · 6 tasks · 9 scored questions · Premium ·
                   13,306 completions · **305 recommends — the most-recommended room in this
                   extraction**
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (accordion loop, 6/6 tasks)
completeness: **all 6 tasks read in full** (~21 KB). 0 sections NOT READ.
              ⚠️ **Priority 3, deliberately short.** Concept room — no lab, no evidence, no commands.
              🟢 No credentials published.
              ⚠️ **Task 5's external static-site exercise was NOT visited** (§4).
              ⚠️ **Extraction note:** the first loop attempt returned `[BLOCKED: Cookie/query string
              data]` **and did not run at all** (`0 of 0`), not merely a blocked output. **A
              screenshot forced the render and the retry worked** — documented failure modes 3 and 5
              together, and worth adding to the recipe.
---

## 1. What the room teaches

**The vocabulary and the ethics of dead-box forensics — competently, to a beginner — with three
factual errors that a course must not inherit.**

🟢🟢 **Its best contribution is the cold-versus-live comparison table**, which is the framing our
`S2-04` row (*"Physical vs logical acquisition"*) needs one level up: **system state, evidence
integrity, data capture, volatile access, time, volume, legal suitability, and access to encrypted
files.** Eight axes, and the last one is the sharpest — *"Access to Encrypted Files: Risk of losing
access if passwords are reset"* on cold versus *"Immediate access while the system is running"* on
live. **That is the full-disk-encryption dilemma stated as a table row**, and it pairs exactly with
room 23's GRUB finding (**K6**): *pull the plug on an encrypted machine and you may never get in.*

🟢 **Its seven "common scenarios" list is genuinely useful** and includes two our material does not
name: **legacy systems** *"where live analysis is not feasible due to outdated or unstable systems"*,
and **cloud/virtualised environments**, where a provider *"might create snapshots of VMs suspected of
being compromised… This ensures that customer services remain uninterrupted."* ⚠️ **The second is
worth one sentence in `S2-04`** — a VM snapshot is a cold acquisition of a live system, which does
not fit neatly into either column.

🟢 **The order-of-volatility list is correct and well-ordered** — registers/cache → routing table,
ARP cache, process table, kernel statistics and RAM → temporary file systems → hard disk → remote
logging → physical configuration and topology → archival media. **RFC 3227's shape**, and it matches
our `S2-01`.

**What it gets wrong — and the first is the one that matters:**

- 🔴🔴 ***"Hashing: Using cryptographic hash functions such as MD5 and SHA-1 to create unique data
  fingerprints and verify that it has not been altered."*** **Those are the two algorithms that must
  not be used for integrity**, and SHA-256 is not mentioned. §3 #1. **This directly contradicts
  `S1-06`.**
- 🔴🔴 **Its history is inverted.** *"Cold system forensics emerged as a direct response to a
  malicious technique known as a cold boot attack."* §3 #2.
- 🔴 ***"Guymager … provides built-in write-blocking functionality."*** An imaging tool does not
  provide write blocking. §3 #3.

⚠️ **And its integrity column overstates the case.** The table gives cold forensics *"Evidence
Integrity: Minimal risk"* and Task 4 says *"always mount images in read-only mode"* — 🔴 **but per
E5, `-o ro` alone is insufficient**: mounting an evidence image still writes mount count, mount time,
`s_last_mounted`, atimes and can replay the journal. **"Minimal risk" is the belief that produced
four of the corpus's seven evidence defects.**

## 2. Artifacts — one 6-box block each

⚠️ **No evidence and no commands.** These blocks treat the room's **process concepts** as the
artifacts they govern, which is what a concept room can honestly supply.

### 2.1 The cold/live decision itself

- **What it is** — the choice the whole room is about: examine powered-off, or examine running.
- **Where it lives** — in the first ten minutes of an engagement, and in the report's method section.
- **What it proves** — nothing; it **determines what can be proved later.**
- **What it does NOT prove** — 🔴🔴 **that it is a binary choice, which the room's table implies.**
  The room's own scenarios contradict it: *"forensic analysts might initially opt for live response
  techniques and later perform cold analysis on a cloned disk image"*, and the VM-snapshot case is
  **a cold acquisition of a running system.** 🟢🟢 **The real-world answer is almost always both, in
  order** — which is `S2-01`'s order of volatility, and the room states the sequence in prose while
  drawing it as a dichotomy.
  ⚠️ **And the table's *"Volatile Memory Access: Cannot retrieve"* for cold is wrong as stated** —
  `hiberfil.sys` and `pagefile.sys` are RAM contents **inside the disk image** (room 30 §2.7).
  **Cold forensics retrieves *some* volatile memory, and saying otherwise loses a real artifact.**
- **How to parse it** — n/a; it is a documented decision, and **documenting it is the deliverable.**
- **Anti-forensics / false-positive caveat** — 🔴 **the decision is often made for you** by whoever
  reached the machine first. **"Was the system powered off before you arrived, and by whom?" is a
  chain-of-custody question**, and the room does not ask it.

### 2.2 Order of volatility

- **What it is** — *"the sequence in which data should be collected based on its volatility."*
- **Where it lives** — the collection plan.
- **What it proves** — 🟢 that the collector understood what they were destroying by not collecting
  it first.
- **What it does NOT prove** — ⚠️ **that the order was followed.** It is a doctrine, and **the
  evidence that it was followed is the acquisition log, not the artifacts.** 🔴 **Nothing in a
  disk image records whether memory was taken first.**
  🟢🟢 **The room's list is more complete than most**, and two entries deserve calling out because
  our own material skips them: **"Physical Configuration and Network Topology"** — *"Documenting this
  data helps analysts understand the infrastructure and context"* — and **"Archival media"**. **Both
  are collection targets that no tool produces; a human writes them down or they do not exist.**
- **How to parse it** — n/a.
- **Anti-forensics / false-positive caveat** — ⚠️ **the order is a default, not a rule.** A live
  ransomware encryption run inverts it: **stopping the destruction may outrank preserving volatile
  state**, and that is a judgement the doctrine does not make for you.

### 2.3 Disk imaging and write blocking

- **What it is** — *"a bit-for-bit copy of a disk"*, taken behind a write blocker.
- **Where it lives** — the acquisition step; the image and its log.
- **What it proves** — that the copy is a faithful reproduction **at the moment it was taken**.
- **What it does NOT prove** — 🔴🔴 **that the original was not modified before you arrived**, and
  🔴 **that a software write blocker worked.** Per **E6**, **NIST CFTT has never tested a Linux
  software write blocker** — *"software write-blocking on Linux is effective and unvalidated."*
  ⚠️ **The room says both hardware and software blockers "perform the operations" without
  distinguishing their evidential weight**, which is the distinction that matters in court.
  🔴 **And "Guymager provides built-in write-blocking functionality" is wrong** (§3 #3) — an imager
  writes an image; it does not interpose on the source device.
- **How to parse it** — n/a. 🟢🟢 **The room's best line is the one nobody follows:** *"It is also
  crucial to document the use of write blockers in the data acquisition logs to inform any other
  individual working on the investigation."* **Which blocker, which serial number, verified how.**
- **Anti-forensics / false-positive caveat** — 🟢 **the verification is the hash, and the hash is the
  room's error** (§3 #1).

### 2.4 Physical acquisition — chip-off and JTAG

- **What it is** — *"removing and imaging hard drives from the target system"*, and beyond it
  **chip-off** (*"removing the storage chip from the device and reading it with specialised
  equipment"*) and **JTAG** (*"the Joint Test Action Group interface to access data from embedded
  systems"*).
- **Where it lives** — a bench, not a keyboard.
- **What it proves** — access to storage that the running system will not give up.
- **What it does NOT prove** — 🔴🔴 **that the data will be interpretable.** Chip-off yields **raw
  NAND**, which still needs the controller's wear-levelling, ECC and address translation reversed —
  **a dump is not a file system.** ⚠️ **And chip-off is destructive and irreversible**: get it wrong
  and there is no second attempt, which makes it a decision with no undo.
  🔴 **On modern devices with hardware-backed encryption, chip-off yields ciphertext** and the key
  lives in a secure element that was left on the board. **The room does not say this**, and it is the
  reason chip-off has become far less useful than its reputation.
- **How to parse it** — out of scope for us entirely.
- **Anti-forensics / false-positive caveat** — 🟢 **worth one sentence in `S2-04` precisely to say we
  do not do it**: naming the technique and its limits is how students learn where the boundary of the
  course is.

### 2.5 Secure storage of acquired evidence

- **What it is** — the room's four practices: **strong encryption (AES-256)**, **access control**,
  **environment control**, **regular audits**.
- **Where it lives** — the evidence store, after acquisition.
- **What it proves** — that the copy was protected between acquisition and analysis.
- **What it does NOT prove** — ⚠️ **that it was not altered — encryption protects confidentiality,
  the hash protects integrity, and they are different guarantees.** 🔴 **The room lists encryption
  under "storage" and hashing under "chain of custody" without connecting them**, which leaves the
  impression that an encrypted image is a verified one.
  🟢🟢 **And it raises something our material genuinely lacks: `evidence/` is gitignored (D2/D22),
  but we have never said how it is protected at rest**, who may access it, or how that access is
  logged. **That is an `S1-07` gap, not a room criticism.**
- **How to parse it** — n/a.
- **Anti-forensics / false-positive caveat** — 🔴 **an encrypted evidence store whose key is lost is
  indistinguishable from destroyed evidence.** **Key custody is part of chain of custody.**

### 2.6 Chain of custody

- **What it is** — *"the documentation of the responsible personnel in charge of evidence, its
  transfer from the point of collection to its presentation."*
- **Where it lives** — the form, and **only** the form.
- **What it proves** — 🟢🟢 **who held the evidence, when, and why they touched it.** The room's four
  guidelines are right: **document every step**, **secure transport** in tamper-proof packaging,
  **hashing**, **write blocking**.
- **What it does NOT prove** — 🔴🔴 **that the documentation is true.** A chain of custody is an
  **assertion by people**, corroborated by hashes and seals. **The hash is what makes the paperwork
  checkable** — which is why §3 #1's algorithm error is not pedantry: **a chain of custody signed
  against an MD5 is a chain whose integrity claim can be forged** (**K7**).
  ⚠️ **And "document every step, no matter how small" is the guideline everyone endorses and nobody
  follows.** 🟢 The corpus supplies the concrete version: **record the examiner's own footprint** —
  room 24's EZ Tools writing Prefetch and Amcache entries, room 23's bootloader boot, room 29's
  profile replacement. **That is what "every step" means and it is more persuasive than the rule.**
- **How to parse it** — n/a. **It is `S1-07` and `D20` criterion 1.**
- **Anti-forensics / false-positive caveat** — 🟢 **the room correctly ties admissibility to
  integrity** and repeats it across three tasks. **Our D7/D20 says the same thing in the language of
  a rubric.**

### 2.7 The imaging and analysis toolset

- **What it is** — the room's tool survey. **Imaging:** `dd`, `dc3dd`, **Guymager**, **FTK Imager**.
  **Analysis:** **TSK** (`fls`, `icat`, `tsk_recover`), **Autopsy**, **EnCase**, **FTK**,
  **Magnet AXIOM**, plus `bulk_extractor` and X-Ways in passing.
- **Where it lives** — the analyst workstation.
- **What it proves** — nothing; it shapes what can be found.
- **What it does NOT prove** — ⚠️ **that a tool reads what you have.** The corpus now has three
  instances: **Autopsy cannot open AD1** (**O1**), **Autopsy supports neither VDI nor AFF4**
  (**E4**), and **`mac_apt` reads AFF4 and DMG which Autopsy does not** (**P4**). 🔴 **The room lists
  formats — *"E01, AFF, raw"* — without ever saying that tool and format must be matched before an
  evidence set is chosen.**
  ⚠️ **Currency notes on the imaging four:** `dd` is *"the foundational tool"* — 🔴 **but per A5 it is
  no longer GNU's recommendation for damaged media**; `dc3dd` is correct and **dormant, not dead**
  (**A6**); **FTK Imager is 8.3, Exterro, still free** (**O1**).
- **How to parse it** — n/a.
- **Anti-forensics / false-positive caveat** — 🟢 **the room's "Associated Risks and Common Mistakes"
  section is good and short**: verify the hash before *and after* analysis, correlate across tools to
  avoid *"misinterpretation of data"*, and *"understand each tool's limitations."* 🟢🟢 **That last
  phrase is the whole currency file in four words.**

### 2.8 The mounting step

- **What it is** — *"Mounting a disk image creates a virtual representation of the original drive.
  This allows forensic analysts to explore file structures without altering the original image."*
- **Where it lives** — between acquisition and analysis.
- **What it proves** — nothing; it is a convenience.
- **What it does NOT prove** — 🔴🔴 **that the image was not altered, and this is the corpus's most
  repeated defect.** The room says *"always mount images in read-only mode or within a forensic
  environment"* — 🟢 correct as far as it goes — **but per E5, `-o ro` alone is not sufficient**:
  mount count, mount time, `s_last_mounted`, atimes and **journal replay on a dirty image** all
  write. The verified incantation is **`ro,noload,noatime` over a `losetup -r` read-only loop
  device.**
  🔴 **Four of the corpus's seven evidence defects are this exact error** (rooms 22, 23, 24, 29), and
  **this room is where a student learns the rule that is not quite strong enough.**
  🟢🟢 **Room 28's `apfs-fuse` is the counter-example worth pairing with it** — *"a read-only FUSE
  driver"*, which cannot write **by construction** rather than by flag (**P4**). **Prefer a tool that
  cannot write over a tool that must be told not to.**
- **How to parse it** — as above; **hash before and after the mount and record both** (`S4-11`).
- **Anti-forensics / false-positive caveat** — 🟢 **the demonstration beats the rule**: show students
  a careless mount changing the hash. **It is the single most convincing five minutes available in
  `S2`.**

## 3. Tools and commands

**No commands.** The room names tools; §2.7 covers them.

### CURRENCY CHECK

| # | claim as the room teaches it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"Hashing: Using cryptographic hash functions such as **MD5 and SHA-1** to create unique data fingerprints and verify that it has not been altered."* | 🔴🔴 **Both are broken for exactly the property being claimed, and SHA-256 is not mentioned.** **MD5** — CERT/CC VU#836068: *"Weaknesses in the MD5 algorithm allow for collisions in output. As a result, attackers can generate cryptographic tokens or other data that illegitimately appear to be authentic"* (**K7**). **SHA-1** — NIST: *"Today's more powerful computers can create fraudulent messages that result in the same hash as the original… These 'collision' attacks have been used to undermine SHA-1 in recent years"*, and *"We recommend that anyone relying on SHA-1 for security migrate to SHA-2 or SHA-3 as soon as possible."* NIST will stop using SHA-1 in its remaining protocols **by 31 Dec 2030**. 🟢🟢 **The distinction the room misses is the one `S1-06` teaches: MD5 and SHA-1 answer *"have we seen this file before?"*; only SHA-2/SHA-3 answer *"is this file unaltered?"*** — and **a chain of custody signed against an MD5 is a chain whose integrity claim can be forged.** **Record both; attest to SHA-256.** | [CERT/CC VU#836068](https://www.kb.cert.org/vuls/id/836068) · [NIST retires SHA-1](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) |
| 2 | *"Cold system forensics emerged as a direct response to a malicious technique known as a cold boot attack… Initially focused on memory analysis, cold system forensics has evolved into a discipline encompassing the examination of the entire dormant system."* | 🔴🔴 **The causality is inverted and the two ideas are conflated.** A **cold boot attack** exploits DRAM remanence to recover keys from a powered-off machine; **cold system / dead-box forensics** is the examination of a powered-off system's storage. **Dead-box disk forensics is the older discipline — it is what digital forensics *was* — and *live* forensics emerged later**, as a response to encryption, volatile-only malware and systems that cannot be taken down. The room has it exactly backwards, and its claim that the field *"initially focused on memory analysis"* and later grew to include disks describes the reverse of what happened. ⚠️ **Stated from general knowledge — NOT VERIFIED against a cited history in this pass**, which is a proportionate choice for a Priority-3 concept room. **But do not repeat the room's version**, and do not repeat mine on a slide without a citation either. | ⚠️ **NOT VERIFIED** — flagged, not cited |
| 3 | *"Guymager … provides built-in write-blocking functionality"* | 🔴 **An imaging tool does not provide write blocking.** Guymager reads a source device and writes an image; **write blocking interposes between the host and the source**, in hardware or as a kernel-level software blocker. Guymager's genuine forensic features — multiple formats (E01/AFF/raw), **MD5/SHA-1 during acquisition** (⚠️ see #1), and logging — are correctly described; the write-blocking claim is not. 🟢🟢 **CONFIRMED as an error against Guymager's own documentation** (back-propagated from room 32, 2026-08-29). Guymager's homepage says only *"Guymager is a free forensic imager for media acquisition"*, with features *"Generates flat (dd), EWF (E01) and AFF images, supports disk cloning"*; its man page adds *"Guymager should be run with root privileges, as other users do not have access to physical devices normally"* — **which is the opposite of a write blocker: it documents that the tool needs raw device access.** A full-text search for *write block* / *write-block* / *write blocker* / *write protect* returns **zero matches in either source.** 🔴 And per **E6**, the distinction matters more than the room implies: **NIST CFTT has never tested a Linux software write blocker.** | block **E6** · [Guymager](https://guymager.sourceforge.io/) · [man page](https://manpages.debian.org/testing/guymager/guymager.1.en.html) |
| 4 | the tool and format survey | 🟢 **Broadly current**, with three notes from existing blocks: `dd` is *"the foundational tool"* but 🔴 **no longer GNU's recommendation for damaged media** (**A5**); `dc3dd` is correct and **dormant, not dead** (**A6**); **FTK Imager is 8.3, Exterro, still free** (**O1**). 🔴 **The survey lists formats and tools separately and never says they must be matched** — the corpus now has three counter-examples: **Autopsy cannot open AD1** (**O1**), **supports neither VDI nor AFF4** (**E4**), and **`mac_apt` reads AFF4 and DMG that Autopsy cannot** (**P4**). | blocks **A5**, **A6**, **E4**, **O1**, **P4** |
| 5 | *"always mount images in read-only mode"* | 🔴 **Necessary and not sufficient** — **E5**: mounting still writes mount count, mount time, `s_last_mounted`, atimes, and **replays the journal on a dirty image**. Use **`ro,noload,noatime` over `losetup -r`**. 🟢🟢 **And prefer a tool that cannot write at all** — room 28's `apfs-fuse` is *"a read-only FUSE driver"* (**P4**). **Four of the corpus's seven evidence defects are this error.** | block **E5** · block **P4** |

### NOT VERIFIED

- **The history of cold vs live forensics** (#2) — my correction is as uncited as the room's claim.
- ~~**Guymager's documented feature list** (#3).~~ 🟢 **CLOSED 2026-08-29** — verified against the homepage and man page; the write-blocking claim is refuted, not merely doubted. See the updated #3 row.
- **Task 5's external static-site exercise** — not visited (§4).

## 4. Evidence used

**None.** No lab, no image, no commands. 🔴 **`ecdfp-evidence` action: none** — `EVS-10` unallocated,
**tenth room running.**

⚠️ **Task 5 is a second off-platform interactive exercise** (an "Order of Volatility" challenge and a
"Chain of Custody" challenge, each yielding a flag), on an external static site. **Not visited.**
🟢 **Same disposition as room 30 §4: the idea is sound and reproducible locally in `quiz.js` (D32);
the off-platform dependency is not, because our lab runs offline (D29).** **Two of the four
Priority-3 rooms depend on an external site — which is itself worth knowing before recommending
either as pre-reading.**

## 5. Lab design worth reusing

### 5.1 🟢🟢 The eight-axis cold/live table

§1. **Adopt for `S2-04`**, with **three corrections**: *"Volatile Memory Access: Cannot retrieve"*
becomes *"limited — `hiberfil.sys` and `pagefile.sys`"* (room 30 §2.7); *"Evidence Integrity: Minimal
risk"* becomes *"low, and only with a validated write path"* (**E5**, **E6**); and a row is added for
**tool/format compatibility** (§3 #4).

### 5.2 🟢 Scenarios that name the awkward cases

Legacy systems and cloud/VM snapshots (§1). 🟢🟢 **The VM-snapshot case is the interesting one** — a
**cold acquisition of a running system**, which fits neither column and is how most modern evidence
is actually taken. **One sentence in `S2-04`.**

### 5.3 🟢 "Understand each tool's limitations"

The room's own risks section. 🟢🟢 **That phrase is the currency file's thesis in four words**, and
it is worth quoting to students when introducing why we maintain one.

### 5.4 🟢 Safety and handling defects

**None** — no lab, nothing to endanger. ⚠️ **But §2.8's insufficient mount rule is the *source* of
four defects elsewhere in the corpus**, which is a different and more interesting kind of harm: **the
room does not commit the error, it teaches the rule that permits it.**

**Running total: 11 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24, 29. Four endanger the
analyst's machine; seven endanger the evidence. Unchanged.**

## 6. Question patterns

**9 scored questions, all recall**, plus two flag submissions from the external site. 🟢 Appropriate
for a concept room.

⚠️ **One is answered by the room's own error.** *"Using hash functions seeks to minimise risks
associated with what element?"* sits in a task that recommends **MD5 and SHA-1** — so the student
learns the right principle attached to the wrong algorithms.

**🔴 Thirty-first room, no "cannot be determined" question.** The room's own text supplies three:

| the room could have asked | correct answer |
|---|---|
| *"The image hash matches the acquisition hash. Is the evidence unaltered?"* | 🔴🔴 **Not if the hash is MD5 or SHA-1** — both are broken for collision resistance (#1). **A match proves the same file only against a non-adversarial change.** |
| *"The system was powered off. Can you retrieve volatile memory?"* — **the room's own table says no** | 🔴 **Partly, yes** — `hiberfil.sys` and `pagefile.sys` are RAM contents inside the disk image (room 30 §2.7). |
| *"The image was mounted read-only. Was it altered?"* | 🔴🔴 **Possibly** — `-o ro` alone still writes mount count, mount time, `s_last_mounted` and atimes, and replays the journal on a dirty image (**E5**). |

## 7. Figures

⚠️ **Not enumerated.** The room references an illustration of *"a hardware write blocker with a USB
drive on the right"*. **Recorded as referenced-not-inspected.**

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F40 | **Cold vs live, corrected** | The room's eight axes as a two-column table, with **our three corrections applied** and each corrected cell footnoted to its block (**E5**, **E6**, room 30 §2.7). | **🔴 P1** | §5.1 — a corrected version of a good table is cheaper to build than a new one, and the corrections *are* the lesson. |
| F41 | **What "read-only" does not stop** | The E5 superblock fields (`s_mnt_count`, `s_mtime`, `s_last_mounted`) changing under a plain `-o ro` mount, beside `losetup -r` + `ro,noload,noatime` leaving them untouched, beside `apfs-fuse` labelled *"cannot write at all."* | **🔴 P1** | §2.8 — this is **F3** from room 22, now with a third column, and it addresses four defects at once. |

## 8. Fit against our material

### 🟢 Part 1's Priority 3 holds — but its *value* is inverted from what the label implies.

**The room's errors are worth more to us than its content.** Its concept coverage duplicates `S1`
and `S2`; **its MD5/SHA-1 recommendation is a live example of the exact mistake `S1-06` exists to
prevent**, in a room with 13,306 completions and **305 recommends — the most-recommended room in this
extraction.** 🔴 **That is the point worth making to students: popularity is not currency.**

### Rows this strengthens

- **`S1-06`** — 🟢🟢 **the room is the worked counter-example.** *"A widely recommended, highly rated
  2025 room tells you to verify evidence integrity with MD5 and SHA-1"* — then NIST and CERT/CC.
  **Better than any abstract argument.**
- **`S1-07`** (chain of custody) — §2.6's four guidelines, and 🔴 **the `evidence/` protection gap
  §2.5 exposes**: we gitignore it and have never said how it is protected at rest or who may access
  it.
- **`S2-04`** — the corrected eight-axis table (**F40**), the VM-snapshot case, and **tool/format
  compatibility as a row**.
- **`S2-01`** — the order-of-volatility list, including **physical configuration/topology** and
  **archival media**, which our version omits and which no tool produces.
- **`S4-11`/`S2-10`** — **F41**, and hash-before-and-after-mount as the ritual's demonstration.

### Back-propagation

🟢 **None.** ✅ No ATT&CK IDs cited. ✅ The MD5/SHA-1 finding **confirms** block **K7** rather than
correcting anything; ✅ the mount finding **confirms E5**; ✅ Autopsy/format findings **confirm E4,
O1, P4**.

### Minutes

**Net zero.** Content into `S1-06`, `S1-07`, `S2-01`, `S2-04`, `S4-11`. **No new rows. Nothing lands
in S5.**

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-sixth room carrying the S5 overdraft.**

### Out of scope

Chip-off and JTAG (§2.4) — 🟢 **worth one sentence naming them as the boundary of the course**.
EnCase, FTK and Magnet AXIOM as products; legal procedure by jurisdiction (already excluded).

### Still unresolved

Unchanged, plus one addition: 🆕 **how `evidence/` is protected at rest and who may access it**
(§2.5) — an `S1-07` gap this room exposed.

## 9. Links

**Room** — <https://tryhackme.com/room/introtocoldsystemforensics>
**Module siblings named in Task 6** — Forensic Imaging · Autopsy · DiskFiltration · ExfilNode
(notes: `forensic-imaging.md`, `autopsy.md`, `diskfiltration.md`, `exfilnode.md`)
**Companion notes** — `forensic-imaging.md` and `autopsy.md` (**E4**–**E6**) ·
`memory-analysis-introduction.md` (room 30, the memory counterpart) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **A5**, **A6**, **E4**, **E5**, **E6**, **K7**, **O1**, **P4**,
and new block **R**.

**Citations from §3:**

- #1 — CERT/CC VU#836068 <https://www.kb.cert.org/vuls/id/836068> ·
  NIST retires SHA-1
  <https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm>
- #2, #3 — ⚠️ **NOT VERIFIED**, flagged rather than cited
- #4, #5 — blocks **A5**, **A6**, **E4**, **E5**, **E6**, **O1**, **P4**
