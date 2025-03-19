"""
The transformation rule is to replace all green (3) pixels with red (2) pixels within a detected shape, while keeping the red (2) and white (0) pixels unchanged.
"""

import numpy as np

def find_shape(grid):
    # Find non-white pixels
    non_white_pixels = np.where(grid != 0)
    if len(non_white_pixels[0]) == 0:  # if the tuples are empty, it is all white
        return None, None, None, None

    # define bounds
    min_row, max_row = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
    min_col, max_col = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by changing green pixels to red within a detected shape.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the bounding box of the shape
    min_row, max_row, min_col, max_col = find_shape(input_grid)
    
    if min_row is None: # Handle the case where there's no shape
        return output_grid

    # Iterate through the bounding box and change green to red
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if output_grid[i, j] == 3:  # Check for green pixels
                output_grid[i, j] = 2  # Change to red

    return output_grid