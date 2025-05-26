#include <U8g2lib.h>

// Initialize the display (adjust pins and constructor for your hardware)
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0);

void setup() {
  u8g2.begin();
}

void loop() {
  uint32_t codepoint = 0x03A9;  // Example: Unicode for Ω (Greek capital letter Omega)

  displayUnicodeCharacter(codepoint);

  delay(5000);  // Delay to keep the character on the screen
}

void displayUnicodeCharacter(uint32_t codepoint) {
  char utf8[5];  // UTF-8 encoding can take up to 4 bytes + null terminator
  int len = codepointToUTF8(codepoint, utf8);

  utf8[len] = '\0';  // Null-terminate the string

  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_unifont_t_symbols);  // Use a font with wide Unicode coverage
  u8g2.drawUTF8(10, 30, utf8);
  u8g2.sendBuffer();
}

// Convert a Unicode codepoint to a UTF-8 encoded string
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
    // Invalid codepoint
    return 0;
  }
}