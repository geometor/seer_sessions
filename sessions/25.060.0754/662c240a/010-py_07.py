"""
Extracts the bottom-right 3x3 subgrid from the input grid if it's large enough,
otherwise returns an empty grid.  Also handles identity transformation.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 subgrid or returns an empty grid if the input
    is too small. Also handles the identity transformation.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The bottom-right 3x3 subgrid, an empty grid, or the input grid.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Handle identity transformation
    if 'output_grid' in locals() and input_array.tolist() == output_grid:  # Check if output_grid is defined first. Not ideal
        return input_grid
    
    # Handle small grids.
    if rows < 3 or cols < 3:
        return []
    
    # Extract the bottom-right 3x3 subgrid.
    output_array = input_array[rows-3:rows, cols-3:cols]
    output_grid = output_array.tolist()
    
    return output_grid