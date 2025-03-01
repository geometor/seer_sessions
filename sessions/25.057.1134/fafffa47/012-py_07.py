"""
1.  **Identify the Object of Interest:** Examine the input grid and locate the first row, from top to bottom, with at least one pixel of any non-black (non-0) color that is directly above a row that is composed of entirely the same color.

2.  **Define the Output Region:** Consider a 3x3 area.

3. **Determine color change:** The object identified in step 1 changes color to red (2)

4.  **Populate Output:** Create an output grid of size 3x3. The identified object's pixels that are in the center column become red (2) in the output grid, within the top 3 rows. All other cells in the output are black/white (0).
"""

import numpy as np

def find_object_of_interest(input_grid):
    """Finds the column index and color of the object of interest."""
    rows, cols = input_grid.shape
    for r in range(rows - 1):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Check if the row below is all the same color
                color = input_grid[r, c]
                next_row = r + 1
                same_color_below = True
                for c2 in range(cols):
                  if input_grid[next_row,c2] != color:
                    same_color_below = False
                    break
                if same_color_below:

                    return next_row, color, c
    return None, None, None

def transform(input_grid):
    # Find the object of interest and its color.
    row_index, color, col_index = find_object_of_interest(input_grid)

    # Initialize a 3x3 output grid with all zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # If no object is found return empty 3x3
    if row_index is None:
      return output_grid

    # Populate center with red(2)
    for r in range(min(3,row_index)):
      output_grid[r,1] = 2

    return output_grid