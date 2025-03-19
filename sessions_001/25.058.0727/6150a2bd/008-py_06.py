"""
1.  **Rotate:** Rotate the entire input grid 90 degrees counter-clockwise.
2.  **Color/value swap:** after rotation:
    *   The element at [2,0] becomes the element at [0,2].
    *   The element at [2,1] becomes the element at [1,2].
    *   The element at [2,2] becomes the element at [2,2].
    *   The element at [1,0] becomes the element at [0,1].
3.  All other elements become 0.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    input_grid = np.array(input_grid) # convert to numpy array
    rotated_grid = rotate_grid(input_grid)  # Rotate the grid
    output_grid = np.zeros_like(rotated_grid) # initialize to all zeros

    # Perform the color/value swaps based on original, pre-rotated positions
    # use the values before rotation and indices after rotation
    output_grid[0, 2] = input_grid[2,0] # original [2,0]
    output_grid[1, 2] = input_grid[2,1] # original [2,1]
    output_grid[2, 2] = input_grid[2,2] # original [2,2]
    output_grid[0, 1] = input_grid[1,0] # original [1,0]
    
    return output_grid.tolist() # return as list