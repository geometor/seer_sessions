"""
Transforms the input grid by changing the color of blue pixels (1) to red (2) 
if they are located at or below the vertical midpoint of the blue pattern.

The transformation follows these steps:
1. Find all blue pixels (1) in the input grid.
2. Determine the minimum and maximum row indices (vertical extent) occupied by these blue pixels.
3. Calculate a threshold row index based on the vertical midpoint: threshold_row = min_row + floor((max_row - min_row + 1) / 2).
4. Create a copy of the input grid.
5. Iterate through the blue pixels. If a blue pixel's row index is greater than or equal to the threshold row, change its color to red (2) in the copied grid.
6. Return the modified grid.
"""

import numpy as np
import math

def find_pixels_by_color(grid, color_value):
    """Finds the coordinates of all pixels with a specific color."""
    coords = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_value:
                coords.append((r, c))
    return coords

def transform(input_grid):
    """
    Applies the color transformation based on vertical position.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # 1. Identify the coordinates of all blue pixels (1)
    blue_pixel_coords = find_pixels_by_color(grid, 1)

    # 2. If no blue pixels are found, return the original grid
    if not blue_pixel_coords:
        return output_grid.tolist() # Return as list of lists

    # 3. Determine the minimum (min_row) and maximum (max_row) row indices
    rows = [r for r, c in blue_pixel_coords]
    min_row = min(rows)
    max_row = max(rows)

    # 4. Calculate the vertical midpoint threshold row
    # threshold_row defines the first row where pixels *will* be changed
    height_of_blue_pattern = max_row - min_row + 1
    threshold_row = min_row + math.floor(height_of_blue_pattern / 2)

    # 5. Iterate through all the identified blue pixel coordinates
    # 6. For each blue pixel, if its row index is >= threshold_row, change color to red (2)
    for r, c in blue_pixel_coords:
        if r >= threshold_row:
            output_grid[r, c] = 2

    # 7. Return the modified output grid as a list of lists
    return output_grid.tolist()