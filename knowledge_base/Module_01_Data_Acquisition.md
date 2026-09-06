# Module 01 — Foundations and Data Acquisition

| | |
|---|---|
| **INE source** | unit 1 — *Introduction to Digital Forensics* (193 pp) · unit 2 — *Data Acquisition* (185 pp) |
| **Feeds sessions** | `S1` · `S2` |
| **Source text** | [`_source_text/INE_Unit_01_Introduction_to_Digital_Forensics.md`](_source_text/INE_Unit_01_Introduction_to_Digital_Forensics.md) · [`_source_text/INE_Unit_02_Data_Acquisition.md`](_source_text/INE_Unit_02_Data_Acquisition.md) |
| **Instructor delivery** | [`instructor/Session_01_Introduction_and_Acquisition.md`](instructor/Session_01_Introduction_and_Acquisition.md) |

> Condensed reference, our words, from INE's eCDFP courseware. Not published.
> Page cites `[U2 p91–115]` point into the source-text files, which are OCR — check any exact
> string on the source page before putting it in front of students.

## 0 · What this module is for

After this module a student can take an unknown machine off a desk and turn it into evidence
that survives challenge: decide what to collect first and why, capture volatile state before
killing it, image a disk without touching it, prove the image equals the source, and hand it
over on a chain-of-custody form a hostile lawyer cannot pull apart. Before this module they
can copy files; after it they can acquire. It sits at the front of the S1–S6 arc because
everything downstream depends on it — S3–S5 parse the image and S6 reports on it, but no
amount of Registry parsing in S4 rescues an unsound acquisition in S2. It also plants the two
ideas the whole diploma is graded on: **findings are not interpretations**, and **a tool
showing you something is not the same as that something being true**.

## 1 · Core concepts

### Digital forensics
- **Definition** — the forensic-science discipline of recovering, preserving and interpreting artifacts from digital devices so the result survives challenge as evidence.
- **Why it exists** — people leave traces they never meant to leave, and deleting a file does not delete the data; without a discipline for recovering those traces, digital activity is unprovable either way.
- **Where it shows up** — always in service of the five W's of an incident: who, what, when, where, why (and how).
- **Example** — INE's framing covers digital crime (phishing, skimming, intrusion) *and* ordinary crime: proving intent from browsing history, or breaking an alibi from network logs showing the suspect's laptop was never on that Wi-Fi.
- **In the case (D19)** — the whole incident is reconstructed from artifacts nobody created deliberately: a document's metadata, a persistence key, a beacon in RAM, a USB serial in the Registry.
`[U1 p12–22]`

### Digital evidence and its life cycle
- **Definition** — digital evidence is any information stored, transmitted or produced by an electronic device or its software; its life cycle is **acquisition → analysis → presentation**.
- **Why it exists** — the phases are ordered by risk, because each can destroy the evidence for the ones after it. INE requires the order regardless of evidence or case type.
- **Where it shows up** — acquisition is scene work plus imaging (S1–S2), analysis is S3–S5, presentation is the report and the courtroom (S6).
- **Example** — an examiner who double-clicks a file "just to read it" has already updated its last-access time: acquisition failed and analysis inherits a corrupted timestamp.
- **In the case (D19)** — the diploma is one pass through this cycle on EVI-SRC01 and the exfil USB.
`[U1 p38–61]`

### Volatility and the order of volatility
- **Definition** — volatility is how likely a data set is to change or vanish; the **order of volatility** says collect from the most volatile store first.
- **Why it exists** — collection takes time, and every minute on the disk is a minute RAM is being overwritten; ordering by fragility maximises what survives.
- **Where it shows up** — INE's ladder runs **CPU registers** (change almost per instruction) down to **external/secondary storage** (survives power loss). ⚠ The intermediate rungs did not survive OCR `[U2 p14]`; teach the full ladder — registers/cache → RAM (processes, connections, sessions, clipboard) → temporary and paging areas → disk → removable and archival media. See §7 G1.
- **Example** — a reboot erases RAM entirely and leaves the disk intact; that single comparison is INE's whole justification.
- **In the case (D19)** — the workstation is found running with the beacon live, so live response and the RAM capture come first; the disk will still be there in an hour, the decrypted C2 config will not.
`[U1 p78–80]` `[U2 p11–15]`

### Static, dynamic, dead and live acquisition
- **Definition** — **static** collects non-volatile data; **dynamic/live** collects volatile data from a running machine; **dead** reads the media *without* the suspect OS's help, via hardware or a foreign OS.
- **Why it exists** — they answer different threats. Static is the default; dynamic exists because RAM-only evidence has nowhere else to be; dead exists because a compromised OS is a lying witness.
- **Where it shows up** — static on disks and flash, dynamic through a live-response collector, dead through a hardware write blocker or a bootable forensic disc.
- **Example** — a rootkit hooks the kernel so a directory listing omits its own files; imaging *through* that OS reproduces the lie, imaging the drive on a write-blocked dock does not.
- **In the case (D19)** — live response while the workstation is up, then power down and image the disk dead on a hardware blocker.
`[U2 p16–21]`

### Imaging vs copying; physical vs logical
- **Definition** — an **image** mirrors every sector, allocated and unallocated; a **copy** takes only the "useful" allocated data. **Physical** takes the whole device, **logical** one partition or volume.
- **Why it exists** — everything forensically interesting about deletion lives in the space a copy throws away: slack, unallocated clusters, deleted content, stale file-system metadata.
- **Where it shows up** — INE's illustration: a disk 60 % used and 40 % "rubbish"; imaging takes 100 %, copying takes the 60 %.
- **Example** — copy a disk and the deleted exfil archive is gone; image it and the archive is recoverable from unallocated space.
- **In the case (D19)** — the staged-then-deleted archive is only recoverable because EVI-SRC01 is a physical image.
`[U2 p36–37]` `[U2 p41–44]`

### Forensic soundness, minimal footprint and repeatability
- **Definition** — a process is *forensically sound* when it preserves the evidence's meaning and can be shown to have done so: never work on the original, touch as little as possible, produce results anyone can reproduce.
- **Why it exists** — you get one shot at the original. INE quotes "to get to the evidence, we might destroy the evidence" and means it literally.
- **Where it shows up** — INE notes the term is used loosely across the industry to justify whatever a vendor is selling, and points at McKemmish's four criteria as an actual definition `[U1 p157–158]`.
- **Example** — **repeatable** = same lab, same tools, same result; **reproducible** = different lab or tools, same result. INE requires both `[U1 p118]`, which is why "I used the GUI and clicked around" is not a method.
- **In the case (D19)** — every acquisition step logs tool, version, operator and timestamp so a defence examiner can rerun it against the same hashes.
`[U1 p54–55]` `[U1 p100]` `[U1 p116–118]` `[U1 p157–160]` `[U2 p10]` `[U2 p45]`

### Admissibility — relevant, reliable, competent
- **Definition** — INE's three-part test. **Relevant**: proves or disproves a hypothesis in *this* case. **Reliable**: authentic and objective. **Competent**: obtained legally, without breaching protected confidentiality.
- **Why it exists** — it separates the legal question (can this be heard?) from the technical one; of the three, INE says the examiner owns **authenticity** and the rest is largely the lawyer's problem `[U1 p167]`.
- **Where it shows up** — authenticity is proven by the chain of custody, from first collector to the person testifying; objectivity means a provable fact, not an opinion.
- **Example** — a video that convicts the suspect is thrown out because the warrant covered text files only `[U1 p189]`: perfect forensics, inadmissible evidence.
- **In the case (D19)** — the exfil USB is relevant and authentic, and competent only if the engagement letter covers employee-owned removable media.
`[U1 p136]` `[U1 p161–168]` `[U1 p188–189]`

### Cryptographic hashing
- **Definition** — a one-way function taking variable-length input and producing a fixed-length digest that fingerprints it; any change, however small, changes the digest completely.
- **Why it exists** — it is the only cheap way to show two multi-terabyte objects are identical, and the only way to show later that an image is the one you acquired.
- **Where it shows up** — hash source and image and compare; hash again before every analysis session. INE demonstrates `sha512sum` on Linux and HashCalc on Windows.
- **Example** — INE changes one letter of `hashtest.txt` from `H` to `h` and the digest is unrecognisable `[U2 p146–150]`. ⚠ Both digests are truncated in the OCR — regenerate live, never quote them.
- **In the case (D19)** — MD5 and SHA-256 taken on the source USB before imaging, on the image after, re-verified at the start of S3.
`[U2 p141–157]`

### Chain of custody (CoC)
- **Definition** — the unbroken, contemporaneous record of who held an exhibit, when, and what they did to it, from seizure to case close.
- **Why it exists** — it is how authenticity is actually proven in court; a gap is not a paperwork problem, it is the moment the other side argues substitution or alteration.
- **Where it shows up** — INE's minimum fields: what the evidence is, how acquired, when, by whom, where stored, and every subsequent action `[U1 p169–170]`. Physical controls belong with it — antistatic bags, padding, sealed containers, **signed tape written across the seal**, controlled temperature and humidity `[U1 p49–51]`.
- **Example** — an examiner who does not label two identical drives from the same office can never say which came from which desk; INE files this under commingling as much as CoC `[U1 p156]`.
- **In the case (D19)** — three exhibits (workstation disk, memory capture, exfil USB), three forms, one storage location, one signature per transfer.
`[U1 p49–52]` `[U1 p137]` `[U1 p164]` `[U1 p169–170]` `[U2 p38]`

