# evidence_sets.md — eCDFP Diploma

**Owned by `ecdfp-evidence`.** No other skill assigns an `EVS-` ID or marks a set verified.
Part 8 step 0: **a session whose evidence set is not verified and hashed does not start.**

**`R9` — the repo carries the manifest, never the bytes.** No image, dump, hive or raw pcap is
committed. Generators write outside the project tree; the mount cannot delete (Part 10), so a
stray file inside it is permanent.

---

## Sourcing tiers

| Tier | What | Rule |
|:-:|---|---|
| **1** | Our own lab acquisitions | primary. One `EVI-SRC01` image feeds S2–S6 at increasing depth (`D19`) |
| **2** | Public corpora — NIST CFReDS, Digital Corpora, published challenges | **linked and credited, never rehosted** (`D22`). Licence checked before use |
| **3** | Synthesized | narrow: pcap, syslog/NDJSON/web logs, artifact **exports** (CSV/JSON). 🔴 **Never** `.evtx`, E01/AD1/raw, memory dump or registry hive — a fabricated hive is a lie about what a forensic artifact looks like |

---

## The sets

### `EVS-01` — Session 1 · the manifest set

| Field | Value |
|---|---|
| **Name** | EVS-01 — Case 01 seizure package |
| **Tier** | **1** — generated in our own lab |
| **Source** | `scripts/make_evs01.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no third-party material, no external corpus |
| **Format** | 4 × UTF-8 plain text (LF), 2 × checksum manifest |
| **Size** | 6 144 B total · 587–2 303 B per file |
| **Contains** | a first responder's contemporaneous notes · an imaging tool's acquisition and verification log · a completed chain-of-custody record · a three-row exhibit inventory |
| **Session** | S1 (`S1-06`, `S1-07`, `S1-09`, `S1-10`) |
| **Date verified** | **2026-08-30** — hashes computed from the generated files, not copied from anywhere |

**🔴 One file is deliberately altered after the manifest is computed.** That is the exercise.

**Published for download (`D67`).** The set is served from `docs/session-01/` — `EVS-01.zip`
(all six files) and the loose folder `EVS-01/`. `R9` still holds: its prohibition is on evidence
**bytes** — images, memory dumps, hives, raw pcaps — and this is 6 144 B of UTF-8 text we authored
ourselves, with no personal data, no credential and no IP address. It was already fully derivable
from the public repo, since `scripts/make_evs01.py` is committed and deterministic. Publishing it
is what makes `D18` achievable: students verify before class.

| # | File | Bytes | State as distributed |
|--:|---|--:|---|
| 1 | `seizure_notes.txt` | 2 303 | clean |
| 2 | `EVI-SRC01_acquisition_log.txt` | 1 340 | 🔴 **altered — one character** |
| 3 | `custody_form_EVI-SRC01.txt` | 1 914 | clean |
| 4 | `evidence_inventory.csv` | 587 | clean |

**The alteration:** `Acquisition started : 2026-03-04 09:14:0` **`2`** ` UTC` → `…09:14:0` **`3`** ` UTC`.
One character. Invisible to the eye, total to the digest.

**Why that file.** It is the file whose *content is the integrity claim* — the one containing the
word `verified`. The catch lands exactly where students reliably fail: *"verified" means the tool
checked its own output.*

#### Manifest — SHA-256 (the values students verify against)

```
ee62e8b1396c7c3d4d3349817dc02cc67fc9fe733eba522090e300665c7a81a1  seizure_notes.txt
f05bfee856c578d50af2302f0bd09f4260e8f8b7617f9162340458cb457171d7  EVI-SRC01_acquisition_log.txt
bb8ea1983fa7a64e738ba7f52fdd905467e0a9db3a0abd1acc0d3746bfcc0adc  custody_form_EVI-SRC01.txt
acc6c87547f0661f739670ef35dd2cfee5290ff4457c3b3d2119b209eb9a29ee  evidence_inventory.csv
```

#### Manifest — MD5 (recorded as a lookup key, never as the integrity control)

```
5127e6d1609da0e140d9483d2198852e  seizure_notes.txt
c9dfb4b8c20095c9f739359b43812515  EVI-SRC01_acquisition_log.txt
a3f69f666078c94d84351ee656e42001  custody_form_EVI-SRC01.txt
11a85407fa5b9cdd2950b1ae71e55838  evidence_inventory.csv
```

#### 🔴 Answer key — instructor only

The digest the **distributed** (altered) file actually computes to:

| Algorithm | Value |
|---|---|
| SHA-256 | `7eda34b36f53700bb3e0c4cd85c6c026b4c67982d7f7c2375fa8540af4bfb3c6` |
| MD5 | `2f3858969b36fc4f06efad19a5e973b1` |

A correct `F-01` quotes **that** value against the manifest's
`f05bfee8…`, names both, and stops there.

#### Verified by running it

```
$ sha256sum -c EVS-01.sha256
seizure_notes.txt: OK
EVI-SRC01_acquisition_log.txt: FAILED
custody_form_EVI-SRC01.txt: OK
evidence_inventory.csv: OK
sha256sum: WARNING: 1 computed checksum did NOT match
```

`md5sum -c EVS-01.md5` gives the same three OK and the same one FAILED.
Regenerated to a second path and diffed: **byte-identical** — the generator is deterministic
(fixed seed `20260304`, fixed base date `2026-03-04`), so a student's copy is diffable against
the instructor's.

#### What it deliberately does not contain

No real personal data · no real company · no real malware · no credential of any kind · no IP
address at all. The narrative carries the case without any of it, which is what `D41` requires:
**no question in this set has a secret or a person's data as its answer.**

#### Distribution

Published by the end of the session before (`D18`) with **both** hashes. Students verify before
class; a mismatch is a finding, not an inconvenience. The instructor holds a prepared fallback
USB set, re-verified before each session that needs it.

Regenerate with:

```
python3 scripts/make_evs01.py --out <a path OUTSIDE the repo>/EVS-01
```

---

### `EVS-05` — Sessions 1, 2 and 3 · the file-type identification set

| Field | Value |
|---|---|
| **Name** | EVS-05 — 12 files whose extensions are unreliable |
| **Tier** | **3 — synthesized.** Every file is one we author. The Tier 3 bar forbids fabricating `.evtx`, E01/AD1/raw, memory dumps and registry hives; it does not forbid making a PNG |
| **Source** | `scripts/make_evs05.py` in this repository |
| **Publisher** | ITGate Academy · **Licence** ours, no third-party material |
| **Format** | 12 files (PDF, PNG, JPEG, ZIP, text) + 2 checksum manifests |
| **Size** | 12 892 B total · 86–3 619 B per file |
| **Session** | **S1-09** (first four bytes of four files) · **S2-06** (signature sweep across the set) · **S3-07** (Case 03, with `EVS-10`) |
| **Date verified** | **2026-09-06** — hashes computed from the generated files |

**Five of the twelve lie about themselves, and two are damaged rather than misnamed.**

| File | Claims | Actually is | First 4 bytes | |
|---|---|---|---|---|
| `q3_summary.pdf` | PDF | PDF | `25 50 44 46` | honest |
| `floorplan.png` | PNG | PNG | `89 50 4E 47` | honest |
| `badge_photo.jpg` | JPEG | JPEG | `FF D8 FF E0` | honest |
| `archive_2026.zip` | ZIP | ZIP | `50 4B 03 04` | honest |
| `readme.txt` | text | text | `4D 65 72 69` | honest |
| `invoice_scan.jpg` | JPEG | **PDF** | `25 50 44 46` | 🔴 mismatch |
| `meeting_notes.txt` | text | **PNG** | `89 50 4E 47` | 🔴 mismatch |
| `holiday_snap.jpg` | JPEG | **ZIP** | `50 4B 03 04` | 🔴 mismatch |
| `policy_v2.docx` | ZIP *(a .docx **is** a ZIP)* | **PNG** | `89 50 4E 47` | 🔴 mismatch — the subtle one |
| `thumbnail.png` | PNG | **JPEG** | `FF D8 FF E0` | 🔴 mismatch |
| `scan_partial.png` | PNG | PNG, **truncated** | `89 50 4E 47` | ⚠️ valid header, damaged body |
| `export_partial.jpg` | JPEG | JPEG, **truncated** | `FF D8 FF E0` | ⚠️ valid header, damaged body |

🟢 **Why `policy_v2.docx` is the best file in the set.** A student who has learned *"`.docx` is really a
ZIP"* will predict `50 4B 03 04` and be **wrong** — it is a PNG. It punishes pattern-matching and
rewards actually looking. 🟢 **Why the two truncated files matter:** a valid signature does **not** mean a
valid file. Header and integrity are different questions — which is the bridge back to `S1-06` hashing.

#### Manifest — SHA-256

```
808b8e51cae87e089b1384f73dfe242ca6d68088fe48ea77bfdde73b11f3dcc0  q3_summary.pdf
dd0e0d61efc3107c035601d78caa07efe4e261b26798be3cf27e85f00a515c9a  floorplan.png
3e3078e3230a105a4cdd99e36aeae6b4f434d5bccd177bcbe9d1ae7b4277dd6b  badge_photo.jpg
34f72cf0712365111e1ca6034f1a175d0eedde3cfbfc028f9536634b7a920095  archive_2026.zip
6b63a2effa2ec28c39c45acb44774ace3be7a687d44f659a0e356e9c8c935e8c  readme.txt
bed0aab08a4026982c5908f93f5cf467c6bb6da55262753a17c03d8259912acf  invoice_scan.jpg
e4f254168d3eee40ebdf3f4ee474563849cd11a85f28943f88ddd69219259ca9  meeting_notes.txt
64403d5cea26afc49f05edd81c9df3a5754173cdc6e280e7d3f2654d61ffbf8c  holiday_snap.jpg
607bf4f5ba089155a8777c515e00902630d405cacb252578852c292beaa7b9eb  policy_v2.docx
18cb3f8719a9b8022288774f1b13c07f1ca81a3b89d165efc2bbf5758141800f  thumbnail.png
93fe41bc71eb0353f0a33cc9841b4ed346c088b0bb9197023490130c53c19c77  scan_partial.png
ee0032d6ef9b3c04f71d2fec22aaa1d840506314241940034e91f4948505a6db  export_partial.jpg
```

#### Manifest — MD5 (lookup key, never the integrity control)

```
622402255b7877af1ede99b7dfe83052  q3_summary.pdf
957ee0bd5c1bfbbf78beb73cb36dc122  floorplan.png
70430b37281eba7b5a5770f6dae1ac15  badge_photo.jpg
f53ff2c999346ceac4d4c121ff7f01fd  archive_2026.zip
b68ebd52f6f619d0f0a5421de7bbc7e3  readme.txt
ce28ad489ad7302185f6d117bff9c127  invoice_scan.jpg
3c7d7f4eeb5f66dfac26b966f0ba3aaf  meeting_notes.txt
57d3dfbdc789dee8799628769ce7cd65  holiday_snap.jpg
d62638fe9ed7cb8950d63a582e9a6799  policy_v2.docx
d67bfa6c87c3201b365a5f380b00bb9b  thumbnail.png
0e074d60e86aa124e6fae82840b37288  scan_partial.png
48018c7ebad3c77617c89916d0ffeea0  export_partial.jpg
```

#### Verified by running it

Regenerated to a second path and diffed: **byte-identical**. A signature sniffer run across the set
finds **exactly 5** extension mismatches, which is the number the lab answer key states. Fictional
content throughout: no personal data, no credential, **no IP address at all** (`D41`, `R8`).

⚠️ **`R9`** — the bytes are never committed. Regenerate with
`python3 scripts/make_evs05.py --out <a path OUTSIDE the repo>/EVS-05`. Requires `Pillow`.

---

### `EVS-10` — Session 3 · the hidden-information image set

| Field | Value |
|---|---|
| **Name** | EVS-10 — hidden-information image set |
| **Tier** | **3 — synthesized, and legitimately so.** These are **images we author**, not forensic containers. The Tier 3 bar forbids fabricating `.evtx`, E01/AD1/raw images, memory dumps and registry hives. It does not forbid making a JPEG — and data hidden *inside* an image we made is ours to hide |
| **Source** | `scripts/make_evs10.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no third-party image, no external corpus, no photograph of any real person or place |
| **Format** | 5 × JPEG/PNG + 2 renamed files + 2 checksum manifests |
| **Size** | 46 402 B total · 156–14 070 B per file |
| **Contains** | EXIF with GPS and three disagreeing timestamps · an LSB-hidden message **and its clean twin** · a JPEG/ZIP polyglot · a PNG named `.txt` · a ZIP named `.jpg` · a JPEG whose EXIF thumbnail outlived a redaction |
| **Session** | S3 (`S3-02`, `S3-03`, `S3-04`, `S3-06`, `S3-07`) |
| **Date verified** | **2026-09-06** — hashes computed from the generated files on two independent machines |

