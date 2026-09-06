# Instructor Session 05 — Practical Windows Forensics, part 2

| | |
|---|---|
| **Deck** | `Resources/Instructor/session 5.pdf` — 23 slides, 18 screenshots |
| **INE material covered** | unit 6 — see [`Module_04_System_and_Network_Forensics.md`](../Module_04_System_and_Network_Forensics.md) |
| **Feeds eCDFP session** | `S5` |
| **Source text** | [`../_source_text/Instructor_Session_05_Practical_Windows_Forensics_part_2.md`](../_source_text/Instructor_Session_05_Practical_Windows_Forensics_part_2.md) |

> How this material was delivered by Eng. Mohab Mustafa. Commands and paths are OCR of slide
> screenshots — verify against the slide before putting one in front of students. Not published.

## 0 · Shape of the session

Almost pure lab. Four slides of positioning (title, lifecycle, evidence sources, process roadmap),
one agenda slide, then eighteen slides of screenshots walking the same Registry Explorer / RegRipper
workflow that session 4 established — this time aimed at *user* artifacts and *evidence of
execution* rather than system identity. The user hives finally get loaded here: Registry Explorer's
hive count rises from `5` in session 4 to `6` and then `7`, which is `NTUSER.DAT` and `USRCLASS.DAT`
being added. There is a take-home challenge on the agenda slide (recover the serial of a connected
USB device) but no challenge walkthrough and no wrap-up; the deck ends on a barely legible WinRAR
screenshot.

**Ten of the twenty-three slides are repeats of session 4.** Slides 4, 5, 6 repeat session 4's
slides 4, 8, 9; slides 8, 9, 10, 11 repeat session 4's 34, 35, 36, 39; slides 13, 14, 15 repeat
session 4's 16, 17, 18 — the same screenshots, not merely the same topic. In a rebuilt single `S5`
that duplication is pure recovered time (see §6).

Two numbering defects to be aware of when reading the deck: the label `#4` is used on both slide 12
and slide 13, and `#9` never appears at all (slide 17 is `#8`, slide 18 is `#10`).

## 1 · Running order

| Slides | Topic | Type |
|---|---|---|
| 1–2 | Title slides (no text recovered in the source extract) | admin |
| 3–4 | Session title; lifecycle "we are here" slide *(repeat of S4 slide 4)* | admin |
| 5–6 | Four Windows evidence sources; "PWF: Disk Analysis Process" roadmap *(repeat of S4 slides 8–9)* | concept |
| 7 | Lab agenda, take-home challenge link, three resource links | admin |
| 8–10 | Timeline Explorer over the SAM export; Uninstall key; App Paths *(repeats of S4 slides 34–36)* | lab |
| 11–12 | Bulk registry processing — the `for /r` one-liner *(11 repeats S4 slide 39)*, then RegRipper running it | lab |
| 13–15 | `$MFT` with MFTECmd — CSV, Excel review, `--de` single record *(repeats of S4 slides 16–18)* | lab |
| 16 | Evidence of execution — BAM (`bam\State\UserSettings\<SID>`) | lab |
| 17 | Evidence of execution — Amcache (`InventoryApplication`) | lab |
| 18 | Firewall policy in the SYSTEM hive *(same content as S4 slide 31)* | lab |
| 19 | UserAssist | lab |
| 20–23 | The MRU family — RunMRU, Office File MRU, Place MRU, WinRAR | lab |

## 2 · Labs and demos — what was actually run

### Lab 1 · Carry-over review: accounts, installed software, App Paths · slides 8–10
**Tools:** Timeline Explorer v2.0.0.1, Registry Explorer v2.0.0.0
**Evidence used:** the SAM export and the SOFTWARE hive already open from session 4.
**Steps as demonstrated:** identical screenshots to session 4 slides 34–36 — the Timeline Explorer
view of `User accounts_Values_Export_<yyyyMMddHHmmss>.xlsx`, the `…\CurrentVersion\Uninstall` key,
and `SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths`. Full detail is recorded once, in
[`Session_04_Practical_Windows_Forensics.md`](Session_04_Practical_Windows_Forensics.md) §2 Lab 6
steps 13–15; it is not duplicated here.
**What this lab teaches (as re-delivered):** nothing new — it is a recap opening. In a merged `S5`
this block disappears entirely.

