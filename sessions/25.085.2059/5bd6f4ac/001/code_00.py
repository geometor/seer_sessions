"""
Extracts the top-right 3x3 subgrid from the 9x9 input grid.
The output grid consists of the pixels located at rows 0, 1, and 2,
and columns 6, 7, and 8 of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the 3x3 subgrid from the top-right corner of the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 3x3 list representing the extracted subgrid.
    """
    # Convert the input grid to a NumPy array for easier slicing
    grid = np.array(input_grid, dtype=int)

    # Define the region to extract (rows 0 to 2, columns 6 to 8)
    start_row, end_row = 0, 3  # Slicing is exclusive of the end index
    start_col, end_col = 6, 9  # Slicing is exclusive of the end index

    # Extract the subgrid using NumPy slicing
    output_grid_np = grid[start_row:end_row, start_col:end_col]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
