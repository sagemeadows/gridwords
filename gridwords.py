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
from handle_files import SaveWindow, open_file, save_file
from indices import Entry, updateClueIndices, spreadIndices
from move import moveUp, moveDown, moveLeft, moveRight, select, highlight
from datasearch import getPossWords, allPossWords, getPossClues

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


# Create a Cell class
# Cells go into an array in the Cellgrid class
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


    def setClueIndex(self, index):
        self.clue_index.set(str(index))

    def onClick(self, args=None):
        logger.debug(f"Clicked Cell: ({self.row}, {self.column}, '{self.letter.get()}')")
        color_hex = self.button['background']
        if self.master.mode == 'grid':
            #color_hex = self.button['background']
            if color_hex == WHITE:
                color_hex = BLACK
                self.letter.set('#')
            else:
                color_hex = WHITE
                self.letter.set('.')
            logger.debug(f"Clicked Cell New Letter: '{self.letter.get()}'")
            self.setColor(color_hex)

            # tell the grid to make the symmetric counterpart cell agree
            self.master.onCellClick(self.row, self.column)

        #elif self.master.mode == 'fill':
        else:
            if color_hex != BLACK:
                # select and highlight new working word and letter
                select(self, self.master)
                highlight(self.master)

    def onScroll(self, event):
        if self.master.mode != 'grid':
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
        color_hex = self.button['background']
        if color_hex != BLACK:
            if self.master.mode != 'grid':
                select(self, self.master)
                logger.debug(f"Working cell: ({self.master.wl[0]}, {self.master.wl[1]})")
            if self.master.mode == 'fill':
                getPossWords(self.master)
            elif self.master.mode == 'clue':
                getPossClues(self.master.wword)

    def setChar(self):
        # update default char for new color assignment
        color_hex = self.button['background']
        if color_hex == BLACK:
            self.letter.set('#')
        else:
            self.letter.set('.')

    def setColor(self, color_hex):
        self.button.configure(background=color_hex, activebackground=color_hex)
        self.clue_label.configure(background=color_hex, activebackground=color_hex)

    def getColor(self):
        return self.button.cget('background')


