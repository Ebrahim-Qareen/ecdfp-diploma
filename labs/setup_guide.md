# eCDFP Lab — Student Setup Guide

> **Living document.** Built step by step during the lab build. Simple English, copy-paste ready.
> No passwords, keys or IPs are ever recorded here — placeholders only (project rule **R8**).

---

## 1. The lab at a glance

Three machines. VMware Workstation, fully offline while handling evidence.
**Host requirement: ≥ 250 GB free disk, 16 GB+ RAM recommended.**

| VM | Role | OS | vCPU | RAM | Disk |
|---|---|---|---:|---:|---:|
| **FOR-WS01** | Analyst workstation — where all analysis happens | Windows 11 Enterprise (Eval) | 4 | 8 GB | 120 GB |
| **EVI-SRC01** | Victim — gets compromised, then imaged | Windows 10 | 2 | 4 GB | 60 GB |
| **Kali** | Linux analysis (dd/dc3dd, Sleuth Kit, plaso, tcpdump) | Kali Linux | 2 | 4 GB | 60 GB |

Snapshot lineage on FOR-WS01: **CLEAN-BASE → CLEAN-TOOLS → per-case working state.**

---

## 2. Build the analyst workstation (FOR-WS01)

### Step 1 — Download the Windows 11 ISO
- Microsoft Evaluation Center: <https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise>
- Choose **Windows 11 Enterprise → ISO – Enterprise (64-bit)**. Free, 90-day, rearmable. (~6 GB)

### Step 2 — Create the VM in VMware Workstation
1. **File → New Virtual Machine → Typical → Next**
2. Select **Installer disc image file (ISO)** → browse to the Win 11 ISO → **Next**
3. Guest OS **Microsoft Windows** → version **Windows 11 x64** → **Next**
4. Name it **`FOR-WS01`**, pick a location with free space → **Next**
5. Win 11 needs a TPM → VMware asks to **encrypt**: choose **"Only the files needed to support a TPM"**, set your own password → **Next**
6. Disk size **120 GB** → **Store as a single file** → **Next**
7. **Customize Hardware:** Memory **8192 MB**, Processors **4 cores**, Network **NAT** (isolated later)
8. **Finish** — do not power on yet.

<!-- STEPS CONTINUE — appended as we build -->

### Step 3 — Install Windows 11
1. Power on **FOR-WS01**. When you see *"Press any key to boot from CD/DVD"*, press a key.
2. Choose language / time / keyboard → **Next** → **Install now**.
3. Edition installs as **Windows 11 Enterprise Evaluation** — no product key needed.
4. Accept the licence → **Custom: Install Windows only** → select the 120 GB disk → **Next**. Wait through install + reboots.
5. In OOBE, choose your **region** and **keyboard**.
6. **Create a local (offline) account** — at the network screen press **Shift + F10**, type `start ms-cxh:localonly` and press **Enter**. The local-account form opens.
7. Username **`analyst`**; set a password *(recorded privately, never in this guide)*.
8. Turn **all privacy toggles OFF** → **Accept**.
9. You reach the Windows desktop.

> **Note:** the local-account trick (`ms-cxh:localonly`) is current for Windows 11 24H2/25H2. If Microsoft removes it, use the "no internet + offline account" path, or disconnect the VM network before OOBE.

> **Account note:** A local account is recommended for an offline forensics workstation (no cloud sync, no telemetry). A **Microsoft account also works** — if used, disable OneDrive sync and device encryption afterwards (covered in Step 4 hardening).

### Step 4 — Install VMware Tools
1. In VMware: top menu **VM → Install VMware Tools**. *(If greyed out, first detach the Windows ISO: VM → Settings → CD/DVD → uncheck "Connected".)*
2. In Windows: **File Explorer → This PC → DVD Drive (VMware Tools)** → run **`setup64.exe`**.
3. Choose **Typical** → **Install** → **Reboot** when prompted.
4. After reboot you get full-screen resolution and working copy/paste between host and VM.

### Step 5 — Windows Update & hardening
1. **Settings → Windows Update → Check for updates.** Install everything, reboot, and repeat until it says *"You're up to date."*
2. Harden the workstation (important for a forensics box):
   - **Device encryption OFF** — Settings → Privacy & security → Device encryption → **Off** (so the analyst disk is never BitLocker-locked).
   - **OneDrive** — unlink / stop sync, so evidence never syncs to the cloud.
   - **Power & sleep** — set screen and sleep to **Never** (imaging and timelines run for hours).
3. *(Optional)* After patching, **pause Windows Update** so the baseline stays stable across cohorts.

### Step 6 — Snapshot: CLEAN-BASE
1. **Shut down** the VM (clean, powered-off snapshot).
2. VMware → **VM → Snapshot → Take Snapshot**.
3. Name it **`CLEAN-BASE`**, description: *"Patched Windows 11, VMware Tools, hardened — no forensic tools yet."*
4. This is your restore point **before any tools touch the machine.**

### Step 7 — Install the forensic tools (session by session)
Tools are installed in the order the course introduces them (see `design/tools_by_session.md`). Scripts live in `scripts/install/`.

**7.0 — Bootstrap (prerequisites).** In an **elevated PowerShell** on FOR-WS01, run `scripts/install/00_bootstrap.ps1`:
- Installs **Chocolatey** (package manager) + **Git**, **Python 3**, **7-Zip**
- Creates `C:\Forensics\Tools` and `C:\Forensics\Cases`
- **Reopen PowerShell (as Admin) afterwards** so the new PATH is loaded.

