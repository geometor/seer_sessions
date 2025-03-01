"""
The transformation identifies the red pixels within the input grid, determines the smallest blue bounding box 
enclosing those red pixels, and then reproduces the red pixels' relative positions within a fixed-size 5x17 blue output grid.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds the coordinates of all red pixels in the grid."""
    return np.argwhere(grid == 2)

def get_blue_bounding_box(grid, red_pixels):
    """Finds the smallest blue bounding box containing all red pixels."""
    if len(red_pixels) == 0:
        return 0, 0, 0, 0
    
    min_r, min_c = red_pixels.min(axis=0)
    max_r, max_c = red_pixels.max(axis=0)

    # Expand to find the blue borders
    while min_r > 0 and grid[min_r-1, min_c] == 1:
        min_r -= 1
    while max_r < grid.shape[0]-1 and grid[max_r+1, min_c] == 1:
        max_r += 1
    while min_c > 0 and grid[min_r, min_c - 1] == 1:
        min_c -= 1
    while max_c < grid.shape[1] -1 and grid[min_r, max_c+1] == 1:
        max_c += 1
    
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Red Pixels
    red_pixels = get_red_pixels(input_grid)

    # 2. Find Minimum Blue Bounding Box
    min_r, max_r, min_c, max_c = get_blue_bounding_box(input_grid, red_pixels)
   

    # 3. Create Output Grid: 5x17 filled with blue (1)
    output_grid = np.ones((5, 17), dtype=int)

    # 4. Map Red Pixels (maintain relative positions)
    for r, c in red_pixels:
        # Calculate relative position with respect to blue box
        relative_r = r - min_r
        relative_c = c - min_c

        # Place red pixel in output grid if it fits, will only work with a bounding box
        # with a height of less than 5 and width of less than 17.  Otherwise will
        # place pixels out of bounds.
        if relative_r < 5 and relative_c < 17:
          output_grid[relative_r, relative_c] = 2

    # 5. Return the output grid.
    return output_grid.tolist()