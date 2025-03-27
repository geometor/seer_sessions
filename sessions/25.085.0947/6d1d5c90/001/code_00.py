"""
Take the input grid.
Select all rows and all columns starting from the second column (index 1) until the last column.
The selected subgrid forms the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Removes the first column of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid, which is the 
                    input grid with the first column removed.
    """
    # Convert input list of lists to numpy array if it isn't already
    input_grid_np = np.array(input_grid)
    
    # Select all rows (:) and all columns starting from index 1 to the end (1:)
    output_grid = input_grid_np[:, 1:]
    
    # Return the resulting subgrid
    return output_grid
