```python
"""
1.  **Identify Initiating Blue Pixels:** Find all blue (1) pixels located in the top row (row 0) of the input grid.

2.  **Determine Affected Columns:** Identify all columns that contain at least one "Initiating Blue Pixel".

3.  **Determine the Bounding Rectangle:**
    *   The top row of the rectangle is always row 0.
    *   The left column of the rectangle is the leftmost column containing an Initiating Blue Pixel.
    *   The right column of the rectangle is the rightmost column containing an Initiating Blue Pixel.
    *   The bottom row is the lowest row containing any blue pixel within the Affected Columns, *or* the bottom row of the input grid if there are no other blue pixels besides the Initiating Blue Pixels.

4.  **Transform to Red Rectangle:** Create a rectangle of red (2) pixels. The dimensions and position of this rectangle are determined by the bounding rectangle calculated in step 3.

5. **Clear Remaining Pixels:** set every other pixel in the input grid to black (0).
"""

import numpy as np

def find_initiating_pixels(grid):
    # Find blue pixels in the top row
    top_row = grid[0, :]
    initiating_pixels = np.where(top_row == 1)[0]
    return initiating_pixels

def find_bottom_row(grid, affected_columns):
     # find lowest row with any blue
    rows, cols = grid.shape
    bottom_row = 0
    for col in affected_columns:
        for row in range(rows):
          if grid[row, col] == 1:
            bottom_row = max(bottom_row, row)
    if bottom_row == 0: # if there were NO blue pixels
      return rows -1  # default to last row
    else:
      return bottom_row

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Find initiating blue pixels (in top row)
    initiating_pixels = find_initiating_pixels(input_grid)

    # If no initiating pixels, return all-black grid
    if initiating_pixels.size == 0:
        return output_grid

    # Determine affected columns
    affected_columns = initiating_pixels

    # Determine bounding rectangle
    top_row = 0
    left_column = np.min(affected_columns)
    right_column = np.max(affected_columns)
    bottom_row = find_bottom_row(input_grid, affected_columns)


    # Create red rectangle
    output_grid[top_row:bottom_row+1, left_column:right_column+1] = 2

    return output_grid
```