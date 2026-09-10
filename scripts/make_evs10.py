#!/usr/bin/env python3
"""
make_evs10.py — EVS-10, the Session 3 hidden-information image set.

Tier 3 (synthesized) and legitimately so: these are IMAGES WE AUTHOR, not forensic containers.
`ecdfp-evidence` forbids synthesizing .evtx / E01 / AD1 / raw disk images / memory dumps /
registry hives. Images, and data hidden inside them, are ours to make.

Deterministic: fixed seed, fixed base timestamps -> a student's regenerated copy is byte-identical
to the instructor's and therefore diffable.

Constraints honoured: fictional company and people (Meridian Retail Group, l.bennett), NO real PII,
NO credentials, documentation IP ranges only, and no question in this set has a secret or a
person's data as its answer (D41).

Usage:  python3 make_evs10.py --out <a path OUTSIDE the repo>/EVS-10
"""
import argparse, hashlib, io, os, random, struct, zipfile
from datetime import datetime, timezone

from PIL import Image, ImageDraw
import piexif

SEED = 20260824                      # fixed
BASE = "2026:08:24 09:14:02"         # EXIF DateTimeOriginal — inside the F7 attack window
RESAVE = "2026:08:31 16:40:05"       # EXIF DateTime (the later resave)
MTIME = 1788307200                   # file mtime, deliberately later again


def canvas(w, h, bg, label, sub="", seedmod=0):
    """A plain generated image. No photograph, no third-party asset, no licence question."""
    rnd = random.Random(SEED + seedmod)
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for i in range(14):                                   # deterministic texture
        x0 = rnd.randrange(0, w); y0 = rnd.randrange(0, h)
        d.rectangle([x0, y0, x0 + rnd.randrange(18, 70), y0 + rnd.randrange(18, 70)],
                    fill=tuple(rnd.randrange(40, 210) for _ in range(3)))
    d.rectangle([0, h - 46, w, h], fill=(18, 20, 28))
    d.text((10, h - 34), label, fill=(235, 238, 245))
    if sub:
        d.text((10, h - 20), sub, fill=(150, 160, 180))
    return im


def exif_bytes(desc, gps=True, with_thumb=None, dt=BASE, dt_digitized=BASE, dt_mod=BASE):
    z = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    z["0th"][piexif.ImageIFD.Make] = b"Meridian"
    z["0th"][piexif.ImageIFD.Model] = b"MRG-CAM-11"
    z["0th"][piexif.ImageIFD.Software] = b"MRG ImageTool 2.4"
    z["0th"][piexif.ImageIFD.ImageDescription] = desc.encode()
    z["0th"][piexif.ImageIFD.DateTime] = dt_mod.encode()
    z["Exif"][piexif.ExifIFD.DateTimeOriginal] = dt.encode()
    z["Exif"][piexif.ExifIFD.DateTimeDigitized] = dt_digitized.encode()
    if gps:
        # A deliberately checkable location. Fictional context, real-format coordinates.
        z["GPS"][piexif.GPSIFD.GPSLatitudeRef] = b"N"
        z["GPS"][piexif.GPSIFD.GPSLatitude] = ((30, 1), (2, 1), (2760, 100))
        z["GPS"][piexif.GPSIFD.GPSLongitudeRef] = b"E"
        z["GPS"][piexif.GPSIFD.GPSLongitude] = ((31, 1), (14, 1), (1320, 100))
        z["GPS"][piexif.GPSIFD.GPSDateStamp] = b"2026:08:24"
    if with_thumb is not None:
        b = io.BytesIO(); with_thumb.save(b, "JPEG", quality=70)
        z["thumbnail"] = b.getvalue()
    return piexif.dump(z)


def lsb_hide(im, message):
    """Classic LSB in the blue channel. The point students must learn is DETECTION."""
    px = im.load()
    payload = message.encode() + b"\x00"
    bits = "".join(f"{b:08b}" for b in payload)
    w, h = im.size
    if len(bits) > w * h:
        raise ValueError("message too long")
    i = 0
    for y in range(h):
        for x in range(w):
            if i >= len(bits):
                return im
            r, g, b = px[x, y]
            px[x, y] = (r, g, (b & 0xFE) | int(bits[i]))
            i += 1
    return im


