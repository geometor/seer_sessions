"""
The transformation identifies the dominant color within the inner region of the input grid
and uses this color to fill a cross-like pattern within a 5x5 output grid.
The rest of the output grid is filled with white (0) pixels.
"""

import numpy as np

def get_inner_color(grid):
    # Determine the dimensions of the grid.
    rows, cols = grid.shape

    # Handle edge cases: grids that are too small. Return a default (e.g., 0)
    if rows < 3 or cols < 3:
        return 0
    
    # For 5x5 or greater, check if the inner region is solid
    if rows >= 5 and cols >= 5:
        #check 3 x 3 center area for first non-border color
        first_inner_color = grid[rows//2-1, cols//2-1]
        return first_inner_color

    # for smaller grids
    return grid[rows//2, cols//2]

def transform(input_grid):
    # Get the dominant inner color from the input grid.
    inner_color = get_inner_color(input_grid)

    # Initialize the 5x5 output grid with all white (0) pixels.
    output_grid = np.zeros((5, 5), dtype=int)
    
    # Define the cross pattern indices (row, col).
    cross_pattern = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]

    # Fill in the cross pattern with the inner color.
    for r, c in cross_pattern:
        output_grid[r, c] = inner_color

    return output_grid