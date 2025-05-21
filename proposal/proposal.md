# Problem description
### Aims
* The aim is to display Lao messages on an OLED or E-Ink screen 
### Current problems:
* Lao uses a combination of tone marks and vowel signs that are placed above or below a base character. 
* One computers, this complexity is handled by font shaping engines like HarfBuzz and FreeType.
* However, microcontrollers lack the memory and processing power to run these font shaping engines.
### Current solution and its challenges
* Bitmap fonts store the characters as pixel arrays and are easy to load and render making them ideal for embedded system applications.
* Unlike vector fonts, bitmapped fonts cannot respond to surrounding characters and there is no dynamic positioning of combining marks
* No resolution scaling is available without distortion of the font. Therefor to suppoer mutiple font sizes many versions of the bitmap must be created.


# Presentation of the proposal

Technical aspects may be described here.

# Assessment of the quality of the proposal

Evaluate its value in the context of the project. What will it solve, is it safe, etc. Check Lara’s slides for what to cover.


