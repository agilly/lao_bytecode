from PIL import Image
import freetype
import uharfbuzz as hb
from tqdm import tqdm
import os
import tempfile

def generate_bitmaps_for_chars(char_list, font_path=None, output_header="bitmaps_for_char_list.h"):
    import os

    if font_path is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, "NotoSansLao-Regular.ttf")

    with open(font_path, "rb") as f:
        font_data = f.read()

    characters = []
    for sublist in char_list:
        characters.extend(sublist)

    # Initialize HarfBuzz
    hb_blob = hb.Blob(font_data)
    hb_face = hb.Face(hb_blob)
    hb_font = hb.Font(hb_face)

    # Initialize FreeType with temporary font file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font_file:
        tmp_font_file.write(font_data)
        tmp_font_path = tmp_font_file.name

    face = freetype.Face(tmp_font_path)
    face.set_char_size(72 * 64)

    # Dictionary to hold hexadecimal representations
    bitmap_dict = {}

    # Progress bar for each character
    for char in tqdm(characters, desc="Processing characters"):
        # Shape text using HarfBuzz
        buf = hb.Buffer()
        buf.add_str(char)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        infos = buf.glyph_infos
        positions = buf.glyph_positions

        # Create a blank image
        image_width, image_height = 100, 100
        image = Image.new("L", (image_width, image_height), 255)
        x, y = 25, 80  # Starting position

        for info, pos in zip(infos, positions):
            glyph_index = info.codepoint
            face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
            bitmap = face.glyph.bitmap

            w, h = bitmap.width, bitmap.rows
            top = face.glyph.bitmap_top
            left = face.glyph.bitmap_left

            if w > 0 and h > 0:
                glyph_image = Image.frombytes('L', (w, h), bytes(bitmap.buffer))
                x_pos = x + (pos.x_offset // 64) + left
                y_pos = y - (pos.y_offset // 64) - top
                image.paste(0, (x_pos, y_pos), glyph_image)

            x += pos.x_advance // 64
            y -= pos.y_advance // 64

        # Resize and convert to black and white
        img_resized = image.resize((30, 30), Image.Resampling.NEAREST)
        img_bw = img_resized.point(lambda p: 0 if p < 128 else 255, mode='1')

        # Convert image to hexadecimal representation
        pixels = img_bw.load()
        byte_array = []
        for y_row in range(30):
            byte = 0
            bits_filled = 0
            for x_col in range(30):
                pix = pixels[x_col, y_row]
                bit = 1 if pix == 0 else 0  # 0 (black) -> 1
                byte = (byte << 1) | bit
                bits_filled += 1
                if bits_filled == 8:
                    byte_array.append(byte)
                    byte = 0
                    bits_filled = 0
            if bits_filled > 0:
                byte <<= (8 - bits_filled)
                byte_array.append(byte)

        hex_repr = ', '.join(f'0x{b:02X}' for b in byte_array)
        bitmap_dict[char] = hex_repr

    # Generate C++ header file
    with open(output_header, "w", encoding="utf-8") as header_file:
        header_file.write("#pragma once\n\n")
        header_file.write("struct GlyphBitmap {\n")
        header_file.write("    const char* characters;\n")
        header_file.write("    const unsigned char bitmap[];\n")
        header_file.write("};\n\n")
        header_file.write("static const GlyphBitmap glyph_bitmaps[] = {\n")
        for char, hex_data in bitmap_dict.items():
            index = characters.index(char)
            header_file.write(f'    {{"{index}", {{ {hex_data} }} }},\n')
        header_file.write("};\n")

    # Clean up temporary font file
    os.remove(tmp_font_path)
    
    return bitmap_dict

# Example usage
if __name__ == "__main__":
    char_list = [['ກິ໊'], ['ກິ໋']]
    bitmap_data = generate_bitmaps_for_chars(char_list)