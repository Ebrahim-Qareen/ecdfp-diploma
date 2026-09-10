# Session 3 — Guided Lab

**Hidden Information: Metadata, Steganography & Malicious Files**
**Six micro-labs, one at the end of every integrated block.**

```
1  WATCH   one command, demonstrated first.       2-3 min
2  DO      the same thing, on your own machine.   3-5 min
3  CHECK   one line you compare against.
4  WHY     what it proves, and what it does not.
```

---

## Environment

| | |
|---|---|
| Workstation | `FOR-WS01` on `CLEAN-TOOLS` |
| Evidence | `EVS-05` and `EVS-10`, **verified against their manifests before you start** |
| Tools | ExifTool 13.59 · HxD 2.5.0.0 · `binwalk` · `zsteg` · Stegsolve · `oledump.py` / `olevba` |

🔴 **Work on a copy.** Verify, copy, then examine the copy — never the file you were handed.

---

## Micro-lab 1 — read every block of metadata · `S3-02`

**WATCH.** `exiftool office_floor3.jpg` is run and the camera and GPS blocks read out.

**DO.** Run it across every file in `EVS-10`.

```
$ exiftool -a -G1 office_floor3.jpg
[ExifIFD]  Date/Time Original   : 2026:08:24 09:14:02
[IFD0]     Modify Date          : 2026:08:31 16:40:05
[GPS]      GPS Latitude         : 30 deg 2' 27.60" N
[GPS]      GPS Longitude        : 31 deg 14' 13.20" E
```

**CHECK.** ✅ You can name the file carrying GPS coordinates and quote them, **and** name at least one
file in the set with no EXIF at all.

**WHY.** *It proves what the device recorded. It does not prove where the photographer was — a device
can be wrong, spoofed, or carried by someone else.*

---

## Micro-lab 2 — line up the four clocks · `S3-02`

**WATCH.** The three EXIF times and the file system mtime of one file are put side by side.

**DO.** Do the same, and write the gap between each pair in days.

```
$ exiftool -DateTimeOriginal -CreateDate -ModifyDate office_floor3.jpg
$ stat -c '%y' office_floor3.jpg
```

**CHECK.** ✅ Four values, three gaps, and you can say **which clock wrote each one**.

**WHY.** *There is no "the date" of a photograph. A finding names which clock it read. Internal
metadata travels with the file; the file system's mtime describes the journey.*

---

## Micro-lab 3 — find the payload, and the clean twin · `S3-03`

**WATCH.** `zsteg receipt_scan.png` is run, then the same command on `receipt_scan_clean.png`.

**DO.** Run both, and recover the message.

```
$ zsteg receipt_scan.png
b1,b,lsb,xy  .. text: "MRG-INTERNAL: staged archive is customer_export.7z"

$ zsteg receipt_scan_clean.png
[nothing]
```

Then browse the bit planes of both in Stegsolve and compare what the low bit looks like.

**CHECK.** ✅ You can quote the recovered string **and** state what `zsteg` reported for the clean
file. In Stegsolve, you can describe how the two low-bit planes differ.

**WHY.** *A negative result does not mean the file is clean. Write it as:* `zsteg <version>` *reported
no LSB payload; this does not exclude other methods.*

---

## Micro-lab 4 — the file that is two files · `S3-04`

**WATCH.** `binwalk team_photo.jpg` is run, then the same file is opened with `unzip`.

**DO.** Do both, and extract the appended file.

```
$ binwalk team_photo.jpg
DECIMAL   HEX      DESCRIPTION
0         0x0      JPEG image data
10327     0x2857   Zip archive data, name: handover.txt

$ unzip team_photo.jpg
```

**CHECK.** ✅ You can name the appended file, give the **offset** where the ZIP begins as a number,
and open the same file normally in an image viewer.

**WHY.** *The offset is the finding. Whether the append was deliberate is not — some formats append
thumbnails and colour profiles legitimately.*

---

## Micro-lab 5 — find the macro · `S3-05`

**WATCH.** A macro-enabled document is unzipped and `word/vbaProject.bin` located; `oledump.py` then
lists the streams inside that part.

**DO.** Do the same on the supplied document. Record the exact path of the macro part.

```
$ unzip -l suspicious.docm | grep -i vba
     18432  2026-08-24 09:14   word/vbaProject.bin

$ oledump.py word/vbaProject.bin
  3:      1149  'VBA/Module1'   M
```

**CHECK.** ✅ You can give the container format, the exact path of the macro part, and its size.

**WHY.** *Locating a macro and reading it are two different steps. And a document being opened is not
evidence that anyone chose to run its macro knowingly.*

⛔ **If `EVS-06` is not yet available**, this lab runs on a locally created macro-enabled document.
The method is identical; only the case relevance is deferred.

---

## Micro-lab 6 — the thumbnail that outlived the edit · `S3-06`

**WATCH.** The EXIF thumbnail is extracted from `invoice_batch.jpg` and opened beside the main image.

**DO.** Do the same, and compare them.

```
$ exiftool -b -ThumbnailImage invoice_batch.jpg > thumb.jpg
```

**CHECK.** ✅ You can describe one region where the thumbnail and the main image differ, and give its
approximate coordinates.

**WHY.** *It proves the main image changed after the thumbnail was generated. It does not prove who,
when, or why — and a **matching** thumbnail proves nothing at all, because many editors update it
correctly.*

---

## Chain of custody — close the lab

| Field | Your entry |
|---|---|
| Exhibit / unique identifier | |
| Date and time received (UTC) | |
| Action taken | |
| Tool and version | |
| Hash before (SHA-256) | |
| Hash after (SHA-256) | |
| Signature | |

⚠️ The custody-transfer log and the disposition are **case-level**. Clearing a session never clears them.

---

## Lab complete — check yourself

| ☐ | |
|:-:|---|
| ☐ | All six micro-labs have a passing check |
| ☐ | Both evidence sets verified against their manifests before you started |
| ☐ | Every date you wrote names **which clock** it came from |
| ☐ | Your steganography result states the tool, its version, and its limit |
| ☐ | Every offset is a number, not a description |
| ☐ | Your custody line is complete and the session's steps are closed |
