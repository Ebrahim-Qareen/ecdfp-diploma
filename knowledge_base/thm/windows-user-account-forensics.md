---
room: Windows User Account Forensics
url: https://tryhackme.com/room/windowsuseraccountforensics
module: Windows Endpoint Investigation (Section 3 of Advanced Endpoint Investigations)
feeds: PARTIALLY. See §8 — Part 1 mapped this to `S5-02`, which is WRONG. Real fit is a
       missing S5 row plus `S6-06`. Roughly half the room is out of eCDFP scope.
difficulty / time: Medium · 60 min · marked **Premium room** (as stated)
extracted: 2026-08-28
extracted_by: ecdfp-web-extract via Chrome (premium room, logged-in session)
completeness: all 6 tasks read in full. 0 sections NOT READ.
---

## 1. What the room teaches

Where Windows records the existence, change and use of an account — across four stores: the
Security event log, the SAM hive, `NTDS.dit`, and Group Policy. It is organised by **account
lifecycle** (created → modified → deleted → authenticated) rather than by artifact, which is a
different and useful teaching order from room 1's timeline-pivot approach.

Its centre of gravity is **domain**, not workstation: two of five content tasks are pure Active
Directory (NTDS.dit extraction, GPO abuse), and a third is network authentication analysis. Only
the SAM and lifecycle-event-ID material is single-host forensics.

Much lighter on hands-on than room 1 — Task 2 is entirely prose tables with no artifact at all.

## 2. Artifacts — one 6-box block each

### 2.1 Security event log — account lifecycle

- **What it is** — Windows' record of account creation, enablement, modification, lockout and
  deletion.
- **Where it lives** — Event Viewer → `Windows Logs → Security`. Logged on the individual host
  for local accounts, and **on the domain controller for domain accounts** — the room is explicit
  about that split, which matters for acquisition planning.
  Event IDs taught: **4720** created · **4722** enabled · **4738** modified · **4740** locked out
  after repeated failed logons · **4726** deleted.
- **What it proves** — that an account operation happened, when, to which account (name, domain,
  **SID**), and which user or process initiated it.
- **What it does NOT prove** — intent. The room makes this point well: creation is onboarding
  *or* attacker persistence; deletion is offboarding *or* track-covering. The event distinguishes
  neither. It also cannot show anything that happened while logging was off or after the log
  rolled, and a 4740 lockout proves failed attempts, not a brute-force *campaign*.
- **How to parse it** — the room uses the Event Viewer GUI only. **No CLI parser, no EVTX
  tooling, no filtering syntax is taught.** That is a real weakness for us: our S6 timeline work
  needs parsed EVTX, not clicking.
- **Anti-forensics / false-positive caveat** — the room states none. Ours: the Security log is
  clearable (and clearing is itself an event), it is size-capped, and 4720/4726 pairs are routine
  noise in any environment with automated provisioning.

### 2.2 SAM — Security Account Manager

- **What it is** — the registry database holding local user and system account information.
- **Where it lives** — `%SystemRoot%\system32\config\SAM`
- **What it proves** — local account names and their unique identifiers, group memberships,
  hashed passwords (never plaintext), whether each account is active/disabled/expired, and
  **last-login timestamps**.
- **What it does NOT prove** — anything about domain accounts (those live in NTDS.dit), and
  nothing about what a user *did* — only that the account exists, its state, and when it last
  logged in. A last-login timestamp is not a session, and the presence of a hash is not evidence
  of compromise.
- **How to parse it** — ⚠️ **the room teaches no tool for the SAM at all.** It states the path,
  states that the file is locked while Windows runs and must be worked from an offline system or
  forensic backup, lists what it contains, and moves on. No RegRipper, no Registry Explorer, no
  `RECmd`. **This is the room's biggest omission and the single most important thing for us to
  supply ourselves.**
- **Anti-forensics / false-positive caveat** — the room gives one implicitly and it is a good
  acquisition lesson: **the SAM is locked on a live system.** Get it from the image, a VSS copy,
  or a live-forensics tool — not by trying to copy it out of a running host.

### 2.3 NTDS.dit — the domain directory database

- **What it is** — the Active Directory database holding domain accounts, groups and directory
  objects.
- **Where it lives** — on a domain controller; the room exports a copy rather than naming the
  production path.
