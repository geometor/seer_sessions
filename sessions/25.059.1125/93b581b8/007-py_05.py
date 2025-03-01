"""
1.  **Identify:** Locate a 2x2 block of non-zero pixels within the input grid.
2.  **Extract:** Note the colors of each pixel in the 2x2 block: top-left, top-right, bottom-left, and bottom-right.
3.  **Mirror and Place:**
    *   Copy the color of the *bottom-right* pixel of the 2x2 block to *all* cells of the top-left 2x2 corner of the output grid.
    *   Copy the color of the *top-left* pixel of the 2x2 block to *all* cells of the bottom-right 2x2 corner of the output grid.
    *   Copy the color of the *bottom-left* pixel of the 2x2 block to *all* cells of the top-right 2x2 corner of the output grid.
    *  Copy the color of the *top-right* pixel of the 2x2 block to *all* cells of the bottom-left 2x2 corner of the output grid.
4. If no 2x2 block of non-zero pixels is found the output grid is the same as the input grid.
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
       return output_grid.tolist()

    # Mirror top-left
    color_tl = block_2x2['bottom_right'][0]
    output_grid[0:2, 0:2] = color_tl

    # Mirror lower-right
    color_lr = block_2x2['top_left'][0]
    output_grid[rows-2:rows, cols-2:cols] = color_lr

    # Mirror top right
    color_tr = block_2x2['bottom_left'][0]
    output_grid[0:2, cols-2:cols] = color_tr

    # Mirror lower left
    color_ll = block_2x2['top_right'][0]
    output_grid[rows-2:rows, 0:2] = color_ll

    return output_grid.tolist()