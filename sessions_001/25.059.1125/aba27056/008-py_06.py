"""
1.  **Identify Magenta Shape:** Find all pixels in the input grid that are magenta (color 6).  These pixels form the "magenta shape."

2.  **Yellow Above:** For every magenta pixel in the magenta shape, if the pixel directly *above* it is white (color 0), change that white pixel to yellow (color 4).

3.  **Yellow Border:** Examine every pixel *adjacent* (up, down, left, or right, but *not diagonal*) to the magenta shape. If an adjacent pixel is white (color 0), change it to yellow (color 4).
"""

import numpy as np

def find_magenta_shape(grid):
    # Find coordinates of all magenta pixels
    magenta_coords = np.argwhere(grid == 6)
    return magenta_coords

def add_yellow_above(grid, magenta_coords):
    # Create a copy of the grid to modify
    new_grid = np.copy(grid)
    for r, c in magenta_coords:
        if r > 0 and grid[r-1, c] == 0:  # Check if pixel above is white
            new_grid[r-1, c] = 4  # Set to yellow
    return new_grid

def add_yellow_border(grid, magenta_coords):
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for r, c in magenta_coords:
        # Check adjacent pixels (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                new_grid[nr, nc] = 4  # Set adjacent white pixel to yellow
    return new_grid

def transform(input_grid):
    # Find the magenta shape
    magenta_coords = find_magenta_shape(input_grid)

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Add Yellow Above
    output_grid = add_yellow_above(output_grid, magenta_coords)

    # Add Yellow Border
    output_grid = add_yellow_border(output_grid, magenta_coords)
    
    return output_grid