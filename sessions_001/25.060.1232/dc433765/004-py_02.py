"""
The transformation involves moving the green object to the center and leaving the yellow object in place. All other positions are filled with white.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of a specific color in the grid.
    coords = np.argwhere(grid == color)
    return coords[0] if coords.size > 0 else None

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, then modify it.
    output_grid = np.zeros_like(input_grid)

    # Find the green object (color 3).
    green_coords = find_object(input_grid, 3)
    
    # Find the yellow object.
    yellow_coords = find_object(input_grid, 4)


    # Move the green object to the center (1, 1).
    if green_coords is not None:
        output_grid[1, 1] = 3

    # Keep yellow object at the original position.
    if yellow_coords is not None:
      output_grid[yellow_coords[0], yellow_coords[1]] = 4
    
    return output_grid