"""
1.  **Locate Red Pixel:** Identify the single red pixel (color value 2) within the input grid.
2.  **Create Bounding Box:** Define a 3x3 square region (BoundingBox) centered on the location of the red pixel. The edges of this square should not extend beyond the boundaries of the input grid.
3.  **Apply Transformation:** Change all pixels within the BoundingBox to blue (color value 1).
4.  **Preserve Red Pixel:** The original red pixel at the center of the BoundingBox retains its original color (2).
"""

import numpy as np

def find_pixel_location(grid, color):
    # Find the location of a pixel of the specified color.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the location of the red pixel (color 2).
    red_pixel_location = find_pixel_location(input_grid, 2)

    if red_pixel_location is None:
        return output_grid
    
    red_row, red_col = red_pixel_location

    # Define the bounds of the 3x3 square around the red pixel.
    start_row = max(0, red_row - 1)
    end_row = min(input_grid.shape[0], red_row + 2)  # Exclusive upper bound
    start_col = max(0, red_col - 1)
    end_col = min(input_grid.shape[1], red_col + 2)  # Exclusive upper bound

    # Iterate through the 3x3 square and change all pixels to blue (1).
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            output_grid[i, j] = 1  # Turn the pixel to blue
    output_grid[red_row, red_col] = 2  # Keep the red pixel unchanged.

    return output_grid