import compact_lao_messages_app.generate_bitmaps as bitmap_gen
import compact_lao_messages_app.preprocess_strings as process_str
from compact_lao_messages_app.debug import display_bitmap, print_char_and_index_lists
import os

def main():


    input_csv_path = './input_files/input_strings.csv'

    if os.path.exists(input_csv_path):
        response = input("An existing input_strings.csv was found. Overwrite it? (y/N): ").strip().lower()
        if response == 'y':
            print("Overwriting input strings...")
            input_list = process_str.get_input_strings()
            process_str.save_strings_to_csv(input_list, input_csv_path)
        else:
            print("Loading input strings from existing CSV...")
            input_list = process_str.get_input_strings_from_csv(input_csv_path)
    else:
        print("No input_strings.csv found, generating input strings...")
        input_list = process_str.get_input_strings()
        process_str.save_strings_to_csv(input_list, input_csv_path)
    
    print("Identifying unique characters...")
    char_list, index_list = process_str.build_char_and_index_lists(input_list)

    print_char_and_index_lists(char_list, index_list)

    print("Generating bitmaps for characters...")
    while True:
        try:
            GLYPH_HEIGHT = int(input("Enter chosen glyph height in pixels... (30 recommended) "))
            break
        except ValueError:
            print("Please enter a valid integer.")

    GLYPH_WIDTH = GLYPH_HEIGHT

    bytes_list = bitmap_gen.generate_bitmaps_for_chars(char_list, GLYPH_WIDTH, GLYPH_HEIGHT, output_header="./arduino_code/glyph_bitmaps.h")

    print("Writing index list to header file...")
    process_str.write_index_list_to_header(index_list, filename="./arduino_code/phrases_to_display.h")

    user_input = input("Would you like to display the whole bitmap for debugging? (y/N): ").strip().lower()
    if user_input in ["y", "yes"]:
        print("Displaying the whole bitmap...")
        display_bitmap(bytes_list, GLYPH_HEIGHT, GLYPH_WIDTH)  # Adjust width as needed



    