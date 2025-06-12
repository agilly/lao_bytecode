from PIL import Image
import freetype
import uharfbuzz as hb
from tqdm import tqdm
import os
import tempfile
import sys # Keep sys import for error printing
import math

def generate_bitmaps_for_chars(char_list, GLYPH_HEIGHT = 30, font_path="./font_files/NotoSansLao-Regular.ttf", output_header="./arduino_code/glyph_bitmaps.h"):
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
    unpadded_widths = []

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
        # Added try-except for robustness, as discussed in previous interactions
        try:
            face.load_glyph(base_glyph, freetype.FT_LOAD_DEFAULT)
        except ValueError as e:
            print(f"\nERROR: Failed to load base glyph {base_glyph} for character '{char}'. Error: {e}", file=sys.stderr)
            # Fallback values if base glyph loading fails
            base_width = GLYPH_HEIGHT # Use GLYPH_HEIGHT as a rough estimate
            wh_ratio = 1.0 # Assume square for aspect ratio
            # Create a minimal image to avoid crashing
            image = Image.new("L", (GLYPH_HEIGHT * 2, GLYPH_HEIGHT * 2), 255) # Larger fallback image
            x = 0
            y = GLYPH_HEIGHT # Adjust fallback baseline
        except Exception as e:
            print(f"\nUNEXPECTED ERROR: during base glyph loading for {base_glyph} for character '{char}'. Error: {e}", file=sys.stderr)
            base_width = GLYPH_HEIGHT
            wh_ratio = 1.0
            image = Image.new("L", (GLYPH_HEIGHT * 2, GLYPH_HEIGHT * 2), 255)
            x = 0
            y = GLYPH_HEIGHT
        else: # Only execute if try block succeeds
            base_width = face.glyph.metrics.horiAdvance // 64
            # base_left = face.glyph.metrics.horiBearingX // 64 # Not directly used for initial canvas size

            # Create a blank image
            # The initial image_width should be able to contain the entire shaped cluster, not just base_width.
            # Using base_width as a starting point is okay for simple cases, but complex scripts might need more.
            # For now, sticking to original request and keeping base_width for initial canvas size.
            image_width = base_width
            image_height = 100 # This is an empirical height for rendering before final scaling
            wh_ratio = image_width / image_height
            image = Image.new("L", (image_width, image_height), 255)
            # CENTERING CALCULATION (Base consonant only)
            x = 0
            y = 80  # Empirical baseline position (adjust as needed)

        for info, pos in zip(infos, positions):
            glyph_index = info.codepoint
            
            # Skip .notdef glyphs (glyph_index 0)
            if glyph_index == 0:
                x += pos.x_advance // 64 # Still advance pen for proper layout
                continue

            try:
                face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
            except ValueError as e:
                print(f"\nERROR: Failed to load/render glyph {glyph_index} for char '{char}'. Error: {e}", file=sys.stderr)
                x += pos.x_advance // 64 # Still advance pen for proper layout
                continue
            except Exception as e:
                print(f"\nUNEXPECTED ERROR: during rendering for glyph_index {glyph_index} for char '{char}'. Error: {e}", file=sys.stderr)
                x += pos.x_advance // 64
                continue

            bitmap = face.glyph.bitmap

            w, h = bitmap.width, bitmap.rows
            top = face.glyph.bitmap_top
            left = face.glyph.bitmap_left

            if w > 0 and h > 0:
                glyph_img = Image.frombytes('L', (w, h), bytes(bitmap.buffer))
                
                
                x_pos = x + (pos.x_offset // 64) + face.glyph.bitmap_left
                y_pos = y - (pos.y_offset // 64) - face.glyph.bitmap_top
                
                # Check bounds before pasting to ensure it doesn't crash Pillow
                if (x_pos < image.width and y_pos < image.height and
                    x_pos + glyph_img.width > 0 and y_pos + glyph_img.height > 0):
                    # Calculate the actual paste region that fits within the image
                    paste_x = max(0, x_pos)
                    paste_y = max(0, y_pos)
                    src_x1 = max(0, -x_pos)
                    src_y1 = max(0, -y_pos)
                    src_x2 = min(glyph_img.width, image.width - x_pos)
                    src_y2 = min(glyph_img.height, image.height - y_pos)
                    
                    if src_x2 > src_x1 and src_y2 > src_y1:
                        cropped_glyph_img = glyph_img.crop((src_x1, src_y1, src_x2, src_y2))
                        image.paste(0, (paste_x, paste_y), cropped_glyph_img)
            
            x += pos.x_advance // 64
            y -= pos.y_advance // 64 

        # Resize glyph image
        resized_width = int(GLYPH_HEIGHT * wh_ratio)
        img_resized = image.resize((resized_width, GLYPH_HEIGHT), Image.Resampling.NEAREST)

        # Convert to 1-bit black & white (remains unchanged)
        img_bw = img_resized.point(lambda p: 0 if p < 128 else 255, mode='1')

        # --- START OF MANUAL HORIZONTAL CROPPING CODE --- much better than using pillow
        # Find the leftmost non-white column
        first_pixel_col = -1
        for x_col in range(img_bw.width):
            for y_row in range(img_bw.height):
                # In '1' mode, 0 is black, 1 is white. We're looking for black pixels (0).
                if img_bw.getpixel((x_col, y_row)) == 0: # Found a black pixel
                    first_pixel_col = x_col
                    break # Break inner loop, move to next column
            if first_pixel_col != -1: # If found in this column, break outer loop
                break

        # Find the rightmost non-white column
        last_pixel_col = -1
        for x_col in range(img_bw.width - 1, -1, -1): # Iterate from right to left
            for y_row in range(img_bw.height):
                if img_bw.getpixel((x_col, y_row)) == 0: # Found a black pixel
                    last_pixel_col = x_col
                    break # Break inner loop
            if last_pixel_col != -1: # If found in this column, break outer loop
                break
        
        if first_pixel_col != -1 and last_pixel_col != -1: # If black pixels were found
            # Crop horizontally using the discovered bounds, keeping full height
            cropped_img_bw = img_bw.crop((first_pixel_col, 0, last_pixel_col + 1, img_bw.height))
        else: # Handle case of entirely white image (e.g., space character, or no black pixels found)
            # Create a small, entirely white placeholder with GLYPH_HEIGHT
            # Use a width that's typical for a space, e.g., GLYPH_HEIGHT // 2
            cropped_img_bw = Image.new('1', (GLYPH_HEIGHT // 4, GLYPH_HEIGHT), 255)
        # --- END OF MANUAL HORIZONTAL CROPPING CODE ---

        # Now, work with the cropped image for padding and byte conversion
        # The 'resized_width' variable name might be confusing here, but we're sticking to it
        padded_width = cropped_img_bw.width # Use the width of the newly cropped image
        unpadded_widths.append(padded_width + math.ceil(GLYPH_HEIGHT * 1/30))


        # Round up padded_width to nearest multiple of 8
        final_width = ((padded_width + 7) // 8) * 8
    

        # Pad the image with white (255) to reach `final_width`
        img_padded = Image.new("L", (final_width, GLYPH_HEIGHT), 255) # Use 'L' mode for padding
        img_padded.paste(cropped_img_bw, (0, 0)) # Paste the cropped B&W image
        
        # Final conversion to 1-bit black & white after padding
        img_final_bw = img_padded.point(lambda p: 0 if p < 128 else 255, mode='1')

        bitmap_widths.append(final_width)

        # Convert image to byte array (1 bit per pixel packed in bytes)
        pixels = img_final_bw.load()
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
            # Removed the 'if bits_filled > 0:' block as final_width is always a multiple of 8,
            # ensuring bits_filled will always be 0 here.
            # No explicit padding needed here for byte alignment, as it's handled by final_width.

        all_bytes.extend(byte_array)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_header), exist_ok=True)

    # Proceed with writing the file
    with open(output_header, "w", encoding="utf-8") as f:
        guard = os.path.basename(output_header).upper().replace('.', '_').replace('-', '_') # Use os.path.basename and replace hyphens too
        f.write(f"#ifndef {guard}\n")
        f.write(f"#define {guard}\n\n")
        f.write(f"#define GLYPH_HEIGHT {GLYPH_HEIGHT}\n\n")
        f.write("#include <avr/pgmspace.h>\n\n")
        f.write("static const uint8_t glyph_bitmaps[] PROGMEM = {\n")

        # Write bytes in rows of 16 for readability
        for i in range(0, len(all_bytes), 16):
            line_bytes = all_bytes[i:i+16]
            line = ", ".join(f"0x{b:02X}" for b in line_bytes)
            f.write(f"  {line},\n") # Add indentation

        f.write("};\n\n")
        # Write glyph widths array
        f.write("const uint16_t glyph_widths[] PROGMEM = {\n")

        # Convert widths to strings and write in rows of 16
        for i in range(0, len(bitmap_widths), 16):
            line = ", ".join(str(width) for width in bitmap_widths[i:i+16])
            f.write(f"  {line},\n")

        f.write("};\n\n")

        # Write unpadded_widths array
        f.write("const uint16_t unpadded_widths[] PROGMEM = {\n")

        # Convert widths to strings and write in rows of 16
        for i in range(0, len(unpadded_widths), 16):
            line = ", ".join(str(width) for width in unpadded_widths[i:i+16])
            f.write(f"  {line},\n")

        f.write("};\n\n")

        # Generate an array of indexes into the bitmap
        bitmap_start_indexes = []
        current_index = 0
        for i in range(len(bitmap_widths)):
            bitmap_start_indexes.append(current_index)
            current_index += ((bitmap_widths[i] + 7) // 8) * GLYPH_HEIGHT

        # Write bitmap start indexes to a const uint16_t array
        f.write("const uint16_t bitmap_starts[] PROGMEM = {\n")
        for i in range(0, len(bitmap_start_indexes), 16):
            line = ", ".join(str(idx) for idx in bitmap_start_indexes[i:i+16])
            f.write(f"  {line},\n")
            

        f.write("};\n\n")

        f.write(f"#endif // {guard}\n")

    # Clean up temp font file
    os.remove(tmp_font_path)

    header_size_kb = os.path.getsize(output_header) / 1024
    print(f"Bitmap header file size: {header_size_kb:.2f} KB")

    return all_bytes, bitmap_widths, bitmap_start_indexes, unpadded_widths