"""
The transformation rule is as follows:
1. Scan the input grid to identify all red (2) pixels.
2. Iterate, row by row, bottom to top, to find, if available the right-most red pixel and change the value to a blue pixel.
3. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the bottom-rightmost red pixel to blue.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through rows from bottom to top
    for i in range(rows - 1, -1, -1):
        # Iterate through columns from right to left
        for j in range(cols - 1, -1, -1):
            if output_grid[i, j] == 2:  # If the pixel is red
                output_grid[i, j] = 1  # Change it to blue
                return output_grid  # Return after the first replacement

    return output_grid