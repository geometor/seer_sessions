"""
For each green pixel in the input grid, create a vertical line of green pixels 
extending upwards to the top edge of the grid.  Other pixels remain unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all green pixels (color 3)
    green_pixel_coords = find_pixels_by_color(input_grid, 3)

    if len(green_pixel_coords) > 0:
        for green_pixel_coord in green_pixel_coords:
            # Get the column index of the current green pixel
            green_col = green_pixel_coord[1]

            # Iterate through rows above the green pixel, changing them to green
            for row in range(green_pixel_coord[0] - 1, -1, -1):
                output_grid[row, green_col] = 3

    return output_grid