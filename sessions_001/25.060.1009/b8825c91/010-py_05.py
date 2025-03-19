"""
Iterate through each pixel in the input grid.
If a pixel and its neighbor to the south have color 4, and the pixel to the east has any color other than 4, change color 4 in the original pixel to 1.
If a pixel and its neighbor to the south have color 4, and the pixel to the east also has color 4, do not change the color.
Leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check conditions for color change
            if input_grid[r, c] == 4:  # Current pixel is yellow
                south_neighbor = input_grid[r + 1, c] if r + 1 < rows else None
                east_neighbor = input_grid[r, c + 1] if c + 1 < cols else None

                if south_neighbor == 4:
                    if east_neighbor != 4:
                        output_grid[r,c] = 1

    return output_grid