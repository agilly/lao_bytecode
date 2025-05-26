from PIL import Image, ImageOps

def image_to_bitmap(image_path, pixel_width, pixel_height):
    # Open image and convert to grayscale
    img = Image.open(image_path).convert("L")

    # Invert for autocropping (to treat glyph as white)
    img_inverted = ImageOps.invert(img)
    bbox = img_inverted.getbbox()
    if bbox:
        img = img.crop(bbox)  # Crop to bounding box
    # If bbox is None, image is blank; we skip cropping

    # Resize to target dimensions
    img = img.resize((pixel_width, pixel_height), Image.Resampling.NEAREST)

    # Binarize explicitly
    threshold = 128
    img = img.point(lambda p: 0 if p < threshold else 255, mode='L')

    # Optional: Save preview for verification
    img.save("processed_image_preview.png")

    pixels = img.load()
    byte_array = []
    for y in range(pixel_height):
        byte = 0
        bits_filled = 0
        for x in range(pixel_width):
            pix = pixels[x, y]
            bit = 1 if pix == 0 else 0  # 0 (black) -> 1, 255 (white) -> 0
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