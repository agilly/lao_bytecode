"""
Debugging Utilities for Grapheme Cluster Bitmap Rendering.

This module contains utility functions for:
1. Displaying monochrome bitmap data as ASCII art in the terminal.
2. Printing grapheme cluster lists and their corresponding index mappings for inspection.

Useful for verifying the correctness of font rendering and character indexing
when preparing data for embedded text display systems.
"""

def display_bitmap_row(data, GLYPH_HEIGHT, glyph_widths, bitmap_offsets):
    """
    Displays multiple monochrome bitmaps side by side as ASCII art.

    Args:
        data (list[int] or bytes): Packed binary image data (1-bit per pixel),
            glyphs stored row-by-row consecutively.
        GLYPH_HEIGHT (int): Height (in pixels) of each glyph (fixed).
        glyph_widths (list[int]): List of glyph widths (in pixels) for each glyph.
        bitmap_offsets (list[int]): Start index (in bytes) of each glyph in `data`.

    Each glyph occupies ceil(width / 8) bytes per row and GLYPH_HEIGHT rows total.
    """
    from math import ceil

    for row in range(GLYPH_HEIGHT):
        line = ""
        for offset, width in zip(bitmap_offsets, glyph_widths):
            bytes_per_row = ceil(width / 8)
            row_start = offset + row * bytes_per_row
            row_bytes = data[row_start : row_start + bytes_per_row]
            row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
            line += ''.join('█' if bit == '1' else ' ' for bit in row_bits[:width])
            line += ' '  # space between glyphs
        print(line)


def print_char_and_index_lists(char_list, index_list):
    """
    Prints the character list and index list in a readable format.

    Args:
        char_list (list[str]): List of grapheme clusters.
        index_list (list[list[int]]): List of index lists for each input string.
    """
    print("Character List:")
    print('[' + ' '.join(char_list) + ']')
    print("\nIndex List:")
    for i, indices in enumerate(index_list):
        print(f"String {i}: {indices}")

import math

def make_dummy_glyphs():
    GLYPH_HEIGHT = 20
    glyph_widths = [15, 15, 15]  # all 15px wide
    glyph_data = bytearray()

    for idx in range(3):  # glyphs "a", "b", "c"
        for row in range(GLYPH_HEIGHT):
            if idx == 0:  # "a" – vertical stripe pattern: 101010101...
                bits = ''.join('10' if i % 2 == 0 else '01' for i in range(math.ceil(15/2)))[:15]
            elif idx == 1:  # "b" – checkerboard
                if row % 2 == 0:
                    bits = '101010101010101'
                else:
                    bits = '010101010101010'
            else:  # "c" – diagonal from top-left to bottom-right
                bits = ['0'] * 15
                if row < 15:
                    bits[row] = '1'
                bits = ''.join(bits)
            
            # pad to 16 bits to fill 2 bytes
            bits_padded = bits.ljust(16, '0')
            byte1 = int(bits_padded[:8], 2)
            byte2 = int(bits_padded[8:], 2)
            glyph_data.append(byte1)
            glyph_data.append(byte2)

    return glyph_data, GLYPH_HEIGHT, glyph_widths

# glyph_data, GLYPH_HEIGHT, glyph_widths = make_dummy_glyphs()
# display_bitmap_row(glyph_data, GLYPH_HEIGHT, glyph_widths)