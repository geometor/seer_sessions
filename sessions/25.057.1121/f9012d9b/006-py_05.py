"""
The transformation extracts the 3x3 square object located at the top-left corner of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    grid = np.array(input_grid)

    # Extract the 3x3 top-left square.
    output_grid = grid[0:3, 0:3]

    return output_grid.tolist()