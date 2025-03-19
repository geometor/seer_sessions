"""
Identify the contiguous block of yellow pixels in the input grid and extract it to create the output grid.
"""

import numpy as np

def find_contiguous_block(grid, color):
    """
    Finds the top-left and bottom-right coordinates of a contiguous block of the given color.
    """
    rows, cols = grid.shape
    top_left = None
    bottom_right = None

    # Find top-left
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                top_left = (r, c)
                break
        if top_left:
            break

    if not top_left:
        return None, None

    # Find bottom-right
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == color:
                bottom_right = (r, c)
                break
        if bottom_right:
            break

    return top_left, bottom_right

def transform(input_grid):
    """
    Transforms the input grid by extracting the contiguous yellow block.
    """
    # Find the top-left and bottom-right corners of the yellow block.
    top_left, bottom_right = find_contiguous_block(input_grid, color=4)

    if top_left is None or bottom_right is None:
        return np.zeros((1,1), dtype=int) # Return an empty array (or appropriate default)

    # Calculate the dimensions of the block.
    height = bottom_right[0] - top_left[0] + 1
    width = bottom_right[1] - top_left[1] + 1

    # Initialize the output grid with the correct dimensions.
    output_grid = np.zeros((height, width), dtype=int)

    # Extract the yellow block.
    r_start, c_start = top_left
    output_grid = input_grid[r_start:r_start+height, c_start:c_start+width].copy()

    return output_grid