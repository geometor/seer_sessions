"""
Preserve gray pixels and use original red pixels to expand upward to fill the whole column, and spread horizontally adjacent to the gray.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the locations of gray (5) pixels.  These remain unchanged.
    gray_pixels = np.where(input_grid == 5)

    # Find original red pixels in the bottom row
    bottom_row_red_pixels = np.where(input_grid[-1, :] == 2)[0]

    # Expand red upwards
    for col in bottom_row_red_pixels:
        output_grid[:, col] = 2

    # Gray Influence - horizontal spread of adjacent reds
    for r, c in zip(gray_pixels[0], gray_pixels[1]):
        if c > 0:
          if output_grid[r, c-1] == 0:
            output_grid[r, c - 1] = 2
        if c < cols - 1:
          if output_grid[r, c+1] == 0:
            output_grid[r, c + 1] = 2
    
    return output_grid