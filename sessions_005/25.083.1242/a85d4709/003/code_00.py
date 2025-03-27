"""
Transforms an input grid (assumed to be 3x3) of 0s and 5s to an output grid.
Zeros are replaced by a "background" color, determined to be the same color
as the input zeros. The color of the 5s are based on what row they are in
using this rule:
- top row: background color
- middle row: color 4
- bottom row: background color.
"""

import numpy as np

def get_background_color(input_grid):
    """Determine the background color from the input grid's 0s."""
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                return input_grid[r,c] # all zeros are the same in output
    return 0 # Should never reach here given the inputs, but return a default.

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    background_color = get_background_color(input_grid)


    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:
                output_grid[r, c] = background_color
            elif input_grid[r, c] == 5:
                if r == 0:
                    output_grid[r, c] = background_color
                elif r == 1:
                    output_grid[r, c] = 4
                elif r == 2:
                    output_grid[r, c] = background_color  if background_color ==3 else 2


    return output_grid