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
import tkinter as tk
from move import select
#from indices import spreadIndices

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

class PossWordBtn(tk.Button):
    # define the ctor method
    def __init__(self, master=None, text=None, entry=None):
        # initialize the base class
        tk.Button.__init__(self, master=master, relief=tk.GROOVE, bd=2, text=text,\
                           command=self.onPossWordClick)
        self.master_window = self.master.master.master.master
        self.entry = entry
        self.cellgrid = self.entry.cellgrid
        self.word = text
        self['font'] = self.entry.main_frame.wip_words.font
        self.pack(expand=True, fill="both")

    def onPossWordClick(self):
        logger.debug(f"Selected word: {self.word}")
        #self.entry.letters.clear()

        for i in range(len(self.word)):
            # set each letter to its coord in order
            coord = self.entry.coords[i]
            self.cellgrid.cells[coord[0]][coord[1]].letter.set(self.word[i])
            ## add letter to entry list of letters
            #self.entry.letters.append(self.word[i])

        # update all entries for cases of intersecting words
        for key,entry in self.cellgrid.words.items():
            # clear letters
            entry.letters.clear()
            for coord in entry.coords:
                cell = self.cellgrid.cells[coord[0]][coord[1]]
                entry.letters.append(cell.letter.get())
            entry.updateWord()
            logger.debug(f"{key}:{repr(entry.letters)}, {entry.word}")
        logger.debug("")
        
        # close pop-up window
        self.master_window.destroy()

class PossClueBtn(tk.Button):
    # define the ctor method
    def __init__(self, master=None, text=None, entry=None, row=None):
        # initialize the base class
        tk.Button.__init__(self, master=master, relief=tk.GROOVE, bd=2, text=text,\
                           command=self.onPossClueClick)
        self.master_window = self.master.master.master.master
        self.entry = entry
        self.cellgrid = self.entry.cellgrid
        self.clue = text
        #self['font'] = self.entry.main_frame.wip_words.font
        self.row = row
        self.grid(row=self.row, column=0, pady=2, sticky="w")

    def onPossClueClick(self):
        #logger.debug(f"Selected clue: {self.clue}")
        self.entry.clue.set(self.clue)
        logger.debug(f"{self.entry.index} {self.entry.direc}: {self.entry.word}, {self.entry.clue.get()}\n")
        
        # close pop-up window
        self.master_window.destroy()

class SearchWindow(tk.Tk):
    # define the ctor method
    def __init__(self, mode=None, entry=None, poss_clues=None, database=words_filename):
        # initialize the base class
        tk.Tk.__init__(self)
        self.configure(bg=WHITE)

        # add frame and canvas for future scrollable frame
        self.root_frame = tk.Frame(self, bg=WHITE, bd=2)
        self.root_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.root_frame, bg=WHITE)
        
        # create scrollbars
        self.scrollbar_y = tk.Scrollbar(self.root_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        # create main scrollable frame to hold all other frames
        self.scrollable_frame = tk.Frame(self.canvas, bg=WHITE, bd=2)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")

        # fill window with poss words or poss clues
        self.mode = mode
        self.entry = entry
        if self.mode == 'fill':
            self.title(f"{len(entry.poss_words)} possible words for {self.entry.index} {self.entry.direc}")
            if len(self.entry.poss_words) > 1:
                for i in range(len(self.entry.poss_words)):
                    pwb = PossWordBtn(self.scrollable_frame, text=self.entry.poss_words[i], entry=self.entry)
            else:
                self.destroy()

        elif self.mode == 'clue':
            self.title(f"Possible Clues for {self.entry.index} {self.entry.direc}")
            txt_clue = tk.Text(self.scrollable_frame, height=3, width=50, wrap="word")
            txt_clue.grid(row=0, column=0, sticky="new")
            btn_submit_clue = tk.Button(self.scrollable_frame, relief=tk.RAISED, bd=3, text="Save & Use Clue", \
                                        command=lambda : self.addNewClue(clue=txt_clue.get("1.0", tk.END)))
            btn_submit_clue.grid(row=1, column=0, pady=10, sticky="n")
            counter = 2
            for c in poss_clues:
                pcb = PossClueBtn(self.scrollable_frame, text=c, entry=self.entry, row=counter)
                counter += 1
            logger.debug(f"Created possible clues search window for {self.entry.index} {self.entry.direc}")

        # establish database for use in methods
        self.database = database

        # quick quit
        self.bind("<Escape>", lambda e: self.quit(e))


    def addNewClue(self, clue=None):
        """Save new clue to database."""
        with open(words_filename, 'a', encoding="utf-8") as f:
            line = str(len(self.entry.word)) + ',' + self.entry.word + ',' + clue
            f.write(line)

        # use clue in puzzle
        self.entry.clue.set(clue)
        logger.debug(f"{self.entry.index} {self.entry.direc}: {self.entry.word}, {self.entry.clue.get()}\n")
        
        # close pop-up window
        self.destroy()


    def quit(self, event):
        self.destroy()


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
    mk_search_window = False
    if not cellgrid.wword.poss_words:
        color_hex = RED
    elif len(cellgrid.wword.poss_words) > 1:
        mk_search_window = True
        if 1 < len(cellgrid.wword.poss_words) <= 10:
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

    # open window for possible words
    if mk_search_window == True:
        search_window = SearchWindow(mode='fill', entry=cellgrid.wword)
        search_window.mainloop()


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


def getPossClues(entry):
    if '.' not in entry.word:
        # get search pattern
        match_length = len(entry.word)
        match_word = '^' + entry.word + '$'
        match_pattern = re.compile(match_word)
        poss_clues = []

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
                    poss_clues.append(clue)

        file_handle.close()
        end = time.time()
        logger.debug(f"Time to find all poss clues: {end - start} secs")
        
        # open search window with possible clues
        search_window = SearchWindow(mode='clue', entry=entry, poss_clues=poss_clues)
        search_window.mainloop()

    else:
        logger.debug(f"Undetermined word for {entry.index} {entry.direc}; cannot find clues for undertimined words")


