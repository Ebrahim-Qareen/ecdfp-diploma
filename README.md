# eCDFP Diploma — ITGate Academy

Practical, instructor-led **Windows digital forensics**, built for the INE eCDFP
(Certified Digital Forensics Professional) exam.

**Live site → https://ebrahim-qareen.github.io/ecdfp-diploma/**

Six four-hour sessions. Every student at a keyboard, every session ending in a verified
acquisition and a written finding. The fourth course in the ITGate path:
SOC Analyst → CEH → eCIR → **eCDFP**.

---

## What this repository holds

The **published course site** and the **planning behind it**. It does not hold evidence.

| | |
|---|---|
| `docs/` | the site served by GitHub Pages — dashboard, the 14 topic pages (`page-01`…`page-14`), shared CSS/JS |
| `design/` | coverage matrix, topic map, scope decisions, the design system |
| `knowledge_base/` | condensed reference, one file per INE module |
| `packages/` | instructor documents — in the repo, never served |
| `cases/` | investigation cases (answer keys are excluded) |
| `labs/` · `scripts/` · `tools/` · `testing/` | lab design, generators, scan scripts, the verification gate |

`PROJECT.md` is the entry document. `DECISIONS.md` says why everything is the way it is.

---

## The sessions

| | Session | Primary domain |
|---|---|---|
| **S1** | Forensic Foundations, Evidence Integrity & Chain of Custody | Fundamentals + Preservation |
| **S2** | Acquisition — Disk, Memory & Live Response | Preservation + Storage |
| **S3** | Data Representation & File Examination | Fundamentals |
| **S4** | Storage Devices, Partitions & File Systems | Storage |
| **S5** | Windows Forensics — Registry, User Activity & Execution | Fundamentals |
| **S6** | Network Forensics, Timelines, Reporting & Capstone | Tools & Techniques |

One incident runs through all six. It is acquired in Session 2 and cut deeper every session
after, so students learn an investigation as a continuous arc rather than six disconnected labs.

Each session is delivered as **topic pages** (`docs/page-01` … `page-14`), each ending in a free, report-backed lab task.

---

## Findings versus interpretation

Separating what the evidence **says** from what you **conclude** is the professional skill this
course exists to teach. It is colour-coded on every page, and it is a graded criterion on every
report.

> **Finding.** `SYSTEM\MountedDevices` records volume GUID `{…}` for a device with serial `07A1…`.
>
> **Interpretation.** A removable device was attached to this host at least once while this hive
> was live.
>
> **Cannot prove.** Who attached it, or that any file was copied to it.

The distinction is carried by border style as well as colour, so it survives a projector, a
greyscale printout, and colour blindness.

---

## Evidence policy

**No evidence bytes are in this repository, and none ever will be.**

- Published here: manifests, hashes (MD5 + SHA-256), acquisition logs, provenance and licence.
- Distributed offline: disk images, memory dumps, registry hives, raw captures.
- Sourcing is declared per set — our own lab acquisitions, public corpora (linked and credited,
  never rehosted), or synthesis where synthesis is actually valid.
- No real personal data, no real company, no real case. Every scenario is purpose-built.

Every push runs a credential scan, a PII scan and an evidence-bytes check before it is allowed.

---

## Running the site locally

```bash
python3 -m http.server --directory docs 8000
```

No build step. The site is plain HTML, one stylesheet and four small scripts, with no external
dependencies — it renders on a classroom machine with no internet.

---

## Verification

Nothing is published until it passes the gate:

```bash
python3 scripts/density_gate.py docs/page-NN/index.html          # bilingual density + terminology
python3 scripts/order_gate.py                                    # topic order and coverage
node   testing/render_gate.js docs/page-NN/index.html            # 1400/1100/900/700/480
powershell -File tools\precommit_scan.ps1                        # credentials · PII · evidence bytes
```

The render harness is mutation-tested — see `testing/README.md`.

---

## Credits and licence

Course material © ITGate Academy. Built against INE's eCDFP curriculum; INE material is
referenced, never republished. Third-party corpora and tools are credited where used and linked
rather than rehosted.

Maintainer: **Ebrahim Mohamed**.
