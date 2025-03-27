"""
For each column in the grid, yellow pixels (4) extend upwards by one row, replacing black (0) pixels directly above them, provided the yellow pixel is not in the bottom row. Yellow pixels in the bottom row remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through columns
    for col in range(cols):
        # Iterate through rows (excluding the bottom row)
        for row in range(rows - 1):
            # Check if the current pixel is yellow and not in the bottom row
            if input_grid[row, col] == 4:
                # Check if the pixel directly above is black
                if row > 0 and input_grid[row - 1, col] == 0:
                    # Change the black pixel above to yellow
                    output_grid[row - 1, col] = 4

    return output_grid.tolist()