import uharfbuzz as hb
from PIL import Image
import freetype
import os
import tempfile

BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "NotoSansLao-Regular.ttf")

text = "ກຼ່"

with open(font_path, "rb") as f:
    font_data = f.read()

# HarfBuzz setup
hb_blob = hb.Blob(font_data)
hb_face = hb.Face(hb_blob)
hb_font = hb.Font(hb_face)

buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()
hb.shape(hb_font, buf)

infos = buf.glyph_infos
positions = buf.glyph_positions

# Write font data to a temporary file for FreeType
with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font_file:
    tmp_font_file.write(font_data)
    tmp_font_path = tmp_font_file.name

try:
    face = freetype.Face(tmp_font_path)
    face.set_char_size(72 * 64)

    image_width, image_height = 100, 100
    image = Image.new("L", (image_width, image_height), 255)
    x, y = 25, 80

    for info, pos in zip(infos, positions):
        glyph_index = info.codepoint
        face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
        bitmap = face.glyph.bitmap

        w, h = bitmap.width, bitmap.rows
        top = face.glyph.bitmap_top
        left = face.glyph.bitmap_left

        glyph_image = Image.frombytes('L', (w, h), bytes(bitmap.buffer))

        x_pos = x + (pos.x_offset // 64) + left
        y_pos = y - (pos.y_offset // 64) - top

        # Paste black with glyph_image as mask directly (no inversion)
        image.paste(0, (x_pos, y_pos), glyph_image)

        x += pos.x_advance // 64
        y -= pos.y_advance // 64
        image.show()
        image.save("harfbuzz_freetype_rendered.png")
finally:
    # Delete the temporary font file to clean up
    os.remove(tmp_font_path)