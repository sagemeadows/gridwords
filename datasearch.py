#! /usr/bin/python
#
# search.py
#
# Usage:
#     module for gridwords.py
#
# Get possible words for partial words and get clues for decided words.
#

import re
from move import select

WHITE = '#ffffff'
BLACK = '#000000'
GRAY = '#d9d9d9'
BLUE = '#0000ff'
CYAN = '#00ffff'
GREEN = '#00ff00'
RED = '#ff0000'
ORANGE = '#ffa500'
YELLOW = '#ffff00'

# Establish words database
# TODO: Replace this with real clue database
words_filename = "/etc/dictionaries-common/words"

def getPossWords(cellgrid):
    # reset poss words
    cellgrid.wword.poss_words.clear()
    
    # search database
    match_word = cellgrid.wword.word.replace('.', '[A-Z]')
    match_pattern = re.compile(match_word)
    
    # open words file
    file_handle = open(words_filename, 'r')
    while True:
        line = file_handle.readline().upper().replace("'", "")
        if not line:
            # at end of file
            break
        mp = match_pattern.findall(line)
        if mp:
            if mp[0] not in cellgrid.wword.poss_words:
                cellgrid.wword.poss_words.append(mp[0])
        
    file_handle.close()
    
    # color working word according to 
    # number of possible words
    color_hex = GREEN
    if not cellgrid.wword.poss_words:
        color_hex = RED
    elif 1 < len(cellgrid.wword.poss_words) <= 10:
        color_hex = ORANGE
    elif 1 < len(cellgrid.wword.poss_words) <= 50:
        color_hex = YELLOW
    
    for coord in cellgrid.wword.coords:
        cellgrid.cells[coord[0]][coord[1]].setColor(color_hex)
    
    ## create frame for poss words
    #if cellgrid.wword.poss_words:
    #    createPossWords(cellgrid.wword.poss_words)
    
    print(f"DEBUG\tPossible words for '{cellgrid.wword.word}':\n\t{cellgrid.wword.poss_words}\n")
    if len(cellgrid.wword.poss_words) > 50:
        print(f"\tTotal possible words: {len(cellgrid.wword.poss_words)}\n")

