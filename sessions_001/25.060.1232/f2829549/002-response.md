# f2829549 • 002 • example_5 • investigate_coder

---
```python
"""
The input grid contains a vertical blue (1) stripe. The output grid is 3x3.
For each cell in the output grid, check the corresponding two rows in the input grid.
If there's an orange (7) pixel to the left of the blue stripe, or an orange pixel exactly 4 columns to the right of the blue stripe, in the corresponding input rows,
the output cell becomes green (3); otherwise, it's white (0). Two rows of input map to a single row of output.
"""

import numpy as np

def find_blue_stripe_column(grid):
    # Find the column index of the blue stripe (value 1).
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == 1):
            return j
    return -1  # Should not happen, but handle the case.

def transform(input_grid):
    # Initialize the output grid as a 3x3 array filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the column index of the blue stripe.
    blue_stripe_col = find_blue_stripe_column(input_grid)

    # Iterate through the output grid's rows.
    for r in range(3):
        # Corresponding input rows.
        input_row1 = r * 2
        input_row2 = r * 2 + 1

        # Check for orange (7) to the left of the blue stripe in both rows.
        if input_row1 < input_grid.shape[0]:
          for col in range(0,2):
            if input_grid[input_row1, col] == 7 :
              output_grid[r, col] = 3

        if input_row2 < input_grid.shape[0]:
          for col in range(0,2):
              if input_grid[input_row2, col] == 7:
                output_grid[r, col] = 3

        #check for orange pixel to the right of column
        if input_row1 < input_grid.shape[0] :
          if  blue_stripe_col + 4 < input_grid.shape[1] and input_grid[input_row1, blue_stripe_col + 4] == 7:
            output_grid[r,2] = 3
        if input_row2 < input_grid.shape[0]:
          if blue_stripe_col + 4 < input_grid.shape[1] and input_grid[input_row2, blue_stripe_col + 4] == 7:
            output_grid[r,2] = 3

    return output_grid
```