- **What it proves** — domain usernames and full names, **SIDs**, group memberships (global,
  domain local, universal), password hashes, account enabled/disabled/expired status, logon
  timestamps and failed-logon counts, password-set and expiry times, plus other domain objects
  and trust relationships.
- **What it does NOT prove** — the room does not say. Ours: it is a *state* snapshot of the
  directory, not an activity log — it cannot tell you who changed what, or when, without the DC's
  event logs alongside it.
- **How to parse it** — a two-stage flow, both PowerShell as Administrator:
  1. export — `ntdsutil.exe "activate instance ntds" "ifm" "create full C:\Exports" quit quit`
     (IFM = install-from-media; produces the database **and** the `SYSTEM` hive)
  2. decrypt and read — DSInternals:
     `$bootKey = Get-BootKey -SystemHivePath 'C:\Exports\registry\SYSTEM'`
     `Get-ADDBAccount -All -DBPath 'C:\Exports\Active Directory\NTDS.dit' -BootKey $bootKey`
  The **SYSTEM hive supplies the boot key**, without which the encrypted material in NTDS.dit
  stays unreadable. That dependency is the genuinely instructive part.
- **Anti-forensics / false-positive caveat** — the room states none. Note the room had to
  pre-export `C:\Exports` for students; the export itself is a heavyweight, noisy operation on a
  live DC.

> **Scope flag:** this whole block is Active Directory forensics. See §8 — it is almost certainly
> not ours to teach.

### 2.4 Authentication event IDs

- **What it is** — the record of logon attempts and Kerberos ticket activity.
- **Where it lives** — the Security log; for domain accounts, **on the domain controllers**.
  Event IDs taught: **4624** successful logon · **4625** failed logon ·
  **4768** Kerberos TGT requested · **4771** Kerberos pre-authentication failed.
- **What it proves** — that an authentication attempt occurred and its outcome. Correlated, they
  suggest patterns: a run of 4625 followed by a 4624 is the brute-force shape; a spike in 4768 is
  worth a second look.
- **What it does NOT prove** — the room says it directly and correctly: **these event IDs alone
  do not confirm malicious activity.** A 4624 does not prove the account owner was at the
  keyboard, and a 4625 run has mundane causes (a stale service credential, a phone with an old
  password). They are correlation inputs, not conclusions.
- **How to parse it** — Event Viewer GUI only. No logon-type breakdown is taught, which is a
  notable gap — logon type is what separates an interactive session from a network authentication.
- **Anti-forensics / false-positive caveat** — the room states none for the logs themselves.

### 2.5 Authentication network traffic (NTLM)

- **What it is** — authentication visible on the wire, analysed in a packet capture.
- **Where it lives** — a capture file. The room supplies `C:\Captures\ntlm.pcapng` on the VM and
  states it came from the **official Wireshark sample captures**.
- **What it proves** — source and destination IPs and hostnames, the domain and user name, the
  protocol in use (NTLM vs Kerberos), timestamps, and success/failure indicators. With the user's
  password supplied, previously opaque fields become readable. The NTLM 3-way handshake is taught
  as Negotiate → Challenge → Authenticate across three consecutive frames.
- **What it does NOT prove** — **the room's best line in the whole room, and worth quoting in
  spirit in our material: inspecting authentication traffic does not reveal Pass-the-Hash or
  Kerberoasting. Malicious or not, those requests look like ordinary authentication.** The wire
  shows the protocol, not the intent behind it. Payload is normally encrypted.
- **How to parse it** — Wireshark. To decrypt: `Edit → Preferences → Protocols → NTLMSSP`, set
  the **NT Password** field, OK. Then re-read the authenticate frame and any RPC responses.
- **Anti-forensics / false-positive caveat** — the room states none. Ours, and it is a big one:
  **this technique requires knowing the plaintext password**, which in a real investigation you
  usually do not. The room hands it to you. Also see §3 — Wireshark supports **ASCII passwords
  only** here.

### 2.6 Group Policy artifacts

- **What it is** — the settings GPOs push to users and computers, and the traces enforcement
  leaves behind.
