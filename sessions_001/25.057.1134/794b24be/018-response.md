# 794b24be • 018 • refine_coder

---
```python
"""
1.  **Identify Blue Pixels:** Locate all pixels in the `input_grid` with a value of '1' (blue).

2.  **Check Grid Dimensions:**
    *   If the input grid has an *even* number of columns, mirror each blue pixel across the Y-axis and change its color to '2' (red). The new column index for a blue pixel at column `c` is calculated as `number_of_columns - 1 - c`.
    * If the input grid has an *odd* number of columns, check the x coordinate.
      * If the blue pixel at column c where c == (number_of_columns-1)//2, change the pixel to red
      * Otherwise, do not change the input

3.  **Output:** Create an output grid where the transformed blue pixels (now red) are placed in their new positions, and all other pixels are '0' (white).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid to find blue pixels.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                # Check if the number of columns is even.
                if cols % 2 == 0:
                    # Mirror blue pixels across the Y axis and change to red.
                    new_c = cols - 1 - c
                    output_grid[r, new_c] = 2
                elif c == (cols - 1) // 2:
                    # change to red at the same position
                    output_grid[r,c] = 2
                else:
                    # copy unchanged
                    output_grid[r,c] = input_grid[r,c]
            else:
                # copy unchanged
                output_grid[r,c] = input_grid[r,c]

    return output_grid
```
