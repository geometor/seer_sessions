"""
Identifies azure (8) pixels in the input grid. For each row containing azure pixels, it finds the leftmost and rightmost azure pixels and fills the entire range between them (inclusive) with green (3) pixels.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def fill_row_between_columns(grid, row, col_start, col_end, color):
    """Fills a row segment between two column indices (inclusive) with a given color."""
    grid[row, col_start:col_end+1] = color

def transform(input_grid):
    """Transforms the input grid by filling the range between the leftmost and rightmost azure pixels on each row with green pixels."""
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

    # Fill the range between the extreme azure pixels on each row with green.
    for row, pixels in pixels_by_row.items():
        # Find the minimum and maximum column indices.
        columns = [pixel[1] for pixel in pixels]
        min_col = min(columns)
        max_col = max(columns)
        fill_row_between_columns(output_grid, row, min_col, max_col, 3)

    return output_grid