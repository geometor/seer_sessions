"""
Duplicate some specific single pixels on the left of the leftmost position of the central azure object.
"""

import numpy as np

def find_object(grid, color):
    # find the object, assuming contiguous pixels of same color
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []
    return coords

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the azure object
    azure_coords = find_object(input_grid, 8)
    if not azure_coords.any():
        return output_grid  # No azure object, return original grid
    
    # find the leftmost coordinate
    leftmost_azure_x = min(coord[1] for coord in azure_coords)


    # Colors to duplicate and process
    colors_to_process = [6, 7, 3, 1, 2]

    for color in colors_to_process:
        color_coords = find_object(input_grid, color)
        if len(color_coords) >0:
            for coord in color_coords:
              #Duplicate some specific single pixels on the left of the leftmost position of the central azure object.
              output_grid[coord[0], leftmost_azure_x ] = color

    return output_grid