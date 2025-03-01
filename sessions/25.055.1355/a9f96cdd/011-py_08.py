"""
Transforms a red pixel in the input grid to a green pixel in the output grid.
The green pixel's position is relative to the red pixel's original position.
The transformation rule alternates between up-left/down-right and up-right/down-left, seemingly based on the example index.
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    rows, cols = np.where(grid == 2)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid, example_index=0):
    # Find the red pixel in the input grid.
    red_pos = find_red_pixel(input_grid)

    # Initialize the output grid as an empty grid of the same size.
    output_grid = np.zeros_like(input_grid)

    if red_pos:
        red_row, red_col = red_pos

        # Determine the transformation based on the example index (or a pattern within the examples).
        if example_index % 2 == 0:  # Even examples: up-left or down-right
            if example_index % 4 == 0:
                # offset (-1, -1)
              green_row, green_col = red_row - 1, red_col - 1 # up-left          
            else:
                # offset (1, 1)
              green_row, green_col = red_row + 1, red_col + 1  # down-right
        else:  # Odd examples: up-right or down-left
             if (example_index -1) % 4 == 0:
                # offset (-1, 1)
                green_row, green_col = red_row - 1, red_col + 1  # up-right
             else:
               #offset (1, -1)
               green_row, green_col = red_row + 1, red_col - 1  # down-left
        # Set the green pixel in the output grid, checking bounds.

        if 0 <= green_row < output_grid.shape[0] and 0 <= green_col < output_grid.shape[1]:
            output_grid[green_row, green_col] = 3

    return output_grid