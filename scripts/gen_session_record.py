#!/usr/bin/env python3
# ============================================================================
# gen_session_record.py -- eCDFP Diploma
# One template + per-session step data -> each docs/session-NN/record.html.
#
# STRUCTURE follows the published standards, not invention:
#   SWGDE 18-Q-002  report content: general info | request & authority |
#                   item identification | results | opinions + basis |
#                   DISPOSITION | AUTHORIZATION + signature
#   SWGDE 18-F-002  chain of custody minimum: unique identifier, date/time of
#                   receipt, record of ALL transfers with name and signature
#   ISO/IEC 27037   phases: identification -> collection -> acquisition ->
#                   preservation; every action reconstructible by a third party
#   CoC six elements: WHAT · HOW · WHO · WHEN · WHERE · WHY
#
# CUMULATIVE: session N shows every earlier session collapsed ("carried
# forward") and session N open. Ids are stable and come from the data, so
# regenerating never changes an id or disturbs saved case data.
# The custody-transfer log and disposition are CASE-level (one running chain),
# rendered once -- never per session, or the chain would fragment.
#
# Evidence IDs come from design/evidence_sets.md (ecdfp-evidence) and are never
# invented here. Examples use placeholder digests, never real case data, and
# never reveal which EVS-01 file is altered (that is Case 01).
#
#   python3 scripts/gen_session_record.py            # all sessions
#   python3 scripts/gen_session_record.py --stdout s2
# ============================================================================
import html
import os
import sys

# ------------------------------------------------- case header (SWGDE 5.1-5.3)
# Three official groups. Filled once; shared across every session on this browser.
CASE_HEADER = [
    ("General information", [
        ("org",       "Organization",              False, "ITGate Academy — Forensic Lab"),
        ("case_id",   "Case / reference number",   False, "e.g. FL-2026-014"),
        ("examiner",  "Examiner name & role",      False, "e.g. A. Analyst, Forensic Analyst"),
        ("rec_date",  "Record date (UTC)",         False, "YYYY-MM-DD"),
    ]),
    ("Request & authority", [
        ("requestor", "Requestor & organization",  False, "who tasked the examination"),
        ("authority", "Legal authority + reference", False, "warrant # / consent / lab job #"),
        ("scope",     "Purpose & scope of examination", True,
            "the questions the examination must answer — and what is out of scope"),
    ]),
    ("Item identification", [
        ("item_id",   "Item ID + description",     True,
            "EVS-01 · EVI-SRC01 seizure package — make / model / serial where a device applies"),
        ("received",  "Received from / delivery method", False, "instructor distribution / hand delivery"),
        ("recv_time", "Date & time received (UTC)", False, "YYYY-MM-DD hh:mm"),
        ("acq_hash",  "Acquisition hash (SHA-256)", False, "as supplied with the item"),
    ]),
]

# ------------------------------------------------------------ shared step text
def auth_step(sid):
    return {
        "id": sid + "-auth", "type": "gate",
        "name": "Authorization & scope check",
        "cmd": "confirm authority before touching the exhibit",
        "example":
            '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
            '<span class="gui-title">authorization — as recorded</span></div><div class="gui-body">'
            '<span class="gui-row"><b>Authority</b><span>Internal investigation — lab job #FL-2026-014</span></span>'
            '<span class="gui-row"><b>Scope</b><span>the exhibit named above · no external systems</span></span>'
            '<span class="gui-row"><b>Out of scope</b><span>anything not in the exhibit</span></span>'
            '<span class="gui-row"><b>Examiner</b><span>&lt;name&gt;, Forensic Analyst</span></span>'
            '<span class="gui-row"><b>Confirmed</b><span>&lt;YYYY-MM-DD hh:mm&gt; UTC</span></span>'
            '</div><span class="gui-cap">Illustrative — fictional job number, no real data.</span></div>',
        "collect": [
            "Authority type and its reference — warrant #, consent, or lab job #",
            "Scope: what you may examine, and what is out of scope",
            "Examiner name and role",
            "Date and time (UTC) authority was confirmed",
        ],
        "why": "SWGDE 18-Q-002 §5.2 requires the legal authority and the scope of the request on the face "
               "of the report. Without it the evidence — and everything derived from it — is inadmissible. "
               "This is the root of the chain: every step below inherits it.",
        "notes_ph": "Authority + reference · scope / out-of-scope · examiner · date-time (UTC)",
    }


def workingcopy_step(sid):
    return {
        "id": sid + "-wc", "type": "active",
        "name": "Working copy verified before examination",
        "cmd": "re-hash the copy · never the original",
        "example":
            '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
            '<span class="gui-title">verify the working copy</span></div><div class="gui-body">'
            '<span class="l"><span class="p">$</span> sha256sum working/image.E01</span>'
            '<span class="l ok">&lt;digest&gt;  == acquisition hash — match</span>'
            '<span class="l d"># original remains sealed and untouched</span>'
            '</div></div>',
        "collect": [
            "Working-copy path, and its hash equal to the acquisition hash",
            "Confirmation the original was not opened this session",
            "Examination platform, and every tool with its version",
        ],
        "why": "ISO/IEC 27037 requires every action to be reconstructible by a qualified third party — that "
               "starts from a copy proven identical to what was acquired. An examination on an unverified "
               "copy proves nothing about the original.",
        "notes_ph": "Copy path + hash = acquisition hash · original untouched · platform + tool versions",
    }