- **Where it lives** — the room names six locations precisely:
  - user settings → `HKEY_CURRENT_USER` and the user profile directories
  - logon scripts → the **SYSVOL** folder, plus execution traces in user profiles
  - user rights assignments → `%SystemRoot%\security\database\secedit.sdb`
  - security policy changes →
    `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies`
  - service configuration → `HKEY_LOCAL_MACHINE\SYSTEM`
  - network configuration →
    `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList`
    and `%SystemRoot%\System32\drivers\etc`
- **What it proves** — that a policy is configured a given way now, what a logon script contains,
  and which principals it targets. The room's worked example: a policy disabling the domain-profile
  firewall, and a logon PowerShell script that beacons out.
- **What it does NOT prove** — the room does not say. Ours: GPMC shows **current state, not
  history** — it cannot tell you who changed the policy or when. That needs DC event logs and
  SYSVOL file timestamps. Nor does a configured logon script prove it ever ran on any host.
- **How to parse it** — Group Policy Management Console (GPMC), navigating the forest → domain →
  Group Policy Objects tree, then Edit on a policy. The room's investigative heuristic is good:
  **a GPO whose name breaks the organisation's naming convention is worth opening first.**
- **Anti-forensics / false-positive caveat** — the room states none.

> **Scope flag:** Active Directory again. See §8.

## 3. Tools and commands

| tool | version the room uses | exact command | what it outputs |
|---|---|---|---|
| Event Viewer | n/a (built-in GUI) | — | Security log entries |
| `ntdsutil.exe` | n/a (built-in) | `ntdsutil.exe "activate instance ntds" "ifm" "create full C:\Exports" quit quit` | IFM set: NTDS.dit + registry hives under `C:\Exports` |
| DSInternals | **not stated** | `$bootKey = Get-BootKey -SystemHivePath 'C:\Exports\registry\SYSTEM'` | boot key into a variable |
| DSInternals | **not stated** | `Get-ADDBAccount -All -DBPath 'C:\Exports\Active Directory\NTDS.dit' -BootKey $bootKey` | per-account records: DN, SID, GUID, SamAccountName, UPN, enabled state, UAC flags, LastLogonDate, names |
| Wireshark | **not stated** | GUI: open capture; `Edit → Preferences → Protocols → NTLMSSP` → NT Password | decrypted NTLMSSP fields |
| GPMC | n/a (built-in) | — | GPO tree and per-policy settings |
| **(none)** | — | **no SAM parser taught** | — |

### CURRENCY CHECK — run 2026-08-28

| item | result |
|---|---|
| **DSInternals** | current **7.1**, published **2026-07-04** (PowerShell Gallery). Supports **PowerShell 5.1 and 7**. |
| `Get-ADDBAccount` | **confirmed still present**; the project README documents it for offline NTDS.dit manipulation and hash dumping. |
| `Get-ADDBAccount -All / -DBPath / -BootKey` | **NOT confirmed from a primary source in this pass.** The README does not enumerate parameters. Verify against the cmdlet docs before teaching the exact line. |
| `Get-BootKey` | **NOT confirmed from a primary source in this pass.** Not mentioned on the README page fetched. Verify before use. |
| `ntdsutil.exe` IFM syntax | built-in, not versioned. Not independently verified. |
| **Wireshark** | current stable **4.6.8**. NTLMSSP dissector fields present across 1.0.0–4.6.8. |
| Wireshark **NT Password** preference | **confirmed**: `Edit → Preferences → Protocols → NTLMSSP`, field "NT Password". |
| ⚠️ Wireshark NTLMSSP caveat the room omits | **ASCII passwords only** — a non-ASCII password will not decrypt, and the room does not mention this. If you have only the hash, a keytab is the alternative route. **Teach this or students will conclude the feature is broken.** |
| Room's version claims | **the room states no version for any tool.** Same defect as room 1. |

**Two commands carry unverified flags** (`Get-BootKey -SystemHivePath`, `Get-ADDBAccount -All
-DBPath -BootKey`). They are recorded here as the room gave them, explicitly flagged as
unverified. Do not put them in student material until confirmed.

## 4. Evidence used

- A THM-hosted **lab machine** (domain-joined Windows with AD, GPMC, DSInternals and Wireshark
  pre-installed), plus a pre-exported `C:\Exports` IFM set.
