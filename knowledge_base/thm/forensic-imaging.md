---
room: Forensic Imaging
url: https://tryhackme.com/room/forensicimaging
module: Disk Image Analysis
feeds: **S2 — the core acquisition session.** `S2-06` (imaging tools) directly; also `S2-02`
       (write-blocking), `S2-04` (hashing and verification) and `S2-07` (mounting for analysis).
       Also **S1** (a sixth safety defect, and the worst one yet) and **R9**.
difficulty / time: Easy · 45 min · 7 tasks · **free room** · 18,481 completions · 344 recommends
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (logged-in session)
completeness: all 7 tasks read in full. 0 sections NOT READ.
              🔴 Room ships plaintext VM credentials in Tasks 2 and 6 — **deliberately not
              reproduced here (R8)**.
---

## 1. What the room teaches

Linux disk imaging end to end: identify the device → set up an audit trail → image with `dc3dd` →
verify by hash → mount and browse. It is the **only room in the path that covers acquisition as a
procedure**, and at 18,481 completions it is by far the most-taken room we have extracted — which
makes what is wrong in it worth more attention, not less.

**🟢 The best thing in it, by a distance, is Task 2's audit trail.** Seven bash settings plus
session recording with `script`, presented as *"we need to preserve the evidence and keep track of
our activities"*. **Nothing else in fourteen rooms teaches the examiner to log themselves.** That
section alone justifies the extraction.

**🔴 And the worst thing in it is Task 5.** The room computes an MD5, confirms it matches, and then
— on the next page — runs `sudo mount -o loop example1.img /mnt/example1`. **A read-write ext4
mount modifies the image.** Mount count, mount time and `s_last_mounted` are written into the
superblock; `relatime` updates the atime of every file older than a day the moment it is listed;
and if the image is dirty the journal is replayed. **The hash the student verified on the previous
page is no longer valid, and the room never re-checks it.** This is not a nitpick — it is the exact
anti-pattern the verification step exists to prevent, taught immediately after the verification
step, to eighteen thousand people.

Everything else sits between those two poles: a genuinely good conceptual frame (write-blockers,
chain of custody, audit trail), applied in a lab that follows almost none of it.

## 2. Artifacts — one 6-box block each

### 2.1 The block-device inventory (`lsblk` / `df`)

- **What it is** — the list of devices the kernel can see, before anything is imaged.
- **Where it lives** — `/dev`; `lsblk` reads **sysfs and the udev database**, not the filesystem
  table, which is why it sees devices `df` cannot.
- **What it proves** — 🟢 **the room makes the right point and makes it well**: the target device
  **does not appear in `df`** because it is not mounted, and *"this is also common for physical
  disks when not directly attached."* `lsblk -a` shows it (`loop11`, 1.1 G) where `df` shows
  nothing. **A student who reaches for `df` will conclude the disk is not there.**
- **What it does NOT prove** — 🔴 **that you are looking at the whole disk.** `lsblk` reports the
  capacity the drive *advertises*. A **Host Protected Area** or **Device Configuration Overlay**
  makes a drive report less than it physically holds, and a naive image of the visible LBA range
  silently misses the hidden region. **The room never mentions HPA or DCO** — see §3 #12. It also
  does not prove the device is the right one; `lsblk` output alone has been the cause of many
  wrong-disk images.
- **How to parse it** — `lsblk -a` (all devices, incl. empty), `lsblk -l` (flat list),
  `lsblk -o NAME,SERIAL,MODEL,SIZE` for identification. Then `sudo losetup -l /dev/loopN` for the
  backing file, and `sudo blkid /dev/loopN` for **UUID and filesystem type**.
- **Anti-forensics / false-positive caveat** — ⚠️ **the room's own `losetup -l` output shows
  `RO 0`** — the loop device is attached **read-write** — on the same page that explains
  write-blockers. See §2.2. Also note **loop numbering is not stable**: the room says so honestly
  (*"the loop devices might change… identify the loop device with a 1.1 GB size"*), which is good
  practice, but **size is a weak identifier** — match on the backing file from `losetup -l`.

### 2.2 The write-blocker (taught, then not used)

- **What it is** — a control that intercepts write commands between the evidence device and the
  examining OS.
- **Where it lives** — hardware, inline on the bus; or, in software, at the block layer.
- **What it proves** — 🟢 **the room's explanation is correct and clear**: *"work by physically
  intercepting all drive commands that write data sent between the disk being imaged and the OS
  attached to it"*, and *"usually required when manipulating physical disks."*
- **What it does NOT prove** — 🔴🔴 **the room never uses one.** The entire lab runs on a loop
  device attached read-write, and `losetup -r` — a genuine block-layer read-only attachment —
  was one flag away. **A room that explains a control and then performs the whole procedure
  without it teaches that the control is optional.**
  ⚠️ And the software/hardware distinction matters: **`blockdev --setro` is advisory**, not
  enforcing — its own man page says *"the currently active access to the device may not be
  affected"*, and filesystem drivers have historically written through it (XFS superblock updates,
  ext3/4 orphan-inode removal, journal error-code transfer, userspace TRIM). **`losetup -r` is
  enforced by the loop driver; `blockdev --setro` is defence in depth.** Neither replaces a
  hardware write blocker for physical media.
- **How to parse it** — for our lab: `sudo losetup -r -f --show <image>` to attach read-only, and
  `blockdev --getro` to confirm. For physical media: a tested hardware blocker.
