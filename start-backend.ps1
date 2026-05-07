$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $repoRoot "backend"
$bundledVenvDir = Join-Path $backendDir "venv"
$localVenvDir = Join-Path $backendDir ".venv"
$venvDir = $bundledVenvDir
$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$requirementsFile = Join-Path $backendDir "requirements.txt"

function Test-PythonCommand {
    param(
        [string]$Command,
        [string[]]$Arguments = @()
    )

    try {
        & $Command @Arguments --version *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Find-PythonCommand {
    $candidates = @(
        @{ Command = "py"; Arguments = @("-3.11") },
        @{ Command = "py"; Arguments = @("-3") },
        @{ Command = "python"; Arguments = @() },
        @{ Command = "python3"; Arguments = @() }
    )

    foreach ($candidate in $candidates) {
        if (Test-PythonCommand -Command $candidate.Command -Arguments $candidate.Arguments) {
            return $candidate
        }
    }

    return $null
}

function Test-VenvPython {
    if (-not (Test-Path $pythonExe)) {
        return $false
    }

    return Test-PythonCommand -Command $pythonExe
}

function Test-BackendDependencies {
    try {
        & $pythonExe -c "import fastapi, uvicorn, sqlalchemy, psycopg2" *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

if (-not (Test-VenvPython)) {
    $venvDir = $localVenvDir
    $pythonExe = Join-Path $venvDir "Scripts\python.exe"
}

if (-not (Test-VenvPython)) {
    $pythonCommand = Find-PythonCommand

    if ($null -ne $pythonCommand) {
        Write-Host "Creating backend virtual environment at $venvDir ..."
        $venvArgs = $pythonCommand.Arguments + @("-m", "venv", $venvDir)
        & $pythonCommand.Command @venvArgs
        if ($LASTEXITCODE -ne 0 -or -not (Test-VenvPython)) {
            Write-Error "Could not create a working backend virtual environment."
            exit 1
        }
    } elseif (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Host "Python 3.11 was not found. Using uv to create the backend virtual environment ..."
        & uv venv --python 3.11 $venvDir
        if ($LASTEXITCODE -ne 0 -or -not (Test-VenvPython)) {
            Write-Error "Could not create a working backend virtual environment with uv."
            exit 1
        }
    } else {
        Write-Error "Python 3.11+ was not found. Install Python 3.11, reopen PowerShell, then run .\start-backend.ps1 again."
        exit 1
    }
}

if (-not (Test-BackendDependencies)) {
    Write-Host "Installing backend dependencies ..."
    & $pythonExe -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & $pythonExe -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & $pythonExe -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Set-Location $backendDir
& $pythonExe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
