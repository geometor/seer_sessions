"""
1.  **Identify the orange pixel:** Locate the pixel with a value of 7 (orange) in the input grid.
2.  **Double the grid width:** Create a new grid with the same height as the original, but twice the width.
3. **Copy the orange:** In the same row where the orange pixel was original, in the new grid, set the corresponding column in the new grid to be 7.
4.  **Mirror the orange pixel:** In the expanded grid, place another orange pixel (7) at the opposite end of the row containing the original orange pixel. Specifically, if the original orange pixel is at `(row, col)`, the new orange pixel will be at `(row, new_width - 1 - col)`.
5.  **Fill remaining cells:** All other cells in the output grid remain white (0).
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return r, c
    return None  # Should not occur in these tasks, but added for safety.

def transform(input_grid):
    # Find the orange pixel
    orange_pixel_coords = find_orange_pixel(input_grid)
    if orange_pixel_coords is None:
      return input_grid
    
    original_row, original_col = orange_pixel_coords

    # Create new grid.
    new_height = input_grid.shape[0]
    new_width = input_grid.shape[1] * 2
    output_grid = np.zeros((new_height, new_width), dtype=int)

    # Copy original to new grid.
    output_grid[original_row, original_col] = 7

    # Mirror the orange pixel.
    mirrored_col = new_width - 1 - original_col
    output_grid[original_row, mirrored_col] = 7

    return output_grid