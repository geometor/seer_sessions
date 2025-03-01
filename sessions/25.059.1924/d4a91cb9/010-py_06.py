"""
The azure (8) pixel remains unchanged. The red (2) pixel is replaced by a horizontal path of yellow (4) pixels extending to the right, stopping one column before the azure (8) pixel.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find the coordinates of a pixel with a specific color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the azure (8) pixel
    azure_pixel = find_pixel_by_color(input_grid, 8)

    # Find the red (2) pixel
    red_pixel = find_pixel_by_color(input_grid, 2)

    # If both pixels are found, proceed with the transformation
    if azure_pixel and red_pixel:
        # Azure pixel remains unchanged, so no action needed

        # Create a horizontal path of yellow (4) pixels
        red_row, red_col = red_pixel
        azure_row, azure_col = azure_pixel
        for col in range(red_col, azure_col):
            output_grid[red_row, col] = 4

    return output_grid