# ============================================================================
# s3_files.ps1  -  eCDFP FOR-WS01  ::  Session 3 (Data Representation & File Examination)
# Run in an elevated PowerShell AFTER 00_bootstrap.ps1.   Ref: design/tools_by_session.md (S3)
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Run as administrator." -ForegroundColor Red; return }
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) { Write-Host "[STOP] Chocolatey missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }
$py = (Get-Command python.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1).Source
if (-not $py) { $py = "C:\Python314\python.exe" }

Write-Host "== S3 :: File examination tools ==" -ForegroundColor Cyan
$dl = "C:\Forensics\Tools"
function Get-File($url,$out){ try { Invoke-WebRequest $url -OutFile $out -UseBasicParsing; Write-Host "  [OK] $out" -ForegroundColor Green } catch { Write-Host "  [FAIL] $url  ->  $($_.Exception.Message)" -ForegroundColor Red } }

# 1. CORE hex + metadata (pinned)
choco install -y hxd --version=2.5.0.0
choco install -y exiftool --version=13.59.0

# 2. Document-macro tools: olevba (oletools) + oledump.py
& $py -m pip install oletools
New-Item -ItemType Directory -Force -Path "$dl\oledump","$dl\TrID","$dl\CyberChef" | Out-Null
Get-File "https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/oledump.py" "$dl\oledump\oledump.py"

# 3. TrID (classic win32 CLI - trid.exe) + current defs
Get-File "https://mark0.net/download/trid_w32.zip" "$dl\TrID\trid_w32.zip"
Get-File "https://mark0.net/download/triddefs.zip" "$dl\TrID\triddefs.zip"
try { Expand-Archive "$dl\TrID\trid_w32.zip" "$dl\TrID" -Force; Expand-Archive "$dl\TrID\triddefs.zip" "$dl\TrID" -Force } catch {}

# 4. CyberChef offline (latest release) for the air-gapped room
try {
    $rel = Invoke-RestMethod "https://api.github.com/repos/gchq/CyberChef/releases/latest" -Headers @{ "User-Agent"="eCDFP" }
    $a = $rel.assets | Where-Object { $_.name -like "CyberChef*.zip" } | Select-Object -First 1
    Get-File $a.browser_download_url "$dl\CyberChef\$($a.name)"
    Expand-Archive "$dl\CyberChef\$($a.name)" "$dl\CyberChef" -Force
    Write-Host "  CyberChef $($rel.tag_name) (offline copy)" -ForegroundColor Green
} catch { Write-Host "  [FAIL] CyberChef: $($_.Exception.Message)" -ForegroundColor Red }

# 5. Verify
Write-Host "`n-- Verify --" -ForegroundColor Yellow
choco list | Select-String -Pattern "hxd|exiftool"
& $py -m pip show oletools | Select-String "Version"
Get-ChildItem "$dl\TrID\trid.exe","$dl\oledump\oledump.py" -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host "[NOTE] 'file' runs on Kali / Git Bash; TrID is the Windows file-type IDer." -ForegroundColor DarkGray
Write-Host "[DROP] Xiao Steganography - not installed (no living vendor)." -ForegroundColor DarkGray
Write-Host "[OK] S3 finished." -ForegroundColor Green