# Create a CellGrid class that derives from tk.Frame
# it will have a grid of Cells
class CellGrid(tk.Frame):
    # define the ctor method
    def __init__(self, master=None, title=None, author=None, descrip=None, rows=None, columns=None, grid=None, clues=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=BLACK, bd=CELL_MARGIN)

        # puzzle info
        self.title = title
        self.author = author
        self.descrip = descrip

        # set mode
        self.mode = 'grid'

        # create cells array
        self.cells = []

        # create entries dict
        self.words = {}

        if grid: # creating a grid from an opened & parsed file
            for row in range(rows):
                self.cells.append([])

                for column in range(columns):
                    # get character from parsed grid
                    char = grid[row][column]
                    cell = Cell(self)
                    if char == '#':
                        cell.setColor(BLACK)
                    cell.letter.set(char)

                    self.cells[row].append(cell)
                    self.cells[row][column].row = row
                    self.cells[row][column].column = column

                    # set cell's grid in this Frame
                    cell.grid(row=row, column=column, padx=CELL_MARGIN, pady=CELL_MARGIN)

        else: # creating a new grid
            for row in range(rows):
                self.cells.append([])

                for column in range(columns):
                    # create a Cell with 'self' as parent
                    cell = Cell(self)

                    self.cells[row].append(cell)
                    self.cells[row][column].row = row
                    self.cells[row][column].column = column

                    # set cell's grid in this Frame
                    cell.grid(row=row, column=column, padx=CELL_MARGIN, pady=CELL_MARGIN)

        # create WIP entries frame
        self.master.wip_words = WIPwordsFrame(self.master)

        # fill entries dict
        updateClueIndices(self)
        spreadIndices(self)

        # match clues, if present, to entries
        if clues:
            for clue_entry in clues:
                key = f'{clue_entry[0]} {clue_entry[1]}'
                if key in self.words:
                    self.words[key].clue.set(clue_entry[2])

        # keep track of working letter coordinates
        self.wl = ()
        # keep track of working direction and word
        self.wdirec = 'across'
        self.wword = None

        # establish shortcut to root window
        self.root_window = self.master.master.master.master

        # bind Shift to changing wdirec
        self.root_window.bind("<Shift_L>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))
        self.root_window.bind("<Shift_R>", lambda e: self.cells[self.wl[0]][self.wl[1]].onScroll(e))

        # bind movement keys
        self.root_window.bind("<Up>", lambda e: moveUp(e, cellgrid=self))
        self.root_window.bind("<Down>", lambda e: moveDown(e, cellgrid=self))
        self.root_window.bind("<Left>", lambda e: moveLeft(e, cellgrid=self))
        self.root_window.bind("<Right>", lambda e: moveRight(e, cellgrid=self))

        # bind letter keys
        self.root_window.bind("<Key>", self.master.insertLetter)
        self.root_window.bind("<BackSpace>", self.master.backspaceLetter)
        self.root_window.bind("<Delete>", self.master.deleteLetter)

        # title root window after puzzle title
        self.root_window.title(f'{self.title} - Gridwords')

        # put grid and wip_words into main frame (master)
        self.grid(row=1, column=1)
        self.master.wip_words.grid(row=2, column=1)


    def onCellClick(self, row, column):
        color_hex = self.cells[row][column].getColor()

        opp_column = 0 - column - 1
        opp_row = 0 - row - 1

        self.cells[opp_row][opp_column].setColor(color_hex)
        self.cells[opp_row][opp_column].setChar()
        self.master.createWIPwords()
        updateClueIndices(self)
        spreadIndices(self)

    def setCellLetter(self, key):
        working_cell = self.cells[self.wl[0]][self.wl[1]]
        working_cell.letter.set(key)
        # edit words dict
        if working_cell.across_num > 0:
            a_index = f'{working_cell.across_num} across'
            self.words[a_index].letters[working_cell.across_pos] = key
            self.words[a_index].updateWord()
        if working_cell.down_num > 0:
            d_index = f'{working_cell.down_num} down'
            self.words[d_index].letters[working_cell.down_pos] = key
            self.words[d_index].updateWord()

        for key,entry in self.words.items():
            logger.debug(f"{key}: {entry.word}")


# Create a SideBar class for making, saving, and opening grids
class SideBar(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=20)

        # create things to go in sidebar
        self.lbl_rows = tk.Label(self, text="Number of rows:", bg=WHITE)
        self.lbl_rows.grid(row=0, column=0)
        self.ent_rows = tk.Entry(self, width=3, highlightcolor=YELLOW)
        self.ent_rows.grid(row=0, column=1)

        self.lbl_columns = tk.Label(self, text="Number of columns:", bg=WHITE)
        self.lbl_columns.grid(row=1, column=0)
        self.ent_columns = tk.Entry(self, width=3, highlightcolor=YELLOW)
        self.ent_columns.grid(row=1, column=1)

        self.btn_mk_grid = tk.Button(self, text="Create Grid", command=lambda : self.master.createGrid(rows=None, columns=None))
        self.btn_mk_grid.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # open a crossword puzzle file
        self.btn_open = tk.Button(self, text="Open...", command=lambda : open_file(self.master))
        self.btn_open.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # save crossword puzzle
        self.btn_save = tk.Button(self, text="Save As...", command=self.openSaveWindow)
        self.btn_save.grid(row=4, column=0, columnspan=2, padx=5)

    def openSaveWindow(self):
        save_window = SaveWindow(main_frame=self.master)
        save_window.mainloop()


# Create a TopBar class for changing between puzzle-crafting modes
class TopBar(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=2)

        # create mode buttons
        self.grid_btn = tk.Button(self, text="Edit Grid", bg=CYAN, activebackground=CYAN,\
                                        command=lambda : self.gridMode(self.master.cellgrid))
        self.fill_btn = tk.Button(self, text="Fill Words", bg=GRAY2, activebackground=CYAN,\
                                        command=lambda : self.fillMode(self.master.cellgrid))
        self.clue_btn = tk.Button(self, text="Find Clues", bg=GRAY2, activebackground=CYAN,\
                                        command=lambda : self.clueMode(self.master.cellgrid))
        self.grid_btn.grid(row=0, column=0)
        self.fill_btn.grid(row=0, column=1, padx=10, pady=10)
        self.clue_btn.grid(row=0, column=2)

        self.search_btn = tk.Button(self, text="Poss Words", bg=GRAY2, activebackground=CYAN,\
                                          command=lambda : allPossWords(self.master.cellgrid))

        # put topbar in main frame (master)
        self.grid(row=0, column=1)

    def gridMode(self, cellgrid):
        cellgrid.mode = 'grid'
        self.grid_btn['background'] = CYAN
        self.fill_btn['background'] = GRAY2
        self.clue_btn['background'] = GRAY2
        self.search_btn.grid_forget()
        self.reset(cellgrid)

    def fillMode(self, cellgrid):
        cellgrid.mode = 'fill'
        self.grid_btn['background'] = GRAY2
        self.fill_btn['background'] = CYAN
        self.clue_btn['background'] = GRAY2
        self.search_btn.grid(row=1, column=1, pady=10)

    def clueMode(self, cellgrid):
        cellgrid.mode = 'clue'
        self.grid_btn['background'] = GRAY2
        self.fill_btn['background'] = GRAY2
        self.clue_btn['background'] = CYAN
        self.search_btn.grid_forget()
        #self.reset(cellgrid)
        #allPossWords(cellgrid)

    def reset(self, cellgrid):
        cellgrid.wl = ()
        cellgrid.wword = None
        cellgrid.wdirec = 'across'
        # reset non-black colors to white
        for row in range(len(cellgrid.cells)):
            for column in range(len(cellgrid.cells[0])):
                cell = cellgrid.cells[row][column]
                if cell.getColor() != BLACK:
                    cell.setColor(WHITE)


# Create a frame for words and clues of puzzle entries
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
        self.wip_across.grid(row=0, column=0, sticky="nw")
        self.wip_down = tk.Frame(self, relief=tk.FLAT, bd=2, bg=WHITE)
        self.wip_down.grid(row=0, column=1, sticky="nw")
        
        # create labels
        self.lbl_across = tk.Label(self.wip_across, text="ACROSS", pady=7, bg=WHITE, bd=2)
        self.lbl_across.grid(row=0, column=0, columnspan=2, sticky="nw")
        self.lbl_down = tk.Label(self.wip_down, text="DOWN", pady=7, bg=WHITE, bd=2)
        self.lbl_down.grid(row=0, column=0, columnspan=2, sticky="nw")

        logger.debug("New WIP Words")


# Create a RootWindow class which inclues a scrollable frame
class RootWindow(tk.Tk):
    # define the ctor method
    def __init__(self):
        # initialize the base class
        tk.Tk.__init__(self)
        self.title("Gridwords")
        self.configure(bg=WHITE)

        ## establish maximum window size as fullscreen
        #self.width= self.winfo_screenwidth()
        #self.height= self.winfo_screenheight()
        #self.maxsize(self.width, self.height)

        # add frame and canvas for future scrollable frame
        self.root_frame = tk.Frame(self, bg=WHITE, bd=0)
        self.root_frame.pack(fill="both", expand=True)#grid(row=0, column=0, sticky="nesw")
        self.canvas = tk.Canvas(self.root_frame, bg=WHITE)
        
        # create scrollbars
        self.scrollbar_y = tk.Scrollbar(self.root_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        # create main scrollable frame to hold all other frames
        self.main_frame = MainFrame(self.canvas)
        #self.main_frame.pack()

        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")


        # quick quit
        self.bind("<Escape>", lambda e: self.quit(e))

    def quit(self, event):
        self.destroy()


# Create a frame, which becomes scrollable within the RootWindow,
# that holds all the other frames
class MainFrame(tk.Frame):
    # define the ctor method
    def __init__(self, master=None):
        # initialize the base class
        tk.Frame.__init__(self, master, bg=WHITE, bd=2)

        ## default rows and columns for grid
        #self.ROWS = 3
        #self.COLUMNS = 3
        
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


    def createGrid(self, rows=None, columns=None, title="Untitled Puzzle", 
                         author="", descrip="", grid=None, clues=None):
        for frame in self.deletable:
            exec(f"if self.{frame}: self.{frame}.destroy()")

        if not rows:
            rows = int(self.sidebar.ent_rows.get())
        if not columns:
            columns = int(self.sidebar.ent_columns.get())

        self.cellgrid = CellGrid(master=self, rows=rows, columns=columns, title=title, 
                                       author=author, descrip=descrip, grid=grid, clues=clues)

        self.topbar = TopBar(self)

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

    def backspaceLetter(self, event):
        if self.cellgrid:
            if self.cellgrid.mode == 'fill':
                # set cell letter to '.'
                self.cellgrid.setCellLetter('.')

                # update WIP words
                for key,entry in self.cellgrid.words.items():
                    entry.updateWord()

                # move selected cell
                if self.cellgrid.wdirec == 'across':
                    moveLeft(None, cellgrid=self.cellgrid)
                elif self.cellgrid.wdirec == 'down':
                    moveUp(None, cellgrid=self.cellgrid)

    def deleteLetter(self, event):
        if self.cellgrid:
            if self.cellgrid.mode == 'fill':
                # set cell letter to '.'
                self.cellgrid.setCellLetter('.')

                # update WIP words
                for key,entry in self.cellgrid.words.items():
                    entry.updateWord()



# this __name__ == "__main__" check will evaluate True when this script is executed directly
# but False when this script is loaded it as a module
if __name__ == "__main__":
    # a root Tk window would be created for us automatically if we neglected to do so
    # but create it explicitly here
    root_window = RootWindow()

    # start handling UI events
    root_window.mainloop()

