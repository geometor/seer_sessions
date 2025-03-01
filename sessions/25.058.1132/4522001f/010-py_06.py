"""
Transforms a 3x3 input grid into a 9x9 output grid. Red (2) pixels are replaced with Green (3).
Each pixel in the input grid, is expanded into a 4x4 block in the output grid at position based on
input pixel location.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            color = input_grid[i, j]

            # Replace red (2) with green (3)
            if color == 2:
                color = 3

            # Expand each pixel to a 4x4 block
            for x in range(3 * i, 3 * i + 3):
              for y in range(3 * j, 3*j + 3):
                output_grid[x,y] = color
            

    return output_grid