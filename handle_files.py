#! /usr/bin/python
#
# handle_files.py
#
# Usage:
#     module for gridwords.py
#
# Open, save, and export files (WIP).
#

import logging
import sys
import os
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

LOGGER_FORMAT = "%(filename)s:%(lineno)s %(funcName)s: %(message)s"
#LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG
logging.basicConfig( format=LOGGER_FORMAT, level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)

WHITE = '#ffffff'
BLACK = '#000000'

# HTML file head templates
html1 = """
<html>
<head>
<style>
.grid-container {
  display: inline-grid;
  row-gap: 2px;
  column-gap: 2px;"""

html2 = """
  background-color: #000000;
  padding: 2px;
}

.grid-item {
  background-color: #ffffff;
  border: 0px solid #000000;
  width: 40px;
  height: 40px;
  padding: 2px
}

.clues-grid {
  display: inline-grid;
  row-gap: 10px;
  column-gap: 10px;
  grid-template-columns: auto auto;
  background-color: #ffffff;
  padding: 10px;
}

.clues-direc {
  background-color: #ffffff;
  border: 0px solid #000000;
  padding: 5px
}

index {
  vertical-align: baseline;
  font-size: 0.75em;
  font-family: arial
}

letter {
  vertical-align: super;
  font-size: 1em;
  font-family: arial
}
</style>
</head>
<body>
"""

