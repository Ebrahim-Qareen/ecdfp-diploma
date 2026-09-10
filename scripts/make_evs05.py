#!/usr/bin/env python3
"""
make_evs05.py — EVS-05, the file-type identification set.

12 files whose EXTENSIONS ARE UNRELIABLE. Used three times in the course:
  S1-09  read the first four bytes of four of them (first look inside a file)
  S2-06  run a signature sweep across the whole set
  S3-07  Case 03, with EVS-10's hidden payload alongside

Tier 3 (synthesized) and legitimately so: every file here is one WE AUTHOR. The Tier 3 bar forbids
fabricating .evtx / E01 / raw images / memory dumps / registry hives. It does not forbid making a PNG.

Deterministic: fixed seed, fixed timestamps -> a student's regenerated copy is byte-identical.
Fictional content only, no PII, no credentials, no IP addresses (D41 / R8).

Usage:  python3 make_evs05.py --out <a path OUTSIDE the repo>/EVS-05
"""
import argparse, hashlib, io, os, random, zipfile

from PIL import Image, ImageDraw

SEED = 20260824
MTIME = 1788307200


def img(w, h, bg, label, mod=0):
    rnd = random.Random(SEED + mod)
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for _ in range(10):
        x, y = rnd.randrange(0, w), rnd.randrange(0, h)
        d.rectangle([x, y, x + rnd.randrange(15, 60), y + rnd.randrange(15, 60)],
                    fill=tuple(rnd.randrange(50, 200) for _ in range(3)))
    d.rectangle([0, h - 30, w, h], fill=(20, 22, 30))
    d.text((8, h - 21), label, fill=(230, 235, 245))
    return im


def as_bytes(im, fmt, **kw):
    b = io.BytesIO(); im.save(b, fmt, **kw); return b.getvalue()


def zip_of(name, text, when=(2026, 8, 24, 9, 14, 2)):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo(name, date_time=when), text)
    return b.getvalue()


def minimal_pdf(title):
    """A tiny but genuinely valid PDF, so `file` and a hex editor both agree."""
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    stream = b"BT /F1 12 Tf 20 50 Td (" + title.encode() + b") Tj ET"
    objs[3] = b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
    out = bytearray(b"%PDF-1.4\n")
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += str(i).encode() + b" 0 obj\n" + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 " + str(len(objs) + 1).encode() + b"\n0000000000 65535 f \n"
    for o in offs:
        out += ("%010d 00000 n \n" % o).encode()
    out += (b"trailer\n<< /Size " + str(len(objs) + 1).encode() + b" /Root 1 0 R >>\nstartxref\n"
            + str(xref).encode() + b"\n%%EOF\n")
    return bytes(out)


def build(out):
    os.makedirs(out, exist_ok=True)

    # (filename, real type, bytes, honest?)  -- 5 of the 12 lie about themselves
    items = [
        ("q3_summary.pdf",        "PDF",  minimal_pdf("Q3 summary - Meridian Retail Group"),        True),
        ("floorplan.png",         "PNG",  as_bytes(img(240, 160, (58, 74, 96), "FLOORPLAN", 1), "PNG"), True),
        ("badge_photo.jpg",       "JPEG", as_bytes(img(200, 200, (96, 62, 58), "BADGE", 2), "JPEG", quality=85), True),
        ("archive_2026.zip",      "ZIP",  zip_of("ledger.csv", "sku,qty\nMRG-2001,8\n"),            True),
        ("readme.txt",            "TEXT", b"Meridian Retail Group - shared drive index\r\n"
                                          b"Contact the AP team for access requests.\r\n",          True),
        # --- the five that lie ---
        ("invoice_scan.jpg",      "PDF",  minimal_pdf("Invoice 2026-0812"),                         False),
        ("meeting_notes.txt",     "PNG",  as_bytes(img(220, 140, (70, 70, 96), "SITE PLAN", 3), "PNG"), False),
        ("holiday_snap.jpg",      "ZIP",  zip_of("inventory.csv", "sku,qty\nMRG-1001,42\n"),        False),
        ("policy_v2.docx",        "PNG",  as_bytes(img(180, 120, (60, 84, 66), "NOT A DOC", 4), "PNG"), False),
        ("thumbnail.png",         "JPEG", as_bytes(img(160, 160, (86, 62, 96), "THUMB", 5), "JPEG", quality=80), False),
        # --- two that are damaged rather than misnamed: header intact, tail truncated ---
        ("scan_partial.png",      "PNG (truncated)",
                                  as_bytes(img(200, 150, (52, 66, 82), "PARTIAL", 6), "PNG")[:900], True),
        ("export_partial.jpg",    "JPEG (truncated)",
                                  as_bytes(img(200, 150, (82, 66, 52), "PARTIAL", 7), "JPEG", quality=85)[:700], True),
    ]

    names = []
    for name, _kind, data, _honest in items:
        p = os.path.join(out, name)
        open(p, "wb").write(data)
        os.utime(p, (MTIME, MTIME))
        names.append(name)

    def dig(alg, n):
        h = hashlib.new(alg); h.update(open(os.path.join(out, n), "rb").read()); return h.hexdigest()

    for alg, ext in (("sha256", "sha256"), ("md5", "md5")):
        open(os.path.join(out, f"EVS-05.{ext}"), "w").writelines(
            f"{dig(alg, n)}  {n}\n" for n in names)

    print(f"EVS-05 written to {out}\n")
    print(f"{'file':22} {'claims':>6}  {'really is':16} {'bytes':>7}  first 4 bytes")
    for name, kind, data, honest in items:
        ext = name.rsplit(".", 1)[1].upper()
        flag = "" if honest else "   <-- MISMATCH"
        print(f"{name:22} {ext:>6}  {kind:16} {len(data):7d}  {data[:4].hex(' ').upper()}{flag}")
    print("\nSHA-256:")
    for n in names:
        print(f"  {n:22} {dig('sha256', n)}")
    print("\nMD5:")
    for n in names:
        print(f"  {n:22} {dig('md5', n)}")
    return names


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    build(ap.parse_args().out)
