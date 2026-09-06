# create_shortcuts.ps1 — eCDFP FOR-WS01 :: desktop shortcuts for the GUI tools.
# Placed on the PUBLIC desktop so they appear for every user (survives cloning to the student image).
# Run in an elevated PowerShell.

$WShell  = New-Object -ComObject WScript.Shell
$desktop = "$env:PUBLIC\Desktop"
$dl = "C:\Forensics\Tools"; $ez = "$dl\EZTools"

function Find-Exe($root,$name){ (Get-ChildItem $root -Recurse -Filter $name -ErrorAction SilentlyContinue | Select-Object -First 1).FullName }
function New-SC($name,$target,$arguments="",$workdir=""){
    if ([string]::IsNullOrWhiteSpace($target) -or -not (Test-Path $target)) { Write-Host "  [skip] $name" -ForegroundColor DarkYellow; return }
    $lnk = $WShell.CreateShortcut((Join-Path $desktop "$name.lnk"))
    $lnk.TargetPath = $target
    if ($arguments) { $lnk.Arguments = $arguments }
    $lnk.WorkingDirectory = if ($workdir) { $workdir } elseif (Test-Path $target -PathType Leaf) { Split-Path $target } else { $target }
    $lnk.Save(); Write-Host "  [ok] $name" -ForegroundColor Green
}

Write-Host "Creating desktop shortcuts in $desktop" -ForegroundColor Cyan
# GUI applications
New-SC "Autopsy"               (Find-Exe "C:\Program Files\Autopsy*" "autopsy64.exe")
New-SC "FTK Imager"            (Find-Exe "C:\Program Files" "FTK Imager.exe")
New-SC "HxD"                   "C:\Program Files\HxD\HxD.exe"
New-SC "Wireshark"             "C:\Program Files\Wireshark\Wireshark.exe"
New-SC "OSFMount"              "C:\Program Files\OSFMount\OSFMount.exe"
New-SC "Arsenal Image Mounter" (Find-Exe "C:\ProgramData\chocolatey\lib\arsenalimagemounter" "ArsenalImageMounter.exe")
New-SC "NetworkMiner"          (Find-Exe "$dl\NetworkMiner" "NetworkMiner.exe")
New-SC "PhotoRec"              (Find-Exe "C:\ProgramData\chocolatey\lib\testdisk-photorec" "qphotorec_win.exe")
# Eric Zimmerman GUI tools
New-SC "Registry Explorer"     (Find-Exe $ez "RegistryExplorer.exe")
New-SC "Timeline Explorer"     (Find-Exe $ez "TimelineExplorer.exe")
New-SC "ShellBags Explorer"    (Find-Exe $ez "ShellBagsExplorer.exe")
New-SC "MFT Explorer"          (Find-Exe $ez "MFTExplorer.exe")
# CyberChef (opens the offline HTML in the default browser)
New-SC "CyberChef"             ((Get-ChildItem "$dl\CyberChef" -Recurse -Filter "*.html" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName)
# CLI launcher + tools folder (for vol, MFTECmd, PECmd, rip.exe, trid, oledump, olevba, TSK...)
New-SC "Forensic CLI"          "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" "-NoExit -Command Set-Location '$dl'" $dl
New-SC "Forensic Tools Folder" "$env:SystemRoot\explorer.exe" "$dl"

Write-Host "`nDone. Refresh the desktop (F5) to see them." -ForegroundColor Green

# --- De-duplicate: installers drop their own desktop icons; keep one clean set ---
$dead = "Autopsy 4.23.0","Externo FTK Imager","Exterro FTK Imager","photorec_win","qphotorec_win","testdisk_win"
$desks = @("$env:PUBLIC\Desktop","$env:USERPROFILE\Desktop","$env:OneDrive\Desktop") | Where-Object { $_ -and (Test-Path $_) }
foreach ($d in $desks) { foreach ($n in $dead) { if (Test-Path "$d\$n.lnk") { Remove-Item "$d\$n.lnk" -Force; Write-Host "  [rm] $n ($d)" -ForegroundColor DarkYellow } } }
# keep only the Public OSFMount (remove the installer's user-desktop copy)
foreach ($d in @("$env:USERPROFILE\Desktop","$env:OneDrive\Desktop")) { if ($d -and (Test-Path "$d\OSFMount.lnk")) { Remove-Item "$d\OSFMount.lnk" -Force } }
# add a clean TestDisk (console, CORE) shortcut
$td = (Get-ChildItem "C:\ProgramData\chocolatey\lib\testdisk-photorec" -Recurse -Filter "testdisk_win.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
if ($td) { $l=$WShell.CreateShortcut("$env:PUBLIC\Desktop\TestDisk.lnk"); $l.TargetPath=$td; $l.WorkingDirectory=Split-Path $td; $l.Save(); Write-Host "  [ok] TestDisk" -ForegroundColor Green }
