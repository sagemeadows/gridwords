#! /usr/bin/python
#
# move.py
#
# Usage:
#     module for gridwords.py
#
# Move working letter and highlight working word.
#

import logging

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

SELECTED_CELL_BACKGROUND = YELLOW
SELECTED_WORD_BACKGROUND = CYAN

def moveUp(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row == 0:
            if column > 0:
                cellgrid.wl = (len(cellgrid.cells), column-1)
            else:
                cellgrid.wl = (len(cellgrid.cells), len(cellgrid.cells[0])-1)
            moveUp(None, cellgrid=cellgrid)

        elif row > 0:
            if cellgrid.cells[row-1][column].getColor() != BLACK:
                cell = cellgrid.cells[row-1][column]
                # select and highlight new working word and letter
                select(cell, cellgrid)
                highlight(cellgrid)

            else:
                cellgrid.wl = (row-1, column)
                moveUp(None, cellgrid=cellgrid)

def moveDown(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row == len(cellgrid.cells) - 1:
            if column < len(cellgrid.cells[0]) - 1:
                cellgrid.wl = (-1, column+1)
            else:
                cellgrid.wl = (-1, 0)
            moveDown(None, cellgrid=cellgrid)

        elif row < len(cellgrid.cells) - 1:
            if cellgrid.cells[row+1][column].getColor() != BLACK:
                cell = cellgrid.cells[row+1][column]
                # select and highlight new working word and letter
                select(cell, cellgrid)
                highlight(cellgrid)

            else:
                cellgrid.wl = (row+1, column)
                moveDown(None, cellgrid=cellgrid)

def moveLeft(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column == 0:
            if row > 0:
                cellgrid.wl = (row-1, len(cellgrid.cells[0]))
            else:
                cellgrid.wl = (len(cellgrid.cells)-1, len(cellgrid.cells[0]))
            moveLeft(None, cellgrid=cellgrid)

        elif column > 0:
            if cellgrid.cells[row][column-1].getColor() != BLACK:
                cell = cellgrid.cells[row][column-1]
                # select and highlight new working word and letter
                select(cell, cellgrid)
                highlight(cellgrid)

            else:
                cellgrid.wl = (row, column-1)
                moveLeft(None, cellgrid=cellgrid)

def moveRight(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column == len(cellgrid.cells[0]) - 1:
            if row < len(cellgrid.cells) - 1:
                cellgrid.wl = (row+1, -1)
            else:
                cellgrid.wl = (0, -1)
            moveRight(None, cellgrid=cellgrid)

        elif column < len(cellgrid.cells[0]) - 1:
            if cellgrid.cells[row][column+1].getColor() != BLACK:
                cell = cellgrid.cells[row][column+1]
                # select and highlight new working word and letter
                select(cell, cellgrid)
                highlight(cellgrid)

            else:
                cellgrid.wl = (row, column+1)
                moveRight(None, cellgrid=cellgrid)


def select(cell, cellgrid):
    # reset old working word, if it exists
    if cellgrid.wword:
        for coord in cellgrid.wword.coords:
            cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)

    # set new working letter
    cellgrid.wl = (cell.row, cell.column)
    logger.debug(f"Working Cell: {cellgrid.wl}")
    
    # get across_num and down_num of new working letter
    acr_num = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].across_num
    dwn_num = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].down_num
    
    # figure out new working word
    if cellgrid.wdirec == 'across':
        if acr_num > 0:
            cellgrid.wword = cellgrid.words[f'{acr_num} across']
        else:
            cellgrid.wdirec = 'down'
            cellgrid.wword = cellgrid.words[f'{dwn_num} down']
    elif cellgrid.wdirec == 'down':
        if dwn_num > 0:
            cellgrid.wword = cellgrid.words[f'{dwn_num} down']
        else:
            cellgrid.wdirec = 'across'
            cellgrid.wword = cellgrid.words[f'{acr_num} across']

def highlight(cellgrid):
    # set colors
    for coord in cellgrid.wword.coords:
        cellgrid.cells[coord[0]][coord[1]].setColor(SELECTED_WORD_BACKGROUND)
    cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].setColor(SELECTED_CELL_BACKGROUND)

