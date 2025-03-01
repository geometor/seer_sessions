"""
The transformation rule involves extending the orange object (color 7) horizontally to create a three-pixel wide object, centered on the original orange pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending orange object horizontally.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Find the coordinates of orange pixels
    orange_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
                orange_pixels.append((r, c))

    # Extend horizontally
    for r, c in orange_pixels:
        if c > 0:
          output_grid[r, c-1] = 7
        
        output_grid[r,c] = 7 #ensure original is there

        if c < cols - 1:
          output_grid[r, c+1] = 7

    return output_grid