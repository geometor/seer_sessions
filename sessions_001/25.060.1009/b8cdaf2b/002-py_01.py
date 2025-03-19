"""
Copies the input grid to the output grid. Then, it iterates through the grid starting from the third-to-last row, moving upwards.
If a pixel above the bottom two rows is white (0), it checks the pixel two rows below. If that pixel has color x, and the current pixel is 0, replace with x. The bottom two rows are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Preserve the bottom two rows
    # output_grid[-2:, :] = input_grid[-2:, :] # already done by np.copy

    # Iterate upwards from the third-to-last row
    for i in range(rows - 3, -1, -1):
        for j in range(cols):
            # Conditional Color Change
            if output_grid[i, j] == 0:  # If the current pixel is white
                if i + 2 < rows: # added this condition
                    output_grid[i,j] = input_grid[i+2,j]

    return output_grid