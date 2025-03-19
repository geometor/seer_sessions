"""
Locate the single white pixel (color 0) within the input grid. If found, change its color to blue (color 1) if it is surrounded by 4 gray pixels, otherwise change it to red (color 2). If no white pixel or multiple white pixels are found, the output is identical to the input.
"""

import numpy as np

def find_white_pixel(grid):
    # Find the coordinates of all white pixels (color 0).
    white_pixels = np.where(grid == 0)
    # If exactly one white pixel is found, return its coordinates.
    if len(white_pixels[0]) == 1:
        return white_pixels[0][0], white_pixels[1][0]
    else:
        return None

def count_surrounding_gray_pixels(grid, row, col):
    # Count the number of gray pixels surrounding the given pixel.
    count = 0
    for i in range(max(0, row - 1), min(grid.shape[0], row + 2)):
        for j in range(max(0, col - 1), min(grid.shape[1], col + 2)):
            if (i, j) != (row, col) and grid[i, j] == 5:
                count += 1
    return count

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the single white pixel.
    white_pixel_location = find_white_pixel(input_grid)

    # If a single white pixel is found, change its color.
    if white_pixel_location:
        row, col = white_pixel_location
        # Count surrounding gray pixels.
        gray_count = count_surrounding_gray_pixels(input_grid, row, col)
        # Change color based on surrounding gray pixel count.
        if gray_count == 4:
            output_grid[row, col] = 1  # Change to blue
        else:
            output_grid[row, col] = 2  # Change to red

    return output_grid