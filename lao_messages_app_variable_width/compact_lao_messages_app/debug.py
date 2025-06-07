"""
Debugging Utilities for Grapheme Cluster Bitmap Rendering.

This module contains utility functions for:
1. Displaying monochrome bitmap data as ASCII art in the terminal.
2. Printing grapheme cluster lists and their corresponding index mappings for inspection.

Useful for verifying the correctness of font rendering and character indexing
when preparing data for embedded text display systems.
"""

import os
from math import ceil

def display_bitmap_row(data, GLYPH_HEIGHT, glyph_widths, bitmap_offsets):
    """
    Displays multiple monochrome bitmaps side by side as ASCII art.
    If the glyphs don't fit on a single line, they are displayed in a grid
    that adapts to the terminal width.

    Args:
        data (list[int] or bytes): Packed binary image data (1-bit per pixel),
            glyphs stored row-by-row consecutively.
        GLYPH_HEIGHT (int): Height (in pixels) of each glyph (fixed).
        glyph_widths (list[int]): List of glyph widths (in pixels) for each glyph.
        bitmap_offsets (list[int]): Start index (in bytes) of each glyph in `data`.

    Each glyph occupies ceil(width / 8) bytes per row and GLYPH_HEIGHT rows total.
    """
    terminal_width = os.get_terminal_size().columns
    GLYPH_SPACING = 1 # Space between glyphs

    # Prepare a list of (offset, width) for easier iteration
    glyphs_info = list(zip(bitmap_offsets, glyph_widths))

    if not glyphs_info:
        return

    # Calculate the effective width of the widest glyph including spacing for single-line fit check
    # For grid layout, we need individual glyph widths
    max_glyph_display_width = max(width for _, width in glyphs_info) + GLYPH_SPACING
    
    # Check if all glyphs can fit on one line (approximately)
    # This check is a bit rough, as individual glyphs have different widths.
    # A more precise check would sum up individual widths.
    # For simplicity, we'll assume a grid is better if the sum is too large.
    
    # Calculate total width if all glyphs were on one line
    total_single_line_width = sum(width + GLYPH_SPACING for _, width in glyphs_info) - GLYPH_SPACING

    if total_single_line_width <= terminal_width:
        # Display all glyphs on a single line
        for row in range(GLYPH_HEIGHT):
            line = ""
            for offset, width in glyphs_info:
                bytes_per_row = ceil(width / 8)
                row_start = offset + row * bytes_per_row
                row_bytes = data[row_start : row_start + bytes_per_row]
                row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
                line += ''.join('█' if bit == '1' else ' ' for bit in row_bits[:width])
                line += ' ' * GLYPH_SPACING # Add space between glyphs
            print(line)
    else:
        # Determine how many glyphs fit on one row in the grid
        # We'll base this on the widest glyph to ensure everything aligns
        glyphs_per_grid_row = (terminal_width + GLYPH_SPACING) // max_glyph_display_width
        
        # Ensure at least one glyph per row
        if glyphs_per_grid_row == 0:
            glyphs_per_grid_row = 1 

        num_glyphs = len(glyphs_info)
        num_grid_rows = ceil(num_glyphs / glyphs_per_grid_row)

        for grid_row_idx in range(num_grid_rows):
            # Get the slice of glyphs for the current grid row
            start_glyph_idx = grid_row_idx * glyphs_per_grid_row
            end_glyph_idx = min(start_glyph_idx + glyphs_per_grid_row, num_glyphs)
            current_grid_row_glyphs = glyphs_info[start_glyph_idx : end_glyph_idx]

            # Find the max width in this specific grid row for padding
            current_max_glyph_width = 0
            if current_grid_row_glyphs:
                current_max_glyph_width = max(width for _, width in current_grid_row_glyphs)

            # Iterate through each pixel row for the current grid row
            for pixel_row in range(GLYPH_HEIGHT):
                line = ""
                for offset, width in current_grid_row_glyphs:
                    bytes_per_row = ceil(width / 8)
                    row_start = offset + pixel_row * bytes_per_row
                    row_bytes = data[row_start : row_start + bytes_per_row]
                    row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
                    
                    glyph_line = ''.join('█' if bit == '1' else ' ' for bit in row_bits[:width])
                    
                    # Pad glyph_line to the max width of glyphs in this grid row for alignment
                    line += glyph_line.ljust(current_max_glyph_width)
                    line += ' ' * GLYPH_SPACING # Add space between glyphs
                print(line)
            print() # Add a blank line between grid rows for better separation


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