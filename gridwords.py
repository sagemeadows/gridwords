#! /usr/bin/python
#
# gridwords.py
#
# Usage:
#     gridwords.py
#
# Create and fill crossword puzzle grids.
#

import logging
import os
import re
import sys
import tkinter as tk
import tkinter.font as tkf

# Import functions from local modules
from handle_files import open_file, save_file
from indices import Entry, updateClueIndices, spreadIndices
from move import moveUp, moveDown, moveLeft, moveRight, select, highlight
from datasearch import getPossWords, allPossWords

LOGGER_FORMAT = "%(filename)s:%(lineno)s %(funcName)s: %(message)s"
#LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG
logging.basicConfig( format=LOGGER_FORMAT, level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)

# Print instructions
instructions = """
Welcome to Gridwords!
"""
print(instructions)

# Define colors with hex codes
WHITE = '#ffffff'
BLACK = '#000000'
GRAY1 = '#f0f0f0'
GRAY2 = '#d9d9d9'
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

# Set temporary/default rows & columns
ROWS = 3
COLUMNS = 3


# Define classes
class Cell(tk.Frame):
    def __init__(self, master=None, text='.', width=CELL_SIDE, height=CELL_SIDE):
        # create and format frame
        tk.Frame.__init__(self, master=master, width=width, height=height, relief=tk.FLAT, bg=BLACK, bd=0)
        self.grid_propagate(0)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        # declare a 'letter' data member for updating the text of the button
        self.letter = tk.StringVar()
        self.letter.set('.')

        self.row = -1
        self.column = -1

        # create a data member called 'button' with 'self' as parent
        self.button = tk.Button(self, textvariable=self.letter, command=self.onClick)
        self.button.bind("<Button-4>", self.onScroll)
        self.button.bind("<Button-5>", self.onScroll)
        self.button.bind("<Button-3>", self.onRightClick)

        # color button always white
        self.button.configure(background=WHITE, activebackground=WHITE, relief=tk.FLAT, bd=0)

        # tell button to expand to fill this entire frame
        self.button.grid(stick='NWSE')

        # add a label for the number in the uppper left corner
        self.clue_index = tk.StringVar()
        self.clue_index.set(str())
        self.clue_label = tk.Label(self, textvariable=self.clue_index)
        self.clue_label.configure(background=WHITE, activebackground=WHITE)
        self.clue_label.place(x=INDEX_MARGIN, y=INDEX_MARGIN)
        self.clue_label.bind('<Button-1>', self.onClick)
        self.clue_label.bind('<Button-3>', self.onRightClick)

        self.across_num = 0
        self.across_pos = -1

        self.down_num = 0
        self.down_pos = -1


    def setText(self, text):
        # update self.text variable which will automatically update the self.button's text
        self.text.set(text)

    def setClueIndex(self, index):
        self.clue_index.set(str(index))

    def onClick(self, args=None):
        logger.debug(f"Clicked Cell: ({self.row}, {self.column})")
        color_hex = self.button['background']
        if self.master.mode == 'grid':
            #color_hex = self.button['background']
            if color_hex == WHITE:
                color_hex = BLACK
            else:
                color_hex = WHITE
            self.setColor(color_hex)

            # tell the grid to make the symmetric counterpart cell agree
            self.master.onCellClick(self.row, self.column)

        elif self.master.mode == 'fill':
            if color_hex != BLACK:
                # select and highlight new working word and letter
                select(self, self.master)
                highlight(self.master)

    def onScroll(self, event):
        if self.master.mode == 'fill':
            color_hex = self.button['background']
            if color_hex != BLACK:
                # change working direc
                if self.master.wdirec == 'across':
                    self.master.wdirec = 'down'
                elif self.master.wdirec == 'down':
                    self.master.wdirec = 'across'

                # click cell
                self.onClick()

    def onRightClick(self, event):
        if self.master.mode == 'fill':
            color_hex = self.button['background']
            if color_hex != BLACK:
                select(self, self.master)
                logger.debug(f"Working cell: ({self.master.wl[0]}, {self.master.wl[1]})")
                getPossWords(self.master)

    def setColor(self, color_hex):
        self.button.configure(background=color_hex, activebackground=color_hex)
        self.clue_label.configure(background=color_hex, activebackground=color_hex)

    def getColor(self):
        return self.button.cget('background')


