# ============================================================================
# s5_windows.ps1  -  eCDFP FOR-WS01  ::  Session 5 (Windows Forensics: Registry, Activity, Execution)
# Run in an elevated PowerShell AFTER s4 (which brought the EZ Tools).   Ref: tools_by_session.md (S5, 1.1)
# S5 adds only RegRipper 3.0 - the rest arrived with the EZ Tools in S4.
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Run as administrator." -ForegroundColor Red; return }
# refresh PATH so 'git' (from bootstrap) is visible even in a reused shell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Host "[STOP] git missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }

Write-Host "== S5 :: Windows forensics tools ==" -ForegroundColor Cyan
$dl = "C:\Forensics\Tools"

# RegRipper 3.0 (MIT) - ships a compiled rip.exe + plugins, so no Perl needed.
# 3.0 ONLY - 4.0's licence bars vendor / paid-training use (tools_by_session.md 1.1).
if (Test-Path "$dl\RegRipper3.0") { Remove-Item -Recurse -Force "$dl\RegRipper3.0" }
git clone --depth 1 https://github.com/keydet89/RegRipper3.0.git "$dl\RegRipper3.0"

Write-Host "`n-- Verify --" -ForegroundColor Yellow
Get-ChildItem "$dl\RegRipper3.0\rip.exe" -ErrorAction SilentlyContinue | Select-Object FullName
$plug = (Get-ChildItem "$dl\RegRipper3.0\plugins" -Filter *.pl -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "RegRipper plugins: $plug"

Write-Host "[FROM S4 - EZ Tools]: RegistryExplorer, AppCompatCacheParser, PECmd, LECmd, TimelineExplorer, RBCmd, ShellBagsExplorer, EvtxECmd." -ForegroundColor DarkGray
Write-Host "[DO NOT] install RegRipper 4.0 - licence bars paid-training use." -ForegroundColor Red
Write-Host "[OK] S5 finished." -ForegroundColor Green
