"""
1.  **Identify Objects:** Locate the contiguous block of green (3) pixels and the contiguous block of red (2) pixels.
2.  **Determine Azure Column Position:** Find the x-coordinate that is two positions to the left of the leftmost edge of the red shape.
3.  **Insert Azure Column:** Create a vertical column of azure (8) pixels at the determined x-coordinate. The height of this column matches the height of the input grid. All cells in this column become azure.
4. The other digits remain in their respective positions.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def find_leftmost_x(coords):
    # Find the minimum x-coordinate among the given coordinates.
    return np.min(coords[:, 1])

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the red object coordinates
    red_coords = find_object(input_grid, 2)
    if red_coords is None:
        return output_grid # or raise an exception

    # Determine the x-coordinate for the azure column
    red_leftmost_x = find_leftmost_x(red_coords)
    azure_x = red_leftmost_x - 2
    
    # Insert the azure column if azure_x >= 0. Check goes here to avoid index errors
    if azure_x >= 0:
      output_grid[:, azure_x] = 8  # Set all rows at azure_x column to 8

    return output_grid