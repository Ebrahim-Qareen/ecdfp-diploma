# 06_symbols_airgap.ps1 — eCDFP FOR-WS01 :: pre-stage Volatility 3 Windows symbols (D2, air-gap)
# On a box WITH internet, Volatility fetches symbols on demand. For the air-gapped student image,
# ship the symbol pack so memory analysis works offline. Volatility reads the .zip in place - no extraction.

$py = "C:\Python314\python.exe"
$symdir = (& $py -c "import volatility3, os; print(os.path.join(os.path.dirname(volatility3.__file__),'symbols'))").Trim()
New-Item -ItemType Directory -Force -Path $symdir | Out-Null
Write-Host "Symbols dir: $symdir" -ForegroundColor Cyan
try {
    Invoke-WebRequest "https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip" -OutFile "$symdir\windows.zip" -UseBasicParsing
    Write-Host "  [OK] windows.zip staged (Volatility reads it in place)" -ForegroundColor Green
} catch { Write-Host "  [FAIL] symbol pack - manual: https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip" -ForegroundColor Red }
