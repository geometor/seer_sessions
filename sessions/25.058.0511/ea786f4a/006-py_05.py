"""
The transformation rule identifies blue (1) pixel blocks. Only the blue pixels within the top-left 3x3 region of a blue block are changed to white (0). If a blue block is smaller than 3x3, all of its pixels are changed to white. If a blue pixel is not part of the top-left 3x3 region of a blue block, its color remains unchanged.
"""

import numpy as np

def find_blue_blocks(grid):
    """
    Finds contiguous blocks of blue (1) pixels in the grid.
    Returns a list of blocks, where each block is a list of (row, col) coordinates.
    """
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, current_block):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != 1):
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 1 and not visited[r, c]:
                current_block = []
                dfs(r, c, current_block)
                blocks.append(current_block)
    return blocks

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find all blue blocks.
    blue_blocks = find_blue_blocks(input_grid)

    # Iterate through each blue block.
    for block in blue_blocks:
        # Find the top-left corner of the block (minimum row and column).
        min_row = min(pixel[0] for pixel in block)
        min_col = min(pixel[1] for pixel in block)

        # Change pixels within the 3x3 top-left region to white.
        for row in range(min_row, min(min_row + 3, input_grid.shape[0])):
            for col in range(min_col, min(min_col + 3, input_grid.shape[1])):
                if (row,col) in block:
                    output_grid[row, col] = 0

    return output_grid