**S1 needs no installers** — only built-in `Get-FileHash` and a text editor.

**7.1 — S2 Acquisition tools** (`scripts/install/s2_acquisition.ps1`, fresh elevated PowerShell):
- **OSFMount** + **Arsenal Image Mounter 3.13.368** via Chocolatey (image mounting).
- **Volatility 3 2.28.2** via pip (memory forensics); adds `vol` to PATH.
- **FTK Imager 8.3** — manual install (Exterro form-gated): <https://www.exterro.com/ftk-product-downloads>. Avoid the paid "Pro" build.
- `dd`/`dc3dd` imaging runs on **Kali**, not Windows.

**7.2 — S3 File examination** (`scripts/install/s3_files.ps1`):
- **HxD 2.5.0.0** + **ExifTool 13.59.0** via Chocolatey (CORE).
- **olevba** (`oletools`, pip) + **oledump.py** (Didier Stevens) - document macros.
- **TrID** (Win64 v2.48 + defs) - file-type identification -> `C:\Forensics\Tools\TrID`.
- **CyberChef** latest - offline standalone -> `C:\Forensics\Tools\CyberChef` (for the air-gapped room).
- `file` runs on Kali/Git Bash. **Xiao Steganography dropped** (no living vendor).

**7.3 - S4 Storage & file systems** (`scripts/install/s4_storage.ps1`):
- **Autopsy** (choco 4.23.0; target 4.23.1) - CORE, ~1 GB download.
- **TestDisk / PhotoRec 7.2.0 stable** via choco (NOT the 7.3-WIP beta).
- **The Sleuth Kit** CLI (mmls/fls/istat).
- **Eric Zimmerman tools** via `Get-ZimmermanTools.ps1` (.NET 9) -> `C:\Forensics\Tools\EZTools` - MFTECmd (S4) + Registry Explorer, PECmd, LECmd, AppCompatCacheParser, Timeline Explorer (S5).

**7.4 - S5 Windows forensics** (`scripts/install/s5_windows.ps1`):
- Most S5 tools already came with **EZ Tools** in S4 (Registry Explorer, AppCompatCacheParser, PECmd, LECmd, Timeline Explorer, RBCmd, ShellBags Explorer, EvtxECmd).
- Adds **RegRipper 3.0** (MIT) via `git clone` - ships compiled `rip.exe` + plugins. **3.0 only** - 4.0's licence bars paid-training use.

**7.5 - S6 Network forensics** (`scripts/install/s6_network.ps1`):
- **Wireshark 4.6.8** via Chocolatey (CORE, pinned). Npcap not needed to read pcaps.
- **NetworkMiner 3.1 Free** direct from Netresec -> `C:\Forensics\Tools\NetworkMiner` (choco stale at 2.5). Free edition can't parse PcapNG - teach in classic pcap.
- **Volatility 3** already installed in S2. **plaso** runs on **Kali** (`apt install plaso`). **Brim/Zui** = mention only.

**7.6 - FTK Imager 8.3 (manual, CORE).** Exterro form-gates it: <https://www.exterro.com/ftk-product-downloads> -> FTK Imager 8.3 -> run installer (Typical). Skip any paid "Pro" build.

**7.7 - Volatility symbols for air-gap** (`scripts/install/06_symbols_airgap.ps1`) - stages `windows.zip` into the Volatility symbols folder so memory analysis works offline (essential on the student image; optional on an online box).

### Step 8 - Verify + baseline manifest + CLEAN-TOOLS snapshot
1. Run `scripts/install/verify_tools.ps1` - every row must read **[PASS]** (FTK Imager included, once installed).
2. **Run `scripts/install/make_tools_manifest.ps1`** - writes `C:\Forensics\Tools\TOOLS.sha256`, the
   SHA-256 of every tool binary at this moment. **`P01`'s guided lab opens this file**, so the
   snapshot is not taken until it exists.
   *It proves a tool has not changed since this baseline. It does **not** prove the binary is what
   the vendor published - that distinction is taught in `T03`.*
3. Shut the VM down.
4. VMware -> **VM -> Snapshot -> Take Snapshot** -> name **`CLEAN-TOOLS`**, description *"Full analyst kit installed, verified and hashed - before any evidence."*
5. This is the known-good baseline the course rolls back to (S1-F6 snapshot lineage). **Kali:** `sudo apt install -y plaso` for the super-timeline work.

### Step 9 - Desktop shortcuts (optional QoL)
Run `scripts/install/create_shortcuts.ps1` (elevated) to drop double-click shortcuts on the **Public Desktop** for the GUI tools (Autopsy, FTK Imager, HxD, Wireshark, OSFMount, Arsenal Image Mounter, NetworkMiner, PhotoRec, Registry/Timeline/ShellBags/MFT Explorer, CyberChef) plus a **Forensic CLI** launcher and a **tools folder** shortcut for the command-line tools. Public Desktop = visible to every user, so it survives cloning to the student image. **Do this before the CLEAN-TOOLS snapshot** so the snapshot already has them.

---
*Build complete: FOR-WS01 analyst workstation, Windows 11 + full eCDFP tool set, session by session.*
