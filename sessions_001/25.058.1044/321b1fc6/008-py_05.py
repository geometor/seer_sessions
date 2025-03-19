"""
1.  **Find Target:** Locate any 2x2 square within the input grid that has the following color pattern: orange (top-left), magenta (top-right), yellow (bottom-left), and maroon (bottom-right).
2.  **Duplicate Target:** If the target square is found, create two *copies* of it.
3.  **Position Copies:**
    *   Place the *first* copy at the bottom of the output grid. Align it horizontally (same x-coordinate) as the *original* square's top-left corner.
    *   Place the *second* copy at the bottom-right corner of the output grid.
4. **Remove Original**: remove the original target square.
5. **Copy Unchanged:** All other pixels in the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_target_square(grid):
    """Finds the 2x2 square with the target color pattern."""
    target_colors = (7, 6, 4, 9)  # orange, magenta, yellow, maroon
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c], grid[r, c+1], grid[r+1, c], grid[r+1, c+1]) == target_colors:
                return (r, c)  # Return top-left coordinates
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find Target
    target_location = find_target_square(input_grid)

    # Duplicate and Position, if found.
    if target_location:
        r, c = target_location

        # first copy - bottom, aligned x
        row_offset = output_grid.shape[0] - 2 - r
        output_grid[r + row_offset, c] = 7
        output_grid[r + row_offset, c + 1] = 6
        output_grid[r + 1 + row_offset, c] = 4
        output_grid[r + 1 + row_offset, c + 1] = 9

        # second copy - bottom right
        col_offset = output_grid.shape[1] - 2 - c
        output_grid[r + row_offset, c + col_offset] = 7
        output_grid[r + row_offset, c + 1 + col_offset] = 6
        output_grid[r + 1 + row_offset, c + col_offset] = 4
        output_grid[r + 1 + row_offset, c + 1 + col_offset] = 9

        # Remove original
        output_grid[r, c] = 0
        output_grid[r, c + 1] = 0
        output_grid[r + 1, c] = 0
        output_grid[r + 1, c + 1] = 0


    return output_grid