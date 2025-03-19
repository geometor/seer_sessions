"""
1.  **Object Detection:** Find all 2x2 blocks of pixels with the same, non-zero color.
2.  **Transformation:** Copy each identified 2x2 block of pixels to the output grid, maintaining its original position and color.  All other pixels in the output grid should be 0.
"""

import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of the same non-zero color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            color = grid[r, c]
            if (color != 0 and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                blocks.append((r, c, color))
    return blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find 2x2 blocks
    blocks = find_2x2_blocks(input_grid)

    # Copy 2x2 blocks to output grid
    for r, c, color in blocks:
        output_grid[r, c] = color
        output_grid[r + 1, c] = color
        output_grid[r, c + 1] = color
        output_grid[r + 1, c + 1] = color

    return output_grid