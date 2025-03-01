"""
1.  **Initialization:** Create a 4x4 output grid filled with zeros.
2.  **Color Filtering:** Remove all pixels of color 2 (red) from the input. Any other color becomes 0 in input.
3.  **Column 1 Logic:**
    *   If there's a yellow (4) anywhere in the filtered input, place a 4 in the top-left cell (0, 0) of the output.
    * If there is a maroon (9) in the first column of the input, place a 9 in the top-left cell (0,0) of the output.
    * Otherwise the top-left cell remains zero.
4.  **Column 2 Logic:**
    *   For each row (from 0 to 3), check if there's a continuous horizontal line of yellow (4) in the *input* grid at that row.
    *  If a horizontal line of yellow exist in the *input* for any row, set all values for column 2 of the output to 4.
5.  **Column 3 Logic:**
    *   Examine specific spatial relationships in the *input* grid:
        *   If a 0 is immediately to the left of a 9, set output[0, 2] to 0.
        *   If a 9 is directly above another 9, set output[1, 2] to 9.
        *   If a 1 is directly above another 1, set output[2, 2] to 1.
        * If a 4 is directly below a 1, set output[3,2] to 4.
6.  **Column 4 Logic:**
    *  If row 4 (index 3) of input has a yellow, set all rows of column 4 to 4.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid (4x4) with zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # Color Filtering (implicitly handled by other rules, as only 0, 1, 4, and 9 are used)
    filtered_grid = np.copy(input_grid)
    filtered_grid[filtered_grid == 2] = 0

    # Column 1 Logic
    if np.any(filtered_grid == 4):
        output_grid[0, 0] = 4
    if np.any(filtered_grid[:, 0] == 9):
        output_grid[0, 0] = 9

    # Column 2 Logic
    for r in range(input_grid.shape[0]):
        if np.any(filtered_grid[r,:] == 4):
          has_horizontal_yellow = False
          for c in range(input_grid.shape[1] -1):
            if input_grid[r,c] == 4 and input_grid[r, c+1] == 4:
              has_horizontal_yellow = True
              break
          if has_horizontal_yellow:
            output_grid[:, 1] = 4
            break # Once a yellow is found set and exit

    # Column 3 Logic
    for r in range(filtered_grid.shape[0]):
        for c in range(filtered_grid.shape[1]):
            if filtered_grid[r, c] == 0 and c + 1 < filtered_grid.shape[1] and filtered_grid[r, c + 1] == 9:
                output_grid[0, 2] = 0
            if filtered_grid[r, c] == 9 and r + 1 < filtered_grid.shape[0] and filtered_grid[r + 1, c] == 9:
                output_grid[1, 2] = 9
            if filtered_grid[r, c] == 1 and r + 1 < filtered_grid.shape[0] and filtered_grid[r + 1, c] == 1:
                output_grid[2, 2] = 1
            if filtered_grid[r, c] == 4 and r > 0 and filtered_grid[r - 1, c] == 1:
                output_grid[3, 2] = 4

    # Column 4 Logic
    if np.any(filtered_grid[3, :] == 4):
        output_grid[:, 3] = 4

    return output_grid