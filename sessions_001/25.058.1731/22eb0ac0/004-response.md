# 22eb0ac0 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the Special Row:** Scan the input grid to find the row where all other values are zero.
2.  **Get Non-Zero Values**: From the special row, save the value of all non-zero entries, moving from left to right, one entry at a time..
3.  **Fill Special Row in Output:** In the identified row, from the input, copy the color found on that to all positions on the same row in the output grid.
4. **Other Rows:** all other rows remain unchanged between input and output.
"""

import numpy as np

def find_special_row(grid):
    # Iterate through rows to find the one with all other values as zero
    for i, row in enumerate(grid):
        is_special = True
        for j, pixel in enumerate(row):
          if j%2 == 1 and pixel != 0:
            is_special = False
        if is_special:
            return i
    return -1  # Return -1 if no such row is found

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find special row
    special_row_index = find_special_row(input_grid)
    # print(special_row_index)

    if special_row_index != -1:
      # get special row
      special_row = input_grid[special_row_index]

      # replace output grid row pixels
      for i in range(len(special_row)):
        if special_row[i] != 0:
          output_grid[special_row_index] = np.full(len(special_row), special_row[i])


    return output_grid
```
