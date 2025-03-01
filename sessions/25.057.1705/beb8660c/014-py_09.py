"""
The transformation is a 90-degree clockwise rotation of the grid *excluding* the bottom row, which remains constant.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise, excluding the bottom row.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Rotate all rows except the last one
    for r in range(rows - 1):
        for c in range(cols):
            output_grid[c, rows - 2 - r] = input_grid[r, c]
            
    return output_grid.tolist()