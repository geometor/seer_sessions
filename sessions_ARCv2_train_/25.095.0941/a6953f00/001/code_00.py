"""
Extracts a 2x2 subgrid from an input grid. 
If the input grid is 4x4, extracts the subgrid from the first two rows and the last two columns (indices [0:2, 2:4]). 
Otherwise, extracts the top-left 2x2 subgrid (indices [0:2, 0:2]).
"""

import numpy as np

def transform(input_grid):
    """
    Extracts a specific 2x2 subgrid from the input grid based on its dimensions.

    Args:
        input_grid (list of lists): A 2D list representing the input grid of integers.

    Returns:
        list of lists: A 2x2 list representing the extracted subgrid.
    """
    # Convert the input list of lists to a numpy array for easier slicing and dimension checking
    grid = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    num_rows, num_cols = grid.shape

    # Initialize the variable to hold the extracted subgrid
    output_subgrid_np = None 

    # Check if the input grid dimensions are 4x4
    if num_rows == 4 and num_cols == 4:
        # Extract the subgrid from rows 0, 1 and columns 2, 3
        output_subgrid_np = grid[0:2, 2:4]
    else:
        # Otherwise, extract the top-left 2x2 subgrid (rows 0, 1 and columns 0, 1)
        output_subgrid_np = grid[0:2, 0:2]

    # Convert the resulting numpy array back to a list of lists for the final output
    output_grid = output_subgrid_np.tolist()

    return output_grid
