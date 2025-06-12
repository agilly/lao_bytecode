 
# Glyph Bitmap Generator – Full Python Code

Author: Oisín Conlon

To understand the code for the glyph bitmap generator, here is a step by step guide:
This Python script generates 1-bit black-and-white glyph bitmaps from a list of grapheme clusters (characters or syllables) that come from Oli's preprocessing code, shapes them using HarfBuzz (the typesetter), renders them with FreeType (the printer), and exports the bitmaps to a C++ header file for use in embedded systems like Arduino.

---

##  Imports

```python
from PIL import Image                  # For image creation and some manipulation
import freetype                        # For loading and rendering font glyphs (printer)
import uharfbuzz as hb                 # For text shaping (cluster shaping, ligatures) (typesetter)
from tqdm import tqdm                  # For progress bars (optional extra but good for user interability and debugging)
import os                              # For filesystem operations
import tempfile                        # To store font temporarily (necessary for the version of harfbuzz)
import sys                             # For printing error messages to stderr
import math                            
```

---

##  Function: `generate_bitmaps_for_chars`

```python
def generate_bitmaps_for_chars(char_list, GLYPH_HEIGHT=30,
                                font_path="./font_files/NotoSansLao-Regular.ttf",
                                output_header="./arduino_code/glyph_bitmaps.h"):
```

- **Purpose**: Generate bitmap representations of characters and output them in a `.h` file. This is the over arching function.
- **Parameters**:
  - `char_list`: List of characters or grapheme clusters to render from pre processing code.
  - `GLYPH_HEIGHT`: The fixed height (in pixels) for output bitmaps input by user.
  - `font_path`: Path to the input TrueType font file so one can change font.
  - `output_header`: Where to save the resulting C++ header file.

---

## Load Font and Initialize HarfBuzz + FreeType

```python
with open(font_path, "rb") as f:
    font_data = f.read()
```

- Read font binary data from disk.

```python
hb_blob = hb.Blob(font_data)
hb_face = hb.Face(hb_blob)
hb_font = hb.Font(hb_face)
```

- Initializes HarfBuzz font structures for shaping.

```python
with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font_file:
    tmp_font_file.write(font_data)
    tmp_font_path = tmp_font_file.name
```

- Writes font data to a temporary file for FreeType to load.

```python
face = freetype.Face(tmp_font_path)
face.set_char_size(72 * 64)
```

- Loads the font with FreeType and set its size.

---

## Prepares for the beginning of the process

```python
all_bytes = []
bitmap_widths = []
unpadded_widths = []
```

- Lists to hold processed data:
  - `all_bytes`: All bitmap bytes
  - `bitmap_widths`: Width of each padded bitmap (padding explained later)
  - `unpadded_widths`: Widths before padding (so that the unpadded symbol can be rendered at the end)

---

##  Procesess Each Character

```python
for char in tqdm(char_list, desc="Processing characters"):
```

### Shape Text

```python
buf = hb.Buffer()
buf.add_str(char)
buf.guess_segment_properties()
hb.shape(hb_font, buf)
```

- Uses HarfBuzz to shape the character. This maps characters to combined glyphs.

```python
infos = buf.glyph_infos
positions = buf.glyph_positions
```

- Extracts ehat glyphs are being used and their positions.

---

## Render Glyphs with FreeType

```python
base_idx = 0
base_glyph = infos[base_idx].codepoint
```

- Selects the base glyph, usually a consonant.

```python
try:
    face.load_glyph(base_glyph, freetype.FT_LOAD_DEFAULT)
```

- Loads the base glyph.

### Fallback Handling

```python
except ValueError as e:
    # Use fallback metrics and blank canvas if the glyph can't be loaded
```

- Error handling for missing or invalid glyphs.

---

## Draws Glyphs onto a Temporary Canvas

```python
image = Image.new("L", (image_width, image_height), 255)
x = 0
y = 80
```

- Creates a blank grayscale image where glyphs will be drawn. This is like preparing the canvas for printing.

```python
for info, pos in zip(infos, positions):
    glyph_index = info.codepoint
```

- Loops over all glyphs in the harfbuzz shaped cluster.

```python
if glyph_index == 0:
    x += pos.x_advance // 64
    continue
```

- Skips `.notdef` glyphs but move pen position forward to were the next bit needs to be drawn.

---

### Load and Render Each Glyph

```python
face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
bitmap = face.glyph.bitmap
```

- Renders each glyph using FreeType (printing time)

```python
glyph_img = Image.frombytes('L', (w, h), bytes(bitmap.buffer))
```

- Converts raw bitmap to a Pillow image, like screenshotting a word document to get an image of the letter.

---

### Paste Glyphs on Canvas

```python
x_pos = x + (pos.x_offset // 64) + left
y_pos = y - (pos.y_offset // 64) - top
```

- Computes position for pasting.

```python
image.paste(0, (paste_x, paste_y), cropped_glyph_img)
```

- Pastes cropped glyph image onto canvas.

---

## Resizes and Crop Image

```python
img_resized = image.resize((resized_width, GLYPH_HEIGHT), Image.Resampling.NEAREST)
img_bw = img_resized.point(lambda p: 0 if p < 128 else 255, mode='1')
```

- Resizes and convert image to 1-bit black/white. This is so it is the correct size and form for the screen and is memory efficient.

---

###  Manual Horizontal Cropping

```python
# Find leftmost and rightmost black pixels to crop width tightly
```

- Searches columns for black pixels to determine cropping bounds.

```python
cropped_img_bw = img_bw.crop((first_pixel_col, 0, last_pixel_col + 1, img_bw.height))
```

- Crops image to actual content, gets rid of unnecessary whitespace harfbuzz creates. We used a manual cropper as Pillow's in built one was unable to do this.

---

## Padding + Byte Packing

```python
final_width = ((padded_width + 7) // 8) * 8
img_padded = Image.new("L", (final_width, GLYPH_HEIGHT), 255)
img_padded.paste(cropped_img_bw, (0, 0))
```

- Pad to nearest multiple of 8 pixels wide for byte alignment. This is so it can be stored efficiently on all microcontrollers. The padding is then stripped off again when the screen renders.

```python
pixels = img_final_bw.load()
for y_row in range(GLYPH_HEIGHT):
    for x_col in range(final_width):
        # Pack 1-bit pixels into bytes (8 pixels = 1 byte)
```

- Convert each row to a byte array.

---

##  Write Header File

```python
with open(output_header, "w", encoding="utf-8") as f:
```

###  Write Preprocessor Header

```cpp
#ifndef GLYPH_BITMAPS_H
#define GLYPH_BITMAPS_H
```

### Write Bitmap Array

```cpp
static const uint8_t glyph_bitmaps[] PROGMEM = {
  0xAB, 0xCD, ... // each line = 16 bytes
};
```

###  Write Width Arrays

```cpp
const uint16_t glyph_widths[] = { ... };
const uint16_t unpadded_widths[] = { ... };
```

###  Write Start Indexes

```cpp
const uint16_t bitmap_starts[] = { ... };
```

### Close Header

```cpp
#endif // GLYPH_BITMAPS_H
```

---

## Clean Up

```python
os.remove(tmp_font_path)
```

- Removes temporary font file.

---

## Done

```python
print(f"Bitmap header file size: {header_size_kb:.2f} KB")
```

- Reports output size to user as some microcontrollers have limited memory. 

---

## Return Packed Data

```python
return all_bytes, bitmap_widths, bitmap_start_indexes, unpadded_widths
```
