"""
Transforms the input grid based on the following rules applied row by row:
1. Initialize the output grid as an identical copy of the input grid.
2. Process each row of the input grid independently.
3. For the current row:
    a. Find all non-white pixels (value != 0). Record their colors and column indices.
    b. Count the number of non-white pixels found (`count`).
    c. If `count` is 0, proceed to the next row.
    d. Determine the set of unique non-white colors present in the row.
    e. Find the column index of the leftmost non-white pixel (`c_left`) and the rightmost non-white pixel (`c_right`).
    f. Check Fill Condition 1: If `count` is exactly 1:
        i. Get the color `C` of the single non-white pixel.
        ii. In the corresponding row of the output grid, change the color of all pixels from column `c_left` (the position of the single pixel) to the last column (inclusive) to color `C`.
    g. Check Fill Condition 2: If `count` is greater than 1 AND there is only one unique non-white color `C` in the row:
        i. In the corresponding row of the output grid, change the color of all pixels from column `c_left` to column `c_right` (inclusive) to color `C`.
    h. Otherwise (i.e., `count` > 1 and multiple different non-white colors exist), make no changes to this row in the output grid.
4. After processing all rows, return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based filling transformation to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find indices of non-white pixels in the current row
        # np.where returns a tuple, we need the first element (the array of indices)
        non_white_indices = np.where(input_grid[r] != 0)[0]
        num_non_white = len(non_white_indices)

        # Skip rows with no non-white pixels (Condition 3.c)
        if num_non_white == 0:
            continue

        # Get the colors of these pixels and unique colors (Condition 3.d)
        non_white_colors = input_grid[r, non_white_indices]
        unique_colors = np.unique(non_white_colors)

        # Get the leftmost and rightmost column indices (Condition 3.e)
        # np.where returns sorted indices, so min is first, max is last
        col_left = non_white_indices[0]
        col_right = non_white_indices[-1]

        # Case 1: Exactly one non-white pixel (Condition 3.f)
        if num_non_white == 1:
            # The color is the only unique color
            color = unique_colors[0]
            # Fill from this pixel's column to the right edge of the grid
            output_grid[r, col_left:] = color

        # Case 2: Multiple non-white pixels, BUT only one unique color (Condition 3.g)
        elif num_non_white > 1 and len(unique_colors) == 1:
            # The color is the single unique color
            color = unique_colors[0]
            # Fill between the leftmost and rightmost non-white pixels (inclusive)
            output_grid[r, col_left:col_right + 1] = color
        
        # Case 3: Multiple non-white pixels with different colors (Condition 3.h)
        # No action needed, the row remains as copied from the input

    # Return the modified grid (Step 4)
    return output_grid