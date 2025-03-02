"""
1. Identify Non-Background Pixels: Find all pixels in the input grid that are *not* color 0 (black).
2. Preserve Non-Background: Copy these non-background pixels to the output grid.
3. Shrink Frame: The output grid is created by removing the outer layer of pixels from input grid resulting in dimensions of input_dimension - 2.
4. Relative Positioning: Maintain the relative positions of the non-background pixels within the reduced frame.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Calculate output grid dimensions
    output_rows = input_rows - 2
    output_cols = input_cols - 2

    # if output_rows or output_cols are invalid, return input
    if output_rows <= 0 or output_cols <= 0:
        return input_grid

    # Initialize output grid with background color (0)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input grid and copy non-background pixels
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] != 0:
                # Calculate corresponding position in output grid
                output_i = i - 1
                output_j = j - 1

                # Check if the position is within the output grid bounds
                if 0 <= output_i < output_rows and 0 <= output_j < output_cols:
                    output_grid[output_i, output_j] = input_grid[i, j]

    return output_grid