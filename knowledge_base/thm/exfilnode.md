---
room: ExfilNode
url: https://tryhackme.com/room/exfilnode
module: Advanced Endpoint Investigations — **challenge room** (Priority 2). Explicit continuation of
        **DiskFiltration** (room 21): same incident, second machine.
feeds: 🔴🔴 **This room is a scope collision, not a topic. It is 100 % Linux, and
       `design/scope_decisions.md` puts Linux/macOS forensics OUT of scope.** Resolved as **D38**
       in §8 — the exclusion holds, and one cross-platform contrast table lands in **S1**, where
       we already owe students the Windows-weighting disclaimer.
       Also **`S6-09`** (the two-machine case shape and the betrayal twist) and **D19**.
       🔴 **First of 22 rooms to contribute no evidence set** — `EVS-10` stays unallocated.
difficulty / time: **Medium** · 70 min · 1 task · 14 questions · Premium · 2,366 completions ·
                   66 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: the single task read in full — briefing, prerequisites, lab instructions and all 14
              question stems. 0 sections NOT READ.
              🟢 Room displays **no** credentials in its task text (split-view lab machine, no VM
              login published) — nothing to withhold under R8. First room in the Priority-2 set
              where that is true.
              ⚠️ **Answers NOT READ** — the lab machine was not started. As for rooms 18–21, §2 is
              reconstructed from the 14 question stems plus the room's own briefing. Where a stem
              is ambiguous about which artifact supplies the answer, that ambiguity is stated
              rather than resolved by guessing.
---

## 1. What the room teaches

**That a second machine is examined because the first machine's attribution is contestable — and
that the accomplice is also a suspect.** Everything else in this room is Linux plumbing; those two
ideas are the transferable content, and both are OS-independent.

🟢🟢 **The premise is the best single sentence in the Priority-2 set.** The room opens by naming the
defence:

> *"However, he could argue that he was framed as he did not own the workstation. So, to uncover the
> whole truth and gather all the possible undeniable evidence, the investigators turned their
> attention to Liam's personal workstation."*

**That is the attribution problem stated as a plot point.** DiskFiltration proved that *a* user
account on a *company* machine did the exfiltration. It could not prove *Liam* did, because the
company owned, imaged and administered the box and half a dozen people had a plausible route to that
account. The second machine exists precisely to close the gap the first one cannot. **We have been
looking for a way to make "what it does NOT prove" feel consequential rather than pedantic; this is
it — an entire second investigation motivated by one unprovable claim.**

🟢🟢 **The second idea is better still: the accomplice betrays Liam.** After the exfiltration is
complete, the external entity SSHes back into Liam's *personal* machine and installs a cronjob
(Q13, Q14). The room states it plainly — *"Liam thought the work was done, but the external entity
had other plans."* **This is a second incident nested inside the first**, and it flips the
investigative question halfway through, from *"prove Liam did it"* to *"who else is in here, and are
they still in here?"* No other room in the path does this. It is exactly the shape a real insider
case takes when the insider turns out to have been recruited rather than acting alone, and it is the
single best scenario idea we have extracted.

⚠️ **But the briefing then commits the opposite sin to DiskFiltration's.** Room 21 prejudiced the
case with behaviour (*"roaming around the critical server room"*). This one prejudices it with the
**conclusion**: *"It seems like the investigators not only revealed more about the external entity
Liam worked with but also exposed a betrayal: Liam was double-crossed."* **The student is told the
finding before being shown the artifact.** So the brief simultaneously models the best practice we
teach (state and test the alternative hypothesis) and the worst (announce the answer). 🟢 **That
makes it a better classroom exercise than either room alone** — §4.

**🔴🔴 And then there is the problem this room actually hands us: it is entirely Linux.** Fourteen
questions, fourteen Linux artifacts, an ext4 image, and a prerequisite list of four Linux rooms.
`design/scope_decisions.md` excludes Linux/macOS forensics by decision, `design/coverage_matrix.md`
repeats it, and `design/topic_map.md` contains no EXT row anywhere. **Nothing in this room is
directly teachable in eCDFP as written.** That is the whole reason the room needed a decision rather
than an intake — **§8, D38**.

**What the room gets wrong — and it is a lot, because Linux artifacts have moved further in three
years than Windows ones have:**

- 🔴🔴🔴 **`last -f /var/log/wtmp` is dead on current Linux.** Debian 13 and Ubuntu 25.04+ ship
  **no `last`, no `lastb`, no `lastlog`, and no `wtmp`/`btmp`/`lastlog` files at all.** The
  replacements are SQLite and **not installed by default**. §3 #2. This is the Linux twin of room
  21's `WordWheelQuery` finding, and it is larger — it removes an artifact *family*, not a key.
