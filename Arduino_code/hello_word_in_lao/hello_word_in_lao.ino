#include <Wire.h>   //for I2C communication
#include <Adafruit_GFX.h>  //graphics library
#include <Adafruit_SSD1306.h> //specific driver for OLED
#include <avr/pgmspace.h> //for storing bitmaps in flash memory
#include "glyph_bitmaps.h"

//screen dimensions
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1 //not using a reset pin

//bitmap details
#define BITMAP_WIDTH 30
#define BYTES_PER_ROW (BITMAP_WIDTH + 7)/8
#define BITMAP_HEIGHT 30
#define BYTES_PER_BITMAP (BYTES_PER_ROW*BITMAP_HEIGHT)
#define NUM_UNIQUE_GLYPHS 9

//creating an instance of the display driver
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//loading bitmap data into flash memory
//static const uint8_t glyph_bitmaps[BYTES_PER_BITMAP*NUM_UNIQUE_GLYPHS] PROGMEM = {...};
//loading word data
const uint8_t lao_word[] = {0, 1, 2, 3, 4, 5, 6, 7, 8};
const uint8_t len_word = sizeof(lao_word) / sizeof(lao_word[0]);


uint8_t glyph_buffer[BYTES_PER_BITMAP];
int scroll_offset = -SCREEN_WIDTH;


void setup() {
  Wire.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0X3C); //0X3C is the I2C address of the OLED controller
  display.clearDisplay();
  display.display();
  delay(2000);
}


void loop() {
  display.clearDisplay();
  int x = -scroll_offset;
  int y = (SCREEN_HEIGHT - BITMAP_HEIGHT)/2;
  for (int i =0; i<len_word; i++) {
    int glyph_index = lao_word[i];
    memcpy_P(glyph_buffer, glyph_bitmaps + (glyph_index * BYTES_PER_BITMAP), BYTES_PER_BITMAP);
    display.drawBitmap(x, y, glyph_buffer, BITMAP_WIDTH, BITMAP_HEIGHT, SSD1306_WHITE);
    x +=BITMAP_WIDTH/2;
  }
  display.display();
  delay(5);

  scroll_offset++;
  if (scroll_offset > BITMAP_WIDTH * len_word / 2) {
    scroll_offset = -SCREEN_WIDTH; // reset for looping scroll
  }
}
