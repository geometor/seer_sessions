"""
1.  **Initialization:** Start with an output grid that is the same size as the input grid, filled with all zeros (white).
2.  **Locate Green Pixels:** Find *all* pixels with the value '3' (green) in the input grid.
3.  **Iterate:** For *each* green pixel found:
    a. **Create Red Square:** Create a 3x3 square of pixels with the value '2' (red) in the output grid.
    b. **Position:** Center the red square on the location in the output grid that corresponds to the location of the current green pixel in the input grid.
    c. **Overwrite Center:** Set the pixel at the *center* of this red square to '3' (green).
4. **Default Output:** If *no* green pixels are found in the input grid, the output grid remains all zeros (white).
"""

import numpy as np

def get_multiple_pixel_locations(grid, color):
  """find all coordinate pairs for the matching color
  """
  coords = np.where(grid == color)
  return list(zip(coords[0],coords[1]))

def transform(input_grid):
    # initialize output_grid as all zeros with the same dimensions
    output_grid = np.zeros_like(input_grid)

    # Find all locations of the green pixel (value 3).
    green_pixel_locations = get_multiple_pixel_locations(input_grid, 3)

    # Iterate through all green pixel locations
    for row, col in green_pixel_locations:
        # Create the 3x3 red square (value 2).
        for i in range(max(0, row - 1), min(output_grid.shape[0], row + 2)):
            for j in range(max(0, col - 1), min(output_grid.shape[1], col + 2)):
                output_grid[i, j] = 2

        # Overwrite the center with green (value 3).
        output_grid[row, col] = 3

    return output_grid