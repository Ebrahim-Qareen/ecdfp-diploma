# ============================================================================
# s4_storage.ps1  -  eCDFP FOR-WS01  ::  Session 4 (Storage, Partitions, File Systems)
# Run in an elevated PowerShell AFTER 00_bootstrap.ps1.   Ref: design/tools_by_session.md (S4)
# NOTE: Autopsy is a ~1 GB download - allow time. Also installs the EZ Tools set used in S5.
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Run as administrator." -ForegroundColor Red; return }
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) { Write-Host "[STOP] Chocolatey missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }

Write-Host "== S4 :: Storage & file-system tools ==" -ForegroundColor Cyan
$dl = "C:\Forensics\Tools"; $ez = "$dl\EZTools"

# 1. Autopsy (CORE, ~1 GB). choco latest = 4.23.0 (target 4.23.1; one patch behind - accepted).
choco install -y autopsy
# 2. TestDisk / PhotoRec 7.2.0 STABLE (CORE) - not the 7.3-WIP beta.
choco install -y testdisk-photorec --version=7.2.0
# 3. The Sleuth Kit CLI (SUPPORTING).
choco install -y sleuthkit

# 4. Eric Zimmerman tools (.NET 9) - covers S4 MFTECmd + all S5 GUI/CLI tools.
New-Item -ItemType Directory -Force -Path $ez | Out-Null
Invoke-WebRequest "https://raw.githubusercontent.com/EricZimmerman/Get-ZimmermanTools/master/Get-ZimmermanTools.ps1" -OutFile "$ez\Get-ZimmermanTools.ps1" -UseBasicParsing
& "$ez\Get-ZimmermanTools.ps1" -Dest $ez -NetVersion 9

# 5. Verify
Write-Host "`n-- Verify --" -ForegroundColor Yellow
choco list | Select-String -Pattern "autopsy|testdisk-photorec|sleuthkit"
Get-ChildItem $ez -Recurse -Filter "MFTECmd.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 FullName
Get-ChildItem $ez -Recurse -Filter "RegistryExplorer.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 FullName

Write-Host "[NOTE] EZ Tools need the .NET 9 runtime (installed with Arsenal Image Mounter in S2)." -ForegroundColor DarkGray
Write-Host "[OK] S4 finished." -ForegroundColor Green
