"""
The transformation rule identifies "seed" pixels (value 8, azure) in the input grid and expands them based on a specific geometric pattern. For each white (0) pixel in the output grid, it checks if any of the eight specific relative locations ((-1, -1), (-1, 1), (-2, 0), (2, 0), (0, -2), (0, 2), (1, -1), (1, 1)) relative to that pixel contains an azure pixel in the input grid. If any of them do, the white pixel becomes azure in the output grid.  Pixels that are already azure in the input remain azure.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the output grid.
    for r in range(rows):
        for c in range(cols):
            # If the pixel is already azure, it remains azure.
            if input_grid[r, c] == 8:
                continue

            # Check the eight specified relative locations.
            neighbors_to_check = [
                (r - 1, c - 1), (r - 1, c + 1),
                (r - 2, c), (r + 2, c),
                (r, c - 2), (r, c + 2),
                (r + 1, c - 1), (r + 1, c + 1)
            ]

            for nr, nc in neighbors_to_check:
                # Ensure the neighbor is within grid bounds.
                if 0 <= nr < rows and 0 <= nc < cols:
                    # If any of the specified neighbors are azure in the input, change the output pixel to azure.
                    if input_grid[nr, nc] == 8:
                        output_grid[r, c] = 8
                        break  # Once an azure neighbor is found, no need to check further.

    return output_grid