### Write blocking
- **Definition** — hardware or software that lets you read a disk while filtering every write command out before it reaches the media.
- **Why it exists** — attaching a disk to a running Windows box *is* a write: Windows touches the volume, updates journal state, and can mount and modify unasked.
- **Where it shows up** — hardware: an inline dock (INE names WiebeTech Forensic UltraDock from CRU and Tableau Forensic Imager TD3). Software: a forensic boot disc, or Windows' `StorageDevicePolicies\WriteProtect` for USB.
- **Example** — INE is blunt that a hardware blocker may simply be unavailable (cost, or jurisdictions that restrict them) and that software is the fallback, not the equal `[U1 p110]` `[U2 p85]`.
- **In the case (D19)** — the exfil USB is imaged through a hardware blocker, and the blocker's log plus a photograph of the rig go in the case file, because "I used a write blocker" is a claim, not a proof.
`[U1 p107]` `[U1 p110]` `[U2 p78–90]`

### Abstraction layer
- **Definition** — every tool sits between you and the bits, applying a rule set that turns raw storage into something readable; what you see is the tool's *representation*, never the data.
- **Why it exists** — humans cannot read bits, but the translation is where bugs, wrong rule sets and misreadings enter. INE states each layer adds a margin of error or distortion `[U1 p180]`.
- **Where it shows up** — a packet analyser turning bits into protocol fields; Notepad applying ASCII; a browser applying HTML on top; a file-system parser turning sectors into a directory tree.
- **Example** — search by extension and you miss the JPEG renamed `.mp9`; you must drop a layer and search by file signature `[U1 p183–187]`. INE's mitigation: two independent tools, or examine both sides of the layer.
- **In the case (D19)** — this is the module's spine and the reason §4 exists: everything a student "finds" in S3–S5 is a tool's assertion until corroborated.
`[U1 p171–187]`

### Commingling / contamination
- **Definition** — mixing evidence from different sources, or from a previous case, so the origin of a byte can no longer be established.
- **Why it exists** — same reason a chemist uses a clean vessel: writing a new image onto a drive holding a previous case's deleted data means the old data can be recovered and mistaken for the new.
- **Where it shows up** — the destination drive. INE requires a new drive, or a verified **forensic wipe** before every acquisition `[U1 p100]` `[U1 p154–155]`.
- **Example** — carve for JPEGs on a re-used destination and you recover images that were never on the suspect's machine.
- **In the case (D19)** — the destination disk for EVI-SRC01 is wiped, the wipe verified, and the wipe log filed.
`[U1 p153–156]`

### Inculpatory, exculpatory and tampering evidence
- **Definition** — evidence that **supports** the hypothesis, evidence that **contradicts** it, and evidence indicating **deliberate manipulation to deceive**.
- **Why it exists** — it forces you to hold a hypothesis rather than a conclusion; INE's method requires actively considering alternatives and trying to disprove them `[U1 p35]`.
- **Where it shows up** — in analysis, but the categories must be set before you start looking or confirmation bias sets them for you.
- **Example** — the Corcoran Group case turned on *missing* files and emails that should have existed: the absence was the finding `[U1 p111–112]`. Conversely, images found only in temporary internet files supported a defendant's claim and exonerated him `[U1 p77]`.
- **In the case (D19)** — the staged ransomware binary that never ran is exculpatory on "ransomware attack" and inculpatory on "prepared a second stage": same artifact, two readings, which is §4's job.
`[U1 p57]` `[U1 p77]` `[U1 p111–112]`

## 2 · Artifacts  (R10 six-box, one table per artifact)

> "Artifact" in an acquisition module means the objects the acquisition *produces* and the
> objects that prove it was done properly. Each one is something a student will be asked to
> hold up in S6 and say what it shows.

### Raw / `dd` image (`.001`, `.dd`, `.img`, `.raw`)
| | |
|---|---|
| **What it is** | A bit-for-bit sequential dump of every addressable sector of the source, with no container, no header and no metadata. What you read is what was on the media. |
| **Where it lives** | A single file on the destination drive, or a numbered set (`image.001`, `image.002`, …) when split. Its size equals the **total capacity** of the source, not the used capacity `[U2 p107]`. Nothing about the case is stored inside it. |
| **What it proves** | That, at read time, the source's addressable LBA range held exactly these bytes — allocated, unallocated, slack and all. Universally readable, so any tool in any framework can be pointed at it and the outputs compared. |
| **What it does NOT prove** | It carries **no integrity of its own**. A raw file has no embedded hash, no CRC, no acquisition metadata and no tamper evidence — if the sidecar hash file is lost, edited or never written, there is nothing in the image itself that can show it was not modified afterwards. It also does not prove the whole *physical* device was captured: a raw image stops at the end of the LBA range the controller reports, so a Host Protected Area, a Device Configuration Overlay, reallocated sectors or SSD over-provisioned blocks can sit outside it and leave no trace of their absence. And "raw imaging tools neglect small errors on the source disk" `[U2 p25]` — a read error can be silently zero-filled, so a region of zeroes in a raw image does not prove that region was zeroed on the disk. |
| **How to parse it** | `dd if=/dev/sdb of=/mnt/case/EVI-SRC01.dd bs=4M conv=noerror,sync status=progress` — then hash both sides. Mount read-only for exploration: `mount -o ro,loop,offset=<bytes> EVI-SRC01.dd /mnt/case002`. FTK Imager and every analysis suite in the course open raw directly. |
| **Anti-forensics / false positive** | An image of a disk that was already wiped, or whose HPA was set by the attacker, looks like a clean acquisition. Full-disk encryption produces a raw image of high-entropy noise that is technically perfect and analytically useless `[U2 p71]`. |

`[U2 p24–27]` `[U2 p107]`

