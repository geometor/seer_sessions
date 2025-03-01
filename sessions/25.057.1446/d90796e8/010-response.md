# d90796e8 • 010 • refine_coder

---
```python
"""
1.  **Identify Rows:** Examine each row of the input grid.
2.  **Identify Green Rows**: Find any horizontal row containing one or more green (3) pixels.
3.  **Check for Vertical Adjacency:** For each green row identified, inspect the rows directly above and below it.
4.  **Conditional Row Transformation:** If *any* red pixel (2) is found in a vertically adjacent row (directly above or below any green pixel in the green row), change *all* green pixels (3) in that identified green row to azure (8).
5.  **Preserve Other Pixels:** All other pixels in the grid that are not part of a transformed green row retain their original values.
6.  **Output:** Create an output grid reflecting these changes.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for row_index in range(rows):
        row = input_grid[row_index]

        # Check if the row contains any green pixels (3)
        if 3 in row:
            # Check for vertically adjacent red pixels
            red_adjacent = False
            if row_index > 0:
                above_row = input_grid[row_index - 1]
                if 2 in above_row:
                    red_adjacent = True
            if row_index < rows - 1:
                below_row = input_grid[row_index + 1]
                if 2 in below_row:
                    red_adjacent = True

            # If red is vertically adjacent, change all greens in the row to azure
            if red_adjacent:
                for col_index in range(cols):
                    if output_grid[row_index, col_index] == 3:
                        output_grid[row_index, col_index] = 8

    return output_grid
```
