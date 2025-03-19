"""
Extracts the bottom-left 3x3 sub-grid from the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-left 3x3 subgrid from the input.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: The 3x3 subgrid extracted from the bottom-left corner.
    """
    # Convert input_grid to a NumPy array for easier slicing.
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_array.shape

    # Extract the bottom-left 3x3 subgrid.
    output_array = input_array[rows-3:rows, 0:3]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid