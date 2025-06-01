from PIL import Image, ImageDraw, ImageFont

# Create blank image (monochrome)
img = Image.new('1', (128, 64), color=0)  # mode '1' = 1-bit


ImageFont.truetype("./Phetsarath-Regular.ttf", size=14)

draw = ImageDraw.Draw(img)
draw.text((10, 20), "Hello", font=font, fill=255)  # fill=255 = white text

# Save or show
img.show()
img.save("output.png")
