"""
The input grid is rotated 90 degrees counter-clockwise. The positions are then mirrored across a vertical axis that cuts through the center of the grid.

1.  **Rotation:** Rotate the entire grid by 90 degrees counter-clockwise.
2. **Reflection**: Swap elements in the first and last columns.
"""

import numpy as np

def rotate_grid_counter_clockwise(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def reflect_grid_vertically(grid):
    """Reflects the grid across its vertical axis."""
    return np.fliplr(grid)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid) # ensure it is a numpy array

    # Rotate the grid 90 degrees counter-clockwise
    rotated_grid = rotate_grid_counter_clockwise(input_grid)
    
    # Reflect the grid vertically.
    output_grid = reflect_grid_vertically(rotated_grid)

    return output_grid.tolist() # return to list format