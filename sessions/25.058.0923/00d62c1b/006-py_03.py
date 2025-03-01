"""
1.  **Identify Green Pixels:** Find all pixels in the input grid that are green (color value 3).
2.  **Change Color:** Change the color of each identified green pixel to yellow (color value 4).
3.  **Output:** Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is green.
            if output_grid[row, col] == 3:
                # Change the color to yellow
                output_grid[row, col] = 4

    return output_grid