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

import os
from math import ceil

import os
from math import ceil

import os
from math import ceil

def display_bitmap_row(data, GLYPH_HEIGHT, glyph_widths, bitmap_offsets, unpadded_widths):
    """
    Displays multiple monochrome bitmaps side by side as ASCII art.
    If the glyphs don't fit on a single line, they are displayed in a grid
    that adapts to the terminal width.

    Args:
        data (list[int] or bytes): Packed binary image data (1-bit per pixel),
            glyphs stored row-by-row consecutively.
        GLYPH_HEIGHT (int): Height (in pixels) of each glyph (fixed).
        glyph_widths (list[int]): List of glyph widths (in pixels) for each glyph (these are the byte-aligned widths).
        bitmap_offsets (list[int]): Start index (in bytes) of each glyph in `data`.
        unpadded_widths (list[int]): List of the *true pixel widths* of each glyph's content
                                      (before byte-alignment padding).

    Each glyph occupies ceil(width / 8) bytes per row and GLYPH_HEIGHT rows total.
    """
    terminal_width = os.get_terminal_size().columns
    GLYPH_SPACING = 0 # No extra space between bitmaps

    # Prepare a list of (offset, byte_aligned_width, unpadded_width) for easier iteration
    glyphs_info = list(zip(bitmap_offsets, glyph_widths, unpadded_widths))

    if not glyphs_info:
        return

    # Calculate the effective width of the widest glyph's UNPADDED content
    # This is used for grid layout calculation to determine how many 'visual' characters fit.
    max_unpadded_width = max(unpadded_width for _, _, unpadded_width in glyphs_info) if glyphs_info else 1
    
    # Calculate total width if all glyphs were on one line using their UNPADDED widths
    total_single_line_width = sum(unpadded_width for _, _, unpadded_width in glyphs_info)

    if total_single_line_width <= terminal_width:
        # Display all glyphs on a single line, using their UNPADDED widths
        for row in range(GLYPH_HEIGHT):
            line = ""
            for offset, byte_aligned_width, unpadded_width in glyphs_info:
                bytes_per_row = ceil(byte_aligned_width / 8) # Use byte_aligned_width for data retrieval
                row_start = offset + row * bytes_per_row
                end_byte_index = min(row_start + bytes_per_row, len(data))
                row_bytes = data[row_start : end_byte_index]
                
                if not row_bytes:
                    row_bits = '0' * byte_aligned_width 
                else:
                    row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
                
                # --- FIX START ---
                # Convert the relevant bits to ASCII art. Slicing ensures we don't read past available bits.
                glyph_art_part = ''.join('█' if bit == '1' else ' ' for bit in row_bits[:unpadded_width])
                
                # Pad with spaces to ensure the final width matches unpadded_width.
                # This handles cases where unpadded_width is greater than byte_aligned_width.
                glyph_line = glyph_art_part.ljust(unpadded_width)
                # --- FIX END ---
                line += glyph_line
            print(line)
    else:
        # Determine how many glyphs fit on one row in the grid
        # Based on the widest glyph's UNPADDED display width
        glyphs_per_grid_row = (terminal_width // max_unpadded_width) if max_unpadded_width > 0 else 1
        
        if glyphs_per_grid_row == 0:
            glyphs_per_grid_row = 1 

        num_glyphs = len(glyphs_info)
        num_grid_rows = ceil(num_glyphs / glyphs_per_grid_row)

        for grid_row_idx in range(num_grid_rows):
            # Get the slice of glyphs for the current grid row
            start_glyph_idx = grid_row_idx * glyphs_per_grid_row
            end_glyph_idx = min(start_glyph_idx + glyphs_per_grid_row, num_glyphs)
            current_grid_row_glyphs = glyphs_info[start_glyph_idx : end_glyph_idx]

            # Iterate through each pixel row for the current grid row
            for pixel_row in range(GLYPH_HEIGHT):
                line = ""
                for offset, byte_aligned_width, unpadded_width in current_grid_row_glyphs:
                    bytes_per_row = ceil(byte_aligned_width / 8)
                    row_start = offset + pixel_row * bytes_per_row
                    end_byte_index = min(row_start + bytes_per_row, len(data))
                    row_bytes = data[row_start : end_byte_index]
                    
                    if not row_bytes:
                        row_bits = '0' * byte_aligned_width
                    else:
                        row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
                    
                    # --- FIX START ---
                    # Convert the relevant bits to ASCII art. Slicing ensures we don't read past available bits.
                    glyph_art_part = ''.join('█' if bit == '1' else ' ' for bit in row_bits[:unpadded_width])
                    
                    # Pad with spaces to ensure the final width matches unpadded_width.
                    # This handles cases where unpadded_width is greater than byte_aligned_width.
                    glyph_line = glyph_art_part.ljust(unpadded_width)
                    # --- FIX END ---
                    
                    line += glyph_line 
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