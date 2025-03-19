"""
Expand the grid, preserving the central azure square and green border, and filling in the new space with mostly white, and red in specific locations.
"""

import numpy as np

def get_objects_by_color(grid, color):
    """Finds objects of a specific color in the grid."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # Initialize output_grid (double the dimensions)
    output_grid = np.zeros((input_grid.shape[0] * 2, input_grid.shape[1] * 2), dtype=int)

    # Copy Azure Region
    azure_objects = get_objects_by_color(input_grid, 8)
    if len(azure_objects) > 0:
        min_row = np.min(azure_objects[:, 0])
        min_col = np.min(azure_objects[:, 1])
        
        for row in azure_objects:
            output_grid[row[0] + (min_row), row[1] + (min_col)] = 8


    # Copy Green Border
    green_objects = get_objects_by_color(input_grid, 3)
    if len(green_objects) > 0:
        for row in green_objects:
            output_grid[row[0] * 2, row[1] * 2] = 3
            output_grid[row[0] * 2 + 1, row[1] * 2] = 3
            output_grid[row[0] * 2, row[1] * 2 + 1] = 3
            output_grid[row[0] * 2+ 1, row[1] * 2+1] = 3

    # add red border
    output_grid[0, 0] = 2
    output_grid[0, 7] = 2
    output_grid[7, 0] = 2
    output_grid[7, 7] = 2

    return output_grid