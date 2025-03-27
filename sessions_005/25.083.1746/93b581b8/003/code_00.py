"""
Transforms the input grid by reflecting non-zero pixels across the main diagonal and duplicating them to form 2x2 blocks.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting and duplicating non-zero pixels.
    """
    input_grid = np.array(input_grid)  # Ensure numpy array
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Reflect: Swap row and column indices
                reflected_r, reflected_c = c, r

                # Duplicate based on position relative to the main diagonal
                if reflected_r <= reflected_c:  # On or above the main diagonal
                    # Reflected pixel is the bottom-right corner of the 2x2 block
                    for i in range(-1, 1):
                        for j in range(-1, 1):
                            if 0 <= reflected_r + i < rows and 0 <= reflected_c + j < cols:
                                output_grid[reflected_r + i, reflected_c + j] = input_grid[r, c]
                else:  # Below the main diagonal
                    # Reflected pixel is the top-left corner of the 2x2 block
                    for i in range(2):
                        for j in range(2):
                            if 0 <= reflected_r + i < rows and 0 <= reflected_c + j < cols:
                                output_grid[reflected_r + i, reflected_c + j] = input_grid[r, c]

    return output_grid.tolist()