- 🔴🔴 **`/etc/timezone` does not exist on a fresh 2026 install** (Q2's likely answer source). §3 #4.
- 🔴🔴 **`grep /var/log/auth.log` is only conditionally right** — true on Ubuntu **Server** through
  26.04, false on Debian 12/13 and Ubuntu Desktop, which have no rsyslog and therefore no
  `auth.log` at all. §3 #1.
- 🔴🔴 **The room hands the student a *mounted* ext4 filesystem and never says read-only.** *"Liam's
  personal workstation's disk is mounted at `/mnt/liam_disk`… You can run commands on the mounted
  disk."* Against **E5**, that is an evidence-endangering defect — and it is the fourth one in the
  project, all four in disk work. §5.
- ⚠️ **It teaches students to suppress a signal.** The room pre-empts
  *"grep: /mnt/liam_disk/var/log/auth.log: binary file matches"* by telling them to use `grep -a`.
  **Binary content inside a text log is a finding**, not a nuisance — §5.4.
- ⚠️ **Autopsy 4.21.0**, which as of today is **exactly three years old to the day** (29 Aug 2023).
  Current is 4.23.1. §3 #9.

🟢 **One thing it gets conspicuously right, and it is a first.** Q12 asks which files are *"likely
timstomped"* — hedged, in the stem, by the room's own authors. **Twenty-two rooms in, that is the
closest any question has come to admitting an artifact has a limit.** It is still not a
"cannot be determined" question, so the tally in §6 does not move, but it deserves the credit.

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 14 question stems (see frontmatter). Eight blocks; the questions map
1 → 2.1, 2 → 2.2, 3/4/10 → 2.3, 5 → 2.4, 6/8/9/11 → 2.5, 7 → 2.6, 12 → 2.7, 13 → 2.1 + 2.6,
14 → 2.8.

### 2.1 Linux login records — an artifact family that is being deleted

- **What it is** — the record of who logged in, from where, and when. Q1 (*"When did Liam last
  logged into the system?"*) and Q13 (*"Which IP address was connected via SSH… a few hours after
  the exfiltration?"*).
- **Where it lives** — historically four files: **`/var/run/utmp`** (current sessions),
  **`/var/log/wtmp`** (login/logout history, read by `last`), **`/var/log/btmp`** (failed attempts,
  `lastb`), **`/var/log/lastlog`** (last login per user). Plus the text trail in
  **`/var/log/auth.log`** (Debian family) or **`/var/log/secure`** (RHEL family), and the binary
  **journal** at `/var/log/journal/<machine-id>/*.journal`.
  🔴🔴🔴 **On Debian 13 and Ubuntu 25.04+, the first four are gone** — see §3 #2. The successors are
  **`/var/log/wtmp.db`** (`wtmpdb`, SQLite) and **`/var/lib/lastlog/lastlog2.db`** (`lastlog2`,
  SQLite), and **neither package is installed by default**, so on a stock 2026 image there is
  usually *nothing there at all*.
- **What it proves** — that an authentication succeeded for a named account, from a source address,
  at a time. For Q13 the `auth.log`/journal line is the strong artifact, because OpenSSH logs the
  source IP and port and, on publickey auth, **the key fingerprint** — §3 #8.
- **What it does NOT prove** — 🔴🔴 **that the human named Liam was at the keyboard.** This is the
  entire premise of the room (§1) and it does not stop being true on the second machine: a login
  record attributes to an *account*, and an SSH login attributes to a *credential or key*. On a
  personal machine the inference is stronger than on a corporate one, but it is still an inference,
  and **Q13 proves the point by existing** — the very next login on this box is somebody else using
  Liam's access.
  🔴🔴 **That `last` reports "the last login" does not mean it reports *all* logins.** `lastlog`
  stores exactly one record per user — overwritten each time. A session that matters can be erased
  by the next legitimate login, with no gap left behind.
  🔴 **And absence proves nothing about the account.** `wtmp` and `btmp` are plain writable files:
  the classic anti-forensic move is to delete records selectively rather than truncate the file.
  ⚠️ **On a journald-only host, absence may mean rotation, not innocence** — journal retention is
  **size-driven, not time-driven** (§3 #3), so there is no defensible "the logs go back N days".
  The examiner must state the observed first and last journal timestamps and bound the claim to
  them.
- **How to parse it** — 🔴 **run the triage check before choosing a tool**:
  `ls -la /mnt/img/var/log/{wtmp*,btmp*,lastlog,auth.log,syslog} /mnt/img/var/log/journal/` — the
  answer to that one command decides everything else. Then: legacy `wtmp` with `last -f` (bring your
  own binary — your workstation may no longer ship one) or plaso's `utmp` parser; `wtmp.db` /
  `lastlog2.db` with any SQLite client, **no vendor parser needed**; the journal with
  `journalctl --file … --utc`; `auth.log` with `grep`. **`lslogins` is the util-linux survivor and
  reports last-use per account.**
- **Anti-forensics / false-positive caveat** — ⚠️ **the room's own instruction is the caveat.**
  Telling students to `grep -a` past *"binary file matches"* in `auth.log` trains them to walk past
  the most interesting thing in the file. NUL bytes in a text log mean something happened to that
  file — truncation, sparse-region overwrite, or injected content — and *that* is the finding. §5.4.

### 2.2 The system timezone on a dead Linux image

- **What it is** — the offset every local-time string on the image must be corrected by. Q2:
  *"What was the timezone of Liam's device?"*
- **Where it lives** — 🔴 **`/etc/localtime`, and it is a *symlink*** — the zone ID is the tail of
  its target under `/usr/share/zoneinfo/`. `localtime(5)`: *"Because the timezone identifier is
  extracted from the symlink target name of /etc/localtime, this file may not be a normal file or
  hardlink."* **`/etc/timezone` is the Debian-family text file the room is almost certainly asking
  for, and it is being retired** — Debian's `tzdata` now *"Only create /etc/timezone if it already
  exists"*, and Ubuntu 26.04's `tzdata` ships no files under `/etc` at all. §3 #4.
- **What it proves** — how the running system rendered local time, and therefore how to read every
  local-time artifact on the image: `auth.log` lines, `syslog`, `setupapi`-equivalent text logs,
  and anything a user saw in a GUI.
- **What it does NOT prove** — 🔴🔴 **what timezone was in effect when a given historic record was
  written.** `/etc/localtime` is current state. A machine that travelled, or whose timezone was
  changed once, has records written under an offset the image no longer declares — and **there is
  no per-record timezone stamp in `auth.log` to catch it**. ⚠️ **A timezone change is itself an
  anti-forensic technique** (`timedatectl set-timezone`, `date -s`, `hwclock`), and it leaves its
  trace in the logs rather than in the config file.
  🔴 **And if `/etc/localtime` is absent the system behaved as UTC** — absence is a value, not a gap.
  ⚠️ If `/etc/timezone` and the `/etc/localtime` target **disagree**, `/etc/localtime` wins, and
  **the disagreement is itself reportable** — it usually means someone edited one by hand.
- **How to parse it** — `ls -l /mnt/img/etc/localtime` and read the target; `cat
  /mnt/img/etc/timezone` as corroboration only. If `/etc/localtime` is a regular file rather than a
  symlink the zone name is unrecoverable from the path — hash it against `/usr/share/zoneinfo/**` to
  identify it.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the journal sidesteps the whole problem and
  that is the teaching point.** systemd's journal stores wall-clock as **microseconds since the Unix
  epoch** — no timezone at all — so `journalctl` renders records in the *examiner's* timezone unless
  told otherwise. **`journalctl --utc` is mandatory for any timeline**, and forgetting it produces a
  timeline that is silently wrong by the analyst's own offset. This is the same class of error as
  room 21's `setupapi.dev.log` local-time trap (**I4**), arriving from the opposite direction: there
  the artifact was local and everything around it was UTC; here the artifact is epoch-absolute and
  the *renderer* introduces the local time.

### 2.3 USB attach and detach — and Linux has no USBSTOR

- **What it is** — evidence that a specific removable device was connected, and when it was removed.
  Q3 (serial), Q4 (connect time), Q10 (disconnect time).
- **Where it lives** — 🔴🔴 **only in the kernel log.** `announce_device()` in
  `drivers/usb/core/hub.c` emits, at `KERN_INFO`:
  `New USB device found, idVendor=…, idProduct=…, bcdDevice=…` then
  `New USB device strings: Mfr=…, Product=…, SerialNumber=…` then separate
  `Manufacturer: …`, `Product: …`, **`SerialNumber: <value>`** lines. Removal is one line from
  `usb_disconnect()`: `USB disconnect, device number %d`.
  Those land in the **journal**, and additionally in **`/var/log/kern.log`** and
  **`/var/log/syslog`** *only where rsyslog exists* (§3 #1).
- **What it proves** — that a device presenting that VID/PID/serial was enumerated by this kernel at
  that time, and that *a* device holding that device number was later disconnected.
- **What it does NOT prove** — 🔴🔴🔴 **this is the block that justifies the whole cross-platform
  contrast in D38, so state all four limits:**
  1. 🔴 **`SerialNumber=3` is not a serial number.** In the *"New USB device strings"* line the
     values are **string-descriptor indices**. The real serial is the separate `SerialNumber:` line.
     A student who greps the wrong line reports an integer as a device identity.
  2. 🔴🔴 **A device with no serial descriptor produces no `SerialNumber:` line at all** —
     `show_string()` returns early on NULL. Many cheap flash drives ship without one. **Absence is
     not evidence of absence of a device; it is evidence of a cheap device.** Windows fabricates an
     instance ID in this case and flags it with the `&` convention (room 21, §2.1); **Linux simply
     omits the line, so there is not even a marker that identity was unavailable.**
  3. 🔴🔴 **The disconnect line carries no serial and no VID/PID — only a device number**, which the
     kernel reuses. Attributing a removal to *this* stick requires correlating the `usb N-M:`
     bus/port prefix and device number back to the earlier connect block. **Across a reboot the
     correlation can be genuinely ambiguous, and Q10 cannot be answered honestly without it.**
  4. 🔴🔴 **There is no persistent Linux equivalent of `USBSTOR`.** `/sys` and `/run/udev` are
     volatile and absent from a dead image; `lsusb` is a live-system tool; `/etc/udev/rules.d`
     holds *rules, not history*. **The only surviving artifact is a log that rotates by size.**
     A stick used daily for a year may have exactly zero surviving records.
- **How to parse it** — `grep -E 'SerialNumber:|idVendor|USB disconnect' /mnt/img/var/log/kern.log`
  where rsyslog existed; otherwise `journalctl --file /mnt/img/var/log/journal/*/system.journal -k
  --utc`. ⚠️ **Always `--utc`** (§2.2). Correlate connect and disconnect on the `usb N-M:` prefix,
  not on the serial, because the disconnect line has none.
- **Anti-forensics / false-positive caveat** — ⚠️ **journal retention is the anti-forensic, and
  nobody has to do anything.** `journald.conf` defaults are `SystemMaxUse=` 10 % of the filesystem
  capped at 4 G and **`MaxRetentionSec=0`, i.e. time-based retention off**. On a busy host a USB
  insertion can age out in days. 🔴 And if `/var/log/journal/` does not exist the journal is
  **volatile** and did not survive the last reboot — **check for that directory before concluding
  anything from an absence.**

### 2.4 Shell configuration as an artifact — the alias that hides the command

- **What it is** — a name the user defined so a long command could be run as a short word. Q5:
  *"What command was executed when Liam ran 'transferfiles'?"*
- **Where it lives** — `~/.bashrc`, `~/.bash_profile`, `~/.bash_login`, `~/.profile`,
  `~/.bash_logout`, and system-wide `/etc/profile`, `/etc/profile.d/*`, `/etc/bash.bashrc`. An
  alias, a shell function, or a `$PATH` shim in `~/.local/bin` all produce the same effect.
- **What it proves** — 🟢🟢 **the user's own definition of what a word means on this machine** —
  which turns an unreadable history line into a readable one. `.bash_history` records
  *`transferfiles`*; only `.bashrc` says what that ran. **This is a resolution artifact: it decodes
  another artifact rather than standing alone**, and that relationship is worth naming in class,
  because it is the same relationship `$MFT` has to a `$UsnJrnl` entry.
- **What it does NOT prove** — 🔴🔴 **that the alias had this definition when the command was run.**
  `.bashrc` is current state with one mtime; the history line is undated (§2.5). **An alias edited
  after the fact silently rewrites the meaning of every historic invocation**, and nothing in either
  file records the change. ⚠️ **Nor does a definition prove execution** — an alias in `.bashrc` that
  never appears in history was never run, as far as this evidence goes. 🔴 **And an alias defined in
  a shell session and never written to a file leaves no trace at all.**
  ⚠️ Definition order matters: a later definition wins, and `/etc/profile.d/` can be shadowed by
  `~/.bashrc`. **Reporting "the alias" without saying which file it came from is an incomplete
  finding.**
- **How to parse it** — read the files; `grep -rn 'alias\|^[a-z_]*()' /mnt/img/home/<user>/.*rc
  /mnt/img/etc/profile.d/`. Record the **file mtime and ctime** alongside the definition — that pair
  is the only dating evidence available, and per §2.7 the ctime is the harder one to forge.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **shell config is also first-rank persistence,
  not just documentation** (ATT&CK **T1546.004**, *Event Triggered Execution: Unix Shell
  Configuration Modification*). A line appended to `~/.bashrc` runs on every interactive login.
  **The examiner reads these files twice: once to decode the user's shorthand, once to look for
  someone else's implant** — and Q14 proves the second read is warranted on this very machine.

### 2.5 `.bash_history` — the intent artifact, and the silent-omission trap

- **What it is** — the commands the user typed. The single highest-yield artifact in this room:
  Q6 (the transfer command), Q8 (*"Which directory was the user in when they created the file
  'mth'?"*), Q9 (the payment amount), Q11 (the `.hidden/` path).
- **Where it lives** — `~/.bash_history` by default (`$HISTFILE`), plus `~/.zsh_history`,
  `~/.python_history`, `~/.mysql_history`, `~/.psql_history`, `~/.lesshst`, `~/.viminfo` for other
  interpreters. Root's is `/root/.bash_history` and is frequently the interesting one.
- **What it proves** — 🟢🟢 **intent, in the subject's own words, in order.** Q9 is the extreme case:
  the payment amount is a *motive* fact recovered from a shell artifact. Nothing else on the disk
  says why.
- **What it does NOT prove** — 🔴🔴🔴 **this is the most important "does NOT prove" box in the note,
  because every one of these limits is a default, not a hardening step:**
  1. 🔴🔴 **Absence of a command is not evidence the command was not run.** Ubuntu ships
     **`HISTCONTROL=ignoreboth`** in `/etc/skel/.bashrc`, and bash's manual is explicit:
     *"lines which begin with a space character are not saved in the history list."* **One leading
     space suppresses a command permanently, and leaves no gap, no marker and no count anomaly.**
     `ignoredups` additionally collapses repeats, destroying repetition counts.
  2. 🔴🔴 **There are no timestamps.** `HISTTIMEFORMAT` is **not** set by default on Debian/Ubuntu —
     there is an open Launchpad request to add it, which is itself the proof. Without it,
     `.bash_history` is an *ordered* list, not a *dated* one. **Q1 and Q13 are timed; Q6, Q8, Q9 and
     Q11 are not, and cannot be — the room's own question set demonstrates the limit.**
  3. 🔴🔴 **Q8 is answered by inference, not by the artifact.** `.bash_history` does not record the
     working directory. The only route to *"which directory was the user in"* is to read a `cd`
     earlier in the file and assume no intervening change — **which fails if a `cd` was suppressed
     by limit 1, or if the commands came from two interleaved shells.** 🟢 This is the best
     "cannot be determined" candidate in the room and §6 uses it.
  4. 🔴 **Interleaving.** With `histappend` (Ubuntu default) several concurrent shells append to one
     file **on exit**, so the file's order is *exit order*, not execution order. Without
     `histappend` the last shell to exit **overwrites** the file and destroys everything earlier.
  5. ⚠️ **Writes happen on clean exit.** A killed shell, a reset box, or a session still open at
     acquisition loses everything since the last exit. **A live-response `history` dump captures
     what the file never will** — which is a memory-vs-disk argument students meet again in S2.
- **How to parse it** — `cat`, in order; correlate against the timed artifacts (`auth.log`/journal
  session open and close, `sudo` lines, cron entries) to bracket each block of commands between two
  known times, and against the filesystem timestamps of files the commands touched (§2.7).
  **That correlation is the exercise**, and it is the honest substitute for the timestamps the file
  does not have. Plaso's `bash_history` and `zsh_extended_history` parsers put it on a timeline.
- **Anti-forensics / false-positive caveat** — ⚠️ `history -c`, `unset HISTFILE`,
  `ln -s /dev/null ~/.bash_history`, `kill -9 $$` — all trivial, all common, none of which the room
  exercises. 🔴 **But note the asymmetry that makes the artifact worth having anyway:** a file that
  has been cleared is *itself* a finding (an empty or zero-length history on an account with months
  of login records is an anomaly), whereas `ignorespace` produces a file that looks entirely normal.
  **The sloppy anti-forensic is visible; the default one is not.** ATT&CK **T1552.003**, which
  🔴 **is now named *Unsecured Credentials: Shell History*, not "Bash History"** — §3 #7.

### 2.6 Remote-host and name-resolution artifacts

- **What it is** — the link between the hostname a command used and the address the traffic went to.
  Q7: *"What is the IP address of the domain to which Liam transferred the files to?"* — and, from
  the other direction, Q13's inbound SSH source.
- **Where it lives** — ⚠️ **the room does not say, and the honest answer is "one of several"**:
  **`/etc/hosts`** (a manual entry is itself suspicious and is the most likely source for a
  question with a single deterministic answer), **`/etc/resolv.conf`** (which resolver was used),
  **`~/.ssh/known_hosts`** (host keys recorded per hostname *and* per address),
  **`~/.ssh/config`** (a `Host` alias mapping a short name to a real address),
  the **journal** (`systemd-resolved` query logging, if enabled), and the command in
  `.bash_history` itself if the user typed a literal IP.
  🔴 **NOT VERIFIED which of these the room intends** — the lab machine was not started, and
  guessing would put a wrong path on a slide.
- **What it proves** — that this host had a configured or cached mapping from that name to that
  address at some point.
- **What it does NOT prove** — 🔴🔴 **that the transfer went to that address.** A resolution artifact
  proves *name → address*; it does not prove a connection, a byte transferred, or that the mapping
  was in force at the moment of the transfer. **Only network evidence proves the transfer**, and
  this room has none — which is the same gap room 21 had, on the other machine.
  🔴 **DNS is time-variant by design.** An A record that resolves to X today resolved elsewhere last
  month; a cached or `/etc/hosts` mapping recorded *now* is not evidence about *then*. ⚠️ And a
  hostname behind a CDN or a shared host resolves to an address that serves thousands of unrelated
  sites — **an IP is not an identity**.
  ⚠️ **`known_hosts` is hashed by default on Debian/Ubuntu (`HashKnownHosts yes`)**, so it usually
  cannot be read straight off; it can only be *tested* against a candidate host you already suspect.
  🟢 That inverts its use: it is a confirmation tool, not a discovery tool, and saying so is a good
  five-minute lesson in the difference.
- **How to parse it** — read `/etc/hosts`, `/etc/resolv.conf`, `~/.ssh/config`; test candidate names
  against hashed `known_hosts` with `ssh-keygen -F <host> -f known_hosts`. **Record which file the
  answer came from** — the four sources have very different evidential weight and a finding that
  does not name its source cannot be weighed.
- **Anti-forensics / false-positive caveat** — 🔴 **a manual `/etc/hosts` entry is an
  attacker-friendly artifact in both directions**: it is strong evidence of deliberate targeting
  when present, and trivially removable. ⚠️ Its **mtime/ctime pair** (§2.7) is the only dating
  available and should be reported with it.

### 2.7 ext4 inode timestamps, and what "likely timestomped" actually means

- **What it is** — the four inode times and the inconsistencies between them. Q12: *"Which files are
  likely timstomped in this `.hidden/` directory"*. Q11's `.hidden/` folder is ATT&CK **T1564.001**,
  🔴 now under tactic **Stealth** — §3 #7.
- **Where it lives** — in the ext4 inode: `i_atime`, `i_ctime`, `i_mtime`, `i_dtime`, and
  **`i_crtime` at offset `0x90`** with `i_crtime_extra` at `0x94` carrying the nanoseconds.
  🔴 **`0x90` is past the end of a 128-byte inode**, so a filesystem formatted with 128-byte inodes
  **physically cannot hold crtime or sub-second precision.** Current `mke2fs` defaults to 256 bytes
  — *"the default inode size is 256 bytes for all file systems, except for the GNU Hurd"* — but an
  old or embedded image may not, **and on such an image Q12 is unanswerable.**
- **What it proves** — that the inode's recorded times are, or are not, mutually consistent with
  normal filesystem behaviour.
- **What it does NOT prove** — 🔴🔴 **that a file *was* timestomped. "Likely" is the right word and
  the room chose it** (§1). Take the four heuristics one at a time:
  - **mtime or atime earlier than crtime** — the strongest signal, because a file cannot be modified
    before it was created. 🟢 Still an *inconsistency*, not a confession: restores, `rsync -a`,
    `tar -p` extraction and container-image layers all legitimately produce it.
  - **ctime much later than mtime** — suggestive, and it works because `utimensat(2)` has no ctime
    parameter: *"The status change time (ctime) will be set to the current time, even if the other
    time stamps don't actually change."* **`touch` cannot set ctime.** But a `chmod`, a `chown`, a
    hardlink change or an xattr write moves ctime for entirely innocent reasons.
  - **nanosecond fields zeroed** — a real signal, since `touch -d "2021-01-01 00:00:00"` writes a
    whole second while normal activity does not. ⚠️ **But soft in both directions:** `touch -r`
    copies a reference file's non-zero nsec, and `touch -d` with a fractional string preserves
    precision. **Absence of the signal proves nothing.**
  - 🔴 **"inode number ordering vs timestamps" — NOT VERIFIED, and do not teach it.** I asked for a
    citation and none was found in primary or strong-DFIR sources. It is also physically shaky:
    ext4's Orlov/flex_bg allocator spreads inodes by directory rather than allocating them
    monotonically, so the premise may simply be false.
  - 🔴🔴 **And the load-bearing correction: crtime and ctime CAN be forged.** Hal Pomeranz, opening
    a 2024 post specifically to kill this claim: *"I was frustrated after reading yet another person
    claiming (incorrectly) that you cannot set `ctime` and `btime` in Linux file systems."*
    `debugfs -w` with `set_inode_field` writes inode fields directly, **on a mounted filesystem**.
    **So the correct phrasing for a report is "inconsistent with normal filesystem behaviour", never
    "proof of tampering"** — which is exactly the D20 criterion-4 distinction, arriving as a
    technical fact rather than a style rule.
- **How to parse it** — 🔴 **the "you must use `debugfs` because `stat` cannot show crtime" premise
  is stale by seven years.** `statx()` (Linux 4.11+) exposes `STATX_BTIME`, ext4 wires `i_crtime`
  into it, and GNU coreutils **8.31** (2019) added it: *"stat now prints file creation time when
  supported by the file system."* Current coreutils is **9.11** (April 2026), `%w`/`%W`. So
  **`stat` prints a real `Birth:` line** on any modern system. `debugfs -R 'stat <131074>'
  /dev/sdXN` (**angle brackets required for the inode-number form**; read-only by default without
  `-w`) is still the right tool for the raw `seconds:extra` hex pairs — and note Pomeranz's decoding
  rule that the low two bits of the extra field are *not* nanoseconds, so divide by 4.
  🟢 **TSK `istat` shows it as `File Created:` and Autopsy exposes a Created Time column**, so a
  GUI-only student can see the field.
- **Anti-forensics / false-positive caveat** — ⚠️ **the ext4 journal is a weak `$LogFile` analogue**:
  inode 8, holding recent copies of metadata blocks, readable with `debugfs -R logdump` or TSK's
  `jls`/`jcat`. 🔴 **Its retention is transaction-volume, not time** — a fixed-size circular log
  (~128 MB by default) that wraps, so the window is minutes on a busy host and days on a quiet lab
  image. And `data=ordered`, the default, journals **metadata only** — perfect for timestamps,
  useless for content. **Treat it as opportunistic corroboration, never as NTFS `$LogFile`.**
  🟢 Assign **Kroll, *"Breaking Time: Methods, Artifacts, and Forensic Detection of Timestomping on
  FAT32, Ext3, and Ext4 File Systems"*, SANS, 23 Oct 2025** as the reading — ⚠️ the PDF body was
  **NOT READ** (robots-blocked), so cite it as a reading-list item, not as a source for a claim.

### 2.8 cron, and the rest of Linux persistence

- **What it is** — the scheduled job the external entity left behind. Q14: *"Which cronjob did the
  external entity set up inside Liam's machine?"* ATT&CK **T1053.003**, tactics **Execution,
  Persistence, Privilege Escalation**.
- **Where it lives** — **`/var/spool/cron/crontabs/<user>`** on Debian/Ubuntu but
  **`/var/spool/cron/<user>`** on RHEL/Fedora; plus **`/etc/crontab`**, **`/etc/cron.d/*`** and
  **`/etc/cron.{hourly,daily,weekly,monthly}`**. 🔴 **`/etc/crontab` and `/etc/cron.d` entries carry
  a `user` field and user crontabs do not** — six fields plus command versus five plus command.
  **A student who miscounts reads the username as part of the schedule and reports the wrong
  command.**
- **What it proves** — that a job was *configured* to run as a named user on a schedule.
- **What it does NOT prove** — 🔴🔴 **that it ever ran.** A crontab entry is configuration.
  Execution evidence is separate and lives in the log: cron logs to syslog facility `cron` at
  `-L 1` (*"log the start of all cron jobs"*, the default) as
  `CRON[12345]: (root) CMD (/path/to/thing)`, with PAM contributing separate
  `pam_unix(cron:session)` lines. 🔴 **Which means that on a host without rsyslog the execution
  evidence is in the binary journal only**, and if the journal is volatile or has rotated, **a
  configured job with no execution record is entirely unremarkable.**
  🔴 **Nor does it prove who installed it.** The spool file's owner is the *target* user, not the
  author. Attribution needs the file's mtime/ctime (§2.7) correlated against the SSH session in
  §2.1 — **which is precisely why Q13 and Q14 are adjacent, and the room deserves credit for
  ordering them that way.**
  ⚠️ **And cron is not the whole answer.** **systemd timers** now carry most distribution periodic
  work and are equally usable for persistence: `/etc/systemd/system/*.timer` (the high-value
  location — *"System units created by the administrator"*), `/run/systemd/system`,
  `/usr/lib/systemd/system`, and per-user `~/.config/systemd/user/`. **A `.timer` does nothing
  without its matching `.service`, so both files must be collected.** 🔴 **An examiner who greps
  only cron misses this entire class**, and the room's question set — which asks only about cron —
  would let a student leave believing cron is the answer.
- **How to parse it** — read the spool files (they are plain text); `journalctl -u cron --utc`
  **not** `_COMM=cron`, because `-u` also captures the *output of jobs running in the unit's
  cgroup* while `_COMM` matches only the daemon. ⚠️ The unit is `cron.service` on Debian/Ubuntu and
  `crond.service` on RHEL — **a copied command fails across families.** Then sweep the rest:
  `~/.bashrc`/`~/.profile`/`/etc/profile.d/` (§2.4), `/etc/rc.local` (still functional via
  `systemd-rc-local-generator`, though systemd calls it *"strongly recommended to avoid"*),
  `/etc/init.d/`, `/etc/update-motd.d/`, at jobs in `/var/spool/cron/atjobs`, and
  `~/.config/autostart/` on desktop images.
- **Anti-forensics / false-positive caveat** — ⚠️ **the crontab spool is not user-writable by hand**
  — the directory is group-`crontab` and `crontab(1)` is setgid, so entries normally arrive through
  the tool. 🔴 **An entry whose file mtime does not match any `crontab -e` session, or a spool file
  with anomalous ownership, indicates direct filesystem write rather than normal use** — a finding
  in its own right. ⚠️ **Exact octal modes NOT VERIFIED** — the man page states the enforcement
  model in prose without printing them; `ls -la` the directory on our own image before putting a
  number on a slide.

## 3. Tools and commands

The room is deliberately shell-only — *"All the questions in this room can be answered by running
commands on the mounted disk."* Autopsy is offered and optional.

| purpose | the room's command | note |
|---|---|---|
| search auth events | `grep -i -a "pattern" /mnt/liam_disk/var/log/auth.log` | ⚠️ `-a` is taught as a workaround, not a finding — §5.4 |
| open the case | `cd /home/ubuntu/autopsy/autopsy-4.21.0/bin && ./autopsy --nosplash` | 🔴 4.21.0 is three years old to the day — #9 |
| login history | *(implied)* `last -f …/var/log/wtmp` | 🔴🔴🔴 dead on current Linux — #2 |
| timezone | *(implied)* `cat …/etc/timezone` | 🔴🔴 gone on fresh 2026 installs — #4 |
| USB identity | *(implied)* `grep SerialNumber …/var/log/kern.log` | ⚠️ conditional on rsyslog — #1 |
| shell history | `cat …/home/<user>/.bash_history` | ⚠️ undated and silently lossy — #5 |
| timestamps | *(implied)* `debugfs -R 'stat <inode>' …` / `stat` | 🔴 the "stat can't show crtime" premise is stale — #6 |
| cron | *(implied)* `cat …/var/spool/cron/crontabs/<user>` | ⚠️ cron alone is an incomplete sweep — §2.8 |

**Commands our own material should use instead** — all of these are corrections, not additions:

```bash
# 0. TRIAGE FIRST — this one command decides which of the artifacts below even exist
ls -la /mnt/img/var/log/{auth.log,syslog,kern.log,wtmp,btmp,lastlog,wtmp.db} \
       /mnt/img/var/log/journal/ /mnt/img/var/lib/lastlog/

# 1. timezone — the symlink target is authoritative, /etc/timezone is corroboration only
ls -l /mnt/img/etc/localtime

# 2. logins, journald path — ALWAYS --utc
journalctl --file /mnt/img/var/log/journal/*/system.journal --utc SYSLOG_FACILITY=4

# 3. sshd — _COMM=sshd now UNDER-COLLECTS (see #8)
journalctl --file … --utc _COMM=sshd _COMM=sshd-session _COMM=sshd-auth

# 4. USB — correlate connect and disconnect on the bus/port prefix, not the serial
journalctl --file … --utc -k | grep -E 'idVendor|SerialNumber:|USB disconnect'

# 5. ext4 creation time — stat works; debugfs is for the raw hex pairs
stat /mnt/img/path/to/file                     # prints a real Birth: line
debugfs -R 'stat <131074>' /dev/loop0p1        # angle brackets required; read-only by default

# 6. cron execution, not just configuration — -u, never _COMM
journalctl --file … --utc -u cron
```

### CURRENCY CHECK

| # | claim as the room teaches it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"`/var/log/auth.log` is where authentication events are"* | 🔴🔴 **Conditionally true — and the condition is the lesson.** Still written on **Ubuntu Server through 26.04 LTS** (rsyslog `8.2512.0-1ubuntu4.1` is in the 26.04 live-server and cloud manifests, and `50-default.conf` still routes `auth,authpriv.* → /var/log/auth.log`). **But Debian dropped rsyslog from the default install at Debian 12** — *"From bookworm, `rsyslog` is no longer installed by default"* — so Debian 12/13 have **no `auth.log`, no `syslog`, no `kern.log`**, only the journal. Ubuntu **Desktop** 26.04's manifest likewise carries no rsyslog line (⚠️ moderate confidence — verify on a real desktop image). **Teach the triage check, not the path.** | [Debian 12 rel. notes §5.1.7](https://www.debian.org/releases/bookworm/amd64/release-notes/ch-information.en.html) · [Ubuntu 26.04.1 live-server manifest](https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest) · [rsyslog 50-default.conf](https://raw.githubusercontent.com/rsyslog/rsyslog-pkg-ubuntu/master/rsyslog/noble/v8-stable/debian/50-default.conf) |
| 2 | *"`last -f /var/log/wtmp` gives login history"* | 🔴🔴🔴 **DEAD on Debian 13 and Ubuntu 25.04+ — the biggest Linux finding in the project.** Debian 13 release notes: *"The **util-linux** package no longer provides the `last` or `lastb` commands, and the **login** package no longer provides `lastlog`… these files will not be usable after 2038… and the upstream developers do not want to change the file formats."* Reason is Y2038, not deprecation-by-fashion. Ubuntu 26.04 ships **no package providing `/usr/bin/lastlog`** and **no package shipping `/var/log/wtmp` or `/var/log/btmp`**; systemd there is built **without utmp** (*"In Ubuntu, systemd is no longer built with utmp support"*), so `/run/utmp` is not created and **`who` and `w` return nothing**. Successors **`wtmpdb`** (`/var/log/wtmp.db`, SQLite) and **`lastlog2`** (`/var/lib/lastlog/lastlog2.db`, SQLite) are **NOT installed by default** on either distro. **Net effect: on a stock 2026 image the login-history artifact family is simply absent, and the journal is all you have.** ⚠️ The corollary nobody expects — **your analysis workstation may no longer ship a `last` binary either**, so bring a parser. | [Debian 13 rel. notes §5.1.9](https://www.debian.org/releases/stable/release-notes/issues.html) · [Ubuntu 25.04 rel. notes](https://documentation.ubuntu.com/release-notes/25.04/) · [Ubuntu contents: lastlog](https://packages.ubuntu.com/search?searchon=contents&keywords=lastlog&mode=exactfilename&suite=resolute&arch=amd64) · [wtmpdb(8)](https://manpages.debian.org/unstable/wtmpdb/wtmpdb.8.en.html) · [lastlog2(8)](https://manpages.debian.org/unstable/lastlog2/lastlog2.8.en.html) |
| 3 | *(implicit)* "the logs cover the relevant period" | 🔴🔴 **Journal retention is size-driven, not time-driven.** `journald.conf(5)`: `SystemMaxUse=` defaults to **10 % of the filesystem, capped at 4 G**; **`MaxRetentionSec=`** has *"the default of 0 (which turns off this feature)"*. **There is no defensible "the logs go back N days."** The examiner must state the observed first and last journal timestamps and bound every negative claim to them. ⚠️ And `Storage=` is compile-time-defaulted — **NOT VERIFIED** whether `/var/log/journal/` exists on a stock Debian 13 / Ubuntu 26.04 image; if it does not, the journal was **volatile** and did not survive the last reboot. One-command check on the image. | [journald.conf(5)](https://man7.org/linux/man-pages/man5/journald.conf.5.html) · [systemd-journald.service(8)](https://man7.org/linux/man-pages/man8/systemd-journald.service.8.html) |
| 4 | *"the timezone is in `/etc/timezone`"* | 🔴🔴 **Gone on fresh 2026 installs.** Debian `tzdata` changelog: `2022g-3` *"Stop creating /etc/timezone"*, then `2024b-5` **"Only create /etc/timezone if it already exists"**; the removal was scheduled for *"Debian 13 'Trixie'"*. Ubuntu 26.04's `tzdata` ships **no files under `/etc`**. Ubuntu's 25.04 notes speak of it in the past tense. **`/etc/localtime` — a symlink into `/usr/share/zoneinfo/` — is authoritative**, is what `timedatectl` reads and writes, and *"If /etc/localtime is missing, the default 'UTC' timezone is used."* 🟢🟢 Journal records carry **no timezone at all** (µs since the Unix epoch), so **`journalctl --utc` is mandatory** for a timeline. | [Debian tzdata changelog](http://metadata.ftp-master.debian.org/changelogs/main/t/tzdata/stable_changelog) · [localtime(5)](https://man7.org/linux/man-pages/man5/localtime.5.html) · [timedatectl(1)](https://man7.org/linux/man-pages/man1/timedatectl.1.html) · [Journal File Format](https://systemd.io/JOURNAL_FILE_FORMAT/) |
| 5 | *(implicit)* "`.bash_history` records what was typed" | 🔴🔴 **True, minus everything a default install removes.** Ubuntu's `/etc/skel/.bashrc` sets **`HISTCONTROL=ignoreboth`**, and bash's manual is explicit: *"lines which begin with a space character are not saved in the history list."* **A leading space suppresses a command with no trace.** `HISTTIMEFORMAT` is **not** set by default — an open Launchpad request to add it is the proof — so **there are no timestamps**. And *"When a shell with history enabled exits, the last $HISTSIZE lines are copied…"* — writes happen **on clean exit**, not per command. ⚠️ Exact `HISTSIZE`/`HISTFILESIZE` values **NOT VERIFIED** (Launchpad/Salsa robots-blocked); read them off the image, which is per-image evidence anyway. | [Bash History Facilities](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html) · [Bash Variables](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html) · [Launchpad #2039508](https://bugs.launchpad.net/ubuntu/+source/bash/+bug/2039508) |
| 6 | *(implicit)* "you need `debugfs` because `stat` cannot show creation time" | 🔴 **Stale by seven years.** `statx()` (Linux 4.11+) exposes `STATX_BTIME`; ext4 populates it from `i_crtime`; GNU coreutils **8.31** (2019-03-10) NEWS: *"stat now prints file creation time when supported by the file system, on GNU Linux systems with glibc >= 2.28 and kernel >= 4.11."* Current coreutils **9.11 (April 2026)**, `%w`/`%W`, *"- if unknown"*. 🟢 TSK `istat` shows it as **`File Created:`** and Autopsy exposes a **Created Time** column, so a GUI-only student can see it. 🔴 **But `i_crtime` sits at inode offset `0x90`**, so a **128-byte-inode** filesystem cannot hold it or sub-second precision — `mke2fs` defaults to **256 bytes** today, and on an older image Q12 is unanswerable. 🔴🔴 **And crtime/ctime are forgeable**: Pomeranz, *"I was frustrated after reading yet another person claiming (incorrectly) that you cannot set `ctime` and `btime`"* — `debugfs -w` + `set_inode_field`, **even on a mounted filesystem**. | [coreutils NEWS](https://raw.githubusercontent.com/coreutils/coreutils/master/NEWS) · [stat(1)](https://man7.org/linux/man-pages/man1/stat.1.html) · [ext4 inode layout](https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html) · [mke2fs(8)](https://man7.org/linux/man-pages/man8/mke2fs.8.html) · [Pomeranz, *More on EXT4 Timestamps and Timestomping*](https://righteousit.com/2024/09/04/more-on-ext4-timestamps-and-timestomping/) |
| 7 | ATT&CK mapping for this room's chain | 🔴 **Three defects, all in our own repo's likely wording.** ATT&CK Enterprise is **v19.2, released 6 Aug 2026** (major v19 was 28 Apr 2026). **(a) T1552.003 has been RENAMED from "Bash History" to *Shell History*** (v2.0, 24 Oct 2025). **(b) T1070.006 Timestomp and T1564.001 Hidden Files and Directories both now sit under tactic *Stealth*, not "Defense Evasion"** (both v2.0, 12 May 2026) — consistent with the TA0005 → TA0112 split we already carry. **(c) `scp` is encrypted, so an scp upload is T1048.002 (Asymmetric Encrypted), NOT T1048.003** — `.003` is *Unencrypted Non-C2* and covers plain-HTTP/FTP `curl`/`wget` only. **Lumping "scp/curl/wget" into one sub-technique is a defect.** Also confirmed: **T1052.001** Exfiltration over USB (Exfiltration; Linux/Windows/macOS — notably *no* ESXi), **T1053.003** Cron (Execution, Persistence, Privilege Escalation), **T1021.004** SSH (**ESXi, Linux, macOS — no Windows**), **T1546.004** Unix Shell Configuration Modification. | [ATT&CK updates](https://attack.mitre.org/resources/updates/) · [T1552.003](https://attack.mitre.org/techniques/T1552/003/) · [T1070.006](https://attack.mitre.org/techniques/T1070/006/) · [T1048.003](https://attack.mitre.org/techniques/T1048/003/) · [T1053.003](https://attack.mitre.org/techniques/T1053/003/) |
| 8 | *(implicit)* "grep the logs for `sshd`" | 🔴🔴 **`journalctl _COMM=sshd` now MISSES the authentication lines.** OpenSSH **9.8** (1 Jul 2024) split the daemon: *"some log messages will be tagged with as originating from a process named "sshd-session" rather than "sshd"."* **10.0** split again, moving *"the user authentication phase of the protocol from the per-connection sshd-session binary to a new sshd-auth binary."* The `Accepted …` line comes from `auth_log()`, i.e. from **`sshd-auth`** on OpenSSH ≥10.0. Ubuntu 26.04 ships **10.2**; current upstream is **10.5 (11 Aug 2026)**. 🟢 The line format itself is **unchanged** — `Accepted %s for %s from %s port %d ssh2` — and carries three fields worth teaching: the **`invalid user ` prefix** for nonexistent accounts, the `method/submethod` pair, and **the RSA/ED25519 key fingerprint** appended on publickey accepts. 🟢 Plain `grep` of `auth.log` is unaffected by the split; only journald filters break. ⚠️ `SyslogFacility` default is **AUTH (4)**, so `SYSLOG_FACILITY=10` (authpriv) catches sudo/PAM but **misses sshd**. | [OpenSSH 9.8](https://www.openssh.com/txt/release-9.8) · [OpenSSH release notes](https://www.openssh.com/releasenotes.html) · [openssh-portable auth.c](https://raw.githubusercontent.com/openssh/openssh-portable/master/auth.c) · [sshd_config(5)](https://man.openbsd.org/sshd_config.5) |
| 9 | *"execute `./autopsy` from `autopsy-4.21.0/bin`"* | ⚠️ **4.21.0 was released 29 Aug 2023 — three years old to the day as of this extraction.** Current is **4.23.1 (7 May 2026)**; 4.23.0 was 15 Apr 2026 and Sleuth Kit 4.15.0 the same day. 🟢 **None of the intervening changes touch ext4 handling**, so the room's exercises still work — but students are running three years of unpatched dependencies. 🔴 **More useful finding: Autopsy has NO ingest module that parses bash history, crontabs or `auth.log`.** The 4.23.0 module list is entirely Windows/mobile-oriented, and 4.23.0's headline features (*"New or updated parsers for: Prefetch, SRU, Thumbcache, Regripper"*) added nothing for Linux. **The workaround worth teaching is the Plaso ingest module**, which does ship `bash_history`, `zsh_extended_history`, `syslog`, `utmp`, `dpkg.log` and `selinux` parsers — **but no cron parser**, so crontabs remain a manual read. **Honest framing: Autopsy gives you the filesystem, the timestamps and the timeline; the Linux persistence analysis is done by hand.** | [autopsy.com/download](https://www.autopsy.com/download/) · [4.21.0 release post](https://www.autopsy.com/4-21-0-release-with-faster-search-and-malware-scanning/) · [Autopsy 4.23.0 user docs](https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/) · [Plaso parsers](https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html) |

### NOT VERIFIED — carried forward honestly

- **Which file supplies Q7's answer** (`/etc/hosts` vs `known_hosts` vs `~/.ssh/config` vs the
  literal command). The lab machine was not started; §2.6 lists the candidates rather than guessing.
- **Whether `/var/log/journal/` exists on a stock Debian 13 / Ubuntu 26.04 image** (compile-time
  default). One command on a real image.
- **Exact `HISTSIZE`/`HISTFILESIZE` in Ubuntu's `/etc/skel/.bashrc`** — read from the image.
- **Octal permissions of `/var/spool/cron/crontabs`** — the man page states the model in prose only.
- **The current-kernel format string** for the `new high-speed USB device number N using xhci_hcd`
  line — function and file confirmed (`hub_port_init`, `drivers/usb/core/hub.c`), wording not
  retrieved. Do not quote it; `dmesg` on a real box first.
- **A Fedora change proposal retiring utmp/wtmp** — only the F43 *Migrate to lastlog2* change is
  confirmed. **Do not cite a Fedora utmp release number.**
- **The "inode number ordering vs timestamps" timestomp heuristic** — no citation found in primary
  or strong-DFIR sources, and ext4's Orlov/flex_bg allocator makes the premise doubtful. **Dropped.**
- **The SANS *Breaking Time* paper body** — landing page read, PDF robots-blocked. Reading-list item
  only.

## 4. Evidence used

**A pre-built Linux VM with the subject disk already mounted.** *"Liam's personal workstation's disk
is mounted at `/mnt/liam_disk`, and the disk image is available at `/home/ubuntu`."* Split-view
browser lab, 70 minutes, Premium only.

- **Downloadable?** ⚠️ **No.** The image exists only inside the lab VM. There is no download link
  and no published hash. **Unusable for us even if Linux were in scope.**
- **Licence?** Not stated. TryHackMe content is subscription-gated; **D22 forbids rehosting** and
  there is nothing to rehost in any case.
- **Reusable?** 🔴 **No, on two independent grounds** — it is not obtainable, and its entire
  artifact set is out of scope per **D38**.
- **`ecdfp-evidence` action: none.** 🔴 **This is the first of 22 rooms to yield no evidence set.**
  `EVS-10` **stays unallocated** rather than being spent on a set we will not build. Recording that
  explicitly, because a silently skipped ID is how a manifest ends up with a hole nobody can explain
  later.

### 🟢🟢 Critique of the scenario brief — and this one is a teaching asset

The brief does something no other room in the set has done: **it names the defence before the
investigation starts.**

> *"However, he could argue that he was framed as he did not own the workstation."*

**That is a defensible-investigation move, stated in a training scenario, and we should use the
sentence verbatim in S1.** It converts "what does this artifact not prove?" from a rubric line into
a plot obligation — the investigators go to a second machine *because* the first one's proof is
contestable.

⚠️ **And then it throws it away two sentences later:**

> *"It seems like the investigators not only revealed more about the external entity Liam worked with
> but also exposed a betrayal: Liam was double-crossed."*

**The conclusion is published before the student has looked at anything.** Q13 and Q14 then ask the
student to "discover" a betrayal the brief already announced.

🟢🟢 **Pairing rooms 21 and 22 as an S1 exercise is better than either alone**, because they fail in
opposite directions and the contrast is legible in ten minutes:

| | room 21 DiskFiltration | room 22 ExfilNode |
|---|---|---|
| **what the brief does wrong** | prejudices with **behaviour** — *"roaming around the critical server room"* | prejudices with the **conclusion** — *"exposed a betrayal"* |
| **what it does right** | publishes the ATT&CK chain, so every question is *prove this claim* | **names the alternative hypothesis** — *"he could argue that he was framed"* |
| **the exercise** | strike the prejudicial sentences; rewrite as a neutral tasking | keep the alternative-hypothesis sentence; strike the conclusion; **write the tasking that sentence justifies** |

**That is a 15-minute S1 activity built entirely from published text, requiring no evidence, no VM
and no Linux.** It is the highest-value thing this room gives us.

## 5. Lab design worth reusing

### 5.1 🟢🟢 The second machine, motivated by the first machine's limit

**Adopt outright.** The structural move — *"he could argue that he was framed as he did not own the
workstation"* → therefore examine a machine he *did* own — is the cleanest illustration of D7 we
have found in 22 rooms. **The limitation is not a caveat at the end of the report; it is the reason
the next step of the investigation exists.**

Applied to **D19**, our carry-through incident currently ends at *"exfiltration to USB"* on
`EVI-SRC01`. **The USB and the receiving host are never examined**, and that is a real hole in the
story that this room made visible. D38 resolves how we close it without adding Linux — §8.

### 5.2 🟢🟢 The betrayal — a second incident nested inside the first

**Adopt for `S6-09`.** Q13 and Q14 are a complete miniature intrusion: an SSH login from an
unexplained address a few hours after the main activity, and a cronjob left behind. Placed *after*
twelve questions of insider-case work, it forces the student to notice that **the timeline did not
stop when the story did.**

🟢 **The two questions are adjacent on purpose**, and that ordering is the lesson: the login gives
the *when* and *from where*, the crontab gives the *what*, and neither attributes on its own —
attribution comes from correlating the spool file's ctime against the session (§2.8).

⚠️ **Our version must not announce it in the brief** (§4). The correct form is a tasking that ends
with *"report anything on the host that you cannot attribute to the subject"* — which is a real
tasking line, and which the betrayal then rewards.

### 5.3 🟢 Shell-first, GUI-optional — and this is the right default

*"All the questions in this room can be answered by running commands on the mounted disk"*, with
Autopsy *"optional"*. **Every lab step in our material should have a CLI path that is the taught
path, with the GUI shown as the convenience.** Reasons this room makes concrete:

- A student who only knows the GUI cannot answer a question the GUI has no module for — and **§3 #9
  shows Autopsy has no Linux user-artifact module at all**, so the GUI-only student is stuck on
  eight of these fourteen questions.
- The CLI path is the one that survives a tool going stale, which is the entire subject of the
  currency file.

### 5.4 ⚠️ The `grep -a` instruction — a signal taught as a nuisance

The room pre-empts the error and tells students to suppress it:

> *"If you get the error `grep: /mnt/liam_disk/var/log/auth.log: binary file matches` with any log
> file, use `grep -a` which will treat the file as text."*

🔴 **NUL bytes inside a text log are a finding.** They mean the file was truncated and re-extended
(sparse region reads back as NULs), overwritten in place, or had binary content injected — all of
which are exactly what an examiner is looking for in an anti-forensics case. **The room turns the
most interesting property of the file into a flag you add to get past it.**

**Our version:** teach `grep -a` *and* teach the follow-up in the same breath —
`tr -d '\0' < auth.log | wc -c` against the file size, then locate the NUL run and report its offset.
**Zero extra lab time; it is the same command with a question attached.**

### 5.5 ⚠️ "Recommended but not mandatory" — the continuity hedge

*"While it is recommended to go through that room first… it's not mandatory. You can also solve this
room independently."* TryHackMe can afford that because its rooms are self-contained by design.
**D8/D19 mean ours are not** — our sessions carry one incident forward, which is a deliberate
advantage and a deliberate fragility.

🟢 **The mitigation this room suggests is cheap and we should take it:** publish a short
**catch-up state** with each session's evidence — the two or three findings from the previous
session that the current lab depends on, stated as given facts. A student who missed S4 can then
still do S5. **This is a `packages/session-NN/` artifact, not a new topic, and it costs no minutes.**
Logged as an action in §9.

### 5.6 🔴 Safety and handling defects

**One, and it is an evidence defect — the eighth in the project and the fourth in disk work.**

🔴🔴 **The room hands the student a mounted ext4 filesystem and never states the mount mode.**

> *"Liam's personal workstation's disk is mounted at `/mnt/liam_disk`, and the disk image is
> available at `/home/ubuntu`. **You can run commands on the mounted disk.**"*

Against **E5** in the currency file, a read-write mount of an ext4 image **modifies it**: mount count
(`s_mnt_count`), mount time (`s_mtime`), last-mounted path (`s_last_mounted`), atimes, and — on a
dirty image — **journal replay**. `mount(8)` is explicit that `-o ro` alone is not sufficient; the
correct incantation is `ro,noload,noatime` over a `losetup -r` read-only loop device.

**Three things make this worse than the earlier instances, not better:**

1. **It is ext4** — the exact filesystem E5 is written about, so this is not an analogy.
2. **The room asks a timestamp question about that filesystem** (Q12). A mount that touches atimes
   is operating on the artifact the student is about to reason from. 🔴 In fairness the mount happens
   before the student arrives and Q12 concerns crtime/mtime rather than atime, so the exercise still
   works — **but the student is never told the surface they are standing on has already been
   written to.**
3. **The room ships the raw image alongside**, at `/home/ubuntu` — so the correct, defensible path
   was *available* and simply not taught. **The fix was free and was not taken.**

**Our version:** the mount command is shown in full, with `losetup -r` and `ro,noload,noatime`, and
**the student hashes the image before and after the mount and records both in the chain-of-custody
close (`S4-11`/`S5-10`).** A demonstration that a careless mount changes the hash is worth more than
any slide about write-blocking — and per **E6**, software write-blocking on Linux is *effective and
unvalidated by NIST CFTT*, which is exactly the nuance that demonstration teaches.

**Running total: 8 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22. Four endanger the analyst's machine;
four endanger the evidence. All four evidence defects are in disk work.**

## 6. Question patterns

**14 questions, one task, no scaffolding — a single unbroken investigation, which is the right shape
for a 70-minute challenge and matches our `[INVESTIGATION]` rows.**

**🟢 Answer formats are specified** where ambiguity is possible — `YYYY-MM-DD HH:MM:SS` on all three
timestamp questions, and *"alphabetical order, ascending, separated by a comma"* on Q12. Same
discipline as rooms 19–21.

**🟢🟢 Q12 hedges its own stem: *"Which files are likely timstomped…"***. **Twenty-two rooms in, that
is the first question in the entire corpus that admits an artifact yields an inference rather than a
fact** — and it happens to be correct for exactly the reason §2.7 gives, since crtime is forgeable
and every heuristic is an inconsistency rather than a proof. **Credit where it is due.** ⚠️ It does
not count in the tally below, because a hedged stem is not the same as a question whose answer is
*"cannot be determined"* — but it is the closest anyone has come, and it is worth telling students
that a professional question sounds like this one.

⚠️ **`timstomped` is a typo in a graded question.** Trivial, except that it is the artifact's name —
a student searching the term as spelled finds nothing. **Our review checklist should include
"spell-check every artifact name in every stem", which sounds beneath mentioning until it happens.**

**⚠️ Stems assert their conclusions, again** — *"the exfiltrated files"* · *"the external entity
helping Liam"* · *"the amount… that Henry **had to give** Liam for this exfiltration task"* ·
*"Liam thought the work was done, but the external entity had other plans"*. Q9 is the worst: it
names the counterparty, the obligation and the purpose inside the question. **Fifth room in a row
with this pattern; it is a house style, not an accident.**

**🔴 Q9 is a content question wearing an artifact question's clothes.** *"What was the amount in USD
that Henry had to give Liam?"* is answered by **reading a file**, not by understanding an artifact.
It exercises search, not forensics. **The distinction matters for us because D20 criterion 3 requires
each finding to be tied to a named artifact** — and "I found a number in a text file" satisfies that
only trivially. 🟢 **Worth one deliberate content question per case for morale and realism** (real
cases do turn on a document), but it should be labelled as such in our answer keys so nobody mistakes
the skill it tests.

**🔴 Twenty-second room, no "cannot be determined" question.** And this room's artifact set makes the
omission particularly sharp, because **the Linux artifacts are weaker than their Windows equivalents
almost across the board** — which means the honest answer to several of these stems is genuinely
"not from this evidence":

| the room could have asked | correct answer |
|---|---|
| *"The USB has no `SerialNumber:` line in the kernel log. What is its serial number?"* | 🟢🟢 **Cannot be determined — and there is not even a marker that it is missing.** `show_string()` returns early on a NULL serial, so the line is simply absent. Windows fabricates an instance ID and flags it with the `&` convention; **Linux is silent.** The best question in this table, because the two OSes fail *differently*. |
| *"`kern.log` shows `USB disconnect, device number 5`. Was that Liam's stick?"* | **Not established from that line** — the disconnect record carries **no serial and no VID/PID**. It requires correlation on the `usb N-M:` bus/port prefix and device number, and across a reboot that correlation can be ambiguous. |
| *"`.bash_history` contains no `scp`. Did the user transfer anything by scp?"* | 🔴🔴 **Cannot be determined.** Ubuntu's default `HISTCONTROL=ignoreboth` means **one leading space suppresses a command with no gap, no marker and no count anomaly.** Absence of a command is not evidence it was not run. |
| *"Which directory was the user in when they created `mth`?"* — i.e. **the room's own Q8** | ⚠️ **Strictly, an inference, not a finding.** `.bash_history` records no working directory; the answer comes from reading an earlier `cd` and **assuming** no suppressed or interleaved command between. **The room asks it as a fact question.** |
| *"`last` returns nothing on this image. Did anyone log in?"* | 🔴🔴🔴 **Cannot be determined — and on Debian 13 / Ubuntu 25.04+ the file does not exist at all.** §3 #2. **This is the direct Linux analogue of room 21's `WordWheelQuery` question, and like that one it is a question the room's authors could not have written**, because the removal postdates the room. |
| *"crtime is later than mtime on `payload.sh`. Is it timestomped?"* | **Not proven** — *likely*, which is what Q12 correctly says. Restores, `rsync -a` and `tar -p` produce the same inconsistency innocently, and **crtime itself is forgeable with `debugfs -w`**. |
| *"The crontab contains a job. Did it run?"* | **No** — a crontab entry is *configuration*. Execution evidence is a separate `CRON[…]: (user) CMD (…)` log line, and **on a journald-only host that may have rotated away entirely.** |
| *"There is no `.timer` question in this room. Is cron the only persistence?"* | 🔴 **No** — `/etc/systemd/system/*.timer` is equally usable and is not asked about anywhere. **A student who finishes this room believing cron is the answer has been taught an incomplete sweep.** |

🟢🟢 **Eight, and two of them are questions no Windows-only course could ask**, because they depend on
Linux failing where Windows succeeds. **That asymmetry is the whole argument for D38's contrast
table** — §8.

## 7. Figures

**The room contains no conceptual diagram of any kind.** Full image inventory taken from the DOM
before extraction: the room icon (700 × 700), a page banner (1920 × 300), a hero illustration
(1092 × 840), two avatars, the target-machine and info SVG glyphs, and a VirusTotal/GTI icon.
**Every one is decorative.** Nothing was worth opening in a lightbox, so **none were viewed
individually** — and that is recorded honestly rather than glossed.

🔴 **That is itself a finding, and it is the fourth room in a row with zero conceptual figures.** A
70-minute investigation across eight artifact families, three of which (USB correlation, ext4
timestamps, the login-record family) are genuinely hard to hold in the head, and **the material
carries not one picture.** Our version cannot copy that.

| # | figure we must draw | spec | priority | what it teaches |
|---|---|---|---|---|
| F1 | **Windows ↔ Linux artifact equivalence** | Two-column table rendered as a diagram: each row is one investigative question (*"which USB?"*, *"who logged in?"*, *"what did they type?"*, *"what persists?"*), with the Windows artifact left, the Linux artifact right, and a **strength bar** on each side. 🔴 The Linux bar is shorter on every row but one. | **🔴 P1** | **This is D38's whole deliverable.** It teaches why the Windows artifacts are remarkable, by showing what their absence looks like. |
| F2 | **The USB attach/detach correlation** | Timeline strip of kernel log lines: connect block (`idVendor` → `SerialNumber:`) at t₁, disconnect line (`device number 5`, **no serial**) at t₂, with a dashed arrow labelled *"correlated on bus/port + devnum, NOT on serial"* and a red break where a reboot intervenes. | **🔴 P1** | The single hardest inference in the room, and the one Q10 hides. |
| F3 | **What a mount writes** | Before/after of the ext4 superblock: `s_mnt_count`, `s_mtime`, `s_last_mounted` changing, plus a hash strip going from green to red. Contrast panel: `losetup -r` + `ro,noload,noatime` leaving all three unchanged. | **🔴 P1** | §5.6, and it serves **E5** across the whole course, not just this room. |
| F4 | **The `.bash_history` silence** | Two stacked shell transcripts — what was typed vs what was saved — with the space-prefixed line greyed out of the second and a callout: *"no gap, no marker, no count anomaly."* | **🟢 P2** | The most counter-intuitive default in the note (§2.5), and it generalises to every "absence of evidence" argument in the course. |
| F5 | **ext4 timestomp decision tree** | Four inode times in a box; branches for *mtime < crtime*, *ctime ≫ mtime*, *nsec == 0*; each leaf labelled **"inconsistent — not proof"**, with a footnote branch for `debugfs -w`. | **🟢 P2** | Turns Q12's *"likely"* into a defensible method, and models D20 criterion 4 in a picture. |
| F6 | **The two-machine case** | Two host boxes with the incident arc across them; the gap between them annotated *"attribution contestable — this is why there is a second machine"*, and the betrayal drawn as a **second, later arrow arriving from outside**. | **🟢 P2** | §5.1 + §5.2 in one image; usable in S1 and again in the S6 capstone brief. |

## 8. 🔴🔴 THE DECISION: Linux forensics stays out of scope — D38

**The collision, stated plainly.** `design/scope_decisions.md` excludes Linux/macOS forensics by
decision; `design/coverage_matrix.md` repeats it as an accepted cost; `design/topic_map.md` contains
no EXT row anywhere and S4 goes MBR → GPT → FAT → NTFS. **This room is 100 % Linux across all
fourteen questions.** It cannot be intaken as written, and pretending otherwise would put an
untaught filesystem into a session that has no minutes for it.

### What was considered

| option | verdict |
|---|---|
| **(a) Add Linux forensics as a topic block** | 🔴 **Rejected.** It needs EXT internals before ext4 timestamps mean anything, which is an `S4-06`-sized dependency, and a Linux artifact block to match S5's ten Windows rows. Realistically 40–60 min. **D1 locks 24 hours**, every session already totals exactly 220 (**D26**), and **S5 is 65 min overdrawn before this room is counted.** It would also break **D24**'s ≤ 1.0 pp domain tolerance, since the minutes come out of Fundamentals and Storage, the two domains already closest to their limits. |
| **(b) Ignore the room** | 🔴 **Rejected.** It would leave two genuine defects standing: **D19's incident ends at *"exfiltration to USB"* with the receiving end never examined**, and our students would meet the Windows artifacts with no idea which of their properties are remarkable. |
| **(c) Keep the exclusion; take the case shape and one contrast** | 🟢🟢 **Adopted — D38.** |

### D38, as it will be written

> **Linux/macOS forensics remains out of scope, confirming `scope_decisions.md`. Three things are
> taken from room 22 instead, all of which cost zero new session minutes:**
>
> 1. **One cross-platform artifact-equivalence table (figure F1), inside `S1-01`** — not a new row.
>    `scope_decisions.md` already obliges us to *"State this to students explicitly in S1"*, and
>    `S1-01` already covers *"what an investigator may not claim"*. **The table converts a
>    disclaimer we already owe into five minutes of teaching.**
> 2. **The two-machine limitation becomes an explicit, stated limitation of the carry-through case
>    (D19)** — the receiving host exists, was not examined, and the report must say so. **A stated
>    limitation is a D20 criterion-4 deliverable, not a gap.**
> 3. **The room-21/room-22 brief-critique pairing (§4) becomes S1 homework**, since it needs only
>    published text — no VM, no evidence, no Linux.

### Why the contrast table is worth more than it looks

The obvious reading is that F1 is a consolation prize for a topic we cannot afford. It is not.
**Every Linux equivalent in this room is weaker than its Windows counterpart, and in instructive
ways:**

| investigative question | Windows | Linux | what the asymmetry teaches |
|---|---|---|---|
| *which USB, and whose?* | `USBSTOR` + `MountedDevices` + `MountPoints2` — **persistent for years, attributable to a user** | kernel log lines only; **no persistent store**, rotates by size, disconnect line has no serial | **a registry is a forensic luxury.** Students who only meet `USBSTOR` never learn why it is remarkable. |
| *who logged in, when?* | Security event log — durable, per-event, structured | wtmp/lastlog **being deleted outright** (§3 #2); journal rotates by size | **artifacts can be removed by an upstream decision that has nothing to do with forensics** — here, Y2038. |
| *what did they type?* | PowerShell script block logging — **three states, on by default for suspicious blocks** (G1) | `.bash_history` — **undated, and silently suppressed by a leading space** (§2.5) | the sharpest *absence-of-evidence* lesson in the course. |
| *what persists?* | Run keys, services, scheduled tasks — enumerable, and Autopsy parses them | cron **plus** systemd timers **plus** shell rc files; **no Autopsy module for any of them** | **completeness of a sweep is a property of the platform, not of the analyst.** |
| *when was the file created?* | `$MFT` `$STANDARD_INFORMATION` vs `$FILE_NAME` — **two independent times, and the classic timestomp tell** | ext4 crtime — **one time, and forgeable with `debugfs -w`** (§2.7) | 🟢 the one row where the platforms are close, and it makes the other four legible. |

**Read down the right-hand column and it is an argument for the left-hand one.** That is a better
justification for a Windows-weighted syllabus than *"24 hours does not stretch"*, and it is the
justification we will actually give students in S1.

### What D38 does not do

⚠️ It does **not** make eCDFP a cross-platform course, add an EXT row, add a Linux VM to the lab
(**D17**), or create a Linux evidence set. **`EVS-10` stays unallocated** (§4). If a future INE
blueprint revision puts Linux on the exam, D38 is superseded by a new dated row — not amended.

## 9. Fit against our material

### ⚠️ Part 1 lists this as *"S4/S6 case — exfiltration; pairs with DiskFiltration"* — that mapping is wrong, and the correction is the finding.

It is not an S4/S6 artifact source at all, because none of its artifacts are in scope. **It is an S1
scope-and-limitations source and an S6-09 scenario-design source.** Amend the Part 1 row to say so,
and note the reason: *the room pairs with DiskFiltration by story, not by platform* — which is a
distinction Part 1's one-line mapping could not have caught before the room was read. **Second time
a Part 1 row has needed correcting after extraction; both times the room was fine and the
one-line summary was the problem.**

### Rows this strengthens

- **`S1-01`** — 🟢🟢 gains figure **F1** (D38) and the sentence *"he could argue that he was framed
  as he did not own the workstation"* as the worked example of *"what an investigator may not
  claim."* **Content into an existing 15-minute row, no new minutes.**
- **`S1-04`** (the report template, D7) — the room-21/22 brief pairing (§4) as **homework**, and
  §2.7's *"inconsistent with normal filesystem behaviour, never proof of tampering"* as the
  house phrasing for criterion 4. 🟢 **That phrasing arrived as a technical fact rather than a style
  rule, which is exactly how we want students to receive it.**
- **`S1-09` / `S4-11` / `S5-10`** — 🔴 §5.6's **hash-before-and-after-mount demonstration**. This is
  the strongest form of **E5** we have found: the student watches a careless mount change the hash.
  It fits the existing ritual rows and costs nothing beyond two hash commands.
- **`S6-09`** — 🟢🟢 the **betrayal** (§5.2) as a capstone structural device, and the **two-machine
  arc** (§5.1) as the brief's framing. Composes with room 20's reverse-order model and room 21's
  published-chain model: **publish the chain, investigate backwards, then find the thing the chain
  did not mention.**
- **`S5-03`** (USB device history) — 🟢 gains figure **F1**'s USB row as its closing slide: *why*
  `USBSTOR` is a strong artifact, answered by showing a platform that has nothing like it.
- **`packages/session-NN/`** — the **catch-up state** artifact (§5.5).

### 🟢🟢 Back-propagation: none — and that is the first time

Every correction this room raised was checked against the repo and every one was **already clean**:

- **ATT&CK "Defense Evasion"** — ✅ the only occurrences are the correction notes themselves in
  `fat32-analysis.md`, `windows-memory-and-network.md` and `diskfiltration.md`. Grepped.
- **T1552.003 "Bash History"** — ✅ **does not appear anywhere in the repo.** The rename to *Shell
  History* is a forward-looking correction only, logged for when the material is written.
- **T1048.003** — ✅ used twice, both for **cleartext HTTP** uploads, which is the correct
  sub-technique. The scp/`.002` distinction (§3 #7) does not invalidate either.
- **`debugfs` / `crtime`** — ✅ no prior note makes a claim about them.

**Twenty-two rooms in, the first with zero back-propagation actions.** Worth recording as evidence
that the ATT&CK-and-currency discipline is now catching things at write time rather than after.

### Minutes

**Net zero.** D38 is deliberately built to be free:

- F1 and the framing sentence are **content inside `S1-01`**, replacing a disclaimer already owed
  under `scope_decisions.md` — **not a new row.** ⚠️ S1 totals exactly **205 + 15 = 220** today, so
  this had to be absorbed rather than added, and it was.
- The brief-critique pairing is **homework**, which consumes no session minutes.
- The hash-before-and-after-mount demonstration lands inside the **existing ritual rows**.

**No new rows. S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Seventeenth room carrying the S5 overdraft** — and, per §10, still no structural fix.
🟢 **But the first room in five that adds nothing to S5.** Rooms 19, 20, 21 and 22's predecessor all
added S5 material; this one adds none, because D38 sites everything in S1. **That is what a scope
decision is supposed to buy.**

### Out of scope

Everything the room actually teaches: EXT internals, Linux logging, Linux USB enumeration, shell
artifacts, cron and systemd persistence. Per **D38**, deliberately. ⚠️ Two adjacent items are worth
one sentence each rather than exclusion:

- **The Y2038 story behind §3 #2** belongs in `S1-01` as a one-line aside — *an artifact can vanish
  because of a decision that has nothing to do with forensics.* It is the most memorable version of
  the currency argument in the whole project.
- **`journalctl --utc`** — our students will meet journald on Linux servers in their day jobs even
  though we do not teach Linux forensics. One line in the S6 timeline row costs nothing.

### Still unresolved

- **S5 re-split** — seventeenth room. 🔴 **Unchanged and unchangeable by extraction:** this room
  added nothing to S5 and the overdraft is still 65 minutes. **No further extraction will move this
  number. It needs a structural re-split.**
- **S4 capstone weighting** — room 18 (Diskrupt) calibrates it at two hours against our one row.
- **Lab OS version** — room 21's `WordWheelQuery` constraint. 🔴 Still gating, still needs deciding
  **before the image is built.**
- **`ecdfp-case` skill** is not installed.
- ⚠️ **`knowledge_base/` EXISTS** — corrected 2026-08-29 while extracting room 25. It was
  built the same day from `Resources/` by `ecdfp-intake`: five condensed module files, an
  `instructor/` folder of 8 session notes, and `_source_text/` holding 10 INE units (2,218 pages)
  plus 9 instructor decks. **`evidence/`, `packages/`, `cases/` and `labs/` still do not exist.**
  🔴 **And the sharper point survives the correction: not one of the room notes has been through
  `ecdfp-intake`.** The knowledge base was built from INE courseware and the instructor's own
  decks — **none of the THM research has landed in it.**

## 10. Links

**Room** — <https://tryhackme.com/room/exfilnode>
**Predecessor (same incident, Windows machine)** — <https://tryhackme.com/room/diskfiltration> ·
companion note `diskfiltration.md`
**Room prerequisites (all Linux, none in our scope)** — Linux Forensics · Linux Incident Surface ·
Linux Logs Investigations · EXT Analysis

**Citations from §3, by finding:**

- #1 logging — Debian 12 release notes ch.5
  <https://www.debian.org/releases/bookworm/amd64/release-notes/ch-information.en.html> ·
  Ubuntu 26.04.1 live-server manifest
  <https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest> ·
  rsyslog `50-default.conf`
  <https://raw.githubusercontent.com/rsyslog/rsyslog-pkg-ubuntu/master/rsyslog/noble/v8-stable/debian/50-default.conf>
- #2 login records — Debian 13 release notes, Issues §5.1.9
  <https://www.debian.org/releases/stable/release-notes/issues.html> ·
  Ubuntu 25.04 release notes <https://documentation.ubuntu.com/release-notes/25.04/> ·
  Ubuntu contents search, `lastlog`
  <https://packages.ubuntu.com/search?searchon=contents&keywords=lastlog&mode=exactfilename&suite=resolute&arch=amd64> ·
  `wtmpdb(8)` <https://manpages.debian.org/unstable/wtmpdb/wtmpdb.8.en.html> ·
  `lastlog2(8)` <https://manpages.debian.org/unstable/lastlog2/lastlog2.8.en.html> ·
  Debian systemd 256.5-2 upload, utmp disabled
  <https://www.mail-archive.com/pkg-systemd-maintainers@alioth-lists.debian.net/msg10045.html>
- #3 journal retention — `journald.conf(5)`
  <https://man7.org/linux/man-pages/man5/journald.conf.5.html> ·
  `systemd-journald.service(8)`
  <https://man7.org/linux/man-pages/man8/systemd-journald.service.8.html>
- #4 timezone — Debian `tzdata` changelog
  <http://metadata.ftp-master.debian.org/changelogs/main/t/tzdata/stable_changelog> ·
  `localtime(5)` <https://man7.org/linux/man-pages/man5/localtime.5.html> ·
  `timedatectl(1)` <https://man7.org/linux/man-pages/man1/timedatectl.1.html> ·
  Journal File Format <https://systemd.io/JOURNAL_FILE_FORMAT/>
- #5 shell history — Bash History Facilities
  <https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html> ·
  Bash Variables <https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html> ·
  Launchpad #2039508 <https://bugs.launchpad.net/ubuntu/+source/bash/+bug/2039508>
- #6 ext4 timestamps — coreutils NEWS
  <https://raw.githubusercontent.com/coreutils/coreutils/master/NEWS> ·
  `stat(1)` <https://man7.org/linux/man-pages/man1/stat.1.html> ·
  ext4 inode layout <https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html> ·
  `mke2fs(8)` <https://man7.org/linux/man-pages/man8/mke2fs.8.html> ·
  `debugfs(8)` <https://man7.org/linux/man-pages/man8/debugfs.8.html> ·
  `utimensat(2)` <https://man7.org/linux/man-pages/man2/utimensat.2.html> ·
  Pomeranz, *More on EXT4 Timestamps and Timestomping*
  <https://righteousit.com/2024/09/04/more-on-ext4-timestamps-and-timestomping/> ·
  Kroll, *Breaking Time* (SANS, 23 Oct 2025) — ⚠️ landing page only, PDF NOT READ
  <https://www.sans.edu/cyber-research/breaking-time-methods-artifacts-forensic-detection-timestomping-fat32-ext3-ext4-file-systems>
- #7 ATT&CK v19.2 — <https://attack.mitre.org/resources/updates/> ·
  T1552.003 <https://attack.mitre.org/techniques/T1552/003/> ·
  T1070.006 <https://attack.mitre.org/techniques/T1070/006/> ·
  T1564.001 <https://attack.mitre.org/techniques/T1564/001/> ·
  T1048.003 <https://attack.mitre.org/techniques/T1048/003/> ·
  T1053.003 <https://attack.mitre.org/techniques/T1053/003/> ·
  T1052.001 <https://attack.mitre.org/techniques/T1052/001/> ·
  T1021.004 <https://attack.mitre.org/techniques/T1021/004/>
- #8 OpenSSH — release notes <https://www.openssh.com/releasenotes.html> ·
  9.8 release <https://www.openssh.com/txt/release-9.8> ·
  `auth.c` <https://raw.githubusercontent.com/openssh/openssh-portable/master/auth.c> ·
  `sshd_config(5)` <https://man.openbsd.org/sshd_config.5>
- #9 Autopsy — download page <https://www.autopsy.com/download/> ·
  4.21.0 release post
  <https://www.autopsy.com/4-21-0-release-with-faster-search-and-malware-scanning/> ·
  4.23.0 user docs <https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/> ·
  Plaso parsers and plugins
  <https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html>
- §2.3 USB — Linux `drivers/usb/core/hub.c`
  <https://raw.githubusercontent.com/torvalds/linux/master/drivers/usb/core/hub.c> ·
  `udev(7)` <https://man7.org/linux/man-pages/man7/udev.7.html>
- §2.8 cron and persistence — Debian `crontab(1)`
  <https://manpages.debian.org/stable/cron/crontab.1.en.html> ·
  `crontab(5)` <https://man7.org/linux/man-pages/man5/crontab.5.html> ·
  `cron(8)` <https://manpages.debian.org/stable/cron/cron.8.en.html> ·
  `systemd.unit(5)` <https://man7.org/linux/man-pages/man5/systemd.unit.5.html> ·
  `systemd-rc-local-generator(8)`
  <https://man7.org/linux/man-pages/man8/systemd-rc-local-generator.8.html> ·
  XDG Autostart <https://specifications.freedesktop.org/autostart-spec/latest/>

**Companion notes** — `diskfiltration.md` (rooms 21/22 are one incident) ·
`windows-user-activity.md` (the USB and search-term artifacts F1 contrasts against) ·
`forensic-imaging.md` and `autopsy.md` (E5, the mount defect) ·
`fat32-analysis.md` (T1070.006 / T1564.001, already carrying the Stealth correction) ·
`_TOOL_CURRENCY_2026-08-28.md` **block J** (this room's reusable findings).
