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
    * **Windows Users:** We recommend using **Git Bash**, which is included with the Git for Windows installation.

* **Arduino IDE:** Required to upload the generated code to your Arduino board.
    * Download from the official [Arduino Software page](https://www.arduino.cc/en/software).

---

## **Step 1: Initial Project Setup (All Users)**

These first three steps are required for **all operating systems** and both setup methods.

1.  **Open Your Terminal**
    * On Windows, we recommend opening **Git Bash** or **PowerShell**.
    * On macOS or Linux, open your standard **Terminal**.

2.  **Clone the Repository**
    Navigate to a suitable directory, then run:
    ```bash
    git clone https://github.com/Technology-for-the-Poorest-Billion/2025-MakerBox-Bytecode.git
    ```

3.  **Navigate to the Project Folder**
    ```bash
    cd 2025-MakerBox-Bytecode/lao_messages_app_variable_width
    ```

After completing these steps, proceed to the instructions for your specific operating system below.

---

## **Linux & macOS Setup**

Choose one of the two methods below. The fast setup is recommended.

### Method 1: Fast Setup ⚡

This method uses a shell script to automate the entire setup.

1.  **Make the Script Executable:**
    ```bash
    chmod +x fast_setup_arduino_LINUX.sh
    ```

2.  **Run the Setup Script:**
    ```bash
    ./fast_setup_arduino_LINUX.sh
    ```
    The script will create the environment, install packages, run the app, and open the Arduino IDE for you.

<br>

### Method 2: Manual Setup 🛠️
<details>
<summary>Click to expand for manual Linux & macOS instructions</summary>

1.  **Create a Python Virtual Environment:**
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
    * Open the Arduino IDE application.
    * Go to `File > Open...` and navigate to the project's `arduino_code` folder.
    * Open the main sketch file: `arduino_code.ino`.

6.  **Deactivate Virtual Environment:** When finished, you can exit the environment by typing:
    ```bash
    deactivate
    ```
</details>

---

## **Windows Setup**

Choose one of the two methods below. The fast setup is recommended.

### Method 1: Fast Setup ⚡

This method uses a PowerShell script to automate the entire setup.

1.  **Run the Setup Script in PowerShell:**
    * **Note:** You may need to adjust your system's execution policy first. If the script fails, open PowerShell as an **Administrator** and run `Set-ExecutionPolicy RemoteSigned`. Press `Y` to confirm. You only need to do this once.
    * In your regular (non-admin) PowerShell terminal, run the script:
    ```powershell
    .\fast_setup_arduino_WINDOWS.ps1
    ```
    The script will handle the rest!

<br>

### Method 2: Manual Setup 🛠️
<details>
<summary>Click to expand for manual Windows instructions</summary>
    
1.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the Virtual Environment:**
    * In **Git Bash** or **PowerShell**:
        ```bash
        source .venv/Scripts/activate
        ```
    * In **Windows Command Prompt (CMD)**:
        ```cmd
        .\.venv\Scripts\activate
        ```
    Your command prompt should now be prefixed with `(.venv)`.

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Python Application:**
    ```bash
    python run.py
    ```

5.  **Launch Arduino IDE:**
    * Open the Arduino IDE application.
    * Go to `File > Open...` and navigate to the project's `arduino_code` folder.
    * Open the main sketch file: `arduino_code.ino`.

6.  **Deactivate Virtual Environment:** When finished, you can exit the environment by typing:
    ```bash
    deactivate
    ```
</details>

---
## Hardware details 
The code can be uploaded to the microcontroller for use on a screen with **no changes** to the code if you are using:
1. **Arduino UNO or Nano**
2. **I2C communication**
3. **SSD1306 128×64 OLED**
   
If your project involves all of the above hardware, connect the OLED screen to the Arduino according to the illustration shown below. 
| **OLED Pin** | **Arduino Uno Pin** |
|--------------|---------------------|
| VCC          | 5V                  |
| GND          | GND                 |
| SDA          | A4                  |
| SCL (or SCK) | A5                  |

<img src="../www/assets/I2C connection.png" alt="Electrical Wiring" width="400"/>
(Taken from Autodesk Instructables, n.d.)

---

### Interfacing with other hardware 
Please refer to the dropdown below if you are using any other form of hardware.
<details>
<summary>Click to expand</summary>

## **Technical Details: Code Portability for Other Screens**

The Arduino code in this project is highly portable to other screens thanks to the Adafruit GFX library. The table below outlines which parts of the code are portable and what actions are required to adapt it for different display types like graphical LCDs or E-Ink screens.

| **Code Section / Function** | **Different OLED** | **LCD** | **E-Ink** | ⚠️ **Action** |
|:---|:---|:---|:---|:---|
| `#include <Wire.h>` (I2C) | Depends | Depends | Depends | Replace with `SPI.h` if using SPI — see SPI section for more details. |
| `#include <Adafruit_SSD1306.h>` | Yes (if SSD1306) | No | No | Replace with correct driver. |
| `Adafruit_SSD1306 display(...)` | Yes (if SSD1306) | No | No | Replace with correct constructor. |
| `display.begin(...)` | Yes (if SSD1306) | No | No | Replace with display's `.begin()` or `.init()`. |
| `#define SCREEN_WIDTH / HEIGHT` | Depends | Depends | Depends | Update to match your display's resolution. |
| `drawBitmap(...)` | Yes | ⚠️ Color update | ⚠️ Use different function | Replace `SSD1306_WHITE` or use `drawInvertedBitmap()` for E-Ink. |
| `Data files (.h)` | Yes | Yes | Yes | None. The core data is 100% portable. |
| `scrollPhrase()` | Yes | Yes | No | Works perfectly for LCD/OLED. Unsuitable for E-Ink due to rapid updates. |
| `staticPhrase()` | Yes | Yes | Yes | Works perfectly for LCD/OLED. Ideal for E-Ink. |

<details>
<summary> More Guidance on Switching from I²C to SPI Display </summary>

If you're replacing an I²C display with an SPI display, here are the required code changes:

#### 1. Remove I²C-Specific Code

Delete or comment out the following:

```cpp
#include <Wire.h>
Wire.begin();
```

#### 2. Add SPI-Specific Code

Replace it with the appropriate SPI setup. Here's an example using an Adafruit ILI9341 display:

```cpp
#include <SPI.h>
#include <Adafruit_ILI9341.h>

// Define the SPI control pins (replace number with your connections)
#define TFT_CS   10 
#define TFT_DC    9
#define TFT_RST   8

// Example display object
Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_RST);

//update the setup function
void setup() {
  SPI.begin();     // Start the SPI bus
  tft.begin();     // Initialize the display
}
```
</details> 

## **Technical Details: Code Portability for Other Microcontrollers**

| Code Aspect / Feature | Arduino (AVR - Uno/Nano) | ESP32 / ESP8266 | Raspberry Pi Pico (RP2040) |
| :--- | :--- | :--- | :--- |
| **Core C++ Logic** | **Baseline** | ✅ **Highly Portable** | ✅ **Highly Portable** |
| **Libraries (Adafruit GFX)** | **Baseline** | ✅ **Fully Supported** | ✅ **Fully Supported** |
| **Hardware I2C (`Wire.h`)** <br>Refer to *More Guidance on Switching from I²C to SPI Display*| **Baseline** | ✅ **Highly Portable** | ✅ **Highly Portable** |
| **Memory (`PROGMEM` and `memcpy_P()`)** | ✅ Baseline — required |⚠️ **Action Required** — prefer `const` and `memcpy()` |⚠️ **Action Required** — use `const` and `memcpy()` |
||**Required.** PROGMEM and <avr/pgmspace.h> are essential to store large data (bitmaps) in flash memory to save precious RAM (2KB on Uno). Requires `memcpy_P()` to read from flash. | These boards have far more RAM.`PROGMEM` is often ignored by ESP cores; use `const` instead. Replace `memcpy_P()` with `memcpy()` to read the data from memory. | `PROGMEM` unsupported — use `const` only. Replace `memcpy_P()` with `memcpy()`.|
| **Pin Definitions** | **Baseline** | ⚠️ **Action Required** | ⚠️ **Action Required** |
| | Uses standard Arduino pin numbers. | Pin numbers correspond to the ESP32's GPIO numbers (e.g., `GPIO21`, `GPIO22`). You must update these for your screen's wiring in `Wire.h()`. | Pin numbers correspond to the Pico's GP numbers (e.g., `GP0`, `GP1`). You must update these in `Wire.h()` |

</details>
