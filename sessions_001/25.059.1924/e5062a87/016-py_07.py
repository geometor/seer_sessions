"""
The program identifies specific white pixels adjacent to other white and red pixels, and changes their color to red. All other pixels remain the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels (0) to red (2) based on their adjacency to other white and red pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Identify white pixels (0)
            if input_grid[r, c] == 0:
                # look for conditions.
                change = False
                # Check for contiguous block of white to left
                if c > 0:
                    if input_grid[r,c-1] == 0:
                        change = True

                # check for a red pixel to right
                if c < cols -1:
                    if input_grid[r,c+1] == 2:
                        change = True
                
                if change:
                  output_grid[r,c] = 2

    return output_grid