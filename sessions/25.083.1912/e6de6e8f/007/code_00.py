"""
1.  **Determine Output Dimensions:**
    *   `output_width` is equal to the `input_width`.
    *   `output_height` is equal to the `input_width` plus the number of rows from the top until the first row that has one or more red pixels plus one, or, `output_height = input_width + first_red_row + 1`. If no red pixels, then the output is an empty grid.

2.  **Initialize Output Grid:**
    *   Create an output grid of size `output_height` x `output_width` filled with white pixels (0).

3.  **Place Green Pixel:**
    *   Calculate the middle column: `green_x = (output_width + 1) // 2 - 1`.
    *   Place a single green pixel (3) at `output_grid[0, green_x]`.

4.  **Place Red Stripes:**
    *   Find the x-coordinates (column indices) of all red pixels in the input grid.
    *   For each `x` (column index) where red appears in the input:
        *   In the output grid, create a vertical red stripe (color 2) at the same `x` coordinate.
        *   The stripe starts at row 3 (`y = 3`).
        *   The stripe extends to the bottom of the output grid (`y = output_height - 1`).

5. **Handle Empty Case:**
  * If there is no red pixel in the input, return an empty output grid
"""

import numpy as np

def get_red_x_positions(grid):
    """Finds the x-coordinates of all red pixels in the grid."""
    red_x_positions = []
    for x in range(grid.shape[1]):
        for y in range(grid.shape[0]):
            if grid[y, x] == 2:
                red_x_positions.append(x)
                break  # Move to the next column once a red pixel is found
    return red_x_positions

def get_first_red_row(grid):
    """Finds the row index of the first row containing a red pixel."""
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                return y
    return -1 # Return -1 to signal no red

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    red_x_positions = get_red_x_positions(input_grid)
    first_red_row = get_first_red_row(input_grid)

    if first_red_row == -1:
       return np.zeros((0,0), dtype=int)

    output_width = input_width
    output_height = input_width + first_red_row + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place green pixel
    green_x = (output_width + 1) // 2 - 1
    output_grid[0, green_x] = 3

    # Place red stripes
    for x in red_x_positions:
        start_row = 3
        for y in range(start_row, output_height):
            output_grid[y, x] = 2

    return output_grid