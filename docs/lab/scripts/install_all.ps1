# ============================================================================
# install_all.ps1  -  eCDFP FOR-WS01  ::  ONE-SHOT full build (run in ONE elevated session)
# Runs bootstrap + S2..S6 + air-gap symbols + desktop shortcuts + verification, in order.
# Each step re-reads PATH from the registry, so no shell reopen is needed between steps.
#
# HOW TO RUN (students):
#   1. Right-click Windows PowerShell -> "Run as administrator" -> Yes
#   2. cd <folder with these scripts>
#   3. Set-ExecutionPolicy Bypass -Scope Process -Force
#   4. .\install_all.ps1
#   5. Do the ONE manual step it prints (FTK Imager 8.3), then take the CLEAN-TOOLS snapshot.
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Right-click PowerShell > 'Run as administrator', then run again." -ForegroundColor Red; return }

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$steps = "00_bootstrap.ps1","s2_acquisition.ps1","s3_files.ps1","s4_storage.ps1","s5_windows.ps1","s6_network.ps1","06_symbols_airgap.ps1","create_shortcuts.ps1","verify_tools.ps1"

foreach ($s in $steps) {
    Write-Host "`n######################## $s ########################" -ForegroundColor Magenta
    & "$here\$s"
    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
}

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "ALL SCRIPTED STEPS DONE." -ForegroundColor Green
Write-Host "ONE manual step left: FTK Imager 8.3 -> https://www.exterro.com/ftk-product-downloads" -ForegroundColor Magenta
Write-Host "Then re-run verify_tools.ps1 (expect 0 missing) and take the CLEAN-TOOLS snapshot." -ForegroundColor Cyan
