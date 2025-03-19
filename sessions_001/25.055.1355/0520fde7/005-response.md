# 0520fde7 • 005 • refine_coder

---
```python
"""
1.  **Identify Rows with Two Gray Pixels:** Iterate through each row of the input grid. If a row contains exactly two gray (5) pixels, note the row index and the column indices of those gray pixels.
2.  **Construct Output Rows:** Create a new output grid with the same height as the input grid, but with a fixed width of 3.
3.  **Fill Output:** For each row:
    *   If the row was identified in step 1 (contains two gray pixels): Place a single red (2) pixel in the output row at index 1. All other cells on this row will be 0.
    *   If the row was not identified in step 1: Fill the entire output row with black (0) pixels.
"""

import numpy as np

def find_gray_pixels(grid):
    # find rows with exactly two gray pixels
    gray_positions = []
    for r in range(grid.shape[0]):
        row = grid[r,:].flatten().tolist()
        if row.count(5) == 2:
            gray_positions.append((r, [i for i, x in enumerate(row) if x == 5]))
    return gray_positions

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height = input_grid.shape[0]
    output_grid = np.zeros((height, 3), dtype=int)

    # find the rows that have 2 gray pixels
    gray_positions = find_gray_pixels(input_grid)

    # change output pixels 
    for row_index, _ in gray_positions:
        output_grid[row_index, 1] = 2  # Place red pixel at the center column

    return output_grid
```
