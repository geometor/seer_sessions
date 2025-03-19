"""
The transformation replaces azure pixels in the center row of the input grid with gray pixels, leaving all other pixels untouched.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing azure pixels in the center row with gray pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D array.

    Returns:
        list of lists: The transformed grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = [row[:] for row in input_grid]
    
    # Get the height of the grid
    height = len(input_grid)

    # Locate the center row index
    center_row_index = height // 2

    # Iterate through the pixels in the center row
    for i in range(len(output_grid[center_row_index])):
      # Check if color is azure (8)
      if input_grid[center_row_index][i] == 8:
        #change to gray (5)
        output_grid[center_row_index][i] = 5

    # Return the modified grid
    return output_grid