| # | File | Bytes | The lesson it carries |
|--:|---|--:|---|
| 1 | `office_floor3.jpg` | 13 786 | EXIF GPS + `DateTimeOriginal` 2026:08:24 ≠ `DateTime` 2026:08:31 ≠ file mtime 2026:09:02 |
| 2 | `receipt_scan.png` | 3 231 | 🔴 LSB payload in the blue channel |
| 3 | `receipt_scan_clean.png` | 2 970 | the same image **without** the payload — diff the two and see the noise |
| 4 | `team_photo.jpg` | 10 476 | valid JPEG **and** a valid ZIP — a polyglot |
| 5 | `meeting_notes.txt` | 1 713 | is really a **PNG** (`89 50 4E 47`) |
| 6 | `holiday_snap.jpg` | 156 | is really a **ZIP** (`50 4B 03 04`) |
| 7 | `invoice_batch.jpg` | 14 070 | the main image is redacted; **the EXIF thumbnail is not** |

#### Manifest — SHA-256

```
f9c69b07a3804b1ca870c373ab5c964db05672a993b3ff019836f81c43599a93  office_floor3.jpg
15d27119ff885ffce0eb07889165f53442f2cbf0d61f561d254d6460fdbfc7ff  receipt_scan.png
6277f5c5a34faefc6690d08442bc4773fe3c4781ce6df2f073d5587c0079c353  receipt_scan_clean.png
bd26ba28f5cb5b498d1869f08206c1a1a30b685f45825a911ef5bf056e25db9e  team_photo.jpg
07c414f459558025685334122707263d02c1aa5c7c8658eeafd063e0c51e14dd  meeting_notes.txt
c6c6895ba546685c32af6c064d7beb01ced7ffbb2465bbbb65ede3d1cd443579  holiday_snap.jpg
3e932d688a069b780f6ed6f1fa8d27bc2d4563927eb1dcfcb6015078b693fc0e  invoice_batch.jpg
```

