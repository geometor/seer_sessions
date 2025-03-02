"""
The transformation rule is a 180-degree rotation of the input grid.  This can be achieved by either flipping the grid vertically and then horizontally, or vice-versa.
"""

import numpy as np

def rotate_180(grid):
    """Rotates a 2D numpy array by 180 degrees."""
    return np.rot90(grid, 2)

def transform(input_grid):
    # initialize output_grid as a numpy array
    input_np = np.array(input_grid)

    # rotate the grid by 180
    output_np = rotate_180(input_np)
    
    # Convert back to list of lists
    output_grid = output_np.tolist()

    return output_grid