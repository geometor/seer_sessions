```python
"""
Identify contiguous blocks of '7's. Iterate through the grid. Inside '7' blocks,
revert other numbers to '7'. In the lower part of the grid (starting from the
height of '7' blocks extending to the bottom), change most isolated digits
to '7', except in columns 9-14. Retain other digits.
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
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    blocks_of_7 = find_blocks(input_grid, 7)

    # Find the minimum height of '7' blocks that extend to the bottom
    min_bottom_block_height = input_grid.shape[0]
    for block in blocks_of_7:
      min_row, max_row, _, _ = get_block_bounds(block)
      if max_row == input_grid.shape[0] - 1:
          min_bottom_block_height = min(min_bottom_block_height, min_row)

    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            # Revert to '7' inside blocks
            inside_block = False
            for block in blocks_of_7:
                if (row, col) in block:
                    inside_block = True
                    break
            if inside_block:
                if input_grid[row,col] != 7:
                    output_grid[row, col] = 7
            elif row >= min_bottom_block_height: # lower_part
                if not (9 <= col <= 14): # keep digits on columns 9 to 14
                    output_grid[row,col] = 7

    return output_grid
```