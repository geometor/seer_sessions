"""
1.  Identify 3x3 Blocks: Examine the input grid to find all 3x3 blocks of uniform, non-zero color.
2.  Check Edge Condition: For each identified 3x3 block, determine if it's located at the *top-left corner* of the input grid (row 0, column 0).
3.  Add a row at bottom: If a 3x3 block meets the above criteria, add one row to the *bottom* of the output grid.
4.  The new row color: The color of this added row will be the same as the color of the 3x3 block at the top-left.
5.  If no such 3x3 blocks exists meeting the criteria at the top-left, then there is no change.
"""

import numpy as np

def find_3x3_blocks(grid):
    """Finds all 3x3 blocks of uniform color in the grid."""
    rows, cols = grid.shape
    blocks = []
    for r in range(rows - 2):
        for c in range(cols - 2):
            block = grid[r:r+3, c:c+3]
            if np.all(block == block[0,0]) and block[0,0] != 0:
                blocks.append((r, c, block[0,0]))
    return blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find 3x3 blocks
    blocks = find_3x3_blocks(input_grid)

    # Check for top-left 3x3 block and add row if found
    for r, c, color in blocks:
        if r == 0 and c == 0:
            new_row = np.full(cols, color)
            output_grid = np.vstack([output_grid, new_row])
            break # Only one row is added based on the top-left rule

    return output_grid.tolist()