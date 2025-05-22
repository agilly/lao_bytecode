# Problem description
### Aims
* The aim is to display Lao messages on an OLED or E-Ink screen 
### Current problems:
* Lao uses a combination of tone marks and vowel signs that are placed above or below a base character. 
* On computers, this complexity is handled by font shaping engines like HarfBuzz and FreeType.
* However, microcontrollers lack the memory and processing power to run these font shaping engines.
### Current solution and its challenges
* Bitmap fonts store the characters as pixel arrays and are easy to load and render making them ideal for embedded system applications.
* Unlike vector fonts, bitmapped fonts cannot respond to surrounding characters and there is no dynamic positioning of combining marks. 
* No resolution scaling is available without distortion of the font. Therefore to support mutiple font sizes many versions of the bitmap must be created.


# Presentation of the proposal
We propose three possible solutions:
### Continuing MakerBox's current solution
* The current solution involves pre-rendering the most common Lao syllables (combinations of base letters and marks) into individual bitmap glyphs.
* While this eliminates the need for shaping or mark positioning, this doesn't scale well as supporting every valid Lao combination would require hundreds of glyphs.
* A specific keyboard would need to be designed for this solution (which would pose a problem in fitting all the combinations onto the keyboard space.)
### Rule-Based Rendering 
* A second solution would be to develop a rule based program which uses a simple set of rules to decide where to place tone marks. Eg. If the incoming text includes a base consonant followed by a vowel, the program would detect this and then place the vowel a fixed offset above or below the consonant.
* This solution would be compatible with a standard Lao keyboard and Unicode.
* It would not require as many bitmapped glyphs - the individual characters would suffice
* However, there may be problems with the overlapping characters due to inadequate offsets and multiple stacked marks could be a problem.
### Pre-processing of the text
* The text could be shaped and preprocessed by the computer sending the message (which has higher compute power). This could then be converted into a set of specific drawing instructions to be sent to the microcontroller. (Eg. Exact offsets after considering each character's height.)

# Assessment of the quality of the proposal
* Laos has a population of 7.5 million with a primarily argicultural economy (60-70% of people working in farming).
* Considering the usecase and the rural infrastructure challenges (low internet penetration, unreliable energy sources ect.) the MakerBox solution of using bitmapped font on microcontrollers is energy efficient, affordable and impact focused.
* Since there is limited access to tech tools in the local script we are responding to a genuine need. 
* Our solution is collaboratively created with a team in Laos and we are expanding on the work of Kabuild (Bill) who is a key member of the MakerBox team. Discussions with the team is vital as not only are they experts on the technology, they can also provide us with local context and a perspective that we, as non-natives, may lack.
* We may have to consider the availability of chosen display screens and microcontrollers in the Laos market and the additional costs of imports and taxes (perhaps making it compatible with many screen types could be a solution).
* Since the majority of our solution will be a software file, it sidesteps the typical challenges of physical systems though successful integration with existing softwares and ecosystems is vital.


