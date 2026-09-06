---
room: Initial Access Pot
url: https://tryhackme.com/room/initialaccesspot
module: **Honeynet Collapse — stage 1 of 6.** *"Investigate the first, Linux part of the Honeynet
        Collapse!"* Challenge room (Priority 2). See `honeynet-collapse-module.md` for the arc.
feeds: 🟢🟢 **`S1-06` (hashing) gets its best content from this room** — the MD5-for-lookup vs
       SHA-256-for-integrity rule, with NIST publishing MD5 hash sets while NIST standards exclude
       MD5 from approved cryptography. **`S1-08` / `S2`** gain *console access is equivalent to
       root*. **`S6-01`/`S6-02`** gain Apache/nginx access logs beside our existing IIS material.
       🔴🔴🔴 **Carries a repo-wide ATT&CK correction bigger than the Stealth rename: T1562 was
       REVOKED and the log-clearing sub-techniques moved out of T1070** — §3 #7.
       ⚠️ Linux artifacts (auditd, privesc state) are out of scope per **D38**; they enter only as
       rows in the S1 contrast table (figure F1).
difficulty / time: **Hard** · 60 min · 2 tasks · 7 questions (6 scored + 1 "Let's go!") · Premium ·
                   3,562 completions · 78 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, network diagram, lab instructions, tips and all
              question stems. 0 sections NOT READ.
              🔴 **Room ships plaintext SSH credentials for the lab machine — deliberately not
              reproduced here (R8).** Note only that they exist and are published in the task body.
              ⚠️ **Answers NOT READ** — the lab machine was not started. §2 is reconstructed from the
              6 scored questions, the room's three tips and the briefing, as for rooms 18–22.
              🟢 **The network diagram WAS viewed** (lightbox + zoom) and is transcribed in §7 — it
              is the map of all six rooms and the most valuable single object in the module.
---

## 1. What the room teaches

**That the instrumentation you deploy to watch attackers is itself attack surface — and that the
first stage of an intrusion is usually somebody's side project.**

The scenario is the best-constructed one in the whole extraction set. DeceptiTech sells honeypots
and does not use them. The CEO tells a **newly hired junior** to prove the product works, with a
deadline. She does the obvious thing:

> *"Configure DeceptiPot to replicate a corporate WordPress blog, deploy the machine in the
> corporate DMZ, expose it to the Internet, and see what it captures over the weekend."*

🟢🟢 **Every element of that sentence is a real control failure, and none of them is incompetence.**
A junior was given a demo deadline and no change process; the box went into the **DMZ** rather than
an isolated segment; it was exposed to the internet over a **weekend**, when nobody was watching;
and the room's own tip admits *"Emily did not properly configure the DeceptiPot."* **The initial
access for a full domain compromise is a demo machine.** That is how it actually happens, and it is
a far better teaching scenario than the usual "user clicked a link."

⚠️ **And the framing is honest about the consequence in a way our material should copy:** *"all
critical on-premises systems were locked down and encrypted… the backups corrupted and all SIEM data
wiped clean."* **The reason there is a DFIR engagement at all is that the detective controls were
destroyed.** That sentence is the justification for the entire discipline we teach — you are doing
disk and memory forensics precisely because the logs are gone.

🟢🟢 **The room is stage 1 of 6, and the module publishes its own map.** A network diagram in Task 1
numbers all six attack stages across the DMZ and CORE subnets, and each room says which number it
covers. §7 transcribes it in full. **That diagram is how the module carries state between rooms
without requiring the student to have completed the previous one**, and it is the design idea we
came here to steal.

**What it gets wrong, or rather what it quietly assumes:**

- 🔴🔴 **`auditd` is not installed by default on Ubuntu** — it is absent from the 24.04 and 26.04
  live-server manifests. The room has to *tell* you *"Auditd is configured with non-standard audit
  rules"* because on a real internet-exposed WordPress box **you would find nothing there at all.**
  §3 #1. The room presents its most powerful artifact as though it were ambient.
- 🔴🔴 **The access log cannot contain what Q1 seems to ask for.** Neither Apache nor nginx logs
  request bodies, and `%u`/`$remote_user` is HTTP-auth only — so a brute force against
  `wp-login.php` records **no usernames and no passwords, ever.** §3 #2.
- 🔴 **`xmlrpc.php` breaks request-counting entirely.** One POST can carry hundreds of credential
  attempts via `system.multicall`. **A student who reports "12 login attempts" from twelve xmlrpc
  requests is wrong by three orders of magnitude.** §3 #3.
- ⚠️ **The room publishes plaintext SSH credentials in the task body** (R8). Third Priority-2 room
  to do so.
- ⚠️ **Q5 asks for an MD5** without saying why an MD5 is the right thing to ask for. It is — for
  *lookup* — but the room never draws the distinction that makes it defensible. §2.6.

🟢 **One thing it does that no other room in the set has done: Q6 is not an artifact question at
all.** *"Can you access the DeceptiPot in recovery mode?"* asks the student to **boot the machine
into a root shell**. It is an access-and-acquisition question wearing a challenge-room flag, and it
is the most transferable question in the room — §2.7.

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 6 scored questions plus the room's three tips (see frontmatter). Mapping:
Q1 → 2.1 · Q2 → 2.2 · Q3 → 2.3 and 2.4 · Q4 → 2.5 · Q5 → 2.6 · Q6 → 2.7 · scenario → 2.8.

### 2.1 Web server access logs — and the one status code that dates the compromise

- **What it is** — one line per HTTP request. Q1: *"Which web page did the attacker attempt to brute
  force?"*
- **Where it lives** — Apache `/var/log/apache2/access.log`, nginx `/var/log/nginx/access.log` on
  Debian/Ubuntu (⚠️ path **NOT VERIFIED** from a primary doc — the mechanism is `${APACHE_LOG_DIR}`
  from `/etc/apache2/envvars`; read it off the box). Apache's default `combined` format is
  `%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"`; nginx's `combined` is the same
  fields as `$remote_addr … $status $body_bytes_sent $http_referer $http_user_agent`.
- **What it proves** — that a request for a given path arrived from a given address at a given time,
  and what the server answered. 🟢🟢 **And, for WordPress specifically, whether it worked** — see the
  caveat box.
- **What it does NOT prove** — 🔴🔴🔴 **the three limits that make this block worth teaching:**
  1. 🔴🔴 **It contains no credentials and no usernames.** Neither server logs the **request body**
     by default — Apache's `mod_log_config` has no format string for it at all, and nginx's
     `$request_length` is a byte count, not content. And `%u` / `$remote_user` is the **HTTP-auth**
     user: Apache's docs say *"If the document is not password protected, this part will be `-`."*
     WordPress login is an application-level form POST, so **`%u` is `-` for every attempt.**
     **The log tells you how much and from where. Never what.**
  2. 🔴🔴 **Request count is not attempt count.** Against `wp-login.php` one POST ≈ one attempt. But
     `system.multicall` on `xmlrpc.php` executes an array of `methodCall`s in a **single** request —
     WordPress's own security doc names it — so twelve log lines may be thousands of guesses. The
     multiplier is only hinted at by request *size*, which **is not in either default format.**
  3. 🔴 **Rotation, not the attack, sets how far back you can see.** ⚠️ The Ubuntu logrotate policy
     for both servers is **NOT VERIFIED** from a primary source — which is itself the lesson:
     **read `/etc/logrotate.d/` off the evidence before concluding "there was no earlier activity."**
  ⚠️ **User-Agent and Referer are attacker-controlled.** Both are logged by default on Apache and
  nginx — matching IIS (**G9**) — but a `WPScan` or `python-requests` UA is a *hint*, never proof,
  and a competent attacker sets a browser string.
- **How to parse it** — plain text; `awk`/`grep`; or into a timeline. 🟢 **The high-value filter is
  by status:** count `POST /wp-login.php` by response code per source IP.
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the 200/302 signal, and it is the single most
  useful thing in this note.** WordPress core's `wp-login.php` calls `wp_safe_redirect()` on
  success — whose signature defaults to **status 302** — and on failure simply falls through to
  re-render the form, with **no `status_header()` call anywhere in the file**, i.e. **200**.
  **So: a long run of `POST /wp-login.php → 200` is failures; the first `POST → 302` is the
  successful credential, and its timestamp is your compromise time.** Corroborate with
  `GET /wp-admin/ → 200` from the same address seconds later.
  ⚠️ Two honest limits: a plugin or a `login_redirect` filter can change the destination (**it is
  still a 30x, not a 200**), and a security plugin or WAF may return 403/429 instead — **if the
  pattern is absent, check for a plugin before concluding nothing happened.**

### 2.2 The dropped PHP webshell

- **What it is** — attacker code placed inside the web root so it can be executed by requesting it.
  Q2: *"What is the absolute path to the backdoored PHP file?"* ATT&CK **T1505.003**, 🔴 now
  **Persistence only** — §3 #7.
