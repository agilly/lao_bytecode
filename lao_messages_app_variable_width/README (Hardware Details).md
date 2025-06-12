## Hardware details 
Authors: Diya Thomas and Oisín Conlon
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
