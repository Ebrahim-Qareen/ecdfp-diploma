# Session 2 — Guided Lab

**Acquisition: Disk, Memory & Live Response**
Eight micro-labs, one after each block. Every one has the same four parts:

```
1  WATCH   one command or one action, demonstrated first.   2–3 min
2  DO      the same thing, on your own machine.             3–5 min
3  CHECK   one line you can compare against — pass or fail.
4  WHY     one sentence: what this proves, and what it does not.
```

---

## Objective

Make evidence, and be able to prove what you did. By the end you have captured volatile data, captured
memory, imaged a volume four ways, verified an image, and closed a custody line.

## Environment

| | |
|---|---|
| Analyst workstation | `FOR-WS01`, restored to the `CLEAN-TOOLS` snapshot |
| Linux host | **Kali**, on the clean pre-staging snapshot (`D56`) |
| Scratch volume | ~100 MB, created by you — used by micro-labs 4, 5, 6 and 7 |
| Free space | ~20 GB |
| Tools | FTK Imager **8.3** · `dc3dd` **7.3.1** · OSFMount **3.3.1000** · Arsenal Image Mounter **3.13.368** |

🔴 **Never run any micro-lab against the original evidence.** Micro-labs use your scratch volume, your
own VM, or your own RAM. The case evidence is used only in `S2-08` and `S2-09`, and only from a
verified set.

---

## Micro-lab 1 — the collection order · `S2-01`

**WATCH.** The seven volatility stores are listed against the time each one survives.

**DO.** You are given this scenario:

> A workstation is running. The user is at the desk and has been asked to step away. The screen is
> unlocked. One USB device is attached. You have one hour and one external drive.

Write the collection order you would follow, and **one line per step saying what that step costs**.

**CHECK.** Your order collects the most fragile store first and the disk last. Every step has a cost
written beside it. Compare against:

```
1  photograph the screen and the attached device      costs: nothing
2  isolate the network, record the time               costs: live connections stop changing
3  capture memory                                     costs: minutes; network state decays meanwhile
4  collect volatile data (processes, connections)     costs: minutes; each command changes the host
5  power down                                         costs: everything volatile that is left
6  image the disk on a write blocker                  costs: time only
7  image the USB device                               costs: time only
```

**WHY.** *This proves you can sequence a collection and state its price. It does not prove the order
is right for every case — an encrypted volume changes it.*

---

## Micro-lab 2 — run the live-response collector · `S2-02`

**WATCH.** The collector is run once from external media, writing to external media.

**DO.** Run the collector on **your own VM**. Write its output to your external volume, never to the
system disk.

**CHECK.** Open the output folder. You should have:

```
<HOSTNAME>_<date>_<time>\
├── ForensicImages\
├── LiveResponseData\
├── <hostname>_hashes.csv
└── Processing_Details.txt
```

✅ **Verification line:** the hash list has **one entry for every collected file** — open
`<hostname>_hashes.csv` and compare its row count against the number of files collected. A missing
entry means a file was collected without being hashed.

**WHY.** *This proves the collected files have not changed since collection. It does not prove the
operating system told the truth when it listed them.*

---

## Micro-lab 3 — capture your own RAM · `S2-03`

**WATCH.** A memory capture is started and the elapsed time is read out at the end.

**DO.** Capture the memory of your own VM.

| | |
|---|---|
| Tool | FTK Imager 8.3 → `File > Capture Memory`, or `winpmem` |
| Destination | your external volume |
| Record | **start time and finish time**, in UTC |

**CHECK.**

```
# Windows — confirm the size against assigned RAM
Get-Item E:\mem.raw | Select-Object Length
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
```

✅ **Verification line:** the dump size is approximately equal to the VM's assigned RAM, **and** you
have written down both times. If the file is much smaller, the capture did not finish.

**WHY.** *The two times define the window your findings describe. The capture is a smear across that
window, not a snapshot of one instant.*

---

## Micro-lab 4 — physical and logical, on the same volume · `S2-04`

**WATCH.** The 100 MB scratch volume is imaged physically, then logically.

**DO.** Do both, with FTK Imager 8.3.

| Run | Source type | Destination |
|---|---|---|
| 1 | `Physical Drive` (or the whole volume) | `scratch_physical` |
| 2 | `Contents of a Folder` (logical) | `scratch_logical` |

**CHECK.**

```
# compare the two output sizes
Get-ChildItem E:\images\ | Select-Object Name, Length
```

