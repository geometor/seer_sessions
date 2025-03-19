"""
1.  **Identify Gray Pixels:** Find all gray pixels.
2.  **Recolor to Red:** Change the color of all identified gray pixels to red.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Gray Pixels
    gray_pixels = find_pixels(input_grid, 5)

    # 2. Recolor Gray to Red
    for r, c in gray_pixels:
        output_grid[r, c] = 2

    return output_grid