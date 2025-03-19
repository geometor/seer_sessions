"""
Extract the 2x2 yellow square from the input grid.
"""

import numpy as np

def find_shape(grid, color, shape_type=None, dimensions=None):
    """
    Finds a shape within a grid based on color, and optionally, type and dimensions.
    Returns the top-left coordinate of the first matching shape found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                if shape_type == 'rectangle' and dimensions:
                    width, height = dimensions
                    if r + height <= rows and c + width <= cols:
                        subgrid = grid[r:r+height, c:c+width]
                        if np.all(subgrid == color):
                            return (r, c)
                elif shape_type is None: #any shape
                    return (r,c)
    return None

def transform(input_grid):
    """
    Transforms the input grid by extracting the 2x2 yellow square.
    """
    # Find the top-left corner of the 2x2 yellow square.
    yellow_square_start = find_shape(input_grid, color=4, shape_type='rectangle', dimensions=(2, 2))

    # Initialize the output grid as an empty 2x2 array (filled with zeros by default).
    output_grid = np.zeros((2, 2), dtype=int)

    if yellow_square_start:
        # Extract the 2x2 yellow square.
        r, c = yellow_square_start
        output_grid = input_grid[r:r+2, c:c+2].copy()

    return output_grid