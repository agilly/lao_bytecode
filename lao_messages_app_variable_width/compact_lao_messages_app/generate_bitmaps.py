"""
Bitmap Glyph Generator for Unicode Grapheme Clusters.

This module uses HarfBuzz and FreeType to render grapheme clusters (e.g., characters
or ligatures in complex scripts) into monochrome bitmaps. It then converts these
bitmaps into a packed byte format suitable for use in C++ embedded environments
(such as AVR microcontrollers), and outputs them to a C++ header file.

Dependencies:
- Pillow
- freetype-py
- uharfbuzz
- tqdm
"""


from PIL import Image
import freetype
import uharfbuzz as hb
from tqdm import tqdm
import os
import tempfile

def generate_bitmaps_for_chars(char_list, GLYPH_WIDTH = 30, GLYPH_HEIGHT = 30, font_path="./font_files/NotoSansLao-Regular.ttf", output_header="./arduino_code/glyph_bitmaps.h"):
    """
    Generates GLYPH_WIDTH x GLYPH_HEIGHT black-and-white bitmap images for each grapheme cluster in `char_list`,
    and exports the packed binary data as a C++ header file for use in embedded systems.

    Args:
        char_list (list[str]): List of grapheme clusters or strings (e.g., letters, syllables, or words).
        font_path (str): Path to a TrueType font file (.ttf) that supports the input characters.
        output_header (str): Output file path for the generated C++ header.

    Returns:
        list[int]: Flat list of all packed bitmap bytes across all input characters.

    The generated bitmaps are:
        - GLYPH_WIDTH x GLYPH_HEIGHT pixels
        - 1-bit monochrome (packed: 8 pixels per byte)
        - Stored consecutively in a C++ array (`glyph_bitmaps[]`) with `PROGMEM` for AVR targets.
    """
    # if font_path is None:
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     font_path = os.path.join(BASE_DIR, "/font_files/NotoSansLao-Regular.ttf")

    with open(font_path, "rb") as f:
        font_data = f.read()

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

    # List to hold all bytes from all glyphs consecutively
    all_bytes = []
    bitmap_widths = []

    # Progress bar for each character
    for char in tqdm(char_list, desc="Processing characters"):
        # Shape text using HarfBuzz
        buf = hb.Buffer()
        buf.add_str(char)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        infos = buf.glyph_infos
        positions = buf.glyph_positions

        # Find base consonant (first glyph typically)
        base_idx = 0  # Default to first glyph
        base_glyph = infos[base_idx].codepoint
    
        # Load base glyph metrics
        face.load_glyph(base_glyph, freetype.FT_LOAD_DEFAULT)
        base_width = face.glyph.metrics.horiAdvance // 64
        base_left = face.glyph.metrics.horiBearingX // 64
        # Create a blank image
        image_width, image_height = base_width, 100
        wh_ratio = image_width / image_height
        image = Image.new("L", (image_width, image_height), 255)
        # CENTERING CALCULATION (Base consonant only)
        x = 0
        y = 80  # Empirical baseline position (adjust as needed)

        for info, pos in zip(infos, positions):
            glyph_index = info.codepoint
            face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
            bitmap = face.glyph.bitmap

            w, h = bitmap.width, bitmap.rows
            top = face.glyph.bitmap_top
            left = face.glyph.bitmap_left

            if w > 0 and h > 0:
                glyph_img = Image.frombytes('L', (w, h), bytes(bitmap.buffer))
                x_pos = x + (pos.x_offset // 64) + face.glyph.bitmap_left
                y_pos = y - (pos.y_offset // 64) - face.glyph.bitmap_top
                image.paste(0, (x_pos, y_pos), glyph_img)
            
            x += pos.x_advance // 64
            y -= pos.y_advance // 64

        # Resize glyph image
        resized_width = int(GLYPH_HEIGHT * wh_ratio)
        img_resized = image.resize((resized_width, GLYPH_HEIGHT), Image.Resampling.NEAREST)

        # Compute padding: add 1/6th of resized_width to each side, then round up to nearest multiple of 8
        pad_each_side = resized_width // 3
        padded_width = resized_width + 2 * pad_each_side

        # Round up padded_width to nearest multiple of 8
        final_width = ((padded_width + 7) // 8) * 8
        total_extra = final_width - resized_width
        pad_left = total_extra // 2
        pad_right = total_extra - pad_left

        # Pad the image with white (255)
        img_padded = Image.new("L", (final_width, GLYPH_HEIGHT), 255)
        img_padded.paste(img_resized, (pad_left, 0))

        # Convert to 1-bit black & white
        img_bw = img_padded.point(lambda p: 0 if p < 128 else 255, mode='1')

        bitmap_widths.append(final_width)

        # Convert image to byte array (1 bit per pixel packed in bytes)
        pixels = img_bw.load()
        byte_array = []
        for y_row in range(GLYPH_HEIGHT):
            byte = 0
            bits_filled = 0
            for x_col in range(final_width):
                pix = pixels[x_col, y_row]
                bit = 1 if pix == 0 else 0  # Black pixel = 1
                byte = (byte << 1) | bit
                bits_filled += 1
                if bits_filled == 8:
                    byte_array.append(byte)
                    byte = 0
                    bits_filled = 0
            if bits_filled > 0:
                byte <<= (8 - bits_filled)
                byte_array.append(byte)

        all_bytes.extend(byte_array)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_header), exist_ok=True)

    # Proceed with writing the file
    with open(output_header, "w", encoding="utf-8") as f:
        guard = output_header.upper().replace('.', '_')
        f.write(f"#ifndef {guard}\n")
        f.write(f"#define {guard}\n\n")
        f.write(f"#define GLYPH_HEIGHT {GLYPH_HEIGHT}\n\n")
        f.write("#include <avr/pgmspace.h>\n\n")
        f.write("static const uint8_t glyph_bitmaps[] PROGMEM = {\n")

        # Write bytes in rows of 16 for readability
        for i in range(0, len(all_bytes), 16):
            line_bytes = all_bytes[i:i+16]
            line = ", ".join(f"0x{b:02X}" for b in line_bytes)
            f.write(f"{line},\n")

        f.write("};\n\n")
        # Write glyph widths array
        f.write("const uint16_t glyph_widths[] = {\n")

        # Convert widths to strings and write in rows of 16
        for i in range(0, len(bitmap_widths), 16):
            line = ", ".join(str(width) for width in bitmap_widths[i:i+16])
            f.write(f"  {line},\n")

        f.write("};\n\n")

        # Generate an array of indexes into the bitmap
        bitmap_start_indexes = []
        current_index = 0
        for i in range(len(bitmap_widths)):
            bitmap_start_indexes.append(current_index)
            current_index += ((bitmap_widths[i] + 7) // 8) * GLYPH_HEIGHT

        # Write bitmap start indexes to a const uint16_t array
        f.write("const uint16_t bitmap_starts[] = {\n")
        for i in range(0, len(bitmap_start_indexes), 16):
            line = ", ".join(str(idx) for idx in bitmap_start_indexes[i:i+16])
            f.write(f"  {line},\n")
            

        f.write("};\n\n")

        f.write(f"#endif // {guard}\n")

    # Clean up temp font file
    os.remove(tmp_font_path)

    header_size_kb = os.path.getsize(output_header) / 1024
    print(f"Bitmap header file size: {header_size_kb:.2f} KB")

    return all_bytes