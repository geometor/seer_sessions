"""
A diagonal line of green (3) pixels is drawn from the top-center of the grid downwards. 
The line shifts one column to the right in each subsequent row. 
The line stops when it is above the azure(8) pixels. The red(2) rectangle on the right and the azure(8) pixel on the bottom remains.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the azure pixels.
    azure_pixels = find_object_by_color(input_grid, 8)
    
    # Determine the stopping row for the green line (one row above the highest azure pixel).
    if azure_pixels.size > 0:
        stop_row = min(azure_pixels[:, 0]) -1 #min row index
    else:
        stop_row = rows
        
    # Starting column for the green line (approximately the center).
    start_col = cols // 2

    # Draw the diagonal green line.
    for row in range(min(stop_row,rows)):
      col = start_col + row
      if (col < cols):
        output_grid[row, col] = 3

    return output_grid