def custody_step(sid):
    return {
        "id": sid + "-coc", "type": "active",
        "name": "Chain-of-custody entry",
        "cmd": "who · what · when · where · why · integrity",
        "example":
            '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
            '<span class="gui-title">custody entry</span></div><div class="gui-body">'
            '<span class="gui-row"><b>Released by</b><span>&lt;name&gt; — signature</span></span>'
            '<span class="gui-row"><b>Received by</b><span>&lt;name&gt; — signature</span></span>'
            '<span class="gui-row"><b>Item</b><span>&lt;item ID&gt;</span></span>'
            '<span class="gui-row"><b>When / where</b><span>&lt;YYYY-MM-DD hh:mm&gt; UTC · Lab WS-01</span></span>'
            '<span class="gui-row"><b>Purpose</b><span>examination</span></span>'
            '<span class="gui-row"><b>Integrity</b><span>SHA-256 re-verified — match</span></span>'
            '</div></div>',
        "collect": [
            "Released by and received by — name AND signature for each",
            "Item unique identifier",
            "Date/time (UTC), and location",
            "Purpose of the transfer",
            "Hash re-verified at transfer? match or mismatch",
        ],
        "why": "SWGDE 18-F-002 sets the minimum: a unique identifier, the date and time, and a record of all "
               "transfers identifying each person taking possession by name and signature. These are the six "
               "elements — who, what, when, where, why, how — and a gap in them is what gets attacked.",
        "notes_ph": "released by → received by (names) · item ID · when/where (UTC) · purpose · hash match?",
    }


def close_step(sid, final=False):
    return {
        "id": sid + "-close", "type": "active",
        "name": ("Final hash-verify, disposition & authorization  ·  [RITUAL]" if final
                 else "Hash-verify, close & disposition  ·  [RITUAL]"),
        "cmd": "re-verify · record disposition",
        "example":
            '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
            '<span class="gui-title">session close</span></div><div class="gui-body">'
            '<span class="l"><span class="p">$</span> sha256sum -c manifest.sha256   <span class="d"># at close</span></span>'
            '<span class="l ok">unchanged from receipt — chain unbroken</span>'
            '<span class="l">Disposition: original returned to store · working copy retained</span>'
            '<span class="l">Closed &lt;YYYY-MM-DD hh:mm&gt; UTC — &lt;examiner&gt;</span>'
            '</div></div>',
        "collect": [
            "Re-verify result at close — match or mismatch",
            "Close date/time (UTC) and examiner",
            "Confirmation the chain is unbroken, with any change explained",
            "Disposition — what happened to the original and to the working copy "
            "(retained / returned / destroyed)",
        ],
        "why": "SWGDE 18-Q-002 §5.6 requires the disposition of originals and derivative works. Re-verifying "
               "at close proves the exhibit left this session in the state it arrived, and hands the chain to "
               "the next session intact.",
        "notes_ph": "Re-verify result · close date-time (UTC) · chain unbroken? · disposition of original + copy",
    }


# ------------------------------------------------------------------- sessions
def S(sid, num, title, phase, evidence, mid_sections):
    """A session: gate first, topic steps, then custody + close. Same spine every time."""
    sections = [{"label": "A · Authorization — the root of the chain", "steps": [auth_step(sid)]}]
    sections += mid_sections
    sections.append({"label": "Z · Custody & close",
                     "steps": [custody_step(sid), close_step(sid, final=(sid == "s6"))]})
    return {"id": sid, "num": num, "title": title, "phase": phase,
            "evidence": evidence, "gate": sid + "-auth", "sections": sections}