### Lab 2 · Bulk registry processing with RegRipper · slides 11–12
**Tools:** RegRipper 3.0 (`rip.exe`) at an elevated command prompt
**Evidence used:** a folder of hives copied out of the KAPE output to a working directory —
`C:\Users\<user>\Desktop\registries\` containing at least `SYSTEM` and `SOFTWARE`.
**Steps as demonstrated:**
1. The one-liner, from the slide text layer (**not** OCR — exact):
```
for /r %i in (*) do (rip.exe -r %i -a > %i.txt)
```
2. Slide 12 shows it actually running, and the expanded single iteration the shell echoes. Account
   name generalised; otherwise as printed:
```
C:\Users\<user>\Desktop\registries>(rip.exe -r C:\Users\<user>\Desktop\registries\SYSTEM -a 1>C:\Users\<user>\Desktop\registries\SYSTEM.txt )
```
`⚠ OCR — verify` (the OCR wraps mid-path as `…\rey stries\…`). Note the shell has rewritten `>` as
   `1>`; that is `cmd` echoing the redirection, not something typed.
3. **What the output showed:** the plugin launch banner, one line per plugin, each with its version
   date — a readable inventory of what `-a` actually does to a SYSTEM hive:
```
Launching ScanButton v.20131210
Launching appcertdlls v.20200427
Launching appcompatcache v.20220921
Launching backuprestore v.20200517
Launching bam v.20200427
Launching bthenum v.20200515
Launching bthport v.20200517
Launching codepage v.20200519
Launching compname v.20090727
Launching cred v.20200427
Launching dafupnp v.20200525
Launching devclass v.20200525
Launching disableeventlog v.20230710
Launching disablelastaccess v.20200517
Launching disableremotescm v.20200513
Launching environment v.20200512
Launching imagedev v.20140104
Launching ips v.20200518
Launching lsa v.20200517
Launching macaddr v.20200515
Launching mountdev v.20200517
Launching mountdev2 v.20200517
Launching netlogon v.20200515
Launching networksetup2 v.20191004
Launching nic2 v.20200525
Launching ntds v.20200427
```
`⚠ OCR — verify` — the list is truncated by the window and `lsa` is OCR'd as `Isa`. The plugin
   version dates (2013 → 2023) are worth showing: they are how a student judges whether a plugin
   has kept up with the Windows build being examined.
   The prompt bar reads `Administrator: Command Prompt` — elevation is not needed to read a
   collected hive, and the deck does not explain why it is elevated here.
**What this lab teaches:** the "I don't yet know what the question is" pass — dump every plugin's
view of every hive to text, then grep. It pairs with the targeted `-p <plugin>` runs shown in
session 4.

### Lab 3 · `$MFT` with MFTECmd · slides 13–15
**Tools:** MFTECmd v1.2.2.1
**Evidence used:** the same `$MFT` (`File size: 712MB`) as session 4.
**Steps as demonstrated:** identical screenshots to session 4 slides 16–18 —
```
mkdir output
MFTECmd.exe -f $MFT --csv output --csvf parsed_mft.csv
MFTECmd.exe -f $MFT --de 92530
```
`⚠ OCR — verify`. Output detail, the blank record counts and the `90016972` / `00016972` leading-zero
problem are recorded in
[`Session_04_Practical_Windows_Forensics.md`](Session_04_Practical_Windows_Forensics.md) §2 Lab 5.
**Note:** slide 13's title reads `#4 analyzing $MFT with MFTEparser`. There is no tool called
"MFTEparser"; the screenshot is MFTECmd. Correct the title on reuse.
**What this lab teaches (as re-delivered):** nothing new. In a merged `S5` this moves to the new
`S4` with the rest of the file-system material.

### Lab 4 · Evidence of execution — BAM (Background Activity Moderator) · slide 16
**Tools:** Registry Explorer v2.0.0.0
**Evidence used:** `C:\Users\<user>\Desktop\registries\SYSTEM` (the working copy from Lab 2).
**Steps as demonstrated:**
1. Navigate to the key. **As printed on the slide:**
```
HKLM\SYSTEM\CurrentControlSet\Services\bam\User Settings
```
   **Likely intended** — and confirmed by the status bar of the screenshot itself, which reads
   `ControlSet001\Services\bam\State\UserSettings\S-1-5-21-<machine-id>-1001`:
