"""
Extracts the top-left 2x2 subgrid from the input grid.

The transformation identifies the input grid and selects the subgrid located 
at the top-left corner. This subgrid spans the first 2 rows (row index 0 and 1) 
and the first 2 columns (column index 0 and 1). The output grid is created 
by copying the pixel values from this selected 2x2 subgrid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid from the given input grid.

    Args:
        input_grid (list or np.ndarray): The input grid represented as a 
                                         list of lists or a numpy array.

    Returns:
        np.ndarray: A 2x2 numpy array representing the top-left corner 
                    of the input grid.
    """
    # Convert input grid to a numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)

    # Extract the subgrid from the top-left corner (rows 0 to 1, columns 0 to 1)
    # Slicing [0:2, 0:2] selects rows with index 0 and 1, and columns with index 0 and 1.
    output_grid = grid[0:2, 0:2]

    # Return the extracted 2x2 subgrid
    return output_grid
