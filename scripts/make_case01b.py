#!/usr/bin/env python3
"""
make_case01b.py - CASE-01B, the hard variant of Case 01.

Case 01 has one tampered file and one command finds it. CASE-01B cannot be
solved by running `sha256sum -c` and reading the output. Six separate defects,
each answerable from Session 1 material, none visible from a single command.

  1  incident_timeline.txt    tampered - fails BOTH manifests
  2  access_log_excerpt.txt   tampered by WHITESPACE ONLY - invisible in an editor
  3  policy_extract.txt       manifests DISAGREE - MD5 fails, SHA-256 passes.
                              The SHA-256 list was regenerated after the change and
                              the MD5 list was not. Which one is authoritative
                              CANNOT be determined from this package.
  4  missing_statement.txt    listed in both manifests, ABSENT from disk
  5  extra_notes.txt          present on disk, listed in NEITHER manifest - silent,
                              found only by comparing the file list to the manifest
  6  photo_evidence.txt       a PNG carrying a .txt name. Its hash MATCHES.
                              Integrity is intact; the NAME is what is wrong.
                              Integrity and identity are different questions.
  +  duplicate_a/b.txt        identical content, two names, one digest listed twice

⚠️ NOT an evidence set and carries NO `EVS-` id - only the `ecdfp-evidence` skill
assigns those. Declare it there before making it permanent.

Deterministic: fixed bytes, fixed order. Regenerating gives byte-identical output.
Fictional throughout. No personal data, no credentials, documentation IP ranges only.

Usage:  python3 make_case01b.py --out docs/session-01/CASE-01B
"""
import argparse, hashlib, os, struct, zlib, zipfile

CASE = "ITG-2026-014"

def png(w, h, rgb):
    """A real, valid PNG - so `xxd -l 4` shows 89 50 4E 47 and `file` agrees."""
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))

DUP = ("EXHIBIT LABEL\n"
       "Case ......: %s\n"
       "Exhibit ...: EVI-SRC02\n"
       "Description: USB mass storage device, recovered from the finance desk\n"
       "Sealed by .: Examiner 2, ITGate Digital Forensics\n" % CASE)

FILES = {
 "handover_note.txt":
   "HANDOVER NOTE\n"
   "Case ......: %s\n"
   "Item ......: EVI-SRC02, USB mass storage device\n"
   "Released by: first responder, on shift\n"
   "Received by: exhibits officer\n"
   "When ......: 2026-03-04 10:22 UTC\n"
   "Condition .: sealed, tamper tape intact, signature across the seam\n" % CASE,

 "interview_summary.txt":
   "INTERVIEW SUMMARY\n"
   "Case ......: %s\n"
   "Subject ...: department administrator\n"
   "Summary ...: states the device was kept in an unlocked drawer and was used by\n"
   "             more than one person. Cannot say who used it last.\n"
   "Note ......: statement is unverified and is recorded as an account, not a fact.\n" % CASE,

 "asset_register.csv":
   "asset_id,description,assigned_to,location,last_audit\n"
   "AST-0041,workstation,finance-01,floor 3,2026-01-14\n"
   "AST-0042,usb mass storage,unassigned,floor 3,2026-01-14\n"
   "AST-0043,label printer,reception,floor 1,2026-01-14\n",

 "incident_timeline.txt":
   "INCIDENT TIMELINE (working draft)\n"
   "Case ......: %s\n"
   "2026-03-03 17:05 UTC  device last seen in the drawer by the administrator\n"
   "2026-03-04 08:30 UTC  drawer found open, device present\n"
   "2026-03-04 09:14 UTC  device seized\n"
   "2026-03-04 10:22 UTC  handed to exhibits\n" % CASE,

 "access_log_excerpt.txt":
   "ACCESS LOG EXCERPT (door controller, floor 3)\n"
   "Case ......: %s\n"
   "2026-03-03 17:02 UTC  badge 0041  exit\n"
   "2026-03-04 06:58 UTC  badge 0041  entry\n"
   "2026-03-04 07:01 UTC  badge 0067  entry\n"
   "2026-03-04 08:29 UTC  badge 0067  exit\n" % CASE,

 "policy_extract.txt":
   "REMOVABLE MEDIA POLICY (extract)\n"
   "Case ......: %s\n"
   "3.2  Removable media issued to a department is recorded in the asset register.\n"
   "3.3  Unassigned media must not hold department data.\n"
   "3.4  Media leaving the floor is logged at reception.\n" % CASE,

 "missing_statement.txt":
   "WITNESS STATEMENT\n"
   "Case ......: %s\n"
   "This file is listed in both manifests and is deliberately not distributed.\n" % CASE,

 "duplicate_a.txt": DUP,
 "duplicate_b.txt": DUP,

 "extra_notes.txt":
   "SCRATCH NOTES (not exhibited)\n"
   "Case ......: %s\n"
   "Loose notes found with the package. Origin unknown. Listed in no manifest.\n" % CASE,
}

