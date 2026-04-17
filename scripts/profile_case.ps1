param(
    [Parameter(Mandatory = $true)]
    [string]$Case,
    [string]$PythonPath = ".\.venv\Scripts\python.exe",
    [string]$OutputPath = "results\$Case.prof"
)

$ErrorActionPreference = "Stop"

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

& $PythonPath -m cProfile -o $OutputPath -m pyspeed $Case

Write-Host ""
Write-Host "Profile saved to $OutputPath"
Write-Host "Inspect with:"
Write-Host "  $PythonPath -m pstats $OutputPath"
