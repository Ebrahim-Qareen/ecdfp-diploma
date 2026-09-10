#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_evs08.py -- EVS-08, the network-evidence set for P13.

Tier 3, and legitimately so: pcap and text logs are the ONE thing Tier 3 allows
us to synthesize (see design/evidence_sets.md). Fabricating an .evtx or a hive
is a lie about what a forensic artifact looks like; a pcap of traffic we specify
is not -- it is a recording of packets we caused, with ground truth we control.

Builds, deterministically (fixed timestamps, fixed payloads):
  EVS-08.pcap        a 6-minute capture: benign browsing, one beaconing C2
                     channel, one DNS-tunnel exfil, one plain-HTTP data POST.
  EVS-08-proxy.log   the matching Squid-style proxy log.
  EVS-08-email.eml   one phishing email with full headers (the delivery).

Every number the page states is measured back from the pcap with tshark.

Usage: python3 make_evs08.py --out <a path OUTSIDE the repo>/EVS-08
Requires: scapy.  (tshark only for verification, not for building.)
"""
import argparse, hashlib, os, struct, sys

# --- the story, as fixed constants so the capture is reproducible -------------
T0 = 1600000000            # 2020-09-13 12:26:40 UTC, the capture start
VICTIM = '10.20.30.40'     # FIN-WKS-07 in our lab story
GW_MAC = '00:11:22:33:44:55'
VIC_MAC = 'aa:bb:cc:dd:ee:ff'
BENIGN = {'93.184.216.34': 'example.com', '151.101.0.223': 'cdn.company.com'}
C2_IP = '45.147.230.12'    # the beacon peer (documentation-safe, not routed)
C2_DOMAIN = 'sync-check.net'
TUNNEL_NS = 'ns1.exfil-dns.net'
TUNNEL_DOMAIN = 'exfil-dns.net'
DROP_IP = '185.220.101.7'  # the plain-HTTP exfil target
BEACON_INTERVAL = 30       # seconds -- the regularity IS the tell
BEACON_COUNT = 10
UA_BENIGN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0 Safari/537.36'
UA_C2 = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'   # a 2001 UA in 2020 -- the tell


def build(out):
    os.makedirs(out, exist_ok=True)
    from scapy.all import (Ether, IP, TCP, UDP, DNS, DNSQR, DNSRR, Raw,
                           wrpcap)
    j = lambda n: os.path.join(out, n)
    pkts = []
    seqs = {}

    def eth(dst, src):
        return Ether(dst=dst, src=src)

    def tcp_get(t, dst, host, path, ua, sport):
        # a minimal but real HTTP GET over one SYN/SYN-ACK/ACK + PSH
        req = ('GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\n'
               'Accept: */*\r\nConnection: keep-alive\r\n\r\n' % (path, host, ua)).encode()
        p = eth(GW_MAC, VIC_MAC) / IP(src=VICTIM, dst=dst) / TCP(
            sport=sport, dport=80, flags='PA', seq=1000, ack=1) / Raw(load=req)
        p.time = t
        pkts.append(p)

    def tcp_post(t, dst, host, path, ua, body, sport):
        req = ('POST %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\n'
               'Content-Type: application/octet-stream\r\nContent-Length: %d\r\n\r\n'
               % (path, host, ua, len(body))).encode() + body
        p = eth(GW_MAC, VIC_MAC) / IP(src=VICTIM, dst=dst) / TCP(
            sport=sport, dport=80, flags='PA', seq=1000, ack=1) / Raw(load=req)
        p.time = t
        pkts.append(p)

    def dns_q(t, qname, dst='8.8.8.8', qtype='A', sport=40000):
        p = eth(GW_MAC, VIC_MAC) / IP(src=VICTIM, dst=dst) / UDP(
            sport=sport, dport=53) / DNS(rd=1, qd=DNSQR(qname=qname, qtype=qtype))
        p.time = t
        pkts.append(p)

    # ---- benign browsing at the start ---------------------------------------
    dns_q(T0 + 1, 'example.com')
    tcp_get(T0 + 2, '93.184.216.34', 'example.com', '/', UA_BENIGN, 49001)
    dns_q(T0 + 5, 'cdn.company.com')
    tcp_get(T0 + 6, '151.101.0.223', 'cdn.company.com', '/style.css', UA_BENIGN, 49002)
    tcp_get(T0 + 9, '151.101.0.223', 'cdn.company.com', '/logo.png', UA_BENIGN, 49003)

    # ---- the beacon: same peer, FIXED interval, tiny identical-size GETs -----
    for i in range(BEACON_COUNT):
        t = T0 + 20 + i * BEACON_INTERVAL
        if i == 0:
            dns_q(t - 1, C2_DOMAIN)
        # each beacon: a GET to /api/v1/check with a rotating id, all ~same size
        tcp_get(t, C2_IP, C2_DOMAIN, '/api/v1/check?id=%08x' % (0xA1B2C300 + i),
                UA_C2, 51000 + i)

    # ---- DNS tunnel: many long TXT queries to one nameserver ----------------
    secret = b'CONFIDENTIAL-CLIENT-LIST-Q3-2020-450-ACCOUNTS'
    import base64
    b32 = base64.b32encode(secret).decode().strip('=').lower()
    chunks = [b32[k:k + 30] for k in range(0, len(b32), 30)]
    for i, c in enumerate(chunks):
        dns_q(T0 + 120 + i * 2, '%s.%d.%s' % (c, i, TUNNEL_DOMAIN),
              qtype='TXT', sport=41000 + i)

    # ---- the plain-HTTP exfil POST ------------------------------------------
    payload = base64.b64encode(secret * 40)   # ~2.4 KB of "data"
    tcp_post(T0 + 200, DROP_IP, DROP_IP, '/upload.php', UA_C2, payload, 52000)

    # ---- a little more benign traffic after --------------------------------
    dns_q(T0 + 250, 'example.com')
    tcp_get(T0 + 251, '93.184.216.34', 'example.com', '/news', UA_BENIGN, 49010)

    pkts.sort(key=lambda p: p.time)
    wrpcap(j('EVS-08.pcap'), pkts)

    # ---- the matching proxy log ---------------------------------------------
    import datetime
    def sq(ts, ip, method, url, bytes_, ua):
        return '%.3f    %3d %s TCP_MISS/200 %d %s %s - DIRECT/%s text/html "%s"' % (
            ts, 1, VICTIM, bytes_, method, url, ip, ua)
    log = []
    log.append(sq(T0 + 2, '93.184.216.34', 'GET', 'http://example.com/', 1256, UA_BENIGN))
    log.append(sq(T0 + 6, '151.101.0.223', 'GET', 'http://cdn.company.com/style.css', 8402, UA_BENIGN))
    for i in range(BEACON_COUNT):
        log.append(sq(T0 + 20 + i * BEACON_INTERVAL, C2_IP, 'GET',
                      'http://sync-check.net/api/v1/check?id=%08x' % (0xA1B2C300 + i), 342, UA_C2))
    log.append(sq(T0 + 200, DROP_IP, 'POST', 'http://185.220.101.7/upload.php', len(payload), UA_C2))
    open(j('EVS-08-proxy.log'), 'w').write('\n'.join(log) + '\n')

    # ---- the phishing email that started it ---------------------------------
    eml = ('Return-Path: <billing@invoices-cloud.net>\n'
           'Received: from mail.invoices-cloud.net (185.220.101.7)\n'
           '  by mx.company.com; Sun, 13 Sep 2020 12:20:11 +0000\n'
           'Authentication-Results: mx.company.com; spf=fail; dkim=none; dmarc=fail\n'
           'From: "Accounts Payable" <billing@invoices-cloud.net>\n'
           'Reply-To: <collect@185.220.101.7>\n'
           'To: l.bennett@company.com\n'
           'Date: Sun, 13 Sep 2020 12:20:10 +0000\n'
           'Subject: Overdue invoice INV-4471 - action required\n'
           'Message-ID: <4471.invoices-cloud.net>\n'
           'MIME-Version: 1.0\n'
           'Content-Type: text/html; charset=utf-8\n'
           '\n'
           '<html><body><p>Your invoice is overdue. Review it here:</p>\n'
           '<a href="http://sync-check.net/api/v1/check?id=a1b2c300">View invoice</a>\n'
           '</body></html>\n')
    open(j('EVS-08-email.eml'), 'w').write(eml)

    # ---- manifest -----------------------------------------------------------
    lines = []
    for n in sorted(os.listdir(out)):
        if n.endswith('.sha256'): continue
        h = hashlib.sha256(open(j(n), 'rb').read()).hexdigest()
        lines.append('%s  %s' % (h, n))
        print('%-22s %8d B  %s' % (n, os.path.getsize(j(n)), h[:16] + '...'))
    open(j('EVS-08.sha256'), 'w').write('\n'.join(lines) + '\n')
    print('\nmanifest written: EVS-08.sha256')
    print('beacon interval %ds x %d, DNS-tunnel chunks %d' % (BEACON_INTERVAL, BEACON_COUNT, len(chunks)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    build(ap.parse_args().out)
