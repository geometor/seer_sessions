"""
The transformation rule involves identifying the positions of contiguous, non-white blocks in the input grid and creating a new grid where 'green' (3) pixels represent the relative diagonal position of these blocks. The output grid's dimensions are determined by the number of blocks found. If there are 'n' blocks, the output grid is an 'n x n' grid. Each block's relative position in the sequence of detected blocks corresponds to its diagonal index in the output grid.
"""

import numpy as np

def find_blocks(grid):
    """Find contiguous blocks of the same color (excluding white/0)."""
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
    num_blocks = len(blocks)

    # Initialize the output grid with zeros, with dimensions based on the number of blocks.
    output_grid = np.zeros((num_blocks, num_blocks), dtype=int)

    # Place a 'green' (3) pixel on the diagonal for each block.
    for i in range(num_blocks):
        output_grid[i, i] = 3

    return output_grid