# -*- coding: utf-8 -*-
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build a full path to the file in that directory
file_path = os.path.join(script_dir, "lao_full_set.txt")


"""
In this program "standalone characters" are considered any characters that do not appear above or below any other character.
This includes all consonants, special symbols, digits and some leading and post-vowels.
Combining marks include some diacritics as well as vowels that are placed above and below.

Output: a file that includes all character combinations as per the above definitions of character classes.
"""

# Lao consonants
consonants = [
    'ກ', 'ຂ', 'ຄ', 'ງ', 'ຈ', 'ຊ', 'ຍ', 'ດ', 'ຕ',
    'ຖ', 'ທ', 'ນ', 'ບ', 'ປ', 'ຜ', 'ຝ', 'ພ', 'ຟ',
    'ມ', 'ຢ', 'ຣ', 'ລ', 'ວ', 'ສ', 'ຫ', 'ອ', 'ຮ'
]


# Marks that combine above or below consonants
combining_marks = ['ິ', 'ີ', 'ຶ', 'ື', 'ຸ', 'ູ', 'ັ', 'ົ', 'ຼ']

# Optional tone marks
tone_marks = ['່', '້', '໊', '໋']

# Leading vowels (standalone)
leading_vowels = ['ເ', 'ແ', 'ໂ', 'ໃ', 'ໄ']

# Post-consonant vowels (standalone)
post_vowels = ['ະ', 'າ', 'ຳ', 'ຽ']

# Special symbols to include (punctuation and consonant clusters)
special_symbols = ['ໆ', 'ໜ', 'ໝ']

# Lao digits
digits = ['໐', '໑', '໒', '໓', '໔', '໕', '໖', '໗', '໘', '໙']

# Combine all standalone characters (vowels not placed above or below are considered standalone)
standalone_chars = consonants + leading_vowels + post_vowels + special_symbols + digits

MAX_LINES = 50000
count = 0

with open(file_path, "w", encoding="utf-8") as f:
    # 1. Standalone consonants and other standalones
    for char in standalone_chars:
        f.write(char + '\n')
        count += 1
        if count >= MAX_LINES: break

    # 2. Consonant + (vowel above/below) + (optional tone)
    for c in consonants:
        for v in [''] + combining_marks:
            for t in [''] + tone_marks:
                if v == '' and t == '':
                    continue  # already written as standalone consonant
                combo = c + v + t
                f.write(combo + '\n')
                count += 1
                if count >= MAX_LINES: break
            if count >= MAX_LINES: break
        if count >= MAX_LINES: break
    f.write(f"Wrote {count} entries to lao_full_set.txt")
print(f"Wrote {count} entries to lao_full_set.txt")
