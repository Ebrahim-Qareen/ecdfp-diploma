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

### `S2-01` — Live response, and the order of volatility · 30 min · 🔴 this session OWNS volatility

**Do not re-teach the ladder as theory.** Session 1 no longer covers it (`D58`). Define it once, here,
at the moment the decision is actually made, then apply it for the rest of the session.

**Open with the paradox:** to preserve a running machine you must touch it, and every command changes
it. There is no clean option — only a **recorded** one.

**Then the race.** Registers/cache → RAM → network state → processes → disk → central logs → archival.
The point to land: *while you collect RAM, network state is decaying; while you image the disk, both
are already gone.* Order is a decision about what you accept losing.

🔴 **Name the tool. The first build of this session did not, and it was the defect the instructor
caught.** It is **BriMor Labs Live Response Collection** — `Windows_Live_Response.bat`, run as
administrator **from external media**, menu **Triage / Memory Dump / Complete** plus the `Secure-`
variants (`[U2 p116–125]`).

**Then the output tree**, and the point that makes it defensible: `Processing_Details.txt` and the
per-file hash list are a record of **your own conduct**, not the host's state. ISO/IEC 27037 wants a
third party able to reconstruct what you did; on a live host that needs a contemporaneous record.

🟢 **Say the Velociraptor sentence out of the licence discussion, not into it:** Apache 2.0, builds a
standalone offline collector, and **may be used on a paid engagement — where KAPE may not.**

**And the limit:** a collector asks the OS what is running. A subverted OS answers with the attacker's
list. A clean report is evidence of *what the host said about itself*. That is the reason memory is
captured too, and it plants `S6-10`.

**Micro-lab 1 · 8 min.** Run it on their own VM, output to external media.
**Check:** the tree exists and the hash list has one row per collected file.

---

### `S2-02` — Memory acquisition · 20 min

Free tools: **WinPmem**, **DumpIt**, or FTK Imager's `File > Capture Memory`.

🔴 **The one idea: a capture is a smear, not a snapshot.** The read takes minutes and the machine keeps
running, so the top and bottom of the dump are from different moments.

| Unreliable | Unaffected |
|---|---|
| two structures being consistent **with each other** at one instant | an artifact you find — it was really there |
| counts that must add up | strings, injected code, connections recovered intact |

**The sentence they should write:** *the capture ran 14:12–14:19 UTC; findings describe that window.*

**Blockers, and what is actually seen:** driver signing (driver refuses to load) · Secure Boot (blocked
below the OS) · a hypervisor (guest sees only its own memory) · anti-cheat/EDR (blocked, or bugcheck).
⚠️ **A failed capture is a finding** — tool, version, exact error, time.

**Micro-lab 2 · 8 min.** Capture their own RAM; record start **and** finish.
**Check:** dump ≈ assigned RAM. Much smaller means it did not finish — catch it **before** power-down.

---

### `S2-03` — Acquisition scope and image formats · 25 min

Two blocks merged under `D58`; they were 35 minutes and overlapped heavily.

**Physical vs logical**, drawn as two envelopes over one disk. 🔴 **Tie it forward by name:** Session 4
recovers deleted staging files from **unallocated space**. A logical image today makes that session
impossible. **The acquisition decision caps every later session.**

**The four methods** — disk-to-image (default) · clone · sparse · logical — each named with what it
forfeits.

**Then the three containers.** raw = bytes and nothing else. E01 = per-chunk CRC, embedded hash, case
metadata. AD1 = selected files, ⚠️ **and Autopsy cannot open it**. 🔴 **The catch that sets up the next
block:** E01's embedded hash verifies the image **against itself**; it never re-reads the source.

**Micro-labs 3 and 4 · 9 min.** Image the scratch volume physically then logically (sizes differ, and
they can say why); then as E01 and raw (`ewfverify` SUCCESS; the raw has no embedded hash at all).

---

### `S2-04` — FTK Imager, and what `verified` covers · 20 min · ★ the `D7` block

**Version:** FTK Imager **8.3**, free edition. 🔴 Not *FTK Imager Pro*, which is paid.

**Demo, narrated:** record the write blocker **before** connecting the source → `Create Disk Image` →
read the size and model against the exhibit record → destination E01, fields filled → 🔴 tick
**Verify images after they are created** → start.

**Then read the log aloud and ask what was actually checked:**