- **Anti-forensics / false-positive caveat** — ⚠️ **NIST CFTT has never tested a Linux software
  write blocker.** Its Software Write Block spec is **version 3.0, dated 2003**, its procedure
  document is titled *"…Interrupt 0x13 Based Software Write Block Tools"*, and the newest SWB test
  report is from **January 2008**. The **Hardware** Write Block programme is live, with reports
  dated **December 2025**. **Say this plainly in `S2-02`:** software write-blocking on Linux is
  effective and unvalidated; hardware write-blocking is the defensible control.

### 2.3 The examiner's audit trail

- **What it is** — a contemporaneous record of **what the examiner did**, as distinct from what the
  evidence contains.
- **Where it lives** — `~/.bash_history` with timestamps, plus a full session transcript from
  `script(1)`, plus the output file of every command.
- **What it proves** — 🟢🟢 **that the examiner's own actions are accountable.** The room's seven
  settings — `set -o history`, `shopt -s histappend`, clearing `HISTCONTROL` and `HISTIGNORE`,
  `HISTFILE`, `HISTFILESIZE=-1`, `HISTSIZE=-1`, `HISTTIMEFORMAT` — are individually correct, and
  clearing `HISTCONTROL`/`HISTIGNORE` so that **nothing is silently excluded** is a subtle, genuinely
  expert touch. Add `script` for the full transcript and *"always save the output of any command…
  to a file"*, and this is a professional habit taught properly.
- **What it does NOT prove** — 🔴 **that anything was actually recorded, if the shell dies.**
  **Bash writes history to `$HISTFILE` at shell exit**, not per command — the manual is explicit:
  *"When a shell with history enabled exits, the last $HISTSIZE lines are copied from the history
  list to the file named by $HISTFILE."* `shopt -s histappend` only changes append-vs-overwrite
  **at that same exit-time write**. A `kill -9`, a closed window, a crashed VM or a reset box
  **loses the entire session's history.** The room's block has no `history -a`. ⚠️ And even with
  `history -a` a hung command that is then killed is never recorded — **which is why `script` is
  the audit trail and history is the convenience copy.**
- **How to parse it** — the corrected block for our material:

  ```bash
  set -o history; shopt -s histappend
  export HISTCONTROL= HISTIGNORE=
  export HISTFILE=~/.bash_history HISTFILESIZE=-1 HISTSIZE=-1
  export HISTTIMEFORMAT="%F %T "          # seconds, not minutes — see below
  export PROMPT_COMMAND='history -a'      # write per command, not at exit
  script --log-timing=session.timing --log-io=session.io   # replayable transcript
  ```

- **Anti-forensics / false-positive caveat** — ⚠️ two small errors to fix before this reaches a
  slide. **`HISTTIMEFORMAT="%F-%R "` produces `YYYY-MM-DD-HH:MM`**, not the room's stated
  *"YYYY-MM-DD HH"* — `%R` is `%H:%M`, and the separator is a literal hyphen. **Use `%F %T ` for
  seconds resolution**, because minute granularity cannot order two commands in the same minute,
  which is precisely when ordering matters. And **`script --timing` is deprecated** in current
  util-linux in favour of `--log-timing`.

### 2.4 The raw image (`dc3dd`)

- **What it is** — a bit-for-bit copy of every sector the device reports, written to a file.
- **Where it lives** — wherever `of=` points; here `example1.img`, root-owned, 1.1 G.
- **What it proves** — the room's output is a good acquisition record in itself: **tool version,
  start and completion timestamps, the full command line, `device size: 2252800 sectors (probed)`,
  `sector size: 512 bytes (probed)`, `2252800 sectors in` / `2252800 sectors out`, and
  `0 bad sectors replaced by zeros`.** 🟢 **That last line is the one to teach** — it is the
  difference between "the copy is complete" and "the copy is complete *and nothing was silently
  substituted*", and it is exactly what plain `dd` will not tell you.
- **What it does NOT prove** — 🔴🔴 **that the image matches the source, because the room did not
  ask `dc3dd` to hash.** It runs `dc3dd if=… of=… log=…` with **no `hash=` and no `hlog=`**, then
  hashes separately afterwards (§2.5). The room's own tool table describes dc3dd as *"an enhanced
  version of dd with additional features for forensic imaging, **including hashing and logging**"*
  — **and then uses the logging and not the hashing.** On-the-fly hashing is the entire reason to
  prefer dc3dd over `dd`.
  ⚠️ It also does not prove the *disk* was fully captured — see the HPA/DCO caveat in §2.1.
- **How to parse it** — what our material should teach instead:

  ```bash
  sudo dc3dd if=/dev/loopN of=evidence.dd \
      hash=md5 hash=sha256 log=acquire.log hlog=evidence.hashes verb=on
  ```

  **`hash=` may be repeated per algorithm** (md5, sha1, sha256, sha512), `log=` captures I/O
  statistics and diagnostics, `hlog=` captures total and piecewise hashes. ⚠️ **`hashlog=` and
  `hashconv=` are `dcfldd` options, not `dc3dd`** — mixing them produces an unrecognised-operand
  error in front of the class.
- **Anti-forensics / false-positive caveat** — ⚠️ **the room's own output is internally
  inconsistent**: `dc3dd` reports *started at 22:58:59 … completed at 22:59:12*, but the very next
  command shows `ls -alh example1.img` → **`Jun 28 22:28`** — a modification time **thirty minutes
  before the command that created the file**. Screenshots taken at different times, spliced into
  one narrative. 🟢 **Add it to the documentation-audit exercise** built from rooms 12–14 §4: it is
  the same failure, in a different room, and it is the kind of thing a defence expert reads for.

