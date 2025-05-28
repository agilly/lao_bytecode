"""
This uses the Phetsarath-Regular.ttf file (in bitmap folder) to draw images of each of the characters (including whitespace characters) 
It loops through each pixel of the drawn image and builds a byte array of the pixel values
It can be used to generate bitmaps with different glyph pixel sizes!
Different Phetsarath fonts sizes can be used to generate the glyphs (font size should be smaller than glyph size)
"""


from PIL import Image, ImageFont, ImageDraw
import os
import math
import unicodedata

BASE_DIR = os.path.dirname(__file__)  # gets the path to the current .py file
FONT_PATH = os.path.join(BASE_DIR, "NotoSansLao-Regular.ttf") #using NotoSansLao instead of Phetsarath because it renders ton marks too
FONT_SIZE = 20
GLYPH_WIDTH = 20  #change as required
GLYPH_HEIGHT = 20
OUTPUT_PATH = os.path.join(BASE_DIR, "lao_bitmap_font.h") #creating a file to write into
LAO_UNICODE_RANGE = range(0x0E80, 0x0F00)


output_file = open(OUTPUT_PATH, "w", encoding="utf-8")  
output_file.write("const uint8_t Font20_Table[] PROGMEM = {\n")
offset = 0

#making a png file to view created glyphs
glyphs = [chr(codepoint) for codepoint in LAO_UNICODE_RANGE]
num_cols = 16
num_rows = math.ceil(len(glyphs)/num_cols)

font_sheet = Image.new("1", (GLYPH_WIDTH*num_cols, GLYPH_HEIGHT*num_rows), color=1)


def image_to_bits(image):
    pixels = image.load()
    byte_array = []
    for y in range(GLYPH_HEIGHT):
        byte = 0
        bits_filled = 0
        for x in range(GLYPH_WIDTH):
            pix = pixels[x,y]
            bit = 0 if pix == 1 else 1 #checks value of pixel @ location in image (black pixels are 0 in image)
            byte = (byte << 1) | bit #shifts bits to the left and adds new bit
            bits_filled += 1
            if bits_filled == 8:
                byte_array.append(byte) #once 8 bits are encoded we append to the array
                byte = 0
                bits_filled = 0
        if bits_filled > 0:
            byte <<= (8-bits_filled) #if we reach the end of a row and we dont have a complete byte, pad with zeros at end
            byte_array.append(byte)
    print(len(byte_array))
    return byte_array

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


for index, codepoint in enumerate(LAO_UNICODE_RANGE):
    char = chr(codepoint) #takes codepoint and returns actual symbol
    img = Image.new("1", (GLYPH_WIDTH, GLYPH_HEIGHT), color=1) #create a blank image of correct size
    draw = ImageDraw.Draw(img) 
    #render_char = 'ກ' + char if unicodedata.combining(char) else char
    draw.text((10, 0), char, font=font, fill=0) #drawing the image described by the font

    col = index % num_cols
    row = index // num_cols
    x_pos = GLYPH_WIDTH*col
    y_pos = GLYPH_HEIGHT*row
    font_sheet.paste(img, (x_pos,y_pos))

    byte_array = image_to_bits(img) #calling the function defined earlier
    safe_char = char if char.isprintable() else '?' #checks if characters are printable
    output_file.write(f"    // @{offset} U+{codepoint:04X} '{safe_char}'\n")  
    hex_line = ", ".join(f"0x{b:02X}" for b in byte_array)
    output_file.write(f"    {hex_line},\n") #writes the bitmap to the file
    offset += len(byte_array)
output_file.write("};\n")
output_file.close()
print(f"Output saved to {OUTPUT_PATH}")
font_sheet.save("preview_of_glyphs.png")





