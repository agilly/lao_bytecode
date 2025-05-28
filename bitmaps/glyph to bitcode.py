import uharfbuzz as hb
from PIL import Image, ImageOps
import freetype
import os
import tempfile

# Paths and text
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "NotoSansLao-Regular.ttf")
text = "ວັ"
image_width, image_height = 400, 150
pixel_width, pixel_height = 30, 30  # Bitmap dimensions

# Read font
with open(font_path, "rb") as f:
    font_data = f.read()

# Setup HarfBuzz
hb_blob = hb.Blob(font_data)
hb_face = hb.Face(hb_blob)
hb_font = hb.Font(hb_face)
buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()
hb.shape(hb_font, buf)
infos = buf.glyph_infos
positions = buf.glyph_positions

# Write font to temporary file for FreeType
with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font_file:
    tmp_font_file.write(font_data)
    tmp_font_path = tmp_font_file.name

try:
    # Render glyph using FreeType
    face = freetype.Face(tmp_font_path)
    face.set_char_size(72 * 64)
    image = Image.new("L", (image_width, image_height), 255)
    x, y = 50, 100

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
        image.paste(0, (x_pos, y_pos), glyph_image)
        x += pos.x_advance // 64
        y -= pos.y_advance // 64

    rendered_path = "harfbuzz_freetype_rendered.png"
    image.save(rendered_path)
    print(f"Saved rendered glyph image as: {rendered_path}")

finally:
    os.remove(tmp_font_path)

# Convert the rendered image to bitmap
def image_to_bitmap(image_path, pixel_width, pixel_height):
    img = Image.open(image_path).convert("L")
    img_inverted = ImageOps.invert(img)
    bbox = img_inverted.getbbox()
    if bbox:
        img = img.crop(bbox)
    img = img.resize((pixel_width, pixel_height), Image.Resampling.NEAREST)
    img = img.point(lambda p: 0 if p < 128 else 255, mode='L')
    img.save("processed_image_preview.png")
    pixels = img.load()
    byte_array = []
    for y in range(pixel_height):
        byte = 0
        bits_filled = 0
        for x in range(pixel_width):
            pix = pixels[x, y]
            bit = 1 if pix == 0 else 0
            byte = (byte << 1) | bit
            bits_filled += 1
            if bits_filled == 8:
                byte_array.append(byte)
                byte = 0
                bits_filled = 0
        if bits_filled > 0:
            byte <<= (8 - bits_filled)
            byte_array.append(byte)
    return byte_array

bitmap = image_to_bitmap(rendered_path, pixel_width, pixel_height)

# Print final bitmap as hex
print("Final bitmap as hex:")
print(", ".join(f"0x{b:02X}" for b in bitmap))