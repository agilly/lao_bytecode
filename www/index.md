---
title: Home
---
# **Developing a Lao Bytecode**
#### **Our collaborator MakerBox** 
Makerbox Lao is a collaborative space that fosters the development of technology-driven solutions to various local challenges in Laos. Given that agriculture is a cornerstone of the Laotian economy that employs around 70% of the population (ASEAN Briefing, 2025), MakerBox is currently building a system to send actionable messages — such as irrigation alerts and weather warnings — to farmers via digital displays in rural areas. In a country where adverse weather can devastate crops, timely information and technology offer strong potential to improve farming efficiency.


<div>
  <img src="assets/MakerBox logo.png" alt="MakerBox Lao Logo" width="200"/>
  <img src="assets/farming in Laos.png" alt="Farming in Laos" width="800"/>
</div>
Image left: MakerBox, n.d. | Image right: FAO, United Nations, n.d.


#### **The Problem**
The Lao language uses a combination of tone marks and vowel signs placed above or below a base character. On computers, this complexity is handled via vector fonts and shaping engines. However, for the agricultural monitoring and messaging system to be implemented at low cost and at scale, it must be done with microcontrollers with low processing power, connected to "dumb screens" with no complex graphical rendering ability. 

Thus we were tasked with developing byte code font for the Lao language compatible with microcontrollers and OLED/E-Ink screens. 

#### **Our solution**
Our solution involves pre-processing input phrases, generation of bitmaps of the unique characters and rendering logic for an OLED screen. Read more about the technical details of the solution [here](about.md).