```
HKLM\SYSTEM\ControlSet00#\Services\bam\State\UserSettings\<SID>
```
   The slide path is missing the `State` level and has an incorrect space in `UserSettings`.
   `⚠ OCR — verify`
2. **What the output showed:** `Total rows: 117`, `119 of 119 values shown (100.00%)`, key last
   write `11/20/2024 9:31:14 AM +00:00`. Each value name is an executable path and each value's data
   decodes to a last-execution time. Sample rows (account name generalised):
```
\Device\HarddiskVolume3\Windows\explorer.exe                                              2024-10-06 19:08:47
\Device\HarddiskVolume3\Windows\System32\oobe\FirstLogonAnim.exe                          2024-10-06 18:44:50
\Device\HarddiskVolume3\Windows\System32\ApplicationFrameHost.exe                         2024-10-06 19:08:47
\Device\HarddiskVolume3\Windows\System32\SystemPropertiesAdvanced.exe                     2024-10-06 18:46:40
\Device\HarddiskVolume3\Windows\System32\mmc.exe                                          2024-10-06 18:59:31
\Device\HarddiskVolume3\Windows\System32\rundll32.exe                                     2024-10-06 19:00:57
\Device\HarddiskVolume3\Program Files (x86)\Microsoft\Edge\Application\msedge.exe          2024-10-06 19:08:46
\Device\HarddiskVolume3\Users\<user>\AppData\Local\Microsoft\OneDrive\OneDrive.exe         2024-10-06 19:08:46
\Device\HarddiskVolume3\Program Files (x86)\IObit\Driver Booster\12.0.0\DriverBooster.exe  2024-10-06 19:08:46
\Device\HarddiskVolume3\Users\<user>\AppData\Local\Temp\is-<8char>.tmp\driver_booster_setup.tmp   2024-10-06 18:48:39
\Device\HarddiskVolume3\Users\<user>\AppData\Local\Temp\is-<8char>.tmp-dbinst\setup.exe    2024-10-06 18:48:52
\Device\HarddiskVolume3\Users\<user>\AppData\Local\Temp\Dbz<hex>\vcredist_x64.exe          2024-10-06 19:05:57
\Device\HarddiskVolume3\Users\<user>\AppData\Local\Temp\Dbz<hex>\vcredist_x86_2013.exe     2024-10-06 19:06:22
MicrosoftWindows.Client.CBS_cw5n1h2txyewy                                                 2024-11-20 09:23:24
Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy                                   2024-11-20 07:21:26
Microsoft.Windows.ShellExperienceHost_cw5n1h2txyewy                                       2024-11-20 07:21:27
windows.immersivecontrolpanel_cw5n1h2txyewy                                               2024-11-20 07:56:07
```
`⚠ OCR — verify` (the temp-directory tokens and package-family suffixes are the least reliable
   characters on the slide; `HarddiskVolume3` is consistent across all rows).
**Three teaching points visible on this one screen and stated on none of the slides:**
   BAM records **last execution time, per binary, per user SID** — presence *and* execution, which
   is what separates it from ShimCache; paths are in **device namespace** (`\Device\HarddiskVolumeN`)
   and must be mapped to a drive letter through `MountedDevices` before they mean anything; and
   Store/packaged apps appear as **package family names** with no path at all. The cluster of
   `AppData\Local\Temp\is-*.tmp\…setup.exe` rows is a textbook installer-execution chain and would
   make an excellent lab question.
