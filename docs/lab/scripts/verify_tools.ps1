# verify_tools.ps1 — eCDFP FOR-WS01 :: confirm every tool is present before the CLEAN-TOOLS snapshot
$dl = "C:\Forensics\Tools"; $ez = "$dl\EZTools"
$py = "C:\Python314\python.exe"
function Row($n,$ok){ "{0,-30} {1}" -f $n, ($(if($ok){"[PASS]"}else{"[MISSING]"})) }
$has = { param($f) (Get-ChildItem $args[0] -Recurse -Filter $f -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0 }

$choco = (choco list) -join "`n"
$r = @()
foreach($p in "hxd","exiftool","autopsy","testdisk-photorec","sleuthkit","osfmount","arsenalimagemounter","wireshark"){
    $r += Row "choco: $p" ($choco -match "(?im)^$([regex]::Escape($p))\s")
}
$r += Row "Volatility 3 (vol.exe)"    (Test-Path "C:\Python314\Scripts\vol.exe")
foreach($t in "MFTECmd","RegistryExplorer","PECmd","LECmd","AppCompatCacheParser","TimelineExplorer","RBCmd","ShellBagsExplorer","EvtxECmd"){
    $r += Row "EZ: $t" ((Get-ChildItem $ez -Recurse -Filter "$t.exe" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
}
$r += Row "RegRipper 3.0 (rip.exe)"   (Test-Path "$dl\RegRipper3.0\rip.exe")
$r += Row "TrID (trid.exe)"           (Test-Path "$dl\TrID\trid.exe")
$r += Row "oledump.py"                (Test-Path "$dl\oledump\oledump.py")
$r += Row "olevba (oletools)"         ([bool]((& $py -m pip show oletools) 2>$null))
$r += Row "CyberChef (offline)"       ((Get-ChildItem "$dl\CyberChef" -Recurse -Filter "*.html" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
$r += Row "NetworkMiner 3.1"          ((Get-ChildItem "$dl\NetworkMiner" -Recurse -Filter "NetworkMiner.exe" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
$r += Row "FTK Imager (manual)"       ((Get-ChildItem "C:\Program Files" -Recurse -Filter "FTK Imager.exe" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)

Write-Host "`n===== eCDFP FOR-WS01 tool verification =====" -ForegroundColor Cyan
$r | ForEach-Object { if($_ -match "MISSING"){ Write-Host $_ -ForegroundColor Red } else { Write-Host $_ -ForegroundColor Green } }
$miss = ($r | Where-Object { $_ -match "MISSING" }).Count
Write-Host "`nMissing: $miss" -ForegroundColor $(if($miss){"Red"}else{"Green"})
