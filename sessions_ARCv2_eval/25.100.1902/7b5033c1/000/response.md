**Perception of Task Elements:**

1.  **Input:** The input is a multi-line string representing a grid of single digits. Each line is a row, and digits within a line are separated by spaces, representing cells in that row.
2.  **Output:** The output is a multi-line string where each line contains a single digit. This represents a list or sequence of digits.
3.  **Core Observation:** The input grid contains a "background" color (digit) and several "foreground" colors (digits) forming distinct or scattered shapes/pixels. The output list consists of all the foreground digits found in the input grid.
4.  **Background Identification:** The background color appears to be the most prevalent color, often filling the majority of the grid and specifically the corners/edges. In both examples, the digit at the top-left corner (`grid[0][0]`) corresponds to the background color that is *excluded* from the output.
5.  **Foreground Extraction:** The digits that are *not* the background color are extracted.
6.  **Ordering:** The order of the digits in the output list corresponds precisely to the order they are encountered when scanning the input grid row by row (top to bottom), and within each row, column by column (left to right).
7.  **Transformation:** The transformation rule involves identifying the background color, scanning the grid in a standard top-to-bottom, left-to-right manner, and collecting every non-background digit encountered into a list, preserving the scanning order.

**Facts:**


```yaml
Task: Extract and order foreground pixels from a grid based on a background color.

Objects:
  - InputGrid:
      Properties:
        - rows: A list of strings or lists representing grid rows.
        - cells: Individual digits within the grid.
        - dimensions: height (number of rows), width (number of columns).
  - Cell:
      Properties:
        - value: The digit (color) of the cell.
        - row_index: The row position (0-based).
        - col_index: The column position (0-based).
  - BackgroundColor:
      Properties:
        - value: The digit identified as the background.
      Identification: Typically the value of the cell at InputGrid[0][0].
  - ForegroundCell:
      Isa: Cell
      Condition: Cell.value != BackgroundColor.value
  - OutputList:
      Properties:
        - elements: A sequence of digits.
      Content: Contains the values of all ForegroundCells from the InputGrid.
      Ordering: Determined by scanning the InputGrid row-by-row, then column-by-column.

Actions:
  - IdentifyBackgroundColor: Determine the BackgroundColor.value from the InputGrid (e.g., using the top-left cell).
  - ScanGrid: Iterate through the InputGrid cells systematically (top-to-bottom, left-to-right).
  - CheckCell: For each cell, compare its value to the BackgroundColor.value.
  - CollectForeground: If a cell is a ForegroundCell, append its value to the OutputList.

Relationships:
  - OutputList.elements are derived exclusively from ForegroundCells in the InputGrid.
  - The order of OutputList.elements depends on the row_index and col_index of the corresponding ForegroundCells during the ScanGrid action.
  - BackgroundColor acts as a filter, excluding cells with its value from the OutputList.
```


**Natural Language Program:**

1.  Read the input string and parse it into a 2D grid of digits.
2.  Identify the background digit: Take the digit value from the cell at the top-left corner (row 0, column 0) of the grid.
3.  Initialize an empty list called `output_digits`.
4.  Iterate through each row of the grid, starting from the top row (row 0) and proceeding downwards.
5.  Within each row, iterate through each cell (digit), starting from the leftmost column (column 0) and proceeding to the right.
6.  For the current cell being examined:
    *   Compare the cell's digit value to the identified background digit.
    *   If the cell's digit is *different* from the background digit, append the cell's digit to the `output_digits` list.
7.  After scanning all cells in the grid, format the `output_digits` list into the required output format (a multi-line string with one digit per line).