**What this lab teaches:** the single most direct "this binary ran, at this time, as this user"
artifact in the registry. See
[ShimCache / Application Compatibility Cache](../Module_04_System_and_Network_Forensics.md#shimcache--application-compatibility-cache)
for the contrast the deck's slide title promises but does not deliver.

### Lab 5 · Evidence of execution — Amcache · slide 17
**Tools:** Registry Explorer v2.0.0.0
**Evidence used:** a hive loaded from `C:\Users\<user>\Desktop\registries\`. **⚠ Ambiguous in the
OCR:** the tree label reads `…\registries\SOFTWARE`, but the keys shown — `DeviceCensus`,
`DriverPackageExtended`, `InventoryAcpiPhatHealthRecord`, `InventoryApplication` — belong to
`Amcache.hve\Root\`, not to SOFTWARE. Resolve at the slide before building a lab step.
**Steps as demonstrated:**
1. Expand `Root\InventoryApplication\<ProgramId>` and read the values for one entry.
2. **What the output showed** for the selected application:
```
ProgramId          RegSz    0000086 7fcd4de1bafc0dfa64d3dea84044f00000904
Name               RegSz    Oracle VirtualBox 7.1.2
Version            RegSz    7.1.2
Publisher          RegSz    Oracle and/or its affiliates
Language           RegDword 1033
InstallDate        RegSz    10/09/2024 00:00:00
Source             RegSz    Msi
RootDirPath        RegSz
HiddenArp          RegDword 0
UninstallString    RegSz    MsiExec.exe /I{708E52B5-CAE0-4474-ABCF-7FCD4B203ACE}
RegistryKeyPath    RegSz    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall
MsiPackageCode     RegSz    {6A35CAA0-...-4577-9EC4-CADC7BA17FA9}
MsiProductCode     RegSz    {708E52B5-CAE0-4474-ABCF-7FCD4B203ACE}
MsiInstallDate     RegSz    10/09/2024 00:00:00
ProgramInstanceId  RegSz    0000240825c3305e4c7aebedec125f458964f6eec2e4
(default)          RegDword 0
```
`⚠ OCR — verify` — the `ProgramId` and both GUIDs contain characters the OCR is not reliable on,
   and the `MsiPackageCode` first field is partly unreadable. The left pane also shows the hive's
   deleted-record counters, including `Unassociated deleted values 5,958`.
**Significant gap:** the slide shows **`InventoryApplication` only** — the *installed software*
subkey. It does not show `InventoryApplicationFile`, which is the subkey that carries per-executable
records with **SHA-1 hashes**, and which is what makes Amcache a presence/execution artifact rather
than a second Add/Remove-Programs list. Module 04 §7 gap 8 flags exactly this hole in INE's own
coverage; the deck does not fill it either. **A rebuilt `S5` must add it.**
**What this lab teaches (as delivered):** where Amcache lives and that it inventories installed
applications with MSI provenance. It does *not* yet teach what Amcache is forensically for.

### Lab 6 · Firewall policy in the SYSTEM hive · slide 18
**Tools:** Registry Explorer v2.0.0.0 (`Registry hives (6)` — one more than session 4)
**Evidence used:** SYSTEM hive; the deck's only stated locator is the bullet "System hive".
**Steps as demonstrated:** the `FirewallRules` values pane, identical in content to session 4
slide 31 — `Action / Active / Dir / Protocol / port / Name / Desc / App` columns, with the same
tree of `DomainProfile`, `DynamicKeywords`, `FirewallRules`, `HypervFirewallPolicy`,
`HypervVMCreators`, `Mdm`, `PublicProfile`, `RestrictedInterfaces`, `RestrictedServices`,
`StandardProfile`, `TenantRestrictions` under `FirewallPolicy`. The pipe-delimited rule-string
breakdown is recorded in
[`Session_04_Practical_Windows_Forensics.md`](Session_04_Practical_Windows_Forensics.md) §2 Lab 6
step 11.
**What this lab teaches (as re-delivered):** nothing beyond session 4. Merge or drop.

### Lab 7 · User behaviour — UserAssist · slide 19
**Tools:** Registry Explorer v2.0.0.0
**Evidence used:** `NTUSER.DAT` for the interactive account.
**Steps as demonstrated:**
1. Navigate to the key. **As printed on the slide** (with a PDF line break inside `CurrentVersion`):
```
NTUSER.DAT\Software\Microsoft\Windows\Currentversion\Explorer\UserAssist\
```
   **Likely intended:**
   `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count`.
2. **What the output showed:** `Total rows: 226`, with columns for run counter, focus count, focus
   time and last-executed. Representative rows:
```
UEME_CTLSESSION                                                    0    0    0d, 0h, 00m, 00s
UEME_CTLCUACount:ctor                                              0    0    0d, 0h, 00m, 00s
Microsoft.Windows.Explorer                                        24  175    0d, 1h, 05m, 42s   2024-11-19 10:34:31
msedge                                                             2  674    0d, 1h, 18m, 55s   2024-11-20 10:06:15
Microsoft.WindowsNotepad_8wekyb3d8bbwe!App                          8    4    0d, 0h, 00m, 37s   2024-11-20 10:02:02
Microsoft.Paint_8wekyb3d8bbwe!App                                   2    1    0d, 0h, 00m, 15s   2024-11-19 10:50:57
Microsoft.WindowsCalculator_8wekyb3d8bbwe!App                       2    2    0d, 0h, 00m, 24s   2024-11-19 00:01:50
windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.…     0    3    0d, 0h, 00m, 35s   2024-11-14 12:25:06
{System}\CompMgmtLauncher.exe                                       1    0    0d, 0h, 00m, 00s   2024-11-17 18:40:21
{System}\mmc.exe                                                    0    0    0d, 0h, 00m, 00s   2024-10-06 18:59:25
{System}\SystemPropertiesAdvanced.exe                               0    0    0d, 0h, 00m, 00s
{ProgramFilesX86}\IObit\Driver Booster\12.0.0\DriverBooster.exe      0    0    0d, 0h, 00m, 00s   2024-11-10 02:22:08
Microsoft.Getstarted_8wekyb3d8bbwe!App                              0    0    0d, 0h, 00m, 00s   2024-10-06 18:41:49
Microsoft.AutoGenerated.{Unmapped GUID: ABD04…-E7D6-8446-A99…}       0    2    0d, 0h, 00m, 26s
```
`⚠ OCR — verify` — package-family suffixes and the unmapped GUID are unreliable; the numeric columns
   are legible.
**Teaching points on the screen, unstated on the slide:** value names are stored **ROT-13 encoded**
and Registry Explorer silently decodes them (a student who opens the same key in `regedit` will see
gibberish and needs to know why); known-folder GUIDs are resolved into `{System}` and
`{ProgramFilesX86}` tokens; and UserAssist only records **GUI/shell launches**, so a run counter of
`0` with a real last-executed time, and the absence of anything launched from a console, are both
normal. `Microsoft.Windows.Explorer` at 24 runs / 1h 05m focus and `msedge` at 674 focus events are
the kind of numbers a user-activity narrative is built from.
See [UserAssist](../Module_04_System_and_Network_Forensics.md#userassist).

### Lab 8 · User behaviour — the MRU family · slides 20–23
**Tools:** Registry Explorer v2.0.0.0 (`Registry hives (7)`, `Available bookmarks (103/0)` by
slide 21 — the user hives are now loaded)
**Evidence used:** `NTUSER.DAT` (and `USRCLASS.DAT`) for the interactive account.
**Steps as demonstrated:**
1. **RunMRU** (slide 20, `#12`). The values pane header reads `RunMRU`; the tree shows it beside
   `RecentDocs`, `Run`, `RunOnce`, `TypedPaths`, `TypedURLs`, `UserAssist`, `Shell Folders`,
   `StuckRects3`, `Streams`, `Taskband`, `FeatureUsage`, `FileHistory`, `FirstFolder`, `WinRAR`
   under `…\Explorer\`. **The value rows are not legible in the OCR** — only the key location is
   recoverable. The step is demonstrated visually; the contents must be read off the slide.
2. **Office File MRU** (slide 21, `#13`). Key location visible in the tree:
```
…\Software\Microsoft\Office\<version>\<application>\User MRU\LiveId_<hash>\File MRU
```
   with `Place MRU` as a sibling. `LiveId_<hash>` is redacted here — the slide shows the presenter's
   own Microsoft-account identifier.
   **What the output showed:** `Item 1` … `Item 16`, each `Item N` a value whose data is a timestamp
   plus a full path, newest first — `Item 1` at `2024-11-20 10:14:58` down to `Item 16` at
   `2024-11-10 16:10:46`. The paths are the presenter's own working tree (course decks under
   `D:\Work\…`) and are **not reproduced here**; the structure is what matters:
