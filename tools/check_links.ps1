<#
    check_links.ps1 -- eCDFP Diploma
    Part 9 link gate: every href / src / download in docs\ must resolve.
    Local paths are resolved on disk. External hosts are DNS-resolved only --
    no page is fetched, so the check works on a classroom machine behind a
    filter and never depends on a third-party site being up.

    Usage:  powershell -ExecutionPolicy Bypass -File tools\check_links.ps1
            -Root <path>       defaults to the repo root
            -SkipExternal      skip DNS resolution entirely (offline runs)
#>
[CmdletBinding()]
param([string] $Root, [switch] $SkipExternal)

$ErrorActionPreference = 'Stop'
if (-not $Root) { $Root = Split-Path -Parent $PSScriptRoot }
$docs = Join-Path $Root 'docs'

if (-not (Test-Path -LiteralPath $docs)) { Write-Host "no docs\ folder -- nothing to check"; exit 0 }

$bad  = New-Object System.Collections.Generic.List[object]
$hosts = New-Object System.Collections.Generic.HashSet[string]
$pages = Get-ChildItem -LiteralPath $docs -Recurse -File -Filter *.html

Write-Host ""
Write-Host "check_links -- $docs" -ForegroundColor White
Write-Host "`n== local targets" -ForegroundColor Cyan

foreach ($p in $pages) {
    $html = Get-Content -LiteralPath $p.FullName -Raw
    $dir  = Split-Path -Parent $p.FullName
    $refs = [regex]::Matches($html, '(?i)\b(?:href|src|download)\s*=\s*["'']([^"'']+)["'']') |
            ForEach-Object { $_.Groups[1].Value }

    foreach ($r in $refs) {
        if ([string]::IsNullOrWhiteSpace($r)) { continue }
        if ($r.StartsWith('#') -or $r.StartsWith('data:') -or $r.StartsWith('mailto:') -or $r.StartsWith('javascript:')) { continue }

        if ($r -match '^(https?:)?//') {
            if ($r -match '^(?:https?:)?//([^/]+)') { [void]$hosts.Add($Matches[1]) }
            continue
        }

        $clean = ($r -split '[#?]')[0]
        if ([string]::IsNullOrWhiteSpace($clean)) { continue }
        $target = Join-Path $dir ($clean -replace '/','\')
        if (-not (Test-Path -LiteralPath $target)) {
            $bad.Add([pscustomobject]@{ Kind='local'; Page=$p.FullName.Replace($Root,'').TrimStart('\'); Ref=$r })
        }
    }
}
Write-Host ("   {0} page(s) scanned, {1} broken local reference(s)" -f $pages.Count, $bad.Count)

Write-Host "`n== external hosts" -ForegroundColor Cyan
if ($SkipExternal) {
    Write-Host "   skipped (-SkipExternal)"
} elseif ($hosts.Count -eq 0) {
    Write-Host "   none referenced"
} else {
    foreach ($h in $hosts) {
        try {
            $null = [System.Net.Dns]::GetHostEntry($h)
            Write-Host "   [ok]   $h" -ForegroundColor Green
        } catch {
            Write-Host "   [FAIL] $h" -ForegroundColor Red
            $bad.Add([pscustomobject]@{ Kind='dns'; Page='(external)'; Ref=$h })
        }
    }
}

Write-Host ""
if ($bad.Count -eq 0) { Write-Host "CLEAN" -ForegroundColor Green; Write-Host ""; exit 0 }
Write-Host "$($bad.Count) BROKEN REFERENCE(S) -- PUSH BLOCKED" -ForegroundColor Red
$bad | ForEach-Object { Write-Host ("        [{0}] {1}  ->  {2}" -f $_.Kind, $_.Page, $_.Ref) }
Write-Host ""
exit 1
