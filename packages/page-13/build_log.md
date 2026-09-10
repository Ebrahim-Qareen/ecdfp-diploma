# P13 — Network evidence · build log

**Topics** `T21` Network Evidence (42) · `T22` C2 in Traffic (28) · `T23` Internet & Email Artifacts (20) — **90 minutes**
**Page** `docs/page-13/index.html` — 25 screens, 7 part dividers — shape v2 (`D136`)
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **4** — `F1` the five layers · `F2` the beacon on a timeline · `F3` DNS tunnelling · `F4` the phishing header |
| SIMSCREEN | **1** — `ss-t21`, the instructor demo: tshark through the whole intrusion in five commands |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | `EVS-08` — one synthesized capture, Tier 3, 20 assertions |

## One intrusion, three topics, one capture

`T21`/`T22`/`T23` are taught as a single story because a real case is one: a phishing email delivers a link, the
victim beacons to that C2 every 30 seconds, and the stolen data leaves three ways. `EVS-08` was **built to carry
exactly that story** with measurable ground truth, then read back with tshark for every number on the page.

- **The beacon**: 10 HTTP GETs to `sync-check.net`, seconds 19…289, **every gap exactly 30 s, zero jitter**, a
  2001 MSIE 6.0 UA against modern-Chrome benign traffic. The lesson: **regularity is the finding, and it survives
  encryption** — no payload needed.
- **The DNS tunnel**: 3 Base32 TXT queries to `exfil-dns.net` that **decode in order** to
  `CONFIDENTIAL-CLIENT-LIST-Q3-2020-450-ACCOUNTS`. The tell is the shape, not the content.
- **The plain POST**: ~2.4 KB to `185.220.101.7`, a raw IP.
- **The email header**: SPF/DKIM/DMARC fail, Reply-To a raw IP, **Received from `185.220.101.7`** — the same IP
  as the POST — and its link is `sync-check.net`, the C2. **One IP ties delivery, command channel and exfil**, the
  strongest fact in the case, and it takes both the pcap and the header to see it.

Everything maps to MITRE (T1566.002, T1071.001, T1048.003, T1070.001, T1571).

## Why Tier 3 is honest here

A pcap and text logs are the **one artifact class the project may synthesize** — the Sourcing-tiers table in
`evidence_sets.md` says so, because a capture of traffic we specified is a real recording, unlike a fabricated
hive or `.evtx`. `EVS-08` is **byte-reproducible** (fixed T0, payloads and ports; two builds `cmp`-identical) and
every address is documentation-safe. 20 assertions in `verify08.py`.

## Real tools

Built with `scapy`, verified with **Wireshark/tshark 4.2** — the SIMSCREEN quotes real tshark output. `tshark`
was installed in the build environment and run against the produced pcap.

## Gates

```
python3 scripts/density_gate.py docs/page-13/index.html      ALL PASS
node testing/render_gate.js docs/page-13/index.html          PASS — zero findings
```

Thirteen pages now pass both. (One screen was trimmed from 255 to under 250 words; the email section&rsquo;s
Arabic `ترويسة` was swept to `الـ header` per `D122`.)