```
Item 1    2024-11-20 10:14:58   <path>\<file>.pptx
Item 2    2024-11-20 07:22:52   <path>\<file>.potx
…
Item 16   2024-11-10 16:10:46   <path>\<file>.pptx
```
   The teaching point — that `Item N` ordering is *recency rank*, so `Item 1` is the most recent and
   the numbering shifts on every open — is not stated on the slide.
3. **Place MRU** (slide 22, `#14`) — sibling key of `File MRU`, holding the *folders* rather than the
   files. **The screenshot's values pane is not legible in the OCR at all**; only the tree position
   is recoverable. Demonstrated visually.
4. **WinRAR** (slide 23, `#15`) — the tree shows a `WinRAR` key under `…\Explorer\` (the archive and
   extraction-path history). **The screenshot is the least legible in the deck**; four value rows are
   visible but unreadable. Demonstrated visually; the key path and contents must be recovered from
   the slide.
**What this lab teaches:** that "what did this user open, and where from" is answerable from MRU
keys spread across `NTUSER.DAT` and application-specific subtrees, and that the same `Item N` /
recency-rank pattern recurs across all of them. See
[Explorer Open/Save and Run MRUs](../Module_04_System_and_Network_Forensics.md#explorer-opensave-and-run-mrus-comdlg32-runmru)
and [RecentDocs](../Module_04_System_and_Network_Forensics.md#recentdocs).

### Challenge · Recover the serial of a connected USB · slide 7
**Set, not walked through.** The agenda slide states the task as
"Windows forensics challenge ( find serial of connected usb)" with a download link (§5). No
evidence description, no expected answer, no marking scheme, and no solution slide anywhere in the
deck. The required method is session 4's `USBSTOR` step (session 4 slide 29) plus the instance-ID
structure. **A rebuilt `S5` needs the evidence re-hosted, the question re-worded to name the
artifact family, and a written answer key.**

## 3 · Registry keys, paths and artifacts named on the slides

| Artifact / key | Path as shown | Purpose given | Module reference |
|---|---|---|---|
| BAM | `HKLM\SYSTEM\CurrentControlSet\Services\bam\User Settings` *(as printed; status bar shows `ControlSet001\Services\bam\State\UserSettings\<SID>`)* | "analyzing shimcache and bamcache" — evidence of execution | [ShimCache / Application Compatibility Cache](../Module_04_System_and_Network_Forensics.md#shimcache--application-compatibility-cache) |
| Amcache | *(not on the slide)* — `Amcache.hve\Root\InventoryApplication\<ProgramId>` from the tree; tree label reads `SOFTWARE` (⚠ ambiguous) | "amcache" — installed application inventory | [Amcache.hve](../Module_04_System_and_Network_Forensics.md#amcachehve-and-recentfilecachebcf) |
| ShimCache | *(named in the slide 16 title only; the key `…\Control\Session Manager\AppCompatCache` is never opened)* | promised, not demonstrated | [ShimCache / Application Compatibility Cache](../Module_04_System_and_Network_Forensics.md#shimcache--application-compatibility-cache) |
| Firewall rules | "System hive" *(no key path given)* — tree shows `…\FirewallPolicy\FirewallRules` | firewall policy | [Evidence-affecting configuration keys](../Module_04_System_and_Network_Forensics.md#evidence-affecting-configuration-keys) |
| UserAssist | `NTUSER.DAT\Software\Microsoft\Windows\Currentversion\Explorer\UserAssist\` *(as printed)* | user behaviour — GUI launch counts and times | [UserAssist](../Module_04_System_and_Network_Forensics.md#userassist) |
| RunMRU | *(not on the slide)* — tree shows `…\Explorer\RunMRU` | "RUN mru" | [Explorer Open/Save and Run MRUs](../Module_04_System_and_Network_Forensics.md#explorer-opensave-and-run-mrus-comdlg32-runmru) |
| Office File MRU | *(not on the slide)* — tree shows `…\Office\<ver>\<app>\User MRU\LiveId_<hash>\File MRU` | "file mru" — recently opened documents | [RecentDocs](../Module_04_System_and_Network_Forensics.md#recentdocs) |
| Office Place MRU | *(not on the slide)* — sibling `…\User MRU\LiveId_<hash>\Place MRU` | "place mru" — recently used folders | [RecentDocs](../Module_04_System_and_Network_Forensics.md#recentdocs) |
| WinRAR history | *(not on the slide)* — tree shows a `WinRAR` key under `…\Explorer\` | archive / extraction history | [Explorer Open/Save and Run MRUs](../Module_04_System_and_Network_Forensics.md#explorer-opensave-and-run-mrus-comdlg32-runmru) |
| Uninstall, App Paths, SAM, `$MFT` | *(repeats — see session 4 §3)* | — | — |
| USBSTOR *(challenge only)* | *(not restated; required by the slide 7 challenge)* | recover a device serial | [USBSTOR](../Module_04_System_and_Network_Forensics.md#usbstor) |

## 4 · What this deck adds beyond the INE material

- **BAM, worked on real data.** Unit 6 does not teach the Background Activity Moderator at all.
  This slide is the only place in the entire course where a student sees a per-SID, per-binary
  last-execution table, with device-namespace paths and packaged-app names — and it is the closest
  thing the course has to a clean "presence vs execution" demonstration.
- **A running list of the `for /r … rip.exe -a` plugin inventory** with per-plugin version dates,
  which is a practical way to teach that plugin coverage lags Windows builds (Module 04 §3 records
  the caveat; this is the evidence for it).
- **Amcache located and opened**, which unit 6 introduces on a single slide and never returns to
  (Module 04 §7 gap 8).
- **The `LiveId_<hash>` Office MRU subtree** — a modern, account-scoped MRU location that INE's
  Windows-7-era coverage does not mention.
- **UserAssist read through Registry Explorer's decoder**, showing focus count and focus time
  columns, not just run count — INE's treatment stops at run count and last-executed.
- **A live demonstration that Registry Explorer's hive count grows** as `NTUSER.DAT` and
  `USRCLASS.DAT` are added (5 → 6 → 7 across the session), which is the practical way to teach the
  machine-hive / user-hive split.

## 5 · What this deck omits that INE covers — and resources it cites

**Omitted (unit 6 covers it, this deck does not):**

- **ShimCache** — named in the slide 16 title and in the agenda, never opened. The
  `…\Control\Session Manager\AppCompatCache` key does not appear anywhere in the deck, and neither
  does `AppCompatCacheParser`. This is the largest single gap, because the ShimCache/BAM contrast is
  the point of the promised slide.
- **`InventoryApplicationFile`** and the Amcache SHA-1 hash records — see Lab 5.
- **Prefetch** — on the roadmap slide (6) and never demonstrated. No `PECmd`, no `.pf` file.
- **ShellBags** — listed on the agenda slide ("shell bags") and never shown. No ShellBags Explorer,
  no `SBECmd`.
- **RecentDocs** — visible in the tree at slide 20 and never opened.
- **LNK files and Jump Lists**, **MountPoints2**, **`setupapi.dev.log`**, **Recycle Bin**,
  **Volume Shadow Copies**, **Thumbcache**, **browser artifacts**, **event logs**.
- **Connected USB drives analysis**, which the agenda slide promises as its own bullet — it is only
  covered in session 4 and set as the unwalked challenge here.
- **`Select\Current`** — as in session 4, `ControlSet001` is read directly. INE is the course's
  truth; correct on reuse.
- **Any finding statement.** Again, nothing is written down as a conclusion.

**Resources cited on the slides** — recorded verbatim, `unverified`, not vouched for:

- `https://easyupload.io/0lmvpm` (slide 7, the USB-serial challenge evidence) — `unverified`.
  A one-click file-sharing link of this kind is unlikely to survive; the evidence needs re-hosting
  and a manifest entry regardless.
