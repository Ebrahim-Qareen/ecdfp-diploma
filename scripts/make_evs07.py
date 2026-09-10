#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_evs07.py -- EVS-07, the storage and partitioning set.

Tier 3, synthesized and legitimately so: these are DISK IMAGES WE AUTHOR, not
forensic containers passed off as somebody's evidence. The Tier 3 bar forbids
fabricating an E01 of a real machine, an .evtx, a memory dump or a registry
hive. It does not forbid formatting a 64 MiB file.

Produces
  EVS-07-mbr.dd    64 MiB, hand-written MBR, FAT16 20 MiB + FAT32 40 MiB,
                   five files whose sizes make the slack arithmetic exact
  EVS-07-slack.dd  the FAT16 volume where a deleted document survives in the
                   slack of a 20-byte memo
  EVS-07-gpt.dd    64 MiB GPT: protective MBR, header, entries, backup header
  EVS-07-wiped.dd  EVS-07-mbr.dd with LBA 0 zeroed -- Case 04

Requires: mkfs.fat (dosfstools), mcopy/mdel (mtools), sgdisk (gdisk).
Usage: python3 make_evs07.py --out <a path OUTSIDE the repo>/EVS-07
"""
import argparse, hashlib, os, struct, subprocess, sys, time

CLUSTER_FILES = [('tiny.txt', 1), ('note.txt', 100), ('exact.bin', 4096),
                 ('over.bin', 4097), ('report.pdf', 10000)]
SECRET = b'CONFIDENTIAL-SALARY-BAND-REVIEW-2026-'
DISK_SIG = 0xA37F19C4


def sh(*a):
    r = subprocess.run(a, capture_output=True)
    if r.returncode:
        sys.exit('failed: %s\n%s' % (' '.join(a), r.stderr.decode()[:400]))


def chs(lba):
    """Legacy CHS. Anything past the old limit is written FE FF FF, which is
       what every modern tool does and what every modern tool ignores."""
    if lba >= 1024 * 255 * 63:
        return b'\xfe\xff\xff'
    c, rem = divmod(lba, 255 * 63)
    h, s = divmod(rem, 63)
    return bytes([h, ((c >> 2) & 0xC0) | ((s + 1) & 0x3F), c & 0xFF])


def entry(boot, ptype, start, count):
    return (bytes([0x80 if boot else 0x00]) + chs(start) + bytes([ptype])
            + chs(start + count - 1) + struct.pack('<II', start, count))


def make_payload_files(d):
    for n, sz in CLUSTER_FILES:
        p = os.path.join(d, n)
        with open(p, 'wb') as f:
            f.write((b'PATTERN-%s-' % n.encode()) * ((sz // 24) + 2))
            f.truncate(sz)


FIXED_MTIME = 1787994000  # 2026-08-24 09:00:00 UTC -- the case window


# FAT-encoded 2026-08-24 09:00:00 -- ((y-1980)<<9)|(m<<5)|d and (h<<11)|(m<<5)|(s//2)
FAT_DATE = ((2026 - 1980) << 9) | (8 << 5) | 24
FAT_TIME = (9 << 11) | (0 << 5) | 0


def pin_label_time(path):
    """mkfs.fat stamps the volume-label directory entry with the clock. Four bytes,
    and they are enough to make two builds of the same volume hash differently.
    Parsing the BPB to find that entry is the same walk the students do by hand."""
    d = bytearray(open(path, 'rb').read())
    bps  = struct.unpack('<H', d[11:13])[0]
    spc  = d[13]
    rsvd = struct.unpack('<H', d[14:16])[0]
    nfat = d[16]
    rec  = struct.unpack('<H', d[17:19])[0]
    fsz  = struct.unpack('<H', d[22:24])[0]
    if fsz == 0:                                   # FAT32
        fsz  = struct.unpack('<I', d[36:40])[0]
        root = struct.unpack('<I', d[44:48])[0]
        off  = (rsvd + nfat * fsz) * bps + (root - 2) * spc * bps
        n    = spc * bps // 32
    else:                                          # FAT12/16
        off = (rsvd + nfat * fsz) * bps
        n   = rec
    for i in range(n):
        e = off + i * 32
        if d[e] == 0x00:
            break
        if d[e + 11] & 0x08 and not d[e + 11] & 0x10:
            d[e + 13] = 0                                        # CrtTimeTenth
            d[e + 14:e + 16] = struct.pack('<H', FAT_TIME)       # CrtTime
            d[e + 16:e + 18] = struct.pack('<H', FAT_DATE)       # CrtDate
            d[e + 18:e + 20] = struct.pack('<H', FAT_DATE)       # LstAccDate
            d[e + 22:e + 24] = struct.pack('<H', FAT_TIME)       # WrtTime
            d[e + 24:e + 26] = struct.pack('<H', FAT_DATE)       # WrtDate
            open(path, 'wb').write(bytes(d))
            return
    raise SystemExit('no volume-label entry found in ' + path)


def build(out):
    # FAT directory entries store LOCAL time, so the timezone is part of the
    # output. Pinned here, with the file mtimes, or the images are not
    # reproducible on a machine in another timezone.
    os.environ['TZ'] = 'UTC'
    time.tzset()
    os.makedirs(out, exist_ok=True)
    j = lambda n: os.path.join(out, n)

    # ---- the two volumes ---------------------------------------------------
    # -s 8 forces 8 sectors per cluster = 4096 B, so the slack numbers on the
    # page are exact rather than "whatever mkfs decided today".
    sh('dd', 'if=/dev/zero', 'of=' + j('p1.img'), 'bs=1M', 'count=20', 'status=none')
    sh('dd', 'if=/dev/zero', 'of=' + j('p2.img'), 'bs=1M', 'count=40', 'status=none')
    # -i fixes the FAT volume serial, which mkfs.fat otherwise takes from the
    # clock -- without it two builds of the same volume differ in four bytes.
    sh('mkfs.fat', '-F', '16', '-n', 'CASEDATA', '-S', '512', '-s', '8',
       '-i', 'A1B2C3D4', j('p1.img'))
    sh('mkfs.fat', '-F', '32', '-n', 'ARCHIVE', '-S', '512', '-s', '8',
       '-i', 'B2C3D4E5', j('p2.img'))

    pin_label_time(j('p1.img'))
    pin_label_time(j('p2.img'))

    make_payload_files(out)
    for n, _ in CLUSTER_FILES:
        os.utime(j(n), (FIXED_MTIME, FIXED_MTIME))
        sh('mcopy', '-m', '-i', j('p1.img'), j(n), '::/' + n)

    # ---- the slack volume: write, delete, overwrite with something smaller --
    sh('cp', j('p1.img'), j('EVS-07-slack.dd'))
    with open(j('secret.txt'), 'wb') as f:
        f.write(SECRET * 110)
    with open(j('memo.txt'), 'wb') as f:
        f.write(b'Team lunch Thursday.')
    os.utime(j('secret.txt'), (FIXED_MTIME, FIXED_MTIME))
    os.utime(j('memo.txt'), (FIXED_MTIME, FIXED_MTIME))
    sh('mcopy', '-m', '-i', j('EVS-07-slack.dd'), j('secret.txt'), '::/secret.txt')
    sh('mdel', '-i', j('EVS-07-slack.dd'), '::/secret.txt')
    sh('mcopy', '-m', '-i', j('EVS-07-slack.dd'), j('memo.txt'), '::/memo.txt')

    # ---- the MBR disk, table written by hand --------------------------------
    sh('dd', 'if=/dev/zero', 'of=' + j('EVS-07-mbr.dd'), 'bs=1M', 'count=64', 'status=none')
    d = bytearray(open(j('EVS-07-mbr.dd'), 'rb').read())
    mbr = bytearray(512)
    mbr[0:3] = b'\x33\xc0\xfa'
    mbr[440:444] = struct.pack('<I', DISK_SIG)
    mbr[446:462] = entry(True, 0x06, 2048, 40960)
    mbr[462:478] = entry(False, 0x0C, 45056, 81920)
    mbr[510:512] = b'\x55\xaa'
    d[0:512] = mbr
    open(j('EVS-07-mbr.dd'), 'wb').write(bytes(d))
    sh('dd', 'if=' + j('p1.img'), 'of=' + j('EVS-07-mbr.dd'), 'bs=512', 'seek=2048',
       'conv=notrunc', 'status=none')
    sh('dd', 'if=' + j('p2.img'), 'of=' + j('EVS-07-mbr.dd'), 'bs=512', 'seek=45056',
       'conv=notrunc', 'status=none')

    # ---- the GPT disk -------------------------------------------------------
    sh('dd', 'if=/dev/zero', 'of=' + j('EVS-07-gpt.dd'), 'bs=1M', 'count=64', 'status=none')
    # sgdisk invents a random disk GUID and two random partition GUIDs. Fixed
    # values here, or the two CRC32 fields in the header differ every build.
    sh('sgdisk', '-n', '1:2048:+20M', '-t', '1:0700', '-c', '1:CASEDATA',
       '-n', '2:0:+30M', '-t', '2:0700', '-c', '2:ARCHIVE',
       '-u', '1:11111111-2222-3333-4444-555555555551',
       '-u', '2:11111111-2222-3333-4444-555555555552',
       '-U', '11111111-2222-3333-4444-555555555550', j('EVS-07-gpt.dd'))

    # ---- Case 04: zero LBA 0 and nothing else -------------------------------
    w = bytearray(open(j('EVS-07-mbr.dd'), 'rb').read())
    w[0:512] = b'\x00' * 512
    open(j('EVS-07-wiped.dd'), 'wb').write(bytes(w))

    for n in ('p1.img', 'p2.img', 'secret.txt', 'memo.txt') + tuple(f for f, _ in CLUSTER_FILES):
        try:
            os.remove(j(n))
        except OSError:
            pass

    # ---- manifest -----------------------------------------------------------
    lines = []
    for n in sorted(os.listdir(out)):
        if not n.endswith('.dd'):
            continue
        h = hashlib.sha256(open(j(n), 'rb').read()).hexdigest()
        lines.append('%s  %s' % (h, n))
        print('%-20s %10d B  %s' % (n, os.path.getsize(j(n)), h[:16] + '...'))
    open(j('EVS-07.sha256'), 'w').write('\n'.join(lines) + '\n')
    print('\nmanifest written: EVS-07.sha256')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    build(ap.parse_args().out)
