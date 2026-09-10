#!/usr/bin/env python3
"""
make_s3_sample.py — the Session 3 STRUCTURE SAMPLE (Tier 3, authored by us).

Stands in for `EVS-06`, which is to be carved from `EVS-02` and is not yet acquired.
Teaches STRUCTURE only, for `S3-04` (document) and `S3-05` (executable).

⚠️ This is NOT an evidence set and carries NO `EVS-` id. Only the `ecdfp-evidence`
skill assigns those. If this becomes permanent, it must be declared there first.

What it makes, and what it deliberately does not:
  quarterly_review.docm  a real OOXML package: 6 parts, a real embedded object, and a
                         `word/vbaProject.bin` carrying the real OLE/CFB signature
                         `D0 CF 11 E0 A1 B1 1A E1`.
                         🔴 It contains NO executable VBA. The teaching point is WHERE the
                         macro lives and WHAT container it is, which needs no runnable code.
  report_viewer.exe      a benign hello-world PE, compiled only to be read: DOS stub, PE
                         header, sections, and an import table with `GetSystemDirectoryA`.
                         Needs a mingw cross-compiler; skipped with a message if absent.

Deterministic: fixed member timestamps, so a regenerated .docm is byte-identical.
Usage:  python3 make_s3_sample.py --out <a path OUTSIDE the repo>/S3-SAMPLE
"""
import argparse, hashlib, os, shutil, struct, subprocess, zipfile

MTIME = (2026, 3, 4, 9, 14, 2)
CFB_SIG = bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1])

CT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.ms-word.document.macroEnabled.main+xml"/>
</Types>'''
RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
DOC = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:r><w:t>ITGate eCDFP - Session 3 structure sample. No macro code is present.</w:t></w:r></w:p>
</w:body></w:document>'''
DOCRELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2006/relationships/vbaProject" Target="vbaProject.bin"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject" Target="embeddings/oleObject1.bin"/>
</Relationships>'''

HELLO_C = '''#include <windows.h>
#include <stdio.h>
int main(void) {
    char buf[64];
    GetSystemDirectoryA(buf, sizeof buf);
    printf("ITGate eCDFP S3 sample. System dir: %s\n", buf);
    return 0;
}
'''

def build_docm(out):
    header = CFB_SIG + b"\x00" * 16 + struct.pack("<HH", 0x003E, 3)
    parts = [("[Content_Types].xml", CT.encode()),
             ("_rels/.rels", RELS.encode()),
             ("word/document.xml", DOC.encode()),
             ("word/_rels/document.xml.rels", DOCRELS.encode()),
             ("word/vbaProject.bin", header + b"\x00" * (1536 - len(header))),
             ("word/embeddings/oleObject1.bin", header + b"\x00" * (512 - len(header)))]
    p = os.path.join(out, "quarterly_review.docm")
    with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts:
            zi = zipfile.ZipInfo(name, MTIME); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    return p

def build_pe(out):
    cc = shutil.which("x86_64-w64-mingw32-gcc")
    if not cc:
        print("  report_viewer.exe  SKIPPED - no x86_64-w64-mingw32-gcc on this machine.")
        print("                     apt install gcc-mingw-w64-x86-64, then re-run.")
        return None
    src = os.path.join(out, "_hello.c")
    open(src, "w").write(HELLO_C)
    p = os.path.join(out, "report_viewer.exe")
    subprocess.run([cc, "-O1", "-o", p, src], check=True)
    os.remove(src)
    return p

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="a directory OUTSIDE the repository")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    print("S3 structure sample - Tier 3, authored, NOT an evidence set\n")
    for p in filter(None, [build_docm(a.out), build_pe(a.out)]):
        d = open(p, "rb").read()
        print("  %-22s %8d B  %s" % (os.path.basename(p), len(d), hashlib.sha256(d).hexdigest()))
    print("\n  The .docm contains no executable macro code. It carries the OLE signature so")
    print("  students can see that a macro part is an OLE file inside an OOXML package.")
