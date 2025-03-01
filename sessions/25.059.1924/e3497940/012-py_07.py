"""
1.  **Identify the grey (5) column:** Find the single vertical column in the input grid that is entirely filled with the color grey (5).

2.  **Define extraction boundaries:**
    *   Start column for extraction: the very next column to the right, where grey ends.
    *   End column: Include all contiguous columns, as long as they don't have any grey or white.

3.  **Extract Sub-grid:** Create the output grid by extracting all rows, and the columns from the calculated start to the calculated end.

4.  **Remove Grey (5) Pixels:** Remove/Exclude any pixels that have a color of grey, leaving only red and magenta and white.
"""

import numpy as np

def find_grey_column(grid):
    """Finds the index of the column that is entirely grey (5)."""
    rows, cols = grid.shape
    for j in range(cols):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Return -1 if no grey column is found

def transform(input_grid):
    """Transforms the input grid by extracting a subgrid around a grey column."""
    # Find the grey column
    grey_col_index = find_grey_column(input_grid)

    # Initialize the output grid
    rows, cols = input_grid.shape
    
    if grey_col_index == -1:
        output_grid = np.zeros_like(input_grid)
        return output_grid
        

    # Define extraction boundaries.
    start_col = grey_col_index + 1

    # find end of contiguous non-grey section, checking all rows
    end_col = start_col
    while end_col < cols:
        if any(input_grid[r,end_col] == 5 or input_grid[r,end_col] == 0 for r in range(rows)):
            break
        end_col += 1
        

    # Extract the sub-grid, and create as all zeros
    output_grid = np.zeros((rows, end_col - start_col))

    # change relevant pixels to values from input, excluding 5
    for r in range(rows):
      for c in range(start_col,end_col):
        if input_grid[r,c] != 5:
          output_grid[r,c-start_col] = input_grid[r,c]

    return output_grid