- `https://github.com/Ahmed-AL-Maghraby/Windows-Registry-Analysis-Cheat-Sheet` (slide 7) — `unverified`
- `https://www.magnetforensics.com/blog/artifact-profile-userassist/` (slide 7) — `unverified`
- `https://github.com/stuxnet999/MemLabs` (slide 7) — `unverified`. Note this is a **memory**
  forensics lab set; nothing in either session 4 or 5 teaches memory analysis, so it is an
  unexplained pointer rather than a resource for this session.

## 6 · Cautions before reuse

**Personal data in screenshots — regenerate on the course lab before any of these goes on a slide.**

- **8, 9, 10, 13, 14, 15** — carry every problem of session 4 slides 34, 35, 36, 16, 17, 18: the
  presenter's account name in export filenames and `AppData` paths, a complete inventory of software
  installed on a personal machine, working-directory paths, and a tool banner containing the author's
  email address.
- **12** — the command prompt shows the full path `C:\Users\<account>\Desktop\registries\` three
  times in one line, with the real account name.
- **16** — BAM values are almost entirely paths under the presenter's profile, including installer
  temp directories; the key path in the status bar carries the machine SID.
- **17** — the hive path shows the account name; the entry itself is software installed on the
  presenter's own machine.
- **19** — UserAssist reveals personal application-usage patterns with timestamps.
- **21** — **the worst slide in the deck for confidentiality.** The Office File MRU lists sixteen
  full paths into the presenter's private working tree, exposing other clients' and other courses'
  material by name, together with a Microsoft-account identifier in the `LiveId_` key name. Do not
  reuse this screenshot in any form.
- **18, 20, 22, 23** — Registry Explorer trees carrying the working-directory path.

**Tools and versions that have moved on:** identical to session 4 — Registry Explorer 2.0.0.0,
Timeline Explorer 2.0.0.1, MFTECmd 1.2.2.1, RegRipper 3.0 with plugins dated `v.20090727` to
`v.20230710`. The RegRipper plugin dates are the ones that matter most here: `bam v.20200427` and
`appcompatcache v.20220921` are being run against a Windows 11 build 22631 hive, and the deck never
raises the question of whether a 2020 plugin parses a 2024 BAM layout correctly. Re-verify every
plugin against the course's chosen Windows build before the lab.

**OCR that could not be resolved and matters:**

- Slide 17 — whether the loaded hive is `SOFTWARE` or `Amcache.hve`. The tree label and the key
  names disagree. This decides what the step is actually teaching.
- Slide 20 (RunMRU), 22 (Place MRU) and 23 (WinRAR) — **the values panes are illegible.** Three of
  the deck's four MRU steps have no recoverable content; only the key locations survive. These three
  steps must be re-shot from scratch.
- Slide 16 — the BAM temp-path tokens (`is-<8char>.tmp`, `Dbz<hex>`) and the packaged-app family
  suffixes are unreliable character by character; the volume (`HarddiskVolume3`) and the timestamps
  are consistent.
- Slide 12 — the prompt path wraps mid-word (`…\rey stries\…`); the plugin list is truncated by the
  console window, so it is **not** a complete inventory of what `-a` runs.
- Slide 17 — `ProgramId`, `MsiPackageCode` and `MsiProductCode` GUIDs are partly unreadable.
- Slide 19 — one UserAssist row is `Microsoft.AutoGenerated.{Unmapped GUID: …}`; the GUID itself is
  not recoverable, and "unmapped" is Registry Explorer's own note, not an OCR failure.
- Deck-wide — the label `#4` is used twice (slides 12 and 13) and `#9` is missing entirely, so the
  deck's own step numbering cannot be used as lab-step numbering without renumbering.

