#! /usr/bin/python
#
# move.py
#
# Usage:
#     module for gridwords.py
#
# Move working letter and highlight working word.
#

WHITE = '#ffffff'
BLACK = '#000000'
GRAY = '#d9d9d9'
BLUE = '#0000ff'
CYAN = '#00ffff'
GREEN = '#00ff00'
RED = '#ff0000'
ORANGE = '#ffa500'
YELLOW = '#ffff00'

def moveUp(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row != 0 and cellgrid.cells[row-1][column].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row-1, column)
            cell = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]]
            
            # select and highlight new working word and letter
            select(cell, cellgrid)
            highlight(cellgrid)

def moveDown(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row != range(len(cellgrid.cells))[-1] and cellgrid.cells[row+1][column].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row+1, column)
            cell = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]]
            
            # select and highlight new working word and letter
            select(cell, cellgrid)
            highlight(cellgrid)

def moveLeft(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column != 0 and cellgrid.cells[row][column-1].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row, column-1)
            cell = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]]
            
            # select and highlight new working word and letter
            select(cell, cellgrid)
            highlight(cellgrid)

def moveRight(event, cellgrid=None):
    if cellgrid.mode == 'fill':
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column != range(len(cellgrid.cells[0]))[-1] and cellgrid.cells[row][column+1].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row, column+1)
            cell = cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]]
            
            # select and highlight new working word and letter
            select(cell, cellgrid)
            highlight(cellgrid)

def select(cell, cellgrid):
    # reset old working word, if it exists
    if cellgrid.wword:
        for coord in cellgrid.wword.coords:
            cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)

    # set new working letter
    cellgrid.wl = (cell.row, cell.column)
    #print(f"DEBUG\tWorking Cell: {cellgrid.wl}")
    
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
        cellgrid.cells[coord[0]][coord[1]].setColor(CYAN)
    cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].setColor(BLUE)

