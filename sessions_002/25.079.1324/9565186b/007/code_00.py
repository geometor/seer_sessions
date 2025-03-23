"""
1.  **Scan:** Examine each pixel in the input grid.
2.  **Locate Azure:** Identify all pixels that are color 8 (azure).
3.  **Row and Column Transformation:** For *each* pixel identified as azure:
    *   Iterate through all pixels in the *same row* as the azure pixel. If a pixel is not color 2 (red), change it to color 5 (grey).
    *   Iterate through all pixels in the *same column* as the azure pixel. If a pixel is not color 2 (red), change it to color 5 (grey).
4. **Output:** Create output grid, replacing those non-2 colors with 5.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid to locate Azure pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:  # Check for azure
                # Iterate through the row and change non-red pixels to grey
                for i in range(cols):
                    if output_grid[r, i] != 2:
                        output_grid[r, i] = 5
                # Iterate through the column and change non-red pixels to grey
                for j in range(rows):
                    if output_grid[j, c] != 2:
                        output_grid[j, c] = 5

    return output_grid