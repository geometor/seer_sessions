"""
Find the azure (8) pixel. Crop a 5x5 square centered on it, excluding any
pixels that were a part of the blue cross in the original image.
"""

import numpy as np

def find_pixel_location(grid, color):
    # Find the location of a pixel with a specific color.
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return [r, c]
    return None

def get_blue_pixels(grid):
    # Find all blue pixels in the grid
    blue_pixels = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == 1:
                blue_pixels.append((r, c))
    return blue_pixels

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find the location of the azure pixel (color 8).
    azure_location = find_pixel_location(input_grid, 8)

    # Get the locations of all blue pixels.
    blue_pixels = get_blue_pixels(input_grid)

    # Determine the boundaries of the 5x5 crop centered on the azure pixel.
    row_start = azure_location[0] - 2
    row_end = azure_location[0] + 3
    col_start = azure_location[1] - 2
    col_end = azure_location[1] + 3

    # Create an empty output grid.
    output_grid = np.zeros((5, 5), dtype=int)

    # Fill the output grid, excluding blue pixels from the original input.
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            # Check if the pixel is within the bounds of the original input grid.
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
                # Check if this pixel was blue in the original input.
                if (r, c) not in blue_pixels:
                    # Calculate the corresponding indices in the output grid.
                    output_row = r - row_start
                    output_col = c - col_start
                    output_grid[output_row, output_col] = input_grid[r, c]

    return output_grid.tolist()