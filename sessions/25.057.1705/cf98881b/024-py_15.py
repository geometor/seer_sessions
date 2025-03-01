"""
1.  **Initialize:** Create a 4x4 output grid and fill it entirely with yellow (color 4).
2.  **Place Origin:** Place a black (color 0) pixel at the top-left corner (0, 0) of the output grid.
3.  **Input Row Iteration:** Iterate through each row of the input grid.
4. **Object Identification within Row:** In the current row, identify the positions of the blue (1) and maroon (9) pixels, if present.
5. **Conditional Placement in Output**
    *   If a blue pixel is found, place a blue pixel in the output grid at column 0 of the row number *below* the input pixel's row index.
    *    If a maroon pixel is found, place a maroon pixel in the output grid at column 1 of the row number *below* the input pixel's row index.
6. **Skip Yellow:** Ignore yellow pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid (step 1)
    output_grid = np.full((4, 4), 4, dtype=int)

    # Place origin (step 2)
    output_grid[0, 0] = 0

    # Input row iteration (step 3)
    for row_index, row in enumerate(input_grid):
        # Object identification within row (step 4)
        for col_index, pixel_value in enumerate(row):
            # Conditional placement in output (step 5)
            if pixel_value == 1:  # Blue pixel
                if row_index + 1 < 4: # boundary condition
                    output_grid[row_index + 1, 0] = 1
            elif pixel_value == 9:  # Maroon pixel
                if row_index + 1 < 4:  # boundary condition
                    output_grid[row_index + 1, 1] = 9
            # Skip yellow (step 6)

    return output_grid