# The bitmap data as pairs of hex bytes (20 rows, 2 bytes each)
bitmap = [
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
    0x0F, 0xF0,
    0x0F, 0xF0,
    0x0C, 0x30,
    0x0C, 0x30,
    0x0C, 0x30,
    0x0C, 0x30,
    0x0C, 0x30,
    0x0C, 0x30,
    0x0F, 0x30,
    0x0F, 0x30,
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0x00,
]

def display_bitmap(data):
    # Each row is 2 bytes = 16 bits wide
    for i in range(0, len(data), 2):
        # Combine two bytes into one 16-bit integer
        row = (data[i] << 8) | data[i + 1]
        # Convert to binary string, pad to 16 bits
        bits = format(row, '016b')
        # Replace 1s with block, 0s with space
        line = ''.join('█' if bit == '1' else ' ' for bit in bits)
        print(line)

display_bitmap(bitmap)