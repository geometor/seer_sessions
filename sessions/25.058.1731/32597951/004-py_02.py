"""
Replace blue pixels with green pixels if and only if the blue pixel is directly adjacent to an azure pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: Replace blue (1) pixels with green (3)
    if they are adjacent to an azure (8) pixel.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is blue (1)
            if input_grid[r, c] == 1:
                # Check for adjacent azure (8) pixels
                is_adjacent_to_azure = False
                # Check above
                if r > 0 and input_grid[r-1, c] == 8:
                    is_adjacent_to_azure = True
                # Check below
                if r < rows - 1 and input_grid[r+1, c] == 8:
                    is_adjacent_to_azure = True
                # Check left
                if c > 0 and input_grid[r, c-1] == 8:
                    is_adjacent_to_azure = True
                # Check right
                if c < cols - 1 and input_grid[r, c+1] == 8:
                    is_adjacent_to_azure = True

                # If adjacent to azure, change to green (3)
                if is_adjacent_to_azure:
                    output_grid[r, c] = 3

    return output_grid