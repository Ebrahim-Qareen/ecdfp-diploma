<#
    precommit_scan.ps1 -- eCDFP Diploma
    Part 9 content gate: credential/secret scan + PII scan + no-evidence-bytes check.
    Must print CLEAN before any commit. The repo is PUBLIC (D22), so a finding
    BLOCKS the push -- it is never waived.

    Usage:  powershell -ExecutionPolicy Bypass -File tools\precommit_scan.ps1
            -Root <path>   defaults to the repo root (parent of tools\)
#>
[CmdletBinding()]
param([string] $Root)

$ErrorActionPreference = 'Stop'
if (-not $Root) { $Root = Split-Path -Parent $PSScriptRoot }

$findings = New-Object System.Collections.Generic.List[object]
function Add-Finding($cat,$file,$line,$text) {
    $findings.Add([pscustomobject]@{ Category=$cat; File=$file; Line=$line; Match=$text })
}

# Paths never scanned (gitignored) and never committed anyway.
$skipDir = @('\.git\','\Resources\','\evidence\','\vm_notes\','\node_modules\')
# Evidence byte formats that must never enter the repo (R9).
$evidenceExt = @('.E01','.Ex01','.AD1','.dd','.raw','.img','.mem','.vmem','.dmp','.pcap','.pcapng','.vhd','.vhdx','.vmdk')
$hiveNames   = @('NTUSER.DAT','SYSTEM','SOFTWARE','SAM','SECURITY','USRCLASS.DAT','$MFT','$LogFile','$UsnJrnl')

$secretPatterns = @(
  @{ n='password assignment';  p='(?i)(password|passwd|pwd)\s*[:=]\s*["'']?[^\s"''<>{}\[\]]{4,}' },
  @{ n='api key / token';      p='(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|bearer)\b\s*[:=]\s*["'']?[A-Za-z0-9_\-\.]{12,}' },
  @{ n='private key block';    p='-----BEGIN\s+(RSA|EC|OPENSSH|PGP|DSA)?\s*PRIVATE KEY' },
  @{ n='AWS access key id';    p='\bAKIA[0-9A-Z]{16}\b' },
  @{ n='GitHub token';         p='\bgh[pousr]_[A-Za-z0-9]{20,}\b' },
  @{ n='connection string';    p='(?i)\b(mongodb|postgres|postgresql|mysql|redis|amqp)://[^\s/@]+:[^\s/@]+@' },
  @{ n='JWT';                  p='\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b' }
)

# PII. Documentation/reserved ranges are allowed on purpose -- labs need example IPs.
$piiPatterns = @(
  @{ n='email address';        p='\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b' },
  @{ n='routable private IP';  p='\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b' },
  @{ n='phone number';         p='\b\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}\b' },
  @{ n='national ID-like';     p='\b\d{3}-\d{2}-\d{4}\b' }
)
$piiAllow = @(
  'example\.(com|org|net)', 'itgate', 'ebrahim-qareen\.github\.io',
  '\b192\.0\.2\.', '\b198\.51\.100\.', '\b203\.0\.113\.',   # RFC 5737 documentation
  'noreply@', 'user@host', 'analyst@'
)

Write-Host ""
Write-Host "precommit_scan -- $Root" -ForegroundColor White

# ---------------------------------------------------------- 1 evidence bytes
Write-Host "`n== evidence bytes (R9)" -ForegroundColor Cyan
Get-ChildItem -LiteralPath $Root -Recurse -File -Force -ErrorAction SilentlyContinue |
  Where-Object { $f=$_.FullName; -not ($skipDir | Where-Object { $f -like "*$_*" }) } |
  ForEach-Object {
    if ($evidenceExt -contains $_.Extension) { Add-Finding 'evidence bytes' $_.FullName 0 "extension $($_.Extension)" }
    if ($hiveNames  -contains $_.Name)       { Add-Finding 'evidence bytes' $_.FullName 0 "registry hive $($_.Name)" }
    if ($_.Length -gt 20MB)                  { Add-Finding 'oversized file' $_.FullName 0 "$([math]::Round($_.Length/1MB,1)) MB" }
  }

# ------------------------------------------------------- 2 secrets + 3 PII
Write-Host "== credentials and PII (R8, R9)" -ForegroundColor Cyan
$textExt = @('.md','.html','.css','.js','.ps1','.py','.json','.yml','.yaml','.txt','.csv','.xml','.gitignore')
$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force -ErrorAction SilentlyContinue |
  Where-Object { $f=$_.FullName
    (-not ($skipDir | Where-Object { $f -like "*$_*" })) -and
    ($textExt -contains $_.Extension -or $_.Name -eq '.gitignore') }

foreach ($file in $files) {
    $n = 0
    foreach ($line in [System.IO.File]::ReadLines($file.FullName)) {
        $n++
        foreach ($sp in $secretPatterns) {
            if ($line -match $sp.p) { Add-Finding "secret: $($sp.n)" $file.FullName $n $Matches[0] }
        }
        foreach ($pp in $piiPatterns) {
            if ($line -match $pp.p) {
                $hit = $Matches[0]
                $allowed = $false
                foreach ($a in $piiAllow) { if ($line -match $a) { $allowed = $true; break } }
                if (-not $allowed) { Add-Finding "PII: $($pp.n)" $file.FullName $n $hit }
            }
        }
    }
}

# ----------------------------------------------------- 4 stage directions
Write-Host "== instructor stage directions in student-facing files (Part 11)" -ForegroundColor Cyan
$stage = @('ask the room','what to listen for','if nobody answers','instructor note','say this','pause here',
           'expect blank stares','watch for confusion','tell them that','do not reveal')
Get-ChildItem -LiteralPath $Root -Recurse -File -Force -Filter *.html -ErrorAction SilentlyContinue |
  Where-Object { $f=$_.FullName; -not ($skipDir | Where-Object { $f -like "*$_*" }) } |
  ForEach-Object {
    $c = Get-Content -LiteralPath $_.FullName -Raw
    foreach ($s in $stage) { if ($c -match [regex]::Escape($s)) { Add-Finding 'stage direction' $_.FullName 0 $s } }
  }

# ------------------------------------------------------------------ report
Write-Host ""
if ($findings.Count -eq 0) {
    Write-Host "CLEAN" -ForegroundColor Green
    Write-Host ""
    exit 0
}
Write-Host "$($findings.Count) FINDING(S) -- COMMIT BLOCKED" -ForegroundColor Red
$findings | Group-Object Category | ForEach-Object {
    Write-Host "`n  [$($_.Count)] $($_.Name)" -ForegroundColor Yellow
    $_.Group | Select-Object -First 8 | ForEach-Object {
        $rel = $_.File.Replace($Root,'').TrimStart('\')
        Write-Host ("        {0}:{1}  {2}" -f $rel, $_.Line, $_.Match)
    }
}
Write-Host ""
exit 1
