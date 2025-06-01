# Compact Lao Messages App for Arduino

This project provides a Python-based pipeline for:

Reading Unicode text (including complex scripts like Lao),
Decomposing each string into human-readable grapheme clusters,
Rasterizing each grapheme using a chosen font,
Generating C++ header files to display text on a pixel-based embedded display (e.g., Arduino).

## The main output:

Main output files are found in the arduino_code folder

1. scrolling_messages.ino : An example of code for displaying a scrolling message on an OLED screem
2. glyph_bitmaps.h : auto-generated header file, containing the bitmaps
3. phrases_to_display.h : auto-generated header file, containing the indexes into the bitmap list for each character of each phrase

## Features

Supports any script thanks to HarfBuzz and FreeType.
1. Clone the Repository
git clone https://github.com/your-username/grapheme-bitmap-generator.git
cd compact_lao_messages_app
2. Create a Virtual Environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
Required packages include:

Pillow
freetype-py
uharfbuzz
grapheme
tqdm
You may also need system-level dependencies like freetype-dev.

## How to Run

1. python3 run.py

### What Happens:
If input.csv already exists, it is loaded and processed.
If input.csv does not exist, you will be prompted to enter phrases one at a time in the terminal.
Each phrase is broken into grapheme clusters and rasterized to 30×30 black & white bitmaps.
### Outputs:
./arduino_code/glyph_bitmaps.h
./arduino_code/phrases_to_display.h

1. Clone the Repository
git clone https://github.com/your-username/grapheme-bitmap-generator.git
cd compact_lao_messages_app
2. Create a Virtual Environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
Required packages include:

Pillow
freetype-py
uharfbuzz
grapheme
tqdm
You may also need system-level dependencies like freetype-dev.

## How to Run

1. python3 run.py

### What Happens:
If input.csv already exists, it is loaded and processed.
If input.csv does not exist, you will be prompted to enter phrases one at a time in the terminal.
Each phrase is broken into grapheme clusters and rasterized to 30×30 black & white bitmaps.
### Outputs:
./arduino_code/glyph_bitmaps.h
./arduino_code/phrases_to_display.h