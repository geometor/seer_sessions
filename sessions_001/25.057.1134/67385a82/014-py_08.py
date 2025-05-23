"""
Start with a 4x4 input grid containing pixels of colors white (0) and green (3).
All white (0) pixels in the input grid remain unchanged in the output grid.
All of the green pixels, except the pixel in the top right corner, are changed to azure (8).
top right green (3) pixel is unchaged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape
    
    # Find the top right corner coordinates
    top_right_corner = (0, cols - 1)

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Preserve white pixels (0)
            if input_grid[i, j] == 0:
                continue  # White pixels remain unchanged
            # Change green (3) to azure (8) except at top right corner
            elif input_grid[i, j] == 3:
                if (i, j) != top_right_corner:
                    output_grid[i, j] = 8  # Change to azure

    return output_grid