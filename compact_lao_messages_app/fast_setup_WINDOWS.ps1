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
