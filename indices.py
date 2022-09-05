#! /usr/bin/python
#
# indices.py
#
# Usage:
#     module for gridwords.py
#
# Figure out clue indices and update grid.
#

import logging
import tkinter as tk
from move import select
from datasearch import getPossWords, getPossClues

LOGGER_FORMAT = "%(filename)s:%(lineno)s %(funcName)s: %(message)s"
#LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG
logging.basicConfig( format=LOGGER_FORMAT, level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)

WHITE = '#ffffff'
BLACK = '#000000'


class Entry:
    def __init__(self, cellgrid, index, direction, row):
        self.cellgrid = cellgrid
        self.main_frame = self.cellgrid.master
        self.index = index
        self.direc = direction
        self.row = row

        self.length = 0
        self.coords = []
        self.letters = []
        self.word = ''
        self.clue = tk.StringVar()
        self.poss_words = []

        # put entry in cellgrid words dict
        self.cellgrid.words[f'{self.index} {self.direc}'] = self
        
        # create entry frame
        exec(f"self.frm = tk.Frame(self.main_frame.wip_words.wip_{self.direc}, relief=tk.FLAT, bd=2, bg=WHITE)")
        self.frm.grid(row=self.row, column=0, sticky="nw")

        # create index label
        self.lbl = tk.Label(self.frm, text=f'{self.index}. ', bd=2, bg=WHITE)
        self.lbl.grid(row=0, column=0)

        # create word button
        self.btn_text = tk.StringVar()
        self.btn = tk.Button(self.frm, bd=2, relief=tk.FLAT, textvariable=self.btn_text, command=self.onEntryButtonClick)
        self.btn_font = self.main_frame.wip_words.font
        self.btn['font'] = self.btn_font
        self.btn.grid(row=0, column=1, sticky="nw")

        # create clue label
        #self.clue_text = tk.StringVar()
        self.clue_lbl = tk.Label(self.frm, textvariable=self.clue, justify="left", bd=2, bg=WHITE)
        self.clue_lbl.grid(row=1, column=1, sticky="nw")


    def updateWord(self):
        self.word = ''
        self.word = self.word.join(self.letters)
        self.btn_text.set(self.word)
        #logger.debug(f"Updated {self.index} {self.direc}")

    def onEntryButtonClick(self):
        if self.cellgrid.mode != 'grid':
            self.cellgrid.wdirec = self.direc
            cell = self.cellgrid.cells[self.coords[0][0]][self.coords[0][1]]
            select(cell, self.cellgrid)
        if self.cellgrid.mode == 'fill':
            getPossWords(self.cellgrid)
        elif self.cellgrid.mode == 'clue':
            getPossClues(self)

