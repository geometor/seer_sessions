"""
The output is a 1x1 grid. If the input contains red, the output is blue.
Otherwise, the output is black.
"""

import numpy as np

def transform(input_grid):
    """
    Transform input_grid.
    """
    # initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Count the occurrences of red (2)
    red_count = np.sum(input_grid == 2)

    # if red exists in input
    if(red_count > 0):
        # Set the output to blue (1)
        output_grid[0, 0] = 1
    else:
        # Set the output to black/white (0) - corrected for no red
        output_grid[0, 0] = 0

    return output_grid