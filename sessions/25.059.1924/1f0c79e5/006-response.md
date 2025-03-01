# 1f0c79e5 • 006 • refine_coder

---
```python
"""
1. **Locate Non-zero Pixel:** Find the coordinates (row, col) of a single non-zero pixel in the input grid. It doesn't matter which non-zero pixel if there are multiple; the first one found is sufficient.
2. **Center 3x3 Yellow Square:** Create a 3x3 square filled with yellow (4) pixels in the output grid. The center of this square should align with the row and column of the non-zero pixel found in step 1.  If the non-zero pixel is too close to the edge to center the square, the square should be placed adjacent to the edge, effectively "pushing" the square into the grid.
3. **Fill Background:** Fill the rest of the output grid with 0 (white).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by placing a 3x3 yellow square centered on a non-zero pixel.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the coordinates of a non-zero pixel
    non_zero_row, non_zero_col = -1, -1
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                non_zero_row, non_zero_col = i, j
                break  # Stop after finding the first non-zero pixel
        if non_zero_row != -1:
            break

    # If no non-zero pixel is found, return an all-zero grid
    if non_zero_row == -1:
        return output_grid

    # Calculate the top-left corner of the 3x3 square, ensuring it stays within bounds
    start_row = max(0, non_zero_row - 1)
    start_col = max(0, non_zero_col - 1)
    end_row = min(rows, start_row + 3)
    end_col = min(cols, start_col + 3)
    
    start_row = end_row - 3
    start_col = end_col -3

    # Create the 3x3 yellow square
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            output_grid[i, j] = 4

    return output_grid
```
