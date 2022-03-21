#! /usr/bin/python
#
# gridmaker.py
#
# Usage:
#     gridmaker.py
#
# Create crossword puzzle grids.
#

import sys
import pygame
print()

# Print instructions
instructions = """
Welcome to Gridwords!

Click on the boxes to design your crossword puzzle.
Press ESC or close Pygame window to quit. 
"""
print(instructions)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Set WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# Set the margin between each cell
MARGIN = 5

# Get number of rows and columns from user input
rows = int(input(" Enter number of rows: "))
columns = int(input(" Enter number of rows: "))
print()

# Create arrays
grid = [] # whether a square is black or white
numgrid = [] # where words start
across = [] # where across words are
down = [] # where down words are

letters = [] # where actual letters go
working_word = [] # word that's being filled in; highlight yellow
working_letter = [] # letter that's being filled in; highlight {color?}
poss = [] # whether a partial word can still 
          # be a word (highlight green) or not (highlight red)

for row in range(rows):
    # Add empty list (row)
    grid.append([])
    numgrid.append([])
    across.append([])
    down.append([])
    
    letters.append([])
    working_word.append([])
    working_letter.append([])
    poss.append([])
    
    for column in range(columns):
        # Add cell (column)
        grid[row].append(1)
        numgrid[row].append(0)
        across[row].append(-1)
        down[row].append(-1)
        
        letters[row].append(' ')
        working_word[row].append(0)
        working_letter[row].append(0)
        poss[row].append(0)
 
# Start pygame
pygame.init()
 
# Set the width and height of the screen [width, height]
# based on number of rows and columns
window_width = WIDTH * columns + MARGIN * (columns + 1)
window_height = HEIGHT * rows + MARGIN * (rows + 1)
window_size = [window_width, window_height]
screen = pygame.display.set_mode(window_size)
 
pygame.display.set_caption("Gridwords")

# Group letters
letter_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, 
               pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, 
               pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, 
               pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]

# Set fonts
num_font = pygame.font.SysFont('Calibri', 15, True, False)
let_font = pygame.font.SysFont('Calibri', 30, False, False)

# Put text in grid boxes
def box_num(row, column, num):
    text = num_font.render(str(num), True, BLACK)
    screen.blit(text, [(MARGIN + WIDTH) * column + MARGIN,
                       (MARGIN + HEIGHT) * row + MARGIN])

def box_let(row, column, letter):
    text = let_font.render(letter, True, BLACK)
    screen.blit(text, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 4,
                       (MARGIN + HEIGHT) * row + MARGIN + HEIGHT / 4])

# Loop until the user clicks the close button.
done = False

# Set initial mode as grid-editing
mode = 'grid'
print("INFO\tYou are in grid-editing mode!")

