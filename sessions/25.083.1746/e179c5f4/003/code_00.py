"""
The transformation rule involves creating a checkered pattern of blue (1) and azure (8) pixels in the output grid, based on the location of a single blue pixel in the input. The output grid has the same dimensions as the input grid. The color of each cell in the output grid is determined by the sum of its row and column indices: if (row + col) % 2 is 0, the color is azure (8); otherwise, it's blue (1).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.empty_like(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixel (not needed for the core logic, but kept for potential future use)
    blue_pixels = np.where(input_grid == 1)
    if len(blue_pixels[0]) > 0:
        blue_row, blue_col = blue_pixels[0][0], blue_pixels[1][0]
    else:
        return input_grid


    # Generate checkered pattern
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = 8  # Azure
            else:
                output_grid[r, c] = 1  # Blue

    return output_grid