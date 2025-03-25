"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, filled with zeros (white).

2.  **Locate Red Pixel:** Find the coordinates (row, col) of the single red pixel (value 2) in the input grid.

3.  **Create "+" Pattern:** Create a "+" shaped pattern in the output grid, *centered* at the location of the input red pixel, adjusted by (-1,0) to be centered one row *above* red pixel.
    *   Set the output pixel at the adjusted location to 0.
    *   Set the output pixel directly above the adjusted center to 3 (green).
    *   Set the output pixel directly below the adjusted center to 6 (magenta).
    *   Set the output pixel to the left of the adjusted center to 8 (azure).
    *   Set the output pixel to the right of the adjusted center to 7 (orange).

4. **Edge Cases Handling**: If the calculated position for any part of the '+' is outside the bounds of the grid, do not place the corresponding colored pixel. (e.g. when Red is in row 0, no color 3 above. If red in col 0 no color 8, etc.)

5.  **Output:** Return the modified `output_grid`.
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

    # create '+' pattern
    center_row = red_row -1
    center_col = red_col

    # bounds check helper
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols
    
    # center
    if is_valid(center_row, center_col):
        output_grid[center_row, center_col] = 0

    # above
    if is_valid(center_row - 1, center_col):
        output_grid[center_row - 1, center_col] = 3

    # below
    if is_valid(center_row + 1, center_col):
        output_grid[center_row + 1, center_col] = 6

    # left
    if is_valid(center_row, center_col - 1):
        output_grid[center_row, center_col - 1] = 8

    # right
    if is_valid(center_row, center_col + 1):
        output_grid[center_row, center_col + 1] = 7
    
    return output_grid