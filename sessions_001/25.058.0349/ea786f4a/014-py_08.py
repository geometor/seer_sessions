"""
Finds the single white pixel in the input grid, then changes all pixels in its row and column to white.
"""

import numpy as np

def find_white_pixel(grid):
    # Find the coordinates of the white pixel (value 0)
    rows, cols = np.where(grid == 0)
    if len(rows) > 0:  # Check if a white pixel was found
        return rows[0], cols[0]
    return None  # Return None if no white pixel is found

def transform(input_grid):
    """
    Transforms the input grid by changing the color of pixels in the same row and column
    as the initial white pixel to white.
    """
    # Create a copy of the input grid to serve as the output grid
    output_grid = np.copy(input_grid)
    
    # Find the coordinates of the initial white pixel
    white_pixel_coords = find_white_pixel(input_grid)
    
    if white_pixel_coords:  # Proceed only if a white pixel was found
      row, col = white_pixel_coords

      # Change the entire row and column to white (0)
      output_grid[row, :] = 0
      output_grid[:, col] = 0

    return output_grid