- **Size: not stated. Not downloadable. No licence offered.** The VM itself is not reusable.
- The room again publishes lab RDP credentials inline. **Deliberately not recorded here (R8).**
- ✅ **ONE REUSABLE SOURCE — flag for `ecdfp-evidence`:** the NTLM capture is stated to come from
  the **official Wireshark sample-captures collection**, not from THM. That is a genuine Tier 2
  candidate — public, citable, and small enough to distribute.
  **Source to verify: <https://wiki.wireshark.org/SampleCaptures>** (find the NTLM/`ntlm.pcapng`
  entry). Not downloaded here — `ecdfp-evidence` owns licence, hash and the EVS- ID.
  Relevance to us is modest: our own C2/RDP pcap is `EVS-08` (Tier 3, scapy). This would only be
  a teaching aid for protocol reading, not case evidence.

## 5. Lab design worth reusing

Weaker than room 1, but two ideas are worth taking:

1. **Lifecycle as the organising spine.** Created → enabled → modified → locked out → deleted,
   each with its event ID. That is a genuinely better teaching order for account artifacts than a
   flat artifact list, and it gives students a mental checklist to walk.
2. **The naming-convention heuristic.** "This GPO does not follow the company's naming
   convention, so it is worth investigating first" is exactly the kind of triage judgement our
   independent-practice hour should be building. Transplantable to any artifact list.

What **not** to copy:

- **Task 2 has no artifact and no hands-on.** It is four prose tables of security risks and
  mitigations — closer to a GRC lesson than a forensics one, and it is the section our students
  have already covered in CEH/eCIR. In our material this is one slide of recall, not a task.
- **The room hands over the password** needed for the Wireshark decryption. Fine as a
  demonstration, dishonest as an investigation. If we reuse this, we must say plainly that in a
  real case you rarely have it.
- **The GPO task tells you where to look** ("in the interest of time, we'll just be guiding you").
  The room admits it is skipping the actual investigative work.

## 6. Question patterns

14 questions across 6 tasks: T1 ×1 (a start-the-machine gate), T2 ×2, T3 ×3, T4 ×3, T5 ×4,
T6 ×1 (completion gate). So 12 real questions.

- **Task 2's two questions are pure definition recall** ("what type of account…", "what centrally
  manages…"). No artifact involved. That is a quiz question, not a forensics question, and it is
  the pattern our cases must avoid.
- **Tasks 3–5 are single-artifact answerable**, which matches our rule: user count and SID from
  the DSInternals output; NTLM username and server challenge from the capture; GPO target user,
  Defender setting, script filename and C2 IP from GPMC.
- **Again, not one question has "this cannot be determined" as its answer** — despite the room
  containing the single best "cannot determine" statement of both rooms so far (Pass-the-Hash and
  Kerberoasting are invisible in authentication traffic). The room states the limit in prose and
  then never tests it. **That gap is precisely the one our D20 criterion 4 exists to close**, and
  this room hands us the ready-made question: *"From this capture alone, can you determine whether
  the authentication used a stolen hash?"* Answer: no.

## 7. Figures we would need to draw

13 images, nearly all screenshots of GPMC and Wireshark panes — i.e. the answers. Two concepts
deserve our own inline SVG:

| room figure showed | our SVG spec (one line) |
|---|---|
| the NTLM 3-way handshake across three frames (shown only as packet-list screenshots) | a three-step vertical exchange diagram — client → server Negotiate, server → client Challenge, client → server Authenticate — each step labelled with what an investigator can read from it *without* the password, and what stays opaque |
| where account data lives (never drawn; scattered across prose) | a single "one account, four stores" diagram: SAM (local) · NTDS.dit (domain) · Security event log (activity) · GPO/SYSVOL (what is pushed at it) — with a caption naming what each can and cannot answer |

The second is the diagram this room needed and does not have. Never their images (D22).

## 8. Fit against our material

### ⚠️ Part 1's mapping for this room is WRONG — correct it

`Resources/THM/_EXTRACTION_PROMPT.md` Part 1 maps this room to **`S5-02`**. `S5-02` is
*"System configuration artifacts — timezone, network, mounted devices"*. That is not what this
room is about. The mapping should be corrected when the S5 gap below is resolved.

### GAP — S5 has no user-account row at all

Grepped the whole map: `S5-01`…`S5-10` cover registry structure, system config, USB, shellbags,
prefetch, amcache/shimcache, LNK, recycle bin/VSS, the case, the ritual. **There is no SAM row,
no local-account row, no SID row, no logon-history row anywhere in the course.**

