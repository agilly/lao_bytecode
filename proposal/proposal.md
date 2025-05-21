# Problem description
### Aims
* The aim is to display Lao messages on an OLED or E-Ink screen 
### Current problems:
* Lao uses a combination of tone marks and vowel signs that are placed above or below a base character. 
* One computers, this complexity is handled by font shaping engines like HarfBuzz and FreeType.
* However, microcontrollers lack the memory and processing power to run these font shaping engines.
### Current solution and its challenges
* Bitmap fonts store the characters as pixel arrays and are easy to load and render making them ideal for embedded system applications.
* Unlike vector fonts, bitmapped fonts cannot respond to surrounding characters and there is no dynamic positioning of combining marks. 
* No resolution scaling is available without distortion of the font. Therefore to suppoer mutiple font sizes many versions of the bitmap must be created.


# Presentation of the proposal
We propose three possible solutions:
### Continuing MakerBox's current solution
* The current solution involves pre-rendering the most common Lao syllables (combinations of base letters and marks) into individual bitmap glyphs.
* While this eliminates the need for shaping or mark positioning, this doens't scale well as supporting every valid Lao combination would require hundreds of glyphs.
* A specific keyboard would need to be designed for this solution (which would pose a problem in fitting all the combinations onto the keyboard space.)
### Rule-Based Rendering 
* A second solution would be to develop a rule based program which uses a simple set of ruled to decide where to place tone marks. Eg. If the incoming text includes a base consonant followed by a vowel, the program would detect this and then place the vowel a fixed offset above or below the consonant.
* This solution would be compatible with a standard Lao keyboard and Unicode.
* However, there may be problems with the overlapping characters due to inadequate offsets and multiple stacked marks could be a problem.
### Pre-processing of the 

# Assessment of the quality of the proposal

Evaluate its value in the context of the project. What will it solve, is it safe, etc. Check Lara’s slides for what to cover.


