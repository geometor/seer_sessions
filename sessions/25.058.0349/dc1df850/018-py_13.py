"""
1.  **Locate the Red Pixel:** Find the single red pixel (value 2) in the input grid.
2.  **Preserve Colors:** Initialize the output grid as a direct copy of the input grid.
3.  **Vertical Propagation:**
    *   Examine the pixels directly above and directly below the red pixel.
    *   If a neighboring pixel is white (value 0), change it to blue (value 1) in the output grid.
    *   Continue this process vertically:
        *   For each newly changed blue pixel, check *its* immediate neighbor directly above or below (depending on the direction of propagation - above for pixels above the red pixel, below for pixels below the red pixel).
        *    If that neighbor is white, change it to blue.
        *   Repeat until a non-white pixel or the edge of the grid is encountered.
4. **Horizontal propagation does not occur**
"""

import numpy as np

def find_pixel_by_value(grid, value):
    # Find the coordinates of a pixel with a specific value.
    rows, cols = np.where(grid == value)
    if len(rows) > 0:
        return rows[0], cols[0]  # return first if multiple
    return None

def is_valid(row, col, grid_shape):
    #check that a coordinate is within bounds
    return 0 <= row < grid_shape[0] and 0 <= col < grid_shape[1]

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # Find the red pixel
    red_pixel_coords = find_pixel_by_value(input_grid, 2)

    if red_pixel_coords:
        red_row, red_col = red_pixel_coords

        # Propagate upwards
        current_row = red_row - 1
        while is_valid(current_row, red_col, grid_shape) and input_grid[current_row, red_col] == 0:
            output_grid[current_row, red_col] = 1
            current_row -= 1

        # Propagate downwards
        current_row = red_row + 1
        while is_valid(current_row, red_col, grid_shape) and input_grid[current_row, red_col] == 0:
            output_grid[current_row, red_col] = 1
            current_row += 1

    return output_grid