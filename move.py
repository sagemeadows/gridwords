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

def highlight(cellgrid):
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
    
    # set colors
    for coord in cellgrid.wword.coords:
        cellgrid.cells[coord[0]][coord[1]].setColor(CYAN)
    cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].setColor(BLUE)

