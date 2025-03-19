"""
1.  **Identify** all contiguous blocks of yellow (4) pixels in the input grid.
2.  **For each yellow block**:
    *   **If** the block forms a 2x2 square, replace all yellow pixels in the square with magenta (6).

3.  **Retain** all other pixels in their original colors and positions.
4.  **Output** the modified grid.
"""

import numpy as np

def find_yellow_blocks(grid):
    # Find contiguous blocks of yellow pixels
    yellow_blocks = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_block):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != 4:
            return
        visited.add((r, c))
        current_block.append((r, c))
        dfs(r + 1, c, current_block)
        dfs(r - 1, c, current_block)
        dfs(r, c + 1, current_block)
        dfs(r, c - 1, current_block)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4 and (r, c) not in visited:
                current_block = []
                dfs(r, c, current_block)
                yellow_blocks.append(current_block)
    return yellow_blocks

def is_2x2_square(block):
    # Check if a block is a 2x2 square
    if len(block) != 4:
      return False

    rows = [p[0] for p in block]
    cols = [p[1] for p in block]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    return (max_row - min_row == 1) and (max_col - min_col == 1)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    yellow_blocks = find_yellow_blocks(input_grid)

    for block in yellow_blocks:
        # check and modify 2x2 squares
        if is_2x2_square(block):
            for r, c in block:
                output_grid[r, c] = 6

    return output_grid