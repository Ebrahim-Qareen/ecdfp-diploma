#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_evs11.py -- EVS-11, the file-system and carving set.

Builds four artifacts for P09:

  EVS-11-ntfs.dd   64 MiB NTFS: a resident file, a non-resident file, a file
                   with an alternate data stream, and a DELETED file whose
                   content is still inside its MFT record.
  EVS-11-fat.dd    40 MiB FAT32: five live files, one of them deliberately
                   FRAGMENTED into two runs, and one deleted file whose
                   directory entry survives with its size and first cluster.
  EVS-11-carve.dd  the same volume with both FAT copies and the root directory
                   zeroed -- 0.2% of the image, and the file system is gone.
  carve_compare.png  the fragmented photo as carved, beside the original.

Nothing here is downloaded and nothing is a real person's data.

Usage: python3 make_evs11.py --out <a path OUTSIDE the repo>/EVS-11
Requires: mkfs.ntfs + ntfscp + ntfs-3g (ntfs-3g package), mkfs.fat + mtools,
          Pillow and reportlab for the payload files.
"""
import argparse, hashlib, os, struct, subprocess, sys, time

FIXED_MTIME = 1787994000                      # 2026-08-24 09:00:00 UTC
FAT_DATE = ((2026 - 1980) << 9) | (8 << 5) | 24
FAT_TIME = (9 << 11)
NTFS_TIME = 133679592000000000                # the same instant, in 100 ns since 1601


def sh(*a):
    r = subprocess.run(a, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r.returncode:
        sys.stdout.write(r.stdout.decode('utf-8', 'replace'))
        raise SystemExit('failed: ' + ' '.join(a))
    return r.stdout


# ---------------------------------------------------------------- payloads --
def payloads(out):
    """Five real files with real magic bytes. Drawn, not downloaded."""
    from PIL import Image, ImageDraw
    import zipfile
    from reportlab.pdfgen import canvas
    j = lambda n: os.path.join(out, n)

    def img(path, w, h, seed, txt, fmt):
        im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
        for y in range(h):
            for x in range(0, w, 8):
                d.rectangle([x, y, x + 7, y],
                            fill=((x * 3 + seed) % 256, (y * 5 + seed) % 256, (x + y + seed) % 256))
        d.rectangle([10, 10, w - 10, 60], fill=(0, 0, 0))
        d.text((20, 25), txt, fill=(255, 255, 255))
        im.save(path, fmt, **({'quality': 88} if fmt == 'JPEG' else {}))

    img(j('site_photo.jpg'), 640, 400, 11, 'SITE PHOTO 2026-08-24', 'JPEG')
    img(j('whiteboard.jpg'), 800, 500, 77, 'WHITEBOARD - PLAN', 'JPEG')
    img(j('badge_scan.png'), 400, 250, 33, 'BADGE SCAN', 'PNG')

    # a ZIP stores a timestamp per member; without a fixed one the archive --
    # and therefore the image containing it -- differs on every build.
    zt = (2026, 8, 24, 9, 0, 0)
    with zipfile.ZipFile(j('exports.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo('export/readme.txt', zt), 'Quarterly export bundle.\n' * 20)
        z.writestr(zipfile.ZipInfo('export/rows.csv', zt), 'id,name,amount\n' +
                   ''.join('%d,row%d,%d\n' % (i, i, i * 7) for i in range(400)))

    def pdf(path, title, lines):
        # invariant=1 pins reportlab's /CreationDate, /ModDate and document ID
        c = canvas.Canvas(path, invariant=1)
        c.drawString(72, 760, title)
        for i, t in enumerate(lines):
            c.drawString(72, 730 - i * 20, t)
        c.save()

    pdf(j('handover.pdf'), 'HANDOVER NOTE - Case 04',
        ['Line %d: exhibit received, sealed, photographed.' % i for i in range(30)])
    pdf(j('old_invoice.pdf'), 'INVOICE 2026-0418 - SUPERSEDED',
        ['Item %d: consultancy day rate, revision withdrawn.' % i for i in range(22)])

    open(j('notes.txt'), 'w').write('Handover notes for case 04. The disk was received sealed.\n' * 5)
    open(j('report.bin'), 'wb').write(bytes(range(256)) * 800)
    open(j('budget.csv'), 'w').write('item,cost\nlaptop,1200\nmonitor,300\n')
    open(j('old_plan.txt'), 'w').write('DRAFT PLAN 2026 -- superseded, delete before review.\n' * 4)
    open(j('logs.txt'), 'wb').write(
        b''.join(b'2026-08-24 09:%02d:%02d  svc  connection from 10.20.30.%d\n'
                 % (i // 60 % 60, i % 60, i % 254) for i in range(700))[:9 * 4096 - 100])
    for n in ('site_photo.jpg', 'whiteboard.jpg', 'badge_scan.png', 'exports.zip',
              'handover.pdf', 'old_invoice.pdf', 'notes.txt', 'report.bin',
              'budget.csv', 'old_plan.txt', 'logs.txt'):
        os.utime(j(n), (FIXED_MTIME, FIXED_MTIME))


# -------------------------------------------------------------- NTFS bits --
def mft_records(d, bps, frs, base, count):
    """Yield (record_index, absolute_offset) for every FILE record."""
    for n in range(count):
        off = base + n * frs
        if d[off:off + 4] == b'FILE':
            yield n, off


def apply_fixup(rec, bps):
    uo, uc = struct.unpack('<HH', rec[4:8])
    usa = rec[uo:uo + uc * 2]
    r = bytearray(rec)
    for i in range(1, uc):
        e = i * bps - 2
        if e + 2 <= len(r):
            r[e:e + 2] = usa[i * 2:i * 2 + 2]
    return r


def undo_fixup(r, bps):
    """Put the update-sequence value back at every sector end and store the
    real bytes in the array. Editing a record without this corrupts it."""
    uo, uc = struct.unpack('<HH', r[4:8])
    val = bytes(r[uo:uo + 2])
    for i in range(1, uc):
        e = i * bps - 2
        if e + 2 <= len(r):
            r[uo + i * 2:uo + i * 2 + 2] = r[e:e + 2]
            r[e:e + 2] = val
    return r


def pin_ntfs(path):
    """mkntfs writes a random volume serial and stamps every record with the
    clock, so two builds of the same volume never match. This walks the $MFT
    and pins both timestamp sets in $STANDARD_INFORMATION (0x10) and
    $FILE_NAME (0x30) -- the same attributes an examiner reads."""
    d = bytearray(open(path, 'rb').read())
    bps = struct.unpack('<H', d[11:13])[0]
    spc = d[13]
    mft = struct.unpack('<Q', d[48:56])[0] * spc * bps
    fr = struct.unpack('<b', d[64:65])[0]
    frs = 2 ** (-fr) if fr < 0 else fr * spc * bps
    d[72:80] = bytes.fromhex('C4197FA3C4197FA3')          # volume serial
    t8 = struct.pack('<Q', NTFS_TIME)
    n = 0
    for idx, off in mft_records(d, bps, frs, mft, 4096):
        rec = apply_fixup(d[off:off + frs], bps)
        used = struct.unpack('<I', rec[0x18:0x1C])[0]
        a = struct.unpack('<H', rec[0x14:0x16])[0]
        touched = False
        while 0 < a < min(used, frs - 8):
            t = struct.unpack('<I', rec[a:a + 4])[0]
            if t == 0xFFFFFFFF:
                break
            ln = struct.unpack('<I', rec[a + 4:a + 8])[0]
            if ln == 0 or a + ln > frs:
                break
            if t in (0x10, 0x30) and rec[a + 8] == 0:      # resident only
                co = struct.unpack('<H', rec[a + 0x14:a + 0x16])[0]
                b = a + co + (0 if t == 0x10 else 8)       # $FILE_NAME: skip the parent ref
                for k in range(4):
                    rec[b + k * 8:b + k * 8 + 8] = t8
                touched = True
            a += ln
        if touched:
            d[off:off + frs] = undo_fixup(rec, bps)
            n += 1
    open(path, 'wb').write(bytes(d))
    return n


def build_ntfs(out, j):
    img = j('EVS-11-ntfs.dd')
    sh('dd', 'if=/dev/zero', 'of=' + img, 'bs=1M', 'count=64', 'status=none')
    sh('mkfs.ntfs', '-F', '-Q', '-L', 'CASENTFS', '-s', '512', '-c', '4096', img)
    for f in ('notes.txt', 'report.bin', 'budget.csv', 'old_plan.txt'):
        sh('ntfscp', img, j(f), f)
    mnt = j('_mnt')
    os.path.isdir(mnt) or os.makedirs(mnt)
    sh('ntfs-3g', '-o', 'streams_interface=windows', img, mnt)
    try:
        open(os.path.join(mnt, 'budget.csv:notes'), 'w').write(
            'SECOND STREAM: the payload nobody lists.\n')
        os.remove(os.path.join(mnt, 'old_plan.txt'))
    finally:
        subprocess.run(['sync'])
        if subprocess.run(['fusermount', '-u', mnt]).returncode:
            subprocess.run(['umount', mnt])
    os.rmdir(mnt)
    return pin_ntfs(img)


# --------------------------------------------------------------- FAT bits --
class Fat32(object):
    def __init__(self, path):
        self.path = path
        self.d = bytearray(open(path, 'rb').read())
        d = self.d
        self.bps = struct.unpack('<H', d[11:13])[0]
        self.spc = d[13]
        self.rsvd = struct.unpack('<H', d[14:16])[0]
        self.nfat = d[16]
        self.fsz = struct.unpack('<I', d[36:40])[0]
        self.rootc = struct.unpack('<I', d[44:48])[0]
        self.CL = self.bps * self.spc
        self.fat0 = self.rsvd * self.bps
        self.data = (self.rsvd + self.nfat * self.fsz) * self.bps

    def off(self, c):
        return self.data + (c - 2) * self.CL

    def get_fat(self, c):
        o = self.fat0 + c * 4
        return struct.unpack('<I', self.d[o:o + 4])[0] & 0x0FFFFFFF

    def set_fat(self, c, v):
        for k in range(self.nfat):
            o = self.fat0 + k * self.fsz * self.bps + c * 4
            old = struct.unpack('<I', self.d[o:o + 4])[0]
            self.d[o:o + 4] = struct.pack('<I', (old & 0xF0000000) | (v & 0x0FFFFFFF))

    def chain(self, c):
        out = []
        while 2 <= c < 0x0FFFFFF8:
            out.append(c)
            c = self.get_fat(c)
        return out

    def entries(self):
        """(index, raw 32 bytes, absolute offset) for the root directory."""
        base = self.off(self.rootc)
        for i in range(self.CL // 32):
            e = base + i * 32
            if self.d[e] == 0:
                return
            yield i, bytes(self.d[e:e + 32]), e

    def write_by_hand(self, name8, ext3, payload, chain):
        """Place a file at chosen clusters. This is what the file system does;
        doing it here is the only way to control fragmentation exactly --
        mtools allocates from a next-free hint and will not fragment."""
        assert (len(payload) + self.CL - 1) // self.CL == len(chain)
        for i, c in enumerate(chain):
            blk = payload[i * self.CL:(i + 1) * self.CL].ljust(self.CL, b'\x00')
            o = self.off(c)
            self.d[o:o + self.CL] = blk
            self.set_fat(c, chain[i + 1] if i + 1 < len(chain) else 0x0FFFFFFF)
        base = self.off(self.rootc)
        for i in range(self.CL // 32):
            e = base + i * 32
            if self.d[e] == 0:
                ent = bytearray(32)
                ent[0:8] = name8.ljust(8).encode()
                ent[8:11] = ext3.ljust(3).encode()
                ent[11] = 0x20
                ent[14:16] = struct.pack('<H', FAT_TIME)
                ent[16:18] = struct.pack('<H', FAT_DATE)
                ent[18:20] = struct.pack('<H', FAT_DATE)
                ent[20:22] = struct.pack('<H', chain[0] >> 16)
                ent[22:24] = struct.pack('<H', FAT_TIME)
                ent[24:26] = struct.pack('<H', FAT_DATE)
                ent[26:28] = struct.pack('<H', chain[0] & 0xFFFF)
                ent[28:32] = struct.pack('<I', len(payload))
                self.d[e:e + 32] = ent
                return i
        raise SystemExit('root directory full')

    def save(self):
        open(self.path, 'wb').write(bytes(self.d))


def pin_fat_label(path):
    """mkfs.fat stamps the volume-label directory entry with the clock."""
    d = bytearray(open(path, 'rb').read())
    bps = struct.unpack('<H', d[11:13])[0]
    spc = d[13]
    rsvd = struct.unpack('<H', d[14:16])[0]
    nfat = d[16]
    fsz = struct.unpack('<I', d[36:40])[0]
    root = struct.unpack('<I', d[44:48])[0]
    off = (rsvd + nfat * fsz) * bps + (root - 2) * spc * bps
    for i in range(spc * bps // 32):
        e = off + i * 32
        if d[e] == 0:
            break
        if d[e + 11] & 0x08 and not d[e + 11] & 0x10:
            d[e + 13] = 0
            d[e + 14:e + 16] = struct.pack('<H', FAT_TIME)
            d[e + 16:e + 18] = struct.pack('<H', FAT_DATE)
            d[e + 18:e + 20] = struct.pack('<H', FAT_DATE)
            d[e + 22:e + 24] = struct.pack('<H', FAT_TIME)
            d[e + 24:e + 26] = struct.pack('<H', FAT_DATE)
            open(path, 'wb').write(bytes(d))
            return
    raise SystemExit('no volume-label entry in ' + path)


# The fragmented file's layout is computed from the volume, not hard-coded:
# the first attempt hard-coded cluster 19 and silently OVERWROTE the deleted
# file that had just been placed there, which removed the very artifact the
# carving lesson depends on. Lay out after everything already allocated.
WB_A, WB_B, LOG_N = 9, 10, 9


def build_fat(out, j):
    img = j('EVS-11-fat.dd')
    sh('dd', 'if=/dev/zero', 'of=' + img, 'bs=1M', 'count=40', 'status=none')
    sh('mkfs.fat', '-F', '32', '-n', 'CASEFAT', '-S', '512', '-s', '8',
       '-i', 'C0DE1234', img)
    pin_fat_label(img)
    for f in ('site_photo.jpg', 'badge_scan.png', 'exports.zip',
              'handover.pdf', 'old_invoice.pdf'):
        sh('mcopy', '-m', '-i', img, j(f), '::/' + f)
    sh('mdel', '-i', img, '::/old_invoice.pdf')          # entry survives as 0xE5

    v = Fat32(img)
    used = [c for c in range(2, 4096) if v.get_fat(c)]
    start = max(used) + 2                     # +2 leaves the deleted file's cluster alone
    a_run = list(range(start, start + WB_A))
    l_run = list(range(start + WB_A, start + WB_A + LOG_N))
    b_run = list(range(start + WB_A + LOG_N, start + WB_A + LOG_N + WB_B))
    v.write_by_hand('WHITEB~1', 'JPG', open(j('whiteboard.jpg'), 'rb').read(), a_run + b_run)
    v.write_by_hand('LOGS    ', 'TXT', open(j('logs.txt'), 'rb').read(), l_run)
    v.save()
    return img, (a_run[0], len(a_run)), (b_run[0], len(b_run)), (l_run[0], len(l_run))


def build_carve(out, j):
    """The same volume with its metadata gone and its data untouched."""
    src = j('EVS-11-fat.dd')
    dst = j('EVS-11-carve.dd')
    v = Fat32(src)
    d = bytearray(open(src, 'rb').read())
    nfb = v.nfat * v.fsz * v.bps
    d[v.fat0:v.fat0 + nfb] = b'\x00' * nfb
    d[v.off(v.rootc):v.off(v.rootc) + v.CL] = b'\x00' * v.CL
    open(dst, 'wb').write(bytes(d))
    return nfb + v.CL, len(d)


SIGS = [('jpg', b'\xff\xd8\xff', b'\xff\xd9', 0),
        ('png', b'\x89PNG\r\n\x1a\n', b'IEND\xaeB`\x82', 0),
        ('pdf', b'%PDF-', b'%%EOF', 0),
        ('zip', b'PK\x03\x04', b'PK\x05\x06', 18)]


def carve(path):
    """A header/footer carver in fifteen lines. This is the whole idea, and
    every limitation on the page comes from these fifteen lines being all
    there is."""
    d = open(path, 'rb').read()
    found = []
    for kind, hdr, ftr, tail in SIGS:
        i = 0
        while True:
            i = d.find(hdr, i)
            if i < 0:
                break
            k = d.find(ftr, i)
            if k < 0:
                break
            end = k + len(ftr) + tail
            found.append((kind, i, d[i:end]))
            i = end
    found.sort(key=lambda x: x[1])
    return found


def compare_png(out, j):
    from PIL import Image, ImageDraw
    got = [b for kind, off, b in carve(j('EVS-11-carve.dd'))
           if kind == 'jpg' and len(b) > 100000]
    if not got:
        return None
    open(j('carved_whiteboard.jpg'), 'wb').write(got[0])
    a = Image.open(j('whiteboard.jpg')).convert('RGB')
    b = Image.open(j('carved_whiteboard.jpg')).convert('RGB')
    W, H = 800, 500
    o = Image.new('RGB', (W * 2 + 36, H + 64), (14, 18, 24))
    dr = ImageDraw.Draw(o)
    o.paste(a.resize((W, H)), (12, 46))
    o.paste(b.resize((W, H)), (W + 24, 46))
    dr.text((14, 20), 'ORIGINAL  whiteboard.jpg  %d bytes' % os.path.getsize(j('whiteboard.jpg')),
            fill=(200, 220, 240))
    dr.text((W + 26, 20), 'CARVED  %d bytes  --  it opens, and it is not the same file' % len(got[0]),
            fill=(255, 150, 120))
    o.save(j('carve_compare.png'))
    return len(got[0])


def build(out):
    os.environ['TZ'] = 'UTC'
    time.tzset()
    os.makedirs(out, exist_ok=True)
    j = lambda n: os.path.join(out, n)

    payloads(out)
    n = build_ntfs(out, j)
    _, ra, rb, rl = build_fat(out, j)
    wiped, total = build_carve(out, j)
    carved = compare_png(out, j)

    print('NTFS   : %d MFT records pinned' % n)
    print('FAT    : whiteboard.jpg fragmented %s + %s, logs.txt in the gap %s'
          % (ra, rb, rl))
    print('carve  : %d of %d bytes wiped (%.4f%%), fragmented photo carved as %s B'
          % (wiped, total, wiped * 100.0 / total, carved))

    for n2 in ('site_photo.jpg', 'whiteboard.jpg', 'badge_scan.png', 'exports.zip',
               'handover.pdf', 'old_invoice.pdf', 'notes.txt', 'report.bin',
               'budget.csv', 'old_plan.txt', 'logs.txt', 'carved_whiteboard.jpg'):
        try:
            os.remove(j(n2))
        except OSError:
            pass

    # -- what is reproducible, and what is not --------------------------------
    # FAT and the carve image are byte-identical across builds. NTFS is NOT:
    # mkntfs writes a journal, an $MFTMirr and index entries that all carry
    # timestamps, and pinning those would mean forging a $LogFile that does not
    # match what happened -- which is a worse thing to hand a student than an
    # unstable hash. So the manifest also carries the four MFT records the page
    # actually reads. Those ARE stable, and they are what a student checks.
    stable = []
    d = open(j('EVS-11-ntfs.dd'), 'rb').read()
    bps = struct.unpack('<H', d[11:13])[0]
    spc = d[13]
    mft = struct.unpack('<Q', d[48:56])[0] * spc * bps
    for n2 in (64, 65, 66, 67):
        rec = bytes(apply_fixup(d[mft + n2 * 1024:mft + (n2 + 1) * 1024], bps))
        stable.append('%s  EVS-11-ntfs.dd:MFT#%d' % (hashlib.sha256(rec).hexdigest(), n2))

    lines = []
    for name in sorted(os.listdir(out)):
        if not (name.endswith('.dd') or name.endswith('.png')):
            continue
        h = hashlib.sha256(open(j(name), 'rb').read()).hexdigest()
        lines.append('%s  %s' % (h, name))
        print('%-22s %10d B  %s' % (name, os.path.getsize(j(name)), h[:16] + '...'))
    print()
    for x in stable:
        print('%s' % x)
    open(j('EVS-11.sha256'), 'w').write('\n'.join(lines + [''] + stable) + '\n')
    print('\nmanifest written: EVS-11.sha256')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    build(ap.parse_args().out)
