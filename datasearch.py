#! /usr/bin/python
#
# search.py
#
# Usage:
#     module for gridwords.py
#
# Get possible words for partial words and get clues for decided words.
#

import time
import os
import logging
import re
from move import select

LOGGER_FORMAT = "%(filename)s:%(lineno)s %(funcName)s: %(message)s"
#LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG 
logging.basicConfig( format=LOGGER_FORMAT, level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)

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
cwd = os.getcwd()
words_filename = f"{cwd}/database.csv"

def getPossWords(cellgrid):
    # reset poss words
    cellgrid.wword.poss_words.clear()

    # get search pattern
    match_length = len(cellgrid.wword.word)
    match_word = '^' + cellgrid.wword.word.replace('.', '[A-Z]') + '$'
    match_pattern = re.compile(match_word)

    # open words file
    file_handle = open(words_filename, 'r')
    next(file_handle)
    start = time.time()
    while True:
        line = file_handle.readline()
        if not line:
            # at end of file
            break

        line = line.replace('\n', '')
        line = line.split(',', 2)
        #logger.debug(print(line))
        word = line[1]
        word_length = len(word)
        clue = line[2]#[:-1]

        if match_length == word_length:
            mp = match_pattern.findall(word)
            if mp:
                if mp[0] not in cellgrid.wword.poss_words:
                    cellgrid.wword.poss_words.append(mp[0])

    file_handle.close()
    end = time.time()
    logger.debug(f"Time to find poss words: {end - start} secs")

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

    logger.debug(f"Possible words for '{cellgrid.wword.word}':\n\t{cellgrid.wword.poss_words}\n")
    if len(cellgrid.wword.poss_words) > 50:
        logger.info(f"\tTotal possible words: {len(cellgrid.wword.poss_words)}\n")

def allPossWords(cellgrid):
    cellgrid.wword = None
    match_patterns = {}

    # reset poss words
    # and get search patterns
    for key,entry in cellgrid.words.items():
        entry.poss_words.clear()
        match_word = '^' + entry.word.replace('.', '[A-Z]') + '$'
        match_pattern = re.compile(match_word)
        match_patterns[f'{entry.index} {entry.direc}'] = match_pattern

    # open words file
    file_handle = open(words_filename, 'r')
    next(file_handle)
    start = time.time()
    while True:
        line = file_handle.readline()
        if not line:
            # at end of file
            break

        line = line.replace('\n', '')
        line = line.split(',', 2)
        #logger.debug(print(line))
        word_length = line[0]
        word = line[1]
        clue = line[2]#[:-1]

        for entry,match_pattern in match_patterns.items():
            mp = match_pattern.findall(word)
            if mp:
                if mp[0] not in cellgrid.words[entry].poss_words:
                    cellgrid.words[entry].poss_words.append(mp[0])

    file_handle.close()
    end = time.time()
    logger.debug(f"Time to find all poss words: {end - start} secs")

    # color cells according to number of poss words
    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            if cellgrid.cells[row][column].getColor() != BLACK:
                acr_num = cellgrid.cells[row][column].across_num
                acr_poss_words = 0
                if acr_num > 0:
                    acr_poss_words = len(cellgrid.words[f'{acr_num} across'].poss_words)
                else:
                    acr_poss_words = -1

                dwn_num = cellgrid.cells[row][column].down_num
                dwn_poss_words = 0
                if dwn_num > 0:
                    dwn_poss_words = len(cellgrid.words[f'{dwn_num} down'].poss_words)
                else:
                    dwn_poss_words = -1

                color_hex = GREEN
                if acr_poss_words == 0 or dwn_poss_words == 0:
                    color_hex = RED
                elif 1 < acr_poss_words <= 10 or 1 < dwn_poss_words <= 10:
                    color_hex = ORANGE
                elif 1 < acr_poss_words <= 50 or 1 < dwn_poss_words <= 50:
                    color_hex = YELLOW

                cellgrid.cells[row][column].setColor(color_hex)

