"""
Transforms the input grid by reflecting non-zero pixels across the main diagonal and duplicating them to form 2x2 blocks, with the reflected position as the top-left of the block.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Identify non-zero pixels
            if input_grid[r, c] != 0:
                # Reflect: Swap row and column indices
                reflected_r, reflected_c = c, r

                # Duplicate: Create 2x2 block with reflected position as top-left
                for i in range(2):
                    for j in range(2):
                        if 0 <= reflected_r + i < rows and 0 <= reflected_c + j < cols:
                            output_grid[reflected_r + i, reflected_c + j] = input_grid[r, c]

    return output_grid.tolist()