# name -> (sha_source, md5_source, on_disk)   'clean' | 'changed'
TAMPER = {
 "incident_timeline.txt":  ("clean",   "clean",   "changed"),  # fails both
 "access_log_excerpt.txt": ("clean",   "clean",   "changed"),  # fails both (whitespace)
 "policy_extract.txt":     ("changed", "clean",   "changed"),  # SHA ok, MD5 fails
}
CHANGES = {
 # a real edit: one timestamp moved
 "incident_timeline.txt":  ("2026-03-04 08:30 UTC", "2026-03-04 08:33 UTC"),
 # whitespace only: two trailing spaces. Invisible in any editor.
 "access_log_excerpt.txt": ("badge 0067  entry\n",  "badge 0067  entry  \n"),
 # a real edit: a clause removed
 "policy_extract.txt":     ("3.3  Unassigned media must not hold department data.\n", ""),
}

MANIFEST_ORDER = ["handover_note.txt", "interview_summary.txt", "asset_register.csv",
                  "incident_timeline.txt", "access_log_excerpt.txt", "policy_extract.txt",
                  "missing_statement.txt", "photo_evidence.txt",
                  "duplicate_a.txt", "duplicate_b.txt"]
DISK_ORDER = [n for n in MANIFEST_ORDER if n != "missing_statement.txt"] + ["extra_notes.txt"]

def variant(name, which):
    base = FILES[name]
    if which == "clean" or name not in CHANGES:
        return base.encode()
    a, b = CHANGES[name]
    assert base.count(a) == 1, "change anchor not unique in " + name
    return base.replace(a, b).encode()

def content(name, which):
    if name == "photo_evidence.txt":
        return png(24, 16, (0x60, 0x3E, 0x3B))
    return variant(name, which)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    sha, md5 = [], []
    for n in MANIFEST_ORDER:
        s_src, m_src, _ = TAMPER.get(n, ("clean", "clean", "clean"))
        sha.append("%s  %s" % (hashlib.sha256(content(n, s_src)).hexdigest(), n))
        md5.append("%s  %s" % (hashlib.md5(content(n, m_src)).hexdigest(), n))
    open(os.path.join(a.out, "CASE-01B.sha256"), "w", newline="\n").write("\n".join(sha) + "\n")
    open(os.path.join(a.out, "CASE-01B.md5"),    "w", newline="\n").write("\n".join(md5) + "\n")

    for n in DISK_ORDER:
        _, _, d_src = TAMPER.get(n, ("clean", "clean", "clean"))
        open(os.path.join(a.out, n), "wb").write(content(n, d_src))

    # The brief sits at the ZIP ROOT, never inside CASE-01B/. Defect 5 is
    # "one file on disk that no manifest lists" - a second unlisted file in
    # that folder would give the student two answers to a one-answer question.
    parent = os.path.dirname(a.out.rstrip("/"))
    z = os.path.join(parent, "CASE-01B.zip")
    brief = os.path.join(parent, "CASE-01B_brief.md")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for n in DISK_ORDER + ["CASE-01B.sha256", "CASE-01B.md5"]:
            zf.write(os.path.join(a.out, n), "CASE-01B/" + n)
        if os.path.exists(brief):
            zf.write(brief, "CASE-01B_brief.md")

    print("CASE-01B written to %s" % a.out)
    print("  %d files on disk, %d manifest entries" % (len(DISK_ORDER), len(MANIFEST_ORDER)))
    print("  zip: %s (%d B), brief %s" %
          (z, os.path.getsize(z), "included" if os.path.exists(brief) else "MISSING"))
