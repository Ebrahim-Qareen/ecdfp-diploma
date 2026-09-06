# ============================================================================
# s6_network.ps1  -  eCDFP FOR-WS01  ::  Session 6 (Network Forensics, Timelines, Capstone)
# Run in an elevated PowerShell AFTER 00_bootstrap.ps1.   Ref: design/tools_by_session.md (S6)
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) { Write-Host "[STOP] Run as administrator." -ForegroundColor Red; return }
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) { Write-Host "[STOP] Chocolatey missing - run 00_bootstrap.ps1 first." -ForegroundColor Red; return }

Write-Host "== S6 :: Network forensics tools ==" -ForegroundColor Cyan
$dl = "C:\Forensics\Tools"

# 1. Wireshark 4.6.8 (CORE, pinned). Npcap not needed to READ pcaps.
choco install -y wireshark --version=4.6.8

# 2. NetworkMiner 3.1 Free (SUPPORTING) - direct from Netresec (choco stale at 2.5).
$nm = "$dl\NetworkMiner"
New-Item -ItemType Directory -Force -Path $nm | Out-Null
try {
    Invoke-WebRequest "https://www.netresec.com/?download=NetworkMiner" -OutFile "$nm\NetworkMiner.zip" -UseBasicParsing
    Expand-Archive "$nm\NetworkMiner.zip" $nm -Force
    Write-Host "  [OK] NetworkMiner extracted" -ForegroundColor Green
} catch { Write-Host "  [FAIL] NetworkMiner - manual: https://www.netresec.com/?page=NetworkMiner" -ForegroundColor Red }

# 3. Verify
Write-Host "`n-- Verify --" -ForegroundColor Yellow
choco list | Select-String -Pattern "wireshark"
Get-ChildItem $nm -Recurse -Filter "NetworkMiner.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 FullName

Write-Host "`n[KALI] plaso / log2timeline:  sudo apt update && sudo apt install -y plaso" -ForegroundColor Cyan
Write-Host "[DONE-EARLIER] Volatility 3 installed in S2 (also an S6 tool)." -ForegroundColor DarkGray
Write-Host "[LIMIT] NetworkMiner Free cannot parse PcapNG - capture/teach in classic pcap." -ForegroundColor DarkGray
Write-Host "[OK] S6 finished." -ForegroundColor Green
