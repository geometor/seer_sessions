"""
1.  **Input:** A grid of any size (input_grid) containing pixels of various colors.
2.  **Output:** A 3x3 grid (output_grid) initialized with all white (0) pixels.
3.  **Transformation Rule:**
    *   Consider only the top-left 3x3 region of the input grid.
    *   Iterate through each cell in the output_grid (from [0,0] to [2,2]).
    *   For each output grid coordinate (r_out, c_out), check if the corresponding *transposed* coordinate (c_out, r_out) in the *input_grid* contains a maroon (9) pixel.
    *  If the input grid contains a maroon (9) pixel, then set the output_grid cell to Red (2), otherwise, set the output grid cell to white(0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 3x3 filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each cell of the output grid
    for r_out in range(3):
        for c_out in range(3):
            # Check if corresponding transposed coordinate in input grid is within bounds and is maroon (9)
            if r_out < input_grid.shape[1] and c_out < input_grid.shape[0] and input_grid[c_out, r_out] == 9:
                output_grid[r_out, c_out] = 2  # Set output pixel to red (2)

    return output_grid