SESSIONS = [
    S("s1", "01", "Foundations — Evidence Integrity & Chain of Custody",
      "Preservation · Chain of custody", "EVS-01 · EVI-SRC01 seizure package",
      [{"label": "B · Receipt & integrity", "steps": [
        {
            "id": "s1-a1", "type": "doc",
            "name": "Exhibit receipt & identification",
            "cmd": "log the package before you open it",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">EVS-01 — received</span></div><div class="gui-body">'
                '<span class="l d"># 6 files, as distributed</span>'
                '<span class="l">seizure_notes.txt · EVI-SRC01_acquisition_log.txt</span>'
                '<span class="l">custody_form_EVI-SRC01.txt · evidence_inventory.csv</span>'
                '<span class="l d">EVS-01.sha256 · EVS-01.md5   # the signed manifest</span>'
                '<span class="l">received: instructor distribution · state: read-only, complete</span>'
                '</div></div>',
            "collect": [
                "Unique identifier and description of the item (SWGDE §5.3)",
                "Date and time of receipt, and from whom",
                "Delivery method, and its state as received — complete, read-only",
                "Where it is stored and how access is controlled",
            ],
            "why": "SWGDE 18-Q-002 §5.3 requires each item to be uniquely identifiable — by make, model, "
                   "serial number or hash. A vague head of chain means nothing below it ties to a specific item.",
            "notes_ph": "Item ID + description · received from / when · delivery · state · storage",
        },
        {
            "id": "s1-a2", "type": "active",
            "name": "Integrity verification against the signed manifest",
            "cmd": "sha256sum -c EVS-01.sha256",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">verify against the manifest</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> sha256sum -c manifest.sha256</span>'
                '<span class="l ok">exhibit_A.txt: OK</span>'
                '<span class="l ok">exhibit_B.txt: OK</span>'
                '<span class="l no">exhibit_C.txt: FAILED</span>'
                '<span class="l d">sha256sum: WARNING: 1 computed checksum did NOT match</span>'
                '</div><span class="gui-cap">Illustrative names — which file fails in EVS-01 is yours to find.</span></div>'
                '<div class="finding"><span class="cl-label">Finding — how to write it</span>'
                '<p><code>exhibit_C.txt</code> did not verify: computed SHA-256 <code>&lt;digest&gt;</code> '
                '&ne; manifest <code>&lt;digest&gt;</code>. Both algorithms recorded.</p></div>',
            "collect": [
                "Tool and version — e.g. sha256sum (GNU coreutils 9.4)",
                "MD5 and SHA-256 per file — both, every time",
                "Result per file: match or mismatch — a mismatch is recorded, never omitted",
                "The two digests being compared for any file that failed",
            ],
            "why": "SHA-256 is the value you defend; MD5 is a lookup key, never the control. A mismatch is a "
                   "finding, not an inconvenience — and a tool reporting “verified” means it compared its own "
                   "write to its own read-back, not that the evidence is untampered.",
            "notes_ph": "Tool+version · per file MD5 & SHA-256 · match/mismatch · which file failed",
        },
        {
            "id": "s1-a3", "type": "active",
            "name": "Working copy & write-block discipline",
            "cmd": "examine the copy, never the original",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">work on a copy · prove read-only</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> cp -r EVS-01 EVS-01_working</span>'
                '<span class="l"><span class="p">$</span> (cd EVS-01_working &amp;&amp; sha256sum -c EVS-01.sha256)</span>'
                '<span class="l d"># imaging a device instead? record the blocker BEFORE connecting the source:</span>'
                '<span class="l">Write blocker: Tableau T8u · engaged &lt;time&gt; UTC · verified read-only</span>'
                '</div></div>',
            "collect": [
                "Working-copy path and its hash — equal to the original's",
                "Confirmation the original was not worked on",
                "For a device: write-blocker make/model, engaged before the source was connected",
                "For a read-only file set: that no blocker was required — and say so explicitly",
            ],
            "why": "Proves the original was never altered. Recording how read-only was assured is what answers "
                   "the challenge “how do you know you didn't change it?” — the question every cross-examination "
                   "reaches eventually.",
            "notes_ph": "Copy path + hash = original · original untouched · blocker model / read-only note",
        },
      ]}]),

    S("s2", "02", "Acquisition — Disk, Memory & Live Response",
      "Identification · Collection · Acquisition", "EVS-02 · EVS-03 · EVS-04 · EVS-09",
      [{"label": "B · Identification & collection", "steps": [
        {
            "id": "s2-a1", "type": "doc",
            "name": "Scene & device documentation",
            "cmd": "document before you touch",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">device as found</span></div><div class="gui-body">'
                '<span class="gui-row"><b>State</b><span>powered ON · screen unlocked · 2 windows open</span></span>'
                '<span class="gui-row"><b>Make / model</b><span>&lt;make&gt; &lt;model&gt;</span></span>'
                '<span class="gui-row"><b>Serial</b><span>&lt;serial&gt;</span></span>'
                '<span class="gui-row"><b>Condition</b><span>no damage · 1 USB device attached</span></span>'
                '<span class="gui-row"><b>Location</b><span>&lt;where&gt; · photographed</span></span>'
                '</div></div>',
            "collect": [
                "Device state — powered on or off, screen locked, open files or windows",
                "Physical characteristics — make, model, serial, damage, identifying marks",
                "Every connection and attached device",
                "Location, described in writing and photographed",
            ],
            "why": "SWGDE 18-F-002 requires all of this at collection. Powered off, you do not turn it on; "
                   "powered on, you never reboot. The state as found can only be recorded once — and it is "
                   "the fact a later examiner cannot recover.",
            "notes_ph": "State (on/off, locked?) · make/model/serial · condition · connections · location + photos",
        },
        {
            "id": "s2-a2", "type": "active",
            "name": "Volatile capture — order of volatility",
            "cmd": "RAM before disk · isolate the network",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">volatile first</span></div><div class="gui-body">'
                '<span class="l d"># most volatile first: RAM → connections → processes → disk</span>'
                '<span class="l"><span class="p">&gt;</span> winpmem_&lt;ver&gt;.exe -o E:\\mem.raw</span>'
                '<span class="l ok">acquired 16 GiB · SHA-256 &lt;digest&gt;</span>'
                '<span class="l d"># network isolated before collection · least-invasive tooling</span>'
                '</div></div>',
            "collect": [
                "Order of collection actually followed, most volatile first",
                "Memory tool and version, dump size, and its hash",
                "That the host was isolated from the network, and when",
                "Every command run on the live host — each one changes it",
            ],
            "why": "Volatile data is destroyed by the next action, including yours. ISO/IEC 27037 asks that a "
                   "third party can reconstruct what you did; on a live host that is only possible if every "
                   "command and its time are recorded as you go.",
            "notes_ph": "Collection order · memory tool+version · dump size + hash · isolation · commands run",
        },
      ]},
       {"label": "C · Acquisition & imaging", "steps": [
        {
            "id": "s2-a3", "type": "active",
            "name": "Write blocker engaged",
            "cmd": "record it BEFORE connecting the source",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">write blocker</span></div><div class="gui-body">'
                '<span class="gui-row"><b>Type</b><span>hardware</span></span>'
                '<span class="gui-row"><b>Make / model</b><span>Tableau T8u</span></span>'
                '<span class="gui-row"><b>Engaged</b><span>&lt;YYYY-MM-DD hh:mm&gt; UTC — before connection</span></span>'
                '<span class="gui-row"><b>Verified</b><span>read-only confirmed</span></span>'
                '</div></div>',
            "collect": [
                "Hardware or software blocker, with make/model or product and version",
                "The time it was engaged — which must precede connecting the source",
                "How read-only was verified",
            ],
            "why": "The blocker is only evidence of anything if it was recorded before the source was attached. "
                   "Written afterwards it proves nothing, because the write you are ruling out would already "
                   "have happened.",
            "notes_ph": "Blocker type · make/model or version · engaged time (UTC) · read-only verified how",
        },
        {
            "id": "s2-a4", "type": "active",
            "name": "Image acquisition",
            "cmd": "FTK Imager 8.3 · dc3dd",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">acquisition log</span></div><div class="gui-body">'
                '<span class="gui-row"><b>Tool</b><span>FTK Imager 8.3</span></span>'
                '<span class="gui-row"><b>Source</b><span>&lt;device&gt; · &lt;serial&gt;</span></span>'
                '<span class="gui-row"><b>Destination</b><span>&lt;path&gt;/EVI-SRC01.E01</span></span>'
                '<span class="gui-row"><b>Format</b><span>E01 · segment 2048 MB · compression 6</span></span>'
                '<span class="gui-row"><b>Sectors</b><span>&lt;n&gt; · errors: 0</span></span>'
                '</div></div>',
            "collect": [
                "Tool and exact version — a tool without a version is not a method",
                "Source device and destination path",
                "Format and why: E01 (embedded verification) vs raw/dd vs AFF4, and segment size",
                "Sectors imaged and any read errors — errors are recorded, not hidden",
            ],
            "why": "This is the acquisition ISO/IEC 27037 means: a verifiable bit-stream copy. The reader has "
                   "to be able to repeat it on the same build and reach the same image, which is only possible "
                   "if the tool, version and settings are on the record.",
            "notes_ph": "Tool+version · source · destination · format + segment size · sectors · errors",
        },
        {
            "id": "s2-a5", "type": "active",
            "name": "Acquisition & verification hash",
            "cmd": "acquisition hash must equal verification hash",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">FTK Imager — verify results</span></div><div class="gui-body">'
                '<span class="l d">[Computed Hashes]</span>'
                '<span class="l">MD5      &lt;digest&gt;</span>'
                '<span class="l">SHA-256  &lt;digest&gt;</span>'
                '<span class="l d">[Verify Results]</span>'
                '<span class="l ok">Verify result: Match</span>'
                '</div></div>',
            "collect": [
                "Hash at acquisition, MD5 and SHA-256",
                "Hash re-computed at verification, and the result: match or mismatch",
                "The verification was of the image against the source, and it says so",
            ],
            "why": "The pair is the point: one hash proves nothing, two equal hashes prove the copy is faithful. "
                   "A mismatch is recorded and explained — an unexplained mismatch ends the evidential value of "
                   "the image.",
            "notes_ph": "Acquisition MD5 + SHA-256 · verification hash · match/mismatch",
        },
      ]}]),

    S("s3", "03", "Data Representation & File Examination",
      "Examination — file identification", "EVS-05 · EVS-06",
      [{"label": "B · Examination — files", "steps": [
        workingcopy_step("s3"),
        {
            "id": "s3-a1", "type": "active",
            "name": "File signature versus extension",
            "cmd": "header / magic bytes, not the name",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">header inspection</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> xxd -l 8 suspect.jpg</span>'
                '<span class="l">00000000: 504b 0304 1400 0600   PK......</span>'
                '<span class="l no">extension .jpg · header PK\\x03\\x04 = ZIP/OOXML — mismatch</span>'
                '</div></div>'
                '<div class="limitation"><span class="cl-label">Cannot prove</span>'
                '<p>A signature mismatch shows the name does not match the content. It does not show who '
                'renamed it, or when.</p></div>',
            "collect": [
                "Tool and version — HxD 2.5.0.0, TrID, ExifTool 13.59",
                "Each file: its extension, its header bytes, and the type they indicate",
                "Whether they agree, and the exact offset examined",
            ],
            "why": "A header survives a rename, which is what makes it worth more than the extension. Recording "
                   "the offset and bytes lets a second examiner reach the same conclusion without taking your "
                   "word for the file type.",
            "notes_ph": "Tool+version · per file: extension vs header bytes · match? · offset",
        },
        {
            "id": "s3-a2", "type": "active",
            "name": "Metadata & embedded content extraction",
            "cmd": "exiftool · OLE / OOXML structure",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">exiftool 13.59</span></div><div class="gui-body">'
                '<span class="l">Create Date      : &lt;timestamp&gt;</span>'
                '<span class="l">Modify Date      : &lt;timestamp&gt;</span>'
                '<span class="l">Author           : &lt;value&gt;</span>'
                '<span class="l d">macro storage present: vbaProject.bin</span>'
                '</div></div>',
            "collect": [
                "Tool and version, and the exact file examined with its path",
                "Metadata fields recovered, quoted as they appear",
                "Embedded objects or macro storage found, and where inside the file",
                "The time zone the timestamps are expressed in",
            ],
            "why": "Metadata is written by software, not by an oath — it is evidence of what a program recorded, "
                   "which is why the field is quoted rather than summarised. Embedded macro storage is a fact "
                   "about structure; what it did is interpretation.",
            "notes_ph": "Tool+version · file path · fields quoted · embedded objects · timezone",
        },
      ]}]),

    S("s4", "04", "Storage Devices, Partitions & File Systems",
      "Examination — file systems", "EVS-02 · EVS-04 · EVS-07",
      [{"label": "B · Examination — file systems", "steps": [
        workingcopy_step("s4"),
        {
            "id": "s4-a1", "type": "active",
            "name": "Partition structure recovered and proven",
            "cmd": "MBR / GPT · prove the recovery",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">partition table</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> mmls EVI-SRC01.E01</span>'
                '<span class="l">002:  000  0000002048  0000411647  NTFS / exFAT</span>'
                '<span class="l d"># wiped table? recovered with TestDisk 7.2 (stable, never 7.3-WIP)</span>'
                '<span class="l ok">recovery verified: volume mounts read-only, hash unchanged</span>'
                '</div></div>',
            "collect": [
                "Tool and version used to read or recover the table",
                "The partition layout found: scheme, offsets, sizes, types",
                "If recovered: what was damaged, what was restored, and how the recovery was verified",
                "That the image hash is unchanged after the work",
            ],
            "why": "Recovering a partition table is an assertion about the disk's original layout, so it needs "
                   "proof — a mounting volume and an unchanged image hash. Without them it is a claim, not a "
                   "finding.",
            "notes_ph": "Tool+version · scheme + offsets/sizes · what was recovered + how verified · image hash unchanged",
        },
        {
            "id": "s4-a2", "type": "active",
            "name": "File system parsed — $MFT and deleted entries",
            "cmd": "MFTECmd · Timeline Explorer",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">MFTECmd</span></div><div class="gui-body">'
                '<span class="l"><span class="p">&gt;</span> MFTECmd.exe -f $MFT --csv out\\</span>'
                '<span class="l ok">&lt;n&gt; records · &lt;n&gt; flagged not-in-use</span>'
                '<span class="l d"># resident vs non-resident · ADS · $LogFile / $UsnJrnl</span>'
                '</div></div>',
            "collect": [
                "Tool and version, input artifact and its full path in the image",
                "Records parsed, and how many are marked not in use",
                "For each artifact of interest: its MFT record number and timestamps",
                "Whether data is resident or non-resident, and any alternate data streams",
            ],
            "why": "The $MFT is the file system's own record, so citing a record number lets a second examiner "
                   "go straight to the same entry. Deletion in NTFS clears an in-use flag rather than the data — "
                   "which is why a “deleted” file can still be a finding.",
            "notes_ph": "Tool+version · artifact path · records parsed · MFT record # + timestamps · resident? ADS?",
        },
        {
            "id": "s4-a3", "type": "active",
            "name": "File carving",
            "cmd": "PhotoRec / foremost",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">carving</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> foremost -t all -i EVI-SRC01.dd -o carved/</span>'
                '<span class="l ok">&lt;n&gt; files carved · first at offset &lt;n&gt;</span>'
                '</div></div>'
                '<div class="limitation"><span class="cl-label">Cannot prove</span>'
                '<p>A carved file has no filename, no path and no file-system timestamps — carving recovers '
                'content, not context.</p></div>',
            "collect": [
                "Tool and version, and the image carved",
                "Files recovered, their types, and the byte offsets they came from",
                "Which carved items are complete and which are partial",
            ],
            "why": "Carving finds content by signature alone, so the offset is the only address it has. Recording "
                   "what carving cannot supply — name, path, timestamps — is what keeps the finding honest.",
            "notes_ph": "Tool+version · image · files carved + types · byte offsets · complete or partial",
        },
      ]}]),

    S("s5", "05", "Windows Forensics — Registry, User Activity & Execution",
      "Examination — Windows artifacts", "EVS-02 · EVS-04",
      [{"label": "B · Examination — Windows artifacts", "steps": [
        workingcopy_step("s5"),
        {
            "id": "s5-a1", "type": "active",
            "name": "Registry hives extracted from the image",
            "cmd": "RegRipper 3.0 · hives are files",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">hive extraction</span></div><div class="gui-body">'
                '<span class="l d"># hives are files on the image — never the live registry</span>'
                r'<span class="l">/Windows/System32/config/SYSTEM · SOFTWARE · SAM</span>'
                r'<span class="l">/Users/&lt;user&gt;/NTUSER.DAT</span>'
                '<span class="l ok">extracted · SHA-256 recorded per hive</span>'
                '</div></div>',
            "collect": [
                "Full path of each hive inside the image, and its hash once extracted",
                "Tool and version used to parse it (RegRipper 3.0 — 4.0 is declined on licence)",
                "That the live registry of the examination host was never used",
            ],
            "why": "A hive is a file, so it is extracted, hashed and parsed like any other artifact. Recording "
                   "its path in the image is what separates a finding about the evidence from a reading of your "
                   "own machine.",
            "notes_ph": "Hive paths in image · hash per hive · tool+version · live registry not used",
        },
        {
            "id": "s5-a2", "type": "active",
            "name": "USB & removable-media history",
            "cmd": "USBSTOR · MountedDevices · setupapi.dev.log",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">device history</span></div><div class="gui-body">'
                r'<span class="l">SYSTEM\CurrentControlSet\Enum\USBSTOR\&lt;device&gt;\&lt;serial&gt;</span>'
                '<span class="l">first connected: &lt;timestamp&gt; · last: &lt;timestamp&gt;</span>'
                r'<span class="l d">MountedDevices → volume GUID · setupapi.dev.log → first install</span>'
                '</div></div>'
                '<div class="limitation"><span class="cl-label">Cannot prove</span>'
                '<p>Device history shows a device was attached. It does not show who attached it, or that any '
                'file was copied to it.</p></div>',
            "collect": [
                "Full key path, the device serial, and the timestamps quoted as stored",
                "The volume GUID and drive letter it mapped to",
                "Which artifact each fact came from — they do not all say the same thing",
            ],
            "why": "This is the artifact family the whole case ends on, so the key path and serial have to be "
                   "exact. Attribution to a person is a separate question that needs a separate artifact — the "
                   "registry records devices and accounts, not people.",
            "notes_ph": "Key path · device + serial · first/last connected · volume GUID · source artifact per fact",
        },
        {
            "id": "s5-a3", "type": "active",
            "name": "Execution evidence",
            "cmd": "Prefetch · Amcache · ShimCache",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">evidence of execution</span></div><div class="gui-body">'
                r'<span class="l">/Windows/Prefetch/&lt;NAME&gt;-&lt;HASH&gt;.pf</span>'
                '<span class="l">run count &lt;n&gt; · first run &lt;ts&gt; · last run &lt;ts&gt;</span>'
                '<span class="l d">Amcache / ShimCache = presence, NOT proof of execution</span>'
                '</div></div>',
            "collect": [
                "Artifact path, tool and version, and the values as parsed",
                "Run count with first and last run times, where the artifact carries them",
                "Which artifact proves execution and which only proves presence",
            ],
            "why": "Prefetch evidences execution; ShimCache and Amcache evidence that a binary was present. "
                   "Writing one as the other is the classic misreading, and it is the difference between a "
                   "finding that survives and one that does not.",
            "notes_ph": "Artifact path · tool+version · run count + first/last · execution vs presence",
        },
      ]}]),

    S("s6", "06", "Network Forensics, Timelines, Reporting & Capstone",
      "Examination · Analysis · Presentation", "EVS-02 · EVS-03 · EVS-08",
      [{"label": "B · Examination — network & timeline", "steps": [
        workingcopy_step("s6"),
        {
            "id": "s6-a1", "type": "active",
            "name": "Packet capture examined",
            "cmd": "Wireshark 4.6.8 · display filters",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">pcap examination</span></div><div class="gui-body">'
                '<span class="l">capture SHA-256 &lt;digest&gt; — verified before opening</span>'
                '<span class="l"><span class="p">filter</span> ip.addr==&lt;host&gt; &amp;&amp; tcp.flags.syn==1</span>'
                '<span class="l">frame &lt;n&gt; · &lt;timestamp&gt; UTC · &lt;n&gt; bytes</span>'
                '</div></div>',
            "collect": [
                "Capture file, its hash, and that it was verified before examination",
                "Tool and version, and every display filter used verbatim",
                "Frame numbers and timestamps for each fact — the frame is the citation",
                "Any object exported, with its own hash",
            ],
            "why": "A display filter is the method; without it the reader cannot reproduce your view of the "
                   "capture. Frame numbers do for a pcap what an MFT record number does for a file system — "
                   "they make the finding checkable.",
            "notes_ph": "Capture + hash verified · tool+version · filters used · frame # + timestamps · exported objects",
        },
        {
            "id": "s6-a2", "type": "active",
            "name": "Super-timeline built",
            "cmd": "log2timeline.py → psort.py",
            "example":
                '<div class="gui"><div class="gui-bar"><span class="gui-dots"><i></i><i></i><i></i></span>'
                '<span class="gui-title">plaso</span></div><div class="gui-body">'
                '<span class="l"><span class="p">$</span> log2timeline.py --storage-file case.plaso EVI-SRC01.E01</span>'
                '<span class="l"><span class="p">$</span> psort.py -o l2tcsv -w timeline.csv case.plaso</span>'
                '<span class="l d">host timezone recorded · clock skew measured and stated</span>'
                '</div></div>',
            "collect": [
                "Tool versions and the exact commands run",
                "Sources ingested, and the filters applied to the output",
                "The host's time zone, how it was determined, and any measured clock skew",
                "The time basis every timestamp in your report is expressed in",
            ],
            "why": "A timeline merges artifacts whose clocks may disagree, so the time basis is part of the "
                   "finding, not a footnote. An unstated skew turns a correct sequence of events into a wrong one.",
            "notes_ph": "Tool versions + commands · sources + filters · host timezone · measured skew · time basis",
        },
        {
            "id": "s6-a3", "type": "active",
            "name": "Findings separated from interpretation",
            "cmd": "fact · then meaning · then what it cannot show",
            "example":
                '<div class="finding"><span class="cl-label">Finding</span>'
                '<p>Artifact at <code>&lt;path&gt;</code>, record <code>&lt;n&gt;</code>, '
                '<code>&lt;timestamp&gt;</code> UTC records &lt;the observed value&gt;.</p></div>'
                '<div class="interpretation"><span class="cl-label">Interpretation</span>'
                '<p>Assessed with moderate confidence to mean &lt;X&gt;, resting on F-01 and F-04. '
                'Alternative considered and not excluded: &lt;Y&gt;.</p></div>'
                '<div class="limitation"><span class="cl-label">Cannot prove</span>'
                '<p>&lt;What no artifact in this case shows&gt;.</p></div>',
            "collect": [
                "Each finding as one observable fact, tied to one named artifact and an exact location",
                "Each interpretation citing the finding numbers it rests on, with a stated confidence",
                "At least one alternative explanation, and why it was rejected or could not be excluded",
                "At least one honest “this evidence cannot show X”",
            ],
            "why": "SWGDE 18-Q-002 §5.5 requires an opinion to be documented with its basis. The separation is "
                   "criterion 4 of the report rubric and the habit the whole diploma is built on: if it needs "
                   "the word because, it is not a finding.",
            "notes_ph": "F-nn facts + artifact/location · I-nn with confidence + alternative · one cannot-prove",
        },
      ]}]),
]

