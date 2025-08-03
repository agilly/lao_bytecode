# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the 2025 MakerBox Bytecode project by Oliver Lee and Diya Thomas, focused on displaying Lao script text on OLED displays using Arduino microcontrollers. The project converts Lao Unicode text into bitmap representations optimized for embedded systems with limited memory.

## Project Structure

- **`lao_messages_app_variable_width/`** - Main production application with variable-width font rendering
- **`Experimentation/`** - Experimental code including Arduino prototypes and various bitmap generation approaches
- **`proposal/`** - Project proposal documentation
- **`interim/`** - Interim presentation materials
- **`www/`** - Jekyll-based project website hosted on GitHub Pages

## Key Development Commands

### Main Application Setup (lao_messages_app_variable_width)

```bash
# Fast setup (Linux/macOS)
chmod +x fast_setup_arduino_LINUX.sh
./fast_setup_arduino_LINUX.sh

# Fast setup (Windows PowerShell)
.\fast_setup_arduino_WINDOWS.ps1

# Manual setup
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR .\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

### Running the Application

```bash
cd lao_messages_app_variable_width
python run.py
```

The application will:
1. Prompt for input strings (or load from existing CSV)
2. Generate character bitmaps at specified height (30px recommended)
3. Create Arduino-compatible header files in `arduino_code/`

## Architecture Overview

### Python Application Pipeline
1. **Input Processing** (`preprocess_strings.py`):
   - Reads Lao text from CSV or user input
   - Decomposes strings into Unicode grapheme clusters
   - Builds character index mappings

2. **Bitmap Generation** (`generate_bitmaps.py`):
   - Uses HarfBuzz for proper Lao script shaping
   - Renders characters to bitmaps using FreeType
   - Optimizes for variable-width display
   - Exports as C++ header files with PROGMEM storage

3. **Output Files**:
   - `arduino_code/glyph_bitmaps.h` - Bitmap data arrays
   - `arduino_code/phrases_to_display.h` - Phrase index mappings
   - `input_files/input_strings.csv` - Input text data

### Arduino Code Architecture
- **Hardware**: Arduino Uno/Nano + SSD1306 128x64 OLED (I2C)
- **Libraries**: Adafruit GFX, Adafruit SSD1306, Wire
- **Memory Optimization**: Uses PROGMEM to store bitmaps in flash memory
- **Display Functions**:
  - `scrollPhrase()` - Scrolling text display
  - `staticPhrase()` - Static text display
  - `displayPhraseByIndex()` - Select phrases by index

## Hardware Requirements

- Arduino Uno or Nano
- SSD1306 128×64 OLED display
- I2C connection (SDA: A4, SCL: A5 on Uno)
- Power: 5V and GND connections

## Python Dependencies

Core libraries used:
- `freetype-py==2.5.1` - Font rendering
- `uharfbuzz==0.50.2` - Text shaping for complex scripts
- `pillow==11.2.1` - Image processing
- `grapheme==0.6.0` - Unicode grapheme cluster segmentation
- `tqdm==4.67.1` - Progress bars

## Font Files

The project uses `NotoSansLao-Regular.ttf` located in `font_files/` for rendering Lao script characters with proper Unicode support.

## Testing and Debugging

- The application includes a debug mode to visualize bitmap output
- Arduino serial monitor can be used to select phrases for display
- Hardware setup guide with wiring diagrams in README files

## Cross-Platform Compatibility

- Setup scripts provided for both Linux/macOS (`.sh`) and Windows (`.ps1`)
- Arduino code is portable to ESP32/ESP8266 and Raspberry Pi Pico with minor I2C pin modifications
- Display code supports other OLED/LCD/E-Ink displays through Adafruit GFX library

## Memory Considerations

The Arduino implementation uses PROGMEM extensively to store bitmap data in flash memory rather than RAM, critical for the Arduino Uno's 2KB RAM limitation.