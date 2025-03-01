# 1f85a75f • 006 • refine_coder

---
```python
"""
1.  **Locate:** Find the 2x2 green square within the input grid. Record its top-left corner coordinates (row, col).
2.  **Determine Output Dimensions:**
    *   The output grid always has 3 columns.
    *   The output grid's number of rows is determined by the green square's row coordinate in the input grid.  Specifically, the number of output rows is equal to the input green square's row index + 1.
3.  **Construct:** Create an output grid with the determined dimensions, initially filled with black (or white, doesn't matter for this rule since it is overwritten).
4. **Populate the green pixels:**
    * Place the 2x2 green square from input to the output, with the top-left at (0,0)
    * Add a green pixel to each output row at column 2.
"""

import numpy as np

def find_green_square(grid):
    # Find the coordinates of a 2x2 square of green (3) pixels.
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 3 and grid[i + 1, j] == 3 and
                grid[i, j + 1] == 3 and grid[i + 1, j + 1] == 3):
                return (i, j)
    return None

def transform(input_grid):
    # Find the green square
    green_square_coords = find_green_square(input_grid)
    if green_square_coords is None:
        return None # Should not happen based on problem description

    row_start, _ = green_square_coords

    # Determine output dimensions
    num_rows = row_start + 1
    num_cols = 3

    # Initialize output_grid
    output_grid = np.zeros((num_rows, num_cols), dtype=int)


    # Place the 2x2 green square in the output grid, top-left at (0, 0).
    output_grid[0:2, 0:2] = 3
    
    # Fill the right most column with green
    for i in range(num_rows):
      output_grid[i,2] = 3

    return output_grid
```
