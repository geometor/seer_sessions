"""
Selects the 3x3 subgrid located at the top-right corner of the input 9x9 grid.
Specifically, it extracts the region defined by rows 0 to 2 (inclusive) and columns 6 to 8 (inclusive).
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-right 3x3 subgrid from the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the extracted 3x3 subgrid.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid_np = np.array(input_grid)

    # Define the coordinates for the top-right 3x3 subgrid
    top_row = 0
    bottom_row = 3 # Slicing is exclusive for the end index
    left_col = 6
    right_col = 9  # Slicing is exclusive for the end index

    # Extract the subgrid using numpy slicing
    output_grid = input_grid_np[top_row:bottom_row, left_col:right_col]

    return output_grid