# ------------------------------------------------ case-level blocks (once only)
CASE_BLOCKS = [
    {
        "id": "case-log",
        "label": "Custody-transfer log — the running chain",
        "hint": "One line per movement of the item, for the whole case — it grows across every session and is "
                "never cleared with a session. SWGDE 18-F-002 requires every transfer to identify each person "
                "taking possession by name and signature.",
        "placeholder":
            "date/time (UTC) · released by (sign) · received by (sign) · purpose · location · integrity (re-verified? match?)\n"
            "2026-03-04 09:02 UTC · Instructor ______ · <you> ______ · examination · Lab WS-01 · SHA-256 match\n"
            "____-__-__ __:__ UTC · ______ · ______ · … · … · …",
    },
    {
        "id": "case-disposition",
        "label": "Disposition of originals and derivative works",
        "hint": "What happened to the original item and to every working copy — retained, returned or destroyed, "
                "with the date and to whom. Required by SWGDE 18-Q-002 §5.6.",
        "placeholder":
            "Original    : retained / returned to <whom> / destroyed — <date>\n"
            "Working copy: retained in <location> / securely destroyed — <date>\n"
            "Derived exports (CSV, carved files, timeline): <where held>",
    },
]


# ---------------------------------------------------------------------- render
def esc(s):
    return html.escape(str(s), quote=True)


