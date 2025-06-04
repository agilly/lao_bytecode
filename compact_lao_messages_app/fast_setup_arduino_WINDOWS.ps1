<#
.SYNOPSIS
    Setup Python virtual environment, install dependencies, and launch Arduino IDE with specified sketch.

.DESCRIPTION
    This script assumes you are running it from the root directory of the cloned Git repository.
    It will:
    - Change into the 'compact_lao_messages_app' folder
    - Create and activate a Python virtual environment if not already present
    - Install Python dependencies from requirements.txt
    - Detect the Arduino IDE installation path
    - Launch Arduino IDE opening the sketch located in 'compact_lao_messages_app\arduino_code'

.PARAMETER None
    No parameters needed. The script uses the current directory as the project root.
<#
.SYNOPSIS
  Setup Python virtual environment, install dependencies, run Python app, then open Arduino IDE with sketch.

.DESCRIPTION
  This script should be run from the root of the cloned Git repo.
  It will:
    - Change directory to 'compact_lao_messages_app'
    - Create and activate a Python virtual environment if not already present
    - Install required Python packages from requirements.txt
    - Run run.py inside the virtual environment
    - Search for the Arduino IDE executable and open the Arduino sketch folder in it
    - If Arduino IDE is missing, instruct the user to install it
    - If Arduino sketch folder is missing, inform the user where it expects the sketch

.EXAMPLE
  .\fast_setup_arduino_WINDOWS.ps1

.NOTES
  Requires PowerShell execution policy to allow running scripts.
#>

# Get current directory (should be repo root)
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

# Launch Arduino IDE with the sketch folder or give info if missing
if ($arduinoExe) {
    if (Test-Path $sketchFolder) {
        Write-Host "🚀 Launching Arduino IDE with sketch folder: $sketchFolder"
        Start-Process "`"$arduinoExe`"" "`"$sketchFolder`""
    } else {
        Write-Host "❌ Arduino sketch folder not found at expected path: $sketchFolder"
        Write-Host "ℹ️ Please verify your Arduino sketch files are located there."
    }
} else {
    Write-Host "❌ Arduino IDE not found. Please install it first from: https://www.arduino.cc/en/software"
}

# Return to original directory if needed
Set-Location $repoRoot

.EXAMPLE
    PS C:\> cd C:\path\to\cloned\repo
    PS C:\path\to\cloned\repo> .\setup_and_open_arduino.ps1

.NOTES
    - Ensure PowerShell execution policy allows running scripts:
      Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#>

# Get current repo root directory (where PowerShell was opened)
$repoRoot = (Get-Location).Path

# Change directory to compact_lao_messages_app inside the repo
$projectDir = Join-Path $repoRoot "compact_lao_messages_app"
Set-Location $projectDir

$venvPath = "$projectDir\.venv"
$reqsFile = "$projectDir\requirements.txt"

# Arduino sketch folder inside compact_lao_messages_app
$sketchFolder = Join-Path $projectDir "arduino_code"

# Attempt to locate Arduino IDE executable
$arduinoPaths = @(
    "$Env:ProgramFiles\Arduino\arduino.exe",
    "$Env:ProgramFiles(x86)\Arduino\arduino.exe",
    "$Env:LocalAppData\Programs\Arduino IDE\Arduino IDE.exe"
)

$arduinoExe = $null
foreach ($path in $arduinoPaths) {
    if (Test-Path $path) {
        $arduinoExe = $path
        break
    }
}

if (-not $arduinoExe) {
    Write-Host "❌ Arduino IDE not found. Please install it first: https://www.arduino.cc/en/software"
    exit 1
}

# Create virtual environment if needed
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "🔧 Creating virtual environment..."
    python -m venv $venvPath
}

# Activate virtual environment
Write-Host "✅ Activating virtual environment..."
. "$venvPath\Scripts\Activate.ps1"

# Install requirements
if (Test-Path $reqsFile) {
    Write-Host "📦 Installing Python dependencies..."
    pip install -r $reqsFile
} else {
    Write-Host "⚠️  No requirements.txt found."
}

# Launch Arduino IDE with the sketch folder
if (Test-Path $sketchFolder) {
    Write-Host "🚀 Launching Arduino IDE with sketch..."
    Start-Process "`"$arduinoExe`"" "`"$sketchFolder`""
} else {
    Write-Host "❌ Sketch folder not found: $sketchFolder"
}
