"""
Transforms an input grid into an output grid of the same dimensions. If the number 9 exists in the input grid, the output grid is filled entirely with 9s.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into an output grid of the same dimensions.
    If 9 exists in input, output is all 9s.
    """
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Check if 9 exists in the input grid.
    if 9 in input_grid:
        # Create an output grid filled entirely with 9s.
        output_grid[:] = 9
    
    return output_grid.tolist()