"""
The rule identifies specific white cells, located at the corners defined by a 3x3 grid, and changes them to magenta. The 3x3 squares don't exist in the input data, but the corners are created using the pattern and shape of the layout of yellow pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing specific white cells to magenta based on their position.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid, checking for potential magenta locations.
    for i in range(rows):
        for j in range(cols):
            # Check if the current cell is white (0).
            if output_grid[i, j] == 0:
                # check if location aligns with the "corner" of 3x3 square
                if i % 2 == 0 and j % 2 == 0:
                    output_grid[i,j] = 6

    return output_grid