# 54d82841 • 006 • refine_coder

---
```python
"""
1.  **Identify Magenta Shapes:** Locate all contiguous blocks (shapes) of magenta (6) pixels within the input grid.
2.  **Determine Columns with Magenta:** Identify all columns that contain at least one magenta pixel, irrespective of the shape or row.
3. **Bottom Row Modification**: In the bottom row of the grid, change the color of *all* pixels that are in the columns identified in step 2 to yellow (4).
4.  **Preserve Other Pixels:** All other pixels in the grid remain unchanged.
"""

import numpy as np

def find_magenta_columns(grid):
    # Find all columns containing magenta pixels.
    rows, cols = grid.shape
    magenta_columns = set()
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == 6:
                magenta_columns.add(c)
                break  # Move to the next column once magenta is found
    return magenta_columns

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find columns containing magenta pixels
    magenta_columns = find_magenta_columns(input_grid)

    # Modify the bottom row based on magenta columns
    for c in range(cols):
        if c in magenta_columns:
            output_grid[rows - 1, c] = 4

    return output_grid
```

