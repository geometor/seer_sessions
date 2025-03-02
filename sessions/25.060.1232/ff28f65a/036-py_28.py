"""
The input grid is divided into nine regions, forming a 3x3 meta-grid. The output is a 3x3 grid.  If a region in the input grid contains red pixels (2), the corresponding cell in the output grid is blue (1).  If a region contains *only* orange (7) in the input, the output cell is white (0). If the region has *any* pixels that are not orange or red, and contains red in that region, it should output blue.
"""

import numpy as np

def get_region_bounds(input_grid, row_index, col_index):
    """Calculates the row and column bounds for a region in the input grid."""
    rows, cols = input_grid.shape
    region_height = rows // 3
    region_width = cols // 3
    row_start = row_index * region_height
    row_end = row_start + region_height
    if row_index == 2:
        row_end = rows
    col_start = col_index * region_width
    col_end = col_start + region_width
    if col_index == 2:
        col_end = cols
    return row_start, row_end, col_start, col_end

def check_region_for_colors(input_grid, row_start, row_end, col_start, col_end):
    """Checks a region for the presence of red and any other non-orange colors."""
    contains_red = False
    contains_non_orange_non_red = False

    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if input_grid[r, c] == 2:
                contains_red = True
            elif input_grid[r,c] != 7:
                contains_non_orange_non_red = True
    
    return contains_red, contains_non_orange_non_red

def transform(input_grid):
    """Transforms the input grid based on the presence of red and other colors."""

    # Initialize the 3x3 output grid with all white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 meta-grid.
    for row_index in range(3):
        for col_index in range(3):
            # Get the bounds of the current region.
            row_start, row_end, col_start, col_end = get_region_bounds(input_grid, row_index, col_index)

            # Check the region for red and other colors.
            contains_red, contains_non_orange_non_red = check_region_for_colors(input_grid, row_start, row_end, col_start, col_end)

            # Determine the output pixel value.
            if contains_red and not contains_non_orange_non_red:
                output_grid[row_index, col_index] = 1  # All red: Blue
            elif contains_red and contains_non_orange_non_red:
                 output_grid[row_index, col_index] = 1  # Mixed with red: Blue
            # default is white (0)

    return output_grid