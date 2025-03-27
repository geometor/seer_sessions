"""
1.  **Initialization:** Create an output grid with the same dimensions as the input grid, filled entirely with magenta (color code 6).

2.  **Locate Bottom-Right:** Scan the *input* grid to find the bottom-right-most pixel that is *not* magenta. Note the row and column coordinates of this pixel.

3.  **Determine 2x2 Color:** Examine the *output* grid. Find the color of the pixel at the row and column identified in Step 2. This will be the color of the 2x2 square.

4.  **Construct 2x2 Square:** Create a 2x2 square in the *output* grid.
    *   The bottom-right corner of this square is located at the row and column found in Step 2.
    *   All pixels within the 2x2 square have the color determined in Step 3.

5. **Fill Background:** Ensure that all other cells (those not part of the 2x2 block) remain magenta.
"""

import numpy as np

def find_bottom_right_non_background(grid, background_color=6):
    """Finds the bottom-right pixel that is not the background color."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != background_color:
                return r, c
    return None  # Should not reach here if there is at least one non-background pixel.

def transform(input_grid, output_grid): # Added output_grid as a parameter
    """Transforms the input grid according to the rule."""
    # 1. Initialization: Output grid filled with magenta.
    rows, cols = input_grid.shape
    transformed_grid = np.full((rows, cols), 6)

    # 2. Locate Bottom-Right non-magenta pixel in input_grid.
    bottom_right_coords = find_bottom_right_non_background(input_grid)

    if bottom_right_coords is not None:
        target_row, target_col = bottom_right_coords

        # 3. Determine 2x2 Color from output_grid.
        square_color = output_grid[target_row, target_col]

        # 4. Construct 2x2 Square.
        top_left_row = max(0, target_row - 1)
        top_left_col = max(0, target_col - 1)

        for r in range(top_left_row, min(rows, target_row + 1)):
            for c in range(top_left_col, min(cols, target_col + 1)):
                transformed_grid[r, c] = square_color

    # 5. Fill Background (already done in initialization).
    return transformed_grid