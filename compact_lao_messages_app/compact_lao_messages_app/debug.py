"""
Debugging Utilities for Grapheme Cluster Bitmap Rendering.

This module contains utility functions for:
1. Displaying monochrome bitmap data as ASCII art in the terminal.
2. Printing grapheme cluster lists and their corresponding index mappings for inspection.

Useful for verifying the correctness of font rendering and character indexing
when preparing data for embedded text display systems.
"""

def display_bitmap(data, row_width_bytes=4):
    """
    Displays a monochrome bitmap as ASCII art in the terminal.

    Each byte in `data` represents 8 pixels (MSB first). This function unpacks
    the bits and prints them using '█' for black pixels (1) and space for white (0).

    Args:
        data (list[int] or bytes): Packed binary image data (1-bit per pixel).
        row_width_bytes (int): Number of bytes per row (default is 4, i.e., 32 pixels wide).

    Example output for one row:
        ███   █  █     ██
    """

    total_rows = len(data) // row_width_bytes
    
    for row_idx in range(total_rows):
        row_bytes = data[row_idx * row_width_bytes : (row_idx + 1) * row_width_bytes]
        row_bits = ''.join(format(byte, '08b') for byte in row_bytes)
        # Convert bits to ASCII art
        line = ''.join('█' if bit == '1' else ' ' for bit in row_bits)
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