"""
The transformation selects a contiguous block of columns from the input grid and places them in the output grid. The selection criteria changes between groups of all-white columns and all-colored columns:

1.  Identify contiguous blocks: Divide the input grid into contiguous blocks of columns where all pixels within each column share the same color.
2.  White Block Selection/Mirroring: If a block is all white (color 0), select a portion of the beginning columns from the block, and then append a mirrored copy of these beginning columns.
3.  Colored Block Selection: If a block contains non-zero colors, select the right-most columns of the block.
4. The width of the selection appears related to the width of the non-white region.
"""

import numpy as np

def get_contiguous_blocks(grid):
    """
    Divides the grid into contiguous blocks of columns with the same color.
    Returns a list of tuples, where each tuple contains the start and end column index of a block.
    """
    blocks = []
    num_cols = grid.shape[1]
    start_col = 0
    for i in range(1, num_cols):
        if np.any(grid[:, i] != grid[:, start_col]):
            blocks.append((start_col, i - 1))
            start_col = i
    blocks.append((start_col, num_cols - 1))  # Add the last block
    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    num_rows = input_grid.shape[0]
    blocks = get_contiguous_blocks(input_grid)
    output_grid_columns = []

    for start_col, end_col in blocks:
        block = input_grid[:, start_col:end_col + 1]
        first_col_color = block[0, 0]  # Get the color of the first column in the block

        if first_col_color == 0:  # White block
            # Select a portion and mirror
            portion_width = (end_col - start_col + 1) //2 + (end_col - start_col + 1) % 2 # integer division and add remainder.
            selected_portion = block[:, :portion_width]
            mirrored_portion = np.fliplr(selected_portion)
            output_grid_columns.append(selected_portion)
            output_grid_columns.append(mirrored_portion)
        else:  # Colored block
            # Select right-most columns.  The number of columns to select appears to be
            # the total width of this colored block.
            output_grid_columns.append(block)

    # Concatenate the selected columns to create the output grid
    output_grid = np.concatenate(output_grid_columns, axis=1)
    return output_grid