✅ **Verification line:** the two files **differ in size**, and you can say why in one sentence.

**WHY.** *The size difference is the evidence you did not collect — free space, slack and deleted
remnants. It does not mean the logical image is wrong; it means it is narrower.*

---

## Micro-lab 5 — the same image as E01 and as raw · `S2-05`

**WATCH.** The scratch volume is imaged twice, once to E01 and once to raw.

**DO.** Create both from the same source.

**CHECK.**

```
# on Kali — verify the E01's embedded hash
ewfverify scratch.E01
```

Expected tail:

```
Verification completed.
   MD5 hash calculated over data: <placeholder-md5>
   ewfverify: SUCCESS
```

✅ **Verification line, three parts:**

1. the E01 is **smaller** than the raw file (compression)
2. `ewfverify` reports **SUCCESS**
3. the raw file has **no embedded hash at all** — there is nothing in it to verify against

**WHY.** *This proves the E01 container is internally intact. It does not prove either image matches
the source device now — nothing re-read the source.*

---

## Micro-lab 6 — FTK Imager, verification ticked · `S2-06`

**WATCH.** `FIN-WKS-07` is imaged end to end, with `Verify images after they are created` ticked.

**DO.** Image your scratch volume the same way.

1. Record the write blocker **before** connecting the source.
2. `File > Create Disk Image` → source type → select source.
3. Destination `E01`, fill the evidence-item fields.
4. 🔴 Tick **`Verify images after they are created`**.
5. Start.

**CHECK.** Open the `.txt` log FTK Imager writes beside the image.

```
[Computed Hashes]
 MD5 checksum    : <placeholder-md5>
 SHA1 checksum   : <placeholder-sha1>

Image Verification Results:
 MD5 checksum    : <placeholder-md5>   : verified
 SHA1 checksum   : <placeholder-sha1>  : verified
```

✅ **Verification line:** the log shows **both digests** and the word **`verified`**.

**WHY.** *This proves the copy is faithful — the tool hashed what it wrote, read it back and got the
same answer. It does not prove the source was unaltered before you arrived, because the source was
never read a second time.*

---

## Micro-lab 7 — `dc3dd` with a hash and a log · `S2-07`

Run this on the **clean Kali snapshot** (`D56`), not the compromised host.

**WATCH.** `dc3dd` images the scratch volume, hashing as it goes.

**DO.**

```
sudo dc3dd if=/dev/sdX of=/evidence/scratch.dd hash=sha256 log=/evidence/scratch.log
```

**CHECK.**

```
cat /evidence/scratch.log
```

Expected tail:

```
   204800 sectors in
   204800 sectors out
   [sha256] <placeholder-sha256>
```

✅ **Verification line:** the log file **contains the SHA-256** — which plain `dd` never produces.

**WHY.** *The log proves the hash was computed at acquisition time, not afterwards. It does not make
the image more complete than a `dd` image — the bytes are the same; only the record is better.*

---

## Micro-lab 8 — close one custody line · `S2-10`

**WATCH.** One custody line is completed on the session record.

**DO.** Open `docs/session-02/record.html` and complete your own custody entry for the exhibit you
acquired.

**CHECK.** ✅ **Verification line:** the record page shows the step **closed**, and Session 1 still
appears above it as *carried forward*.

**WHY.** *The record is the deliverable that carries from session to session. A session that does not
close it leaves the chain broken — and a broken chain is the first thing an opposing examiner looks
for.*

---

## Chain of custody — close the lab

Complete one line for the exhibit you handled today. Use the same form you used in Session 1.

| Field | Your entry |
|---|---|
| Exhibit / unique identifier | |
| Date and time received (UTC) | |
| Received from | |
| Purpose | acquisition |
| Action taken | |
| Tool and version | |
| Hash before (SHA-256) | |
| Hash after (SHA-256) | |
| Released to | |
| Date and time released (UTC) | |
| Signature | |

⚠️ The **custody-transfer log** and the **disposition** are case-level. They are recorded once for the
case and are never cleared with a session.

---

## Lab complete — check yourself

| ☐ | |
|:-:|---|
| ☐ | All eight micro-labs have a passing verification line |
| ☐ | Both digests recorded for every artifact you produced |
| ☐ | Start **and** finish times recorded for the memory capture |
| ☐ | You can state in one sentence what `verified` does not cover |
| ☐ | Your custody line is complete and the session's steps are closed on the record page |
| ☐ | Nothing you produced was written to the evidence disk |
