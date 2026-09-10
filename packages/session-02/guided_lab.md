# Session 2 — Guided Lab

**Acquisition: Disk, Memory &amp; Live Response**
**Seven micro-labs, one at the end of every integrated block.** Each has the same four parts:

```
1  WATCH   one command or action, demonstrated first.   2-3 min
2  DO      the same thing, on your own machine.         3-5 min
3  CHECK   one line you compare against: pass or fail.
4  WHY     what it proves, and what it does not.
```

---

## Environment

| | |
|---|---|
| Analyst workstation | `FOR-WS01`, restored to `CLEAN-TOOLS` |
| Linux host | **Kali**, on the **clean pre-staging snapshot** (`D56`) |
| Scratch volume | ~100 MB, made by you — used by labs 3, 4 and 5 |
| Free space | ~20 GB |
| Tools | BriMor Labs Live Response Collection · Velociraptor · WinPmem · FTK Imager **8.3** · `dc3dd` **7.3.1** · OSFMount **3.3.1000** · Arsenal **3.13.368** |

🔴 **No micro-lab touches the original evidence.** They use your scratch volume, your own VM, or your
own RAM. Case evidence is used only in `S2-07` and `S2-08`, and only from a verified set.

---

## Micro-lab 1 — run the collector · `S2-01`

**WATCH.** `Windows_Live_Response.bat` is launched **from the external drive**, as administrator, and
**Triage** is chosen.

**DO.** Run it on your own VM. Output goes to your external volume — never the system disk.

**CHECK.**

```
<HOSTNAME>_<date>_<time>\
├── ForensicImages\
├── LiveResponseData\
├── <hostname>_hashes.csv
└── Processing_Details.txt
```

✅ **Verification line:** the tree exists, and `<hostname>_hashes.csv` has **one row for every
collected file**. A missing row means a file was collected without being hashed.

**WHY.** *This proves the collected files have not changed since collection. It does not prove the
operating system told the truth when it listed them.*

---

## Micro-lab 2 — capture your own RAM · `S2-02`

**WATCH.** RAM is captured with **WinPmem** and the elapsed time is read out.

**DO.** Capture your own VM's memory. Record **start and finish** times in UTC.

**CHECK.**

```
PS> Get-Item E:\mem.raw | Select-Object Length
PS> Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
```

✅ **Verification line:** the dump is approximately the size of assigned RAM, **and** both times are
written down. Much smaller means the capture did not finish — check now, because after power-down
there is nothing to re-run.

**WHY.** *The two times define the window your findings describe. The capture is a smear across that
window, not a snapshot of one instant.*

---

## Micro-lab 3 — physical and logical, same volume · `S2-03`

**WATCH.** The 100 MB scratch volume is imaged physically, then logically.

**DO.** Do both with FTK Imager 8.3 — `Physical Drive`, then `Contents of a Folder`.

**CHECK.**

```
PS> Get-ChildItem E:\images\ | Select-Object Name, Length
```

✅ **Verification line:** the two files **differ in size**, and you can say why in one sentence.

**WHY.** *The size difference is the evidence you did not collect. The logical image is not wrong —
it is narrower.*

---

## Micro-lab 4 — E01 and raw, same volume · `S2-03`

**WATCH.** The scratch volume is imaged twice — once to E01, once to raw.

**DO.** Create both from the same source.

**CHECK.** Verify the E01 on Kali.

```
$ ewfverify scratch.E01
   MD5 hash calculated over data: <placeholder-md5>
   ewfverify: SUCCESS
```

✅ **Verification line, three parts:** the E01 is **smaller** (compression) · `ewfverify` reports
**SUCCESS** · the raw file has **no embedded hash at all** — nothing inside it to verify against.

**WHY.** *This proves the E01 container is internally intact. It does not prove either image matches
the source device now — nothing re-read the source.*

---

## Micro-lab 5 — FTK Imager with verification ticked · `S2-04`

**WATCH.** `FIN-WKS-07` is imaged end to end with **Verify images after they are created** ticked.

**DO.** Image your scratch volume the same way.

1. **Record the write blocker — before connecting the source.**
2. `File > Create Disk Image` → source type → select source.
3. Destination `E01`, evidence-item fields filled.
4. 🔴 Tick **Verify images after they are created**.

**CHECK.**

```
[Computed Hashes]
 MD5 checksum    : <placeholder-md5>
 SHA1 checksum   : <placeholder-sha1>
Image Verification Results:
 MD5  : <placeholder-md5>   : verified
 SHA1 : <placeholder-sha1>  : verified
```

✅ **Verification line:** the `.txt` log shows **both digests** and the word **`verified`**.

**WHY.** *It proves the copy is faithful — the tool hashed what it wrote, read it back, and got the
same answer. It does not prove the source was unaltered before you arrived, because the source was
never read a second time.*

---

## Micro-lab 6 — `dc3dd` with a hash and a log · `S2-05`

Run this on the **clean Kali snapshot**, never the compromised host.

**WATCH.** `dc3dd` images the scratch volume, hashing as it goes.

**DO.**

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

**CHECK.**

```
$ cat /evidence/scratch.log
   204800 sectors in / out
   [sha256] <placeholder-sha256>
```

✅ **Verification line:** the log **contains the SHA-256**, which plain `dd` never produces.

**WHY.** *The log proves the hash was computed at acquisition time, not afterwards. It does not make
the image more complete than a `dd` image — the bytes are identical; only the record is better.*

---

## Micro-lab 7 — find the files that lie · `S2-06`

**WATCH.** `file` and TrID are run across the mounted image, and one mismatch is picked out.

**DO.** Mount your image **read-only** (OSFMount or Arsenal Image Mounter) and sweep it. For the
`EVS-05` set, record the first four bytes of every file.

**CHECK.**

```
$ file *
$ xxd -l 4 holiday_snap.jpg
00000000: 504b 0304                                PK..
```

✅ **Verification line:** you can name at least one file, quote its **first four bytes**, and state
the type those bytes indicate. In `EVS-05` there are **five** such files.

⚠️ **The trap:** `policy_v2.docx` — a `.docx` really is a ZIP, so a student who has learned that rule
will predict `50 4B 03 04`. It is a PNG. Look, do not predict.

**WHY.** *The bytes say what a file is. They never say who named it, or why. And a valid signature
does not mean a valid file — `scan_partial.png` has a perfect PNG header and a truncated body.*

---

## Chain of custody — close the lab

Complete one line for the exhibit you handled today, on the same form you used in Session 1.

| Field | Your entry |
|---|---|
| Exhibit / unique identifier | |
| Date and time received (UTC) | |
| Received from | |
| Action taken | |
| Tool and version | |
| Hash before (SHA-256) | |
| Hash after (SHA-256) | |
| Released to · when | |
| Signature | |

⚠️ The **custody-transfer log** and the **disposition** are case-level. They are recorded once for the
case and are never cleared with a session.

---

## Lab complete — check yourself

| ☐ | |
|:-:|---|
| ☐ | All seven micro-labs have a passing verification line |
| ☐ | Both digests recorded for every artifact you produced |
| ☐ | Start **and** finish times recorded for the memory capture |
| ☐ | You can state in one sentence what `verified` does not cover |
| ☐ | You found all five extension mismatches in `EVS-05` |
| ☐ | Your custody line is complete and the session's steps are closed |
| ☐ | Nothing you produced was written to the evidence disk |