| The tool did | The tool did not |
|---|---|
| hash the data as it wrote | re-read the source drive |
| read the image back and hash again | prove the image matches the original **now** |
| prove the two match | prove nothing was altered before you arrived |

**Micro-lab 5 · 8 min.** Image the scratch volume with verification ticked.
**Check:** the `.txt` log shows both digests and `verified`.

---

### `S2-05` — `dc3dd` and targeted triage · 15 min

`dd` produces no hash and no log. `dc3dd` hashes while imaging and writes a log, so the digest is
provably from acquisition time. **The bytes are identical — only the record is better.**

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

**Triage** collects what answers the question instead of the whole disk. **What it forfeits:**
unallocated, slack, deleted files, anything off the target list. *You cannot answer a question about
data you chose not to collect* — so the choice is recorded.

🔴 **KAPE licence, stated in the room** (`D37`): no commercial use since 1 January 2026. Classroom use
is educational and free. Pair every KAPE step with the free path — the EZ Tools underneath are
separately free, and a target set is a list of paths a script can collect. ⚠️ Also correct the common
claim: the core binary is 1.3.0.2 but **KapeFiles ships by commit and is current** — "KAPE is stale"
is wrong.

**Micro-lab 6 · 7 min.** On the **clean Kali snapshot**, never the compromised host.

---

### `S2-06` — File signature vs extension · 20 min · 🔴 new (`D58`)

They met magic bytes in `S1-09`. Now they run it across a whole image — the first question an examiner
asks of a file set is *are these what they claim to be?*

| Type | Signature | Worth saying |
|---|---|---|
| JPEG | `FF D8 FF` | **ends** `FF D9` — Session 3 finds things after that marker |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | the `89` catches a 7-bit transfer |
| ZIP / OOXML | `50 4B 03 04` | ASCII `PK`. A `.docx` **is** a ZIP of XML |
| OLE | `D0 CF 11 E0 A1 B1 1A E1` | legacy `.doc` — a macro lives somewhere different from OOXML |

**Micro-lab 7 · 10 min** on `EVS-05`, which is **verified and ready**. There are exactly **five**
extension mismatches.
🟢 **The best file in the set is `policy_v2.docx`:** a student who learned *".docx is really a ZIP"*
predicts `50 4B 03 04` and is wrong — it is a PNG. It punishes pattern-matching and rewards looking.
🟢 **And the two truncated files** have perfect headers with damaged bodies: a valid signature does not
mean a valid file, which is the bridge back to `S1-06` hashing.

🔴 **The error to catch:** *"the user renamed it to hide it"* — two interpretations stacked on one
observation.

---

### `S2-07` — Case 02a · 35 min · blocked investigation

Individual at the keyboard (`D16`). Hand out the brief, give the decision tree once, then stay quiet
and answer questions with questions. **Q1 is always hash verification.**

**Watch for:** imaging without recording the blocker first; and *"the USB was used to steal data"* as a
finding — the `D7` error, and it costs marks under criterion 4.

---

### `S2-08` — Case 02b · 25 min · blocked investigation

Partition table, types, file systems, and whether the sizes reconcile. Mount **read-only** with
OSFMount 3.3.1000 or Arsenal 3.13.368 — and ask *how they know* it was read-only.

**The buried lesson:** an unallocated gap is a *finding*; what it means is an *interpretation*; and one
question is answerable only as *"this evidence cannot show why"*. That is deliberate.

---

### `S2-09` — The closing ritual · 15 min

Identical in shape to `S1-11`, and it must stay identical.

1. Re-verify hashes against the manifest. 2. Each student completes **one custody line**.
3. Close the session's steps on `docs/session-02/record.html`.

⚠️ The custody-transfer log and the disposition are **case-level** — rendered once, never cleared with
a session. Do not let a student "reset" the page to tidy it.

## 3 · Where students reliably go wrong — the seven

| # | The error | The correction |
|--:|---|---|
| 1 | Reading `verified` as *"the evidence is untampered"* | the tool checked its own output; it never re-read the source |
| 2 | Powering the host down to "preserve" it | that destroys stores 1–4. Preservation on a live host means **capture first** |
| 3 | Writing collector output to the evidence disk | it overwrites unallocated space — the space `S4` needs |
| 4 | Treating a memory dump as an instant snapshot | it is a smear across the capture window; say the window |
| 5 | Choosing logical acquisition because it is faster | it forfeits deleted data and caps every later session |
| 7 | **Believing the extension over the bytes** | when the name and the signature disagree, the signature wins |
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