#### Manifest — MD5 (lookup key, never the integrity control)

```
2409f222904e27c918c9743e5154397d  office_floor3.jpg
e98d3f23d7d05f76b34b6325549f2d23  receipt_scan.png
1b56df2955e64dd2b627a735e22016b4  receipt_scan_clean.png
de223da408450e69b0be278a7897a5d8  team_photo.jpg
eb842c4423ea7375eb294d007302eea6  meeting_notes.txt
8c9ea6aa3ad1e62ed100157fa974845f  holiday_snap.jpg
613d1b9fc0bd1a7dbc7e6fe2497a39cf  invoice_batch.jpg
```

#### Verified by running it — and by proving each lesson lands

Not "the generator said so". Every claim above was asserted against the produced files:
EXIF GPS present and the three timestamps genuinely differ · the LSB message decodes to
`MRG-INTERNAL: staged archive is customer_export.7z` and the clean twin decodes to nothing ·
`team_photo.jpg` opens as an image **and** `zipfile` lists `handover.txt` in it ·
the two renamed files carry PNG and ZIP magic bytes · and the EXIF thumbnail differs from the
main image across **290 of 290** sampled pixels in the redacted region. **13 of 13 assertions passed.**

**Determinism proved twice:** regenerated to a second path and diffed byte-for-byte, then regenerated
**on a different machine** (the lab VM) — all 7 SHA-256 values identical. A student's copy is
diffable against the instructor's.

⚠️ **`R9` — the bytes are never committed.** The repo carries this manifest and
`scripts/make_evs10.py`. Regenerate with:

```
python3 scripts/make_evs10.py --out <a path OUTSIDE the repo>/EVS-10
```

Requires `Pillow` and `piexif`.

#### What it deliberately does not contain

No real personal data · no real company · no real photograph of anyone · no malware · no credential ·
no IP address at all. The LSB payload is a fictional internal note, so **no question in this set has a
secret or a person's data as its answer** (`D41`).

### `EVS-07` — Page 8 · the storage and partitioning set

