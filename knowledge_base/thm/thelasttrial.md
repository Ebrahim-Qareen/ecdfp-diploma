---
room: The Last Trial
url: https://tryhackme.com/room/thelasttrial
module: **Honeynet Collapse — stage 6 of 6, the final room.** *"Investigate the sixth, macOS part of
        the Honeynet Collapse!"* Challenge room (Priority 2). Target: **Lucas Rivera's macOS
        laptop** — a **Remote User**, outside both subnets on the module map.
feeds: ⚠️ **macOS, therefore OUT OF SCOPE per D38** — like stage 1 (Linux). **The module is
       Linux → Windows ×4 → macOS, so only four of six stages are in scope.**
       🟢🟢 **But it supplies the third column of the D38 contrast table (figure F1)**, and two
       platform-neutral lessons: **enforcement lives in the running OS, not in the data** (§2.3),
       and **the "install" that leaves no installation record** (§2.2).
       🔴🔴 **It also refutes an inference I made in room 26** — corrected there, recorded in §8.
difficulty / time: **Hard** · 60 min · 2 tasks · 7 questions (6 scored + 1 "Let's go!") · Premium ·
                   1,236 completions · 23 recommends
extracted: 2026-08-29
extracted_by: ecdfp-web-extract via Chrome (premium path, logged-in session)
completeness: both tasks read in full — briefing, scenario, analysis approach, mount and tool
              commands, and all question stems. 0 sections NOT READ.
              🟢 **First room in the module that publishes NO credentials** — there is no
              Credentials block in the task text. Nothing to withhold under R8, and worth noting
              after six rooms that did.
              ⚠️ **Answers NOT READ** — lab machine not started. §2 reconstructed from the 6 scored
              questions, the scenario and the named tooling, as for rooms 18–27.
---

## 1. What the room teaches

**That the last host in an intrusion chain may have nothing to do with the intrusion — and that the
module is willing to say so.**

The brief is the most quietly interesting in the six:

> *"But, amidst this primary attack, another critical compromise took place, this time on a macOS
> system. Lucas, the lead developer of DeceptiTech, unintentionally became a victim of a **different**
> compromise."*
> *"**Not every attack is targeted. Sometimes, your curiosity makes you fall into a trap.**"*

🟢🟢 **Two compromises, one organisation, one week, and the module refuses to connect them.** After
five rooms of a single escalating chain, the final stage is a **coincidence** — a developer who
downloaded a trojanised *"free trial of an AI development tool"* he found while browsing.

⚠️ **That is a deliberate design choice and it is a good one**, because it is the shape real
engagements take: an incident scope that seems obvious turns out to contain two unrelated things, and
the analyst who assumes one story writes a wrong report. 🔴🔴 **I know this because I made exactly
that error one room earlier** — see §8, and the correction now standing in `crmsnatch.md` §5.2.

**The lure is current and worth noting for its own sake.** A free AI-tool trial, found while
browsing, that installs an infostealer, requests privacy permissions and beacons out is the dominant
macOS social-engineering pattern of 2025–26. 🟢 **The room does not need a zero-day and does not
pretend to have one** — *"Sometimes, your curiosity makes you fall into a trap"* is the entire
initial access vector, and it is honest.

**What it teaches that transfers, despite the platform being out of scope:**

- 🟢🟢 **`TCC.db` is unreadable on the live system and trivially readable from the image** (§2.3).
  **Enforcement lives in the running OS, not in the data** — and that is a platform-neutral
  acquisition argument as strong as anything in the Windows rooms.
- 🟢🟢 **The macOS download-provenance artifact is split in two** — a UUID on the file, the URL in a
  user database (§2.1) — where Windows keeps both together in one ADS. **That asymmetry has real
  investigative consequences and it is the best row F1 will have.**
- 🔴 **A drag-and-drop install leaves no installation record at all** (§2.2), so Q3's *"when was the
  malicious application installed"* may be unanswerable from the artifacts that are supposed to
  answer it — **the third room running whose own question outruns its evidence.**

**What it gets wrong:** very little, and less than any other room in the module.

- ⚠️ **Q4 — *"Which TCC permission did the application request **first**?"*** — presumes ordering the
  artifact may not preserve. `access` rows carry `last_modified`, which is **last** modification, not
  first grant (§2.3).
- ⚠️ **Q6 — *"Which persistence mechanism did the application use?"*** — a single-answer stem for a
  question whose honest answer may be a list.
- 🟢 **And credit where it is due: no published credentials, a read-only mount command, a named tool
  with a documented path, and a warning that the VM takes four minutes to boot.** **That is the most
  carefully assembled lab of the six.**

## 2. Artifacts — one 6-box block each

⚠️ Reconstructed from the 6 scored questions, the scenario and the analysis instructions. Mapping:
Q1/Q2 → 2.1 · Q3 → 2.2 · Q4 → 2.3 · Q5 → 2.4 · Q6 → 2.5 · the image and mount → 2.6 ·
`mac_apt` → 2.7 · the lure → 2.8.

### 2.1 The quarantine pair — macOS's answer to Zone.Identifier, and it is split in two