def render_step(step, current):
    active = ' data-active' if step["type"] == "active" else ''
    cur = ' data-current' if current else ''
    type_label = {"gate": "gate", "active": "active", "doc": "log"}[step["type"]]
    cmd = ('<code class="rec-cmd">%s</code>' % esc(step["cmd"])) if step.get("cmd") else ''
    collect = ''.join('<li>%s</li>' % esc(c) for c in step.get("collect", []))
    return (
        '<div class="rec-step" data-step="%s">'
        '<label class="rec-check"><input type="checkbox" data-check="%s"%s%s><span class="rec-box"></span></label>'
        '<div class="rec-main">'
        '<div class="rec-row"><span class="rec-name">%s</span><span class="rec-type %s">%s</span>%s'
        '<button class="rec-toggle" type="button" aria-expanded="false" aria-label="show example, record and why"></button></div>'
        '<div class="rec-detail">'
        '<div class="rec-eg"><div class="rec-lbl">Example</div>%s</div>'
        '<div class="rec-collect"><div class="rec-lbl">Record</div><ul>%s</ul></div>'
        '<div class="rec-why"><b>Why it matters &middot; admissibility:</b> %s</div>'
        '</div>'
        '<textarea class="rec-notes" data-notes="%s" placeholder="%s"></textarea>'
        '</div></div>'
    ) % (esc(step["id"]), esc(step["id"]), active, cur, esc(step["name"]), step["type"],
         esc(type_label), cmd, step["example"], collect, esc(step["why"]),
         esc(step["id"]), esc(step.get("notes_ph", "Record your entry…")))


