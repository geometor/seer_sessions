"""
Changes zeros to ones within a 2x2 block of ones.
"""

import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of ones in the grid."""
    rows, cols = grid.shape
    blocks = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if grid[i, j] == 1 and grid[i + 1, j] == 1 and grid[i, j + 1] == 1 and grid[i + 1, j + 1] == 1:
                blocks.append((i, j))
    return blocks

def transform(input_grid):
    """Transforms the input grid by changing zeros to ones if they are inside a 2x2 block of ones."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find 2x2 blocks of ones
    blocks = find_2x2_blocks(input_grid)

    # Iterate through the blocks
    for block_row, block_col in blocks:
      # Check surrounding zero pixels
      if input_grid[block_row+1, block_col ] == 0:
          output_grid[block_row+1, block_col] = 1
      if input_grid[block_row, block_col+1 ] == 0:
          output_grid[block_row, block_col+1] = 1
      if input_grid[block_row-1, block_col ] == 0:
          output_grid[block_row-1, block_col] = 1
      if input_grid[block_row, block_col -1] == 0:
          output_grid[block_row, block_col - 1] = 1

      if input_grid[block_row + 1, block_col+1] == 0:
        output_grid[block_row+1,block_col+1] = 1
      if input_grid[block_row - 1, block_col -1] == 0:
        output_grid[block_row - 1,block_col - 1] = 1
      if input_grid[block_row-1, block_col+1 ] == 0:
          output_grid[block_row-1, block_col+1] = 1
      if input_grid[block_row+1, block_col -1] == 0:
          output_grid[block_row+1, block_col - 1] = 1

    return output_grid.tolist()