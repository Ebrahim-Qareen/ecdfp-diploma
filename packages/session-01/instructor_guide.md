# Session 1 — Instructor Guide

**Forensic Foundations, Evidence Integrity & Chain of Custody**
**Instructor-facing. Not published, not served, never copied into `docs/`.**

---

## 0 · Pre-class checklist

Run this the day before, not the morning of.

| ☐ | Item | How you know it is done |
|:-:|---|---|
| ☐ | `EVS-01` staged and hash-verified on your own machine | `sha256sum -c EVS-01.sha256` → 3 × `OK`, 1 × `FAILED`. **The FAILED is correct — it is the exercise** |
| ☐ | Fallback USB set prepared and re-verified | same command, on the USB |
| ☐ | `FOR-WS01` base VM boots and is at a clean snapshot | snapshot manager shows `CLEAN-BASE`, nothing after it |
| ☐ | Tool installers staged locally | classroom is offline — nothing downloads on the day |
| ☐ | Tool versions re-checked against vendor pages | `design/tools_by_session.md` §2, re-verified on the build date |
| ☐ | Blank chain-of-custody forms printed, one per student + 3 spare | paper. Not a PDF on screen |
| ☐ | `red-stealer` VirusTotal screenshots taken in advance | the demo depends on a third-party service; if it rate-limits mid-class you continue from the screenshots |
| ☐ | Pre-course task confirmed | students report `introdigitalforensics` complete |

**If a student arrives without verified evidence:** hand them the fallback USB and have them
verify it in front of you. That is not a delay — it is the session's first lesson happening early.

---

## 1 · The two sentences the session turns on

Say these in the first five minutes, in these words.

> **1.** *"You already know how to decide whether something is bad. This course is about whether
> you can defend that in front of someone whose job is to break it."*

> **2.** *"This is the most important session in the diploma, and it needs no forensic software at
> all. Everything after it does — and none of it will save you if you skip this."*

Then show the session shape (figure `S1-F12`) so the room knows the rhythm and can see the break
coming.

---

## 2 · Per-block teaching notes

### `S1-01` — What digital forensics is · 15 min

**Teach:** the mandate (recover · preserve · interpret so it survives challenge) · the evidence
life cycle **acquisition → analysis → presentation** · what an investigator may **not** claim.

**The life cycle's point is not the three words. It is that each phase can destroy the next.**
Walk figure `S1-F2` and make them name the failure at each stage. The worked example:
an examiner who double-clicks a file "just to read it" has updated its last-access time —
acquisition failed and analysis inherits a corrupted timestamp.

⚠️ **Say honestly that this specific example has aged:** modern Windows disables last-access
updates by default. The *lesson* holds; the *effect* often does not. This is the students' first
taste of "the courseware is a decade old", and hearing it from you first buys credibility for the
rest of the diploma.

**"What you may not claim"** is the block's real content, and it is the first appearance of `D7`:

| You may write | You may not write |
|---|---|
| the artifact recorded X at time T | the user did X |
| the file was not present in the collected set | the file was never on the machine |
| the process was running at collection time | the process was running at the time of compromise |

**The cross-platform table (figure `S1-F3`)** is the scope statement. Read *down* the Linux column
— no `USBSTOR` at all, login records deleted outright, `.bash_history` undated and silently
suppressed by a leading space, no Autopsy module for any Linux persistence artifact. **That column
is the argument for the Windows-weighted syllabus.** It converts a disclaimer into five minutes of
teaching. (`D38` — Linux and macOS forensics are out of scope, decided, not overlooked.)

**Common misconception:** *"forensics is about finding the bad thing."* It is about establishing
what can and cannot be shown. Absence is a finding — the Corcoran Group case turned on emails that
should have existed and did not.

---

### `S1-02` — Forensic principles · 20 min

**Teach:** minimal footprint · repeatable vs reproducible · always work on a
copy.

⚠️ **Order of volatility is no longer taught here** (`D58`). `S2-01` owns it and teaches it
operationally, at the moment the collection decision is actually made. Do not re-explain it —
one clause in passing is enough if a student raises it.


**Then invert it.** The rule has a reason, not a chant: if a wiper is actively running, pulling
power is correct and the RAM is lost on purpose. Ask the room which rule wins, and why. A student
who can only recite "RAM first" has not learned the block.

**Repeatable vs reproducible** — INE requires both, and the distinction is examinable:

| | Meaning |
|---|---|
| **Repeatable** | same lab, same tools, same result |
| **Reproducible** | **different** lab or tools, same result |

