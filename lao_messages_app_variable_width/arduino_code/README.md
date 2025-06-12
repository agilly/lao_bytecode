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
* Waits for numeric input from the user (e.g., 1, 2, ...)
* Validates the input and passes the index to `displayPhraseByIndex()`
* Prints an error if the input is invalid or out of range
  
</details>
<details>
<summary>displayPhraseByIndex</summary>
  
Selects and displays the phrase corresponding to a given index.

* Retrieves phrase start and length from `phrase_starts[]` and `phrase_lengths[]`
* Points to the correct slice of `all_phrases[]`
* Sends the glyph sequence to `scrollPhrase()` (or `staticPhrase()` if preferred)
* Abstracts the phrase selection, so only an index is needed
  
</details>

<details>
<summary>scrollPhrase</summary>

Scrolls a phrase horizontally across the screen.

* Calculates the total scroll width from the unpadded glyph widths
* Starts the phrase off-screen and scrolls it one pixel at a time
* Loads each glyph from flash memory and renders it with tight spacing
* Updates the screen at each step to animate the scroll

</details>
<details>
  
<summary>staticPhrase</summary>

Displays a phrase statically (no scrolling).

* Clears the screen and centers the text vertically
* Iterates through glyphs, drawing each side by side
* Uses unpadded widths for spacing
* Updates the screen once after all glyphs are drawn

</details>

## Adapting to any project

#### User Input
The current system expects a numeric input via Serial.
You can replace this with another input source, such as:
* Physical buttons mapped to phrase numbers
* A internet module that sends an input
* A sensor that triggers a specific phrase

**Replace the `checkSerialInput` with your bespoke input reading function. At the end of your custom input function, simply call `displayPhraseByIndex`**

The code will handle the rest!

#### Output
The current system expects the following hardware:

* Arduino UNO or Nano
* I2C communication
* SSD1306 128×64 OLED

If you are using **any other hardware, refer to this [README](../../lao_messages_app_variable_width/README_Hardware_Details.md).**

A dropdown contains all the relevant modification tables (interfacing with SPI instead, different microcontrollers, different screen types ect.).
