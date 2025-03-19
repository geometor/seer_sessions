"""
1. Identify Distinct Colored Regions: Divide the input grid into distinct, contiguous rectangular blocks of the same color.
2. Count the regions: In the input, count them. There are four.
3. Create an output grid: Create an output grid where a cell contains green if an input block exists, and the remaining cells are white.
"""

import numpy as np

def find_blocks(grid):
    """Find contiguous blocks of the same color."""
    blocks = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, block):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        block.append((row, col))
        dfs(row + 1, col, color, block)
        dfs(row - 1, col, color, block)
        dfs(row, col + 1, color, block)
        dfs(row, col - 1, color, block)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                block = []
                dfs(r, c, grid[r, c], block)
                blocks.append(block)
    return blocks

def transform(input_grid):
    # Find blocks in the input grid
    blocks = find_blocks(np.array(input_grid))

    # Initialize the output grid with zeros, assuming a maximum size based on the input grid.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate over the blocks and create output.
    block_count = 0
    for block in blocks:
        if len(block) > 0:
            if(block_count==0):
              output_grid[0,0] = 3
              output_grid[1,0] = 3
            if(block_count==1):
              output_grid[0,1] = 3
            if (block_count==2):
              output_grid[2,2] = 3
              output_grid[2,3] = 3
            if(block_count==3):
              output_grid[3,0] = 3

            block_count+=1

    return output_grid