"""This script should:

1.  collect a number of input strings from the user 
    i.e get input_list = ['héllo', 'world']

    or

    read a CSV file line-by-line, treating each line as a sentence input.

then contain a function to

2.  store a list 'char_list' of all unique characters across all strings, 
    but collecting any composite characters made of multiple codepoints together 
    (e.g. Lao characters that are made of a base consonant + up/down vowel + tone mark)
    i.e. input ['héllo', 'world'] -> output char_list = [['h'], ['e', '´'], ['l'], ['o'], ['w'], ['r'], ['d']]

3.  create a second array 'index_list', containing a list of indexes for each input string,
    indexing each character in the char_list
    i.e. input ['héllo', 'world'] -> output index_list = [[0, 1, 2, 2, 3], [4, 3, 5, 2, 6]]

reurn char_list and index_list

4.  print the char_list and index_list
"""

import csv
import grapheme

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



import unicodedata

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
            char_list (list[list[str]]): List of grapheme clusters, where each cluster is a list of characters.
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
    char_list = [[c for c in cluster] for cluster in all_clusters]

    return char_list, index_list



# Main execution
#input_list = get_input_strings()
#save_strings_to_csv(input_list, './input_strings.csv')  # Save input to CSV for later use

input_list = get_input_strings_from_csv('input_strings.csv')  # Replace with your CSV file path

char_list, index_list = build_char_and_index_lists(input_list)

# Print the results
print("Character List:")
print('[' + ' '.join([''.join(cluster) for cluster in char_list]) + ']')
print("\nIndex List:")
for i, indices in enumerate(index_list):
    print(f"String {i}: {indices}")

    