from PIL import Image

def image_to_bitmap(image_path, pixel_width, pixel_height):
    # Open image and convert to grayscale
    img = Image.open(image_path).convert("L")
    
    # Resize to desired dimensions
    img = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
    
    # Convert to 1-bit (black & white)
    img_bw = img.point(lambda x: 0 if x < 128 else 1, mode='1')
    
    # Get pixel data
    pixels = img_bw.load()
    
    byte_array = []
    for y in range(pixel_height):
        byte = 0
        bits_filled = 0
        for x in range(pixel_width):
            pix = pixels[x, y]
            bit = 1 if pix == 0 else 0  # 0=black pixel becomes bit=1
            byte = (byte << 1) | bit
            bits_filled += 1
            if bits_filled == 8:
                byte_array.append(byte)
                byte = 0
                bits_filled = 0
        if bits_filled > 0:
            byte <<= (8 - bits_filled)
            byte_array.append(byte)
    return byte_array

# Example usage
image_path = "harfbuzz_freetype_rendered.png"
pixel_width = 30
pixel_height = 30
bitmap = image_to_bitmap(image_path, pixel_width, pixel_height)

# Print bitmap as hex
print(", ".join(f"0x{b:02X}" for b in bitmap))