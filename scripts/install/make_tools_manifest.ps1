# make_tools_manifest.ps1 — eCDFP FOR-WS01
# Writes C:\Forensics\Tools\TOOLS.sha256, the lab's BASELINE manifest.
#
# WHAT THIS PROVES, and what it does not:
#   It records the SHA-256 of every tool binary at the moment the CLEAN-TOOLS snapshot is taken.
#   A later check proves the tool has NOT CHANGED SINCE THAT BASELINE.
#   It does NOT prove the binary is what the vendor shipped — nobody has verified that here.
#   That distinction is the whole of T03, and the lab says it out loud (D94: never claim more
#   than the artifact shows).
#
# Run AFTER every tool is installed and verify_tools.ps1 passes, and BEFORE the snapshot.

$root = "C:\Forensics\Tools"
$out  = Join-Path $root "TOOLS.sha256"
if (-not (Test-Path $root)) { Write-Host "[FAIL] $root not found — install the tools first." -ForegroundColor Red; exit 1 }

$exts = @('.exe','.dll','.jar','.py','.ps1')
$files = Get-ChildItem $root -Recurse -File -ErrorAction SilentlyContinue |
         Where-Object { $exts -contains $_.Extension.ToLower() -and $_.Name -ne 'TOOLS.sha256' } |
         Sort-Object FullName

if (-not $files) { Write-Host "[FAIL] no tool binaries found under $root" -ForegroundColor Red; exit 1 }

$header = @(
  "# eCDFP FOR-WS01 — tool baseline manifest",
  "# Generated $(Get-Date -Format 'yyyy-MM-dd HH:mm') UTC$([char]0x2011)offset $(Get-Date -Format 'zzz')",
  "# Algorithm: SHA-256",
  "#",
  "# This is the LAB BASELINE, taken at the CLEAN-TOOLS snapshot.",
  "# It proves a tool has not changed since that baseline.",
  "# It does NOT prove the binary is what the vendor published.",
  "#"
)

$rows = foreach ($f in $files) {
  $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLower()
  "{0}  {1}" -f $h, $f.FullName.Substring($root.Length + 1)
}

($header + $rows) | Set-Content -LiteralPath $out -Encoding ASCII

Write-Host "`n===== TOOLS.sha256 written =====" -ForegroundColor Cyan
Write-Host ("  {0}" -f $out)
Write-Host ("  {0} binaries hashed" -f $files.Count) -ForegroundColor Green
Write-Host "`n  Re-check any time with:" -ForegroundColor DarkGray
Write-Host '    Get-FileHash "C:\Forensics\Tools\<relative path>" -Algorithm SHA256' -ForegroundColor DarkGray
