# P11 — What ran, what was touched · build log

**Topics** `T18` Evidence of Execution (40 min) · `T19` User Activity — Shellbags, Recycle Bin, VSS (38 min) — **78 minutes**
**Page** `docs/page-11/index.html` — 25 screens, 7 part dividers — shape v2 (`D136`)
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **6** — `F1` five questions / seven artifacts · `F2` inside a prefetch file · `F3` four artifacts, four events · `F4` a shellbag path key by key · `F5` the $I/$R pair · `F6` what a shadow copy is |
| SIMSCREEN | **1** — `ss-t18`, the instructor demo: PECmd + RegRipper + RBCmd across five artifacts |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | `EVS-13` — 10 published artifacts, Tier 2, 40 assertions |

## The spine of the page

Every artifact here is a **side effect** — Windows recording what happened for its own reasons, not for an
investigator. The page's whole discipline is one move: **each artifact supports exactly one verb, and you refuse
to upgrade it.** Started, was present, was launched, browsed, binned. "Used" and "ran" (on a ShimCache line) are
the two errors the page is built to prevent.

## Every number was read from the real files

**Prefetch (`libscca`):** `CMD.EXE-D269B812.pf` — **run count 55**, most recent **2016-01-12 20:07:03**, eight
start times kept, **62 files referenced** including `DISKPART.EXE` and `INIT.BAT`, two volumes with serials.
`CHROME.EXE` ran 20 times / 282 files; `CALC.EXE` 2 times / 63 files — the contrast is the student lab.

**ShimCache:** 350 entries; `PowerShell.exe` carries **2015-03-14 08:55:44**, which is the file's mtime, not a
run time — the page's central trap.

**UserAssist (EVS-12 NTUSER.DAT):** 578 entries; `mstsc.exe` 3 launches, `VisualStudio.12.0` 18 launches with
**43,392 seconds of focus**.

**ShellBags:** `UsrClass.dat` has 65 bag entries under a drive lettered **J:** — `woo`, `woo\bar`, browsed
**2014-11-07** — and **the drive is not in the evidence**. The deleted-bags hive has exactly **2 free nk cells**
(recoverable deleted keys), read by hand.

**LNK / JumpList / Recycle Bin:** the LNK targets `D:\Temp\osTriage2NonLE\...`, 4,412 B, drive serial
`0xDAFFD9CE`, tracker host `sagerez`. The jump list is Explorer's own, 9 entries, `C:\Temp` accessed twice. The
two `$I` records: `C:\temp` (14,155,310 B) and `C:\vss` (3,276,800 B), deleted **eight seconds apart** on
2018-08-07.

## Real tools, real output

`libscca`, `python-registry`, `regipy` (with `pyfwsi`/`pyfwps` for shellbags), `olefile`+`LnkParse3` for the jump
list, and **RegRipper 3.0 run on the real `UsrClass.dat`** — the shellbag SIMSCREEN block is character-for-character
its output. 40 assertions in `verify13.py`, all passing.

## Honesty about scope

Amcache and live Volume Shadow Copies are **taught here and run in `P14`** — both need a full disk image or a
running system, and `EVS-13` is loose artifact files. The page says so and points at the TryHackMe rooms. The
shellbag J: is **not** silently equated with `P10`'s ADATA J: — a letter is not a device, and the page makes that
its own caveat screen.

## Gates

```
python3 scripts/density_gate.py docs/page-11/index.html      ALL PASS
node testing/render_gate.js docs/page-11/index.html          PASS — zero findings
```

Eleven pages now pass both.
