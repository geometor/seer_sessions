"""
Identifies azure (8) pixels in the input grid and changes some of them to blue (1) based on these rules:
1. If there is an adjacent 0 to the right, and no adjacent 8 to the left, change the pixel to 1.
2. If there is an adjacent 0 below, and no adjacent 8 above, change the pixel to 1.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is azure (8)
            if input_grid[r, c] == 8:
                # check for adjacent cells, handle grid edges
                left_is_8 = (c > 0) and (input_grid[r, c-1] == 8)
                right_is_0 = (c < cols - 1) and (input_grid[r, c+1] == 0)
                above_is_8 = (r > 0) and (input_grid[r-1, c] == 8)
                below_is_0 = (r < rows-1) and (input_grid[r+1, c] == 0)
                
                # Apply the replacement rules
                if right_is_0 and not left_is_8:
                    output_grid[r, c] = 1
                elif below_is_0 and not above_is_8:
                    output_grid[r,c] = 1

    return output_grid