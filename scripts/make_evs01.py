#!/usr/bin/env python3
"""
make_evs01.py — generator for EVS-01, the Session 1 evidence set.

Tier 1 (our own lab). Four plain-text documents plus the signed manifests.
Deterministic: fixed seed, fixed base timestamp — two runs anywhere produce
byte-identical output, so a student's copy is diffable against the instructor's.

ONE FILE IS DELIBERATELY ALTERED after the manifest is computed. That is the
exercise: `sha256sum -c` must report 3 OK and 1 FAILED.

  python3 make_evs01.py --out /path/outside/the/repo/EVS-01

R9: never write the output inside the project tree. The repo carries the
manifest, never the bytes.
"""
import argparse, hashlib, os, random, sys

random.seed(20260304)                     # fixed seed  — generator rule 2
BASE = "2026-03-04"                       # fixed base timestamp

CASE   = "ITG-2026-014"
COMPANY= "Meridian Metals Ltd (fictional)"
HOST   = "EVI-SRC01"
EXHIBIT= "ITG-2026-014-A1"

# --------------------------------------------------------------------- files
FILES = {}

FILES["seizure_notes.txt"] = f"""FIRST RESPONDER — CONTEMPORANEOUS NOTES
Case reference : {CASE}
Client         : {COMPANY}
Written by     : Responder 1, IR Analyst (ITGate IR)
All times UTC. Local site time was UTC+02:00; offset confirmed against the
site domain controller and recorded below.

{BASE} 08:31 UTC  Arrived on site. Escorted to the finance office by the IT
                   manager. Workstation {HOST} powered ON, screen locked,
                   user reported "pop-up then everything got slow" and left
                   the machine untouched from approx 07:50 UTC.

{BASE} 08:38 UTC  Photographed the desk and the machine in place before
                   touching anything. Four photographs, frames 001-004.
                   Rear ports photographed with cabling attached.

{BASE} 08:44 UTC  Confirmed with the IT manager that the engagement letter
                   covers company-owned endpoints and company-owned removable
                   media. It does NOT cover employee personal devices.
                   One personally-owned phone on the desk was NOT seized.

{BASE} 08:52 UTC  Host powered down. Power removed at the wall rather than a
                   graceful shutdown, on the IT manager's instruction that a
                   process was still writing to disk.
                   NOTE: volatile state was NOT captured. No memory capture
                   was taken. This is a known and accepted loss, recorded here
                   rather than left to be discovered later.

{BASE} 09:02 UTC  Disk removed. Make/model/serial transcribed onto the
                   exhibit label and cross-checked twice by two people.
                   Sealed in an antistatic bag, tamper tape applied across the
                   seal, tape signed and dated across the join.

{BASE} 09:07 UTC  Exhibit {EXHIBIT} logged. Chain of custody opened.
                   Handed to Responder 2 for transport to the lab.

OPEN ITEMS AT HANDOVER
  - No memory image. The host was powered down at 08:52 UTC.
  - The USB device the user mentions was not present on the desk and was not
    located during the site visit.
  - Site time offset UTC+02:00 recorded from the domain controller; the
    workstation's own clock was NOT read before power-down.
"""

FILES["EVI-SRC01_acquisition_log.txt"] = f"""Created By ITGate Forensic Imager 8.3

Case Information:
 Case Number       : {CASE}
 Evidence Number   : {EXHIBIT}
 Unique Description: Finance workstation system disk, {HOST}
 Examiner          : Examiner 1, ITGate Digital Forensics
 Notes             : Imaged on a hardware write blocker. Blocker make/model/
                     serial and firmware are recorded on the chain of custody
                     form, not in this file.

Source Drive Geometry:
 Cylinders         : 60 801
 Tracks per Cylinder: 255
 Sectors per Track : 63
 Bytes per Sector  : 512
 Sector Count      : 976 773 168
 Source drive interface : SATA
 Removable         : False

Acquisition started : {BASE} 09:14:02 UTC
Acquisition finished: {BASE} 11:47:33 UTC

Image Verification Results:
 Verification started : {BASE} 11:47:35 UTC
 Verification finished: {BASE} 12:31:08 UTC
 MD5 checksum   : (computed over the written image)  : verified
 SHA256 checksum: (computed over the written image)  : verified

 NOTE ON SCOPE OF VERIFICATION
 The verification above compares the digest computed while WRITING the image
 against the digest computed while READING THE IMAGE BACK. The source drive
 was not re-read during verification. This log records the tool's own
 write-then-read round trip and nothing about the state of the source.
"""

