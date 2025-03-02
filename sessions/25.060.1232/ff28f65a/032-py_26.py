"""
1. **Iterate** through the input grid to find all 2x2 blocks of red (value '2') pixels.
2. **For each** 2x2 red block found:
    a. **Replace** the top-left pixel of the 2x2 red block with a blue pixel (value '1').
    b. **Set** all the pixels within that specific 2x2 red block in the grid to white(0).
3. **Return** the final grid.
"""

import numpy as np

def find_all_2x2_red_blocks(grid):
    # Helper function to find all 2x2 red blocks in a grid
    rows, cols = grid.shape
    blocks = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 2 and grid[i + 1, j] == 2 and
                grid[i, j + 1] == 2 and grid[i + 1, j + 1] == 2):
                blocks.append((i, j))
    return blocks

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find all 2x2 red blocks
    red_blocks = find_all_2x2_red_blocks(input_grid)

    # Iterate through each red block and apply the transformation
    for (i, j) in red_blocks:
        # Replace top-left with blue
        output_grid[i, j] = 1
        # Set the entire 2x2 block to white (0)
        output_grid[i:i+2, j:j+2] = 0

    return output_grid