

import char_list_bitmap_generator_canonical_form as bitmap_gen
import process_input_strings as process_str
from test_functions import display_bitmap 

# see if an input_strings file exists, if not, generate it
try:

    input_list = process_str.get_input_strings_from_csv('input_strings.csv')  # Replace with your CSV file path
    print("Input strings loaded from CSV.")

except FileNotFoundError:

    print("No input_strings.csv found, generating input strings...")
    input_list = process_str.get_input_strings()
    process_str.save_strings_to_csv(input_list, './input_strings.csv')  # Save input to CSV for later use

print("Identifying unique characters...")
char_list, index_list = process_str.build_char_and_index_lists(input_list)

print("Generating bitmaps for characters...")
bytes_list = bitmap_gen.generate_bitmaps_for_chars(char_list, font_path='./NotoSansLao-Regular.ttf', output_header="./glyph_bitmaps_bespoke.h")

print("Writing index list to header file...")
process_str.write_index_list_to_header(index_list)

print("displaying the whole bitmap...")
display_bitmap(bytes_list, 4)
