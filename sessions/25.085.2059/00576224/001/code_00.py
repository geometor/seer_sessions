"""
Transforms a 2x2 input grid into a 6x6 output grid by tiling.
The output grid is composed of a 3x3 arrangement of 2x2 blocks.
The blocks in the first and third rows of the arrangement are copies of the input grid.
The blocks in the second row of the arrangement are horizontally flipped copies of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Tiles a 3x3 grid using the input pattern and its horizontal flip.

    Args:
        input_grid (np.array): A 2x2 numpy array representing the input grid.

    Returns:
        np.array: A 6x6 numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    input_block = np.array(input_grid)
    input_height, input_width = input_block.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Create the horizontally flipped version of the input block
    flipped_block = np.fliplr(input_block)

    # Initialize the output grid with zeros (or any placeholder)
    # Use the dtype of the input grid to maintain consistency
    output_grid = np.zeros((output_height, output_width), dtype=input_block.dtype)

    # Tile the output grid according to the pattern
    # Iterate through the 3x3 block grid structure
    for block_row in range(3):
        for block_col in range(3):
            # Determine which block to use (original or flipped)
            if block_row == 1:  # Middle row uses the flipped block
                current_block = flipped_block
            else:  # Top and bottom rows use the original input block
                current_block = input_block

            # Calculate the top-left corner coordinates for placing the current block
            start_row = block_row * input_height
            start_col = block_col * input_width

            # Place the current block into the output grid
            output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = current_block

    return output_grid
