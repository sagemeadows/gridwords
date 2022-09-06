# gridwords
Gridwords is a custom crossword puzzle maker that lets you design crossword puzzle grids, put words into the grid, and select clues for the words. You can also add new words and new clues to the database, save your progress, and create printable versions of your puzzle.

## Download
`git clone https://github.com/sagemeadows/gridwords` or click on the green 'Code' button in the upper right corner and download ZIP

## Use
- Open gridwords with `python3 gridwords.py`
- In **Grid-Editing Mode**, click on boxes to design puzzle
- In **Word-Filling Mode**:
  - Click on a box to select it, press a letter to fill it in
  - Use arrow keys to move the selected box
  - Press `Shift` of scroll over a box to change the direction of the selected word
  - Right click on a box to see the number of possible words in the database that can fill the selected word
- In **Clue-Filling Mode**:
  - Click on a box to select it
  - Use arrow keys to move the selected box
  - Press `Shift` or scroll over a box to change the direction of the selected word
  - Right click on a box to see the possible clues for the selected word
- Click 'Save As...' button to save puzzle
- Press `ESC` or close the window to quit

### Saving Files
#### TEXT
**.txt** files are for saving your WIP puzzle progress and for opening a puzzle in gridwords. Black spaces are maked with `#`, unfilled white spaces with `.`
```<GRIDWORDS PUZZLE>
<TITLE>
  Incomplete Puzzle
<AUTHOR>
  sagemeadows
<DESCRIPTION>
  This is an unfinished puzzle.
<SIZE>
  5x5
<GRID>
  #O..A
  .U.#W
  STERN
  .#.OY
  EPIC#
<CLUES>
  1 across,
  1 down,Available? Not here (3)
  2 down,
  3 down,"Scratching face, old Scotsman with a beard (4)"
  4 across,
  4 down,
  5 across,Small aquatic bird in rear of vessel (5)
  6 down,Legendary bird biting head off dangerous reptile (3)
  7 across,
  8 across,Great drama
```
Note that there is a variety of clue formats (i.e. whether they include the number of letters or not, whether they are in quotation marks or not). If you like a clue but not its format, you can always edit the .txt file directly to change things to your liking.

```<GRIDWORDS PUZZLE>
<TITLE>
  A Little Example
<AUTHOR>
  sagemeadows
<DESCRIPTION>
  Here is a crossword puzzle description.
<SIZE>
  4x4
<GRID>
  BAT#
  OVER
  YOLO
  #WET
<CLUES>
  1 across,Animal hiding in abattoir
  1 down,Not yet a man
  2 down,Swear nothing's been hidden in a car
  3 down,Prefix for vision and marketing
  4 across,"Copy that, __."
  5 down,Root vegetable loses half to decay
  6 across,"Seize the day!"
  7 across,How backstroke contestant ends
```
If you have a .txt file with this layout, you can load it in Gridwords with the 'Open...' button.

This .txt file layout is adapted from the example given [here](https://www.litsoft.com/across/docs/AcrossTextFormat.pdf) on page 2.

#### HTML
**.html** files are for creating a version of the puzzle that can be converted to a printable PDF. The easiest way to do this is to open the .html file in a browser that lets you turn pages into PDFs (e.g. Chrome) and save a PDF version there.

If the black spaces don't show up on the PDF, check 'More Options' to see if there's a 'Show Backgrounds' option and make sure to check the box.

```<!DOCTYPE html>

<!--4x4-->

<html>
<head>
<style>
.grid-container {
  display: inline-grid;
  row-gap: 2px;
  column-gap: 2px;  grid-template-columns: auto auto auto auto ;
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

<h1>A Little Example</h1>

<h3>By sagemeadows</h3>

<p>Here is a crossword puzzle description.</p>

<div class="grid-container">
  <div class="grid-item"><index>1</index></div>
  <div class="grid-item"><index>2</index></div>
  <div class="grid-item"><index>3</index></div>
  <div class="grid-item" style="background-color:#000000"></div>
  <div class="grid-item"><index>4</index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item"><index>5</index></div>
  <div class="grid-item"><index>6</index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item" style="background-color:#000000"></div>
  <div class="grid-item"><index>7</index></div>
  <div class="grid-item"><index></index></div>
  <div class="grid-item"><index></index></div>
</div>

<br>

<div class="clues-grid">
  <div class="clues-direc"><b>Across</b><br>
    1. Animal hiding in abattoir<br>
    4. "Copy that, __."<br>
    6. "Seize the day!"<br>
    7. How backstroke contestant ends<br>
  </div>
  <div class="clues-direc"><b>Down</b><br>
    1. Not yet a man<br>
    2. Swear nothing's been hidden in a car<br>
    3. Prefix for vision and marketing<br>
    5. Root vegetable loses half to decay<br>
  </div>
</div>

<p style="page-break-after: always;">&nbsp;</p>
<p style="page-break-before: always;">&nbsp;</p>

<h1>A Little Example Solution</h1>

<div class="grid-container">
  <div class="grid-item"><index>1</index><br><center><letter>B</letter></center></div>
  <div class="grid-item"><index>2</index><br><center><letter>A</letter></center></div>
  <div class="grid-item"><index>3</index><br><center><letter>T</letter></center></div>
  <div class="grid-item" style="background-color:#000000"></div>
  <div class="grid-item"><index>4</index><br><center><letter>O</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>V</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>E</letter></center></div>
  <div class="grid-item"><index>5</index><br><center><letter>R</letter></center></div>
  <div class="grid-item"><index>6</index><br><center><letter>Y</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>O</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>L</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>O</letter></center></div>
  <div class="grid-item" style="background-color:#000000"></div>
  <div class="grid-item"><index>7</index><br><center><letter>W</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>E</letter></center></div>
  <div class="grid-item"><index></index><br><center><letter>T</letter></center></div>
</div>

</body>
</html>
```
## TO-DO:
- Improve selected-cell movement so that it jumps to next unfinished word.
- Clean up database, more clue format consistency.

## Disclaimers
The crossword dataset used here is adapted from the [cryptics.georgeho.org](https://cryptics.georgeho.org/) dataset.

