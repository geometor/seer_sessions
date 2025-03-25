"""
1.  **Initialization:** Create an output grid (`output_grid`) with the same dimensions as the input grid, filled with zeros (white).

2.  **Locate Red Pixel:** Find the row and column coordinates (`red_row`, `red_col`) of the single red pixel (value 2) within the input grid.

3.  **Conditional Output:** If no red pixel is found, return the initialized `output_grid` (all zeros).

4.  **Calculate Relative Positions and Place Colored Pixels**:
    *   **Green Pixel (3):** Place a green pixel (value 3) at the location one row *above* and one column *to the left* of the red pixel (`red_row - 1`, `red_col - 1`).
    *   **Magenta Pixel (6):** Place a magenta pixel (value 6) at the location one row *above* and one column *to the right* of the red pixel (`red_row - 1`, `red_col + 1`).
    *   **Azure Pixel (8):** Place an azure pixel (value 8) at the location one row *below* and one column *to the left* of the red pixel (`red_row + 1`, `red_col - 1`).
    *   **Orange Pixel (7):** Place an orange pixel (value 7) at the location one row *below* and one column *to the right* of the red pixel (`red_row + 1`, `red_col + 1`).

5.  **Boundary Check**: Before placing any colored pixel, check if its calculated row and column coordinates are within the valid bounds of the `output_grid`. If not, skip placing that specific pixel. There is NO central black pixel being placed.

6.  **Output:** Return the modified `output_grid`.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # find red pixel
    red_row, red_col = -1, -1  # Initialize to invalid values
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 2:
                red_row, red_col = i, j
                break  # Only one red pixel expected
        if red_row != -1:
            break

    if red_row == -1: # no red pixel
      return output_grid

    # bounds check helper
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # green
    if is_valid(red_row - 1, red_col - 1):
        output_grid[red_row - 1, red_col - 1] = 3

    # magenta
    if is_valid(red_row - 1, red_col + 1):
        output_grid[red_row - 1, red_col + 1] = 6

    # azure
    if is_valid(red_row + 1, red_col - 1):
        output_grid[red_row + 1, red_col - 1] = 8

    # orange
    if is_valid(red_row + 1, red_col + 1):
        output_grid[red_row + 1, red_col + 1] = 7
    
    return output_grid