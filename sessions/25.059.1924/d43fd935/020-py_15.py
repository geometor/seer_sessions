"""
1. Preserve Green: Copy all green pixels from the input grid to the output grid.
2. Extend Blue Downward: For each blue pixel in the input grid, check the cell directly below it in the output grid.
3. White Below: If the cell below is white, set that cell to blue in the output grid.
"""

import numpy as np

def find_objects_by_color(grid, color):
    # Find coordinates of all pixels of the specified color.
    objects = []
    rows, cols = np.where(grid == color)
    for r, c in zip(rows, cols):
        objects.append((r, c))
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Preserve Green
    green_objects = find_objects_by_color(input_grid, 3)
    for r, c in green_objects:
        output_grid[r, c] = 3

    # Find blue objects.
    blue_objects = find_objects_by_color(input_grid, 1)

    # Extend blue pixels downwards.
    for r, c in blue_objects:
        # Check if within bounds and the cell below is white.
        if r + 1 < rows and output_grid[r + 1, c] == 0:
            output_grid[r + 1, c] = 1

    return output_grid