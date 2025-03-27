```python
"""
1.  **Iterate through every pixel:** Examine each cell in the input grid, one by one.
2.  **Check for Yellow:** If the current pixel is yellow (color 4), initiate the "Fill Down" process for that pixel's column.
3.  **Fill Down Process:** Starting from the yellow pixel, change all the white pixels (color 0) directly below it in the same column to yellow (color 4). Continue this downward filling until the bottom row of the grid is reached.
4. **Preserve all other colors.** If a cell is any color other than yellow, it is unchanged unless a yellow pixel above it in the same column triggers the fill-down, in which case, it can only be changed from white to yellow.
5. **Maintain Grid Dimensions.** Ensure that the transformation does not add or remove any rows or columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if the current pixel is yellow
            if input_grid[i][j] == 4:
                # Fill down process
                for k in range(i, rows):
                    if output_grid[k][j] == 0: # only fill if cell below is white.
                       output_grid[k][j] = 4

    return output_grid
```