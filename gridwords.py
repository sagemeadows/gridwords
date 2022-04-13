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
import string
import tkinter as tk

# Import functions from local modules
from handleFiles import open_file, save_file
from indices import Entry, updateClueIndices, spreadIndices
from move import highlight

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
        
        self.across_num = 0
        self.across_pos = -1
        
        self.down_num = 0
        self.down_pos = -1
        

    def setText(self, text):
        # update self.text variable which will automatically update the self.button's text
        self.text.set(text)

    def setClueIndex(self, index):
        self.clue_index.set(str(index))

    def onClick(self):
        color_hex = self.button['background']
        if mode == 'grid':
            #color_hex = self.button['background']
            if color_hex == WHITE:
                color_hex = BLACK
            else:
                color_hex = WHITE
            self.setColor(color_hex)
            
            # tell the grid to make the symmetric counterpart cell agree
            self.master.onCellClick(self.row, self.column)
        
        elif mode == 'fill':
            if color_hex != BLACK:
                # reset old working word, if it exists
                if self.master.wword:
                    for coord in self.master.wword.coords:
                        self.master.cells[coord[0]][coord[1]].setColor(WHITE)

                # set new working letter
                self.master.wl = (self.row, self.column)
                #print(f"DEBUG\tWorking Cell: {self.master.wl}")
                
                # highlight new working word and letter
                highlight(self.master)
    
    def onScroll(self, event):
        if mode == 'fill':
            color_hex = self.button['background']
            if color_hex != BLACK:
                # change working direc
                if self.master.wdirec == 'across':
                    self.master.wdirec = 'down'
                elif self.master.wdirec == 'down':
                    self.master.wdirec = 'across'
                
                # click cell
                self.onClick()

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
        
        # create cells array
        self.cells = []
        
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
        
        # keep track of working letter coordinates
        self.wl = ()
        # keep track of working direction and word
        self.wdirec = 'across'
        self.wword = None
        
        #print(f"DEBUG\tCells Grid: {self.cells}")


    def onCellClick(self, row, column):
        color_hex = self.cells[row][column].getColor()

        opp_column = 0 - column - 1
        opp_row = 0 - row - 1

        self.cells[opp_row][opp_column].setColor(color_hex)
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
        
        #print(f"DEBUG\tWords: {self.words}")


# Define functions
def buildWindow(root_window):
    # Create gridwords logo in top left corner (TODO)
    logo = tk.Label(root_window, text="LOGO", background=YELLOW) # temporary
    logo.grid(row=0, column=0, sticky="nw")
    
    # Create sidebar
    frm_sidebar = tk.Frame(root_window, relief=tk.FLAT, bd=20, bg=WHITE)
    frm_sidebar.grid(row=1, column=0)
    
    # create things to go in sidebar
    lbl_rows = tk.Label(frm_sidebar, text="Number of rows:", bg=WHITE)
    lbl_rows.grid(row=0, column=0)
    ent_rows = tk.Entry(frm_sidebar, width=3, highlightcolor=YELLOW)
    ent_rows.grid(row=0, column=1)
    
    lbl_columns = tk.Label(frm_sidebar, text="Number of columns:", bg=WHITE)
    lbl_columns.grid(row=1, column=0)
    ent_columns = tk.Entry(frm_sidebar, width=3, highlightcolor=YELLOW)
    ent_columns.grid(row=1, column=1)
    
    btn_mk_grid = tk.Button(frm_sidebar, text="Create Grid", command=lambda : createGrid(root_window, ent_rows, ent_columns))
    btn_mk_grid.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    btn_open = tk.Button(frm_sidebar, text="Open", command=open_file)
    btn_open.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    btn_save = tk.Button(frm_sidebar, text="Save As...", command=save_file)
    btn_save.grid(row=4, column=0, columnspan=2, padx=5)

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
    
    # Create top bar with mode button
    frm_topbar = tk.Frame(root_window, relief=tk.FLAT, bd=2, bg=WHITE)
    frm_topbar.grid(row=0, column=1)
    frames_dict["frm_topbar"] = frm_topbar
    # create mode label
    lbl_mode = tk.Label(frm_topbar, text="You are in Grid-Editing Mode", bd=2, bg=WHITE)
    lbl_mode.grid(row=0, column=0)
    # create mode button
    global mode
    mode = 'grid'
    btn_chmd = tk.Button(frm_topbar, text="Change Mode", command=lambda : changeMode(lbl_mode))
    btn_chmd.grid(row=0, column=1)


def changeMode(lbl_mode):
    global mode
    if mode == 'grid':
        mode = 'fill'
        lbl_mode["text"] = "You are in Word-Filling Mode"
    elif mode == 'fill':
        mode = 'grid'
        lbl_mode["text"] = "You are in Grid-Editing Mode"
        if "cell_grid" in frames_dict:
            cellgrid = frames_dict["cell_grid"]
            # clear working letter, word, and direction
            cellgrid.wl = ()
            cellgrid.wword = None
            cellgrid.wdirec = 'across'
            # reset non-black colors to white
            for row in range(len(cellgrid.cells)):
                for column in range(len(cellgrid.cells[0])):
                    cell = cellgrid.cells[row][column]
                    if cell.getColor() != BLACK:
                        cell.setColor(WHITE)

def insertLetter(event):
    if mode == 'fill':
        key = event.char.upper()
        if key in string.ascii_uppercase: #ascii_letters:
            #print(f"DEBUG\tLetter = {event.char}")
            frames_dict["cell_grid"].setCellLetter(key)

def deleteLetter(event):
    if mode == 'fill':
       frames_dict["cell_grid"].setCellLetter('.') 


def moveUp(event):
    if mode == 'fill':
        cellgrid = frames_dict["cell_grid"]
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row != 0 and cellgrid.cells[row-1][column].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row-1, column)
            
            # highlight new working word and letter
            highlight(cellgrid)

def moveDown(event):
    if mode == 'fill':
        cellgrid = frames_dict["cell_grid"]
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if row != range(ROWS)[-1] and cellgrid.cells[row+1][column].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row+1, column)
            
            # highlight new working word and letter
            highlight(cellgrid)

def moveLeft(event):
    if mode == 'fill':
        cellgrid = frames_dict["cell_grid"]
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column != 0 and cellgrid.cells[row][column-1].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row, column-1)
            
            # highlight new working word and letter
            highlight(cellgrid)

def moveRight(event):
    if mode == 'fill':
        cellgrid = frames_dict["cell_grid"]
        row = cellgrid.wl[0]
        column = cellgrid.wl[1]
        if column != range(COLUMNS)[-1] and cellgrid.cells[row][column+1].getColor() != BLACK:
            # reset old working word, if it exists
            if cellgrid.wword:
                for coord in cellgrid.wword.coords:
                    cellgrid.cells[coord[0]][coord[1]].setColor(WHITE)
            
            # set new working letter
            cellgrid.wl = (row, column+1)
            
            # highlight new working word and letter
            highlight(cellgrid)

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
    
    # initial mode
    mode = 'grid'

    buildWindow(root_window)
    
    # bind keypresses
    root_window.bind("<Key>", insertLetter)
    root_window.bind("<BackSpace>", deleteLetter)
    root_window.bind("<Up>", moveUp)
    root_window.bind("<Down>", moveDown)
    root_window.bind("<Left>", moveLeft)
    root_window.bind("<Right>", moveRight)
    root_window.bind("<Escape>", lambda e: quit(e))
    
    # start handling UI events
    root_window.mainloop()