### 2.5 The integrity check (hash of image vs source)

- **What it is** — proof that the copy is identical to what was read from the source.
- **Where it lives** — computed over the image file and over the device: `md5sum example1.img` and
  `md5sum /dev/loop11`, which match.
- **What it proves** — 🟢 **the method is right and worth keeping.** Hashing the **device node**
  and not just the file is exactly correct, and it is a step many courses skip.
- **What it does NOT prove** — 🔴 **MD5 alone is not a defensible integrity control in 2026.**
  The room's own prose says *"cryptographic hash functions, such as MD5, SHA-1, or SHA-256"* and
  then uses only MD5, for both exercises and both answers. MD5 and SHA-1 are collision-broken; they
  are retained for **legacy tool interoperability**, not for integrity. **R9 requires both — MD5 for
  compatibility, SHA-256 as the control.** ⚠️ It also does not prove the source was unaltered
  *before* imaging — a hash taken after the fact establishes a chain from that moment forward and
  nothing earlier.
- **How to parse it** — `sha256sum image > image.sha256` then **`sha256sum -c image.sha256`**, and
  the same for the device. 🟢 **Teach `-c`**, not a visual comparison of two hex strings — rooms
  12–14 showed a `diff`-based comparison that could never have worked, and eyeballing 64 hex
  characters is not a control.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **and then Task 5 invalidates it.** See §2.6.
  **The room verifies the hash and immediately performs an operation that changes it, and never
  re-verifies.** Any competent cross-examination ends there.

### 2.6 🔴🔴 The mounted image — the room's central defect

- **What it is** — the image attached and browsed as a filesystem: `sudo mkdir -p /mnt/example1`
  then **`sudo mount -o loop example1.img /mnt/example1`**, then `ls`.
- **Where it lives** — a loop device created implicitly by `mount`, **read-write**, with default
  options.
- **What it proves** — that the image contains a valid, browsable ext4 filesystem. That is a real
  and useful check.
- **What it does NOT prove** — 🔴🔴 **anything about the image afterwards, because the mount
  changed it.** Four independent mechanisms, all verified:
  1. **Mount count and mount time.** Every read-write mount does `le16_add_cpu(&es->s_mnt_count, 1)`
     and `es->s_mtime = …` in the superblock. **This alone changes the hash, on a perfectly clean
     image.**
  2. **`s_last_mounted`.** On first file access the kernel writes **the examiner's own mount path**
     into the evidence superblock.
  3. **atime.** The default is `relatime`, which is not "no writes": *"the file's last access time
     is always updated if it is more than 1 day old."* **Every file on an evidence image is older
     than a day**, so the first `ls`/`cat`/`grep` writes to the image *and* destroys the atime
     evidence.
  4. **Journal replay**, if the image is dirty. The kernel's own ext4 documentation:
     *"ext4 will replay the journal (and thus write to the partition) **even when mounted 'read
     only'**."*
  ⚠️ **`-o ro` alone is therefore NOT sufficient.** `mount(8)`: *"depending on the filesystem type,
  state and kernel behavior, the system may still write to the device… you may want to mount an
  ext3 or ext4 filesystem with the `ro,noload` mount options or set the block device itself to
  read-only mode."*
- **How to parse it** — the corrected commands for `S2-07`:

  ```bash
  # ext4 / raw
  sudo losetup -r -f --show evidence.dd            # read-only at the block layer, first
  sudo mount -o ro,noload,noatime,nodev,noexec /dev/loopN /mnt/case
  # NTFS
  sudo mount -t ntfs-3g -o ro,noatime,nodev,noexec,show_sys_files,streams_interface=windows \
       /dev/loopN /mnt/case
  ```

  `ro` + **`noload`/`norecovery`** stops journal replay · `noatime` stops the relatime writes ·
  `nodev`/`noexec` protect **the analyst's workstation** from device nodes and malware in the
  evidence (they protect the examiner, not the evidence — say which is which). For NTFS,
  **`show_sys_files` exposes `$MFT`, `$LogFile` and `$UsnJrnl`, and `streams_interface=windows`
  exposes alternate data streams** — both are off by default, and both are the artifacts our S4 and
  S5 material depends on.
- **Anti-forensics / false-positive caveat** — 🟢 **the exercise writes itself**: hash the image,
  mount it the room's way, hash it again. **The hashes differ.** Then do it correctly and show they
  match. **That five-minute demonstration is the most persuasive thing we can put in `S2`**, and
  the room hands us the setup for free. ⚠️ Best practice beyond the mount options: **prefer not to
  mount at all** — `fls`/`icat` and Autopsy read the image without attaching a filesystem driver
  to it.

### 2.7 The loop device as a stand-in for physical media

- **What it is** — `losetup` attaching a **file** so the kernel presents it as a block device.
- **Where it lives** — `/dev/loopN`, with the backing file visible in `losetup -l`
  (`BACK-FILE /home/ubuntu/example1.img`).
- **What it proves** — 🟢🟢 **that we can teach the whole acquisition workflow with no physical
  disk and no purchased hardware.** `losetup` gives students a "drive" to identify, write-block,
  image, hash, mount and verify. **This is a fifth Tier 1 evidence route and it costs nothing** —
  see §4.
