"""
The transformation rule for the 3x3 grids can be described as follows:

1.  Preserve the First Row: The entire first row of the input grid is copied to the output grid without any changes.
2.  Preserve the Main Diagonal: The elements on the main diagonal (top-left to bottom-right) of the input grid are preserved in the output grid.
3.  Clear Other Elements: All other elements in the output grid, except those in the first row and on the main diagonal, are set to 0.

In essence, the transformation preserves the first row and the main diagonal and sets all other cells to 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  We'll modify it in place.
    output_grid = np.copy(input_grid)
    size = output_grid.shape[0]

    # Preserve the first row (already done by copying).

    # Preserve the main diagonal (iterate through the diagonal indices).
    for i in range(size):
        output_grid[i, i] = input_grid[i, i]

    # Clear other elements (iterate and check if not first row and not diagonal).
    for i in range(size):
        for j in range(size):
            if i != 0 and i != j:  # Check for not first row (i=0) and not diagonal (i=j)
                output_grid[i, j] = 0

    return output_grid