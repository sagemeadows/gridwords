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
    # (re)start counter
    counter = 0
    # clear any old cellgrid info
    cellgrid.words = {}
    cellgrid.wl = (-1, -1)
    
    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            # clear any old positions
            #cellgrid.cells[row][column].across_word_start = False
            #cellgrid.cells[row][column].across_word_member = False
            #cellgrid.cells[row][column].down_word_start = False
            #cellgrid.cells[row][column].down_word_member = False
            cellgrid.cells[row][column].across_pos = -1
            cellgrid.cells[row][column].down_pos = -1
            
            # if cell is colored from word-filling mode,
            # return it to white
            if cellgrid.cells[row][column].getColor() != WHITE \
            and cellgrid.cells[row][column].getColor() != BLACK:
                cellgrid.cells[row][column].setColor(WHITE)
            
            # if cell is white
            if cellgrid.cells[row][column].getColor() == WHITE:
                # clear any old directions indices to 0
                cellgrid.cells[row][column].across_num = 0
                cellgrid.cells[row][column].down_num = 0
                
                
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
                    
                    # add number to words dict
                    cellgrid.words[str(counter)] = [[], []]
                else:
                    cellgrid.cells[row][column].setClueIndex('')
                 
                # if cell is the start of a horizontal word
                if word_across:
                    cellgrid.cells[row][column].across_word_start = True
                    #cellgrid.across[row][column] = counter
                    cellgrid.cells[row][column].across_num = counter
                    #cellgrid.cells[row][column].across_pos = 0
                    # fill 'across' space for number in words dict
                    cellgrid.words[str(counter)][0].extend([0, '', "clue", [] ])
                else:
                    cellgrid.cells[row][column].across_word_start = False
      
                # if cell is the start of a vertical word
                if word_down:
                    #cellgrid.down[row][column] = counter
                    cellgrid.cells[row][column].down_num = counter
                    #cellgrid.cells[row][column].down_pos = 0
                    # fill 'down' space for number in words dict
                    cellgrid.words[str(counter)][1].extend([0, '', "clue", [] ])

            else: # cell is black
                cellgrid.cells[row][column].setClueIndex(-1)
                # clear any old direction indices to -1
                cellgrid.cells[row][column].across_num = -1
                cellgrid.cells[row][column].down_num = -1
                #cellgrid.numgrid[row][column] = -1 
                # clear any old letter to '.'
                cellgrid.cells[row][column].letter.set('.')


def spreadIndices(cellgrid):
    # Put numbers in 'across' and 'down' grid templates
    # and put letters in 'words'
    for row in range(len(cellgrid.cells)):
        for column in range(len(cellgrid.cells[0])):
            # check across array at coordinate.
            # if cell already has the number of an across word
            if cellgrid.cells[row][column].across_num > 0:
                # update length of across word
                cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][0] += 1
                # figure out cell's position in the across word
                # for ease of future word changes
                # by subtracting 1 from current recorded word length
                cellgrid.cells[row][column].across_pos = cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][0] - 1
                # add letter to across word
                cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][1] += cellgrid.cells[row][column].letter.get()
            
            # if the cell is white does not already have the number of an across word
            elif cellgrid.cells[row][column].across_num == 0:
                # if the cell has a neighbor to its left 
                # that does have the number of an across word
                if column != 0 and cellgrid.cells[row][column-1].across_num > 0:
                    # make cell's across_num the same as its leftward neighbor
                    cellgrid.cells[row][column].across_num = cellgrid.cells[row][column-1].across_num
                    # update length of across word
                    cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][0] += 1
                    # figure out cell's position in the across word
                    # for ease of future word changes
                    # by subtracting 1 from current recorded word length
                    cellgrid.cells[row][column].across_pos = cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][0] - 1
                    # add letter to across word
                    cellgrid.words[str(cellgrid.cells[row][column].across_num)][0][1] += cellgrid.cells[row][column].letter.get()
            
            # check down array at coordinate.
            # if cell already has the number of a down word
            if cellgrid.cells[row][column].down_num > 0:
                # update length of across word
                cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][0] += 1
                # figure out cell's position in the down word
                # for ease of future word changes
                # by subtracting 1 from the current recorded word length
                cellgrid.cells[row][column].down_pos = cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][0] - 1
                # add letter to down word
                cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][1] += cellgrid.cells[row][column].letter.get()
            
            # if the cell is white but does not already have the number of a down word
            elif cellgrid.cells[row][column].down_num == 0:
                # if the cell has an upwards neighbor
                # that does have the number of a down word
                if row != 0 and cellgrid.cells[row-1][column].down_num > 0:
                    # make cell's down_num the same as its upwards neighbor
                    cellgrid.cells[row][column].down_num = cellgrid.cells[row-1][column].down_num
                    # update length of down word
                    cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][0] += 1
                    # figure out cell's position in the down word
                    # for ease of future word changes
                    # by subtracting 1 from current recorded word length
                    cellgrid.cells[row][column].down_pos = cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][0] - 1
                    # add letter to down word
                    cellgrid.words[str(cellgrid.cells[row][column].down_num)][1][1] += cellgrid.cells[row][column].letter.get()
                    
    print(f"DEBUG\tWords: {cellgrid.words}\n")