| Field | Value |
|---|---|
| **Name** | EVS-07 — storage internals, MBR and GPT |
| **Tier** | **1 — built in our own lab.** Four disk images we author. No third-party image, no corpus, no acquisition from a real machine — so nothing here is a fabricated forensic container in the sense `R9` forbids: these **are** disks, made by `mkfs` and by hand, not synthesized artifacts pretending to be acquisitions |
| **Source** | `scripts/make_evs07.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no third-party material, no real data, no real person |
| **Format** | 4 × raw `dd` image |
| **Size** | 222 298 112 B total · 20 MiB (slack) + 3 × 64 MiB |
| **Contains** | a FAT16 volume with 4 096-byte clusters and five files whose slack is exact · a deleted document surviving in the slack of an unrelated 20-byte memo · an MBR partition table written byte by byte · a GPT disk with both headers and a valid CRC32 pair · the same MBR disk with LBA 0 zeroed and nothing else touched |
| **Page** | `P08` (`T12`, `T13`) |
| **Date verified** | **2026-09-09** — 37 assertions run against the produced images, not against the generator's intentions |

| # | File | Bytes | The lesson it carries |
|--:|---|--:|---|
| 1 | `EVS-07-slack.dd` | 20 971 520 | one visible file of 20 B, and **4 076 B of a deleted document** in the same cluster |
| 2 | `EVS-07-mbr.dd` | 67 108 864 | a real partition table: 🔴 disk signature `C4 19 7F A3`, two entries, two empty, `55 AA` |
| 3 | `EVS-07-gpt.dd` | 67 108 864 | protective MBR `0xEE`, `EFI PART` at LBA 1, 128 × 128 entry array, backup header at LBA 131 071 |
| 4 | `EVS-07-wiped.dd` | 67 108 864 | 🔴 **Case 04** — image 2 with 512 bytes zeroed. 0.0008% of the disk, and it will not mount |

#### Manifest — SHA-256

```
c5c357c7eb8758ff001d4e3df8c032c287799e48f8a19b41e6d7d0f692c23669  EVS-07-gpt.dd
fbe6fba24599776829b158a4ace6c63b842e93ad377ed96638bd3d00b6534faa  EVS-07-mbr.dd
c71eb7bb82dc60b425554db05184951d2b5973c6f9c5f66e79e2f029719b1e73  EVS-07-slack.dd
2f4fc7aa77c18b5767d24cc6ce191e09c48c1014c2fdd91578df2d0500842f8b  EVS-07-wiped.dd
```

#### Manifest — MD5 (lookup key, never the integrity control)

```
d18421a8bd7168c17d258bfea1e50612  EVS-07-gpt.dd
03a3a56695ec58e766734f6a2c6b2578  EVS-07-mbr.dd
04061c502bc3534e9ca20eb14c679194  EVS-07-slack.dd
2537fda6d93e39acfec954eabf9caf16  EVS-07-wiped.dd
```

#### Verified by reading the images back — 37 of 37 assertions passed

Not "the generator said so". Every number that reaches a student was read out of the produced
bytes: cluster size **4 096** from the BPB · five files at **1 / 100 / 4 096 / 4 097 / 10 000 B**
giving slack of **4 095 / 3 996 / 0 / 4 095 / 2 288** · **18 294 B of files occupying 32 768 B**,
so **14 474 B of slack** on a volume with five files on it · `MEMO.TXT` 20 B in cluster 10 at
offset **0x13000** with **4 076 B** of a deleted document behind it · both MBR entries decoded to
type / start / count · the GPT header and array **CRC32 recomputed and matched** · the backup
header found at LBA **131 071** · and, for Case 04, **three** boot-sector candidates found,
`BPB_BkBootSec` = **6** discarding LBA 45 062, and the recovered 64-byte table **byte-identical**
to the original (`e541ef6f624eb09775c4b21f70bc08e85188d26788febf4ffd9e2c758cde5cab`).

#### Determinism — and what it cost

`mkfs.fat` takes the FAT volume serial from the clock, `mcopy` stamps directory entries with the
current time unless told otherwise, FAT stores **local** time so the timezone is part of the
output, `mkfs.fat` also stamps the **volume-label** directory entry, and `sgdisk` invents three
random GUIDs that both CRC32 fields then cover. All five are pinned in the generator — the last
one by parsing the BPB to find the label entry, which is the same walk the students do by hand.
Two builds to different paths are now **byte-identical across all four images**; before the fix
they differed in as little as **two bytes**, which is exactly the amount that makes a manifest a
lie.

⚠️ **Second-machine check is deferred.** `mtools` is not installable on the second host available
here, so determinism is proved by two independent builds on one machine, not two. Toolchain used:
`dosfstools 4.2`, `mtools 4.0.43`, `sgdisk 1.0.10`, `python 3.11`. A different major version of
any of these may move the bytes — that is a property of the tools, not of the method, and it is
why the manifest names them.

⚠️ **`R9` — the bytes are never committed.** The repo carries this manifest and
`scripts/make_evs07.py`. Regenerate with:

```
python3 scripts/make_evs07.py --out <a path OUTSIDE the repo>/EVS-07
```

Requires `dosfstools`, `mtools` and `gdisk`.

#### What it deliberately does not contain

No real personal data · no real company · no malware · no credential · no IP address. The document
recovered from slack is a fictional internal note, so **no question in this set has a secret or a
person's data as its answer** (`D41`).

---

### `EVS-11` — Page 9 · the file-system and carving set

| Field | Value |
|---|---|
| **Name** | EVS-11 — FAT, NTFS and a volume with no file system |
| **Tier** | **1 — built in our own lab.** Three disk images we author with `mkfs`, `mkntfs` and, where the tools could not be made to cooperate, by hand. Nothing is downloaded and nothing is a synthesized *artifact* pretending to be an acquisition |
| **Source** | `scripts/make_evs11.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no third-party material, no real data, no real person |
| **Format** | 3 × raw `dd` image + 1 rendered PNG |
| **Size** | 150 994 944 B total · 64 MiB + 2 × 40 MiB |
| **Contains** | an NTFS volume with a resident file, a non-resident file, an alternate data stream, and a **deleted file whose content is still in its MFT record** · a FAT32 volume with a **deliberately fragmented** file and a deleted entry that keeps its size and first cluster · the same FAT volume with its metadata zeroed |
| **Page** | `P09` (`T14`, `T15`) |
| **Date verified** | **2026-09-09** — 49 assertions run against the produced images |

