"""
The transformation moves a single-pixel object of either color 5 or 8 to a new location within the grid. The movement is always to row 3 (index 3). The column of the object, and the dimensions and color of the grid do not change. If no single-pixel object exists, or if the object is not color 5 or 8, the output is identical to the input.
"""

import numpy as np

def find_single_pixel_object(grid):
    """Finds a single-pixel object of color 5 or 8."""
    rows, cols = len(grid), len(grid[0])
    target_colors = [5, 8]
    found_pixel = None

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in target_colors:
                if found_pixel is None:
                    found_pixel = (r, c, grid[r][c])
                else:
                    return None  # More than one pixel found

    return found_pixel

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    rows, cols = len(input_grid), len(input_grid[0])
    output_grid = [row[:] for row in input_grid]  # Create a deep copy

    # Find single-pixel object
    pixel_info = find_single_pixel_object(input_grid)

    if pixel_info is None:
        return output_grid  # No transformation needed

    old_row, old_col, color = pixel_info

    # Move the pixel to row 3
    new_row = 3
    output_grid[old_row][old_col] = 0     # Clear the old position
    output_grid[new_row][old_col] = color  # Set the new position

    return output_grid