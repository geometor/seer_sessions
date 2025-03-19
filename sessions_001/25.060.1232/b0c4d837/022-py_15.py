"""
Extracts the azure (8) colored pixels from the input grid and places them into a new 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find azure (8) pixels
    azure_pixels = []
    for r_idx, row in enumerate(input_grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 8:
                azure_pixels.append((r_idx, c_idx))

    # Fill the output grid with azure pixels, row by row. stops when 3x3 grid is full.
    count = 0
    for r in range(3):
      for c in range(3):
        if count < len(azure_pixels):
            output_grid[r][c] = 8
            count +=1

    return output_grid