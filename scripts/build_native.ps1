param(
    [string]$Compiler = "gcc",
    [string]$SourcePath = "native\pyspeed_native.c",
    [string]$OutputPath = "native\build\pyspeed_native.dll"
)

$ErrorActionPreference = "Stop"

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

switch ($Compiler) {
    "gcc" {
        $gccCandidates = @(
            "C:\c\bin\gcc.exe",
            "gcc"
        )
        $gccCommand = $gccCandidates | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } | Select-Object -First 1
        if (-not $gccCommand) {
            throw "gcc compiler not found. Checked C:\c\bin\gcc.exe and PATH."
        }
        & $gccCommand -shared -O3 -o $OutputPath $SourcePath
    }
    "clang" {
        & clang -shared -O3 -o $OutputPath $SourcePath
    }
    default {
        throw "Unsupported compiler: $Compiler"
    }
}

if ($LASTEXITCODE -ne 0 -or -not (Test-Path $OutputPath)) {
    throw "Failed to build native library at $OutputPath."
}

Write-Host "Built native library at $OutputPath"
