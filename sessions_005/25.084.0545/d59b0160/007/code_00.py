"""
1.  **Identify Dominant Block:** Find the largest contiguous block of orange (7) pixels that spans the entire height of the grid (from the top row to the bottom row). This is the "dominant block".

2.  **Inner Block Transformation:** Within the dominant block's column range, change all pixels to orange, *except* for those in columns 9 to 14 (inclusive, 0-indexed).

3. **Transformation Outside Dominant Block's Columns** For all rows:
   * Change to orange any cells not in the columns that define the dominate block's width *except* for those in columns 9 to 14.

4.  **Protected Columns:** No pixels within columns 9 to 14 (0-indexed) should be modified, regardless of other rules.
"""

import numpy as np

def find_blocks(grid, value):
    """Finds contiguous blocks of a specific value in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != value):
            return []  # Return an empty list to combine results properly
        visited[row, col] = True
        block = [(row, col)]  # Start a new block with the current cell
        # Recursively explore neighbors and combine results
        block += dfs(row + 1, col)
        block += dfs(row - 1, col)
        block += dfs(row, col + 1)
        block += dfs(row, col - 1)
        return block

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == value and not visited[row, col]:
                blocks.append(dfs(row, col))
    return blocks

def get_block_bounds(block):
    """Calculates the bounding box of a block."""
    rows, cols = zip(*block)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
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
        for col in range(min_col_dominant, max_col_dominant + 1):
            if (row, col) in dominant_block:
                if not (9 <= col <= 14):
                    output_grid[row, col] = 7

    # Lower region transformation.
    for row in range(max_row_dominant + 1, input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if not (9 <= col <= 14):
                output_grid[row, col] = 7

    # Upper region transformation
    for row in range(0, max_row_dominant + 1):
        for col in range(input_grid.shape[1]):
            if not (9 <= col <= 14):
                if not (min_col_dominant <= col <= max_col_dominant and (row,col) in dominant_block):
                  output_grid[row,col] = 7

    return output_grid