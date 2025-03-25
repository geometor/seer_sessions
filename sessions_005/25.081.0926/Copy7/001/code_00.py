"""
Iterate through each pixel in the input grid.
Identify target pixels with a value not equal to black (0).
Check the pixel to the right:
    If the pixel to the right is black (0):
        And if to the right of that black pixel there is an orange pixel (7) and the target pixel is green (3), change the black pixel (0) adjacent to green to green (3).
        And if to the right of that black pixel there is a blue pixel (1) and the target pixel is blue (2), change the black pixel (0) adjacent to blue to blue (1).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Identify Target: Find pixels with value not equal to black (0).
            if input_grid[r, c] != 0:
                # Check Neighbors: For the next pixel, to the right:
                if c + 1 < cols and input_grid[r, c+1] == 0:
                  # And if to the right of that black pixel (c+2)
                  if c + 2 < cols:
                    # there is an orange pixel (7) and the target pixel is green (3),
                    if input_grid[r,c+2] == 7 and input_grid[r,c] == 3:
                      # change the black pixel (0) adjacent to green to green (3).
                      output_grid[r, c+1] = 3
                    # there is a blue pixel (1) and the target pixel is blue (2),
                    if input_grid[r,c+2] == 1 and input_grid[r,c] == 2:
                      # change the black pixel (0) adjacent to blue to blue (1).
                      output_grid[r, c+1] = 1
    return output_grid