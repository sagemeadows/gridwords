#!/usr/bin/python

'''
simple-tk-grid.py

Demo scirpt using object-oriented methods to build a tkinter window
with a grid of cells, each cell with a button holding a single letter of text.
'''

import tkinter as tk
from colour import Color

PIXELS_PER_CELL_SIDE = 100
PIXELS_PER_CELL_MARGIN = 4
CELLS_PER_GRID_SIDE = 4
CELLS_PER_GRID = CELLS_PER_GRID_SIDE * CELLS_PER_GRID_SIDE

WHITE = Color('#ffffff')
BLACK = Color('#000000')
GRAY = Color('#d9d9d9')

# Some notes about Tk:
#
# A 'tk.Frame' is a rectangular 'widget' used to organize other widgets.
#
# To add a new widget to the system there are typically two steps:
#  (1) create it and assign its parent:
#    widget = tk.Widget(parent, other_args)
#  (2) 'place' it in its parent in one of three ways:
#    (a) widget.pack() organizes widgets in horizontal and vertical boxes that are limited to left,
#        right, top, bottom positions. Each box is offset and relative to each other.
#    (b) widget.place() places widgets in a two dimensional grid using x and y absolute coordinates.
#    (c) widget.grid() locates widgets in a two dimensional grid using row and column absolute coordinates.


# create a Cell class that derives from tk.Frame
# it will have a button with text
class Cell(tk.Frame):
    # define the "constructor" (aka: ctor) method with some named arguments with default values
    def __init__(self, master=None, text='.', width=PIXELS_PER_CELL_SIDE, height=PIXELS_PER_CELL_SIDE, index=-1):
        # initialize base class
        tk.Frame.__init__(self, master=master, width=width, height=height)

        # configure this frame to not allow resizing
        self.grid_propagate(0)

        # configure this frame to have only one row and one column
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        # declare a 'text' data member for updating the text of the button
        self.text = tk.StringVar()
        self.text.set('.')

        self.index = index

        # create a data member called 'button' with 'self' as parent
        self.button = tk.Button(self, textvariable=self.text, command=self.onClick)

        # color button always white
        self.button.configure(background=WHITE.hex, activebackground=WHITE.hex)

        # tell button to expand to fill this entire frame
        self.button.grid(stick='NWSE')

    def setText(self, text):
        # update self.text variable which will automatically update the self.button's text
        self.text.set(text)

    def onClick(self):
        color_hex = self.button.cget('background')
        if color_hex == WHITE.hex:
            color_hex = BLACK.hex
        else:
            color_hex = WHITE.hex
        self.setColor(color_hex)

        # tell the grid to make the symmetric counterpart cell agree
        self.master.onCellClick(self.index)

    def setColor(self, color_hex):
        self.button.configure(background=color_hex, activebackground=color_hex)

    def getColor(self):
        return self.button.cget('background')

# create a CellGrid class that derives from tk.Frame
# it will have a grid of Cells
class CellGrid(tk.Frame):
    # define the ctor method 
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master)

        # create the member variable 'cells'
        self.cells = []
        for i in range(CELLS_PER_GRID):
            # create a Cell with 'self' as parent
            cell = Cell(self, index=i)

            # set cell's grid in this Frame
            column = int(i % CELLS_PER_GRID_SIDE)
            row = int(i / CELLS_PER_GRID_SIDE)
            cell.grid(row=row, column=column)

            # DEBUG HACK: for now we populate cell with a unique letter of the alphabet
            #t = chr(ord('A') + i)
            #cell.setText(t)
            self.cells.append(cell)

    def onCellClick(self, index):
        color_hex = self.cells[index].getColor()
        column = int(index % CELLS_PER_GRID_SIDE)
        row = int(index / CELLS_PER_GRID_SIDE)

        other_column = CELLS_PER_GRID_SIDE - column - 1
        other_row = CELLS_PER_GRID_SIDE - row - 1

        other_index = other_row * CELLS_PER_GRID_SIDE + other_column

        self.cells[other_index].setColor(color_hex)

# this __name__ == "__main__" check will evaluate True when this script is executed directly
# but False when this script is loaded it as a module
if __name__ == "__main__":
    # a root Tk window would be created for us automatically if we neglected to do so
    # but create it explicitly here
    root_window = tk.Tk()

    # create a CellGrid and pack it into its parent (e.g. root_window)
    cell_grid = CellGrid(root_window)
    cell_grid.pack(side = "left")

    # start handling UI events
    root_window.mainloop()
