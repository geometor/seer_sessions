"""
The input grid contains a single connected object composed of grey (5) pixels. This object is recolored with two colors, azure (8) and red (2), based on the position of pixels within the object. Red is assigned to the leftmost column(s) of the object, while azure fills the remaining area.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []  # Handle case where object is not found
    return coords

def get_leftmost_column(coords):
    # Find the minimum x-coordinate (column index).
    min_col = np.min(coords[:, 1])
    # Get all coordinates in the leftmost column.
    leftmost_coords = coords[coords[:, 1] == min_col]
    return leftmost_coords, min_col

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the primary object (grey pixels).
    object_coords = find_object(input_grid, 5)
    if not object_coords.any():
        return output_grid
    
    # Determine the leftmost column.
    leftmost_coords, min_col = get_leftmost_column(object_coords)

    # Color the leftmost column red.
    for row, col in leftmost_coords:
        output_grid[row, col] = 2
    
    #color the other columns azure
    for row, col in object_coords:
        if(col != min_col):
            output_grid[row, col] = 8

    return output_grid