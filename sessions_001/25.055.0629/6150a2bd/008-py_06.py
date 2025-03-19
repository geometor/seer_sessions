"""
1. Rotate the Grid: Rotate the entire input grid by 180 degrees clockwise. This means the top-left element becomes the bottom-right, the top-right becomes the bottom-left, etc.

2. Color Swap: Perform the following color substitutions based on the rotated grid:
    *   If a pixel is '1' (blue), change it to '5'(grey).
    *   If a pixel is '2' (red), change it to '1' (blue).
    *  If a pixel is '5'(grey), change it to '2'(red).
    All other colors remain unchanged.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 180 degrees clockwise."""
    return np.rot90(grid, 2)

def color_swap(val):
    """Performs the color swap."""
    if val == 1:
        return 5
    elif val == 2:
        return 1
    elif val == 5:
        return 2
    else:
        return val

def transform(input_grid):
    # initialize output_grid
    output_grid = np.array(input_grid)
    
    # Rotate the grid 180 degrees
    output_grid = rotate_grid(output_grid)

    # Apply color swap
    it = np.nditer(output_grid, flags=['multi_index'], op_flags=['readwrite'])
    for x in it:
      output_grid[it.multi_index] = color_swap(int(x))

    return output_grid.tolist()