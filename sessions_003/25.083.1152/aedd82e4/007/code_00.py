"""
1.  **Identify Red Pixels:** Find all pixels in the input grid that have a value of '2' (red).

2.  **Conditional Transformation:** For *each* identified red pixel:
    *   Check if it is the *bottom-most* red pixel within its column in the *original* input grid. If it is, change it to blue ('1') in the output grid.
    *   Check if it is the *right-most* red pixel within its row in the *original* input grid. If it is, change it to blue ('1') in the output grid.

3.  **Copy Other Pixels:** All other pixels (non-red) from the input grid should be copied directly to the output grid without modification.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all red pixel coordinates in the original input grid
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))

    # Apply the transformation rules based on the original input grid
    for r, c in red_pixels:
        # Check if it's the last red in its column in the original input
        last_red_in_col = True
        for r2 in range(r + 1, rows):
            if input_grid[r2, c] == 2:
                last_red_in_col = False
                break

        # Check if it's the last red in its row in the original input
        last_red_in_row = True
        for c2 in range(c + 1, cols):
            if input_grid[r, c2] == 2:
                last_red_in_row = False
                break

        # Change to blue in the output grid if either condition is met
        if last_red_in_col or last_red_in_row:
            output_grid[r, c] = 1

    return output_grid