This is why *"I used the GUI and clicked around"* is not a method. Say that sentence out loud.

**Common misconception, and it is the big one for this block:** students reach for the disk first
under pressure, because the disk *feels* like the real evidence. Drill RAM-first until it is
reflex — then run the counter-case above so the reflex has a reason behind it.

---

### `S1-03` — What makes evidence defensible · 12 min

**Teach:** INE's three-part test.

| Test | Means | Who owns it |
|---|---|---|
| **Relevant** | proves or disproves a hypothesis in *this* case | the lawyer |
| **Reliable** | authentic (chain of custody) + objective (a fact, not an opinion) | 🔴 **you** own authenticity |
| **Competent** | obtained legally, no protected confidentiality breached | the lawyer |

**The example that lands:** a video that convicts the suspect is thrown out because the warrant
covered text files only. Perfect forensics, inadmissible evidence. Ask the room whose failure that
is — the answer is *nobody's forensics*, and that is the point of separating the three tests.

**Of the three, only authenticity is the examiner's.** Everything else is somebody else's problem,
and pretending otherwise is how analysts end up giving legal opinions they are not qualified to
give.

**No figure here.** A three-column table states the test more compactly than any diagram, and a
diagram that only re-labels the bullets beside it has failed.

---

### `S1-04` — The report template · 25 min · 🔴 **the point of the diploma**

`D7` makes findings-versus-interpretation the thing this course exists to teach. `D20` grades it
as criterion 4 of a rubric that never changes across all six sessions. **If this block is thin,
the session has failed regardless of how good the rest was.**

#### The three-way split (figure `S1-F1`)

Not two categories. Three:

| | Border | Contains | Test |
|---|---|---|---|
| **FINDING** | **solid** | only what the artifact literally says, artifact named, exact path given | if it needs the word *because*, it is not a finding |
| **INTERPRETATION** | **dashed** | the reasoning, citing the finding numbers it rests on | must name an alternative it considered |
| **CANNOT PROVE** | **dotted** | what this evidence cannot show, however it is read | every investigation has at least one |

**The border style is the lesson, not decoration.** A solid line is something you observed; a
dashed line is something you reasoned to. A student who cannot tell blue from violet still reads
the page correctly, and the metaphor does the teaching.

#### Work this triple live, on the board

Take it from `Module_01` §4 and write all three lines yourself before anyone speaks:

> **FINDING** — the FTK Imager log for `EVI-SRC01.E01` reads `MD5 checksum: <value> : verified`
> and `SHA1 checksum: <value> : verified`, with acquisition start and finish timestamps.
>
> **INTERPRETATION** — the image was written and read back without corruption, so the file on the
> destination drive is very probably a faithful copy of whatever the tool read from the source.
>
> **CANNOT PROVE** — that the **source** is unaltered. The tool hashed its own read and its own
> write-back; **it never re-read the drive.** It cannot show a write blocker was in the path, that
> the device selected was the one on the custody form, or that the read covered the whole physical
> medium — an HPA excluded from the read is excluded from both hashes, and they match perfectly.

**Then ask the room to mark which lines of that log describe the source.** The answer is *almost
none of them*. This is the single most productive five minutes in the session.

#### The two line formats they must write from memory

> **F-07** — `System.evtx` on `WKSTN-07`, record 41 992, Event ID 7045,
> `2026-03-03 09:12:55 UTC`: a service named `WinDefendUpd` was installed with image path
> `C:\Users\<user>\AppData\Local\Temp\svchost.exe` and start type *auto start*.

> **I-03** — The service in **F-07** is assessed, with high confidence, to be attacker
> persistence: its name imitates a Microsoft component, its binary sits in a user-writable temp
> directory, and it was installed 41 seconds after the document execution in **F-05**.
> Considered and not excluded: a legitimate third-party installer using a misleading name — no
> corresponding installer entry was found in `Application.evtx`, but the log covers only 6 days
> (**F-02**).

**Point at what makes `I-03` acceptable:** it cites finding numbers, it states a confidence, and
it names an alternative it could not exclude. An interpretation with none of those is an opinion.

#### Banned in Findings

*clearly · obviously · we are sure · we are certain · proves that · the attacker · malicious ·
unauthorised.* Every one is an interpretation wearing a finding's clothes.

**Banned everywhere:** two date formats in one report · two terms for one thing · sentences of
25–30 words · jargon with no glossary entry · **any sentence assigning guilt.**

> **The hard rule:** *you are not the judge.* Never write "in my opinion Mr X committed this
> crime." Present method and evidence. The decision is not yours.

