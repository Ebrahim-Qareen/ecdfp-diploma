# Instructor Session 04 — Practical Windows Forensics, part 1

| | |
|---|---|
| **Deck** | `Resources/Instructor/session 4.pdf` — 39 slides, 30 screenshots |
| **INE material covered** | unit 6 — see [`Module_04_System_and_Network_Forensics.md`](../Module_04_System_and_Network_Forensics.md) |
| **Feeds eCDFP session** | `S5` |
| **Source text** | [`../_source_text/Instructor_Session_04_Practical_Windows_Forensics_part_1.md`](../_source_text/Instructor_Session_04_Practical_Windows_Forensics_part_1.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Roughly the first quarter is lecture (NTFS metadata files, `$MFT` record structure, the four
Windows evidence sources, a roadmap of the disk-analysis process), and everything from slide 11 to
the end is one continuous hands-on run. The lab half is itself in two blocks: a short tool-tour
block (ADS, TestDisk, PhotoRec, KAPE, MFTECmd — slides 11–18) and then a long, uninterrupted
registry investigation using Registry Explorer against the hives KAPE just collected (slides
19–36), closing with RegRipper automation (37–39). There is no challenge and no wrap-up slide; the
deck simply stops on the bulk-processing one-liner. The whole registry block is delivered as a
numbered walk — `#1` through `#15` — one key per slide, which makes it trivially convertible into
a guided lab but means almost no time is spent on interpretation.

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–2 | Title slides (no text recovered in the source extract) | admin |
| 3–4 | Session title; "digital evidence lifecycle — we are here" positioning slide | admin |
| 5–7 | NTFS metadata files (`$MFT`, `$LogFile`, `$Bitmap`, …) shown in WinHex; MFT record structure | concept |
| 8–9 | The four Windows evidence sources; the "PWF: Disk Analysis Process" roadmap | concept |
| 10 | Lab agenda for the session + cheat-sheet link | admin |
| 11–12 | Alternate Data Streams — concept then hands-on hide | concept · lab |
| 13–14 | TestDisk (repair partition structure) and PhotoRec (carve) | lab |
| 15 | KAPE triage collection | lab |
| 16–18 | `$MFT` parsing with MFTECmd; review in Excel; single-record dump | lab |
| 19–20 | Where the registry hives live; "black box of your Windows machine" | concept |
| 21–33 | Registry Explorer walk `#1`–`#12` — hive load, computer name, OS version, timezone, network, shutdown time, Defender, ProfileList, USBSTOR, Services, firewall rules, SAM users; plus a note on ProfileList semantics | lab |
| 34 | Timeline Explorer over the exported SAM user table (`#13`) | lab |
| 35–36 | Registry Explorer `#14`–`#15` — Uninstall key and App Paths | lab |
| 37–38 | RegRipper single-plugin runs (`timezone`, `del`) | lab |
| 39 | Bulk registry processing one-liner | lab |

## 2 · Labs and demos — what was actually run

### Lab 1 · Hiding data in an Alternate Data Stream · slides 11–12
**Tools:** `cmd.exe`, `notepad.exe`
**Evidence used:** a text file the instructor creates on the desktop of the live presenter
workstation. No prepared evidence set.
**Steps as demonstrated:**
1. Change to the desktop and create a normal file, then create a named stream on it. Prompt paths
   generalised — the slide shows the presenter's own account:
```
C:\Users\<user>>cd Desktop

C:\Users\<user>\Desktop>notepad file.txt

C:\Users\<user>\Desktop>notepad file.txt:secret
```
`⚠ OCR — verify before use` (only the account name has been replaced; the commands are as printed).
2. **What the output showed:** nothing beyond the three prompt lines. The slide is a command-prompt
   screenshot only — the two Notepad windows, the hidden content and the fact that `dir` and
   Explorer both show one file are demonstrated visually and are not on the slide.
**Gap:** the deck never shows the *detection* half — no `dir /r`, no `streams.exe`, no
`Get-Item -Stream *`. A guided lab must supply it.
**What this lab teaches:** NTFS supports named data streams, and `file:stream` content is invisible
to Explorer, to `dir` without `/r`, and to file-size accounting.

### Lab 2 · Repairing a partition structure with TestDisk · slide 13
**Tools:** TestDisk 7.3-WIP (September 2024), `testdisk_win.exe`
**Evidence used:** `\\.\PhysicalDrive2` — 157 MB / 150 MiB, described in the TestDisk banner as
`Arsenal Virtual` (i.e. a small image attached with Arsenal Image Mounter, not physical media),
`CHS 19 255 63 - sector size=512`.
**Steps as demonstrated:**
1. Launch the tool from the course tools folder (window title shows the presenter's own path — use
   `<tools>\testdisk-7.3-WIP\testdisk_win.exe`).
2. The disk menu is on screen with the cursor on the first option:
```
Analyse current partition structure and search for lost partitions
[ Advanced  ]  Filesystem Utils
[ Geometry  ]  Change disk geometry
[ Options   ]  Modify options
[ MBR Code  ]  Write TestDisk MBR code to first sector
[ Delete    ]  Delete all data in the partition table
[ Quit      ]  Return to disk selection
```
`⚠ OCR — verify`
3. **What the output showed:** only this menu screen. Everything past it — Quick Search, the
   recovered partition list, `Write` — is **demonstrated visually and the keystrokes must be
   recovered from the slide or the recording**. The deck contains no TestDisk result screen.
**What this lab teaches:** partition-table damage is recoverable, and TestDisk works against a
mounted image as readily as against a disk — which is what makes it usable on evidence.

### Lab 3 · Carving deleted data with PhotoRec · slide 14
**Tools:** PhotoRec 7.3-WIP (September 2024), `photorec_win.exe`
**Evidence used:** the same attached image, this time opened read-only —
`Disk \\.\PhysicalDrive2 - 157 MB / 150 MiB (RO) - Arsenal Virtual`.
**Steps as demonstrated:**
1. Launch `photorec_win.exe`; the partition-selection screen is shown:
```
Partition                  Start        End    Size in sectors
 No partition      0  6 1   19 33 13     307327 [Whole disk]
>1 * HPFS - NTFS   0  2 3   19 33 13     307199
[Options ] [File Opt] [ Quit ]
Start file recovery
```
`⚠ OCR — verify` (the CHS triples are the least reliable characters on the slide).
2. **What the output showed:** the selection screen only. No destination prompt, no recovery
   summary, no recovered-file listing. The rest is visual.
**Worth teaching from the slide:** the `(RO)` marker — PhotoRec has opened the source read-only,
which is the integrity behaviour the course requires. The deck does not call this out.
**What this lab teaches:** signature-based carving recovers content without file-system metadata,
and therefore without original names, paths or timestamps.

### Lab 4 · KAPE triage collection · slides 15
**Tools:** KAPE 1.3.0.2 (`gkape` GUI front end), by Eric Zimmerman / Kroll
**Evidence used:** the live `C:` of the presenter workstation (`Target source [C:`).
**Steps as demonstrated:**
1. Set target source, target destination, tick flush, select the `KapeTriage` compound target, run.
   The GUI's "Current command line" box reads:
```
.\kape.exe --tsource C: --tdest "D:\kape image" --tflush --target KapeTriage --gui
```
   and the log pane echoes the same without quoting:
```
--tsource C: --tdest D:\kape image --tflush --target KapeTriage --gui
```
`⚠ OCR — verify`. For course use substitute a placeholder destination:
`--tdest "<case>\kape image"`.
2. **What the output showed:** `Targets available: 318`, `Targets selected: 1`,
   `Modules available: 414`, `Modules selected:` (blank — no modules run), `Process VSCs`
   unticked, `Deduplicate` ticked, container `None / VHDX / VHD / Zip` with none chosen,
   `Retain local copies` unticked. The `KapeTriage` target is described as
   `Compound  KapeTriage collects most o…` (truncated).
**Caution:** `--tflush` **empties the destination directory before collecting**. The deck does not
warn about this and it is a genuine evidence-destruction risk in a classroom.
**What this lab teaches:** targeted triage collection. Everything from slide 16 onward reads out of
this output tree — `<dest>\C\Windows\System32\config\…` — so this is the pivot of the whole session.

### Lab 5 · Parsing `$MFT` with MFTECmd · slides 16–18
**Tools:** MFTECmd v1.2.2.1 (Eric Zimmerman); Excel for review
**Evidence used:** the `$MFT` extracted by the KAPE run — reported as `File size: 712MB`.
**Steps as demonstrated:**
1. Create an output directory and parse the whole `$MFT` to CSV:
```
mkdir output

MFTECmd.exe -f $MFT --csv output --csvf parsed_mft.csv
```
`⚠ OCR — verify`
   **What the output showed:**
```
MFTECmd version 1.2.2.1
Command line: -f $MFT --csv output --csvf parsed_mft.csv
Warning: Administrator privileges not found!
File type: Mft
Processed $MFT in  seconds
$MFT: FILE records found: (Free records: ) File size: 712MB
CSV output will be saved to output\parsed_mft.csv
```
   The record counts and the elapsed time render blank in the OCR (the terminal colours them) —
   **do not quote counts from this slide.** The `Warning: Administrator privileges not found!` line
   is worth showing students: MFTECmd still parsed the extracted file fine, because the input was a
   KAPE-collected copy rather than a live volume.
2. Review the CSV in Excel (slide 17). Visible columns:
   `EntryNumber | SequenceNumber | InUse | ParentEntryNumber | ParentSequenceNumber | ParentPath | FileName`.
   The rows on screen are around entry `645515`+, all `InUse = FALSE`, with `ParentPath` values of
   the form `.\Users\<user>\AppData\Local\Microsoft\Edge\User Da…` and
   `.\PathUnknown\Directory with ID 0x000085FC-00000005`. Two teaching points sit in that screen
   and are not verbalised on the slide: `InUse = FALSE` rows are **deleted** records still resident
   in the table, and `.\PathUnknown\…` means the parent directory record could not be resolved.
3. Dump one record in full (slide 18):
```
MFTECmd.exe -f $MFT --de 92530
```
`⚠ OCR — verify`
   **What the output showed:**
```
Command line: -f $MFT --de 92530
File type: Mft
Dumping details for file record with key 00016972-0000000A
Entry-seq #: 0x16972-0xB, Offset: 0x5A5C800, Flags: IsFree, Log seq #: 0x2FE750C84, Base Record entry-seq: 0x0-0x0
Reference count: 0x1, FixUp Data Expected: 2B-00, FixUp Data Actual: 00-00 | 00-00 (FixUp OK: True)
**** STANDARD INFO ****
Attribute #: 0x0, Size: 0x60, Content size: 0x48, Name size: 0x0, ContentOffset 0x18. Resident: True
Flags: Archive, Max Version: 0x0, Flags 2: 512, Class Id: 0x0, Owner Id: 0x0, Security Id: 0x831, Quota charged: 0x0,
Update sequence #: 0xAD5E1D70
Created On:         2024-11-17 11:11:02.1050043
Modified On:        2024-11-17 11:11:02.1050043
Record Modified On: 2024-11-19 19:35:22.1750502
```
`⚠ OCR — verify`. The record key is OCR'd as `90016972-0000000A` and the FixUp actual bytes as
`00-00 | 90-00`; in both cases a leading `0` has been read as `9`. **As printed:** `90016972`.
**Likely intended:** `00016972`.
   Two things worth building a lab step on: `0x16972 = 92530` decimal, so the echoed entry number
   confirms the `--de` argument was interpreted as decimal; and `Flags: IsFree` means this is a
   deleted record whose `$STANDARD_INFORMATION` timestamps are still intact.
**What this lab teaches:** `$MFT` gives a whole-volume file inventory including free (deleted)
records, and `--de` drops to a single record's attributes for hand verification of anything the CSV
suggests.

### Lab 6 · Manual registry analysis with Registry Explorer · slides 19–36
This is the spine of the session — fifteen numbered steps, one key per slide.
**Tools:** Registry Explorer v2.0.0.0 (Eric Zimmerman); Timeline Explorer v2.0.0.1 at step 13
**Evidence used:** the five system hives from the KAPE output, loaded together —
`<kape-dest>\C\Windows\System32\config\` → `DEFAULT`, `SAM`, `SECURITY`, `SOFTWARE`, `SYSTEM`.
Registry Explorer reports `Registry hives (5)` and `Available bookmarks (76/0)`.
**Steps as demonstrated:**

1. **Locate and load the hives** (slides 19, 21). The deck lists the locations as:
```
C:Windows\System32\config
   DEFAULT, SECUIRTY, SYSTEM, SAM, SOFTWARE
C:Users\{user}
   NTUSER.DAT
C: Users\<user>\AppData\Local\Microsoft\Windows
   USRCLASS.DAT
```
   Quoted as printed except the account name. Note the defects: two missing backslashes after
   `C:`, `SECUIRTY` for `SECURITY`, a space in `C: Users`, and `BCD` absent from the hive list.
   **What the load showed:** per-hive counts of `Associated deleted records`,
   `Unassociated deleted records` and `Unassociated deleted values` — including `5,958` and
   `30,680` unassociated deleted values on two of the hives. This is the single best thing on the
   slide and the deck does not mention it: Registry Explorer recovers deleted registry data that
   `regedit` cannot show.

2. **Computer name** (slide 22, `#2`), as printed on the slide:
```
HKLM\System\CurrentControlSet\Control\Computer name\
```
   **Likely intended:** `HKLM\SYSTEM\ControlSet00#\Control\ComputerName\ComputerName` — the status
   bar of the screenshot confirms the real path,
   `ControlSet001\Control\ComputerName\ComputerName`, and shows two values,
   `ActiveComputerName` and `ComputerName`, both `RegSz`. Value redacted here; the slide shows the
   presenter's own hostname together with its raw UTF-16LE bytes.

3. **Windows version** (slide 23, `#3`), as printed:
```
HKLM\Software\Microsoft\Windows NT\Currentver sion\
```
   (`Currentver sion` is a PDF line-break artefact for `CurrentVersion`.)
   **What the output showed:** `SystemRoot C:\Windows`, `CurrentBuild 22631`,
   `CurrentBuildNumber 22631`, `CurrentMajorVersionNumber 10`, `CurrentMinorVersionNumber 0`,
   `CurrentVersion 6.3`, `DisplayVersion 23H2`, `EditionID Core`, `ProductName Windows 10 Home`,
   `ReleaseId 2009`, `InstallationType Client`, `InstallDate 1728274675` (REG_DWORD, Unix 32-bit),
   `UBR 4460`, `BuildLab`/`BuildLabEx` `22621…amd64fre.ni_release…`, `InstallationType Client`,
   plus `ProductId` and `DigitalProductId`.
   **Teaching point the deck misses:** build `22631` with `DisplayVersion 23H2` is **Windows 11**,
   yet `ProductName` reads `Windows 10 Home`. `ProductName` is not a reliable OS identifier on
   Win10/11 — read `CurrentBuild` + `DisplayVersion`. Also `CurrentVersion 6.3` is a frozen
   Windows-8.1-era value. Both are exactly the kind of trap the exam likes.

4. **Timezone** (slide 24, `#4`). **No key path is given on the slide.** The screenshot is cropped
   to two decoded values:
```
DaylightBias    60          4294967236
DaylightStart   Month 4, week of month 5, day of week 4, Hours:Minutes:Seconds:Milliseconds
                00-00-04-00-05-00-17-00-38-00-38-00-E7-03-04-00
```
`⚠ OCR — verify`. The path only appears later, in the RegRipper output on slide 37:
`ControlSet001\Control\TimeZoneInformation`. See
[TimeZoneInformation](../Module_04_System_and_Network_Forensics.md#timezoneinformation).

5. **Network configuration** (slide 25, `#5`). No path on the slide; the tree shows
   `…\Services\Tcpip\Parameters\Interfaces\{GUID}` with eight interface GUIDs.
   **What the output showed** for the selected interface:
   `EnableDHCP 1`, `DhcpIPAddress 192.168.238.1`, `DhcpSubnetMask 255.255.255.0`,
   `DhcpServer 192.168.238.254`, `Lease 1800`, `LeaseObtainedTime 1732094543`, `T1 1732095443`,
   `T2 1732096118`, `LeaseTerminatesTime 1732096343` (all REG_DWORD Unix times), `AddressType 0`,
   `IsServerNapAware 0`, `DhcpConnForceBroadcastFlag 0`,
   `DhcpSubnetMaskOpt 255.255.255.0` (REG_MULTI_SZ), `DhcpInterfaceOptions` (REG_BINARY).
   This is a VMware host-only adapter, not the workstation's real LAN — worth saying aloud, because
   the eight GUIDs are exactly the "extra networks" false positive the module warns about.

6. **Shutdown time** (slide 26, `#6`), as printed:
```
HKLM\System\ CurrentControlSet \Control\Win dows\ShutdownTime
```
   (spaces are PDF line-break artefacts). **Likely intended:**
   `HKLM\SYSTEM\ControlSet00#\Control\Windows\ShutdownTime`.
   **What the output showed:** `ShutdownTime  RegBinary  2C-8E-86-5A-50-36-…` — an unconverted
   FILETIME. The deck does **not** decode it on screen; a lab needs to add the decode step and the
   caveat that this is the last *graceful* shutdown only.

7. **Windows Defender settings** (slide 27, `#7`):
```
HKLM\Software\Microsoft\Windows Defender\
```
   **What the output showed:** `DisableAntiSpyware 0`, `DisableAntiVirus 0`, `PUAProtection 0`,
   `ProductStatus 0`, `SmartLockerMode 0`, `ManagedDefenderProductType 0`, `IsServiceRunning`,
   `InstallTime` and `OEMInstallTime` (REG_BINARY FILETIMEs), `InstallLocation`,
   `ProductAppDataPath`, `BackupLocation`, `RemediationExe windowsdefender://`,
   `SecLearningModeSwitch 1`, `VerifiedAndReputableTrustModeEnabled 0`, `HybridModeEnabled 0`.
   The two `Disable*` values at `0` are the investigative point (AV was not switched off) but the
   deck states no such finding.

8. **User profiles** (slide 28, `#8`), as printed:
```
HKLM\Software\Microsoft\Windows NT\Current er sion\ProfileList\SID
```
   **Likely intended:** `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>`.
   **What the output showed:** four `S-1-5-…` rows with last-write times and `ProfileImagePath`
   values; the interactive account is `S-1-5-21-<machine-id>-1001` →
   `C:\Users\<user>`, last write `2024-11-20 07:21:21`. RID `1001` for the first
   locally created interactive account is worth naming — the deck does not.

9. **Connected USB devices** (slide 29, `#9`):
```
HKLM\SYSTEM\ControlSet001\Enum\USBSTOR
```
   **What the output showed:** `Total rows: 18`, each row giving the key last-write time, the
   `Ven_ / Prod_ / Rev_` device string, the instance ID (serial), a friendly name, a container GUID
   and four separate timestamps. Device families present: `Ven_Kingston&Prod_DataTraveler_3.0`
   with several `Rev_` values (`PMAP`, `0000`, blank), `Ven_SanDisk&Prod_Cruzer_Force&Rev_1.00`,
   `Ven_Seagate&Prod_Backup+_BL&Rev_0419`, `Ven_WD&Prod_My_Passport_262&Rev_4010` plus a matching
   `Ven_WD&Prod_SES_Device`, `Ven_VendorCo&Prod_ProductCode&Rev_2.00`,
   `Ven_NAND&Prod_USB2DISK&Rev_0.00`, `Ven_ATA&Prod_ST1000LM035-1RK1&Rev_ACM4`,
   `Ven_wj&Prod_UDisk&Rev_5.00`. **Serial numbers are redacted here** — they are the presenter's
   own drives. Two structural facts worth teaching from this screen and absent from the slide: a
   second character of `&` in the instance ID means the serial was *not* supplied by the device,
   and the `Ven_ATA…ST1000LM035` row is an internal SATA disk seen through a USB bridge, not a
   thumb drive. See [USBSTOR](../Module_04_System_and_Network_Forensics.md#usbstor).

10. **Services** (slide 30, `#10`):
```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services
```
    **What the output showed:** `Total rows: 787`, columns
    `Name | Description | Display Name | Start Mode | Type | Key Last Write | Parameters Key Last Write | Group | Image Path | Service DLL | Required Privileges`.
    Registry Explorer is decoding `Start` into `Boot / Manual / Disabled` and resolving
    `@%SystemRoot%\system32\<dll>,-NNN` indirect strings. The deck reads the list but does not
    show a filter or a triage question, so a lab must supply one (e.g. `Start = Auto` **and**
    `Image Path` outside `System32`).

11. **Firewall rules** (slide 31, `#11`). **No key path on the slide**; the tree shows
    `FirewallPolicy` with children `DomainProfile`, `DynamicKeywords`, `FirewallRules`,
    `HypervFirewallPolicy`, `HypervVMCreators`, `Mdm`, `PublicProfile`, `RestrictedInterfaces`,
    `RestrictedServices`, `StandardProfile`, `TenantRestrictions`.
    **What the output showed:** `Total rows: 534`, and — the most useful single artefact on the
    slide — one rule's full pipe-delimited value in the Type viewer:
```
v2.32|Action=Allow|Active=TRUE|Dir=Out|Profile=Public|App=%SystemRoot%\system32\spoolsv.exe|Svc=Spooler|Name=@FirewallAPI.dll,-36858|Desc=@FirewallAPI.dll,-36859|EmbedCtxt=@FirewallAPI.dll,-36851|
```
`⚠ OCR — verify` (the trailing `|TK2_22=WFDPrint]` fragment is unreliable). Teaching the
    `Action / Active / Dir / Profile / App / Svc` field grammar is what makes an attacker-added
    allow rule findable; the deck shows the string but does not decompose it.

12. **Local accounts** (slide 32, `#12`). No path shown; the tree shows the `SAM` hive with
    `Aliases` and `Users`. Registry Explorer's `User accounts` bookmark is what is on screen.
    **What the output showed:** `Total rows: 5` — `Administrator` (Administrators, built-in,
    disabled), `Guest` (Guests, built-in), `DefaultAccount` (System Managed Accounts),
    `WDAGUtilityAccount`, and the interactive account (Administrators). Columns include
    created/last-login/last-password-change/last-incorrect-password/expires plus flags.
    Slide 33 adds the delivered claim: *"A user is added to profilelists if it have been already
    logged using GUI before."* — i.e. SAM lists every account, ProfileList only those that have
    interactively logged on. That pairing is the actual lesson of steps 8 and 12 and is worth
    keeping verbatim (corrected) in the rebuild.

13. **Export to Timeline Explorer** (slide 34, `#13`). The SAM user table is exported from Registry
    Explorer and reopened in Timeline Explorer v2.0.0.1. The export filename is visible and encodes
    the convention: `User accounts_Values_Export_<yyyyMMddHHmmss>.xlsx`.
    **What the output showed:** the same five accounts with `Created On`, `Last Login Time`,
    `Last Password Change`, `Last Incorrect Password`, `Expires On`, `User Name`, `Full Name`,
    `Password Hint`, `Groups`. `WDAGUtilityAccount` carries a `Last Login Time` of
    `2024-10-07 04:14:22`. No filtering or grouping is demonstrated — Timeline Explorer is used
    purely as a viewer here.

14. **Installed and uninstalled software** (slide 35, `#14`). No path on the slide; the tree shows
    `…\CurrentVersion\Uninstall` (and the presence of both `Run` and `RunOnce` beside it).
    **What the output showed:** per-entry key last-write time, display name, version, publisher,
    an `InstallDate` in `yyyyMMdd` form, install location and the full `UninstallString`. Entries
    on screen include `Advanced SystemCare`, `Driver Booster 12`, `Microsoft Edge 131.0.2903.51`,
    `Microsoft Edge Update 1.3.195.35`, `Microsoft Edge WebView2 130.0.2849.80`,
    `Npcap 1.73 (Nmap Project)`, `Office 15 PROPLUS`, `OpenAL`, `VLC media player 3.0.21`, `WIC`.
    The `2022-05-07 05:27:59` cluster of OS-bundled entries versus the 2024 cluster of
    user-installed ones is a readable install timeline and the deck does not point at it.

15. **App Paths** (slide 36, `#15`):
```
SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths
```
    **What the output showed:** key last-write time, executable name, the registered command and
    the `Path` value. Entries include `EXCEL.EXE`, `GROOVE.EXE`, `IEXPLORE.EXE`, `IEDIAG.EXE`,
    `infopath.exe`, `licensemanagershellext.exe`, `Lync.exe`, `wmplayer.exe`, `MSACCESS.EXE`,
    `msedge.exe`, `msoxmled.exe`, `MSPUB.EXE`, `OneNote`, `OUTLOOK.EXE`, `powerpnt.exe`,
    `Powershell.exe`, `Python.exe → C:\Python27\Python.exe`, `recuva.exe`. The forensic value —
    that `App Paths` lets a name typed in Run resolve to an arbitrary binary, and that a
    non-Microsoft entry here is worth a second look — is not stated.

**What this lab teaches:** offline hive analysis end to end — load the collected hives, read system
identity, time base, network, device history, accounts and installed software out of them, and
export any table for review. It is a competent tour; it is not yet an investigation, because no
question is being answered and no finding is written down.

### Lab 7 · Automated registry analysis with RegRipper · slides 37–39
**Tools:** RegRipper 3.0 (`rip.exe`), plugin-driven
**Evidence used:** hives copied to a working folder — the slide shows `registries/SYSTEM` relative
to the RegRipper directory.
**Steps as demonstrated:**
1. Run a single plugin against one hive:
```
rip.exe -r registries/SYSTEM —p timezone
```
   **As printed** (with an em dash, and a forward slash in the path). **Likely intended:**
   `rip.exe -r registries/SYSTEM -p timezone`. `⚠ OCR — verify`
   **What the output showed:**
```
Launching timezone v.20200518
timezone v.20200518
(System) Get TimeZoneInformation key contents

TimeZoneInformation key
ControlSet001\Control\TimeZoneInformation
LastWrite Time 202U-19-31 21:09:53Z
  DaylightName   -> @tzres.dll,-341
  StandardName   -> @tzres.dll,-342
  Bias           -> -120 (-2 hours)
  ActiveTimeBias -> -120 (-2 hours)
  TimeZoneKeyName-> Egypt Standard Time
```
`⚠ OCR — verify`. **The `LastWrite Time` is unusable** — `202U-19-31` has no valid month; do not
   quote it. Everything else is consistent: `Bias -120` = UTC+2, matching `Egypt Standard Time`.
   Note the contrast with step 4 of Lab 6: RegRipper prints the raw indirect string
   `@tzres.dll,-342` where Registry Explorer resolves it — a good side-by-side for students on why
   two tools disagree without either being wrong.
2. Run the deleted-data plugin:
```
rip.exe -r registries/SYSTEM -p del
```
   **What the output showed:**
```
Launching del v.20200515
del v.20200515
(ALL) Parse hive, print deleted keys/values
------------- Deleted Data ------------
…hex dump…
Value Name: Silo
   Data Length: 0x8   Data Offset: 0x3c0570  Data Type: REG_SZ
Value Name: AllowedProcessName
   Data Length: 0xc8  Data Offset: 0x7d6890  Data Type: REG_SZ
Value Name: DeviceNameTdt
   Data Length: 0x29  Data Offset: 0x7d6988  Data Type: REG_SZ
Key name: Parameters
Key LastWrite time = 2024-11-20 08:00:57Z
   Offset to parent: 0x3c0510
Key name: Wdf
Key LastWrite time = 2024-11-19 10:51:4?Z
```
`⚠ OCR — verify` — the OCR renders `Key` as `Hey` throughout and the last timestamp's seconds are
   unreadable (`10:51:MUZ`). This output is the automated counterpart to the "unassociated deleted
   values" counts seen in Lab 6 step 1; pairing them is the strongest single teaching moment
   available from this deck.
3. Process every hive in a folder in one pass (slide 39, from the slide text layer — **not** OCR,
   so this one is exact):
```
for /r %i in (*) do (rip.exe -r %i -a > %i.txt)
```
   `-a` runs all plugins rather than a named one. Note `%i` (single percent) is correct at an
   interactive prompt; inside a `.bat` file it must be `%%i`. The deck does not say so, and
   session 5 slide 12 confirms it was run interactively.
**What this lab teaches:** the automation counterweight to Lab 6 — one plugin when you have a
question, `-a` over everything when you do not yet know what the question is.

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| NTFS metadata files | `$MFT` (0), `$MFTMirr` (1), `$LogFile` (2), `$Volume` (3), `$AttrDef` (4), `.` (5), `$Bitmap` (6), `$Boot` (7), `$BadClus` (8), `$Secure` (9), `$UpCase` (10), `$Extend` (11), 12–15 reserved | Per-file record table, mirror, journal, volume info, attribute definitions, root dir, free-cluster map, boot sector, bad clusters, security descriptors, case table, extensions | [`Module_03_Disks_and_File_Systems.md`](../Module_03_Disks_and_File_Systems.md) |
| System hives | `C:Windows\System32\config` → `DEFAULT, SECUIRTY, SYSTEM, SAM, SOFTWARE` *(as printed — two typos)* | "where Windows registry is located" | [Registry hive files](../Module_04_System_and_Network_Forensics.md#registry-hive-files) |
| Per-user hive | `C:Users\{user}` → `NTUSER.DAT` | per-user registry | [Registry hive files](../Module_04_System_and_Network_Forensics.md#registry-hive-files) |
| Per-user class hive | `C: Users\<user>\AppData\Local\Microsoft\Windows` → `USRCLASS.DAT` | per-user class registrations | [Registry hive files](../Module_04_System_and_Network_Forensics.md#registry-hive-files) |
| Computer name | `HKLM\System\CurrentControlSet\Control\Computer name\` *(as printed)* | identify the host | [System identity and lifecycle keys](../Module_04_System_and_Network_Forensics.md#system-identity-and-lifecycle-keys-computer-name-product-shutdown) |
| OS version | `HKLM\Software\Microsoft\Windows NT\Currentver sion\` *(as printed)* | build, edition, install date | [System identity and lifecycle keys](../Module_04_System_and_Network_Forensics.md#system-identity-and-lifecycle-keys-computer-name-product-shutdown) |
| Timezone | *(not on the slide)* — `ControlSet001\Control\TimeZoneInformation` from the RegRipper output, slide 37 | time base for the whole timeline | [TimeZoneInformation](../Module_04_System_and_Network_Forensics.md#timezoneinformation) |
| Network interfaces | *(not on the slide)* — tree shows `…\Services\Tcpip\Parameters\Interfaces\{GUID}` | "network infrastructure": DHCP address, server, lease times | [Network configuration and network history keys](../Module_04_System_and_Network_Forensics.md#network-configuration-and-network-history-keys) |
| Shutdown time | `HKLM\System\ CurrentControlSet \Control\Win dows\ShutdownTime` *(as printed)* | last shutdown | [System identity and lifecycle keys](../Module_04_System_and_Network_Forensics.md#system-identity-and-lifecycle-keys-computer-name-product-shutdown) |
| Defender configuration | `HKLM\Software\Microsoft\Windows Defender\` | whether AV was disabled | [Evidence-affecting configuration keys](../Module_04_System_and_Network_Forensics.md#evidence-affecting-configuration-keys) |
| ProfileList | `HKLM\Software\Microsoft\Windows NT\Current er sion\ProfileList\SID` *(as printed)* | SID → profile path mapping | [SAM accounts and ProfileList](../Module_04_System_and_Network_Forensics.md#sam-accounts-and-profilelist) |
| USB storage history | `HKLM\SYSTEM\ControlSet001\Enum\USBSTOR` | connected USB devices | [USBSTOR](../Module_04_System_and_Network_Forensics.md#usbstor) |
| Services | `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services` | "currently running services" *(actually all registered services)* | [Services key](../Module_04_System_and_Network_Forensics.md#services-key) |
| Firewall rules | *(not on the slide)* — tree shows `…\FirewallPolicy\FirewallRules` | firewall rule set | [Evidence-affecting configuration keys](../Module_04_System_and_Network_Forensics.md#evidence-affecting-configuration-keys) |
| Local accounts | *(not on the slide)* — `SAM` hive, `Users` / `Aliases` | users on the system | [SAM accounts and ProfileList](../Module_04_System_and_Network_Forensics.md#sam-accounts-and-profilelist) |
| Uninstall | *(not on the slide)* — tree shows `…\CurrentVersion\Uninstall` | installed software and install dates | [Autostart keys](../Module_04_System_and_Network_Forensics.md#autostart-keys-runrunonce-appinit_dlls-and-friends) *(neighbouring key; INE covers `Run`/`RunOnce` here)* |
| App Paths | `SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths` | registered executable name → path | *(not covered by INE — see §4)* |
| Alternate Data Stream | `file.txt:secret` | hiding data on NTFS | [`Module_03_Disks_and_File_Systems.md`](../Module_03_Disks_and_File_Systems.md) |

## 4 · What this deck adds beyond the INE material

- **A collection layer INE has no equivalent for.** KAPE (`--target KapeTriage`) with a real
  command line, and the resulting `<dest>\C\Windows\System32\config\` tree that every later step
  reads from. INE simply assumes you already have the hive.
- **`$MFT` parsing as a first-class step.** MFTECmd with both the bulk CSV mode and single-record
  `--de` dump. INE's unit 6 never touches `$MFT`; Module 04 §7 gap 10 asks for exactly this
  cross-reference and this deck supplies it.
- **Timeline Explorer as the review layer** for EZ-tool output — named in Module 04 §3 as a course
  addition, and this is where it is actually used.
- **TestDisk and PhotoRec** hands-on. INE covers carving as a concept; nobody runs a tool.
- **RegRipper worked at plugin granularity** (`-p timezone`, `-p del`) and then in bulk (`-a` in a
  `for /r` loop). Module 04 §3 records RegRipper's `-f <profile>` entry point only.
- **Deleted registry data demonstrated twice, two different ways** — Registry Explorer's
  unassociated-deleted-value counts on hive load, and RegRipper's `del` plugin. INE asserts that
  deleted registry records are recoverable; this deck is the only place in the course where a
  student sees it happen.
- **`App Paths`** and the **Windows Defender** configuration key, neither of which appears in
  unit 6.
- **A Windows 11 (build 22631) subject system.** Unit 6's OS table stops at Windows 8.1 (Module 04
  §7 gap 7). The `ProductName = Windows 10 Home` / `CurrentBuild = 22631` contradiction visible on
  slide 23 is a free, current, exam-shaped teaching point.
- **Registry Explorer's bookmark set** (`76` available) as a workflow accelerator — a practical
  detail INE never mentions.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted (unit 6 covers it, this deck does not):**

- **`Select\Current`.** The deck reads `ControlSet001` directly at slides 26, 29 and 30. Module 04
  names this as "a real and common error" — the `Select\Current` value decides which control set
  was live. **INE is the course's truth here; this must be corrected before reuse.**
- **Transaction logs (`.LOG1`/`.LOG2`) and dirty hives.** Never mentioned; a KAPE-collected hive is
  routinely dirty.
- **That only keys carry last-write times, never values.** The whole registry walk depends on it.
- **Evidence of execution**, which the deck's own roadmap slide (9) promises: Prefetch, ShimCache,
  Amcache, BAM. All are deferred to session 5.
- **Shell and user artifacts:** ShellBags, LNK files, Jump Lists, RecentDocs, RunMRU, UserAssist,
  MountPoints2, `setupapi.dev.log`, LogonUI, Recycle Bin, Thumbcache, File History, Libraries.
- **Volume Shadow Copies** — `Process VSCs` is visibly unticked in the KAPE run and not discussed.
- **Event logs and browser artifacts** (units 6 and 8).
- **`NTUSER.DAT` and `USRCLASS.DAT`** are named on slide 19 and then never loaded; the whole session
  runs on the five machine hives.
- **Findings.** No finding/interpretation/cannot-prove statement is made anywhere in the deck.

**Resources cited on the slides** — recorded verbatim, `unverified`, not vouched for:

- `https://github.com/Ahmed-AL-Maghraby/Windows-Registry-Analysis-Cheat-Sheet` (slide 10) — `unverified`
- `https://www.cgsecurity.org` (TestDisk / PhotoRec banner, slides 13–14) — `unverified`
- `https://github.com/EricZimmerman/MFTECmd` (MFTECmd banner, slides 16, 18) — `unverified`
- `https://www.kroll.com/kape` (KAPE title bar, slide 15) — `unverified`

## 6 · Cautions before reuse

**Personal data in screenshots — regenerate on the course lab before any of these goes on a slide.**
In practice *every* screenshot from slide 12 onward carries at least a local path or an account
name. The ones that must not be reused at all:

- **12** — command prompt showing the presenter's account name.
- **13, 14** — window titles showing the presenter's tools path; both banners print the tool
  author's email address.
- **15** — the worst single slide: KAPE's `System info:` line prints machine name, user name and OS
  build together, plus the KAPE directory path and a vendor contact address.
- **16, 18, 37, 38** — command prompts showing the presenter's working directories; MFTECmd's
  banner prints the author's email address.
- **17** — twenty-five rows of the presenter's own `AppData` paths, including browser cache
  artifacts that reveal personal web activity.
- **21, 26, 27, 30, 31, 32, 35, 36** — Registry Explorer trees showing the KAPE output path.
- **22** — the workstation's hostname and its raw bytes.
- **23** — `ProductId` and `DigitalProductId` (licence identifiers).
- **25** — the presenter's virtual-adapter DHCP lease.
- **28** — a machine SID together with the profile path containing the account name.
- **29** — serial numbers of the presenter's personal USB drives (Kingston, SanDisk, WD, Seagate).
- **32, 34** — the SAM account row and the Timeline Explorer export, both naming the account.
- **35, 36** — a complete inventory of software installed on the presenter's personal machine.
- **37** — `TimeZoneKeyName -> Egypt Standard Time` is locational; keep or replace deliberately.

**Tools and versions that have moved on** (the deck dates from around November 2024 — the
timestamps throughout are 2024-10 to 2024-11):

- Pinned in the deck: TestDisk/PhotoRec **7.3-WIP (Sept 2024)**, KAPE **1.3.0.2**, MFTECmd
  **1.2.2.1**, Registry Explorer **2.0.0.0**, Timeline Explorer **2.0.0.1**, RegRipper **3.0**
  (`RegRipper3.0-master`, newest plugin seen `v.20230710`). Re-check every one of these against the
  current release before the lab; the Eric Zimmerman set in particular has changed both its runtime
  and its distribution mechanism since. Do not print version numbers on a slide.
- TestDisk 7.3 is still a **WIP** build. Decide deliberately whether the course uses WIP or stable.
- `--tflush` on the KAPE line deletes the destination contents. Either drop it from the student
  command or make the warning explicit.

**OCR that could not be resolved and matters:**

- Slide 37, `LastWrite Time 202U-19-31 21:09:53Z` — no valid month; **the date is unrecoverable**.
- Slides 16 and 18, MFTECmd's `FILE records found:` / `Free records:` / `Processed in _ seconds` —
  blank in the OCR. Do not quote counts.
- Slide 18, record key `90016972` and FixUp actual `90-00` — leading zeros read as `9`.
- Slide 37, `—p timezone` — em dash for hyphen.
- Slides 19, 23, 26, 28 — missing backslashes and PDF line-break spaces inside key paths
  (`C:Windows`, `Currentver sion`, `Win dows`, `Current er sion`), plus `SECUIRTY` for `SECURITY`.
- Slide 22 — `Control\Computer name\` for `Control\ComputerName\ComputerName`.
- Slides 24, 31, 32 — the key path is genuinely **not on the slide**; it has to come from the
  screenshot's tree or status bar, or from INE.
- Slide 38 — RegRipper's `Key` rendered as `Hey` throughout, and one `LastWrite time` with
  unreadable seconds.

**Fitting sessions 4 and 5 into one 4-hour eCDFP `S5`.**
The two decks total 62 slides and about 16 hands-on steps, and they overlap heavily (see the
duplicate analysis in [`Session_05_Practical_Windows_Forensics_part_2.md`](Session_05_Practical_Windows_Forensics_part_2.md) §0).
`S5`'s outcome is *Windows registry and execution artifacts*, so the cut lines follow from that:

- **Keep** — KAPE triage (or ship the output pre-collected and save 15 minutes); the Registry
  Explorer system block (hive load and deleted-record counts, computer name, timezone, OS build,
  network, shutdown, ProfileList, SAM, USBSTOR, Services); the execution-artifact block from
  session 5 (BAM, ShimCache, Amcache, UserAssist), which is the actual learning outcome and is
  currently the *thinnest* part of the delivery; RegRipper bulk + Timeline Explorer review.
- **Move to the new `S4` (storage / partitions / file systems)** — the NTFS metadata block
  (slides 5–7), ADS (11–12), TestDisk (13), PhotoRec (14) and the whole `$MFT`/MFTECmd block
  (16–18, repeated as session 5 slides 13–15). None of it is registry work, and `$MFT` is
  currently taught twice.
- **Move to homework or a cheat-sheet walk-through** — Defender settings (27), firewall rules (31),
  Uninstall (35), App Paths (36), and session 5's Office File MRU / Place MRU / WinRAR block.
  These are one-line lookups; the cheat-sheet cited on slide 10 covers them.
- **Make pre-reading** — slides 8–9 (evidence sources, process roadmap) and 19–20 (where the hives
  live).
- **Must be added, from INE not from these decks** — `Select\Current`, transaction-log handling,
  Prefetch, ShellBags, RecentDocs, MountPoints2, and a written finding /
  interpretation / cannot-prove statement at the end of the lab.
