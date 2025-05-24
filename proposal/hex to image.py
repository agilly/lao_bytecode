hex_data = [
    0x00, 0x00, 0x0E, 0x00,
    0x11, 0x00, 0x11, 0x00,
    0x11, 0x00, 0x11, 0x00,
    0x1F, 0x00, 0x11, 0x00,
    0x11, 0x00, 0x0E, 0x00,
    0x00, 0x00, 0x00, 0x00
]

def hex_to_pixel_art(hex_values, width=8):
    # Go through each hex value
    for i in range(0, len(hex_values), 2):  # Step by 2, in case the higher byte is ignored
        byte = hex_values[i]  # Lower byte
        # Convert to binary string, remove '0b', pad with zeros
        bin_str = format(byte, f'0{width}b')
        # Replace 1 with block and 0 with space
        row = ''.join('█' if bit == '1' else ' ' for bit in bin_str)
        print(row)

hex_to_pixel_art(hex_data)