# Create a CellGrid class that derives from tk.Frame
# it will have a grid of Cells
class CellGrid(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=BLACK, bd=CELL_MARGIN)

        # set mode
        self.mode = 'grid'

        # create cells array
        self.cells = []

        # create entries dict
        self.words = {}

        for row in range(self.master.ROWS):
            self.cells.append([])

            for column in range(self.master.COLUMNS):
                # create a Cell with 'self' as parent
                cell = Cell(self)

                # set cell's grid in this Frame
                cell.grid(row=row, column=column, padx=CELL_MARGIN, pady=CELL_MARGIN)

                self.cells[row].append(cell)
                self.cells[row][column].row = row
                self.cells[row][column].column = column

        # keep track of working letter coordinates
        self.wl = ()
        # keep track of working direction and word
        self.wdirec = 'across'
        self.wword = None

        # bind Shift to changing wdirec
        self.master.bind("<Shift_L>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))
        self.master.bind("<Shift_R>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))

        # bind movement keys
        self.master.bind("<Up>", lambda e: moveUp(e, cellgrid=self))
        self.master.bind("<Down>", lambda e: moveDown(e, cellgrid=self))
        self.master.bind("<Left>", lambda e: moveLeft(e, cellgrid=self))
        self.master.bind("<Right>", lambda e: moveRight(e, cellgrid=self))

        # bind letter keys
        self.master.bind("<Key>", self.master.insertLetter)
        self.master.bind("<BackSpace>", self.master.deleteLetter)

        logger.debug(f"Cells Grid: {self.cells}")


    def onCellClick(self, row, column):
        color_hex = self.cells[row][column].getColor()

        opp_column = 0 - column - 1
        opp_row = 0 - row - 1

        self.cells[opp_row][opp_column].setColor(color_hex)
        self.master.createWIPwords()
        updateClueIndices(self)
        spreadIndices(self)

    def setCellLetter(self, key):
        working_cell = self.cells[self.wl[0]][self.wl[1]]
        #self.cells[self.wl[0]][self.wl[1]].letter.set(key)
        working_cell.letter.set(key)
        # edit words dict
        if working_cell.across_num > 0:
            a_index = f'{working_cell.across_num} across'
            self.words[a_index].letters[working_cell.across_pos] = key
            self.words[a_index].updateWord()
            #self.words[str(working_cell.across_num)][0][1][working_cell.across_pos] = key
        if working_cell.down_num > 0:
            d_index = f'{working_cell.down_num} down'
            self.words[d_index].letters[working_cell.down_pos] = key
            self.words[d_index].updateWord()
            #self.words[str(working_cell.down_num)][0][1][working_cell.down_pos] = key

        for key,entry in self.words.items():
            logger.debug(f"{key}: {entry.word}")


class SideBar(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=20)
        #self.grid(row=1, column=0)

        # create things to go in sidebar
        lbl_rows = tk.Label(self, text="Number of rows:", bg=WHITE)
        lbl_rows.grid(row=0, column=0)
        ent_rows = tk.Entry(self, width=3, highlightcolor=YELLOW)
        ent_rows.grid(row=0, column=1)

        lbl_columns = tk.Label(self, text="Number of columns:", bg=WHITE)
        lbl_columns.grid(row=1, column=0)
        ent_columns = tk.Entry(self, width=3, highlightcolor=YELLOW)
        ent_columns.grid(row=1, column=1)

        btn_mk_grid = tk.Button(self, text="Create Grid", command=lambda : self.master.createGrid(ent_rows, ent_columns))
        btn_mk_grid.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # TODO: Figure out how to open a crossword puzzle file
        #btn_open = tk.Button(sidebar, text="Open", command=open_file)
        #btn_open.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # TODO: Figure out how to save a crossword puzzle file
        #btn_save = tk.Button(sidebar, text="Save As...", command=save_file)
        #btn_save.grid(row=4, column=0, columnspan=2, padx=5)


class TopBar(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=2)

        # create mode buttons
        self.grid_btn = tk.Button(self, text="Edit Grid", bg=GRAY1, command=lambda : self.gridMode(self.master.cellgrid))
        self.fill_btn = tk.Button(self, text="Fill Words", bg=GRAY2, command=lambda : self.fillMode(self.master.cellgrid))
        #self.clue_btn = tk.Button(self, text="Find Clues", bg=GRAY2, command=lambda : self.clueMode(self.master.cellgrid))
        self.grid_btn.grid(row=0, column=0)
        self.fill_btn.grid(row=0, column=1, padx=10)
        #self.clue_btn.grid(row=0, column=2)

        self.search_btn = tk.Button(self, text="Poss Words", bg=GRAY2, command=lambda : allPossWords(self.master.cellgrid))

    def gridMode(self, cellgrid):
        cellgrid.mode = 'grid'
        self.grid_btn['background'] = GRAY1
        self.fill_btn['background'] = GRAY2
        #self.clue_btn['background'] = GRAY2
        self.search_btn.grid_forget()
        cellgrid.wl = ()
        cellgrid.wword = None
        cellgrid.wdirec = 'across'
        # reset non-black colors to white
        for row in range(len(cellgrid.cells)):
            for column in range(len(cellgrid.cells[0])):
                cell = cellgrid.cells[row][column]
                if cell.getColor() != BLACK:
                    cell.setColor(WHITE)

    def fillMode(self, cellgrid):
        cellgrid.mode = 'fill'
        self.grid_btn['background'] = GRAY2
        self.fill_btn['background'] = GRAY1
        #self.clue_btn['background'] = GRAY2
        self.search_btn.grid(row=1, column=1, pady=10)


class WIPwordsFrame(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=2)
        #self.grid(row=2, column=1)

        # establish font for entry buttons
        self.font = tkf.Font(family='Terminal')

        # create across and down word frames
        self.wip_across = tk.Frame(self, relief=tk.FLAT, bd=2, bg=WHITE)
        self.wip_across.grid(row=0, column=0)
        self.wip_down = tk.Frame(self, relief=tk.FLAT, bd=2, bg=WHITE)
        self.wip_down.grid(row=0, column=1)
        
        # create labels
        self.lbl_across = tk.Label(self.wip_across, text="ACROSS", bg=WHITE, bd=2)
        self.lbl_across.pack(side="top")
        self.lbl_down = tk.Label(self.wip_down, text="DOWN", bg=WHITE, bd=2)
        self.lbl_down.pack(side="top")

        logger.debug("New WIP Words")

class RootWindow(tk.Tk):
    # define the ctor method
    def __init__(self):
        # initialize the base class
        tk.Tk.__init__(self)
        self.title("Gridwords")
        self.configure(bg=WHITE)

        # default rows and columsn for grid
        self.ROWS = 3
        self.COLUMNS = 3
        
        # create logo
        self.logo = tk.Label(self, text="LOGO", background=YELLOW) # temporary
        self.logo.grid(row=0, column=0, sticky="nw")

        # create sidebar
        self.sidebar = SideBar(self)
        self.sidebar.grid(row=1, column=0)

        # establish future frames
        self.cellgrid = None
        self.topbar = None
        self.wip_words = None
        
        # establish list of deletable frame names
        self.deletable = ["cellgrid", "topbar", "wip_words"]

        # quick quit
        self.bind("<Escape>", lambda e: self.quit(e))

    def createGrid(self, ent_rows, ent_columns):
        for frame in self.deletable:
            exec(f"if self.{frame}: self.{frame}.destroy()")

        self.ROWS = int(ent_rows.get())
        self.COLUMNS = int(ent_columns.get())

        self.cellgrid = CellGrid(self)
        self.cellgrid.grid(row=1, column=1)

        self.topbar = TopBar(self)
        self.topbar.grid(row=0, column=1)

        self.wip_words = WIPwordsFrame(self)
        self.wip_words.grid(row=2, column=1)

        updateClueIndices(self.cellgrid)
        spreadIndices(self.cellgrid)

    def createWIPwords(self):
        if self.wip_words:
            self.wip_words.destroy()
        
        self.wip_words = WIPwordsFrame(self)
        self.wip_words.grid(row=2, column=1)

    def insertLetter(self, event):
        if self.cellgrid:
            if self.cellgrid.mode == 'fill':
                key = event.char.upper()
                if key and key >= 'A' and key <= 'Z':
                    # set cell letter
                    self.cellgrid.setCellLetter(key)

                    # update WIP words
                    for key,entry in self.cellgrid.words.items():
                        entry.updateWord()

                    # move selected cell
                    if self.cellgrid.wdirec == 'across':
                        moveRight(None, cellgrid=self.cellgrid)
                    elif self.cellgrid.wdirec == 'down':
                        moveDown(None, cellgrid=self.cellgrid)

    def deleteLetter(self, event):
        if self.cellgrid:
            if self.cellgrid.mode == 'fill':
                # set cell letter to '.'
                self.cellgrid.setCellLetter('.')

                # update WIP words
                for key,entry in self.cellgrid.words.items():
                    entry.updateWord()

    def quit(self, event):
        self.destroy()



# this __name__ == "__main__" check will evaluate True when this script is executed directly
# but False when this script is loaded it as a module
if __name__ == "__main__":
    # a root Tk window would be created for us automatically if we neglected to do so
    # but create it explicitly here
    root_window = RootWindow()

    # start handling UI events
    root_window.mainloop()

