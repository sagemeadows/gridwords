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

# Print instructions
instructions = """
Welcome to Gridwords!
"""
print(instructions)

# Define colors with hex codes
WHITE = '#ffffff'
BLACK = '#000000'
GRAY = '#d9d9d9'
BLUE = '#0000ff'
CYAN = '#00ffff'
GREEN = '#00ff00'
RED = '#ff0000'
ORANGE = '#ffa500'
YELLOW = '#ffff00'

# Set grid cell square size
CELL_SIDE = 50

# Set the margin between each cell
CELL_MARGIN = 3
INDEX_MARGIN = 2

## Get number of rows and columns from user input
ROWS = int(input(" Enter number of rows: "))
COLUMNS = int(input(" Enter number of rows: "))
CELLS_PER_GRID = ROWS * COLUMNS
print()

# Define classes
class Cell(tk.Frame):
    def __init__(self, master=None, text='.', width=CELL_SIDE, height=CELL_SIDE, index=-1):
        # create and format frame
        tk.Frame.__init__(self, master=master, width=width, height=height, relief=tk.FLAT, bg=BLACK, bd=0)
        self.grid_propagate(0)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        
        # declare a 'letter' data member for updating the text of the button
        self.letter = tk.StringVar()
        self.letter.set('.')

        self.index = index

        # create a data member called 'button' with 'self' as parent
        self.button = tk.Button(self, textvariable=self.letter, command=self.onClick)

        # color button always white
        self.button.configure(background=WHITE, activebackground=WHITE, relief=tk.FLAT, bd=0)

        # tell button to expand to fill this entire frame
        self.button.grid(stick='NWSE')

        # add a label for the number in the uppper left corner
        self.clue_index = tk.StringVar()
        self.clue_index.set(str(index))
        self.clue_label = tk.Label(self, textvariable=self.clue_index)
        self.clue_label.configure(background=WHITE, activebackground=WHITE)
        self.clue_label.place(x=INDEX_MARGIN, y=INDEX_MARGIN)

    def setText(self, text):
        # update self.text variable which will automatically update the self.button's text
        self.text.set(text)

    def setClueIndex(self, index):
        self.clue_index.set(str(index))

    def onClick(self):
        if mode == 'grid':
            color_hex = self.button.cget('background')
            if color_hex == WHITE:
                color_hex = BLACK
            else:
                color_hex = WHITE
            self.setColor(color_hex)
            
            # tell the grid to make the symmetric counterpart cell agree
            self.master.onCellClick(self.index)
        elif mode == 'fill':
            print(f"Clicked on cell at ({self.x}, {self.y})")

    def setColor(self, color_hex):
        self.button.configure(background=color_hex, activebackground=color_hex)
        self.clue_label.configure(background=color_hex, activebackground=color_hex)

    def getColor(self):
        return self.button.cget('background')


# create a CellGrid class that derives from tk.Frame
# it will have a grid of Cells
class CellGrid(tk.Frame):
    # define the ctor method 
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=BLACK, bd=CELL_MARGIN)

        # create the member variable 'cells'
        self.cells = []
        for i in range(CELLS_PER_GRID):
            # create a Cell with 'self' as parent
            cell = Cell(self, index=i)

            # set cell's grid in this Frame
            column = int(i % COLUMNS)
            row = int(i / ROWS)
            cell.grid(row=row, column=column, padx=CELL_MARGIN, pady=CELL_MARGIN)

            # DEBUG HACK: for now we populate cell with a unique letter of the alphabet
            #t = chr(ord('A') + i)
            #cell.setText(t)
            self.cells.append(cell)

    def onCellClick(self, index):
        color_hex = self.cells[index].getColor()
        column = int(index % COLUMNS)
        row = int(index / ROWS)

        other_column = COLUMNS - column - 1
        other_row = ROWS - row - 1

        other_index = CELLS_PER_GRID - index - 1

        self.cells[other_index].setColor(color_hex)


# Initial mode
mode = 'grid'

# Define functions
def changeMode():
    global mode
    if mode == 'grid':
        mode = 'fill'
        lbl_mode["text"] = "You are in Word-Filling Mode"
    elif mode == 'fill':
        mode = 'grid'
        lbl_mode["text"] = "You are in Grid-Editing Mode"


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

# this __name__ == "__main__" check will evaluate True when this script is executed directly
# but False when this script is loaded it as a module
if __name__ == "__main__":
    # a root Tk window would be created for us automatically if we neglected to do so
    # but create it explicitly here
    root_window = tk.Tk()
    root_window.title("Gridwords")
    root_window.configure(bg='white')

    # create gridwords logo in top left corner
    logo = tk.Label(root_window, text="LOGO", background=YELLOW)
    logo.grid(row=0, column=0)
    
    # create top bar with mode button
    frm_topbar = tk.Frame(root_window, relief=tk.FLAT, bd=2, bg=WHITE)
    frm_topbar.grid(row=0, column=1)
    # create mode label
    lbl_mode = tk.Label(frm_topbar, text="You are in Grid-Editing Mode", bd=2, bg=WHITE)
    lbl_mode.grid(row=0, column=0)
    # create mode button
    btn_chmd = tk.Button(frm_topbar, text="Change Mode", command=changeMode)
    btn_chmd.grid(row=0, column=1)
    
    # create sidebar
    frm_sidebar = tk.Frame(root_window, relief=tk.FLAT, bd=2, bg=WHITE)
    frm_sidebar.grid(row=1, column=0)
    # create buttons to go in sidebar
    btn_resize = tk.Button(frm_sidebar, text="Resize")#, command=resize)
    btn_resize.grid(row=0, column=0, padx=5, pady=5)
    
    btn_open = tk.Button(frm_sidebar, text="Open", command=open_file)
    btn_open.grid(row=1, column=0, padx=5, pady=5)

    btn_save = tk.Button(frm_sidebar, text="Save As...", command=save_file)
    btn_save.grid(row=2, column=0, padx=5)
    
    # create a CellGrid and pack it into its parent (e.g. root_window)
    cell_grid = CellGrid(root_window)
    cell_grid.grid(row=1, column=1)
    
    # start handling UI events
    root_window.mainloop()


