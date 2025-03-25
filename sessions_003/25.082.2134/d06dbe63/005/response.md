```python
"""
1.  **Seed Identification:** Locate the single azure (8) pixel within the input grid. This pixel's position remains constant between the input and output.

2.  **Gray Region Initialization:**
    *   Place a gray (5) pixel directly to the right of the seed pixel.
    *   Place a gray (5) pixel directly below the seed pixel.

3.  **Gray Region Expansion (Two Directions)**
    * From the position below the seed, extend the grey region to the left.
    * From the position to the right of the seed, extend the grey region downwards

4.  **Diagonal Extension and adjacent pixels:**
    *   Starting from the gray pixel to the *right* of the seed pixel, extend gray pixels diagonally down and to the right, one pixel at a time, until the edge of the grid is reached (either bottom or right edge).
    *   Starting from the gray pixel *below* the seed pixel, extend gray pixels diagonally up and to the left, one pixel at a time, until the edge of the grid is reached (either top or left edge).

5. **Connect**: Connect the end of each line of pixels that were added to the
   grid - use the gray color.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    return (rows[0], cols[0]) if len(rows) > 0 else None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the seed (azure pixel) location.
    seed_location = find_seed(input_grid)
    if seed_location is None:
        return output_grid  # Return original if no seed is found

    seed_row, seed_col = seed_location

    # Keep seed
    output_grid[seed_row, seed_col] = 8

    # Gray Region Initialization
    if seed_col + 1 < width:
        output_grid[seed_row, seed_col + 1] = 5  # Right of seed
    if seed_row + 1 < height:
        output_grid[seed_row + 1, seed_col] = 5  # Below seed

    # Gray Region Expansion (Two Directions) and Diagonal Extension
    # Down and Right
    current_row, current_col = seed_row, seed_col + 1
    while current_row < height and current_col < width:
        output_grid[current_row, current_col] = 5
        current_row += 1
        current_col += 1
    down_right_end = (current_row -1, current_col - 1)

    # Up and Left
    current_row, current_col = seed_row + 1, seed_col
    while current_row >= 0 and current_row < height and current_col >= 0 and current_col < width :
        output_grid[current_row, current_col] = 5
        current_row += 1
        current_col -= 1

    up_left_end = (current_row-1, current_col+1)

    # connect
    start_row, start_col = down_right_end
    end_row, end_col = up_left_end

    if start_row > end_row:
      start_row, end_row = end_row, start_row
      start_col, end_col = end_col, start_col

    row_diff = end_row - start_row
    col_diff = end_col - start_col
    row_step = 0
    if row_diff > 0:
      row_step = 1
    col_step = 0
    if col_diff > 0:
      col_step = 1
    elif col_diff < 0:
      col_step = -1

    current_row = start_row
    current_col = start_col
    while current_row <= end_row or current_col != end_col:
      output_grid[current_row, current_col] = 5
      if current_row < end_row:
          current_row += row_step
      if current_col != end_col:
        current_col += col_step


    return output_grid
```