- **What it is** — Q1 (*"the website from which the user downloaded the malicious application's
  installer"*) and Q2 (*"the name of the malicious application's installer"*).
- **Where it lives** — 🔴🔴 **two places, and the split is the point:**
  1. **The `com.apple.quarantine` extended attribute**, on the downloaded file. Its value is a
     four-part string of the form `0083;5991b778;Safari.app;BC4DFC58-…` — *"the quarantine value in
     hexadecimal, the time at which the xattr was attached, in hexadecimal, the app or agent
     responsible for creating the xattr, [and] a UUID referring to the entry for this quarantine flag
     in the QuarantineEvents database."* **🔴 Note what is absent: there is no URL in the xattr.**
  2. **`~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2`** — an SQLite database,
     table **`LSQuarantineEvent`**, columns **`LSQuarantineTimeStamp`**,
     **`LSQuarantineDataURLString`**, **`LSQuarantineOriginURLString`**, **`LSQuarantineAgentName`**,
     **`LSQuarantineAgentBundleIdentifier`**, **`LSQuarantineEventIdentifier`**. ⚠️ Timestamps are
     **Cocoa epoch** — add **978,307,200** seconds to reach Unix time.
- **What it proves** — 🟢🟢 **that a file was downloaded from a recorded URL, by a named application,
  at a recorded time** — with the **UUID as the join key** between the file and the record.
- **What it does NOT prove** — 🔴🔴🔴 **the contrast with Windows is the finding, and it runs both
  ways:**
  **Windows' `Zone.Identifier` keeps the URL *in an ADS attached to the file*** (**O2**). **macOS
  keeps a UUID on the file and the URL in a per-user database.** Consequences:
  - 🔴 **Delete the macOS database and *every* downloaded file on that profile loses its provenance
    at once** — the xattrs remain but point at nothing. **On Windows, removing one file's ADS affects
    one file.** **One command versus one file: that is a materially different anti-forensic cost.**
  - 🟢 **Conversely, macOS's record survives the file's deletion** — the database row persists after
    the installer is gone, where a Windows ADS dies with its file. **Each platform preserves what the
    other loses.**
  ⚠️ **Which column means what is NOT VERIFIED.** Secondary sources gloss `DataURLString` as the
  direct download and `OriginURLString` as the referring page, but **no primary source defines them**.
  **Teach the column names; do not teach the gloss.**
  ⚠️ **A correction to the obvious assumption about fragility:** FAT/exFAT do **not** simply destroy
  xattrs — *"Files that are copied to non-native file systems including FAT and ExFAT volumes can
  preserve xattrs in hidden shadow files, but those copied to NFS will have all their xattrs
  stripped."* **NFS strips them; `xattr -d` removes them deliberately.**
  🔴 **And whether the database is still populated on the current macOS is NOT VERIFIED.** The
  **xattr** is confirmed current (an April 2026 source describes it in the present tense), and the
  database path is unchanged in current tooling — **but no source tested the database on macOS 26.**
  **Do not assert it in class.**
- **How to parse it** — `xattr -p com.apple.quarantine <file>` on a live system; from an image, read
  the xattr and query the SQLite database directly, joining `LSQuarantineEventIdentifier` to the
  xattr's UUID. 🟢 `mac_apt` automates it (§2.7).
- **Anti-forensics / false-positive caveat** — ⚠️ **the agent name is a claim about the downloader,
  not the origin** — `Safari.app` means Safari wrote the record, not that Safari is trustworthy.
  🟢 **And as on Windows, presence is stronger than absence**: the OS writes it, so its presence is
  hard to fake and its absence has many innocent explanations.

### 2.2 Installation time — and the install that leaves no record

- **What it is** — Q3: *"When was the malicious application installed in the system?"*, answer format
  `2025-01-15 12:30:45`.
- **Where it lives** — the package-installer artifacts:
  **`/Library/Receipts/InstallHistory.plist`** — *"records App Store and Installer app
  installations"*, an XML plist carrying *"installation dates, app names, versions, URLs, and
  installer process names"* — and **`/var/db/receipts/`**, holding BOM and plist files:
  *"Complete records of individual files installed by each package."*
- **What it proves** — for anything installed by a `.pkg`, a precise, attributed installation event.
- **What it does NOT prove** — 🔴🔴🔴 **that an absence means it was not installed. A drag-and-drop
  application from a DMG produces no receipt and no `InstallHistory` entry at all** — the mechanism
  *"bypasses the mechanisms built into OS X for recording installation and updating"*, and the same
  source concludes: *"If you want to keep a record of those events, you will need to keep your own
  notes, I am afraid."*
  🔴 **A "free trial" downloaded as a DMG and dragged to `/Applications` is exactly that case** —
  which is the most likely shape of this room's scenario. **So Q3's answer may have to come from
  somewhere else entirely**: the quarantine timestamp (§2.1), the bundle's filesystem timestamps,
  or FSEvents.
  ⚠️ **And those substitutes are weaker in specific ways.** The quarantine timestamp is when the
  file was **downloaded**, not installed. Filesystem timestamps on a copied bundle reflect the copy,
  and can be preserved from the source by the copying method. **"Installed" is a word that assumes a
  mechanism, and if the mechanism was drag-and-drop the word does not have a precise referent.**
  🟢🟢 **That is a real and transferable idea: some questions are unanswerable not because evidence
  was destroyed but because the event was never an event the system records.** Same family as **O4**
  and **L1**.
- **How to parse it** — read `InstallHistory.plist` and `/var/db/receipts/`; if empty for this app,
  pivot to §2.1's timestamp and the bundle's own dates, **and say which one you used.**
- **Anti-forensics / false-positive caveat** — 🟢 **no anti-forensics is involved**, which is what
  makes it instructive. ⚠️ **A report that gives a single timestamp for "installed" without naming
  the artifact behind it is unfalsifiable** — and here three candidate artifacts give three different
  answers.

### 2.3 `TCC.db` — and the lesson that outlives the platform

- **What it is** — Q4: *"Which TCC permission did the application request first?"* **TCC** —
  *"Transparency, Consent, and Control … a mechanism in macOS to limit and control application access
  to certain features, usually from a privacy perspective."*
- **Where it lives** — **two databases**: the **user** one at
  `/Users/<username>/Library/Application Support/com.apple.TCC/TCC.db`, and the **system** one at
  `/Library/Application Support/com.apple.TCC/TCC.db`. The **`access`** table records
  *"the requesting application bundle ID, the service being accessed, the authorization decision, and
  a timestamp of when access was granted or denied"* — columns **`service`**, **`client`**,
  **`client_type`**, **`auth_value`**, **`auth_reason`**, **`last_modified`** (plus `csreq`,
  `policy_id`, `flags`, `prompt_count`). **`auth_value`: *"denied(0), unknown(1), allowed(2), or
  limited(3)"***.
- **What it proves** — 🟢🟢 **which application asked for which privacy-sensitive capability, and
  what the user answered.** For an infostealer that is close to a statement of intent: a "developer
  tool" requesting screen recording or full-disk access is doing something its description does not
  cover.
- **What it does NOT prove** — 🔴🔴 **the ordering Q4 asks for.** The column is **`last_modified`** —
  *last*, not first. **A permission granted, revoked and re-granted carries only the most recent
  timestamp**, so *"which did it request **first**"* is answerable only if nothing was subsequently
  changed, and the database cannot tell you whether that is true. ⚠️ **`prompt_count` is a hint that
  more happened than one row shows**, and should be read alongside.
  🔴 **Nor does a row prove the capability was used** — an `allowed` entry is authorisation, not
  activity. **Permission ≠ access**, the same distinction as *presence vs execution* (**L2**) and
  *state vs event* (room 23 §2.3).
  ⚠️ **And the two databases mean different things** — a user-level grant is that user's decision;
  a system-level entry is administrative. **Reporting "TCC shows X" without saying which database is
  an incomplete finding.**
- **How to parse it** — read the SQLite directly from the mounted image, or `mac_apt`'s
  `plugins/tcc.py`, which *"Parses TCC.db and extract date, service name, app bundle id, and so on."*
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the asymmetry here is the single most
  transferable thing in this room, and it is platform-neutral.**
  **On a live Mac you cannot read these databases**: *"The previous databases are also TCC protected
  for read access. So you won't be able to read your regular user TCC database unless it's from a TCC
  privileged process."* ⚠️ **Be precise about the mechanism:** the **user** database is
  **TCC-protected**, not SIP-protected; the **system** database is **SIP-protected** — *"This
  database is SIP protected, so only a SIP bypass can write into it."*
  🟢🟢 **From a mounted image, both are ordinary SQLite files.** **The protection is enforced by the
  running operating system, not carried by the data** — so it evaporates the moment the disk is read
  by something else.
  **That is a general principle worth teaching in `S2-04`:** *access controls are a property of the
  live system; imaging the disk removes the enforcer.* **It is why offline analysis sees things live
  response cannot** — and it is the same reason a Windows registry hive read from an image ignores
  the permissions that guarded it. ⚠️ **It also cuts the other way: it is precisely why an evidence
  image must be handled as sensitive data**, because every access control the subject relied on is
  gone.

### 2.4 The C2 URL

- **What it is** — Q5: *"What is the full C2 URL to which the application exfiltrated data?"*
- **Where it lives** — not a named artifact. Realistically: **strings inside the application bundle**
  (`/Applications/<app>.app/Contents/MacOS/`), its **plists** and embedded scripts, the **persistence
  plist's** `ProgramArguments` (§2.5), shell histories, and — if present — proxy or DNS caches.
- **What it proves** — that a URL appears in code or configuration on the host.
- **What it does NOT prove** — 🔴🔴 **that data was sent to it.** Exactly as in room 26 §2.3: **a URL
  in a binary is a capability, not a transmission.** Proof of exfiltration needs network evidence,
  and a single laptop image has none. ⚠️ **And "C2" is an interpretation** — the stem asserts a role
  the string does not carry. 🔴 A binary may contain several endpoints, dead infrastructure, or
  decoys.
  ⚠️ **ATT&CK mapping is worth getting right and the obvious choice is wrong:** an HTTP POST to
  attacker infrastructure is **T1041 Exfiltration Over C2 Channel** (*"Adversaries may steal data by
  exfiltrating it over an existing command and control channel"*), **not T1567.002**, which is
  *Exfiltration to Cloud Storage* and is scoped to services like Dropbox or S3. **Room 26's rclone
  case was T1567.002; this one is T1041, and the difference is the destination, not the protocol.**
- **How to parse it** — `strings` over the bundle, read the plists, and check the persistence
  plist's arguments. **Record the string as a finding and its role as an interpretation.**
- **Anti-forensics / false-positive caveat** — ⚠️ **modern stealers fetch their endpoint at runtime**
  rather than embedding it, in which case **the URL is in memory and not on disk at all** — and this
  room supplies only a disk image. 🟢 **"No C2 URL found on disk" is therefore a normal result**, and
  the honest finding names memory as the artifact that would settle it (**M1**).

### 2.5 Persistence — Launch Agents and Launch Daemons

- **What it is** — Q6: *"Which persistence mechanism did the application use?"*
- **Where it lives** — property lists in four locations, and **the location is the privilege claim**:
  **`~/Library/LaunchAgents`** (this user), **`/Library/LaunchAgents`** (all users),
  **`/System/Library/LaunchAgents`** (Apple), and **`/Library/LaunchDaemons`** +
  **`/System/Library/LaunchDaemons`** (system-wide, pre-login).
  ATT&CK: **T1543.001 Launch Agent** — *"Launch Agents are created with user level privileges and
  execute with user level permissions"* — and **T1543.004 Launch Daemon** — *"Launch Daemons require
  elevated privileges to install, are executed for every user on a system prior to login."*
  **Both are Persistence + Privilege Escalation.** ⚠️ **Neither carries the Stealth tactic** — checked
  specifically, because the TA0005 rename (**E11**) makes that an easy assumption to get wrong.
- **What it proves** — 🟢🟢 **that something was configured to run automatically, and at what
  privilege.** **A daemon rather than an agent is itself a finding**: it means the installer obtained
  administrative rights, which narrows how the compromise proceeded.
- **What it does NOT prove** — 🔴🔴 **that it ran, or that it is the only mechanism.** A plist is
  configuration; execution is a separate artifact (**the same *state vs event* distinction as room
  23 §2.3**). ⚠️ **Q6's singular phrasing — *"Which persistence mechanism"* — presumes one**, and
  real samples commonly install two or three (an agent, a login item, and a modified shell profile)
  so that removing one leaves the rest. **The honest answer may be a list, and the question cannot
  accept it.**
  🔴 **And a plist's own timestamps date the file, not the persistence** — a bundle copied with
  preserved dates lies about both.
- **How to parse it** — read the plists (`plutil -p`, or `mac_apt`); check `RunAtLoad`,
  `StartInterval`, `ProgramArguments` and `Label`. 🟢 **`ProgramArguments` frequently contains the
  §2.4 URL** — the two questions are one artifact.
- **Anti-forensics / false-positive caveat** — ⚠️ **legitimate software uses these constantly** —
  updaters, sync clients, and printer drivers all install agents. **The finding is never "a
  LaunchAgent exists"**; it is an agent whose `Label` mimics a system service, whose binary sits in a
  user-writable path, or whose publisher does not match its name (**M5**'s three checks, in macOS
  clothing).

### 2.6 The APFS image, and a mount command that is actually safe

- **What it is** — `Lucas_Disk.img`, mounted with
  `sudo apfs-fuse -v 4 /home/ubuntu/Lucas_Disk.img /home/ubuntu/mac_mount`.
- **Where it lives** — `/home/ubuntu/` on the analysis VM.
- **What it proves** — the state of the volume at acquisition.
- **What it does NOT prove** — ⚠️ **acquisition provenance is absent again** — no hash, no tool, no
  operator, no capture time. **Noted, and deliberately not counted as a defect**, for the reason
  given in `lostinramslation.md` §4: it is near-universal in the corpus.
  ⚠️ **`-v 4` selects a volume within the APFS container** — so **the student is examining one volume
  of several**, and the others (including any Recovery or Preboot volume, and **snapshots**) are not
  in view unless deliberately mounted. **"I did not find it" again may mean "I did not mount it."**
- **How to parse it** — `apfs-fuse`, by **sgan81** — *"This project is a **read-only** FUSE driver for
  the new Apple File System."* 🟢🟢 **Read-only by design**, with writing listed under Limitations as
  unsupported. It supports *"software encrypted volumes and fusion drives"* and has *"support for
  mounting snapshots and sealed volumes."*
- **Anti-forensics / false-positive caveat** — 🟢🟢 **This is the first room in the module whose mount
  command is forensically correct by construction, and it deserves saying plainly.** Room 22 handed
  students a pre-mounted ext4 filesystem with no mount mode stated (**E5**, defect #8); **this room
  hands them a driver that physically cannot write.** ⚠️ **Our version should still make the student
  say *why* it is safe** — *"read-only by design"* is a property to verify, not to assume, and
  `apfs-fuse`'s own documentation is the citation.
  🟢 **Snapshot support is a genuine investigative opportunity** — APFS snapshots are the closest
  macOS analogue to Volume Shadow Copies, and the room does not ask about them.

### 2.7 `mac_apt` — automated triage, and what automation costs

- **What it is** — the room's optional second path: *"If you wish to run automated analysis through
  the mac_apt tool… run the `mac_apt.py` script on the disk image."*
- **Where it lives** — **`mac_apt`**, by **Yogesh Khatri**, *"macOS (& ios) Artifact Parsing Tool"*,
  current **v1.29.0 (11 Feb 2026)**. 🟢 **It reads images directly** — *"Works on E01, VMDK, AFF4, DD,
  split-DD, DMG (no compression), SPARSEIMAGE, UAC collections, Velociraptor collected files (VR) &
  mounted images"* — **so the `apfs-fuse` mount is optional, not required.**
- **What it proves** — whatever its plugins parse, at scale and quickly.
- **What it does NOT prove** — 🔴🔴 **that the artifact set it produced is the artifact set that
  exists.** A parser reports what it has a plugin for; **absence in `mac_apt` output means absent
  from the plugin's coverage, not absent from the disk.** ⚠️ **On this room's questions that matters
  directly** — §2.2 showed that a drag-and-drop install produces no receipt, so an automated
  "installed applications" report can be **complete and still miss the malicious app.**
  ⚠️ **And a tool that reads the image directly is doing its own filesystem parsing** — its APFS
  implementation and `apfs-fuse`'s are different code. **Where they disagree, that is a finding about
  the tools, not the evidence**, and it is worth checking one against the other.
- **How to parse it** — `source /root/mac_apt/venv/bin/activate`, then run against the image.
  🟢 **Note the room's own good practice: a virtualenv with a documented activation path.**
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the interesting cross-reference is that
  `mac_apt` reads formats Autopsy cannot** — **AFF4 and DMG** among them, where Autopsy supports
  neither AFF4 (**E4**) nor AD1 (**O1**). **No single tool reads every container**, and the practical
  consequence for our lab is that **format compatibility must be checked before an evidence set is
  chosen**, not after. **Third room in a row to make that point from a different direction.**

### 2.8 The lure — a "free AI tool trial" as the entire initial access

- **What it is** — the scenario: *"Lucas, always interested in researching AI to enhance his
  development skills, stumbled upon a free trial of an AI development tool while browsing online."*
- **Where it lives** — in §2.1's quarantine record, which is the artifact that makes this claim
  checkable at all.
- **What it proves** — that a file came from a named URL via a named application, at a known time.
- **What it does NOT prove** — 🔴🔴 **that the user was targeted, or that this is connected to the
  main intrusion.** The room states both explicitly — *"a **different** compromise"*, *"Not every
  attack is targeted"* — and **the temptation to link them is exactly the error §8 records me
  making.**
  ⚠️ **Nor does the URL identify the campaign.** Malvertising and SEO-poisoned "free trial" pages are
  disposable; the domain is infrastructure, not attribution (**O5**'s argument, one platform over).
  🟢 **And "unintentionally became a victim" is the scenario's own framing, not a finding.** Whether
  Lucas installed it knowingly, was socially engineered, or was compromised some other way is a
  question the artifacts answer, not the brief.
- **How to parse it** — quarantine record (§2.1), browser history for the browsing that led there,
  the bundle itself, and the persistence plist (§2.5).
- **Anti-forensics / false-positive caveat** — 🟢🟢 **the most useful thing here is organisational,
  not technical.** A lead developer downloading an unvetted "AI development tool" onto a machine with
  access to the company's source is a **software-supply and endpoint-control failure**, and it is
  the fourth distinct organisational failure the module has staged: a junior deploying a honeypot to
  the DMZ (stage 1), a "known issue" providing cover (stage 2), a symptom routed as a helpdesk ticket
  (stage 4), and now unmanaged software installation. ⚠️ **None of the six rooms was compromised by a
  clever exploit.** **That is worth saying out loud in `S1`.**

## 3. Tools and commands

The room names its commands, which is unusual and welcome.

| purpose | command | note |
|---|---|---|
| mount the image | `sudo apfs-fuse -v 4 <img> <mount>` | 🟢🟢 **read-only by design** — #4 |
| analyse mounted | `sudo su`, then work in `/home/ubuntu/mac_mount` | ⚠️ `-v 4` = one volume only — §2.6 |
| automated triage | `source /root/mac_apt/venv/bin/activate` → `mac_apt.py` | 🟢 reads the image directly — #4 |
| download origin (Q1/Q2) | `xattr -p com.apple.quarantine`; query `QuarantineEventsV2` | 🔴 URL is in the **DB**, not the xattr — #1 |
| install time (Q3) | `InstallHistory.plist`; `/var/db/receipts/` | 🔴 **drag-and-drop leaves no receipt** — #2 |
| permissions (Q4) | `TCC.db` (user and system) | 🔴 `last_modified` ≠ first request — #3 |
| persistence (Q6) | `plutil -p` over `Launch*` plists | ⚠️ may be more than one — §2.5 |

### CURRENCY CHECK

⚠️ **Scoped deliberately.** macOS is **out of scope (D38)**, so this pass verifies only what feeds
the **F1 contrast table** and the platform-neutral lessons. **No macOS module is being built.**

| # | claim as the room assumes it | verdict, Aug 2026 | source |
|---|---|---|---|
| 1 | Q1: *"the website from which the user downloaded"* | 🟢🟢 **Recoverable, and the mechanism differs from Windows in a way worth teaching.** The **`com.apple.quarantine` xattr** holds *"the quarantine value in hexadecimal, the time at which the xattr was attached, in hexadecimal, the app or agent responsible for creating the xattr, [and] a UUID referring to the entry for this quarantine flag in the QuarantineEvents database"* — 🔴 **no URL.** The URL lives in **`~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2`**, table **`LSQuarantineEvent`**, columns `LSQuarantineTimeStamp`, `LSQuarantineDataURLString`, `LSQuarantineOriginURLString`, `LSQuarantineAgentName`, `LSQuarantineAgentBundleIdentifier`, `LSQuarantineEventIdentifier`; **timestamps are Cocoa epoch (+978,307,200 s)**. 🔴🔴 **Contrast with Windows (O2): Zone.Identifier keeps the URL *on the file*; macOS keeps a UUID on the file and the URL in a per-user database — so one deletion strips provenance from every downloaded file at once, while the macOS record survives the file's own deletion.** ⚠️ **Column semantics NOT VERIFIED** — teach the names, not the gloss. ⚠️ FAT/exFAT do **not** destroy xattrs (*"can preserve xattrs in hidden shadow files"*); **NFS strips them.** 🔴 **Whether the DB is still populated on macOS 26 is NOT VERIFIED** — the xattr is confirmed current (Apr 2026), the path is unchanged in tooling, but no source tested the DB on 26. **Current macOS is Tahoe 26** (26.6.1, 6 Aug 2026). | [Eclectic Light, quarantine flag](https://eclecticlight.co/2020/10/29/quarantine-and-the-quarantine-flag/) · [Eclectic Light, xattrs, Apr 2026](https://eclecticlight.co/2026/04/24/the-secret-life-of-the-xattr/) · [Velociraptor QuarantineEvents](https://docs.velociraptor.app/artifact_references/pages/macos.system.quarantineevents/) · [Apple LSFileQuarantineEnabled](https://developer.apple.com/documentation/bundleresources/information-property-list/lsfilequarantineenabled) |
| 2 | Q3: *"When was the malicious application installed?"* | 🔴🔴 **May be unanswerable from installation artifacts.** `/Library/Receipts/InstallHistory.plist` *"records App Store and Installer app installations"* with *"installation dates, app names, versions, URLs, and installer process names"*, and `/var/db/receipts` holds *"Complete records of individual files installed by each package."* **But a drag-and-drop app from a DMG produces neither** — the mechanism *"bypasses the mechanisms built into OS X for recording installation and updating"*, and *"If you want to keep a record of those events, you will need to keep your own notes."* 🔴 **A "free trial" DMG is exactly that case.** Fallbacks — quarantine timestamp (**#1**, which is *download*, not install), bundle filesystem timestamps (which reflect the copy), FSEvents — **give three different answers to one question.** 🟢 **Same family as O4 and L1: the event was never recorded, not destroyed.** | [Eclectic Light, what was installed](https://eclecticlight.co/2015/09/25/what-was-installed/) |
| 3 | Q4: *"Which TCC permission did the application request **first**?"* | 🔴 **"First" is not what the artifact stores.** The `access` table records *"the requesting application bundle ID, the service being accessed, the authorization decision, and a timestamp of when access was granted or denied"* — columns `service`, `client`, `client_type`, `auth_value`, `auth_reason`, **`last_modified`**, plus `csreq`, `policy_id`, `flags`, `prompt_count`. **`last_modified` is *last*** — a permission granted, revoked and re-granted keeps only the latest time. `auth_value` is *"denied(0), unknown(1), allowed(2), or limited(3)"*. 🟢🟢 **The transferable finding is the access asymmetry:** *"you won't be able to read your regular user TCC database unless it's from a TCC privileged process"* — ⚠️ **and be precise: the user DB is TCC-protected, the system DB is SIP-protected** (*"only a SIP bypass can write into it"*). **From a mounted image both are ordinary SQLite files** — mac_apt ships `plugins/tcc.py` to do exactly that. **Enforcement lives in the running OS, not in the data.** **ATT&CK T1548.006 Abuse Elevation Control Mechanism: TCC Manipulation, tactic Privilege Escalation.** | [Rainforest QA, TCC deep dive](https://www.rainforestqa.com/blog/macos-tcc-db-deep-dive) · [HackTricks, macOS TCC](https://book.hacktricks.wiki/en/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/index.html) · [mac_apt tcc.py](https://github.com/ydkhatri/mac_apt/blob/master/plugins/tcc.py) · [T1548.006](https://attack.mitre.org/techniques/T1548/006/) |
| 4 | the tooling | 🟢🟢 **`apfs-fuse` (sgan81) is *"a read-only FUSE driver for the new Apple File System"*** — writing is an explicit Limitation. **So this room's mount command cannot modify the evidence** — the first in the module for which that is true by construction (contrast **E5** and room 22's defect #8). It supports *"software encrypted volumes and fusion drives"* and *"mounting snapshots and sealed volumes"*. 🟢 **`mac_apt` (Yogesh Khatri), v1.29.0, 11 Feb 2026** — *"Works on E01, VMDK, AFF4, DD, split-DD, DMG (no compression), SPARSEIMAGE, UAC collections, Velociraptor collected files (VR) & mounted images"*, **so no mount is required.** ⚠️ **Note it reads AFF4 and DMG, which Autopsy does not** (**E4**, **O1**) — **no single tool reads every container, and format compatibility must be settled before an evidence set is chosen.** | [apfs-fuse](https://github.com/sgan81/apfs-fuse) · [mac_apt](https://github.com/ydkhatri/mac_apt) |
| 5 | ATT&CK for this chain | ✅ **T1204.002** User Execution: Malicious File → **Execution** · **T1543.001** Create or Modify System Process: Launch Agent → **Persistence, Privilege Escalation** · **T1543.004** Launch Daemon → **Persistence, Privilege Escalation** · **T1548.006** TCC Manipulation → **Privilege Escalation**. ⚠️ **Checked specifically: neither T1543 sub-technique carries the Stealth tactic**, despite the TA0005 rename (**E11**) making that an easy wrong assumption. 🔴 **And the exfiltration mapping is not the one room 26 used:** an HTTP POST to attacker infrastructure is **T1041 Exfiltration Over C2 Channel** — *"Adversaries may steal data by exfiltrating it over an existing command and control channel"* — **not T1567.002**, which is scoped to cloud-storage services. **Room 26 was T1567.002 (Mega via rclone); this is T1041. The difference is the destination, not the protocol.** | [T1204.002](https://attack.mitre.org/techniques/T1204/002/) · [T1543.001](https://attack.mitre.org/techniques/T1543/001/) · [T1543.004](https://attack.mitre.org/techniques/T1543/004/) · [T1041](https://attack.mitre.org/techniques/T1041/) |

### NOT VERIFIED — carried forward honestly

- **Whether `QuarantineEventsV2` is still populated on macOS 26 (Tahoe).** The xattr is confirmed
  current; the DB path is unchanged in tooling; **no source tested the DB on 26.**
- **The semantics of `LSQuarantineDataURLString` vs `LSQuarantineOriginURLString`** — secondary
  sources gloss them as file-URL vs referring-page; **no primary source defines them.**
- **FTK Imager 8.3's release date** — carried from block **O**.
- **Whether this room's app was a `.pkg` or a drag-and-drop bundle** — decides whether Q3 has a
  receipt-based answer at all (#2).

## 4. Evidence used

**A raw APFS disk image, `Lucas_Disk.img`, plus `apfs-fuse` and `mac_apt` on the analysis VM.**

- **Downloadable?** ⚠️ **No.** **Reusable?** 🔴 **No** — and out of scope besides (**D38**).
- **`ecdfp-evidence` action: none.** 🔴 **Seventh room running with no evidence set, and the module
  is now complete: SIX FOR SIX.** `EVS-10` remains unallocated.
  🟢🟢 **That is now a settled conclusion rather than a running tally: the entire Honeynet Collapse
  module is live-VM-only and will never supply an evidence set.** **Our S4/S5/S6 Windows intrusion
  image must be staged on `EVI-SRC01` (D19) or sourced from CFReDS (D36).** **No further extraction
  will change this**, and the module note should close the question.

### 🟢 The best-assembled lab of the six

Worth recording, because five previous rooms gave the opposite example:

- 🟢🟢 **No published credentials** — the first room in the module without a plaintext password in
  the task body (**R8**).
- 🟢🟢 **A read-only mount command** (§2.6) — the first that cannot modify the evidence.
- 🟢 **Named tools with documented paths**, a virtualenv activation line, and a warning that the VM
  takes four minutes to boot.
- ⚠️ **Still no acquisition provenance** — no hash, no tool, no operator, no capture time. **Noted,
  not counted**, per `lostinramslation.md` §4.

### Critique of the scenario brief

🟢🟢 **The most disciplined brief in the module, and the only one that resists a conclusion.**

*"Not every attack is targeted. Sometimes, your curiosity makes you fall into a trap."* — **the room
tells the student the obvious narrative link is not there.** After five rooms of one escalating
chain, that is a deliberate and slightly brave choice, and it is **the same instinct as room 27's
*"Go beyond the obvious"***: two of the module's six briefs actively warn against the easy reading.

⚠️ **It still narrates more than a first responder would know** — *"unintentionally became a
victim"*, *"the deceptive software trials"* — but it narrates the **lure**, not the **artifacts**,
and it leaves every question the evidence must answer genuinely open.

🟢 **Use the two sentences verbatim in `S1`.** They are the shortest available statement of why scope
is a finding and not an assumption.

## 5. Lab design worth reusing

### 5.1 🟢🟢 A final stage that is deliberately not connected

§1 and §4 cover it. **Adopt the *idea*, carefully.** A capstone in which one strand turns out to be
unrelated teaches scope discipline better than any amount of instruction — **but it must be
gradeable**, which means the brief cannot simply assert the disconnection as this room does.

**The version that works for `S6-09`:** present two incidents and one shared name, **and grade the
student on whether they claim a link and on what evidence.** 🟢 Both answers are acceptable; **only
an unsupported assertion is wrong.** ⚠️ **That requires the D20 rubric to reward a correctly stated
uncertainty**, which criterion 4 already does.

### 5.2 🟢🟢 A mount command that is safe by construction

§2.6. **`apfs-fuse` is read-only by design**, so the room cannot produce room 22's defect even if the
student is careless. **Adopt the principle for our labs: prefer a tool that cannot write over a tool
that must be told not to.** ⚠️ **And still make the student say why it is safe** — *"read-only by
design"* is a property to verify from documentation, not an assumption.

### 5.3 🟢 Everything a student needs, stated once

Named image path, exact mount command, tool location, virtualenv activation, and a boot-time warning.
🟢 **Copy the format for our lab hand-outs.** ⚠️ **Add the two things it omits: the image hash and a
verify-before-you-start step** (**D18**).

### 5.4 ⚠️ Automation offered, not imposed

*"If you wish to run automated analysis through the mac_apt tool…"* — **optional, after the manual
path.** 🟢 **That is the right order and matches room 23 §5.3's shell-first principle**: the manual
route is the taught route, automation is the accelerator. ⚠️ **Our version should add the caveat from
§2.7 — an automated report's silence is the plugin's silence, not the disk's.**

### 5.5 🟢 Safety and handling defects

**None — and this room is the corpus's positive example.** §2.6 and §4: read-only mount, no published
credentials, documented tooling.

🟢🟢 **The module ends with a clean block of four** (rooms 25, 26, 27, 28), after three rooms that
had defects (22, 23, 24). **The pattern is structural, not editorial:** stages 1–2 are live response
by nature; **stages 3–6 are offline analysis of captured artifacts**, and the correct handling
follows from where in the incident you stand. ⚠️ **That is the single best argument in the corpus for
teaching acquisition and analysis as separate disciplines with separate rules**, and the module
demonstrates it across six rooms without ever stating it.

**Running total: 10 defects — rooms 6, 8, 9, 12, 13, 15, 18, 22, 23, 24. Four endanger the analyst's
machine; six endanger the evidence. Unchanged for four rooms.**

## 6. Question patterns

**Six scored questions tracing download → install → permissions → exfiltration → persistence.**
🟢 Clean order, each answer feeding the next.

**🟢 One answer format specified** (Q3's timestamp) — ⚠️ **and again no timezone**, on a room whose
timestamps are **Cocoa epoch** and need conversion (**+978,307,200 s**). **A format without an epoch
and a zone is half a format**, and this is the room where that bites hardest.

**⚠️ Stems assert conclusions, again** — *"the **malicious** application's installer"* · *"the full
**C2** URL to which the application **exfiltrated** data"*. **Eleventh room running.** 🔴 Q5 is the
worst of them: it asserts the URL is C2 **and** that data was exfiltrated, from a string on disk.

**⚠️ Two stems outrun their artifacts** — Q4's *"**first**"* against a `last_modified` column (§2.3),
and Q6's singular *"Which persistence mechanism"* against samples that habitually install several
(§2.5).

**🔴 Twenty-eighth room, and the last of the module — still no "cannot be determined" question.**
🟢🟢 **But two of the six briefs actively warn against the obvious reading** (this room's *"Not every
attack is targeted"*, room 27's *"Go beyond the obvious"*), **which is the closest the module comes
and is worth counting separately from zero.**

| the room could have asked | correct answer |
|---|---|
| *"When was the application installed?"* — **the room's own Q3** | 🔴🔴 **Possibly not determinable.** A drag-and-drop app from a DMG produces **no receipt and no `InstallHistory` entry** — the mechanism *"bypasses the mechanisms built into OS X for recording installation."* Quarantine gives **download** time; bundle timestamps reflect the **copy**. **Three artifacts, three different answers, and the question presumes one.** |
| *"TCC shows Screen Recording. Which permission was requested first?"* | 🔴 **Not from `last_modified`** — it records the *most recent* change. A granted-revoked-regranted permission keeps one timestamp. **Read `prompt_count` alongside as a hint that more happened.** |
| *"TCC shows `allowed` for Full Disk Access. Did the app read the disk?"* | 🔴🔴 **No — permission is not access.** The row is authorisation; use is a separate artifact. **Same family as *presence vs execution* (L2) and *state vs event* (room 23).** |
| *"The binary contains `https://…`. Was data exfiltrated there?"* | 🔴🔴 **Not established.** A URL in a binary is a **capability**, not a transmission — and **modern stealers fetch the endpoint at runtime**, so "no C2 URL on disk" is a normal result. **Memory would settle it (M1); a disk image cannot.** |
| *"There is a LaunchAgent. Is that the persistence mechanism?"* | ⚠️ **Possibly one of several.** Samples routinely install an agent *and* a login item *and* a shell-profile change so removal of one leaves the rest. **The honest answer is a list.** |
| *"No quarantine record for the installer. Was it downloaded from the web?"* | 🔴 **Cannot be determined.** `xattr -d` removes it; an NFS hop strips it; and the record could have been written and the database since deleted — **which on macOS strips provenance from *every* downloaded file at once** (#1). |
| *"Lucas appears in stage 4's stolen data and is compromised at stage 6. Are they connected?"* | 🔴🔴 **Not established — and the module says they are not.** *"Not every attack is targeted."* 🟢🟢 **The best row here, because I got it wrong myself** — see §8. **Proximity plus a shared name is not a link.** |
| *"`mac_apt` lists no malicious application. Was one installed?"* | 🔴🔴 **No.** A parser reports what it has a plugin for, and §2.2 shows a drag-and-drop install leaves no receipt — **so the automated "installed applications" report can be complete and still miss it.** |

🟢🟢 **Eight rows, and one of them is a mistake of mine caught by the module itself.** ⚠️ **Across
rooms 24–28 the finding is now settled: the "cannot be determined" answer is repeatedly the *correct*
answer to questions these rooms actually ask.** **It is a correctness finding about existing
material, not a suggested improvement to question design** — and the module note should say so as the
project's headline conclusion about assessment.

## 7. Figures

**No room-specific figure.** ⚠️ Images were **not enumerated** — the module's pattern (one reused
topology SVG plus decorative assets) was established in rooms 23–24. **Recorded as not-checked.**

🔴 **Ninth room running with no conceptual figure, and the module ends 0 for 6.** Six rooms, one
shared topology diagram, and nothing else — across Linux, Windows, memory, disk, file systems and
macOS.

| # | figure | spec | priority | what it teaches |
|---|---|---|---|---|
| F32 | **Download provenance across three platforms** | Three columns. **Windows:** the file with a `Zone.Identifier` ADS attached, `HostUrl` inside it. **macOS:** the file carrying a UUID xattr, an arrow to a separate `QuarantineEventsV2` database holding the URL. **Linux:** the file alone, nothing attached. Beneath each, the failure mode: *"delete one ADS → one file"* · *"delete one DB → every file"* · *"nothing to delete."* | **🔴 P1** | **The completed F1 row, and the best three-platform contrast in the project.** §2.1 versus **O2** versus block **J**. |
| F33 | **Enforcement lives in the running OS** | A live Mac with `TCC.db` behind a locked door labelled *"TCC-protected"*, beside the same file on a mounted image, open. Caption: **"imaging removes the enforcer."** Small print: *user DB = TCC-protected; system DB = SIP-protected.* | **🔴 P1** | §2.3 — platform-neutral, serves `S2-04`, and explains both why offline analysis sees more *and* why an image must be treated as sensitive. |
| F34 | **The install with no installation record** | Two paths to `/Applications`: a `.pkg` producing an `InstallHistory` entry and a receipt; a DMG drag-and-drop producing **neither**, with three candidate timestamps (quarantine, bundle ctime, FSEvents) fanning out to three different answers. | **🟢 P2** | §2.2 — *the event was never recorded*, the same family as **L1** and **O4**. |

## 8. Fit against our material

### ⚠️ Part 1 lists this as *"Honeynet Collapse chain step 6"* — correct, and it is out of scope.

**macOS, per D38.** Amend the Part 1 row to record that **stages 1 and 6 are out of scope (Linux and
macOS) and stages 2–5 are in scope**, so the module is **four usable rooms of six** — a fact worth
having in one place before anyone plans work from that list again.

### Rows this strengthens

- **`S1-01`** — 🟢🟢 **figure F32 completes the D38 contrast table** with its third column, and it is
  the strongest row the table will have: **the same investigative question, three platforms, three
  different failure modes.**
- **`S2-04`** (*"Physical vs logical acquisition — what each captures and what each misses"*) —
  🟢🟢 **figure F33 and §2.3's asymmetry.** *Access controls are a property of the live system;
  imaging removes the enforcer.* **That is a better argument for offline analysis than any we
  currently have, and it is platform-neutral.** ⚠️ **With its corollary: an evidence image must be
  handled as sensitive data, because every control the subject relied on is gone.**
- **`S1-03`** (*"What makes evidence defensible"*) — §2.2's point that **some questions are
  unanswerable because the event was never recorded**, not because evidence was destroyed. Third
  instance (**L1**, **O4**, here) and now clearly a theme rather than a coincidence.
- **`S6-09`** (capstone) — §5.1's unrelated-strand design, **graded on whether the student claims a
  link and on what evidence.**
- **`S2-06`** — ⚠️ **format compatibility must be settled before an evidence set is chosen** (§2.7):
  `mac_apt` reads AFF4 and DMG; Autopsy reads neither AFF4 (**E4**) nor AD1 (**O1**).

### 🔴 Back-propagation: one, and it is mine

🔴🔴 **This room refuted an inference I made in room 26, and I have corrected it.**

In `crmsnatch.md` §5.2 I wrote that *"stage 4's loot is stage 6's targeting"* — that the customer
export stolen from the CRM server supplied the contact details used to reach Lucas in the final room.
**Stage 6 says otherwise, in its own words:** *"another critical compromise took place … Lucas …
unintentionally became a victim of a **different** compromise"*, and *"Not every attack is targeted."*

**`crmsnatch.md` §5.2 and its frontmatter line have been rewritten** to record the error rather than
delete it, and the note re-verified (PASS). 🟢🟢 **Recording it is the point:** the inference rested
on **proximity plus a shared name** with no artifact connecting them — **precisely the failure mode
I documented one room later** in `shockandsilence.md` §2.8 (*"the most dangerous artifact here is the
plausible story"*). **Committing the error before writing the warning is the most useful thing in
either note**, and the corrected §5.2 keeps the design idea it supported while withdrawing the
evidence for it.

✅ **Everything else checked clean:** `T1204.002`, `T1543.001`, `T1543.004`, `T1548.006` and `T1041`
appear nowhere in the repo — forward-looking only. ⚠️ **`T1041` is worth flagging against room 26's
`T1567.002`:** both are exfiltration, and **the destination decides which** — cloud-storage service
versus attacker infrastructure.

### Minutes

**Net zero in rows.** `S1-01`, `S1-03`, `S2-04`, `S2-06` and `S6-09` gain content; **nothing lands in
S5 at all**, since the platform is excluded.

🟢 **Second room running that adds nothing to S5.** ⚠️ **But the row-overload list is unchanged and
still outstanding: `S5-06`, `S5-08`, `S6-06`, `S4-07`** — four rows carrying material from six rooms
with no row-count change. 🔴 **Stated for the fifth time: the S5 re-split must size rows, not count
them.**

**S2 220 · S4 220 · S6 220 · S5 65 min overdrawn** (rooms 1–5, unchanged).
🔴 **Twenty-third room carrying the S5 overdraft.**

### Out of scope

All of it, per **D38** — macOS artifacts, APFS, TCC, `mac_apt`, Launch Agents. ⚠️ **Three items cross
the line and should be in**, all platform-neutral:

- **§2.3's enforcement asymmetry** — `S2-04`, one slide, and it is the best version of that argument
  we have.
- **§2.2's "never recorded" idea** — `S1-03`, one sentence.
- **§2.1's three-platform provenance row** — `S1-01`, figure **F32**, already committed under D38.

### Still unresolved

- **S5 re-split** — twenty-third room; **four-row overload list**, unchanged.
- **S4 capstone weighting** · **Lab OS version** — unchanged.
- 🟢 **CLOSED: "is there a Windows intrusion image in the Priority-2 set?"** — **No. Six of six
  Honeynet rooms are live-VM-only.** `EVS-10` unallocated. **The image must come from `EVI-SRC01`
  (D19) or CFReDS (D36); extraction will not supply one.**
- **FTK Imager in `CLEAN-TOOLS`** (room 27) · **Volatility symbol pre-population** (**D2**) — both
  outstanding lab-build items.
- **D19 has no per-session host map** — still gating **F7**.
- **`ecdfp-case` skill** not installed; **no room note through `ecdfp-intake`.**
- **🆕 The module arc note** — `honeynet-collapse-module.md`, next.

## 9. Links

**Room** — <https://tryhackme.com/room/thelasttrial>
**Module** — Honeynet Collapse, **stage 6 of 6 (final)**. Previous:
<https://tryhackme.com/room/shockandsilence>.
**All six:** <https://tryhackme.com/room/initialaccesspot> · <https://tryhackme.com/room/elevatingmovement> ·
<https://tryhackme.com/room/lostinramslation> · <https://tryhackme.com/room/crmsnatch> ·
<https://tryhackme.com/room/shockandsilence> · <https://tryhackme.com/room/thelasttrial>
**Companion notes** — `crmsnatch.md` (stage 4 — **§5.2 corrected by this room**) ·
`shockandsilence.md` (stage 5) · `initialaccesspot.md` (the module map) ·
`exfilnode.md` (**D38**, the scope decision that excludes this room) ·
`honeynet-collapse-module.md` (the arc) ·
`_TOOL_CURRENCY_2026-08-28.md` blocks **E4**, **J**, **L1**, **L2**, **M1**, **O1**, **O2**, **O4**,
and new block **P**.

**Citations from §3, by finding:**

- #1 quarantine — Eclectic Light, the quarantine flag
  <https://eclecticlight.co/2020/10/29/quarantine-and-the-quarantine-flag/> ·
  Eclectic Light, xattrs (Apr 2026) <https://eclecticlight.co/2026/04/24/the-secret-life-of-the-xattr/> ·
  Velociraptor `MacOS.System.QuarantineEvents`
  <https://docs.velociraptor.app/artifact_references/pages/macos.system.quarantineevents/> ·
  Apple `LSFileQuarantineEnabled`
  <https://developer.apple.com/documentation/bundleresources/information-property-list/lsfilequarantineenabled> ·
  macOS 26.6.1 release <https://www.macrumors.com/2026/08/06/apple-releases-macos-tahoe-26-6-1/>
- #2 install records — Eclectic Light, what was installed
  <https://eclecticlight.co/2015/09/25/what-was-installed/>
- #3 TCC — Rainforest QA <https://www.rainforestqa.com/blog/macos-tcc-db-deep-dive> ·
  Forge Work <https://forge-work.com/dfir/knowledge/artifacts/macos-tcc-db> ·
  HackTricks
  <https://book.hacktricks.wiki/en/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/index.html> ·
  mac_apt `plugins/tcc.py` <https://github.com/ydkhatri/mac_apt/blob/master/plugins/tcc.py> ·
  T1548.006 <https://attack.mitre.org/techniques/T1548/006/>
- #4 tooling — apfs-fuse <https://github.com/sgan81/apfs-fuse> ·
  mac_apt <https://github.com/ydkhatri/mac_apt>
- #5 ATT&CK — T1204.002 <https://attack.mitre.org/techniques/T1204/002/> ·
  T1543.001 <https://attack.mitre.org/techniques/T1543/001/> ·
  T1543.004 <https://attack.mitre.org/techniques/T1543/004/> ·
  T1041 <https://attack.mitre.org/techniques/T1041/> ·
  T1567.002 <https://attack.mitre.org/techniques/T1567/002/> ·
  TA0005 <https://attack.mitre.org/tactics/TA0005/>
