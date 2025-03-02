"""
The input grid is conceptually divided into nine regions, forming a 3x3 meta-grid.  For each region, if it contains any red (2) pixels, the corresponding pixel in a 3x3 output grid is set to blue (1). Otherwise, the output pixel is set to white (0).  This creates a presence/absence map of red objects in the input.
"""

import numpy as np

def get_region_bounds(input_grid, row_index, col_index):
    """Calculates the row and column bounds for a region in the input grid."""
    rows, cols = input_grid.shape
    region_height = rows // 3
    region_width = cols // 3

    # Calculate start and end indices for rows and cols.  Handle edge cases where the grid
    # dimensions are not perfectly divisible by 3.
    row_start = row_index * region_height
    row_end = row_start + region_height
    if row_index == 2:  # Adjust the last row's endpoint
        row_end = rows

    col_start = col_index * region_width
    col_end = col_start + region_width
    if col_index == 2:  # Adjust the last column's endpoint.
        col_end = cols

    return row_start, row_end, col_start, col_end

def check_region_for_color(input_grid, row_start, row_end, col_start, col_end, color):
    """Checks if a specified color exists within a region of the input grid."""
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if input_grid[r, c] == color:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid into a 3x3 output grid indicating the presence of red pixels."""

    # Initialize the 3x3 output grid with all white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 meta-grid.
    for row_index in range(3):
        for col_index in range(3):
            # Get the bounds of the current region.
            row_start, row_end, col_start, col_end = get_region_bounds(input_grid, row_index, col_index)

            # Check if the region contains red (2) pixels.
            if check_region_for_color(input_grid, row_start, row_end, col_start, col_end, 2):
                output_grid[row_index, col_index] = 1  # Set to blue (1) if red is present.

    return output_grid