def render_free(free):
    return ('<div class="rec-free"><span class="rec-free-label">%s</span>'
            '<p class="rec-free-hint">%s</p>'
            '<textarea data-notes="%s" placeholder="%s"></textarea></div>'
            % (esc(free["label"]), esc(free["hint"]), esc(free["id"]), esc(free["placeholder"])))


def render_group_inner(sess, current):
    parts = []
    for sec in sess["sections"]:
        parts.append('<h3 class="rec-sec">%s</h3>' % esc(sec["label"]))
        for step in sec["steps"]:
            parts.append(render_step(step, current))
    return '\n'.join(parts)


def render_current_group(sess):
    head = ('<div class="rec-group-head">Session %s &middot; %s '
            '<span class="rec-group-now">this session</span>'
            '<span class="rec-group-phase">%s</span></div>'
            % (esc(sess["num"]), esc(sess["title"]), esc(sess["phase"])))
    return ('<section class="rec-group current" data-group-title="Session %s — %s">%s\n%s</section>'
            % (esc(sess["num"]), esc(sess["title"]), head, render_group_inner(sess, True)))


def render_prior_group(sess):
    summ = ('<summary><span>Session %s &middot; %s</span>'
            '<span class="rec-group-carried">carried forward</span></summary>'
            % (esc(sess["num"]), esc(sess["title"])))
    return ('<details class="rec-group" data-group-title="Session %s — %s">%s\n%s</details>'
            % (esc(sess["num"]), esc(sess["title"]), summ, render_group_inner(sess, False)))


