
1. send the whole bitmap to the arduino, use the computer to pregenerate - with pillow etc.

2. for our rules based system:

we need, a current x, current y

we need to map unicode codepoints onto a bitmap, x_offset & y_offset

we could categorise all the characters into:

Hybrid: Indexed Table + Bitmap Blob that we offset into to get our bitmap.
This is how .bdf fonts work

potential to use 
https://www.tinkercad.com/things/1wJ95uVnOK3/editel