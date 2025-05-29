import uharfbuzz as hb
from PIL import Image
import freetype
import os
import tempfile

import unicodedata
import re

import unicodedata
import re

def preprocess_text(text: str) -> str:
    """
    Preprocess text for HarfBuzz shaping:
    - Normalize Unicode to NFC form
    - Remove control characters and unsupported characters
    - Optionally, remove or replace unwanted characters
    
    Args:
        text (str): Raw input text
    
    Returns:
        str: Cleaned and normalized text ready for shaping
    """
    # Normalize Unicode (use NFC or NFD depending on your font/script needs)
    normalized_text = unicodedata.normalize('NFC', text)

    # Remove control characters (e.g. \u200b zero width space, other invisible controls)
    cleaned_text = ''.join(ch for ch in normalized_text if unicodedata.category(ch)[0] != 'C')

    # Optionally remove non-Lao characters if you want to strictly restrict script:
    # Lao Unicode range: U+0E80 to U+0EFF
    # Uncomment if needed:
    # cleaned_text = ''.join(ch for ch in cleaned_text if '\u0E80' <= ch <= '\u0EFF' or ch.isspace())

    # Remove extra whitespace (collapse multiple spaces)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text



def render_text_with_harfbuzz_freetype(text: str, font_path: str, output_path: str = "harfbuzz_freetype_rendered.png"):
    """
    Render complex text using HarfBuzz for shaping and FreeType for rasterization.

    Parameters:
        text (str): The text to render.
        font_path (str): Path to the TrueType font (.ttf) file.
        output_path (str): Where to save the rendered image.
    """
    
    # Read font data from the font file
    with open(font_path, "rb") as f:
        font_data = f.read()

    # Setup HarfBuzz with the font data
    hb_blob = hb.Blob(font_data)             # Create a HarfBuzz blob from the font binary
    hb_face = hb.Face(hb_blob)               # Create a face object from the blob
    hb_font = hb.Font(hb_face)               # Create a font object from the face

    # Create a buffer and shape the text using HarfBuzz
    buf = hb.Buffer()                        # Create a HarfBuzz buffer
    buf.add_str(text)                        # Add text to the buffer
    buf.guess_segment_properties()           # Let HarfBuzz detect script/direction/language
    hb.shape(hb_font, buf)                   # Shape the text, populating glyph info/positions

    # Extract glyph information and positioning
    infos = buf.glyph_infos                  # Glyph indices and clusters
    positions = buf.glyph_positions          # Glyph positioning (advance/offsets)

    # Write the font to a temporary file for FreeType to load
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font_file:
        tmp_font_file.write(font_data)
        tmp_font_path = tmp_font_file.name

    try:
        # Load the font using FreeType
        face = freetype.Face(tmp_font_path)
        face.set_char_size(72 * 64)          # Set character size in 26.6 fixed-point format

        # Create a blank image for rendering the text
        image_width, image_height = 10000, 150
        image = Image.new("L", (image_width, image_height), 255)  # White background
        x, y = 50, 100                      # Starting position for the text baseline

        # Loop through each glyph and render it
        for info, pos in zip(infos, positions):
            glyph_index = info.codepoint     # HarfBuzz glyph index

            # Load and render glyph into a bitmap
            face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
            bitmap = face.glyph.bitmap       # Get the rendered bitmap

            # Glyph metrics
            w, h = bitmap.width, bitmap.rows
            top = face.glyph.bitmap_top      # Vertical distance from baseline to top
            left = face.glyph.bitmap_left    # Horizontal offset

            # Create an image from the bitmap buffer
            glyph_image = Image.frombytes('L', (w, h), bytes(bitmap.buffer))

            # Compute glyph position on the canvas
            x_pos = x + (pos.x_offset // 64) + left
            y_pos = y - (pos.y_offset // 64) - top

            # Paste glyph onto the main image (use glyph image as its own mask)
            image.paste(0, (x_pos, y_pos), glyph_image)


            # Move to the next glyph position

            x += 2 * pos.x_advance // 64
            y -= pos.y_advance // 64

        # Show and save the final rendered image
        image.show()
        image.save(output_path)

    finally:
        # Clean up temporary font file
        os.remove(tmp_font_path)

# Example usage
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    font_path = os.path.join(BASE_DIR, "./Phetsarath-Regular.ttf")
    text = "ກຂຄງຈຊຍຏຑຒດຕຖທນບປຜຝພຟມຢຣລວສຫອຮຯກະກັກາກຳກິກີກຶກືກຸກູຂະຂັຂາຂຳຂິຂີຂຶຂືຂຸຂູຄະຄັຄາຄຳຄິຄີຄຶຄືຄຸຄູງະງັງາງຳງິງີງຶງືງຸງູຈະຈັຈາຈຳຈິຈີຈຶຈືຈຸຈູຊະຊັຊາຊຳຊິຊີຊຶຊືຊຸຊູຍະຍັຍາຍຳຍິຍີຍຶຍືຍຸຍູດະດັດາດຳດິດີດຶດືດຸດູຕະຕັຕາຕຳຕິຕີຕຶຕືຕຸຕູຖະຖັຖາຖຳຖິຖີຖຶຖືຖຸຖູທະທັທາທຳທິທີທຶທືທຸທູນະນັນານຳນິນີນຶນືນຸນູບະບັບາບຳບິບີບຶບືບຸບູປະປັປາປຳປິປີປຶປືປຸປູຜະຜັຜາຜຳຜິຜີຜຶຜືຜຸຜູຝະຝັຝາຝຳຝິຝີຝຶຝືຝຸຝູພະພັພາພຳພິພີພຶພືພຸພູຟະຟັຟາຟຳຟິຟີຟຶຟືຟຸຟູມະມັມາມຳມິມີມຶມືມຸມູຢະຢັຢາຢຳຢິຢີຢຶຢືຢຸຢູຣະຣັຣາຣຳຣິຣີຣຶຣືຣຸຣູລະລັລາລຳລິລີລຶລືລຸລູວະວັວາວຳວິວີວຶວືວຸວູສະສັສາສຳສິສີສຶສືສຸສູຫະຫັຫາຫຳຫິຫີຫຶຫືຫຸຫູອະອັອາອຳອິອີອຶອືອຸອູຮະຮັຮາຮຳຮິຮີຮຶຮືຮຸຮູຯະຯັຯາຯຳຯິຯີຯຶຯືຯຸຯູກ່ກ້ກ໊ກ໋ຂ່ຂ້ຂ໊ຂ໋ຄ່ຄ້ຄ໊ຄ໋ງ່ງ້ງ໊ງ໋ຈ່ຈ້ຈ໊ຈ໋ຊ່ຊ້ຊ໊ຊ໋ຍ່ຍ້ຍ໊ຍ໋ຏ່ຏ້ຏ໊ຏ໋ຑ່ຑ້ຑ໊ຑ໋ຒ່ຒ້ຒ໊ຒ໋ດ່ດ້ດ໊ດ໋ຕ່ຕ້ຕ໊ຕ໋ຖ່ຖ້ຖ໊ຖ໋ທ່ທ້ທ໊ທ໋ນ່ນ້ນ໊ນ໋ບ່ບ້ບ໊ບ໋ປ່ປ້ປ໊ປ໋ຜ່ຜ້ຜ໊ຜ໋ຝ່ຝ້ຝ໊ຝ໋ພ່ພ້ພ໊ພ໋ຟ່ຟ້ຟ໊ຟ໋ມ່ມ້ມ໊ມ໋ຢ່ຢ້ຢ໊ຢ໋ຣ່ຣ້ຣ໊ຣ໋ລ່ລ້ລ໊ລ໋ວ່ວ້ວ໊ວ໋ສ່ສ້ສ໊ສ໋ຫ່ຫ້ຫ໊ຫ໋ອ່ອ້ອ໊ອ໋ຮ່ຮ້ຮ໊ຮ໋ຯ່ຯ້ຯ໊ຯ໋ກະ່ກະ້ກະ໊ກະ໋ກັ່ກັ້ກັ໊ກັ໋ກາ່ກາ້ກາ໊ກາ໋ກຳ່ກຳ້ກຳ໊ກຳ໋ກິ່ກິ້ກິ໊ກິ໋ກີ່ກີ້ກີ໊ກີ໋ກຶ່ກຶ້ກຶ໊ກຶ໋ກື່ກື້ກື໊ກື໋ກຸ່ກຸ້ກຸ໊ກຸ໋ກູ່ກູ້ກູ໊ກູ໋ຂະ່ຂະ້ຂະ໊ຂະ໋ຂັ່ຂັ້ຂັ໊ຂັ໋ຂາ່ຂາ້ຂາ໊ຂາ໋ຂຳ່ຂຳ້ຂຳ໊ຂຳ໋ຂິ່ຂິ້ຂິ໊ຂິ໋ຂີ່ຂີ້ຂີ໊ຂີ໋ຂຶ່ຂຶ້ຂຶ໊ຂຶ໋ຂື່ຂື້ຂື໊ຂື໋ຂຸ່ຂຸ້ຂຸ໊ຂຸ໋ຂູ່ຂູ້ຂູ໊ຂູ໋ຄະ່ຄະ້ຄະ໊ຄະ໋ຄັ່ຄັ້ຄັ໊ຄັ໋ຄາ່ຄາ້ຄາ໊ຄາ໋ຄຳ່ຄຳ້ຄຳ໊ຄຳ໋ຄິ່ຄິ້ຄິ໊ຄິ໋ຄີ່ຄີ້ຄີ໊ຄີ໋ຄຶ່ຄຶ້ຄຶ໊ຄຶ໋ຄື່ຄື້ຄື໊ຄື໋ຄຸ່ຄຸ້ຄຸ໊ຄຸ໋ຄູ່ຄູ້ຄູ໊ຄູ໋ງະ່ງະ້ງະ໊ງະ໋ງັ່ງັ້ງັ໊ງັ໋ງາ່ງາ້ງາ໊ງາ໋ງຳ່ງຳ້ງຳ໊ງຳ໋ງິ່ງິ້ງິ໊ງິ໋ງີ່ງີ້ງີ໊ງີ໋ງຶ່ງຶ້ງຶ໊ງຶ໋ງື່ງື້ງື໊ງື໋ງຸ່ງຸ້ງຸ໊ງຸ໋ງູ່ງູ້ງູ໊ງູ໋ຈະ່ຈະ້ຈະ໊ຈະ໋ຈັ່ຈັ້ຈັ໊ຈັ໋ຈາ່ຈາ້ຈາ໊ຈາ໋ຈຳ່ຈຳ້ຈຳ໊ຈຳ໋ຈິ່ຈິ້ຈິ໊ຈິ໋ຈີ່ຈີ້ຈີ໊ຈີ໋ຈຶ່ຈຶ້ຈຶ໊ຈຶ໋ຈື່ຈື້ຈື໊ຈື໋ຈຸ່ຈຸ້ຈຸ໊ຈຸ໋ຈູ່ຈູ້ຈູ໊ຈູ໋ຊະ່ຊະ້ຊະ໊ຊະ໋ຊັ່ຊັ້ຊັ໊ຊັ໋ຊາ່ຊາ້ຊາ໊ຊາ໋ຊຳ່ຊຳ້ຊຳ໊ຊຳ໋ຊິ່ຊິ້ຊິ໊ຊິ໋ຊີ່ຊີ້ຊີ໊ຊີ໋ຊຶ່ຊຶ້ຊຶ໊ຊຶ໋ຊື່ຊື້ຊື໊ຊື໋ຊຸ່ຊຸ້ຊຸ໊ຊຸ໋ຊູ່ຊູ້ຊູ໊ຊູ໋ຍະ່ຍະ້ຍະ໊ຍະ໋ຍັ່ຍັ້ຍັ໊ຍັ໋ຍາ່ຍາ້ຍາ໊ຍາ໋ຍຳ່ຍຳ້ຍຳ໊ຍຳ໋ຍິ່ຍິ້ຍິ໊ຍິ໋ຍີ່ຍີ້ຍີ໊ຍີ໋ຍຶ່ຍຶ້ຍຶ໊ຍຶ໋ຍື່ຍື້ຍື໊ຍື໋ຍຸ່ຍຸ້ຍຸ໊ຍຸ໋ຍູ່ຍູ້ຍູ໊ຍູ໋ຏະ່ຏະ້ຏະ໊ຏະ໋ຏັ່ຏັ້ຏັ໊ຏັ໋ຏາ່ຏາ້າ໋ະ່ຑະ້ຑະ໊ະ໋າ່ຑາ້ຑາ໊ຑາ໋ຑຸ້ຑຸ໊ຑຸ໋ຑູ່ຑູ້ຑູ໊ຑູ໋ຒະ່ຒະ້ຒະ໊ຒະ໋ຒັ່ຒັ້ຒັ໊ຒັ໋ຒາ່ຒາ້ຒາ໊ຒາ໋ຒຳ່ຒຳ້ຒຳ໊ຒຳ໋ຒິ່ຒິ້ຒິ໊ຒິ໋ຒີ່ຒີ້ຒີ໊ຒີ໋ຒຶ່ຒຶ້ຒຶ໊ຒຶ໋ຒື່ຒື້ຒື໊ຒື໋ຒຸ່ຒຸ້ຒຸ໊ຒຸ໋ຒູ່ຒູ້ຒູ໊ຒູ໋ດະ່ດະ້ດະ໊ດະ໋ດັ່ດັ້ດັ໊ດັ໋ດາ່ດາ້ດາ໊ດາ໋ດຳ່ດຳ້ດຳ໊ດຳ໋ດິ່ດິ້ດິ໊ດິ໋ດີ່ດີ້ດີ໊ດີ໋ດຶ່ດຶ້ດຶ໊ດຶ໋ດື່ດື້ດື໊ດື໋ດຸ່ດຸ້ດຸ໊ດຸ໋ດູ່ດູ້ດູ໊ດູ໋ຕະ່ຕະ້ຕະ໊ຕະ໋ຕັ່ຕັ້ຕັ໊ຕັ໋ຕາ່ຕາ້ຕາ໊ຕາ໋ຕຳ່ຕຳ້ຕຳ໊ຕຳ໋ຕິ່ຕິ້ຕິ໊ຕິ໋ຕີ່ຕີ້ຕີ໊ຕີ໋ຕຶ່ຕຶ້ຕຶ໊ຕຶ໋ຕື່ຕື້ຕື໊ຕື໋ຕຸ່ຕຸ້ຕຸ໊ຕຸ໋ຕູ່ຕູ້ຕູ໊ຕູ໋ຖະ່ຖະ້ຖະ໊ຖະ໋ຖັ່ຖັ້ຖັ໊ຖັ໋ຖາ່ຖາ້ຖາ໊ຖາ໋ຖຳ່ຖຳ້ຖຳ໊ຖຳ໋ຖິ່ຖິ້ຖິ໊ຖິ໋ຖີ່ຖີ້ຖີ໊ຖີ໋ຖຶ່ຖຶ້ຖຶ໊ຖຶ໋ຖື່ຖື້ຖື໊ຖື໋ຖຸ່ຖຸ້ຖຸ໊ຖຸ໋ຖູ່ຖູ້ຖູ໊ຖູ໋ທະ່ທະ້ທະ໊ທະ໋ທັ່ທັ້ທັ໊ທັ໋ທາ່ທາ້ທາ໊ທາ໋ທຳ່ທຳ້ທຳ໊ທຳ໋ທິ່ທິ້ທິ໊ທິ໋ທີ່ທີ້ທີ໊ທີ໋ທຶ່ທຶ້ທຶ໊ທຶ໋ທື່ທື້ທື໊ທື໋ທຸ່ທຸ້ທຸ໊ທຸ໋ທູ່ທູ້ທູ໊ທູ໋ນະ່ນະ້ນະ໊ນະ໋ນັ່ນັ້ນັ໊ນັ໋ນາ່ນາ້ນາ໊ນາ໋ນຳ່ນຳ້ນຳ໊ນຳ໋ນິ່ນິ້ນິ໊ນິ໋ນີ່ນີ້ນີ໊ນີ໋ນຶ່ນຶ້ນຶ໊ນຶ໋ນື່ນື້ນື໊ນື໋ນຸ່ນຸ້ນຸ໊ນຸ໋ນູ່ນູ້ນູ໊ນູ໋ບະ່ບະ້ບະ໊ບະ໋ບັ່ບັ້ບັ໊ບັ໋ບາ່ບາ້ບາ໊ບາ໋ບຳ່ບຳ້ບຳ໊ບຳ໋ບິ່ບິ້ບິ໊ບິ໋ບີ່ບີ້ບີ໊ບີ໋ບຶ່ບຶ້ບຶ໊ບຶ໋ບື່ບື້ບື໊ບື໋ບຸ່ບຸ້ບຸ໊ບຸ໋ບູ່ບູ້ບູ໊ບູ໋ປະ່ປະ້ປະ໊ປະ໋ປັ່ປັ້ປັ໊ປັ໋ປາ່ປາ້ປາ໊ປາ໋ປຳ່ປຳ້ປຳ໊ປຳ໋ປິ່ປິ້ປິ໊ປິ໋ປີ່ປີ້ປີ໊ປີ໋ປຶ່ປຶ້ປຶ໊ປຶ໋ປື່ປື້ປື໊ປື໋ປຸ່ປຸ້ປຸ໊ປຸ໋ປູ່ປູ້ປູ໊ປູ໋ຜະ່ຜະ້ຜະ໊ຜະ໋ຜັ່ຜັ້ຜັ໊ຜັ໋ຜາ່ຜາ້ຜາ໊ຜາ໋ຜຳ່ຜຳ້ຜຳ໊ຜຳ໋ຜິ່ຜິ້ຜິ໊ຜິ໋ຜີ່ຜີ້ຜີ໊ຜີ໋ຜຶ່ຜຶ້ຜຶ໊ຜຶ໋ຜື່ຜື້ຜື໊ຜື໋ຜຸ່ຜຸ້ຜຸ໊ຜຸ໋ຜູ່ຜູ້ຜູ໊ຜູ໋ຝະ່ຝະ້ຝະ໊ຝະ໋ຝັ່ຝັ້ຝັ໊ຝັ໋ຝາ່ຝາ້ຝາ໊ຝາ໋ຝຳ່ຝຳ້ຝຳ໊ຝຳ໋ຝິ່ຝິ້ຝິ໊ຝິ໋ຝີ່ຝີ້ຝີ໊ຝີ໋ຝຶ່ຝຶ້ຝຶ໊ຝຶ໋ຝື່ຝື້ຝື໊ຝື໋ຝຸ່ຝຸ້ຝຸ໊ຝຸ໋ຝູ່ຝູ້ຝູ໊ຝູ໋ພະ່ພະ້ພະ໊ພະ໋ພັ່ພັ້ພັ໊ພັ໋ພາ່ພາ້ພາ໊ພາ໋ພຳ່ພຳ້ພຳ໊ພຳ໋ພິ່ພິ້ພິ໊ພິ໋ພີ່ພີ້ພີ໊ພີ໋ພຶ່ພຶ້ພຶ໊ພຶ໋ພື່ພື້ພື໊ພື໋ພຸ່ພຸ້ພຸ໊ພຸ໋ພູ່ພູ້ພູ໊ພູ໋ຟະ່ຟະ້ຟະ໊ຟະ໋ຟັ່ຟັ້ຟັ໊ຟັ໋ຟາ່ຟາ້ຟາ໊ຟາ໋ຟຳ່ຟຳ້ຟຳ໊ຟຳ໋ຟິ່ຟິ້ຟິ໊ຟິ໋ຟີ່ຟີ້ຟີ໊ຟີ໋ຟຶ່ຟຶ້ຟຶ໊ຟຶ໋ຟື່ຟື້ຟື໊ຟື໋ຟຸ່ຟຸ້ຟຸ໊ຟຸ໋ຟູ່ຟູ້ຟູ໊ຟູ໋ມະ່ມະ້ມະ໊ມະ໋ມັ່ມັ້ມັ໊ມັ໋ມາ່ມາ້ມາ໊ມາ໋ມຳ່ມຳ້ມຳ໊ມຳ໋ມິ່ມິ້ມິ໊ມິ໋ມີ່ມີ້ມີ໊ມີ໋ມຶ່ມຶ້ມຶ໊ມຶ໋ມື່ມື້ມື໊ມື໋ມຸ່ມຸ້ມຸ໊ມຸ໋ມູ່ມູ້ມູ໊ມູ໋ຢະ່ຢະ້ຢະ໊ຢະ໋ຢັ່ຢັ້ຢັ໊ຢັ໋ຢາ່ຢາ້ຢາ໊ຢາ໋ຢຳ່ຢຳ້ຢຳ໊ຢຳ໋ຢິ່ຢິ້ຢິ໊ຢິ໋ຢີ່ຢີ້ຢີ໊ຢີ໋ຢຶ່ຢຶ້ຢຶ໊ຢຶ໋ຢື່ຢື້ຢື໊ຢື໋ຢຸ່ຢຸ້ຢຸ໊ຢຸ໋ຢູ່ຢູ້ຢູ໊ຢູ໋ຣະ່ຣະ້ຣະ໊ຣະ໋ຣັ່ຣັ້ຣັ໊ຣັ໋ຣາ່ຣາ້ຣາ໊ຣາ໋ຣຳ່ຣຳ້ຣຳ໊ຣຳ໋ຣິ່ຣິ້ຣິ໊ຣິ໋ຣີ່ຣີ້ຣີ໊ຣີ໋ຣຶ່ຣຶ້ຣຶ໊ຣຶ໋ຣື່ຣື້ຣື໊ຣື໋ຣຸ່ຣຸ້ຣຸ໊ຣຸ໋ຣູ່ຣູ້ຣູ໊ຣູ໋ລະ່ລະ້ລະ໊ລະ໋ລັ່ລັ້ລັ໊ລັ໋ລາ່ລາ້ລາ໊ລາ໋ລຳ່ລຳ້ລຳ໊ລຳ໋ລິ່ລິ້ລິ໊ລິ໋ລີ່ລີ້ລີ໊ລີ໋ລຶ່ລຶ້ລຶ໊ລຶ໋ລື່ລື້ລື໊ລື໋ລຸ່ລຸ້ລຸ໊ລຸ໋ລູ່ລູ້ລູ໊ລູ໋ວະ່ວະ້ວະ໊ວະ໋ວັ່ວັ້ວັ໊ວັ໋ວາ່ວາ້ວາ໊ວາ໋ວຳ່ວຳ້ວຳ໊ວຳ໋ວິ່ວິ້ວິ໊ວິ໋ວີ່ວີ້ວີ໊ວີ໋ວຶ່ວຶ້ວຶ໊ວຶ໋ວື່ວື້ວື໊ວື໋ວຸ່ວຸ້ວຸ໊ວຸ໋ວູ່ວູ້ວູ໊ວູ໋ສະ່ສະ້ສະ໊ສະ໋ສັ່ສັ້ສັ໊ສັ໋ສາ່ສາ້ສາ໊ສາ໋ສຳ່ສຳ້ສຳ໊ສຳ໋ສິ່ສິ້ສິ໊ສິ໋ສີ່ສີ້ສີ໊ສີ໋ສຶ່ສຶ້ສຶ໊ສຶ໋ສື່ສື້ສື໊ສື໋ສຸ່ສຸ້ສຸ໊ສຸ໋ສູ່ສູ້ສູ໊ສູ໋ຫະ່ຫະ້ຫະ໊ຫະ໋ຫັ່ຫັ້ຫັ໊ຫັ໋ຫາ່ຫາ້ຫາ໊ຫາ໋ຫຳ່ຫຳ້ຫຳ໊ຫຳ໋ຫິ່ຫິ້ຫິ໊ຫິ໋ຫີ່ຫີ້ຫີ໊ຫີ໋ຫຶ່ຫຶ້ຫຶ໊ຫຶ໋ຫື່ຫື້ຫື໊ຫື໋ຫຸ່ຫຸ້ຫຸ໊ຫຸ໋ຫູ່ຫູ້ຫູ໊ຫູ໋ອະ່ອະ້ອະ໊ອະ໋ອັ່ອັ້ອັ໊ອັ໋ອາ່ອາ້ອາ໊ອາ໋ອຳ່ອຳ້ອຳ໊ອຳ໋ອິ່ອິ້ອິ໊ອິ໋ອີ່ອີ້ອີ໊ອີ໋ອຶ່ອຶ້ອຶ໊ອຶ໋ອື່ອື້ອື໊ອື໋ອຸ່ອຸ້ອຸ໊ອຸ໋ອູ່ອູ້ອູ໊ອູ໋ຮະ່ຮະ້ຮະ໊ຮະ໋ຮັ່ຮັ້ຮັ໊ຮັ໋ຮາ່ຮາ້ຮາ໊ຮາ໋ຮຳ່ຮຳ້ຮຳ໊ຮຳ໋ຮິ່ຮິ້ຮິ໊ຮິ໋ຮີ່ຮີ້ຮີ໊ຮີ໋ຮຶ່ຮຶ້ຮຶ໊ຮຶ໋ຮື່ຮື້ຮື໊ຮື໋ຮຸ່ຮຸ້ຮຸ໊ຮຸ໋ຮູ່ຮູ້ຮູ໊ຮູ໋ຯະ່ຯະ້ຯະ໊ຯະ໋ຯັ່ຯັ້ຯັ໊ຯັ໋ຯາ່ຯາ້ຯາ໊ຯາ໋ຯຳ່ຯຳ້ຯຳ໊ຯຳ໋ຯິ່ຯິ້ຯິ໊ຯິ໋ຯີ່ຯີ້ຯີ໊ຯີ໋ຯຶ່ຯຶ້ຯຶ໊ຯຶ໋ຯື່ຯື້ຯື໊ຯື໋ຯຸ່ຯຸ້ຯຸ໊ຯຸ໋ຯູ່ຯູ້ຯູ໊ຯູ໋ເແໂໃໄ"
    #text = "ກຂຄງຈຊຍຏຑຒດຕຖທນ"
    clean_text = preprocess_text(text)
    render_text_with_harfbuzz_freetype(clean_text, font_path)
