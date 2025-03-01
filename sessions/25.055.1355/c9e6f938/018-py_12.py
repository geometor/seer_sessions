"""
1.  **Expand the Grid:** Create an output grid that is two rows taller and two columns wider than the input grid. Initialize all cells in the output grid to black (0).
2.  **Find and Mirror Orange Pixels:** Locate each orange pixel (7) in the input grid.
3.  **Horizontal Mirror:** For each orange pixel found, place an orange pixel in the output grid, two rows down from the original row, and mirrored horizontally. To perform mirroring, place an orange pixel in the output. If an orange pixel is at input[row, col], place an orange at output[row+2, col+2] and at output[row + 2, output_width - col - 1 + 2]
"""

import numpy as np

def find_all_orange_pixels(grid):
    # Find the coordinates of all orange pixels (value 7).
    orange_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                orange_pixels.append((r, c))
    return orange_pixels

def transform(input_grid):
    # Initialize output_grid by adding 2 to both height and width.
    output_grid = np.zeros((input_grid.shape[0] + 2, input_grid.shape[1] + 4), dtype=int)

    # Find all orange pixels in the input grid.
    orange_pixel_coords = find_all_orange_pixels(input_grid)

    for coords in orange_pixel_coords:
      # Place the first orange pixel two rows and columns offset from input.
      output_grid[coords[0] + 2, coords[1] + 2] = 7
      # Mirror the pixel horizontally.
      output_grid[coords[0] + 2, output_grid.shape[1] - coords[1] - 1] = 7

    return output_grid