def build(out):
    os.makedirs(out, exist_ok=True)
    files = []

    def write(name, data, mtime=MTIME, exif=None):
        # piexif.insert() wants a path, not bytes -- write first, then insert in place.
        p = os.path.join(out, name)
        with open(p, "wb") as f:
            f.write(data)
        if exif is not None:
            piexif.insert(exif, p)
        os.utime(p, (mtime, mtime))
        files.append(name)

    # 1 -- EXIF + GPS, and three timestamps that disagree with each other and with the file system
    im = canvas(640, 420, (52, 74, 96), "MERIDIAN RETAIL GROUP", "office floor 3", 1)
    b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    write("office_floor3.jpg", b.getvalue(),
          exif=exif_bytes("Office floor 3", gps=True, dt=BASE, dt_digitized=BASE, dt_mod=RESAVE))

    # 2 -- LSB steganography in a PNG (lossless, so the bits survive)
    im = canvas(320, 240, (96, 62, 58), "RECEIPT SCAN", "AP-2026-0812", 2)
    im = lsb_hide(im, "MRG-INTERNAL: staged archive is customer_export.7z")
    b = io.BytesIO(); im.save(b, "PNG", optimize=False)
    write("receipt_scan.png", b.getvalue())

    # 2b -- the SAME image without the payload, so students can diff and see LSB noise
    im = canvas(320, 240, (96, 62, 58), "RECEIPT SCAN", "AP-2026-0812", 2)
    b = io.BytesIO(); im.save(b, "PNG", optimize=False)
    write("receipt_scan_clean.png", b.getvalue())

    # 3 -- polyglot: a valid JPEG with a ZIP appended. binwalk / unzip both find it.
    im = canvas(500, 340, (60, 84, 66), "TEAM PHOTO", "Q3 offsite", 3)
    b = io.BytesIO(); im.save(b, "JPEG", quality=85)
    jpg = b.getvalue()
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as z:
        zi = zipfile.ZipInfo("handover.txt", date_time=(2026, 8, 24, 9, 14, 2))
        z.writestr(zi, "Meeting point confirmed. Use the shared drive, not email.\n")
    write("team_photo.jpg", jpg + zb.getvalue())

    # 4 -- extension lies: a PNG called .txt and a ZIP called .jpg
    im = canvas(300, 200, (70, 70, 96), "SITE PLAN", "", 4)
    b = io.BytesIO(); im.save(b, "PNG")
    write("meeting_notes.txt", b.getvalue())

    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as z:
        zi = zipfile.ZipInfo("inventory.csv", date_time=(2026, 8, 25, 11, 0, 0))
        z.writestr(zi, "sku,qty\nMRG-1001,42\nMRG-1002,17\n")
    write("holiday_snap.jpg", zb.getvalue())

    # 5 -- the thumbnail that outlived the edit: main image redacted, EXIF thumbnail is not
    original = canvas(600, 400, (86, 62, 96), "INVOICE BATCH", "pre-redaction", 5)
    edited = original.copy()
    ImageDraw.Draw(edited).rectangle([180, 150, 470, 250], fill=(12, 12, 14))   # the "redaction"
    thumb = original.resize((160, 107))                                          # thumbnail of the ORIGINAL
    b = io.BytesIO(); edited.save(b, "JPEG", quality=88)
    write("invoice_batch.jpg", b.getvalue(),
          exif=exif_bytes("Invoice batch", gps=False, with_thumb=thumb,
                          dt=BASE, dt_digitized=BASE, dt_mod=RESAVE))

    # ---- manifests
    def digest(alg, name):
        h = hashlib.new(alg)
        h.update(open(os.path.join(out, name), "rb").read())
        return h.hexdigest()

    for alg, ext in (("sha256", "sha256"), ("md5", "md5")):
        lines = [f"{digest(alg, n)}  {n}\n" for n in files]
        with open(os.path.join(out, f"EVS-10.{ext}"), "w") as f:
            f.writelines(lines)

    print(f"EVS-10 written to {out}\n")
    print(f"{'file':28} {'bytes':>8}  sha256")
    for n in files:
        print(f"{n:28} {os.path.getsize(os.path.join(out,n)):8d}  {digest('sha256', n)}")
    print("\nMD5 (lookup key only, never the integrity control):")
    for n in files:
        print(f"{n:28} {digest('md5', n)}")
    return files


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    build(ap.parse_args().out)
