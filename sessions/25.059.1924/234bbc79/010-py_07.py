"""
The transformation removes the gray areas and expands the single blue to fill those gray spaces, without otherwise altering the Red and Green.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    
    # Find and Remove gray (5) pixels.
    gray_pixels = find_pixels_by_color(input_grid, 5)
    for x, y in gray_pixels:
        output_grid[x, y] = 0
        
    # Find the blue (1) pixel.
    blue_pixels = find_pixels_by_color(input_grid, 1)

    if len(blue_pixels) > 0:
        blue_x, blue_y = blue_pixels[0] #assuming a single blue

        #find the empty spots on the row
        row = output_grid[blue_x]
        empty_indices = np.where(row == 0)[0]

        #fill the empty spaces, adjacent to blue
        for x in empty_indices:
          if abs(x - blue_y) <= 2 : #fill to adjacent 0s on this row
            output_grid[blue_x,x] = 1


    return output_grid