#! /usr/bin/python
#
# indices.py
#
# Usage:
#     module for gridwords.py
#
# Figure out clue indices and update grid.
#

WHITE = '#ffffff'
BLACK = '#000000'

def updateClueIndices(cellgrid):
    counter = 0
    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            # if cell is white
            if cellgrid.cells[row][column].getColor() == WHITE:
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
                        cellgrid.cells[row][column].setClueIndex('')
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
                    and cellgrid.cells[row+1][column] == WHITE:
                        give_num = True
                        word_down = True

                # if cell is the start of a word
                if give_num:
                    # give it a number
                    counter += 1
                    cellgrid.cells[row][column].setClueIndex(counter)
                    #cellgrid.numgrid[row][column] = counter
                    # add number to words dict (how?)
                    #words[str(counter)] = [[], []]
                else:
                    cellgrid.cells[row][column].setClueIndex('')
                 
                # if cell is the start of a horizontal word
                if word_across:
                    #cellgrid.across[row][column] = counter
                    cellgrid.cells[row][column].across_num = counter
                    cellgrid.cells[row][column].across_pos = 0
                    # fill 'across' space for number in words dict (how)
                    #words[str(counter)][0].extend([0, '', "clue", [] ])
      
                # if cell is the start of a vertical word
                #if word_down:
                    #cellgrid.down[row][column] = counter
                    cellgrid.cells[row][column].down_num = counter
                    cellgrid.cells[row][column].down_pos = 0
                    # fill 'down' space for number in words dict (how)
                    #words[str(counter)][1].extend([0, '', "clue", [] ])

            else: # cell is black
                cellgrid.cells[row][column].setClueIndex(-1)
                #cellgrid.numgrid[row][column] = -1        