def render_case_header():
    groups = []
    for label, fields in CASE_HEADER:
        items = []
        for key, flabel, wide, ph in fields:
            items.append('<div class="%s"><label>%s</label>'
                         '<input data-field="%s" data-label="%s" placeholder="%s" autocomplete="off"></div>'
                         % ('rec-field wide' if wide else 'rec-field',
                            esc(flabel), esc(key), esc(flabel), esc(ph)))
        groups.append('<div class="rec-hgroup"><div class="rec-hgroup-t">%s</div>'
                      '<div class="rec-fields">%s</div></div>' % (esc(label), ''.join(items)))
    return ('<div class="rec-cardhead"><h2>Case header</h2>'
            '<p>Filled once. It prints atop the exported record and is shared across every session '
            'on this browser.</p>%s</div>' % ''.join(groups))


def total_checks(upto):
    return sum(len(sec["steps"]) for s in SESSIONS[:upto + 1] for sec in s["sections"])


def render_page(index):
    sess = SESSIONS[index]
    body = ''.join(render_prior_group(SESSIONS[i]) for i in range(index)) + render_current_group(sess)
    return PAGE.format(
        num=esc(sess["num"]), title=esc(sess["title"]), phase=esc(sess["phase"]),
        evidence=esc(sess["evidence"]), sid=esc(sess["id"]), gate=esc(sess["gate"]),
        total=total_checks(index), caseheader=render_case_header(), body=body,
        caseblocks='\n'.join(render_free(b) for b in CASE_BLOCKS),
        sesslink=session_link(sess["num"]),
    )


