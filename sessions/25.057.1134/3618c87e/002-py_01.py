"""
The transformation rule is to swap the blue pixel (1) with the gray pixel (5) located two rows below it.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return as (row, col)
    return None

def transform(input_grid):
    """
    Swaps the blue pixel (1) with the gray pixel (5) located two rows below it.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the coordinates of the blue pixel (1)
    blue_coords = find_pixel(input_grid, 1)

    # If blue pixel is found, proceed with the swap
    if blue_coords:
        # Calculate the target coordinates for the swap (two rows below)
        target_row = blue_coords[0] + 2

        # Check if the target row is within the grid boundaries
        if target_row < output_grid.shape[0]:
            # Get current color at target.
            target_color = output_grid[target_row, blue_coords[1]]

            # perform the swap only if it is 5
            if target_color == 5:
                output_grid[target_row, blue_coords[1]] = 1
                output_grid[blue_coords[0], blue_coords[1]] = 5

    return output_grid