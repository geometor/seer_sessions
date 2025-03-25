```python
"""
1.  **Initialization:** Make a copy of the input grid. This copy will be modified to create the output grid.

2.  **Iterate:** Go through each cell (pixel) of the input grid, row by row, and column by column.

3.  **Non-Gray Pixel Handling:** If the current pixel in the *input* grid is *not* gray (5), copy its value directly to the *output* grid at the same position.

4.  **Gray Pixel Processing:** If the current pixel in the *input* grid *is* gray (5), do the following:

    a. **Find Source Color:**
    *   **Left Scan:** Check cells to the *left* of the current cell, in the same row. Stop at the first cell that is *not* gray (5) and *not* zero (0). If found, this is the "source color".
    *   **Right Scan:** If no source color was found on the left, check cells to the *right* of the current cell, in the same row. Stop at the first cell that is *not* gray (5) and *not* zero (0). If found, this is the "source color".
    *  **Zero Assignment:** If no source color is found after checking both left and right, set the *output* grid's corresponding pixel to 0.

    b. **Propagate Source Color:** If a source color was found (in step 4a):
    *   Set the current pixel in the *output* grid (which was gray in the input) to the source color.
    *   Continue in the *same direction* (left or right) where the source color was found.
    *   Replace *only* pixels that were gray (5) in the *input* grid with the source color.
    *   **Stop Propagation:** Stop when you encounter:
        *   A pixel that was *not* gray (5) in the *input* grid (this includes 0).
        *   The edge of the grid.

5.  **Remove Zero Rows (Original Input Only):** After processing *all* pixels, examine the *input* grid. Identify any rows that contain *only* zeros. Remove these rows from the *output* grid. Rows in the output that contain zeros generated as part of the transformation process are *not* removed.

6.  **Output:** The modified copy of the input grid, after gray pixel processing and original zero-row removal, is the final output.
"""

import numpy as np

def _find_source_color(input_grid, row, col):
    """Finds the source color and direction for a gray pixel."""
    rows, cols = input_grid.shape
    # Left Scan
    for i in range(col - 1, -1, -1):
        if input_grid[row, i] != 5 and input_grid[row, i] != 0:
            return input_grid[row, i], -1  # -1: left
        if input_grid[row,i] == 0: # stop at zeros
            break
    # Right Scan
    for i in range(col + 1, cols):
        if input_grid[row, i] != 5 and input_grid[row, i] != 0:
            return input_grid[row, i], 1  # 1: right
        if input_grid[row, i] == 0:
            break

    return 0, 0  # No source color found


def _propagate_color(input_grid, output_grid, row, col, color, direction):
    """Propagates color in the given direction, stopping at non-gray or edge."""
    rows, cols = input_grid.shape
    current_col = col + direction

    while 0 <= current_col < cols:
        if input_grid[row, current_col] == 5:
            output_grid[row, current_col] = color
            current_col += direction
        else:
            break  # Stop propagation


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    input_grid_orig = np.copy(input_grid) # for checking original zero rows

    # iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Gray Pixel Processing
            if input_grid[r, c] == 5:
                # find source color and propogation direction
                source_color, direction = _find_source_color(input_grid, r, c)

                if source_color != 0:
                    # propagate the color in the output grid
                    output_grid[r, c] = source_color
                    _propagate_color(input_grid, output_grid, r, c, source_color, direction)
                else:
                    # set to zero of no source color
                    output_grid[r,c] = 0

            # Non-Gray Pixel Preservation (already handled by copying input_grid)

    # Remove Zero Rows (based on the original input grid)
    rows_to_keep = []
    for r in range(input_grid_orig.shape[0]):
        if np.any(input_grid_orig[r] != 0):  # only check original grid
            rows_to_keep.append(r)
    output_grid = output_grid[rows_to_keep]

    return output_grid
```