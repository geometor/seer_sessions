"""
The transformation rule involves identifying a 2x2 central block in the input grid, copying it to the same location in the output grid, rotating it 90 degrees clockwise, and then placing copies of the rotated block in the four 2x2 corners of the output grid.
"""

import numpy as np

def get_central_block(grid):
    """Extracts the 2x2 central block from the input grid."""
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return grid[center_row-1:center_row+1, center_col-1:center_col+1]

def rotate_block(block):
    """Rotates a 2x2 block 90 degrees clockwise."""
    return np.array([[block[1,0], block[0,0]], [block[1,1], block[0,1]]])

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Initialize output grid with zeros, same size/type as input
    output_grid = np.zeros_like(input_grid)

    # Get the central 2x2 block
    central_block = get_central_block(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2
    
    # set the center 2x2 block to be same
    output_grid[center_row-1:center_row+1, center_col-1:center_col+1] = central_block

    # Rotate the central block
    rotated_block = rotate_block(central_block)
    
    # Place in the four corners
    output_grid[0:2, 0:2] = rotated_block  # Top-left
    output_grid[0:2, cols-2:cols] = rotated_block # Top-right
    output_grid[rows-2:rows, 0:2] = rotated_block  # Bottom-left
    output_grid[rows-2:rows, cols-2:cols] = rotated_block  # Bottom-right

    return output_grid