"""
Wherever there's a gray pixel in the input, put a red pixel in the same column on all rows that have any grey pixels. The gray pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule: Replaces some white pixels (0) with red pixels (2)
    based on the positions of gray pixels (5).
    """
    output_grid = np.copy(input_grid)
    rows_with_gray = set()
    gray_cols = set()

    # Find rows and columns with gray pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 5:
                rows_with_gray.add(r)
                gray_cols.add(c)

    # Substitute white pixels with red in the identified rows and columns
    for r in rows_with_gray:
        for c in gray_cols:
            if input_grid[r,c] == 0:
                output_grid[r, c] = 2

    return output_grid