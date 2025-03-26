"""
Extracts the 2x2 subgrid located at the top-left corner (indices [0,0] to [1,1]) of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid from the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the 2x2 output grid.
    """
    # Ensure the input is a numpy array
    input_grid_np = np.array(input_grid)

    # Extract the subgrid from the top-left corner (rows 0 and 1, columns 0 and 1)
    # The slice [0:2] includes index 0 and 1 (up to, but not including, 2)
    # The slice [0:2] includes index 0 and 1 (up to, but not including, 2)
    output_grid = input_grid_np[0:2, 0:2]

    # Return the extracted 2x2 subgrid
    return output_grid
