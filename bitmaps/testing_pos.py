from PIL import Image, ImageFont, ImageDraw
import os


BASE_DIR = os.path.dirname(__file__)  # gets the path to the current .py file
FONT_PATH = os.path.join(BASE_DIR, "NotoSansLao-Regular.ttf")
FONT_SIZE = 20
GLYPH_WIDTH = 35
GLYPH_HEIGHT = 35

# Characters to test
base_char = 'ກ'
tone_mark = '໋'


font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


img = Image.new("1", (GLYPH_WIDTH, GLYPH_HEIGHT), color=1)  # 1 = white background
draw = ImageDraw.Draw(img)

# Draw base character at lower position
draw.text((0, 3), base_char, font=font, fill=0)  

# Manually draw tone mark above base
draw.text((2, 0), tone_mark, font=font, fill=0)  

img.save("manual_combination.png")