- **What it does NOT prove** — 🔴 **that the student has handled real media.** A loop device has no
  HPA, no DCO, no bad sectors, no SMART data, no serial number, no bus, no ATA command set, and no
  way to fail halfway. **Everything in `S2` that is about the physical layer must be taught
  separately**, and students must be told plainly that the loop exercise models the *procedure*,
  not the *medium*.
- **How to parse it** — `losetup -l /dev/loopN` for the backing file and the **`RO` column**;
  `losetup -r -f --show <file>` to attach read-only; `losetup -d /dev/loopN` to detach.
- **Anti-forensics / false-positive caveat** — ⚠️ the room images `/dev/loop11` **to a file whose
  basename matches the loop device's own backing file** (`example1.img` → `example1.img`). It works
  because the cwd differs, but it is confusing and it is exactly how a student overwrites their
  evidence. **Name the output `<case>-<device>-<date>.dd` and never reuse the source basename.**

### 2.8 The device's identity (what the room omits)

- **What it is** — manufacturer, model, serial number, firmware, native capacity: the facts that go
  on the chain-of-custody form.
- **Where it lives** — the drive's own IDENTIFY DEVICE response, not the filesystem.
- **What it proves** — **which physical object this image came from.** An image with no serial
  number is an image of *a* disk.
- **What it does NOT prove** — ⚠️ **the reported capacity is not necessarily the real one.**
  `hdparm -N` returns *two* values — current max sectors and the **native hardware limit** — and a
  difference *"indicates how many sectors of the disk are currently hidden from the operating
  system, in the form of a Host Protected Area."* `--dco-identify` covers the DCO case.
  **A naive image captures only the visible range**, which is why HPA/DCO is a classic hiding
  place. **The room omits this entirely.**
- **How to parse it** — 🔴 **the room says `hparn`. That command does not exist; it is `hdparm`.**
  Use **`hdparm -I /dev/sdX`** (queries the drive now), not `-i` (the kernel's cached copy from
  boot). Corroborate with `lsblk -o NAME,SERIAL,MODEL`, `smartctl -i /dev/sdX`, and
  `udevadm info --query=all --name=/dev/sdX` (`ID_SERIAL`, `ID_MODEL`, `ID_WWN`).
- **Anti-forensics / false-positive caveat** — 🔴🔴 **`hdparm -N` and `--dco-restore` are WRITE
  commands to the drive's configuration.** `--dco-restore` *"reset[s] all drive settings, features,
  and accessible capacities back to factory defaults"*. **Detect and document with `-N` (no
  parameter) and `--dco-identify`; never modify evidence media outside an authorised, recorded
  procedure.** This belongs in the S1 handling exercise as the one case where the *documented*
  right answer is still dangerous.

## 3. Tools and commands

| step | command as the room writes it | what it gives |
|---|---|---|
| mounted filesystems | `df` / `df -h` | ⚠️ **will not show the target** — it is unmounted |
| all block devices | `lsblk -a` / `lsblk -l` | the device, incl. unmounted and loop |
| loop backing file | `sudo losetup -l /dev/loop11` | backing file, **`RO` flag**, sector size |
| filesystem identity | `sudo blkid /dev/loop11` | UUID and TYPE |
| audit trail | 7 × `export`/`shopt` + `script` | ⚠️ **needs `history -a`** — §2.3 |
| image | `sudo dc3dd if=/dev/loop11 of=example1.img log=imaging_loop11.txt` | ⚠️ **no `hash=`** — §2.4 |
| size check | `ls -alh example1.img` | 1.1 G, matches |
| verify | `sudo md5sum example1.img` and `sudo md5sum /dev/loop11` | ⚠️ **MD5 only** |
| mount | `sudo mkdir -p /mnt/example1` · `sudo mount -o loop example1.img /mnt/example1` | 🔴🔴 **modifies the image** |
| browse | `ls /mnt/example1/` | 25 directories + `lost+found` |
| disk identity | `hparn` | 🔴 **not a command — it is `hdparm`** |

The room's own imaging-tool table, with our currency verdict on each:

| tool | room's description | verified status, 2026-08-28 |
|---|---|---|
| `dd` | *"standard Unix utility… often used for creating raw disk images"* | ⚠️ **do not teach for acquisition** — no hashing, no bad-sector accounting, no resume |
| `dc3dd` | *"enhanced… including hashing and logging"* | **7.3.1** (Apr 2023) upstream — **dormant upstream, actively packaged** (Debian `7.3.1-4`, Sep 2025; Kali 7.3.1). Room shows **7.2.646** (Mar 2017) |
| `ddrescue` | *"recovery tool… rescue as much data as possible"* | ✅ **GNU ddrescue 1.30, Jan 2026** — current and correct for damaged media |
| FTK Imager | *"GUI-based… widely used"* | see `_TOOL_CURRENCY_2026-08-28.md` block A |
| Guymager | *"GUI-based… supports various image formats and detailed logs"* | **0.8.13 (Aug 2021)** upstream — stale, but **packaged in Debian as recently as Feb 2026**. Writes **dd, E01 and AFF** |
| EWF tools (`ewfacquire`) | *"creating and handling Expert Witness Format images"* | ⚠️ **messy** — see #7 below |

### CURRENCY CHECK — verified 2026-08-28

