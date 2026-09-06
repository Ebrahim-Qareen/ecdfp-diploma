<#
    scaffold.ps1 -- eCDFP Diploma, Phase 0

    Creates the Phase 0-1 folder tree (Part 2 of 00_INSTRUCTIONS.md, subset per D11)
    and initialises git with automatic maintenance DISABLED (Part 10, D14).

    IDEMPOTENT. Safe to re-run. It only ever creates; it never deletes, never
    overwrites an existing file, and never runs a git command that removes refs
    or objects (R3 / Part 10).

    Run from Windows PowerShell:
        powershell -ExecutionPolicy Bypass -File "E:\Work\ITgate\ECDFP_Course\tools\scaffold.ps1"
#>

[CmdletBinding()]
param(
    [string] $Root = 'E:\Work\ITgate\ECDFP_Course'
)

$ErrorActionPreference = 'Stop'

function Write-Step { param($m) Write-Host "`n== $m" -ForegroundColor Cyan }
function Write-Ok   { param($m) Write-Host "   [ok]   $m" -ForegroundColor Green }
function Write-Skip { param($m) Write-Host "   [skip] $m" -ForegroundColor DarkGray }
function Write-Warn { param($m) Write-Host "   [warn] $m" -ForegroundColor Yellow }

Write-Host ""
Write-Host "eCDFP Diploma -- Phase 0 scaffold" -ForegroundColor White
Write-Host "Root: $Root"

# ---------------------------------------------------------------- 1. the tree
# Only the folders Phase 0-1 needs (D11). knowledge_base, evidence, packages,
# cases, labs, scripts and the Phase 4 docs/ subfolders are created on first use.

$folders = @(
    'Resources\INE_eCDFP',
    'Resources\Instructor',
    'design',
    'docs\assets\css',
    'docs\assets\js',
    'docs\assets\img',
    'testing',
    'tools'
)

Write-Step "Folder tree (Phase 0-1 subset)"

if (-not (Test-Path -LiteralPath $Root)) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    Write-Ok "created root $Root"
}

foreach ($f in $folders) {
    $p = Join-Path $Root $f
    if (Test-Path -LiteralPath $p) {
        Write-Skip "$f"
    } else {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
        Write-Ok "$f"
    }
}

# GitHub Pages marker -- must exist from day one (D5, Part 13 action 4)
$nojekyll = Join-Path $Root 'docs\.nojekyll'
if (Test-Path -LiteralPath $nojekyll) {
    Write-Skip 'docs\.nojekyll'
} else {
    New-Item -ItemType File -Path $nojekyll -Force | Out-Null
    Write-Ok 'docs\.nojekyll'
}

# ------------------------------------------------------- 2. root files (guard)
# These are written by the build, not by this script. It only reports on them so
# a re-run never silently clobbers hand-edited content (R1: edit in place).

Write-Step "Root documents"

foreach ($f in @('00_INSTRUCTIONS.md','PROJECT.md','DECISIONS.md','.gitignore')) {
    $p = Join-Path $Root $f
    if (Test-Path -LiteralPath $p) { Write-Ok "$f present" }
    else { Write-Warn "$f MISSING -- Phase 0 is not complete without it" }
}

# ------------------------------------------------------------------- 3. git
# Part 10 / D14: git's automatic maintenance is what produces gc.lock and
# maintenance.lock on the device mount, and the mount cannot delete them.
# Both are turned off immediately after init, before git can ever schedule them.

Write-Step "git"

# git may not be on PATH. GitHub Desktop bundles its own copy and does not
# register it, so look there too before giving up -- and since the push goes
# through GitHub Desktop anyway (R11), its git is the one that matches.
function Resolve-Git {
    $onPath = Get-Command git -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }

    $candidates = @()

    # GitHub Desktop -- newest app-<version> wins
    $ghd = Join-Path $env:LOCALAPPDATA 'GitHubDesktop'
    if (Test-Path -LiteralPath $ghd) {
        $candidates += Get-ChildItem -LiteralPath $ghd -Directory -Filter 'app-*' -ErrorAction SilentlyContinue |
            Sort-Object {
                $v = $null
                if ([version]::TryParse(($_.Name -replace '^app-',''), [ref]$v)) { $v } else { [version]'0.0.0' }
            } -Descending |
            ForEach-Object { Join-Path $_.FullName 'resources\app\git\cmd\git.exe' }
    }

    # standard Git for Windows locations
    $candidates += @(
        (Join-Path $env:ProgramFiles 'Git\cmd\git.exe'),
        (Join-Path ${env:ProgramFiles(x86)} 'Git\cmd\git.exe'),
        (Join-Path $env:LOCALAPPDATA 'Programs\Git\cmd\git.exe')
    )

    foreach ($c in $candidates) { if ($c -and (Test-Path -LiteralPath $c)) { return $c } }
    return $null
}

$git = Resolve-Git
if (-not $git) {
    Write-Warn 'git not found -- install Git for Windows (winget install --id Git.Git -e), then re-run.'
    Write-Host ""
    exit 1
}
if ($git -like '*GitHubDesktop*') { Write-Ok "using GitHub Desktop's bundled git" }
Write-Host ("   " + $git) -ForegroundColor DarkGray

Push-Location $Root

# PowerShell 7.3+ turns a non-zero native exit code into a terminating error when
# ErrorActionPreference is Stop. That would kill the `git init -b main` fallback
# below on older git. Relax it for this block only, then restore it.
$savedEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$hasNativePref = Test-Path variable:PSNativeCommandUseErrorActionPreference
if ($hasNativePref) {
    $savedNative = $PSNativeCommandUseErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $false
}

try {
    if (Test-Path -LiteralPath (Join-Path $Root '.git')) {
        Write-Skip 'repository already initialised'
    } else {
        # -b main matters: Pages is served from main / /docs (D5)
        & $git init -b main 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            & $git init | Out-Null
            & $git symbolic-ref HEAD refs/heads/main | Out-Null
        }
        Write-Ok 'git init (default branch: main)'
    }

    & $git config gc.auto 0
    Write-Ok 'gc.auto = 0'

    & $git config maintenance.auto false
    Write-Ok 'maintenance.auto = false'

    Write-Host ""
    Write-Host "   verify:" -ForegroundColor DarkGray
    Write-Host ("     gc.auto           = " + (& $git config --get gc.auto))
    Write-Host ("     maintenance.auto  = " + (& $git config --get maintenance.auto))
    Write-Host ("     branch            = " + (& $git symbolic-ref --short HEAD))
}
finally {
    $ErrorActionPreference = $savedEap
    if ($hasNativePref) {
        $PSNativeCommandUseErrorActionPreference = $savedNative
    }
    Pop-Location
}

# -------------------------------------------------------------- 4. final tree

Write-Step "Tree"

Get-ChildItem -LiteralPath $Root -Recurse -Force |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.Name -ne '.git' } |
    Sort-Object FullName |
    ForEach-Object {
        $rel = $_.FullName.Substring($Root.Length).TrimStart('\')
        $depth = ($rel.ToCharArray() | Where-Object { $_ -eq '\' }).Count
        $pad = '  ' * $depth
        if ($_.PSIsContainer) { Write-Host "$pad$($_.Name)\" -ForegroundColor Cyan }
        else                  { Write-Host "$pad$($_.Name)" }
    }

Write-Host ""
Write-Host "Phase 0 scaffold complete." -ForegroundColor Green
Write-Host "Next: create the 6 ecdfp- skills, then Phase 1." -ForegroundColor DarkGray
Write-Host ""
