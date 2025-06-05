"""
Utilities for processing Unicode strings into grapheme clusters,
generating index mappings, and exporting them for embedded C++ use.
"""

import csv
import grapheme
import os

def decompose_string_to_clusters(s):
    """
    Splits a string into Unicode grapheme clusters (what a human sees as one character),
    using the ICU-standard grapheme segmentation.

    Args:
        s (str): Input string.

    Returns:
        list[str]: List of grapheme clusters.
    """
    return list(grapheme.graphemes(s))

def get_input_strings_from_csv(file_path):
    """
    Reads a CSV file and extracts one sentence per line.
    
    Each line in the CSV is treated as a separate input string (sentence).
    If a line contains multiple comma-separated values (e.g., multiple columns),
    they are joined into a single string using spaces.

    Args:
        file_path (str): Path to the .csv file.

    Returns:
        List[str]: A list of strings, one per line from the CSV.
    """
    input_list = []

    # Open the file with UTF-8 encoding to support Unicode characters (e.g., Lao script)
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)  # Use the built-in CSV reader

        for row in reader:
            if row:
                # Combine all values in the row into one string
                # This is useful if a row has multiple columns
                sentence = ' '.join(row).strip()
                input_list.append(sentence)

    return input_list

def get_input_strings():
    """
    Collects strings from user input interactively.

    Prompts the user to enter strings one by one via the terminal.
    Input ends when the user submits an empty line.

    Returns:
        list[str]: A list of all entered strings.
    """
    print("Enter strings one by one. Press Enter on an empty line to finish.")
    input_list = []
    while True:
        s = input("Enter string: ")
        if s == "":
            break  # Stop input when an empty line is entered
        input_list.append(s)
    return input_list

def save_strings_to_csv(input_list, file_path):
    """
    Saves a list of strings to a CSV file, one string per row.

    Args:
        input_list (list[str]): List of strings to save.
        file_path (str): Path to the output CSV file.
    """
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for string in input_list:
            writer.writerow([string])  # Write each string as a single-column row


def build_char_and_index_lists(input_list):
    """
    Builds a list of unique grapheme clusters and indexes input strings based on them.

    For each input string:
      - Splits the string into grapheme clusters.
      - Adds any new cluster to a master list.
      - Maps each cluster in the string to its index in the master list.

    Returns:
        tuple:
            char_list (list[str]): List of grapheme clustered characters.
            index_list (list[list[int]]): List of index lists, each mapping a string to cluster indices.
    """
    all_clusters = []          # List of unique grapheme clusters
    index_list = []            # List of index lists for each input string
    cluster_to_index = {}      # Mapping from cluster to its unique index

    for s in input_list:
        clusters = decompose_string_to_clusters(s)

        indices = []           # Indices for current string

        for cluster in clusters:
            if cluster not in cluster_to_index:
                # New cluster: assign a new index and add to master list
                cluster_to_index[cluster] = len(all_clusters)
                all_clusters.append(cluster)
            # Append index of this cluster to string's index list
            indices.append(cluster_to_index[cluster])

        index_list.append(indices)

    # Convert each cluster string (e.g. 'é') into a list of its characters ['e', '́']
    # char_list = [[c for c in cluster] for cluster in all_clusters]
    char_list = [cluster for cluster in all_clusters]  # Keep each cluster as a single string

    return char_list, index_list

def write_index_list_to_header(index_list, filename="./arduino_code/phrases_to_display.h"):
    """
    Writes the index list to a C++ header file.

    Args:
        index_list (list[list[int]]): List of index lists for each input string.
        filename (str): Output header file name (default: "phrases_to_display.h")
    """

    # Flatten the list of indices
    all_indices = [idx for phrase in index_list for idx in phrase]

    # Compute start indices and lengths
    starts = []
    lengths = []
    current_start = 0
    for phrase in index_list:
        starts.append(current_start)
        lengths.append(len(phrase))
        current_start += len(phrase)

    num_phrases = len(index_list)

    with open(filename, "w") as f:
        f.write("#ifndef PHRASES_TO_DISPLAY_H\n")
        f.write("#define PHRASES_TO_DISPLAY_H\n\n")

        # Write all_phrases
        f.write("const uint8_t all_phrases[] = {\n")
        for phrase in index_list:
            f.write("    ")
            f.write(", ".join(str(i) for i in phrase))
            f.write(",    // phrase {}\n".format(index_list.index(phrase) + 1))
        f.write("};\n\n")

        # Write phrase_starts
        f.write("const uint8_t phrase_starts[] = {")
        f.write(", ".join(str(s) for s in starts))
        f.write("};     // starting index of each phrase\n")

        # Write phrase_lengths
        f.write("const uint8_t phrase_lengths[] = {")
        f.write(", ".join(str(l) for l in lengths))
        f.write("};    // length of each phrase\n")

        # Write num_phrases
        f.write(f"const uint8_t num_phrases = {num_phrases};\n\n")

        f.write("#endif\n")

    header_size_kb = os.path.getsize(filename) / 1024
    print(f"Index header file size: {header_size_kb:.2f} KB")


    