"""
Transforms a 3x3 input grid into a 9x9 output grid. Each pixel in the input
grid is expanded into a 3x3 block in the output grid. The color of the 3x3
block depends on the original color: Red(2) and Yellow(4) become
Green(3); Azure(8) becomes Red(2); otherwise, the color is copied.
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

            # Apply color transformation rules
            if color == 2:  # Red to Green
                color = 3
            elif color == 4:  # Yellow to Green
                color = 3
            elif color == 8: # Azure to Red
                color = 2
            

            # Expand each pixel to a 3x3 block
            for x in range(3 * i, 3 * i + 3):
              for y in range(3 * j, 3 * j + 3):
                output_grid[x,y] = color

    return output_grid