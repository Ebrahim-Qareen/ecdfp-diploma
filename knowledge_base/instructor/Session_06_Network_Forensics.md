# Instructor Session 06 — Network Forensics

| | |
|---|---|
| **Deck** | `Resources/Instructor/session 6.pdf` — 72 slides, 52 screenshots |
| **INE material covered** | unit 7 — see [`Module_04_System_and_Network_Forensics.md`](../Module_04_System_and_Network_Forensics.md) |
| **Feeds eCDFP session** | `S6` |
| **Source text** | [`../_source_text/Instructor_Session_06_Network_Forensics.md`](../_source_text/Instructor_Session_06_Network_Forensics.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

The longest deck in the course and the most lecture-heavy: **sixty slides of networking
fundamentals before the first lab.** Slides 4–48 rebuild the stack from OSI down to ARP —
protocols, ports, the TCP handshake, HTTP/HTTPS, SMTP, FTP, SSH, DNS, DHCP, ICMP, ARP — then
slides 49–55 walk the **OSCAR methodology**, 56–58 cover acquisition, 59–63 show four attack
patterns, and only at slide 64 does the lab start.

That ordering is a deliberate choice and it is the right one for a mixed-level room: you cannot
read a pcap you cannot read a packet from. But it costs roughly three hours before anyone opens
Wireshark, and the rebuilt `S6` has **141 minutes total** for network work *plus* timelines,
reporting and the capstone. See §5 — this deck cannot be delivered as-is.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–3 | Course outline, session title | `admin` |
| 4–6 | OSI model; PDU per layer (packet at L3, frame at L2); client-server model | `concept` |
| 7 | Message types — unicast / multicast / broadcast | `concept` |
| 8–10 | Networking devices — switch (L2, MAC), router (L3, IP) | `concept` |
| 11–12 | Protocol metadata; application layer | `concept` |
| 13–18 | Transport layer; SCTP/DCCP/RSVP named as out of scope; port ranges; the well-known 0–1023 range; **ephemeral source ports** | `concept` |
| 19 | TCP vs UDP | `concept` |
| 20–21 | Three-way handshake with sequence/ack numbers; the same handshake in Wireshark | `demo` |
| 22 | UDP segment structure | `concept` |
| 23–24 | Data-link layer; 48-bit MAC = 24-bit OUI + 24-bit NIC; message classes again | `concept` |
| 25–26 | Common protocols; public standard vs proprietary format | `concept` |
| 27–31 | HTTP in the clear; GET/POST; request anatomy; response codes 1xx–5xx | `concept` |
| 32–33 | HTTPS = HTTP over SSL/TLS, shown as `Application Data (23)`; can we decrypt? | `concept` |
| 34–36 | Symmetric vs asymmetric; hash functions; SSL/TLS | `concept` |
| 37–39 | SMTP — fraud/harassment cases; `HELO`, `MAIL FROM`, `RCPT TO`; a conversation | `concept` |
| 40–41 | FTP (cleartext, `331 Please specify the password.`); SSH | `concept` |
| 42–43 | DNS; record types A, AAAA, PTR, TXT, NS, MX | `concept` |
| 44–45 | DHCP — IP, lease time, default gateway, DNS servers | `concept` |
| 46–47 | ICMP echo request/reply; "the echo request contains dummy data" | `concept` |
| 48 | ARP — MAC↔IP mapping, with `arp -a` on screen | `demo` |
| 49–55 | **OSCAR methodology** — Obtain, Strategise, Collect, Analyse, Report (six steps as taught) | `concept` |
| 56–58 | Acquisition — wiretapping by medium; sniffers | `concept` |
| 59–63 | Attacks — rogue DHCP, port scanning, MAC flooding, ARP poisoning | `concept` |
| 64 | **Lab agenda** + challenge-capture download link | `admin` |
| 65–67 | **Lab 1** — capture live traffic in Wireshark, save as pcapng | `lab` |
| 68–69 | **Lab 2** — Evidence 1: filter by suspect IP, recover first comment and username | `lab` |
| 70–71 | **Lab 2** — extract an email attachment, inspect in HxD | `lab` |
| 72 | **Lab 2** — the same job with NetworkMiner | `lab` |

## 2 · Labs and demos — what was actually run

### The three-way handshake, live · slides 20–21
**Tools:** Wireshark
**Steps as demonstrated:** slide 20 gives the theory with concrete numbers —
`SYN seq: 100` → `SYN-ACK seq: 200 ack: 101` → `ACK seq: 101 ack: 201`, with the state machine
annotated (`SYN-SENT` → `SYN-RECEIVED` → `ESTABLISHED` on both sides). Slide 21 then shows the
same three packets in a real capture (`wireshark_Wi-Fi…pcapng`, 137 packets, 62 displayed —
so a display filter was applied; **the filter string itself is not legible**).

`⚠ OCR — verify` the filter on the slide. The conventional form is `tcp.flags.syn == 1` or
`tcp.flags.syn == 1 && tcp.flags.ack == 0`.

**What this lab teaches:** a handshake is three packets with arithmetically related numbers —
which is what lets you say two hosts *actually established a session*, not merely exchanged
traffic.

### ARP table on the host · slide 48
**Tools:** Windows `arp`
**Steps as demonstrated:**

```
arp -a
```

Output shown includes the broadcast entry
`255.255.255.255   ff-ff-ff-ff-ff-ff   static`.
`⚠` The prompt in the capture is the presenter's own profile (`C:\Users\<user>>`) — see §6.

**What this lab teaches:** IP↔MAC bindings are local, cached and forgeable — the setup for the
ARP-poisoning slide at 63.

### Lab 1 · live capture and save · slides 65–67
**Tools:** **Wireshark 4.4.1** (`v4.4.1-0-9575b2bf4746e`, as shown on the start screen)
**Steps as demonstrated:**

1. Open Wireshark; the start screen lists available interfaces —
   `Adapter for loopback traffic capture`, `Local Area Connection* 8/9/10`,
   `Bluetooth Network Connection`, `VMware Network Adapter VMnet8`, `VMware Network Adapter
   VMnet1`, `Wi-Fi`. A capture filter box sits under the interface list, unused here.
2. Double-click the interface (`Wi-Fi` in the capture) to start.
3. Traffic appears live. The screenshot shows QUIC and DNS — notably
   `Standard query 0xfee9 A accounts.google.com` and its response
   `A accounts.google.com A 108.177.15.84`, plus QUIC `Initial` and `0-RTT` packets to that
   address. The detail pane is expanded through
   `Frame → Ethernet II → Internet Protocol Version 4 → User Datagram Protocol → QUIC IETF`,
   with `Src Port: 50630, Dst Port: 443`.
4. Stop, then **File → Save As**; the deck notes the saved file is a network capture and the
   dialog offers `Wireshark/… - pcapng`.

**What this lab teaches:** modern traffic is mostly opaque — the capture is real, current and
almost entirely QUIC/TLS. **The DNS query is the one readable thing in it**, and that is
exactly the `S6-05` lesson about DNS as the surviving name evidence when payloads are encrypted.
The deck does not draw that conclusion; make it explicit.

### Lab 2 · working a challenge capture · slides 68–72
**Tools:** Wireshark; **HxD**; **NetworkMiner**
**Evidence used:** `evidence01.pcap` — one of a set `evidence01`–`evidence07` the deck
distributes by link (§5). The MRU list on slide 65 shows the presenter's folder was named
`network forensics chellenges`.

> **Provenance note — act on this before reuse.** The capture is worked by filtering on
> `192.168.1.158` and recovering a chat comment, a username and an emailed attachment for a
> subject named **"Ann"**. That is the signature of the **Network Forensics Puzzle Contest**
> series (Puzzle #1, *Ann's Bad AIM*, LMG Security / forensicscontest.com) — a well-known
> public DFIR corpus with published answer keys. If so it is a strong **Tier 2** candidate for
> `S6`: linked, never rehosted, licence recorded. **Confirm the origin and route it through
> `ecdfp-evidence` before any use** — do not adopt it on the strength of this note.

**Steps as demonstrated:**

1. Open `evidence01.pcap`. Apply a display filter for the suspect host:

```
ip.addr == 192.168.1.158
```

(The screenshot shows this typed into the filter bar with the green/valid highlight.)

2. Slide 69 — "First comment and Ann username": read the recovered chat content and account
   name out of the filtered stream. **The mechanism is not shown** — no `Follow TCP Stream`
   screenshot survives. Recover the step from the slide, or rebuild it: `Follow → TCP Stream`
   on the messaging conversation is the standard route.
3. Slides 70–71 — "extracting email attachments": the attachment is carved out and opened in
   **HxD** (the title bar shows a `.docx` on the presenter's Desktop). Again the **extraction
   step is not on screen** — the likely route is `File → Export Objects → HTTP/IMF`, or
   `Follow Stream → Show data as Raw → Save as`.
4. Slide 72 — "using automated tool (network miner)": the same extraction repeated in
   **NetworkMiner**, which parses files, credentials and sessions out of a pcap automatically.
   **No screenshot content resolved for this slide.**

**What this lab teaches:** filter to the host, follow the conversation, export the payload,
then verify the payload's type in hex — and then show that a tool does the same thing in one
click. Doing it by hand first and NetworkMiner second is the right order; keep it.

## 3 · Registry keys, paths and artifacts named on the slides

This deck names protocol fields and evidence sources rather than on-disk artifacts.

| Artifact / evidence source | As shown | Purpose given | Module reference |
|---|---|---|---|
| pcap / pcapng capture | Saved from Wireshark; `evidence01.pcap` … `evidence07.pcap` | Full packet evidence | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| DNS query / response | `Standard query 0xfee9 A accounts.google.com` → `A 108.177.15.84` | Name resolution, readable when payload is not | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| TCP handshake | `SYN seq:100` / `SYN-ACK seq:200 ack:101` / `ACK seq:101 ack:201` | Proof a session was established | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| Ephemeral source port | Destination 80/443 fixed, source random (`50630` in the capture) | Distinguishing client from server | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| MAC address | 48 bits = 24-bit OUI + 24-bit NIC identifier | Vendor attribution at L2 | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| ARP cache | `arp -a` on the live host | IP↔MAC bindings | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| TLS record type | `Content Type: Application Data (23)` | Marks encrypted payload | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| SMTP verbs | `HELO`, `MAIL FROM:`, `RCPT TO:` | Sender/recipient attribution | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| FTP response | `331 Please specify the password.` | Cleartext credential exchange | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |
| DNS record types | A, AAAA, PTR, TXT, NS, MX | What each answer means | [M04 §2B](../Module_04_System_and_Network_Forensics.md) |

## 4 · What this deck adds beyond the INE material

- **A working Wireshark workflow on current software.** INE unit 7 is 455 pages of protocol
  theory with very little tooling; this deck is where Wireshark 4.4.1 and NetworkMiner actually
  appear.
- **A live capture of modern traffic (slide 66)** — QUIC over UDP/443, TLS `Application Data`.
  INE's material predates QUIC entirely. This single screenshot is the best available argument
  for why DNS and flow metadata now carry the investigation.
- **The challenge capture set** (`evidence01`–`evidence07`) — seven ready-made network
  investigations with a known-good answer path, if the provenance in §2 checks out.
- **The manual-then-automated pairing** (HxD carve → NetworkMiner) — a teaching pattern INE
  never uses and which the rebuilt course should keep everywhere.
- **The four attack patterns (slides 59–63)** presented from the *defender's* pcap view rather
  than the attacker's.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted, and needed for `S6`:**

- **C2 beaconing.** Not present anywhere. The topic map's `S6-05` requires beaconing intervals,
  DNS anomalies and TLS fingerprinting, and `D19` makes a C2 beacon part of the carry-through
  incident. **This is the largest gap in the deck**, and INE unit 7 does not cover it well
  either — see [`Module_04`](../Module_04_System_and_Network_Forensics.md) §7.
- **`tcpdump` and capture methodology** — capture filters, ring buffers, what a filtered capture
  loses. `S6-03` requires it; the deck is Wireshark-only.
- **Statistical flow analysis** (INE `7.6.4`, pp. 293–308) — NetFlow/IPFIX, and what flow shows
  when payload is encrypted. Given slide 66's QUIC capture, this omission is acute.
- **Wireshark display-filter fluency as a taught skill.** Exactly one filter appears in the whole
  deck (`ip.addr ==`). `S6-02` needs a filter vocabulary — `tcp.stream`, `http.request.method`,
  `dns.qry.name`, `frame contains`, `tls.handshake.type`.
- **Export Objects and Follow Stream** — used implicitly in Lab 2, never shown.
- **Email header analysis** — SMTP verbs are taught, but `Received:` header chains, the actual
  attribution technique, are not.
- **INE `7.8 OSCAR` is covered; INE `7.9 Network Evidence Acquisition` (pp. 341–368) is not** —
  taps, SPAN ports, inline vs passive, and the legal constraints on wiretapping get three
  slides (56–58) against INE's 28 pages.

**Delivery-time reality check.** Slides 4–48 are ~45 slides of networking fundamentals.
The rebuilt `S6` budget for network topics is far smaller than that, and `S6` also carries
timelines, the report and the capstone. Options, in order of preference:

1. **Move fundamentals to pre-work.** Issue slides 4–48 as a required pre-read/video with a
   short entry quiz; open `S6` at OSCAR. This is the only option that preserves the labs.
2. Cut to what a pcap reading actually needs: L2/L3/L4 addressing, ports, the handshake,
   HTTP/DNS/TLS, and drop SMTP/FTP/SSH/ICMP/DHCP to a reference sheet.
3. Keep the fundamentals and drop Lab 2 — **not recommended**; the lab is the session.

**Resources cited on slides** (all `unverified` — do not link from `docs/` until checked):

- `https://easyupload.io/5dh4fk` — challenge captures `evidence01`–`evidence07` (slide 64).
  A free file-drop link; **assume it is already dead** and re-host.
- `https://en.wikipedia.org/wiki/NTFS` and `InterviewBit`, `Ciscozine` image credits — diagram
  sources only.

## 6 · Cautions before reuse

- **Personal and home-network data in screenshots — regenerate on the course lab before reuse:**
  - **slide 48** — the `arp -a` capture shows the presenter's own command prompt path.
  - **slide 65** — the Wireshark MRU list shows the presenter's working tree
    (`D:\Work\ECDFP\network forensics chellenges\…`) across six entries.
  - **slide 66** — a **live capture of the presenter's own home network**: private IP
    `192.168.1.119`, the router at `192.168.1.1`, real Intel and TP-Link MAC addresses, and the
    hosts they were talking to (including a Google account-login DNS query). This is real
    personal traffic and should not be reused as-is under `R9`.
  - **slide 67** — the Save dialog shows the presenter's `Documents` folder and its contents.
  - **slide 71** — HxD title bar shows a Desktop path under the presenter's profile.
- **Re-capture slide 66 on FOR-WS01.** A synthetic QUIC/DNS capture makes the same point with
  no personal data, and can then be hashed and published as an evidence set.
- **The challenge-capture link (slide 64) is a `easyupload.io` drop** — ephemeral by design and
  the single point of failure for the entire lab. Confirm the corpus origin (see §2), then
  either link the original publisher or distribute on the academy share with hashes.
- **Slide 33 — "practically impossible" to decrypt HTTPS without the key.** True as stated, but
  it invites the wrong conclusion that encrypted traffic is worthless. Follow it immediately
  with what *is* still visible: SNI, certificate details, JA3/JA4 fingerprints, timing, volume,
  DNS. Slide 66's own capture proves the point.
- **Slide 35 lists AES, DES and RC4 as "common cryptographic algorithms" under the heading
  *Hash function*.** All three are ciphers, not hashes. Correct this before delivery — a
  student who confuses hashing with encryption fails criterion 1 of the report rubric.
- **Slide 34 — RSA described as "the most used cryptographic algorithm nowadays".** Dated;
  ECDHE/ECDSA dominate TLS today. Minor, but it sits next to a real error.
- **Wireshark 4.4.1 is from late 2024.** Confirm the classroom build before the run.
- **OCR-unresolved and worth checking on the slide:** the display filter on slide 21;
  the entirety of slides 69, 70 and 72 (the recovered username, the extraction step, and the
  NetworkMiner screen) — these are the three steps the lab most needs and the three the OCR
  recovered least.
