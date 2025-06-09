#!/bin/bash

# .SYNOPSIS
#   Setup Python venv, install dependencies, run app, and launch Arduino IDE with sketch.

# .DESCRIPTION
#   Run this from the root of the GitHub repo. It:
#     - Navigates to `lao_messages_app_variable_width` (assuming this is the current directory or a subdirectory)
#     - Creates/activates a Python virtual environment
#     - Installs dependencies from requirements.txt
#     - Runs run.py
#     - Tries to launch Arduino IDE with the sketch folder

# .EXAMPLE
#   ./fast_setup_arduino_LINUX.sh

# .NOTES
#   Make sure the script is executable: chmod +x fast_setup_arduino_LINUX.sh

# Store original repo root
projectDir=$(pwd)
venvPath="$projectDir/.venv"
reqsFile="$projectDir/requirements.txt"
runPyFile="$projectDir/run.py"
sketchFolder="$projectDir/arduino_code"

# Navigate to project directory (already there if script run from root)
cd "$projectDir"

# Create virtual environment if needed
if [ ! -d "$venvPath" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$venvPath"
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$venvPath/bin/activate"

# Install dependencies
if [ -f "$reqsFile" ]; then
    echo "Installing Python dependencies..."
    pip install -r "$reqsFile"
else
    echo "requirements.txt not found at $reqsFile"
fi

# Run the Python app
if [ -f "$runPyFile" ]; then
    echo "Running run.py..."
    python "$runPyFile" & # Run in background so the script can continue
    # Store the PID of the Python process
    PYTHON_PID=$!
else
    echo "run.py not found at $runPyFile"
fi

# Locate Arduino IDE
echo "Searching for Arduino IDE..."

# Known install paths and common executable names
arduinoExecutables=(
    "arduino" # Common symlink or executable name
    "/usr/bin/arduino"
    "/opt/arduino/arduino"
    "$HOME/arduino-ide/arduino-ide" # Common for manual installs
)

arduinoExe=""

# Try known locations
for path in "${arduinoExecutables[@]}"; do
    if command -v "$path" &> /dev/null; then
        arduinoExe="$path"
        break
    elif [ -f "$path" ]; then # Check if it's a file, not necessarily in PATH
        arduinoExe="$path"
        break
    fi
done

# Launch or explain
if [ -n "$arduinoExe" ]; then
    if [ -d "$sketchFolder" ]; then
        echo "Launching Arduino IDE with sketch folder: $sketchFolder"
        # Use 'nohup' and '&' to detach the Arduino IDE from the terminal
        nohup "$arduinoExe" "$sketchFolder" &>/dev/null &
    else
        echo "Arduino sketch folder not found at: $sketchFolder"
        echo "Please ensure the sketch files are inside: $sketchFolder"
    fi
else
    echo "Arduino IDE not found."
    echo "Please install it, or ensure it's in your PATH or one of the common install locations."
    echo "Common download page: https://www.arduino.cc/en/software"
    if [ -d "$sketchFolder" ]; then
        echo "You can then manually open the sketch folder: $sketchFolder"
    fi
fi

# Deactivate the virtual environment when the script finishes
deactivate

echo "Setup script finished."
echo "The Python application (run.py) is running in the background (PID: $PYTHON_PID)."
echo "You may need to manually stop it later, or it will stop when you close your terminal."