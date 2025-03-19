# 794b24be • 056 • example_10 • investigate_coder

---
```python
"""
1.  **Identify Blue Pixels:** Locate all pixels in the input grid with a value of 1 (blue).
2.  **Replace Blue with Red**: Change the value of all identified blue pixels (1) to 2 (red).
3.  **Bounding box:** Find the smallest rectangle that encompasses all of the 1s (blue).
4. **Replace Top Row** Replace the values in the output grid within this rectangle with 2 in the first row.
5.  **Retain Other Whites:** All other white pixels (0) in the input grid remain white (0) in the output grid.
"""

import numpy as np

def find_bounding_box(grid):
    # Find coordinates of all blue (1) pixels
    coords = np.argwhere(grid == 1)
    if coords.size == 0:
        return None  # Handle the case where there are no blue pixels

    # Find min and max row and column
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()

    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Initialize output grid with the same dimensions and all zeros
    output_grid = np.zeros_like(input_grid)

    # Find the bounding box of blue pixels
    bounding_box = find_bounding_box(input_grid)

    if bounding_box:
        (min_row, min_col), (max_row, max_col) = bounding_box

        # Replace the top row within the bounding box with red (2)
        output_grid[min_row, min_col:max_col+1] = 2

        # change the blue in input to red in the output
        for r in range(min_row, max_row+1):
          for c in range(min_col, max_col+1):
            if input_grid[r,c] == 1:
              output_grid[r,c] = 2


    return output_grid
```