| # | File | Bytes | The lesson it carries |
|--:|---|--:|---|
| 1 | `EVS-11-ntfs.dd` | 67 108 864 | resident vs non-resident `$DATA` · a second `$DATA:notes` stream · 🔴 **record 67, deleted, 212 bytes of content still readable** |
| 2 | `EVS-11-fat.dd` | 41 943 040 | a directory entry, a cluster chain, 🔴 **a file in two runs with someone else's data between them**, and a `0xE5` entry that keeps its size and first cluster |
| 3 | `EVS-11-carve.dd` | 41 943 040 | 🔴 **Case 05** — image 2 with 0.2051% zeroed. No file system, and every byte of every file still present |
| 4 | `carve_compare.png` | — | the fragmented photograph as the carver returns it, beside the original |

#### Manifest — SHA-256

```
8d5d754731e7d5b015f79cb33fa43abfdef3d07ce95f1f0693b31909a8ee3ef6  EVS-11-carve.dd
b17f87c2ce248340955836bc95c43b8e17f3dfd3f454716465fb5b8bca22f343  EVS-11-fat.dd
```

*(the two byte-reproducible images; see below for why the NTFS image has no stable file hash)*

#### The stable fingerprint — what a student actually checks

```
dc3e48e093b8d565ca87116846bd7ce807235c8b036e1f3dbf3c857f434d69bd  EVS-11-ntfs.dd:MFT#64
0c958d614d3a5bdd9958bf535dd5287a11bcc1864bdd3a2a5347ee7071210a79  EVS-11-ntfs.dd:MFT#65
9fffdd4f00822bd1ed500b1622779a05dfefed6097830835747a57db9ce4652e  EVS-11-ntfs.dd:MFT#66
10166762987252d9f6f2161a543476c3ce86f020474309e63a262af49d382f34  EVS-11-ntfs.dd:MFT#67
e279697e1e744f1db862a7415f6339cb9eb15601f91c7f50fd46d69dd3131a93  carve_compare.png:PIXELS
```

#### Verified by reading the images back — 49 of 49 assertions passed

**NTFS.** Record size **1 024 B**, `$MFT` at LCN 4 · record 64 `notes.txt` **290 B resident**, using 672 of
its 1 024 bytes and occupying **no cluster anywhere** · record 65 `report.bin` **204 800 B non-resident** ·
record 66 `budget.csv` carrying **two** `$DATA` attributes, **34 B unnamed and 41 B named `notes`** · record
67 `old_plan.txt` with **flags 0x00, link count 0, sequence 2** — deleted — and its **212 bytes still
readable at offset `0x14D78`**.

**FAT.** Cluster **4 096 B**, data area at `0x18000` · six live files and one `0xE5` entry that still records
**`LD_IN~1PDF`, 1 583 bytes, first cluster 19**, with that cluster marked free in the FAT and still beginning
`25 50 44 46` · `whiteboard.jpg` in **two runs, (20, 9) and (38, 10)**, with nine clusters of `logs.txt`
between them, reassembling from the chain to the original hash.

**Carving.** 86 016 of 41 943 040 bytes zeroed = **0.2051%**, data area byte-identical · **six** objects
carved from **five** files: three **exact**, two PDFs **one byte short** (`%%EOF` versus `%%EOF\n`), and the
fragmented photograph at **112 253 bytes instead of 75 389** — exactly **+36 864**, nine clusters of the log
file — which **still opens as an 800×500 JPEG**. One of the six was **deleted before the wipe**, and the
carver found it because it never asked the file system.

#### Determinism — and one image that honestly cannot have it

The FAT and carve images are **byte-identical across builds**. Getting there meant pinning the FAT volume
serial, `mcopy`'s timestamps, the timezone, the volume-label entry (`D133`), **and** two payload formats that
carry their own clocks: a ZIP stores a timestamp per member, and reportlab writes `/CreationDate` and a
document ID into every PDF.

**The NTFS image is not reproducible, and the manifest says so instead of pretending.** `mkntfs` writes a
`$LogFile`, an `$MFTMirr` and index entries that all carry timestamps; **344 bytes of 67 108 864 differ
between two builds.** Pinning them would mean forging a journal that does not correspond to what happened —
a worse thing to hand a forensics student than an unstable hash. So the manifest carries the **four MFT
records the page actually reads**, which are byte-identical across builds, and those are what a student
verifies.

Toolchain: `dosfstools 4.2`, `mtools 4.0.43`, `ntfs-3g 2022.10.3`, `Pillow`, `reportlab`, `python 3.11`.

⚠️ **`R9` — the bytes are never committed.** The repo carries this manifest and `scripts/make_evs11.py`.
Regenerate with:

```
python3 scripts/make_evs11.py --out <a path OUTSIDE the repo>/EVS-11
```

Requires `dosfstools`, `mtools`, `ntfs-3g` (with FUSE available for the one mount it performs), `Pillow` and
`reportlab`.

#### What it deliberately does not contain

No real personal data · no real company · no malware · no credential · no IP address that resolves anywhere.
The deleted documents are a fictional draft plan and a fictional withdrawn invoice, so **no question in this
set has a secret or a person's data as its answer** (`D41`).

---

### `EVS-12` · `EVS-13` · `EVS-14` — Pages 10–12 · the published Windows artifact corpora

**Tier 2 — published corpora, linked and credited, never rehosted (`D22`, `R9`).** All three are fetched by
one script, `scripts/fetch_corpora.py`, which clones each source **at a pinned commit** (so upstream cannot
move under us), copies the exact files the pages use, and **refuses to finish unless every SHA-256 below
matches**. The repo carries this manifest; the bytes stay outside it.

