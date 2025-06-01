#ifndef PHRASES_TO_DISPLAY_H
#define PHRASES_TO_DISPLAY_H

const uint8_t all_phrases[] = {
    0, 1, 2, 3, 4, 5,    // phrase 1
    6, 7, 3, 8, 9, 3, 10, 11, 12,    // phrase 2
};

const uint8_t phrase_starts[] = {0, 6};     // starting index of each phrase
const uint8_t phrase_lengths[] = {6, 9};    // length of each phrase
const uint8_t num_phrases = 2;

#endif
