import freetype
import uharfbuzz as hb
from PIL import Image

# Load font binary data into memory
with open("./Phetsarath-Regular.ttf", "rb") as f:
    font_data = f.read()

text = "ວັ"

# HarfBuzz shaping
hb_blob = hb.Blob(font_data)
hb_face = hb.Face(hb_blob)
hb_font = hb.Font(hb_face)

buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()
hb.shape(hb_font, buf)

infos = buf.glyph_infos
positions = buf.glyph_positions

# Load font in-memory using freetype-py
face = freetype.Face(memoryview(font_data))
face.set_char_size(72 * 64)  # Set font size

# Create blank image to render onto
image_width, image_height = 400, 150
image = Image.new("L", (image_width, image_height), 255)
x, y = 50, 100  # Baseline start

# Draw shaped glyphs
for info, pos in zip(infos, positions):
    glyph_index = info.codepoint
    face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
    bitmap = face.glyph.bitmap

    w, h = bitmap.width, bitmap.rows
    top = face.glyph.bitmap_top
    left = face.glyph.bitmap_left

    glyph_image = Image.frombytes("L", (w, h), bytes(bitmap.buffer))

    x_pos = x + (pos.x_offset // 64) + left
    y_pos = y - (pos.y_offset // 64) - top

    image.paste(0, (x_pos, y_pos), glyph_image)

    x += pos.x_advance // 64
    y -= pos.y_advance // 64

# Save or display
image.save("harfbuzz_freetype_rendered.png")
image.show()
