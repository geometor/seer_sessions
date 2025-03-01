"""
1.  **Output Grid Initialization:** Create a 3x3 output grid. Each cell will be filled based on the rules below.

2.  **Row-by-Row Processing:** Process each row of the input grid independently. The output grid's rows correspond directly to the input grid's rows.

3.  **All White Rule:** If *all* pixels in an input row are white (0), then fill the entire corresponding row in the output grid with red (2).

4.  **All Non-White Rule:** If *all* pixels in an input row are *not* white (i.e., all have values other than 0), then fill the entire corresponding row in the output grid with white (0).

5.  **Mixed Pixels Rule:** If a row contains a *mixture* of white and non-white pixels:
    *   If the mixed row is the *last* row of the input, fill the corresponding output row with magenta (6).
    *   Otherwise, if the mixed row is *not* the last row, fill the corresponding row with blue (1).

6. **Return:** The output is the resulting 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each row of the input grid
    for i, row in enumerate(input_grid):
        # Check if all pixels in the row are white (0)
        if np.all(row == 0):
            output_grid[i, :] = 2  # Fill corresponding output row with red (2)
        # Check if all pixels in the row are non-white
        elif np.all(row != 0):
            output_grid[i, :] = 0 # Fill the corresponding output row with white.
        # Handle mixed pixel cases
        elif i == input_grid.shape[0] - 1: # Last row
            output_grid[i,:] = 6 # magenta
        else: # Not the last row
            output_grid[i,:] = 1 # blue

    return output_grid