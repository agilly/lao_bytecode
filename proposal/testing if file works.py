import uharfbuzz as hb
import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

# Font file and text
font_path = r"C:\Users\Oisín Conlon\Documents\GM2\2025-MakerBox-Bytecode\Initial Files\NotoSansLao-Regular.ttf"
text = "ວັ"

# Output image size
width, height = 200, 100
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Create Pango layout
pangocairo_ctx = PangoCairo.create_context(ctx)
layout = Pango.Layout.new(pangocairo_ctx)

# Set font description with custom font
font_desc = Pango.FontDescription("Noto Sans Lao 72")  # Big size
layout.set_font_description(font_desc)

# Set the text to render
layout.set_text(text, -1)

# Move the drawing position
ctx.move_to(10, 10)

# Render the text
PangoCairo.show_layout(ctx, layout)

# Save to file
output_file = "output_cairo.png"
surface.write_to_png(output_file)
print(f"Rendered text saved as {output_file}")