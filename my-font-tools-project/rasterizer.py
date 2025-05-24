import freetype
import numpy as np
import matplotlib.pyplot as plt

# Load the font
face = freetype.Face("./Phetsarath-Regular.ttf")

# Set pixel size (height in pixels)
face.set_pixel_sizes(0, 24)

# Choose a character
char = 'ກ'  # Lao letter Ko (U+0E81)

# Load and render the glyph
face.load_char(char, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)

# Access the bitmap
bitmap = face.glyph.bitmap
width = bitmap.width
rows = bitmap.rows
buffer = bitmap.buffer

# Convert to numpy array (1-bit monochrome)
bitmap_array = np.unpackbits(np.frombuffer(buffer, dtype=np.uint8)).reshape(rows, -1)[:, :width]

# Display it
plt.imshow(bitmap_array, cmap='gray')
plt.title(f"Rasterized glyph for '{char}'")
plt.axis('off')
plt.show()