#### The guided task (8 min of the 25)

Hand out three contaminated findings and have each student rewrite them — one clean finding, one
interpretation, one limitation. They are in `student_activity.md` §1. Take answers from two
students, not the whole room; the block is tight.

**Common misconception:** *"limitations make the report look weak."* The opposite — criterion 4
awards marks for exactly this, and a report with no stated limitation is a report nobody senior
believes.

---

### `S1-05` — Toolkit install and the `CLEAN-TOOLS` snapshot · 20 min

`D17`: `FOR-WS01` ships pre-built and clean. Students install the tool set and snapshot. The
snapshot **is** the lesson — a known-good baseline you can always return to.

**Cover the licence findings while installs run** (`D48` — check the version you ship **and** the
one ahead):

| Finding | Say it as a finding, not a recommendation |
|---|---|
| RegRipper **4.0** bars *"vendor training"* and *"any distribution"* | we are paid training, so we stay on 3.0 and record why. New plugins and the ATT&CK mappings are in 4.0 — **a capability we decline on licence grounds** |
| 010 Editor is 30-day evaluation, no free tier | HxD does everything this course needs and is free for commercial use |
| Xiao Steganography has no living vendor | every copy is a third-party mirror from 2010 or earlier. We do not ask students to run unsigned executables from download mirrors |

**End the block by starting the snapshot, then break.** Name it `CLEAN-TOOLS` exactly — later
sessions refer to it by that name.

---

### `S1-06` — Cryptographic hashing · 18 min

They know what a hash is. **They do not know what it proves.** Teach only the gap.

#### Demo A — the avalanche · 4 min

Type this, do not paste it:

```powershell
"Evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

Expected: a 64-hex-character digest and the path.

```powershell
"evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

One capital letter changed. Expected: **a completely unrecognisable digest.**

> **Regenerate these live. Never transcribe a digest from a slide or from the courseware** — every
> digest in the INE source is OCR-truncated and every digest in the instructor deck resolves
> differently on each of the three slides it appears on.

**Then the sentence that is the whole block:**

> *"The two digests differ. That tells you the file changed. It does not tell you who changed it,
> when, or whether the original was ever genuine."*

#### Demo B — hash as a lookup key · 5 min

Put **CyberDefenders `red-stealer`** on screen. The entire lab is *"investigate this executable by
analyzing its hash"* — hash → VirusTotal → C2 infrastructure → ATT&CK. Run two questions, no more.

Then ask: **"we just identified a file by its hash. Does that mean the file is unaltered?"**

That is the distinction, demonstrated instead of asserted:

| Question | Answer with | Why |
|---|---|---|
| *"Have we seen this exact file before?"* | MD5 acceptable | **preimage** resistance holds — this is why NIST's own NSRL ships MD5 and SHA-1 hash sets to eliminate known files |
| *"Is this file unaltered?"* | 🔴 **SHA-2 / SHA-3 only** | **collision** resistance is broken for MD5 (CERT/CC VU#836068) and SHA-1 (NIST retired it) |

**The teaching card:** the same agency publishes MD5 hash sets for forensics *and* excludes MD5
from approved cryptography — because they are different problems.

**Course standard: record MD5 and SHA-256 for every artifact. SHA-256 is what you defend; MD5 is a
secondary lookup key.** A chain of custody signed against an MD5 is a chain whose integrity claim
can be forged.

⚠️ Do not assign `red-stealer` as a task without this framing attached.

#### Demo C — a published course getting it wrong · 3 min

Put the TryHackMe room **`introtocoldsystemforensics`** on screen and read its own sentence:

> *"Hashing: Using cryptographic hash functions such as MD5 and SHA-1 to create unique data
> fingerprints and verify that it has not been altered."*

**Have the room find the error before you say it.** Then put CERT/CC VU#836068 and NIST's SHA-1
retirement beside it.

**Why this is worth three minutes:** it is a 2025 room, free, with **305 recommends — the
most-recommended room in the whole catalogue** — giving advice that has been wrong since before
these students were in secondary school. **Popularity is not currency.** No abstract argument
makes that point as well.

🔴 **Never assign this room as a task.** A student working alone absorbs the MD5 advice and
nothing contradicts it. It is safe only with the correction attached.

*(The same room also claims Guymager "provides built-in write-blocking functionality" — refuted by
Guymager's own documentation. Keep that in reserve for `S1-08` if the room is sharp.)*

#### What a hash does **not** prove — the four you must state

1. **Not authenticity, not provenance.** It says the copy equals the source *as read at that
   moment*. It says nothing about where the source came from or whether it was already altered.
2. **Not completeness.** An HPA excluded from the read is excluded from both hashes. They match
   perfectly.
3. **A mismatch is not proof of tampering.** A failing sector, a cable fault, or an SSD's own
   garbage collection between two reads all produce mismatches with no misconduct at all.
4. **Not protection, if stored together.** An attacker holding both the disk and the hash simply
   recomputes. The hash must be stored **securely and separately.**

⚠️ **INE contradicts itself on this, one slide apart** — first that hashes "prove the file has not
been tampered with", then that an attacker with both recomputes. **The second is correct.** Use
both slides together: it is the module's own worked example of a finding stated as an
interpretation, which is the thing you are grading.

---

### `S1-07` — Chain of custody · 12 min

They met the *concept* in eCIR S5. **The discipline is new.** Teach the document.

**Minimum fields:** what the evidence is · how acquired · when · by whom · where stored · and
**every subsequent action**.

**Physical controls belong with it** — this is where `evidence-bag-sealed.jpg` goes on screen:
antistatic bag, padding, sealed container, **tape signed and written across the seal** so a
re-opening is visible, controlled temperature and humidity. Point at the completed label, the
unique bag number and the tamper strip. **It is a document and a physical control, not a tool
output. No software produces it. That is the lesson.**

**Fill one in on the board for a single exhibit, then have a student play defence counsel against
it.** Give the student one instruction: *find a gap and argue substitution.* Figure `S1-F9` has a
deliberately broken hop — if the room does not find it, point at it.

**The asymmetry they must remember:** an unbroken chain does not by itself win admissibility; a
single unexplained gap is enough to lose it, because the other side only has to raise the
*possibility* of substitution.

**What it does not prove:** that the **data** is genuine. The attacker's wiper ran before you
arrived and the custody record is still perfect.

**The commonest real failure is not malice** — it is a junior examiner who does not label two
identical drives from the same office. After that, no form on earth can say which desk each came
from.

---

### `S1-08` — Write blocking, and how to prove one was used · 8 min

🔴 **This is the course's largest documented gap.** The source material explains thoroughly what a
blocker is and why it matters, then **never addresses the evidential question.** Build the proof
trail explicitly — it cannot be recovered after the fact.

**Put `write-blocker-inline.jpg` on screen.** The point of the photograph is that it is a
**physical box in the path**, and that a photograph of the connected rig is itself part of the
proof. Then `write-blocker-ports.jpg` for the port side.

**The sentence that motivates the whole block:**

> *"An image taken on a write blocker and an image taken without one are byte-identical. Nothing
> in the image records that you used one. So how do you prove it?"*

**The proof trail — four parts, and they must name all four:**

| # | Part | Why it counts |
|--:|---|---|
| 1 | 🔴 **Source hash before and after the imaging run** | **the actual technical proof** — two matching source hashes across the run |
| 2 | The blocker's own display or log | the device attesting to its own state |
| 3 | A photograph of the connected rig, serials legible | taken **before** disconnecting |
| 4 | The custody line naming blocker make, model, serial and firmware | contemporaneous, not reconstructed |

**And the honest limit** — this is the `CANNOT PROVE` for the block:

> Two identical source hashes are **consistent with** a blocker, with a correctly-set software
> policy, and with sheer luck on a system that happened not to touch the volume. They do not prove
> a blocker was used. The blocker is proven by the photograph, the serial on the form and your
> contemporaneous notes.

**Software fallback, and the classic false positive.** `HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies`
→ `REG_DWORD` `WriteProtect` = `1`. It sits in the **examiner's** registry, not the evidence's, so
it proves something about the analysis workstation and **nothing about how any exhibit was
handled**. It is not per-device and not timestamped.

> **The classic failure:** set the value, do not reboot, plug the evidence in, report "software
> write blocked". Windows writes to it happily. **Always demonstrate the block on a scratch stick
> before touching evidence. Never assume it.**

*(The full demo — set it, fail to reboot, write successfully, reboot, fail — is S2's, where there
is time for it. Describe it here in one sentence.)*

---

### `S1-09` — Inside a file: hex and magic bytes · 22 min · 🔴 new (`D58`)

**The move:** they have just proved a hash detects one changed byte. So ask the obvious next question —
*what are the bytes?* This is the first time they open a file and look at what it actually is.

**The one idea:** a file is bytes; the name is a label stored **beside** it, in a directory entry.
Renaming rewrites the label and touches nothing in the file.

| Type | Signature | Worth saying |
|---|---|---|
| JPEG | `FF D8 FF` | also **ends** `FF D9` — Session 3 finds things after that marker |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | the `89` is set so a 7-bit transfer corrupts it visibly |
| ZIP / DOCX | `50 4B 03 04` | ASCII `PK`. A `.docx` **is** a ZIP of XML — rename one and it opens |
| PDF | `25 50 44 46` | literally `%PDF` |

**Micro-lab · 10 min.** They open the four supplied files in HxD and write down the first four bytes
of each. One file's bytes disagree with its extension.
**Check:** every file has its four bytes recorded and a type named.
**Why:** *the bytes say what a file is. They never say who named it, or why.*

🔴 **The error to catch:** a student writing *&ldquo;the user renamed it to hide it&rdquo;*. That is two
interpretations stacked on one observation, and it is the same `D7` failure the report template exists
to prevent. Feeds `S2-06` directly, where they run this across a whole image.

---

### `S1-10` — Case 01 · 60 min · blocked investigation

Students work **alone at the keyboard** (`D16`). You unblock, you do not lead.

The brief, the manifest and the six questions are in `student_activity.md`. **Q1 is always hash
verification** — that rule holds for every case in the diploma.

**What right looks like:** a student who finds the mismatch in ten minutes and spends fifty
writing it up correctly has done better than one who finds it in three and writes
*"the acquisition log was tampered with."*

**The trap the case is built around.** The tampered file is
`EVI-SRC01_acquisition_log.txt` — the file whose *content is the integrity claim*. Expect at least
one student to write:

> ❌ *"The acquisition log was modified to hide the real acquisition time."*

That is an interpretation, stated as a finding, with a motive attached that no artifact supports.
The correct finding is:

> ✅ *"`EVI-SRC01_acquisition_log.txt` computes to SHA-256 `<value>`, which does not match the
> value `<value>` recorded for that filename in `EVS-01.sha256`. The other three files match."*

…and the interpretation, separately, names at least one alternative — transfer corruption, a
failed download, an editor that rewrote line endings — and says which it could not exclude.

**At least one question has the correct answer *"this artifact cannot prove that."*** If a student
answers it with a guess, that is the teaching moment of the session.

---

### `S1-11` — The closing ritual · 15 min

Every session ends this way, all six. It is not a formality; it is the habit the exam tests.

1. **Re-hash** every evidence file against the manifest. State the result out loud.
2. **Write one custody line** each: who · what · when · from where · hash · where stored.
3. **Sign it.** Paper, one line, every student, every session.
4. **Close with the bridge:** *"Everything you did today was preparation. Nothing has been
   acquired yet. That is Session 2."*

---

## 3 · Where students reliably go wrong — the seven

Reference list. Each has a countermeasure above.

| # | The error | Where it bites |
|--:|---|---|
| 1 | **"The hash proves the evidence is genuine."** They fuse integrity with authenticity every time | `S1-06` |
| 2 | **"Verified means verified against the disk."** It means the tool checked its own output | `S1-04` · `S1-06` |
| 3 | **"We didn't find it, so it isn't there."** The permitted sentence is *"not present in the collected set"* | `S1-01` · `S1-09` |
| 4 | **"Live response tells you what's on the machine."** It tells you what the machine *says* is on it | `S1-01` |
| 5 | **Believing the extension over the bytes** — they read `.pdf` and stop looking | `S1-09` |
| 6 | **Working on the first image.** Stated twice in the source and they still do it | `S1-02` |
| 7 | **Motive smuggled into a finding.** "to hide", "to avoid", "deliberately" | `S1-04` · `S1-09` |

---

## 4 · If you are running short

Cut in this order. Never cut `S1-04`.

| Cut | Recover | Cost |
|---|--:|---|
| Demo B (`red-stealer`) → describe instead of showing | 4 min | low — the distinction survives in `S1-F8` |
| `S1-03`'s defence-counsel exchange | 3 min | low |
| Demo C (the wrong room) → state it, do not screen it | 2 min | **medium — this is the best argument in the block** |
| `S1-05` licence discussion → move to the student guide | 4 min | medium |

**Never cut:** the three-way split, the live triple on the board, the proof trail, or the ritual.

---

## 5 · Bridge to Session 2

> *"You have a seized host, verified evidence and an open custody record. You have not acquired
> anything. Next session we take the image — live response first, then memory, then the disk —
> and every one of today's rules gets tested by a tool that will happily let you break them."*

S2 opens on order of volatility **in practice**, and the first thing it does is re-verify
`EVS-01`. The ritual is not decoration; it is the start of the next session.
