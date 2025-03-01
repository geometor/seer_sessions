"""
Transforms a 3x3 input grid into a 9x9 output grid. Each pixel in the input
grid is expanded into a 3x3 block in the output grid.  If a pixel in the
input has color 2 (red), the corresponding 3x3 block in the output will have
color 3 (green). Otherwise, the color is directly copied.
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

            # Check for red (2) and replace with green (3)
            if color == 2:
                color = 3

            # Expand each pixel to a 3x3 block
            for x in range(3 * i, 3 * i + 3):
              for y in range(3 * j, 3*j + 3):
                output_grid[x,y] = color

    return output_grid