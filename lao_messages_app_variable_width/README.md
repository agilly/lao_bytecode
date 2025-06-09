# `lao_messages_app_variable_width` Setup Guide

This guide explains how to set up and run the `lao_messages_app_variable_width` project on both Linux-based systems and Windows.

---

## **Prerequisites**

Before you begin, please ensure you have the following software installed on your system.

* **Python 3:** Required to run the application's backend scripts.
    * Download from the official [Python website](https://www.python.org/downloads/).
    * **Windows Users:** During installation, make sure to check the box that says **"Add Python to PATH"**.

* **Git:** Needed to clone the project repository from GitHub.
    * Install from the official [Git website](https://git-scm.com/downloads).
    * **Windows Users:** We recommend using **Git Bash**, which is included with the Git for Windows installation, for a command-line experience similar to Linux.

* **Arduino IDE:** Recommended to be installed to upload the code to your Arduino board.
    * Download from the official [Arduino Software page](https://www.arduino.cc/en/software).

---

## **Linux & macOS Setup**

### Method 1: Fast Setup Script ⚡

This method uses the provided shell script to automate the setup process.

1.  **Open Your Terminal:** Navigate to a suitable folder where you want to store the project.
    ```bash
    cd /path/to/your/folder
    ```

2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git](https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git)
    ```

3.  **Navigate to Project Folder:**
    ```bash
    cd 2025-MakerBox-Bytecode/lao_messages_app_variable_width
    ```

4.  **Make the Script Executable:**
    ```bash
    chmod +x fast_setup_arduino_LINUX.sh
    ```

5.  **Run the Setup Script:**
    ```bash
    ./fast_setup_arduino_LINUX.sh
    ```
    The script will guide you through the rest of the setup.

### Method 2: Manual Setup 🛠️

Follow these steps if you prefer to set up the project manually.

1.  **Create a Python Virtual Environment:** This isolates your project's dependencies.
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
    Your terminal prompt should now show `(.venv)`.

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Python Application:**
    ```bash
    python run.py
    ```

5.  **Launch Arduino IDE:**
    Open the Arduino IDE and load the project sketch from:
    `.../lao_messages_app_variable_width/arduino_code/`

    You will need to open the main sketch file:
    * `arduino_code.ino`

6.  **Deactivate Virtual Environment:** When you are finished, you can exit the virtual environment:
    ```bash
    deactivate
    ```

---

## **Windows Setup**

Windows users should follow the manual setup instructions.

### Manual Setup 🛠️

1.  **Open a Terminal:** We recommend using **Git Bash** for these commands. You can also use Command Prompt (CMD) or PowerShell.

2.  **Clone the Repository:** Navigate to a suitable folder and run:
    ```bash
    git clone [https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git](https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git)
    ```

3.  **Navigate to Project Folder:**
    ```bash
    cd 2025-MakerBox-Bytecode/lao_messages_app_variable_width
    ```

4.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv .venv
    ```

5.  **Activate the Virtual Environment:** This command is different from Linux.
    ```bash
    # In Git Bash or PowerShell
    source .venv/Scripts/activate

    # Or in Windows Command Prompt (CMD)
    .\.venv\Scripts\activate
    ```
    Your command prompt should now be prefixed with `(.venv)`.

6.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

7.  **Run the Python Application:**
    ```bash
    python run.py
    ```

8.  **Launch Arduino IDE:**
    Open the Arduino IDE and load the project sketch from:
    `...\lao_messages_app_variable_width\arduino_code\`

    You will need to open the main sketch file:
    * `arduino_code.ino`

9.  **Deactivate Virtual Environment:** When you are done, simply run:
    ```bash
    deactivate
    ```















# Linux Setup Guide for `lao_messages_app_variable_width`

This guide explains how to use the `fast_setup_arduino_LINUX.sh` script (and how to setup manually if you prefer)

## Prerequisites

**Python 3:** Ensure Python 3 is installed.  
    * For more details refer to the official [Python website](https://www.python.org/downloads/linux/)

**Git:** Needed to clone the repository.  
    * For more details visit the [Git website](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

**Arduino IDE:** Recommended to be installed *before* starting this guide.
    * If not, follow the instructions at the official [Arduino Software page](https://www.arduino.cc/en/software).

## To run `fast_setup_arduino_LINUX.sh`

1. Open your terminal and navigate to a suitable folder.  

```bash
cd /path/to/desired/folder
```

2. Clone the Repository:  

```bash
git clone https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git
```

3. Navigate into the repository and the `lao_messages_app_variable_width`

```bash
cd 2025-MakerBox-Bytecode/lao_messages_app_variable_width
```

4. Give permissions

```bash
chmod +x fast_setup_arduino_LINUX.sh
```

5. Run the setup wizard!

```bash
./fast_setup_arduino_LINUX.sh
```

## Next steps (without using the script)

1.  **Create a Python Virtual Environment:**
    A virtual environment keeps your project's Python dependencies isolated, preventing conflicts with other Python projects or your system's Python installation.

    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the Virtual Environment:**
    You'll typically see `(.venv)` or a similar indicator in your terminal prompt, signifying that the virtual environment is active. This ensures that any Python commands you run use the dependencies within this isolated environment.

    ```bash
    source .venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    This command reads the `requirements.txt` file and installs all the necessary Python libraries that your project depends on into your active virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Python Application:**
    This starts your Python application (`run.py`).

    ```bash
    python run.py
    ```

5.  **Launch Arduino IDE:**
    Open your Arduino IDE and load the project's sketch files located in the `2025-MakerBox-Bytecode/lao_messages_app_variable_width/arduino_code` folder.  

    There will be: 
    * arduino_code.ino
    * glyph_bitmaps.h
    * phrases_to_display.h

6.  **Deactivate Virtual Environment:**
    When you are finished, you can exit the virtual environment:

    ```bash
    deactivate
    ```
















# Compact Lao Messages App for Arduino

This project provides a Python-based pipeline for:

Reading Unicode text (including complex scripts like Lao),
Decomposing each string into human-readable grapheme clusters,
Rasterizing each grapheme using a chosen font,
Generating C++ header files to display text on a pixel-based embedded display (e.g., Arduino).

Supports any script thanks to HarfBuzz and FreeType.

## Setup

1. Clone the Repository:  
`git clone https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git'
`cd compact_lao_messages_app`  
2. Create a Virtual Environment:  
`python -m venv .venv`  
`source .venv/bin/activate`   # On Windows: `.venv\Scripts\activate`
3. Install Dependencies:  
`pip install -r requirements.txt`  

    Required packages include:
    * Pillow
    * freetype-py
    * uharfbuzz
    * grapheme
    * tqdm

    You may also need system-level dependencies like freetype-dev.

## Run

1. `python run.py` # For some Windows machines: `py -m run.py` (from within the `compact_lao_messages_app` directory)

### Main Loop Explanation

1.  Input String Handling

    CSV Check:  
    The app looks for `./input_files/input_strings.csv`, which stores Lao strings to convert. An example input_strings.csv file for editing can be found under the input_files folder.

    Overwrite Prompt:  
    If the file exists, it asks the user whether to overwrite it.
    
    If the user chooses to overwrite (y):  
    It prompts the user for new strings (`get_input_strings()`).
    Saves them to CSV using `save_strings_to_csv()`.

    Otherwise:  
    It loads the existing strings from the CSV.

3.  Character Analysis

    Build Unique Characters:  
    It extracts all unique characters across the input strings and builds:
    `char_list`: the sorted list of unique characters.
    `index_list`: a list of indices representing which characters form each phrase.

     Debug Print:
    Displays both lists for developer inspection using `print_char_and_index_lists()`.

4.  Bitmap Generation

    Create Bitmaps:  
    It generates monochrome bitmap images (bit-packed) for each unique character using `generate_bitmaps_for_chars()`.
    These are written to a C header file: `./arduino_code/glyph_bitmaps.h`

5.  Index Header Export

    Write Index List:  
    The index_list, which maps phrases to character indices, is exported to another header file:
    `./arduino_code/phrases_to_display.h`
    This allows the microcontroller to reconstruct phrases using the glyphs.

6.  Visual Debug Output

    ASCII Preview of Glyphs:  
    The app calls `display_bitmap()` to render the combined character bitmaps as ASCII art in the terminal for quick visual debugging.

## Uploading to the Arduino. 

1.  Arduino and OLED connection

    Connect the OLED to the Arduino using standard I2C protocol, as shown in the image below


    <img src="https://github.com/user-attachments/assets/4d621d55-6ca1-4c4c-ba90-db2016acd8e0" width="300">[^1]

3. Open and upload the `arduino_code.ino` file to the arduino using the Arduino IDE.


[^1]: Autodesk Instructables [link](https://www.instructables.com/OLED-I2C-DISPLAY-WITH-ARDUINO-Tutorial/).
