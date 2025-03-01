"""
The transformation rule is to replace green (3) pixels with red (2) pixels within a rectangular shape defined by red (2) pixels, but only if the interior of that shape contains only green and red pixels. If other colors are present inside the shape, the transformation does not occur.
"""

import numpy as np

def find_shape(grid):
    # Find red pixels
    red_pixels = np.where(grid == 2)
    if len(red_pixels[0]) == 0:  # if the tuples are empty, there are no red pixels
        return None, None, None, None

    # define bounds
    min_row, max_row = np.min(red_pixels[0]), np.max(red_pixels[0])
    min_col, max_col = np.min(red_pixels[1]), np.max(red_pixels[1])
    
    return min_row, max_row, min_col, max_col

def check_interior_colors(grid, min_row, max_row, min_col, max_col):
    """Checks if the interior of the bounding box contains only red and green pixels."""
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if grid[i, j] != 2 and grid[i, j] != 3:
                return False  # Found a color other than red or green
    return True

def transform(input_grid):
    """
    Transforms the input grid by changing green pixels to red within a rectangular shape
    defined by red pixels, but only if the interior contains only red and green.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the bounding box of the shape defined by red pixels
    min_row, max_row, min_col, max_col = find_shape(input_grid)
    
    if min_row is None: # Handle the case where there's no shape
        return output_grid

    # Check if the interior of the shape contains only red and green pixels
    if check_interior_colors(input_grid, min_row, max_row, min_col, max_col):
        # Iterate through the bounding box and change green to red
        for i in range(min_row, max_row + 1):
            for j in range(min_col, max_col + 1):
                if output_grid[i, j] == 3:  # Check for green pixels
                    output_grid[i, j] = 2  # Change to red

    return output_grid