| Set | Page | Source, licence, commit | Files |
|---|---|---|---|
| `EVS-12` | `P10` | Eric Zimmerman, `Registry` test hives — MIT — `1b0b3c41` | `SYSTEM` · `SOFTWARE` · `SAM` · `SECURITY` · `NTUSER.DAT` |
| `EVS-13` | `P11` | Eric Zimmerman, `Registry` · `Prefetch` · `Lnk` · `JumpList` · `RBCmd` · `AppCompatCacheParser` test files — MIT — `1b0b3c41` · `27d87a09` · `918bea4a` · `e87bacd4` · `756498f9` · `0cf059f4` | `UsrClass.dat` · `UsrClassDeletedBags.dat` · 3 × `.pf` · 1 × `.lnk` · 1 × `.automaticDestinations-ms` · 2 × `$I` · `AppCompatCache-Win10.bin` |
| `EVS-14` | `P12` | Samir Bousseaden, `EVTX-ATTACK-SAMPLES` — GPL-3.0 — `4ceed2f4` | 6 × `.evtx` |

#### `EVS-12` manifest — SHA-256

```
ec01a4ec205c5354a4ad1d5d088f45e2331ffb13773dcc7008e6ea6f2175466f  SYSTEM
658c4323cc2c4e33e09ef3e5251651300ff1a49937e136242565cc5c49fd5e96  SOFTWARE
8aea3c9217bfe1ecc39df535c25a02d5dfb76d0427298898a370a086c10f72aa  SAM
4a427cfa5a9de9075b38a71717bbe9f303ed3cd458015cc4d39a58f47589a567  SECURITY
8d5fdee75d69b878a0bf602f7a15f0410c5622b9c8c84a5c2f346d44a8cdb759  NTUSER.DAT
```

#### `EVS-13` manifest — SHA-256

```
6dbfecef68d01ddaedaec98b9142e3c17ae9d4a6ec98456680f0c9a74a054a07  UsrClass.dat
8a649ddeff18e1d4b2f913794ab006c7d2d4e8c702bf32a545e3484324cf9abc  UsrClassDeletedBags.dat
0ef6ce683365dac64191608b47a74665ddec28eaae530ce2622900130c404077  CMD.EXE-D269B812.pf
52543b5a85b9ee1936e048dc7f7fab6ffaa18834f5db68ee87926e38e84b8e13  CHROME.EXE-B3BA7868.pf
e1d11876560511788c58e957d302a4a953e8cd8e8d7c0290796393058c164319  CALC.EXE-3FBEF7FD.pf
744a78dc8ea8ca49edf45e2a8536447918663fbc718469a9b938f05c9be6bc3c  Files Copied.txt.lnk
a724713d2ff51d32e3f028c57ab906339f882de0c93dc9903f0f8b241c53fd56  f01b4d95cf55d32a.automaticDestinations-ms
d2966f4c3de5968bffb5cdaacf75857cd34357f00c86def6fdcff67fe31d9af8  $I2JRX90
6a49ebf257e3bf193eeeb021c1bfda524594b50e71615d71711f6f588a891420  $IFATB0K
6f175c17506bd1ae94683b791b2151a6b8266196d33db2ad4971c09287c632fa  AppCompatCache-Win10.bin
```

#### `EVS-14` manifest — SHA-256

```
a0615707b547a2ac254688fd725c3c590f62440fc9b7947c2843dd40498a39e8  DE_1102_security_log_cleared.evtx
5579cdca073ee4864ea82d656aa2d25400b5c1e85b8e688db5d85f6dc558c2af  DE_104_system_log_cleared.evtx
75f199b68d473172705bf874720b01820317fdd7aa4843545c98720dd6de197f  CA_4624_4625_LogonType2.evtx
bbfd87cacdd56a9135de1838666937cd6c74daba47b366bba0c11f95ce97f461  LM_4624_pth_source.evtx
b8df8232d917fed223e2bf9abebb249489f84c6204c40b72dab6a74157d6f8bd  persist_run_key_sysmon_13.evtx
9619b9d9d7bb8a277080167ff639fd9162e3d88d61d674cf1606beadce17ea5a  guest_added_to_admins_4732.evtx
```

Every hash above was **copied from the fetcher's output**, not typed (`D135`).

#### `EVS-12` — verified by reading the hives back, 39 of 39 assertions

`regf` header: sequence **20610 / 20609**, root cell at **0x20** (file offset 0x1020), data size 10 473 472,
**XOR-32 checksum 0xF76F4711 recomputed and matching** · `Select\Current` = 1 · ComputerName **HAXOR4** ·
Mountain Standard Time, bias 420 · `SOFTWARE`: Windows 7 Professional build 7601, installed
**2013-10-10 01:33:45**, profile `C:\Users\Win7SP1` · `SAM`: RIDs 500 and 501 only, both never logged in ·
`USBSTOR`: **9 devices**; the ADATA drive `2361808400440061&0` → `VID_125F&PID_DE7A` → `\DosDevices\J:` →
volume `{3aa3a4a9-087f-11e4-825d-ac220b2a5a56}` → present in `NTUSER.DAT` `MountPoints2`, last written
**2014-10-14 20:39:34** · its four device timestamps: `0064` **2015-02-23 17:31:31**, `0066` **2015-02-24
03:23:35**, no `0067`; the Mushkin's `0067` is **2015-02-23 17:31:21**, ten seconds earlier · the ADATA volume
GUID is UUIDv1, minted **2014-07-10 22:12:06**, node `ac220b2a5a56` · **43 of 52** `MountPoints2` GUIDs also
appear in `SYSTEM`'s `MountedDevices`, which is the proof those two hives share a machine.

⚠️ **The corpus is not one case.** `SYSTEM` + `NTUSER.DAT` are from one machine (HAXOR4); `SOFTWARE` and
`SAM` are from a clean Win7 SP1 VM. `P10` says so on the screen where it matters, and turns it into the
question *do the hives I was handed come from the same machine?*

⚠️ **`NTUSER.DAT` is the author's real profile, published by him for this purpose.** The pages use only its
device keys (`MountPoints2`) and counts; nothing that describes the person — `Run` entries, `RecentDocs`,
`TypedPaths` — is displayed.

#### What they deliberately do not contain

