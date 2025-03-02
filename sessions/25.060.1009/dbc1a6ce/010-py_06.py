"""
Identify blue (1) pixels. For each blue pixel, change horizontally adjacent white (0) pixels to azure (8) until a non-white pixel or grid edge is encountered.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is blue (1)
            if output_grid[r, c] == 1:
                # Fill to the right
                for c_right in range(c + 1, cols):
                    if output_grid[r, c_right] == 0:
                        output_grid[r, c_right] = 8
                    else:
                        break  # Stop when encountering a non-white pixel

                # Fill to the left
                for c_left in range(c - 1, -1, -1):
                    if output_grid[r, c_left] == 0:
                        output_grid[r, c_left] = 8
                    else:
                        break  # Stop when encountering a non-white pixel

    return output_grid