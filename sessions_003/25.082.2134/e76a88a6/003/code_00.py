"""
1. Identify 3x3 blocks of gray (color 5).
2. Identify the 3x3 region at the top-left corner of the grid.
3. Replace each identified gray block with corresponding colors from the top-left 3x3 subgrid.
"""

import numpy as np

def find_3x3_gray_blocks(grid):
    """Find the top-left coordinates of all 3x3 gray blocks (all 5s)."""
    gray_blocks = []
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            if np.all(grid[i:i+3, j:j+3] == 5):
                gray_blocks.append((i, j))
    return gray_blocks

def get_top_left_3x3(grid):
    """Extract the 3x3 subgrid from the top-left corner."""
    return grid[:3, :3]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the top-left 3x3 block.
    top_left_3x3 = get_top_left_3x3(input_grid)

    # Find all 3x3 gray blocks.
    gray_blocks = find_3x3_gray_blocks(input_grid)

    # Replace each gray block with the top-left 3x3 block.
    for i, j in gray_blocks:
        output_grid[i:i+3, j:j+3] = top_left_3x3

    return output_grid