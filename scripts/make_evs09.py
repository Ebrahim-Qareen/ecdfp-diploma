#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_evs09.py -- EVS-09-timeline, the super-timeline for P14 (the capstone).

Tier 3, and legitimately so: this is an artifact EXPORT (a CSV timeline), the
class Tier 3 permits -- not a fabricated hive or .evtx. It is a plaso-style
`l2tcsv` super-timeline that stitches ONE coherent incident from the SAME kinds
of artifacts the diploma read on P08-P13: a phishing email, a registry Run-key
persistence, a prefetch execution, a Windows logon, a file deletion, a C2
beacon, and a log clear -- each row carrying the source artifact it came from,
so the capstone can teach correlation across evidence types on one axis.

The rows are consistent with the real evidence sets already built (EVS-08's
IP 185.220.101.7 and C2 sync-check.net; EVS-12's HAXOR4 / Mountain time), so a
student can trace a timeline row back to the page that taught that artifact.

Usage: python3 make_evs09.py --out <path OUTSIDE the repo>/EVS-09
"""
import argparse, hashlib, os, sys, datetime

# one incident, on one clock (UTC), 2020-09-13
INCIDENT = [
    # (datetime,           source,        sourcetype,          host,     user,     short,                                             MACB, evidence)
    ('2020-09-13 12:20:10', 'EMAIL',       'Email header',      'MX',     'l.bennett','phish INV-4471 from invoices-cloud.net (SPF/DMARC fail)', '....', 'EVS-08-email.eml'),
    ('2020-09-13 12:24:03', 'WEBHIST',     'Browser history',   'FIN-WKS-07','l.bennett','GET http://sync-check.net/api/v1/check (clicked link)', '....', 'History (P09)'),
    ('2020-09-13 12:24:07', 'PE/EXEC',     'Prefetch',          'FIN-WKS-07','-',      'A.EXE-*.pf run count 1, first execution',          'MACB', 'EVS-13 Prefetch'),
    ('2020-09-13 12:24:07', 'REG',         'Registry (Sysmon 13)','FIN-WKS-07','l.bennett','HKLM\\..\\Run\\ set to "c:\\windows\\tasks\\taskhost.exe"', '...B', 'EVS-14 sysmon 13'),
    ('2020-09-13 12:24:20', 'NET',         'PCAP (C2 beacon)',  'FIN-WKS-07','-',      'first beacon to sync-check.net, 30s interval begins', '....', 'EVS-08.pcap'),
    ('2020-09-13 12:26:29', 'EVT',         'Security 4624',     'FIN-WKS-07','user01', 'LogonType 9 (NewCredentials) via seclogo -- pass-the-hash', '....', 'EVS-14 4624'),
    ('2020-09-13 12:28:40', 'NET',         'PCAP (DNS tunnel)', 'FIN-WKS-07','-',      '3 TXT queries to exfil-dns.net (client list exfil)', '....', 'EVS-08.pcap'),
    ('2020-09-13 12:30:00', 'NET',         'PCAP (HTTP exfil)', 'FIN-WKS-07','-',      'POST /upload.php 2.4KB to 185.220.101.7',         '....', 'EVS-08.pcap'),
    ('2020-09-13 12:31:12', 'FILE',        'Recycle Bin $I',    'FIN-WKS-07','l.bennett','C:\\temp sent to Recycle Bin (staging cleanup)',  'MAC.', 'EVS-13 $I'),
    ('2020-09-13 12:34:25', 'EVT',         'System 104',        'FIN-WKS-07','user01', 'System event log cleared',                         '....', 'EVS-14 104'),
    ('2020-09-13 12:35:07', 'EVT',         'Security 1102',     'FIN-WKS-07','user01', 'Security event log cleared',                       '....', 'EVS-14 1102'),
]


def l2t_row(dtstr, source, stype, host, user, short, macb, evidence):
    dt = datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
    date = dt.strftime('%m/%d/%Y'); time = dt.strftime('%H:%M:%S')
    # plaso l2tcsv columns
    return ','.join([date, time, 'UTC', macb, source, stype,
                     'Creation', user, host,
                     '"%s"' % short, '"%s"' % short,
                     '2', evidence, '-', '-', '-', 'evs09'])


def build(out):
    os.makedirs(out, exist_ok=True)
    j = lambda n: os.path.join(out, n)
    header = ('date,time,timezone,MACB,source,sourcetype,type,user,host,'
              'short,desc,version,filename,inode,notes,format,extra')
    lines = [header] + [l2t_row(*r) for r in INCIDENT]
    open(j('EVS-09-timeline.csv'), 'w').write('\n'.join(lines) + '\n')

    # a "mini bodyfile" excerpt too (mactime-style), for the report screen
    body = []
    for dtstr, source, stype, host, user, short, macb, ev in INCIDENT:
        body.append('%s | %-22s | %-8s | %s' % (dtstr, stype, macb, short))
    open(j('EVS-09-incident.txt'), 'w').write('\n'.join(body) + '\n')

    lines2 = []
    for n in sorted(os.listdir(out)):
        if n.endswith('.sha256'): continue
        h = hashlib.sha256(open(j(n), 'rb').read()).hexdigest()
        lines2.append('%s  %s' % (h, n))
        print('%-24s %6d B  %s' % (n, os.path.getsize(j(n)), h[:16] + '...'))
    open(j('EVS-09.sha256'), 'w').write('\n'.join(lines2) + '\n')
    print('\nmanifest written: EVS-09.sha256  (%d timeline rows)' % len(INCIDENT))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    build(ap.parse_args().out)
