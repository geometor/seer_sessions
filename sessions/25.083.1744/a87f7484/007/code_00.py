"""
1.  **Initialization:** Create an empty 3x3 output grid filled with zeros.

2.  **Cross Search:** Iterate through all possible 3x3 subgrids within the input grid. For each 3x3 subgrid:

    a.  Check if the center pixel is non-zero. If not, continue to the next subgrid.

    b.  Let `color` be the value of the center pixel.

    c.  Check if the "cross" pattern exists:
        *   The center pixel, the pixel above, below, left, and right of the center must all have the value `color`.
        *   The four corner pixels (top-left, top-right, bottom-left, bottom-right) must all have the value 0.

    d. If the cross pattern criteria are met, copy the current 3x3 subgrid to the output grid and terminate the search.

3.  **Return:** Return the 3x3 output grid. This will be the first valid cross found, or a 3x3 grid of zeros if no cross is found.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through all possible 3x3 subgrids
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if center pixel is non-zero
            center_color = input_grid[r + 1, c + 1]
            if center_color == 0:
                continue

            # Check for cross pattern
            if (input_grid[r, c + 1] == center_color and
                input_grid[r + 2, c + 1] == center_color and
                input_grid[r + 1, c] == center_color and
                input_grid[r + 1, c + 2] == center_color and
                input_grid[r, c] == 0 and
                input_grid[r, c + 2] == 0 and
                input_grid[r + 2, c] == 0 and
                input_grid[r + 2, c + 2] == 0):

                # Copy 3x3 subgrid to output and return
                output_grid = input_grid[r:r+3, c:c+3].copy()
                return output_grid

    return output_grid