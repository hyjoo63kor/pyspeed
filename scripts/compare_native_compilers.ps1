param(
    [string]$PythonPath = ".\.venv\Scripts\python.exe",
    [string]$OutputPath = "results\native_compiler_compare.txt",
    [string]$JsonOutputPath = "results\native_compiler_compare.json"
)

$ErrorActionPreference = "Stop"

$runId = Get-Date -Format "yyyyMMdd_HHmmss"
$targets = @(
    @{ Compiler = "gcc"; OutputPath = "native\build\pyspeed_native_gcc_compare_$runId.dll" },
    @{ Compiler = "clang"; OutputPath = "native\build\pyspeed_native_clang_compare_$runId.dll" }
)

foreach ($target in $targets) {
    & ".\scripts\build_native.ps1" -Compiler $target.Compiler -OutputPath $target.OutputPath
}

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$jsonOutputDir = Split-Path -Parent $JsonOutputPath
if ($jsonOutputDir -and -not (Test-Path $jsonOutputDir)) {
    New-Item -ItemType Directory -Path $jsonOutputDir -Force | Out-Null
}

$textLines = @(
    "generated_at  : $(Get-Date -Format s)"
    "profile       : quick"
    ""
    "Compiler comparison:"
    ""
)

$jsonItems = @()

foreach ($target in $targets) {
    $env:PYSPEED_NATIVE_DLL = $target.OutputPath
    $jsonText = & $PythonPath -m pyspeed cdll --profile quick --format json
    $result = $jsonText | ConvertFrom-Json | Select-Object -First 1
    $result | Add-Member -NotePropertyName compiler -NotePropertyValue $target.Compiler
    $result | Add-Member -NotePropertyName dll_path -NotePropertyValue $target.OutputPath
    $jsonItems += $result

    $textLines += "[$($target.Compiler)]"
    $textLines += "[cdll] $($result.description)"
    $textLines += "timer         : $($result.timer)"
    $textLines += ("baseline best : {0:N6}s" -f [double]$result.baseline_best)
    $textLines += ("optimized best: {0:N6}s" -f [double]$result.optimized_best)
    $textLines += ("speedup       : {0:N2}x" -f [double]$result.speedup)
    $textLines += "dll_path      : $($target.OutputPath)"
    $textLines += ""
}

Remove-Item Env:\PYSPEED_NATIVE_DLL -ErrorAction SilentlyContinue

$textLines | Set-Content -Path $OutputPath
$jsonItems | ConvertTo-Json -Depth 3 | Set-Content -Path $JsonOutputPath

$textLines

Write-Host ""
Write-Host "Saved compiler comparison to $OutputPath"
Write-Host "Saved compiler comparison JSON to $JsonOutputPath"
