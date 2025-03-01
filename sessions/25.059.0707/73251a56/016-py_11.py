"""
Identifies a main shape composed of various colors and removes all pixels of a specific target color (white/0) within that shape, leaving other colors unchanged.
"""

import numpy as np

def find_main_shape_bounds(grid):
    # Find the min and max row and col indices that contain non-background colors
    rows, cols = np.where(grid >= 0)  # Assuming any color is part of the shape.
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Removes white (0) pixels from within main shape.

    Args:
        input_grid: The input grid as a 2D numpy array.

    Returns:
        The transformed grid as a 2D numpy array.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find bounding box of main shape
    (min_row, min_col), (max_row, max_col) = find_main_shape_bounds(input_grid)

    # Iterate over the pixels within the bounding box.
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            # Check if the pixel is white (0).
            if output_grid[i, j] == 0:
                # Remove the white pixel (in this case, by setting to backgound which in effect is removing it)
                output_grid[i,j] = 0 # essentially does nothing, but illustrates the point
    return output_grid