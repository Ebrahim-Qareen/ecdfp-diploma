# FOR-WS01 tool install - session by session

Installer scripts for the eCDFP analyst workstation, grouped by the session that first needs each
tool (source of truth: `design/tools_by_session.md`). Every script was tested on the instructor's
FOR-WS01 and fixed until it runs clean, so a student can run them first-time on a fresh Windows 11.

## Run order (elevated PowerShell)
Right-click Windows PowerShell -> **Run as administrator**, then:
```
Set-ExecutionPolicy Bypass -Scope Process -Force
cd <this folder>
```

**Option A - one shot (recommended for students):**
```
.\install_all.ps1
```
Runs everything in order in a single session. Then do the one manual step (FTK Imager) and snapshot.

**Option B - session by session:**
```
.\00_bootstrap.ps1      # Chocolatey + Git + Python + 7-Zip + kit folders  (reopen shell after)
.\s2_acquisition.ps1    # OSFMount, Arsenal Image Mounter, Volatility 3   (+ FTK Imager = manual)
.\s3_files.ps1          # HxD, ExifTool, oletools, oledump, TrID, CyberChef
.\s4_storage.ps1        # Autopsy, TestDisk/PhotoRec 7.2, Sleuth Kit, EZ Tools (covers S5 too)
.\s5_windows.ps1        # RegRipper 3.0
.\s6_network.ps1        # Wireshark, NetworkMiner
.\06_symbols_airgap.ps1 # Volatility Windows symbol pack (for the offline student image)
.\create_shortcuts.ps1  # desktop shortcuts for the GUI tools
.\verify_tools.ps1      # PASS/MISSING checklist - expect 0 missing (after FTK)
```

## Every script is student-safe
Each one, on its own, checks: **elevated?**, **PATH refreshed** (so choco/git/python are visible even
in a reused shell), **Chocolatey present** (else "run bootstrap first"), and resolves the **real
Python** (dodging the Windows 11 Store alias). Run any of them twice - they are idempotent.

## S1 needs NO installers
S1 uses only built-in `Get-FileHash` + a text editor - that is the lesson (the most important session
needs no forensic software).

## Two platform decisions (2026-09)
- **plaso / log2timeline runs on Kali**, not Windows:  `sudo apt install -y plaso`.
- **FTK Imager 8.3 is a manual download** (Exterro form-gated) - cannot be scripted. No paid "Pro".

## Version binding & licence
Pinned to `tools_by_session.md`: FTK Imager 8.3, HxD 2.5.0.0, ExifTool 13.59.0, Arsenal Image Mounter
3.13.368, TestDisk/PhotoRec 7.2.0 stable (not 7.3-WIP), Wireshark 4.6.8, Volatility 3 2.28.2.
Licence-rejected and never installed: 010 Editor, **RegRipper 4.0**, Xiao Steganography.

## Fixes baked in (issues hit during the build)
- Chocolatey needs an **elevated** shell; a non-admin attempt leaves a broken partial - bootstrap self-heals it.
- Windows 11 **Store python alias** intercepts `python` - scripts call the real `C:\Python314\python.exe` and put it ahead on PATH.
- **Stale PATH** in a reused shell hides freshly-installed `git`/`choco` - every script refreshes PATH first.
- **TrID**: the win64 zip ships an installer - use `trid_w32.zip` (the classic `trid.exe`).
- **NetworkMiner 3.1** is a manual Netresec download (choco is stale at 2.5) - scripted with a fallback link.
- **EZ Tools** need the **.NET 9** runtime (installed with Arsenal Image Mounter in S2).
