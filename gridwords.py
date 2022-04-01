#! /usr/bin/python
#
# gridwords.py
#
# Usage:
#     gridwords.py
#
# Create and fill crossword puzzle grids.
#

import sys
import os
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Define classes
class Cell(tk.Button):
    def __init__(self, master, x, y, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        #self.clue_index
        #self.letter
        #self.bind("<Button-1>", lambda : cell_click(x, y))


# Print instructions
instructions = """
Welcome to Gridwords!
"""
print(instructions)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Set WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40

# Set the margin between each cell
MARGIN = 5

## Get number of rows and columns from user input
ROWS = int(input(" Enter number of rows: "))
COLUMNS = int(input(" Enter number of rows: "))
print()

# Create arrays
grid = [] # whether a square is black or white
numgrid = [] # where words start
across = [] # where across words are
down = [] # where down words are

letters = [] # where actual letters go
working_word = [] # word that's being filled in; highlight yellow
working_letter = [] # letter that's being filled in; highlight {color?}

poss_nums_across = [] # how many possibilities for across words
poss_nums_down = [] # how many possibilities for down words

for row in range(ROWS):
    # Add empty list (row)
    grid.append([])
    numgrid.append([])
    across.append([])
    down.append([])
    
    letters.append([])
    working_word.append([])
    working_letter.append([])
    
    poss_nums_across.append([])
    poss_nums_down.append([])

    for column in range(COLUMNS):
        # Add cell (column)
        grid[row].append(1)
        numgrid[row].append(0)
        across[row].append(-1)
        down[row].append(-1)
        
        letters[row].append('.')
        working_word[row].append(0)
        working_letter[row].append(0)
        
        poss_nums_across[row].append(100)
        poss_nums_down[row].append(100)

# Initial mode
mode = 'grid'

# Define functions
def change_mode():
    global mode
    if mode == 'grid':
        mode = 'fill'
        btn_chmd = tk.Button(frm_buttons, text="Word-Filling Mode", command=change_mode)
        btn_chmd.grid(row=0, column=0, sticky="ew", padx=MARGIN, pady=MARGIN)
    elif mode == 'fill':
        mode = 'grid'
        btn_chmd = tk.Button(frm_buttons, text="Grid-Editing Mode", command=change_mode)
        btn_chmd.grid(row=0, column=0, sticky="ew", padx=MARGIN, pady=MARGIN)

def opp_coords(row, column):
    opp_row = range(ROWS)[0-row-1]
    opp_col = range(COLUMNS)[0-column-1]
    return opp_row, opp_col

def cell_click(row, column):
    global mode
    if mode == 'grid':
        if grid[row][column] == 1:
            grid[row][column] = 0
            grid[0-row-1][0-column-1] = 0
            opp_row, opp_col = opp_coords(row, column)
            
            exec(f'frm{row}_{column}.destroy()')
            exec(f'frm{row}_{column} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
            exec(f'frm{row}_{column}.grid_propagate(False)')
            exec(f'frm{row}_{column}.columnconfigure(0, weight=1)')
            exec(f'frm{row}_{column}.rowconfigure(0, weight=1)')
            exec(f'frm{row}_{column}.grid(row={row}, column={column})')
            exec(f'btn{row}_{column} = Cell(frm{row}_{column}, {row}, {column}, text="({row}, {column})", \
                   height=40, width=40, bg="black", activebackground="#28211b", relief=tk.FLAT, \
                   command=lambda : cell_click({row}, {column})).grid(sticky="news")')
            
            exec(f'frm{opp_row}_{opp_col}.destroy()')
            exec(f'frm{opp_row}_{opp_col} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
            exec(f'frm{opp_row}_{opp_col}.grid_propagate(False)')
            exec(f'frm{opp_row}_{opp_col}.columnconfigure(0, weight=1)')
            exec(f'frm{opp_row}_{opp_col}.rowconfigure(0, weight=1)')
            exec(f'frm{opp_row}_{opp_col}.grid(row={opp_row}, column={opp_col})')
            exec(f'btn{opp_row}_{opp_col} = Cell(frm{opp_row}_{opp_col}, {opp_row}, {opp_col}, text="({opp_row}, {opp_col})", \
                   height=40, width=40, bg="black", activebackground="#28211b", relief=tk.FLAT, \
                   command=lambda : cell_click({opp_row}, {opp_col})).grid(sticky="news")')
            
            print(f"Turned box black at ({row}, {column}) and ({opp_row}, {opp_col})")
            
        elif grid[row][column] == 0:
            grid[row][column] = 1
            grid[0-row-1][0-column-1] = 1
            opp_row, opp_col = opp_coords(row, column)
            
            exec(f'frm{row}_{column}.destroy()')
            exec(f'frm{row}_{column} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
            exec(f'frm{row}_{column}.grid_propagate(False)')
            exec(f'frm{row}_{column}.columnconfigure(0, weight=1)')
            exec(f'frm{row}_{column}.rowconfigure(0, weight=1)')
            exec(f'frm{row}_{column}.grid(row={row}, column={column})')
            exec(f'btn{row}_{column} = Cell(frm{row}_{column}, {row}, {column}, text="({row}, {column})", \
                   height=40, width=40, bg="white", relief=tk.FLAT, \
                   command=lambda : cell_click({row}, {column})).grid(sticky="news")')
            
            exec(f'frm{opp_row}_{opp_col}.destroy()')
            exec(f'frm{opp_row}_{opp_col} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
            exec(f'frm{opp_row}_{opp_col}.grid_propagate(False)')
            exec(f'frm{opp_row}_{opp_col}.columnconfigure(0, weight=1)')
            exec(f'frm{opp_row}_{opp_col}.rowconfigure(0, weight=1)')
            exec(f'frm{opp_row}_{opp_col}.grid(row={opp_row}, column={opp_col})')
            exec(f'btn{opp_row}_{opp_col} = Cell(frm{opp_row}_{opp_col}, {opp_row}, {opp_col}, text="({opp_row}, {opp_col})", \
                   height=40, width=40, bg="white", relief=tk.FLAT, \
                   command=lambda : cell_click({opp_row}, {opp_col})).grid(sticky="news")')
            
            print(f"Turned box white at ({row}, {column}) and ({opp_row}, {opp_col})")
    
    elif mode == 'fill':
        print(f"Clicked on box at ({row}, {column})")

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

# Establish window
window = tk.Tk()
window.title("Gridwords")
window.configure(bg='white')
#window.rowconfigure([0, 1, 2], minsize=400, weight=1)
#window.columnconfigure([0, 1, 2], minsize=400, weight=1)

frm_buttons = tk.Frame(window, relief=tk.FLAT, bd=2, bg="white")

btn_chmd = tk.Button(frm_buttons, text="Grid-Editing Mode", command=change_mode)
btn_chmd.grid(row=0, column=0, sticky="e", padx=MARGIN, pady=MARGIN)

btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_open.grid(row=0, column=1, sticky="w", padx=5, pady=5)

btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
btn_save.grid(row=0, column=2, sticky="w", padx=5)

frm_grid = tk.Frame(window, relief=tk.FLAT, bd=2, bg="black")
for row in range(ROWS):
    for column in range(COLUMNS):
        #exec(f'btn{row}_{column} = tk.Button(frm_grid, text="({row}, {column})", command=open_file)')
        #exec(f'frm{row}_{column} = tk.Frame(master=btn{row}_{column}, height=40, width=40, relief=tk.FLAT, bg="white").pack()')
        #exec(f'btn{row}_{column}.grid(row={row}, column={column}, padx=MARGIN, pady=MARGIN)')
        
        #exec(f'frm{row}_{column} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
        #exec(f'frm{row}_{column}.grid(row={row}, column={column})')
        #exec(f'btn{row}_{column} = tk.Button(frm{row}_{column}, text="({row}, {column})", \
        #       bg="white", relief=tk.FLAT, command=open_file).pack()')

        exec(f'frm{row}_{column} = tk.Frame(master=frm_grid, height=40, width=40,relief=tk.FLAT, bd=2, bg="black")')
        exec(f'frm{row}_{column}.grid_propagate(False)')
        exec(f'frm{row}_{column}.columnconfigure(0, weight=1)')
        exec(f'frm{row}_{column}.rowconfigure(0, weight=1)')
        exec(f'frm{row}_{column}.grid(row={row}, column={column})')
        exec(f'btn{row}_{column} = Cell(frm{row}_{column}, {row}, {column}, text="({row}, {column})", \
               height=40, width=40, bg="white", relief=tk.FLAT, \
               command=lambda : cell_click({row}, {column})).grid(sticky="news")')

frm_buttons.grid(row=0, column=0)
frm_grid.grid(row=1, column=0)

# Establish frames
#
#frm_posswords = tk.Frame(window)
#
#frm_clues = tk.Frame(window)

#frm_acr = tk.Frame(frm_clues)
#frm_dwn = tk.Frame(frm_clues)





#frm_buttons.grid(row=0, column=0)
#frm_grid.grid(row=1, column=0)
#frm_clues.grid(row=2, column=0)
#frm_posswords.grid(row=1, column=1)

#btn_decrease = tk.Button(master=window, text="-", command=decrease)
#btn_decrease.grid(row=0, column=0, sticky="nsew")

#lbl_value = tk.Label(master=window, text="0")
#lbl_value.grid(row=0, column=1)

#btn_increase = tk.Button(master=window, text="+", command=increase)
#btn_increase.grid(row=0, column=2, sticky="nsew")

window.mainloop()

