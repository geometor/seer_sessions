"""
The input is a 9x3 grid. The output is the top 3x3 sub-grid of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top 3x3 sub-grid from a 9x3 input grid.
    """
    # Convert input_grid to a NumPy array for easier slicing.
    input_grid = np.array(input_grid)

    # Extract the top 3x3 sub-grid (rows 0-2, all columns).
    output_grid = input_grid[:3, :]

    # Convert the result back to a list.
    return output_grid.tolist()