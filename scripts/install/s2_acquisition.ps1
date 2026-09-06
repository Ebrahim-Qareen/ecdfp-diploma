# ============================================================================
# s2_acquisition.ps1  -  eCDFP FOR-WS01  ::  Session 2 (Acquisition, Memory, Live Response)
# Run in an elevated PowerShell AFTER 00_bootstrap.ps1.   Ref: design/tools_by_session.md (S2)
# ============================================================================

# --- robust prelude (every fix we hit, baked in) ---
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Run as administrator." -ForegroundColor Red; return }
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) { Write-Host "[STOP] Chocolatey missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }
$py = (Get-Command python.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1).Source
if (-not $py) { $py = "C:\Python314\python.exe" }
if (-not (Test-Path $py)) { Write-Host "[STOP] Python missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }

Write-Host "== S2 :: Acquisition tools ==" -ForegroundColor Cyan

# 1. Mounting tools (SUPPORTING)
choco install -y osfmount
choco install -y arsenalimagemounter --version=3.13.368

# 2. Volatility 3 (CORE, also S6)
& $py -m pip install --upgrade pip
& $py -m pip install volatility3==2.28.2

# 2a. Put real python + its Scripts dir ahead of the Windows Store alias (permanent)
$pydir   = Split-Path $py
$scripts = (& $py -c "import sysconfig; print(sysconfig.get_path('scripts'))").Trim()
$m = [Environment]::GetEnvironmentVariable("Path","Machine")
if ($m -notlike "*$pydir*")   { $m = "$pydir;$m" }
if ($m -notlike "*$scripts*") { $m = "$m;$scripts" }
[Environment]::SetEnvironmentVariable("Path",$m,"Machine")
$env:Path = "$pydir;$scripts;$env:Path"

# 3. Verify
Write-Host "`n-- Verify --" -ForegroundColor Yellow
choco list | Select-String -Pattern "osfmount|arsenalimagemounter"
& $py -c "import volatility3.framework as f; print('Volatility 3 OK:', f.constants.PACKAGE_VERSION)"

# 4. Manual / platform
Write-Host "`n[MANUAL] FTK Imager 8.3 (CORE): https://www.exterro.com/ftk-product-downloads -> 'FTK Imager 8.3' -> run installer (Typical). No paid 'Pro'." -ForegroundColor Magenta
Write-Host "[NOTE] dd / dc3dd imaging runs on Kali." -ForegroundColor DarkGray
Write-Host "[OK] S2 finished." -ForegroundColor Green
