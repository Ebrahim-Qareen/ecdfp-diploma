# beyond_map.md — the self-study track

**`D82` · `D83`.** Fourteen units that make a complete DF practitioner and that the eCDFP syllabus
does not cover. They live at **`docs/beyond/`** with their own index, and **`design/topic_map.md`
never carries a row from this file.**

| | Taught track | This track |
|---|---|---|
| Minutes | budgeted, 190/session | **none — it never competes for class time** |
| Instructor script (`D77`) | required | not written |
| Evidence | Tier 1, our lab | **Tier 2 only — linked public corpora, never rehosted** |
| Domain reconciliation (`D24`) | counted | excluded |
| Prerequisite of anything taught | — | **never** (`D80` covers the taught tier only) |

> **The rule that decides whether this track is worth having: a unit ships COMPLETE, or it does not
> ship.** Same `R10` six-box standard, the same findings-vs-interpretation discipline, real licensed
> evidence, and an answer key for anything it sets. **No stubs. No "coming soon" tiles.** The
> previous instructor announced six labs and built none — an untaught tier is exactly where that
> failure returns unnoticed, because nobody is standing in a room discovering it is empty.

---

## The fourteen units

| ID | Unit | Covers | Evidence route | Status |
|---|---|---|---|:-:|
| **`M01`** | Linux Forensics — Filesystem | ext4 internals · inodes · the four timestamps · superblock · `/etc` · users and groups · what deletion leaves on ext4 | public Linux DFIR images | ⛔ not built |
| **`M02`** | Linux Forensics — Logs & User Activity | `/var/log` · `journald` · `auth.log` · `bash_history` · `cron` · `systemd` persistence · `.ssh` · `sudo` | same corpus as `M01` | ⛔ not built |
| **`M03`** | Mobile — Acquisition & Its Limits | logical vs filesystem vs physical · backups · encryption · **what cannot be obtained, and saying so** | ⚠ purpose-built research image required | ⛔ not built |
| **`M04`** | Mobile — Android & iOS Artifacts | SQLite stores · WAL and journals · app data · chat · location · media metadata | ⚠ same — **cut rather than faked** if none licensable | ⛔ not built |
| **`M05`** | macOS Forensics | APFS · plists · unified logs · FSEvents · Spotlight · quarantine | ⚠ scarce public corpora | ⛔ not built |
| **`M06`** | Virtual Machine Forensics | VMDK/VHDX structure · snapshots · deleted VMs · the hypervisor's own logs | **we can build this ourselves** | ⛔ not built |
| **`M07`** | Cloud Forensics | M365 unified audit log · Workspace admin log · AWS CloudTrail · what a provider will and will not give you | published sample log sets | ⛔ not built |
| **`M08`** | Database Forensics | SQLite deep — WAL, journals, freelist, recovering deleted rows · server-side transaction logs | trivial to produce ourselves | ⛔ not built |
| **`M09`** | Encryption in an Examination | BitLocker · VeraCrypt · recovery keys · memory-resident keys · **what is genuinely unrecoverable** | our own lab | ⛔ not built |
| **`M10`** | Anti-Forensics Detection | timestomping · wiping · log clearing · trace removal · **proving absence, and its limits** | our own lab | ⛔ not built |
| **`M11`** | Advanced Memory Forensics | Volatility 3 deep · process injection · rootkit traces · page-file and hibernation analysis | public memory samples | ⛔ not built |
| **`M12`** | Enterprise DFIR at Scale | KAPE and Velociraptor across many hosts · triage-first collection · what changes when it is 500 machines | documented workflows | ⛔ not built |
| **`M13`** | Legal, Admissibility & Expert Testimony | admissibility · scope and authorisation · the expert's duty · cross-examination · **"you are not the judge"** | none needed | ⛔ not built |
| **`M14`** | Malware Triage for Examiners | static triage · strings and imports · packing · IOC extraction · **where an examiner stops and hands over** | our own lab | ⛔ not built |

---

## Build order, when the taught track is done

1. **`M13` Legal** — needs no evidence, and it is the piece an examiner is judged on.
2. **`M10` Anti-Forensics** and **`M09` Encryption** — our own lab, and both feed straight back into
   the taught track's caveat boxes.
3. **`M01`/`M02` Linux** — the largest real gap, and public corpora exist.
4. **`M08` Database**, **`M06` VM** — cheap to produce, immediately useful.
5. **`M07` Cloud**, **`M11` Memory**, **`M12` Scale**, **`M14` Malware triage**.
6. **`M03`/`M04` Mobile**, **`M05` macOS** — last, because the evidence question is unresolved.
   **If no image can be licensed, the unit is cut and this table says so. It is not faked.**

---

## Status

**0 of 14 built.** Nothing from this track is linked from the site until the unit behind the link is
complete.