Nothing fabricated: no synthesized hive, `.evtx`, prefetch or LNK (Tier 3 forbids them, and none was needed).
No credential from any file is displayed. The `EVTX-ATTACK-SAMPLES` logs record **simulated** attacks on lab
machines, as their README states.

---

### `EVS-08` — Page 13 · the network-evidence set

| Field | Value |
|---|---|
| **Name** | EVS-08 — one captured intrusion: pcap + proxy log + phishing email |
| **Tier** | **3 — synthesized, and the ONE artifact class Tier 3 permits.** A pcap and text logs may be authored (see the Sourcing tiers table); a captured packet is a recording of traffic we caused, with ground truth we control. Fabricating an `.evtx`, a hive or a memory image would be a lie about what a forensic artifact looks like — a pcap of specified traffic is not |
| **Source** | `scripts/make_evs08.py` in this repository (scapy) |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no real capture, no real host, no routable address |
| **Format** | 1 × pcap + 1 × Squid-style proxy log + 1 × RFC-822 email |
| **Size** | 9 983 B total · pcap 6 808 B |
| **Contains** | 22 packets over 6 minutes: benign browsing, a **30-second HTTP beacon** to one C2, a **DNS-TXT exfil tunnel**, a **plain-HTTP POST** exfil — plus the phishing email that delivered it, and a proxy log that agrees with the pcap |
| **Page** | `P13` (`T21`, `T22`, `T23`) |
| **Date verified** | **2026-09-09** — 20 assertions run against the pcap with tshark |

| # | File | Bytes | The lesson it carries |
|--:|---|--:|---|
| 1 | `EVS-08.pcap` | 6 808 | the five layers · a beacon at a fixed 30 s · a DNS tunnel · a plain POST exfil |
| 2 | `EVS-08-proxy.log` | 2 504 | a second source that agrees with the pcap, row for row |
| 3 | `EVS-08-email.eml` | 671 | 🔴 SPF/DMARC fail, Reply-To a raw IP, Received = the exfil IP, link = the C2 |

#### Manifest — SHA-256

```
cb3cf82e5ab48aacd1dbdfb745a55086cdb73b43cd4824612ada32a8916ed3c1  EVS-08.pcap
ba8547424374d7eebe85e68ba099061758e020e151966abe8215072dc9f4b598  EVS-08-proxy.log
ae0d39945722e0cfed1f6b952206b412b24cf25474336a9e601b7e40d1697f5e  EVS-08-email.eml
```

Every hash above was copied from the builder's output (`D135`).

#### Verified by reading the pcap back — 20 of 20 assertions

**22 packets**, DNS (7) and HTTP (15) only. The beacon: **10 GETs to `sync-check.net`** at seconds 19, 49, 79 …
289 — **every gap exactly 30 s, zero jitter**, one **2001 MSIE 6.0** User-Agent while the benign traffic uses
modern Chrome. The DNS tunnel: **3 TXT queries** to `exfil-dns.net`, whose Base32 labels **decode in order to**
`CONFIDENTIAL-CLIENT-LIST-Q3-2020-450-ACCOUNTS`. The plain exfil: one **POST /upload.php of ~2.4 KB** to
`185.220.101.7`. The email: **SPF/DKIM/DMARC all fail**, **Reply-To a raw IP**, **Received from `185.220.101.7`**
— the same IP the POST went to — and its only link is `sync-check.net`, the C2. **One IP ties delivery, command
channel and exfil.**

#### Determinism

Fixed capture start (`T0 = 1600000000`), fixed payloads, fixed ports. Two builds to two paths are **byte-identical
across all three files** (`cmp` clean). No clock, no randomness enters the output.

⚠️ **`R9` — the bytes stay out of the repo.** The manifest and `scripts/make_evs08.py` are committed; regenerate with:

```
python3 scripts/make_evs08.py --out <a path OUTSIDE the repo>/EVS-08
```

Requires `scapy`. (`tshark` only to verify.)

#### What it deliberately does not contain

Every IP is documentation-/TEST-NET-safe and routes nowhere. The "stolen" string is fictional. No real person,
company, domain that resolves, or captured traffic appears (`D41`). The email addresses and hostnames are
invented fixtures.

---

### `EVS-09` — Page 14 · the incident super-timeline (capstone)

| Field | Value |
|---|---|
| **Name** | EVS-09 — one incident, merged onto one timeline |
| **Tier** | **3 — an artifact EXPORT, the class Tier 3 permits.** A timeline CSV is a plaso `l2tcsv` export, not a fabricated container. Its rows are made **consistent with the real evidence sets already built** so each traces to the page that taught its artifact |
| **Source** | `scripts/make_evs09.py` in this repository |
| **Publisher** | ITGate Academy |
| **Licence** | ours — no real case, host or address |
| **Format** | 1 × plaso-style `l2tcsv` CSV + 1 × mactime-style incident excerpt |
| **Size** | 3 415 B total · 11 timeline rows |
| **Contains** | one intrusion end to end: phish → click → execution+persistence (same second) → C2 beacon → pass-the-hash logon → DNS + HTTP exfil → Recycle-Bin cleanup → two log clears |
| **Page** | `P14` (`T24`, `T25`) |
| **Date verified** | **2026-09-09** — rows cross-checked against EVS-08/12/13/14 |

#### Manifest — SHA-256

```
c4c94a6d5430784feea3c8975e0133b1dc9ff321264d4e2a27eba55cb313bdc1  EVS-09-timeline.csv
57c7c25e1442cd8f5d46165346cc840efc375c2e9ced548cd076209fecc73794  EVS-09-incident.txt
```

Both hashes copied from the builder's output (`D135`).

#### The eleven rows, and where each traces

