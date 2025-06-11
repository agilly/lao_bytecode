Author: Diya Thomas

Technical contributers: Diya Thomas

# Understanding and Adapting the Arduino code for your project

## Overview

`arduino_code.ino` contains the logic which the microcontroller uses to display text on a screen. 
It is accompanied by 2 header files which contain the **core data** outputs from the preprocessing stages:

* `glyph_bitmaps.h` contains the bitmap data
* `phrases_to_display.h` contains the phrase data. 

It takes a number input from the user, and displays the phrase associated with the number. 
There are 2 display options:

* `scrollPhrase` displays phrases scrolling across a screen (ideal for small screens)
* `staticPhrase` displays a static phrase on the screen (ideal for E-Ink screens or larger screens)

## Main Functions
<img src="../../www/assets/flowchart.png" alt="Flowchart" width="800"/>
This is an in-depth review of the core functions. 
They are designed to be modular and can be adapted to different project specifics. 

<details>
<summary>setup</summary>

Initializes the hardware.  
* Starts Serial communication (`Serial.begin`)  
* Sets up I²C (`Wire.begin`)  
* Initializes the OLED display (`display.begin(SSD1306_SWITCHCAPVCC, 0X3C);`)  
* Clears and refreshes the display 
* Prompts the user for a input (`Serial.println("Enter the number corresponding to the phrase you'd like to display")`)
</details>

<details>
<summary>checkSerialInput</summary>
  
Monitors the Serial input buffer.  
* Waits for numeric input from the user (e.g., `1`, `2`, ...)
* Validates the input and passes the **index** to `displayPhraseByIndex()`  
* Prints errors if the input is invalid or out of range
  
</details>
<details>
<summary>displayPhraseByIndex</summary>
  
Selects and displays the phrase corresponding to a given index.
* Retrieves **phrase data** from program memory:
* Uses `phrase_starts[]` to locate the starting index of the phrase inside `all_phrases[]`
* Uses `phrase_lengths[]` to determine how many glyphs to read for that phrase
* Each glyph is represented as an integer index into the bitmap font arrays
* Passes the resulting glyph sequence and its length to either:
* Calls `scrollPhrase()` at the end for animated scrolling
* or `staticPhrase()` for a static layout
- This function abstracts away the data lookup so your project can simply call:
```cpp
displayPhraseByIndex(2);  // Displays the second defined phrase
```
</details>
<details>
<summary>scrollPhrase</summary>
</details>
<details>
<summary>staticPhrase</summary>
</details>

## Interfacing with your project

## Compatibility with other hardware

## Troubleshooting
