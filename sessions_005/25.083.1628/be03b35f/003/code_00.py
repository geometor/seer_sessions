"""
1.  **Identify the Top-Left Object:** Find the largest connected region of
    pixels, starting from the top-left corner (0,0) of the input grid, where all
    pixels within this region are either blue (1) or white (0).  "Connected"
    means adjacent horizontally or vertically.
2.  **Determine Bounding Box:** Find the minimum row, maximum row, minimum
    column, and maximum column of the top-left object identified in step 1.
3.  **Extract Sub-grid:** Extract the sub-grid defined by the bounding box. The
    output grid's dimensions will be (max_row - min_row + 1) x (max_col -
    min_col + 1).
4.  **Copy Pixels:** Copy the pixel values within the bounding box from the
    input grid to the corresponding positions in the new output grid.
5.  The expected output dimensions should be 2x2.
"""

import numpy as np

def get_bounding_box(grid):
    """Helper function to find the bounding box of connected blue/white pixels."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    visited = set()

    def dfs(row, col):
        nonlocal min_row, min_col, max_row, max_col
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] not in (0, 1):
            return

        visited.add((row, col))
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        # Explore adjacent cells
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    dfs(0, 0)  # Start DFS from the top-left corner

    if max_row == -1: # Handle edge case of no object at top-left
      return 0,0,0,0
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid by extracting the top-left object."""
    input_grid = np.array(input_grid)

    # Determine bounding box of the top-left object
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Calculate output grid dimensions
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # Create output grid and copy pixels
    output_grid = np.zeros((height, width), dtype=int)

    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col + 1):
        output_grid[r - min_row, c - min_col] = input_grid[r, c]

    return output_grid.tolist()