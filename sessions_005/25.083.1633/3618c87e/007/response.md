```python
"""
1.  Identify: Find all blue (1) and gray (5) pixels in the input grid.
2.  Initial Placement:
    *   Move all blue pixels to the bottom row of the output grid, maintaining their original column.
    *   Move all gray pixels to the bottom row of the output grid, maintaining their original column. If a blue pixel is already in that position on the bottom row, the blue pixel remains (overwrites).
3.  Gray Pixel Adjustment: For each column that contains *both* a blue pixel and a gray pixel on the bottom row: move the gray pixel to the second-to-last row of the output grid, keeping its original column.
4.  Clear: Set all cells that are not on the bottom row or, when relevant, on the second-to-last row, to black (0).
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape
    bottom_row_index = rows - 1
    second_to_last_row_index = rows - 2

    # Initial Placement: Move blue (1) pixels to the bottom row
    blue_pixels = find_pixels_by_color(input_grid, 1)
    for r, c in blue_pixels:
        output_grid[bottom_row_index, c] = 1

    # Initial Placement: Move gray (5) pixels to the bottom row
    gray_pixels = find_pixels_by_color(input_grid, 5)
    for r, c in gray_pixels:
        if output_grid[bottom_row_index, c] != 1:
            output_grid[bottom_row_index, c] = 5

    # Gray Pixel Adjustment: Move gray pixels up one row if blue is present in the same column
    for c in range(cols):
        if output_grid[bottom_row_index, c] == 1:  # Blue is present in this column
            for r, c2 in gray_pixels:
                if c2 == c:
                    #Check to prevent index errors if input is 1xN
                    if second_to_last_row_index >= 0:
                        output_grid[second_to_last_row_index, c] = 5
                        # since it was on the bottom, clear it after move
                        output_grid[bottom_row_index,c] = 1


    return output_grid
```