# Establish word-filling direction variable
working_direc = 'across'
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            
            # If user is eiditing grid layout
            if mode == 'grid':
                # Set that location and opposite location
                # to the opposite of its current value
                if grid[row][column] == 0:
                    grid[row][column] = 1
                    grid[0-row-1][0-column-1] = 1
                elif grid[row][column] == 1:
                    grid[row][column] = 0
                    grid[0-row-1][0-column-1] = 0
                #print(f"CLICK\t{pos}\tGrid coordinates: ({row}, {column})")
            
            # If user is filling in words
            elif mode == 'fill':
                # make sure user clicked on an open square
                if grid[row][column] == 1:
                    # clear previous working letter and word
                    for rw in range(rows):
                        for cl in range(columns):
                            working_letter[rw][cl] = 0
                            working_word[rw][cl] = 0
                    # mark new working letter
                    working_letter[row][column] = 1
                    # use left click to get default direction which
                    # is across unless square is not in an across word
                    if event.button == 1:
                        if across[row][column] > 0:
                            working_direc = 'across'
                        elif down[row][column] > 0:
                            working_direc = 'down'
                    # use right click to change working direction
                    elif event.button == 3:
                        # as long as that letter is in both an across and down word
                        if across[row][column] > 0 and down[row][column] > 0:
                            if working_direc == 'across':
                                working_direc = 'down'
                            elif working_direc == 'down':
                                working_direc = 'across'
                    if working_direc == 'across':
                        for rw in range(rows):
                            for cl in range(columns):
                                if across[rw][cl] == across[row][column]:
                                    working_word[rw][cl] = 1
                    elif working_direc == 'down':
                        for rw in range(rows):
                            for cl in range(columns):
                                if down[rw][cl] == down[row][column]:
                                    working_word[rw][cl] = 1
        
        elif event.type == pygame.KEYDOWN:
            # Quit
            if event.key == pygame.K_ESCAPE:
                done = True
            # Change mode
            elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if mode == 'grid':
                    mode = 'fill'
                    print("INFO\tYou are in word-filling mode!")
                elif mode == 'fill':
                    mode = 'grid'
                    # clear working_letter and working_word
                    for row in range(rows):
                        for column in range(columns):
                            working_letter[row][column] = 0
                            working_word[row][column] = 0
                    print("INFO\tYou are in grid-editing mode!")
            # Save grid
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                #print(f"DEBUG\tAcross Grid: {across}")
                #print(f"DEBUG\tDown Grid: {down}")
                #print(f"DEBUG\tLetters Grid: {letters}")
                #print(f"DEBUG\tWords: {words}")
                proceed = input("QUERY\tSave grid? Y/n : ")
                yes = 'Y', 'y', ''
                if proceed in yes:
                    filename = input("INPUT\tEnter file name: ")
                    f = open(filename, 'w')
                    f.write('grid = ' + repr(grid) + '\n')
                    f.write('numgrid = ' + repr(numgrid) + '\n')
                    f.write('across = ' + repr(across) + '\n')
                    f.write('down = ' + repr(down) + '\n')
                    f.write('letters = ' + repr(letters) + '\n')
                    f.write('words = ' + repr(words) + '\n')
                    f.close()
                    print(f"INFO\tGrid saved to '{filename}'")
                    exit = input("QUERY\tClose Gridwords? Y/n : ")
                    if exit in yes:
                        done = True
                else:
                    print("INFO\tGrid not saved")
                    exit = input("QUERY\tClose Gridwords? Y/n : ")
                    if exit in yes:
                        done = True
                    elif mode == 'grid':
                        print("INFO\tYou are in grid-editing mode!")
                    elif mode == 'fill':
                        print("INFO\tYou are in word-filling mode!")
            # Insert letter
            elif event.key in letter_keys:
                for row in range(rows):
                    for column in range(columns):
                        if working_letter[row][column] == 1:
                            letters[row][column] = pygame.key.name(event.key).upper()
            # Delete letter
            elif event.key == pygame.K_BACKSPACE:
                for row in range(rows):
                    for column in range(columns):
                        if working_letter[row][column] == 1:
                            letters[row][column] = ' '
    
    # Clear screen
    screen.fill(BLACK)
 
    # Draw grid boxes
    for row in range(rows):
        for column in range(columns):
            color = WHITE
            if grid[row][column] == 0:
                color = BLACK
            elif working_letter[row][column] == 1:
                color = ORANGE
            elif working_word[row][column] == 1:
                color = YELLOW
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Clear box numbers
    for row in range(rows):
        for column in range(columns):
            numgrid[row][column] = 0

    # Get grid template for 'across' and 'down' grids,
    # with -1 for black spaces and 0 for white spaces.
    # For 'letters', get template with '#' for black spaces
    # but leave any letters in the white spaces
    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == 0:
                across[row][column] = -1
                down[row][column] = -1
                letters[row][column] = '#'
            elif grid[row][column] == 1:
                across[row][column] = 0
                down[row][column] = 0

    # Get empty words dict
    words = {}

    # Count boxes and draw box numbers
    counter = 0
    for row in range(rows):
        for column in range(columns):
            # if square is white
            if grid[row][column] == 1:
                give_num = False
                word_across = False
                word_down = False
                
                # if square is in the top row
                if row == 0:
                    # if square is in the top left corner
                    if column == 0:
                        # HORIZONTAL CHECK FROM EDGE: if the square to its right is white
                        if grid[row][column+1] == 1:
                            give_num = True
                            word_across = True
                        # VERTICAL CHECK FROM EDGE: if the square below is white
                        if grid[row+1][column] == 1:
                            give_num = True
                            word_down = True
                    # if square is in the top right corner
                    elif column == range(columns)[-1]:
                        # VERTICAL CHECK FROM EDGE ONLY: if the square below is white
                        if grid[row+1][column] == 1:
                            give_num = True
                            word_down = True
                    else: # the square is in the top row 
                          # but not leftmost or rightmost column
                        # REGULAR HORIZONTAL CHECK: if the square to the left is black 
                        #                           and the one to the right is white
                        if grid[row][column-1] == 0 and grid[row][column+1] == 1:
                            give_num = True
                            word_across = True
                        # VERTICAL CHECK FROM EDGE: if square below is white
                        if grid[row+1][column] == 1:
                            give_num = True
                            word_down = True
                
                # if square is on bottom row
                if row == range(rows)[-1]:
                    # if the square is in the bottom left corner
                    if column == 0:
                        # HORIZONTAL CHECK FROM EDGE ONLY: if the square to its right is white
                        if grid[row][column+1] == 1:
                            give_num = True
                            word_across = True
                    # if square is in the bottom right corner
                    elif column == range(columns)[-1]:
                        # NO HORIZONTAL OR VERTICAL CHECK
                        break
                    else: # the square is on the bottom row 
                          # but not leftmost or rightmost column
                        # REGULAR HORIZONTAL CHECK ONLY: if the square to the left is black 
                        #                                and the one to the right is white
                        if grid[row][column-1] == 0 and grid[row][column+1] == 1:
                            give_num = True
                            word_across = True
                
                # if square is in the leftmost column
                # (but not in top or bottom row, bc we already covered that)
                elif column == 0 and row != 0:
                    # HORIZONTAL CHECK FROM EDGE: if the square to its right is white
                    if grid[row][column+1] == 1:
                        give_num = True
                        word_across = True
                    # REGULAR VERTICAL CHECK: if the square above is black 
                    #                         and the one below is white
                    if grid[row-1][column] == 0 and grid[row+1][column] == 1:
                        give_num = True
                        word_down = True
                
                # if square is in the rightmost column
                # (but not in top or bottom row, bc we already covered that)
                elif column == range(columns)[-1]:
                    # REGULAR VERTICAL CHECK ONLY: if the square above is black
                    #                              and the one below is white
                    if grid[row-1][column] == 0 and grid[row+1][column] == 1:
                        give_num = True
                        word_down = True
                
                else: # square is not at any edge
                    # REGULAR HORIZONTAL CHECK: if the square to its left is black
                    #                           and the one to its right is white
                    if grid[row][column-1] == 0 and grid[row][column+1] == 1:
                        give_num = True
                        word_across = True
                    # REGULAR VERTICAL CHECK: if the square above is black
                    #                         and the one below is white
                    if grid[row-1][column] == 0 and grid[row+1][column] == 1:
                        give_num = True
                        word_down = True
                
                # if square is the start of a word
                if give_num:
                    # give it a number
                    counter += 1
                    numgrid[row][column] = counter
                    box_num(row, column, counter)
                    # add number to words dict
                    words[str(counter)] = [[], []]
                
                # if square is the start of horizontal word
                if word_across:
                    # add number to 'across' grid
                    across[row][column] = counter
                    # fill 'across' space for number in words dict
                    words[str(counter)][0].extend([0, '', "clue"])
                
                # if square is the start of vertical word
                if word_down:
                    # add number to the down grid
                    down[row][column] = counter
                    # fill 'down' space for number in words dict
                    words[str(counter)][1].extend([0, '', "clue"])

    
    # Put numbers in 'across' and 'down' grid templates
    # and put letters in 'words'
    for row in range(rows):
        for column in range(columns):
            # check across array at coordinate
            if across[row][column] > 0:
                words[str(across[row][column])][0][0] += 1
                words[str(across[row][column])][0][1] += letters[row][column]
            elif across[row][column] == 0:
                if across[row][column-1] > 0:
                    across[row][column] += across[row][column-1]
                    words[str(across[row][column])][0][0] += 1
                    words[str(across[row][column])][0][1] += letters[row][column]
            # check down array at coordinate
            if down[row][column] > 0:
                words[str(down[row][column])][1][0] += 1
                words[str(down[row][column])][1][1] += letters[row][column]
            elif down[row][column] == 0:
                if down[row-1][column] > 0:
                    down[row][column] += down[row-1][column]
                    words[str(down[row][column])][1][0] += 1
                    words[str(down[row][column])][1][1] += letters[row][column]


    # Draw letters
    for row in range(rows):
        for column in range(columns):
            # if square is white
            if grid[row][column] == 1:
                ignore = ['#', ' ']
                if letters[row][column] not in ignore:
                    box_let(row, column, letters[row][column])
    
    # Update the screen with what we've drawn
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit
print("INFO\tExiting Gridwords...\n")
pygame.quit()