**Fitting sessions 4 and 5 into one 4-hour eCDFP `S5`.**
The duplication does most of the work: **ten of this deck's twenty-three slides are repeats**
(4, 5, 6, 8, 9, 10, 11, 13, 14, 15), so merging costs nothing to remove them. What is left, ranked
against `S5`'s outcome — *Windows registry and execution artifacts*:

- **Keep and expand** — Lab 4 (BAM) and Lab 5 (Amcache) are the core of the merged session and are
  currently the *shortest* part of the delivery: one slide each. They need to grow, and ShimCache
  plus Prefetch have to be built alongside them from INE (Module 04 §2A), because the deck promises
  both and delivers neither.
- **Keep** — Lab 7 (UserAssist), with the ROT-13 and shell-launch-only caveats added.
- **Compress into one demonstration** — Lab 8's four MRU steps become a single "MRU family" step
  (three of the four screenshots are illegible and must be re-shot anyway).
- **Move to the new `S4`** — Lab 3 (`$MFT`/MFTECmd), with session 4's NTFS, ADS, TestDisk and
  PhotoRec material.
- **Move to homework** — Lab 6 (firewall policy), Lab 1's Uninstall and App Paths recap, and the
  USB-serial challenge, which is a self-contained take-home once the evidence is re-hosted with an
  answer key.
- **Drop entirely** — Lab 1's Timeline Explorer recap and slides 4–6, all pure repetition.

Rough budget for the merged four hours: 30 min lecture (registry as a file system, hive locations,
key-vs-value timestamps, `Select\Current`), 20 min KAPE collection (or pre-supplied), 60 min system
block, 75 min execution-artifact block (BAM, ShimCache, Amcache, Prefetch, UserAssist), 25 min
RegRipper bulk + Timeline Explorer review, 30 min writing a finding / interpretation /
cannot-prove statement — which neither deck currently asks for and which is the thing the eCDFP
exam actually tests.
