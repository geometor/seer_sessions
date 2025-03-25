"""
1.  **Grid Dimensions:** The output grid retains the same dimensions (height and width) as the input grid.
2.  **Fifth Column Rule:** If a cell in the 5th column (index 4) of the input grid is gray (value 5), change it to blue (value 1) in the output grid.
3. **Third and Seventh Column Rule:**
    * Examine each row.
        * If the row has a gray pixel in *both* the 3rd column (index 2) and the 7th column (index 6), change the 7th column pixel to red (value 2).
        * Otherwise, if the row has gray pixel in the 3rd column, change it to blue.
4.  **Preservation:** Any pixel not matching the above conditions remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through rows
    for i in range(rows):
        # Fifth Column Rule
        if cols > 4 and input_grid[i, 4] == 5:
            output_grid[i, 4] = 1

        # Third and Seventh Column Rule
        if cols > 6 and input_grid[i, 2] == 5 and input_grid[i, 6] == 5:
            output_grid[i, 6] = 2
        elif cols > 2 and input_grid[i, 2] == 5:
            output_grid[i, 2] = 1

    return output_grid