def updateClueIndices(cellgrid):
    # (re)start counter to get entry indexes
    counter = 0

    # count number of across and down words
    # for use in gridding entries in wip words frame
    row_across = 0
    row_down = 0

    # clear any old cellgrid info
    cellgrid.words = {}
    cellgrid.wl = (-1, -1)

    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            cell = cellgrid.cells[row][column]

            # clear any old positions
            cell.across_pos = -1
            cell.down_pos = -1

            # if cell is colored from word-filling mode,
            # return it to white
            if cell.getColor() != WHITE \
            and cell.getColor() != BLACK:
                cell.setColor(WHITE)

            # if cell is white
            if cell.getColor() == WHITE:
                # clear any old directions indices to 0
                cell.across_num = 0
                cell.down_num = 0

                give_num = False
                word_across = False
                word_down = False

                # if cell is in the top row
                if row == 0:
                    # if square is in the top left corner
                    if column == 0:
                        # HORIZONTAL CHECK FROM EDGE: if the square to its right is white
                        if cellgrid.cells[row][column+1].getColor() == WHITE:
                            give_num = True
                            word_across = True
                        # VERTICAL CHECK FROM EDGE: if the square below is white
                        if cellgrid.cells[row+1][column].getColor() == WHITE:
                            give_num = True
                            word_down = True
                    # if square is in the top right corner
                    elif column == range(len(cellgrid.cells[0]))[-1]:
                        # VERTICAL CHECK FROM EDGE ONLY: if the square below is white
                        if cellgrid.cells[row+1][column].getColor() == WHITE:
                            give_num = True
                            word_down = True
                    else: # the square is in the top row but not leftmost or rightmost column
                        # REGULAR HORIZONTAL CHECK: if the square to the left is black
                        #                           and the one to the right is white
                        if cellgrid.cells[row][column-1].getColor() == BLACK \
                        and cellgrid.cells[row][column+1].getColor() == WHITE:
                            give_num = True
                            word_across = True
                        # VERTICAL CHECK FROM EDGE: if square below is white
                        if cellgrid.cells[row+1][column].getColor() == WHITE:
                            give_num = True
                            word_down = True

                # if cell is on bottom row
                elif row == range(len(cellgrid.cells))[-1]:
                    # if the square is in the bottom left corner
                    if column == 0:
                        # HORIZONTAL CHECK FROM EDGE ONLY: if the square to its right is white
                        if cellgrid.cells[row][column+1].getColor() == WHITE:
                            give_num = True
                            word_across = True
                    # if square is in the bottom right corner
                    elif column == range(len(cellgrid.cells[0]))[-1]:
                        # NO HORIZONTAL OR VERTICAL CHECK
                        # but since it's white, make sure it doesn't have a clue index
                        cell.setClueIndex('')
                    else: # the square is on the bottom row but not leftmost or rightmost column
                        # REGULAR HORIZONTAL CHECK ONLY: if the square to the left is black
                        #                                and the one to the right is white
                        if cellgrid.cells[row][column-1].getColor() == BLACK \
                        and cellgrid.cells[row][column+1].getColor() == WHITE:
                            give_num = True
                            word_across = True

                # if cell is in leftmost column
                # (but not in top or bottom row, bc we already covered that)
                elif column == 0:
                    # HORIZONTAL CHECK FROM EDGE: if the square to its right is white
                    if cellgrid.cells[row][column+1].getColor() == WHITE:
                        give_num = True
                        word_across = True
                    # REGULAR VERTICAL CHECK: if the square above is black
                    #                         and the one below is white
                    if cellgrid.cells[row-1][column].getColor() == BLACK \
                    and cellgrid.cells[row+1][column].getColor() == WHITE:
                        give_num = True
                        word_down = True

                # if cell is in rightmost column
                # (but not in top or bottom row, bc we already covered that)
                elif column == range(len(cellgrid.cells[0]))[-1]:
                    # REGULAR VERTICAL CHECK ONLY: if the square above is black
                    #                              and the one below is white
                    if cellgrid.cells[row-1][column].getColor() == BLACK \
                    and cellgrid.cells[row+1][column].getColor() == WHITE:
                        give_num = True
                        word_down = True

                else: # cell is not at any edge
                    # REGULAR HORIZONTAL CHECK: if the square to its left is black
                    #                           and the one to its right is white
                    if cellgrid.cells[row][column-1].getColor() == BLACK \
                    and cellgrid.cells[row][column+1].getColor() == WHITE:
                        give_num = True
                        word_across = True
                    # REGULAR VERTICAL CHECK: if the square above is black
                    #                         and the one below is white
                    if cellgrid.cells[row-1][column].getColor() == BLACK \
                    and cellgrid.cells[row+1][column].getColor() == WHITE:
                        give_num = True
                        word_down = True

                # if cell is the start of a word
                if give_num:
                    # give it a number
                    counter += 1
                    cell.setClueIndex(counter)

                else:
                    cell.setClueIndex('')

                # if cell is the start of a horizontal word
                if word_across:
                    cell.across_num = counter
                    row_across += 1

                    # create across entry and add to words dict
                    entry = Entry(cellgrid, counter, 'across', row_across)

                # if cell is the start of a vertical word
                if word_down:
                    cell.down_num = counter
                    row_down += 1

                    # create down entry and add to words dict
                    entry = Entry(cellgrid, counter, 'down', row_down)

            else: # cell is black
                cell.setClueIndex(-1)
                # clear any old direction indices to -1
                cell.across_num = -1
                cell.down_num = -1

                # clear any old letter to '#'
                cell.letter.set('#')


