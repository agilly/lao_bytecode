#include <U8g2lib.h>

// Initialize the OLED display (adjust constructor for your hardware)
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0);

void setup() {
  u8g2.begin();
}

void loop() {
  // Define the Unicode range to display, e.g. basic Latin characters:
  uint32_t startCodepoint = 0x41;  // 'A'
  uint32_t endCodepoint = 0x5A;    // 'Z'

  for (uint32_t cp = startCodepoint; cp <= endCodepoint; cp++) {
    displayUnicodeCharacter(cp);
    delay(1000);  // Show each character for 1 second
  }
}

void displayUnicodeCharacter(uint32_t codepoint) {
  char utf8[5];  // Buffer for UTF-8 encoded character + null terminator
  int len = codepointToUTF8(codepoint, utf8);

  if (len == 0) {
    // Invalid codepoint, skip display
    return;
  }

  utf8[len] = '\0';

  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_unifont_t_symbols);  // Font with wide Unicode support
  u8g2.drawUTF8(10, 40, utf8);
  u8g2.sendBuffer();
}

int codepointToUTF8(uint32_t cp, char* utf8) {
  if (cp <= 0x7F) {
    utf8[0] = cp;
    return 1;
  } else if (cp <= 0x7FF) {
    utf8[0] = 0xC0 | (cp >> 6);
    utf8[1] = 0x80 | (cp & 0x3F);
    return 2;
  } else if (cp <= 0xFFFF) {
    utf8[0] = 0xE0 | (cp >> 12);
    utf8[1] = 0x80 | ((cp >> 6) & 0x3F);
    utf8[2] = 0x80 | (cp & 0x3F);
    return 3;
  } else if (cp <= 0x10FFFF) {
    utf8[0] = 0xF0 | (cp >> 18);
    utf8[1] = 0x80 | ((cp >> 12) & 0x3F);
    utf8[2] = 0x80 | ((cp >> 6) & 0x3F);
    utf8[3] = 0x80 | (cp & 0x3F);
    return 4;
  } else {
    return 0;  // Invalid codepoint
  }
}