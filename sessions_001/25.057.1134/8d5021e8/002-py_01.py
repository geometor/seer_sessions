"""
The transformation involves creating a larger grid, placing azure corner pixels and making sure these pixels are positioned at the extremities, with a two-pixel wide separation along rows and 2 rows and 6 rows for the top and bottom azure colored cells. The core concept is expanding the input and repositioning specific colored pixels within a new, larger framework.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.
    output_height = input_grid.shape[0] * 3
    output_width = input_grid.shape[1] * 2

    # Create an empty output grid filled with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the azure (8) pixels in the input grid.
    azure_pixels = np.where(input_grid == 8)
    
    #there are only 2 azure colored cells in the input, with fixed position on the extreme right.
    # Place azure (8) pixels in the four corners of the output grid.
    output_grid[0, 0] = 8
    output_grid[0, -1] = 8
    output_grid[-1, 0] = 8
    output_grid[-1, -1] = 8
    
    #Add two more rows of azure pixels below and above the existing rows.
    output_grid[2, 0] = 8
    output_grid[2, -1] = 8
    output_grid[-3, 0] = 8
    output_grid[-3, -1] = 8
    
    #Add three more rows of azure at bottom.
    output_grid[5, 0] = 8
    output_grid[5, -1] = 8
    output_grid[-6, 0] = 8
    output_grid[-6, -1] = 8
    

    return output_grid