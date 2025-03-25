"""
1.  **Identify Horizontal Color Changes:** Scan the input grid to find all pairs of horizontally adjacent pixels that have different colors, and where neither pixel is black (color 0).

2.  **Create and Position Green Bars:** For each group of *vertically stacked* horizontal color changes, create green (color 3) bars.
    *   The green bar starts *between* each horizontally adjacent, non-black, different-colored pixel pairs.
    *   The bar's top row is located *between* the rows of vertically stacked horizontal color changes.
    *   The bar's width is 2 pixels, aligned with the columns of the color-changing pixels.

3.  **Vertical Fill:** Extend the green bars downwards. If a horizontal color change does not have another directly below it, then fill the area below the horizontal color change with green, extending downwards to either another horizontal color change or the bottom of the grid.

4. No other changes occur. Copy any non-modified pixel from input to output grid.
"""

import numpy as np

def find_horizontal_changes(grid):
    """Finds pairs of horizontally adjacent pixels with different colors, excluding black."""
    changes = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 1):
            if grid[r, c] != grid[r, c + 1] and grid[r, c] != 0 and grid[r, c + 1] != 0:
                changes.append((r, c, c + 1))  # Store row and both column indices
    return changes

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find horizontal color changes
    changes = find_horizontal_changes(input_grid)

    # Group changes by columns
    column_groups = {}
    for r, c1, c2 in changes:
        if (c1, c2) not in column_groups:
            column_groups[(c1, c2)] = []
        column_groups[(c1, c2)].append(r)

    # Create and position green bars, and handle vertical fill
    for (c1, c2), row_list in column_groups.items():
        row_list.sort()
        for i in range(len(row_list)):
            start_row = row_list[i]

            if i+1 < len(row_list): # Another below
                fill_to_row = row_list[i+1]
            else:
                fill_to_row = rows

            if start_row+1 < rows: # avoid writing out of bounds
               output_grid[start_row + 1:fill_to_row, c1] = 3
               output_grid[start_row + 1:fill_to_row, c2] = 3

    return output_grid