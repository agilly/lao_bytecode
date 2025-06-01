#ifndef PHRASES_TO_DISPLAY_H
#define PHRASES_TO_DISPLAY_H

const uint8_t all_phrases[] = {
  0, 1, 2, 3, 4, 5, 6, 7, 8,    // phrase 1
  0, 6, 6, 8,                   //phrase 2
  4, 4                         //phrase 3
};

const uint8_t phrase_starts[] = {0, 9, 13};     // starting index of each phrase
const uint8_t phrase_lengths[] = {9, 4, 2};    // length of each phrase
const uint8_t num_phrases = 3;

#endif