| # | item | result |
|---|---|---|
| 1 | 🔴🔴 **`mount -o loop` modifies the evidence image** | Verified four ways. **Mount count + mount time**: every rw mount runs `le16_add_cpu(&es->s_mnt_count, 1)` and `es->s_mtime = …` in the superblock. **`s_last_mounted`**: the kernel writes the examiner's mount path into the evidence on first file access. **atime**: `relatime` is the default and *"the file's last access time is always updated if it is more than 1 day old"* — true of every file on an evidence image. **Journal replay** on a dirty image. **The MD5 verified in Task 4 is invalid by the end of Task 5, and the room never re-checks it.** |
| 2 | 🔴 **`-o ro` alone would still be wrong** | `mount(8)`: *"depending on the filesystem type, state and kernel behavior, the system may still write to the device. For example, ext3 and ext4 will replay the journal if the filesystem is dirty. To prevent this kind of write access, you may want to mount an ext3 or ext4 filesystem with the `ro,noload` mount options or set the block device itself to read-only mode."* The kernel's ext4 doc is blunter: *"ext4 will replay the journal (and thus write to the partition) even when mounted 'read only'."* **Minimum correct set: `ro,noload,noatime`, over a `losetup -r` device.** |
| 3 | 🔴 **the room teaches write-blocking and then does not use it** | `losetup -r` is one flag and gives a **genuinely enforced** read-only device — the loop driver stops write and discard requests. The room's own `losetup -l` output shows **`RO 0`**. |
| 4 | ⚠️ **`blockdev --setro` is advisory, not enforcing** | Its man page: *"the currently active access to the device may not be affected by the change."* It is up to each filesystem driver to honour it, and several historically did not (XFS superblock writes, ext3/4 orphan-inode removal, journal error-code transfer, userspace TRIM). **Defence in depth, not a write blocker.** |
| 5 | 🔴 **NIST CFTT has never tested a Linux software write blocker** | The **Software** Write Block spec is **v3.0, dated 1 Sep 2003**; the procedure document is titled *"…Interrupt 0x13 Based Software Write Block Tools"*; newest SWB test report **Jan 2008**. The **Hardware** Write Block programme is **live** — spec v2.0, test reports dated **16 Dec 2025**. **Software write-blocking on Linux is effective and unvalidated; hardware is the defensible control.** Say so in `S2-02`. |
| 6 | 🔴 **the room never uses `dc3dd`'s hashing** | Correct form: `dc3dd if=… of=… hash=md5 hash=sha256 log=acquire.log hlog=evidence.hashes verb=on`. **`hash=` repeats per algorithm** (md5/sha1/sha256/sha512). ⚠️ **`hashlog=` and `hashconv=` are `dcfldd` options, not `dc3dd`.** ⚠️ Also: the Debian **man page footer still reads `dc3dd 7.2.646`** even on 7.3.1 — a student checking the version via `man` gets the wrong answer. |
| 7 | ⚠️ **libewf / `ewfacquire` — stale but standard** | Upstream `libyal/libewf` is marked **"Status: experimental"** and its newest artefact is a **pre-release, 20240506**. **Distros still ship the 2014 stable release** (Debian `20140816-2`, uploaded Nov 2025; Kali `20140816`). `ewfacquire` still exists. **E01 remains the interchange standard — AFF4 has NOT replaced it** (AFF4-L appears in EnCase and AXIOM Cyber alongside E01, not instead of it). **Teach E01; mention AFF4-L.** |
| 8 | ⚠️ **`dcfldd` is the more actively released sibling** | Upstream died; now maintained by volunteers (*"dcfldd needs your help"*). **v1.9.3**, Debian `1.9.3-2` (Aug 2025) — more recent than dc3dd's 2023. Its `hashwindow=` piecewise hashing is genuinely useful. **Recommendation for our lab: Guymager or `ewfacquire` for the primary acquisition (E01 + metadata + integrated verify), `ddrescue` for damaged media, `dc3dd`/`dcfldd` as the "raw dd with hashing" teaching step, and never plain `dd`.** |
| 9 | ⚠️ **`HISTTIMEFORMAT="%F-%R "` is misdescribed** | `%R` is `%H:%M`, so the output is **`YYYY-MM-DD-HH:MM`**, not the room's *"YYYY-MM-DD HH"*. **Use `%F %T ` for seconds** — minute granularity cannot order two commands in the same minute. `HISTSIZE=-1` and `HISTFILESIZE=-1` are both correct (negative = unlimited / no truncation). |
| 10 | 🔴 **the audit trail is not crash-safe** | Bash manual: *"When a shell with history enabled exits, the last $HISTSIZE lines are copied from the history list to the file named by $HISTFILE."* **At exit.** `histappend` only changes append-vs-overwrite at that same write. **Add `PROMPT_COMMAND='history -a'`.** ⚠️ Even then, a hung-then-killed command is never recorded — **`script` is the audit trail; history is the convenience copy.** |
| 11 | ⚠️ **`script --timing` is deprecated** | Current util-linux: *"the `--timing` option is deprecated in favour of `--log-timing`."* Use `script --log-timing=f.timing --log-io=f.io`, replay with `scriptreplay`. `ttyrec` is still packaged (Debian `1.1.7.1-2`, Aug 2025) but has **no remaining advantage**; `asciinema` **3.0 (Sep 2025, Rust rewrite)** is better for producing teaching material. **`script` is the right default** — it is in util-linux, present on every evidence-handling boot medium, and needs no install. |
| 12 | 🔴 **`hparn` does not exist** | It is **`hdparm`**, and **`-I`** (query the drive now) not `-i` (kernel's cached copy from boot). ⚠️ **The room omits HPA and DCO entirely.** `hdparm -N` returns current-max **and** native-max sectors; a difference *"indicates how many sectors of the disk are currently hidden from the operating system."* `--dco-identify` covers DCO. 🔴🔴 **`-N` with a parameter and `--dco-restore` are WRITE commands to the drive configuration** — detect and document only. |
| 13 | ⚠️ **MD5-only** | Room's prose names MD5, SHA-1 and SHA-256; the lab and both answers use MD5 alone. **R9 requires both** — MD5 for legacy tool interoperability, **SHA-256 as the control** — and verification via **`sha256sum -c`**, never by eye. |
| 14 | ⚠️ **an unsourced legal claim** | *"The use of open-source software for image acquisition is an advantage in many cases since it can satisfy guidelines for evidential reliability."* Plausible and commonly argued, but **jurisdiction-dependent and uncited**. **Do not repeat it as fact in a GRC-adjacent module** — attribute it or drop it. |
| 15 | ⚠️ **"Docker Images" is a category error** | Task 5 lists Docker alongside remote and USB imaging, hedged as *"while not strictly an image"*. A Docker **image** is a layered build artefact, not a forensic image. What you acquire from a **container** is the writable layer plus a checkpoint (`docker export` / `docker commit` / CRIU), and the host's storage driver directory. **Rewrite the row or drop it** — the terminology collision will confuse students permanently. |

## 4. Evidence used

- A **1.1 GB virtual disk attached to a loop device** on an Ubuntu lab VM, backed by a file
  (`losetup -l` shows `BACK-FILE /home/ubuntu/example1.img`), containing an **ext4** filesystem with
  25 directories and `lost+found`. A second image, `exercise.img`, in the analyst's home directory
  holds a `flag.txt` for the assessed questions. Task 6 attaches a second, separate lab machine.
- **Not downloadable. No licence offered. Not reusable.**
- 🔴 **The room prints plaintext VM credentials for both lab machines.** **Not reproduced here
  (R8), and our material must never ship credentials in a slide or a handout** — they go in the
  session's private lab sheet or nowhere.

### 🟢🟢 A fifth Tier 1 evidence route, and the cheapest one yet — `EVS-05`

The loop-device technique is the whole point. **We can build a complete acquisition lab with no
physical media, no write-blocker hardware and no purchase:**

```bash
# build a "disk" — done once, shipped as one file per student, or made by them in class
dd if=/dev/zero of=EVS-05.raw bs=1M count=1024
mkfs.ext4 EVS-05.raw                       # or mkfs.ntfs / mkfs.vfat for S4 variants
sudo losetup -f --show EVS-05.raw          # populate it, then detach
# … students then attach it READ-ONLY and image it:
sudo losetup -r -f --show EVS-05.raw
```

**What this gives `S2` for free:** a device to identify (`lsblk`, `losetup -l`, `blkid`), a
write-block step that is actually verifiable (`losetup -r`, `blockdev --getro`), an acquisition
with real hashing (`dc3dd hash=sha256`), a verification, a **correct** mount, and — the exercise
that matters — **the same mount done wrongly, with the hash re-computed to show it changed.**

**What it does not give**, and students must be told: no HPA, no DCO, no bad sectors, no SMART, no
serial number, no bus, no ATA command set, no partial-failure mode. **It models the procedure, not
the medium.** Existing routes for reference: FAT32 image (room 6) · carving target (room 8) ·
MBR/GPT structures (room 9) · `EVS-03` VMware memory pair (rooms 10–11). **This is the fifth.**

### 🟢 It also completes the S1 handling exercise's most important case

Rooms 6, 8, 9, 12 and 13 each supplied *"a technically correct instruction with the containment
step missing."* **This room supplies something worse and better: an instruction that actively
destroys the control taught two pages earlier.** Hash → mount rw → never re-hash. **That is the
strongest single item in the set, and it is demonstrable in five minutes.**

## 5. Lab design worth reusing

1. **🟢🟢 The audit trail (Task 2).** Seven settings, session recording, save every command's
   output. **No other room in the path teaches the examiner to log themselves**, and it is the
   habit that distinguishes an examiner from a tool operator. **Take it, add `history -a`, fix the
   time format, and make it `S2`'s first practical exercise** — before any evidence is touched.
2. **🟢 `df` won't show it, `lsblk` will.** A small, memorable, correct lesson about why the obvious
   command is the wrong one, with the honest generalisation to physical disks. **Keep verbatim.**
3. **🟢 `0 bad sectors replaced by zeros`.** The one line in the `dc3dd` output that separates
   "the copy finished" from "the copy is faithful". **Point at it explicitly.**
4. **🟢 Hash the device node, not just the file.** Correct, and commonly skipped.
5. **🟢 "Identify the device by size, not by number."** The room warns that loop numbering is not
   stable. **Right instinct, weak identifier** — teach matching on the backing file or serial
   instead, but keep the warning.
6. **🟢 Two lab machines, one for teaching and one for assessment** (Tasks 2 and 6), with an
   explicit instruction to shut the first down. Clean separation; worth copying.
7. **⚠️ The caveat in Task 1** — *"performance and timing… intentionally left behind to avoid the
   focus on the process itself"* — is honest scope-setting, and it is the right call for a 45-minute
   room. **But `S2` cannot make that omission**: imaging time drives the whole acquisition plan, and
   students will be asked about it.

### 🔴 Safety defect #6 — and the first that damages the *evidence* rather than the analyst

| room | defect |
|---|---|
| 6 · FAT32 | paste-recovered PowerShell into a live shell |
| 8 · File Carving | `binwalk -e` with no isolation (CVE-2022-4510) |
| 9 · MBR/GPT | edit and save the evidence image in place |
| 12 · Memory & Processes | dump live malware to the home directory, no containment |
| 13 · Memory & User Activity | `unzip` hostile OOXML in `~`; live C2 URL never flagged |
| **15 · Forensic Imaging** | **verify the hash, then mount the image read-write, then never re-verify** |

🟢 **The set is now complete and it has two halves**: rooms 6, 8, 12, 13 endanger **the analyst's
machine**; rooms 9 and 15 endanger **the evidence**. **That split is the structure of the `S1`
exercise** — *"who or what does this instruction put at risk?"* — and it was not visible until this
room. **Stop collecting. Write it.**

## 6. Question patterns

**8 questions across 7 tasks**, and three of them are "click to complete" — so **five real
questions**, which is thin for a 45-minute room.

**⚠️ Two are pure recall.** *"What command can be used to list all block devices in Linux OS?"*
(`lsblk`) · *"Which bash command displays all commands executed in a session?"* (`history`).

**🟢 Three require doing the work**, and they are correctly built:
- *"What is the MD5 hash of the image `exercise.img` located in `/home/analyst/`?"* — run the tool.
- *"Mount the image `exercise.img`… What is the content of the file `flag.txt` within it?"* —
  the full mount-and-browse procedure, verified by a value only obtainable by completing it.
- **Task 6, unassisted**: *"Create an image of the attached 1 GB loop device. What is the MD5 hash
  of the image?"* then *"Mount the image… what is the content of `flag.txt`?"* — 🟢 **a separate
  machine, no walkthrough, the whole workflow from scratch.** That is a proper practical
  assessment and the best-constructed one in fifteen rooms.

**🔴 But the assessment rewards the defect.** Task 6 asks for the MD5 **and then asks the student
to mount it** — with the room's own read-write command, which changes the image. **A student who
re-hashed after mounting would get a different value and conclude they had made a mistake.** The
assessment is only self-consistent because nobody checks twice.

🟢 **Our version of Task 6, with one sentence added:**
> *"Image the device, record the SHA-256, mount it and read `flag.txt`, then re-compute the
> SHA-256. Do the two values match? Explain."*

That is the same lab, the same five minutes, and it teaches the opposite lesson.

**🔴 Fifteenth room, no question whose answer is "cannot be determined."** Candidates here:

| the room could have asked | correct answer |
|---|---|
| *"`lsblk` reports 1 GB. Is that the whole disk?"* | **Cannot be determined** without `hdparm -N` and `--dco-identify` — an HPA or DCO hides capacity from the OS. |
| *"The hashes matched. Does that prove the evidence is unaltered?"* | **No** — it proves the copy matches the source *at the moment of imaging*. It says nothing about what happened before. |
| *"`0 bad sectors replaced by zeros`. Does that prove a complete copy?"* | **Of the visible LBA range, yes. Of the disk, not without the HPA/DCO check.** |

## 7. Figures we would need to draw

Figures present in the room: **none.** Every visual is a terminal transcript.

| # | what is needed | our SVG spec (one line) | priority |
|---|---|---|---|
| 1 | **what a read-write mount writes** | the image as a byte strip with four write sites marked and labelled: **`s_mnt_count`** and **`s_mtime`** (superblock, every rw mount) · **`s_last_mounted`** (the examiner's own path, on first access) · **journal replay** (if dirty) · **atime**, drawn scattered across the inode area with *"relatime still writes if atime > 1 day — always true on evidence"*; the hash shown **before and after, different**, at the two ends | **highest** |
| 2 | **the layered read-only stack** | four stacked bands — **hardware write blocker** (enforced, NIST-tested) · **`losetup -r`** (enforced by the loop driver) · **`blockdev --setro`** (advisory — drivers may write through) · **`mount -o ro`** (insufficient alone — journal replays) — each annotated with what it does and does not stop; caption *"only the top two are controls"* | **highest** |
| 3 | **the acquisition workflow as a chain of custody** | identify → document identity (`hdparm -I`, serial) → **check HPA/DCO** → write-block → image with on-the-fly hash → verify → **store, then work on a copy**; with the room's actual path drawn beside it and **three steps greyed out as omitted** | **high** |
| 4 | **HPA / DCO** | one drive drawn as a bar: **visible LBA range** accented, **hidden HPA** and **DCO-removed** regions shaded, with `hdparm -N`'s two return values arrowed at the boundary; caption *"a naive image stops at the first number"* | **high** |
| 5 | **the audit trail's two layers** | `script` transcript as a continuous ribbon vs `.bash_history` as discrete stamped entries, with a **crash marked on the timeline** and the history entries after it greyed out — captioned *"history writes at exit; the transcript writes continuously"* | medium |
| 6 | **image formats** | raw/dd · E01 · AFF4-L compared on four axes — compression, embedded case metadata, integrated hash, segment files — with **E01 marked "the interchange standard"** and AFF4-L "concurrent, not a replacement" | medium |

Figure 1 is the one that makes the defect undeniable. Figure 2 is the one students will still be
using in five years. Never their images (**D22**).

## 8. Fit against our material

### ✅ Part 1's mapping is correct — and understated

Mapped to **S2** / `S2-06` FTK Imager. Correct, but this room reaches **four** S2 rows, not one.
**Amend Part 1's entry** to: `S2-02` (write-blocking) · `S2-04` (hashing and verification) ·
`S2-06` (imaging tools) · `S2-07` (mounting for analysis).

### Rows this strengthens

- **`S2-06`** imaging tools — the room's six-tool table is the right shape; our currency column
  (§3) makes it teachable. **The recommendation our lab should adopt: Guymager or `ewfacquire` for
  the primary acquisition, `ddrescue` for damaged media, `dc3dd`/`dcfldd` as the "raw dd with
  hashing" teaching step, never plain `dd`.**
- **`S2-02`** write-blocking — the room supplies the concept; **we supply the layered stack (§7 #2)
  and the NIST CFTT finding**, which is the fact that makes the slide worth showing.
- **`S2-04`** hashing — **the room's method is right and its algorithm is wrong.** Keep hashing the
  device node; add SHA-256 and `sha256sum -c`.
- **`S2-07`** mounting — 🔴 **this row must now be rewritten around what NOT to do.** The corrected
  mount lines in §2.6, and the before/after hash demonstration, are the row.
- **`S1`** — the sixth safety defect, and the one that completes the analyst-vs-evidence split
  (§5). **Write the exercise.**
- **`EVS-05`** — the loop-device evidence route (§4). Free, self-contained, reusable across S2 and
  S4.

### Five things `S2` must do differently from the room

1. **Attach read-only before doing anything else** (`losetup -r`), and *show* the `RO` flag.
2. **Hash during acquisition** (`dc3dd hash=md5 hash=sha256 hlog=…`), not after.
3. **Mount `ro,noload,noatime,nodev,noexec`** — and demonstrate why, with hashes either side.
4. **Check HPA and DCO before imaging**, and document the result whether or not one is present.
5. **Record the device's identity** — `hdparm -I`, serial, model — before the first byte is copied.

### Minutes

`S2` currently carries `S2-06` at its existing length. Everything above is either a **correction**
to an existing row, a **demonstration** inside `S2-07` (five minutes, replacing content already
budgeted), or the **`EVS-05` lab**, which replaces whatever `S2`'s current hands-on was going to be
rather than adding to it. The HPA/DCO material is genuinely new but belongs as a **slide inside
`S2-02`**, not a row.

**No new rows. S2 stays at 220.**

**Running totals: S2 220 · S4 220 · S6 220 · S5 65 minutes overdrawn** (rooms 1–5, unchanged).
🔴 **Tenth room carrying the S5 overdraft unresolved.** It needs a structural re-split and no
further extraction will change it.

### Out of scope

Performance and imaging time — **the room explicitly excludes it and says so**; `S2` cannot.
Windows-side imaging (FTK Imager as a tool, not just a table row) — `S2-06`'s own content.
Remote and cloud acquisition — mentioned in one line of Task 5 and not taught. **No scope
conflict.**

### Still unresolved

**Browser forensics** — fifteenth room, still no `DECISIONS.md` row. **Decide it.**

## 9. Links

- Room: <https://tryhackme.com/room/forensicimaging>
- Room's stated prerequisites: Intro to Digital Forensics · DFIR: An Introduction ·
  Linux Fundamentals 1 · **Legal Considerations in DFIR**.
- Room's suggested follow-ups: Linux Forensics · Linux Fundamentals 2 · Linux Logs Investigation
  (the last is `linuxlogsinvestigations`, Priority 2 in our list).
- `mount(8)` <https://man7.org/linux/man-pages/man8/mount.8.html> ·
  `ext4(5)` <https://man7.org/linux/man-pages/man5/ext4.5.html> ·
  kernel ext4 doc (the "replays even when read only" line)
  <https://docs.kernel.org/admin-guide/ext4.html> ·
  ext4 superblock fields <https://docs.kernel.org/filesystems/ext4/super.html>
- `losetup(8)` <https://man7.org/linux/man-pages/man8/losetup.8.html> ·
  `blockdev(8)` <https://man7.org/linux/man-pages/man8/blockdev.8.html> ·
  `hdparm(8)` <https://man7.org/linux/man-pages/man8/hdparm.8.html>
- **NIST CFTT** — hardware write block (live, reports to Dec 2025)
  <https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/cftt-technical/hardware>
  · software write block (spec v3.0, 2003; last report 2008)
  <https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/cftt-technical/software>
- Software write-blocking on Linux, with the documented leak cases:
  <https://github.com/msuhanov/Linux-write-blocker/blob/master/README.md>
- Forensic mount options, worked: CIRCL
  <https://github.com/CIRCL/forensic-tools/blob/master/docs/mounting_ntfs.md>
- Kessler & Carlton, *A Study of Forensic Imaging in the Absence of Write-Blockers*, JDFSL 9(3)
  <https://commons.erau.edu/jdfsl/vol9/iss3/4/> — **assign this in `S2-02`**
- Tools: dc3dd <https://sourceforge.net/projects/dc3dd/files/dc3dd/> ·
  dcfldd <https://github.com/resurrecting-open-source-projects/dcfldd> ·
  Guymager <https://guymager.sourceforge.io/> ·
  libewf <https://github.com/libyal/libewf> ·
  GNU ddrescue 1.30 <https://man.archlinux.org/man/ddrescue.1.en>
- Bash history semantics <https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html>
  · `script(1)` <https://man7.org/linux/man-pages/man1/script.1.html>
- Imaging/partition tool currency: `Resources/THM/_TOOL_CURRENCY_2026-08-28.md` **block A**
