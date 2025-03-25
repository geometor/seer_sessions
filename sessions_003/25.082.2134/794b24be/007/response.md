```python
"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, initially filled with black (0) pixels.

2.  **Identify Top-Row Blue Pixels:** Locate all blue (1) pixels in the top row (row 0) of the input grid.

3.  **Determine Rectangle Width:**
    *   The leftmost edge of the rectangle corresponds to the leftmost column containing a blue pixel on the top row.
    *   The rightmost edge corresponds to the rightmost column with blue pixel on the top row.
    *   The width of the rectangle is the difference between the rightmost and leftmost blue pixel columns in the top row + 1.

4.  **Determine the presence of lower blue pixels:**
     * Iterate through all of the input grid below the top row.
     * Check for the presence of blue (1) pixels.

5.  **Determine Rectangle Height:**
     * If any other blue pixels are identified below row 0, the rectangle height is 2.
     * If there are no other blue pixels, the height of the rectangle is 1.

6.  **Create Red Rectangle:** Create a rectangle of red (2) pixels in the output grid.
    *   The rectangle always starts at row 0.
    *   The left and right edges, and therefore width, are determined in steps 3.
    * The height is defined in step 5

7.  **Clear Remaining Pixels:** (This is implicit in the initialization and rectangle creation, no separate action is needed). All pixels in the output grid that are not part of the red rectangle remain black (0).
"""

import numpy as np

def find_top_row_blue_pixels(grid):
    """Finds the column indices of blue pixels in the top row."""
    return np.where(grid[0, :] == 1)[0]

def check_for_lower_blue_pixels(grid):
    """Checks if there are any blue pixels below the top row."""
    rows, cols = grid.shape
    if rows > 1:
        return np.any(grid[1:, :] == 1)
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Find top-row blue pixels
    top_row_blue_pixels = find_top_row_blue_pixels(input_grid)

    # If no top-row blue pixels, return all-black grid
    if top_row_blue_pixels.size == 0:
        return output_grid

    # Determine rectangle width
    left_column = np.min(top_row_blue_pixels)
    right_column = np.max(top_row_blue_pixels)
    width = right_column - left_column + 1

    # Determine rectangle height
    if check_for_lower_blue_pixels(input_grid):
        height = 2
    else:
        height = 1

    # Create red rectangle in output grid
    output_grid[0:height, left_column:right_column + 1] = 2

    return output_grid
```