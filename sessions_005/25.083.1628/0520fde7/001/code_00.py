"""
1.  **Initialization:** Create an output grid with the same dimensions as the input grid, initially filled with black (0) pixels.

2.  **Iteration:** For each pixel in the input grid, do the following:

    *   **Conditional Check:** examine value.
    *   If the pixel is gray (5), set the corresponding pixel in the output grid to red (2).
    *   If pixel is not gray(5) and is not black(0), change it to black(0)
    *   If the pixel is black (0) then leave it the same.

3.  **Output:** The output grid now represents the transformed image.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input, filled with black (0).
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # If the pixel is gray (5), set the corresponding output pixel to red (2).
            if input_grid[i, j] == 5:
                output_grid[i, j] = 2
            # if not gray or black, change to black
            elif input_grid[i,j] != 0:
                output_grid[i,j] = 0
            # else leave as black
            else:
                output_grid[i,j] = 0

    return output_grid