- **Where it lives** — under the web root. 🟢 **The permission model tells you where to look first.**
  WordPress's own hardening doc: `/wp-content/` is *"intended to be writable by your user account
  and the web server process"*, while `/wp-content/plugins/` *"should be writable only by your user
  account"*. **`wp-content/uploads/` is the one directory that must be web-server-writable in every
  install**, which makes `/wp-content/uploads/YYYY/MM/<name>.php` the highest-probability landing
  zone — at a predictable, publicly servable URL.
  ⚠️ Two secondary zones: `wp-content/themes/` becomes writable the moment the theme editor is used
  (or after a sloppy `chmod -R 777`), and **a compromised admin account can write PHP through the UI**
  via the plugin/theme editor — which is why an admin compromise produces a shell in `plugins/` or
  `themes/` even under correct permissions.
- **What it proves** — that a file containing executable code exists at a path the web server will
  serve. 🟢 Combined with §2.1, that it was *requested*, and when.
- **What it does NOT prove** — 🔴🔴 **that it ever executed.** Presence is presence. Execution
  evidence is a **request for that path in the access log** (§2.1) or a process/syscall record
  (§2.5). ⚠️ **And its timestamps are the weakest dating you have** — a webshell's mtime is set by
  whatever wrote it and is trivially changed (`touch -r` against a neighbouring file makes it blend
  into the directory perfectly). 🔴 **`ctime` is the harder one**, per room 22 §2.7 — and on ext4 it
  is still forgeable by root, so date the shell from the **access log**, not from the file.
  🔴 **A PHP file in `uploads/` is not by itself a compromise finding** — plugins legitimately write
  `index.php` guard files there. **Read the content before calling it a shell.**
- **How to parse it** — `find <webroot> -name '*.php' -newermt '<date>'`; hash every PHP file and
  diff against a clean WordPress of the same version (core, plugins and themes are all publicly
  downloadable, so **a known-good baseline is free** — that is the fastest route and the room does
  not mention it); `grep -rE 'eval|base64_decode|assert|preg_replace.*/e|\$_(GET|POST|REQUEST)\['`.
- **Anti-forensics / false-positive caveat** — 🔴🔴 **the mitigation that would have stopped this is
  not a WordPress default.** WordPress's hardening doc does **not** address blocking PHP execution in
  `uploads/`, so **an uploaded `.php` there will execute on a stock install.** ⚠️ Modern shells are
  often a *one-line* addition to a legitimate core or plugin file rather than a new file — **a
  `find -newer` sweep for new files misses those entirely**, which is why the hash-vs-baseline route
  is the one to teach.

### 2.3 Privilege-escalation state — SUID, sudoers, and the one nobody checks

- **What it is** — the misconfiguration that let `www-data` become root. Q3: *"Which file path allowed
  the attacker to escalate to root?"* ATT&CK **T1548.001** (Setuid and Setgid) or **T1548.003** (Sudo
  and Sudo Caching) — 🔴 **both are now Privilege Escalation *only*** — §3 #7.
- **Where it lives** — SUID/SGID bits in the inode mode; sudo rules in `/etc/sudoers` and
  `/etc/sudoers.d/`; **file capabilities in the extended attribute `security.capability`**; writable
  systemd units under the load path (**`/etc/systemd/system/` shadows `/usr/lib/systemd/system/`**,
  so an override for a packaged unit is itself the artifact); writable cron files.
- **What it proves** — 🔴🔴 **that the opportunity existed at the moment you looked. Nothing more.**
  This is the block's whole point and §2.4 is its counterpart.
- **What it does NOT prove** — 🔴🔴🔴 **that anyone used it, who, or when.** Of the five common
  mechanisms, **only `sudo` produces a persistent timestamped record of an event** (§2.4); the other
  four are **configuration state**:
  | mechanism | enumerate with | record of what happened? |
  |---|---|---|
  | SUID/SGID | `find / -perm -4000 -type f 2>/dev/null` | **state only** — corroborate with `stat` (a ctime shift means a `chmod u+s` happened) and `dpkg -V`/`rpm -Va` to spot a binary whose mode differs from the distro's |
  | sudoers | `sudo -l`; read `/etc/sudoers.d/*` | **both** — the only self-documenting one |
  | capabilities | `getcap -r / 2>/dev/null` | **state only, and nearly invisible** |
  | writable unit / cron | inspect the load path; `/etc/cron.d/*` | **mixed** — the file is state, but cron and systemd log the *payload running* |
  | PATH hijack | no command finds a past one | **state only, and the weakest** — an exported `PATH` leaves nothing on disk once the process exits |
  🔴🔴 **Capabilities are the trap.** `capabilities(7)`: the sets are *"stored in an extended
  attribute … named `security.capability`."* An xattr is **not a mode bit**, so there is no character
  in `ls -l` that can show it — a binary with `cap_setuid+ep` looks exactly like `-rwxr-xr-x root
  root`. **A student who runs only `find -perm -4000` misses it completely**, and `getcap -r /` must
  be a separate, named step.
  ⚠️ **`-perm -4000`, not `4000`.** The leading hyphen means *"all of these bits are set"*; bare
  `4000` means *exactly* those bits and is the classic student error.
- **How to parse it** — the four commands above, plus `getfattr -n security.capability <file>` to
  show the raw attribute when demonstrating. 🟢 Note the detection rule cron hands you for free:
  *"/etc/crontab and the files in /etc/cron.d must be owned by root, and must not be group- or
  other-writable"* — **a group-writable file there is both the vulnerability and the flag.**
- **Anti-forensics / false-positive caveat** — ⚠️ **a distribution ships legitimate SUID binaries**
  (`passwd`, `sudo`, `mount`, `ping`); the finding is a binary that is SUID **and should not be**,
  which needs the package baseline, not a bare list. 🟢 The reverse also matters: the room's Q3 has a
  single answer, but on a real box the honest output is *"these three paths would each have worked"* —
  **and identifying which one was actually used requires §2.4, not §2.3.**

### 2.4 `sudo`'s own log — the privesc artifact that self-documents

- **What it is** — a timestamped, attributed record of a command run with elevated privilege. Not a
  question in this room, and **that omission is itself worth noting** (§6).
- **Where it lives** — `sudoers(5)`: *"Messages can be logged to syslog(3), a log file, or both.
  **The default is to log to syslog(3)**"*, facility *"**Defaults to authpriv**"*, success priority
  *"**Defaults to notice**"*. On Debian/Ubuntu `authpriv` routes to **`/var/log/auth.log`**
  (RHEL: `/var/log/secure`); on a journald-only host, `journalctl SYSLOG_FACILITY=10`. ⚠️ The doc
  guarantees the **facility**, not the filename — per room 22 §3 #1 the filename is conditional.
- **What it proves** — 🟢🟢 **the richest privesc evidence available on a default box, with no
  auditd required.** The documented format is
  `date hostname progname: username : TTY=ttyname ; PWD=cwd ; USER=runasuser ; GROUP=runasgroup ;
  TSID=logid ; COMMAND=command` — **who, from which terminal, in which directory, as whom, running
  exactly what.** Contrast with §2.3: `find -perm -4000` tells you what was *possible*; this tells
  you what *happened*.
- **What it does NOT prove** — 🔴🔴 **what happened inside the elevated process.** `sudo` logs the
  command line it was **asked** to run. `sudo /bin/bash` produces **one line**, and everything typed
  in that root shell is invisible to sudo forever. **That single gap is the entire justification for
  §2.5**, and it is the cleanest motivation for syscall auditing we have found.
  ⚠️ Nor does it prove the escalation route was sudo at all — a SUID or capability escalation
  (§2.3) produces **no sudo line whatsoever**, so **absence here does not mean no escalation.**
  🔴 And once root is obtained by any route, the log itself is writable.
- **How to parse it** — `grep sudo /var/log/auth.log`, or `journalctl SYSLOG_FACILITY=10 --utc`.
  🟢 **Failed** sudo is logged too (`user NOT in sudoers`, `incorrect password attempts`) — that is
  the sudo-brute-force indicator and a good exercise in its own right.
- **Anti-forensics / false-positive caveat** — ⚠️ a legitimate administrator generates hundreds of
  these lines a day; **the finding is a sudo line from an account that should never run one** — here,
  `www-data`. 🟢 **Teach the query that way round**: not *"find sudo"*, but *"find sudo by a service
  account."* That inverts the search from thousands of hits to one, and it is the same shape as the
  Windows question *"which service account authenticated interactively?"*

### 2.5 auditd — syscall records, and the one field that survives escalation

- **What it is** — kernel-level syscall auditing. The room's second tip: *"Auditd is configured with
  **non-standard** audit rules."* Q4 (*"Which IP was port-scanned after the privilege escalation?"*)
  is answerable because of it. ⚠️ **Out of scope per D38** — it enters our material only as a row in
  the S1 contrast table (figure F1).