# Pop-up window for puzzle info
class SaveWindow(tk.Tk):
    # define the ctor method
    def __init__(self, main_frame=None):
        # initialize the base class
        tk.Tk.__init__(self)
        self.title("Save Grid")
        self.configure(bg=WHITE)

        # establish main_frame
        self.main_frame = main_frame

        # add frame and canvas for future scrollable frame
        self.root_frame = tk.Frame(self, bg=WHITE, bd=2)
        self.root_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.root_frame, bg=WHITE)
        
        # create scrollbars
        self.scrollbar_y = tk.Scrollbar(self.root_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        # create main scrollable frame to hold all other frames
        self.scrollable_frame = tk.Frame(self.canvas, bg=WHITE, bd=2)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")


        # fill window with fields to fill in
        self.lbl_title = tk.Label(self.scrollable_frame, text="Title:", bg=WHITE)
        self.lbl_title.grid(row=0, column=0, columnspan=2)
        self.ent_title = tk.Entry(self.scrollable_frame, width=40)
        self.ent_title.grid(row=1, column=0, columnspan=2, pady=5, ipady=3, ipadx=3)
        self.ent_title.insert(0, self.main_frame.cellgrid.title)

        self.lbl_author = tk.Label(self.scrollable_frame, text="Author:", bg=WHITE)
        self.lbl_author.grid(row=2, column=0, columnspan=2)
        self.ent_author = tk.Entry(self.scrollable_frame, width=40)
        self.ent_author.grid(row=3, column=0, columnspan=2, pady=5, ipady=3, ipadx=3)
        if self.main_frame.cellgrid.author:
            self.ent_author.insert(0, self.main_frame.cellgrid.author)
        
        self.lbl_descrip = tk.Label(self.scrollable_frame, text="Puzzle description:", bg=WHITE)
        self.lbl_descrip.grid(row=4, column=0, columnspan=2)
        self.ent_descrip = tk.Entry(self.scrollable_frame, width=40)
        self.ent_descrip.grid(row=5, column=0, columnspan=2, pady=5, ipady=3, ipadx=3)
        if self.main_frame.cellgrid.descrip:
            self.ent_descrip.insert(0, self.main_frame.cellgrid.descrip)

        self.btn_save = tk.Button(self.scrollable_frame, text="Save Grid", command=self.getGridInfo)
        self.btn_save.grid(row=6, column=0, pady=10)
        self.btn_cancel = tk.Button(self.scrollable_frame, text="Cancel", command=self.destroy)
        self.btn_cancel.grid(row=6, column=1, pady=10)

        # quick quit
        self.bind("<Escape>", lambda e: self.quit(e))

    def getGridInfo(self):#window, title=None, author=None, descrip=None):
        """Get puzzle title, author, and description info and save file."""
        t = self.ent_title.get()
        if not t:
            t = "Untitled Puzzle"
        self.main_frame.cellgrid.title = t

        a = self.ent_author.get()
        self.main_frame.cellgrid.author = a

        d = self.ent_descrip.get()
        self.main_frame.cellgrid.descrip = d

        # save file
        save_file(self.main_frame)

        # close pop-up window
        self.destroy()

    def quit(self, event):
        save_file(self.main_frame)
        self.destroy()


# Open and parse .txt files
# to reload puzzle grid
def open_file(main_frame):
    """Open a puzzle for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )
    if not filepath:
        return
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        line = input_file.readline().rstrip('\n')
        if line != '<GRIDWORDS PUZZLE>':
            logger.debug(f"{filepath} not a suitable format for opening")
            return
        else: # Parse file
            line = input_file.readline() # '<TITLE>'
            title = input_file.readline().strip(' \n')
            line = input_file.readline() # '<AUTHOR>'
            author = input_file.readline().strip(' \n')
            line = input_file.readline() # '<DESCRIPTION>'
            descrip = input_file.readline().strip(' \n')
            line = input_file.readline() # '<SIZE>'
            size = input_file.readline().split('x')
            rows = int(size[0])
            columns = int(size[1])
            line = input_file.readline() # '<GRID>'
            grid = []
            line = input_file.readline()
            while line.startswith(' '):
                gridline = line.strip(' \n')
                letters = list(gridline)
                grid.append(letters)
                line = input_file.readline()
            clues = []
            line = input_file.readline()
            while line.startswith(' '):
                if not line:
                    break
                clueline = line.strip(' \n')
                key,clue = clueline.split(',')[0], clueline.split(',')[1]
                index,direc = int(key.split()[0]), key.split()[1]
                clue_entry = (index, direc, clue)
                clues.append(clue_entry)
                line = input_file.readline()

            # Create cellgrid using parsed info
            main_frame.createGrid(rows=rows, columns=columns, title=title, 
                                  author=author, descrip=descrip, grid=grid, clues=clues)
        
    logger.debug(f"Opened puzzle file {filepath}")


# Convert puzzle to reloadable .txt file
# or to printable .html file
def save_file(main_frame):#, rows, columns, title=main_frame.cellgrid., author="Unknown", descrip=None):
    """Save current puzzle as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html")]
    )
    if not filepath:
        return

    # get puzzle info
    title = main_frame.cellgrid.title
    author = main_frame.cellgrid.author
    descrip = main_frame.cellgrid.descrip
    rows = len(main_frame.cellgrid.cells)
    columns = len(main_frame.cellgrid.cells[0])

    # write file
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        # write .txt files for opening and editing puzzles
        if ".txt" in filepath:
            output_file.write('<GRIDWORDS PUZZLE>\n')
            output_file.write('<TITLE>\n')
            output_file.write(f'  {title}\n')

            output_file.write('<AUTHOR>\n')
            if author:
                output_file.write(f'  {author}\n')
            else:
                output_file.write(f'  Unknown\n')

            output_file.write('<DESCRIPTION>\n')
            if descrip:
                output_file.write(f'  {descrip}\n')
            else:
                output_file.write(f'  None\n')

            output_file.write('<SIZE>\n')
            output_file.write(f'  {rows}x{columns}\n')

            output_file.write('<GRID>\n')
            for row in range(rows):
                line = ""
                for column in range(columns):
                    line = line + main_frame.cellgrid.cells[row][column].letter.get()
                output_file.write(f'  {line}\n')
            output_file.write('<CLUES>\n')
            for key,entry in main_frame.cellgrid.words.items():
                output_file.write(f'  {key},{entry.clue.get()}\n')

        # write .html files for printing puzzle + solution
        # (on separate pages, once converted to pdf)
        elif ".html" in filepath:
            # write puzzle info and html style
            output_file.write('<!DOCTYPE html>\n\n')
            output_file.write(f'<!--{rows}x{columns}-->\n')
            html_columns = columns * 'auto '
            output_file.write(html1)
            output_file.write(f'  grid-template-columns: {html_columns};')
            output_file.write(html2 + '\n')

            # write title
            output_file.write(f'<h1>{title}</h1>\n\n')

            # write author if present;
            # write comment if not
            if author:
                output_file.write(f'<h3>By {author}</h3>\n\n')
            else:
                output_file.write('<!--Unknown author-->\n\n')

            # write description if present;
            # write comment if not
            if descrip:
                output_file.write(f'<p>{descrip}</p>\n\n')
            else:
                output_file.write('<!--No descriptions-->\n\n')
            
            # write fill-in-able puzzle grid
            output_file.write('<div class="grid-container">\n')
            for row in range(rows):
                for column in range(columns):
                    cell = main_frame.cellgrid.cells[row][column]
                    if cell.button['background'] == BLACK:
                        output_file.write('  <div class="grid-item" style="background-color:#000000"></div>\n')
                    else:
                        output_file.write(f'  <div class="grid-item"><index>{cell.clue_index.get()}</index></div>\n')
            output_file.write('</div>\n\n')
            output_file.write('<br>\n\n')

            # write clues
            output_file.write('<div class="clues-grid">\n')
            clues_acr = []
            clues_dwn = []
            for key,entry in main_frame.cellgrid.words.items():
                if entry.direc == 'across':
                    clues_acr.append(f'{entry.index}. {entry.clue.get()}')
                elif entry.direc == 'down':
                    clues_dwn.append(f'{entry.index}. {entry.clue.get()}')
            output_file.write('  <div class="clues-direc"><b>Across</b><br>\n')
            for clue in clues_acr:
                output_file.write(f'    {clue}<br>\n')
            output_file.write('  </div>\n')
            output_file.write('  <div class="clues-direc"><b>Down</b><br>\n')
            for clue in clues_dwn:
                output_file.write(f'    {clue}<br>\n')
            output_file.write('  </div>\n')
            output_file.write('</div>\n\n')

            # create page break for printable pdf
            output_file.write('<p style="page-break-after: always;">&nbsp;</p>\n')
            output_file.write('<p style="page-break-before: always;">&nbsp;</p>\n\n')

            # write solved puzzle grid
            output_file.write(f'<h1>{title} Solution</h1>\n\n')
            output_file.write('<div class="grid-container">\n')
            for row in range(len(main_frame.cellgrid.cells)):
                for column in range(len(main_frame.cellgrid.cells[0])):
                    cell = main_frame.cellgrid.cells[row][column]
                    if cell.button['background'] == BLACK:
                        output_file.write('  <div class="grid-item" style="background-color:#000000"></div>\n')
                    else:
                        output_file.write(f'  <div class="grid-item"><index>{cell.clue_index.get()}</index><br>' +
                                          f'<center><letter>{cell.letter.get()}</letter></center></div>\n')
            output_file.write('</div>\n\n')

            # end html file
            output_file.write('</body>\n')
            output_file.write('</html>\n')

    logger.debug(f"Saved puzzle to {filepath}")
    main_frame.master.master.master.title(f'{title} - Gridwords')