### E01 / Expert Witness Format (EWF) image
| | |
|---|---|
| **What it is** | A proprietary forensic container (EnCase's format) that holds the source data plus a header of case metadata and **integrity data embedded in the file itself**, usually compressed. |
| **Where it lives** | `case.E01`, `case.E02`, … as a segmented set. Case number, evidence number, examiner, unique description and notes live in the header; per-chunk checksums and the acquisition hash live inside the container. ⚠ INE describes proprietary formats generically — "a header with metadata such as hash value or CRC embedded within" `[U2 p28]` — and never documents E01's internal layout. Do not quote chunk sizes or offsets from this course; see §7 G4. |
| **What it proves** | That the image carries its own verification: the container can be checked against itself without an external hash file, and corruption is localised to the chunk that fails. Compression means it is normally much smaller than the source, so a whole case fits on one destination drive `[U2 p29]`. |
| **What it does NOT prove** | The embedded hash proves the container's **internal consistency**, not the **provenance** of the data — it says the bytes have not changed since the container was written, and says nothing whatever about whether those bytes came from the drive named on the chain-of-custody form, or whether a write blocker was in place while they were read. The metadata header is examiner-typed free text: a case number, examiner name and description inside an E01 are only as true as the person who typed them, and are not evidence of anything. "Verified" on the acquisition log is likewise not a statement about the *source* — it compares the image to a hash the same tool computed during the same read. And a compressed image is **slower** to acquire and to analyse `[U2 p30]`; that cost is real and is why raw still wins on very large media. |
| **How to parse it** | FTK Imager: `File ▸ Add Evidence Item ▸ Image File`. Command line: `ewfverify case.E01` to re-check integrity, `ewfmount`/`ewfexport` (libewf) to expose or convert it. `mmls` / `fls` (TSK) read E01 directly where libewf is linked. |
| **Anti-forensics / false positive** | Older EWF variants were size-limited — INE cites a 2 GB per-segment cap that forces chunking `[U2 p32]` — which is a legacy-image compatibility trap, not a security issue. Proprietary formats also **bind you to the framework**: an image your analysis tool cannot open is evidence you cannot use `[U2 p30]`. |

`[U2 p28–32]`

### AD1 logical image (AccessData custom content)
| | |
|---|---|
| **What it is** | AccessData's *logical* evidence container: selected files and folders plus their file-system metadata, packaged with a header, rather than a sector-level image of a device. |
| **Where it lives** | `collection.ad1` (segmented as `.ad1`, `.ad2`, …). Produced by FTK Imager's **Custom Content Image** path, not by `Create Disk Image`. ⚠ **AD1 is not taught anywhere in units 1 or 2** — the FTK Imager format-selection dialog on `[U2 p98]` is a screenshot whose option list did not survive OCR. This box is written from outside the source to fill a course requirement; get a citable reference before teaching internals. See §7 G5. |
| **What it proves** | That specific named files existed at specific paths with specific timestamps at collection time. It is the right container when scope is limited by warrant or engagement letter to named material, and when the volume is too large to image. |
| **What it does NOT prove** | It proves **nothing about anything you did not select**. There is no unallocated space, no slack, no deleted content and no file-system structure outside the chosen paths — so an AD1 can never support a statement like "the file was not on the machine", only "the file was not in what I collected". Carving, timeline reconstruction from `$MFT`, and recovery of deleted evidence are all impossible against it. It is also the format most vulnerable to the sparse-acquisition trap INE warns about `[U2 p52]`: if the evidence was in a path that was not on the collection list, it is silently absent and the report will read as though it never existed. |
| **How to parse it** | FTK Imager: `File ▸ Add Evidence Item ▸ Image File` and select the `.ad1`; FTK proper mounts it as a logical evidence set. Most non-AccessData tools cannot read it — treat that as a reason to prefer E01 unless scope forces logical collection. |
| **Anti-forensics / false positive** | A tidy AD1 gives a false impression of completeness in a report. Anyone reading "forensic image" and seeing an AD1 will assume unallocated space was covered. Say **logical collection** in the report, never "image". |

`[U2 p50–52]` · *format itself not in U1/U2 — §7 G5*

### Acquisition hash set (MD5 / SHA-1 / SHA-256)
| | |
|---|---|
| **What it is** | The digest(s) computed over the source media before or during acquisition and over the resulting image afterwards, plus the recorded comparison of the two. |
| **Where it lives** | In the imager's log file, in the E01 container, in a sidecar `.txt`/`.md5`/`.sha256` next to a raw image, on the chain-of-custody form, and in the examiner's notes. INE is emphatic that the hash must be **stored securely and separately** `[U2 p144]`. |
| **What it proves** | That two byte streams are identical to within the collision resistance of the function. Re-hashing the image before each analysis session proves that nothing in your own custody chain altered it. |
| **What it does NOT prove** | A matching hash proves **integrity, not authenticity and not provenance** — it says the copy equals the source *as read at that moment*, and says nothing about where the source came from, who owned the data, whether it had already been altered before you arrived, or whether the drive in your hand is the drive from the seizure. INE itself blurs this: `[U2 p143]` says hashes "prove that the file has not been tampered with", which is only true if the hash was recorded before the attacker had access and stored somewhere they could not reach — INE gets this right one slide later at `[U2 p144]`, where an attacker with both the disk and the hash simply recomputes. A hash also does not prove the acquisition was **complete** (an HPA excluded from the read is excluded from both hashes, so they match perfectly), and a **mismatch** does not prove tampering — a failing sector, a cable fault or an SSD's own garbage collection between the two reads all produce mismatches with no misconduct at all. |
| **How to parse it** | Linux: `sha256sum EVI-SRC01.dd`, `md5sum EVI-SRC01.dd`, `sha512sum` (INE's demo, `[U2 p147–150]`). Windows: HashCalc computes MD5/SHA-1/SHA-256/SHA-512/RIPEMD in one pass `[U2 p151–157]`; FTK Imager computes and verifies automatically when *Verify images after they are created* is ticked. |
| **Anti-forensics / false positive** | MD5 and SHA-1 are broken for collision resistance `[U2 p145]` — record **both** MD5 and SHA-256 so a challenge to one does not sink the exhibit. SSDs with TRIM can return different content on a second read of the same deleted region, breaking hash repeatability with no wrongdoing involved (§7 G8). |

`[U2 p140–158]`

### FTK Imager acquisition & verification log (`<image>.001.txt` / `.E01.txt`)
| | |
|---|---|
| **What it is** | The plain-text summary FTK Imager writes beside every image it creates: examiner-entered case metadata, machine-detected source geometry, the acquisition and verification timestamps, and the computed digests with their verify result. |
| **Where it lives** | Same directory as the image, same base name, `.txt` extension `[U2 p103]`. Contains: `Created By AccessData® FTK® Imager <version>`; Case Information (case number, evidence number, unique description, examiner, notes); Drive Geometry (cylinders, tracks per cylinder, sectors per track, bytes per sector); drive interface and removable flag; source data size and sector count; `Acquisition started` / `Acquisition finished`; `Image Verification Results` with `MD5 checksum: … : verified` and `SHA1 checksum: … : verified` `[U2 p104]`. ⚠ The OCR mangles the version string and renders the 2017 acquisition dates as 2027 — read the real values off the page. |
| **What it proves** | That this image was produced by that tool version at that time, that the tool read back the completed image and recomputed the digests, and that the recomputation matched. It is the single most useful page to attach to a chain-of-custody form. |
| **What it does NOT prove** | `verified` is a **self-check, not an independent check** — the same program computed the hash while writing and again while reading back, so the line proves the write-then-read round trip was clean and proves nothing about the source drive, which the tool never re-reads. It does not record whether a write blocker was attached, does not record which physical device was selected, and does not detect that the examiner imaged the wrong disk. The Case Information block is entirely free text typed by the operator, so an evidence number in this file is a claim, not corroboration. The drive geometry is what the **interface reported**, so an HPA/DCO-shortened capacity is faithfully logged as though it were the whole disk. |
| **How to parse it** | Open in any text editor and transcribe MD5/SHA-1, start/finish times and source sector count onto the CoC form. Keep it with the image forever — losing it costs you the acquisition timestamps. |
| **Anti-forensics / false positive** | The file is an ordinary editable `.txt` sitting next to the image with no signature of any kind. Treat it as *documentation of* the acquisition, not as evidence of it; the authority comes from your notes and the CoC, not from this file being present. |

`[U2 p99–104]`

### Chain of custody form
| | |
|---|---|
| **What it is** | The continuous written record of possession and handling of one exhibit, from the moment it was seized to the moment the case closes. |
| **Where it lives** | Paper or case-management system, one form per exhibit, travelling with the exhibit. INE's required content: what the evidence is, how it was acquired, when, by whom, where it was stored, and every subsequent action performed on it `[U1 p169–170]`. Physical controls belong with it: antistatic bags and padding, sealed containers, **tape signed and written across the seal** so a re-opening is visible, and controlled temperature and humidity `[U1 p49–51]`. |
| **What it proves** | Continuity. It is the mechanism by which authenticity is actually demonstrated in court `[U1 p164]` — the examiner testifying can trace the exhibit back to the seizure through named, dated, signed hands. |
| **What it does NOT prove** | A complete CoC proves the **exhibit** was handled continuously; it says nothing about whether the **data on it** is genuine, unaltered before seizure, or relevant. The attacker's wiper ran before you arrived and the CoC is still perfect. It also does not prove that the acquisition was competent — a flawlessly documented image taken without a write blocker is flawlessly documented and still challengeable. And its evidential value is asymmetric: an unbroken CoC does not by itself win admissibility, while a single unexplained gap is enough to lose it, because the other side only has to raise the possibility of substitution or alteration `[U1 p137]`. |
| **How to parse it** | Read it as a timeline and check three things: no unexplained time gaps, no transfer without two signatures, and hash values recorded at seizure that still match today. Re-hash the exhibit at hand-off and record the result on the form. |
| **Anti-forensics / false positive** | The commonest failure is not malice but a junior examiner who does not label two identical drives from the same office `[U1 p156]` — after that, no form on earth can say which desk each came from. |

`[U1 p49–52]` `[U1 p137]` `[U1 p164]` `[U1 p169–170]` `[U2 p38]`

### Write blocker and its proof trail
| | |
|---|---|
| **What it is** | The hardware dock or software control that filters write commands out of the path to the evidence media — plus, and this is the artifact, the **record that shows it was in the path** during a specific acquisition. |
| **Where it lives** | Hardware: an inline unit between disk and workstation (INE names the WiebeTech Forensic UltraDock from CRU and the Tableau Forensic Imager TD3 `[U2 p81]`). Software: a forensic boot disc, or a registry policy (next artifact). The *proof trail* lives in four places — the blocker's own display/log, a photograph of the connected rig with serials legible, the CoC line naming blocker make/model/serial, and the examiner's contemporaneous notes. |
| **What it proves** | That write commands to the source could not reach the media, so the source hash taken before acquisition and after acquisition should be identical. Two matching source hashes taken across the imaging run are the strongest available technical evidence that nothing was written. |
| **What it does NOT prove** | Owning a write blocker proves nothing; **using** one is what must be evidenced, and no image file records that it was used — an image taken on a blocker and an image taken without one are byte-identical, so the fact lives only in your documentation and cannot be recovered later if you did not write it down. A blocker also protects only the **path it is in**: it does not stop the examiner mounting the source read-write on another port, does not protect other exhibits on the bench, and does not stop the *destination* being contaminated. Some blockers filter a configurable command list `[U2 p80]` rather than all writes, so "write blocked" is a claim about a specific device in a specific mode. And a blocker cannot undo damage already done — if the machine was booted once before you arrived, the blocker preserves the already-altered state perfectly. |
| **How to parse it** | Photograph the rig before disconnecting. Record blocker make/model/serial and firmware on the CoC. Hash the **source** before and after the imaging run and record both; matching source hashes across the run is the assertion you will defend, not the sentence "a write blocker was used". |
| **Anti-forensics / false positive** | INE warns hardware blockers may be unavailable — expensive, or restricted in some jurisdictions `[U2 p85]` — pushing examiners to software methods that are easier to get wrong and harder to evidence. A software blocker verified only by "I set the registry key" is not a proof trail. |

`[U1 p107]` `[U1 p110]` `[U2 p78–82]`

### `StorageDevicePolicies\WriteProtect` (software USB write block)
| | |
|---|---|
| **What it is** | A Windows policy value that makes the OS refuse write access to USB mass-storage devices, used as a fallback when no hardware blocker is available. |
| **Where it lives** | `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` — create the key if absent, then create a `REG_DWORD` named `WriteProtect` and set it to `1` (`0` = writes allowed). ⚠ The OCR on `[U2 p88]` shows only the `CurrentControlSet\Control` fragment of the path and the value at `0x00000000`; confirm the full path and the target value on the source page. Introduced for USB write-blocking in Windows XP, set via `regedit` on Windows 7 and later `[U2 p86–90]`. |
| **What it proves** | On the machine where it is set, USB mass-storage volumes are presented read-only, so plugging in evidence does not let Windows write to it. It is free and always available. |
| **What it does NOT prove** | This value sits in the **examiner's** registry, not the evidence's, so finding it set proves something about the analysis workstation and **nothing at all about how any particular exhibit was handled** — it is not per-device, not timestamped, and leaves no record tying it to an acquisition. It only covers devices enumerated as **USB mass storage**: it does not protect a SATA disk on an internal port, a drive in a USB-attached dock that presents as a fixed disk, MTP/PTP devices, or anything already mounted before the value was set. It is enforced by the same OS you are trying not to trust, so on a compromised or unpatched examiner box it is a policy request, not a hardware guarantee — and it typically needs a reboot or at minimum a re-enumeration of the device to take effect, so setting it with the evidence already plugged in may do nothing while looking like it worked. |
| **How to parse it** | Set it, reboot, then **test it** on a scratch USB stick before touching evidence: attempt a write and confirm the failure, and photograph or log the result. On the evidence side, verify by hashing the exhibit before and after connection. |
| **Anti-forensics / false positive** | The classic false positive is an examiner who sets the value, does not reboot, plugs the evidence in and reports "software write blocked". Windows will happily write to it. Always demonstrate the block, never assume it. |

`[U2 p84–90]`

### Memory image (RAM dump)
| | |
|---|---|
| **What it is** | A capture of physical memory contents from a running machine, taken by loading a kernel driver that reads physical address space and streams it to a file. |
| **Where it lives** | A single file on the examiner's removable drive — never the suspect's disk. In INE's Live Response Collection layout: `…\<HOSTNAME>_<date>_<time>\ForensicImages\Memory\<HOSTNAME>_<date>_<time>_mem.dmp` `[U2 p118]` `[U2 p123]`. Related non-volatile stores hold overlapping content: pagefile, hibernation file and crash dumps `[U2 p129]`; INE also notes memory pages paged out to disk can be met during **static** acquisition `[U2 p19]`. |
| **What it proves** | The contents of physical memory at the time of the capture: running processes, network state, injected code, unpacked executables, decrypted buffers, clipboard, browsing data, and encryption keys — including the full-disk-encryption key that makes an otherwise useless disk image readable `[U2 p71]` `[U2 p74]`. For RAM-only malware and rootkits that never touch disk, it is the *only* evidence there is `[U1 p142]` `[U2 p72–73]`. |
| **What it does NOT prove** | A RAM dump is a **smear, not a snapshot** — the machine keeps running while the capture streams, so pages captured at the start and at the end are from different moments and the image can contain structures that never coexisted; an inconsistent process list is a normal artifact of this, not evidence of anti-forensics. It proves state at **capture time only**, which is your arrival time, not incident time: a process seen here does not prove it was running during the incident, and a process absent here does not prove it never ran. It is also self-incriminating by construction — the collector must load a driver and allocate memory, so some of what you capture is your own footprint, and INE says this plainly: "running your forensic tool will change part of the memory" `[U1 p80]`. Finally, RAM has **no built-in structure to help you** — unlike a file system there is no allocation table or directory, so everything above raw bytes is a profile-driven reconstruction `[U2 p69]`. |
| **How to parse it** | Identify the profile first: `volatility_2.6_win64_standalone.exe imageinfo -f <mem.dmp>` `[U2 p130]`, then pass it to every later command: `volatility --profile=Win7SP0x64 pslist -f img_mem.dmp` `[U2 p131]`. ⚠ Profile strings are case-sensitive (`Win7SP0x64`); the OCR renders it `Win7sP0x64`. Also run `bulk_extractor <mem.dmp> -o <outdir>` for strings-level yield `[U2 p137]`. |
| **Anti-forensics / false positive** | Anti-forensic tooling can hide from a live collector running through the OS. Cutting power to preserve the disk destroys RAM entirely, and INE flags the opposite emergency too: if a destructive program is running (a wipe in progress), pulling power immediately may be the right call and you lose memory to save the disk `[U1 p47–48]`. |

`[U2 p57–76]` `[U2 p126–133]`

### Live Response Collection output tree
| | |
|---|---|
| **What it is** | The directory of volatile-state artifacts, copied files and logs produced by an automated live-response collector run against a machine that is still up. INE uses BriMor Labs' Live Response Collection. |
| **Where it lives** | One folder per host, named `<HOSTNAME>_<yyyymmdd>_<hhmmss>`, containing `ForensicImages\` (with `Memory\` and `DiskImage\`) and `LiveResponseData\` with `BasicInfo\`, `CopiedFiles\`, `NetworkInfo\`, `PersistenceMechanisms\` and `UserInfo\` `[U2 p119–125]`. A `Processing_Details.txt` logs every command the framework ran, and a hash list records a digest for **every file collected** `[U2 p121–122]`. Menu options: Secure-Complete, Secure-Memory Dump, Secure-Triage, Complete, Memory Dump, Triage — the "Secure-" variants compress and password-protect the output `[U2 p117]`. ⚠ The first menu label did not OCR cleanly; read it off the page. |
| **What it proves** | What the machine looked like from the inside at collection time: OS version and build, computer name and accounts, uptime, time zone, installed updates, installed software, running processes, loaded drivers, NICs with MAC and IP addresses, open sessions and shares, event logs, persistence locations `[U2 p63–68]`. The per-file hash list and command log make the collection itself auditable. |
| **What it does NOT prove** | Every file in this tree is the **operating system's answer to a question**, not a reading of the disk — which means on a rootkitted host the collection faithfully records the rootkit's lies, and a clean process list here is not evidence of a clean machine `[U2 p20–21]`. The timestamps throughout are **collection timestamps**, so the tree establishes state at your arrival and cannot be used to place any process, connection or user session at the time of the incident. It is also an unavoidably invasive act: the collector writes to memory, creates processes, and (if the output goes anywhere but removable media) writes to the suspect disk, so some of what a later examiner finds in prefetch, `$MFT` and event logs is *you*. And "hash of every collected file" proves the collection was not altered afterwards; it says nothing about whether the file was authentic on the host. |
| **How to parse it** | Read `Processing_Details.txt` first to learn exactly what was run — that is your method section. Then work `BasicInfo\` for host identity, `NetworkInfo\` for connections, `PersistenceMechanisms\` for autoruns, `CopiedFiles\event logs\Logs\*.evtx` for the event log set. The memory image under `ForensicImages\Memory\` goes to Volatility; the disk image under `ForensicImages\DiskImage\` goes to FTK Imager `[U2 p124]`. |
| **Anti-forensics / false positive** | Anything driven by the live OS can be subverted by the live OS. Corroborate every live finding against the dead image afterwards — this is the abstraction-layer lesson applied to a whole toolchain. |

`[U2 p116–125]`

### Targeted (sparse) triage collection set
| | |
|---|---|
| **What it is** | A selective forensic copy of a defined list of files, folders and — optionally — the unallocated area, taken instead of a full image when a full image is impossible or disproportionate. |
| **Where it lives** | Wherever the collector writes it: a folder tree, a container, or a logical image. The defining feature is the **targets list** — the checklist of what was collected — which must be preserved alongside the output. |
| **What it proves** | That the listed items existed with the recorded content and metadata at collection time. It is the right answer when the system cannot be taken offline, or when the volume is so large that imaging would take longer than the case allows `[U2 p51]` — INE's "size and distribution" challenge `[U1 p144]`. |
| **What it does NOT prove** | **Absence in a triage set is not absence on the disk.** This is the single most dangerous inference in the module: everything outside the targets list is uncollected, not non-existent, and a report that says "no evidence of X was found" after a targeted collection is making a claim the collection cannot support. INE states the trade-off directly — the examiner "must either know what to select for acquisition and have a checklist, or he will leave some evidence behind" `[U2 p52]`, and warns you may simply fail to acquire the relevant data `[U1 p144]`. It also cannot support carving, unallocated recovery or full-timeline reconstruction unless unallocated was explicitly included, and it cannot be re-interrogated later with a new hypothesis — a full image can, which is why a triage set is a *first* response, not a substitute for one. |
| **How to parse it** | Publish the targets list in the report as part of the method. Then treat every negative finding as bounded: "not present in the collected set" rather than "not present on the system". ⚠ **KAPE** — the standard targeted-triage tool for this course — is not in units 1 or 2 (released after this courseware); INE teaches only the concept. See §7 G6. |
| **Anti-forensics / false positive** | An attacker who stores tooling outside the usual paths (an unusual directory, an unmounted volume, alternate data streams) defeats a stock targets list entirely and leaves the collection looking complete. |

`[U2 p50–55]` `[U1 p144]`

### `bulk_extractor` feature files
| | |
|---|---|
| **What it is** | The set of text reports produced by scanning an image, a file or a memory dump for recognisable patterns **without parsing the file system at all** — it reads the bytes and reports what it recognises. |
| **Where it lives** | One output directory, one file per feature type: `email.txt`, `domain.txt`, `ip.txt`, `ether.txt`, `url.txt`, `url_searches.txt`, `telephone.txt`, `ccn.txt` and `ccn_track2.txt` (payment card data), `exif.txt`, `zip.txt`, `wordlist.txt`, `aes_keys.txt`, `packets.pcap`, plus a `*_histogram.txt` for each and a `report.xml` `[U2 p136]` `[U2 p139]`. ⚠ The OCR renders the credit-card files as `con.txt` / `con_track2.txt`; the real names are `ccn.txt` / `ccn_track2.txt` — verify on the page. |
| **What it proves** | That a byte sequence matching that pattern exists somewhere in the scanned data — including inside compressed archives, hibernation files, swap and file fragments that no file-system-aware tool would reach. The histograms rank by frequency, which is a fast way to find the addresses and domains that actually matter `[U2 p135]`. |
| **What it does NOT prove** | A feature file entry proves a **string was present in the bytes**, and nothing more: no file, no owner, no timestamp, no application, no user action. An email address in `email.txt` does not mean a message was sent or received — the address may come from a software licence blob, a cached web page, a mailing-list footer or an installer's manifest; a URL in `url.txt` does not mean anyone visited it, since browsers, updaters and executables carry hard-coded URLs by the thousand; an IP in `ip.txt` may have been carved out of a packet fragment in swap that the machine never originated. Because it deliberately ignores the file system, it **cannot tell allocated from deleted from never-a-file**, so it can never support a statement about what a user did — only about what bytes existed. Everything it outputs is a lead requiring corroboration in the file system or the logs. |
| **How to parse it** | `bulk_extractor <image-or-dump> -o /root/Bulk` `[U2 p137]`; a summary and the input's hash are printed on completion `[U2 p138]`. Start with the `*_histogram.txt` files, not the raw feature files. |
| **Anti-forensics / false positive** | It is a false-positive engine by design — this is the intended trade, breadth over precision. Note also the privacy exposure: `ccn.txt` and `pii.txt` will contain live payment-card and personal data from bystanders, and must be handled under the privacy constraint INE raises at `[U1 p138]`. |

`[U2 p134–139]`

### Acquisition timestamp and time-zone record
| | |
|---|---|
| **What it is** | The recorded date, time **and time zone** of every acquisition event, captured for each exhibit at the moment it is acquired. |
| **Where it lives** | Auto-generated into the imager's metadata and log (`Acquisition started` / `Acquisition finished` in the FTK Imager `.txt` `[U2 p104]`), and written by hand onto the CoC when the tool does not produce it — INE makes that the examiner's explicit responsibility `[U2 p176]`. |
| **What it proves** | When *your* handling of the exhibit happened, which anchors the acquisition into the case timeline and lets an integrity challenge be tested against a specific window `[U2 p177]`. |
| **What it does NOT prove** | These are **your clock's** timestamps, not the evidence's — they say when you imaged, and carry no information whatever about when anything on the media was created, accessed or modified. Nor does the *presence* of a time zone in the log prove the zone is right: it is read from the acquisition workstation's own settings, so an examiner box set to the wrong zone produces a confidently wrong record. On-media timestamps are a separate problem entirely: they are stored in binary formats and rendered by a tool's interpretation layer, INE warns that interpretation "might not be reliable" across formats `[U2 p179]`, and a suspect can simply have changed the system clock before acting `[U1 p117]` — so a file time is never a fact about when something happened until it is corroborated. |
| **How to parse it** | Record local time **with offset** and the UTC equivalent for every event. Convert on-media binary timestamps with DCode: format `Windows: 64 bit Hex Value - Little Endian`, e.g. `FF03D2315FE1C701` → `Sat, 18 August 2007 06:15:37 UTC` `[U2 p181–182]` (verified correct by independent FILETIME decode). Cross-check any critical timestamp with a second tool `[U2 p180]`. |
| **Anti-forensics / false positive** | System-clock manipulation is trivial and invisible in the timestamp itself. Anchor at least one on-media time to an external reference — a server log, a network capture, an NTP-synced source — before building a timeline on it (this is S5's problem, seeded here). |

`[U2 p174–182]` `[U1 p117]`

## 3 · Tools

| Tool | What it is for | Command / entry point | Output | Caveat |
|---|---|---|---|---|
| **FTK Imager** (AccessData/Exterro, free) | Imaging, verification, mounting, previewing, exporting `[U2 p91–115]` | `File ▸ Create Disk Image` ▸ source type (Physical Drive, Logical Drive, Image File, Contents of a Folder, Fernico Device) ▸ format ▸ metadata ▸ destination. Tick *Verify images after they are created* and *Create directory listings of all files in the image* | Image set plus a `.txt` log with case metadata, geometry, times and verified MD5/SHA-1 | Free version is imaging-and-triage only, not full analysis. INE stresses: still use a write blocker — the tool does not blockify anything `[U2 p92]` |
| **FTK Imager — image mounting** | Read-only mounting for exploration `[U2 p109–113]` | `File ▸ Image Mounting` ▸ Mount Type `Physical & Logical` ▸ Drive Letter `Next Available` ▸ Mount Method `Block Device / Read Only` ▸ Mount | Image appears as a drive in *This PC*; unmount from the same dialog | **Never** mount Read/Write `[U2 p164]`. ⚠ Mount Method label is garbled in OCR — confirm on p113 |
| **`dd`** | Raw imaging on Linux (and Windows via a port) `[U2 p26–27]` | `dd if=/dev/sdb of=/mnt/case/EVI-SRC01.dd bs=4M conv=noerror,sync status=progress` | Single raw file, or split parts | No hashing, no logging, no metadata — all four are your job. ⚠ INE attributes splitting to a `-b` option "through command pipelining" `[U2 p27]`; `-b` is `split`'s flag, so the real form is `dd if=… \| split -b 1G - image.dd.` (pipe escaped for this table) — **verify against source page** and see §7 G3 |
| **`dc3dd`** | Forensic fork of `dd` — hashing on the fly, progress, error logging, verification | `dc3dd if=/dev/sdb of=EVI-SRC01.dd hash=sha256 log=EVI-SRC01.log` | Raw image plus a log containing the hash and any read errors | **Not in units 1 or 2** — see §7 G3. Prefer it to plain `dd` in the lab precisely because it produces the log `dd` does not |
| **Hardware write blocker** | Physically filtering writes to the source `[U2 p78–82]` | Inline between evidence disk and workstation. INE names WiebeTech Forensic UltraDock (CRU) and Tableau Forensic Imager TD3 | No file output — the evidence is the photograph, the unit's log and your notes | Some units block only a configured command list `[U2 p80]`. May be unavailable by cost or jurisdiction `[U2 p85]` |
| **Windows USB write protect** | Software fallback write block `[U2 p86–90]` | `regedit` ▸ `HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` ▸ new `REG_DWORD` `WriteProtect` = `1` | Nothing — a policy state on the examiner box | Reboot/re-enumerate, then **prove** it with a scratch stick before touching evidence. ⚠ verify full path on p88 |
| **Bootable forensic disc** | Dead acquisition without trusting the suspect OS `[U2 p83]` | Boot the suspect machine from a self-contained read-only OS | Image written to attached destination media | Must confirm the distro does not auto-mount or auto-swap. Changing boot order touches firmware settings — record it |
| **BriMor Labs Live Response Collection** | Scripted volatile-data and triage collection `[U2 p116–125]` | Run `Windows Live Response Collection` as administrator, pick Triage / Memory Dump / Complete (or the "Secure-" variants) | `<HOSTNAME>_<date>_<time>\` with `ForensicImages\` and `LiveResponseData\`, a per-file hash list and `Processing_Details.txt` | Everything it reports comes through the suspect OS. Write output to removable media, never the suspect disk |
| **Belkasoft Live RAM Capturer** | Memory acquisition (the engine inside the collection above) `[U2 p118]` | `RamCapture64.exe <output-path>` — loads a driver, reports page size and total physical memory | `<HOSTNAME>_<date>_<time>_mem.dmp` | Capturing takes minutes on a busy host and the result is a smear, not a snapshot |
| **Volatility 2.6** | Memory image analysis `[U2 p127–132]` | `volatility_2.6_win64_standalone.exe imageinfo -f <mem.dmp>` then `volatility --profile=Win7SP0x64 pslist -f img_mem.dmp` | Per-plugin text output | Profile must match exactly and is case-sensitive. Version-locked profile list — see §7 G9 |
| **`bulk_extractor`** | File-system-agnostic pattern extraction from images and dumps `[U2 p134–139]` | `bulk_extractor <image-or-dump> -o /root/Bulk` | ~40 feature files plus histograms and `report.xml` | Leads only. Handle `ccn.txt` / `pii.txt` under privacy constraints |
| **`sha256sum` / `md5sum` / `sha512sum`** | Hashing on Linux, built in `[U2 p147–150]` | `sha256sum EVI-SRC01.dd` | 64-hex-character digest plus filename | INE demonstrates SHA-512; the course standard is MD5 **and** SHA-256 — see §7 G7 |
| **HashCalc** (SlavaSoft) | Hashing on Windows, several algorithms in one pass `[U2 p151–157]` | GUI: choose data format and path, `Calculate` | MD5, SHA-1, SHA-256/384/512, RIPEMD, CRC32 in one window | Unmaintained freeware. `certutil -hashfile <file> SHA256` is the built-in modern alternative — see §7 G7 |
| **Linux read-only mount** | Exploring an image without a forensic suite `[U2 p166]` | `mount -o ro,loop,show_sys_files,streams_interface=windows,offset=<bytes> evidence.raw /mnt/cases/case002` | Image contents browsable read-only | ⚠ Four OCR defects on p166 — see §7 G2. `offset` is in **bytes**, so a partition starting at LBA 2048 is `offset=1048576`; get it from `mmls`. The two NTFS options need `-t ntfs-3g` |
| **Image mounters** | Read-only mounting `[U2 p171]` | Arsenal Image Mounter, OSFMount, Mount Image Pro, P2 eXplorer Pro, FTK Imager | Mounted read-only volume | Mounting is an abstraction layer: you are seeing the mounter's file-system parser, not the disk |
| **DCode** (Digital Detective) | Converting binary timestamps to human time `[U2 p181–182]` | Pick *Decode Format*, paste the value, read *Date & Time* | Human-readable UTC with selectable bias | Getting the source format wrong yields a confident wrong date. Cross-check with a second tool `[U2 p180]` |
| **KAPE** | Targeted triage collection against Targets and Modules | `kape.exe --tsource C: --tdest <out> --target !SANS_Triage --mdest <out> --module !EZParser` | Collected artifact tree plus parsed CSV output | **Not in units 1 or 2** — post-dates this courseware. See §7 G6. Verify current syntax before class |

## 4 · Findings vs interpretation — worked from this module

> **FINDING** — the FTK Imager log for `EVI-SRC01.E01` reads `MD5 checksum: <value> : verified` and `SHA1 checksum: <value> : verified`, with acquisition start and finish timestamps `[U2 p104]`.
> **INTERPRETATION** — the image was written and read back without corruption, so the file on the destination drive is very probably a faithful copy of whatever the tool read from the source.
> **CANNOT PROVE** — that the *source* is unaltered. The tool hashed its own read and its own write-back; it never re-read the drive. It also cannot show that a write blocker was in the path, that the physical device selected was the one on the CoC form, or that the read covered the whole physical medium — an HPA or DCO excluded from the read is excluded from both hashes, and they match perfectly.

> **FINDING** — the source USB hashed `SHA-256 <value>` before imaging and the same value after the imaging run completed.
> **INTERPRETATION** — nothing was written to the device across the imaging window, which is consistent with an effective write block, and the acquisition is defensible on that point.
> **CANNOT PROVE** — that a write blocker was used. Two identical hashes are consistent with a blocker, with a correctly-set software policy, and with sheer luck on a system that happened not to touch the volume. The blocker itself is proven only by the photograph, the serial on the CoC and the contemporaneous notes — which is exactly why "how do you prove you used one" is a graded question and not a rhetorical one.

> **FINDING** — the Live Response Collection `pslist` output lists a process named `svch0st.exe` running from `C:\Users\<user>\AppData\Roaming\`, and `NetworkInfo\` records an established connection from that process to `198.51.100.42:443`.
> **INTERPRETATION** — a process masquerading as a system binary was beaconing to an external host at the moment of collection; this is consistent with the C2 stage of our incident and is a strong lead for the memory image.
> **CANNOT PROVE** — that the process was malicious (the name is suggestive, not diagnostic), that the logged-on user launched it, that it was running at the time of the original compromise, or that it is even really there — the list came from the suspect OS's own API, and a rootkit that hides processes would produce a clean-looking list `[U2 p20–21]`. It establishes collection-time state only.

> **FINDING** — `bulk_extractor` `email.txt` from `EVI-SRC01.dd` contains an external address, and `url_searches.txt` contains a search term matching the exfiltration hypothesis.
> **INTERPRETATION** — data matching those patterns exists somewhere in the image, in allocated space, deleted space, swap or a compressed blob; both are worth resolving to a file and a timestamp.
> **CANNOT PROVE** — that the user ever sent to that address, saw that page or typed that search. `bulk_extractor` does not parse the file system at all `[U2 p134]`, so it cannot say whether the string was in a live file, a deleted fragment, a cached page, an installer's manifest or a licence blob — and it attaches no owner, no timestamp and no application to anything it finds.

> **FINDING** — the acquired image of the suspect USB is 64 GB, exactly the device's reported capacity, and the file listing shows only four documents totalling 3 MB `[U2 p107]`.
> **INTERPRETATION** — the device was imaged physically rather than copied logically, so the remaining ~64 GB of unallocated space is present in the image and available for carving in S3; the small live file count says nothing yet about what was on the device previously.
> **CANNOT PROVE** — that the whole physical medium was captured. The image covers the LBA range the controller reported; flash over-provisioning, remapped blocks and any controller-hidden area are outside it. Nor does an image the size of the device prove the device was full, or that anything was deleted — INE's own point at `[U2 p107]` is only that image size tracks capacity, not usage.

## 5 · Exam-relevant points

- The three phases of the digital evidence life cycle in order: **acquisition, analysis, presentation** `[U1 p38]`.
- **Order of volatility**: most volatile is CPU registers, least volatile is external/secondary storage; collect most-volatile first `[U2 p13–15]`.
- Acquisition types: **static** (non-volatile), **dynamic/live** (volatile, machine running), **dead** (without the suspect OS's help, because a rootkitted OS cannot be trusted) `[U2 p16–21]`.
- **Imaging** copies every sector including unallocated; **copying** takes only allocated data `[U2 p36–37]`.
- Acquisition *methods*: disk-to-image (scalable, many copies), disk-to-disk/clone (when imaging fails, needs a physical disk per acquisition), **sparse** (selective, fastest, risks leaving evidence behind), **logical disk-to-disk** (one partition, slower than sparse but complete within it) `[U2 p41–55]`.
- Three evidence characteristics INE lists: **admissible, authentic, complete** `[U1 p96]`. Three admissibility tests: **relevant, reliable, competent** `[U1 p163–166]`.
- Reliability decomposes into **authenticity** (proven by chain of custody) and **objectivity** (a proven fact, not an opinion) `[U1 p164–165]`.
- Acceptance in court depends on the **credibility of the scientific method**, the **investigator's qualifications**, and **reproducibility** `[U1 p168]`.
- **Repeatable** = same lab, same tools, same result. **Reproducible** = different lab or tools, same result. Both are required `[U1 p118]`.
- Three evidence outcomes against a hypothesis: **inculpatory** (supports), **exculpatory** (contradicts), **tampering** (indicates deception) `[U1 p57]`.
- Hidden data types: **metadata**, **residual** (deleted), **replicant** (temporary copies made by applications) `[U1 p68–75]`.
- Investigation types INE distinguishes: **internal** (inside an organisation, bound by its own policy — fraud, data exfiltration, harassment; escalate to law enforcement if something graver surfaces) and **civil** (organisational assets, copyright, illegal access, malware; harder at scale, more expensive tooling, a legal background helps) `[U1 p120–125]`. ⚠ The third type — almost certainly criminal — is on p126, which did not OCR; see §7 G21.
- Image formats INE names: **raw/dd** (fast, portable, no metadata, tolerates small read errors silently), **proprietary/EWF** used by EnCase (compression, embedded hash or CRC, case metadata, single framework), **sgzip** used by PyFlag, **ILook Investigator**, and the open **AFF** — Advanced Forensics Format, compression plus integrity check plus custom metadata fields that can be embedded or held in a sidecar, copying in 16 MB pages; early versions could not collect live data, lacked encryption and mishandled NTFS metadata `[U2 p31–35]`.
- Crime-reconstruction analyses: **relational** (what relates to what), **functional** (how a thing was used or works), **temporal** (ordering events), plus **same-origin comparison** `[U1 p129–131]`.
- Hash functions are one-way, fixed-length, avalanche-sensitive; MD5 and SHA-1 are collision-vulnerable `[U2 p142–145]`.
- The hash must be **stored securely and separately** from the evidence, or an attacker with both can recompute after altering `[U2 p144]`.
- Write blockers filter write commands and come in **hardware and software** forms; some filter a configurable command list `[U2 p80]`.
- Windows USB write protect: `HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` ▸ `WriteProtect` DWORD `= 1`, first introduced in Windows XP `[U2 p86–90]`.
- Evidence is always mounted **read-only**; never read-write `[U2 p163–164]`.
- **Commingling**: use a new or forensically wiped destination drive for every case `[U1 p100]` `[U1 p154]`.
- **Abstraction layer**: you never see the data, only the tool's representation of it; each layer adds a margin of error; mitigate with multiple tools or by examining both sides of the layer `[U1 p171–185]`.
- Four challenge categories INE names: **legal**, **type of digital evidence**, **size and distribution**, **evidence dynamic** `[U1 p136–149]`.
- Memory forensics is indicated for **full-disk encryption** (key recovery), **rootkits/APT**, and **memory-only malware** `[U1 p142]` `[U2 p70–73]`.
- Record acquisition **date, time and time zone** for every exhibit; if the tool does not, you must `[U2 p176]`.
- Chain-of-custody fields: what, how, when, who, where stored, and every subsequent action `[U1 p170]`.

## 6 · Teaching notes

**Where students reliably go wrong**

1. **"The hash proves the evidence is genuine."** They fuse integrity with authenticity every time. Make them say the two sentences separately — *the copy equals the source* (hash) and *the source is what the form says it is* (chain of custody) — then put `[U2 p143]` and `[U2 p144]` side by side, where INE says both things one slide apart and the second corrects the first. This is the module's best live example of a source blurring finding and interpretation.
2. **"Verified means verified against the disk."** It means the tool checked its own output. Walk the FTK Imager log line by line and have them mark which lines describe the source and which describe the image. Almost nothing describes the source.
3. **"We didn't find it, so it isn't there."** Kill this on the triage set and on `bulk_extractor` both. The permitted sentence is *"not present in the collected set"*.
4. **"Live response tells you what's on the machine."** It tells you what the machine *says* is on the machine. Pair it with dead acquisition every time you demo it.
5. **Order of volatility inverted under pressure.** In a simulated call-out students reach for the disk first because it feels like the real evidence. Drill RAM-first until it is reflex — then run INE's counter-case `[U1 p47–48]`, where a wiper is running and pulling power *is* correct, so they learn the rule has a reason rather than a chant.
6. **Confusing sparse / logical / physical.** Three columns on the board, one scenario each: 40 TB SAN (sparse), one partition under warrant (logical), single laptop disk (physical).
7. **Working on the first image.** INE says it twice `[U2 p10]` `[U2 p45]` and they still do it. Enforce it in the lab: original hashed and shelved, work copy under a different filename.

**Demo live (S1)** — hash a text file, change one character, hash again `[U2 p146–150]`, using `sha256sum` rather than INE's `sha512sum` so the digest matches what students will use. Fill in a CoC form on the board for one exhibit and have a student play defence counsel against it. Show a file's last-access time before and after opening it — and say honestly that modern Windows usually disables last-access updates, which is a first taste of "this courseware is a decade old".

**Demo live (S2)** — FTK Imager end to end on a small USB: create disk image, fill the metadata, tick *Verify*, then read the verification block of the `.txt` log aloud. Then the USB write-protect key: set it, **fail to reboot**, write to a scratch stick successfully, reboot, fail. Best five minutes in the module. Then mount the image read-only, browse, attempt a write, watch it fail. Finally run a triage collector against a live VM and diff the result against a full image of the same VM — what is missing from the triage set is the lesson.

**Leave to homework** — `bulk_extractor` over a supplied memory dump, reporting three leads and, for each, what it does *not* establish. Volatility `imageinfo` then `pslist` on the same dump (profile identification is fiddly and better done unhurried). Write the acquisition section of the report for the exfil USB: tools, versions, hashes, times with zone, write-block method and how it is evidenced. Read McKemmish on "forensically sound" `[U1 p158]` and answer which of his four criteria our USB acquisition met.

## 7 · Gaps, cautions and disagreements

Tags: **[missing]** the course needs it, these units lack it (→ gap row) · **[dated]** INE is behind current practice · **[OCR]** the source text is unreliable here · **[disagreement]** INE conflicts with outside fact or with itself.

**G1 · [OCR] Order-of-volatility ladder incomplete.** `[U2 p14]` is a graphic; OCR recovered only the two ends ("Registers", "External and secondary storage devices"). Every intermediate rung is lost — teach the full ladder from an external source, not this page.

**G2 · [OCR] The read-only mount command on `[U2 p166]` has five defects.** OCR reads `mount —o ro,loop,show_sys_ files,streams_interace=windows offset=2048 evidence.raw /mnt/case002`: em-dash for `-o`; a space inside `show_sys_files`; `streams_interace` for `streams_interface`; a missing comma before `offset=`; and a mount point that disagrees with the prose on the same slide (`/mnt/cases/case002`). Also `offset` is in **bytes** — a partition at LBA 2048 needs `offset=1048576`. Never slide this line as printed.

**G3 · [OCR + missing] `dd` splitting misattributed; `dc3dd` absent.** `[U2 p27]` credits splitting to a `-b` option "through command pipelining". `-b` is `split`'s flag; `dd`'s `bs=` is block size and does not split. **INE wins on technical meaning for this course, but this is a flat flag error — correct it in delivery and record the disagreement.** `dc3dd` (hashes on the fly, writes a log) is never mentioned and is the tool students should actually use. → gap row.

**G4 · [missing] E01 internals undocumented.** INE describes proprietary formats only as "a header with metadata such as hash value or CRC embedded within" `[U2 p28]`. No segments, chunk CRC, stored acquisition hash or footer — so nothing explains *why* E01 verification beats a sidecar `.md5`. → gap row.

**G5 · [missing] AD1 is absent entirely.** No slide names AD1, SMART or "custom content"; the FTK Imager format dialog `[U2 p98]` is a screenshot whose option list did not OCR. §2's AD1 table is written from outside the source and needs an external citation before teaching. → gap row.

**G6 · [missing] KAPE is absent.** INE teaches *sparse acquisition* as a concept `[U2 p50–55]` but names no targeted-triage tool; KAPE post-dates this courseware. Targets/Modules syntax and the parse-on-collection workflow need external material. → gap row.

**G7 · [missing + dated] SHA-256 never named; Windows hashing advice obsolete.** INE demonstrates SHA-512 `[U2 p147–150]`, warns off MD5 and SHA-1 `[U2 p145]`, and recommends no replacement — the "many hash functions today" list lost items 1–3 to OCR. It also claims Windows has no built-in hashing tool `[U2 p151]`: wrong then for `certutil -hashfile <file> SHA256`, wrong now for `Get-FileHash -Algorithm SHA256`. HashCalc is unmaintained. Course standard: record **MD5 and SHA-256**. → gap row.

**G8 · [missing] SSDs, TRIM and hash repeatability.** Neither unit distinguishes flash from spinning media. A TRIMmed SSD can return different content on a second read of the same deleted region, so re-imaging can yield a different hash with no wrongdoing — which directly undercuts INE's repeatability requirement `[U1 p118]`. Over-provisioned and remapped blocks are also unreachable via normal LBAs. → gap row.

**G9 · [dated] Volatility 2.6 and the profile model.** `[U2 p129]` bounds support at Windows XP SP2–10, Server 2003–2016, macOS 10.5–10.12. Volatility 3 dropped profiles for symbol tables, so `--profile=Win7SP0x64` `[U2 p131]` does not exist in the version students will install. Fix the lab's version and say which.

**G10 · [missing] How to *prove* a write blocker was used — the module's largest hole.** The units explain thoroughly what a blocker is and why it matters `[U1 p110]` `[U2 p78–82]`, then never address the evidential question the topic map asks: the blocker's own log, photographing the rig, recording make/model/serial/firmware on the CoC, and the before-and-after **source** hash across the imaging run, which is the actual technical proof. Because a blocked and an unblocked image are byte-identical, this cannot be recovered after the fact and must be taught as procedure. → gap row, highest priority.

**G11 · [missing] HPA, DCO and hidden device areas.** Never mentioned — so the course says "image the whole disk" without ever saying the reported capacity may not be the whole disk, and gives no detection or removal procedure. → gap row.

**G12 · [missing] Full-disk encryption at acquisition.** INE's only answer to FDE is "recover the key from memory" `[U2 p71]`. Nothing on capturing a BitLocker recovery key before power-down, suspending BitLocker, acquiring a decrypted logical volume live, or recognising an encrypted volume during triage. → gap row.

**G13 · [missing] Memory acquisition pitfalls and current tooling.** `[U2 p69]` says memory forensics "is not easy" and stops. Nothing on the capture being a smear rather than an atomic snapshot; driver signing and Secure Boot blocking a capture driver; the pagefile, hibernation file and crash dumps as acquisition sources (named once in passing at `[U2 p129]`); or current capture tools (WinPmem, DumpIt, Magnet RAM Capture) — INE has only Belkasoft via the BriMor framework. → gap row.

**G14 · [missing] No standards cited by name.** No ACPO, NIST SP 800-86, SWGDE or ISO/IEC 27037; the only external anchors are McKemmish `[U1 p158]` and Casey `[U1 p193]`. ACPO Principle 1 ("no action should change data held on a device") is the cleanest one-line statement of this module and must come from outside. → gap row.

**G15 · [missing] No CoC template or exhibit-numbering scheme.** `[U1 p169–170]` lists the *fields* but gives no form, transfer-log layout, signature discipline or exhibit-ID convention. Students need a concrete artefact to fill in. → gap row.

**G16 · [missing] Virtual machine, cloud and remote acquisition.** Remote acquisition appears once, as a *challenge* `[U1 p139]`, and is never taught. Nothing on VMDK/VHDX, snapshot semantics, hypervisor-level acquisition or cloud collection. → gap row.

**G17 · [missing] Evidence retention and disposal.** The life cycle ends at presentation `[U1 p58–61]`; nothing on holding periods, secure destruction or returning media. → gap row.

**G18 · [dated] Versions, vendors, limits.** `[U2 p81]` gives the Tableau TD3 to Guidance Software (EnCase is now OpenText); FTK Imager is now Exterro. The 2 GB EWF segment limit `[U2 p32]` is legacy-image history, not a current constraint. All registry and OS demos are Windows 7 `[U2 p87–90]`; the lab is Windows 10/11, where the key still works but last-access updates are disabled by default — which softens INE's "double-clicking ruins evidence" example `[U1 p160]`. The lesson holds; the specific timestamp effect often does not.

**G19 · [OCR] FTK Imager screenshots heavily degraded.** `[U2 p98]`'s format list did not OCR at all. `[U2 p104]` gives the version as both `#4.5.8` and `a0g3.4,3,.3`, and dates the acquisition to **2027** (it is 2017). `[U2 p96]` reads "Femico Device" for *Fernico*; `[U2 p113]` reads "Bec Devce (ReadOnly" for *Block Device / Read Only*. Read all of these off the page before slide-making.

**G20 · [OCR] Exact strings to check before use.** Both demo SHA-512 digests are truncated (`a545de…`, `34a593…`) `[U2 p148]` `[U2 p150]` — regenerate live. The registry path shows only the `CurrentControlSet\Control` fragment, and the screenshot shows `WriteProtect` at `0x00000000` while the prose says change it "from 0" — the target value (1) is implied, not printed `[U2 p88–90]`. The Volatility profile renders `Win7sP0x64`; correct is `Win7SP0x64` `[U2 p131]`. `bulk_extractor`'s card outputs read `con.txt`/`con_track2.txt`; they are `ccn.txt`/`ccn_track2.txt` `[U2 p136]`. The first Live Response menu label (Secure-Complete) did not OCR `[U2 p117]`. **Verified good:** the DCode example `FF03D2315FE1C701` → `Sat, 18 August 2007 06:15:37 UTC` `[U2 p181–182]` decodes correctly as a little-endian Windows FILETIME, weekday included — usable as printed.

**G21 · [OCR] Pages that produced no text.** Unit 1: 4, 11, 23, 37, 126, 151. Unit 2: 3, 22, 40, 126, 140, 159, 173. All are section dividers **except U1 p126**, which sits between "Civil Investigation" and the Crime Reconstruction divider and is almost certainly the third investigation type (criminal) — recover it from the PDF before teaching investigation scope. Unit 1's contents also jumps `1.4.2.3` → `1.4.2.5`: **§1.4.2.4 is missing from the source's own contents**, so a subsection may be unaccounted for.

**G22 · [disagreement] AFF attribution.** `[U2 p33]` credits AFF to Basis Technology; it is generally attributed to Simson Garfinkel, with Basis Technology associated with AFFLIB's later maintenance. **INE wins on technical meaning for this course** — say "as INE has it" rather than repeating the attribution as fact.

**G23 · [disagreement] INE contradicts itself on what a hash proves — teach the contradiction.** `[U2 p143]`: hashes "prove that the file has not been tampered with". `[U2 p144]`, one slide later: an attacker holding both the disk and the hash alters the disk and recomputes. The second is correct; the first is a finding stated as an interpretation. Use both slides together in S1 as the module's worked example of the distinction the course grades on (D7).

**G24 · [disagreement] Two INE case stories are unreliable.** `[U1 p106]` is headed "The 'BTK' Serial Killer Child Pornography case in 2004" but describes an entirely different matter (a machine taken to a retail repair counter). `[U1 p71]` says the BTK killer "murdered 10 people within 90 years". The forensic *lessons* (document metadata identified the sender; third-party discovery starts investigations) are sound; the case details are not — use the lessons, drop or verify the specifics.

**G25 · [OCR] Duplicate section numbers in both contents tables.** Unit 1 lists `1.2`, `1.8` and `1.9` twice each — the extraction re-emitted a header when a heading reappeared later. §8 preserves the duplicates so every row maps to a real page range, but the numbering itself is not a reliable index.

**Deliberately not written up.** U1 p87 (handheld devices) and U2 p129 (Volatility macOS profiles) touch mobile and macOS forensics — out of scope for this diploma, skipped rather than summarised. Linux appears only as a *host* for tools used against Windows evidence (`dd`, `sha512sum`, `mount`, `bulk_extractor`, Volatility on Kali), which is in scope and is covered. The presentation phase `[U1 p58–61]` is left to the reporting module.

## 8 · Section index → source pages

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `1.1` | Introduction | 4–10 | §0 (course framing) |
| `1.2` | Background | 11–14 | §1 Digital forensics |
| `1.2.1` | Background: Digital Forensics Uses | 15–17 | §1 Digital forensics |
| `1.2` | Background *(repeat)* | 18–22 | §1 Digital forensics |
| `1.3` | Fundamentals | 23–24 | §1 Digital evidence and its life cycle |
| `1.3.1` | Fundamentals: Digital Evidence | 25–28 | §1 Digital evidence and its life cycle |
| `1.3.2` | Fundamentals: Digital Forensics Tools | 29–31 | §1 Abstraction layer · §3 |
| `1.3.3` | Fundamentals: Scientific Method | 32–36 | §1 Forensic soundness · §1 Inculpatory/exculpatory · §4 |
| `1.4` | Digital Evidence | 37–37 | — divider slide |
| `1.4.1` | Digital Evidence Life Cycle | 38–38 | §1 Digital evidence and its life cycle |
| `1.4.1.1` | Digital Evidence Life Cycle: Acquisition | 39–52 | §1 life cycle · §2 Chain of custody form |
| `1.4.1.2` | Digital Evidence Life Cycle: Analysis | 53–57 | §1 Forensic soundness · §1 Inculpatory/exculpatory |
| `1.4.1.3` | Digital Evidence Life Cycle: Presentation | 58–61 | — reporting module |
| `1.4.2` | Types & Sources of Digital Evidence | 62–64 | §1 Digital evidence and its life cycle |
| `1.4.2.1` | Active Data | 65–65 | §1 Digital evidence · §5 |
| `1.4.2.2` | Archive and Backup | 66–66 | §1 Digital evidence · §5 |
| `1.4.2.3` | Hidden Data Types | 67–80 | §1 Volatility and order of volatility · §5 (metadata / residual / replicant) |
| `1.4.2.5` | Devices | 81–97 | §1 Admissibility · §5 — handhelds skipped, §7 |
| `1.5` | Analysis Steps | 98–119 | §1 Forensic soundness · §1 Commingling · §2 Write blocker · §5 |
| `1.6` | Investigation Scope | 120–127 | §5 (investigation types) · §7 G21 (p126 lost) |
| `1.7` | Crime Reconstruction | 128–134 | §5 (relational / functional / temporal / same-origin) |
| `1.8` | Challenges of Digital Evidence | 135–150 | §1 Admissibility · §5 · §7 |
| `1.9` | Major Concepts | 151–177 | §1 Commingling · §1 Abstraction layer · §1 Admissibility · §1 Chain of custody |
| `1.8` | Challenges of Digital Evidence *(repeat)* | 178–178 | §1 Abstraction layer |
| `1.9` | Major Concepts *(repeat)* | 179–193 | §1 Abstraction layer · §6 |
| `2.1` | Introduction | 3–12 | §0 · §1 Imaging vs copying · §1 Volatility |
| `2.1.1` | Order of Volatility | 13–15 | §1 Volatility and the order of volatility · §7 G1 |
| `2.1.2` | Types of Data Acquisition | 16–21 | §1 Static, dynamic, dead and live acquisition |
| `2.2` | Storage Formats | 22–39 | §2 Raw/dd image · §2 E01 · §1 Imaging vs copying · §5 (AFF, sgzip, ILook) |
| `2.3` | Acquisition Methods | 40–55 | §1 Imaging vs copying · §2 Targeted (sparse) triage set · §5 |
| `2.4` | Live Data Acquisition | 56–76 | §2 Memory image · §2 Live Response Collection output tree |
| `2.5` | Tools | 77–77 | — divider slide |
| `2.5.1` | Write Blockers | 78–82 | §1 Write blocking · §2 Write blocker and its proof trail |
| `2.5.2` | Bootable Disks | 83–83 | §1 Static/dynamic/dead acquisition · §3 |
| `2.5.3` | Non-Writable USB | 84–90 | §2 StorageDevicePolicies WriteProtect |
| `2.5.4` | FTK Imager | 91–115 | §2 FTK Imager acquisition & verification log · §3 |
| `2.5.5` | Live Response Tools | 116–125 | §2 Live Response Collection output tree · §3 |
| `2.5.6` | Memory Forensic Tools | 126–133 | §2 Memory image · §3 Volatility |
| `2.5.7` | Other Forensic Tools | 134–139 | §2 bulk_extractor feature files |
| `2.6` | Validating Evidence | 140–158 | §1 Cryptographic hashing · §2 Acquisition hash set · §4 |
| `2.7` | Exploring Evidence | 159–172 | §3 image mounters · §1 Abstraction layer |
| `2.8` | Miscellaneous | 173–185 | §2 Acquisition timestamp and time-zone record |
