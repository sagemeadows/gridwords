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
Welcome to Crossword Grid Maker!

Click on the boxes to design your crossword puzzle.
Press ESC or close Pygame window to quit. 
"""
print(instructions)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
grid = []
numgrid = []
across = []
down = []

for row in range(rows):
    # Add empty list (row)
    grid.append([])
    numgrid.append([])
    across.append([])
    down.append([])
    for column in range(columns):
        # Add cell (column)
        grid[row].append(1)
        numgrid[row].append(0)
        across[row].append(-1)
        down[row].append(-1)
 
# Start pygame
pygame.init()
 
# Set the width and height of the screen [width, height]
# based on number of rows and columns
window_width = WIDTH * columns + MARGIN * (columns + 1)
window_height = HEIGHT * rows + MARGIN * (rows + 1)
window_size = [window_width, window_height]
screen = pygame.display.set_mode(window_size)
 
pygame.display.set_caption("Crossword Grid Maker")
 
# Set fonts
font = pygame.font.SysFont('Calibri', 25, False, False)
num_font = pygame.font.SysFont('Calibri', 10, True, False)

# Put text in grid boxes
def box_num(row, column, num):
    text = font.render(str(num), True, BLACK)
    screen.blit(text, [(MARGIN + WIDTH) * column + MARGIN,
                       (MARGIN + HEIGHT) * row + MARGIN])

# Loop until the user clicks the close button.
done = False
 
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
            # Set that location and opposite location
            # to the opposite of its current value
            if grid[row][column] == 0:
                grid[row][column] = 1
                grid[0-row-1][0-column-1] = 1
            elif grid[row][column] == 1:
                grid[row][column] = 0
                grid[0-row-1][0-column-1] = 0
            #print("INFO", "Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("  Exiting grid maker\n")
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                #print("DEBUG", f"Across Grid: {across}")
                #print("DEBUG", f"Down Grid: {down}")
                #print("DEBUG", f"Words: {words}")
                proceed = input(" Save grid? Y/n : ")
                yes = 'Y', 'y', ''
                if proceed in yes:
                    filename = input("Enter file name: ")
                    f = open(filename, 'w')
                    f.write('grid = ' + repr(grid) + '\n')
                    f.write('numgrid = ' + repr(numgrid) + '\n')
                    f.write('across = ' + repr(across) + '\n')
                    f.write('down = ' + repr(down) + '\n')
                    f.close()
                    print(f"  Grid saved to '{filename}'")
                else:
                    print("  Grid not saved")
                    exit = input(" Close grid? Y/n : ")
                    if exit in yes:
                        print("  Exiting grid maker\n")
                        pygame.quit()
                        sys.exit()
                    else:
                        print(" Return to editing\n")
 
    # Clear screen
    screen.fill(BLACK)
 
    # Draw grid boxes
    for row in range(rows):
        for column in range(columns):
            color = WHITE
            if grid[row][column] == 0:
                color = BLACK
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

    # Get grid template for across and down grids,
    # with -1 for black spaces and 0 for white spaces
    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == 0:
                across[row][column] = -1
                down[row][column] = -1
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
                    words[str(counter)][0].extend([0, "word", "clue"])
                
                # if square is the start of vertical word
                if word_down:
                    # add number to the down grid
                    down[row][column] = counter
                    # fill 'down' space for number in words dict
                    words[str(counter)][1].extend([0, "word", "clue"])

    
    # Put numbers in 'across' and 'down' grid templates
    for row in range(rows):
        for column in range(columns):
            # check across array at coordinate
            if across[row][column] > 0:
                words[str(across[row][column])][0][0] += 1
            elif across[row][column] == 0:
                if across[row][column-1] > 0:
                    across[row][column] += across[row][column-1]
                    words[str(across[row][column])][0][0] += 1
            # check down array at coordinate
            if down[row][column] > 0:
                words[str(down[row][column])][1][0] += 1
            elif down[row][column] == 0:
                if down[row-1][column] > 0:
                    down[row][column] += down[row-1][column]
                    words[str(down[row][column])][1][0] += 1


    # Update the screen with what we've drawn
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()

