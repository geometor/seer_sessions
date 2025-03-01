"""
The transformation identifies the location of orange (7) pixels in the input grid.  If an orange pixel is found, a 3x3 cross of orange pixels is created in the output grid, centered at the location of the *input* orange pixel.  If there are multiple orange pixels, a cross is created for each. The crosses are created by coloring orange the pixels directly above/below and left/right of the original orange pixel. If no orange pixel is present, the grid remains all black (0). If multiple crosses overlap, the overlapping pixels remain orange.
"""

import numpy as np

def find_orange_pixels(grid):
    # Find the coordinates of all orange pixels (value 7)
    orange_pixels = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 7:
                orange_pixels.append((r, c))
    return orange_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all orange pixels
    orange_pixels = find_orange_pixels(input_grid)

    # Create a 3x3 cross for each orange pixel
    for row, col in orange_pixels:
        # Color the center pixel
        if 0 <= row < len(output_grid) and 0 <= col < len(output_grid[0]):
          output_grid[row][col] = 7

        # Color above and below, ensuring bounds
        if 0 <= row - 1 < len(output_grid):
            output_grid[row - 1][col] = 7
        if 0 <= row + 1 < len(output_grid):
          output_grid[row + 1][col] = 7

        # Color left and right ensuring bounds
        if 0 <= col - 1 < len(output_grid[0]):
            output_grid[row][col - 1] = 7

        if 0 <= col + 1 < len(output_grid[0]):
          output_grid[row][col+1] = 7

    return output_grid