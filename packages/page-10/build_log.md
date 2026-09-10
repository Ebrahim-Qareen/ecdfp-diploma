# P10 — The registry · build log

**Topics** `T16` Registry Structure & System Configuration (28 min) · `T17` USB & Device History (35 min) — **63 minutes**
**Page** `docs/page-10/index.html` — 27 screens, 7 part dividers — **the first page built in shape v2 (`D136`)**
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **4** — `F1` six files behind one tree · `F2` inside a hive file · `F3` the USB chain · `F4` four timestamps on a timeline |
| SIMSCREEN | **1** — `ss-t17`, the instructor demo: five RegRipper commands, **every output line verbatim** from `rip.pl` on the real hives |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | `EVS-12` — five published hives, Tier 2, pinned commit, 39 assertions |

## Shape v2, applied for the first time

Cover → Where we are **with a bridge paragraph from `P09`** → Objectives → PART 1 (what it is) → PART 2 (what the
system says about itself) → PART 3 (device history) → **INSTRUCTOR DEMO** → **YOUR TURN** (solo or team of two)
→ **CHEAT SHEET** → **TASK** (with grading, and the report stage) → Summary → References.

## Every number was read from the hives

The `regf` header by hand — sequence numbers **20610 / 20609** (one apart: not cleanly flushed), root cell at
**0x20** from the first bin, checksum **0xF76F4711** recomputed and matching. `ComputerName` **HAXOR4**,
Mountain Standard Time. `SOFTWARE`: Windows 7 Professional 7601, installed **2013-10-10**. `SAM`: two built-in
accounts, never logged in.

**The USB chain, for the ADATA drive:** serial `2361808400440061&0` → `VID_125F&PID_DE7A` → `J:` →
`{3aa3a4a9-087f-11e4-825d-ac220b2a5a56}` → the user's `MountPoints2`, last written **2014-10-14**.

**The finding the page turns on** was not planned — it was in the data. The device's "First InstallDate" is
**2015-02-23 17:31:31**, *seven months after* the user last mounted it and *eight months after* its volume GUID
was minted (UUIDv1 clock: **2014-07-10 22:12:06**). Ten seconds before that "first install", a Mushkin drive
recorded its last removal. Windows reinstalled the driver instance that day. **"First install" is the latest
of four dates, and the earliest date on the disk is inside a GUID nobody decodes.**

## Real tool, real output

RegRipper 3.0 was installed in the build environment (`libparse-win32registry-perl`) and run on the real hives.
The SIMSCREEN quotes `compname`, `timezone`, `usbstor`, `mountdev` and `mp2` **character for character**, so a
student who runs the same command sees the same text. One detail caught in the process: `mp2` prints the
timestamp on the line **above** the GUID, which reads as if it belonged to the previous entry until you know.

## Honesty about the corpus

`SYSTEM` and `NTUSER.DAT` share a machine (43 volume GUIDs in common). `SOFTWARE` and `SAM` do not — they are
from a clean VM. The page says so where it matters and turns it into a question the student should ask on every
case. The user hive is the author's own profile, published by him; only its device keys are shown.

## Gates

```
python3 scripts/density_gate.py docs/page-10/index.html      ALL PASS
node testing/render_gate.js docs/page-10/index.html          PASS — zero findings
```

Three tables were restructured to two columns before the render gate passed (`D129`'s rule, three more
times). Ten pages now pass both gates.