This matters more than it looks: **`S5-09` is the case "which USB, which user, which program ran,
when, how many times"** — and nothing in S5 teaches how to establish *which user*. The case asks a
question the session does not equip the student to answer.

Proposed row — `ecdfp-intake` decides:

> `S5-02b` · Local accounts and the SAM — account names, SIDs, group membership, enabled/disabled
> state, last-logon; plus the account-lifecycle event IDs (4720 · 4722 · 4726 · 4738 · 4740) ·
> M4 · prereq `S5-01` · S5 · hands-on Yes · **15 min** · `F` · EVS-02

Note the room teaches **no SAM parser**, so our version must supply one (Registry Explorer or
RegRipper against the offline hive — both already on the FOR-WS01 tool list, Part 6).

### 🔴 CUMULATIVE MINUTE PROBLEM — surface this now, do not let it accumulate

S5 totals exactly **220** (D26) and has no slack. Two rooms in, S5 has been asked for **30 extra
minutes**:

| from | proposed row | minutes |
|---|---|---|
| room 1 · Compromised Windows Analysis | `S5-06b` scheduled tasks / persistence | 15 |
| room 2 · this room | `S5-02b` local accounts and the SAM | 15 |
| | **total demanded** | **30** |

Fifteen minutes can plausibly come out of `S5-08` (25 → 10). **Thirty cannot** without gutting an
investigation row. And there are **three more S5 rooms still unextracted** (User Activity,
Expediting Registry, Applications Forensics), each likely to propose more.

**Recommendation to `ecdfp-intake`: do not absorb these one at a time.** Extract the remaining S5
rooms first, then re-split S5 in the map in one deliberate pass. D26 explicitly permits re-splitting
in the map and forbids carrying overflow into the build — this is exactly that situation, arriving
early enough to handle cleanly.

### Rows this genuinely strengthens

- **`S6-06`** Windows event logs — supplies ten concrete event IDs across two coherent groups
  (lifecycle 4720/4722/4726/4738/4740; authentication 4624/4625/4768/4771). Good raw material.
  Caveat: the room teaches Event Viewer clicking only, and `S6-07` needs *parsed* EVTX for plaso.

### OUT OF SCOPE — roughly half this room

`design/scope_decisions.md` (lines 193, 213) puts **Active Directory** in the "already taught,
never re-taught" column, and eCDFP is a single-workstation, Windows-weighted, 24-hour course.

| room content | verdict |
|---|---|
| SAM, account lifecycle event IDs | **in scope** — propose `S5-02b` above |
| Authentication event IDs (4624/4625) | **in scope** — feeds `S6-06` |
| Kerberos event IDs (4768/4771) | **borderline** — domain-only. Mention, do not teach. |
| NTDS.dit + `ntdsutil` IFM + DSInternals | **OUT** — domain-controller forensics |
| GPO / GPMC / SYSVOL / `secedit.sdb` | **OUT** — Active Directory administration and abuse |
| NTLM traffic decryption in Wireshark | **OUT as taught** — it is a domain-auth exercise that requires the plaintext password. The *protocol-reading* skill belongs to `S6-02`/`S6-05`, using our own pcap. |
| Task 2 account-type theory | **OUT** — already covered in their earlier courses |

Extracting the out-of-scope half further would be wasted effort. It is recorded here as a boundary
decision, not carried forward.

## 9. Links

- Room: <https://tryhackme.com/room/windowsuseraccountforensics>
- Path: <https://tryhackme.com/path/outline/advancedendpointinvestigations> (Section 3)
- Room's own stated prerequisites — Sysmon, Windows Event Logs, Active Directory and Domain
  accounts, Wireshark and Traffic Analysis. Our students have all four from CEH/eCIR.
- Room's onward pointer: "Windows Application Forensics" in the Incident Response module —
  **not the same as `windowsapplications` in this path**; check before treating them as one.
- DSInternals: <https://github.com/MichaelGrafnetter/DSInternals> ·
  <https://www.powershellgallery.com/packages/DSInternals/> (7.1)
- Wireshark NTLMSSP decryption: <https://wiki.wireshark.org/NTLMSSP>
- Wireshark sample captures (evidence candidate): <https://wiki.wireshark.org/SampleCaptures>

END OF NOTE.
