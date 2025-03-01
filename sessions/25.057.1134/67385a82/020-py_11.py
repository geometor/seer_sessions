"""
Replaces green (3) pixels in the input grid with azure (8) pixels based on these conditions:
1. If a green pixel is at the top-left corner, it's changed to azure.
2. Green pixels in the first two columns change to azure.
3. Other pixels, including white (0), remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)  # Create a copy to modify
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is green (3)
            if output_grid[r, c] == 3:
                # Check for the top-left corner condition
                # if r == 0 and c == 0:
                #    output_grid[r, c] = 8
                # Check if within first two cols
                if c < 2:
                    output_grid[r,c] = 8


    return output_grid