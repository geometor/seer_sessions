"""
Shifts the entire content of the input grid one column to the left. 
The first column is discarded, and the last column is filled with the 
background color, which is determined from the top-left corner pixel 
of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Shifts the grid content one column to the left, discarding the first 
    column and filling the last column with the background color.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Determine the background color from the top-left corner
    background_color = input_array[0, 0]

    # Initialize the output grid with the same dimensions
    # We can initialize with the background color, as the last column will be this color.
    output_grid = np.full((height, width), background_color, dtype=int)

    # Check if the grid width is greater than 1 to avoid index errors
    if width > 1:
        # Copy the content from the second column onwards from the input 
        # to the first column up to the second-to-last column in the output.
        # input_array[:, 1:] selects all rows, and columns from index 1 to the end.
        # output_grid[:, :-1] selects all rows, and columns from index 0 up to (but not including) the last one.
        output_grid[:, :-1] = input_array[:, 1:]
    
    # The last column is already filled with the background color due to initialization.
    # If we hadn't initialized with the background color, we would do:
    # output_grid[:, -1] = background_color

    return output_grid
