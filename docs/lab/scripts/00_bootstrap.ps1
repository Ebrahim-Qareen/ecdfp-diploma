# ============================================================================
# 00_bootstrap.ps1  -  eCDFP FOR-WS01  ::  STEP 1 of the tool install (run FIRST)
# Installs the Chocolatey package manager + Git, Python 3, 7-Zip, and makes the
# kit folders. Self-heals a broken partial Chocolatey from an earlier non-admin run.
#
# HOW TO RUN (students):
#   1. Start menu -> type PowerShell -> right-click -> "Run as administrator" -> Yes
#   2. Set-ExecutionPolicy Bypass -Scope Process -Force
#   3. .\00_bootstrap.ps1
#   4. CLOSE the window and open a NEW admin PowerShell before the next script.
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Not elevated. Right-click Windows PowerShell > 'Run as administrator', then run again." -ForegroundColor Red; return }

Write-Host "== eCDFP FOR-WS01 :: Bootstrap ==" -ForegroundColor Cyan

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    # self-heal: a non-admin attempt can leave a folder with no choco.exe
    if ((Test-Path "C:\ProgramData\chocolatey") -and -not (Test-Path "C:\ProgramData\chocolatey\bin\choco.exe")) {
        Write-Host "  Cleaning a broken partial Chocolatey install..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "C:\ProgramData\chocolatey" -ErrorAction SilentlyContinue
        [Environment]::SetEnvironmentVariable("ChocolateyInstall", $null, "User")
        [Environment]::SetEnvironmentVariable("ChocolateyInstall", $null, "Machine")
    }
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
} else { Write-Host "  Chocolatey already present." -ForegroundColor DarkGray }

# Load PATH so 'choco' works in THIS session
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")

# Prerequisites used by later sessions (Volatility 3, oletools, git clones)
choco install -y git python 7zip

# Kit folders
New-Item -ItemType Directory -Force -Path C:\Forensics\Tools, C:\Forensics\Cases | Out-Null

Write-Host "`n[OK] Bootstrap done. CLOSE this window, open a NEW elevated PowerShell, then run s2_acquisition.ps1." -ForegroundColor Green
