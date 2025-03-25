"""
Expands contiguous blocks of non-white pixels to the left under specific conditions:
- Blocks wider than one pixel expand to the left until blocked.
- Single-pixel blocks expand to the left only if they have a neighbor of the same color to their right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the expansion rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        c = 0
        while c < cols:
            color = input_grid[r, c]
            if color != 0:  # Non-white pixel
                # Check for neighbors to right
                if c + 1 < cols and input_grid[r, c+1] == color:
                    # Expand left
                    c_left = c -1
                    while c_left >= 0 and output_grid[r,c_left] == 0:
                        output_grid[r, c_left] = color
                        c_left -= 1

            c += 1

    return output_grid