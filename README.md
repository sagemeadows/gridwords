# gridwords
Gridwords is a custom crossword puzzle maker that lets you design crossword puzzle grids and put words into the grid, and shows you if no words will fit in any slots.

**TODO:** Use tkinter to open window with possible words for slots in grid; speed up word-search process?

## Download:
`git clone https://github.com/sagemeadows/gridwords` or click on the green 'Code' button in the upper right corner and download ZIP

### Dependencies
`gridwords.py` uses [pygame](https://www.pygame.org/docs/) to create an easy-to-interact with UI. Install pygame with `pip install (--upgrade) pygame`.

## Using Gridwords:
- Enter number of rows and columns for the grid.
- Press CTRL+M to toggle between grid-editing mode and word-filling mode.
    grid-editing mode:
    - Click on boxes to design your crossword puzzle.
    word-filling mode:
    - Click on a box to highlight it.
    - Press a letter key to insert that letter into the highlighted box.
    - Use the arrow keys to move the highlighted box.
    - Scroll up or down to change direction of the highlighted word.
    - Press CTRL+P to see how many words will fit slots in the grid.
- Press ESC or close pygame window to quit.
