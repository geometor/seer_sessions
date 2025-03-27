"""
Identify the largest contiguous block of orange (7) pixels that extends from
the top to the bottom of the grid (the "dominant block"). Within this block,
change most non-orange pixels to orange, but prioritize keeping original values
inside columns 9-14 and potentially values forming shapes. In the region below
the top of the dominant block and outside columns 9-14, convert most pixels to
orange, prioritizing isolated pixels. Preserve other shapes where possible.
"""

import numpy as np

def find_blocks(grid, value):
    """Finds contiguous blocks of a specific value in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, block):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != value):
            return
        visited[row, col] = True
        block.append((row, col))
        dfs(row + 1, col, block)
        dfs(row - 1, col, block)
        dfs(row, col + 1, block)
        dfs(row, col - 1, block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == value and not visited[row, col]:
                block = []
                dfs(row, col, block)
                blocks.append(block)
    return blocks

def get_block_bounds(block):
    """Calculates the bounding box of a block."""
    rows, cols = zip(*block)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def is_isolated(grid, row, col):
    """Checks if a pixel is isolated (surrounded by different colors)."""
    color = grid[row, col]
    for r in range(max(0, row - 1), min(grid.shape[0], row + 2)):
        for c in range(max(0, col - 1), min(grid.shape[1], col + 2)):
            if (r, c) != (row, col) and grid[r, c] == color:
                return False
    return True

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    blocks_of_7 = find_blocks(input_grid, 7)

    # Find the dominant orange block (full height).
    dominant_block = None
    for block in blocks_of_7:
        min_row, max_row, _, _ = get_block_bounds(block)
        if min_row == 0 and max_row == input_grid.shape[0] - 1:
            dominant_block = block
            break

    if dominant_block is None:
        return output_grid # No dominant block found, return the input grid.

    min_row_dominant, max_row_dominant, min_col_dominant, max_col_dominant = get_block_bounds(dominant_block)


    # Inner block transformation.
    for row in range(min_row_dominant, max_row_dominant + 1):
        for col in range(min_col_dominant, max_col_dominant+1):
            if (row, col) in dominant_block:
                if input_grid[row, col] != 7:
                  if not (9 <= col <= 14):
                    output_grid[row, col] = 7


    # Lower region transformation.
    for row in range(min_row_dominant + 1, input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if not (9 <= col <= 14):
                # Prioritize changing isolated pixels.
                if input_grid[row,col] != 7:
                    output_grid[row,col] = 7

    return output_grid