"""
1.  **Find the Gray Column:** Identify the vertical column in the input grid where all pixels are gray (value 5).
2.  **Calculate Offset:** Calculate the offset of this gray column's index from the center column index of the input grid. (Center column index = input_width // 2).
3.  **Create Output Grid:** Initialize a 3x3 output grid filled with white pixels (value 0).
4.  **Place Red Pixels:**
    *   If the offset is 0 (gray column is in the center of input):
        *   Place a red pixel (value 2) at row 1, column = offset.
        *   Place another red pixel as follows, based on the example:
            * If output[1,0] is occupied: place at row 2, column 2
            * If output[0,1] is occupied: place at row 1, column 2

    *   If the offset is not zero. (Further examples are needed to establish this rule, none given).

5. **Return output grid.**

"""

import numpy as np

def find_gray_column(grid):
    """Finds the index of the column containing all 5s."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen in these examples

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the gray column index
    gray_column_index = find_gray_column(input_grid)

    # Calculate the offset from center
    center_column_index = input_grid.shape[1] // 2
    offset = gray_column_index - center_column_index

    # Place red pixels based on offset.
    if offset == 0:
        # Place first red pixel
        output_grid[1, 1 + offset] = 2

        # Place the second based on which one occupied
        if output_grid[1,0] == 2:
             output_grid[2,2] = 2
        elif output_grid[0,1]==2:
            output_grid[1,2]=2
        else:
             output_grid[2,2] = 2

    return output_grid