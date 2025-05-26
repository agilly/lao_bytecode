import uharfbuzz as hb
import freetype
from PIL import Image, ImageDraw

def render_text_with_harfbuzz(text, font_path, size=64, image_size=(200, 200)):
    # Load font using FreeType
    face = freetype.Face(font_path)
    face.set_char_size(size * 64)

    # Initialize HarfBuzz buffer
    hb_font = hb.Font.create(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()

    # Shape the text
    hb.shape(hb_font, buf)

    # Extract glyph info and positions
    infos = buf.glyph_infos
    positions = buf.glyph_positions

    # Prepare PIL image
    image = Image.new("L", image_size, 255)
    draw = ImageDraw.Draw(image)

    # Render glyphs using FreeType
    pen_x, pen_y = 10, 100  # Start position
    for info, pos in zip(infos, positions):
        gid = info.codepoint
        x_offset = pos.x_offset / 64
        y_offset = pos.y_offset / 64
        x_advance = pos.x_advance / 64
        y_advance = pos.y_advance / 64

        face.load_glyph(gid, freetype.FT_LOAD_RENDER)
        bitmap = face.glyph.bitmap
        top = face.glyph.bitmap_top
        left = face.glyph.bitmap_left

        glyph_image = Image.frombytes("L", (bitmap.width, bitmap.rows), bitmap.buffer)

        # Paste the glyph into the main image
        image.paste(glyph_image, (int(pen_x + left + x_offset), int(pen_y - top - y_offset)))

        # Advance pen position
        pen_x += x_advance
        pen_y += y_advance

    # Save the output
    image.save("output_with_harfbuzz.png")
    print("Saved output_with_harfbuzz.png")

if __name__ == "__main__":
    text = "ວັ"  # Your Lao text
    font_path = r"C:\Users\Oisín Conlon\Downloads\Noto_Sans_Lao\static\NotoSansLao-Regular.ttf"
    render_text_with_harfbuzz(text, font_path)