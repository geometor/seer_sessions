"""
The transformation extracts a 2x2 subgrid from the top-left corner of the input grid. The top-left corner of the output grid corresponds to position (0, 0) of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the 2x2 subgrid at the top-left corner of the input grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Extract the 2x2 subgrid starting at (0, 0)
    output_grid = input_grid[0:2, 0:2]

    return output_grid.tolist()