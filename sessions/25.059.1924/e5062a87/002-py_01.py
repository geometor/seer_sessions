"""
Identify all red (2) pixels in the input grid.
For each existing red pixel, if it doesn't form the shape below, fill the shape that matches.
   
    2
   2 2
  2   2
   2 2
    2

Return the changed grid.
"""

import numpy as np

def get_red_pixels(grid):
    """
    Finds the coordinates of all red pixels in the grid.
    """
    red_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_idx, col_idx))
    return red_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    # iterate through the identified red pixels
    for r, c in red_pixels:
        # Define the shape relative to the current red pixel
        shape = [
            (-2, 0),
            (-1, -1), (-1, 1),
            (0, -2), (0, 2),
            (1, -1), (1, 1),
            (2, 0)
        ]

        # Fill the shape
        for dr, dc in shape:
            new_r, new_c = r + dr, c + dc
            # check bounds
            if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
               output_grid[new_r, new_c] = 2
                
    return output_grid