def session_link(num):
    """Teaching page if it is built, otherwise the brief (D48).

    session-NN/index.html is reserved for Phase 4; linking it before it exists
    puts a 404 on the live site.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    page = os.path.join(here, "..", "docs", "session-%s" % num, "index.html")
    return "index.html" if os.path.exists(page) else "brief.html"


PAGE = '''<!DOCTYPE html>
<!--
  record.html -- eCDFP Session {num} Chain-of-Custody Record.
  GENERATED by scripts/gen_session_record.py -- do not hand-edit; edit the data there.
  Structure follows SWGDE 18-Q-002 / 18-F-002 and ISO/IEC 27037.
-->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Session {num} — Chain-of-Custody Record · eCDFP · ITGate Academy</title>
<meta name="description" content="ITGate Academy eCDFP diploma — the cumulative Chain-of-Custody record maintained across the case. Structure follows SWGDE 18-Q-002, SWGDE 18-F-002 and ISO/IEC 27037.">
<link rel="stylesheet" href="../assets/css/ecdfp.css">
<link rel="icon" href="../assets/img/itgate-logo.jpg">
</head>
<body>

<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="hb" href="../index.html">
      <img src="../assets/img/itgate-logo.jpg" alt="ITGate Academy">
      <span class="hb-text">
        <span class="hb-name">ITGate Academy</span>
        <span class="hb-sub">eCDFP · Session {num} Record</span>
      </span>
    </a>
    <nav class="topnav">
      <a href="{sesslink}">Session {num}</a>
      <a href="../index.html#records">Case Records</a>
      <a href="../index.html">All sessions</a>
    </nav>
  </div>
</header>

<main class="wrap section">
  <div class="hub-main">
  <div class="rec" data-record="{sid}" data-record-title="eCDFP Session {num} — Chain-of-Custody Record" data-current="{sid}">

    <div class="rec-head">
      <div class="rec-eyebrow">eCDFP · Chain-of-Custody Record</div>
      <div class="rec-head-row">
        <h1>Chain-of-Custody Record</h1>
        <span class="rec-badge">Session {num}</span>
        <span class="rec-badge">{phase}</span>
      </div>
      <p class="rec-lede">One unbroken record for the case. Tick each step as you do it, open
        <em>example</em> for a correct entry, what to record and why it matters, then write your own entry.
        Saves in <strong>this browser</strong> and carries forward into later sessions.
        <strong>Export to HTML or PDF</strong> — the exported file is what you submit.</p>
      <div class="rec-note"><b>Standards.</b> Structure follows <b>SWGDE 18-Q-002</b> (report content),
        <b>SWGDE 18-F-002</b> (evidence collection and custody) and <b>ISO/IEC 27037</b> (identification,
        collection, acquisition, preservation). The governing rule: every action must be reconstructible by a
        qualified third party. Evidence IDs come from the case manifest ({evidence}); digests in examples are
        placeholders. The browser copy is a working copy — the exported file is the record of authority.</div>
    </div>

    {caseheader}

    <div class="rec-bar">
      <div class="rec-prog"><b data-progress>0 / {total} steps</b><span class="pbar"><span data-progress-bar></span></span></div>
      <div class="rec-actions">
        <span class="rec-saved" data-saved>saved ✓</span>
        <button class="rec-btn primary" type="button" data-export-html>⭳ Download HTML</button>
        <button class="rec-btn" type="button" data-export-pdf>\U0001f5a8 Save as PDF</button>
        <button class="rec-btn ghost" type="button" data-clear>Clear this session</button>
      </div>
    </div>

    <div class="rec-gate" data-gate="{gate}"><b>⚠ Authorization not signed.</b> An <b>active</b> step in this
      session is ticked, but its <b>authorization &amp; scope check</b> is not signed off. Confirm the authority
      and scope first — work done without documented authority can render the evidence, and everything derived
      from it, inadmissible.</div>

    <div data-record-body>
{body}
    </div>

    <div class="rec-case" data-case-blocks>
      <h3 class="rec-sec">Case record &middot; the whole case, not one session</h3>
{caseblocks}
    </div>

  </div>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <span>ITGate Academy · eCDFP Diploma · Chain-of-Custody Record</span>
    <span class="mono">SWGDE 18-Q-002 · 18-F-002 · ISO/IEC 27037</span>
  </div>
</footer>

<script src="../assets/js/record.js"></script>
</body>
</html>
'''


def main():
    args = sys.argv[1:]
    if args and args[0] == "--stdout":
        want = args[1] if len(args) > 1 else SESSIONS[0]["id"]
        for i, s in enumerate(SESSIONS):
            if s["id"] == want:
                sys.stdout.write(render_page(i))
                return
        sys.stderr.write("no such session: %s\n" % want)
        sys.exit(2)

    here = os.path.dirname(os.path.abspath(__file__))
    docs = os.path.normpath(os.path.join(here, "..", "docs"))
    for i, sess in enumerate(SESSIONS):
        out_dir = os.path.join(docs, "session-%s" % sess["num"])
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "record.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_page(i))
        print("wrote", out, "(%d steps cumulative)" % total_checks(i))


if __name__ == "__main__":
    main()
