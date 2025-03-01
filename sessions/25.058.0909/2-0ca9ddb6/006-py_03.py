"""
1.  **Identify Red Pixels:** Locate all red (value 2) pixels within the input grid.

2.  **Red Transformation:** For each red pixel, change all directly adjacent (up, down, left, right) white (value 0) pixels to yellow (value 4).

3.  **Identify Blue Pixels:** Locate all blue (value 1) pixels within the input grid.

4.  **Blue Transformation:** For each blue pixel, change all directly adjacent (up, down, left, right) white (value 0) pixels to orange (value 7).

5. **Order of transformation:** The order of transformation is important, perform the red transformation first, then the blue transformation.

6. **Preservation:** Pixels that are not white and adjacent to either red or blue, are not modified. Yellow and orange pixels do not propogate changes.
"""

import numpy as np

def find_pixels(grid, color_value):
    # Find the coordinates of pixels with the specified color value.
    return np.array(np.where(grid == color_value)).T.tolist()

def transform(input_grid):
    """Transforms the input grid based on red and blue pixel locations."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find red (2) and blue (1) pixels
    red_pixels = find_pixels(input_grid, 2)
    blue_pixels = find_pixels(input_grid, 1)

    # Define adjacent offsets (up, down, left, right)
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Transform around red pixels
    for r, c in red_pixels:
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = 4

    # Transform around blue pixels
    for r, c in blue_pixels:
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = 7

    return output_grid