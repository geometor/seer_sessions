"""
1.  **Create Output Grid:** Create an output grid with the exact same dimensions (height and width) as the input grid.
2.  **Draw Border:** Fill the entire outer perimeter (top, bottom, left, and right edges) of the output grid with red pixels (color value 2).
3.  **Copy Objects:** Iterate through every pixel in the *input* grid. If a pixel is *not* the background color (0), copy its color value to the *same* position (row, column) in the output grid.
4.  **Fill Background:** Iterate through the output grid. For any cell not on the border, and not containing a copied color, set the pixel value to 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input grid
    output_grid = np.zeros_like(input_grid, dtype=int)
    height, width = output_grid.shape

    # Draw border
    for row in range(height):
        for col in range(width):
            if row == 0 or row == height - 1 or col == 0 or col == width - 1:
                output_grid[row, col] = 2

    # Copy non-background pixels
    for row in range(height):
        for col in range(width):
            if input_grid[row, col] != 0:
                output_grid[row, col] = input_grid[row, col]
            elif not (row == 0 or row == height - 1 or col == 0 or col == width - 1):
                output_grid[row,col] = 0

    return output_grid