`12:20` phish (`EVS-08-email.eml`) · `12:24:03` click → `sync-check.net` (browser history, `P09`) · `12:24:07`
**execution + Run-key set in the same second** (`EVS-13` prefetch + `EVS-14` sysmon 13) · `12:24:20` first C2
beacon (`EVS-08.pcap`, `P13`) · `12:26:29` **4624 type-9 pass-the-hash** (`EVS-14`, `P12`) · `12:28:40` DNS-TXT
exfil + `12:30:00` HTTP POST (`EVS-08.pcap`) · `12:31:12` Recycle-Bin `$I` (`EVS-13`) · `12:34:25` + `12:35:07`
**System and Security logs cleared** (`EVS-14`) — **and the nine rows above the clears survived, because they live
in the pcap, registry and MFT, not the event logs.**

#### Determinism

Fixed incident constants, no clock or randomness. Two builds are byte-identical.

⚠️ **`R9`** — the CSV and `scripts/make_evs09.py` are committed; the row content is a manifest of the incident,
not extracted bytes. Regenerate with `python3 scripts/make_evs09.py --out <path outside the repo>/EVS-09`.

#### What it deliberately does not contain

No real case, person, company, or resolvable address (`D41`). It is a teaching reconstruction whose only purpose
is to show correlation across the artifact types the diploma taught.

---

---

### Session 2 sets — design LOCKED, manifests PENDING acquisition

**Status 2026-09-06.** The staging + acquisition (`labs/vm_notes/acquisition_runbook.md`, Phases C-D of
`staging_plan.md`) has not been run yet, so **no real hashes exist and none are invented** (Tier 1 rule:
E01, memory dump and USB image are never synthesised). Each set below is fully specified; the instructor
runs the runbook, then the two hashes per artifact are pasted in and the row is marked **verified** with the
date the check was actually run. **Part 8 step 0 stays FAILED for S2 until that happens.**

Source host for all four: exhibit **`EVI-SRC01`** = Windows host **`FIN-WKS-07`** (the built victim VM,
Meridian Retail Group / `l.bennett`). Attack window **24-26 Aug 2026**, acquired ~1 week later (`D57`).

| ID | Tier | Source | Format | Contains | Session | MD5 / SHA-256 | Verified |
|---|:-:|---|---|---|---|---|---|
| `EVS-02` | **1** | our lab — image of `FIN-WKS-07` system disk after power-down, on a write blocker | **E01** (compressed, per-chunk CRC + embedded hash) **and** raw `dd` | full system disk: OS, `l.bennett` profile, persistence, `$MFT`, USBSTOR history, cleared event logs, one timestomp | `S2-05` `S2-06` `S2-09` (and S3-S6) | ⛔ PENDING | ⛔ |
| `EVS-03` | **1** | our lab — live memory capture of `FIN-WKS-07` **before** power-down | raw memory image (`.raw`/`.mem`) + tool log | running processes, network connections, injected code, the C2 beacon in memory | `S2-03` · `S6-09` · `S6-10` | ⛔ PENDING | ⛔ |
| `EVS-04` | **1** | our lab — image of the suspect USB device | **E01** + raw | the staged `customer_export` archive, exfil artefacts, USB volume + file-system structure | `S2-08` `S2-09` `S2-10` | ⛔ PENDING | ⛔ |
| `EVS-09` | **1** | our lab — targeted triage collection from `FIN-WKS-07` (live) | KAPE/triage output tree + per-file hash list | key artefacts only (registry hives, event logs, prefetch, `$MFT`) as a triage set, not a full image | `S2-07` | ⛔ PENDING | ⛔ |

**Reconciliation with `topic_map.md`:** the map's provisional `EVS-05`..`EVS-09` are unchanged; `EVS-09`
is bound here to the S2 triage set. No IDs moved.

**Licence / IP notes for the S2 sets:** all Tier 1, ours, no third-party material. Fictional company and
users, documentation IPs only, no real malware, no real credentials (`D19`, `D41`, `R8`/`R9`). The USB
`customer_export` is benign decoy content seeded on the victim's Data drive (`seed_victim.ps1`).

---

### Reference — original placeholder table (superseded by the block above)

### Not yet built

| ID | Session | What it needs to be | Status |
|---|:-:|---|---|
| `EVS-02` | S2 | `EVI-SRC01` disk image (E01 + raw) | ⛔ **not started** — blocks S2 (Part 8 step 0) |
| `EVS-03` | S2 | memory capture from `EVI-SRC01` | ⛔ not started |
| `EVS-04` | S2 | the suspect USB device image | ⛔ not started |
| `EVS-05` | P02–P07 | file-type identification set | ✅ **built and verified** — 2026-09-04 |
| `EVS-06` | P07 | the malicious document | ⛔ not started — `P07` shipped **without it**, deliberately (`D131`) |
| `EVS-07` | P08 | storage internals, MBR and GPT | ✅ **built and verified** — 2026-09-09 |
| `EVS-08` | P13 | network capture, proxy log, phishing email (Tier 3) | ✅ **built and verified** — 2026-09-09 |
| `EVS-09` | P14 | incident super-timeline (capstone) | ✅ **built and verified** — 2026-09-09 |
| `EVS-11` | P09 | file systems and carving | ✅ **built and verified** — 2026-09-09 |
| `EVS-12` | P10 | published registry hives (Tier 2) | ✅ **fetched, pinned and verified** — 2026-09-09 |
| `EVS-13` | P11 | published user-activity artifacts (Tier 2) | ✅ **fetched and pinned** — 2026-09-09 |
| `EVS-14` | P12 | published attack event logs (Tier 2) | ✅ **fetched and pinned** — 2026-09-09 |
| `EVS-10` | P06 | hidden-information image set | ✅ **built and verified** — 2026-09-06 |

⚠️ **`EVS-02` is the critical path.** S2 cannot begin without it, and it is a real acquisition
from a real staged host — not a text file.

⚠️ **The Drive `Cases/` folder is not a source until its provenance is established.** Six
folders whose contents were never enumerated; if they are copies of public corpora, `D22` says
link and credit, never rehost.
