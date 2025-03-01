# 6d0160f0 • 012 • refine_coder

---
```python
"""
1.  Check for Gray Pixels: Examine the entire input grid. If *any* pixel is gray (value 5), proceed to step 2. If *no* pixel is gray, preserve the entire input grid and skip the remaining steps.

2.  Identify Gray Columns: For each column, determine if it contains at least one gray pixel.

3.  Preserve or Replace: For each pixel in the input grid:
    *   If the pixel is gray, maintain its value in the output grid.
    *   If the pixel is *not* gray, and it is in a column identified in step 2 (a "gray column"), maintain its value in the output grid.
    *   Otherwise (if the pixel is not gray and not in a "gray column"), replace it with a gray pixel (value 5) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to check for the presence of any gray pixel
    def has_gray_pixel(grid):
        return np.any(grid == 5)

    # Helper function to identify columns containing gray pixels
    def get_gray_columns(grid):
        gray_columns = set()
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == 5:
                    gray_columns.add(c)
        return gray_columns

    # Check if any gray pixel exists (Step 1)
    if not has_gray_pixel(input_grid):
        return output_grid  # Preserve entire grid if no gray pixels

    # Identify gray columns (Step 2)
    gray_columns = get_gray_columns(input_grid)

    # Preserve or replace pixels (Step 3)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                continue  # Already gray, no change
            elif c in gray_columns:
                continue  # Non-gray in gray column, no change
            else:
                output_grid[r, c] = 5  # Replace with gray

    return output_grid
```

