<#
.SYNOPSIS
  Setup Python venv, install dependencies, run app, and launch Arduino IDE with sketch.

.DESCRIPTION
  Run this from the root of the GitHub repo. It:
    - Navigates to `lao_messages_app_variable_width`
    - Creates/activates a Python virtual environment
    - Installs dependencies from requirements.txt
    - Runs run.py
    - Tries to launch Arduino IDE with the sketch folder

.EXAMPLE
  .\fast_setup_arduino_WINDOWS.ps1

.NOTES
  If PowerShell blocks the script, run:
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#>

# Store original repo root
$projectDir = Get-Location
$venvPath = Join-Path $projectDir ".venv"
$reqsFile = Join-Path $projectDir "requirements.txt"
$runPyFile = Join-Path $projectDir "run.py"
$sketchFolder = Join-Path $projectDir "arduino_code"

# Navigate to project directory
Set-Location $projectDir

# Create virtual environment if needed
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists."
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
. "$venvPath\Scripts\Activate.ps1"

# Install dependencies
if (Test-Path $reqsFile) {
    Write-Host "Installing Python dependencies..."
    pip install -r $reqsFile
} else {
    Write-Host "requirements.txt not found at $reqsFile"
}

# Run the Python app
if (Test-Path $runPyFile) {
    Write-Host "Running run.py..."
    python $runPyFile
} else {
    Write-Host "run.py not found at $runPyFile"
}

# Locate Arduino IDE
Write-Host "Searching for Arduino IDE..."

# Known install paths
$arduinoPaths = @(
    "$Env:ProgramFiles\Arduino\arduino.exe",
    "$Env:ProgramFiles(x86)\Arduino\arduino.exe",
    "$Env:LocalAppData\Programs\Arduino IDE\Arduino IDE.exe"
)

# Fallback: resolve shortcut
$startMenuLnk = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Arduino IDE.lnk"

function Resolve-ShortcutTarget($shortcutPath) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    return $shortcut.TargetPath
}

$arduinoExe = $null

# Try known locations
foreach ($path in $arduinoPaths) {
    if (Test-Path $path) {
        $arduinoExe = $path
        break
    }
}

# Try shortcut
if (-not $arduinoExe -and (Test-Path $startMenuLnk)) {
    $resolvedPath = Resolve-ShortcutTarget $startMenuLnk
    if (Test-Path $resolvedPath) {
        $arduinoExe = $resolvedPath
    }
}

# Launch or explain
if ($arduinoExe) {
    if (Test-Path $sketchFolder) {
        Write-Host "Launching Arduino IDE with sketch folder: $sketchFolder"
        Start-Process "`"$arduinoExe`"" "`"$sketchFolder`""
    } else {
        Write-Host "Arduino sketch folder not found at: $sketchFolder"
        Write-Host "Please ensure the sketch files are inside: $sketchFolder"
    }
} else {
    Write-Host "Arduino IDE not found."
    Write-Host "Please install it from: https://www.arduino.cc/en/software"
    if (Test-Path $sketchFolder) {
        Write-Host "You can then manually open the sketch folder: $sketchFolder"
    }
}

# Restore working directory
Set-Location $projectDir

