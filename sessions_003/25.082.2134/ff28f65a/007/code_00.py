"""
Detects 2x2 red blocks in the input grid and represents their presence with '1's in a smaller output grid. The output grid's dimensions are one less than the input grid's dimensions. Each cell in the output grid corresponds to the top-left corner of a potential 2x2 red block in the input grid.
"""

import numpy as np

def find_red_blocks(input_grid):
    """Finds all 2x2 blocks of red (value 2) pixels in the input grid."""
    red_blocks = []
    for r in range(input_grid.shape[0] - 1):
        for c in range(input_grid.shape[1] - 1):
            if (input_grid[r, c] == 2 and input_grid[r + 1, c] == 2 and
                input_grid[r, c + 1] == 2 and input_grid[r + 1, c + 1] == 2):
                red_blocks.append((r, c))  # Store the top-left corner coordinates
    return red_blocks

def transform(input_grid):
    input_grid = np.array(input_grid)
    # Find Red Block positions
    red_blocks = find_red_blocks(input_grid)

    # Determine output grid dimensions.
    output_height = input_grid.shape[0] - 1
    output_width = input_grid.shape[1] - 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid.
    for r, c in red_blocks:
        output_grid[r, c] = 1

    return output_grid.tolist()