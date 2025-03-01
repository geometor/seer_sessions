"""
The input grid contains gray borders, red "plus" shapes, and blue "plus" shapes.
The transformation rule involves changing the color of one of the blue plus shapes
located on the inner area of the grid, inside the border, to red (2), while keeping all other elements the same.
"""

import numpy as np

def find_plus_shapes(grid, color):
    """
    Finds all "plus" shaped objects of a specified color in the grid.
    Returns a list of center coordinates of the plus shapes.
    """
    plus_centers = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == color and
                grid[r - 1, c] == color and
                grid[r + 1, c] == color and
                grid[r, c - 1] == color and
                grid[r, c + 1] == color):
                plus_centers.append((r, c))
    return plus_centers

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find all blue plus shapes within grid.
    blue_plus_centers = find_plus_shapes(input_grid, 1)

    # Check to see that the blue plus shape is not on the borders.
    rows, cols = input_grid.shape
    valid_blue_plus_centers = []

    for r,c in blue_plus_centers:
        if 1 <= r < rows - 1 and 1 <= c < cols - 1:
            valid_blue_plus_centers.append((r,c))
    
    # If any blue plus shapes exist within the border, change one to red.
    if valid_blue_plus_centers:
        center_r, center_c = valid_blue_plus_centers[0]  # Change only the first one
        output_grid[center_r, center_c] = 2
        output_grid[center_r - 1, center_c] = 2
        output_grid[center_r + 1, center_c] = 2
        output_grid[center_r, center_c - 1] = 2
        output_grid[center_r, center_c + 1] = 2

    return output_grid