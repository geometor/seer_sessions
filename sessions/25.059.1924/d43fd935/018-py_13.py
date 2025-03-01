"""
The transformation rule involves extending blue pixels downwards by one unit if the cell below is white,
and not already blue. Green objects and original blue pixels are preserved.
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

    # Find blue objects.
    blue_objects = find_objects_by_color(input_grid, 1)

    # Extend blue pixels downwards.
    for r, c in blue_objects:
        # Check if within bounds and the cell below is white and not blue.
        if r + 1 < rows and input_grid[r + 1, c] == 0 :
            output_grid[r + 1, c] = 1

    return output_grid