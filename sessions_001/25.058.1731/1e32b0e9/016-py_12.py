"""
1.  **Blue Pixel Expansion:**  Blue pixels initiate a full expansion of blue color both horizontally and vertically, covering the entire row and column they occupy.

2.  **Green Pixel Conditional Activation:** Green pixels *activate* the row they are on and the column they are on for potential blue filling.

3. **Green Pixel Vertical Expansion:** A green pixel will cause its *entire column* to be filled with blue *if and only if* there is at least one blue pixel anywhere below it in that column.

4. **Green Pixel Horizontal Expansion:**  A green pixel will cause its *entire row* to be filled with blue *if and only if* there is at least one blue pixel anywhere to the right of it in that row.

5. **Combining:** Where expansions from blue and green pixels overlap, the overlapping area remains blue. The fill color is always blue.

6. **Boundaries:** Expansions stop at the edges of the grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Find blue and green pixels
    blue_pixels = np.argwhere(input_grid == 1)
    green_pixels = np.argwhere(input_grid == 3)

    # 1. Blue Pixel Expansion: Fill entire row and column for each blue pixel.
    for r, c in blue_pixels:
        output_grid[r, :] = 1  # Fill row
        output_grid[:, c] = 1  # Fill column

    # 2. Green Pixel Conditional Activation and Expansion
    for r, c in green_pixels:
        # Vertical Expansion: Check for blue pixel below
        has_blue_below = False
        for row_below in range(r + 1, rows):
            if input_grid[row_below, c] == 1:
                has_blue_below = True
                break
        if has_blue_below:
            output_grid[:, c] = 1  # Fill entire column

        # Horizontal Expansion: Check for blue pixel to the right
        has_blue_right = False
        for col_right in range(c + 1, cols):
            if input_grid[r, col_right] == 1:
                has_blue_right = True
                break
        if has_blue_right:
            output_grid[r, :] = 1  # Fill entire row

    return output_grid