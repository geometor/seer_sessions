"""
The transformation rule observes the following:
1. White (0) pixels in the input remain unchanged.
2. Green (3) pixels are changed to azure (8) unless they are at the end of a contiguous horizontal line of green pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell
    for r in range(rows):
        for c in range(cols):
            # White pixels remain unchanged
            if input_grid[r, c] == 0:
                continue
            # Check for green pixels
            elif input_grid[r, c] == 3:
                # Check if it's the end of a contiguous horizontal line of green pixels
                if c == cols - 1 or input_grid[r, c + 1] != 3:
                    continue  # Remains green
                else:
                    output_grid[r, c] = 8  # Change to azure

    return output_grid