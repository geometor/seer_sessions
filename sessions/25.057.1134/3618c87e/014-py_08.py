"""
The input grid is vertically reflected. This means the top row becomes the bottom row, the second row becomes the second-to-last row, and so on.
As part of, or after, the reflection process, the colors are swapped based on the input color:
    *   If a pixel is blue (1) in the input, it becomes gray (5) in the output.
    *   If a pixel is gray (5) in the input, it becomes blue (1) in the output.
    *   If a pixel is white(0), it remains white (0)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # get height
    height = output_grid.shape[0]

    # Reflect vertically
    output_grid = np.flipud(output_grid)

    # Color swap
    for r in range(height):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] == 1:
                output_grid[r, c] = 5
            elif output_grid[r, c] == 5:
                output_grid[r, c] = 1

    return output_grid