FILES["custody_form_EVI-SRC01.txt"] = f"""CHAIN OF CUSTODY — one exhibit, one form
Case reference : {CASE}
Exhibit        : {EXHIBIT}
Description    : Internal 3.5in SATA hard disk removed from {HOST}
Storage        : Evidence store, cabinet 2, shelf B. Access logged.

TRANSFERS  (all times UTC; no transfer without two signatures)

 # | When              | From             | To               | Hash recorded | Sig
---+-------------------+------------------+------------------+---------------+-----
 1 | {BASE} 09:07 | Responder 1      | Responder 2      | yes           | RS/RT
 2 | {BASE} 10:22 | Responder 2      | Evidence store   | yes           | RT/ES
 3 | {BASE} 13:40 | Evidence store   | Examiner 1       | yes           | ES/E1
 4 | 2026-03-05 08:55 | Examiner 1       | Evidence store   | yes           | E1/ES

ACTIONS PERFORMED ON THE EXHIBIT
 {BASE} 09:12  Source hashed before imaging. Value recorded in the
                     examiner's notebook, page 41, stored separately from the
                     exhibit and separately from the image.
 {BASE} 09:14  Imaging started, hardware write blocker inline.
                     Blocker recorded as: make/model/serial/firmware on
                     notebook page 41 and photographed with the rig, frames
                     011-013, before anything was disconnected.
 {BASE} 11:47  Imaging completed.
 {BASE} 11:52  Source re-hashed after the imaging run. The before and
                     after source values match. This pair is the technical
                     evidence that nothing was written across the run.
 2026-03-05 08:50  Working copy taken. Original image shelved and not
                     worked on.

DECLARATION
 The exhibit was sealed in an antistatic bag with tamper tape signed across
 the seal at {BASE} 09:02 UTC and the seal was intact at every transfer
 above. No transfer in this record is unaccounted for.
"""

FILES["evidence_inventory.csv"] = """exhibit_id,type,description,source_host,seized_utc,acquired_utc,acquired_by,notes
ITG-2026-014-A1,disk,Internal 3.5in SATA system disk 500GB,EVI-SRC01,2026-03-04T09:02:00Z,2026-03-04T11:47:33Z,Examiner 1,imaged on a hardware write blocker
ITG-2026-014-A2,photographs,Scene and rig photographs frames 001-013,EVI-SRC01,2026-03-04T08:38:00Z,2026-03-04T08:38:00Z,Responder 1,includes rear ports with cabling attached
ITG-2026-014-A3,notes,First responder contemporaneous notes 3 pages,EVI-SRC01,2026-03-04T08:31:00Z,2026-03-04T09:07:00Z,Responder 1,records that no memory capture was taken
"""

# The alteration: ONE character of ONE timestamp in the acquisition log.
# 09:14:02 -> 09:14:03.  Invisible to the eye, fatal to the digest.
TAMPER_FILE = "EVI-SRC01_acquisition_log.txt"
TAMPER_FROM = "Acquisition started : 2026-03-04 09:14:02 UTC"
TAMPER_TO   = "Acquisition started : 2026-03-04 09:14:03 UTC"


def digests(b):
    return hashlib.md5(b).hexdigest(), hashlib.sha256(b).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(here, "EVS-01"),
                    help="output directory (MUST be outside the project tree — R9)")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)

    # 1 · write the CLEAN set and hash it — this is what the manifest records
    manifest = {}
    for name, text in FILES.items():
        b = text.encode("utf-8")
        manifest[name] = digests(b)
        with open(os.path.join(out, name), "wb") as f:
            f.write(b)

    # 2 · write the manifests from the CLEAN hashes
    for algo, idx in (("sha256", 1), ("md5", 0)):
        with open(os.path.join(out, f"EVS-01.{algo}"), "w", newline="\n") as f:
            for name in FILES:
                f.write(f"{manifest[name][idx]}  {name}\n")

    # 3 · NOW alter one file. The manifest already holds its clean digest.
    p = os.path.join(out, TAMPER_FILE)
    src = open(p, encoding="utf-8").read()
    assert src.count(TAMPER_FROM) == 1, "tamper anchor not found — refusing to guess"
    open(p, "w", encoding="utf-8", newline="\n").write(src.replace(TAMPER_FROM, TAMPER_TO))

    # 4 · report — the block below is pasted into the case file
    print(f"EVS-01 written to {out}\n")
    print(f"{'file':34} {'state':9} sha256")
    print("-" * 110)
    for name in FILES:
        actual = digests(open(os.path.join(out, name), "rb").read())
        state = "clean" if actual[1] == manifest[name][1] else "ALTERED"
        print(f"{name:34} {state:9} {manifest[name][1]}")
    print("\nMD5 (as recorded in the manifest):")
    for name in FILES:
        print(f"  {manifest[name][0]}  {name}")
    print("\nsizes:")
    for name in FILES:
        print(f"  {os.path.getsize(os.path.join(out, name)):6} B  {name}")
    print("\nExpected `sha256sum -c EVS-01.sha256`: 3 OK, 1 FAILED "
          f"({TAMPER_FILE}).")


if __name__ == "__main__":
    sys.exit(main())
