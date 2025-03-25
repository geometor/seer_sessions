"""
Iterate through each cell of the input grid.
Identify all '2' (red) pixels.
For each '2' (red) pixel:
    If the pixel to the *right* is a '0' (white), change it to a '4' (yellow) in the output grid.
    If the pixel *below* is a '0' (white), change it to a '4' (yellow) in the output grid.
Copy any pixels not changed to a 4, including all the original 2's, to the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Identify '2' (red) pixels
            if input_grid[r, c] == 2:
                # Check the pixel to the right
                if c + 1 < cols and input_grid[r, c + 1] == 0:
                    output_grid[r, c + 1] = 4
                # Check the pixel below
                if r + 1 < rows and input_grid[r + 1, c] == 0:
                    output_grid[r + 1, c] = 4

    return output_grid