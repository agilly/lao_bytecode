bases = "ກຂຄງຈຊຍຏຑຒດຕຖທນບປຜຝພຟມຢຣລວສຫອຮຯ"
vowels_above_below = "ະັາຳິີຶືຸູ"
vowels_side = "ເແໂໃໄ"
tones = "່້໊໋"

# Start with base consonants alone
composites = list(bases)

# Add base + above/below vowel
for base in bases:
    for v in vowels_above_below:
        composites.append(base + v)

# Add base + tone
for base in bases:
    for t in tones:
        composites.append(base + t)

# Add base + above/below vowel + tone
for base in bases:
    for v in vowels_above_below:
        for t in tones:
            composites.append(base + v + t)

# Add the side vowels as standalone (not combined)
composites.extend(vowels_side)

# Join all into one string
all_composites_str = "".join(composites)
print(all_composites_str)
