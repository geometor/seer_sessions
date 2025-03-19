"""
The transformation rule is: white (0) pixels in the input grid shift down by one row, wrapping around from the bottom row to the top. Maroon (9) pixels remain in their original positions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: white pixels shift down one row, wrapping around.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid to find white pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:
                # Calculate the new row index, wrapping around
                new_r = (r + 1) % rows
                # Shift the white pixel down
                output_grid[r, c] = 9  # original spot becomes maroon
                output_grid[new_r, c] = 0 # new location

    return output_grid