def spreadIndices(cellgrid):
    # Put numbers in 'across' and 'down' grid templates
    # and put letters in 'words'
    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            cell = cellgrid.cells[row][column]

            # check across array at coordinate.
            # if cell already has the number of an across word
            if cell.across_num > 0:
                # across number index shortcut
                a_index = f'{cell.across_num} across'

                # update length of across word
                cellgrid.words[a_index].length += 1

                # figure out cell's position in the across word
                # for ease of future word changes
                # by subtracting 1 from current recorded word length
                cell.across_pos = cellgrid.words[a_index].length - 1

                # add coords to entry
                cellgrid.words[a_index].coords.append((row, column))

                # add letter to list in entry (later to be joined into word)
                cellgrid.words[a_index].letters.append(cell.letter.get())

            # if the cell is white does not already have the number of an across word
            elif cell.across_num == 0:
                # if the cell has a neighbor to its left
                # that does have the number of an across word
                if column != 0 and cellgrid.cells[row][column-1].across_num > 0:
                    # make cell's across_num the same as its leftward neighbor
                    cell.across_num = cellgrid.cells[row][column-1].across_num
                    a_index = f'{cell.across_num} across'

                    # update length of across word
                    cellgrid.words[a_index].length += 1

                    # figure out cell's position in the across word
                    # for ease of future word changes
                    # by subtracting 1 from current recorded word length
                    cell.across_pos = cellgrid.words[a_index].length - 1

                    # add coords to entry
                    cellgrid.words[a_index].coords.append((row, column))

                    # add letter to list in entry (later to be joined into word)
                    cellgrid.words[a_index].letters.append(cell.letter.get())

            # check down array at coordinate.
            # if cell already has the number of a down word
            if cell.down_num > 0:
                # down number index shortcut
                d_index = f'{cell.down_num} down'

                # update length of across word
                cellgrid.words[d_index].length += 1

                # figure out cell's position in the down word
                # for ease of future word changes
                # by subtracting 1 from the current recorded word length
                cell.down_pos = cellgrid.words[d_index].length - 1

                # add coords to entry
                cellgrid.words[d_index].coords.append((row, column))

                # add letter to down word
                cellgrid.words[d_index].letters.append(cell.letter.get())

            # if the cell is white but does not already have the number of a down word
            elif cell.down_num == 0:
                # if the cell has an upwards neighbor
                # that does have the number of a down word
                if row != 0 and cellgrid.cells[row-1][column].down_num > 0:
                    # make cell's down_num the same as its upwards neighbor
                    cell.down_num = cellgrid.cells[row-1][column].down_num
                    d_index = f'{cell.down_num} down'

                    # update length of down word
                    cellgrid.words[d_index].length += 1

                    # figure out cell's position in the down word
                    # for ease of future word changes
                    # by subtracting 1 from current recorded word length
                    cell.down_pos = cellgrid.words[d_index].length - 1

                    # add coords to entry
                    cellgrid.words[d_index].coords.append((row, column))

                    # add letter to down word
                    cellgrid.words[d_index].letters.append(cell.letter.get())

    for entry_key in cellgrid.words:
        cellgrid.words[entry_key].updateWord()
        logger.debug(f"{entry_key}:{repr(cellgrid.words[entry_key].letters)}, {cellgrid.words[entry_key].word}")
    logger.debug("")

    #logger.debug(f"DEBUG\tWords: {cellgrid.words}\n")

