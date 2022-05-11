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
                ## reset old working word, if it exists
                #if self.master.wword:
                #    for coord in self.master.wword.coords:
                #        self.master.cells[coord[0]][coord[1]].setColor(WHITE)

                ## set new working letter
                #self.master.wl = (self.row, self.column)
                logger.debug(f"Working Cell: {self.master.wl}")

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

                #entry = self.master.

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
        global frames_dict
        frames_dict["cell_grid"] = self

        # set mode
        self.mode = 'grid'

        # create cells array
        self.cells = []

        # create entries dict
        self.words = {}

        for row in range(ROWS):
            self.cells.append([])

            for column in range(COLUMNS):
                # create a Cell with 'self' as parent
                cell = Cell(self)

                # set cell's grid in this Frame
                cell.grid(row=row, column=column, padx=CELL_MARGIN, pady=CELL_MARGIN)

                self.cells[row].append(cell)
                self.cells[row][column].row = row
                self.cells[row][column].column = column


        updateClueIndices(self)
        spreadIndices(self)
        createWIPwords(self.master)

        # keep track of working letter coordinates
        self.wl = ()
        # keep track of working direction and word
        self.wdirec = 'across'
        self.wword = None

        # bind Shift to changing wdirec
        self.master.bind("<Shift_L>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))
        self.master.bind("<Shift_R>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))

        logger.debug(f"Cells Grid: {self.cells}")


    def onCellClick(self, row, column):
        color_hex = self.cells[row][column].getColor()

        opp_column = 0 - column - 1
        opp_row = 0 - row - 1

        self.cells[opp_row][opp_column].setColor(color_hex)
        updateClueIndices(self)
        spreadIndices(self)
        createWIPwords(self.master)

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

        logger.debug(f"Words: {self.words}")


class Topbar(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=2)
        global frames_dict
        frames_dict["topbar"] = self

        # create mode buttons
        self.grid_btn = tk.Button(self, text="Edit Grid", bg=GRAY1, command=lambda : self.gridMode(frames_dict["cell_grid"]))
        self.fill_btn = tk.Button(self, text="Fill Words", bg=GRAY2, command=lambda : self.fillMode(frames_dict["cell_grid"]))
        #self.clue_btn = tk.Button(self, text="Find Clues", bg=GRAY2, command=lambda : self.clueMode(frames_dict["cell_grid"]))
        self.grid_btn.grid(row=0, column=0)
        self.fill_btn.grid(row=0, column=1, padx=10)
        #self.clue_btn.grid(row=0, column=2)

        self.search_btn = tk.Button(self, text="Poss Words", bg=GRAY2, command=lambda : allPossWords(frames_dict["cell_grid"]))

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


# Define functions
def buildWindow(root_window):
    # Create gridwords logo in top left corner (TODO)
    logo = tk.Label(root_window, text="LOGO", background=YELLOW) # temporary
    logo.grid(row=0, column=0, sticky="nw")

    # Create sidebar
    sidebar = tk.Frame(root_window, relief=tk.FLAT, bd=20, bg=WHITE)
    sidebar.grid(row=1, column=0)

    # create things to go in sidebar
    lbl_rows = tk.Label(sidebar, text="Number of rows:", bg=WHITE)
    lbl_rows.grid(row=0, column=0)
    ent_rows = tk.Entry(sidebar, width=3, highlightcolor=YELLOW)
    ent_rows.grid(row=0, column=1)

    lbl_columns = tk.Label(sidebar, text="Number of columns:", bg=WHITE)
    lbl_columns.grid(row=1, column=0)
    ent_columns = tk.Entry(sidebar, width=3, highlightcolor=YELLOW)
    ent_columns.grid(row=1, column=1)

    btn_mk_grid = tk.Button(sidebar, text="Create Grid", command=lambda : createGrid(root_window, ent_rows, ent_columns))
    btn_mk_grid.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # TODO: Figure out how to open a crossword puzzle file
    #btn_open = tk.Button(sidebar, text="Open", command=open_file)
    #btn_open.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # TODO: Figure out how to save a crossword puzzle file
    #btn_save = tk.Button(sidebar, text="Save As...", command=save_file)
    #btn_save.grid(row=4, column=0, columnspan=2, padx=5)

def createGrid(root_window, ent_rows, ent_columns):
    # Clear old grid and related frames
    for key,frame in frames_dict.items():
        frame.destroy()

    # Create grid
    global ROWS
    global COLUMNS
    ROWS = int(ent_rows.get())
    COLUMNS = int(ent_columns.get())
    cell_grid = CellGrid(root_window)
    cell_grid.grid(row=1, column=1)
    frames_dict["cell_grid"] = cell_grid
    root_window.bind("<Up>", lambda e: moveUp(e, cellgrid=frames_dict["cell_grid"]))
    root_window.bind("<Down>", lambda e: moveDown(e, cellgrid=frames_dict["cell_grid"]))
    root_window.bind("<Left>", lambda e: moveLeft(e, cellgrid=frames_dict["cell_grid"]))
    root_window.bind("<Right>", lambda e: moveRight(e, cellgrid=frames_dict["cell_grid"]))

    # Create top bar with mode button
    topbar = Topbar(root_window)
    topbar.grid(row=0, column=1)
    frames_dict["topbar"] = topbar
    topbar_dict = {}

    # Create frame for WIP words
    createWIPwords(root_window)

    # remove focus from end_rows/_columns by setting it on root_window
    root_window.focus_set()

def createWIPwords(root_window):
    global frames_dict
    for key,frame in frames_dict.items():
        if key == "wip_words":
            frame.destroy()

    wip_words = tk.Frame(root_window, relief=tk.FLAT, bd=2, bg=WHITE)
    wip_words.grid(row=2, column=1)
    frames_dict["wip_words"] = wip_words
    # create across and down word frames
    wip_across = tk.Frame(wip_words, relief=tk.FLAT, bd=2, bg=WHITE)
    wip_across.grid(row=0, column=0)
    wip_down = tk.Frame(wip_words, relief=tk.FLAT, bd=2, bg=WHITE)
    wip_down.grid(row=0, column=1)
    # create labels
    lbl_across = tk.Label(wip_across, text="ACROSS", bg=WHITE, bd=2)
    lbl_across.pack(side="top")
    lbl_down = tk.Label(wip_down, text="DOWN", bg=WHITE, bd=2)
    lbl_down.pack(side="top")
    # fill in wip words
    wip_words_dict = frames_dict["cell_grid"].words
    for key,entry in wip_words_dict.items():
        word = tk.StringVar()
        word.set(entry.word)
        #word.set(f'{entry.index}. {entry.word}')

        if entry.direc == 'across':
            frm = tk.Frame(wip_across, relief=tk.FLAT, bd=2, bg=WHITE)
        elif entry.direc == 'down':
            frm = tk.Frame(wip_down, relief=tk.FLAT, bd=2, bg=WHITE)

        lbl = tk.Label(frm, text=f'{entry.index}. ', bd=2, bg=WHITE)
        lbl.grid(row=0, column=0)
        btn = tk.Button(frm, bd=2, textvariable=word)#, command=)
        btn.grid(row=0, column=1)
        frm.pack(side="top")


def insertLetter(event):
    if "cell_grid" in frames_dict:
        cellgrid = frames_dict["cell_grid"]
        if cellgrid.mode == 'fill':
            key = event.char.upper()
            if key and key >= 'A' and key <= 'Z':
                cellgrid.setCellLetter(key)
                createWIPwords(root_window)
                if cellgrid.wdirec == 'across':
                    moveRight(None, cellgrid=cellgrid)
                elif cellgrid.wdirec == 'down':
                    moveDown(None, cellgrid=cellgrid)

def deleteLetter(event):
    if "cell_grid" in frames_dict:
        if frames_dict["cell_grid"].mode == 'fill':
            frames_dict["cell_grid"].setCellLetter('.')
            createWIPwords(root_window)

def quit(event):
    root_window.destroy()

# this __name__ == "__main__" check will evaluate True when this script is executed directly
# but False when this script is loaded it as a module
if __name__ == "__main__":
    # a root Tk window would be created for us automatically if we neglected to do so
    # but create it explicitly here
    root_window = tk.Tk()
    root_window.title("Gridwords")
    root_window.configure(bg=WHITE)

    # create dictionary to keep track of frames
    # that may later need to be updated
    # (via deletion and recreation)
    frames_dict = {}

    buildWindow(root_window)

    # bind keypresses
    root_window.bind("<Key>", insertLetter)
    root_window.bind("<BackSpace>", deleteLetter)
    root_window.bind("<Escape>", lambda e: quit(e))

    # start handling UI events
    root_window.mainloop()

