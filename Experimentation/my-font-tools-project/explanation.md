I have imported the Phetsarath_regular.ttf
used fonttools to convert to ttx: 
ttx -t GSUB -t GPOS MyFont.ttf

ttx -o ./output_files -t GSUB -t GPOS -t cmap -t glyf -g Phetsarath-Regular.ttf

1. cmap (Character to Glyph Mapping)
Maps Unicode codepoints (e.g., Lao letters, vowels, tone marks) to glyph IDs in the font.
Use: When your Arduino receives Unicode input, use the cmap table to translate each character into the correct glyph index or name.
This lets you identify which bitmaps to draw.
2. GSUB (Glyph Substitution Table)
Contains substitution rules like ligatures, contextual forms, or reordering of glyphs.
Example: It might say “when this consonant is followed by this vowel, substitute with a special combined glyph.”
Use: To implement rules where multiple codepoints become a single composite glyph or need reordering.
You can parse these rules from the .ttx to understand when to swap glyphs or reorder marks.
3. GPOS (Glyph Positioning Table)
Contains positioning adjustments — where to place combining marks relative to base glyphs.
Example: offsetting a tone mark above a consonant.
Use: To get the exact (x, y) offsets to draw your mark bitmaps relative to the base bitmap.
4. glyf (Glyph Data Table)
Contains the vector outlines of each glyph.
Since you want bitmaps, you would rasterize these outlines to bitmaps at your target resolution.
Tools like FontForge, or Python libraries (e.g., fonttools + rasterizer), can help export bitmaps for each glyph from glyf.

EBDT -> Embedded Bitmap Data Table 

pip install freetype-py