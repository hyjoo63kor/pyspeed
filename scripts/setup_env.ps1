param(
    [string]$PythonVersion = "3.12",
    [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"
$env:UV_NO_CACHE = "1"
$venvPython = ".\$VenvPath\Scripts\python.exe"
$activateScript = ".\$VenvPath\Scripts\Activate.ps1"

if ((Test-Path $venvPython) -and (Test-Path $activateScript)) {
    Write-Host "Virtual environment already exists at $VenvPath"
} else {
    if (Test-Path $VenvPath) {
        Write-Host "Removing incomplete virtual environment at $VenvPath"
        Remove-Item -LiteralPath $VenvPath -Recurse -Force
    }

    Write-Host "Creating virtual environment at $VenvPath"
    uv venv $VenvPath --python $PythonVersion
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython) -or -not (Test-Path $activateScript)) {
        throw "Failed to create a complete virtual environment at $VenvPath."
    }
}

Write-Host "Python version in venv:"
& $venvPython -V

Write-Host ""
Write-Host "Installing project dependencies into $VenvPath"
uv pip install --python $venvPython -e .
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install project dependencies into $VenvPath."
}

Write-Host ""
Write-Host "Try these commands next:"
Write-Host "  .\$VenvPath\Scripts\Activate.ps1"
Write-Host "  python -m pyspeed --list"
Write-Host "  python -m pyspeed all"
