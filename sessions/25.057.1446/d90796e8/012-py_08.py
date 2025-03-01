"""
1.  **Iterate through the grid:** Examine each pixel in the input grid.
2.  **Identify Green Pixels:** Locate all pixels that are green (value 3).
3.  **Check for Vertical Adjacency and Same Column:** For each green pixel, check for red pixels (value 2) in the *same column* in the rows *directly above and below*.
4.  **Conditional Transformation:** If a red pixel is found in the same column in either vertically adjacent row, change the green pixel to azure (value 8).
5. **Preserve All Other Pixels:** Any pixel that is not a green pixel meeting the condition in step 4 remains unchanged.
6.  **Output:** Create an output grid reflecting these changes.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for row_index in range(rows):
        for col_index in range(cols):
            # Identify green pixels
            if input_grid[row_index, col_index] == 3:
                # Check for red pixels in the same column above and below
                red_above = False
                red_below = False

                if row_index > 0 and input_grid[row_index - 1, col_index] == 2:
                    red_above = True
                if row_index < rows - 1 and input_grid[row_index + 1, col_index] == 2:
                    red_below = True

                # Conditional transformation: change to azure if red is present above or below
                if red_above or red_below:
                    output_grid[row_index, col_index] = 8

    return output_grid