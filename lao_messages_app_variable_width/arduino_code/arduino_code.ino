#include <Wire.h>   //for I2C communication
#include <Adafruit_GFX.h>  //graphics library
#include <Adafruit_SSD1306.h> //specific driver for OLED
#include <avr/pgmspace.h> //for storing bitmaps in flash memory
#include "glyph_bitmaps.h" //the bitmap file
#include "phrases_to_display.h" //the phrases file

//screen dimensions
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1 //not using a reset pin

//bitmap details
//#define BYTES_PER_ROW (GLYPH_WIDTH + 7)/8
//#define BYTES_PER_BITMAP (BYTES_PER_ROW*GLYPH_HEIGHT)

//creating an instance of the display driver
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);



void scrollPhrase(const uint8_t* lao_phrase, uint8_t len_phrase){
  int scroll_offset = -SCREEN_WIDTH;   //first character to be displayed at rightmost point
  int total_scroll_width = 0;
  for (int i = 0; i < len_phrase; i++) {
    total_scroll_width += glyph_widths[lao_phrase[i]];
  }
  while (scroll_offset <= total_scroll_width){
    display.clearDisplay();
    int x = -scroll_offset;
    int y = (SCREEN_HEIGHT - GLYPH_HEIGHT)/2;  //y does not change
    for (int i =0; i<len_phrase; i++) {
      int glyph_index = lao_phrase[i];
      int bitmap_start = bitmap_starts[glyph_index];
      int glyph_width = glyph_widths[glyph_index];
      int BYTES_PER_ROW = (glyph_width + 7)/8;
      int BYTES_PER_BITMAP = BYTES_PER_ROW*GLYPH_HEIGHT;
      uint8_t glyph_buffer[BYTES_PER_BITMAP];
      memcpy_P(glyph_buffer, glyph_bitmaps + bitmap_start, BYTES_PER_BITMAP); //loads the glyph buffer with a bitmap from the file
      display.drawBitmap(x, y, glyph_buffer, glyph_width, GLYPH_HEIGHT, SSD1306_WHITE); //draws a grapheme
      x +=glyph_width; //moves along by glyph_width to the next grapheme position
    }
    display.display(); //display the word 
    delay(5);

    scroll_offset++; //move scroll_offset by 1 pixel
  }
}

void setup() {
  Wire.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0X3C); //0X3C is the I2C address of the OLED controller
  display.clearDisplay();
  display.display();
  delay(2000);  //clear the display and wait
}


void loop() {
  //loops through every phrase and displays all
  for (int i=0; i<num_phrases; i++){
    const uint8_t* lao_phrase = &all_phrases[phrase_starts[i]]; 
    uint8_t len_phrase = phrase_lengths[i];
    scrollPhrase(lao_phrase, len_phrase);
}
}
