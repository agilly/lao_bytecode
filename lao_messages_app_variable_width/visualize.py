#!/usr/bin/env python3
"""
Terminal-based visualization of Lao text bitmaps.
Renders characters as ASCII art using block characters to preview how they'll appear on the OLED display.
"""

import argparse
import sys
import os
from PIL import Image
import freetype
import uharfbuzz as hb
import tempfile
import math
import grapheme

def generate_char_bitmap(char, glyph_height=30, font_path="./font_files/NotoSansLao-Regular.ttf"):
    """
    Generate a bitmap for a single character using the same logic as the main application.
    Returns a PIL Image in 1-bit mode.
    """
    try:
        with open(font_path, "rb") as f:
            font_data = f.read()
    except FileNotFoundError:
        print(f"Error: Font file not found at {font_path}", file=sys.stderr)
        sys.exit(1)

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

    try:
        # Shape text using HarfBuzz
        buf = hb.Buffer()
        buf.add_str(char)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        infos = buf.glyph_infos
        positions = buf.glyph_positions

        # Find base consonant (first glyph typically)
        base_idx = 0
        base_glyph = infos[base_idx].codepoint
    
        # Load base glyph metrics
        try:
            face.load_glyph(base_glyph, freetype.FT_LOAD_DEFAULT)
            base_width = face.glyph.metrics.horiAdvance // 64
            image_width = base_width
            image_height = 100
            wh_ratio = image_width / image_height
            image = Image.new("L", (image_width, image_height), 255)
            x = 0
            y = 80  # Empirical baseline position
        except (ValueError, Exception) as e:
            # Fallback for problematic glyphs
            base_width = glyph_height
            wh_ratio = 1.0
            image = Image.new("L", (glyph_height * 2, glyph_height * 2), 255)
            x = 0
            y = glyph_height

        for info, pos in zip(infos, positions):
            glyph_index = info.codepoint
            
            # Skip .notdef glyphs (glyph_index 0)
            if glyph_index == 0:
                x += pos.x_advance // 64
                continue

            try:
                face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
            except (ValueError, Exception) as e:
                x += pos.x_advance // 64
                continue

            bitmap = face.glyph.bitmap
            w, h = bitmap.width, bitmap.rows

            if w > 0 and h > 0:
                glyph_img = Image.frombytes('L', (w, h), bytes(bitmap.buffer))
                
                x_pos = x + (pos.x_offset // 64) + face.glyph.bitmap_left
                y_pos = y - (pos.y_offset // 64) - face.glyph.bitmap_top
                
                # Check bounds before pasting
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

        # Resize to target height
        resized_width = int(glyph_height * wh_ratio)
        img_resized = image.resize((resized_width, glyph_height), Image.Resampling.NEAREST)

        # Convert to 1-bit black & white
        img_bw = img_resized.point(lambda p: 0 if p < 128 else 255, mode='1')

        # Manual horizontal cropping to remove whitespace
        first_pixel_col = -1
        for x_col in range(img_bw.width):
            for y_row in range(img_bw.height):
                if img_bw.getpixel((x_col, y_row)) == 0:  # Found a black pixel
                    first_pixel_col = x_col
                    break
            if first_pixel_col != -1:
                break

        last_pixel_col = -1
        for x_col in range(img_bw.width - 1, -1, -1):
            for y_row in range(img_bw.height):
                if img_bw.getpixel((x_col, y_row)) == 0:  # Found a black pixel
                    last_pixel_col = x_col
                    break
            if last_pixel_col != -1:
                break
        
        if first_pixel_col != -1 and last_pixel_col != -1:
            # Crop horizontally using the discovered bounds
            cropped_img_bw = img_bw.crop((first_pixel_col, 0, last_pixel_col + 1, img_bw.height))
        else:
            # Handle case of entirely white image (e.g., space character)
            cropped_img_bw = Image.new('1', (glyph_height // 4, glyph_height), 255)

        return cropped_img_bw

    finally:
        # Clean up temp font file
        os.remove(tmp_font_path)


def bitmap_to_ascii(bitmap_image):
    """
    Convert a 1-bit PIL Image to ASCII art using block characters.
    Uses '█' for black pixels and ' ' for white pixels.
    """
    pixels = bitmap_image.load()
    width, height = bitmap_image.size
    
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            pixel = pixels[x, y]
            # In 1-bit mode: 0 = black, 1 = white
            if pixel == 0:
                line += "█"  # Full block character
            else:
                line += " "  # Space for white pixels
        lines.append(line)
    
    return lines


def visualize_text(text, font_height=30, font_path="./font_files/NotoSansLao-Regular.ttf", spacing=0):
    """
    Visualize a string of text as ASCII art in the terminal.
    """
    # Break text into grapheme clusters (individual characters)
    chars = list(grapheme.graphemes(text))
    
    if not chars:
        print("No characters to display")
        return
    
    print(f"Visualizing '{text}' at {font_height}px height:")
    print("=" * 50)
    
    # Generate bitmaps for each character
    char_bitmaps = []
    char_ascii_lines = []
    
    for char in chars:
        bitmap = generate_char_bitmap(char, font_height, font_path)
        ascii_lines = bitmap_to_ascii(bitmap)
        char_bitmaps.append(bitmap)
        char_ascii_lines.append(ascii_lines)
    
    # Find the maximum height (should all be font_height, but just in case)
    max_height = max(len(lines) for lines in char_ascii_lines) if char_ascii_lines else 0
    
    # Print character by character with labels
    for i, (char, lines) in enumerate(zip(chars, char_ascii_lines)):
        print(f"Character {i+1}: '{char}' (width: {len(lines[0]) if lines else 0}px)")
        for line in lines:
            print(line)
        print()  # Empty line between characters
    
    # Print combined horizontal view
    print("Combined horizontal view:")
    print("-" * 50)
    
    # Pad all character lines to the same height
    for lines in char_ascii_lines:
        while len(lines) < max_height:
            lines.append(" " * len(lines[0]) if lines else "")
    
    # Print each row across all characters
    for row in range(max_height):
        combined_line = ""
        for i, lines in enumerate(char_ascii_lines):
            if row < len(lines):
                combined_line += lines[row]
            # Add spacing between characters (except after the last one)
            if i < len(char_ascii_lines) - 1 and spacing > 0:
                combined_line += " " * spacing
        print(combined_line)


def main():
    parser = argparse.ArgumentParser(
        description="Visualize Lao text as ASCII art to preview OLED display output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python visualize.py --font-height 10 --text "ພົດຈະນານຸກົມ"
  python visualize.py --font-height 30 --text "ສະບາຍດີ" --spacing 2
  python visualize.py -s 20 -t "ລາວ" -p 1
        """
    )
    
    parser.add_argument(
        "--font-height", "-s",
        type=int,
        default=30,
        help="Font height in pixels (default: 30)"
    )
    
    parser.add_argument(
        "--text", "-t",
        type=str,
        required=True,
        help="Lao text to visualize"
    )
    
    parser.add_argument(
        "--font-path", "-f",
        type=str,
        default="./font_files/NotoSansLao-Regular.ttf",
        help="Path to font file (default: ./font_files/NotoSansLao-Regular.ttf)"
    )
    
    parser.add_argument(
        "--spacing", "-p",
        type=int,
        default=0,
        help="Number of spaces between characters in combined view (default: 0)"
    )
    
    args = parser.parse_args()
    
    # Validate font height
    if args.font_height < 5 or args.font_height > 100:
        print("Error: Font height must be between 5 and 100 pixels", file=sys.stderr)
        sys.exit(1)
    
    # Check if font file exists
    if not os.path.exists(args.font_path):
        print(f"Error: Font file not found at {args.font_path}", file=sys.stderr)
        print("Make sure you're running this from the lao_messages_app_variable_width directory", file=sys.stderr)
        sys.exit(1)
    
    try:
        visualize_text(args.text, args.font_height, args.font_path, args.spacing)
    except KeyboardInterrupt:
        print("\nVisualization interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()