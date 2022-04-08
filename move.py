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
    if f'{acr_num} {cellgrid.wdirec}' in cellgrid.words:
        cellgrid.wword = cellgrid.words[f'{acr_num} {cellgrid.wdirec}']
    elif f'{dwn_num} {cellgrid.wdirec}' in cellgrid.words:
        cellgrid.wword = cellgrid.words[f'{dwn_num} {cellgrid.wdirec}']
    elif f'{acr_num} across' in cellgrid.words:
        cellgrid.wword = cellgrid.words[f'{acr_num} across']
        cellgrid.wdirec = 'across'
    elif f'{dwn_num} down' in cellgrid.words:
        cellgrid.wword = cellgrid.words[f'{dwn_num} down']
        cellgrid.wdirec = 'down'
    
    # set colors
    for coord in cellgrid.wword.coords:
        cellgrid.cells[coord[0]][coord[1]].setColor(CYAN)
    cellgrid.cells[cellgrid.wl[0]][cellgrid.wl[1]].setColor(BLUE)

