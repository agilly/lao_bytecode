<#
.SYNOPSIS
  Setup Python virtual environment, install dependencies, run the app, then open Arduino IDE.

.DESCRIPTION
  This script should be run from the root of the cloned GitHub repository.
  It will:
    - Change directory into 'compact_lao_messages_app'
    - Create and activate a Python virtual environment if missing
    - Install required Python packages from requirements.txt
    - Run run.py inside the virtual environment
    - Search for the Arduino IDE executable and open the Arduino sketch folder
    - If Arduino IDE is missing, it informs the user
    - If the Arduino sketch folder is missing, it also provides guidance

.EXAMPLE
  .\fast_setup_arduino_WINDOWS.ps1

.NOTES
  Make sure PowerShell allows running local scripts:
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#>

# Get current directory (assumed repo root)
$repoRoot = Get-Location
$projectDir = Join-Path $repoRoot "compact_lao_messages_app"
$venvPath = Join-Path $projectDir ".venv"
$reqsFile = Join-Path $projectDir "requirements.txt"
$runPyFile = Join-Path $projectDir "run.py"
$sketchFolder = Join-Path $projectDir "arduino_code"

# Change to project directory
Set-Location $projectDir

# Create virtual environment if missing
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "🔧 Creating virtual environment..."
    python -m venv $venvPath
} else {
    Write-Host "✅ Virtual environment already exists."
}

# Activate virtual environment
Write-Host "✅ Activating virtual environment..."
. "$venvPath\Scripts\Activate.ps1"

# Install Python requirements
if (Test-Path $reqsFile) {
    Write-Host "📦 Installing Python dependencies from requirements.txt..."
    pip install -r $reqsFile
} else {
    Write-Host "⚠️  requirements.txt not found at $reqsFile"
}

# Run the Python app
if (Test-Path $runPyFile) {
    Write-Host "▶️ Running run.py..."
    python $runPyFile
} else {
    Write-Host "❌ run.py not found at $runPyFile"
}

# === Find Arduino IDE executable ===

Write-Host "🔍 Searching for Arduino IDE executable..."

# Search LocalAppData\Programs recursively for arduino*.exe
$foundArduinoExe = Get-ChildItem -Path "$Env:LocalAppData\Programs" -Filter "arduino*.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($foundArduinoExe) {
    $arduinoExe = $foundArduinoExe.FullName
    Write-Host "✅ Found Arduino IDE at: $arduinoExe"
} else {
    # Fallback common locations
    $arduinoPaths = @(
        "$Env:ProgramFiles\Arduino\arduino.exe",
        "$Env:ProgramFiles(x86)\Arduino\arduino.exe",
        "$Env:LocalAppData\Programs\Arduino IDE\Arduino IDE.exe"
    )
    $arduinoExe = $null
    foreach ($path in $arduinoPaths) {
        if (Test-Path $path) {
            $arduinoExe = $path
            Write-Host "✅ Found Arduino IDE at fallback path: $arduinoExe"
            break
        }
    }
}

# Launch Arduino IDE with the sketch folder or provide message
if ($arduinoExe) {
    if (Test-Path $sketchFolder) {
        Write-Host "🚀 Launching Arduino IDE with sketch folder: $sketchFolder"
        Start-Process "`"$arduinoExe`"" "`"$sketchFolder`""
    } else {
        Write-Host "❌ Arduino sketch folder not found at: $sketchFolder"
        Write-Host "ℹ️ Make sure your Arduino files are in that folder before trying again."
    }
} else {
    Write-Host "❌ Arduino IDE not found."
    Write-Host "📥 Please install it from: https://www.arduino.cc/en/software"
}

# Return to root
Set-Location $repoRoot
