param(
    [string]$PythonPath = ".\.venv\Scripts\python.exe",
    [string]$OutputPath = "results\latest.txt",
    [string]$JsonOutputPath = "results\latest.json",
    [string]$SummaryOutputPath = "results\latest_summary.txt",
    [ValidateSet("timeit", "perf_counter_ns")]
    [string]$TimerName = "timeit",
    [ValidateSet("quick", "full")]
    [string]$ProfileName = "quick",
    [string[]]$SkipCases = @()
)

$ErrorActionPreference = "Stop"

foreach ($path in @($OutputPath, $JsonOutputPath, $SummaryOutputPath)) {
    $outputDir = Split-Path -Parent $path
    if ($outputDir -and -not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir | Out-Null
    }
}

$header = @(
    "generated_at  : $(Get-Date -Format s)"
    "timer         : $TimerName"
    "profile       : $ProfileName"
    "skip_cases    : $($SkipCases -join ', ')"
    ""
)

$skipArgs = @()
foreach ($caseName in $SkipCases) {
    $skipArgs += @("--skip-case", $caseName)
}

$textOutput = & $PythonPath -m pyspeed all --timer $TimerName --profile $ProfileName @skipArgs
$jsonOutput = & $PythonPath -m pyspeed all --timer $TimerName --format json --profile $ProfileName @skipArgs

$header + $textOutput | Set-Content -Path $OutputPath
$jsonOutput | Set-Content -Path $JsonOutputPath

$summaryOutput = & $PythonPath .\scripts\summarize_results.py $JsonOutputPath
$summaryOutput | Set-Content -Path $SummaryOutputPath

$header + $textOutput
Write-Host ""
$summaryOutput

Write-Host ""
Write-Host "Saved benchmark output to $OutputPath"
Write-Host "Saved benchmark JSON to $JsonOutputPath"
Write-Host "Saved benchmark summary to $SummaryOutputPath"
