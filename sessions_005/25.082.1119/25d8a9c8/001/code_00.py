"""
Iterate through each row of the input grid. If all pixels in a row are identical, create a corresponding row in the output grid filled with 5s. Otherwise, create a corresponding row filled with 0s.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on whether all elements in a row are the same.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each row of the input grid
    for i in range(rows):
        # Check if all elements in the row are identical
        if all(input_grid[i][j] == input_grid[i][0] for j in range(cols)):
            # Fill the corresponding output row with 5s
            output_grid[i, :] = 5
        else:
            # Fill the corresponding output row with 0s
            output_grid[i, :] = 0

    return output_grid