"""
Preserve the Center: The central pixel of the input grid retains its original color in the output grid.

Checkerboard the Surroundings: All pixels adjacent to the center pixel are considered. 
Starting from the top-left corner of the input, alternate these pixels between 0 (white) and 1 (blue).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    #Preserve Center
    center_row = rows // 2
    center_col = cols // 2
    output_grid[center_row, center_col] = input_grid[center_row][center_col]


    #Checkerboard surrounding
    for i in range(rows):
        for j in range(cols):
            if (i,j) != (center_row, center_col): #Skip the center
                if (i + j) % 2 == 0: # Even sum, set to white (0)
                    output_grid[i,j] = 0

                else:   #Odd sum
                    output_grid[i, j] = 1

    return output_grid