- **Where it lives** — `/var/log/audit/audit.log` (*"The default path is /var/log/audit/audit.log if
  not explicitly set"*), configured by `/etc/audit/auditd.conf`, rules in `/etc/audit/rules.d/*.rules`
  compiled by `augenrules` into `/etc/audit/audit.rules`. 🟢 **A discrepancy between `rules.d/` and
  the compiled `audit.rules` is itself an anti-forensic tell.**
- **What it proves** — 🟢🟢 **`auid`, and this is the whole reason auditd exists.** Red Hat: the
  `auid` field *"records the Audit user ID, that is the loginuid. This ID is assigned to a user upon
  login and **is inherited by every process even when the user's identity changes**, for example, by
  switching user accounts with the `su - john` command."* **So `auid=1000 uid=0` reads: "user 1000
  escalated and is now acting as root."** That is the attribution `/var/log/auth.log` and a process
  listing cannot give you, and it is the exact answer to §2.4's gap. Records also carry `exe=`,
  `comm=`, `success=`, `tty=`, `ses=`, and the rule's `key=`.
- **What it does NOT prove** — 🔴🔴🔴 **that the log is complete — and on this host the attacker had
  root.** `auditctl -e 0` disables auditing; `-D` deletes all rules; the attacker acts; `-e 1`
  re-enables. **The result is a gap with no deletion marker.** The one configuration that changes the
  answer is **`-e 2` (immutable)**: *"Any attempt to change the configuration in this mode will be
  audited and denied. The configuration can only be changed by rebooting the machine."* — under
  `-e 2`, tampering is itself evidence and **an unexplained reboot becomes a first-class indicator.**
  **Teach students to check `auditctl -s` for the enabled flag before trusting the log.**
  🔴🔴 **And it is almost never there.** `auditd` is **absent from the Ubuntu 24.04 and 26.04
  live-server manifests** — only `libaudit1`, the shared library, ships. **A stock Ubuntu Server has
  no `/var/log/audit/` at all.** §3 #1.
  🔴 **Retention is far shorter than students expect.** Upstream `auditd.conf` ships `max_log_file =
  8` (MiB), `num_logs = 5`, `max_log_file_action = ROTATE` — **a ~40 MiB ceiling**, which on a noisily
  ruled host is *hours*. ⚠️ And `disk_full_action = SUSPEND` means **auditd stops writing while the
  machine keeps running** — an attacker who fills the disk creates a silent gap.
- **How to parse it** — `ausearch -k <key> -i` (*"-k … Search for an event based on the given key
  string"*, *"-i … Interpret numeric entities into text"*); time-bounded with `-ts`/`-te`, which
  accept keywords including `boot`, `today`, `yesterday`, `checkpoint`; **attribution pivot `-ul
  <auid>`**. Triage with `aureport -k`, `-au`, `-x`, `--summary`.
  ⚠️ **Timestamps are `msg=audit(EPOCH.mmm:SERIAL)`** — *"the Unix time format - seconds since
  00:00:00 UTC on 1 January 1970"* — **UTC, not local**, and the serial stitches multi-record events
  together. `a0`–`a3` are the first four syscall arguments *"encoded in hexadecimal notation"*.
- **Anti-forensics / false-positive caveat** — 🟢 **the journal has *some* audit data even with no
  auditd.** `journald.conf`: `Audit=` *"Defaults to yes in the default journal namespace"*, so kernel
  auditing is on and `journalctl _TRANSPORT=audit` returns records. ⚠️ **But with no rules loaded that
  is limited to always-on record types — login/session and LSM denials — not the syscall and
  file-watch records this room depends on.** Teach it as *"look there anyway, expect little."*

### 2.6 Persistence, and the MD5 the room asks for

- **What it is** — the malware left behind, identified by hash. Q5: *"What is the MD5 hash of the
  malware persisting on the host?"* Persistence mechanisms per room 22 §2.8 — cron (**T1053.003**),
  systemd timers, shell rc files (**T1546.004**).
- **Where it lives** — the binary somewhere on disk; the *mechanism* in cron/systemd/rc files. 🟢 The
  two are separate findings and should be reported separately: **the payload and its launcher.**
- **What it proves** — that a file with this exact content exists on this host. 🟢🟢 **And, via
  lookup, whether anyone else has ever seen it** — VirusTotal's file-report API documents its `id`
  parameter as *"SHA-256, SHA-1 or MD5 identifying the file"*.
- **What it does NOT prove** — 🔴🔴 **that the file is unaltered, and this is the distinction the
  room asks for without teaching.** CERT/CC **VU#836068**, *"MD5 vulnerable to collision attacks"*:
  *"Weaknesses in the MD5 algorithm allow for collisions in output. As a result, attackers can
  generate cryptographic tokens or other data that illegitimately appear to be authentic."* The break
  is in **collision resistance**; **preimage resistance is not practically broken**, which is exactly
  why lookup still works and integrity does not.
  🟢🟢 **The teaching card is that NIST does both.** NIST's own **NSRL** ships *"Cryptographic hash
  values (MD5 and SHA-1) of the file's content"* which *"uniquely identify the file even if, for
  example, it has been renamed"* — while MD5 is absent from FIPS 180-4's approved list. **The same
  agency publishes MD5 hash sets for forensics and excludes MD5 from approved cryptography, because
  they are different problems.** ⚠️ The FIPS 180-4 citation is **NOT VERIFIED** — I did not read the
  document; CERT/CC carries the break and NSRL carries the lookup half.
  ⚠️ **Nor does a hash prove maliciousness** — an unknown hash means unknown, not clean. And a
  *matching* NSRL hash means "known OS/application file", which is how NSRL is used: *"to eliminate
  known files … during criminal forensic investigations."*
- **How to parse it** — `md5sum` and `sha256sum`. 🟢🟢 **The rule for `S1-06`:**
  > **MD5 answers "have we seen this exact file before?" It does not answer "is this file
  > unaltered?" Use it to look things up; never to prove integrity — and never as the hash you
  > attest to in a report or on a chain-of-custody form.**
  **Acceptable:** VirusTotal/NSRL/IOC-feed lookups, corpus dedup, matching an IOC list that only
  publishes MD5, a *secondary* hash beside a strong one. **Not acceptable:** the acquisition hash
  (use SHA-256), verifying a download, or anything where an adversary influences the content.
  **Habit to drill: record SHA-256 *and* MD5 for every artifact — SHA-256 is what you defend, MD5 is
  what you paste into the search box.**
- **Anti-forensics / false-positive caveat** — ⚠️ **the room asking for MD5 is asking the *lookup*
  question**, and a correct student answer says so. 🔴 A student who learns "MD5 is the malware hash"
  without the distinction will put MD5 on a chain-of-custody form, which is a **D20 criterion-1
  failure** — integrity. **This is the cheapest place in the whole course to prevent that error.**

### 2.7 The bootloader as an access path

- **What it is** — Q6: *"Can you access the DeceptiPot in recovery mode?"* — a question that asks the
  student to **boot the machine into a root shell**, not to parse anything.
- **Where it lives** — GRUB's menu, and the kernel command line it builds.
- **What it proves** — 🟢🟢 **that console access to a machine with unprotected GRUB is equivalent to
  root. Not a step toward root — equivalent.** The GNU GRUB manual says so outright:
  *"anyone can select and edit any menu entry, and anyone can get direct access to a GRUB shell
  prompt."* Its stated rationale — that *"physical console access already implies other security
  vulnerabilities"* — belongs on a slide, because **that assumption silently fails on a VM**, where
  "console" means the hypervisor console and there is no physical barrier at all.
  The fully verified route is the kernel parameter: `bootparam(7)` — `init=` *"sets the initial
  command to be executed by the kernel"* — so appending `init=/bin/bash rw` yields **a root shell as
  PID 1, before any userspace security control initialises.**
- **What it does NOT prove** — 🔴🔴 **nothing that happens this way is recorded anywhere.** No PAM,
  no `auth.log` line, no `auid` assignment (§2.5), no auditd rules loaded, no AppArmor policy — **none
  of the artifacts in §2.1–2.6 fire, because none of those daemons are running yet.** The attacker
  can reset the root password, gut `/etc/audit/rules.d/`, edit `/etc/shadow`, and truncate the very
  logs an examiner would use, **without generating a single log line about it.** The only residue is
  filesystem timestamps, and root rewrites those (room 22 §2.7).
  ⚠️ **The encryption nuance, which students get backwards:** full-disk encryption with a **boot-time
  passphrase** defeats this — the root filesystem is ciphertext and `init=/bin/bash` has nothing to
  mount. Encryption that **auto-unlocks** (TPM-sealed with no PIN, a keyfile in an unencrypted
  `/boot`, provider-managed cloud keys) does **not** — booting to a shell unlocks the disk for the
  attacker exactly as for the owner. **A GRUB password is not a substitute for FDE, and FDE is not
  automatically a substitute for a GRUB password.**
  ⚠️ **NOT VERIFIED:** whether Ubuntu's `friendly-recovery` menu passes `sulogin --force` and so
  gives a passwordless root shell. The *mechanism* is documented — `sulogin(8)`: *"when root account
  is locked by '!' or '*' at the begin of the password then sulogin will start a root shell without
  asking for a password"* — and Ubuntu does lock root by default, but the invocation is unconfirmed.
  **Teach the `init=/bin/bash` route, which is fully verified and makes the same point.**
- **How to parse it** — not applicable; this is an *access* technique. 🔴🔴 **Which is precisely why
  it needs a handling rule:** this is how an examiner gets a shell on a box whose credentials are
  unknown — **and doing so mounts and modifies the evidence.** For acquisition, boot external
  read-only media and image the disk. **Never `init=/bin/bash` a machine you intend to treat as
  evidence.** ⚠️ Room 22's mount defect (§5.6 there) and this are the same error at different layers.
- **Anti-forensics / false-positive caveat** — 🟢 **it is platform-neutral and that is why it is in
  scope despite D38.** The identical argument runs on Windows with a boot USB and a SAM/utilman
  swap, and it is the honest answer to *"why do we bother with write blockers?"* — because **the
  machine will happily boot into a state that rewrites itself.**

### 2.8 The honeypot's own capture data — instrumentation is not security

- **What it is** — the DeceptiPot was deployed *to record attacks*. Its capture data is the one
  artifact the scenario was designed around, and the room's third tip says *"Emily did not properly
  configure the DeceptiPot."*
- **Where it lives** — product-specific and fictional, so ⚠️ **NOT determinable** without running the
  lab. **What matters is the category, not the path.**
- **What it proves** — in principle, a complete record of attacker interaction: a honeypot is
  purpose-built instrumentation and does not have production's excuses about volume or privacy.
- **What it does NOT prove** — 🔴🔴🔴 **the room's entire joke, and it is a real lesson: a honeypot
  records attacks against the *service it emulates*. It does not record attacks against *itself*.**
  Emily's box was a real Ubuntu host running real WordPress in the DMZ. **When the attacker got a
  shell on the host, they left the instrumented surface entirely** — from that point the evidence is
  ordinary Linux artifacts (§2.1–2.6), not honeypot captures. **Deploying a honeypot did not make
  this machine observable; it made it exposed.**
  🔴🔴 **And the deployment location destroyed the control's value.** A honeypot belongs on an
  isolated segment where *any* interaction is a signal. Placed in the **DMZ with routes to
  production**, a compromise becomes a foothold — which is exactly stage 1 → stage 2 on the diagram
  in §7. **The artifact did not fail; the architecture did.**
  ⚠️ **A honeypot's evidence also carries a legal question no other artifact here does** —
  entrapment/enticement framing, and consent-to-monitor scope. One sentence in the GRC-adjacent
  material, not a topic.
- **How to parse it** — n/a. 🟢 **The examiner's question is the transferable part:** *"what was this
  control designed to see, and was the observed activity inside or outside that design?"*
- **Anti-forensics / false-positive caveat** — 🟢🟢 **generalise it, because this is not really about
  honeypots.** The same question applies to every detective control we teach: Sysmon sees what its
  config includes; auditd sees what its rules watch (§2.5); an access log sees requests, not bodies
  (§2.1). **"The tool saw nothing" and "nothing happened" are different statements**, and a report
  that conflates them fails **D20 criterion 4**. ⚠️ **Twenty-three rooms in, this is the first that
  makes coverage-vs-absence a scenario premise rather than a footnote.**

## 3. Tools and commands

The room names almost no commands — it is a challenge room with three tips and a lab machine. The
table below is therefore **what the questions require**, not what the room prints.

| purpose | command | note |
|---|---|---|
| find the brute-forced page | `awk '$9==200' access.log` / `awk '$9==302'` | 🟢🟢 the 200-vs-302 split is the whole answer — #3 |
| count attempts per source | `awk '{print $1}' access.log \| sort \| uniq -c \| sort -rn` | 🔴 invalid for `xmlrpc.php` — #3 |
| find the webshell | `find /var/www -name '*.php' -newermt '<date>'` | ⚠️ misses a one-line edit to an existing file — §2.2 |
| baseline diff | hash every PHP file against a clean WordPress of the same version | 🟢🟢 free, and the room never mentions it |
| SUID sweep | `find / -perm -4000 -type f 2>/dev/null` | ⚠️ `-4000`, not `4000` — #5 |
| capability sweep | `getcap -r / 2>/dev/null` | 🔴🔴 **invisible to `ls -l`** — #5 |
| sudo rules | `sudo -l` · read `/etc/sudoers.d/*` | the only self-documenting mechanism — §2.4 |
| audit by rule key | `ausearch -k <key> -i` | `-i` interprets uids to names — #1 |
| audit by login user | `ausearch -ul <auid> -i` | 🟢🟢 the attribution pivot — §2.5 |
| audit triage | `aureport -k` · `-au` · `-x` · `--summary` | — |
| audit state | `auditctl -s` | 🔴 **check the enabled flag before trusting the log** — #1 |
| hash the malware | `sha256sum f && md5sum f` | 🟢 both, always — §2.6 |
| root shell via bootloader | GRUB `e`, append `init=/bin/bash rw` | 🔴 **modifies the evidence** — §2.7 |

### CURRENCY CHECK

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | *"Auditd is configured with non-standard audit rules"* — presented as an ambient artifact | 🔴🔴 **auditd is NOT installed by default on Ubuntu.** The 24.04.3 and 26.04.1 live-server manifests contain only **`libaudit-common`** and **`libaudit1`** — the shared library PAM and systemd link against, which loads no rules. **The `auditd` package is absent, so a stock Ubuntu Server has no `/var/log/audit/` at all.** It is realistic only on a CIS/STIG-hardened host or one running an EDR that ships audit rules. Paths confirmed: `auditd.conf(5)` — *"The default path is /var/log/audit/audit.log if not explicitly set"*; rules in `/etc/audit/rules.d/` compiled by `augenrules`. 🔴 **Retention:** upstream ships `max_log_file = 8` MiB, `num_logs = 5`, `max_log_file_action = ROTATE` → **~40 MiB total**, hours on a noisy host; `disk_full_action = SUSPEND` stops writing while the box runs. ⚠️ The Debian/Ubuntu-patched `auditd.conf` is **NOT VERIFIED** — read it off the box. 🟢 **Immutability is the trust switch:** `auditctl -e 2` — *"Any attempt to change the configuration in this mode will be audited and denied. The configuration can only be changed by rebooting the machine."* Without it, `-e 0` / `-D` leave no marker. 🟢 Even with no auditd, `journald.conf`'s `Audit=` *"Defaults to yes"*, so `journalctl _TRANSPORT=audit` has the always-on record types — **but not syscall or file-watch records.** | [auditd.conf(5)](https://manpages.debian.org/testing/auditd/auditd.conf.5.en.html) · [auditctl(8)](https://manpages.debian.org/testing/auditd/auditctl.8.en.html) · [upstream auditd.conf](https://raw.githubusercontent.com/linux-audit/audit-userspace/master/init.d/auditd.conf) · [Ubuntu 26.04.1 live-server manifest](https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest) · [RHEL 9 audit docs](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening) |
| 2 | *(implicit)* "the access log shows the brute force" | 🔴🔴 **It shows the requests and nothing inside them.** Apache's `combined` is `%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"`; nginx's is the same fields. **`%u` is the HTTP-auth user** — *"If the document is not password protected, this part will be `-`"* — and a WordPress login is an application-level POST, so **`%u` is `-` for every attempt**. **Neither server logs the request body by default**: `mod_log_config` defines no format string for it, and nginx's `$request_length` is a byte count. 🟢 Both log **Referer and User-Agent** by default, matching IIS (**G9**) — but both are attacker-controlled. ⚠️ **NOT VERIFIED:** the literal `/var/log/apache2` and `/var/log/nginx` paths from a primary doc (the mechanism is `${APACHE_LOG_DIR}` via `/etc/apache2/envvars`), and the Ubuntu **logrotate** policy for either. **Read both off the evidence — rotation, not the attack, bounds how far back you can see.** | [Apache logs](https://httpd.apache.org/docs/2.4/logs.html) · [mod_log_config](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html) · [ngx_http_log_module](https://nginx.org/en/docs/http/ngx_http_log_module.html) |
| 3 | *(implicit)* "you can tell a successful brute force from the log" | 🟢🟢 **You can, and this is the most useful verified fact in the note.** WordPress core's `wp-login.php` calls `wp_safe_redirect( $redirect_to ); exit;` on success — and `wp_safe_redirect()`'s signature is `( string $location, int $status = 302, … )`, **default 302**. On failure it sets `$errors` and falls through to re-render the form; **`status_header()` appears nowhere in the file**, so failure is PHP's default **200**. **A run of `POST /wp-login.php → 200` is failures; the first `POST → 302` is the compromise, and its timestamp is your incident clock.** 🔴 **But WordPress logs logins nowhere by default** — core fires the `wp_login_failed` action *"after a user login has failed"* with the username, and if nothing subscribes, **nothing is written anywhere.** 🔴🔴 **`xmlrpc.php` destroys request-counting:** `system.multicall` loops an array of `methodCall`s inside one POST, and WordPress's own doc calls it *"a frequent brute-force target (especially the `system.multicall` method)"*. XML-RPC remains **enabled by default** (`xmlrpc_enabled` — *"Default true"*). Current WordPress is **7.1 "Mary Lou", 19 Aug 2026**. | [wp-login.php](https://raw.githubusercontent.com/WordPress/WordPress/master/wp-login.php) · [wp_safe_redirect()](https://developer.wordpress.org/reference/functions/wp_safe_redirect/) · [wp_login_failed](https://developer.wordpress.org/reference/hooks/wp_login_failed/) · [brute force hardening](https://developer.wordpress.org/advanced-administration/security/brute-force/) · [xmlrpc_enabled](https://developer.wordpress.org/reference/hooks/xmlrpc_enabled/) |
| 4 | *(implicit)* "the backdoor is somewhere in the web root" | 🟢 **Predictably so, and permissions say where.** WordPress hardening: `/wp-content/` is *"intended to be writable by your user account and the web server process"*, `/wp-content/plugins/` *"should be writable only by your user account"*, baseline *"all files are set to 0644 and all directories are set to 0755"*. **`wp-content/uploads/` is the one directory that must be web-server-writable in every install.** 🔴🔴 **And WordPress's hardening doc does not address blocking PHP execution in `uploads/`** — I looked specifically; it is absent. **So an uploaded `.php` there executes on a stock install.** That is the attack, and the mitigation is not a default. | [WordPress hardening](https://developer.wordpress.org/advanced-administration/security/hardening/) |
| 5 | *(implicit)* "find the SUID binary" | ⚠️ **Incomplete as a method.** `find(1)`: `-perm -mode` means *"All of the permission bits mode are set for the file"* — so **`-4000`, not `4000`**. 🔴🔴 **And file capabilities are invisible to it and to `ls -l`.** `capabilities(7)`: the sets are *"stored in an extended attribute … named `security.capability`"* — an xattr, not a mode bit, so **no character in the `ls -l` string can represent it**; a `cap_setuid+ep` binary looks exactly like `-rwxr-xr-x root root`. `getcap -r /` is a separate mandatory step. 🟢 `sudo` is the only mechanism that self-documents: `sudoers(5)` — logging *"default is to log to syslog(3)"*, facility *"Defaults to authpriv"*, format `username : TTY=… ; PWD=… ; USER=… ; COMMAND=…`. 🟢 Cron hands you a detection rule for free: *"/etc/crontab and the files in /etc/cron.d must be owned by root, and must not be group- or other-writable."* | [find(1)](https://man7.org/linux/man-pages/man1/find.1.html) · [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html) · [getcap(8)](https://man7.org/linux/man-pages/man8/getcap.8.html) · [sudoers(5)](https://www.sudo.ws/docs/man/sudoers.man/) · [cron(8)](https://manpages.debian.org/testing/cron/cron.8.en.html) |
| 6 | *"Can you access the DeceptiPot in recovery mode?"* | 🟢🟢 **Yes, and the manual says why.** GNU GRUB: *"anyone can select and edit any menu entry, and anyone can get direct access to a GRUB shell prompt"* — **no password is configured by default**; `superusers` + `password_pbkdf2` are opt-in. `bootparam(7)`: `init=` *"sets the initial command to be executed by the kernel"*, so `init=/bin/bash rw` gives **a root shell as PID 1 before any userspace security control starts.** GRUB's stated rationale — *"physical console access already implies other security vulnerabilities"* — **fails silently on a VM**, where the console is the hypervisor's. ⚠️ **NOT VERIFIED:** whether Ubuntu's `friendly-recovery` passes `sulogin --force`. The mechanism is documented (`sulogin(8)`: *"when root account is locked by '!' or '*' … sulogin will start a root shell without asking for a password"*) and Ubuntu locks root, but the invocation is unconfirmed. **Teach the `init=/bin/bash` route.** | [GRUB authentication](https://www.gnu.org/software/grub/manual/grub/html_node/Authentication-and-authorisation.html) · [bootparam(7)](https://man7.org/linux/man-pages/man7/bootparam.7.html) · [sulogin(8)](https://man7.org/linux/man-pages/man8/sulogin.8.html) |
| 7 | ATT&CK mapping for this chain | 🔴🔴🔴 **The largest ATT&CK finding of the project — bigger than the Stealth rename, because it is a REVOCATION, not a rename.** In **v19 (28 Apr 2026)**, **T1562 "Impair Defenses" was REVOKED**, not renamed: the release notes list *"Impair Defenses (revoked by Disable or Modify Tools)"*, *"Indicator Blocking (revoked by Disable or Modify Tools)"*, *"Spoof Security Alerting (revoked by …: Modify or Spoof Tool UI)"*. The successor is **T1685 "Disable or Modify Tools", tactic Defense Impairment (TA0112), v1.0, 12 May 2026**, with six sub-techniques: `.001` Disable or Modify Windows Event Log · `.002` Disable or Modify Cloud Log · `.003` Modify or Spoof Tool UI · **`.004` Disable or Modify Linux Audit System Log** · **`.005` Clear Windows Event Logs** · **`.006` Clear Linux or Mac System Logs**. 🔴🔴 **So the log-clearing techniques moved OUT of T1070.** Independently confirmed: **T1070 "Indicator Removal" is live at v3.0 (12 May 2026), tactic Stealth**, and its sub-technique list is now `.003 .004 .005 .006 .007 .008 .009 .010` — **`.001` and `.002` are gone.** **"Clear Windows Event Logs" is no longer T1070.001; it is T1685.005.** ✅ **Repo grepped: T1562 appears nowhere, and we cite only T1070.004/.006/.009, all still live — zero back-propagation.** But **`S6-06` will want log-clearing and must use T1685.005.** Two smaller deltas: **T1548.001, T1548.003 and T1505.003 are now single-tactic** (Privilege Escalation, Privilege Escalation, Persistence) — if a slide shows a dual Defense-Evasion mapping for any of them it is stale. ✅ Confirmed unchanged: **T1190** (Initial Access) · **T1110.001 Password Guessing** — the right sub-technique for a web login form, **not** `.004 Credential Stuffing` unless reused *pairs* were sprayed, **which per #2 the access log cannot tell you** · **T1046** (Discovery) · **T1053.003** (Execution, Persistence, Privilege Escalation). | [v19 release notes](https://attack.mitre.org/resources/updates/updates-april-2026/) · [T1685](https://attack.mitre.org/techniques/T1685/) · [T1685.004](https://attack.mitre.org/techniques/T1685/004/) · [T1070](https://attack.mitre.org/techniques/T1070/) · [enterprise tactics](https://attack.mitre.org/tactics/enterprise/) · [T1110](https://attack.mitre.org/techniques/T1110/) |
| 8 | *"What is the MD5 hash of the malware"* | 🟢 **The right question, for the wrong-looking reason — and the room never says which.** CERT/CC **VU#836068**: *"Weaknesses in the MD5 algorithm allow for collisions in output. As a result, attackers can generate cryptographic tokens or other data that illegitimately appear to be authentic"* — the break is **collision resistance**; preimage resistance is not practically broken, which is why lookup survives. 🟢🟢 NIST's **NSRL** ships *"Cryptographic hash values (MD5 and SHA-1) of the file's content"* that *"uniquely identify the file even if, for example, it has been renamed"*, used *"to eliminate known files … during criminal forensic investigations"*; VirusTotal's file-report `id` is documented as *"SHA-256, SHA-1 or MD5 identifying the file"*. **The same agency publishes MD5 hash sets and excludes MD5 from approved cryptography, because they are different problems.** ⚠️ The FIPS 180-4 exclusion is **NOT VERIFIED** — not read; CERT/CC carries the break, NSRL the lookup. | [CERT/CC VU#836068](https://www.kb.cert.org/vuls/id/836068) · [NIST NSRL](https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl/about-nsrl/nsrl) · [VirusTotal file API](https://docs.virustotal.com/reference/file-info) |

### NOT VERIFIED — carried forward honestly

- **Ubuntu logrotate policy for Apache and nginx**, and the literal `/var/log/apache2` /
  `/var/log/nginx` paths from a primary doc. **Read both off the evidence.**
- **The Debian/Ubuntu-patched `auditd.conf`** — upstream values given; distro copy unconfirmed.
- **A direct "ROTATE deletes old logs" sentence** — established by contrast with `keep_logs`, whose
  documented purpose is *"This prevents audit logs from being overwritten."* Flagged as inference.
- **Whether Ubuntu's `friendly-recovery` passes `sulogin --force`.** Mechanism documented,
  invocation not. **Test on a VM; it takes thirty seconds and is a better exercise anyway.**
- **A NIST-authored sentence naming MD5** (FIPS 180-4 §1) — not read.
- **Which artifact supplies Q1's answer if the target was `xmlrpc.php` rather than `wp-login.php`** —
  the room does not say, and the two have different evidential properties (#3).

## 4. Evidence used

**A two-machine lab: an AttackBox plus a target VM reached over SSH.** No image, no download, no
published hash — the evidence exists only inside the running lab.

- **Downloadable?** ⚠️ **No.** Unusable for us on that ground alone.
- **Licence?** Not stated; subscription-gated. **D22 forbids rehosting** and there is nothing to
  rehost.
- **Reusable?** 🔴 **No** — not obtainable, and its artifact set is Linux, excluded by **D38**.
- **`ecdfp-evidence` action: none.** 🔴 **Second room running to yield no evidence set.** `EVS-10`
  remains unallocated.

### 🔴 The credential defect, and it is worse here than in room 21

**The room publishes the target's SSH username and password in the task body** (not reproduced —
**R8**). Rooms 18, 21 and now 23 all do this.

⚠️ **What makes this instance worse is the pairing.** The same room then asks the student to obtain
a **root shell via the bootloader** (§2.7). So the material demonstrates two credential-handling
behaviours back to back: *publish a working password in plaintext*, and *bypass authentication
entirely*. **Neither is accompanied by a single sentence about handling.** For a room whose scenario
is a company that lost everything because a control was misconfigured, that is an unforced irony.

**Our version:** lab credentials are issued out of band and never printed in the material; any
material that shows a credential shows a **redacted** one; and the bootloader exercise is preceded by
the handling rule in §2.7, not followed by it.

### 🟢🟢 Critique of the scenario brief — the best one in the set

Rooms 21 and 22 prejudiced the case (behaviour, then conclusion). **This brief does neither.** It
states a business situation, a deadline, an action taken by a named junior employee, and an outcome —
and **it never tells the student what to conclude.** The three tips are *technical orientation*
(*"The system is running WordPress on port 80"*, *"Auditd is configured with non-standard audit
rules"*, *"Emily did not properly configure the DeceptiPot"*), not answers.

⚠️ **One asymmetry worth naming in class:** the third tip is a *finding* handed over as a *given*.
*"Emily did not properly configure the DeceptiPot"* is the conclusion of the whole exercise, stated
up front. 🟢 **Defensible here** — it scopes a 60-minute challenge rather than prejudicing an
attribution — **but the S1 exercise should ask students to spot the difference** between tip 1
(orientation) and tip 3 (a conclusion in orientation's clothing). **That is a sharper version of the
room-21/22 pairing, and it uses a brief that is otherwise well made.**

## 5. Lab design worth reusing

### 5.1 🟢🟢 The published module map — the single best structural idea in the extraction set

Task 1 carries a network diagram with **all six attack stages numbered on it** (§7), and every room
in the module says which number it covers: *"This room is about the first attack stage (#1 on the
network diagram)."*

**That solves the problem room 22 §5.5 raised.** TryHackMe needs each room to stand alone; we need
**D8/D19**'s one incident carried across six sessions. The diagram does both at once:

- A student who has done every prior room reads it as **a timeline they helped build.**
- A student who has done none reads it as **the given context** — the map *is* the catch-up state.
- 🟢 And the numbering makes the **scope of the current session explicit**, which is exactly what
  our `[INVESTIGATION]` rows need: *this session, this host, this stage.*

**Adopt outright.** One diagram, drawn once, appearing on the first page of all six sessions with the
current stage highlighted. **Cost: one figure, reused six times.** It replaces the per-session
catch-up prose room 22 suggested with something cheaper and better.

⚠️ **One correction when we draw ours: use documentation IP ranges.** The module uses `172.16.x.x`
(RFC 1918); **D19 requires documentation ranges** (RFC 5737 `192.0.2.0/24`, `198.51.100.0/24`,
`203.0.113.0/24`). Trivial, but it is the kind of thing that gets copied by accident.

### 5.2 🟢🟢 The scenario is a control failure, not a user error

§1 covers why: a junior with a deadline, no change process, a DMZ deployment, a weekend window.
**Adopt the shape for `S1` and for D19's opening.** Our carry-through incident currently starts with a
malicious document — the classic. **This is better**, because the class can be asked *"which control
failed?"* and get five defensible answers instead of *"the user clicked"*.

🟢 **And it makes the honeypot lesson land** — §2.8's *instrumentation is not security* generalises to
every detective control we teach, which is the most reusable idea in the room.

### 5.3 🟢🟢 Q6 is an access question, not an artifact question

*"Can you access the DeceptiPot in recovery mode?"* is the only question in 23 rooms that asks the
student to **get into a machine** rather than parse something out of one. **It is directly in scope
despite D38**, because the argument is platform-neutral: the same reasoning runs on Windows with a
boot USB, and it is the honest answer to *"why do we bother with write blockers?"*

**Site it in `S1-08` (write blocking) and `S2` (acquisition)** — see §8. ⚠️ **But invert the order**:
the handling rule first, the technique second. §5.5.

### 5.4 🟢 Three tips instead of a walkthrough

The room gives orientation (*"running WordPress on port 80"*), a hint that a non-default artifact
exists (*"Auditd is configured with non-standard audit rules"*), and a scope statement (*"Emily did
not properly configure the DeceptiPot"*) — **and then nothing.** That is the right amount of
scaffolding for a 60-minute investigation and matches the shape of our `[INVESTIGATION]` rows.

⚠️ Tip 2 exists because the artifact is **not a default** (§3 #1). 🟢 **Our version should say so out
loud** — *"this host runs auditd; most do not"* — because **the fact that the tip was necessary is
itself the finding.**

### 5.5 🔴 Safety and handling defects

**One new, and it is an evidence defect — the ninth in the project.**

🔴🔴 **Q6 asks the student to reboot the machine they are investigating, with no handling statement
whatsoever.**

Booting into recovery mode or appending `init=/bin/bash`:

1. **Destroys all volatile evidence** — running processes, network connections, memory-resident
   malware, and any attacker shell still attached. Against **D9**'s order of volatility, this is the
   most destructive single action available to the student, and the room asks for it **last**, after
   they have already established the host was compromised.
2. **Mounts and modifies the disk** — the same defect as room 22 §5.6, one layer lower. Filesystem
   timestamps, journal replay, `/var/log` writes on the next boot.
3. **Produces no record of itself** (§2.7), so **an examiner cannot later distinguish the student's
   own boot from the attacker's.** 🔴 That is the part that makes it a genuine forensic defect rather
   than merely untidy: **the investigator's action is indistinguishable from the adversary's in the
   evidence.**

🟢 **In fairness, the technique is worth teaching and the room is right to include it.** The defect is
the missing sentence, not the exercise.

**Our version:** the exercise runs on a **throwaway clone**, never on the imaged evidence; it is
preceded by the rule from §2.7 — *for acquisition, boot external read-only media and image the disk;
never `init=/bin/bash` a machine you intend to treat as evidence* — and it ends with the student
**recording the boot in the chain-of-custody form as an examiner action**, which is the habit that
makes the difference legible later.

**Running total: 9 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23. Four endanger the analyst's
machine; five endanger the evidence.** ⚠️ **All five evidence defects involve booting or mounting a
system rather than imaging it first** — that is now a pattern across the corpus, not a coincidence,
and it deserves a named slide in `S2`.

⚠️ **Not counted as a new defect, but recorded:** the room **publishes plaintext SSH credentials**
(§4), the third Priority-2 room to do so. It endangers neither the analyst's machine nor the
evidence, so it does not enter the tally — **but three rooms in a row is a house style**, and our
answer to it is in §4.

## 6. Question patterns

**Six scored questions plus a "Let's go!" gate, across two tasks — a single unbroken investigation
with three tips and no scaffolding.** The right shape.

**🟢🟢 Q6 breaks the mould entirely** — *"Can you access the DeceptiPot in recovery mode?"* is an
**access** question, not an artifact question (§5.3). Twenty-three rooms, and this is the first.

**🟢 The question set traces a clean kill chain** — brute force → webshell → privesc → discovery →
persistence — so a student who answers all six has reconstructed the intrusion in order **without
being told the order.** That is better than room 21's published-chain model for a *first* session,
and the two compose: publish the chain later, discover it first.

**⚠️ Stems assert their conclusions, again** — *"the **backdoored** PHP file"* · *"the malware
**persisting** on the host"* · *"Which IP was port-scanned **after the privilege escalation**"*.
🟢 **Q4's clause is defensible**, though: it orders the timeline for the student rather than
prejudicing an attribution, which is scaffolding, not prejudice. **Sixth room in a row with the
pattern; first where at least one instance earns its keep.**

**⚠️ Q1 presumes a single brute-forced page.** Per §3 #3, `wp-login.php` and `xmlrpc.php` have
completely different evidential properties — one POST ≈ one attempt versus one POST ≈ hundreds — and
**the room never makes the student say which they found.** A correct answer to Q1 that names
`xmlrpc.php` implies a different attempt count than one naming `wp-login.php`, and the room treats
them as interchangeable.

**🔴 Twenty-third room, no "cannot be determined" question** — and this room is the richest source of
them so far, because **five of its six artifacts have a limit the question walks straight past:**

| the room could have asked | correct answer |
|---|---|
| *"Which username did the attacker brute-force?"* | 🔴🔴 **Cannot be determined from the access log.** No request body is logged, and `%u`/`$remote_user` is HTTP-auth only — *"If the document is not password protected, this part will be `-`"*. **And WordPress logs failed logins nowhere by default.** If a student produces a username, they must name the source — a plugin, `wp_users`, a WAF, or auditd. |
| *"How many login attempts did the attacker make?"* | 🔴🔴 **Cannot be determined if the target was `xmlrpc.php`** — `system.multicall` carries an array of calls in one POST. Twelve log lines may be thousands of guesses. **Against `wp-login.php` the same question is perfectly answerable.** The best row here, because the answer depends on which page Q1 identified. |
| *"When was the webshell created?"* | ⚠️ **Not from the file.** mtime is set by whatever wrote it and `touch -r` blends it into the directory; ctime is harder but root-forgeable. **Date it from the access log request, not the inode.** |
| *"Three SUID binaries are misconfigured. Which did the attacker use?"* | 🔴 **Cannot be determined from `find -perm -4000`** — that is *state*, not an event. It needs `sudo`'s log or an auditd syscall record. **The honest report says "these three would each have worked."** |
| *"auditd shows no port scan before 14:00. Did one happen?"* | 🔴🔴 **Cannot be determined.** The attacker had root: `auditctl -e 0` … act … `-e 1` leaves **no deletion marker**. And with `max_log_file 8` × `num_logs 5` the whole log is ~40 MiB. **Only `-e 2` (immutable) changes the answer** — check `auditctl -s` first. |
| *"The DeceptiPot captured nothing after 02:14. Did the attack stop?"* | 🟢🟢 **No — the attacker left the instrumented surface.** A honeypot records attacks against the service it emulates, not against the host it runs on. **The single best question in this table**, because it turns the room's own premise into the lesson (§2.8). |
| *"Was this machine ever accessed via recovery mode?"* | 🔴🔴 **Cannot be determined at all.** Nothing logs it — no PAM, no `auth.log`, no `auid`, no auditd. **A question with no answer anywhere on the disk, which is the purest form of the thing we are trying to teach.** |
| *"The malware's MD5 matches a known sample. Is it that sample?"* | ⚠️ **Almost certainly, but not provably** — MD5's **collision** resistance is broken, so for adversary-influenced content a match is not proof of identity. **Preimage resistance holds, which is why the lookup is still worth doing.** |

🟢🟢 **Eight, and two of them — the honeypot row and the recovery-mode row — are questions no other
room in the corpus could ask**, because they depend on this room's own scenario. **That is the
strongest argument yet that "cannot be determined" questions are not a gimmick: they fall out of the
scenario if the scenario is well built.**

## 7. Figures

🟢🟢 **This room has the first genuinely valuable figure in 23 rooms, and it was viewed** — lightbox
and zoom. `A diagram of the DeceptiTech network`, SVG, 1760 × 670, in Task 1. Every other image is
decorative (room icon 600 × 600, banner 1920 × 300, hero, avatars, target-machine placeholder).

### The module map, transcribed

**AWS Environment** (isolated product platform) — `deceptipot-emea`, `deceptipot-na`,
`deceptipot-apac` compute clusters. **No attack stage touches it.**

**Remote Users** — Lucas Rivera (Lead Developer) **⑥** · Emily Ross (IT Support) · Matthew Collins
(IT Administrator).

**DeceptiTech Corporate Network**, on-premises AD, ~50 users, two subnets:

| stage | host | address | subnet | platform |
|---|---|---|---|---|
| — | `deceptitech-web` | 172.16.8.8 | DMZ 172.16.8.0/24 | web server, **not a stage** |
| **①** | `deceptipot-demo` | 172.16.8.239 | DMZ | **Linux** — Emily's honeypot. **This room.** |
| **②** | `SRV-IT-QA` | 172.16.8.216 | DMZ | Windows |
| **③** | `SRV-DMZ-GW` | 172.16.8.15 | DMZ | Windows |
| **④** | `SRV-CRM-01` | 172.16.2.9 | CORE 172.16.2.0/24 | Windows |
| **⑤** | `DC-01` | 172.16.2.4 | CORE | Windows — **domain controller, drawn with a padlock** |
| — | `SRV-FSSQL-PRD` | 172.16.2.11 | CORE | file/SQL, **target of ⑤** |
| — | `SRV-FSSQL-FIN` | 172.16.2.17 | CORE | file/SQL, **target of ⑤** |

**Attack path drawn in red:** ① → ② → ③ **→ across the subnet boundary →** ④ → ⑤, then ⑤ fans out to
both file/SQL servers. **⑥ is a remote user, outside both subnets.**

🟢🟢 **Four structural readings, and they are why this diagram was worth opening:**

1. **The arc is DMZ → CORE → DC → out to a person.** Five host stages then a *human* — so the module
   almost certainly ends on the endpoint of a remote developer, not another server.
2. **Stage ① is the only Linux host in the chain.** Under **D38** that means **rooms 24–28 are all
   Windows and all potentially in scope** — this room is the one Linux entry point, and its
   out-of-scope content is bounded to a single stage.
3. **The lateral path crosses the DMZ/CORE boundary exactly once, at ③ → ④.** That single edge is
   where the architecture failed, and it is the most teachable point on the whole map.
4. **The two file/SQL servers are drawn as targets, not stages** — so the module ends with impact
   (encryption, the wiped SIEM) rather than another investigation. **Our S6 capstone should do the
   same: the last stage is consequence, not another artifact.**

⚠️ **Verify readings 1 and 2 against rooms 24–28 rather than trusting this table** — the stage
numbers are the room's, but the platform column is my inference from the host icons and names.

### Figures we must draw

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F7 | **Our module map** | The D19 incident as one diagram: hosts, subnets (documentation ranges — §5.1), the attack path in a single accent, **stages numbered 1–6 to match the sessions**, current stage highlighted per page. | **🔴 P1** | §5.1. **One figure, six sessions.** The single highest reuse-per-effort item in the project. |
| F8 | **The 200/302 login signal** | Access-log excerpt: a column of `POST /wp-login.php → 200` in muted grey, one `→ 302` highlighted, then `GET /wp-admin/ → 200` seconds later. Callout: *"this timestamp is the compromise."* | **🔴 P1** | §2.1. The most immediately usable investigative technique in the note. |
| F9 | **What the access log cannot hold** | One HTTP POST drawn as head + body; the head shaded "logged", the body shaded "never logged". Beside it `%u` resolving to `-`. Inset: one xmlrpc POST expanding into N credential attempts. | **🔴 P1** | §2.1's three limits in one image; feeds the "absence of evidence" thread. |
| F10 | **State vs event** | Two columns: *opportunity* (`find -perm -4000`, `getcap -r /`, a writable unit) against *event* (a `sudo` log line, an auditd `auid` record, a cron execution). Arrow: *"only the right column has a timestamp."* | **🔴 P1** | §2.3/§2.4 — the distinction is the whole privesc lesson and generalises to Windows unchanged. |
| F11 | **`auid` survives escalation** | Process chain `sshd → bash (auid=1000 uid=1000) → sudo → bash (auid=1000 uid=0)`, with `uid` changing and `auid` constant and highlighted. | **🟢 P2** | §2.5. Only for the S1 contrast row, per D38 — but it is the clearest picture of attribution in the whole corpus. |
| F12 | **Boot to root** | Timeline of a boot: GRUB → kernel → **`init=/bin/bash`** → root shell, with PAM, auditd, AppArmor and logging drawn as boxes that **never start**. | **🔴 P1** | §2.7 + §5.5. Platform-neutral, and the best justification for write blocking we have. |
| F13 | **Coverage vs absence** | A honeypot's emulated service drawn as a lit circle; the host it runs on drawn dark; the attacker's path crossing from lit to dark. Caption: *"the tool saw nothing" ≠ "nothing happened."* | **🟢 P2** | §2.8 generalised to Sysmon, auditd and access logs — the D20 criterion-4 idea as a picture. |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 1"* — correct, and incomplete in a useful way.

It is step 1 of the chain **and** the module's map-bearer (§7) **and**, unexpectedly, the best source
we have found for **`S1-06`**. Amend the Part 1 row to note that its value is not the Linux content —
which **D38** excludes — but the **scenario shape, the map, and three platform-neutral lessons**:
hashing, boot-to-root, and state-vs-event.

### Rows this strengthens

- **`S1-06`** (*"Cryptographic hashing for evidence — MD5, SHA-256, what a hash proves and what it
  does not"*) — 🟢🟢 **the row is already named for exactly this lesson and this room supplies its
  content**: the CERT/CC collision break, the preimage/collision distinction that explains *why*
  lookup survives, and **the NSRL card — NIST publishes MD5 hash sets while excluding MD5 from
  approved cryptography, because they are different problems.** Plus the one-line rule and the
  record-both habit (§2.6). **Strictly better content in an existing 18-minute row.**
- **`S2-01`** (*"Order of volatility in practice — the collection sequence, and **what you destroy by
  getting it wrong**"*) — 🟢🟢 **figure F12 and §2.7/§5.5 make that row concrete.** Booting a suspect
  host to a root shell destroys every volatile artifact *and* leaves no record that the examiner did
  it. **The row currently teaches the principle; this gives it the worst-case demonstration**, and it
  is platform-neutral. `S1-08` (write blocking) gains one sentence pointing at it.
- **`S5-06`** (*"Amcache and ShimCache — presence vs execution, and the classic misreading"*) —
  🟢🟢 **figure F10 belongs here and adds no minutes.** *State vs event* is the same lesson as
  *presence vs execution*, one abstraction level up: `find -perm -4000` and a writable unit are
  opportunity; a `sudo` line and a cron execution are events. **Generalising the row this way makes
  the Amcache misreading a specific case of a rule rather than a fact to memorise.**
- **`S6-01`** (*"Network evidence sources — pcap, flow, logs, and what each can and cannot prove"*) —
  figure **F9** puts Apache/nginx beside our existing IIS material (**G9/G10**) and shows the request
  body as the thing no access log holds. **Replaces generic content; does not add.**
- **`S1-04`** (the report template) — figure **F13**, *"the tool saw nothing" ≠ "nothing happened"*,
  which is **D20 criterion 4** stated as a coverage question (§2.8).
- **`S1-01`** — the **F11** `auid` row joins the D38 contrast table: the Linux column's one genuine
  advantage over Windows, which is worth showing precisely because the other rows run the other way.
- **All six session pages** — figure **F7**, the module map (§5.1).

### 🟢🟢 Back-propagation: none again — and this time it was close

The ATT&CK revocation in §3 #7 is the largest mapping change the project has met, and it could have
invalidated three notes. It did not, and each was checked rather than assumed:

- **T1562 (revoked → T1685)** — ✅ **appears nowhere in the repo.** Grepped.
- **T1070.001 / .002 (moved to T1685.005 / .006)** — ✅ we cite only **T1070.004, .006 and .009**,
  and **T1070 itself is live at v3.0 with all three still under it** — independently confirmed by
  fetching the technique page, not inferred from the sub-agent's report.
- **T1548.001 / .003 and T1505.003 now single-tactic** — ✅ none of the three appears in the repo.

**Second room running with zero back-propagation actions.** ⚠️ **But this one is a warning, not a
reassurance:** the repo is clean because it is still small and mostly THM notes. **`S6-06` will want
"clear Windows event logs" the moment it is written, and the answer is `T1685.005`, not `T1070.001`.**
Recorded in block **K** so the correction is waiting when the row is built.

### Minutes

**Net zero, plus one homework.** Every item above lands as content inside a named existing row —
`S1-01`, `S1-04`, `S1-06`, `S2-01`, `S5-06`, `S6-01` — and F7 is a page element, not a topic.

**The one genuine addition is the 200/302 technique (F8)**, which needs ~5 minutes S6 does not have.
🟢 **It becomes S6 homework**, the same disposition as the room-21/22 brief critique in S1: a log
file, one `awk` command, one timestamp, no VM and no evidence set. **Homework is now carrying two of
the last three rooms' additions, which is a pattern worth watching** — it is cheap, but a homework
track that grows without limit is just an unbudgeted session.

**No new rows. S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Eighteenth room carrying the S5 overdraft.** 🟢 **Second room running that adds nothing to it** —
F10 lands in `S5-06` as a reframing, not an addition.

### Out of scope

auditd, Linux privilege-escalation state, WordPress administration, and the honeypot product itself —
per **D38** and `scope_decisions.md`. ⚠️ Three items sit on the line and are worth one sentence each
rather than exclusion:

- **`auid`** — one row in the F1 contrast table. It is the only place the Linux column *wins*, and
  omitting it would make the table dishonest.
- **Web access logs** — already in scope via **S6-01**; this room extends existing IIS material to
  Apache/nginx, which our students meet constantly.
- **The webshell baseline-diff technique** (§2.2) — platform-neutral, and the honest answer to *"how
  do you find a modified file when the timestamps lie."* One sentence in `S3-03` or `S6-09`.

### Still unresolved

- **S5 re-split** — eighteenth room. Unchanged at 65 minutes; no extraction will move it.
- **S4 capstone weighting** — room 18.
- **Lab OS version** — room 21's `WordWheelQuery` constraint. Still gating.
- **🆕 D19 has no per-session host map.** F7 requires our incident to be expressed as *six numbered
  stages across named hosts*, and **D19 currently describes a chain of techniques, not a topology.**
  ⚠️ **This must be resolved before any session page is built**, since F7 appears on all six.
  **Deliberately not decided here** — the module note is the right place, once all six rooms are
  read and the arc is understood.
- **`ecdfp-case` skill** is not installed.
- ⚠️ **`knowledge_base/` EXISTS** — corrected 2026-08-29 while extracting room 25. It was
  built the same day from `Resources/` by `ecdfp-intake`: five condensed module files, an
  `instructor/` folder of 8 session notes, and `_source_text/` holding 10 INE units (2,218 pages)
  plus 9 instructor decks. **`evidence/`, `packages/`, `cases/` and `labs/` still do not exist.**
  🔴 **And the sharper point survives the correction: not one of the room notes has been through
  `ecdfp-intake`.** The knowledge base was built from INE courseware and the instructor's own
  decks — **none of the THM research has landed in it.**

## 9. Links

**Room** — <https://tryhackme.com/room/initialaccesspot>
**Module** — Honeynet Collapse, stage 1 of 6. Stages 2–6:
<https://tryhackme.com/room/elevatingmovement> · <https://tryhackme.com/room/lostinramslation> ·
<https://tryhackme.com/room/crmsnatch> · <https://tryhackme.com/room/shockandsilence> ·
<https://tryhackme.com/room/thelasttrial>
**Companion notes** — `honeynet-collapse-module.md` (the arc, written after stage 6) ·
`exfilnode.md` (D38, and the Linux artifact material this room extends) ·
`_TOOL_CURRENCY_2026-08-28.md` **block K**.

**Citations from §3, by finding:**

- #1 auditd — `auditd.conf(5)` <https://manpages.debian.org/testing/auditd/auditd.conf.5.en.html> ·
  `auditd(8)` <https://manpages.debian.org/testing/auditd/auditd.8.en.html> ·
  `auditctl(8)` <https://manpages.debian.org/testing/auditd/auditctl.8.en.html> ·
  `ausearch(8)` <https://manpages.debian.org/testing/auditd/ausearch.8.en.html> ·
  `aureport(8)` <https://manpages.debian.org/testing/auditd/aureport.8.en.html> ·
  upstream `auditd.conf`
  <https://raw.githubusercontent.com/linux-audit/audit-userspace/master/init.d/auditd.conf> ·
  Ubuntu 26.04.1 live-server manifest
  <https://releases.ubuntu.com/26.04/ubuntu-26.04.1-live-server-amd64.manifest> ·
  RHEL 9 auditing <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening> ·
  `journald.conf(5)` <https://manpages.debian.org/testing/systemd/journald.conf.5.en.html>
- #2 web logs — Apache log files <https://httpd.apache.org/docs/2.4/logs.html> ·
  `mod_log_config` <https://httpd.apache.org/docs/2.4/mod/mod_log_config.html> ·
  nginx `ngx_http_log_module` <https://nginx.org/en/docs/http/ngx_http_log_module.html>
- #3 WordPress — `wp-login.php`
  <https://raw.githubusercontent.com/WordPress/WordPress/master/wp-login.php> ·
  `wp_safe_redirect()` <https://developer.wordpress.org/reference/functions/wp_safe_redirect/> ·
  `wp_login_failed` <https://developer.wordpress.org/reference/hooks/wp_login_failed/> ·
  brute-force hardening
  <https://developer.wordpress.org/advanced-administration/security/brute-force/> ·
  `xmlrpc_enabled` <https://developer.wordpress.org/reference/hooks/xmlrpc_enabled/> ·
  IXR server <https://raw.githubusercontent.com/WordPress/WordPress/master/wp-includes/IXR/class-IXR-server.php> ·
  releases <https://wordpress.org/news/category/releases/>
- #4 web root permissions — WordPress hardening
  <https://developer.wordpress.org/advanced-administration/security/hardening/>
- #5 privesc — `find(1)` <https://man7.org/linux/man-pages/man1/find.1.html> ·
  `capabilities(7)` <https://man7.org/linux/man-pages/man7/capabilities.7.html> ·
  `getcap(8)` <https://man7.org/linux/man-pages/man8/getcap.8.html> ·
  `sudoers(5)` <https://www.sudo.ws/docs/man/sudoers.man/> ·
  `sudo(8)` <https://www.sudo.ws/docs/man/sudo.man/> ·
  `cron(8)` <https://manpages.debian.org/testing/cron/cron.8.en.html> ·
  `systemd.unit(5)` <https://manpages.debian.org/testing/systemd/systemd.unit.5.en.html>
- #6 bootloader — GRUB authentication and authorisation
  <https://www.gnu.org/software/grub/manual/grub/html_node/Authentication-and-authorisation.html> ·
  `bootparam(7)` <https://man7.org/linux/man-pages/man7/bootparam.7.html> ·
  `sulogin(8)` <https://man7.org/linux/man-pages/man8/sulogin.8.html>
- #7 ATT&CK — v19 release notes
  <https://attack.mitre.org/resources/updates/updates-april-2026/> ·
  updates index <https://attack.mitre.org/resources/updates/> ·
  enterprise tactics <https://attack.mitre.org/tactics/enterprise/> ·
  T1685 <https://attack.mitre.org/techniques/T1685/> ·
  T1685.004 <https://attack.mitre.org/techniques/T1685/004/> ·
  T1070 <https://attack.mitre.org/techniques/T1070/> ·
  T1190 <https://attack.mitre.org/techniques/T1190/> ·
  T1505.003 <https://attack.mitre.org/techniques/T1505/003/> ·
  T1110 <https://attack.mitre.org/techniques/T1110/> ·
  T1548.001 <https://attack.mitre.org/techniques/T1548/001/> ·
  T1548.003 <https://attack.mitre.org/techniques/T1548/003/> ·
  T1046 <https://attack.mitre.org/techniques/T1046/>
- #8 MD5 — CERT/CC VU#836068 <https://www.kb.cert.org/vuls/id/836068> ·
  NIST NSRL
  <https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl/about-nsrl/nsrl> ·
  VirusTotal file report <https://docs.virustotal.com/reference/file-info>
