"""
Identifies azure (8) pixels in the input grid and connects each pair of azure pixels on the same row with a horizontal line of green (3) pixels.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def connect_pixels(grid, coord1, coord2, color):
    """Fills the space between two coordinates on the same row with a given color."""
    row = coord1[0]
    start_col = min(coord1[1], coord2[1])
    end_col = max(coord1[1], coord2[1])
    grid[row, start_col + 1:end_col] = color

def transform(input_grid):
    """Transforms the input grid by connecting azure pixels with green pixels."""
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find all azure pixels.
    azure_pixels = find_pixels_by_color(output_grid, 8)

    # Group azure pixels by row.
    pixels_by_row = {}
    for pixel in azure_pixels:
        row = pixel[0]
        if row not in pixels_by_row:
            pixels_by_row[row] = []
        pixels_by_row[row].append(pixel)

    # Connect azure pixels on the same row.
    for row, pixels in pixels_by_row.items():
        # Ensure there are at least two pixels in the row to connect.
        if len(pixels) >= 2:
            # Sort pixels by column to handle multiple pairs correctly
            pixels.sort(key=lambda x: x[1])
             #Iterate through pairs in current row
            for i in range(len(pixels) - 1):
                connect_pixels(output_grid, pixels[i], pixels[i+1], 3)


    return output_grid