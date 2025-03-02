"""
The program performs a simple color substitution on the input grid. All instances of color 4 (yellow) are replaced with color 3 (green), and all instances of color 8 (azure) are replaced with color 9 (maroon). The grid dimensions remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the grid
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            # Change yellow (4) to green (3)
            if output_grid[row, col] == 4:
                output_grid[row, col] = 3
            # Change light blue/azure (8) to maroon (9)
            elif output_grid[row, col] == 8:
                output_grid[row, col] = 9

    return output_grid