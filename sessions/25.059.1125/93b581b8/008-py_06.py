"""
Identify a 2x2 block of non-zero colored pixels in the input grid.  Mirror the colors of this block to the other corners of the grid, creating new 2x2 blocks. If no such block exists, return a copy of input.
"""

import numpy as np

def get_2x2_block(grid):
    """Identifies the 2x2 block of non-zero pixels and returns their colors and positions."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            block = grid[r:r+2, c:c+2]
            if np.all(block != 0):
                return {
                    "top_left": (block[0, 0], (r, c)),
                    "top_right": (block[0, 1], (r, c + 1)),
                    "bottom_left": (block[1, 0], (r + 1, c)),
                    "bottom_right": (block[1, 1], (r + 1, c + 1)),
                }
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find 2 x 2 block
    block_2x2 = get_2x2_block(input_grid)
    if not block_2x2:
       return output_grid.tolist() # Return input copy if no 2x2 block

    # Mirror bottom-right to top-left
    color_tl = block_2x2['bottom_right'][0]
    output_grid[0:2, 0:2] = color_tl

    # Mirror top-left to lower-right
    color_lr = block_2x2['top_left'][0]
    output_grid[rows-2:rows, cols-2:cols] = color_lr

    # Mirror bottom-left to top right
    color_tr = block_2x2['bottom_left'][0]
    output_grid[0:2, cols-2:cols] = color_tr

    # Mirror top-right to lower left
    color_ll = block_2x2['top_right'][0]
    output_grid[rows-2:rows, 0:2] = color_ll

    return output_grid.tolist()